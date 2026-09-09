#!/usr/bin/env python3

from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(
    encoding="utf-8"
).strip()

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

def classify(token):
    normalized = token.replace("_", ".")

    if normalized == VERSION:
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


def main():
    files = subprocess.check_output(
        [
            "git", "-C", str(ROOT),
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        text=True
    ).splitlines()

    entries = []

    for rel in sorted(set(files)):
        if rel in SCAN_EXCLUDE:
            continue

        path = ROOT / rel

        if not path.is_file():
            continue

        if (
            path.name != "VERSION"
            and path.suffix.lower() not in TEXT_SUFFIXES
        ):
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for line_no, line in enumerate(
            content.splitlines(),
            start=1
        ):
            for match in TOKEN_RE.finditer(line):
                token = match.group(0)

                entries.append({
                    "path": rel,
                    "line": line_no,
                    "token": token,
                    "classification": classify(token),
                })

    entries.sort(
        key=lambda x: (
            x["path"],
            x["line"],
            x["token"]
        )
    )

    branch = subprocess.check_output(
        ["git", "-C", str(ROOT), "branch", "--show-current"],
        text=True
    ).strip()

    if json.loads((ROOT / "VERSION.json").read_text())["promotion_state"] == "CANONICAL":
        branch = "main"

    inventory = {
        "schema_version": "1.0",
        "native_version": VERSION,
        "source_branch": branch,
        "scope": (
            "repository-wide textual version references "
            "for v39/v40/v41/v42 families"
        ),
        "excluded_control_files": sorted(SCAN_EXCLUDE),
        "entries": entries,
    }

    (ROOT / "VERSION_REFERENCES.json").write_text(
        json.dumps(inventory, indent=2) + "\n",
        encoding="utf-8"
    )

    print(
        f"VERSION REFERENCES REGENERATED: {len(entries)} entries"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
