#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "contracts/promotion/TRANSITION_RECEIPT.md"
SCHEMA = ROOT / "schemas/promotion/transition_receipt.schema.json"
RECEIPT = ROOT / "receipts/promotion/R7_I_TRANSITION_RECEIPT.json"

VERSION = ROOT / "VERSION"
VERSION_JSON = ROOT / "VERSION.json"
V40 = ROOT / "canonical/ZERVAN_v40_0_CANONICAL_LOAD.md"
R6 = ROOT / "contracts/validation/RING6_AGGREGATE_AUDIT_CLOSURE.md"
PLAY = ROOT / "docs/deployment/RING7_DEPLOYMENT_PLAY.md"


def normalized(path):
    text = path.read_text(encoding="utf-8")

    for token in ("**", "__", "`"):
        text = text.replace(token, "")

    return " ".join(text.split())


def validate():
    errors = []

    for path, label in (
        (CONTRACT, "R7-I contract"),
        (SCHEMA, "R7-I schema"),
        (RECEIPT, "R7-I receipt"),
        (VERSION, "VERSION"),
        (VERSION_JSON, "VERSION.json"),
        (V40, "v40 canonical baseline"),
        (R6, "Ring 6 closure"),
        (PLAY, "Ring 7 deployment play"),
    ):
        if not path.exists():
            errors.append(f"missing {label}")

    if errors:
        return errors

    if VERSION.read_text(encoding="utf-8").strip() != "vTemporal.41.0":
        errors.append("candidate VERSION is not vTemporal.41.0")

    version_json = json.loads(
        VERSION_JSON.read_text(encoding="utf-8")
    )

    if version_json.get("version") != "vTemporal.41.0":
        errors.append("VERSION.json candidate version disagreement")

    if version_json.get("promotion_state") != "CANDIDATE":
        errors.append("VERSION.json promotion state is not CANDIDATE")

    if version_json.get("canonical") is not False:
        errors.append("VERSION.json falsely marks candidate canonical")

    v40 = normalized(V40)

    for marker in (
        "vTemporal.40.0",
        "v40.0 is a complete canonical rebuild.",
    ):
        if marker not in v40:
            errors.append(
                f"prior canonical baseline missing marker: {marker}"
            )

    r6 = normalized(R6)

    for marker in (
        "R6-P",
        "VALIDATED_CANDIDATE",
        "Ring 6 closes when:",
    ):
        if marker not in r6:
            errors.append(
                f"Ring 6 closure missing transition marker: {marker}"
            )

    contract = normalized(CONTRACT)

    for marker in (
        "R7-I = Transition Receipt.",
        "Prior canonical -> candidate -> validated candidate -> authorized future promotion.",
        "Transition accounting != promotion.",
        "Receipt != authority.",
        "Prior canonical baseline = vTemporal.40.0.",
        "Native candidate = vTemporal.41.0.",
        "Candidate != canonical.",
        "Validated candidate != promoted candidate.",
        "Ring 7 target = READY_FOR_HUMAN_GATE.",
        "READY_FOR_HUMAN_GATE != CANONICAL.",
        "READY_FOR_HUMAN_GATE != PROMOTED.",
        "READY_FOR_HUMAN_GATE != MERGED.",
        "Future canonical target = main.",
        "Explicit Human Gate authorization is required.",
        "performed = false.",
        "Historical provenance remains preserved.",
        "Transition != replacement of history.",
        "ACCOUNTED != PROMOTED.",
        "ACCOUNTED != CANONICAL.",
        "ACCOUNTED != MERGED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "R7-J owns Stability Receipt.",
    ):
        if marker not in contract:
            errors.append(
                f"R7-I contract missing lock: {marker}"
            )

    schema = json.loads(
        SCHEMA.read_text(encoding="utf-8")
    )

    if (
        schema.get("$schema")
        != "https://json-schema.org/draft/2020-12/schema"
    ):
        errors.append(
            "R7-I schema must use JSON Schema Draft 2020-12"
        )

    receipt = json.loads(
        RECEIPT.read_text(encoding="utf-8")
    )

    checks = {
        "schema_version": "1.0",
        "receipt_type": "TRANSITION_RECEIPT",
        "ring": "R7-I",
        "native_version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "history_preserved": True,
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "promotion_state": "CANDIDATE",
        "transition_disposition": "ACCOUNTED",
    }

    for key, expected in checks.items():
        if receipt.get(key) != expected:
            errors.append(
                f"R7-I receipt mismatch for {key}: "
                f"expected {expected!r}, got {receipt.get(key)!r}"
            )

    prior = receipt.get("prior_canonical", {})

    if prior.get("branch") != "main":
        errors.append("prior canonical branch must be main")

    if prior.get("version") != "vTemporal.40.0":
        errors.append("prior canonical version must be vTemporal.40.0")

    if (
        prior.get("provenance_surface")
        != "canonical/ZERVAN_v40_0_CANONICAL_LOAD.md"
    ):
        errors.append("prior canonical provenance disagreement")

    candidate = receipt.get("candidate", {})

    if candidate.get("branch") != "candidate/v41-complete":
        errors.append("candidate branch disagreement")

    if candidate.get("version") != "vTemporal.41.0":
        errors.append("candidate version disagreement")

    if candidate.get("promotion_state") != "CANDIDATE":
        errors.append("candidate promotion state disagreement")

    if candidate.get("canonical") is not False:
        errors.append("candidate falsely marked canonical")

    validated = receipt.get("validated_candidate", {})

    if validated.get("state") != "VALIDATED_CANDIDATE":
        errors.append("validated-candidate state missing")

    if validated.get("ring6_result") != "PASS":
        errors.append("Ring 6 PASS not preserved")

    future = receipt.get("future_transition", {})

    if future.get("source_branch") != "candidate/v41-complete":
        errors.append("future source branch disagreement")

    if future.get("target_branch") != "main":
        errors.append("future target branch must be main")

    if future.get("target_state") != "CANONICAL":
        errors.append("future target state must be CANONICAL")

    if future.get("authorization_required") != "EXPLICIT_HUMAN_GATE":
        errors.append("explicit Human Gate authorization not required")

    if future.get("performed") is not False:
        errors.append("future promotion must remain unperformed")

    if not receipt.get("provenance"):
        errors.append("transition provenance missing")

    play = normalized(PLAY)

    for marker in (
        "Section identifier defines ownership, not mandatory chronological execution.",
        "Final documentation completion follows stabilized implementation state.",
        "Implementation leads.",
        "Documentation follows.",
        "Section identifier != execution dependency order.",
    ):
        if marker not in play:
            errors.append(
                f"deployment dependency correction missing: {marker}"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print("R7-I TRANSITION RECEIPT: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    print("R7-I TRANSITION RECEIPT: PASS")
    print("Prior canonical baseline: vTemporal.40.0 / main")
    print("Native candidate: vTemporal.41.0 / candidate/v41-complete")
    print("Ring 6 state: VALIDATED_CANDIDATE / PASS")
    print("Transition history: ACCOUNTED")
    print("Historical provenance: PRESERVED")
    print("Future canonical target: main")
    print("Future promotion performed: FALSE")
    print("Explicit Human Gate authorization: REQUIRED")
    print("Transition accounting -> promotion: REJECTED")
    print("Receipt self-authorization: REJECTED")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")
    print("Promotion State: CANDIDATE")
    print("TRANSITION ACCOUNTING COMPLETE")
    print("R7-J Stability Receipt: NEXT")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
