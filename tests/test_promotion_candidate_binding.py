import importlib.util
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR_PATH = ROOT / (
    "tools/"
    "validate_promotion_candidate_binding.py"
)
RESOLVER_PATH = ROOT / (
    "tools/"
    "resolve_promotion_candidate_binding.py"
)

validator_spec = importlib.util.spec_from_file_location(
    "validate_promotion_candidate_binding",
    VALIDATOR_PATH,
)
validator = importlib.util.module_from_spec(
    validator_spec
)
validator_spec.loader.exec_module(
    validator
)

resolver_spec = importlib.util.spec_from_file_location(
    "resolve_promotion_candidate_binding",
    RESOLVER_PATH,
)
resolver = importlib.util.module_from_spec(
    resolver_spec
)
resolver_spec.loader.exec_module(
    resolver
)


class PromotionCandidateBindingTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(cls):
        cls.binding = resolver.resolve(
            "HEAD"
        )

    def test_validator(self):
        self.assertEqual(
            validator.validate(),
            [],
        )

    def test_record_type(self):
        self.assertEqual(
            self.binding[
                "record_type"
            ],
            "PROMOTION_CANDIDATE_BINDING",
        )

    def test_ring(self):
        self.assertEqual(
            self.binding[
                "ring"
            ],
            "R8-C",
        )

    def test_candidate_branch(self):
        self.assertEqual(
            self.binding[
                "candidate_branch"
            ],
            "candidate/v41-complete",
        )

    def test_candidate_commit_exact(self):
        self.assertEqual(
            len(
                self.binding[
                    "candidate_commit"
                ]
            ),
            40,
        )

    def test_candidate_tree_exact(self):
        self.assertEqual(
            len(
                self.binding[
                    "candidate_tree"
                ]
            ),
            40,
        )

    def test_target_main(self):
        self.assertEqual(
            self.binding[
                "target_branch"
            ],
            "main",
        )

    def test_ring7_blob(self):
        self.assertEqual(
            len(
                self.binding[
                    "ring7_closure_blob"
                ]
            ),
            40,
        )

    def test_r8a_blob(self):
        self.assertEqual(
            len(
                self.binding[
                    "r8a_boundary_blob"
                ]
            ),
            40,
        )

    def test_r8b_blob(self):
        self.assertEqual(
            len(
                self.binding[
                    "r8b_decision_contract_blob"
                ]
            ),
            40,
        )

    def test_deterministic_hash(self):
        payload = dict(
            self.binding
        )

        supplied = payload.pop(
            "binding_sha512"
        )

        serialized = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

        expected = hashlib.sha512(
            serialized
        ).hexdigest()

        self.assertEqual(
            supplied,
            expected,
        )

    def test_hash_length(self):
        self.assertEqual(
            len(
                self.binding[
                    "binding_sha512"
                ]
            ),
            128,
        )

    def test_authority_none(self):
        self.assertEqual(
            self.binding[
                "authority_state"
            ],
            "NONE",
        )

    def test_human_gate_active(self):
        self.assertEqual(
            self.binding[
                "human_gate_state"
            ],
            "ACTIVE",
        )

    def test_contract_no_self_reference(self):
        text = validator.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "No self-referential candidate binding is permitted.",
            text,
        )

    def test_binding_not_decision(self):
        text = validator.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Binding != decision.",
            text,
        )

    def test_binding_not_authorization(self):
        text = validator.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Binding != authorization.",
            text,
        )

    def test_binding_not_execution(self):
        text = validator.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Binding != execution.",
            text,
        )

    def test_closure(self):
        text = validator.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "R8-C PROMOTION CANDIDATE BINDING COMPLETE.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
