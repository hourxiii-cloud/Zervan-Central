import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_decision_option_lineage.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_decision_option_lineage",
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
        "option_label":
            "Observe",
        "option_description":
            "Continue bounded observation.",
        "option_status":
            "AVAILABLE",
        "object_id":
            "sha512:" + "1" * 128,
        "room_revision_id":
            "revision:test",
        "room_state_root":
            "sha512:" + "2" * 128,
        "authorized_view_root":
            "sha512:" + "3" * 128,
        "coordinate_reference":
            "coordinate:test",
        "evidence_boundary_reference":
            "boundary:test",
        "evidence_ceiling_reference":
            "ceiling:test",
        "pmc_intake_binding_id":
            "sha512:" + "4" * 128,
        "pmc_run_id":
            "pmc:test",
        "ccr_id":
            "sha512:" + "5" * 128,
        "mc_evaluation_id":
            "sha512:" + "6" * 128,
        "mc_response_class":
            "observation",
        "mc_disposition":
            "ADMISSIBLE",
        "required_conditions": [],
        "inadmissibility_reasons": [],
        "raven_representation_id":
            "sha512:" + "7" * 128,
        "human_gate_decision_reference":
            None,
        "uncertainty_references": [
            "uncertainty:test"
        ],
        "lineage_reference":
            "lineage:test",
        "provenance_route": [
            "room:test",
            "pmc:test",
            "ccr:test",
            "mc:test",
            "raven:test"
        ],
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "decision_option_id"
    ] = module.compute_decision_option_id(
        record
    )

    return record


class DecisionOptionLineageTests(
    unittest.TestCase
):

    def test_valid_available_option(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_available_requires_mc_admissible(self):
        record = make_record()

        record[
            "mc_disposition"
        ] = "INADMISSIBLE"

        record[
            "decision_option_id"
        ] = module.compute_decision_option_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "AVAILABLE requires MC ADMISSIBLE"
                in error
                for error in errors
            )
        )

    def test_conditional_requires_mc_conditional(self):
        record = make_record()

        record[
            "option_status"
        ] = "CONDITIONAL"

        record[
            "mc_disposition"
        ] = "ADMISSIBLE"

        record[
            "required_conditions"
        ] = [
            "condition:test"
        ]

        record[
            "decision_option_id"
        ] = module.compute_decision_option_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "requires MC CONDITIONAL"
                in error
                for error in errors
            )
        )

    def test_conditional_requires_conditions(self):
        record = make_record()

        record[
            "option_status"
        ] = "CONDITIONAL"

        record[
            "mc_disposition"
        ] = "CONDITIONAL"

        record[
            "required_conditions"
        ] = []

        record[
            "decision_option_id"
        ] = module.compute_decision_option_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "requires conditions"
                in error
                for error in errors
            )
        )

    def test_unavailable_requires_mc_inadmissible(self):
        record = make_record()

        record[
            "option_status"
        ] = "UNAVAILABLE"

        record[
            "mc_disposition"
        ] = "ADMISSIBLE"

        record[
            "inadmissibility_reasons"
        ] = [
            "reason:test"
        ]

        record[
            "decision_option_id"
        ] = module.compute_decision_option_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "UNAVAILABLE requires MC INADMISSIBLE"
                in error
                for error in errors
            )
        )

    def test_unavailable_requires_reason(self):
        record = make_record()

        record[
            "option_status"
        ] = "UNAVAILABLE"

        record[
            "mc_disposition"
        ] = "INADMISSIBLE"

        record[
            "inadmissibility_reasons"
        ] = []

        record[
            "decision_option_id"
        ] = module.compute_decision_option_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "requires inadmissibility reasons"
                in error
                for error in errors
            )
        )

    def test_room_identity_required(self):
        record = make_record()

        record[
            "object_id"
        ] = ""

        record[
            "decision_option_id"
        ] = module.compute_decision_option_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "object_id"
                in error
                for error in errors
            )
        )

    def test_raven_lineage_required(self):
        record = make_record()

        record[
            "raven_representation_id"
        ] = ""

        record[
            "decision_option_id"
        ] = module.compute_decision_option_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "raven_representation_id"
                in error
                for error in errors
            )
        )

    def test_human_gate_reference_may_be_null(self):
        record = make_record()

        self.assertIsNone(
            record[
                "human_gate_decision_reference"
            ]
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_authority_remains_none(self):
        record = make_record()

        record[
            "authority_state"
        ] = "WRITE"

        record[
            "decision_option_id"
        ] = module.compute_decision_option_id(
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
            "option_description"
        ] = "A materially different option."

        second[
            "decision_option_id"
        ] = module.compute_decision_option_id(
            second
        )

        self.assertNotEqual(
            first[
                "decision_option_id"
            ],
            second[
                "decision_option_id"
            ]
        )

    def test_schema_does_not_absorb_decision_authority(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "execution_authorization",
            "publication_authorization",
            "canonical_promotion",
            "decision_authority",
            "evidence_boundary_override",
            "evidence_ceiling_override",
            "room_lifecycle_transition",
            "preferred_option",
            "automatic_selection",
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
