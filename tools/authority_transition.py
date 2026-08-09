#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
from typing import Iterable


AUTHORITY_STATE = "NONE"
HUMAN_GATE_STATE = "ACTIVE"

PENDING = "PENDING"
APPROVED = "APPROVED"
DENIED = "DENIED"

ADMISSIBLE = "ADMISSIBLE"
CONDITIONAL = "CONDITIONAL"
INADMISSIBLE = "INADMISSIBLE"

SINGLE = "SINGLE"
BOUNDED_REPEAT = "BOUNDED_REPEAT"

UNUSED = "UNUSED"
PARTIALLY_CONSUMED = "PARTIALLY_CONSUMED"
CONSUMED = "CONSUMED"
INVALIDATED = "INVALIDATED"

PREPARATION = "PREPARATION"
EXECUTION = "EXECUTION"

TRANSITION_CLASSES = frozenset({
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
})


class AuthorityTransitionError(ValueError):
    pass


@dataclass(frozen=True)
class AuthorizationBinding:
    authorization_binding_id: str
    human_gate_decision_id: str
    decision_state: str

    transition_class: str
    transition_target: str

    object_id: str
    room_revision_id: str
    room_state_root: str
    authorized_view_root: str

    evidence_boundary_reference: str
    evidence_ceiling_reference: str

    approved_scope: tuple[str, ...]

    mc_disposition: str
    conditional_requirement_references: tuple[str, ...]
    condition_satisfaction_references: tuple[str, ...]

    execution_cardinality: str
    maximum_execution_count: int
    successful_execution_count: int
    consumption_state: str

    invalidation_reasons: tuple[str, ...]
    provenance_route: tuple[str, ...]

    authority_state: str = AUTHORITY_STATE
    human_gate_state: str = HUMAN_GATE_STATE


@dataclass(frozen=True)
class ExecutionRequest:
    transition_class: str
    transition_target: str

    object_id: str
    room_revision_id: str
    room_state_root: str
    authorized_view_root: str

    evidence_boundary_reference: str
    evidence_ceiling_reference: str

    requested_scope: tuple[str, ...]

    operation_label: str
    authority_bearing_effect: bool

    provenance_route: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionReceipt:
    execution_id: str
    authorization_binding_id: str
    human_gate_decision_id: str

    transition_class: str
    transition_target: str

    object_id: str
    room_revision_id: str
    room_state_root: str
    authorized_view_root: str

    evidence_boundary_reference: str
    evidence_ceiling_reference: str

    approved_scope: tuple[str, ...]
    requested_execution_scope: tuple[str, ...]

    execution_attempt: int
    execution_state: str

    provenance_route: tuple[str, ...]

    authority_state: str = AUTHORITY_STATE
    human_gate_state: str = HUMAN_GATE_STATE


def _tuple(
    values: Iterable[str] | None,
) -> tuple[str, ...]:
    if values is None:
        return ()

    return tuple(values)


def _canonical(value) -> bytes:
    payload = asdict(value)

    for key, item in tuple(
        payload.items()
    ):
        if isinstance(item, tuple):
            payload[key] = list(item)

    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _identity(
    value,
    identity_field: str,
) -> str:
    payload = asdict(value)
    payload.pop(
        identity_field,
        None,
    )

    for key, item in tuple(
        payload.items()
    ):
        if isinstance(item, tuple):
            payload[key] = list(item)

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return (
        "sha512:"
        + hashlib.sha512(
            encoded
        ).hexdigest()
    )


def authorization_identity(
    binding: AuthorizationBinding,
) -> str:
    return _identity(
        binding,
        "authorization_binding_id",
    )


def execution_identity(
    receipt: ExecutionReceipt,
) -> str:
    return _identity(
        receipt,
        "execution_id",
    )


def validate_binding(
    binding: AuthorizationBinding,
) -> list[str]:
    errors: list[str] = []

    if (
        binding.decision_state
        not in {
            PENDING,
            APPROVED,
            DENIED,
        }
    ):
        errors.append(
            "invalid Human Gate decision state"
        )

    if (
        binding.transition_class
        not in TRANSITION_CLASSES
    ):
        errors.append(
            "unknown authority-bearing transition class"
        )

    for name in (
        "human_gate_decision_id",
        "transition_target",
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
    ):
        if not getattr(
            binding,
            name,
        ):
            errors.append(
                f"{name} required"
            )

    if not binding.approved_scope:
        errors.append(
            "approved scope required"
        )

    if not binding.provenance_route:
        errors.append(
            "authorization provenance required"
        )

    if (
        binding.mc_disposition
        not in {
            ADMISSIBLE,
            CONDITIONAL,
            INADMISSIBLE,
        }
    ):
        errors.append(
            "invalid MC disposition"
        )

    if (
        binding.mc_disposition
        == CONDITIONAL
        and not
        binding.conditional_requirement_references
    ):
        errors.append(
            "CONDITIONAL requires explicit conditions"
        )

    if (
        binding.execution_cardinality
        not in {
            SINGLE,
            BOUNDED_REPEAT,
        }
    ):
        errors.append(
            "invalid execution cardinality"
        )

    if (
        binding.execution_cardinality
        == SINGLE
        and binding.maximum_execution_count
        != 1
    ):
        errors.append(
            "SINGLE authorization maximum must equal 1"
        )

    if (
        binding.execution_cardinality
        == BOUNDED_REPEAT
        and binding.maximum_execution_count
        < 1
    ):
        errors.append(
            "BOUNDED_REPEAT requires positive maximum"
        )

    if (
        binding.successful_execution_count
        < 0
    ):
        errors.append(
            "successful execution count cannot be negative"
        )

    if (
        binding.successful_execution_count
        > binding.maximum_execution_count
    ):
        errors.append(
            "successful execution count exceeds authorization"
        )

    if (
        binding.consumption_state
        not in {
            UNUSED,
            PARTIALLY_CONSUMED,
            CONSUMED,
            INVALIDATED,
        }
    ):
        errors.append(
            "invalid consumption state"
        )

    if (
        binding.invalidation_reasons
        and binding.consumption_state
        != INVALIDATED
    ):
        errors.append(
            "invalidation reasons require INVALIDATED state"
        )

    if (
        binding.consumption_state
        == INVALIDATED
        and not binding.invalidation_reasons
    ):
        errors.append(
            "INVALIDATED requires reason"
        )

    if (
        binding.consumption_state
        == CONSUMED
        and binding.successful_execution_count
        < binding.maximum_execution_count
    ):
        errors.append(
            "CONSUMED before cardinality exhaustion"
        )

    if (
        binding.authority_state
        != AUTHORITY_STATE
    ):
        errors.append(
            "Authority must remain NONE"
        )

    if (
        binding.human_gate_state
        != HUMAN_GATE_STATE
    ):
        errors.append(
            "Human Gate must remain ACTIVE"
        )

    expected = authorization_identity(
        binding
    )

    if (
        binding.authorization_binding_id
        != expected
    ):
        errors.append(
            "authorization binding identity mismatch"
        )

    return sorted(
        set(errors)
    )


def make_binding(
    *,
    human_gate_decision_id: str,
    decision_state: str,
    transition_class: str,
    transition_target: str,
    object_id: str,
    room_revision_id: str,
    room_state_root: str,
    authorized_view_root: str,
    evidence_boundary_reference: str,
    evidence_ceiling_reference: str,
    approved_scope: Iterable[str],
    mc_disposition: str,
    conditional_requirement_references:
        Iterable[str] = (),
    condition_satisfaction_references:
        Iterable[str] = (),
    execution_cardinality: str = SINGLE,
    maximum_execution_count: int = 1,
    successful_execution_count: int = 0,
    consumption_state: str = UNUSED,
    invalidation_reasons:
        Iterable[str] = (),
    provenance_route: Iterable[str],
) -> AuthorizationBinding:
    binding = AuthorizationBinding(
        authorization_binding_id="",
        human_gate_decision_id=
            human_gate_decision_id,
        decision_state=decision_state,
        transition_class=
            transition_class,
        transition_target=
            transition_target,
        object_id=object_id,
        room_revision_id=
            room_revision_id,
        room_state_root=
            room_state_root,
        authorized_view_root=
            authorized_view_root,
        evidence_boundary_reference=
            evidence_boundary_reference,
        evidence_ceiling_reference=
            evidence_ceiling_reference,
        approved_scope=_tuple(
            approved_scope
        ),
        mc_disposition=
            mc_disposition,
        conditional_requirement_references=
            _tuple(
                conditional_requirement_references
            ),
        condition_satisfaction_references=
            _tuple(
                condition_satisfaction_references
            ),
        execution_cardinality=
            execution_cardinality,
        maximum_execution_count=
            maximum_execution_count,
        successful_execution_count=
            successful_execution_count,
        consumption_state=
            consumption_state,
        invalidation_reasons=
            _tuple(
                invalidation_reasons
            ),
        provenance_route=
            _tuple(
                provenance_route
            ),
    )

    binding = replace(
        binding,
        authorization_binding_id=
            authorization_identity(
                binding
            ),
    )

    errors = validate_binding(
        binding
    )

    if errors:
        raise AuthorityTransitionError(
            "; ".join(errors)
        )

    return binding


def classify_operation(
    request: ExecutionRequest,
) -> str:
    if request.authority_bearing_effect:
        return EXECUTION

    return PREPARATION


def validate_execution(
    binding: AuthorizationBinding,
    request: ExecutionRequest,
) -> list[str]:
    errors = list(
        validate_binding(
            binding
        )
    )

    if (
        binding.decision_state
        != APPROVED
    ):
        errors.append(
            "Human Gate approval required"
        )

    if (
        binding.mc_disposition
        == INADMISSIBLE
    ):
        errors.append(
            "MC INADMISSIBLE blocks execution"
        )

    if (
        binding.mc_disposition
        == CONDITIONAL
    ):
        required = set(
            binding
            .conditional_requirement_references
        )

        satisfied = set(
            binding
            .condition_satisfaction_references
        )

        missing = sorted(
            required - satisfied
        )

        if missing:
            errors.append(
                "unsatisfied conditional requirements: "
                + ", ".join(missing)
            )

    comparisons = (
        (
            "transition class",
            binding.transition_class,
            request.transition_class,
        ),
        (
            "transition target",
            binding.transition_target,
            request.transition_target,
        ),
        (
            "Room",
            binding.object_id,
            request.object_id,
        ),
        (
            "Room revision",
            binding.room_revision_id,
            request.room_revision_id,
        ),
        (
            "Room state",
            binding.room_state_root,
            request.room_state_root,
        ),
        (
            "Authorized View",
            binding.authorized_view_root,
            request.authorized_view_root,
        ),
        (
            "evidence boundary",
            binding.evidence_boundary_reference,
            request.evidence_boundary_reference,
        ),
        (
            "evidence ceiling",
            binding.evidence_ceiling_reference,
            request.evidence_ceiling_reference,
        ),
    )

    for label, approved, requested in comparisons:
        if approved != requested:
            errors.append(
                f"{label} mismatch"
            )

    approved_scope = set(
        binding.approved_scope
    )

    requested_scope = set(
        request.requested_scope
    )

    if not requested_scope:
        errors.append(
            "requested execution scope required"
        )

    if not requested_scope.issubset(
        approved_scope
    ):
        errors.append(
            "execution scope exceeds approval"
        )

    if (
        binding.consumption_state
        == INVALIDATED
    ):
        errors.append(
            "invalidated authorization cannot execute"
        )

    if (
        binding.consumption_state
        == CONSUMED
    ):
        errors.append(
            "consumed authorization cannot execute"
        )

    if (
        binding.successful_execution_count
        >= binding.maximum_execution_count
    ):
        errors.append(
            "execution cardinality exhausted"
        )

    if not request.provenance_route:
        errors.append(
            "execution provenance required"
        )

    # AR-059: labels do not control the boundary.
    if (
        request.operation_label
        == PREPARATION
        and request.authority_bearing_effect
    ):
        errors.append(
            "authority-bearing execution disguised as preparation"
        )

    return sorted(
        set(errors)
    )


def execution_eligible(
    binding: AuthorizationBinding,
    request: ExecutionRequest,
) -> bool:
    return not validate_execution(
        binding,
        request,
    )


def make_execution_receipt(
    binding: AuthorizationBinding,
    request: ExecutionRequest,
    *,
    execution_state: str,
) -> ExecutionReceipt:
    errors = validate_execution(
        binding,
        request,
    )

    if errors:
        raise AuthorityTransitionError(
            "; ".join(errors)
        )

    attempt = (
        binding.successful_execution_count
        + 1
    )

    receipt = ExecutionReceipt(
        execution_id="",
        authorization_binding_id=
            binding.authorization_binding_id,
        human_gate_decision_id=
            binding.human_gate_decision_id,
        transition_class=
            request.transition_class,
        transition_target=
            request.transition_target,
        object_id=
            request.object_id,
        room_revision_id=
            request.room_revision_id,
        room_state_root=
            request.room_state_root,
        authorized_view_root=
            request.authorized_view_root,
        evidence_boundary_reference=
            request.evidence_boundary_reference,
        evidence_ceiling_reference=
            request.evidence_ceiling_reference,
        approved_scope=
            binding.approved_scope,
        requested_execution_scope=
            request.requested_scope,
        execution_attempt=attempt,
        execution_state=
            execution_state,
        provenance_route=
            request.provenance_route,
    )

    return replace(
        receipt,
        execution_id=
            execution_identity(
                receipt
            ),
    )


def consume_success(
    binding: AuthorizationBinding,
) -> AuthorizationBinding:
    errors = validate_binding(
        binding
    )

    if errors:
        raise AuthorityTransitionError(
            "; ".join(errors)
        )

    if (
        binding.consumption_state
        == INVALIDATED
    ):
        raise AuthorityTransitionError(
            "invalidated authorization cannot be consumed"
        )

    if (
        binding.successful_execution_count
        >= binding.maximum_execution_count
    ):
        raise AuthorityTransitionError(
            "execution cardinality exhausted"
        )

    count = (
        binding.successful_execution_count
        + 1
    )

    state = (
        CONSUMED
        if count
        >= binding.maximum_execution_count
        else PARTIALLY_CONSUMED
    )

    updated = replace(
        binding,
        authorization_binding_id="",
        successful_execution_count=
            count,
        consumption_state=state,
    )

    return replace(
        updated,
        authorization_binding_id=
            authorization_identity(
                updated
            ),
    )


def invalidate(
    binding: AuthorizationBinding,
    *,
    reasons: Iterable[str],
) -> AuthorizationBinding:
    reasons = _tuple(
        reasons
    )

    if not reasons:
        raise AuthorityTransitionError(
            "invalidation reason required"
        )

    updated = replace(
        binding,
        authorization_binding_id="",
        consumption_state=
            INVALIDATED,
        invalidation_reasons=
            reasons,
    )

    return replace(
        updated,
        authorization_binding_id=
            authorization_identity(
                updated
            ),
    )
