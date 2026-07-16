#!/usr/bin/env python3
"""Run a read-only integrated validation of v40 Scar and Replay continuity."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from candidate.v40.runtime.continuity import (  # noqa: E402
    MinimumReplay,
    ScarLedgerWriter,
    reconcile_scars,
    replay_digest,
    scar_digest,
)
from candidate.v40.runtime.transition_writer import TransitionWitnessWriter  # noqa: E402


CONTRACT_PATH = ROOT / "candidate/v40/contracts/wave0_tranche1.operational_contract.json"
SCAR_SCHEMA_PATH = ROOT / "candidate/v40/contracts/scar.schema.json"
REPLAY_SCHEMA_PATH = ROOT / "candidate/v40/contracts/replay_receipt.schema.json"


def payload(**overrides: object) -> dict:
    value = {
        "event_class": "ACTIVATION",
        "from_state": "INITIALIZING",
        "to_state": "ACTIVE",
        "trigger": "activation_checks_passed",
        "action": None,
        "request_ref": None,
        "reason": "Activation checks passed",
        "authorization": "CONTRACT_PERMITTED",
        "participants": ["Audit", "Governance"],
        "evidence_refs": ["continuity-validator"],
        "conformance_before": "UNKNOWN",
        "conformance_after": "CONFORMING",
        "audit_result": "PASS",
        "human_gate_latched": False,
        "decision_ref": None,
        "stop_class": None,
        "scar_required": False,
        "scar_reason": None,
    }
    value.update(overrides)
    return value


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    try:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        scar_schema = json.loads(SCAR_SCHEMA_PATH.read_text(encoding="utf-8"))
        replay_schema = json.loads(REPLAY_SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(str(exc))
    if scar_schema.get("$id") != "zervan://candidate/v40/contracts/scar/1":
        return fail("Scar schema identifier mismatch")
    if replay_schema.get("$id") != "zervan://candidate/v40/contracts/replay_receipt/1":
        return fail("Replay schema identifier mismatch")
    if contract.get("authority_state") != "NONE" or contract.get("human_gate") != "ACTIVE":
        return fail("candidate authority or Human Gate invariant mismatch")
    posture = contract.get("posture", {})
    if posture.get("external_runtime") != "DISABLED" or posture.get("system_population") != "DISALLOWED":
        return fail("candidate external-runtime or system-population posture mismatch")

    contract_ref = contract["contract_id"]
    contract_instance_id = contract["contract_instance_id"]
    route_lock = contract["route"]["route_id"]
    binding = contract["canonical_binding"]
    canonical_binding_ref = f"{binding['repository']}@{binding['commit']}"

    with tempfile.TemporaryDirectory(prefix="zervan-v40-continuity-") as directory:
        root = Path(directory)
        transition_writer = TransitionWitnessWriter(
            root / "transitions",
            contract_ref,
            contract_instance_id,
            route_lock,
            clock=lambda: "2026-07-16T15:00:00+00:00",
        )
        transition_writer.append(payload())
        terminal = transition_writer.append(
            payload(
                event_class="STOP",
                from_state="ACTIVE",
                to_state="STOPPED",
                trigger="continuity_validation_stop",
                reason="Validator created an inert terminal witness",
                authorization="REJECTED",
                conformance_before="CONFORMING",
                conformance_after="NONCONFORMING",
                audit_result="FAIL",
                stop_class="AUDIT_INTERRUPT",
                scar_required=True,
                scar_reason="Validator created an inert terminal witness",
            )
        )
        scar_writer = ScarLedgerWriter(
            root / "scars",
            root / "transitions",
            contract_ref,
            contract_instance_id,
            route_lock,
            canonical_binding_ref,
            clock=lambda: "2026-07-16T15:00:01+00:00",
        )
        scar = scar_writer.append(
            terminal["event_id"],
            scar_class="CONTRACT_CONTROL_STOP",
            evidence_boundary={
                "boundary_state": "PARTIAL",
                "available_evidence_refs": ["continuity-validator"],
                "missing_evidence_refs": ["future-evidence"],
                "contradiction_refs": [],
                "invalid_evidence_refs": [],
                "scope_exclusions": [],
                "boundary_reason": "Validation preserves one explicit missing evidence reference",
                "evidence_time_utc": "2026-07-16T14:59:59+00:00",
            },
            analysis_state={
                "inquiry_ref": "INQUIRY-CONTINUITY-VALIDATION",
                "claim_refs": [],
                "unresolved_claim_refs": ["future-evidence"],
                "eliminated_world_refs": [],
                "surviving_world_refs": [],
                "function_participation_refs": ["Audit", "Governance"],
                "last_supported_conclusion_refs": [],
                "state_summary": "The inert validation route stopped before continuation.",
            },
            continuation={
                "replay_eligible": True,
                "replay_blockers": [],
                "replay_preconditions": ["Complete Scar reconciliation"],
                "new_contract_required": True,
                "continuation_ref": None,
                "human_gate_decision_required": True,
            },
            provenance_refs=["continuity-validator"],
        )
        if scar["scar_sha512"] != scar_digest(scar):
            return fail("Scar digest mismatch")
        reconciliation = reconcile_scars(
            root / "transitions",
            root / "scars",
            contract_ref,
            contract_instance_id,
            route_lock,
            canonical_binding_ref,
        )
        if reconciliation["state"] != "COMPLETE":
            return fail(f"Scar reconciliation is {reconciliation['state']}")

        restored_context = [
            {"context_class": "ROUTE_CONTRACT", "ref": contract_ref},
            {"context_class": "CANONICAL_BINDING", "ref": canonical_binding_ref},
            {"context_class": "TRANSITION_LEDGER", "ref": terminal["event_sha512"]},
            {"context_class": "TERMINAL_EVENT", "ref": terminal["event_id"]},
            {"context_class": "SCAR", "ref": scar["scar_id"]},
            {"context_class": "EVIDENCE_BOUNDARY", "ref": "continuity-validator"},
            {"context_class": "ANALYTICAL_STATE", "ref": "INQUIRY-CONTINUITY-VALIDATION"},
            {"context_class": "FUNCTION_PARTICIPATION", "ref": "Audit"},
            {"context_class": "PRIOR_DECISION", "ref": "continuity-validation-stop"},
        ]
        replay = MinimumReplay(
            root / "transitions",
            root / "scars",
            root / "replays",
            contract_ref,
            contract_instance_id,
            route_lock,
            canonical_binding_ref,
            clock=lambda: "2026-07-16T15:00:02+00:00",
        )
        preparation = replay.prepare(
            scar["scar_id"],
            requested_at_utc="2026-07-16T15:00:01+00:00",
            current_canonical_binding_ref=canonical_binding_ref,
            canonical_comparison="UNCHANGED",
            restored_context=restored_context,
            unavailable_context=[],
            proposed_route_id="v40_continuity_validation_candidate",
            proposed_scope=["Continue only under a separately reviewed contract"],
            proposed_completion_criteria=["Satisfy the separately reviewed contract"],
            required_evidence_refs=["future-evidence"],
        )
        decision = replay.record_human_decision(
            preparation["replay_id"],
            approved=True,
            decision_ref="HG-CONTINUITY-VALIDATION",
            decided_at_utc="2026-07-16T15:00:03+00:00",
            decision_owner="HUMAN",
        )
        if preparation["status"] != "HUMAN_GATE_REVIEW":
            return fail("Replay did not latch Human Gate review")
        if decision["status"] != "AUTHORIZED_NEW_CONTRACT_REQUIRED":
            return fail("Replay approval did not require a new contract")
        if decision["continuation_proposal"]["new_contract_ref"] is not None:
            return fail("Replay approval improperly created a contract")
        if decision["replay_sha512"] != replay_digest(decision):
            return fail("Replay decision digest mismatch")
        if len(list((root / "transitions").glob("*.json"))) != 2:
            return fail("Replay mutated the source transition ledger")

    print(
        "PASS: v40 candidate continuity verified "
        "(terminal witness -> immutable Scar -> Human-Gated Replay; no persistent output)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
