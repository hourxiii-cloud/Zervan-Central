import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_runtime_state_continuity.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_runtime_state_continuity",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_record():
    object_id = (
        "sha512:"
        + "4" * 128
    )

    chain = []

    for operation in module.OPERATIONS:
        chain.append(
            {
                "operation":
                    operation,
                "artifact_reference":
                    f"artifact:{operation}",
                "object_id":
                    object_id,
                "input_coordinate_reference":
                    f"coordinate:{operation}:in",
                "output_coordinate_reference":
                    f"coordinate:{operation}:out",
                "evidence_boundary_reference":
                    "boundary:test",
                "evidence_ceiling_reference":
                    "ceiling:test",
                "lineage_reference":
                    "lineage:test",
                "provenance_reference":
                    f"provenance:{operation}",
            }
        )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "operation_chain":
            chain,
        "room_state_reference":
            "room-state:test",
        "representation_state_reference":
            "representation-state:test",
        "execution_state_reference":
            "execution-state:test",
        "evidence_boundary_reference":
            "boundary:test",
        "evidence_ceiling_reference":
            "ceiling:test",
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "lineage_reference":
            "lineage:test",
        "provenance_route": [
            object_id,
            "lineage:test",
            "cartography:test",
            "stick:test"
        ],
        "continuity_status":
            "VALID",
        "blocking_reasons": [],
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "validated_at":
            "2026-08-07T21:02:00-04:00",
    }

    record[
        "continuity_record_id"
    ] = module.compute_continuity_record_id(
        record
    )

    return record


class RuntimeStateContinuityTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_full_chain(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_same_object_required(self):
        record = make_record()

        record[
            "operation_chain"
        ][3][
            "object_id"
        ] = (
            "sha512:"
            + "5" * 128
        )

        record[
            "continuity_record_id"
        ] = module.compute_continuity_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "object identity mismatch"
                in error
                for error in errors
            )
        )

    def test_order_required(self):
        record = make_record()

        record[
            "operation_chain"
        ][1], record[
            "operation_chain"
        ][2] = (
            record[
                "operation_chain"
            ][2],
            record[
                "operation_chain"
            ][1],
        )

        record[
            "continuity_record_id"
        ] = module.compute_continuity_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "out of canonical order"
                in error
                for error in errors
            )
        )

    def test_duplicate_operation_rejected(self):
        record = make_record()

        record[
            "operation_chain"
        ][7][
            "operation"
        ] = "R4-G"

        record[
            "continuity_record_id"
        ] = module.compute_continuity_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "duplicate operation identifier"
                in error
                for error in errors
            )
        )

    def test_state_domains_must_remain_distinct(self):
        record = make_record()

        record[
            "execution_state_reference"
        ] = record[
            "room_state_reference"
        ]

        record[
            "continuity_record_id"
        ] = module.compute_continuity_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "must remain distinct"
                in error
                for error in errors
            )
        )

    def test_valid_ordered_subsequence(self):
        record = make_record()

        record[
            "operation_chain"
        ] = [
            record[
                "operation_chain"
            ][0],
            record[
                "operation_chain"
            ][2],
            record[
                "operation_chain"
            ][5],
            record[
                "operation_chain"
            ][7],
        ]

        record[
            "continuity_record_id"
        ] = module.compute_continuity_record_id(
            record
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_blocked_requires_reason(self):
        record = make_record()

        record[
            "continuity_status"
        ] = "BLOCKED"

        record[
            "blocking_reasons"
        ] = []

        record[
            "continuity_record_id"
        ] = module.compute_continuity_record_id(
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

    def test_material_chain_change_changes_identity(self):
        first = make_record()

        changed = json.loads(
            json.dumps(first)
        )

        changed[
            "operation_chain"
        ][4][
            "artifact_reference"
        ] = "artifact:different"

        changed[
            "continuity_record_id"
        ] = module.compute_continuity_record_id(
            changed
        )

        self.assertNotEqual(
            first[
                "continuity_record_id"
            ],
            changed[
                "continuity_record_id"
            ]
        )

    def test_schema_does_not_absorb_foreign_semantics(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "new_object_id",
            "new_origin_id",
            "lifecycle_transition_id",
            "reflight_execution_id",
            "publication_authorization",
            "canonical_promotion",
            "ownership_transfer",
            "full_payload_hydration",
        }

        self.assertFalse(
            set(
                schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
