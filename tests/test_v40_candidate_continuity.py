from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from typing import Any

from candidate.v40.runtime.continuity import (
    ContinuityError,
    MinimumReplay,
    ReplayLedgerWriter,
    ScarLedgerWriter,
    ScarPersistenceError,
    detect_repeating_thirds_marker,
    reconcile_scars,
    replay_digest,
    scar_digest,
)
from candidate.v40.runtime.control_plane import AuditInterrupted, RuntimeControlPlane
from candidate.v40.runtime.transition_writer import TransitionWitnessWriter


ROOT = Path(__file__).resolve().parents[1]
SCAR_SCHEMA_PATH = ROOT / "candidate/v40/contracts/scar.schema.json"
REPLAY_SCHEMA_PATH = ROOT / "candidate/v40/contracts/replay_receipt.schema.json"
OPERATIONAL_CONTRACT_PATH = ROOT / "candidate/v40/contracts/wave0_tranche1.operational_contract.json"


class SchemaValidationError(ValueError):
    pass


def _schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    raise SchemaValidationError(f"unsupported schema type: {expected}")


def _resolve_local_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise SchemaValidationError(f"unsupported non-local reference: {ref}")
    value: Any = root_schema
    for raw_part in ref[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        try:
            value = value[part]
        except (KeyError, TypeError) as exc:
            raise SchemaValidationError(f"unresolved schema reference: {ref}") from exc
    if not isinstance(value, dict):
        raise SchemaValidationError(f"schema reference is not an object: {ref}")
    return value


def _is_date_time(value: str) -> bool:
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return "T" in value and parsed.tzinfo is not None


def validate_schema(
    instance: Any,
    schema: dict[str, Any],
    *,
    root_schema: dict[str, Any] | None = None,
    path: str = "$",
) -> None:
    root = root_schema or schema

    if "$ref" in schema:
        validate_schema(instance, _resolve_local_ref(root, schema["$ref"]), root_schema=root, path=path)
        return

    for keyword in ("allOf",):
        for branch in schema.get(keyword, []):
            validate_schema(instance, branch, root_schema=root, path=path)

    if "anyOf" in schema:
        matches = 0
        for branch in schema["anyOf"]:
            try:
                validate_schema(instance, branch, root_schema=root, path=path)
            except SchemaValidationError:
                continue
            matches += 1
        if matches == 0:
            raise SchemaValidationError(f"{path}: no anyOf branch matched")

    if "if" in schema:
        try:
            validate_schema(instance, schema["if"], root_schema=root, path=path)
        except SchemaValidationError:
            branch = schema.get("else")
        else:
            branch = schema.get("then")
        if branch is not None:
            validate_schema(instance, branch, root_schema=root, path=path)

    expected_types = schema.get("type")
    if expected_types is not None:
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        if not any(_schema_type_matches(instance, expected) for expected in expected_types):
            raise SchemaValidationError(f"{path}: expected type {expected_types}")

    if "const" in schema and instance != schema["const"]:
        raise SchemaValidationError(f"{path}: value does not match const")
    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaValidationError(f"{path}: value is not in enum")

    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise SchemaValidationError(f"{path}: string is too short")
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            raise SchemaValidationError(f"{path}: string does not match pattern")
        if schema.get("format") == "date-time" and not _is_date_time(instance):
            raise SchemaValidationError(f"{path}: invalid date-time")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise SchemaValidationError(f"{path}: value is below minimum")

    if isinstance(instance, list):
        if schema.get("uniqueItems"):
            canonical_items = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in instance]
            if len(canonical_items) != len(set(canonical_items)):
                raise SchemaValidationError(f"{path}: array items are not unique")
        if "items" in schema:
            for index, item in enumerate(instance):
                validate_schema(item, schema["items"], root_schema=root, path=f"{path}[{index}]")

    if isinstance(instance, dict):
        missing = [name for name in schema.get("required", []) if name not in instance]
        if missing:
            raise SchemaValidationError(f"{path}: missing required properties {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise SchemaValidationError(f"{path}: unexpected properties {extras}")
        for name, child_schema in properties.items():
            if name in instance:
                validate_schema(instance[name], child_schema, root_schema=root, path=f"{path}.{name}")


def scar_schema() -> dict[str, Any]:
    return json.loads(SCAR_SCHEMA_PATH.read_text(encoding="utf-8"))


def replay_schema() -> dict[str, Any]:
    return json.loads(REPLAY_SCHEMA_PATH.read_text(encoding="utf-8"))


def operational_contract() -> dict[str, Any]:
    return json.loads(OPERATIONAL_CONTRACT_PATH.read_text(encoding="utf-8"))


def valid_scar() -> dict[str, Any]:
    digest_a = "a" * 128
    digest_b = "b" * 128
    return {
        "scar_version": "v40-candidate.1",
        "scar_id": "SC-OCI-TEST.7",
        "contract_ref": "OC-V40-WAVE0-TRANCHE2",
        "contract_instance_id": "OCI-TEST.1",
        "route_id": "v40_wave0_control_route",
        "route_lock": "v40_wave0_control_route",
        "canonical_binding_ref": "CANONICAL-V39.0",
        "terminal_event_id": "TE-OCI-TEST.7",
        "terminal_event_sequence": 7,
        "terminal_event_sha512": digest_a,
        "transition_ledger_head_sha512": digest_a,
        "recorded_at_utc": "2026-07-16T14:00:01+00:00",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "scar_class": "CONTRACT_CONTROL_STOP",
        "stop_class": "AUDIT_INTERRUPT",
        "trigger": "Explicit Audit interrupt",
        "reason": "The runtime stopped after a contract control failure.",
        "evidence_boundary": {
            "boundary_state": "PARTIAL",
            "available_evidence_refs": ["EV-AVAILABLE-1"],
            "missing_evidence_refs": ["EV-MISSING-1"],
            "contradiction_refs": [],
            "invalid_evidence_refs": [],
            "scope_exclusions": ["SCOPE-EXCLUSION-1"],
            "boundary_reason": "One required evidence item remains unavailable.",
            "evidence_time_utc": None,
        },
        "analysis_state": {
            "inquiry_ref": "INQUIRY-1",
            "claim_refs": ["CLAIM-1"],
            "unresolved_claim_refs": ["CLAIM-2"],
            "eliminated_world_refs": ["WORLD-1"],
            "surviving_world_refs": ["WORLD-2"],
            "function_participation_refs": ["Audit"],
            "last_supported_conclusion_refs": ["CONCLUSION-1"],
            "state_summary": "The supported record stops before the unresolved claim.",
        },
        "continuation": {
            "replay_eligible": True,
            "replay_blockers": [],
            "replay_preconditions": ["Reconcile terminal transition and Scar"],
            "new_contract_required": True,
            "continuation_ref": None,
            "human_gate_decision_required": True,
        },
        "provenance_refs": ["PROV-1", "PROV-2"],
        "scar_sha512": digest_b,
    }


def valid_replay() -> dict[str, Any]:
    digest_a = "a" * 128
    digest_b = "b" * 128
    digest_c = "c" * 128
    return {
        "replay_version": "v40-candidate.1",
        "replay_id": "RP-OCI-TEST.1",
        "replay_sequence": 1,
        "decision_of_replay_id": None,
        "requested_at_utc": "2026-07-16T14:01:00+00:00",
        "prepared_at_utc": "2026-07-16T14:01:01+00:00",
        "scar_ref": "SC-OCI-TEST.7",
        "scar_sha512": digest_a,
        "source_contract_ref": "OC-V40-WAVE0-TRANCHE2",
        "source_contract_instance_id": "OCI-TEST.1",
        "source_route_id": "v40_wave0_control_route",
        "source_route_lock": "v40_wave0_control_route",
        "terminal_event_id": "TE-OCI-TEST.7",
        "terminal_event_sha512": digest_b,
        "transition_ledger_head_sha512": digest_b,
        "scar_ledger_sha512": digest_c,
        "source_canonical_binding_ref": "CANONICAL-V39.0",
        "current_canonical_binding_ref": "CANONICAL-V39.0",
        "canonical_comparison": "UNCHANGED",
        "authority_state": "NONE",
        "restored_context": [
            {"context_class": "ROUTE_CONTRACT", "ref": "OC-V40-WAVE0-TRANCHE2"},
            {"context_class": "CANONICAL_BINDING", "ref": "CANONICAL-V39.0"},
            {"context_class": "TRANSITION_LEDGER", "ref": "LEDGER-OCI-TEST.1"},
            {"context_class": "TERMINAL_EVENT", "ref": "TE-OCI-TEST.7"},
            {"context_class": "SCAR", "ref": "SC-OCI-TEST.7"},
            {"context_class": "EVIDENCE_BOUNDARY", "ref": "EV-BOUNDARY-1"},
            {"context_class": "ANALYTICAL_STATE", "ref": "ANALYSIS-STATE-1"},
            {"context_class": "FUNCTION_PARTICIPATION", "ref": "Audit"},
            {"context_class": "PRIOR_DECISION", "ref": "DECISION-1"},
        ],
        "unavailable_context": [],
        "continuation_proposal": {
            "proposed_route_id": "v40_wave0_continuation_candidate",
            "proposed_scope": ["Continue the bounded inquiry from explicit records"],
            "proposed_completion_criteria": ["Satisfy a separately authorized contract"],
            "required_evidence_refs": ["EV-MISSING-1"],
            "new_contract_required": True,
            "new_contract_ref": None,
            "new_contract_instance_id": None,
            "continuation_ref": None,
        },
        "human_gate": {
            "state": "ACTIVE",
            "decision": "PENDING",
            "decision_ref": None,
            "decided_at_utc": None,
            "decision_owner": None,
        },
        "status": "HUMAN_GATE_REVIEW",
        "previous_replay_sha512": None,
        "replay_sha512": digest_a,
    }


def authorized_replay() -> dict[str, Any]:
    value = valid_replay()
    value["replay_id"] = "RP-OCI-TEST.2"
    value["replay_sequence"] = 2
    value["decision_of_replay_id"] = "RP-OCI-TEST.1"
    value["status"] = "AUTHORIZED_NEW_CONTRACT_REQUIRED"
    value["previous_replay_sha512"] = value["replay_sha512"]
    value["replay_sha512"] = "d" * 128
    value["continuation_proposal"]["continuation_ref"] = "CONT-OCI-TEST.1"
    value["human_gate"] = {
        "state": "ACTIVE",
        "decision": "APPROVED",
        "decision_ref": "HG-APPROVE-1",
        "decided_at_utc": "2026-07-16T14:02:00+00:00",
        "decision_owner": "HUMAN",
    }
    return value


def transition_payload(**overrides: Any) -> dict[str, Any]:
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
        "evidence_refs": ["OC-V40.WAVE0.TRANCHE2"],
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


def scar_write_inputs() -> dict[str, Any]:
    value = valid_scar()
    return {
        "scar_class": value["scar_class"],
        "evidence_boundary": copy.deepcopy(value["evidence_boundary"]),
        "analysis_state": copy.deepcopy(value["analysis_state"]),
        "continuation": copy.deepcopy(value["continuation"]),
        "provenance_refs": list(value["provenance_refs"]),
    }


def complete_restored_context() -> list[dict[str, str]]:
    return [
        {"context_class": "ROUTE_CONTRACT", "ref": "OC-V40.WAVE0.TRANCHE2"},
        {"context_class": "CANONICAL_BINDING", "ref": "CANONICAL-V39.0"},
        {"context_class": "TRANSITION_LEDGER", "ref": "LEDGER-1"},
        {"context_class": "TERMINAL_EVENT", "ref": "TE-TERMINAL"},
        {"context_class": "SCAR", "ref": "SC-TERMINAL"},
        {"context_class": "EVIDENCE_BOUNDARY", "ref": "EVIDENCE-BOUNDARY-1"},
        {"context_class": "ANALYTICAL_STATE", "ref": "ANALYSIS-STATE-1"},
        {"context_class": "FUNCTION_PARTICIPATION", "ref": "Audit"},
        {"context_class": "PRIOR_DECISION", "ref": "DECISION-1"},
    ]


class ScarSchemaFixtures(unittest.TestCase):
    def assert_invalid(self, value: dict[str, Any]) -> None:
        with self.assertRaises(SchemaValidationError):
            validate_schema(value, scar_schema())

    def test_valid_scar_fixture_passes(self):
        validate_schema(valid_scar(), scar_schema())

    def test_missing_required_field_fails_closed(self):
        value = valid_scar()
        del value["reason"]
        self.assert_invalid(value)

    def test_authority_promotion_is_rejected(self):
        value = valid_scar()
        value["authority_state"] = "FULL"
        self.assert_invalid(value)

    def test_scar_cannot_carry_a_continuation_reference(self):
        value = valid_scar()
        value["continuation"]["continuation_ref"] = "CONT-1"
        self.assert_invalid(value)

    def test_malformed_or_unsupported_scar_class_is_rejected(self):
        value = valid_scar()
        value["scar_class"] = "HELPFUL_GUESS"
        self.assert_invalid(value)

    def test_duplicate_references_are_rejected(self):
        value = valid_scar()
        value["provenance_refs"] = ["PROV-1", "PROV-1"]
        self.assert_invalid(value)

    def test_malformed_hash_is_rejected(self):
        value = valid_scar()
        value["scar_sha512"] = "A" * 128
        self.assert_invalid(value)

    def test_unknown_fields_are_rejected_at_every_object_boundary(self):
        top_level = valid_scar()
        top_level["assistant_note"] = "not part of the contract"
        self.assert_invalid(top_level)

        nested = valid_scar()
        nested["evidence_boundary"]["inferred_evidence"] = []
        self.assert_invalid(nested)

    def test_unknown_evidence_time_is_explicitly_null(self):
        value = valid_scar()
        value["evidence_boundary"]["evidence_time_utc"] = None
        validate_schema(value, scar_schema())

    def test_invalid_evidence_time_is_rejected(self):
        value = valid_scar()
        value["evidence_boundary"]["evidence_time_utc"] = "sometime yesterday"
        self.assert_invalid(value)


class ReplayReceiptSchemaFixtures(unittest.TestCase):
    def assert_invalid(self, value: dict[str, Any]) -> None:
        with self.assertRaises(SchemaValidationError):
            validate_schema(value, replay_schema())

    def test_valid_human_gate_review_receipt_passes(self):
        validate_schema(valid_replay(), replay_schema())

    def test_valid_human_authorization_requires_a_new_contract(self):
        value = authorized_replay()
        validate_schema(value, replay_schema())
        self.assertIsNone(value["continuation_proposal"]["new_contract_ref"])
        self.assertIsNone(value["continuation_proposal"]["new_contract_instance_id"])

    def test_unknown_or_active_runtime_status_is_rejected(self):
        for status in ("ACTIVE", "RUNNING", "RESUMED"):
            with self.subTest(status=status):
                value = valid_replay()
                value["status"] = status
                self.assert_invalid(value)

    def test_authority_promotion_is_rejected(self):
        value = valid_replay()
        value["authority_state"] = "DELEGATED"
        self.assert_invalid(value)

    def test_preparation_receipt_cannot_contain_a_decision(self):
        value = valid_replay()
        value["human_gate"]["decision"] = "APPROVED"
        value["human_gate"]["decision_owner"] = "HUMAN"
        self.assert_invalid(value)

    def test_human_gate_review_requires_unchanged_canonical_binding(self):
        value = valid_replay()
        value["canonical_comparison"] = "DRIFTED"
        self.assert_invalid(value)

    def test_authorization_requires_human_owned_decision_metadata(self):
        value = authorized_replay()
        value["human_gate"]["decision_owner"] = None
        self.assert_invalid(value)

    def test_authorization_requires_a_continuation_reference(self):
        value = authorized_replay()
        value["continuation_proposal"]["continuation_ref"] = None
        self.assert_invalid(value)

    def test_denial_cannot_carry_a_continuation_reference(self):
        value = authorized_replay()
        value["status"] = "DENIED"
        value["human_gate"]["decision"] = "DENIED"
        value["continuation_proposal"]["continuation_ref"] = "CONT-FORBIDDEN"
        self.assert_invalid(value)

    def test_decision_receipt_must_reference_its_preparation_receipt(self):
        value = authorized_replay()
        value["decision_of_replay_id"] = None
        self.assert_invalid(value)

    def test_malformed_replay_chain_hash_is_rejected(self):
        value = authorized_replay()
        value["previous_replay_sha512"] = "not-a-sha512"
        self.assert_invalid(value)

    def test_unknown_nested_fields_are_rejected(self):
        value = valid_replay()
        value["human_gate"]["assistant_approval"] = True
        self.assert_invalid(value)


class ScarLedgerWriterFixtures(unittest.TestCase):
    contract_ref = "OC-V40.WAVE0.TRANCHE2"
    contract_instance_id = "OCI-V40.WAVE0.TRANCHE2.001"
    route_lock = "v40_candidate_wave0_tranche2"
    canonical_binding_ref = "CANONICAL-V39.0"

    def make_transition_writer(self, directory: Path) -> TransitionWitnessWriter:
        return TransitionWitnessWriter(
            directory,
            self.contract_ref,
            self.contract_instance_id,
            self.route_lock,
            clock=lambda: "2026-07-16T14:00:00+00:00",
        )

    def make_terminal_ledger(self, directory: Path) -> dict[str, Any]:
        writer = self.make_transition_writer(directory)
        writer.append(transition_payload())
        return writer.append(
            transition_payload(
                event_class="STOP",
                from_state="ACTIVE",
                to_state="STOPPED",
                trigger="explicit_audit_interrupt",
                reason="Audit stopped the contract instance",
                authorization="REJECTED",
                conformance_before="CONFORMING",
                conformance_after="NONCONFORMING",
                audit_result="FAIL",
                stop_class="AUDIT_INTERRUPT",
                scar_required=True,
                scar_reason="Audit stopped the contract instance",
            )
        )

    def make_scar_writer(self, scar_dir: Path, transition_dir: Path, **options: Any) -> ScarLedgerWriter:
        return ScarLedgerWriter(
            scar_dir,
            transition_dir,
            self.contract_ref,
            self.contract_instance_id,
            self.route_lock,
            self.canonical_binding_ref,
            clock=lambda: "2026-07-16T14:00:01+00:00",
            **options,
        )

    def reconcile(self, root: Path, **options: Any) -> dict[str, Any]:
        return reconcile_scars(
            root / "transitions",
            root / "scars",
            self.contract_ref,
            self.contract_instance_id,
            self.route_lock,
            self.canonical_binding_ref,
            **options,
        )

    def test_fixture_01_valid_terminal_event_produces_one_valid_scar(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            scar = writer.append(event["event_id"], **scar_write_inputs())
            self.assertEqual(scar["terminal_event_sha512"], event["event_sha512"])
            self.assertEqual(scar["transition_ledger_head_sha512"], event["event_sha512"])
            self.assertEqual(scar["scar_sha512"], scar_digest(scar))
            self.assertEqual(len(list((root / "scars").glob("*.json"))), 1)

    def test_fixture_04_duplicate_scar_for_terminal_event_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            writer.append(event["event_id"], **scar_write_inputs())
            with self.assertRaisesRegex(ContinuityError, "duplicate Scar terminal-event binding"):
                writer.append(event["event_id"], **scar_write_inputs())
            self.assertEqual(len(list((root / "scars").glob("*.json"))), 1)

    def test_fixture_05_nonterminal_event_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transition_writer = self.make_transition_writer(root / "transitions")
            event = transition_writer.append(transition_payload())
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            with self.assertRaisesRegex(ContinuityError, "terminal STOPPED transition"):
                writer.append(event["event_id"], **scar_write_inputs())
            self.assertEqual(list((root / "scars").glob("*.json")), [])

    def test_fixture_08_contract_instance_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = ScarLedgerWriter(
                root / "scars",
                root / "transitions",
                self.contract_ref,
                "OCI-DIFFERENT.001",
                self.route_lock,
                self.canonical_binding_ref,
            )
            with self.assertRaisesRegex(ContinuityError, "transition contract binding mismatch"):
                writer.append(event["event_id"], **scar_write_inputs())

    def test_fixture_09_route_lock_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = ScarLedgerWriter(
                root / "scars",
                root / "transitions",
                self.contract_ref,
                self.contract_instance_id,
                "different_route",
                self.canonical_binding_ref,
            )
            with self.assertRaisesRegex(ContinuityError, "transition route-lock mismatch"):
                writer.append(event["event_id"], **scar_write_inputs())

    def test_fixture_10_existing_scar_canonical_binding_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            writer.append(event["event_id"], **scar_write_inputs())
            with self.assertRaisesRegex(ContinuityError, "Scar canonical binding mismatch"):
                ScarLedgerWriter(
                    root / "scars",
                    root / "transitions",
                    self.contract_ref,
                    self.contract_instance_id,
                    self.route_lock,
                    "CANONICAL-DIFFERENT",
                )

    def test_fixture_11_scar_digest_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            writer.append(event["event_id"], **scar_write_inputs())
            path = next((root / "scars").glob("*.json"))
            scar = json.loads(path.read_text(encoding="utf-8"))
            scar["reason"] = "tampered"
            path.write_text(json.dumps(scar), encoding="utf-8")
            with self.assertRaisesRegex(ContinuityError, "scar_sha512 mismatch"):
                self.make_scar_writer(root / "scars", root / "transitions")

    def test_fixture_13_scar_overwrite_attempt_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            expected_id = f"SC-{self.contract_instance_id.removeprefix('OCI-')}-{event['sequence']:06d}"
            target = root / "scars" / f"{event['sequence']:06d}_{expected_id}.json"
            target.write_text("occupied", encoding="utf-8")
            with self.assertRaisesRegex(ContinuityError, "Scar overwrite refused"):
                writer.append(event["event_id"], **scar_write_inputs())
            self.assertEqual(target.read_text(encoding="utf-8"), "occupied")

    def test_fixture_14_persistence_failure_leaves_no_partial_scar(self):
        def fail_publish(_temporary: Path, _target: Path) -> None:
            raise OSError("simulated Scar persistence failure")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions", publisher=fail_publish)
            with self.assertRaisesRegex(ScarPersistenceError, "simulated Scar persistence failure"):
                writer.append(event["event_id"], **scar_write_inputs())
            self.assertEqual(list((root / "scars").iterdir()), [])

    def test_reconciliation_complete_binds_the_full_scar_set(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            scar = writer.append(event["event_id"], **scar_write_inputs())
            result = self.reconcile(root)
            self.assertEqual(result["state"], "COMPLETE")
            self.assertEqual(result["terminal_event_ids"], [event["event_id"]])
            self.assertEqual(result["scar_ids"], [scar["scar_id"]])
            self.assertRegex(result["scar_ledger_sha512"], r"^[0-9a-f]{128}$")

    def test_fixture_02_terminal_event_missing_scar_reconciles_as_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            (root / "scars").mkdir()
            result = self.reconcile(root)
            self.assertEqual(result["state"], "MISSING_SCAR")
            self.assertEqual(result["missing_terminal_event_ids"], [event["event_id"]])

    def test_fixture_03_orphan_scar_reconciles_as_orphan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            writer.append(event["event_id"], **scar_write_inputs())
            path = next((root / "scars").glob("*.json"))
            scar = json.loads(path.read_text(encoding="utf-8"))
            scar["terminal_event_id"] = "TE-ORPHAN.999"
            scar["scar_sha512"] = scar_digest(scar)
            path.write_text(json.dumps(scar), encoding="utf-8")
            result = self.reconcile(root)
            self.assertEqual(result["state"], "ORPHAN_SCAR")
            self.assertEqual(result["orphan_scar_ids"], [scar["scar_id"]])

    def test_duplicate_scar_ledger_reconciles_as_duplicate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            first = writer.append(event["event_id"], **scar_write_inputs())
            duplicate = copy.deepcopy(first)
            duplicate["scar_id"] = first["scar_id"] + "-DUP"
            duplicate["scar_sha512"] = scar_digest(duplicate)
            path = root / "scars" / f"{event['sequence']:06d}_{duplicate['scar_id']}.json"
            path.write_text(json.dumps(duplicate), encoding="utf-8")
            result = self.reconcile(root)
            self.assertEqual(result["state"], "DUPLICATE_SCAR")
            self.assertEqual(result["duplicate_terminal_event_ids"], [event["event_id"]])

    def test_fixture_06_terminal_event_hash_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            writer.append(event["event_id"], **scar_write_inputs())
            path = next((root / "scars").glob("*.json"))
            scar = json.loads(path.read_text(encoding="utf-8"))
            scar["terminal_event_sha512"] = "f" * 128
            scar["scar_sha512"] = scar_digest(scar)
            path.write_text(json.dumps(scar), encoding="utf-8")
            result = self.reconcile(root)
            self.assertEqual(result["state"], "BINDING_MISMATCH")

    def test_fixture_07_transition_ledger_head_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            writer.append(event["event_id"], **scar_write_inputs())
            path = next((root / "scars").glob("*.json"))
            scar = json.loads(path.read_text(encoding="utf-8"))
            scar["transition_ledger_head_sha512"] = "e" * 128
            scar["scar_sha512"] = scar_digest(scar)
            path.write_text(json.dumps(scar), encoding="utf-8")
            result = self.reconcile(root)
            self.assertEqual(result["state"], "BINDING_MISMATCH")

    def test_reconciliation_distinguishes_integrity_failure_from_binding_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            writer.append(event["event_id"], **scar_write_inputs())
            path = next((root / "scars").glob("*.json"))
            scar = json.loads(path.read_text(encoding="utf-8"))
            scar["reason"] = "tampered without updating integrity"
            path.write_text(json.dumps(scar), encoding="utf-8")
            result = self.reconcile(root)
            self.assertEqual(result["state"], "INTEGRITY_FAILURE")

    def test_fixture_15_unknown_evidence_remains_explicitly_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            inputs = scar_write_inputs()
            inputs["evidence_boundary"]["boundary_state"] = "UNKNOWN"
            inputs["evidence_boundary"]["evidence_time_utc"] = None
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            scar = writer.append(event["event_id"], **inputs)
            self.assertEqual(scar["evidence_boundary"]["boundary_state"], "UNKNOWN")
            self.assertIsNone(scar["evidence_boundary"]["evidence_time_utc"])

    def test_fixture_16_missing_evidence_is_carried_explicitly(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = self.make_terminal_ledger(root / "transitions")
            inputs = scar_write_inputs()
            inputs["evidence_boundary"]["missing_evidence_refs"] = ["EV-REQUIRED-BUT-MISSING"]
            writer = self.make_scar_writer(root / "scars", root / "transitions")
            scar = writer.append(event["event_id"], **inputs)
            self.assertEqual(
                scar["evidence_boundary"]["missing_evidence_refs"],
                ["EV-REQUIRED-BUT-MISSING"],
            )


class StructuredThirdsMarkerFixtures(unittest.TestCase):
    def make_plane(self, directory: Path) -> RuntimeControlPlane:
        selected = operational_contract()
        handlers = {action: (lambda: None) for action in selected["route"]["permitted_actions"]}
        plane = RuntimeControlPlane(
            selected,
            directory,
            action_handlers=handlers,
            writer_options={"clock": lambda: "2026-07-16T14:10:00+00:00"},
        )
        plane.activate()
        return plane

    @staticmethod
    def marker(**overrides: Any) -> dict[str, Any]:
        value = {
            "marker_kind": "REPEATING_ONE_THIRD",
            "condition_class": "UNRESOLVED_CONTRADICTION",
            "source_ref": "SENSOR-TRACE-1",
            "observation_time_utc": "2026-07-16T14:09:59+00:00",
            "evidence_refs": ["EV-CONTRADICTION-1"],
        }
        value.update(overrides)
        return value

    def test_fixture_17_structured_repeating_one_third_terminates_and_requires_scar(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(Path(directory))
            with self.assertRaises(AuditInterrupted):
                plane.observe_runtime_marker(self.marker())
            self.assertEqual(plane.state, "STOPPED")
            self.assertEqual(plane.stop_class, "AUDIT_INTERRUPT")
            self.assertEqual(plane.required_scar_class, "UNRESOLVED_CONTRADICTION")
            self.assertTrue(plane.writer.sequence >= 2)

    def test_fixture_18_structured_repeating_two_thirds_terminates_and_requires_scar(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(Path(directory))
            marker = self.marker(
                marker_kind="REPEATING_TWO_THIRDS",
                condition_class="EVIDENCE_BOUNDARY_EXHAUSTION",
            )
            with self.assertRaises(AuditInterrupted):
                plane.observe_runtime_marker(marker)
            self.assertEqual(plane.required_scar_class, "EVIDENCE_BOUNDARY_EXHAUSTION")

    def test_fixture_19_normal_numeric_one_third_does_not_trigger(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(Path(directory))
            result = plane.observe_runtime_marker(1 / 3)
            self.assertFalse(result["detected"])
            self.assertEqual(plane.state, "ACTIVE")
            self.assertIsNone(plane.required_scar_class)

    def test_fixture_20_free_form_prose_does_not_trigger(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(Path(directory))
            result = plane.observe_runtime_marker("The report literally contains .333 and .666 as quoted text.")
            self.assertFalse(result["detected"])
            self.assertEqual(plane.state, "ACTIVE")

    def test_confidence_object_does_not_trigger(self):
        value = {"confidence": 0.6666666666666666, "source_ref": "MODEL-1"}
        self.assertIsNone(detect_repeating_thirds_marker(value))

    def test_fixture_21_detection_is_self_observation_not_confidence(self):
        observation = detect_repeating_thirds_marker(self.marker())
        self.assertIsNotNone(observation)
        assert observation is not None
        self.assertEqual(observation["self_observation"], "SUCCESSFUL")
        self.assertEqual(observation["confidence_interpretation"], "NOT_CONFIDENCE")
        self.assertTrue(observation["termination_required"])

    def test_fixture_22_unknown_thirds_condition_terminates_without_fabrication(self):
        with tempfile.TemporaryDirectory() as directory:
            plane = self.make_plane(Path(directory))
            marker = self.marker(condition_class="UNKNOWN")
            with self.assertRaises(AuditInterrupted):
                plane.observe_runtime_marker(marker)
            self.assertEqual(plane.required_scar_class, "UNCLASSIFIED_CONTROL_STOP")
            self.assertEqual(plane.last_runtime_control_marker["condition_class"], "UNKNOWN")

    def test_malformed_structured_marker_fails_closed_before_classification(self):
        marker = self.marker()
        del marker["source_ref"]
        with self.assertRaisesRegex(ContinuityError, "malformed thirds marker"):
            detect_repeating_thirds_marker(marker)


class MinimumReplayFixtures(unittest.TestCase):
    contract_ref = "OC-V40.WAVE0.TRANCHE2"
    contract_instance_id = "OCI-V40.WAVE0.TRANCHE2.001"
    route_lock = "v40_candidate_wave0_tranche2"
    canonical_binding_ref = "CANONICAL-V39.0"

    def create_terminal_scar(self, root: Path, *, evidence_time_utc: str | None = None) -> dict[str, Any]:
        transition_writer = TransitionWitnessWriter(
            root / "transitions",
            self.contract_ref,
            self.contract_instance_id,
            self.route_lock,
            clock=lambda: "2026-07-16T14:20:00+00:00",
        )
        transition_writer.append(transition_payload())
        event = transition_writer.append(
            transition_payload(
                event_class="STOP",
                from_state="ACTIVE",
                to_state="STOPPED",
                trigger="explicit_audit_interrupt",
                reason="Audit stopped the contract instance",
                authorization="REJECTED",
                conformance_before="CONFORMING",
                conformance_after="NONCONFORMING",
                audit_result="FAIL",
                stop_class="AUDIT_INTERRUPT",
                scar_required=True,
                scar_reason="Audit stopped the contract instance",
            )
        )
        scar_writer = ScarLedgerWriter(
            root / "scars",
            root / "transitions",
            self.contract_ref,
            self.contract_instance_id,
            self.route_lock,
            self.canonical_binding_ref,
            clock=lambda: "2026-07-16T14:20:01+00:00",
        )
        inputs = scar_write_inputs()
        inputs["evidence_boundary"]["evidence_time_utc"] = evidence_time_utc
        return scar_writer.append(event["event_id"], **inputs)

    def make_replay(self, root: Path, **options: Any) -> MinimumReplay:
        return MinimumReplay(
            root / "transitions",
            root / "scars",
            root / "replays",
            self.contract_ref,
            self.contract_instance_id,
            self.route_lock,
            self.canonical_binding_ref,
            clock=lambda: "2026-07-16T14:20:02+00:00",
            **options,
        )

    def prepare(self, replay: MinimumReplay, scar_ref: str, **overrides: Any) -> dict[str, Any]:
        values: dict[str, Any] = {
            "requested_at_utc": "2026-07-16T14:19:59+00:00",
            "current_canonical_binding_ref": self.canonical_binding_ref,
            "canonical_comparison": "UNCHANGED",
            "restored_context": complete_restored_context(),
            "unavailable_context": [],
            "proposed_route_id": "v40_candidate_continuation",
            "proposed_scope": ["Continue the bounded inquiry"],
            "proposed_completion_criteria": ["Meet the new contract criteria"],
            "required_evidence_refs": ["EV-MISSING-1"],
        }
        values.update(overrides)
        return replay.prepare(scar_ref, **values)

    def test_minimum_replay_prepares_review_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            before_transitions = sorted(path.name for path in (root / "transitions").glob("*.json"))
            replay = self.make_replay(root)
            receipt = self.prepare(replay, scar["scar_id"])
            after_transitions = sorted(path.name for path in (root / "transitions").glob("*.json"))
            self.assertEqual(receipt["status"], "HUMAN_GATE_REVIEW")
            self.assertEqual(receipt["human_gate"]["decision"], "PENDING")
            self.assertEqual(receipt["authority_state"], "NONE")
            self.assertEqual(receipt["replay_sha512"], replay_digest(receipt))
            self.assertEqual(before_transitions, after_transitions)

    def test_fixture_23_replay_preparation_fails_when_scar_reconciliation_is_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transition_writer = TransitionWitnessWriter(
                root / "transitions",
                self.contract_ref,
                self.contract_instance_id,
                self.route_lock,
                clock=lambda: "2026-07-16T14:20:00+00:00",
            )
            transition_writer.append(transition_payload())
            event = transition_writer.append(
                transition_payload(
                    event_class="STOP",
                    from_state="ACTIVE",
                    to_state="STOPPED",
                    trigger="explicit_audit_interrupt",
                    reason="stop",
                    authorization="REJECTED",
                    conformance_after="NONCONFORMING",
                    audit_result="FAIL",
                    stop_class="AUDIT_INTERRUPT",
                    scar_required=True,
                    scar_reason="stop",
                )
            )
            (root / "scars").mkdir()
            replay = self.make_replay(root)
            with self.assertRaisesRegex(ContinuityError, "requires COMPLETE Scar reconciliation; got MISSING_SCAR"):
                self.prepare(replay, f"SC-{event['event_id']}")
            self.assertEqual(list((root / "replays").glob("*.json")), [])

    def test_fixture_24_replay_preparation_fails_on_invalid_scar_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            path = next((root / "scars").glob("*.json"))
            value = json.loads(path.read_text(encoding="utf-8"))
            value["reason"] = "tampered"
            path.write_text(json.dumps(value), encoding="utf-8")
            replay = self.make_replay(root)
            with self.assertRaisesRegex(ContinuityError, "got INTEGRITY_FAILURE"):
                self.prepare(replay, scar["scar_id"])

    def test_fixture_25_replay_blocks_on_canonical_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            receipt = self.prepare(
                replay,
                scar["scar_id"],
                current_canonical_binding_ref="CANONICAL-V40.1-DIFFERENT",
                canonical_comparison="DRIFTED",
            )
            self.assertEqual(receipt["status"], "BLOCKED")
            self.assertEqual(receipt["human_gate"]["decision"], "PENDING")

    def test_fixture_26_unavailable_context_is_recorded_without_conversation_reconstruction(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            restored = complete_restored_context()
            restored = [item for item in restored if item["context_class"] != "PRIOR_DECISION"]
            unavailable = [
                {
                    "context_class": "PRIOR_DECISION",
                    "ref": None,
                    "reason": "No prior decision record exists in the explicit source set",
                }
            ]
            replay = self.make_replay(root)
            receipt = self.prepare(
                replay,
                scar["scar_id"],
                restored_context=restored,
                unavailable_context=unavailable,
            )
            self.assertEqual(receipt["status"], "BLOCKED")
            self.assertEqual(receipt["unavailable_context"], unavailable)
            self.assertNotIn("conversation", json.dumps(receipt).lower())

    def test_fixture_27_replay_cannot_reopen_the_source_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            receipt = self.prepare(replay, scar["scar_id"])
            self.assertNotIn(receipt["status"], {"ACTIVE", "RUNNING", "RESUMED"})
            terminal = json.loads(sorted((root / "transitions").glob("*.json"))[-1].read_text(encoding="utf-8"))
            self.assertEqual(terminal["to_state"], "STOPPED")

    def test_fixture_28_replay_cannot_execute_the_continuation_proposal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            receipt = self.prepare(replay, scar["scar_id"])
            proposal = receipt["continuation_proposal"]
            self.assertTrue(proposal["new_contract_required"])
            self.assertIsNone(proposal["new_contract_ref"])
            self.assertIsNone(proposal["new_contract_instance_id"])
            self.assertIsNone(proposal["continuation_ref"])

    def test_fixture_29_human_gate_remains_latched_before_decision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            receipt = self.prepare(replay, scar["scar_id"])
            self.assertEqual(receipt["status"], "HUMAN_GATE_REVIEW")
            self.assertEqual(
                receipt["human_gate"],
                {
                    "state": "ACTIVE",
                    "decision": "PENDING",
                    "decision_ref": None,
                    "decided_at_utc": None,
                    "decision_owner": None,
                },
            )

    def test_fixture_30_runtime_generated_approval_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            preparation = self.prepare(replay, scar["scar_id"])
            with self.assertRaisesRegex(ContinuityError, "non-human Replay approval is forbidden"):
                replay.record_human_decision(
                    preparation["replay_id"],
                    approved=True,
                    decision_ref="RUNTIME-GUESS-1",
                    decided_at_utc="2026-07-16T14:20:03+00:00",
                    decision_owner="RUNTIME",
                )
            self.assertEqual(len(replay.writer.receipts), 1)

    def test_fixture_31_human_gate_denial_produces_immutable_denied_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            preparation = self.prepare(replay, scar["scar_id"])
            denial = replay.record_human_decision(
                preparation["replay_id"],
                approved=False,
                decision_ref="HG-DENY-1",
                decided_at_utc="2026-07-16T14:20:03+00:00",
                decision_owner="HUMAN",
            )
            self.assertEqual(denial["status"], "DENIED")
            self.assertEqual(denial["decision_of_replay_id"], preparation["replay_id"])
            self.assertIsNone(denial["continuation_proposal"]["continuation_ref"])
            self.assertEqual(denial["previous_replay_sha512"], preparation["replay_sha512"])
            with self.assertRaisesRegex(ContinuityError, "already has an immutable"):
                replay.record_human_decision(
                    preparation["replay_id"],
                    approved=True,
                    decision_ref="HG-SECOND-DECISION",
                    decided_at_utc="2026-07-16T14:20:04+00:00",
                    decision_owner="HUMAN",
                )

    def test_fixture_32_approval_requires_new_contract_not_active_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            preparation = self.prepare(replay, scar["scar_id"])
            approval = replay.record_human_decision(
                preparation["replay_id"],
                approved=True,
                decision_ref="HG-APPROVE-1",
                decided_at_utc="2026-07-16T14:20:03+00:00",
                decision_owner="HUMAN",
            )
            self.assertEqual(approval["status"], "AUTHORIZED_NEW_CONTRACT_REQUIRED")
            self.assertNotIn(approval["status"], {"ACTIVE", "RUNNING", "RESUMED"})
            self.assertEqual(approval["human_gate"]["decision_owner"], "HUMAN")

    def test_fixture_33_approval_creates_reference_but_no_contract_or_route_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            preparation = self.prepare(replay, scar["scar_id"])
            transition_files = sorted(path.name for path in (root / "transitions").glob("*.json"))
            approval = replay.record_human_decision(
                preparation["replay_id"],
                approved=True,
                decision_ref="HG-APPROVE-2",
                decided_at_utc="2026-07-16T14:20:03+00:00",
                decision_owner="HUMAN",
            )
            proposal = approval["continuation_proposal"]
            self.assertRegex(proposal["continuation_ref"], r"^CONT-[A-Z0-9._-]+$")
            self.assertIsNone(proposal["new_contract_ref"])
            self.assertIsNone(proposal["new_contract_instance_id"])
            self.assertEqual(
                sorted(path.name for path in (root / "transitions").glob("*.json")),
                transition_files,
            )

    def test_fixture_34_replay_receipt_overwrite_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            preparation = self.prepare(replay, scar["scar_id"])
            next_id = f"RP-{self.contract_instance_id.removeprefix('OCI-')}-000002"
            target = root / "replays" / f"000002_{next_id}.json"
            target.write_text("occupied", encoding="utf-8")
            with self.assertRaises(ContinuityError):
                replay.record_human_decision(
                    preparation["replay_id"],
                    approved=False,
                    decision_ref="HG-DENY-OVERWRITE",
                    decided_at_utc="2026-07-16T14:20:03+00:00",
                    decision_owner="HUMAN",
                )
            self.assertEqual(target.read_text(encoding="utf-8"), "occupied")

    def test_fixture_35_replay_sequence_gap_and_hash_chain_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            preparation = self.prepare(replay, scar["scar_id"])
            replay.record_human_decision(
                preparation["replay_id"],
                approved=False,
                decision_ref="HG-DENY-CHAIN",
                decided_at_utc="2026-07-16T14:20:03+00:00",
                decision_owner="HUMAN",
            )
            path = sorted((root / "replays").glob("*.json"))[-1]
            decision = json.loads(path.read_text(encoding="utf-8"))
            decision["previous_replay_sha512"] = "f" * 128
            decision["replay_sha512"] = replay_digest(decision)
            path.write_text(json.dumps(decision), encoding="utf-8")
            with self.assertRaisesRegex(ContinuityError, "previous-receipt hash mismatch"):
                ReplayLedgerWriter(root / "replays", self.contract_ref, self.contract_instance_id)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scar = self.create_terminal_scar(root)
            replay = self.make_replay(root)
            preparation = self.prepare(replay, scar["scar_id"])
            decision = replay.record_human_decision(
                preparation["replay_id"],
                approved=False,
                decision_ref="HG-DENY-SEQUENCE",
                decided_at_utc="2026-07-16T14:20:03+00:00",
                decision_owner="HUMAN",
            )
            path = sorted((root / "replays").glob("*.json"))[-1]
            decision["replay_sequence"] = 3
            decision["replay_sha512"] = replay_digest(decision)
            path.write_text(json.dumps(decision), encoding="utf-8")
            with self.assertRaisesRegex(ContinuityError, "sequence gap or rollback"):
                ReplayLedgerWriter(root / "replays", self.contract_ref, self.contract_instance_id)

    def test_fixture_36_temporal_fields_remain_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence_time = "2026-07-16T14:19:58+00:00"
            scar = self.create_terminal_scar(root, evidence_time_utc=evidence_time)
            replay = self.make_replay(root)
            preparation = self.prepare(replay, scar["scar_id"])
            decision_time = "2026-07-16T14:20:03+00:00"
            decision = replay.record_human_decision(
                preparation["replay_id"],
                approved=False,
                decision_ref="HG-DENY-TIME",
                decided_at_utc=decision_time,
                decision_owner="HUMAN",
            )
            terminal = json.loads(sorted((root / "transitions").glob("*.json"))[-1].read_text(encoding="utf-8"))
            observed_times = {
                evidence_time,
                terminal["timestamp_utc"],
                scar["recorded_at_utc"],
                preparation["requested_at_utc"],
                preparation["prepared_at_utc"],
                decision["human_gate"]["decided_at_utc"],
            }
            self.assertEqual(len(observed_times), 6)


class ContinuityRegressionBoundaryFixtures(unittest.TestCase):
    def test_fixture_37_default_validation_leaves_repository_tree_unchanged(self):
        before = subprocess.run(
            ["git", "status", "--porcelain=v1"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        before_caches = {path for path in (ROOT / "candidate").rglob("__pycache__")}
        child_environment = dict(os.environ)
        child_environment.pop("PYTHONDONTWRITEBYTECODE", None)
        result = subprocess.run(
            [sys.executable, "candidate/v40/tools/validate_continuity.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            env=child_environment,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no persistent output", result.stdout)
        after = subprocess.run(
            ["git", "status", "--porcelain=v1"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertEqual(after, before)
        after_caches = {path for path in (ROOT / "candidate").rglob("__pycache__")}
        self.assertEqual(after_caches, before_caches)

    def test_fixture_38_validation_cannot_activate_external_runtime_or_populate_system(self):
        contract = operational_contract()
        self.assertEqual(contract["authority_state"], "NONE")
        self.assertEqual(contract["human_gate"], "ACTIVE")
        self.assertEqual(contract["posture"]["external_runtime"], "DISABLED")
        self.assertEqual(contract["posture"]["system_population"], "DISALLOWED")
        source = (ROOT / "candidate/v40/tools/validate_continuity.py").read_text(encoding="utf-8")
        self.assertNotIn("git push", source)
        self.assertNotIn("subprocess", source)


if __name__ == "__main__":
    unittest.main()
