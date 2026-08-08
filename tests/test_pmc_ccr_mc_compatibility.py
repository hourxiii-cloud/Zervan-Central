import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_pmc_ccr_mc_compatibility.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_pmc_ccr_mc_compatibility",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class PmcCcrMcCompatibilityTests(
    unittest.TestCase
):

    def test_native_route_valid(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_native_route_exact(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "pipeline_route"
            ],
            module.NATIVE_ROUTE
        )

    def test_direct_pmc_mc_route_blocked(self):
        record = module.make_record(
            pipeline_route=[
                "EVIDENCE",
                "PMC",
                "MC",
                "RAVEN",
                "HUMAN_GATE",
            ],
        )

        self.assertIn(
            "CCR_BYPASSED",
            record[
                "failure_reasons"
            ]
        )

    def test_raw_pmc_mc_input_blocked(self):
        record = module.make_record(
            mc_input_kind="RAW_PMC"
        )

        self.assertIn(
            "MC_RAW_PMC_INPUT_USED",
            record[
                "failure_reasons"
            ]
        )

    def test_ccr_reference_required(self):
        record = module.make_record(
            ccr_reference=None
        )

        self.assertIn(
            "CCR_REFERENCE_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_room_identity_preserved(self):
        record = module.make_record()

        self.assertEqual(
            len(
                {
                    record[
                        "room_object_id"
                    ],
                    record[
                        "pmc_room_object_id"
                    ],
                    record[
                        "ccr_room_object_id"
                    ],
                    record[
                        "mc_room_object_id"
                    ],
                }
            ),
            1
        )

    def test_room_identity_change_blocked(self):
        record = module.make_record(
            mc_room_object_id=(
                "sha512:"
                + "2" * 128
            )
        )

        self.assertIn(
            "ROOM_IDENTITY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_pmc_selection_preserved(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "pmc_selected_world_id"
            ],
            record[
                "ccr_selected_world_id"
            ]
        )

    def test_pmc_selection_rewrite_blocked(self):
        record = module.make_record(
            ccr_selected_world_id="world:b"
        )

        self.assertIn(
            "PMC_SELECTION_REINTERPRETED",
            record[
                "failure_reasons"
            ]
        )

    def test_null_pmc_result_preserved(self):
        record = module.make_record(
            pmc_selected_world_id=None,
            ccr_selected_world_id=None,
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_null_pmc_result_cannot_become_winner(self):
        record = module.make_record(
            pmc_selected_world_id=None,
            ccr_selected_world_id="world:a",
        )

        self.assertIn(
            "PMC_SELECTION_REINTERPRETED",
            record[
                "failure_reasons"
            ]
        )

    def test_candidate_order_preserved(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "pmc_candidate_ordering"
            ],
            record[
                "ccr_candidate_ordering"
            ]
        )

    def test_candidate_reorder_blocked(self):
        record = module.make_record(
            ccr_candidate_ordering=[
                "world:b",
                "world:a",
                "world:c",
            ]
        )

        self.assertIn(
            "PMC_CANDIDATE_ORDER_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_rejection_history_preserved(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "pmc_rejection_references"
            ],
            record[
                "ccr_rejection_references"
            ]
        )

    def test_rejection_history_loss_blocked(self):
        record = module.make_record(
            ccr_rejection_references=[]
        )

        self.assertIn(
            "PMC_REJECTION_HISTORY_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_uncertainty_preserved(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "pmc_uncertainty_references"
            ],
            record[
                "ccr_uncertainty_references"
            ]
        )

        self.assertEqual(
            record[
                "ccr_uncertainty_references"
            ],
            record[
                "mc_uncertainty_references"
            ]
        )

    def test_uncertainty_loss_at_ccr_blocked(self):
        record = module.make_record(
            ccr_uncertainty_references=[]
        )

        self.assertIn(
            "UNCERTAINTY_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_uncertainty_loss_at_mc_blocked(self):
        record = module.make_record(
            mc_uncertainty_references=[]
        )

        self.assertIn(
            "UNCERTAINTY_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_boundary_change_blocked(self):
        record = module.make_record(
            mc_evidence_boundary_reference="boundary:wider"
        )

        self.assertIn(
            "EVIDENCE_BOUNDARY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_ceiling_change_blocked(self):
        record = module.make_record(
            ccr_evidence_ceiling_reference="ceiling:higher"
        )

        self.assertIn(
            "EVIDENCE_CEILING_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_historical_interface_required(self):
        record = module.make_record(
            legacy_direct_interface_present=False
        )

        self.assertIn(
            "HISTORICAL_INTERFACE_ARTIFACT_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_historical_naming_lock_required(self):
        record = module.make_record(
            legacy_naming_lock_present=False
        )

        self.assertIn(
            "HISTORICAL_NAMING_LOCK_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_interface_collision_must_remain_visible(self):
        record = module.make_record(
            interface_collision_state=None
        )

        self.assertIn(
            "INTERFACE_COLLISION_NORMALIZED_AWAY",
            record[
                "failure_reasons"
            ]
        )

    def test_mc_ephemerality_collision_must_remain_visible(self):
        record = module.make_record(
            mc_ephemerality_collision_state=None
        )

        self.assertIn(
            "MC_EPHEMERALITY_COLLISION_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_room_semantic_absorption_blocked(self):
        record = module.make_record(
            room_semantics_absorbed=True
        )

        self.assertIn(
            "ROOM_SEMANTICS_ABSORBED",
            record[
                "failure_reasons"
            ]
        )

    def test_pmc_authority_promotion_blocked(self):
        record = module.make_record(
            pmc_authority_promoted=True
        )

        self.assertIn(
            "PMC_AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_ccr_authority_promotion_blocked(self):
        record = module.make_record(
            ccr_authority_promoted=True
        )

        self.assertIn(
            "CCR_AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_mc_authority_promotion_blocked(self):
        record = module.make_record(
            mc_authority_promoted=True
        )

        self.assertIn(
            "MC_AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_global_authority_promotion_blocked(self):
        record = module.make_record(
            authority_state="WRITE"
        )

        self.assertIn(
            "AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
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


if __name__ == "__main__":
    unittest.main()
