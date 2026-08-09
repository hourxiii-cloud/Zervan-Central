#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.collision_boundary import (
    CLEAN,
    COLLISION,
    UNRESOLVED_CONTEXT,
    analyze_collision_boundary,
)

from tools.evidence_ceiling import (
    ROW_LOCAL,
    GROUP_LOCAL,
    EVENT_CONTEXT,
    NATIVE_CONTEXT,
    OBSERVED,
    INFERRED,
    UNKNOWN,
    ADMISSIBLE,
    CONDITIONAL,
    INADMISSIBLE,
    UNRESOLVED,
    AUTHORITY_STATE,
    HUMAN_GATE_STATE,
    evaluate_claim,
    validate_epistemic_transition,
    validate_scope_promotion,
    confidence_changes_evidence_scope,
)


CONTRACT = (
    ROOT
    / "contracts"
    / "analysis"
    / "EVIDENCE_CEILING_ENFORCEMENT.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "analysis"
    / "evidence_ceiling.schema.json"
)

COLLISION_CONTRACT = (
    ROOT
    / "contracts"
    / "analysis"
    / "COLLISION_BOUNDARY.md"
)

COLLISION_SCHEMA = (
    ROOT
    / "schemas"
    / "analysis"
    / "collision_boundary.schema.json"
)


def normalized(path: Path) -> str:
    return " ".join(
        path.read_text(
            encoding="utf-8"
        ).replace("`", "").split()
    )


def validate_contract_and_schema() -> list[str]:
    errors = []

    for path in (
        CONTRACT,
        SCHEMA,
        COLLISION_CONTRACT,
        COLLISION_SCHEMA,
    ):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )

        collision_schema = json.loads(
            COLLISION_SCHEMA.read_text(
                encoding="utf-8"
            )
        )

    except Exception as exc:
        return [
            f"schema invalid: {exc}"
        ]

    contract = normalized(CONTRACT)

    required_markers = (
        "Evidence ceiling != confidence score.",
        "Confidence does not override claim ceiling.",
        "UNRESOLVED != ADMISSIBLE.",
        "CONDITIONAL != ADMISSIBLE.",
        "INFERRED MUST NOT silently become OBSERVED.",
        "UNKNOWN MUST NOT silently become INFERRED.",
        "UNKNOWN MUST NOT silently become OBSERVED.",
        "Collision != event attribution.",
        "Collision != attack attribution.",
        "Collision != command-and-control evidence.",
        "UNRESOLVED_CONTEXT MUST NOT be used as affirmative evidence.",
        "Missing evidence != negative evidence.",
        "Missing evidence != permission to infer.",
        "Human approval does not manufacture evidence.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Human Gate approval does not raise the evidence ceiling.",
    )

    for marker in required_markers:
        if marker not in contract:
            errors.append(
                f"contract marker missing: {marker}"
            )

    properties = schema.get(
        "properties",
        {},
    )

    if set(
        properties.get(
            "epistemic_class",
            {},
        ).get(
            "enum",
            [],
        )
    ) != {
        OBSERVED,
        INFERRED,
        UNKNOWN,
    }:
        errors.append(
            "schema epistemic classes disagree"
        )

    expected_scopes = {
        ROW_LOCAL,
        GROUP_LOCAL,
        EVENT_CONTEXT,
        NATIVE_CONTEXT,
    }

    for field in (
        "available_evidence_scope",
        "required_evidence_scope",
    ):
        if set(
            properties.get(
                field,
                {},
            ).get(
                "enum",
                [],
            )
        ) != expected_scopes:
            errors.append(
                f"schema evidence scopes disagree: {field}"
            )

    if set(
        properties.get(
            "claim_disposition",
            {},
        ).get(
            "enum",
            [],
        )
    ) != {
        ADMISSIBLE,
        CONDITIONAL,
        INADMISSIBLE,
        UNRESOLVED,
    }:
        errors.append(
            "schema claim dispositions disagree"
        )

    collision_enum = set(
        properties.get(
            "collision_disposition",
            {},
        ).get(
            "enum",
            [],
        )
    )

    collision_source_enum = set(
        collision_schema.get(
            "properties",
            {},
        ).get(
            "population_disposition",
            {},
        ).get(
            "enum",
            [],
        )
    )

    if collision_enum != {
        CLEAN,
        COLLISION,
        UNRESOLVED_CONTEXT,
    }:
        errors.append(
            "evidence-ceiling collision states disagree"
        )

    if collision_enum != collision_source_enum:
        errors.append(
            "AC-RTIOT-01 / AC-RTIOT-02 collision enums drifted"
        )

    if (
        properties.get(
            "authority_state",
            {},
        ).get("const")
        != "NONE"
    ):
        errors.append(
            "schema authority state must remain NONE"
        )

    if (
        properties.get(
            "human_gate_state",
            {},
        ).get("const")
        != "ACTIVE"
    ):
        errors.append(
            "schema Human Gate state must remain ACTIVE"
        )

    if AUTHORITY_STATE != "NONE":
        errors.append(
            "runtime authority state promoted"
        )

    if HUMAN_GATE_STATE != "ACTIVE":
        errors.append(
            "runtime Human Gate state changed"
        )

    return errors


def integration_checks() -> list[str]:
    errors = []

    surface = (
        "proto",
        "service",
        "src_port",
        "dst_port",
        "duration",
        "packets",
        "bytes",
    )

    rows = [
        {
            "member_reference": "udp5353:a",
            "reviewed_label": "Metasploit",
            "proto": "udp",
            "service": "dns",
            "src_port": 5353,
            "dst_port": 5353,
            "duration": 0,
            "packets": 1,
            "bytes": 139,
            "provenance_reference":
                "fixture:rt-iot2022",
        },
        {
            "member_reference": "udp5353:b",
            "reviewed_label": "NMAP_UDP",
            "proto": "udp",
            "service": "dns",
            "src_port": 5353,
            "dst_port": 5353,
            "duration": 0,
            "packets": 1,
            "bytes": 139,
            "provenance_reference":
                "fixture:rt-iot2022",
        },
    ]

    collision = analyze_collision_boundary(
        rows,
        surface,
    )

    if collision.collision_rows != 2:
        errors.append(
            "AC-RTIOT-01 integration fixture "
            "did not produce collision"
        )

        return errors

    collision_state = (
        collision.row_dispositions[0][
            "population_disposition"
        ]
    )

    if collision_state != COLLISION:
        errors.append(
            "collision state not preserved into ceiling evaluation"
        )

    # Supported row-local observation.
    residue = evaluate_claim(
        claim_id="claim:protocol-residue",
        claim_text=(
            "The admitted measurable row contains "
            "UDP 5353 protocol-compatible residue."
        ),
        epistemic_class=OBSERVED,
        available_evidence_scope=ROW_LOCAL,
        required_evidence_scope=ROW_LOCAL,
        evidence_boundary_reference=
            "boundary:rt-iot2022:row-features",
        evidence_ceiling_reference=
            "ceiling:protocol-instruction-residue",
        evidence_references=(
            collision.row_dispositions[0][
                "measurable_body_sha512"
            ],
        ),
        collision_disposition=collision_state,
        confidence=0.999999,
        provenance_route=(
            "rt-iot2022",
            "AC-RTIOT-01",
            "AC-RTIOT-02",
        ),
    )

    if residue.claim_disposition != ADMISSIBLE:
        errors.append(
            "supported row-local residue observation blocked"
        )

    # Unsupported macro-event claim.
    c2 = evaluate_claim(
        claim_id="claim:c2",
        claim_text=(
            "UDP 5353 collision residue establishes "
            "command-and-control activity."
        ),
        epistemic_class=INFERRED,
        available_evidence_scope=ROW_LOCAL,
        required_evidence_scope=NATIVE_CONTEXT,
        evidence_boundary_reference=
            "boundary:rt-iot2022:row-features",
        evidence_ceiling_reference=
            "ceiling:protocol-instruction-residue",
        evidence_references=(
            collision.row_dispositions[0][
                "measurable_body_sha512"
            ],
        ),
        missing_evidence_requirements=(
            "native_packet_context",
            "event_window",
            "process_lineage",
        ),
        collision_disposition=collision_state,
        confidence=0.999999,
        provenance_route=(
            "rt-iot2022",
            "AC-RTIOT-01",
            "AC-RTIOT-02",
        ),
    )

    if c2.claim_disposition == ADMISSIBLE:
        errors.append(
            "high-confidence collision residue "
            "promoted into C2 claim"
        )

    if c2.claim_disposition != INADMISSIBLE:
        errors.append(
            "collision-specific hard ceiling "
            "did not take precedence"
        )

    # Confidence MUST NOT move the evidence surface.
    if (
        confidence_changes_evidence_scope(
            available_scope=ROW_LOCAL,
            confidence_before=0.0,
            confidence_after=1.0,
        )
        != ROW_LOCAL
    ):
        errors.append(
            "confidence changed evidence scope"
        )

    # No new evidence -> no epistemic promotion.
    if validate_epistemic_transition(
        prior_class=UNKNOWN,
        requested_class=OBSERVED,
    ):
        errors.append(
            "UNKNOWN promoted to OBSERVED "
            "without new evidence"
        )

    # No new evidence -> no scope promotion.
    if validate_scope_promotion(
        prior_scope=ROW_LOCAL,
        requested_scope=NATIVE_CONTEXT,
    ):
        errors.append(
            "ROW_LOCAL promoted to NATIVE_CONTEXT "
            "without new evidence"
        )

    # New attributable evidence may make promotion eligible
    # for a separate evaluation; it does not mutate the old claim.
    if not validate_scope_promotion(
        prior_scope=ROW_LOCAL,
        requested_scope=EVENT_CONTEXT,
        new_evidence_references=(
            "event-window:verified:1",
        ),
    ):
        errors.append(
            "new attributable evidence "
            "could not support reevaluation"
        )

    return errors


def main() -> int:
    errors = validate_contract_and_schema()
    errors.extend(
        integration_checks()
    )

    if errors:
        print(
            "AC-RTIOT-02 EVIDENCE CEILING: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "AC-RTIOT-02 EVIDENCE CEILING: PASS"
    )
    print(
        "AC-RTIOT-01 collision integration: VERIFIED"
    )
    print(
        "Row-local residue observation: ADMISSIBLE"
    )
    print(
        "Collision -> macro-event promotion: BLOCKED"
    )
    print(
        "0.999999 confidence -> evidence promotion: BLOCKED"
    )
    print(
        "UNKNOWN -> OBSERVED without new evidence: BLOCKED"
    )
    print(
        "ROW_LOCAL -> NATIVE_CONTEXT without new evidence: BLOCKED"
    )
    print(
        "New attributable evidence -> reevaluation eligibility: VERIFIED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Disposition: AC_RTIOT_02_VALID"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
