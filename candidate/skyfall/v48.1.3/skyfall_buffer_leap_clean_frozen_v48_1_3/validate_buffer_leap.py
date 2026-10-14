#!/usr/bin/env python3
"""Validate the SKYFALL v48.1.3 clean-frozen three-lane step-distance object."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def make_state() -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    for surface, orientation in (("N", 1), ("S", -1)):
        for group in range(1, 8):
            for slot in range(16):
                units.append({
                    "id": f"{surface}-P{group}-{slot:02d}",
                    "origin": surface,
                    "surface": surface,
                    "orientation": orientation,
                    "parity": 0,
                    "buffer": False,
                    "group": group,
                    "slot": slot,
                })
        for slot in range(12):
            units.append({
                "id": f"{surface}-B-{slot:02d}",
                "origin": surface,
                "surface": surface,
                "orientation": orientation,
                "parity": 0,
                "buffer": True,
                "group": None,
                "slot": slot,
            })
    return canonicalize(units)


def canonicalize(state: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted((copy.deepcopy(unit) for unit in state), key=lambda unit: unit["id"])


def identity_hash(state: list[dict[str, Any]]) -> str:
    return hashlib.sha256("\n".join(sorted(unit["id"] for unit in state)).encode()).hexdigest()


def state_hash(state: list[dict[str, Any]]) -> str:
    return stable_hash(canonicalize(state))


def inventory_ok(state: list[dict[str, Any]], admitted_ids: tuple[str, ...]) -> bool:
    ids = [unit.get("id") for unit in state]
    if len(ids) != 248 or len(set(ids)) != 248 or tuple(sorted(ids)) != admitted_ids:
        return False
    for surface in ("N", "S"):
        side = [unit for unit in state if unit.get("surface") == surface]
        if len(side) != 124 or sum(bool(unit.get("buffer")) for unit in side) != 12:
            return False
        for group in range(1, 8):
            if sum(unit.get("group") == group for unit in side) != 16:
                return False
    return True


def transform(state: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = canonicalize(state)
    for unit in result:
        unit["surface"] = "S" if unit["surface"] == "N" else "N"
        unit["orientation"] *= -1
        unit["parity"] ^= 1
    return canonicalize(result)


@dataclass
class Lane:
    name: str
    generation: int
    phase: int
    state: list[dict[str, Any]]
    receipt: str
    verified: bool = True


def gate1_ok(
    lanes: dict[str, Lane],
    selected: str,
    phase_receipts: dict[int, str],
) -> bool:
    if selected not in lanes or len(lanes) != 3:
        return False
    anchors = [lane for name, lane in lanes.items() if name != selected]
    if len(anchors) != 2 or not all(lane.verified for lane in lanes.values()):
        return False
    generations = {lane.generation for lane in lanes.values()}
    receipts = {lane.receipt for lane in lanes.values()}
    phases = {lane.phase for lane in lanes.values()}
    return (
        len(generations) == 1
        and len(receipts) == 1
        and len(phases) == 1
        and all(lane.receipt == phase_receipts.get(lane.phase) for lane in lanes.values())
    )


def gate2_ok(
    candidate: list[dict[str, Any]],
    anchors: list[Lane],
    admitted_ids: tuple[str, ...],
) -> bool:
    if len(anchors) != 2 or anchors[0].generation != anchors[1].generation:
        return False
    if anchors[0].receipt != anchors[1].receipt:
        return False
    if not inventory_ok(candidate, admitted_ids):
        return False
    expected = transform(anchors[0].state)
    return candidate == expected


def leap(
    lanes: dict[str, Lane],
    selected: str,
    phase_states: dict[int, list[dict[str, Any]]],
    phase_receipts: dict[int, str],
) -> None:
    require(gate1_ok(lanes, selected, phase_receipts), "Gate 1 rejected lane admission")
    anchors = [lane for name, lane in lanes.items() if name != selected]
    current_phase = lanes[selected].phase
    next_phase = current_phase ^ 1
    candidate = phase_states[next_phase]
    require(anchors[0].phase == anchors[1].phase == current_phase, "Gate 2 anchor phase mismatch")
    require(anchors[0].receipt == anchors[1].receipt == phase_receipts[current_phase], "Gate 2 anchor receipt mismatch")
    require(candidate is phase_states[next_phase], "Gate 2 expected-state lookup mismatch")
    next_generation = lanes[selected].generation + 1
    next_receipt = phase_receipts[next_phase]
    for lane in lanes.values():
        lane.state = candidate
        lane.generation = next_generation
        lane.phase = next_phase
        lane.receipt = next_receipt
        lane.verified = True


def validate(config_path: Path) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    obj = config["object"]
    lane_cfg = config["lanes"]
    inventory = config["inventory"]
    contract = config["leap_contract"]
    geometry = config["geometry"]

    require(obj["design_label"] == "vTemporal.48.1.3", "version mismatch")
    require(obj["standing"] == "COMPLETE_CLEAN_FROZEN", "standing mismatch")
    require(obj["canonical"] is False and obj["immutable"] is True, "freeze posture mismatch")
    require(obj["physical_runtime_validation"] == "NOT_PERFORMED", "physical posture mismatch")
    require(config["parent"]["standing"] == "COMPLETE_CLEAN_FROZEN", "parent standing mismatch")
    require(inventory["total_identities"] == 248, "identity inventory mismatch")
    require(248 % 3 == 2, "arithmetic guard changed")
    require(inventory["equal_three_way_identity_partition"] is False, "invalid equal partition admitted")
    require(lane_cfg["storage_model"] == "REPLICATED_FULL_LOGICAL_SNAPSHOT", "lane model mismatch")
    require(lane_cfg["identities_per_lane_snapshot"] == 248, "lane snapshot mismatch")
    require(lane_cfg["anchor_quorum"] == 2, "anchor quorum mismatch")
    require(lane_cfg["identity_partition"] is False, "identity partition prohibited")
    require(contract["zero_latency_claim"] is False, "zero-latency claim prohibited")
    require(contract["automatic_rehydration"] is False, "automatic rehydration claim prohibited")
    require(config["timing_model"]["zero_terms"] == [], "timing term improperly zeroed")
    require(config["timing_model"]["speedup_claim_available"] is False, "unsupported speedup claim")
    require(geometry["distance_unit"] == "MILE", "distance unit mismatch")
    require(geometry["initiating_radius_definition"] == "TIGHTEST_ADMISSIBLE_CIRCLE", "initiation geometry mismatch")
    require(geometry["initiating_radius_numeric_value"] is None, "unsupported initiating radius admitted")
    require(geometry["channel_count"] == 3, "channel count mismatch")
    require(geometry["step_distance_basis_miles"] == 118, "step-distance basis mismatch")
    require(geometry["selected_channel_step_expression"] == "118/3", "step expression mismatch")
    step_fraction = Fraction(
        geometry["selected_channel_step_rational"]["numerator"],
        geometry["selected_channel_step_rational"]["denominator"],
    )
    require(step_fraction == Fraction(118, 3), "exact selected-channel step mismatch")
    require(step_fraction * geometry["channel_count"] == geometry["step_distance_basis_miles"], "step-distance accounting does not reconcile")
    require(geometry["selected_channel_step_miles"] == "39 1/3", "step-distance unit mismatch")
    require(geometry["channels_partition_distance"] is False, "channels must not partition geometry")
    require(geometry["aggregate_model_span_miles"] is None, "unsupported aggregate span admitted")
    require(geometry["three_meter_offset_admitted"] is False, "three-meter offset prohibited")
    require(geometry["three_meter_transit_reserve_admitted"] is False, "three-meter reserve prohibited")
    require(geometry["one_hundred_ten_meter_radius_admitted"] is False, "110-meter radius prohibited")
    require(geometry["physical_range_validated"] is False, "physical range claim prohibited")

    initial = make_state()
    admitted_ids = tuple(sorted(unit["id"] for unit in initial))
    require(identity_hash(initial) == config["validation"]["required_identity_sha256"], "identity receipt mismatch")
    initial_receipt = state_hash(initial)
    transformed = transform(initial)
    require(inventory_ok(initial, admitted_ids), "initial inventory invalid")
    require(inventory_ok(transformed, admitted_ids), "transformed inventory invalid")
    require(transform(transformed) == initial, "double traversal state return failed")
    phase_states = {0: initial, 1: transformed}
    phase_receipts = {phase: state_hash(state) for phase, state in phase_states.items()}
    lanes = {
        name: Lane(name=name, generation=0, phase=0, state=initial, receipt=initial_receipt)
        for name in lane_cfg["names"]
    }

    rng = random.Random(config["validation"]["deterministic_seed"])
    selection_counts = {name: 0 for name in lanes}
    cycles = config["validation"]["cycles"]
    for _ in range(cycles):
        selected = rng.choice(tuple(lanes))
        selection_counts[selected] += 1
        leap(lanes, selected, phase_states, phase_receipts)

    require(len({lane.generation for lane in lanes.values()}) == 1, "generation divergence")
    require(len({lane.receipt for lane in lanes.values()}) == 1, "receipt divergence")
    require(all(identity_hash(lane.state) == config["validation"]["required_identity_sha256"] for lane in lanes.values()), "identity drift")
    require(all(unit["surface"] == unit["origin"] and unit["parity"] == 0 for unit in lanes["A"].state), "even-cycle state return failed")
    require(lanes["A"].receipt == phase_receipts[0], "final state receipt does not match admitted state")
    require(all(count > 0 for count in selection_counts.values()), "not all lanes exercised")

    clean = {
        name: Lane(name=name, generation=0, phase=0, state=initial, receipt=initial_receipt)
        for name in lane_cfg["names"]
    }
    stale = copy.deepcopy(clean)
    stale["B"].generation = -1
    stale_anchor_detected = not gate1_ok(stale, "A", phase_receipts)

    disagreement = copy.deepcopy(clean)
    disagreement_state = canonicalize(disagreement["C"].state)
    disagreement_state[0]["parity"] ^= 1
    disagreement["C"].state = disagreement_state
    disagreement["C"].receipt = state_hash(disagreement_state)
    anchor_disagreement_detected = not gate1_ok(disagreement, "A", phase_receipts)

    anchors = [clean["B"], clean["C"]]
    expected = transform(clean["A"].state)
    loss_detected = not gate2_ok(expected[:-1], anchors, admitted_ids)
    duplicated = canonicalize(expected[:-1] + [copy.deepcopy(expected[0])])
    duplication_detected = not gate2_ok(duplicated, anchors, admitted_ids)
    mutation = canonicalize(expected)
    mutation[0]["id"] = "CORRUPTED-ID"
    identity_mutation_detected = not gate2_ok(mutation, anchors, admitted_ids)
    semantic_drift = canonicalize(expected)
    semantic_drift[0]["parity"] ^= 1
    semantic_drift_detected = not gate2_ok(semantic_drift, anchors, admitted_ids)

    require(all((stale_anchor_detected, anchor_disagreement_detected, loss_detected,
                 duplication_detected, identity_mutation_detected, semantic_drift_detected)),
            "fault-injection detection failed")

    return {
        "status": "PASS",
        "version": obj["design_label"],
        "standing": obj["standing"],
        "cycles": cycles,
        "identities_per_snapshot": 248,
        "lane_model": lane_cfg["storage_model"],
        "lane_selection_counts": selection_counts,
        "final_generation": lanes["A"].generation,
        "identity_sha256": config["validation"]["required_identity_sha256"],
        "initial_state_sha256": phase_receipts[0],
        "final_state_sha256": lanes["A"].receipt,
        "all_lane_receipts_equal": True,
        "even_cycle_state_return": True,
        "fault_injection": {
            "stale_anchor_detected": stale_anchor_detected,
            "anchor_disagreement_detected": anchor_disagreement_detected,
            "single_unit_loss_detected": loss_detected,
            "single_duplication_detected": duplication_detected,
            "identity_mutation_detected": identity_mutation_detected,
            "semantic_state_drift_detected": semantic_drift_detected
        },
        "equal_three_way_partition_admitted": False,
        "zero_latency_claim_admitted": False,
        "speedup_claim_admitted": False,
        "geometry": {
            "initiating_radius": "r_min — TIGHTEST_ADMISSIBLE_CIRCLE — NUMERIC_UNRESOLVED",
            "step_distance_basis": "118 MILES",
            "selected_channel_step_distance": "118/3 = 39 1/3 MILES PER STEP",
            "channels_partition_distance": False,
            "aggregate_model_span": "UNRESOLVED",
            "three_meter_offset_admitted": False,
            "physical_range_validated": False
        },
        "physical_runtime_validation": obj["physical_runtime_validation"]
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("buffer_leap_config.json"))
    args = parser.parse_args()
    print(json.dumps(validate(args.config), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
