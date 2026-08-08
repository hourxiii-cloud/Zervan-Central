#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, timezone
import argparse
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

RESOLVER_PATH = ROOT / (
    "tools/"
    "resolve_promotion_candidate_binding.py"
)

AUTHORIZATION_MAP = {
    "APPROVE": "GRANTED",
    "REJECT": "DENIED",
    "DEFER": "DEFERRED",
}


def load_resolver():
    spec = importlib.util.spec_from_file_location(
        "resolve_promotion_candidate_binding",
        RESOLVER_PATH,
    )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


def issue(
    decision,
    actor,
    scope,
    rationale,
    timestamp=None,
):
    if decision not in AUTHORIZATION_MAP:
        raise ValueError(
            "decision must be APPROVE, REJECT, or DEFER"
        )

    for name, value in (
        ("actor", actor),
        ("scope", scope),
        ("rationale", rationale),
    ):
        if not value or not value.strip():
            raise ValueError(
                f"{name} must be explicitly supplied"
            )

    resolver = load_resolver()
    binding = resolver.resolve("HEAD")

    if timestamp is None:
        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

    return {
        "schema_version": "1.0",
        "record_type": "HUMAN_GATE_AUTHORIZATION_RECEIPT",
        "ring": "R8-E",
        "native_version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "candidate_branch": binding[
            "candidate_branch"
        ],
        "candidate_commit": binding[
            "candidate_commit"
        ],
        "candidate_tree": binding[
            "candidate_tree"
        ],
        "target_branch": binding[
            "target_branch"
        ],
        "binding_sha512": binding[
            "binding_sha512"
        ],
        "decision": decision,
        "authorization_state": AUTHORIZATION_MAP[
            decision
        ],
        "decision_actor": actor.strip(),
        "decision_timestamp": timestamp,
        "decision_scope": scope.strip(),
        "rationale": rationale.strip(),
        "provenance": [
            (
                "contracts/validation/"
                "RING7_AGGREGATE_DOCUMENTATION_"
                "PROMOTION_READINESS_CLOSURE.md"
            ),
            (
                "contracts/promotion/"
                "RING8_HUMAN_GATE_PROMOTION_BOUNDARY.md"
            ),
            (
                "contracts/promotion/"
                "PROMOTION_DECISION_CONTRACT.md"
            ),
            (
                "contracts/promotion/"
                "PROMOTION_CANDIDATE_BINDING.md"
            ),
            (
                "contracts/promotion/"
                "PRE_PROMOTION_VERIFICATION.md"
            ),
        ],
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "promotion_state": "CANDIDATE",
        "promotion_executed": False,
        "canonical": False,
        "promoted": False,
        "merged": False,
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--decision",
        choices=[
            "APPROVE",
            "REJECT",
            "DEFER",
        ],
        required=True,
    )

    parser.add_argument(
        "--actor",
        required=True,
    )

    parser.add_argument(
        "--scope",
        required=True,
    )

    parser.add_argument(
        "--rationale",
        required=True,
    )

    parser.add_argument(
        "--timestamp",
    )

    args = parser.parse_args()

    receipt = issue(
        decision=args.decision,
        actor=args.actor,
        scope=args.scope,
        rationale=args.rationale,
        timestamp=args.timestamp,
    )

    print(
        json.dumps(
            receipt,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
