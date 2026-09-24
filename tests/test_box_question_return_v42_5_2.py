import copy
import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "tools/validate_box_question_return_v42_5_2.py"
SPEC = importlib.util.spec_from_file_location("box_question_return_v42_5_2", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

Q = "How do I feel right now throughout time and space?"


def valid_case():
    return {
        "schema_version": "1.0", "operation_id": "op:feeling", "governed_object_id": "object:andrew-feeling",
        "root_box_id": "box:one", "original_question": Q, "question_scope": "GLOBAL",
        "representations": [{
            "id": "rep:local", "root_box_id": "box:one", "governed_object_id": "object:andrew-feeling",
            "question": Q, "possibility_state": "OBSERVED", "observation_refs": ["observation:local"]
        }, {
            "id": "rep:unobserved", "root_box_id": "box:one", "governed_object_id": "object:andrew-feeling",
            "question": Q, "possibility_state": "AVAILABLE_UNACTUALIZED", "observation_refs": []
        }],
        "collapse": {"disposition": "PARTIAL_RESOLUTION", "standing_refs": ["standing:local"],
                     "unresolved_scope": ["global temporal/spatial state"],
                     "retained_possibilities": ["rep:unobserved"], "paradox_trigger": False},
        "return": {"question": Q, "result": "Locally delighted, amused, excited; global state unresolved.",
                   "answer_scope": "LOCAL", "root_box_id": "box:one",
                   "governed_object_id": "object:andrew-feeling",
                   "identity_receipt": {"question": Q, "root_box_id": "box:one", "governed_object_id": "object:andrew-feeling"},
                   "traversal_receipts": [{"representation_id": "rep:local", "evidence_refs": ["observation:local"]}],
                   "opened": True, "observed": True, "qualified": False},
        "authority_state": "NONE", "human_gate_state": "ACTIVE"
    }


class BoxReturnTests(unittest.TestCase):
    def test_global_question_survives_bounded_local_result(self):
        self.assertEqual(MODULE.validate(valid_case()), [])

    def test_shrunk_question_is_blocked_even_when_result_is_plausible(self):
        case = valid_case()
        case["return"]["question"] = "How do I appear to feel here?"
        self.assertIn("ORIGINAL_Q_NOT_RETURNED", MODULE.validate(case))

    def test_plural_representation_cannot_mutate_governed_question(self):
        case = valid_case()
        case["representations"][1]["question"] = "How did I feel yesterday?"
        self.assertIn("REPRESENTATION_QUESTION_DRIFT:1", MODULE.validate(case))

    def test_global_question_cannot_be_silently_answered_locally(self):
        case = valid_case()
        case["collapse"]["unresolved_scope"] = []
        self.assertIn("GLOBAL_Q_SHRUNK_TO_LOCAL_ANSWER", MODULE.validate(case))

    def test_possible_state_does_not_gain_observation_from_representation(self):
        case = valid_case()
        case["representations"][1]["possibility_state"] = "OBSERVED"
        self.assertIn("POSSIBILITY_PROMOTED_WITHOUT_OBSERVATION:1", MODULE.validate(case))

    def test_return_is_not_validation(self):
        case = valid_case()
        case["return"]["opened"] = False
        case["return"]["qualified"] = True
        self.assertIn("QUALIFICATION_ON_RETURN_ALONE", MODULE.validate(case))

    def test_local_collapse_cannot_erase_unactualized_representation(self):
        case = valid_case()
        case["collapse"]["retained_possibilities"] = []
        self.assertIn("UNCOLLAPSED_POSSIBILITY_ERASED:rep:unobserved", MODULE.validate(case))

    def test_claimed_traversal_needs_a_real_representation(self):
        case = valid_case()
        case["return"]["traversal_receipts"][0]["representation_id"] = "rep:invented"
        self.assertIn("TRAVERSAL_WITHOUT_REPRESENTATION:0", MODULE.validate(case))

    def test_original_source_is_not_mutated_by_validation(self):
        case = valid_case()
        original = copy.deepcopy(case)
        MODULE.validate(case)
        self.assertEqual(case, original)


if __name__ == "__main__":
    unittest.main()
