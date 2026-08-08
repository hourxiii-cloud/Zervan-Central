import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_report_rendering_contract.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_report_rendering_contract",
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
        "report_class":
            "TECHNICAL",
        "rendering_profile": {
            "format":
                "markdown",
            "audience":
                "technical",
            "density":
                "full",
            "language":
                "en"
        },
        "raven_representation_id":
            "sha512:" + "1" * 128,
        "decision_option_references": [
            "option:test"
        ],
        "human_gate_decision_reference":
            None,
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
                    "Unknown."
            }
        ],
        "unknowns": [
            "Unknown."
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
                    "raven:test"
                ]
            }
        ],
        "redaction_references": [
            {
                "restricted_reference":
                    "restricted:test",
                "existence_preserved":
                    True,
                "governing_reference":
                    "governance:test"
            }
        ],
        "lineage_reference":
            "lineage:test",
        "provenance_route": [
            "room:test",
            "pmc:test",
            "ccr:test",
            "mc:test",
            "raven:test",
            "report:test"
        ],
        "report_status":
            "DEGRADED",
        "publication_state":
            "RENDERED",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "report_id"
    ] = module.compute_report_id(
        record
    )

    return record


class ReportRenderingContractTests(
    unittest.TestCase
):

    def test_valid_report(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_raven_binding_required(self):
        record = make_record()

        record[
            "raven_representation_id"
        ] = ""

        record[
            "report_id"
        ] = module.compute_report_id(
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

    def test_material_finding_requires_trace(self):
        record = make_record()

        record[
            "trace_map"
        ] = []

        record[
            "report_id"
        ] = module.compute_report_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "material report finding requires trace mapping"
                in error
                for error in errors
            )
        )

    def test_unknown_need_not_be_promoted_to_fact(self):
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
            "report_id"
        ] = module.compute_report_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertFalse(
            any(
                "material report finding requires trace mapping"
                in error
                for error in errors
            )
        )

    def test_conditional_class_requires_condition(self):
        record = make_record()

        record[
            "mc_response_class_results"
        ][1][
            "required_conditions"
        ] = []

        record[
            "report_id"
        ] = module.compute_report_id(
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

    def test_inadmissible_class_requires_reason(self):
        record = make_record()

        record[
            "mc_response_class_results"
        ][2][
            "inadmissibility_reasons"
        ] = []

        record[
            "report_id"
        ] = module.compute_report_id(
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

    def test_publication_approved_requires_gate(self):
        record = make_record()

        record[
            "publication_state"
        ] = "PUBLICATION_APPROVED"

        record[
            "human_gate_decision_reference"
        ] = None

        record[
            "report_id"
        ] = module.compute_report_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "PUBLICATION_APPROVED requires Human Gate"
                in error
                for error in errors
            )
        )

    def test_valid_publication_approved_binding(self):
        record = make_record()

        record[
            "publication_state"
        ] = "PUBLICATION_APPROVED"

        record[
            "human_gate_decision_reference"
        ] = "human-gate:test"

        record[
            "report_id"
        ] = module.compute_report_id(
            record
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_redaction_preserves_existence(self):
        record = make_record()

        record[
            "redaction_references"
        ][0][
            "existence_preserved"
        ] = False

        record[
            "report_id"
        ] = module.compute_report_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "redaction must preserve restricted-content existence"
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
            "report_id"
        ] = module.compute_report_id(
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

    def test_material_change_changes_report_identity(self):
        first = make_record()
        second = make_record()

        second[
            "rendering_profile"
        ][
            "audience"
        ] = "executive"

        second[
            "report_id"
        ] = module.compute_report_id(
            second
        )

        self.assertNotEqual(
            first[
                "report_id"
            ],
            second[
                "report_id"
            ]
        )

    def test_schema_does_not_absorb_forbidden_semantics(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "new_evidence",
            "pmc_world_selection",
            "mc_disposition_override",
            "decision_authority",
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
