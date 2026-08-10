#!/usr/bin/env python3
import sys

SURFACES = ("PMC", "CCR", "MC", "RAVEN", "AUDIT")


def blocked(reason):
    return {
        "disposition": "BLOCKED",
        "reason": reason,
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "canonical_mutation": False,
        "evidence_mutation": False,
        "claim_ceiling_increased": False
    }


def integrate(composition):
    if not isinstance(composition, dict):
        return blocked("COMPOSITION_NOT_OBJECT")

    if composition.get("disposition") != "COMPOSED":
        return blocked("COMPOSITION_NOT_COMPLETE")

    if composition.get("authority") != "NONE":
        return blocked("AUTHORITY_VIOLATION")

    if composition.get("human_gate") != "ACTIVE":
        return blocked("HUMAN_GATE_VIOLATION")

    if composition.get("primary_evidence_mutated") is not False:
        return blocked("PRIMARY_EVIDENCE_MUTATION")

    if composition.get("canonical_state_mutated") is not False:
        return blocked("CANONICAL_STATE_MUTATION")

    if composition.get("claim_ceiling_increased") is not False:
        return blocked("CLAIM_CEILING_ESCALATION")

    primary = composition.get("primary_results", [])
    controlled = composition.get("controlled_pressure", [])

    if not isinstance(primary, list):
        return blocked("PRIMARY_RESULTS_INVALID")

    if not isinstance(controlled, list):
        return blocked("CONTROLLED_PRESSURE_INVALID")

    primary_ids = [
        item.get("observer_id")
        for item in primary
    ]

    controlled_ids = [
        item.get("observer_id")
        for item in controlled
    ]

    if len(primary_ids) != len(set(primary_ids)):
        return blocked("PRIMARY_IDENTITY_DUPLICATION")

    if len(controlled_ids) != len(set(controlled_ids)):
        return blocked("CONTROLLED_IDENTITY_DUPLICATION")

    common = set(primary_ids) & set(controlled_ids)

    if common:
        return blocked("OBSERVER_CLASS_COLLISION")

    envelope = {
        "room_id": composition.get("room_id"),
        "room_revision": composition.get("room_revision"),
        "observer_count": composition.get("observer_count"),
        "primary_observer_count": composition.get(
            "primary_observer_count"
        ),
        "controlled_pressure_count": composition.get(
            "controlled_pressure_count"
        ),
        "primary_results": primary,
        "controlled_pressure": controlled,
        "composition_signals": composition.get(
            "composition_signals", []
        ),
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "voting_performed": False,
        "averaging_performed": False,
        "winner_selected": False,
        "forced_consensus": False,
        "silent_reconciliation": False,
        "canonical_mutation": False,
        "evidence_mutation": False,
        "claim_ceiling_increased": False
    }

    return {
        "disposition": "INTEGRATION_READY",
        "authority": "NONE",
        "human_gate": "ACTIVE",

        "PMC": {
            "role": "RECEIVE_OBSERVER_COMPOSITION_FOR_PMC_CONSIDERATION",
            "input": envelope,
            "may_mutate_observer_results": False,
            "may_create_authority": False
        },

        "CCR": {
            "role": "RECEIVE_OBSERVER_COMPOSITION_FOR_CCR_CONSIDERATION",
            "input": envelope,
            "may_mutate_observer_results": False,
            "may_create_authority": False
        },

        "MC": {
            "role": "RECEIVE_OBSERVER_COMPOSITION_FOR_MC_CONSIDERATION",
            "input": envelope,
            "may_mutate_observer_results": False,
            "may_create_authority": False
        },

        "RAVEN": {
            "role": "RECEIVE_OBSERVER_COMPOSITION_FOR_REPORTING",
            "input": envelope,
            "observer_identity_preserved": True,
            "controlled_pressure_preserved": True,
            "publication_authority_created": False
        },

        "AUDIT": {
            "role": "RECEIVE_OBSERVER_COMPOSITION_FOR_INTEGRITY_REVIEW",
            "input": envelope,
            "observer_identity_preserved": True,
            "provenance_preserved": True,
            "approval_authority_created": False
        },

        "canonical_mutation": False,
        "evidence_mutation": False,
        "claim_ceiling_increased": False
    }


def sample():
    primary = {
        "observer_id": "eagle",
        "observer_class": "PRIMARY",
        "observer_mode": "PRIMARY",
        "operation_id": "op:eagle",
        "authorized_view": "view:a",
        "disposition": "OBSERVED",
        "observations": [],
        "unresolved_conditions": [],
        "scars": [],
        "provenance": {
            "room_id": "room:test",
            "room_revision": "revision:test"
        }
    }

    controlled = {
        "observer_id": "osprey",
        "observer_class": "CONTROLLED_SUB_OBSERVER",
        "observer_mode": "CONTROLLED_SUB_OBSERVER",
        "operation_id": "op:osprey",
        "authorized_view": "view:a",
        "disposition": "OBSERVED",
        "observations": [],
        "unresolved_conditions": [],
        "scars": [],
        "provenance": {
            "room_id": "room:test",
            "room_revision": "revision:test"
        }
    }

    return {
        "disposition": "COMPOSED",
        "room_id": "room:test",
        "room_revision": "revision:test",
        "observer_count": 2,
        "primary_observer_count": 1,
        "controlled_pressure_count": 1,
        "primary_results": [primary],
        "controlled_pressure": [controlled],
        "composition_signals": [
            "CONTROLLED_PRESSURE_PRESENT"
        ],
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "voting_performed": False,
        "averaging_performed": False,
        "winner_selected": False,
        "forced_consensus": False,
        "silent_reconciliation": False,
        "primary_evidence_mutated": False,
        "canonical_state_mutated": False,
        "claim_ceiling_increased": False
    }


def self_test():
    tests = []

    good = sample()
    out = integrate(good)

    tests.append(
        out["disposition"] == "INTEGRATION_READY"
    )

    tests.append(
        all(surface in out for surface in SURFACES)
    )

    tests.append(
        all(
            out[surface]["input"]["primary_results"][0]
            ["observer_id"] == "eagle"
            for surface in SURFACES
        )
    )

    tests.append(
        all(
            out[surface]["input"]["controlled_pressure"][0]
            ["observer_id"] == "osprey"
            for surface in SURFACES
        )
    )

    tests.append(
        out["RAVEN"]["publication_authority_created"]
        is False
    )

    tests.append(
        out["AUDIT"]["approval_authority_created"]
        is False
    )

    bad = sample()
    bad["authority"] = "OBSERVER"
    tests.append(
        integrate(bad)["disposition"] == "BLOCKED"
    )

    bad = sample()
    bad["human_gate"] = "SATISFIED"
    tests.append(
        integrate(bad)["disposition"] == "BLOCKED"
    )

    bad = sample()
    bad["primary_evidence_mutated"] = True
    tests.append(
        integrate(bad)["disposition"] == "BLOCKED"
    )

    bad = sample()
    bad["canonical_state_mutated"] = True
    tests.append(
        integrate(bad)["disposition"] == "BLOCKED"
    )

    bad = sample()
    bad["claim_ceiling_increased"] = True
    tests.append(
        integrate(bad)["disposition"] == "BLOCKED"
    )

    bad = sample()
    bad["controlled_pressure"][0]["observer_id"] = "eagle"
    tests.append(
        integrate(bad)["disposition"] == "BLOCKED"
    )

    if not all(tests):
        print(
            "OR-7 INTEGRATION SELF-TEST: FAIL",
            [
                i + 1
                for i, ok in enumerate(tests)
                if not ok
            ]
        )
        return 1

    print("OR-7 INTEGRATION SELF-TEST: 12/12 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(
        self_test()
        if "--self-test" in sys.argv
        else 0
    )
