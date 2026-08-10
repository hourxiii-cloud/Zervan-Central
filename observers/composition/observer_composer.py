#!/usr/bin/env python3
import sys

PRIMARY = {
    "eagle", "mole", "duck", "wildflower",
    "mockingbird", "platypus", "owl_hoot"
}

CONTROLLED = {
    "osprey", "animal_kingdom", "armadillo"
}

ALL = PRIMARY | CONTROLLED


def blocked(reason):
    return {
        "disposition": "BLOCKED",
        "reason": reason,
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "voting_performed": False,
        "averaging_performed": False,
        "winner_selected": False,
        "forced_consensus": False,
        "primary_evidence_mutated": False,
        "canonical_state_mutated": False,
        "claim_ceiling_increased": False
    }


def compose(results):
    if not isinstance(results, list):
        return blocked("RESULT_SET_NOT_ARRAY")

    if len(results) < 2:
        return blocked("MULTI_OBSERVER_REQUIRES_TWO_OR_MORE_RESULTS")

    ids = [r.get("observer_id") for r in results]

    if any(x not in ALL for x in ids):
        return blocked("UNKNOWN_OBSERVER")

    if len(ids) != len(set(ids)):
        return blocked("DUPLICATE_OBSERVER_RESULT")

    # Shared territory must remain one Room/revision.
    room_ids = {r.get("provenance", {}).get("room_id") for r in results}
    revisions = {r.get("provenance", {}).get("room_revision") for r in results}

    if len(room_ids) != 1:
        return blocked("ROOM_ID_DIVERGENCE")

    if len(revisions) != 1:
        return blocked("ROOM_REVISION_DIVERGENCE")

    # Observer outputs cannot acquire authority during composition.
    for r in results:
        if r.get("authority") != "NONE":
            return blocked("AUTHORITY_VIOLATION")

        if r.get("human_gate") != "ACTIVE":
            return blocked("HUMAN_GATE_VIOLATION")

        if r.get("primary_evidence_mutated") is not False:
            return blocked("PRIMARY_EVIDENCE_MUTATION")

        if r.get("canonical_state_mutated") is not False:
            return blocked("CANONICAL_STATE_MUTATION")

        if r.get("claim_ceiling_increased") is not False:
            return blocked("CLAIM_CEILING_ESCALATION")

        oid = r["observer_id"]
        cls = r.get("observer_class")
        mode = r.get("observer_mode")

        if oid in PRIMARY and cls != "PRIMARY":
            return blocked("PRIMARY_CLASS_VIOLATION:" + oid)

        if oid in CONTROLLED and cls != "CONTROLLED_SUB_OBSERVER":
            return blocked("CONTROLLED_CLASS_VIOLATION:" + oid)

        if oid in PRIMARY - {"owl_hoot"} and mode != "PRIMARY":
            return blocked("PRIMARY_MODE_VIOLATION:" + oid)

        if oid in CONTROLLED and mode != "CONTROLLED_SUB_OBSERVER":
            return blocked("CONTROLLED_MODE_VIOLATION:" + oid)

        if oid == "owl_hoot" and mode not in {
            "PRIMARY", "BOUNDED_SUB_OBSERVER"
        }:
            return blocked("OWL_HOOT_MODE_VIOLATION")

    primary_results = []
    controlled_pressure = []
    views = set()
    dispositions = set()

    for r in results:
        oid = r["observer_id"]
        prov = r["provenance"]

        views.add(prov.get("authorized_view"))
        dispositions.add(r.get("disposition"))

        preserved = {
            "observer_id": oid,
            "observer_class": r["observer_class"],
            "observer_mode": r["observer_mode"],
            "operation_id": r["operation_id"],
            "authorized_view": prov.get("authorized_view"),
            "disposition": r["disposition"],
            "observations": r.get("observations", []),
            "unresolved_conditions": r.get("unresolved_conditions", []),
            "scars": r.get("scars", []),
            "provenance": prov
        }

        if oid in CONTROLLED:
            controlled_pressure.append(preserved)
        else:
            primary_results.append(preserved)

    signals = []

    if len(views) > 1:
        signals.append("AUTHORIZED_VIEW_DIVERGENCE_PRESERVED")

    if len(dispositions) > 1:
        signals.append("DISPOSITION_DIVERGENCE_PRESERVED")

    if len(primary_results) > 1:
        signals.append("MULTIPLE_PRIMARY_PERSPECTIVES_PRESENT")

    if controlled_pressure:
        signals.append("CONTROLLED_PRESSURE_PRESENT")

    return {
        "disposition": "COMPOSED",
        "room_id": next(iter(room_ids)),
        "room_revision": next(iter(revisions)),
        "observer_count": len(results),
        "primary_observer_count": len(primary_results),
        "controlled_pressure_count": len(controlled_pressure),
        "primary_results": primary_results,
        "controlled_pressure": controlled_pressure,
        "composition_signals": signals,
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


def sample(
    oid,
    cls,
    mode,
    op,
    view="view:a",
    disposition="OBSERVED"
):
    return {
        "result_type": "ZERVAN_V41_OBSERVER_RESULT",
        "result_version": "1.0",
        "observer_id": oid,
        "observer_class": cls,
        "observer_mode": mode,
        "operation_id": op,
        "disposition": disposition,
        "observations": [{
            "observation_type": oid + "_observation",
            "statement": "Bounded " + oid + " observation.",
            "evidence_refs": ["evidence:test"],
            "confidence_status": "BOUNDED"
        }],
        "unresolved_conditions": [],
        "scars": [],
        "provenance": {
            "observer_id": oid,
            "observer_class": cls,
            "observer_mode": mode,
            "operation_id": op,
            "room_id": "room:test",
            "room_revision": "revision:test",
            "authorized_view": view,
            "evidence_refs": ["evidence:test"],
            "input_provenance_refs": ["provenance:test"],
            "claim_ceiling": "OBSERVATIONAL",
            "disposition": disposition,
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
    eagle = sample("eagle", "PRIMARY", "PRIMARY", "op:eagle")
    duck = sample("duck", "PRIMARY", "PRIMARY", "op:duck")
    owl = sample(
        "owl_hoot", "PRIMARY",
        "BOUNDED_SUB_OBSERVER", "op:owl"
    )
    osprey = sample(
        "osprey", "CONTROLLED_SUB_OBSERVER",
        "CONTROLLED_SUB_OBSERVER", "op:osprey"
    )

    tests = []

    # 1: two Primary Observers compose.
    out = compose([eagle, duck])
    tests.append(
        out["disposition"] == "COMPOSED"
        and out["primary_observer_count"] == 2
    )

    # 2: Primary + controlled pressure remains separated.
    out = compose([eagle, osprey])
    tests.append(
        out["disposition"] == "COMPOSED"
        and out["primary_observer_count"] == 1
        and out["controlled_pressure_count"] == 1
    )

    # 3: Owl_Hoot bounded mode preserves Primary identity.
    out = compose([eagle, owl])
    tests.append(
        out["disposition"] == "COMPOSED"
        and out["primary_observer_count"] == 2
    )

    # 4: differing authorized views are preserved, not collapsed.
    duck_view = sample(
        "duck", "PRIMARY", "PRIMARY",
        "op:duck", view="view:b"
    )
    out = compose([eagle, duck_view])
    tests.append(
        out["disposition"] == "COMPOSED"
        and "AUTHORIZED_VIEW_DIVERGENCE_PRESERVED"
            in out["composition_signals"]
    )

    # 5: differing dispositions are preserved.
    duck_diff = sample(
        "duck", "PRIMARY", "PRIMARY",
        "op:duck", disposition="NO_SIGNAL"
    )
    out = compose([eagle, duck_diff])
    tests.append(
        out["disposition"] == "COMPOSED"
        and "DISPOSITION_DIVERGENCE_PRESERVED"
            in out["composition_signals"]
    )

    # 6: no voting/averaging/winner/consensus.
    out = compose([eagle, duck])
    tests.append(
        out["voting_performed"] is False
        and out["averaging_performed"] is False
        and out["winner_selected"] is False
        and out["forced_consensus"] is False
        and out["silent_reconciliation"] is False
    )

    # 7: single result blocked.
    tests.append(
        compose([eagle])["disposition"] == "BLOCKED"
    )

    # 8: duplicate Observer result blocked.
    tests.append(
        compose([eagle, eagle])["disposition"] == "BLOCKED"
    )

    # 9: Room divergence blocked.
    foreign = sample(
        "duck", "PRIMARY", "PRIMARY", "op:duck"
    )
    foreign["provenance"]["room_id"] = "room:other"
    tests.append(
        compose([eagle, foreign])["disposition"] == "BLOCKED"
    )

    # 10: revision divergence blocked.
    foreign = sample(
        "duck", "PRIMARY", "PRIMARY", "op:duck"
    )
    foreign["provenance"]["room_revision"] = "revision:other"
    tests.append(
        compose([eagle, foreign])["disposition"] == "BLOCKED"
    )

    # 11: authority promotion blocked.
    bad = sample(
        "duck", "PRIMARY", "PRIMARY", "op:duck"
    )
    bad["authority"] = "OBSERVER"
    tests.append(
        compose([eagle, bad])["disposition"] == "BLOCKED"
    )

    # 12: claim ceiling escalation blocked.
    bad = sample(
        "duck", "PRIMARY", "PRIMARY", "op:duck"
    )
    bad["claim_ceiling_increased"] = True
    tests.append(
        compose([eagle, bad])["disposition"] == "BLOCKED"
    )

    if not all(tests):
        print(
            "OR-6 COMPOSER SELF-TEST: FAIL",
            [i + 1 for i, ok in enumerate(tests) if not ok]
        )
        return 1

    print("OR-6 COMPOSER SELF-TEST: 12/12 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(
        self_test()
        if "--self-test" in sys.argv
        else 0
    )
