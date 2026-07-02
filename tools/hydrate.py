#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# -----------------------------
# Utilities
# -----------------------------

_HTTP_RX = re.compile(r"^HTTP\s+(\d{3})\b")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha512_hex(data: bytes) -> str:
    return hashlib.sha512(data).hexdigest()


def hard_halt(msg: str) -> None:
    print(f"HARD HALT: {msg}", file=sys.stderr)
    sys.exit(2)


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_token_from_file(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            tok = f.read().strip()
            return tok or None
    except Exception:
        return None


def get_github_token(args: argparse.Namespace) -> Optional[str]:
    """
    Token resolution order:
      1) --token
      2) $GITHUB_TOKEN
      3) --token-file
      4) $GITHUB_TOKEN_FILE
    """
    if getattr(args, "token", None):
        tok = str(args.token).strip()
        return tok or None

    env_tok = os.environ.get("GITHUB_TOKEN")
    if env_tok and env_tok.strip():
        return env_tok.strip()

    token_file = getattr(args, "token_file", None) or os.environ.get("GITHUB_TOKEN_FILE")
    if token_file:
        return read_token_from_file(token_file)

    return None


def is_github_raw(uri: str) -> bool:
    return uri.startswith("https://raw.githubusercontent.com/")


def fetch_bytes(uri: str, timeout: int = 20, token: Optional[str] = None) -> Tuple[int, bytes]:
    """
    Fetch bytes from a URI.

    GitHub Raw behavior notes:
      - Private raw can return 404 when unauthenticated.
      - Some raw/CDN edges can return 404 when Authorization is present for *public* files.
        (Observed via curl 200 while urllib+Authorization yields 404.)

    Policy:
      - If token is provided and uri is GitHub raw:
          1) try with Authorization
          2) if HTTP 404, retry once WITHOUT Authorization
      - Otherwise: normal fetch without auth.
    """

    def _do_request(with_auth: bool) -> Tuple[int, bytes]:
        headers = {"User-Agent": "zervan-hydrator/1.3"}
        if with_auth and token and is_github_raw(uri):
            headers["Authorization"] = f"Bearer {token}"

        req = Request(uri, headers=headers)
        with urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            data = resp.read()
            return int(status), data

    try:
        if token and is_github_raw(uri):
            try:
                return _do_request(with_auth=True)
            except HTTPError as e:
                if e.code == 404:
                    # Retry once without auth for public/CDN weirdness
                    return _do_request(with_auth=False)
                raise RuntimeError(f"HTTP {e.code}") from e

        return _do_request(with_auth=False)

    except HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}") from e
    except URLError as e:
        raise RuntimeError(f"URL error: {e.reason}") from e
    except Exception as e:
        raise RuntimeError(f"Fetch error: {e}") from e


# -----------------------------
# Visibility Index (non-assertive)
# -----------------------------

_PATH_RX = re.compile(
    r"\b(?:Accelerator|DoctrineOps|Doctrine|Observers|Observer|Modules|Module|Contracts|Contract|schema|Schemas)/[A-Za-z0-9._/\-]+\b"
)


def extract_inventory_candidates(text: str) -> Dict[str, List[str]]:
    """
    Extract path-like tokens from INVENTORY content.
    This does NOT assert semantics; it only reports what the inventory *mentions*.

    Buckets are heuristic by prefix for convenience only.
    """
    paths = sorted(set(_PATH_RX.findall(text)))
    buckets: Dict[str, List[str]] = {
        "observers": [],
        "modules": [],
        "contracts": [],
        "doctrine": [],
        "other": [],
    }

    for p in paths:
        if p.startswith(("Observers/", "Observer/")):
            buckets["observers"].append(p)
        elif p.startswith(("Modules/", "Module/")):
            buckets["modules"].append(p)
        elif p.startswith(("Contracts/", "Contract/")):
            buckets["contracts"].append(p)
        elif p.startswith(("Doctrine/", "DoctrineOps/")):
            buckets["doctrine"].append(p)
        else:
            buckets["other"].append(p)

    return buckets


def build_visibility_index(receipt: Dict[str, Any], artifacts_bytes: Dict[str, bytes]) -> Dict[str, Any]:
    """
    Build a minimal visibility index from hydrated artifacts.
    - Uses INVENTORY.md bytes if present.
    - Does NOT infer existence beyond what inventory text mentions.
    """
    inv_art = None
    for a in receipt.get("artifacts", []):
        if a.get("name") == "INVENTORY.md" or str(a.get("uri", "")).endswith("/INVENTORY.md"):
            inv_art = a
            break

    inv_uri = inv_art.get("uri") if inv_art else None
    inv_sha = inv_art.get("sha512") if inv_art else None
    inv_bytes = artifacts_bytes.get(inv_uri) if inv_uri else None

    visibility: Dict[str, Any] = {
        "version": "zervan://accelerator/hydration_visibility_index/1",
        "generated_at": utc_now_iso(),
        "inventory": {
            "uri": inv_uri,
            "sha512": inv_sha,
            "byte_length": inv_art.get("byte_length") if inv_art else None,
        },
        "candidates": {
            "observers": [],
            "modules": [],
            "contracts": [],
            "doctrine": [],
            "other": [],
        },
        "notes": [
            "Visibility index is derived by extracting path-like tokens from INVENTORY.md.",
            "This index does not assert existence/eligibility semantics; it reports only what INVENTORY text mentions.",
        ],
    }

    if inv_bytes:
        text = inv_bytes.decode("utf-8", errors="replace")
        visibility["candidates"] = extract_inventory_candidates(text)

    return visibility


# -----------------------------
# CLI / Profile parsing
# -----------------------------

def maybe_validate_receipt(
    receipt: Dict[str, Any],
    receipt_schema_uri: str,
    timeout: int,
) -> Optional[str]:
    """
    Validate receipt against the schema at receipt_schema_uri.
    Returns None on success, or an error message string on failure.

    IMPORTANT:
      - Schema fetch is performed WITHOUT Authorization headers.
      - Validation must be globally reproducible.
    """
    try:
        import jsonschema  # type: ignore
    except Exception:
        return "jsonschema not installed; cannot validate receipt. Install with: pip install jsonschema"

    status, schema_bytes = fetch_bytes(
        receipt_schema_uri,
        timeout=timeout,
        token=None,  # 🔒 CRITICAL
    )

    if status != 200:
        return f"schema fetch failed: HTTP {status}"

    try:
        schema = json.loads(schema_bytes.decode("utf-8", errors="replace"))
    except Exception as e:
        return f"schema parse failed: {e}"

    try:
        jsonschema.validate(instance=receipt, schema=schema)
    except Exception as e:
        return f"schema validation failed: {e}"

    return None


def collect_items(profile: Dict[str, Any], include_groups: List[str]) -> List[Dict[str, Any]]:
    """
    Build the enumerated item list: required + selected optional groups.
    Adds a 'required' boolean per item (True for required list, False for optional groups).
    """
    items: List[Dict[str, Any]] = []

    required = profile.get("required", [])
    if not isinstance(required, list) or not required:
        hard_halt("profile.required missing or empty")

    for it in required:
        if not isinstance(it, dict) or "uri" not in it or "name" not in it:
            hard_halt("profile.required contains invalid item (must include name, uri)")
        items.append({"required": True, **it})

    if include_groups:
        optional_groups = profile.get("optional_groups", [])
        name_to_group: Dict[str, Dict[str, Any]] = {}
        for g in optional_groups:
            if isinstance(g, dict) and "group" in g:
                name_to_group[str(g["group"])] = g

        for gname in include_groups:
            if gname not in name_to_group:
                hard_halt(f"optional group not found in profile: {gname}")
            grp = name_to_group[gname]
            for it in grp.get("items", []):
                if not isinstance(it, dict) or "uri" not in it or "name" not in it:
                    hard_halt(f"optional group '{gname}' contains invalid item (must include name, uri)")
                items.append({"required": False, **it})

    return items


def _parse_http_status_from_error(err: str) -> Optional[int]:
    """
    Best-effort: extract HTTP status code from error strings like 'HTTP 404'.
    """
    m = _HTTP_RX.match(err.strip())
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def maybe_validate_receipt(
    receipt: Dict[str, Any],
    receipt_schema_uri: str,
    timeout: int,
) -> Optional[str]:
    """
    Validate receipt against the schema at receipt_schema_uri.
    Returns None on success, or an error message string on failure.

    Requires jsonschema installed. If missing, returns an error message.

    IMPORTANT:
      - Receipt schema fetch is performed WITHOUT Authorization headers.
      - Schema validation must be globally reproducible (cache-stable).
    """
    try:
        import jsonschema  # type: ignore
    except Exception:
        return "jsonschema not installed; cannot validate receipt. Install with: pip install jsonschema"

    # Fetch schema WITHOUT AUTH (critical fix)
    status, schema_bytes = fetch_bytes(receipt_schema_uri, timeout=timeout, token=None)
    if status != 200:
        return f"schema fetch failed: HTTP {status}"

    try:
        schema = json.loads(schema_bytes.decode("utf-8", errors="replace"))
    except Exception as e:
        return f"schema parse failed: {e}"

    try:
        jsonschema.validate(instance=receipt, schema=schema)
    except Exception as e:
        return f"schema validation failed: {e}"

    return None


def _enforce_uniqueness(items: List[Dict[str, Any]]) -> None:
    """
    Fail closed if duplicate URIs or duplicate names exist in the enumerated set.
    (Duplicates create ambiguous receipts and can hide partial fetch behavior.)
    """
    uris = [str(it.get("uri", "")) for it in items]
    names = [str(it.get("name", "")) for it in items]

    dup_uris = sorted({u for u in uris if u and uris.count(u) > 1})
    dup_names = sorted({n for n in names if n and names.count(n) > 1})

    if dup_uris:
        hard_halt(
            f"duplicate uri entries in profile enumeration: {dup_uris[:10]}{'...' if len(dup_uris) > 10 else ''}"
        )
    if dup_names:
        hard_halt(
            f"duplicate name entries in profile enumeration: {dup_names[:10]}{'...' if len(dup_names) > 10 else ''}"
        )


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    args = parse_args()
    profile = load_json(args.profile_path)

    # Enforce fail-closed + no discovery
    if profile.get("no_discovery") is not True:
        hard_halt("profile.no_discovery must be true")
    if profile.get("default") != "FAIL_CLOSED":
        hard_halt("profile.default must be FAIL_CLOSED")

    # Resolve token (if any)
    token = get_github_token(args)

    if args.require_auth and not token:
        hard_halt("authentication required but no token resolved (set GITHUB_TOKEN or use --token/--token-file)")

    # Binding stamp (post-hydration)
    binding_profiles = profile.get("binding_profiles", {})
    bind = binding_profiles.get(args.binding_profile)
    if not isinstance(bind, dict):
        hard_halt(f"binding_profiles missing entry: {args.binding_profile}")

    authority_enabled = bool(bind.get("authority_enabled", False))
    promotion_allowed = bind.get("promotion_allowed", False)
    conflict_behavior = bind.get("conflict_behavior", None)

    # Enumerate allowed fetches (no crawl proof)
    items = collect_items(profile, args.include_optional_group)

    # Enforce uniqueness for unambiguous receipts
    _enforce_uniqueness(items)

    enumerated_uri_set = [str(it["uri"]) for it in items]
    enumerated_allow = set(enumerated_uri_set)

    fetched_uri_set: List[str] = []
    unauthorized_fetches: List[str] = []
    artifacts: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []

    # Keep bytes for optional index
    artifacts_bytes: Dict[str, bytes] = {}

    # Fetch ONLY enumerated URIs
    for it in items:
        name = str(it["name"])
        uri = str(it["uri"])
        required_flag = bool(it["required"])
        pinned = it.get("pinned_sha512", None)

        # Guardrail: any attempt outside allowlist is a violation
        if uri not in enumerated_allow:
            unauthorized_fetches.append(uri)
            continue

        # Record attempted URI (even if it fails)
        fetched_uri_set.append(uri)

        try:
            http_status, data = fetch_bytes(uri, timeout=args.timeout, token=token)
            if http_status != 200:
                raise RuntimeError(f"HTTP {http_status}")

            digest = sha512_hex(data)

            if pinned is not None and pinned != digest:
                raise RuntimeError("pinned_sha512 mismatch")

            artifacts_bytes[uri] = data

            artifacts.append(
                {
                    "name": name,
                    "uri": uri,
                    "required": required_flag,
                    "status": "PASS",
                    "http_status": http_status,
                    "sha512": digest,
                    "byte_length": len(data),
                    "retrieved_at": utc_now_iso(),
                    "pinned_sha512": pinned,
                    "error": None,
                }
            )

        except Exception as e:
            err_s = str(e)
            inferred_http = _parse_http_status_from_error(err_s)

            artifacts.append(
                {
                    "name": name,
                    "uri": uri,
                    "required": required_flag,
                    "status": "FAIL",
                    "http_status": inferred_http,  # best-effort
                    "sha512": None,
                    "byte_length": None,
                    "retrieved_at": None,
                    "pinned_sha512": pinned,
                    "error": err_s,
                }
            )
            failures.append({"name": name, "uri": uri, "error": err_s})

    # Fail-closed overall status
    overall_status = "PASS"
    if unauthorized_fetches:
        overall_status = "HARD_HALT"
    if any(a.get("required") is True and a.get("status") == "FAIL" for a in artifacts):
        overall_status = "HARD_HALT"

    receipt_schema_uri = profile.get("receipt_schema_uri", None)

    receipt: Dict[str, Any] = {
        "hydration_surface_version": profile.get("hydration_surface_version", "UNKNOWN"),
        "binding_profile_selected": args.binding_profile,
        "authority_enabled": authority_enabled,
        "promotion_allowed": promotion_allowed,
        "conflict_behavior": conflict_behavior,
        "no_discovery": True,
        "transport": {
            "repo": profile.get("transport_repo"),
            "auth": {
                "token_present": bool(token),
                "auth_required": bool(args.require_auth),
                "mechanism": "GITHUB_TOKEN_BEARER" if token else "NONE",
            },
        },
        "overall_status": overall_status,
        "enumerated_uri_set": enumerated_uri_set,
        "fetched_uri_set": fetched_uri_set,
        "unauthorized_fetches": unauthorized_fetches,
        "artifacts": artifacts,
    }

    if failures:
        receipt["failures"] = failures

    # Optional schema validation (fail-closed if requested)
    if args.validate_receipt:
        if not receipt_schema_uri:
            receipt["receipt_validation"] = {
                "status": "FAIL",
                "error": "receipt_schema_uri missing from profile",
            }
            receipt["overall_status"] = "HARD_HALT"
        else:
            err = maybe_validate_receipt(receipt, str(receipt_schema_uri), timeout=args.timeout)
            if err:
                receipt["receipt_validation"] = {
                    "status": "FAIL",
                    "error": err,
                    "schema_uri": str(receipt_schema_uri),
                    "notes": [
                        "Receipt schema fetch performed without Authorization headers for cache-stable verification."
                    ],
                }
                receipt["overall_status"] = "HARD_HALT"
            else:
                receipt["receipt_validation"] = {
                    "status": "PASS",
                    "schema_uri": str(receipt_schema_uri),
                    "notes": [
                        "Receipt schema fetch performed without Authorization headers for cache-stable verification."
                    ],
                }

    # Optional visibility index sidecar
    if args.emit_visibility_index:
        vis = build_visibility_index(receipt, artifacts_bytes)
        with open(args.emit_visibility_index, "w", encoding="utf-8") as vf:
            vf.write(json.dumps(vis, indent=2) + "\n")

    out_json = json.dumps(receipt, indent=2)

    if args.out == "-" or args.out.strip() == "":
        print(out_json)
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out_json + "\n")

    sys.exit(0 if receipt.get("overall_status") == "PASS" else 2)


if __name__ == "__main__":
    main()
