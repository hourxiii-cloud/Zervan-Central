import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_proportional_force_routing.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_proportional_force_routing",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class ProportionalForceRoutingTests(
    unittest.TestCase
):

    def test_faint_localized_single_goblin(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_split_signal_goblin_signal(self):
        record = module.make_record(
            signal_profile="SPLIT_PLAUSIBLE_SOURCES",
            territory_complexity="MEDIUM",
            selected_scale="SIGNAL_OR_INTEL",
            selected_capability_class="GOBLIN_SIGNAL",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_split_signal_intel_squad(self):
        record = module.make_record(
            signal_profile="SPLIT_PLAUSIBLE_SOURCES",
            territory_complexity="MEDIUM",
            selected_scale="SIGNAL_OR_INTEL",
            selected_capability_class="INTEL_SQUAD",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_distributed_scar_platoon(self):
        record = module.make_record(
            signal_profile="DISTRIBUTED_RECURSIVE_SCAR",
            territory_complexity="LARGE_DISTRIBUTED",
            selected_scale="PLATOON",
            selected_capability_class="GOBLIN_PLATOON",
            selected_capability_count=4,
            selection_basis=[
                "profile:distributed_recursive_scar",
                "territory:large_distributed",
                "question:preserved",
                "evidence:bounded",
                "larger-force-required:parallel independent routes",
            ],
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_faint_platoon_without_reason_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="PLATOON",
            selected_capability_class="GOBLIN_PLATOON",
        )

        self.assertIn(
            "OVERSIZED_FORCE_WITHOUT_JUSTIFICATION",
            record[
                "failure_reasons"
            ]
        )

    def test_faint_team_without_reason_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="TEAM",
            selected_capability_class="GOBLIN_TEAM",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "REJECTED"
        )

    def test_split_platoon_without_reason_rejected(self):
        record = module.make_record(
            signal_profile="SPLIT_PLAUSIBLE_SOURCES",
            territory_complexity="MEDIUM",
            selected_scale="PLATOON",
            selected_capability_class="GOBLIN_PLATOON",
        )

        self.assertIn(
            "OVERSIZED_FORCE_WITHOUT_JUSTIFICATION",
            record[
                "failure_reasons"
            ]
        )

    def test_escalation_by_capability_availability_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="TEAM",
            selected_capability_class="GOBLIN_TEAM",
            selection_basis=[
                "profile:faint_localized",
                "territory:small",
                "question:preserved",
                "evidence:bounded",
                "escalation:capability-available",
            ],
        )

        self.assertIn(
            "ESCALATION_WITHOUT_EVIDENCE",
            record[
                "failure_reasons"
            ]
        )

    def test_deescalation_with_evidence_allowed(self):
        record = module.make_record(
            signal_profile="DISTRIBUTED_RECURSIVE_SCAR",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
            selection_basis=[
                "profile:distributed_recursive_scar",
                "territory:small",
                "question:preserved",
                "evidence:bounded",
                "deescalation-supported:signal localized",
            ],
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_class_scale_mismatch_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN_PLATOON",
        )

        self.assertIn(
            "FORCE_FORMATION_COLLAPSE",
            record[
                "failure_reasons"
            ]
        )

    def test_formation_reference_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
            formation_reference="SWARM",
        )

        self.assertIn(
            "FORCE_FORMATION_COLLAPSE",
            record[
                "failure_reasons"
            ]
        )

    def test_occupancy_invention_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
            occupancy_created=True,
        )

        self.assertIn(
            "OCCUPANCY_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_active_state_invention_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
            active_lifecycle_created=True,
        )

        self.assertIn(
            "ACTIVE_STATE_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_execution_authority_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
            execution_authorized=True,
        )

        self.assertIn(
            "EXECUTION_AUTHORITY_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_authority_promotion_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
            authority_state="WRITE",
        )

        self.assertIn(
            "AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_question_rewrite_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
            selection_basis=[
                "profile:faint_localized",
                "territory:small",
                "question:rewritten-for-force",
                "evidence:bounded",
            ],
        )

        self.assertIn(
            "QUESTION_REWRITTEN_FOR_FORCE",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_boundary_exceed_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
            selection_basis=[
                "profile:faint_localized",
                "territory:small",
                "question:preserved",
                "evidence-boundary:exceeded",
            ],
        )

        self.assertIn(
            "EVIDENCE_BOUNDARY_EXCEEDED",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_ceiling_promotion_rejected(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
            selection_basis=[
                "profile:faint_localized",
                "territory:small",
                "question:preserved",
                "evidence-ceiling:promoted",
            ],
        )

        self.assertIn(
            "EVIDENCE_CEILING_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_reselection_does_not_create_new_room(self):
        first = module.make_record(
            signal_profile="SPLIT_PLAUSIBLE_SOURCES",
            territory_complexity="MEDIUM",
            selected_scale="SIGNAL_OR_INTEL",
            selected_capability_class="GOBLIN_SIGNAL",
        )

        second = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
        )

        self.assertEqual(
            first[
                "object_id"
            ],
            second[
                "object_id"
            ]
        )

    def test_human_gate_remains_active(self):
        record = module.make_record(
            signal_profile="FAINT_LOCALIZED",
            territory_complexity="SMALL",
            selected_scale="SINGLE",
            selected_capability_class="GOBLIN",
        )

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

    def test_schema_does_not_absorb_formation_or_authority(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "formation_type",
            "occupancy_witness",
            "active_transition",
            "hydration_release",
            "execution_result",
            "publication_authorization",
            "canonical_promotion",
            "claim_ceiling_override",
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
