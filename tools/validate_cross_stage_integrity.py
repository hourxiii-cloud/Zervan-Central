#!/usr/bin/env python3

from pathlib import Path
import json

from tools.cross_stage_integrity import (
    ACTIVE,
    NONE,
    VALID,
    make_valid_pipeline,
    validate_composition,
)


ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "integrity"
    / "CROSS_STAGE_SEMANTIC_INTEGRITY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "integrity"
    / "cross_stage_semantic_integrity.schema.json"
)


def normalized(path):
    return " ".join(
        path.read_text(
            encoding="utf-8"
        ).split()
    )


def validate():
    errors = []

    for path in (
        CONTRACT,
        SCHEMA,
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
    except Exception as exc:
        return [
            f"AC-07 schema invalid: {exc}"
        ]

    if (
        schema.get("title")
        != "AC-07 Cross-Stage Semantic Integrity"
    ):
        errors.append(
            "AC-07 schema title mismatch"
        )

    contract = normalized(
        CONTRACT
    )

    required_markers = (
        "Local validity != composed validity.",
        "Stage PASS != composition PASS.",
        (
            "PMC -> CCR -> MC -> Raven -> Human Gate "
            "MUST preserve attributable analytical "
            "meaning across the complete composition."
        ),
        "Candidate identity survives commitment.",
        "Rejected candidates remain attributable.",
        "Candidate ordering remains attributable.",
        "Uncertainty remains uncertainty.",
        "Material unknowns remain visible.",
        "Evidence boundary remains bounded.",
        "Evidence ceiling remains bounded.",
        "Governance constraints remain attributable.",
        (
            "CONDITIONAL remains conditional until "
            "attributable satisfaction."
        ),
        "Rendering does not strengthen analysis.",
        (
            "Every stage may pass while the "
            "composition fails."
        ),
        (
            "Globally impossible analytical state "
            "= BLOCKED."
        ),
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
    )

    for marker in required_markers:
        if marker not in contract:
            errors.append(
                f"AC-07 contract marker missing: {marker}"
            )

    pipeline = make_valid_pipeline()

    result = validate_composition(
        *pipeline
    )

    if (
        result.composition_disposition
        != VALID
    ):
        errors.append(
            "valid AC-07 composition does not validate"
        )

    if result.failure_reasons:
        errors.append(
            "valid AC-07 composition emitted failures"
        )

    if any(
        state.authority_state != NONE
        for state in pipeline
    ):
        errors.append(
            "AC-07 authority state drift"
        )

    if any(
        state.human_gate_state != ACTIVE
        for state in pipeline
    ):
        errors.append(
            "AC-07 Human Gate state drift"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "AC-07 CROSS-STAGE SEMANTIC INTEGRITY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "AC-07 CROSS-STAGE SEMANTIC INTEGRITY: PASS"
    )
    print(
        "Pipeline: PMC -> CCR -> MC -> Raven -> Human Gate"
    )
    print(
        "Local validity != composed validity"
    )
    print(
        "Stage PASS != composition PASS"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
