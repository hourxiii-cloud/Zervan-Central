import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_premature_analysis_rejection.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_premature_analysis_rejection",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class PrematureAnalysisRejectionTests(
    unittest.TestCase
):

    def test_ready_positive_control(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "gate_result"
            ],
            "ALLOWED"
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_request_draft_rejected(self):
        record = module.make_record(
            request_state="DRAFT"
        )

        self.assertEqual(
            record[
                "gate_result"
            ],
            "REJECTED"
        )

        self.assertIn(
            "REQUEST_NOT_READY",
            record[
                "rejection_reasons"
            ]
        )

    def test_request_ready_does_not_equal_room_ready(self):
        record = module.make_record(
            request_state="READY",
            room_lifecycle_state="QUALIFYING"
        )

        self.assertEqual(
            record[
                "gate_result"
            ],
            "REJECTED"
        )

        self.assertIn(
            "ROOM_NOT_READY",
            record[
                "rejection_reasons"
            ]
        )

    def test_provisional_rejected_with_capability_available(self):
        record = module.make_record(
            qualification_disposition="PROVISIONAL",
            room_lifecycle_state="PROVISIONAL",
            analytical_capability_available=True
        )

        self.assertEqual(
            record[
                "gate_result"
            ],
            "REJECTED"
        )

    def test_rejected_disposition_rejected(self):
        record = module.make_record(
            qualification_disposition="REJECTED",
            room_lifecycle_state="REJECTED"
        )

        self.assertIn(
            "ROOM_NOT_QUALIFIED",
            record[
                "rejection_reasons"
            ]
        )

    def test_degraded_disposition_rejected(self):
        record = module.make_record(
            qualification_disposition="DEGRADED",
            room_lifecycle_state="DEGRADED"
        )

        self.assertEqual(
            record[
                "gate_result"
            ],
            "REJECTED"
        )

    def test_qualified_without_ready_rejected(self):
        record = module.make_record(
            qualification_disposition="QUALIFIED",
            room_lifecycle_state="QUALIFIED"
        )

        self.assertEqual(
            record[
                "gate_result"
            ],
            "REJECTED"
        )

        self.assertIn(
            "ROOM_NOT_READY",
            record[
                "rejection_reasons"
            ]
        )

    def test_readiness_blocker_rejected(self):
        record = module.make_record(
            readiness_blockers=[
                "provenance unresolved"
            ]
        )

        self.assertIn(
            "READINESS_BLOCKER_PRESENT",
            record[
                "rejection_reasons"
            ]
        )

    def test_released_hydration_does_not_substitute_for_ready(self):
        record = module.make_record(
            room_lifecycle_state="QUALIFIED",
            hydration_state="RELEASED"
        )

        self.assertEqual(
            record[
                "gate_result"
            ],
            "REJECTED"
        )

        self.assertIn(
            "ROOM_NOT_READY",
            record[
                "rejection_reasons"
            ]
        )

    def test_missing_boundary_rejected(self):
        record = module.make_record(
            evidence_boundary_reference=None
        )

        self.assertIn(
            "EVIDENCE_BOUNDARY_UNRESOLVED",
            record[
                "rejection_reasons"
            ]
        )

    def test_missing_ceiling_rejected(self):
        record = module.make_record(
            evidence_ceiling_reference=None
        )

        self.assertIn(
            "EVIDENCE_CEILING_UNRESOLVED",
            record[
                "rejection_reasons"
            ]
        )

    def test_capability_unavailable_rejected(self):
        record = module.make_record(
            analytical_capability_available=False
        )

        self.assertIn(
            "CAPABILITY_UNAVAILABLE",
            record[
                "rejection_reasons"
            ]
        )

    def test_analysis_not_requested_rejected(self):
        record = module.make_record(
            analytical_admission_requested=False
        )

        self.assertIn(
            "ANALYSIS_NOT_REQUESTED",
            record[
                "rejection_reasons"
            ]
        )

    def test_rejection_reasons_must_be_complete(self):
        record = module.make_record(
            room_lifecycle_state="QUALIFIED"
        )

        record[
            "rejection_reasons"
        ] = []

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "rejection reasons are incomplete"
                in error
                for error in errors
            )
        )

    def test_false_allowed_result_rejected(self):
        record = module.make_record(
            room_lifecycle_state="QUALIFIED"
        )

        record[
            "gate_result"
        ] = "ALLOWED"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "gate result contradicts"
                in error
                for error in errors
            )
        )

    def test_gate_never_establishes_occupation(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "analytical_occupancy_state"
            ],
            "NOT_ENTERED"
        )

    def test_authority_remains_none(self):
        record = module.make_record()

        record[
            "authority_state"
        ] = "WRITE"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "authority state must remain NONE"
                in error
                for error in errors
            )
        )

    def test_human_gate_remains_active(self):
        record = module.make_record()

        record[
            "human_gate_state"
        ] = "DISABLED"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "Human Gate state must remain ACTIVE"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_absorb_downstream_pipeline(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "pmc_output",
            "ccr_id",
            "mc_evaluation",
            "raven_report",
            "active_transition",
            "occupancy_witness",
            "execution_authorization",
            "canonical_promotion",
            "evidence_boundary_override",
            "evidence_ceiling_override",
        }

        self.assertFalse(
            set(
                schema[
                    "properties"
                ]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
