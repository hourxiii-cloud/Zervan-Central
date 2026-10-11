#!/usr/bin/env python3
"""Record the explicit v47.8 flow-math Human Gate approval on synchronized main."""
import hashlib
import json
import subprocess
from pathlib import Path

EXPECTED_ARCHIVE_SHA256 = "b9f25ee53f604ec731412bc72db56bb4870c880633e835137efbbb788729f330"
SOURCE_SHA = "249a62f631f661ae688fb6e21bb8302969385e4f"
SOURCE_BASELINE_SHA = "bf8c82dfb911ba4eac4b984c77ace741c4e81c6f"
PORT_BASELINE_SHA = "1e2847133eb69c925dcb85fa91bf1fe17919e4b2"
PORT_COMMIT_SHA = "21c9f1e83f7f999f9af03f856c9ede47564a0e3b"

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

root = Path(git("rev-parse", "--show-toplevel"))
if git("branch", "--show-current") != "main":
    raise SystemExit("STOP: switch to main; no files changed.")
git("fetch", "origin", "main")
if git("rev-parse", "HEAD") != git("rev-parse", "origin/main"):
    raise SystemExit("STOP: local main is not synchronized with origin/main; no files changed.")

archive = root / "Zervan_v47_8_Flow_Math_Port.zip"
if not archive.is_file() or hashlib.sha256(archive.read_bytes()).hexdigest() != EXPECTED_ARCHIVE_SHA256:
    raise SystemExit("STOP: transport ZIP missing or its SHA-256 differs; no files changed.")

paths = [
    "canonical/geometry/FLOW_MATH_ORIGIN_CONTRACT.md",
    "canonical/geometry/FLOW_MATH_ADMISSION.json",
    "canonical/v47.8/HUMAN_GATE_DECISION.md",
    "canonical/ZERVAN_v47_8_CANONICAL_ENTRY.md",
    "verification/v47.8/PROMOTION_RECEIPT.json",
    "tools/validate_flow_math_admission.py",
    "tests/test_flow_math_admission.py",
]
for rel in paths:
    p = root / rel
    for args in (["diff", "--quiet", "--", rel], ["diff", "--cached", "--quiet", "--", rel]):
        result = subprocess.run(["git", *args], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode not in (0, 1):
            raise SystemExit(f"STOP: unable to inspect {rel}; no files changed.")
        if result.returncode == 1:
            raise SystemExit(f"STOP: preserving existing edits to {rel}; no files changed.")

contract_rel = "canonical/geometry/FLOW_MATH_ORIGIN_CONTRACT.md"
receipt_rel = "verification/v47.8/PROMOTION_RECEIPT.json"
contract = f"""# v47.8 Relational Flow Math Origin Contract

Contract standing: HUMAN-GATE APPROVED FOR CANONICAL INTEGRATION
Authority: NONE
Human Gate: ACTIVE for runtime, physical validation, external action, and further scope.

## Origin identity

Originating candidate commit SHA: `{SOURCE_SHA}`
Source baseline commit SHA: `{SOURCE_BASELINE_SHA}` (vTemporal.42.5.4)
Transport artifact: `Zervan_v47_8_Flow_Math_Port.zip`
Transport artifact SHA-256: `{EXPECTED_ARCHIVE_SHA256}`
Port baseline commit on main: `{PORT_BASELINE_SHA}`
Port commit on main: `{PORT_COMMIT_SHA}`

The originating candidate SHA above is the required identity for this port. A different source SHA, source baseline, or transport-artifact digest breaks this contract and requires a new origin reconciliation and Human Gate decision. The source lineage must not be substituted with a matching version label.

## Human Gate decision

On 2026-10-11 (America/New_York), the user explicitly approved the provided package for canonical qualification and integration: “I DID THIS. I APPROVE.” This decision restores the approval omitted from the package handoff and authorizes this bounded flow-math package to be recorded in Canon. The decision is recorded in `canonical/v47.8/HUMAN_GATE_DECISION.md` and `{receipt_rel}`.

## Scope

The approval covers the provided relational-flow mathematics supplement, its deterministic synthetic arithmetic implementation, its admission record, and its existing tests, bound to the originating candidate SHA above. The frozen parent remains byte-identical to the SHA-256 recorded in `canonical/geometry/FLOW_MATH_ADMISSION.json`.

The source qualification receipt reports 19 tests passing on the source baseline. That result belongs to that source SHA and is not represented as a new v47.8 port test result. The v47.8 port test status is not asserted as passing by this approval.

Runtime deployment, physical applicability, sensor qualification, independent component execution, external action, and real-person assessment remain unqualified or disabled. This approval does not issue component credentials or grant authority.

## Binding

The promotion receipt repeats the originating candidate SHA and transport-artifact SHA-256. The flow-math admission binds this contract and receipt by file size and SHA-256. Any mismatch among this contract, the receipt, and the admission record invalidates the origin binding.
"""

contract_bytes = contract.encode("utf-8")
contract_sha = hashlib.sha256(contract_bytes).hexdigest()
contract_path = root / contract_rel
contract_path.parent.mkdir(parents=True, exist_ok=True)
contract_path.write_bytes(contract_bytes)

decision_rel = "canonical/v47.8/HUMAN_GATE_DECISION.md"
(root / decision_rel).write_text(f"""# Human Gate Decision — v47.8 Specification and Flow Math

Decision: APPROVE the v47.8 relational-flow mathematics package for canonical integration.
Date: 2026-10-11
Basis: User's direct approval: “I DID THIS. I APPROVE.”

This decision restores the Human Gate approval omitted from the package handoff. It applies to the provided flow-math package whose originating candidate commit is `{SOURCE_SHA}` and whose transport archive SHA-256 is `{EXPECTED_ARCHIVE_SHA256}`. The matching origin contract is `{contract_rel}`; the superseding receipt is `{receipt_rel}`.

Approval covers the bounded mathematical supplement, its deterministic synthetic arithmetic implementation, its admission record, and existing tests. The source qualification receipt reports 19 tests on the source baseline; that result is not a v47.8 port test result. This approval does not claim that the current v47.8 `make check` passed.

Runtime deployment, physical applicability, sensors, independent component execution, and external action remain unqualified or disabled. Authority remains NONE. Human Gate remains ACTIVE for those actions and any scope beyond this decision.
""", encoding="utf-8")

recorded_head = git("rev-parse", "HEAD")
receipt = {
    "schema": "zervan-promotion-receipt/v2",
    "version": "vTemporal.47.8.0",
    "branch": "main",
    "standing": "HUMAN-GATE APPROVED FOR CANONICAL INTEGRATION",
    "decision": "APPROVE",
    "decision_scope": "Origin-bound v47.8 relational-flow mathematics package: specification, deterministic synthetic arithmetic implementation, admission record, and existing tests.",
    "decision_date": "2026-10-11",
    "decision_timezone": "America/New_York",
    "decision_basis": "User's direct approval: “I DID THIS. I APPROVE.” The record restores the Human Gate approval omitted from the package handoff.",
    "decision_record": decision_rel,
    "supersedes": "Prior v47.8 promotion receipt for the flow-math approval scope.",
    "recorded_against_main_commit": recorded_head,
    "originating_candidate_commit": SOURCE_SHA,
    "source_baseline_commit": SOURCE_BASELINE_SHA,
    "source_baseline_release": "vTemporal.42.5.4",
    "transport_artifact": {"path": archive.name, "sha256": EXPECTED_ARCHIVE_SHA256},
    "port_baseline_commit": PORT_BASELINE_SHA,
    "port_commit": PORT_COMMIT_SHA,
    "origin_contract": {"path": contract_rel, "sha256": contract_sha},
    "qualification_evidence": {
        "source_receipt": "verification/geometry/FLOW_MATH_QUALIFICATION_RECEIPT.md",
        "source_receipt_scope": "Historical source-baseline qualification only; it reports 19 tests passing at the source baseline.",
        "v47_8_port_tests": "NOT ASSERTED AS PASSING",
        "repository_check": "This receipt records user approval and origin binding; it does not certify a successful make check."
    },
    "runtime_validation": "NOT PERFORMED",
    "physical_applicability": "NOT QUALIFIED",
    "sensor_qualification": "NOT PERFORMED",
    "independent_component_execution": False,
    "external_action": "DISABLED",
    "authority": "NONE",
    "human_gate": "ACTIVE for runtime, physical validation, external action, and any scope beyond this approval."
}
receipt_bytes = (json.dumps(receipt, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
(root / receipt_rel).write_bytes(receipt_bytes)
receipt_sha = hashlib.sha256(receipt_bytes).hexdigest()

admission_rel = "canonical/geometry/FLOW_MATH_ADMISSION.json"
admission_path = root / admission_rel
admission = json.loads(admission_path.read_text(encoding="utf-8"))
admission["human_authorization"] = "2026-10-11 America/New_York: user explicitly approved the origin-bound flow-math package for Canon integration; see canonical/v47.8/HUMAN_GATE_DECISION.md"
admission["originating_candidate_commit"] = SOURCE_SHA
admission["transport_artifact_sha256"] = EXPECTED_ARCHIVE_SHA256
admission["origin_contract"] = contract_rel
admission["promotion_receipt"] = receipt_rel
existing = {item["path"] for item in admission["payloads"]}
for rel in (contract_rel, receipt_rel):
    if rel not in existing:
        admission["payloads"].append({"path": rel})
# Keep the original source and port records; refresh every payload binding from the exact files.
for item in admission["payloads"]:
    data = (root / item["path"]).read_bytes()
    item["size_bytes"] = len(data)
    item["sha256"] = hashlib.sha256(data).hexdigest()
admission_path.write_text(json.dumps(admission, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

validator_rel = "tools/validate_flow_math_admission.py"
validator_path = root / validator_rel
validator = validator_path.read_text(encoding="utf-8")
needle = "    entry = (root / version['canonical_entry']).read_text()\n    for path in [admission_path, *a['load_order']]:\n"
replacement = """    origin_sha = a.get('originating_candidate_commit')
    transport_sha = a.get('transport_artifact_sha256')
    contract_path = a.get('origin_contract')
    receipt_path = a.get('promotion_receipt')
    payloads = {item['path']: item for item in a['payloads']}
    if not origin_sha or not transport_sha or contract_path not in payloads or receipt_path not in payloads:
        raise ValueError('origin contract or receipt binding missing')
    contract_text = (root / contract_path).read_text()
    receipt = json.loads((root / receipt_path).read_text())
    contract_item = payloads[contract_path]
    if f"Originating candidate commit SHA: `{origin_sha}`" not in contract_text:
        raise ValueError('originating candidate SHA mismatch')
    if f"Transport artifact SHA-256: `{transport_sha}`" not in contract_text:
        raise ValueError('transport artifact SHA mismatch')
    if receipt.get('originating_candidate_commit') != origin_sha:
        raise ValueError('receipt originating SHA mismatch')
    if receipt.get('transport_artifact', {}).get('sha256') != transport_sha:
        raise ValueError('receipt transport SHA mismatch')
    if receipt.get('origin_contract') != {'path': contract_path, 'sha256': contract_item['sha256']}:
        raise ValueError('receipt contract binding mismatch')
    entry = (root / version['canonical_entry']).read_text()
    for path in [admission_path, *a['load_order'], contract_path, receipt_path]:
"""
if validator.count(needle) != 1:
    raise SystemExit("STOP: flow-math validator anchor changed; no commit made.")
validator_path.write_text(validator.replace(needle, replacement), encoding="utf-8")

test_rel = "tests/test_flow_math_admission.py"
test_path = root / test_rel
test = test_path.read_text(encoding="utf-8")
old = "            p = dest / 'canonical/ZERVAN_v42_5_4_CANONICAL_ENTRY.md'\n"
new = "            version = json.loads((dest / 'VERSION.json').read_text())\n            p = dest / version['canonical_entry']\n"
if test.count(old) != 1:
    raise SystemExit("STOP: expected historical canonical-entry test path missing; no commit made.")
test_path.write_text(test.replace(old, new), encoding="utf-8")

entry_rel = "canonical/ZERVAN_v47_8_CANONICAL_ENTRY.md"
entry_path = root / entry_rel
entry = entry_path.read_text(encoding="utf-8")
old_block = "The v47.8 supplement binds `/canonical/geometry/FLOW_MATH_ADMISSION.json`, which loads the frozen flow/pressure/vortex source before `/canonical/geometry/RELATIONAL_FLOW_MATHEMATICS.md`. The scoped arithmetic implementation is `/tools/relational_flow_math.py`; its port record is `/verification/v47.8/FLOW_MATH_PORT_RECEIPT.md`.\n\nThe supplement provides synthetic accounting and interval-flow calculations. Runtime deployment, physical applicability, sensors, and independent execution remain unqualified. The historical source-suite result is not a test result for this v47.8 port."
new_block = "The v47.8 supplement binds `/canonical/geometry/FLOW_MATH_ADMISSION.json`, which loads the frozen flow/pressure/vortex source before `/canonical/geometry/RELATIONAL_FLOW_MATHEMATICS.md`. The scoped arithmetic implementation is `/tools/relational_flow_math.py`.\n\nThe Human Gate approval and exact source lineage are bound by `/canonical/geometry/FLOW_MATH_ORIGIN_CONTRACT.md`, `/canonical/v47.8/HUMAN_GATE_DECISION.md`, and `/verification/v47.8/PROMOTION_RECEIPT.json`. The earlier port record remains `/verification/v47.8/FLOW_MATH_PORT_RECEIPT.md`. The originating candidate SHA and transport archive digest must match the contract and admission.\n\nThe supplement provides synthetic accounting and interval-flow calculations. The source qualification receipt is scoped to its original baseline and is not a v47.8 port test result. This approval does not certify that `make check` passed. Runtime deployment, physical applicability, sensors, and independent execution remain unqualified."
if entry.count(old_block) != 1:
    raise SystemExit("STOP: canonical-entry text changed; no commit made.")
entry_path.write_text(entry.replace(old_block, new_block), encoding="utf-8")

# Refresh admission bindings after updating the test and its validator.
admission = json.loads(admission_path.read_text(encoding="utf-8"))
for item in admission["payloads"]:
    data = (root / item["path"]).read_bytes()
    item["size_bytes"] = len(data)
    item["sha256"] = hashlib.sha256(data).hexdigest()
admission_path.write_text(json.dumps(admission, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

git("add", "--", *paths)
git("commit", "-m", "Record origin-bound flow math Human Gate approval")
git("push", "origin", "main")
expected = git("rev-parse", "HEAD")
remote = subprocess.check_output(["git", "ls-remote", "origin", "refs/heads/main"], text=True).split()[0]
if remote != expected:
    raise SystemExit(f"ERROR: push verification mismatch; local={expected} remote={remote}")
print(f"PROMOTION_RECEIPT_RECORDED branch=main commit={expected}")
print(f"ORIGIN_SHA={SOURCE_SHA}")
print(f"TRANSPORT_SHA256={EXPECTED_ARCHIVE_SHA256}")
print("No tests were run by this script.")
