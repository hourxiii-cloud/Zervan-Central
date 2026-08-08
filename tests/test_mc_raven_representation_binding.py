import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_mc_raven_representation_binding.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_mc_raven_representation_binding",
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
        "mc_evaluation_id":
            "sha512:" + "1" * 128,
        "ccr_id":
            "sha512:" + "2" * 128,
        "object_id":
            "sha512:" + "3" * 128,
        "room_revision_id":
            "revision:test",
        "room_state_root":
            "sha512:" + "4" * 128,
        "authorized_view_root":
            "sha512:" + "5" * 128,
        "evidence_boundary_reference":
            "boundary:test",
        "evidence_ceiling_reference":
            "ceiling:test",
        "coordinate_reference":
            "coordinate:test",
        "upstream_representation_reference":
            "representation:test",
        "raven_transform_references": [
            "transform:test"
        ],
        "findings": [
            {
                "finding_id":
                    "finding:test",
                "classification":
                    "OBSERVED",
                "text":
                    "Supported finding."
            },
            {
                "finding_id":
                    "unknown:test",
                "classification":
                    "UNKNOWN",
                "text":
                    "Known unknown."
            }
        ],
        "unknowns": [
            "Known unknown."
        ],
        "mc_response_class_results": [
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
                    "mitigation",
                "disposition":
                    "CONDITIONAL",
                "required_conditions": [
                    "condition:test"
                ],
                "inadmissibility_reasons": []
            },
            {
                "response_class":
                    "escalation",
                "disposition":
                    "INADMISSIBLE",
                "required_conditions": [],
                "inadmissibility_reasons": [
                    "reason:test"
                ]
            }
        ],
        "trace_map": [
            {
                "claim_reference":
                    "finding:test",
                "source_references": [
                    "evidence:test",
                    "mc:test"
                ]
            }
        ],
        "lineage_reference":
            "lineage:test",
        "provenance_route": [
            "sha512:" + "3" * 128,
            "sha512:" + "2" * 128,
            "sha512:" + "1" * 128,
            "raven:test"
        ],
        "raven_status":
            "DEGRADED",
        "unkindness_disposition":
            "RAVEN_ASSOCIATED_FORWARD_TRANSLATION",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "raven_representation_id"
    ] = module.compute_raven_representation_id(
        record
    )

    return record


class MCRavenRepresentationBindingTests(
    unittest.TestCase
):

    def test_valid_raven_binding(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_mc_evaluation_required(self):
        record = make_record()

        record[
            "mc_evaluation_id"
        ] = ""

        record[
            "raven_representation_id"
        ] = module.compute_raven_representation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "mc_evaluation_id"
                in error
                for error in errors
            )
        )

    def test_material_finding_requires_trace(self):
        record = make_record()

        record[
            "trace_map"
        ] = []

        record[
            "raven_representation_id"
        ] = module.compute_raven_representation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "material Raven finding requires trace mapping"
                in error
                for error in errors
            )
        )

    def test_unknown_does_not_require_false_trace(self):
        record = make_record()

        record[
            "findings"
        ] = [
            {
                "finding_id":
                    "unknown:test",
                "classification":
                    "UNKNOWN",
                "text":
                    "Unknown."
            }
        ]

        record[
            "trace_map"
        ] = []

        record[
            "raven_representation_id"
        ] = module.compute_raven_representation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertFalse(
            any(
                "material Raven finding requires trace mapping"
                in error
                for error in errors
            )
        )

    def test_conditional_requirement_preserved(self):
        record = make_record()

        record[
            "mc_response_class_results"
        ][1][
            "required_conditions"
        ] = []

        record[
            "raven_representation_id"
        ] = module.compute_raven_representation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "preserve conditions"
                in error
                for error in errors
            )
        )

    def test_inadmissibility_reason_preserved(self):
        record = make_record()

        record[
            "mc_response_class_results"
        ][2][
            "inadmissibility_reasons"
        ] = []

        record[
            "raven_representation_id"
        ] = module.compute_raven_representation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "preserve reasons"
                in error
                for error in errors
            )
        )

    def test_duplicate_mc_class_rejected(self):
        record = make_record()

        record[
            "mc_response_class_results"
        ].append(
            {
                "response_class":
                    "observation",
                "disposition":
                    "ADMISSIBLE",
                "required_conditions": [],
                "inadmissibility_reasons": []
            }
        )

        record[
            "raven_representation_id"
        ] = module.compute_raven_representation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "may not duplicate MC response class"
                in error
                for error in errors
            )
        )

    def test_unkindness_remains_raven_associated(self):
        record = make_record()

        record[
            "unkindness_disposition"
        ] = "SEPARATE_PIPELINE_STAGE"

        record[
            "raven_representation_id"
        ] = module.compute_raven_representation_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "Raven-associated forward translation"
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
            "raven_representation_id"
        ] = module.compute_raven_representation_id(
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
            "raven_transform_references"
        ] = [
            "transform:different"
        ]

        second[
            "raven_representation_id"
        ] = module.compute_raven_representation_id(
            second
        )

        self.assertNotEqual(
            first[
                "raven_representation_id"
            ],
            second[
                "raven_representation_id"
            ]
        )

    def test_schema_does_not_absorb_forbidden_semantics(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "new_evidence",
            "raw_telemetry",
            "pmc_world_selection",
            "ccr_generation",
            "mc_disposition_override",
            "publication_authorization",
            "execution_authorization",
            "canonical_promotion",
            "room_lifecycle_transition",
            "cartography_mutation",
            "decision_authority",
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
