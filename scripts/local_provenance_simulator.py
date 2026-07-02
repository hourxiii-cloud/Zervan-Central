#!/usr/bin/env python3
"""Zervan v39.0 local provenance simulator.

Purpose:
- Simulate Origin Dataset Boundary behavior locally.
- Simulate no-change / no-reach behavior locally.
- Record local-only transition rows in a JSON ledger.
- Never reach S3, DynamoDB, Jira, or any external system.

Usage:
    python scripts/local_provenance_simulator.py README.md demo.origin
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PACKAGE_ID = "LCALL-2026.06.17-001"
CANONICAL_VERSION = "vTemporal.39.0"
LOCAL_STATE_DIR = ".zervan_local"
LEDGER_FILE = "provenance_ledger.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def hash_file(path: Path) -> dict[str, str]:
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()

    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            sha256.update(chunk)
            sha512.update(chunk)

    return {
        "sha256": sha256.hexdigest(),
        "sha512": sha512.hexdigest(),
    }


def ledger_path(root: Path) -> Path:
    return root / LOCAL_STATE_DIR / LEDGER_FILE


def load_ledger(root: Path) -> dict[str, Any]:
    path = ledger_path(root)
    if not path.exists():
        return {
            "package_id": PACKAGE_ID,
            "canonical_configuration": CANONICAL_VERSION,
            "external_runtime": "DISABLED",
            "system_population": "DISALLOWED",
            "authority_state": "NONE",
            "human_gate": "ACTIVE",
            "origins": {},
            "transitions": [],
        }

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Local ledger is not valid JSON: {path}") from exc


def save_ledger(root: Path, ledger: dict[str, Any]) -> None:
    path = ledger_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def simulate(root: Path, source_file: Path, origin_id: str) -> dict[str, Any]:
    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    if not source_file.is_file():
        raise ValueError(f"Source path is not a file: {source_file}")

    ledger = load_ledger(root)
    hashes = hash_file(source_file)
    source_path = relative_to_root(source_file, root)
    existing = ledger["origins"].get(origin_id)

    if existing is None:
        now = utc_now()
        origin_record = {
            "origin_id": origin_id,
            "source_path": source_path,
            "first_seen_utc": now,
            "last_seen_utc": now,
            "sha256": hashes["sha256"],
            "sha512": hashes["sha512"],
            "origin_boundary": "This started here.",
            "authority_state": "NONE",
            "human_gate": "ACTIVE",
            "external_reach": False,
            "system_population": False,
        }

        ledger["origins"][origin_id] = origin_record
        ledger["transitions"].append(
            {
                "transition_id": f"{origin_id}:origin-recorded:{now}",
                "timestamp_utc": now,
                "origin_id": origin_id,
                "source_path": source_path,
                "status": "ORIGIN_RECORDED",
                "reason": "No prior local origin record existed.",
                "external_reach": False,
                "system_population": False,
                "authority_state": "NONE",
            }
        )
        save_ledger(root, ledger)

        return {
            "status": "ORIGIN_RECORDED",
            "origin_id": origin_id,
            "source_path": source_path,
            "sha256": hashes["sha256"],
            "sha512": hashes["sha512"],
            "external_reach": False,
            "system_population": False,
            "authority_state": "NONE",
            "human_gate": "ACTIVE",
        }

    if existing.get("sha512") == hashes["sha512"]:
        existing["last_seen_utc"] = utc_now()
        save_ledger(root, ledger)

        return {
            "status": "NO_CHANGE_NO_REACH",
            "origin_id": origin_id,
            "source_path": source_path,
            "sha256": hashes["sha256"],
            "sha512": hashes["sha512"],
            "reason": "Local hash matched existing origin record. No external reach required.",
            "external_reach": False,
            "system_population": False,
            "authority_state": "NONE",
            "human_gate": "ACTIVE",
        }

    prior_sha512 = existing.get("sha512")
    now = utc_now()
    existing["last_seen_utc"] = now
    existing["sha256"] = hashes["sha256"]
    existing["sha512"] = hashes["sha512"]
    existing["source_path"] = source_path

    ledger["transitions"].append(
        {
            "transition_id": f"{origin_id}:changed-local:{now}",
            "timestamp_utc": now,
            "origin_id": origin_id,
            "source_path": source_path,
            "status": "LOCAL_CHANGE_RECORDED",
            "reason": "Local source hash changed. Transition row recorded locally only.",
            "prior_sha512": prior_sha512,
            "new_sha512": hashes["sha512"],
            "external_reach": False,
            "system_population": False,
            "authority_state": "NONE",
        }
    )
    save_ledger(root, ledger)

    return {
        "status": "LOCAL_CHANGE_RECORDED",
        "origin_id": origin_id,
        "source_path": source_path,
        "prior_sha512": prior_sha512,
        "new_sha512": hashes["sha512"],
        "external_reach": False,
        "system_population": False,
        "authority_state": "NONE",
        "human_gate": "ACTIVE",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulate Zervan v39.0 local provenance behavior."
    )
    parser.add_argument(
        "source_file",
        help="Local file to register or compare, such as README.md.",
    )
    parser.add_argument(
        "origin_id",
        help="Origin Dataset Boundary ID, such as demo.origin.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    source_file = (root / args.source_file).resolve()

    try:
        result = simulate(root, source_file, args.origin_id)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
