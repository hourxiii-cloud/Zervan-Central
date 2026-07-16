#!/usr/bin/env python3
"""Validate the Zervan 5.6 bridge package.

This script is intentionally local and read-only. It validates bridge artifacts,
JSON parseability, Python syntax, expected observer/sub-observer paths, and the
canonical text invariants required by the 5.6 transition bridge.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass
class Check:
    name: str
    status: str
    detail: str


def iter_files(root: Path, suffix: str) -> Iterable[Path]:
    ignored_parts = {".git", "__pycache__"}
    for path in root.rglob(f"*{suffix}"):
        if any(part in ignored_parts for part in path.parts):
            continue
        if path.is_file():
            yield path


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def require_file(root: Path, path: str, checks: list[Check]) -> None:
    target = root / path
    if target.is_file():
        checks.append(Check(f"required_file:{path}", "PASS", "present"))
    else:
        checks.append(Check(f"required_file:{path}", "FAIL", "missing"))


def require_dir(root: Path, path: str, checks: list[Check]) -> None:
    target = root / path
    if target.is_dir():
        checks.append(Check(f"required_dir:{path}", "PASS", "present"))
    else:
        checks.append(Check(f"required_dir:{path}", "FAIL", "missing"))


def require_text(root: Path, path: str, needle: str, checks: list[Check]) -> None:
    target = root / path
    try:
        text = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        checks.append(Check(f"required_text:{path}", "FAIL", f"missing file for text: {needle}"))
        return
    if needle in text:
        checks.append(Check(f"required_text:{path}", "PASS", needle))
    else:
        checks.append(Check(f"required_text:{path}", "FAIL", f"missing text: {needle}"))


def validate_json(root: Path, checks: list[Check]) -> None:
    failures = []
    count = 0
    for path in iter_files(root, ".json"):
        count += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report validation failure
            failures.append(f"{rel(root, path)}: {exc}")
    if failures:
        checks.append(Check("json_parse", "FAIL", "; ".join(failures)))
    else:
        checks.append(Check("json_parse", "PASS", f"{count} JSON files parsed"))


def validate_python(root: Path, checks: list[Check]) -> None:
    failures = []
    count = 0
    for path in iter_files(root, ".py"):
        count += 1
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec", dont_inherit=True)
        except Exception as exc:  # noqa: BLE001 - report validation failure
            failures.append(f"{rel(root, path)}: {exc}")
    if failures:
        checks.append(Check("python_compile", "FAIL", "; ".join(failures)))
    else:
        checks.append(Check("python_compile", "PASS", f"{count} Python files compiled"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Zervan 5.6 bridge package")
    parser.add_argument("--root", default=".", help="Repository or package root to validate")
    parser.add_argument(
        "--emit",
        help="Optional JSON output path. Omit for a truly read-only validation run.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    root = Path(args.root).resolve()
    checks: list[Check] = []

    require_file(root, "ZERVAN_5_6_CANONICAL_DEFINITIONS.md", checks)
    require_file(root, "ZERVAN_5_6_TRANSITION_NOTE.md", checks)
    require_file(root, "ZERVAN_5_6_VALIDATION_PROCESS.md", checks)
    require_file(root, "ZERVAN_5_6_MODIFIED_FILE_RECORD.md", checks)
    require_file(root, "DoctrineOps/ZERVAN_5_6_DEPLOYMENT_BRIDGE.md", checks)
    require_file(root, "tools/validate_zervan_5_6_bridge.py", checks)

    for path in [
        "observers/Eagle",
        "observers/Mole",
        "observers/Duck",
        "observers/Wildflower",
        "observers/Mockingbird",
        "observers/Platypus",
        "observers/owl_hoot",
        "observers/Osprey",
        "observers/Armadillo",
        "observers/AnimalKingdom",
        "Modules/AnimalKingdom",
    ]:
        require_dir(root, path, checks)

    canonical = "ZERVAN_5_6_CANONICAL_DEFINITIONS.md"
    for needle in [
        "INIT → SIGNAL / Signal Ecology → DELTA → K9 / Pups → FAMILY / Teams",
        "Primary modules produce evidence.",
        "Primary observers observe evidence",
        "Controlled sub-observers pressure evidence.",
        "Owl_Hoot remains a primary observer.",
        "Owl_Hoot is not canonically reseated as a sub-observer.",
        "The Unkindness is Raven's reporting brand and output voice.",
        "No capability is compressed out.",
    ]:
        require_text(root, canonical, needle, checks)

    require_text(root, "ZERVAN_5_6_TRANSITION_NOTE.md", "python tools/validate_zervan_5_6_bridge.py --root . --emit ZERVAN_5_6_VALIDATION_RESULTS.json", checks)
    require_text(root, "DoctrineOps/ZERVAN_5_6_DEPLOYMENT_BRIDGE.md", "ZERVAN_5_6_CANONICAL_DEFINITIONS.md", checks)
    require_text(root, "ZERVAN_5_6_MODIFIED_FILE_RECORD.md", "- Deleted files: 0", checks)

    validate_json(root, checks)
    validate_python(root, checks)

    status = "PASS" if all(check.status == "PASS" for check in checks) else "FAIL"
    output = {
        "validation_id": "zervan_5_6_bridge_validation",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "status": status,
        "checks": [asdict(check) for check in checks],
    }

    if args.emit:
        emit = Path(args.emit)
        if not emit.is_absolute():
            emit = root / emit
        emit.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
