import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_ring5_aggregate_closure.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_ring5_aggregate_closure",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class Ring5AggregateClosureTests(
    unittest.TestCase
):

    def test_valid_closure_receipt(self):
        record = module.make_valid_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_all_subrings_required_in_order(self):
        record = module.make_valid_record()

        record[
            "completed_subrings"
        ] = record[
            "completed_subrings"
        ][:-1]

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "subring order is incomplete or changed"
                in error
                for error in errors
            )
        )

    def test_dependencies_required(self):
        record = module.make_valid_record()

        record[
            "dependency_rings"
        ] = [
            "R1",
            "R2",
            "R3",
        ]

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "dependency ring set is incomplete or changed"
                in error
                for error in errors
            )
        )

    def test_native_route_requires_ccr(self):
        record = module.make_valid_record()

        record[
            "pipeline_route"
        ].remove(
            "CCR"
        )

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "pipeline route is incomplete or changed"
                in error
                for error in errors
            )
        )

    def test_collisions_required(self):
        record = module.make_valid_record()

        record[
            "collision_states"
        ] = []

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "collision set is incomplete or changed"
                in error
                for error in errors
            )
        )

    def test_ownership_separation_preserved(self):
        record = module.make_valid_record()

        record[
            "ownership_separation_state"
        ] = "ABSORBED"

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "ownership separation must remain PRESERVED"
                in error
                for error in errors
            )
        )

    def test_authority_separation_preserved(self):
        record = module.make_valid_record()

        record[
            "authority_separation_state"
        ] = "ABSORBED"

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "authority separation must remain PRESERVED"
                in error
                for error in errors
            )
        )

    def test_no_compression_out_preserved(self):
        record = module.make_valid_record()

        record[
            "no_compression_out_state"
        ] = "DISABLED"

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "No Compression Out state must remain PRESERVED"
                in error
                for error in errors
            )
        )

    def test_candidate_promotion_state_required(self):
        record = module.make_valid_record()

        record[
            "promotion_state"
        ] = "CANONICAL"

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "promotion_state must remain CANDIDATE"
                in error
                for error in errors
            )
        )

    def test_authority_remains_none(self):
        record = module.make_valid_record()

        record[
            "authority_state"
        ] = "WRITE"

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "authority_state must remain NONE"
                in error
                for error in errors
            )
        )

    def test_human_gate_remains_active(self):
        record = module.make_valid_record()

        record[
            "human_gate_state"
        ] = "DISABLED"

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

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

    def test_blocked_requires_reason(self):
        record = module.make_valid_record()

        record[
            "closure_disposition"
        ] = "BLOCKED"

        record[
            "blocking_reasons"
        ] = []

        record[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "BLOCKED Ring 5 closure requires blocking reasons"
                in error
                for error in errors
            )
        )

    def test_material_change_changes_closure_identity(self):
        first = module.make_valid_record()
        second = module.make_valid_record()

        second[
            "lineage_reference"
        ] = "ring5:lineage:different"

        second[
            "ring5_closure_id"
        ] = module.compute_ring5_closure_id(
            second
        )

        self.assertNotEqual(
            first[
                "ring5_closure_id"
            ],
            second[
                "ring5_closure_id"
            ]
        )

    def test_subring_surface_is_closed(self):
        self.assertEqual(
            module.validate_subring_surface(),
            []
        )

    def test_runner_surface_is_complete(self):
        self.assertEqual(
            module.validate_runner_surface(),
            []
        )

    def test_schema_does_not_create_new_primitive_or_authority(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "new_pipeline_stage",
            "new_analytical_primitive",
            "execution_authorization",
            "publication_execution",
            "canonical_promotion",
            "room_lifecycle_transition",
            "cartography_mutation",
            "evidence_boundary_override",
            "evidence_ceiling_override",
            "autonomous_authority",
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
