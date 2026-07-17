#!/usr/bin/env python3
"""Run a read-only integrated validation of the v40 candidate control plane."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from candidate.v40.runtime.control_plane import RuntimeControlPlane  # noqa: E402
from candidate.v40.runtime.transition_writer import TransitionWitnessWriter  # noqa: E402


CONTRACT = ROOT / "candidate/v40/contracts/wave1_reporting_production.operational_contract.json"


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    handlers = {action: (lambda: None) for action in contract["route"]["permitted_actions"]}
    with tempfile.TemporaryDirectory(prefix="zervan-v40-control-") as directory:
        ledger = Path(directory)
        plane = RuntimeControlPlane(contract, ledger, action_handlers=handlers)
        plane.activate()
        plane.request_action("canonical.read")
        plane.complete(contract["completion_criteria"])
        snapshot = plane.snapshot()
        if snapshot["state"] != "COMPLETE" or snapshot["transition_sequence"] != 4:
            print(f"FAIL: unexpected terminal snapshot: {snapshot}", file=sys.stderr)
            return 1
        replay_check = TransitionWitnessWriter(
            ledger,
            contract["contract_id"],
            contract["contract_instance_id"],
            contract["route"]["route_id"],
        )
        if replay_check.sequence != 4 or replay_check.head_sha512 != snapshot["ledger_head_sha512"]:
            print("FAIL: transition ledger replay check mismatch", file=sys.stderr)
            return 1
    print("PASS: v40 candidate control plane verified (4-event complete ledger; no persistent output)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
