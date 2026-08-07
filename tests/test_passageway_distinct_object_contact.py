import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_passageway_distinct_object_contact.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_passageway_distinct_object_contact",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_passageway(
    result="DISTINCT_OBJECT",
    state="ESTABLISHED"
):
    source = (
        "sha512:"
        + "3" * 128
    )

    target = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version": "1.0",
        "source_object_id": source,
        "target_object_id": target,
        "distinct_object_determination_reference":
            "distinct:test",
        "distinct_object_result":
            result,
        "relationship_to_source":
            "adjoining object",
        "source_origin_reference":
            "origin:source",
        "target_origin_reference":
            "origin:target",
        "source_cartography_reference":
            "cartography:source",
        "target_cartography_reference":
            "cartography:target",
        "source_stick_reference":
            "stick:source",
        "target_stick_reference":
            "stick:target",
        "shared_provenance": [
            "provenance:shared"
        ],
        "non_shared_provenance": [
            "provenance:source",
            "provenance:target"
        ],
        "evidence_of_distinctness_references": [
            "evidence:distinct"
        ],
        "passageway_conditions": [
            "condition:a"
        ],
        "contamination_controls": [
            "control:a"
        ],
        "return_route": [
            "source",
            "orientation:source"
        ],
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "passageway_state":
            state,
        "provenance_route": [
            source,
            "distinct:test",
            target,
        ],
        "recorded_at":
            "2026-08-07T18:58:00-04:00",
    }

    record[
        "passageway_id"
    ] = module.compute_passageway_id(
        record
    )

    return record


class PassagewayDistinctObjectContactTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_established_passageway(self):
        record = make_passageway()

        self.assertEqual(
            module.validate_passageway(
                record
            ),
            []
        )

    def test_same_object_cannot_establish_passageway(self):
        record = make_passageway(
            result="SAME_OBJECT"
        )

        record[
            "target_object_id"
        ] = record[
            "source_object_id"
        ]

        record[
            "passageway_id"
        ] = module.compute_passageway_id(
            record
        )

        errors = module.validate_passageway(
            record
        )

        self.assertTrue(
            errors
        )

    def test_unresolved_cannot_establish_passageway(self):
        record = make_passageway(
            result="UNRESOLVED"
        )

        errors = module.validate_passageway(
            record
        )

        self.assertTrue(
            any(
                "DISTINCT_OBJECT"
                in error
                or "UNRESOLVED"
                in error
                for error in errors
            )
        )

    def test_proposed_may_preserve_unresolved_contact(self):
        record = make_passageway(
            result="UNRESOLVED",
            state="PROPOSED"
        )

        self.assertEqual(
            module.validate_passageway(
                record
            ),
            []
        )

    def test_passageway_identity_is_deterministic(self):
        record = make_passageway()

        self.assertEqual(
            record["passageway_id"],
            module.compute_passageway_id(
                record
            )
        )

    def test_passageway_id_does_not_replace_object_ids(self):
        record = make_passageway()

        self.assertNotEqual(
            record["passageway_id"],
            record["source_object_id"]
        )

        self.assertNotEqual(
            record["passageway_id"],
            record["target_object_id"]
        )

    def test_schema_does_not_pull_occupation_or_merge_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        properties = set(
            schema["properties"]
        )

        for field in {
            "occupation_id",
            "occupant_id",
            "capability_position",
            "movement_execution",
            "traversal_record",
            "merge_id",
            "new_object_id",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
