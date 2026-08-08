import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_pipeline_integration_boundary.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_pipeline_integration_boundary",
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
        "native_version":
            "vTemporal.41.0",
        "promotion_state":
            "CANDIDATE",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "pipeline_sequence":
            list(module.PIPELINE),
        "pmc_meaning":
            "PROBABILISTIC_MULTIVERSE_COMPUTATION",
        "ccr_meaning":
            "CANONICAL_COMMITMENT_RECORD",
        "mc_meaning":
            "META_COLLAPSE_RESPONSE_ADMISSIBILITY",
        "unkindness_disposition":
            "RAVEN_ASSOCIATED_FORWARD_TRANSLATION",
        "pmc_mc_interface_collision":
            "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION",
        "room_binding_state":
            "BOUNDARY_LOCKED",
        "evidence_lineage_state":
            "PRESERVED",
        "coordinate_binding_state":
            "PRESERVED",
        "responsibility_separation_state":
            "PRESERVED",
        "provenance_route": [
            "naming-lock",
            "interface-collision",
            "raven",
            "human-gate",
            "room"
        ],
        "recorded_at":
            "2026-08-07T21:27:00-04:00",
    }

    record[
        "boundary_record_id"
    ] = module.compute_boundary_record_id(
        record
    )

    return record


class PipelineIntegrationBoundaryTests(
    unittest.TestCase
):

    def test_valid_boundary(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_ccr_cannot_be_omitted(self):
        record = make_record()

        record[
            "pipeline_sequence"
        ] = [
            "EVIDENCE",
            "PMC",
            "MC",
            "RAVEN",
            "HUMAN_GATE",
        ]

        record[
            "boundary_record_id"
        ] = module.compute_boundary_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "pipeline_sequence"
                in error
                for error in errors
            )
        )

    def test_unkindness_is_not_independent_stage(self):
        record = make_record()

        record[
            "unkindness_disposition"
        ] = "INDEPENDENT_PIPELINE_STAGE"

        record[
            "boundary_record_id"
        ] = module.compute_boundary_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "unkindness_disposition"
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
            "boundary_record_id"
        ] = module.compute_boundary_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "authority_state"
                in error
                for error in errors
            )
        )

    def test_pipeline_change_changes_identity(self):
        first = make_record()

        changed = make_record()

        changed[
            "evidence_lineage_state"
        ] = "BROKEN"

        changed[
            "boundary_record_id"
        ] = module.compute_boundary_record_id(
            changed
        )

        self.assertNotEqual(
            first[
                "boundary_record_id"
            ],
            changed[
                "boundary_record_id"
            ]
        )

    def test_schema_does_not_implement_downstream_stages(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "pmc_output",
            "ccr_content",
            "mc_decision",
            "raven_report",
            "human_gate_decision",
            "decision_option",
            "publication_authorization",
            "execution_authorization",
            "canonical_promotion",
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
