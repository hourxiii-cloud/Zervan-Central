"""Duck-mode logical stress test for middleware standing.

This is a deterministic candidate-side model check. It is not a formal Duck
observer execution over Beagle-validated runtime telemetry.
"""

from __future__ import annotations

import random


CONTROLLED_FIELDS = (
    "authority",
    "membership",
    "work_id",
    "persona_owner",
    "promotion",
    "human_gate",
)


def fresh_state() -> dict[str, str]:
    return {
        "authority": "NONE",
        "membership": "NONE",
        "work_id": "NONE",
        "persona_owner": "NONE",
        "promotion": "NONE",
        "human_gate": "ACTIVE",
        "attribution": "PRESENT",
        "unresolved": "UNKNOWN",
    }


ACTORS = ("CHAT", "TECH", "EAGLE", "OSPREY", "DUCK")
ACTIONS = (
    "claim_authority",
    "claim_membership",
    "issue_work_id",
    "replace_persona",
    "promote_candidate",
    "satisfy_human_gate",
    "mutate_canon",
    "authorize_external_action",
    "drop_attribution",
    "restore_attribution",
    "resolve_unknown_without_evidence",
    "transport_context",
)


def apply_event(state: dict[str, str], actor: str, action: str) -> None:
    """Apply only effects allowed by the middleware/observer boundary."""

    # All listed escalation and mutation attempts are rejected for every actor
    # in this candidate-side standing model.
    if action in {
        "claim_authority",
        "claim_membership",
        "issue_work_id",
        "replace_persona",
        "promote_candidate",
        "satisfy_human_gate",
        "mutate_canon",
        "authorize_external_action",
    }:
        return
    if action == "drop_attribution":
        state["attribution"] = "MISSING"
    elif action == "restore_attribution":
        state["attribution"] = "PRESENT"
    elif action == "resolve_unknown_without_evidence":
        return
    elif action == "transport_context":
        return
    else:
        raise AssertionError(f"unhandled action: {action}")


def main() -> None:
    rng = random.Random(100000)
    trials = 100_000
    events = 0
    rejected_escalations = 0
    max_wobble = 0
    for _ in range(trials):
        state = fresh_state()
        baseline = {key: state[key] for key in CONTROLLED_FIELDS}
        prior = tuple(state[key] for key in CONTROLLED_FIELDS)
        for _ in range(32):
            actor = rng.choice(ACTORS)
            action = rng.choice(ACTIONS)
            if action in {
                "claim_authority",
                "claim_membership",
                "issue_work_id",
                "replace_persona",
                "promote_candidate",
                "satisfy_human_gate",
                "mutate_canon",
                "authorize_external_action",
            }:
                rejected_escalations += 1
            apply_event(state, actor, action)
            current = tuple(state[key] for key in CONTROLLED_FIELDS)
            if current != prior:
                max_wobble = max(max_wobble, 1)
            prior = current
            events += 1
            assert {key: state[key] for key in CONTROLLED_FIELDS} == baseline
        assert state["unresolved"] == "UNKNOWN"

    assert max_wobble == 0
    print(
        "PASS: Duck-mode stress test; "
        f"{trials} trials; {events} events; "
        f"{rejected_escalations} escalation attempts rejected; "
        "wobble=0; governed standing preserved"
    )


if __name__ == "__main__":
    main()
