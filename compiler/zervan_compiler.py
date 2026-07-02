from __future__ import annotations

import base64
import hashlib
import json
import unicodedata
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Tuple

# ---- Canonicalization (envelope_v1.md) ----

class CanonicalizationError(Exception):
    pass


def _nfc_string(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def _normalize(obj: Any) -> Any:
    """
    Recursively:
      - NFC normalize strings
      - ensure all decimals in signed scope are NOT represented as JSON floats
      - preserve arrays order
      - preserve null vs missing (handled by caller)
    """
    if obj is None:
        return None
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int):
        return obj
    if isinstance(obj, float):
        # Hard fail: signed scope forbids binary float ambiguity.
        raise CanonicalizationError("Float found in signed scope. Use string or fixed-point int.")
    if isinstance(obj, Decimal):
        # If you parsed JSON decimals into Decimal, only allow integers.
        if obj != obj.to_integral_value():
            raise CanonicalizationError("Non-integer Decimal found in signed scope. Use string or fixed-point int.")
        return int(obj)
    if isinstance(obj, str):
        return _nfc_string(obj)
    if isinstance(obj, list):
        return [_normalize(x) for x in obj]
    if isinstance(obj, dict):
        # Sort keys lexicographically by Unicode code point
        normalized_items = []
        for k, v in obj.items():
            if not isinstance(k, str):
                raise CanonicalizationError("Non-string JSON object key encountered.")
            nk = _nfc_string(k)
            nv = _normalize(v)
            normalized_items.append((nk, nv))
        normalized_items.sort(key=lambda kv: kv[0])
        return {k: v for k, v in normalized_items}
    raise CanonicalizationError(f"Unsupported JSON type for canonicalization: {type(obj).__name__}")


def canonical_json_bytes(envelope_obj: Dict[str, Any]) -> bytes:
    """
    Canonical JSON:
      - UTF-8
      - no BOM
      - minimal separators
      - sorted keys (recursively)
      - NFC strings
      - arrays preserved
      - forbid floats (unless they are strings, which is fine)
    """
    normalized = _normalize(envelope_obj)
    canonical_str = json.dumps(
        normalized,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True  # safe even after our sorting; reinforces determinism
    )
    return canonical_str.encode("utf-8")


def sha512_id(data: bytes) -> str:
    return "sha512:" + hashlib.sha512(data).hexdigest()


# ---- Signing helpers (RSA-PSS-SHA512 and ECDSA-SHA512) ----

@dataclass(frozen=True)
class SignatureResult:
    alg: str
    signer_key_id: str
    signature_b64: str


def key_id_from_public_key_spki_der(public_spki_der: bytes) -> str:
    return sha512_id(public_spki_der)


def sign_sha512_digest(
    digest64: bytes,
    alg: str,
    private_key_pem: bytes,
) -> Tuple[SignatureResult, bytes]:
    """
    Signs the *raw* 64-byte SHA-512 digest bytes (not the hex string).
    Returns (SignatureResult, public_spki_der)
    """
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec, padding, utils
    except Exception as e:
        raise RuntimeError(
            "cryptography package is required. Install it in your environment."
        ) from e

    priv = serialization.load_pem_private_key(private_key_pem, password=None)

    # Extract SPKI for key_id
    pub = priv.public_key()
    public_spki_der = pub.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    signer_key_id = key_id_from_public_key_spki_der(public_spki_der)

    if alg == "RSA-PSS-SHA512":
        signature = priv.sign(
            digest64,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=hashes.SHA512().digest_size,
            ),
            utils.Prehashed(hashes.SHA512()),
        )
    elif alg == "ECDSA-SHA512":
        signature = priv.sign(
            digest64,
            ec.ECDSA(utils.Prehashed(hashes.SHA512())),
        )
    else:
        raise ValueError(f"Unsupported alg: {alg}")

    return SignatureResult(
        alg=alg,
        signer_key_id=signer_key_id,
        signature_b64=base64.b64encode(signature).decode("ascii"),
    ), public_spki_der


# ---- Public API: sign manifest ----

def sign_manifest(manifest: Dict[str, Any], private_key_pem: bytes, alg: str = "ECDSA-SHA512") -> Dict[str, Any]:
    """
    Mutates the manifest by adding:
      - crypto.signed_hash
      - crypto.signatures[0]
    Requires manifest.canonicalization.signature_scope == "full_envelope" per your schema v1.1.0.
    """
    # Canonicalize + hash full manifest
    canonical = canonical_json_bytes(manifest)
    signed_hash = sha512_id(canonical)

    # Sign raw digest bytes
    digest64 = hashlib.sha512(canonical).digest()
    sig, _public_spki_der = sign_sha512_digest(digest64=digest64, alg=alg, private_key_pem=private_key_pem)

    manifest.setdefault("crypto", {})
    manifest["crypto"]["signed_hash"] = signed_hash
    manifest["crypto"].setdefault("signatures", [])
    manifest["crypto"]["signatures"] = [{
        "role": "engine",
        "alg": sig.alg,
        "signer_key_id": sig.signer_key_id,
        "signature_b64": sig.signature_b64
    }]

    return manifest


def load_json_no_float(path: str) -> Dict[str, Any]:
    """
    Loads JSON but parses floats into Decimal so we can reject non-integers deterministically.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, parse_float=Decimal)
