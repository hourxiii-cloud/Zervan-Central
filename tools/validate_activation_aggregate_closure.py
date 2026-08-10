#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "activation"
    / "ACTIVATION_AGGREGATE_CLOSURE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "activation"
    / "activation_aggregate_closure.schema.json"
)

REQUIRED_CONTROLS = tuple(
    f"AC-{number:02d}"
    for number in range(1, 12)
)

FAILURE_REASONS = {
    "REQUIRED_CONTROL_MISSING",
    "REQUIRED_CONTROL_FAILED",
    "REQUIRED_CONTROL_BLOCKED",
    "CONTROL_RESULT_UNKNOWN",
    "CROSS_CONTROL_SEMANTIC_CONFLICT",
    "EVIDENCE_CEILING_ENFORCEMENT_MISSING",
    "HUMAN_GATE_ENFORCEMENT_MISSING",
    "AUTHORITY_PROMOTED",
    "HUMAN_GATE_DISABLED",
    "EXECUTION_INFERRED",
    "PUBLICATION_INFERRED",
    "CANONICAL_MUTATION_INFERRED",
    "SYSTEM_POPULATION_INFERRED",
    "PROVENANCE_MISSING",
    "FAILURE_COMPRESSED_OUT",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def normalized(path: Path) -> str:
    text = path.read_text(
        encoding="utf-8"
    )

    for token in (
        "**",
        "__",
        "`",
    ):
        text = text.replace(
            token,
            ""
        )

    return " ".join(
        text.split()
    )


def make_control_result(
    control_id: str,
    *,
    validation_state: str = "PASS",
) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "validation_state": validation_state,
        "validator_reference": (
            f"validator:{control_id.lower()}"
        ),
        "test_reference": (
            f"test:{control_id.lower()}"
        ),
        "provenance_reference": (
            f"provenance:{control_id.lower()}"
        ),
    }


def make_record(
    *,
    control_results: list[dict[str, Any]] | None = None,
    evidence_ceiling_state: str = "ENFORCED",
    human_gate_semantic_state: str = "ENFORCED",
    cross_control_integrity_state: str = "VALID",
    authority_state: str = "NONE",
    human_gate_state: str = "ACTIVE",
    execution_state: str = "NOT_INFERRED",
    publication_state: str = "NOT_INFERRED",
    canonical_mutation_state: str = "NOT_INFERRED",
    system_population_state: str = "DISALLOWED",
    provenance_route: list[str] | None = None,
) -> dict[str, Any]:

    if control_results is None:
        control_results = [
            make_control_result(control_id)
            for control_id in REQUIRED_CONTROLS
        ]

    if provenance_route is None:
        provenance_route = [
            "activation:ac01-ac11",
            "activation:ac10:evidence-ceiling",
            "activation:ac11:human-gate-authority",
            "activation:ac12:aggregate-closure",
        ]

    record = {
        "schema_version": "1.0",
        "activation_control": "AC-12",
        "required_controls": list(
            REQUIRED_CONTROLS
        ),
        "control_results": control_results,
        "required_control_count": 11,
        "passed_control_count": 0,
        "failed_control_count": 0,
        "blocked_control_count": 0,
        "evidence_ceiling_state":
            evidence_ceiling_state,
        "human_gate_semantic_state":
            human_gate_semantic_state,
        "cross_control_integrity_state":
            cross_control_integrity_state,
        "authority_state":
            authority_state,
        "human_gate_state":
            human_gate_state,
        "execution_state":
            execution_state,
        "publication_state":
            publication_state,
        "canonical_mutation_state":
            canonical_mutation_state,
        "system_population_state":
            system_population_state,
        "provenance_route":
            provenance_route,
        "closure_disposition": "",
        "failure_reasons": [],
    }

    synchronize_record(record)

    return record


def control_state_counts(
    record: dict[str, Any],
) -> tuple[int, int, int]:

    results = record.get(
        "control_results",
        []
    )

    passed = sum(
        1
        for result in results
        if result.get(
            "validation_state"
        ) == "PASS"
    )

    failed = sum(
        1
        for result in results
        if result.get(
            "validation_state"
        ) == "FAIL"
    )

    blocked = sum(
        1
        for result in results
        if result.get(
            "validation_state"
        ) == "BLOCKED"
    )

    return (
        passed,
        failed,
        blocked,
    )


def evaluate_record(
    record: dict[str, Any],
) -> tuple[str, ...]:

    reasons: list[str] = []

    results = record.get(
        "control_results",
        []
    )

    result_ids = [
        result.get(
            "control_id"
        )
        for result in results
    ]

    for control_id in REQUIRED_CONTROLS:
        if control_id not in result_ids:
            reasons.append(
                "REQUIRED_CONTROL_MISSING"
            )

    if len(result_ids) != len(
        set(result_ids)
    ):
        reasons.append(
            "CROSS_CONTROL_SEMANTIC_CONFLICT"
        )

    for result in results:
        state = result.get(
            "validation_state"
        )

        if state == "FAIL":
            reasons.append(
                "REQUIRED_CONTROL_FAILED"
            )

        elif state == "BLOCKED":
            reasons.append(
                "REQUIRED_CONTROL_BLOCKED"
            )

        elif state != "PASS":
            reasons.append(
                "CONTROL_RESULT_UNKNOWN"
            )

        if not result.get(
            "validator_reference"
        ):
            reasons.append(
                "PROVENANCE_MISSING"
            )

        if not result.get(
            "test_reference"
        ):
            reasons.append(
                "PROVENANCE_MISSING"
            )

        if not result.get(
            "provenance_reference"
        ):
            reasons.append(
                "PROVENANCE_MISSING"
            )

    if (
        record.get(
            "evidence_ceiling_state"
        )
        != "ENFORCED"
    ):
        reasons.append(
            "EVIDENCE_CEILING_ENFORCEMENT_MISSING"
        )

    if (
        record.get(
            "human_gate_semantic_state"
        )
        != "ENFORCED"
    ):
        reasons.append(
            "HUMAN_GATE_ENFORCEMENT_MISSING"
        )

    if (
        record.get(
            "cross_control_integrity_state"
        )
        != "VALID"
    ):
        reasons.append(
            "CROSS_CONTROL_SEMANTIC_CONFLICT"
        )

    if (
        record.get(
            "authority_state"
        )
        != "NONE"
    ):
        reasons.append(
            "AUTHORITY_PROMOTED"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        reasons.append(
            "HUMAN_GATE_DISABLED"
        )

    if (
        record.get(
            "execution_state"
        )
        != "NOT_INFERRED"
    ):
        reasons.append(
            "EXECUTION_INFERRED"
        )

    if (
        record.get(
            "publication_state"
        )
        != "NOT_INFERRED"
    ):
        reasons.append(
            "PUBLICATION_INFERRED"
        )

    if (
        record.get(
            "canonical_mutation_state"
        )
        != "NOT_INFERRED"
    ):
        reasons.append(
            "CANONICAL_MUTATION_INFERRED"
        )

    if (
        record.get(
            "system_population_state"
        )
        != "DISALLOWED"
    ):
        reasons.append(
            "SYSTEM_POPULATION_INFERRED"
        )

    provenance = record.get(
        "provenance_route"
    )

    if (
        not isinstance(
            provenance,
            list,
        )
        or not provenance
        or any(
            not isinstance(item, str)
            or not item
            for item in provenance
        )
    ):
        reasons.append(
            "PROVENANCE_MISSING"
        )

    return tuple(
        sorted(
            set(
                reasons
            )
        )
    )


def synchronize_record(
    record: dict[str, Any],
) -> dict[str, Any]:

    passed, failed, blocked = (
        control_state_counts(
            record
        )
    )

    reasons = evaluate_record(
        record
    )

    record[
        "passed_control_count"
    ] = passed

    record[
        "failed_control_count"
    ] = failed

    record[
        "blocked_control_count"
    ] = blocked

    record[
        "failure_reasons"
    ] = list(
        reasons
    )

    record[
        "closure_disposition"
    ] = (
        "CLOSED"
        if not reasons
        else "BLOCKED"
    )

    return record


def validate_record(
    record: dict[str, Any],
) -> list[str]:

    errors: list[str] = []

    if (
        record.get(
            "schema_version"
        )
        != "1.0"
    ):
        errors.append(
            "schema version must be 1.0"
        )

    if (
        record.get(
            "activation_control"
        )
        != "AC-12"
    ):
        errors.append(
            "activation control must be AC-12"
        )

    if tuple(
        record.get(
            "required_controls",
            []
        )
    ) != REQUIRED_CONTROLS:
        errors.append(
            "required controls must be exact ordered AC-01 through AC-11"
        )

    if (
        record.get(
            "required_control_count"
        )
        != 11
    ):
        errors.append(
            "required control count must be 11"
        )

    reasons = evaluate_record(
        record
    )

    expected_disposition = (
        "CLOSED"
        if not reasons
        else "BLOCKED"
    )

    if (
        record.get(
            "closure_disposition"
        )
        != expected_disposition
    ):
        errors.append(
            "closure disposition contradicts aggregate state"
        )

    if sorted(
        record.get(
            "failure_reasons",
            []
        )
    ) != list(
        reasons
    ):
        errors.append(
            "failure reasons are incomplete or incorrect"
        )

    passed, failed, blocked = (
        control_state_counts(
            record
        )
    )

    expected_counts = {
        "passed_control_count":
            passed,
        "failed_control_count":
            failed,
        "blocked_control_count":
            blocked,
    }

    for field, expected in (
        expected_counts.items()
    ):
        if (
            record.get(
                field
            )
            != expected
        ):
            errors.append(
                f"{field} contradicts control results"
            )

    if not reasons:
        if passed != 11:
            errors.append(
                "CLOSED requires 11 passed controls"
            )

        if failed != 0:
            errors.append(
                "CLOSED requires zero failed controls"
            )

        if blocked != 0:
            errors.append(
                "CLOSED requires zero blocked controls"
            )

    return errors


def validate_contract_and_schema() -> list[str]:

    errors: list[str] = []

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

    contract = normalized(
        CONTRACT
    )

    for marker in (
        "AC-12 = Activation Aggregate Closure.",
        "AC-12 is the final activation control.",
        "AC-10 remains binding.",
        "AC-11 remains binding.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Validation PASS != execution.",
        "Validation != canonical mutation.",
        "Activation capability != population authority.",
        "No default closure.",
        "No inferred closure.",
        "Fail closed.",
        "No Compression Out applies.",
    ):
        if marker not in contract:
            errors.append(
                f"contract marker missing: {marker}"
            )

    try:
        schema = load_json(
            SCHEMA
        )
    except Exception as exc:
        errors.append(
            f"schema invalid: {exc}"
        )
        return errors

    properties = schema.get(
        "properties",
        {}
    )

    expected_consts = {
        "schema_version":
            "1.0",
        "activation_control":
            "AC-12",
        "required_control_count":
            11,
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "execution_state":
            "NOT_INFERRED",
        "publication_state":
            "NOT_INFERRED",
        "canonical_mutation_state":
            "NOT_INFERRED",
        "system_population_state":
            "DISALLOWED",
    }

    for field, expected in (
        expected_consts.items()
    ):
        if (
            properties.get(
                field,
                {},
            ).get(
                "const"
            )
            != expected
        ):
            errors.append(
                f"schema constant disagreement: {field}"
            )

    schema_reasons = set(
        properties.get(
            "failure_reasons",
            {},
        ).get(
            "items",
            {},
        ).get(
            "enum",
            [],
        )
    )

    if schema_reasons != FAILURE_REASONS:
        errors.append(
            "schema failure-reason vocabulary disagreement"
        )

    return errors


def main() -> int:

    errors = (
        validate_contract_and_schema()
    )

    if errors:
        print(
            "AC-12 ACTIVATION AGGREGATE VALIDATOR: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    valid = make_record()

    valid_errors = validate_record(
        valid
    )

    if valid_errors:
        print(
            "AC-12 ACTIVATION AGGREGATE VALIDATOR: FAIL"
        )

        for error in valid_errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "AC-12 ACTIVATION AGGREGATE VALIDATOR: READY"
    )
    print(
        "Required controls: AC-01 through AC-11"
    )
    print(
        "Required control count: 11"
    )
    print(
        "Valid aggregate disposition: CLOSED"
    )
    print(
        "AC-10 evidence ceiling: ENFORCED"
    )
    print(
        "AC-11 Human-Gate / authority semantics: ENFORCED"
    )
    print(
        "Cross-control integrity: VALID"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Execution: NOT_INFERRED"
    )
    print(
        "Publication: NOT_INFERRED"
    )
    print(
        "Canonical Mutation: NOT_INFERRED"
    )
    print(
        "System Population: DISALLOWED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
