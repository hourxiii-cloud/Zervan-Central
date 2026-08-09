#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha512
import json
from typing import Iterable


PROVEN = "PROVEN"
BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class HistoricalWitness:
    reference: str
    historical_state_root: str
    sequence: int
    existed: bool = True


@dataclass(frozen=True)
class LineageEdge:
    parent_reference: str
    child_reference: str
    historical_state_root: str
    sequence: int


@dataclass(frozen=True)
class HistoricalFidelityInput:
    object_id: str
    historical_room_revision_id: str
    historical_state_root: str
    historical_coordinate: str

    historical_question_reference: str
    replay_question_reference: str

    historical_inquiry_envelope_reference: str
    replay_inquiry_envelope_reference: str

    historical_evidence_used_references: tuple[str, ...]
    replay_evidence_used_references: tuple[str, ...]

    historical_evidence_boundary_reference: str
    replay_evidence_boundary_reference: str

    historical_evidence_ceiling_reference: str
    replay_evidence_ceiling_reference: str

    historical_provenance_route: tuple[str, ...]
    replay_provenance_route: tuple[str, ...]

    historical_lineage_edges: tuple[LineageEdge, ...]
    replay_lineage_edges: tuple[LineageEdge, ...]

    historical_collapse_references: tuple[str, ...]
    replay_collapse_references: tuple[str, ...]

    historical_eliminated_alternatives: tuple[str, ...]
    replay_eliminated_alternatives: tuple[str, ...]

    historical_retained_alternatives: tuple[str, ...]
    replay_retained_alternatives: tuple[str, ...]

    historical_deferred_alternatives: tuple[str, ...]
    replay_deferred_alternatives: tuple[str, ...]

    historical_finding_references: tuple[str, ...]
    replay_finding_references: tuple[str, ...]

    historical_rendering_reference: str | None
    replay_rendering_reference: str | None

    historical_cartography_reference: str
    replay_cartography_reference: str

    historical_stick_reference: str
    replay_stick_reference: str

    proof_witnesses: tuple[HistoricalWitness, ...]

    later_evidence_used_to_strengthen_history: bool = False
    replay_reflight_evidence_mixed: bool = False
    regenerated_rendering_claimed_historical: bool = False


@dataclass(frozen=True)
class HistoricalFidelityResult:
    proof_id: str
    proof_disposition: str
    blocking_reasons: tuple[str, ...]


def _witness_map(
    witnesses: Iterable[HistoricalWitness],
) -> dict[str, HistoricalWitness]:
    return {
        witness.reference: witness
        for witness in witnesses
    }


def _required_historical_references(
    record: HistoricalFidelityInput,
) -> tuple[str, ...]:
    refs: list[str] = [
        record.object_id,
        record.historical_room_revision_id,
        record.historical_coordinate,
        record.historical_question_reference,
        record.historical_inquiry_envelope_reference,
        record.historical_evidence_boundary_reference,
        record.historical_evidence_ceiling_reference,
        record.historical_cartography_reference,
        record.historical_stick_reference,
    ]

    refs.extend(record.historical_evidence_used_references)
    refs.extend(record.historical_provenance_route)
    refs.extend(record.historical_collapse_references)
    refs.extend(record.historical_eliminated_alternatives)
    refs.extend(record.historical_retained_alternatives)
    refs.extend(record.historical_deferred_alternatives)
    refs.extend(record.historical_finding_references)

    if record.historical_rendering_reference is not None:
        refs.append(record.historical_rendering_reference)

    for edge in record.historical_lineage_edges:
        refs.extend(
            (
                edge.parent_reference,
                edge.child_reference,
            )
        )

    return tuple(dict.fromkeys(refs))


def _historically_proven(
    reference: str,
    historical_state_root: str,
    witnesses: dict[str, HistoricalWitness],
) -> bool:
    witness = witnesses.get(reference)

    return bool(
        witness
        and witness.existed
        and witness.historical_state_root == historical_state_root
    )


def _lineage_temporally_ordered(
    edges: tuple[LineageEdge, ...],
) -> bool:
    sequences = tuple(edge.sequence for edge in edges)
    return sequences == tuple(sorted(sequences))


def _lineage_bound_to_state(
    edges: tuple[LineageEdge, ...],
    historical_state_root: str,
) -> bool:
    return all(
        edge.historical_state_root == historical_state_root
        for edge in edges
    )


def _lineage_matches(
    historical: tuple[LineageEdge, ...],
    replay: tuple[LineageEdge, ...],
) -> bool:
    return historical == replay


def evaluate(
    record: HistoricalFidelityInput,
) -> HistoricalFidelityResult:
    reasons: set[str] = set()

    if not record.historical_state_root:
        reasons.add("HISTORICAL_STATE_ROOT_MISSING")

    witnesses = _witness_map(record.proof_witnesses)

    required_refs = _required_historical_references(record)

    for reference in required_refs:
        if not _historically_proven(
            reference,
            record.historical_state_root,
            witnesses,
        ):
            reasons.add("HISTORICAL_EXISTENCE_UNPROVEN")
            break

    # AR-005
    if (
        record.replay_question_reference
        != record.historical_question_reference
    ):
        reasons.add("CURRENT_QUESTION_SUBSTITUTED")

    # Historical inquiry cannot silently become current inquiry.
    if (
        record.replay_inquiry_envelope_reference
        != record.historical_inquiry_envelope_reference
    ):
        reasons.add("CURRENT_ONLY_RESOLUTION")

    # AR-006
    if (
        record.replay_evidence_used_references
        != record.historical_evidence_used_references
    ):
        reasons.add("CURRENT_EVIDENCE_REBOUND")

    if (
        record.replay_evidence_boundary_reference
        != record.historical_evidence_boundary_reference
    ):
        reasons.add("CURRENT_EVIDENCE_REBOUND")

    # AR-013
    if (
        record.replay_evidence_ceiling_reference
        != record.historical_evidence_ceiling_reference
        or record.later_evidence_used_to_strengthen_history
    ):
        reasons.add(
            "LATER_EVIDENCE_STRENGTHENED_HISTORY"
        )

    # AR-045
    if record.replay_reflight_evidence_mixed:
        reasons.add("REPLAY_REFLIGHT_EVIDENCE_MIXED")

    # AR-002 / AR-030 / AR-031 / AR-032
    if not record.historical_provenance_route:
        reasons.add("PROVENANCE_MISSING")

    if (
        len(record.replay_provenance_route)
        < len(record.historical_provenance_route)
    ):
        reasons.add("PROVENANCE_TRUNCATED")

    elif (
        record.replay_provenance_route
        != record.historical_provenance_route
    ):
        historical_set = set(
            record.historical_provenance_route
        )
        replay_set = set(record.replay_provenance_route)

        if historical_set == replay_set:
            reasons.add("PROVENANCE_TEMPORAL_REORDER")
        elif replay_set - historical_set:
            reasons.add("PROVENANCE_GRAFT")
        else:
            reasons.add("PROVENANCE_CHAIN_FALSE")

    if not _lineage_temporally_ordered(
        record.historical_lineage_edges
    ):
        reasons.add("PROVENANCE_TEMPORAL_REORDER")

    if not _lineage_bound_to_state(
        record.historical_lineage_edges,
        record.historical_state_root,
    ):
        reasons.add("PROVENANCE_CHAIN_FALSE")

    if not _lineage_matches(
        record.historical_lineage_edges,
        record.replay_lineage_edges,
    ):
        historical_edges = set(
            record.historical_lineage_edges
        )
        replay_edges = set(record.replay_lineage_edges)

        if replay_edges - historical_edges:
            reasons.add("PROVENANCE_GRAFT")

        if historical_edges - replay_edges:
            reasons.add("PROVENANCE_TRUNCATED")

    # AR-007
    if (
        record.replay_collapse_references
        != record.historical_collapse_references
        or
        record.replay_retained_alternatives
        != record.historical_retained_alternatives
        or
        record.replay_deferred_alternatives
        != record.historical_deferred_alternatives
    ):
        reasons.add("COLLAPSE_HISTORY_MUTATED")

    # AR-043
    if (
        record.replay_eliminated_alternatives
        != record.historical_eliminated_alternatives
    ):
        reasons.add("ELIMINATED_ALTERNATIVES_LOST")

    if (
        record.replay_finding_references
        != record.historical_finding_references
    ):
        reasons.add("COLLAPSE_HISTORY_MUTATED")

    # AR-014
    if (
        record.replay_rendering_reference
        != record.historical_rendering_reference
    ):
        if (
            record.historical_rendering_reference is None
            and record.replay_rendering_reference is not None
        ):
            reasons.add(
                "REGENERATED_RENDERING_IMPERSONATES_HISTORICAL"
            )
        else:
            reasons.add("HISTORICAL_EXISTENCE_UNPROVEN")

    if record.regenerated_rendering_claimed_historical:
        reasons.add(
            "REGENERATED_RENDERING_IMPERSONATES_HISTORICAL"
        )

    if (
        record.replay_cartography_reference
        != record.historical_cartography_reference
        or record.replay_stick_reference
        != record.historical_stick_reference
    ):
        reasons.add("CURRENT_ONLY_RESOLUTION")

    if not record.proof_witnesses:
        reasons.add("PROOF_WITNESS_MISSING")

    ordered = tuple(sorted(reasons))

    payload = {
        "object_id": record.object_id,
        "historical_room_revision_id":
            record.historical_room_revision_id,
        "historical_state_root":
            record.historical_state_root,
        "historical_coordinate":
            record.historical_coordinate,
        "blocking_reasons": list(ordered),
    }

    proof_id = (
        "sha512:"
        + sha512(
            json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
    )

    return HistoricalFidelityResult(
        proof_id=proof_id,
        proof_disposition=(
            PROVEN if not ordered else BLOCKED
        ),
        blocking_reasons=ordered,
    )


def make_valid_record() -> HistoricalFidelityInput:
    state = "sha512:" + "2" * 128
    object_id = "sha512:" + "1" * 128

    lineage = (
        LineageEdge(
            "origin:a",
            "evidence:a",
            state,
            1,
        ),
        LineageEdge(
            "evidence:a",
            "finding:a",
            state,
            2,
        ),
    )

    refs = (
        object_id,
        "revision:a",
        "coord:a",
        "question:a",
        "inquiry:a",
        "evidence:a",
        "boundary:a",
        "ceiling:a",
        "origin:a",
        "collapse:a",
        "alternative:eliminated:a",
        "alternative:retained:a",
        "alternative:deferred:a",
        "finding:a",
        "rendering:a",
        "cartography:a",
        "stick:a",
    )

    witnesses = tuple(
        HistoricalWitness(
            reference=ref,
            historical_state_root=state,
            sequence=index,
        )
        for index, ref in enumerate(refs, 1)
    )

    return HistoricalFidelityInput(
        object_id=object_id,
        historical_room_revision_id="revision:a",
        historical_state_root=state,
        historical_coordinate="coord:a",

        historical_question_reference="question:a",
        replay_question_reference="question:a",

        historical_inquiry_envelope_reference="inquiry:a",
        replay_inquiry_envelope_reference="inquiry:a",

        historical_evidence_used_references=("evidence:a",),
        replay_evidence_used_references=("evidence:a",),

        historical_evidence_boundary_reference="boundary:a",
        replay_evidence_boundary_reference="boundary:a",

        historical_evidence_ceiling_reference="ceiling:a",
        replay_evidence_ceiling_reference="ceiling:a",

        historical_provenance_route=(
            "origin:a",
            "evidence:a",
            "finding:a",
        ),
        replay_provenance_route=(
            "origin:a",
            "evidence:a",
            "finding:a",
        ),

        historical_lineage_edges=lineage,
        replay_lineage_edges=lineage,

        historical_collapse_references=("collapse:a",),
        replay_collapse_references=("collapse:a",),

        historical_eliminated_alternatives=(
            "alternative:eliminated:a",
        ),
        replay_eliminated_alternatives=(
            "alternative:eliminated:a",
        ),

        historical_retained_alternatives=(
            "alternative:retained:a",
        ),
        replay_retained_alternatives=(
            "alternative:retained:a",
        ),

        historical_deferred_alternatives=(
            "alternative:deferred:a",
        ),
        replay_deferred_alternatives=(
            "alternative:deferred:a",
        ),

        historical_finding_references=("finding:a",),
        replay_finding_references=("finding:a",),

        historical_rendering_reference="rendering:a",
        replay_rendering_reference="rendering:a",

        historical_cartography_reference="cartography:a",
        replay_cartography_reference="cartography:a",

        historical_stick_reference="stick:a",
        replay_stick_reference="stick:a",

        proof_witnesses=witnesses,
    )
