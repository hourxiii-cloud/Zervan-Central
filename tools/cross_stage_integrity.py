#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha512
import json
from typing import Tuple


PIPELINE = (
    "PMC",
    "CCR",
    "MC",
    "RAVEN",
    "HUMAN_GATE",
)

VALID = "VALID"
BLOCKED = "BLOCKED"

ADMISSIBLE = "ADMISSIBLE"
CONDITIONAL = "CONDITIONAL"
INADMISSIBLE = "INADMISSIBLE"

NONE = "NONE"
ACTIVE = "ACTIVE"


@dataclass(frozen=True)
class StageState:
    stage: str
    object_id: str
    room_revision_id: str
    room_state_root: str
    authorized_view_root: str

    emitted_candidates: Tuple[str, ...]
    candidate_order: Tuple[str, ...]
    rejected_candidates: Tuple[str, ...]

    uncertainty_references: Tuple[str, ...]
    material_unknown_references: Tuple[str, ...]

    evidence_boundary_reference: str
    evidence_ceiling: int

    governance_constraint_references: Tuple[str, ...]

    claim_strength: int

    mc_disposition: str
    conditional_requirement_references: Tuple[str, ...]
    condition_satisfaction_references: Tuple[str, ...]

    lineage_references: Tuple[str, ...]
    provenance_route: Tuple[str, ...]

    local_valid: bool = True
    authority_state: str = NONE
    human_gate_state: str = ACTIVE


@dataclass(frozen=True)
class CompositionResult:
    composition_id: str
    composition_disposition: str
    failure_reasons: Tuple[str, ...]


def canonical(value) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def identity(payload) -> str:
    return "sha512:" + sha512(
        canonical(payload).encode("utf-8")
    ).hexdigest()


def _lost(before: Tuple[str, ...], after: Tuple[str, ...]) -> bool:
    return not set(before).issubset(set(after))


def _added(before: Tuple[str, ...], after: Tuple[str, ...]) -> bool:
    return not set(after).issubset(set(before))


def _condition_satisfied(state: StageState) -> bool:
    required = set(
        state.conditional_requirement_references
    )
    satisfied = set(
        state.condition_satisfaction_references
    )

    return bool(required) and required.issubset(satisfied)


def validate_composition(
    pmc: StageState,
    ccr: StageState,
    mc: StageState,
    raven: StageState,
    human_gate: StageState,
) -> CompositionResult:

    states = (
        pmc,
        ccr,
        mc,
        raven,
        human_gate,
    )

    reasons = []

    # ---------------------------------------------------------
    # GLOBAL STRUCTURE
    # ---------------------------------------------------------

    if tuple(state.stage for state in states) != PIPELINE:
        reasons.append(
            "STAGE_SEQUENCE_INVALID"
        )

    # Local validity is necessary, never sufficient.
    if not all(state.local_valid for state in states):
        reasons.append(
            "GLOBAL_STATE_IMPOSSIBLE"
        )

    # ---------------------------------------------------------
    # AR-063 — CROSS-OBJECT / ROOM CONTINUITY
    # ---------------------------------------------------------

    object_coordinates = {
        (
            state.object_id,
            state.room_revision_id,
            state.room_state_root,
            state.authorized_view_root,
        )
        for state in states
    }

    if len(object_coordinates) != 1:
        reasons.extend(
            (
                "OBJECT_IDENTITY_CHANGED",
                "CROSS_OBJECT_CONTAMINATION",
            )
        )

    # ---------------------------------------------------------
    # AR-046 / 047 / 048 — PMC -> CCR
    # ---------------------------------------------------------

    if not set(
        ccr.emitted_candidates
    ).issubset(
        set(pmc.emitted_candidates)
    ):
        reasons.append(
            "PMC_CANDIDATE_NOT_EMITTED"
        )

    if _lost(
        pmc.rejected_candidates,
        ccr.rejected_candidates,
    ):
        reasons.append(
            "REJECTED_CANDIDATE_LOST"
        )

    if (
        ccr.candidate_order
        != pmc.candidate_order
    ):
        reasons.append(
            "CANDIDATE_ORDER_CHANGED"
        )

    if _lost(
        pmc.uncertainty_references,
        ccr.uncertainty_references,
    ):
        reasons.append(
            "UNCERTAINTY_ERASED"
        )

    # ---------------------------------------------------------
    # EVIDENCE BOUNDARY — ENTIRE COMPOSITION
    # ---------------------------------------------------------

    boundary = (
        pmc.evidence_boundary_reference
    )

    if any(
        state.evidence_boundary_reference
        != boundary
        for state in states[1:]
    ):
        reasons.append(
            "EVIDENCE_BOUNDARY_CHANGED"
        )

    # ---------------------------------------------------------
    # AR-050 — EVIDENCE CEILING
    #
    # A later stage may narrow supported claim strength.
    # It may not raise the inherited ceiling.
    # ---------------------------------------------------------

    previous_ceiling = pmc.evidence_ceiling

    for state in states[1:]:
        if state.evidence_ceiling > previous_ceiling:
            reasons.append(
                "EVIDENCE_CEILING_RAISED"
            )

        previous_ceiling = min(
            previous_ceiling,
            state.evidence_ceiling,
        )

    # ---------------------------------------------------------
    # AR-049 — GOVERNANCE CONSTRAINT LINEAGE
    # ---------------------------------------------------------

    if _added(
        ccr.governance_constraint_references,
        mc.governance_constraint_references,
    ):
        reasons.append(
            "GOVERNANCE_CONSTRAINT_INVENTED"
        )

    if _lost(
        ccr.governance_constraint_references,
        mc.governance_constraint_references,
    ):
        reasons.append(
            "GOVERNANCE_CONSTRAINT_DROPPED"
        )

    # Once MC has evaluated the governed constraint set,
    # Raven and Human Gate may not silently rewrite it.

    for downstream in (
        raven,
        human_gate,
    ):
        if _added(
            mc.governance_constraint_references,
            downstream.governance_constraint_references,
        ):
            reasons.append(
                "GOVERNANCE_CONSTRAINT_INVENTED"
            )

        if _lost(
            mc.governance_constraint_references,
            downstream.governance_constraint_references,
        ):
            reasons.append(
                "GOVERNANCE_CONSTRAINT_DROPPED"
            )

    # ---------------------------------------------------------
    # AR-051 — CONDITIONAL STATE
    # ---------------------------------------------------------

    if (
        mc.mc_disposition == CONDITIONAL
        and not _condition_satisfied(mc)
    ):
        for downstream in (
            raven,
            human_gate,
        ):
            if downstream.mc_disposition == ADMISSIBLE:
                reasons.append(
                    "CONDITIONAL_STATE_PROMOTED"
                )

    if mc.mc_disposition == INADMISSIBLE:
        for downstream in (
            raven,
            human_gate,
        ):
            if downstream.mc_disposition != INADMISSIBLE:
                reasons.append(
                    "CONDITIONAL_STATE_PROMOTED"
                )

    # ---------------------------------------------------------
    # AR-052 — MATERIAL UNKNOWN / UNCERTAINTY PRESERVATION
    # ---------------------------------------------------------

    previous = pmc

    for state in states[1:]:
        if _lost(
            previous.uncertainty_references,
            state.uncertainty_references,
        ):
            reasons.append(
                "UNCERTAINTY_ERASED"
            )

        if _lost(
            previous.material_unknown_references,
            state.material_unknown_references,
        ):
            reasons.append(
                "MATERIAL_UNKNOWN_SUPPRESSED"
            )

        previous = state

    # ---------------------------------------------------------
    # AR-053 — CLAIM STRENGTH
    #
    # Downstream representation / governance may narrow.
    # It may not strengthen without new analytical state.
    # ---------------------------------------------------------

    previous_strength = pmc.claim_strength

    for state in states[1:]:
        if state.claim_strength > previous_strength:
            reasons.append(
                "CLAIM_STRENGTH_INCREASED"
            )

        previous_strength = min(
            previous_strength,
            state.claim_strength,
        )

    # ---------------------------------------------------------
    # LINEAGE / PROVENANCE
    # ---------------------------------------------------------

    for state in states:
        if not state.lineage_references:
            reasons.append(
                "LINEAGE_BROKEN"
            )

        if not state.provenance_route:
            reasons.append(
                "PROVENANCE_BROKEN"
            )

        if state.authority_state != NONE:
            reasons.append(
                "GLOBAL_STATE_IMPOSSIBLE"
            )

        if state.human_gate_state != ACTIVE:
            reasons.append(
                "GLOBAL_STATE_IMPOSSIBLE"
            )

    # ---------------------------------------------------------
    # AR-064 — AGGREGATE POSSIBILITY
    # ---------------------------------------------------------

    reasons = sorted(set(reasons))

    semantic_failures = [
        reason
        for reason in reasons
        if reason != "GLOBAL_STATE_IMPOSSIBLE"
    ]

    if semantic_failures:
        reasons.append(
            "GLOBAL_STATE_IMPOSSIBLE"
        )

    reasons = tuple(
        sorted(set(reasons))
    )

    payload = {
        "stage_sequence": [
            state.stage
            for state in states
        ],
        "object_coordinates": [
            [
                state.object_id,
                state.room_revision_id,
                state.room_state_root,
                state.authorized_view_root,
            ]
            for state in states
        ],
        "candidate_orders": [
            list(state.candidate_order)
            for state in states
        ],
        "rejected_candidates": [
            list(state.rejected_candidates)
            for state in states
        ],
        "uncertainty": [
            list(state.uncertainty_references)
            for state in states
        ],
        "unknowns": [
            list(state.material_unknown_references)
            for state in states
        ],
        "boundaries": [
            state.evidence_boundary_reference
            for state in states
        ],
        "ceilings": [
            state.evidence_ceiling
            for state in states
        ],
        "governance": [
            list(
                state.governance_constraint_references
            )
            for state in states
        ],
        "claim_strength": [
            state.claim_strength
            for state in states
        ],
        "mc_dispositions": [
            state.mc_disposition
            for state in states
        ],
        "failure_reasons": list(reasons),
    }

    return CompositionResult(
        composition_id=identity(payload),
        composition_disposition=(
            VALID
            if not reasons
            else BLOCKED
        ),
        failure_reasons=reasons,
    )


def make_valid_pipeline():
    common = dict(
        object_id="room:alpha",
        room_revision_id="revision:1",
        room_state_root="state:1",
        authorized_view_root="view:1",

        emitted_candidates=(
            "candidate:a",
            "candidate:b",
        ),
        candidate_order=(
            "candidate:a",
            "candidate:b",
        ),
        rejected_candidates=(
            "candidate:z",
        ),

        uncertainty_references=(
            "uncertainty:1",
        ),
        material_unknown_references=(
            "unknown:1",
        ),

        evidence_boundary_reference=(
            "boundary:1"
        ),
        evidence_ceiling=3,

        governance_constraint_references=(
            "governance:1",
        ),

        claim_strength=2,

        mc_disposition=ADMISSIBLE,
        conditional_requirement_references=(),
        condition_satisfaction_references=(),

        lineage_references=(
            "lineage:1",
        ),
        provenance_route=(
            "origin:1",
            "evidence:1",
        ),

        local_valid=True,
        authority_state=NONE,
        human_gate_state=ACTIVE,
    )

    return tuple(
        StageState(
            stage=stage,
            **common,
        )
        for stage in PIPELINE
    )
