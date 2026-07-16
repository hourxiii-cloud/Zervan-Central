from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from candidate.v40.runtime.schema_validation import SchemaValidationError, validate_schema


ROOT = Path(__file__).resolve().parents[1]
STATE_SCHEMA_PATH = ROOT / "candidate/v40/contracts/production_state.schema.json"
EVENT_SCHEMA_PATH = ROOT / "candidate/v40/contracts/production_event.schema.json"

PRODUCTION_STATES = [
    "DISCOVERY",
    "ANALYSIS_COMPLETE",
    "REPORTING",
    "RECONCILIATION",
    "REVIEW_READY",
    "HUMAN_GATE_REVIEW",
    "PROMOTED",
    "RETURNED",
    "STOPPED",
]

PRODUCTION_FAILURE_CLASSES = [
    "CANONICAL_BINDING_FAILURE",
    "CONTRACT_NONCONFORMANCE",
    "ANALYTICAL_FREEZE_FAILURE",
    "REPORT_MUTATION",
    "LINEAGE_BREAK",
    "REQUIREMENT_OMISSION",
    "INVENTORY_OMISSION",
    "PLACEHOLDER_SUBSTITUTION",
    "EVIDENCE_CARRIAGE_FAILURE",
    "ESCALATION_ORDER_FAILURE",
    "SCOPE_INFLATION",
    "STANDALONE_REVIEW_FAILURE",
    "PACKAGE_INTEGRITY_FAILURE",
    "COMPLETION_MISMATCH",
    "CLAIM_CEILING_VIOLATION",
    "HUMAN_GATE_REQUIRED",
    "HUMAN_GATE_DENIED",
    "LOGIC_FREEZE",
    "UNKNOWN_PRODUCTION_FAILURE",
]

EVENT_CLASSES = [
    "ANALYTICAL_FREEZE_ACCEPTED",
    "PROJECTION_ACCEPTED",
    "ARTIFACT_PRODUCED",
    "RECONCILIATION_STARTED",
    "BOUNDED_RECONCILIATION_RETURN",
    "REVIEW_READY_DECLARED",
    "HUMAN_GATE_REQUESTED",
    "HUMAN_GATE_DECISION",
    "AUDIT_STOP",
]


def load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def state_schema() -> dict:
    return load_schema(STATE_SCHEMA_PATH)


def event_schema() -> dict:
    return load_schema(EVENT_SCHEMA_PATH)


def git_binding(branch: str, commit: str) -> dict:
    return {
        "repository": "https://github.com/hourxiii-cloud/Zervan-Core-v39.git",
        "branch": branch,
        "commit": commit,
    }


def valid_state(current_state: str = "DISCOVERY") -> dict:
    value = {
        "production_state_version": "v40-candidate.1",
        "production_state_id": "PS-REPORTING-001",
        "contract_ref": "OC-V40.WAVE1.REPORTING-PRODUCTION",
        "contract_instance_id": "OCI-V40.WAVE1.REPORTING-PRODUCTION.001",
        "request_ref": "USER-REQUEST-REPORT-001",
        "route_ref": "v40_candidate_wave1_reporting_production",
        "route_lock": "sha512:" + "1" * 128,
        "canonical_git_binding": git_binding(
            "main", "d07023f028833f3ed1b61eebbd3298ed61c28d72"
        ),
        "candidate_git_binding": git_binding(
            "candidate/v40-wave0", "9" * 40
        ),
        "current_state": current_state,
        "freeze_ref": None,
        "freeze_sha512": None,
        "projection_ref": None,
        "projection_sha512": None,
        "manifest_ref": None,
        "manifest_sha512": None,
        "completion_receipt_ref": None,
        "human_gate_request_ref": None,
        "human_gate_decision_ref": None,
        "event_count": 0,
        "last_event_ref": None,
        "last_event_sha512": None,
        "reconciliation_return_count": 0,
        "non_progressing_return_count": 0,
        "last_verified_state": None,
        "production_failure_class": None,
        "terminal": False,
        "scar_required": False,
        "external_action_state": "NOT_AUTHORIZED",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "created_at_utc": "2026-07-16T21:00:00+00:00",
        "updated_at_utc": "2026-07-16T21:00:00+00:00",
        "production_state_sha512": "a" * 128,
    }

    if current_state == "DISCOVERY":
        return value

    value.update(
        event_count=1,
        last_event_ref="PE-REPORTING-001",
        last_event_sha512="b" * 128,
    )
    if current_state == "STOPPED":
        value.update(
            freeze_ref="AIF-REPORTING-001",
            freeze_sha512="c" * 128,
            projection_ref="RP-REPORTING-001",
            projection_sha512="d" * 128,
            last_verified_state="REPORTING",
            production_failure_class="REPORT_MUTATION",
            terminal=True,
            scar_required=True,
        )
        return value

    value.update(
        freeze_ref="AIF-REPORTING-001",
        freeze_sha512="c" * 128,
    )
    if current_state == "ANALYSIS_COMPLETE":
        return value

    value.update(
        projection_ref="RP-REPORTING-001",
        projection_sha512="d" * 128,
    )
    if current_state in {"REPORTING", "RECONCILIATION"}:
        return value

    value.update(
        manifest_ref="PM-REPORTING-001",
        manifest_sha512="e" * 128,
        completion_receipt_ref="PCR-REPORTING-001",
    )
    if current_state == "REVIEW_READY":
        return value

    value["human_gate_request_ref"] = "HGR-REPORTING-001"
    if current_state == "HUMAN_GATE_REVIEW":
        return value

    value.update(
        human_gate_decision_ref="HGD-REPORTING-001",
        terminal=True,
    )
    return value


def valid_decision(next_state: str = "PROMOTED") -> dict:
    return {
        "decision_ref": "HGD-REPORTING-001",
        "decision_owner": "HUMAN",
        "authorized_next_state": next_state,
        "review_ready_receipt_ref": "PCR-REPORTING-001",
        "manifest_ref": "PM-REPORTING-001",
        "manifest_sha512": "e" * 128,
        "authorized_scope": ["candidate_review_state_only"],
        "external_movement_included": False,
        "authorized_target_or_audience": None,
        "decision_time_utc": "2026-07-16T21:09:00+00:00",
        "limitations_and_conditions": [
            "External delivery requires separate authorization."
        ],
    }


def valid_return_boundary() -> dict:
    return {
        "return_id": "PRR-REPORTING-001",
        "defect_class": "BROKEN_LOCAL_ANCHOR",
        "defect_ref": "DEFECT-ANCHOR-001",
        "route_unchanged": True,
        "freeze_unchanged": True,
        "projection_valid": True,
        "claim_mutation_detected": False,
        "evidence_mutation_detected": False,
        "uncertainty_mutation_detected": False,
        "lineage_mutation_detected": False,
        "progress_state": "PROGRESSING",
        "return_ordinal": 1,
        "prior_return_event_refs": [],
    }


def valid_event(event_class: str = "ARTIFACT_PRODUCED", *, returned: bool = False) -> dict:
    value = {
        "production_event_version": "v40-candidate.1",
        "production_event_id": "PE-REPORTING-002",
        "production_state_ref": "PS-REPORTING-001",
        "contract_ref": "OC-V40.WAVE1.REPORTING-PRODUCTION",
        "contract_instance_id": "OCI-V40.WAVE1.REPORTING-PRODUCTION.001",
        "sequence": 2,
        "timestamp_utc": "2026-07-16T21:02:00+00:00",
        "event_class": event_class,
        "from_state": "REPORTING",
        "to_state": "REPORTING",
        "trigger": "artifact_production",
        "reason": "Produce one declared local artifact inside the locked route.",
        "request_ref": "USER-REQUEST-REPORT-001",
        "route_ref": "v40_candidate_wave1_reporting_production",
        "route_lock": "sha512:" + "1" * 128,
        "canonical_commit": "d07023f028833f3ed1b61eebbd3298ed61c28d72",
        "candidate_commit": "9" * 40,
        "freeze_ref": "AIF-REPORTING-001",
        "freeze_sha512": "c" * 128,
        "projection_ref": "RP-REPORTING-001",
        "projection_sha512": "d" * 128,
        "artifact_refs": ["ARTIFACT-REPORT-001"],
        "completion_declaration_ref": None,
        "completion_receipt_ref": None,
        "manifest_ref": None,
        "manifest_sha512": None,
        "gate_receipt_refs": [],
        "human_gate_request_ref": None,
        "human_gate_decision": None,
        "reconciliation_return": None,
        "production_failure_class": None,
        "audit_result": "NOT_INVOKED",
        "control_stop_class": None,
        "control_transition_event_ref": None,
        "scar_required": False,
        "external_action_state": "NOT_AUTHORIZED",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "previous_event_sha512": "f" * 128,
        "event_sha512": "0" * 128,
    }

    if event_class == "ANALYTICAL_FREEZE_ACCEPTED":
        value.update(
            production_event_id="PE-REPORTING-001",
            sequence=1,
            previous_event_sha512=None,
            from_state="DISCOVERY",
            to_state="ANALYSIS_COMPLETE",
            trigger="analytical_inventory_frozen",
            reason="Accept the valid immutable analytical inventory freeze.",
            projection_ref=None,
            projection_sha512=None,
            artifact_refs=[],
            audit_result="PASS",
        )
    elif event_class == "PROJECTION_ACCEPTED":
        value.update(
            from_state="ANALYSIS_COMPLETE",
            to_state="REPORTING",
            trigger="report_projection_locked",
            reason="Accept the valid locked Report Projection.",
            artifact_refs=[],
            audit_result="PASS",
        )
    elif event_class == "RECONCILIATION_STARTED":
        value.update(
            to_state="RECONCILIATION",
            trigger="all_required_artifacts_declared",
            reason="Begin reconciliation after declaring every required artifact.",
            completion_declaration_ref="PCD-REPORTING-001",
            audit_result="PASS",
        )
    elif event_class == "BOUNDED_RECONCILIATION_RETURN":
        value.update(
            from_state="RECONCILIATION",
            to_state="REPORTING",
            trigger="bounded_artifact_defect",
            reason="Return for a bounded non-integrity anchor defect.",
            reconciliation_return=valid_return_boundary(),
            audit_result="PASS",
        )
    elif event_class == "REVIEW_READY_DECLARED":
        value.update(
            from_state="RECONCILIATION",
            to_state="REVIEW_READY",
            trigger="mandatory_gates_passed",
            reason="Declare review readiness after every mandatory gate passes.",
            completion_receipt_ref="PCR-REPORTING-001",
            manifest_ref="PM-REPORTING-001",
            manifest_sha512="e" * 128,
            gate_receipt_refs=["GATE-RECONCILIATION-001"],
            audit_result="PASS",
        )
    elif event_class == "HUMAN_GATE_REQUESTED":
        value.update(
            from_state="REVIEW_READY",
            to_state="HUMAN_GATE_REVIEW",
            trigger="explicit_promotion_request",
            reason="Submit the review-ready package to the active Human Gate.",
            completion_receipt_ref="PCR-REPORTING-001",
            manifest_ref="PM-REPORTING-001",
            manifest_sha512="e" * 128,
            gate_receipt_refs=["GATE-RECONCILIATION-001"],
            human_gate_request_ref="HGR-REPORTING-001",
            audit_result="PASS",
        )
    elif event_class == "HUMAN_GATE_DECISION":
        next_state = "RETURNED" if returned else "PROMOTED"
        value.update(
            from_state="HUMAN_GATE_REVIEW",
            to_state=next_state,
            trigger="explicit_human_decision",
            reason=f"Record the explicit human decision to enter {next_state}.",
            completion_receipt_ref="PCR-REPORTING-001",
            manifest_ref="PM-REPORTING-001",
            manifest_sha512="e" * 128,
            gate_receipt_refs=["GATE-RECONCILIATION-001"],
            human_gate_request_ref="HGR-REPORTING-001",
            human_gate_decision=valid_decision(next_state),
            audit_result="NOT_INVOKED",
        )
    elif event_class == "AUDIT_STOP":
        value.update(
            to_state="STOPPED",
            trigger="report_mutation_detected",
            reason="Audit interrupted production after detecting report mutation.",
            production_failure_class="REPORT_MUTATION",
            audit_result="FAIL",
            control_stop_class="AUDIT_INTERRUPT",
            control_transition_event_ref="TE-REPORTING-STOP-001",
            scar_required=True,
        )
    return value


class ProductionStateSchemaFixtures(unittest.TestCase):
    def assert_valid(self, value: dict) -> None:
        validate_schema(value, state_schema())

    def assert_invalid(self, value: dict) -> None:
        with self.assertRaises(SchemaValidationError):
            self.assert_valid(value)

    def test_all_nine_declared_states_validate_with_their_required_shape(self):
        for current_state in PRODUCTION_STATES:
            with self.subTest(current_state=current_state):
                self.assert_valid(valid_state(current_state))

    def test_state_and_failure_taxonomies_are_exact(self):
        schema = state_schema()
        self.assertEqual(schema["$defs"]["production_state"]["enum"], PRODUCTION_STATES)
        self.assertEqual(
            schema["$defs"]["production_failure_class"]["enum"],
            PRODUCTION_FAILURE_CLASSES,
        )

    def test_discovery_cannot_claim_frozen_or_projected_work(self):
        value = valid_state()
        value["freeze_ref"] = "AIF-REPORTING-001"
        value["freeze_sha512"] = "c" * 128
        self.assert_invalid(value)

    def test_analysis_complete_requires_a_bound_freeze_but_no_projection(self):
        value = valid_state("ANALYSIS_COMPLETE")
        value["freeze_ref"] = None
        value["freeze_sha512"] = None
        self.assert_invalid(value)

        value = valid_state("ANALYSIS_COMPLETE")
        value["projection_ref"] = "RP-REPORTING-001"
        value["projection_sha512"] = "d" * 128
        self.assert_invalid(value)

    def test_reporting_requires_the_exact_freeze_and_projection_bindings(self):
        for field in ("freeze_ref", "freeze_sha512", "projection_ref", "projection_sha512"):
            with self.subTest(field=field):
                value = valid_state("REPORTING")
                value[field] = None
                self.assert_invalid(value)

    def test_review_ready_requires_manifest_and_completion_receipt(self):
        for field in ("manifest_ref", "manifest_sha512", "completion_receipt_ref"):
            with self.subTest(field=field):
                value = valid_state("REVIEW_READY")
                value[field] = None
                self.assert_invalid(value)

    def test_human_gate_review_requires_request_but_rejects_premature_decision(self):
        value = valid_state("HUMAN_GATE_REVIEW")
        value["human_gate_request_ref"] = None
        self.assert_invalid(value)

        value = valid_state("HUMAN_GATE_REVIEW")
        value["human_gate_decision_ref"] = "HGD-RUNTIME-SYNTHESIZED"
        self.assert_invalid(value)

    def test_promoted_and_returned_are_terminal_and_decision_bound(self):
        for current_state in ("PROMOTED", "RETURNED"):
            with self.subTest(current_state=current_state):
                value = valid_state(current_state)
                value["human_gate_decision_ref"] = None
                self.assert_invalid(value)

                value = valid_state(current_state)
                value["terminal"] = False
                self.assert_invalid(value)

    def test_stopped_requires_failure_last_verified_state_and_scar(self):
        for field, replacement in (
            ("production_failure_class", None),
            ("last_verified_state", None),
            ("scar_required", False),
            ("terminal", False),
        ):
            with self.subTest(field=field):
                value = valid_state("STOPPED")
                value[field] = replacement
                self.assert_invalid(value)

    def test_nonterminal_state_cannot_claim_terminal_failure_or_scar(self):
        mutations = (
            ("terminal", True),
            ("scar_required", True),
            ("production_failure_class", "LOGIC_FREEZE"),
            ("last_verified_state", "REPORTING"),
        )
        for field, replacement in mutations:
            with self.subTest(field=field):
                value = valid_state("RECONCILIATION")
                value[field] = replacement
                self.assert_invalid(value)

    def test_authority_gate_and_external_action_invariants_are_closed(self):
        mutations = (
            ("authority_state", "ASSUMED"),
            ("human_gate_state", "BYPASSED"),
            ("external_action_state", "AUTHORIZED"),
        )
        for field, replacement in mutations:
            with self.subTest(field=field):
                value = valid_state("PROMOTED")
                value[field] = replacement
                self.assert_invalid(value)

    def test_state_rejects_unknown_fields_and_malformed_integrity(self):
        value = valid_state("REPORTING")
        value["assistant_completion_override"] = True
        self.assert_invalid(value)

        value = valid_state("REPORTING")
        value["canonical_git_binding"]["untracked"] = True
        self.assert_invalid(value)

        for field, replacement in (
            ("production_state_id", "STATE-001"),
            ("production_state_sha512", "short"),
            ("updated_at_utc", "not-a-time"),
        ):
            with self.subTest(field=field):
                value = valid_state("REPORTING")
                value[field] = replacement
                self.assert_invalid(value)


class ProductionEventSchemaFixtures(unittest.TestCase):
    def assert_valid(self, value: dict) -> None:
        validate_schema(value, event_schema())

    def assert_invalid(self, value: dict) -> None:
        with self.assertRaises(SchemaValidationError):
            self.assert_valid(value)

    def test_all_ten_declared_transition_forms_validate(self):
        fixtures = [
            valid_event("ANALYTICAL_FREEZE_ACCEPTED"),
            valid_event("PROJECTION_ACCEPTED"),
            valid_event("ARTIFACT_PRODUCED"),
            valid_event("RECONCILIATION_STARTED"),
            valid_event("BOUNDED_RECONCILIATION_RETURN"),
            valid_event("REVIEW_READY_DECLARED"),
            valid_event("HUMAN_GATE_REQUESTED"),
            valid_event("HUMAN_GATE_DECISION"),
            valid_event("HUMAN_GATE_DECISION", returned=True),
            valid_event("AUDIT_STOP"),
        ]
        for value in fixtures:
            with self.subTest(
                event_class=value["event_class"],
                transition=f"{value['from_state']}->{value['to_state']}",
            ):
                self.assert_valid(value)

    def test_event_taxonomies_are_exact(self):
        schema = event_schema()
        self.assertEqual(schema["properties"]["event_class"]["enum"], EVENT_CLASSES)
        self.assertEqual(schema["$defs"]["production_state"]["enum"], PRODUCTION_STATES)
        self.assertEqual(
            schema["$defs"]["production_failure_class"]["enum"],
            PRODUCTION_FAILURE_CLASSES,
        )

    def test_fixture_28_undeclared_transitions_are_rejected(self):
        cases = (
            ("ANALYTICAL_FREEZE_ACCEPTED", "DISCOVERY", "REPORTING"),
            ("PROJECTION_ACCEPTED", "ANALYSIS_COMPLETE", "RECONCILIATION"),
            ("ARTIFACT_PRODUCED", "REPORTING", "REVIEW_READY"),
            ("RECONCILIATION_STARTED", "REPORTING", "REVIEW_READY"),
            ("REVIEW_READY_DECLARED", "RECONCILIATION", "PROMOTED"),
            ("HUMAN_GATE_REQUESTED", "REVIEW_READY", "PROMOTED"),
        )
        for event_class, from_state, to_state in cases:
            with self.subTest(event_class=event_class):
                value = valid_event(event_class)
                value["from_state"] = from_state
                value["to_state"] = to_state
                self.assert_invalid(value)

    def test_fixture_29_terminal_states_reject_reentry(self):
        for terminal_state in ("PROMOTED", "RETURNED", "STOPPED"):
            with self.subTest(terminal_state=terminal_state):
                value = valid_event("ARTIFACT_PRODUCED")
                value["from_state"] = terminal_state
                self.assert_invalid(value)

    def test_fixture_30_bounded_return_preserves_route_freeze_projection_and_meaning(self):
        immutable_flags = (
            "route_unchanged",
            "freeze_unchanged",
            "projection_valid",
        )
        for field in immutable_flags:
            with self.subTest(field=field):
                value = valid_event("BOUNDED_RECONCILIATION_RETURN")
                value["reconciliation_return"][field] = False
                self.assert_invalid(value)

        mutation_flags = (
            "claim_mutation_detected",
            "evidence_mutation_detected",
            "uncertainty_mutation_detected",
            "lineage_mutation_detected",
        )
        for field in mutation_flags:
            with self.subTest(field=field):
                value = valid_event("BOUNDED_RECONCILIATION_RETURN")
                value["reconciliation_return"][field] = True
                self.assert_invalid(value)

    def test_fixture_31_claim_or_integrity_defect_requires_audit_stop(self):
        value = valid_event("BOUNDED_RECONCILIATION_RETURN")
        value["production_failure_class"] = "REPORT_MUTATION"
        self.assert_invalid(value)

        value = valid_event("AUDIT_STOP")
        value["production_failure_class"] = "PACKAGE_INTEGRITY_FAILURE"
        self.assert_valid(value)

    def test_fixture_32_nonprogress_is_a_marker_not_an_allowed_resume(self):
        value = valid_event("BOUNDED_RECONCILIATION_RETURN")
        value["reconciliation_return"]["progress_state"] = "NON_PROGRESSING"
        value["reconciliation_return"]["return_ordinal"] = 2
        value["reconciliation_return"]["prior_return_event_refs"] = [
            "PE-RETURN-001"
        ]
        self.assert_valid(value)

        value["reconciliation_return"]["progress_state"] = "IGNORED"
        self.assert_invalid(value)

    def test_audit_stop_accepts_every_nonterminal_source_only(self):
        for from_state in PRODUCTION_STATES[:6]:
            with self.subTest(from_state=from_state):
                value = valid_event("AUDIT_STOP")
                value["from_state"] = from_state
                if from_state in {"DISCOVERY", "ANALYSIS_COMPLETE"}:
                    value["projection_ref"] = None
                    value["projection_sha512"] = None
                if from_state == "DISCOVERY":
                    value["freeze_ref"] = None
                    value["freeze_sha512"] = None
                self.assert_valid(value)

    def test_audit_stop_requires_failure_interrupt_witness_and_scar(self):
        mutations = (
            ("production_failure_class", None),
            ("audit_result", "PASS"),
            ("control_stop_class", None),
            ("control_transition_event_ref", None),
            ("scar_required", False),
        )
        for field, replacement in mutations:
            with self.subTest(field=field):
                value = valid_event("AUDIT_STOP")
                value[field] = replacement
                self.assert_invalid(value)

    def test_human_decision_is_human_owned_state_exact_and_nonexternal(self):
        mutations = (
            ("decision_owner", "RUNTIME"),
            ("authorized_next_state", "RETURNED"),
            ("external_movement_included", True),
            ("authorized_target_or_audience", "external-recipient"),
        )
        for field, replacement in mutations:
            with self.subTest(field=field):
                value = valid_event("HUMAN_GATE_DECISION")
                value["human_gate_decision"][field] = replacement
                self.assert_invalid(value)

    def test_human_gate_decision_cannot_be_synthesized_on_other_transitions(self):
        value = valid_event("HUMAN_GATE_REQUESTED")
        value["human_gate_decision"] = valid_decision()
        self.assert_invalid(value)

        value = valid_event("ARTIFACT_PRODUCED")
        value["human_gate_request_ref"] = "HGR-PREMATURE-001"
        self.assert_invalid(value)

        value = valid_event("ARTIFACT_PRODUCED")
        value["control_stop_class"] = "AUDIT_INTERRUPT"
        self.assert_invalid(value)

        value = valid_event("HUMAN_GATE_DECISION")
        value["human_gate_decision"] = None
        self.assert_invalid(value)

    def test_first_event_has_no_predecessor_and_later_events_require_one(self):
        value = valid_event("ANALYTICAL_FREEZE_ACCEPTED")
        value["previous_event_sha512"] = "f" * 128
        self.assert_invalid(value)

        value = valid_event("ARTIFACT_PRODUCED")
        value["previous_event_sha512"] = None
        self.assert_invalid(value)

    def test_stage_gates_require_their_declared_evidence(self):
        cases = (
            ("ANALYTICAL_FREEZE_ACCEPTED", "freeze_ref"),
            ("ANALYTICAL_FREEZE_ACCEPTED", "freeze_sha512"),
            ("PROJECTION_ACCEPTED", "projection_ref"),
            ("PROJECTION_ACCEPTED", "projection_sha512"),
            ("RECONCILIATION_STARTED", "completion_declaration_ref"),
            ("REVIEW_READY_DECLARED", "manifest_ref"),
            ("REVIEW_READY_DECLARED", "manifest_sha512"),
            ("REVIEW_READY_DECLARED", "completion_receipt_ref"),
            ("HUMAN_GATE_REQUESTED", "human_gate_request_ref"),
        )
        for event_class, field in cases:
            with self.subTest(event_class=event_class, field=field):
                value = valid_event(event_class)
                value[field] = None
                self.assert_invalid(value)

    def test_authority_gate_and_external_action_invariants_are_closed(self):
        mutations = (
            ("authority_state", "ASSUMED"),
            ("human_gate_state", "BYPASSED"),
            ("external_action_state", "AUTHORIZED"),
        )
        for field, replacement in mutations:
            with self.subTest(field=field):
                value = valid_event("HUMAN_GATE_DECISION")
                value[field] = replacement
                self.assert_invalid(value)

    def test_event_rejects_unknown_fields_malformed_integrity_and_duplicate_refs(self):
        value = valid_event()
        value["publication_completed"] = True
        self.assert_invalid(value)

        for field, replacement in (
            ("production_event_id", "EVENT-001"),
            ("event_sha512", "short"),
            ("timestamp_utc", "unknown"),
        ):
            with self.subTest(field=field):
                value = valid_event()
                value[field] = replacement
                self.assert_invalid(value)

        value = valid_event()
        value["artifact_refs"] = ["ARTIFACT-001", "ARTIFACT-001"]
        self.assert_invalid(value)


if __name__ == "__main__":
    unittest.main()
