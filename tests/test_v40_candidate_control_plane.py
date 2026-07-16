from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from candidate.v40.runtime.control_plane import (
    AuditInterrupted,
    HumanGateLatched,
    HumanGateRequired,
    RuntimeControlPlane,
    TerminalStateError,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "candidate/v40/contracts/wave0_tranche1.operational_contract.json"


def contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


class ControlPlaneAcceptanceFixtures(unittest.TestCase):
    def make_plane(self, directory: str, value: dict | None = None, handlers: dict | None = None, **writer_options) -> RuntimeControlPlane:
        selected = value or contract()
        registered = handlers if handlers is not None else {action: (lambda: None) for action in selected["route"]["permitted_actions"]}
        return RuntimeControlPlane(
            selected,
            Path(directory),
            action_handlers=registered,
            writer_options={"clock": lambda: "2026-07-16T00:00:00+00:00", **writer_options},
        )

    def test_fixture_01_valid_activation_enters_active_and_writes_event_one(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            event = plane.activate()
            self.assertEqual(plane.state, "ACTIVE")
            self.assertEqual(plane.conformance, "CONFORMING")
            self.assertEqual(event["sequence"], 1)
            self.assertEqual(event["event_class"], "ACTIVATION")

    def test_fixture_02_authority_drift_during_initialization_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.contract["authority_state"] = "FULL"
            with self.assertRaises(AuditInterrupted):
                plane.activate()
            self.assertEqual(plane.state, "STOPPED")
            self.assertEqual(plane.stop_class, "CONTRACT_NONCONFORMANCE")

    def test_fixture_03_canonical_commit_mismatch_stops(self):
        value = contract()
        value["canonical_binding"]["commit"] = "0" * 40
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory, value)
            with self.assertRaises(AuditInterrupted):
                plane.activate()
            self.assertEqual(plane.stop_class, "CANONICAL_BINDING_FAILURE")

    def test_fixture_04_canonical_artifact_hash_mismatch_stops(self):
        value = contract()
        value["canonical_binding"]["artifacts"][0]["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory, value)
            with self.assertRaises(AuditInterrupted):
                plane.activate()
            self.assertEqual(plane.stop_class, "CANONICAL_BINDING_FAILURE")

    def test_fixture_05_permitted_action_writes_intent_and_result(self):
        calls: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            handlers = {action: (lambda: None) for action in contract()["route"]["permitted_actions"]}
            handlers["test.run"] = lambda: calls.append("executed") or "result"
            plane = self.make_plane(directory, handlers=handlers)
            plane.activate()
            result = plane.request_action("test.run")
            self.assertEqual(result, "result")
            self.assertEqual(calls, ["executed"])
            self.assertEqual(plane.state, "ACTIVE")
            self.assertEqual(plane.writer.sequence, 3)

    def test_fixture_06_explicit_route_replacement_latches_gate_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(HumanGateRequired):
                plane.request_route("alternate_route", "REQ-ROUTE-1")
            self.assertEqual(plane.state, "HUMAN_GATE_REVIEW")
            self.assertTrue(plane.human_gate_latched)
            self.assertEqual(plane.runtime_route, plane.route_lock)

    def test_fixture_07_direct_route_drift_invokes_audit_stop(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            plane.runtime_route = "drifted_route"
            with self.assertRaises(AuditInterrupted):
                plane.request_action("test.run")
            self.assertEqual(plane.state, "STOPPED")
            self.assertEqual(plane.stop_class, "ROUTE_DRIFT")

    def test_fixture_08_prohibited_action_latches_gate_without_execution(self):
        calls: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(HumanGateRequired):
                plane.request_action("git.push", "REQ-PUSH-1")
            self.assertEqual(calls, [])
            self.assertEqual(plane.state, "HUMAN_GATE_REVIEW")

    def test_fixture_09_undeclared_action_invokes_audit_stop(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(AuditInterrupted):
                plane.request_action("unknown.action")
            self.assertEqual(plane.stop_class, "UNDECLARED_ACTION")

    def test_fixture_10_explicit_audit_fail_interrupts_active_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(AuditInterrupted):
                plane.audit_interrupt("Explicit control failure", ["evidence:test"])
            self.assertEqual(plane.state, "STOPPED")
            self.assertEqual(plane.stop_class, "AUDIT_INTERRUPT")

    def test_fixture_11_human_gate_latch_blocks_permitted_action(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(HumanGateRequired):
                plane.request_action("git.push", request_ref="REQ-PUSH-2")
            with self.assertRaises(HumanGateLatched):
                plane.request_action("test.run")

    def test_fixture_12_human_gate_denial_enters_terminal_stopped(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(HumanGateRequired):
                plane.request_route("alternate_route", "REQ-ROUTE-2")
            plane.resolve_human_gate(approved=False, decision_ref="HG-DENY-1")
            self.assertEqual(plane.state, "STOPPED")
            self.assertEqual(plane.stop_class, "HUMAN_GATE_DENIED")

    def test_fixture_13_human_gate_approval_requires_new_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(HumanGateRequired):
                plane.request_route("alternate_route", "REQ-ROUTE-3")
            plane.resolve_human_gate(approved=True, decision_ref="HG-APPROVE-1")
            self.assertEqual(plane.state, "STOPPED")
            self.assertEqual(plane.stop_class, "HUMAN_GATE_APPROVED_NEW_CONTRACT_REQUIRED")
            self.assertEqual(plane.runtime_route, plane.route_lock)

    def test_fixture_14_runtime_cannot_synthesize_human_gate_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(HumanGateRequired):
                plane.request_route("alternate_route", "REQ-ROUTE-4")
            with self.assertRaises(HumanGateLatched):
                plane.resolve_human_gate(approved=True, decision_ref="")
            self.assertEqual(plane.state, "HUMAN_GATE_REVIEW")

    def test_fixture_19_missing_completion_criterion_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(AuditInterrupted):
                plane.complete(plane.contract["completion_criteria"][:-1])
            self.assertEqual(plane.state, "STOPPED")
            self.assertEqual(plane.stop_class, "COMPLETION_MISMATCH")

    def test_fixture_20_complete_criteria_enter_terminal_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            plane.complete(plane.contract["completion_criteria"])
            self.assertEqual(plane.state, "COMPLETE")

    def test_fixture_21_reentry_from_stopped_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            with self.assertRaises(AuditInterrupted):
                plane.audit_interrupt("stop")
            with self.assertRaises(TerminalStateError):
                plane.request_action("test.run")

    def test_fixture_22_reentry_from_complete_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            plane.complete(plane.contract["completion_criteria"])
            with self.assertRaises(TerminalStateError):
                plane.request_action("test.run")

    def test_fixture_23_default_control_route_has_no_repository_side_effect(self):
        before = subprocess.run(["git", "status", "--porcelain=v1"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory)
            plane.activate()
            plane.request_action("canonical.read")
            plane.complete(plane.contract["completion_criteria"])
            self.assertEqual(plane.contract["posture"]["external_runtime"], "DISABLED")
            self.assertEqual(plane.contract["posture"]["system_population"], "DISALLOWED")
        after = subprocess.run(["git", "status", "--porcelain=v1"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
        self.assertEqual(after, before)

    def test_activation_rejects_unbound_action_handler_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory, handlers={"test.run": lambda: None})
            with self.assertRaises(AuditInterrupted):
                plane.activate()
            self.assertEqual(plane.stop_class, "CONTRACT_NONCONFORMANCE")

    def test_registered_action_handler_failure_invokes_audit_stop(self):
        def fail() -> None:
            raise RuntimeError("simulated handler failure")

        handlers = {action: (lambda: None) for action in contract()["route"]["permitted_actions"]}
        handlers["test.run"] = fail
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(directory, handlers=handlers)
            plane.activate()
            with self.assertRaises(AuditInterrupted):
                plane.request_action("test.run")
            self.assertEqual(plane.state, "STOPPED")
            self.assertEqual(plane.stop_class, "AUDIT_INTERRUPT")


if __name__ == "__main__":
    unittest.main()
