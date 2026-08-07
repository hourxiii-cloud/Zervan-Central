import importlib.util

from pathlib import Path

import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (

    ROOT

    / "tools"

    / "validate_representation_transform.py"

)

spec = importlib.util.spec_from_file_location(

    "validate_representation_transform",

    VALIDATOR

)

module = importlib.util.module_from_spec(spec)

spec.loader.exec_module(module)

def make_transform():

    object_id = (

        "sha512:"

        + "2" * 128

    )

    transform = {

        "object_id":

            object_id,

        "source_orientation": {

            "reference":

                "orientation:a"

        },

        "target_orientation": {

            "reference":

                "orientation:b"

        },

        "shifted_dimensions": [

            "observer",

            "discipline",

        ],

        "preserved_invariants":

            sorted(

                module.REQUIRED_INVARIANTS

            ),

        "included_evidence": [

            "evidence:a"

        ],

        "excluded_evidence": [

            "evidence:b"

        ],

        "assumptions": [

            "assumption:a"

        ],

        "prohibited_assumptions": [

            "assumption:b"

        ],

        "evidence_ceiling":

            "CEILING:A",

        "return_coordinates": {

            "reference":

                "return:a"

        },

    }

    transform["transform_id"] = (

        module.compute_transform_id(

            transform["object_id"],

            transform["source_orientation"],

            transform["target_orientation"],

            transform["shifted_dimensions"],

            transform["preserved_invariants"],

            transform["included_evidence"],

            transform["excluded_evidence"],

            transform["assumptions"],

            transform["prohibited_assumptions"],

            transform["evidence_ceiling"],

            transform["return_coordinates"],

        )

    )

    return transform

class RepresentationTransformTests(

    unittest.TestCase

):

    def test_repository_contract(self):

        self.assertEqual(

            module.validate(),

            []

        )

    def test_valid_transform(self):

        transform = make_transform()

        self.assertEqual(

            module.validate_transform(

                transform

            ),

            []

        )

    def test_missing_required_invariant_fails(self):

        transform = make_transform()

        transform[

            "preserved_invariants"

        ].remove(

            "object_identity"

        )

        transform["transform_id"] = (

            module.compute_transform_id(

                transform["object_id"],

                transform["source_orientation"],

                transform["target_orientation"],

                transform["shifted_dimensions"],

                transform["preserved_invariants"],

                transform["included_evidence"],

                transform["excluded_evidence"],

                transform["assumptions"],

                transform["prohibited_assumptions"],

                transform["evidence_ceiling"],

                transform["return_coordinates"],

            )

        )

        errors = module.validate_transform(

            transform

        )

        self.assertTrue(

            any(

                "required transform invariants missing"

                in error

                for error in errors

            )

        )

    def test_evidence_overlap_fails(self):

        transform = make_transform()

        transform[

            "excluded_evidence"

        ].append(

            "evidence:a"

        )

        transform["transform_id"] = (

            module.compute_transform_id(

                transform["object_id"],

                transform["source_orientation"],

                transform["target_orientation"],

                transform["shifted_dimensions"],

                transform["preserved_invariants"],

                transform["included_evidence"],

                transform["excluded_evidence"],

                transform["assumptions"],

                transform["prohibited_assumptions"],

                transform["evidence_ceiling"],

                transform["return_coordinates"],

            )

        )

        errors = module.validate_transform(

            transform

        )

        self.assertTrue(

            any(

                "both included and excluded"

                in error

                for error in errors

            )

        )

    def test_active_and_prohibited_assumption_conflict_fails(self):

        transform = make_transform()

        transform[

            "prohibited_assumptions"

        ].append(

            "assumption:a"

        )

        transform["transform_id"] = (

            module.compute_transform_id(

                transform["object_id"],

                transform["source_orientation"],

                transform["target_orientation"],

                transform["shifted_dimensions"],

                transform["preserved_invariants"],

                transform["included_evidence"],

                transform["excluded_evidence"],

                transform["assumptions"],

                transform["prohibited_assumptions"],

                transform["evidence_ceiling"],

                transform["return_coordinates"],

            )

        )

        errors = module.validate_transform(

            transform

        )

        self.assertTrue(

            any(

                "simultaneously active and prohibited"

                in error

                for error in errors

            )

        )

    def test_target_orientation_change_changes_transform_id(self):

        transform = make_transform()

        changed = module.compute_transform_id(

            transform["object_id"],

            transform["source_orientation"],

            {"reference": "orientation:c"},

            transform["shifted_dimensions"],

            transform["preserved_invariants"],

            transform["included_evidence"],

            transform["excluded_evidence"],

            transform["assumptions"],

            transform["prohibited_assumptions"],

            transform["evidence_ceiling"],

            transform["return_coordinates"],

        )

        self.assertNotEqual(

            transform["transform_id"],

            changed

        )

    def test_transform_id_does_not_replace_object_id(self):

        transform = make_transform()

        self.assertNotEqual(

            transform["transform_id"],

            transform["object_id"]

        )

    def test_schema_does_not_pull_cartography_forward(self):

        schema = module.load_schema()

        properties = set(

            schema["properties"]

        )

        for field in {

            "cartography_id",

            "stick_id",

            "occupation_id",

            "passageway_id",

        }:

            self.assertNotIn(

                field,

                properties

            )

if __name__ == "__main__":

    unittest.main()

