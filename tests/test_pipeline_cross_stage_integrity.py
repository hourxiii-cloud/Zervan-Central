import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_pipeline_cross_stage_integrity.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_pipeline_cross_stage_integrity",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class PipelineCrossStageIntegrityTests(
    unittest.TestCase
):

    def test_valid_cross_stage_receipt(self):
        record = module.make_valid_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_native_route_exact(self):
        record = module.make_valid_record()

        record[
            "pipeline_route"
        ] = list(
            module.PIPELINE_ROUTE
        )

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            record
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_ccr_bypass_rejected(self):
        record = module.make_valid_record()

        record[
            "pipeline_route"
        ] = [
            "ROOM_BOUND_EVIDENCE",
            "PMC_INTAKE",
            "PMC",
            "MC",
            "RAVEN",
            "HUMAN_GATE",
        ]

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "pipeline route is invalid"
                in error
                for error in errors
            )
        )

    def test_mc_bypass_rejected(self):
        record = module.make_valid_record()

        record[
            "pipeline_route"
        ] = [
            "ROOM_BOUND_EVIDENCE",
            "PMC_INTAKE",
            "PMC",
            "CCR",
            "RAVEN",
            "HUMAN_GATE",
        ]

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "pipeline route is invalid"
                in error
                for error in errors
            )
        )

    def test_ownership_checks_complete(self):
        record = module.make_valid_record()

        record[
            "ownership_checks"
        ].remove(
            "REGISTRY_NOT_ABSORBED"
        )

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "missing ownership checks"
                in error
                for error in errors
            )
        )

    def test_authority_checks_complete(self):
        record = module.make_valid_record()

        record[
            "authority_checks"
        ].remove(
            "RAVEN_NO_ACTION_AUTHORITY"
        )

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "missing authority checks"
                in error
                for error in errors
            )
        )

    def test_human_gate_approval_not_execution_check_required(self):
        record = module.make_valid_record()

        record[
            "authority_checks"
        ].remove(
            "HUMAN_GATE_APPROVAL_NOT_EXECUTION"
        )

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "missing authority checks"
                in error
                for error in errors
            )
        )

    def test_ccr_collision_must_remain_visible(self):
        record = module.make_valid_record()

        record[
            "collision_states"
        ].remove(
            "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION"
        )

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "collision state was silently removed"
                in error
                for error in errors
            )
        )

    def test_mc_ephemerality_collision_must_remain_visible(self):
        record = module.make_valid_record()

        record[
            "collision_states"
        ].remove(
            "MC_EPHEMERALITY_LINEAGE_COLLISION"
        )

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "collision state was silently removed"
                in error
                for error in errors
            )
        )

    def test_blocked_requires_reason(self):
        record = module.make_valid_record()

        record[
            "integrity_disposition"
        ] = "BLOCKED"

        record[
            "blocking_reasons"
        ] = []

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "requires blocking reasons"
                in error
                for error in errors
            )
        )

    def test_authority_remains_none(self):
        record = module.make_valid_record()

        record[
            "authority_state"
        ] = "AUTONOMOUS"

        record[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
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

    def test_material_change_changes_integrity_identity(self):
        first = module.make_valid_record()
        second = module.make_valid_record()

        second[
            "report_references"
        ] = [
            "report:different"
        ]

        second[
            "cross_stage_integrity_id"
        ] = module.compute_cross_stage_integrity_id(
            second
        )

        self.assertNotEqual(
            first[
                "cross_stage_integrity_id"
            ],
            second[
                "cross_stage_integrity_id"
            ]
        )

    def test_contract_surface_cross_stage_locks(self):
        self.assertEqual(
            module.validate_contract_surface(),
            []
        )

    def test_schema_surface_no_absorption(self):
        self.assertEqual(
            module.validate_schema_surface(),
            []
        )

    def test_schema_does_not_absorb_execution_or_stage_ownership(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "pmc_selected_world_override",
            "ccr_generation",
            "mc_disposition_override",
            "raven_rendering_override",
            "human_gate_approval_override",
            "execution_authorization",
            "publication_execution",
            "canonical_promotion",
            "room_lifecycle_transition",
            "cartography_mutation",
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
