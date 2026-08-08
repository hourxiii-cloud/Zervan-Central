import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = ROOT / "tools/validate_distinct_object_validation.py"

spec = importlib.util.spec_from_file_location(
    "validate_distinct_object_validation",
    VALIDATOR
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DistinctObjectValidationTests(unittest.TestCase):

    def test_perspective_change_same_object(self):
        record = module.make_record(
            determination="SAME_OBJECT",
            perspective_changed=True,
            zone_changed=True,
            space_changed=True,
            authorized_view_changed=True,
        )

        self.assertEqual(
            record["validation_disposition"],
            "VALID"
        )

    def test_branch_same_object_by_default(self):
        record = module.make_record(
            determination="SAME_OBJECT",
            branch_present=True,
        )

        self.assertEqual(
            record["validation_disposition"],
            "VALID"
        )

    def test_distinct_object_valid(self):
        record = module.distinct_record()

        self.assertEqual(
            record["validation_disposition"],
            "VALID"
        )

    def test_distinct_object_requires_different_identity(self):
        record = module.distinct_record()
        record["candidate_target_object_id"] = record["source_object_id"]
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "DISTINCT_OBJECT_IDENTITY_COLLISION",
            record["failure_reasons"]
        )

    def test_distinct_object_requires_evidence(self):
        record = module.distinct_record()
        record["evidence_of_distinctness"] = []
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "DISTINCTNESS_WITHOUT_EVIDENCE",
            record["failure_reasons"]
        )

    def test_distinct_object_requires_genesis(self):
        record = module.distinct_record()
        record["independent_genesis_reference"] = None
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "INDEPENDENT_GENESIS_MISSING",
            record["failure_reasons"]
        )

    def test_distinct_object_requires_origin(self):
        record = module.distinct_record()
        record["independent_origin_reference"] = None
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "INDEPENDENT_ORIGIN_MISSING",
            record["failure_reasons"]
        )

    def test_distinct_object_requires_boundary(self):
        record = module.distinct_record()
        record["independent_boundary_reference"] = None
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "INDEPENDENT_BOUNDARY_MISSING",
            record["failure_reasons"]
        )

    def test_distinct_object_requires_geometry(self):
        record = module.distinct_record()
        record["independent_geometry_reference"] = None
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "INDEPENDENT_GEOMETRY_MISSING",
            record["failure_reasons"]
        )

    def test_distinct_object_requires_non_shared_provenance(self):
        record = module.distinct_record()
        record["non_shared_provenance"] = []
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "NON_SHARED_PROVENANCE_MISSING",
            record["failure_reasons"]
        )

    def test_same_object_cannot_establish_passageway(self):
        record = module.make_record(
            determination="SAME_OBJECT",
            perspective_changed=True,
            passageway_state="ESTABLISHED",
        )

        self.assertIn(
            "PASSAGEWAY_ESTABLISHED_FOR_SAME_OBJECT",
            record["failure_reasons"]
        )

    def test_unresolved_cannot_establish_passageway(self):
        record = module.make_record(
            determination="UNRESOLVED",
            target_object_id="sha512:" + "2" * 128,
            passageway_state="ESTABLISHED",
        )

        self.assertIn(
            "PASSAGEWAY_ESTABLISHED_WHILE_UNRESOLVED",
            record["failure_reasons"]
        )

    def test_unresolved_may_remain_proposed(self):
        record = module.make_record(
            determination="UNRESOLVED",
            target_object_id="sha512:" + "2" * 128,
            passageway_state="PROPOSED",
        )

        self.assertEqual(
            record["validation_disposition"],
            "VALID"
        )

    def test_unresolved_cannot_create_new_object(self):
        record = module.make_record(
            determination="UNRESOLVED",
            target_object_id="sha512:" + "2" * 128,
            passageway_state="PROPOSED",
            new_object_created=True,
        )

        self.assertIn(
            "NEW_OBJECT_CREATED_WHILE_UNRESOLVED",
            record["failure_reasons"]
        )

    def test_perspective_clone_rejected(self):
        record = module.make_record(
            determination="SAME_OBJECT",
            target_object_id="sha512:" + "2" * 128,
            perspective_changed=True,
        )

        self.assertIn(
            "PERSPECTIVE_CLONED_AS_OBJECT",
            record["failure_reasons"]
        )

    def test_branch_clone_rejected(self):
        record = module.make_record(
            determination="SAME_OBJECT",
            target_object_id="sha512:" + "2" * 128,
            branch_present=True,
        )

        self.assertIn(
            "BRANCH_CLONED_AS_OBJECT",
            record["failure_reasons"]
        )

    def test_established_passageway_requires_controls(self):
        record = module.distinct_record()
        record["contamination_controls"] = []
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "PASSAGEWAY_CONTROLS_MISSING",
            record["failure_reasons"]
        )

    def test_established_passageway_requires_return_route(self):
        record = module.distinct_record()
        record["return_route"] = None
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "RETURN_ROUTE_MISSING",
            record["failure_reasons"]
        )

    def test_authority_promotion_rejected(self):
        record = module.distinct_record()
        record["authority_state"] = "WRITE"
        record["failure_reasons"] = module.evaluate_record(record)

        self.assertIn(
            "AUTHORITY_PROMOTED",
            record["failure_reasons"]
        )

    def test_human_gate_remains_active(self):
        record = module.distinct_record()
        record["human_gate_state"] = "DISABLED"

        errors = module.validate_record(record)

        self.assertTrue(
            any(
                "Human Gate state must remain ACTIVE"
                in error
                for error in errors
            )
        )


if __name__ == "__main__":
    unittest.main()
