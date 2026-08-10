#!/usr/bin/env python3

from __future__ import annotations

from typing import Any


AUTHORITY_BEARING_TRANSITIONS = {
    "PUBLICATION",
    "EXTERNAL_DEPLOYMENT",
    "PRODUCTION_EXECUTION",
    "SYSTEM_POPULATION",
    "PACKAGE_PROMOTION",
    "COMPLIANCE_CLAIM",
    "LEGAL_FINDING",
    "CERTIFICATION_CLAIM",
    "OPERATIONAL_AUTHORITY",
    "DISCIPLINARY_OR_HR_ACTION",
    "AUTHORITY_BEARING_AUTOMATION",
    "IRREVERSIBLE_EXTERNAL_CHANGE",
}


MATERIAL_BINDINGS = (
    "transition_class",
    "transition_target",
    "requested_scope",
    "room_object_id",
    "room_revision_id",
    "room_state_root",
    "authorized_view_root",
    "evidence_boundary_ref",
    "evidence_ceiling_ref",
)


def _changed(
    source: dict[str, Any],
    downstream: dict[str, Any],
    field: str,
) -> bool:
    return source.get(field) != downstream.get(field)


def validate_human_gate_authority_transition(
    source_state: dict[str, Any],
    downstream_state: dict[str, Any],
) -> tuple[str, ...]:
    """
    Validate AC-11 authority and Human-Gate semantics.

    This validator is read-only.

    It does not authorize movement.
    It does not execute movement.
    It does not mutate either state.
    """

    reasons: list[str] = []

    # Authority NONE is invariant.
    if downstream_state.get("authority_state", "NONE") != "NONE":
        reasons.append("AUTHORITY_PROMOTED")

    # Human Gate ACTIVE is invariant.
    if downstream_state.get("human_gate_state", "ACTIVE") != "ACTIVE":
        reasons.append("HUMAN_GATE_DISABLED")

    transition_class = downstream_state.get("transition_class")
    decision = downstream_state.get("human_gate_decision")

    authority_bearing = (
        transition_class in AUTHORITY_BEARING_TRANSITIONS
    )

    # Authority-bearing movement requires explicit Human Gate state.
    if authority_bearing and decision not in {
        "PENDING",
        "APPROVED",
        "DENIED",
    }:
        reasons.append("HUMAN_GATE_DECISION_MISSING")

    # Approval requires attributable human decision.
    if (
        decision == "APPROVED"
        and not downstream_state.get("human_decision_ref")
    ):
        reasons.append("HUMAN_DECISION_REFERENCE_MISSING")

    # Approval must be explicitly scoped.
    if decision == "APPROVED":
        for field in (
            "transition_class",
            "transition_target",
            "requested_scope",
            "room_object_id",
            "room_revision_id",
            "room_state_root",
            "authorized_view_root",
            "evidence_boundary_ref",
            "evidence_ceiling_ref",
        ):
            if not downstream_state.get(field):
                reasons.append(
                    f"APPROVAL_BINDING_MISSING:{field}"
                )

    # MC admissibility cannot be rewritten by downstream authority handling.
    if _changed(
        source_state,
        downstream_state,
        "mc_admissibility",
    ):
        reasons.append("MC_ADMISSIBILITY_REWRITTEN")

    # Human approval cannot manufacture stronger evidence scope.
    if _changed(
        source_state,
        downstream_state,
        "evidence_boundary_ref",
    ):
        reasons.append("EVIDENCE_BOUNDARY_CHANGED")

    if _changed(
        source_state,
        downstream_state,
        "evidence_ceiling_ref",
    ):
        reasons.append("EVIDENCE_CEILING_CHANGED")

    # Approval is not execution.
    if (
        decision == "APPROVED"
        and source_state.get("execution_state") == "NOT_EXECUTED"
        and downstream_state.get("execution_state") == "EXECUTED"
    ):
        reasons.append("APPROVAL_PROMOTED_TO_EXECUTION")

    # Publication approval is not proof of publication.
    if (
        source_state.get("publication_state") == "NOT_PUBLISHED"
        and downstream_state.get("publication_state") == "PUBLISHED"
        and decision == "APPROVED"
    ):
        reasons.append("APPROVAL_PROMOTED_TO_PUBLICATION")

    # Validation/approval does not imply canonical mutation.
    if (
        source_state.get("canonical_mutation_state") == "NOT_MUTATED"
        and downstream_state.get("canonical_mutation_state") == "MUTATED"
    ):
        reasons.append("CANONICAL_MUTATION_INFERRED")

    # Approval for some other movement does not imply system population.
    if (
        source_state.get("system_population_state") == "NOT_POPULATED"
        and downstream_state.get("system_population_state") == "POPULATED"
        and transition_class != "SYSTEM_POPULATION"
    ):
        reasons.append("SYSTEM_POPULATION_INFERRED")

    # Human Gate approval does not manufacture claim authority.
    if (
        source_state.get("claim_authority_state") == "NONE"
        and downstream_state.get("claim_authority_state") != "NONE"
    ):
        reasons.append("CLAIM_AUTHORITY_INFERRED")

    # Prior approval cannot silently carry across changed material state.
    if (
        source_state.get("human_gate_decision") == "APPROVED"
        and downstream_state.get("human_gate_decision") == "APPROVED"
    ):
        changed_bindings = [
            field
            for field in MATERIAL_BINDINGS
            if _changed(source_state, downstream_state, field)
        ]

        if changed_bindings:
            reasons.append("PRIOR_APPROVAL_REUSED_AFTER_CHANGE")

    # INADMISSIBLE cannot become approved through the native path.
    if (
        downstream_state.get("mc_admissibility") == "INADMISSIBLE"
        and decision == "APPROVED"
    ):
        reasons.append("INADMISSIBLE_STATE_APPROVED")

    # CONDITIONAL remains constrained.
    if (
        downstream_state.get("mc_admissibility") == "CONDITIONAL"
        and decision == "APPROVED"
    ):
        reasons.append("CONDITIONAL_STATE_APPROVED_WITHOUT_EVIDENCE")

    return tuple(sorted(set(reasons)))


def human_gate_authority_semantic_transition_valid(
    source_state: dict[str, Any],
    downstream_state: dict[str, Any],
) -> bool:
    return not validate_human_gate_authority_transition(
        source_state,
        downstream_state,
    )


def _baseline() -> dict[str, Any]:
    return {
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "analytical_support": "SUPPORTED",
        "selection_state": "SELECTED",
        "mc_admissibility": "ADMISSIBLE",
        "report_state": "PUBLICATION_READY",
        "human_gate_decision": "PENDING",
        "human_decision_ref": None,
        "transition_class": "PUBLICATION",
        "transition_target": "report:ac11:a",
        "requested_scope": "exact-report",
        "room_object_id": "room:ac11:a",
        "room_revision_id": "revision:ac11:a",
        "room_state_root": "state:ac11:a",
        "authorized_view_root": "view:ac11:a",
        "evidence_boundary_ref": "boundary:ac11:a",
        "evidence_ceiling_ref": "ceiling:ac11:a",
        "execution_state": "NOT_EXECUTED",
        "publication_state": "NOT_PUBLISHED",
        "canonical_mutation_state": "NOT_MUTATED",
        "system_population_state": "NOT_POPULATED",
        "claim_authority_state": "NONE",
    }


def main() -> int:
    source = _baseline()

    approved = dict(source)
    approved["human_gate_decision"] = "APPROVED"
    approved["human_decision_ref"] = "human:ac11:approval:a"

    if not human_gate_authority_semantic_transition_valid(
        source,
        approved,
    ):
        print("AC-11 validator self-check: FAIL")
        return 1

    executed = dict(approved)
    executed["execution_state"] = "EXECUTED"

    if human_gate_authority_semantic_transition_valid(
        source,
        executed,
    ):
        print("AC-11 execution separation probe: FAIL")
        return 1

    authority = dict(source)
    authority["authority_state"] = "FULL"

    if human_gate_authority_semantic_transition_valid(
        source,
        authority,
    ):
        print("AC-11 authority probe: FAIL")
        return 1

    print("AC-11 HUMAN-GATE / AUTHORITY SEMANTIC VALIDATOR: READY")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
