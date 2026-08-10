#!/usr/bin/env python3
import sys

CONTROLLED = {
    "osprey",
    "animal_kingdom",
    "armadillo"
}


def blocked(reason):
    return {
        "disposition": "BLOCKED",
        "reason": reason,
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "primary_evidence_mutated": False,
        "canonical_state_mutated": False,
        "claim_ceiling_increased": False,
        "primary_output_steered": False
    }


def isolate(result):
    if not isinstance(result, dict):
        return blocked("RESULT_NOT_OBJECT")

    oid = result.get("observer_id")

    if oid not in CONTROLLED:
        return blocked("NOT_CONTROLLED_SUB_OBSERVER")

    if result.get("observer_class") != "CONTROLLED_SUB_OBSERVER":
        return blocked("CONTROLLED_CLASS_VIOLATION")

    if result.get("observer_mode") != "CONTROLLED_SUB_OBSERVER":
        return blocked("CONTROLLED_MODE_VIOLATION")

    if result.get("authority") != "NONE":
        return blocked("AUTHORITY_VIOLATION")

    if result.get("human_gate") != "ACTIVE":
        return blocked("HUMAN_GATE_VIOLATION")

    if result.get("primary_evidence_mutated") is not False:
        return blocked("PRIMARY_EVIDENCE_MUTATION")

    if result.get("canonical_state_mutated") is not False:
        return blocked("CANONICAL_STATE_MUTATION")

    if result.get("claim_ceiling_increased") is not False:
        return blocked("CLAIM_CEILING_ESCALATION")

    pressure = {
        "observer_id": oid,
        "observer_class": "CONTROLLED_SUB_OBSERVER",
        "observer_mode": "CONTROLLED_SUB_OBSERVER",
        "operation_id": result.get("operation_id"),
        "disposition": result.get("disposition"),
        "observations": result.get("observations", []),
        "unresolved_conditions": result.get(
            "unresolved_conditions", []
        ),
        "scars": result.get("scars", []),
        "provenance": result.get("provenance", {}),
        "pressure_status": "ISOLATED",
        "factual_promotion": False,
        "primary_evidence_status": "UNCHANGED",
        "primary_output_steering": False,
        "authority_created": False,
        "canonical_state_mutated": False,
        "claim_ceiling_increased": False
    }

    if oid == "osprey":
        pressure["pressure_type"] = "EXTERNAL_CONTEXT"
        pressure["external_collection_authorized"] = False
        pressure["external_runtime_authorized"] = False
        pressure["external_action_authorized"] = False
        pressure["external_context_promoted_to_primary_evidence"] = False

    elif oid == "animal_kingdom":
        pressure["pressure_type"] = "SYNTHETIC_ADVERSARIAL"
        pressure["synthetic_input_promoted_to_fact"] = False
        pressure["synthetic_input_promoted_to_primary_evidence"] = False

    elif oid == "armadillo":
        pressure["pressure_type"] = "INTEGRITY_AUTHENTICATION_ATTRIBUTION"
        pressure["challenge_establishes_authenticity"] = False
        pressure["challenge_establishes_attribution"] = False

    return {
        "disposition": "PRESSURE_ISOLATED",
        "controlled_pressure": pressure,
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "primary_evidence_mutated": False,
        "canonical_state_mutated": False,
        "claim_ceiling_increased": False,
        "primary_output_steered": False
    }


def sample(oid):
    return {
        "result_type": "ZERVAN_V41_OBSERVER_RESULT",
        "result_version": "1.0",
        "observer_id": oid,
        "observer_class": "CONTROLLED_SUB_OBSERVER",
        "observer_mode": "CONTROLLED_SUB_OBSERVER",
        "operation_id": "operation:" + oid,
        "disposition": "OBSERVED",
        "observations": [{
            "observation_type": oid + "_pressure",
            "statement": "Bounded controlled pressure.",
            "evidence_refs": ["evidence:test"],
            "confidence_status": "BOUNDED"
        }],
        "unresolved_conditions": [],
        "scars": [],
        "provenance": {
            "observer_id": oid,
            "observer_class": "CONTROLLED_SUB_OBSERVER",
            "observer_mode": "CONTROLLED_SUB_OBSERVER",
            "operation_id": "operation:" + oid,
            "room_id": "room:test",
            "room_revision": "revision:test",
            "authorized_view": "view:test",
            "evidence_refs": ["evidence:test"],
            "input_provenance_refs": ["provenance:test"],
            "claim_ceiling": "OBSERVATIONAL",
            "disposition": "OBSERVED",
            "sequence": 1,
            "timestamp": None,
            "downstream_refs": []
        },
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "primary_evidence_mutated": False,
        "canonical_state_mutated": False,
        "claim_ceiling_increased": False
    }


def self_test():
    tests = []

    # 1. Osprey isolated.
    out = isolate(sample("osprey"))
    tests.append(
        out["disposition"] == "PRESSURE_ISOLATED"
        and out["controlled_pressure"]["pressure_type"]
            == "EXTERNAL_CONTEXT"
    )

    # 2. Osprey cannot acquire collection/action/runtime authority.
    p = out["controlled_pressure"]
    tests.append(
        p["external_collection_authorized"] is False
        and p["external_runtime_authorized"] is False
        and p["external_action_authorized"] is False
        and p["external_context_promoted_to_primary_evidence"] is False
    )

    # 3. AnimalKingdom isolated.
    out = isolate(sample("animal_kingdom"))
    tests.append(
        out["disposition"] == "PRESSURE_ISOLATED"
        and out["controlled_pressure"]["pressure_type"]
            == "SYNTHETIC_ADVERSARIAL"
    )

    # 4. Synthetic remains synthetic.
    p = out["controlled_pressure"]
    tests.append(
        p["synthetic_input_promoted_to_fact"] is False
        and p["synthetic_input_promoted_to_primary_evidence"] is False
    )

    # 5. Armadillo isolated.
    out = isolate(sample("armadillo"))
    tests.append(
        out["disposition"] == "PRESSURE_ISOLATED"
        and out["controlled_pressure"]["pressure_type"]
            == "INTEGRITY_AUTHENTICATION_ATTRIBUTION"
    )

    # 6. Challenge does not establish authenticity/attribution.
    p = out["controlled_pressure"]
    tests.append(
        p["challenge_establishes_authenticity"] is False
        and p["challenge_establishes_attribution"] is False
    )

    # 7. Primary Observer rejected from pressure isolator.
    bad = sample("osprey")
    bad["observer_id"] = "eagle"
    tests.append(
        isolate(bad)["disposition"] == "BLOCKED"
    )

    # 8. Controlled class violation blocked.
    bad = sample("osprey")
    bad["observer_class"] = "PRIMARY"
    tests.append(
        isolate(bad)["disposition"] == "BLOCKED"
    )

    # 9. Controlled mode violation blocked.
    bad = sample("osprey")
    bad["observer_mode"] = "PRIMARY"
    tests.append(
        isolate(bad)["disposition"] == "BLOCKED"
    )

    # 10. Authority promotion blocked.
    bad = sample("osprey")
    bad["authority"] = "OBSERVER"
    tests.append(
        isolate(bad)["disposition"] == "BLOCKED"
    )

    # 11. Human Gate substitution blocked.
    bad = sample("osprey")
    bad["human_gate"] = "SATISFIED"
    tests.append(
        isolate(bad)["disposition"] == "BLOCKED"
    )

    # 12. Primary evidence mutation blocked.
    bad = sample("animal_kingdom")
    bad["primary_evidence_mutated"] = True
    tests.append(
        isolate(bad)["disposition"] == "BLOCKED"
    )

    # 13. Canonical mutation blocked.
    bad = sample("armadillo")
    bad["canonical_state_mutated"] = True
    tests.append(
        isolate(bad)["disposition"] == "BLOCKED"
    )

    # 14. Claim ceiling increase blocked.
    bad = sample("armadillo")
    bad["claim_ceiling_increased"] = True
    tests.append(
        isolate(bad)["disposition"] == "BLOCKED"
    )

    # 15. Successful isolation still cannot steer primary output.
    out = isolate(sample("animal_kingdom"))
    tests.append(
        out["primary_output_steered"] is False
        and out["controlled_pressure"]["primary_output_steering"] is False
    )

    if not all(tests):
        print(
            "OR-8 PRESSURE SELF-TEST: FAIL",
            [
                i + 1
                for i, ok in enumerate(tests)
                if not ok
            ]
        )
        return 1

    print("OR-8 PRESSURE SELF-TEST: 15/15 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(
        self_test()
        if "--self-test" in sys.argv
        else 0
    )
