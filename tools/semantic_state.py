#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
from typing import Iterable


# ---------------------------------------------------------------------------
# AC-05 — Explicit Semantic-State Geometry
# ---------------------------------------------------------------------------

AUTHORITY_STATE = "NONE"
HUMAN_GATE_STATE = "ACTIVE"

# Existence
KNOWN_PRESENT = "KNOWN_PRESENT"
KNOWN_ABSENT = "KNOWN_ABSENT"
UNRESOLVED_EXISTENCE = "UNRESOLVED_EXISTENCE"

EXISTENCE_STATES = frozenset({
    KNOWN_PRESENT,
    KNOWN_ABSENT,
    UNRESOLVED_EXISTENCE,
})

# Epistemic
KNOWN = "KNOWN"
UNKNOWN = "UNKNOWN"
UNRESOLVED = "UNRESOLVED"
CONTRADICTED = "CONTRADICTED"

EPISTEMIC_STATES = frozenset({
    KNOWN,
    UNKNOWN,
    UNRESOLVED,
    CONTRADICTED,
})

# Accessibility
AVAILABLE = "AVAILABLE"
RESTRICTED = "RESTRICTED"
UNAVAILABLE = "UNAVAILABLE"

ACCESSIBILITY_STATES = frozenset({
    AVAILABLE,
    RESTRICTED,
    UNAVAILABLE,
})

# Topology
TOPOLOGY_KNOWN = "TOPOLOGY_KNOWN"
TOPOLOGY_RESTRICTED = "TOPOLOGY_RESTRICTED"
TOPOLOGY_UNRESOLVED = "TOPOLOGY_UNRESOLVED"
TOPOLOGY_ABSENT = "TOPOLOGY_ABSENT"

TOPOLOGY_STATES = frozenset({
    TOPOLOGY_KNOWN,
    TOPOLOGY_RESTRICTED,
    TOPOLOGY_UNRESOLVED,
    TOPOLOGY_ABSENT,
})

# Hydration
UNHYDRATED = "UNHYDRATED"
PARTIAL = "PARTIAL"
COMPLETE = "COMPLETE"

HYDRATION_STATES = frozenset({
    UNHYDRATED,
    PARTIAL,
    COMPLETE,
})

# Operational
PERMITTED = "PERMITTED"
BLOCKED = "BLOCKED"
INACTIVE = "INACTIVE"
ACTIVE = "ACTIVE"
COMPLETED = "COMPLETED"
FAILED = "FAILED"

OPERATIONAL_STATES = frozenset({
    PERMITTED,
    BLOCKED,
    INACTIVE,
    ACTIVE,
    COMPLETED,
    FAILED,
})

# Decision
NOT_REQUIRED = "NOT_REQUIRED"
PENDING = "PENDING"
APPROVED = "APPROVED"
DENIED = "DENIED"

DECISION_STATES = frozenset({
    NOT_REQUIRED,
    PENDING,
    APPROVED,
    DENIED,
})

# Representation
FULL = "FULL"
REDACTED = "REDACTED"
EXISTENCE_ONLY = "EXISTENCE_ONLY"
SUMMARY = "SUMMARY"
OMITTED_BY_VIEW = "OMITTED_BY_VIEW"

REPRESENTATION_STATES = frozenset({
    FULL,
    REDACTED,
    EXISTENCE_ONLY,
    SUMMARY,
    OMITTED_BY_VIEW,
})

DIMENSIONS = (
    "existence_state",
    "epistemic_state",
    "accessibility_state",
    "topology_state",
    "hydration_state",
    "operational_state",
    "decision_state",
    "representation_state",
)


@dataclass(frozen=True)
class SemanticStateCoordinate:
    semantic_state_id: str
    subject_reference: str

    existence_state: str
    epistemic_state: str
    accessibility_state: str
    topology_state: str
    hydration_state: str
    hydration_boundary_reference: str | None
    operational_state: str
    decision_state: str
    representation_state: str

    evidence_boundary_reference: str
    evidence_ceiling_reference: str

    restriction_references: tuple[str, ...]
    unresolved_references: tuple[str, ...]
    provenance_route: tuple[str, ...]

    authority_state: str = AUTHORITY_STATE
    human_gate_state: str = HUMAN_GATE_STATE


@dataclass(frozen=True)
class SemanticTransition:
    prior_semantic_state_id: str
    resulting_semantic_state_id: str
    requested_dimensions: tuple[str, ...]
    changed_dimensions: tuple[str, ...]
    evidence_references: tuple[str, ...]
    authorization_references: tuple[str, ...]
    hydration_evidence_references: tuple[str, ...]
    provenance_route: tuple[str, ...]
    transition_reason: str


class SemanticStateError(ValueError):
    pass


def _tuple(values: Iterable[str] | None) -> tuple[str, ...]:
    if values is None:
        return ()

    return tuple(values)


def _canonical_payload(
    coordinate: SemanticStateCoordinate,
) -> dict:
    payload = asdict(coordinate)
    payload.pop("semantic_state_id", None)

    for field in (
        "restriction_references",
        "unresolved_references",
        "provenance_route",
    ):
        payload[field] = list(payload[field])

    return payload


def semantic_state_identity(
    coordinate: SemanticStateCoordinate,
) -> str:
    payload = _canonical_payload(coordinate)

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return "sha512:" + hashlib.sha512(
        encoded
    ).hexdigest()


def validate_coordinate(
    coordinate: SemanticStateCoordinate,
) -> list[str]:
    errors: list[str] = []

    checks = (
        (
            "existence_state",
            coordinate.existence_state,
            EXISTENCE_STATES,
        ),
        (
            "epistemic_state",
            coordinate.epistemic_state,
            EPISTEMIC_STATES,
        ),
        (
            "accessibility_state",
            coordinate.accessibility_state,
            ACCESSIBILITY_STATES,
        ),
        (
            "topology_state",
            coordinate.topology_state,
            TOPOLOGY_STATES,
        ),
        (
            "hydration_state",
            coordinate.hydration_state,
            HYDRATION_STATES,
        ),
        (
            "operational_state",
            coordinate.operational_state,
            OPERATIONAL_STATES,
        ),
        (
            "decision_state",
            coordinate.decision_state,
            DECISION_STATES,
        ),
        (
            "representation_state",
            coordinate.representation_state,
            REPRESENTATION_STATES,
        ),
    )

    for name, value, allowed in checks:
        if value not in allowed:
            errors.append(
                f"invalid {name}: {value}"
            )

    if not coordinate.subject_reference:
        errors.append(
            "subject reference required"
        )

    if not coordinate.evidence_boundary_reference:
        errors.append(
            "evidence boundary required"
        )

    if not coordinate.evidence_ceiling_reference:
        errors.append(
            "evidence ceiling required"
        )

    if not coordinate.provenance_route:
        errors.append(
            "provenance route required"
        )

    if (
        coordinate.authority_state
        != AUTHORITY_STATE
    ):
        errors.append(
            "authority state must remain NONE"
        )

    if (
        coordinate.human_gate_state
        != HUMAN_GATE_STATE
    ):
        errors.append(
            "Human Gate state must remain ACTIVE"
        )

    # Restriction is existence-aware.
    if (
        coordinate.accessibility_state
        == RESTRICTED
        and coordinate.existence_state
        == KNOWN_ABSENT
    ):
        errors.append(
            "restricted material cannot be represented as absent"
        )

    if (
        coordinate.accessibility_state
        == RESTRICTED
        and not coordinate.restriction_references
    ):
        errors.append(
            "restricted state requires restriction reference"
        )

    # Restricted topology must survive representation.
    if (
        coordinate.topology_state
        == TOPOLOGY_RESTRICTED
        and not coordinate.restriction_references
    ):
        errors.append(
            "restricted topology requires restriction reference"
        )

    # Partial means unresolved territory still exists.
    if (
        coordinate.hydration_state
        == PARTIAL
        and not coordinate.hydration_boundary_reference
    ):
        errors.append(
            "partial hydration requires hydration boundary"
        )

    if (
        coordinate.hydration_state
        == PARTIAL
        and not (
            coordinate.unresolved_references
            or coordinate.restriction_references
        )
    ):
        errors.append(
            "partial hydration must preserve unresolved or restricted surface"
        )

    # Unknown/unresolved semantic state must remain attributable.
    if (
        coordinate.epistemic_state
        in {
            UNKNOWN,
            UNRESOLVED,
            CONTRADICTED,
        }
        and not coordinate.unresolved_references
    ):
        errors.append(
            "unknown/unresolved epistemic state requires unresolved reference"
        )

    expected_id = semantic_state_identity(
        coordinate
    )

    if (
        coordinate.semantic_state_id
        != expected_id
    ):
        errors.append(
            "semantic state identity mismatch"
        )

    return errors


def make_coordinate(
    *,
    subject_reference: str,
    existence_state: str,
    epistemic_state: str,
    accessibility_state: str,
    topology_state: str,
    hydration_state: str,
    hydration_boundary_reference: str | None,
    operational_state: str,
    decision_state: str,
    representation_state: str,
    evidence_boundary_reference: str,
    evidence_ceiling_reference: str,
    restriction_references: Iterable[str] = (),
    unresolved_references: Iterable[str] = (),
    provenance_route: Iterable[str],
) -> SemanticStateCoordinate:
    coordinate = SemanticStateCoordinate(
        semantic_state_id="",
        subject_reference=subject_reference,
        existence_state=existence_state,
        epistemic_state=epistemic_state,
        accessibility_state=accessibility_state,
        topology_state=topology_state,
        hydration_state=hydration_state,
        hydration_boundary_reference=
            hydration_boundary_reference,
        operational_state=operational_state,
        decision_state=decision_state,
        representation_state=representation_state,
        evidence_boundary_reference=
            evidence_boundary_reference,
        evidence_ceiling_reference=
            evidence_ceiling_reference,
        restriction_references=_tuple(
            restriction_references
        ),
        unresolved_references=_tuple(
            unresolved_references
        ),
        provenance_route=_tuple(
            provenance_route
        ),
    )

    coordinate = replace(
        coordinate,
        semantic_state_id=
            semantic_state_identity(
                coordinate
            ),
    )

    errors = validate_coordinate(
        coordinate
    )

    if errors:
        raise SemanticStateError(
            "; ".join(errors)
        )

    return coordinate


def changed_dimensions(
    prior: SemanticStateCoordinate,
    result: SemanticStateCoordinate,
) -> tuple[str, ...]:
    return tuple(
        dimension
        for dimension in DIMENSIONS
        if getattr(prior, dimension)
        != getattr(result, dimension)
    )


def validate_transition(
    prior: SemanticStateCoordinate,
    result: SemanticStateCoordinate,
    *,
    requested_dimensions: Iterable[str],
    evidence_references: Iterable[str] = (),
    authorization_references: Iterable[str] = (),
    hydration_evidence_references: Iterable[str] = (),
) -> list[str]:
    errors: list[str] = []

    errors.extend(
        f"prior: {error}"
        for error in validate_coordinate(prior)
    )

    errors.extend(
        f"result: {error}"
        for error in validate_coordinate(result)
    )

    requested = set(
        requested_dimensions
    )

    invalid_requested = (
        requested
        - set(DIMENSIONS)
    )

    if invalid_requested:
        errors.append(
            "unknown requested dimension: "
            + ", ".join(
                sorted(invalid_requested)
            )
        )

    changed = set(
        changed_dimensions(
            prior,
            result,
        )
    )

    undeclared = (
        changed
        - requested
    )

    if undeclared:
        errors.append(
            "cross-dimension mutation: "
            + ", ".join(
                sorted(undeclared)
            )
        )

    evidence = tuple(
        evidence_references
    )

    authorization = tuple(
        authorization_references
    )

    hydration_evidence = tuple(
        hydration_evidence_references
    )

    # --------------------------------------------------------
    # Existence movement requires evidence.
    # --------------------------------------------------------

    if (
        prior.existence_state
        == UNRESOLVED_EXISTENCE
        and result.existence_state
        in {
            KNOWN_PRESENT,
            KNOWN_ABSENT,
        }
        and not evidence
    ):
        errors.append(
            "existence resolution requires attributable evidence"
        )

    # UNKNOWN / UNRESOLVED / CONTRADICTED -> KNOWN
    # requires attributable evidence.
    if (
        prior.epistemic_state
        in {
            UNKNOWN,
            UNRESOLVED,
            CONTRADICTED,
        }
        and result.epistemic_state
        == KNOWN
        and not evidence
    ):
        errors.append(
            "epistemic promotion requires attributable evidence"
        )

    # --------------------------------------------------------
    # Accessibility movement requires authorization.
    # --------------------------------------------------------

    if (
        prior.accessibility_state
        in {
            RESTRICTED,
            UNAVAILABLE,
        }
        and result.accessibility_state
        == AVAILABLE
        and not authorization
    ):
        errors.append(
            "accessibility promotion requires attributable authorization"
        )

    # Restriction cannot mutate existence into absence.
    if (
        prior.accessibility_state
        == RESTRICTED
        and result.existence_state
        == KNOWN_ABSENT
    ):
        errors.append(
            "restriction cannot collapse into absence"
        )

    # --------------------------------------------------------
    # Topology movement requires evidence.
    # --------------------------------------------------------

    if (
        prior.topology_state
        in {
            TOPOLOGY_RESTRICTED,
            TOPOLOGY_UNRESOLVED,
        }
        and result.topology_state
        in {
            TOPOLOGY_KNOWN,
            TOPOLOGY_ABSENT,
        }
        and not evidence
    ):
        errors.append(
            "topology resolution requires attributable evidence"
        )

    if (
        prior.topology_state
        == TOPOLOGY_RESTRICTED
        and result.topology_state
        == TOPOLOGY_ABSENT
        and not evidence
    ):
        errors.append(
            "restricted topology cannot disappear"
        )

    # --------------------------------------------------------
    # Hydration movement requires hydration evidence.
    # --------------------------------------------------------

    if (
        prior.hydration_state
        in {
            UNHYDRATED,
            PARTIAL,
        }
        and result.hydration_state
        == COMPLETE
        and not hydration_evidence
    ):
        errors.append(
            "hydration completion requires attributable hydration evidence"
        )

    # --------------------------------------------------------
    # Decision movement requires authorization.
    # --------------------------------------------------------

    if (
        prior.decision_state
        == PENDING
        and result.decision_state
        in {
            APPROVED,
            DENIED,
        }
        and not authorization
    ):
        errors.append(
            "decision resolution requires attributable authorization"
        )

    # BLOCKED and DENIED belong to different dimensions.
    if (
        prior.operational_state
        == BLOCKED
        and result.decision_state
        == DENIED
        and not authorization
    ):
        errors.append(
            "blocked operation cannot manufacture denial"
        )

    # --------------------------------------------------------
    # Representation cannot improve underlying reality.
    # --------------------------------------------------------

    representation_only = (
        changed
        and changed
        <= {
            "representation_state",
        }
    )

    if representation_only:
        for dimension in (
            "existence_state",
            "epistemic_state",
            "accessibility_state",
            "topology_state",
            "hydration_state",
            "operational_state",
            "decision_state",
        ):
            if (
                getattr(prior, dimension)
                != getattr(result, dimension)
            ):
                errors.append(
                    "representation transform mutated "
                    + dimension
                )

    return sorted(
        set(errors)
    )


def make_transition(
    prior: SemanticStateCoordinate,
    result: SemanticStateCoordinate,
    *,
    requested_dimensions: Iterable[str],
    evidence_references: Iterable[str] = (),
    authorization_references: Iterable[str] = (),
    hydration_evidence_references: Iterable[str] = (),
    provenance_route: Iterable[str],
    transition_reason: str,
) -> SemanticTransition:
    requested = tuple(
        requested_dimensions
    )

    evidence = _tuple(
        evidence_references
    )

    authorization = _tuple(
        authorization_references
    )

    hydration_evidence = _tuple(
        hydration_evidence_references
    )

    errors = validate_transition(
        prior,
        result,
        requested_dimensions=requested,
        evidence_references=evidence,
        authorization_references=
            authorization,
        hydration_evidence_references=
            hydration_evidence,
    )

    if errors:
        raise SemanticStateError(
            "; ".join(errors)
        )

    if not transition_reason:
        raise SemanticStateError(
            "transition reason required"
        )

    route = _tuple(
        provenance_route
    )

    if not route:
        raise SemanticStateError(
            "transition provenance required"
        )

    return SemanticTransition(
        prior_semantic_state_id=
            prior.semantic_state_id,
        resulting_semantic_state_id=
            result.semantic_state_id,
        requested_dimensions=requested,
        changed_dimensions=
            changed_dimensions(
                prior,
                result,
            ),
        evidence_references=evidence,
        authorization_references=
            authorization,
        hydration_evidence_references=
            hydration_evidence,
        provenance_route=route,
        transition_reason=
            transition_reason,
    )
