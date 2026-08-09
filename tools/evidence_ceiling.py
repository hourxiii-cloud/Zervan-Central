#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from tools.collision_boundary import (
    CLEAN,
    COLLISION,
    UNRESOLVED_CONTEXT,
)


ROW_LOCAL = "ROW_LOCAL"
GROUP_LOCAL = "GROUP_LOCAL"
EVENT_CONTEXT = "EVENT_CONTEXT"
NATIVE_CONTEXT = "NATIVE_CONTEXT"

OBSERVED = "OBSERVED"
INFERRED = "INFERRED"
UNKNOWN = "UNKNOWN"

ADMISSIBLE = "ADMISSIBLE"
CONDITIONAL = "CONDITIONAL"
INADMISSIBLE = "INADMISSIBLE"
UNRESOLVED = "UNRESOLVED"

AUTHORITY_STATE = "NONE"
HUMAN_GATE_STATE = "ACTIVE"


SCOPE_ORDER = {
    ROW_LOCAL: 0,
    GROUP_LOCAL: 1,
    EVENT_CONTEXT: 2,
    NATIVE_CONTEXT: 3,
}

EPISTEMIC_ORDER = {
    UNKNOWN: 0,
    INFERRED: 1,
    OBSERVED: 2,
}


@dataclass(frozen=True)
class ClaimEvaluation:
    claim_id: str
    claim_text: str
    epistemic_class: str
    available_evidence_scope: str
    required_evidence_scope: str
    evidence_boundary_reference: str
    evidence_ceiling_reference: str
    evidence_references: tuple[str, ...]
    missing_evidence_requirements: tuple[str, ...]
    collision_disposition: str
    confidence: Optional[float]
    claim_disposition: str
    disposition_reasons: tuple[str, ...]
    provenance_route: tuple[str, ...]
    authority_state: str = AUTHORITY_STATE
    human_gate_state: str = HUMAN_GATE_STATE


def _validate_scope(scope: str) -> None:
    if scope not in SCOPE_ORDER:
        raise ValueError(
            f"invalid evidence scope: {scope}"
        )


def _validate_epistemic_class(
    epistemic_class: str,
) -> None:
    if epistemic_class not in EPISTEMIC_ORDER:
        raise ValueError(
            f"invalid epistemic class: {epistemic_class}"
        )


def _validate_collision_disposition(
    disposition: str,
) -> None:
    if disposition not in {
        CLEAN,
        COLLISION,
        UNRESOLVED_CONTEXT,
    }:
        raise ValueError(
            "invalid collision disposition: "
            f"{disposition}"
        )


def _validate_confidence(
    confidence: Optional[float],
) -> None:
    if confidence is None:
        return

    if isinstance(confidence, bool):
        raise ValueError(
            "confidence must be numeric or null"
        )

    if not isinstance(
        confidence,
        (int, float),
    ):
        raise ValueError(
            "confidence must be numeric or null"
        )

    if not 0.0 <= float(confidence) <= 1.0:
        raise ValueError(
            "confidence must be between 0 and 1"
        )


def evaluate_claim(
    *,
    claim_id: str,
    claim_text: str,
    epistemic_class: str,
    available_evidence_scope: str,
    required_evidence_scope: str,
    evidence_boundary_reference: str,
    evidence_ceiling_reference: str,
    evidence_references: Iterable[str],
    missing_evidence_requirements: Iterable[str] = (),
    collision_disposition: str = CLEAN,
    confidence: Optional[float] = None,
    provenance_route: Iterable[str],
) -> ClaimEvaluation:
    _validate_scope(
        available_evidence_scope
    )
    _validate_scope(
        required_evidence_scope
    )
    _validate_epistemic_class(
        epistemic_class
    )
    _validate_collision_disposition(
        collision_disposition
    )
    _validate_confidence(
        confidence
    )

    if not claim_id:
        raise ValueError(
            "claim_id is required"
        )

    if not claim_text:
        raise ValueError(
            "claim_text is required"
        )

    if not evidence_boundary_reference:
        raise ValueError(
            "evidence boundary is required"
        )

    if not evidence_ceiling_reference:
        raise ValueError(
            "evidence ceiling is required"
        )

    evidence = tuple(
        str(reference)
        for reference in evidence_references
        if str(reference)
    )

    provenance = tuple(
        str(reference)
        for reference in provenance_route
        if str(reference)
    )

    if not provenance:
        raise ValueError(
            "provenance route is required"
        )

    missing = tuple(sorted(set(
        str(requirement)
        for requirement
        in missing_evidence_requirements
        if str(requirement)
    )))

    reasons: list[str] = []

    available_rank = SCOPE_ORDER[
        available_evidence_scope
    ]
    required_rank = SCOPE_ORDER[
        required_evidence_scope
    ]

    if (
        collision_disposition
        == UNRESOLVED_CONTEXT
    ):
        reasons.append(
            "COLLISION_CONTEXT_UNRESOLVED"
        )

    if (
        collision_disposition == COLLISION
        and required_rank
        > SCOPE_ORDER[GROUP_LOCAL]
    ):
        reasons.append(
            "COLLISION_CANNOT_ESTABLISH_EVENT_CONTEXT"
        )

    if required_rank > available_rank:
        reasons.append(
            "REQUIRED_SCOPE_EXCEEDS_AVAILABLE_SCOPE"
        )

    if missing:
        reasons.append(
            "REQUIRED_EVIDENCE_MISSING"
        )

    if epistemic_class == UNKNOWN:
        reasons.append(
            "CLAIM_REMAINS_UNKNOWN"
        )

    if (
        collision_disposition == COLLISION
        and epistemic_class == OBSERVED
        and required_rank > SCOPE_ORDER[ROW_LOCAL]
    ):
        reasons.append(
            "COLLISION_NOT_OBSERVED_MACRO_CONTEXT"
        )

    if (
        collision_disposition
        == UNRESOLVED_CONTEXT
    ):
        disposition = UNRESOLVED

    elif epistemic_class == UNKNOWN:
        disposition = UNRESOLVED

    elif (
        collision_disposition == COLLISION
        and required_rank
        > SCOPE_ORDER[GROUP_LOCAL]
    ):
        disposition = INADMISSIBLE

    elif (
        required_rank > available_rank
        or missing
    ):
        disposition = CONDITIONAL

    else:
        disposition = ADMISSIBLE

    return ClaimEvaluation(
        claim_id=claim_id,
        claim_text=claim_text,
        epistemic_class=epistemic_class,
        available_evidence_scope=
            available_evidence_scope,
        required_evidence_scope=
            required_evidence_scope,
        evidence_boundary_reference=
            evidence_boundary_reference,
        evidence_ceiling_reference=
            evidence_ceiling_reference,
        evidence_references=evidence,
        missing_evidence_requirements=
            missing,
        collision_disposition=
            collision_disposition,
        confidence=(
            None
            if confidence is None
            else float(confidence)
        ),
        claim_disposition=disposition,
        disposition_reasons=tuple(
            sorted(set(reasons))
        ),
        provenance_route=provenance,
    )


def validate_epistemic_transition(
    *,
    prior_class: str,
    requested_class: str,
    new_evidence_references: Iterable[str] = (),
) -> bool:
    _validate_epistemic_class(
        prior_class
    )
    _validate_epistemic_class(
        requested_class
    )

    prior_rank = EPISTEMIC_ORDER[
        prior_class
    ]
    requested_rank = EPISTEMIC_ORDER[
        requested_class
    ]

    if requested_rank <= prior_rank:
        return True

    new_evidence = tuple(
        str(reference)
        for reference in new_evidence_references
        if str(reference)
    )

    return bool(new_evidence)


def validate_scope_promotion(
    *,
    prior_scope: str,
    requested_scope: str,
    new_evidence_references: Iterable[str] = (),
) -> bool:
    _validate_scope(
        prior_scope
    )
    _validate_scope(
        requested_scope
    )

    if (
        SCOPE_ORDER[requested_scope]
        <= SCOPE_ORDER[prior_scope]
    ):
        return True

    new_evidence = tuple(
        str(reference)
        for reference in new_evidence_references
        if str(reference)
    )

    return bool(new_evidence)


def confidence_changes_evidence_scope(
    *,
    available_scope: str,
    confidence_before: Optional[float],
    confidence_after: Optional[float],
) -> str:
    _validate_scope(
        available_scope
    )
    _validate_confidence(
        confidence_before
    )
    _validate_confidence(
        confidence_after
    )

    # Confidence is metadata.
    # It never changes evidence scope.
    return available_scope
