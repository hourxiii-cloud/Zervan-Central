#!/usr/bin/env python3
“””
Zervan v39.0 local call verifier.

Purpose:

* Verify the repo-carried v39.0 package spine exists.
* Verify required files contain expected v39.0 markers.
* Verify manifest JSON parses and points to required source files.
* Confirm local-call posture remains inert: no external runtime, no system population, no authority promotion.

This script performs local file checks only.
It does not deploy infrastructure.
It does not populate S3, DynamoDB, Jira, or any external system.
It does not create authority.
“””

from future import annotations

import json
import sys
from pathlib import Path

PACKAGE_ID = “LCALL-2026.06.17-001”
CANONICAL_VERSION = “vTemporal.39.0”

REQUIRED_FILES = {
“README.md”: [“Zervan-Core-v39”, CANONICAL_VERSION],
“canonical/ZERVAN_v39_0_CANONICAL_LOAD.md”: [
“ZERVAN CANONICAL LOAD”,
CANONICAL_VERSION,
“MULTIDIRECTIONAL COMMUNICATION MESH”,
“No compression out”,
],
“call/INITIATION_STATEMENT_V39_0.md”: [
“Local Call Initiation Statement”,
PACKAGE_ID,
CANONICAL_VERSION,
“canonical/ZERVAN_v39_0_CANONICAL_LOAD.md”,
],
“manifests/v39_0_manifest.json”: [
PACKAGE_ID,
CANONICAL_VERSION,
“canonical/ZERVAN_v39_0_CANONICAL_LOAD.md”,
],
“receipts/v39_0_load_receipt.md”: [
“Zervan v39.0 Load Receipt”,
PACKAGE_ID,
CANONICAL_VERSION,
],
“replay/v39_0_replay_scars.md”: [
“Zervan v39.0 Replay Scars”,
CANONICAL_VERSION,
“A reference that sounds verified is not verified unless the route actually verified it.”,
],
“routes/operation_route_catalog_v39_0.md”: [
“Zervan v39.0 Operation Route Catalog”,
CANONICAL_VERSION,
“Workbook / Spreadsheet / Tabular Attribute Analysis”,
],
}

def repo_root() -> Path:
return Path(file).resolve().parents[1]

def read_text(path: Path) -> str:
try:
return path.read_text(encoding=“utf-8”)
except UnicodeDecodeError as exc:
raise AssertionError(f”File is not valid UTF-8: {path}”) from exc

def require_file(path: Path) -> str:
if not path.exists():
raise AssertionError(f”Missing required file: {path}”)
if not path.is_file():
raise AssertionError(f”Required path is not a file: {path}”)
return read_text(path)

def verify_required_files(root: Path) -> None:
for relative_path, markers in REQUIRED_FILES.items():
full_path = root / relative_path
text = require_file(full_path)

    for marker in markers:
        if marker not in text:
            raise AssertionError(
                f"Missing marker in {relative_path}: {marker!r}"
            )

def verify_manifest(root: Path) -> None:
manifest_path = root / “manifests/v39_0_manifest.json”
manifest_text = require_file(manifest_path)

try:
    manifest = json.loads(manifest_text)
except json.JSONDecodeError as exc:
    raise AssertionError(f"Manifest is not valid JSON: {manifest_path}") from exc
expected_pairs = {
    "package_id": PACKAGE_ID,
    "repository": "Zervan-Core-v39",
    "canonical_configuration": CANONICAL_VERSION,
    "artifact_state": "Produced Only",
    "authority_state": "NONE",
    "human_gate": "ACTIVE",
    "external_runtime": "DISABLED",
    "system_population": "DISALLOWED",
}
for key, expected_value in expected_pairs.items():
    actual_value = manifest.get(key)
    if actual_value != expected_value:
        raise AssertionError(
            f"Manifest mismatch for {key!r}: expected {expected_value!r}, got {actual_value!r}"
        )
source_of_truth = manifest.get("source_of_truth", {})
expected_sources = {
    "canonical_body": "canonical/ZERVAN_v39_0_CANONICAL_LOAD.md",
    "local_call_statement": "call/INITIATION_STATEMENT_V39_0.md",
    "readme": "README.md",
}
for key, expected_path in expected_sources.items():
    actual_path = source_of_truth.get(key)
    if actual_path != expected_path:
        raise AssertionError(
            f"Manifest source_of_truth mismatch for {key!r}: expected {expected_path!r}, got {actual_path!r}"
        )
manifest_files = manifest.get("files", [])
manifest_paths = {item.get("path") for item in manifest_files if isinstance(item, dict)}
for required_path in expected_sources.values():
    if required_path not in manifest_paths:
        raise AssertionError(f"Manifest files list missing: {required_path}")
if "receipts/v39_0_load_receipt.md" not in REQUIRED_FILES:
    raise AssertionError("Internal verifier error: receipt path not tracked.")

def verify_inert_posture(root: Path) -> None:
call_text = require_file(root / “call/INITIATION_STATEMENT_V39_0.md”)
receipt_text = require_file(root / “receipts/v39_0_load_receipt.md”)

required_boundary_markers = [
    "Authority State: `NONE`",
    "Human Gate: `ACTIVE`",
    "External Runtime: `DISABLED`",
    "System Population: `DISALLOWED`",
    "No external action",
    "Human Gate controls authority",
]
combined = f"{call_text}\n{receipt_text}"
for marker in required_boundary_markers:
    if marker not in combined:
        raise AssertionError(f"Missing inert-posture boundary marker: {marker!r}")

def main() -> int:
root = repo_root()

try:
    verify_required_files(root)
    verify_manifest(root)
    verify_inert_posture(root)
except AssertionError as exc:
    print(f"FAIL: {exc}", file=sys.stderr)
    return 1
print("PASS: v39.0 local call package verified")
return 0

if name == “main”:
raise SystemExit(main())
