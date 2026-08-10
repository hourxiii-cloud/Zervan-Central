#!/usr/bin/env python3
import sys

FAILURES = {
    "NO_SIGNAL",
    "INSUFFICIENT_EVIDENCE",
    "EVIDENCE_CEILING_REACHED",
    "VIEW_RESTRICTED",
    "BOUNDARY_BLOCKED",
    "PROVENANCE_INCOMPLETE",
    "STALE_BINDING",
    "DIVERGENT_BINDING",
    "SEMANTIC_CONFLICT",
    "OBSERVER_UNAVAILABLE",
    "OPERATING_SCOPE_EXCEEDED",
    "AUTHORITY_VIOLATION",
    "SCARRED",
}

NON_SCAR_TERMINALS = {
    "NO_SIGNAL",
    "VIEW_RESTRICTED",
    "BOUNDARY_BLOCKED",
    "OBSERVER_UNAVAILABLE",
}

SCAR_REQUIRED = {
    "INSUFFICIENT_EVIDENCE",
    "EVIDENCE_CEILING_REACHED",
    "PROVENANCE_INCOMPLETE",
    "STALE_BINDING",
    "DIVERGENT_BINDING",
    "SEMANTIC_CONFLICT",
    "OPERATING_SCOPE_EXCEEDED",
    "AUTHORITY_VIOLATION",
    "SCARRED",
}


def blocked(reason):
    return {
        "disposition": "BLOCKED",
        "reason": reason,
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "finding_created": False,
        "fact_created": False,
        "claim_ceiling_increased": False,
        "canonical_state_mutated": False
    }


def classify(event):
    if not isinstance(event, dict):
        return blocked("EVENT_NOT_OBJECT")

    failure = event.get("failure")

    if failure not in FAILURES:
        return blocked("UNKNOWN_FAILURE_SEMANTIC")

    if event.get("authority") != "NONE":
        return blocked("AUTHORITY_VIOLATION")

    if event.get("human_gate") != "ACTIVE":
        return blocked("HUMAN_GATE_VIOLATION")

    if event.get("fact_created") is not False:
        return blocked("FAILURE_PROMOTED_TO_FACT")

    if event.get("finding_created") is not False:
        return blocked("FAILURE_PROMOTED_TO_FINDING")

    if event.get("claim_ceiling_increased") is not False:
        return blocked("CLAIM_CEILING_ESCALATION")

    if event.get("canonical_state_mutated") is not False:
        return blocked("CANONICAL_STATE_MUTATION")

    scar = event.get("scar")

    if failure in SCAR_REQUIRED:
        if not isinstance(scar, dict):
            return blocked("SCAR_REQUIRED")

        if not scar.get("scar_id"):
            return blocked("SCAR_ID_REQUIRED")

        if not scar.get("reason"):
            return blocked("SCAR_REASON_REQUIRED")

        if scar.get("resolved") is True:
            return blocked("SCAR_CANNOT_SELF_RESOLVE")

        scar_state = "PRESERVED"

    else:
        if scar is not None:
            return blocked("UNNECESSARY_SCAR")

        scar_state = "NOT_REQUIRED"

    return {
        "disposition": "FAILURE_RECORDED",
        "failure": failure,
        "scar_state": scar_state,
        "scar": scar,
        "observer_id": event.get("observer_id"),
        "operation_id": event.get("operation_id"),
        "room_id": event.get("room_id"),
        "room_revision": event.get("room_revision"),
        "authorized_view": event.get("authorized_view"),
        "evidence_refs": event.get("evidence_refs", []),
        "provenance_refs": event.get(
            "provenance_refs", []
        ),
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "finding_created": False,
        "fact_created": False,
        "claim_ceiling_increased": False,
        "canonical_state_mutated": False
    }


def event(failure, with_scar=False):
    out = {
        "failure": failure,
        "observer_id": "owl_hoot",
        "operation_id": "operation:test",
        "room_id": "room:test",
        "room_revision": "revision:test",
        "authorized_view": "view:test",
        "evidence_refs": ["evidence:test"],
        "provenance_refs": ["provenance:test"],
        "authority": "NONE",
        "human_gate": "ACTIVE",
        "finding_created": False,
        "fact_created": False,
        "claim_ceiling_increased": False,
        "canonical_state_mutated": False,
        "scar": None
    }

    if with_scar:
        out["scar"] = {
            "scar_id": "scar:test",
            "reason": failure,
            "resolved": False
        }

    return out


def self_test():
    tests = []

    # 1-4: non-scar terminal states remain bounded.
    for failure in sorted(NON_SCAR_TERMINALS):
        out = classify(event(failure))
        tests.append(
            out["disposition"]
                == "FAILURE_RECORDED"
            and out["scar_state"]
                == "NOT_REQUIRED"
        )

    # 5-13: all scar-required states preserve scar.
    for failure in sorted(SCAR_REQUIRED):
        out = classify(
            event(failure, with_scar=True)
        )
        tests.append(
            out["disposition"]
                == "FAILURE_RECORDED"
            and out["scar_state"]
                == "PRESERVED"
        )

    # 14: scar-required state without scar blocked.
    tests.append(
        classify(
            event("SEMANTIC_CONFLICT")
        )["disposition"] == "BLOCKED"
    )

    # 15: unnecessary scar blocked.
    tests.append(
        classify(
            event("NO_SIGNAL", with_scar=True)
        )["disposition"] == "BLOCKED"
    )

    # 16: failure cannot create authority.
    bad = event(
        "AUTHORITY_VIOLATION",
        with_scar=True
    )
    bad["authority"] = "OBSERVER"

    tests.append(
        classify(bad)["disposition"]
        == "BLOCKED"
    )

    # 17: failure cannot substitute Human Gate.
    bad = event(
        "INSUFFICIENT_EVIDENCE",
        with_scar=True
    )
    bad["human_gate"] = "SATISFIED"

    tests.append(
        classify(bad)["disposition"]
        == "BLOCKED"
    )

    # 18: failure cannot silently become fact.
    bad = event(
        "PROVENANCE_INCOMPLETE",
        with_scar=True
    )
    bad["fact_created"] = True

    tests.append(
        classify(bad)["disposition"]
        == "BLOCKED"
    )

    # 19: failure cannot silently become finding.
    bad = event(
        "STALE_BINDING",
        with_scar=True
    )
    bad["finding_created"] = True

    tests.append(
        classify(bad)["disposition"]
        == "BLOCKED"
    )

    # 20: scar cannot self-resolve.
    bad = event(
        "DIVERGENT_BINDING",
        with_scar=True
    )
    bad["scar"]["resolved"] = True

    tests.append(
        classify(bad)["disposition"]
        == "BLOCKED"
    )

    # 21: claim ceiling cannot rise.
    bad = event(
        "EVIDENCE_CEILING_REACHED",
        with_scar=True
    )
    bad["claim_ceiling_increased"] = True

    tests.append(
        classify(bad)["disposition"]
        == "BLOCKED"
    )

    # 22: canonical state cannot mutate.
    bad = event(
        "OPERATING_SCOPE_EXCEEDED",
        with_scar=True
    )
    bad["canonical_state_mutated"] = True

    tests.append(
        classify(bad)["disposition"]
        == "BLOCKED"
    )

    if not all(tests):
        print(
            "OR-9 FAILURE SELF-TEST: FAIL",
            [
                i + 1
                for i, ok in enumerate(tests)
                if not ok
            ]
        )
        return 1

    print(
        "OR-9 FAILURE SELF-TEST: 22/22 PASS"
    )
    return 0


if __name__ == "__main__":
    sys.exit(
        self_test()
        if "--self-test" in sys.argv
        else 0
    )
