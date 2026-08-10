#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
CAP_ROOT = ROOT / "canonical/observers/capabilities"

PRIMARY = {
    "eagle", "mole", "duck", "wildflower",
    "mockingbird", "platypus", "owl_hoot"
}

CONTROLLED = {
    "osprey", "animal_kingdom", "armadillo"
}

ALL = PRIMARY | CONTROLLED


def load_caps():
    caps = {}

    for path in CAP_ROOT.glob("*_CAPABILITY.json"):
        obj = json.loads(path.read_text(encoding="utf-8"))
        caps[obj["observer_id"]] = obj

    if set(caps) != ALL:
        raise RuntimeError("Observer capability set mismatch")

    return caps


def blocked(reason):
    return {
        "disposition": "BLOCKED",
        "reason": reason,
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "payload_moved": False,
        "analysis_executed": False,
        "composition_executed": False
    }


def route(request):
    if request.get("authority") != "NONE":
        return blocked("AUTHORITY_VIOLATION")

    if request.get("human_gate") != "ACTIVE":
        return blocked("HUMAN_GATE_VIOLATION")

    if request.get("external_runtime") != "DISABLED":
        return blocked("EXTERNAL_RUNTIME_VIOLATION")

    if request.get("external_action") != "DISABLED":
        return blocked("EXTERNAL_ACTION_VIOLATION")

    caps = load_caps()

    needs = set(request.get("needs", []))
    requested = request.get("requested_observers", [])
    permitted = set(request.get("permitted_observers", []))
    modes = request.get("requested_modes", {})

    if len(requested) != len(set(requested)):
        return blocked("DUPLICATE_OBSERVER")

    if set(requested) - ALL:
        return blocked("UNKNOWN_OBSERVER")

    candidates = sorted(
        oid
        for oid, cap in caps.items()
        if needs.intersection(cap["signals"])
    )

    if not requested:
        return {
            "disposition": (
                "CANDIDATES_IDENTIFIED"
                if candidates
                else "NO_OBSERVER_REQUIRED"
            ),
            "candidates": candidates,
            "authority": "NONE",
            "human_gate": "ACTIVE",
            "payload_moved": False,
            "analysis_executed": False,
            "composition_executed": False
        }

    if set(requested) - permitted:
        return blocked("OBSERVER_NOT_PERMITTED")

    selected = []

    for oid in requested:
        cap = caps[oid]
        mode = modes.get(oid)

        if mode not in cap["supported_modes"]:
            return blocked("UNSUPPORTED_MODE:" + oid)

        if oid in PRIMARY - {"owl_hoot"} and mode != "PRIMARY":
            return blocked("PRIMARY_SEAT_VIOLATION:" + oid)

        if oid in CONTROLLED and mode != "CONTROLLED_SUB_OBSERVER":
            return blocked("CONTROLLED_SEAT_VIOLATION:" + oid)

        if oid == "owl_hoot" and mode not in {
            "PRIMARY",
            "BOUNDED_SUB_OBSERVER"
        }:
            return blocked("OWL_HOOT_MODE_VIOLATION")

        selected.append({
            "observer_id": oid,
            "mode": mode,
            "canonical_seat": cap["canonical_seat"]
        })

    return {
        "disposition": "ROUTABLE",
        "selected": selected,
        "candidates": candidates,
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "payload_moved": False,
        "analysis_executed": False,
        "composition_executed": False,
        "composition_state": "DEFERRED_TO_OR_6"
    }


def self_test():
    def req(
        needs=(),
        requested=(),
        modes=None,
        permitted=(),
        authority="NONE",
        human_gate="ACTIVE",
        external_runtime="DISABLED",
        external_action="DISABLED"
    ):
        return route({
            "needs": list(needs),
            "requested_observers": list(requested),
            "requested_modes": modes or {},
            "permitted_observers": list(permitted),
            "authority": authority,
            "human_gate": human_gate,
            "external_runtime": external_runtime,
            "external_action": external_action
        })["disposition"]

    tests = [
        req() == "NO_OBSERVER_REQUIRED",

        req(
            needs=("trajectory",)
        ) == "CANDIDATES_IDENTIFIED",

        req(
            needs=("trajectory",),
            requested=("eagle",),
            modes={"eagle": "PRIMARY"},
            permitted=("eagle",)
        ) == "ROUTABLE",

        req(
            needs=("trajectory", "divergence"),
            requested=("eagle", "duck"),
            modes={
                "eagle": "PRIMARY",
                "duck": "PRIMARY"
            },
            permitted=("eagle", "duck")
        ) == "ROUTABLE",

        req(
            needs=("absence",),
            requested=("owl_hoot",),
            modes={"owl_hoot": "BOUNDED_SUB_OBSERVER"},
            permitted=("owl_hoot",)
        ) == "ROUTABLE",

        req(
            needs=("external_context_pressure",),
            requested=("osprey",),
            modes={"osprey": "CONTROLLED_SUB_OBSERVER"},
            permitted=("osprey",)
        ) == "ROUTABLE",

        req(
            requested=("generic_observer",),
            modes={"generic_observer": "PRIMARY"},
            permitted=("generic_observer",)
        ) == "BLOCKED",

        req(
            requested=("eagle",),
            modes={"eagle": "PRIMARY"},
            permitted=()
        ) == "BLOCKED",

        req(
            requested=("eagle",),
            modes={"eagle": "CONTROLLED_SUB_OBSERVER"},
            permitted=("eagle",)
        ) == "BLOCKED",

        req(
            requested=("osprey",),
            modes={"osprey": "PRIMARY"},
            permitted=("osprey",)
        ) == "BLOCKED",

        req(
            requested=("eagle",),
            modes={"eagle": "PRIMARY"},
            permitted=("eagle",),
            authority="OBSERVER"
        ) == "BLOCKED",

        req(
            requested=("eagle",),
            modes={"eagle": "PRIMARY"},
            permitted=("eagle",),
            human_gate="SATISFIED"
        ) == "BLOCKED",

        req(
            requested=("eagle",),
            modes={"eagle": "PRIMARY"},
            permitted=("eagle",),
            external_runtime="ENABLED"
        ) == "BLOCKED",

        req(
            requested=("eagle",),
            modes={"eagle": "PRIMARY"},
            permitted=("eagle",),
            external_action="ENABLED"
        ) == "BLOCKED"
    ]

    if not all(tests):
        failed = [
            i + 1
            for i, passed in enumerate(tests)
            if not passed
        ]
        print("OR-5 ROUTER SELF-TEST: FAIL", failed)
        return 1

    print("OR-5 ROUTER SELF-TEST: 14/14 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(
        self_test()
        if "--self-test" in sys.argv
        else 0
    )
