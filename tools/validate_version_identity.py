#!/usr/bin/env python3

from pathlib import Path
import argparse
import json
import re
import subprocess
import sys

TOKEN_RE = re.compile(
    r"\b(?:"
    r"vTemporal\.(?:39|40|41|42)(?:[._]\d+){0,3}"
    r"|v(?:39|40|41|42)(?:[._]\d+){0,3}"
    r")\b"
)

TEXT_SUFFIXES = {
    ".md", ".json", ".py", ".txt", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".sh"
}

SCAN_EXCLUDE = {
    "VERSION_REFERENCES.json",
    "tools/validate_version_identity.py",
    "tools/regenerate_version_references.py",
    "tests/test_version_identity.py",
}

ACTIVE_VERSION_DECLARATION_SURFACES = {
    "VERSION",
    "VERSION.json",
}

def classify(token, native_version):
    normalized = token.replace("_", ".")
    if normalized == native_version:
        return "CURRENT_NATIVE_VERSION"
    if normalized.startswith("v41.1"):
        return "CANDIDATE_BRIDGE_HISTORY"
    if normalized.startswith("vTemporal.39") or normalized.startswith("v39"):
        return "HISTORICAL_V39"
    if normalized.startswith("vTemporal.40") or normalized.startswith("v40"):
        return "HISTORICAL_V40"
    if normalized == "v41" or normalized.startswith("v41.0") or normalized.startswith("vTemporal.41"):
        return "HISTORICAL_V41"
    if normalized == "v42" or normalized.startswith("v42.0") or normalized.startswith("vTemporal.42"):
        return "CURRENT_V42_FAMILY"
    return "REVIEW_REQUIRED"

def git_files(root):
    result = subprocess.check_output(
        [
            "git", "-C", str(root),
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        text=True
    )
    return sorted(set(filter(None, result.splitlines())))

def scan(root, native_version):
    entries = []

    for rel in git_files(root):
        if rel in SCAN_EXCLUDE:
            continue

        path = root / rel

        if not path.is_file():
            continue

        if path.name != "VERSION" and path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            for match in TOKEN_RE.finditer(line):
                token = match.group(0)
                entries.append({
                    "path": rel,
                    "line": line_no,
                    "token": token,
                    "classification": classify(token, native_version),
                })

    return sorted(
        entries,
        key=lambda x: (x["path"], x["line"], x["token"])
    )

def validate(root):
    errors = []

    version_path = root / "VERSION"
    json_path = root / "VERSION.json"
    authority_path = root / "VERSION_AUTHORITY.md"
    inventory_path = root / "VERSION_REFERENCES.json"

    for path in (
        version_path,
        json_path,
        authority_path,
        inventory_path,
    ):
        if not path.exists():
            errors.append(f"missing required R1-B artifact: {path.name}")

    if errors:
        return errors

    native_version = version_path.read_text(
        encoding="utf-8"
    ).strip()

    if not native_version:
        errors.append("VERSION is empty")
        return errors

    try:
        metadata = json.loads(
            json_path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        errors.append(f"VERSION.json invalid: {exc}")
        return errors

    if metadata.get("version") != native_version:
        errors.append(
            "VERSION and VERSION.json disagree: "
            f"{native_version!r} != {metadata.get('version')!r}"
        )

    if metadata.get("inferred_versioning_allowed") is not False:
        errors.append("inferred versioning must be false")

    if metadata.get("mixed_version_identity_allowed") is not False:
        errors.append("mixed version identity must be false")

    state = metadata.get("promotion_state")
    canonical = metadata.get("canonical")

    if state == "CANDIDATE" and canonical is not False:
        errors.append(
            "CANDIDATE state must declare canonical=false"
        )

    if state == "CANONICAL" and canonical is not True:
        errors.append(
            "CANONICAL state must declare canonical=true"
        )

    if state not in {"CANDIDATE", "CANONICAL"}:
        errors.append(
            f"invalid promotion_state: {state!r}"
        )

    if metadata.get("authority_contract") != "VERSION_AUTHORITY.md":
        errors.append(
            "VERSION.json authority_contract does not resolve "
            "to VERSION_AUTHORITY.md"
        )

    try:
        inventory = json.loads(
            inventory_path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        errors.append(
            f"VERSION_REFERENCES.json invalid: {exc}"
        )
        return errors

    if inventory.get("native_version") != native_version:
        errors.append(
            "historical-reference inventory native_version "
            "does not match VERSION"
        )

    actual = scan(root, native_version)
    recorded = inventory.get("entries")

    if actual != recorded:
        errors.append(
            "repository version references differ from "
            "VERSION_REFERENCES.json; regenerate inventory"
        )

    # Active control surfaces may reference the native version or v41
    # family, but may not assert v39/v40 or v41.1.x as active identity.
    for entry in actual:
        if entry["path"] not in ACTIVE_VERSION_DECLARATION_SURFACES:
            continue

        if entry["classification"] in {
            "HISTORICAL_V39",
            "HISTORICAL_V40",
            "CANDIDATE_BRIDGE_HISTORY",
            "REVIEW_REQUIRED",
        }:
            errors.append(
                "competing version reference on active control surface: "
                f"{entry['path']}:{entry['line']} "
                f"{entry['token']} "
                f"({entry['classification']})"
            )

    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=".",
        help="repository root"
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors = validate(root)

    if errors:
        print("R1-B VERSION IDENTITY VALIDATION: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    version = (root / "VERSION").read_text(
        encoding="utf-8"
    ).strip()

    metadata = json.loads(
        (root / "VERSION.json").read_text(
            encoding="utf-8"
        )
    )

    print("R1-B VERSION IDENTITY VALIDATION: PASS")
    print(f"Version: {version}")
    print(
        "Promotion State: "
        f"{metadata['promotion_state']}"
    )
    print(
        "Canonical: "
        f"{str(metadata['canonical']).upper()}"
    )
    print("Mixed-Version Identity: NONE DETECTED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
