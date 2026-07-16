from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


WRITER = load_module("v40_transition_writer", "candidate/v40/runtime/transition_writer.py")


def payload(**overrides):
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
        "evidence_refs": ["OC-V40.WAVE0.TRANCHE1"],
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


class TransitionWriterTests(unittest.TestCase):
    def make_writer(self, directory: str, **kwargs):
        return WRITER.TransitionWitnessWriter(
            Path(directory),
            "OC-V40.WAVE0.TRANCHE1",
            "OCI-V40.WAVE0.TRANCHE1.001",
            "v40_candidate_wave0_tranche1",
            clock=lambda: "2026-07-16T00:00:00+00:00",
            **kwargs,
        )

    def test_first_witness_is_persisted_and_hashed(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory)
            event = writer.append(payload())
            self.assertEqual(event["sequence"], 1)
            self.assertIsNone(event["previous_event_sha512"])
            self.assertEqual(event["event_sha512"], WRITER.event_digest(event))
            self.assertEqual(len(list(Path(directory).glob("*.json"))), 1)

    def test_second_witness_chains_to_first(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory)
            first = writer.append(payload())
            second = writer.append(payload(event_class="NO_CHANGE", from_state="ACTIVE", to_state="ACTIVE", trigger="same_route", reason="Route lock unchanged"))
            self.assertEqual(second["sequence"], 2)
            self.assertEqual(second["previous_event_sha512"], first["event_sha512"])

    def test_fixture_15_duplicate_event_identifier_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory)
            first = writer.append(payload())
            with self.assertRaisesRegex(WRITER.TransitionWitnessError, "duplicate event identifier"):
                writer.append(payload(event_id=first["event_id"]))

    def test_caller_sequence_gap_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory)
            with self.assertRaisesRegex(WRITER.TransitionWitnessError, "sequence gap or rollback"):
                writer.append(payload(sequence=2))

    def test_fixture_16_existing_ledger_sequence_gap_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory)
            first = writer.append(payload())
            event = dict(first)
            event["sequence"] = 3
            event["event_id"] = "TE-V40.WAVE0.TRANCHE1.001-000003"
            event["previous_event_sha512"] = first["event_sha512"]
            event["event_sha512"] = WRITER.event_digest(event)
            path = Path(directory) / f"000003_{event['event_id']}.json"
            path.write_text(json.dumps(event), encoding="utf-8")
            with self.assertRaisesRegex(WRITER.TransitionWitnessError, "sequence gap or rollback"):
                self.make_writer(directory)

    def test_fixture_17_hash_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory)
            writer.append(payload())
            path = next(Path(directory).glob("*.json"))
            event = json.loads(path.read_text(encoding="utf-8"))
            event["reason"] = "tampered"
            path.write_text(json.dumps(event), encoding="utf-8")
            with self.assertRaisesRegex(WRITER.TransitionWitnessError, "event_sha512 mismatch"):
                self.make_writer(directory)

    def test_fixture_18_persistence_failure_returns_non_durable_stop_record(self):
        def fail_publish(_temporary: Path, _target: Path) -> None:
            raise OSError("simulated persistence failure")

        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory, publisher=fail_publish)
            with self.assertRaises(WRITER.WitnessPersistenceError) as raised:
                writer.append(payload())
            self.assertEqual(raised.exception.emergency_record["state"], "STOPPED")
            self.assertEqual(raised.exception.emergency_record["stop_class"], "TRANSITION_WITNESS_FAILURE")
            self.assertFalse(raised.exception.emergency_record["durable"])
            self.assertEqual(writer.sequence, 0)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_stopped_witness_requires_scar_reason(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory)
            with self.assertRaisesRegex(WRITER.TransitionWitnessError, "Scar-required event requires scar_reason"):
                writer.append(payload(event_class="STOP", to_state="STOPPED", audit_result="FAIL", stop_class="AUDIT_INTERRUPT", scar_required=True, scar_reason=None))

    def test_illegal_state_transition_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory)
            with self.assertRaisesRegex(WRITER.TransitionWitnessError, "state transition is not permitted"):
                writer.append(payload(event_class="NO_CHANGE", from_state="ACTIVE", to_state="INITIALIZING"))

    def test_event_class_must_match_transition(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = self.make_writer(directory)
            with self.assertRaisesRegex(WRITER.TransitionWitnessError, "event class does not match state transition"):
                writer.append(payload(event_class="COMPLETION", from_state="ACTIVE", to_state="ACTIVE"))


if __name__ == "__main__":
    unittest.main()
