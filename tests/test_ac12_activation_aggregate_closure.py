from __future__ import annotations

import unittest

from tools.validate_activation_aggregate_closure import (
    REQUIRED_CONTROLS,
    evaluate_record,
    make_control_result,
    make_record,
    validate_contract_and_schema,
    validate_record,
)


class ActivationAggregateClosureTests(
    unittest.TestCase
):

    def assert_valid_record(
        self,
        record,
    ):
        self.assertEqual(
            validate_record(record),
            [],
        )

    def assert_blocked(
        self,
        record,
        reason,
    ):
        self.assert_valid_record(
            record
        )

        self.assertEqual(
            record[
                "closure_disposition"
            ],
            "BLOCKED",
        )

        self.assertIn(
            reason,
            record[
                "failure_reasons"
            ],
        )

    def test_contract_and_schema(self):
        self.assertEqual(
            validate_contract_and_schema(),
            [],
        )

    def test_required_controls_exact(self):
        self.assertEqual(
            REQUIRED_CONTROLS,
            (
                "AC-01",
                "AC-02",
                "AC-03",
                "AC-04",
                "AC-05",
                "AC-06",
                "AC-07",
                "AC-08",
                "AC-09",
                "AC-10",
                "AC-11",
            ),
        )

    def test_complete_aggregate_closes(self):
        record = make_record()

        self.assert_valid_record(
            record
        )

        self.assertEqual(
            record[
                "closure_disposition"
            ],
            "CLOSED",
        )

        self.assertEqual(
            record[
                "passed_control_count"
            ],
            11,
        )

        self.assertEqual(
            record[
                "failed_control_count"
            ],
            0,
        )

        self.assertEqual(
            record[
                "blocked_control_count"
            ],
            0,
        )

        self.assertEqual(
            record[
                "failure_reasons"
            ],
            [],
        )

    def test_missing_control_blocks(self):
        results = [
            make_control_result(
                control
            )
            for control
            in REQUIRED_CONTROLS
            if control != "AC-09"
        ]

        self.assert_blocked(
            make_record(
                control_results=results
            ),
            "REQUIRED_CONTROL_MISSING",
        )

    def test_failed_control_blocks(self):
        results = [
            make_control_result(
                control
            )
            for control
            in REQUIRED_CONTROLS
        ]

        results[2][
            "validation_state"
        ] = "FAIL"

        self.assert_blocked(
            make_record(
                control_results=results
            ),
            "REQUIRED_CONTROL_FAILED",
        )

    def test_blocked_control_blocks(self):
        results = [
            make_control_result(
                control
            )
            for control
            in REQUIRED_CONTROLS
        ]

        results[4][
            "validation_state"
        ] = "BLOCKED"

        self.assert_blocked(
            make_record(
                control_results=results
            ),
            "REQUIRED_CONTROL_BLOCKED",
        )

    def test_unknown_control_state_blocks(self):
        results = [
            make_control_result(
                control
            )
            for control
            in REQUIRED_CONTROLS
        ]

        results[6][
            "validation_state"
        ] = "UNKNOWN"

        self.assert_blocked(
            make_record(
                control_results=results
            ),
            "CONTROL_RESULT_UNKNOWN",
        )

    def test_duplicate_control_blocks(self):
        results = [
            make_control_result(
                control
            )
            for control
            in REQUIRED_CONTROLS
        ]

        results.append(
            make_control_result(
                "AC-11"
            )
        )

        self.assert_blocked(
            make_record(
                control_results=results
            ),
            "CROSS_CONTROL_SEMANTIC_CONFLICT",
        )

    def test_ac10_evidence_ceiling_required(self):
        self.assert_blocked(
            make_record(
                evidence_ceiling_state=
                    "MISSING"
            ),
            "EVIDENCE_CEILING_ENFORCEMENT_MISSING",
        )

    def test_ac11_human_gate_semantics_required(self):
        self.assert_blocked(
            make_record(
                human_gate_semantic_state=
                    "MISSING"
            ),
            "HUMAN_GATE_ENFORCEMENT_MISSING",
        )

    def test_cross_control_integrity_required(self):
        self.assert_blocked(
            make_record(
                cross_control_integrity_state=
                    "BLOCKED"
            ),
            "CROSS_CONTROL_SEMANTIC_CONFLICT",
        )

    def test_authority_remains_none(self):
        self.assert_blocked(
            make_record(
                authority_state="FULL"
            ),
            "AUTHORITY_PROMOTED",
        )

    def test_human_gate_remains_active(self):
        self.assert_blocked(
            make_record(
                human_gate_state=
                    "DISABLED"
            ),
            "HUMAN_GATE_DISABLED",
        )

    def test_execution_not_inferred(self):
        self.assert_blocked(
            make_record(
                execution_state=
                    "EXECUTED"
            ),
            "EXECUTION_INFERRED",
        )

    def test_publication_not_inferred(self):
        self.assert_blocked(
            make_record(
                publication_state=
                    "PUBLISHED"
            ),
            "PUBLICATION_INFERRED",
        )

    def test_canonical_mutation_not_inferred(self):
        self.assert_blocked(
            make_record(
                canonical_mutation_state=
                    "MUTATED"
            ),
            "CANONICAL_MUTATION_INFERRED",
        )

    def test_system_population_disallowed(self):
        self.assert_blocked(
            make_record(
                system_population_state=
                    "ALLOWED"
            ),
            "SYSTEM_POPULATION_INFERRED",
        )

    def test_provenance_required(self):
        self.assert_blocked(
            make_record(
                provenance_route=[]
            ),
            "PROVENANCE_MISSING",
        )

    def test_control_provenance_required(self):
        results = [
            make_control_result(
                control
            )
            for control
            in REQUIRED_CONTROLS
        ]

        results[0][
            "provenance_reference"
        ] = ""

        self.assert_blocked(
            make_record(
                control_results=results
            ),
            "PROVENANCE_MISSING",
        )

    def test_failure_reasons_accumulate(self):
        record = make_record(
            evidence_ceiling_state=
                "MISSING",
            human_gate_semantic_state=
                "MISSING",
            authority_state=
                "FULL",
            human_gate_state=
                "DISABLED",
            execution_state=
                "EXECUTED",
            provenance_route=[],
        )

        expected = {
            "EVIDENCE_CEILING_ENFORCEMENT_MISSING",
            "HUMAN_GATE_ENFORCEMENT_MISSING",
            "AUTHORITY_PROMOTED",
            "HUMAN_GATE_DISABLED",
            "EXECUTION_INFERRED",
            "PROVENANCE_MISSING",
        }

        self.assertTrue(
            expected.issubset(
                set(
                    evaluate_record(
                        record
                    )
                )
            )
        )

        self.assert_valid_record(
            record
        )

        self.assertEqual(
            record[
                "closure_disposition"
            ],
            "BLOCKED",
        )

    def test_validation_does_not_create_authority(self):
        record = make_record()

        self.assert_valid_record(
            record
        )

        self.assertEqual(
            record[
                "authority_state"
            ],
            "NONE",
        )

        self.assertEqual(
            record[
                "human_gate_state"
            ],
            "ACTIVE",
        )

        self.assertEqual(
            record[
                "execution_state"
            ],
            "NOT_INFERRED",
        )


if __name__ == "__main__":
    unittest.main()
