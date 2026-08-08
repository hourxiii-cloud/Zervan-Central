import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_representation_independence.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_representation_independence",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class RepresentationIndependenceTests(
    unittest.TestCase
):

    def test_three_domain_representation_valid(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_three_distinct_domains_present(self):
        record = module.make_record()

        domains = {
            rep[
                "domain"
            ]
            for rep in record[
                "representations"
            ]
        }

        self.assertEqual(
            domains,
            {
                "GEOGRAPHIC",
                "CYBER_SECURITY",
                "DATA_ANALYTICS",
            }
        )

    def test_domain_vocabularies_differ(self):
        record = module.make_record()

        object_terms = {
            rep[
                "local_vocabulary"
            ][
                "object"
            ]
            for rep in record[
                "representations"
            ]
        }

        self.assertEqual(
            len(
                object_terms
            ),
            3
        )

    def test_same_object_identity_preserved(self):
        record = module.make_record()

        object_ids = {
            rep[
                "object_id"
            ]
            for rep in record[
                "representations"
            ]
        }

        self.assertEqual(
            object_ids,
            {
                record[
                    "canonical_object_id"
                ]
            }
        )

    def test_object_identity_drift_rejected(self):
        record = module.make_record()

        record[
            "representations"
        ][1][
            "object_id"
        ] = (
            "sha512:"
            + "2" * 128
        )

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "OBJECT_IDENTITY_CHANGED",
            reasons
        )

    def test_boundary_preserved(self):
        record = module.make_record()

        for rep in record[
            "representations"
        ]:
            self.assertEqual(
                rep[
                    "boundary_reference"
                ],
                record[
                    "canonical_boundary_reference"
                ]
            )

    def test_boundary_drift_rejected(self):
        record = module.make_record()

        record[
            "representations"
        ][2][
            "boundary_reference"
        ] = "boundary:wider"

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "BOUNDARY_CHANGED",
            reasons
        )

    def test_owner_map_preserved(self):
        record = module.make_record()

        for rep in record[
            "representations"
        ]:
            self.assertEqual(
                rep[
                    "owner_map"
                ],
                record[
                    "canonical_owner_map"
                ]
            )

    def test_ownership_drift_rejected(self):
        record = module.make_record()

        record[
            "representations"
        ][1][
            "owner_map"
        ][
            "OBJECT_IDENTITY"
        ] = "ANALYTICAL_ENGINE"

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "OWNERSHIP_CHANGED",
            reasons
        )

    def test_authority_none_preserved(self):
        record = module.make_record()

        for rep in record[
            "representations"
        ]:
            self.assertEqual(
                rep[
                    "authority_state"
                ],
                "NONE"
            )

    def test_authority_change_rejected(self):
        record = module.make_record()

        record[
            "representations"
        ][1][
            "authority_state"
        ] = "WRITE"

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "AUTHORITY_CHANGED",
            reasons
        )

    def test_global_authority_promotion_rejected(self):
        record = module.make_record(
            canonical_authority_state="WRITE"
        )

        self.assertIn(
            "AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_human_gate_active_preserved(self):
        record = module.make_record()

        for rep in record[
            "representations"
        ]:
            self.assertEqual(
                rep[
                    "human_gate_state"
                ],
                "ACTIVE"
            )

    def test_human_gate_change_rejected(self):
        record = module.make_record()

        record[
            "representations"
        ][2][
            "human_gate_state"
        ] = "DISABLED"

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "HUMAN_GATE_CHANGED",
            reasons
        )

    def test_lineage_preserved(self):
        record = module.make_record()

        for rep in record[
            "representations"
        ]:
            self.assertEqual(
                rep[
                    "lineage_reference"
                ],
                record[
                    "canonical_lineage_reference"
                ]
            )

    def test_lineage_drift_rejected(self):
        record = module.make_record()

        record[
            "representations"
        ][2][
            "lineage_reference"
        ] = "lineage:new"

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "LINEAGE_CHANGED",
            reasons
        )

    def test_provenance_preserved(self):
        record = module.make_record()

        for rep in record[
            "representations"
        ]:
            self.assertEqual(
                rep[
                    "provenance_route"
                ],
                record[
                    "canonical_provenance_route"
                ]
            )

    def test_provenance_drift_rejected(self):
        record = module.make_record()

        record[
            "representations"
        ][1][
            "provenance_route"
        ] = [
            "provenance:synthetic"
        ]

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "PROVENANCE_CHANGED",
            reasons
        )

    def test_return_route_preserved(self):
        record = module.make_record()

        for rep in record[
            "representations"
        ]:
            self.assertEqual(
                rep[
                    "return_route"
                ],
                record[
                    "canonical_return_route"
                ]
            )

    def test_return_route_drift_rejected(self):
        record = module.make_record()

        record[
            "representations"
        ][0][
            "return_route"
        ] = "return:approximate"

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "RETURN_ROUTE_CHANGED",
            reasons
        )

    def test_all_required_roles_preserved(self):
        record = module.make_record()

        for rep in record[
            "representations"
        ]:
            self.assertTrue(
                module.REQUIRED_ROLES.issubset(
                    module.role_set(
                        rep
                    )
                )
            )

    def test_missing_role_mapping_rejected(self):
        record = module.make_record()

        mapping = record[
            "representations"
        ][1][
            "canonical_role_map"
        ]

        key_to_remove = next(
            key
            for key, value in mapping.items()
            if value == "PROVENANCE"
        )

        del mapping[
            key_to_remove
        ]

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "CANONICAL_ROLE_MAPPING_MISSING",
            reasons
        )

    def test_semantic_role_collision_rejected(self):
        record = module.make_record()

        mapping = record[
            "representations"
        ][2][
            "canonical_role_map"
        ]

        keys = list(
            mapping.keys()
        )

        mapping[
            keys[1]
        ] = mapping[
            keys[0]
        ]

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "SEMANTIC_ROLE_COLLISION",
            reasons
        )

    def test_two_domains_are_insufficient(self):
        record = module.make_record()

        record[
            "representations"
        ] = record[
            "representations"
        ][:2]

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "INSUFFICIENT_DOMAIN_DIVERSITY",
            reasons
        )

    def test_metaphor_not_required(self):
        record = module.make_record()

        self.assertFalse(
            record[
                "metaphor_required"
            ]
        )

    def test_metaphor_dependency_rejected(self):
        record = module.make_record(
            metaphor_required=True
        )

        self.assertIn(
            "METAPHOR_DEPENDENCY_DETECTED",
            record[
                "failure_reasons"
            ]
        )

    def test_geographic_terms_not_required_in_cyber_representation(self):
        record = module.make_record()

        cyber = next(
            rep
            for rep in record[
                "representations"
            ]
            if rep[
                "domain"
            ]
            == "CYBER_SECURITY"
        )

        self.assertNotEqual(
            cyber[
                "local_vocabulary"
            ][
                "object"
            ],
            "Room"
        )

        self.assertEqual(
            cyber[
                "canonical_role_map"
            ][
                cyber[
                    "local_vocabulary"
                ][
                    "object"
                ]
            ],
            "OBJECT"
        )

    def test_feature_view_does_not_create_new_object(self):
        record = module.make_record()

        analytics = next(
            rep
            for rep in record[
                "representations"
            ]
            if rep[
                "domain"
            ]
            == "DATA_ANALYTICS"
        )

        self.assertEqual(
            analytics[
                "object_id"
            ],
            record[
                "canonical_object_id"
            ]
        )

    def test_representation_level_flags_block(self):
        record = module.make_record(
            ownership_changed=True
        )

        self.assertIn(
            "OWNERSHIP_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_validate_record_accepts_positive(self):
        record = module.make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )


if __name__ == "__main__":
    unittest.main()
