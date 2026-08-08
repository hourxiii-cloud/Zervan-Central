import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_ccr_mc_response_output_admissibility.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_ccr_mc_response_output_admissibility",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_record():
    record = {
        "schema_version":
            "1.0",
        "ccr_id":
            "sha512:" + "1" * 128,
        "object_id":
            "sha512:" + "2" * 128,
        "room_revision_id":
            "revision:test",
        "room_state_root":
            "sha512:" + "3" * 128,
        "authorized_view_root":
            "sha512:" + "4" * 128,
        "evidence_boundary_reference":
            "boundary:test",
        "evidence_ceiling_reference":
            "ceiling:test",
        "coordinate_reference":
            "coordinate:test",
        "representation_reference":
            "representation:test",
        "governance_constraint_references": [
            "governance:test"
        ],
        "propagated_uncertainty_references": [
            "uncertainty:test"
        ],
        "response_class_results": [
            {
                "response_class":
                    "observation",
                "disposition":
                    "ADMISSIBLE",
                "required_conditions": [],
                "inadmissibility_reasons": []
            },
            {
                "response_class":
                    "technical_mitigation",
                "disposition":
                    "CONDITIONAL",
                "required_conditions": [
                    "condition:test"
                ],
                "inadmissibility_reasons": []
            },
            {
                "response_class":
                    "executive_notification",
                "disposition":
                    "INADMISSIBLE",
                "required_conditions": [],
                "inadmissibility_reasons": [
                    "reason:test"
                ]
            }
        ],
        "lineage_reference":
            "lineage:test",
        "provenance_route": [
            "sha512:" + "2" * 128,
            "sha512:" + "1" * 128,
            "mc:test"
        ],
        "evaluation_disposition":
            "EVALUATED",
        "blocking_reasons": [],
        "ephemerality_collision_state":
            "MC_EPHEMERALITY_LINEAGE_COLLISION",
        "interface_collision_state":
            "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "mc_evaluation_id"
    ] = module.compute_mc_evaluation_id(
        record
    )

    return record


class CCRMCResponseOutputAdmissibilityTests(
    unittest.TestCase
):

    def test_valid_evaluation(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_ccr_required(self):
        record = make_record()

        record["ccr_id"] = ""

        record[
            "mc_evaluation_id"
        ] = module.compute_mc_evaluation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "ccr_id"
                in error
                for error in errors
            )
        )

    def test_conditional_requires_condition(self):
        record = make_record()

        record[
            "response_class_results"
        ][1][
            "required_conditions"
        ] = []

        record[
            "mc_evaluation_id"
        ] = module.compute_mc_evaluation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "CONDITIONAL response class requires conditions"
                in error
                for error in errors
            )
        )

    def test_inadmissible_requires_reason(self):
        record = make_record()

        record[
            "response_class_results"
        ][2][
            "inadmissibility_reasons"
        ] = []

        record[
            "mc_evaluation_id"
        ] = module.compute_mc_evaluation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "INADMISSIBLE response class requires reasons"
                in error
                for error in errors
            )
        )

    def test_one_disposition_per_response_class(self):
        record = make_record()

        record[
            "response_class_results"
        ].append(
            {
                "response_class":
                    "observation",
                "disposition":
                    "INADMISSIBLE",
                "required_conditions": [],
                "inadmissibility_reasons": [
                    "reason:duplicate"
                ]
            }
        )

        record[
            "mc_evaluation_id"
        ] = module.compute_mc_evaluation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "may appear only once"
                in error
                for error in errors
            )
        )

    def test_blocked_requires_reason(self):
        record = make_record()

        record[
            "evaluation_disposition"
        ] = "BLOCKED"

        record[
            "blocking_reasons"
        ] = []

        record[
            "mc_evaluation_id"
        ] = module.compute_mc_evaluation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "BLOCKED MC evaluation requires blocking reasons"
                in error
                for error in errors
            )
        )

    def test_ephemerality_collision_cannot_disappear(self):
        record = make_record()

        record[
            "ephemerality_collision_state"
        ] = "RESOLVED"

        record[
            "mc_evaluation_id"
        ] = module.compute_mc_evaluation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "ephemerality collision must remain explicit"
                in error
                for error in errors
            )
        )

    def test_ccr_collision_cannot_disappear(self):
        record = make_record()

        record[
            "interface_collision_state"
        ] = "DIRECT_PMC_ALLOWED"

        record[
            "mc_evaluation_id"
        ] = module.compute_mc_evaluation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "must preserve CCR"
                in error
                for error in errors
            )
        )

    def test_authority_remains_none(self):
        record = make_record()

        record[
            "authority_state"
        ] = "WRITE"

        record[
            "mc_evaluation_id"
        ] = module.compute_mc_evaluation_id(
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

    def test_material_change_changes_identity(self):
        first = make_record()
        second = make_record()

        second[
            "response_class_results"
        ][0][
            "disposition"
        ] = "INADMISSIBLE"

        second[
            "response_class_results"
        ][0][
            "inadmissibility_reasons"
        ] = [
            "reason:changed"
        ]

        second[
            "mc_evaluation_id"
        ] = module.compute_mc_evaluation_id(
            second
        )

        self.assertNotEqual(
            first["mc_evaluation_id"],
            second["mc_evaluation_id"]
        )

    def test_schema_does_not_absorb_forbidden_semantics(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "raw_telemetry",
            "selected_world_id_override",
            "pmc_candidate_ordering_override",
            "new_evidence",
            "incident_declaration",
            "actor_attribution",
            "execution_authorization",
            "publication_authorization",
            "canonical_promotion",
            "room_lifecycle_transition",
            "mc_internal_working_state",
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
