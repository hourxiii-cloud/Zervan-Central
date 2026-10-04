"""Deterministic logical invariant test for the staged ChatGPT/Codex condition.

This is a candidate-side state model. It does not claim deployed runtime
validation or canonical promotion.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class State:
    canonical_authority: str = "NONE"
    human_gate: str = "ACTIVE"
    chat_role: str = "ZERVAN MIDDLEWARE"
    chat_membership: str = "NONE"
    chat_work_id: str = "NONE"
    chat_persona_owner: str = "NONE"
    promotion: str = "NONE"
    attribution: bool = True
    unresolved: str = "UNKNOWN"


FORBIDDEN_ESCALATIONS = {
    "self_issue_work_id",
    "claim_membership",
    "claim_authority",
    "promote_candidate",
    "replace_persona",
    "assign_persona_weight",
    "invent_chain",
    "declare_private_channel",
}


def apply_chat_event(state: State, event: str) -> None:
    """Apply an event under the middleware condition.

    Chat-originated escalation events are rejected and cannot mutate governed
    standing. Valid transport events may preserve attribution only.
    """

    if event in FORBIDDEN_ESCALATIONS:
        return
    if event == "drop_attribution":
        state.attribution = False
        return
    if event == "restore_attribution":
        state.attribution = True
        return
    if event == "resolve_unknown_without_evidence":
        return
    if event == "qualified_return":
        state.unresolved = "QUALIFIED_RETURN"
        return
    if event == "transport_only":
        return
    raise AssertionError(f"unhandled event: {event}")


def assert_invariants(state: State) -> None:
    assert state.canonical_authority == "NONE"
    assert state.human_gate == "ACTIVE"
    assert state.chat_role == "ZERVAN MIDDLEWARE"
    assert state.chat_membership == "NONE"
    assert state.chat_work_id == "NONE"
    assert state.chat_persona_owner == "NONE"
    assert state.promotion == "NONE"


def main() -> None:
    rng = random.Random(4254)
    events = [
        "self_issue_work_id",
        "claim_membership",
        "claim_authority",
        "promote_candidate",
        "replace_persona",
        "assign_persona_weight",
        "invent_chain",
        "declare_private_channel",
        "drop_attribution",
        "restore_attribution",
        "resolve_unknown_without_evidence",
        "qualified_return",
        "transport_only",
    ]
    trials = 1000
    total_events = 0
    for _ in range(trials):
        state = State()
        sequence = [rng.choice(events) for _ in range(32)]
        for event in sequence:
            apply_chat_event(state, event)
            total_events += 1
            assert_invariants(state)
        # A failed attribution event is visible and cannot authenticate itself.
        if "drop_attribution" in sequence and "restore_attribution" not in sequence:
            assert state.attribution is False
        # Unknown cannot be resolved by narration alone.
        if "resolve_unknown_without_evidence" in sequence and "qualified_return" not in sequence:
            assert state.unresolved == "UNKNOWN"

    print(f"PASS: {trials} trials; {total_events} events; invariants preserved")


if __name__ == "__main__":
    main()
