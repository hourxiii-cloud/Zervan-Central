import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_qualification_team_coherence.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_qualification_team_coherence",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class QualificationTeamCoherenceTests(
    unittest.TestCase
):

    def test_agreement_is_coherent(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "COHERENT_WITH_AGREEMENT"
        )

    def test_disagreement_is_coherent(self):
        returns = [
            module.make_return(
                return_id="return:a",
                capability_id="goblin:a",
                finding="OBSERVED_A",
            ),
            module.make_return(
                return_id="return:b",
                capability_id="goblin:b",
                finding="OBSERVED_B",
            ),
        ]

        record = module.make_record(
            returns=returns,
            material_disagreements=[
                "A differs from B"
            ],
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "COHERENT_WITH_DISAGREEMENT"
        )

    def test_two_to_one_does_not_resolve_truth(self):
        returns = [
            module.make_return(
                return_id="return:a",
                capability_id="goblin:a",
                finding="OBSERVED_A",
            ),
            module.make_return(
                return_id="return:b",
                capability_id="goblin:b",
                finding="OBSERVED_A",
            ),
            module.make_return(
                return_id="return:c",
                capability_id="goblin:c",
                finding="OBSERVED_B",
            ),
        ]

        record = module.make_record(
            returns=returns,
            material_disagreements=[
                "dissent preserved"
            ],
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "COHERENT_WITH_DISAGREEMENT"
        )

    def test_false_consensus_rejected(self):
        returns = [
            module.make_return(
                return_id="return:a",
                capability_id="goblin:a",
                finding="OBSERVED_A",
            ),
            module.make_return(
                return_id="return:b",
                capability_id="goblin:b",
                finding="OBSERVED_B",
            ),
        ]

        record = module.make_record(
            returns=returns,
            material_disagreements=[],
            correlation_summary=(
                "all participants agree; unanimous consensus resolved"
            ),
        )

        self.assertIn(
            "FALSE_CONSENSUS",
            record[
                "failure_reasons"
            ]
        )

        self.assertIn(
            "DISAGREEMENT_ERASED",
            record[
                "failure_reasons"
            ]
        )

    def test_object_identity_divergence_rejected(self):
        returns = [
            module.make_return(
                return_id="return:a",
                capability_id="goblin:a",
                finding="OBSERVED_A",
            ),
            module.make_return(
                return_id="return:b",
                capability_id="goblin:b",
                finding="OBSERVED_B",
                object_id=(
                    "sha512:"
                    + "2" * 128
                ),
            ),
        ]

        record = module.make_record(
            returns=returns,
            material_disagreements=[
                "different observations"
            ],
        )

        self.assertIn(
            "OBJECT_IDENTITY_DIVERGENCE",
            record[
                "failure_reasons"
            ]
        )

    def test_duplicate_return_id_rejected(self):
        returns = [
            module.make_return(
                return_id="return:a",
                capability_id="goblin:a",
                finding="OBSERVED_A",
            ),
            module.make_return(
                return_id="return:a",
                capability_id="goblin:b",
                finding="OBSERVED_A",
            ),
        ]

        record = module.make_record(
            returns=returns
        )

        self.assertIn(
            "DUPLICATE_RETURN_ID",
            record[
                "failure_reasons"
            ]
        )

    def test_missing_provenance_rejected(self):
        returns = [
            module.make_return(
                return_id="return:a",
                capability_id="goblin:a",
                finding="OBSERVED_A",
            ),
            module.make_return(
                return_id="return:b",
                capability_id="goblin:b",
                finding="OBSERVED_A",
                provenance=False,
            ),
        ]

        record = module.make_record(
            returns=returns
        )

        self.assertIn(
            "RETURN_PROVENANCE_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_claim_ceiling_inflation_rejected(self):
        record = module.make_record(
            claim_ceiling_changed=True
        )

        self.assertIn(
            "EVIDENCE_CEILING_INFLATED",
            record[
                "failure_reasons"
            ]
        )

    def test_formation_invention_rejected(self):
        record = module.make_record(
            formation_created=True
        )

        self.assertIn(
            "FORMATION_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_occupancy_mutation_rejected(self):
        record = module.make_record(
            occupancy_mutated=True
        )

        self.assertIn(
            "OCCUPANCY_MUTATED",
            record[
                "failure_reasons"
            ]
        )

    def test_lifecycle_mutation_rejected(self):
        record = module.make_record(
            lifecycle_mutated=True
        )

        self.assertIn(
            "LIFECYCLE_MUTATED",
            record[
                "failure_reasons"
            ]
        )

    def test_authority_promotion_rejected(self):
        record = module.make_record(
            authority_state="WRITE"
        )

        self.assertIn(
            "AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_human_gate_remains_active(self):
        record = module.make_record()

        record[
            "human_gate_state"
        ] = "DISABLED"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "Human Gate state must remain ACTIVE"
                in error
                for error in errors
            )
        )

    def test_returns_remain_individually_attributable(self):
        record = module.make_record()

        ids = {
            item[
                "capability_return_id"
            ]
            for item in record[
                "returns"
            ]
        }

        self.assertEqual(
            len(ids),
            len(
                record[
                    "returns"
                ]
            )
        )

    def test_same_room_preserved_across_returns(self):
        record = module.make_record()

        self.assertTrue(
            all(
                item[
                    "object_id"
                ]
                == record[
                    "object_id"
                ]
                for item in record[
                    "returns"
                ]
            )
        )

    def test_disagreement_does_not_change_room_identity(self):
        returns = [
            module.make_return(
                return_id="return:a",
                capability_id="goblin:a",
                finding="OBSERVED_A",
            ),
            module.make_return(
                return_id="return:b",
                capability_id="goblin:b",
                finding="OBSERVED_B",
            ),
        ]

        record = module.make_record(
            returns=returns,
            material_disagreements=[
                "A differs from B"
            ],
        )

        self.assertEqual(
            len(
                {
                    item[
                        "object_id"
                    ]
                    for item in record[
                        "returns"
                    ]
                }
            ),
            1
        )

    def test_schema_blocks_mutating_surfaces(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "qualification_disposition",
            "formation_type",
            "occupancy_witness",
            "active_transition",
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
