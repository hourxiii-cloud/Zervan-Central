import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_formation_rejustification.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_formation_rejustification",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class FormationRejustificationTests(
    unittest.TestCase
):

    def valid(
        self,
        previous,
        new,
        trigger,
    ):
        return module.make_record(
            previous_formation_type=previous,
            new_formation_type=new,
            trigger=trigger,
        )

    def test_single_to_stack(self):
        record = self.valid(
            "SINGLE_ROUTE",
            "STACK_ANALYSIS",
            "CONTRADICTION_APPEARED_OR_PERSISTED",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_stack_to_expanded(self):
        record = self.valid(
            "STACK_ANALYSIS",
            "EXPANDED_ANALYSIS",
            "TERRAIN_CONTACT_CHANGED",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_expanded_to_swarm(self):
        record = self.valid(
            "EXPANDED_ANALYSIS",
            "SWARM",
            "SIGNAL_ECOLOGY_CHANGED",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_deescalation_to_single(self):
        record = self.valid(
            "STACK_ANALYSIS",
            "SINGLE_ROUTE",
            "ONE_ROUTE_BECAME_SUFFICIENT",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_missing_trigger_blocked(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger=None,
        )

        self.assertIn(
            "REJUSTIFICATION_TRIGGER_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_missing_basis_blocked(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            basis=[],
        )

        self.assertIn(
            "REJUSTIFICATION_BASIS_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_prior_history_must_survive(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            prior_history_preserved=False,
        )

        self.assertIn(
            "PRIOR_HISTORY_ERASED",
            record[
                "failure_reasons"
            ]
        )

    def test_broken_stick_blocked(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            stick_continuity_state="BROKEN",
        )

        self.assertIn(
            "STICK_NOT_PRESERVED",
            record[
                "failure_reasons"
            ]
        )

    def test_missing_origin_blocked(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            origin_reference=None,
        )

        self.assertIn(
            "ORIGIN_CONTINUITY_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_missing_ingress_blocked(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            ingress_reference=None,
        )

        self.assertIn(
            "INGRESS_CONTINUITY_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_missing_cartography_blocked(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            cartography_reference=None,
        )

        self.assertIn(
            "CARTOGRAPHY_CONTINUITY_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_missing_evidence_lineage_blocked(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            evidence_lineage_references=[],
        )

        self.assertIn(
            "EVIDENCE_LINEAGE_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_missing_provenance_blocked(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            provenance_route=[],
        )

        self.assertIn(
            "PROVENANCE_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_missing_return_coordinates_blocked(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            return_coordinates=None,
        )

        self.assertIn(
            "RETURN_COORDINATES_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_silent_force_change_blocked(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger="CONTRADICTION_APPEARED_OR_PERSISTED",
            force_scale_changed=True,
            force_change_reference=None,
        )

        self.assertIn(
            "SILENT_FORCE_INFLATION",
            record[
                "failure_reasons"
            ]
        )

    def test_attributed_force_change_allowed(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger="CONTRADICTION_APPEARED_OR_PERSISTED",
            force_scale_changed=True,
            force_change_reference="force-selection:new",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_unattributed_ceiling_change_blocked(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="EVIDENCE_CEILING_CHANGED",
            previous_ceiling="ceiling:a",
            new_ceiling="ceiling:b",
            ceiling_change_reference=None,
        )

        self.assertIn(
            "EVIDENCE_CEILING_CHANGED_UNATTRIBUTED",
            record[
                "failure_reasons"
            ]
        )

    def test_attributed_ceiling_change_allowed(self):
        record = module.make_record(
            previous_formation_type="STACK_ANALYSIS",
            new_formation_type="EXPANDED_ANALYSIS",
            trigger="EVIDENCE_CEILING_CHANGED",
            previous_ceiling="ceiling:a",
            new_ceiling="ceiling:b",
            ceiling_change_reference="ceiling-change:a",
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_new_room_invention_blocked(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            new_room_created=True,
        )

        self.assertIn(
            "NEW_ROOM_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_branch_invention_blocked(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            branch_created=True,
        )

        self.assertIn(
            "BRANCH_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_passageway_invention_blocked(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            passageway_created=True,
        )

        self.assertIn(
            "PASSAGEWAY_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_occupancy_mutation_blocked(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            occupancy_mutated=True,
        )

        self.assertIn(
            "OCCUPANCY_MUTATED",
            record[
                "failure_reasons"
            ]
        )

    def test_lifecycle_mutation_blocked(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            lifecycle_mutated=True,
        )

        self.assertIn(
            "LIFECYCLE_MUTATED",
            record[
                "failure_reasons"
            ]
        )

    def test_authority_promotion_blocked(self):
        record = module.make_record(
            previous_formation_type="SINGLE_ROUTE",
            new_formation_type="STACK_ANALYSIS",
            trigger="TERRAIN_CONTACT_CHANGED",
            authority_state="WRITE",
        )

        self.assertIn(
            "AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_new_formation_record_required(self):
        record = self.valid(
            "SINGLE_ROUTE",
            "STACK_ANALYSIS",
            "TERRAIN_CONTACT_CHANGED",
        )

        record[
            "new_formation_id"
        ] = record[
            "previous_formation_id"
        ]

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "new attributable formation record"
                in error
                for error in errors
            )
        )

    def test_human_gate_remains_active(self):
        record = self.valid(
            "SINGLE_ROUTE",
            "STACK_ANALYSIS",
            "TERRAIN_CONTACT_CHANGED",
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


if __name__ == "__main__":
    unittest.main()
