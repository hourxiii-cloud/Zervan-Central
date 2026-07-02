#!/usr/bin/env python3
"""
Zervan envelope validator (fail-closed).

Validates:
  1) canonicalization.version matches expected
  2) canonical bytes are reproducible (JSON canonicalization)
  3) signed_hash matches SHA-512(canonical_bytes)
  4) signature verifies (ECDSA) over either:
       - digest bytes, or
       - canonical bytes
     depending on --signature-scope
  5) optional: JSON Schema validation with schema fetched WITHOUT auth headers

Notes:
- This script uses RFC 8785-style JSON canonicalization via python's json module
  with strict sorting and separators. If your Zervan compiler uses a different
  canonicalization, swap canonical_json_bytes() accordingly.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import urllib.request
from typing import Any, Dict, Optional

def canonical_json_bytes(obj: Any) -> bytes:
    """
    Deterministic JSON bytes. If your canonicalization differs, replace this.
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

def sha512_hex(b: bytes) -> str:
    return hashlib.sha512(b).hexdigest()

def fetch_bytes_no_auth(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={})
    # IMPORTANT: no Authorization header
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))

def load_public_key_pem(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def verify_signature(public_key_pem: bytes, data: bytes, sig_b64: str) -> None:
    """
    ECDSA verify. Requires cryptography.
    """
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.exceptions import InvalidSignature
    except Exception as e:
        raise RuntimeError(
            "cryptography is required for signature verification. Install: pip install cryptography"
        ) from e

    pub = serialization.load_pem_public_key(public_key_pem)
    sig = base64.b64decode(sig_b64)

    # Assumption: ECDSA with SHA-512 over provided data.
    # If your policy uses SHA-256, change hashes.SHA512() accordingly.
    try:
        pub.verify(sig, data, ec.ECDSA(hashes.SHA512()))
    except InvalidSignature as e:
        raise ValueError("signature verification failed") from e

def validate_schema(manifest: Dict[str, Any], schema_url: str, timeout: int) -> None:
    try:
        import jsonschema  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "jsonschema is required for schema validation. Install: pip install jsonschema"
        ) from e

    schema_bytes = fetch_bytes_no_auth(schema_url, timeout=timeout)
    schema = json.loads(schema_bytes.decode("utf-8"))
    jsonschema.validate(instance=manifest, schema=schema)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="Path to envelope/manifest JSON")
    ap.add_argument("--public-key", required=True, help="Path to PEM public key")
    ap.add_argument("--expected-canon-version", default="zervan://crypto/canonicalization/envelope/1")
    ap.add_argument("--signature-scope", choices=["digest", "canonical_bytes"], default="digest",
                    help="What the signature is over per your policy")
    ap.add_argument("--schema-url", default=None, help="Optional schema URL (fetched WITHOUT auth)")
    ap.add_argument("--timeout", type=int, default=20)
    args = ap.parse_args()

    manifest = load_json(args.manifest)

    canon = manifest.get("canonicalization", {})
    canon_version = canon.get("version")
    if canon_version != args.expected_canon_version:
        print(f"FAIL: canonicalization.version mismatch: got {canon_version!r}", file=sys.stderr)
        return 2

    # Canonicalize the envelope. Many systems canonicalize the entire manifest.
    # If your policy canonicalizes only a subset, change this selection.
    canon_bytes = canonical_json_bytes(manifest)
    digest_hex = sha512_hex(canon_bytes)
    digest_bytes = hashlib.sha512(canon_bytes).digest()

    crypto = manifest.get("crypto", {})
    signed_hash = crypto.get("signed_hash")
    if not isinstance(signed_hash, str) or len(signed_hash) != 128:
        print("FAIL: crypto.signed_hash missing or not SHA-512 hex", file=sys.stderr)
        return 2

    if signed_hash.lower() != digest_hex.lower():
        print("FAIL: signed_hash does not match SHA-512(canonical_bytes)", file=sys.stderr)
        print(f"  expected: {digest_hex}", file=sys.stderr)
        print(f"  got:      {signed_hash}", file=sys.stderr)
        return 2

    sig_b64 = crypto.get("signature_b64") or crypto.get("signature")
    if not isinstance(sig_b64, str) or not sig_b64.strip():
        print("FAIL: signature missing (crypto.signature_b64)", file=sys.stderr)
        return 2

    pub_pem = load_public_key_pem(args.public_key)

    if args.signature_scope == "digest":
        verify_data = digest_bytes
    else:
        verify_data = canon_bytes

    try:
        verify_signature(pub_pem, verify_data, sig_b64)
    except Exception as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 2

    if args.schema_url:
        try:
            validate_schema(manifest, args.schema_url, args.timeout)
        except Exception as e:
            print(f"FAIL: schema validation failed: {e}", file=sys.stderr)
            return 2

    print("PASS: envelope validation succeeded")
    print(f"  canonicalization.version: {canon_version}")
    print(f"  sha512(canonical_bytes):  {digest_hex}")
    print(f"  signature_scope:          {args.signature_scope}")
    if args.schema_url:
        print(f"  schema_url:               {args.schema_url} (fetched w/o auth)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
