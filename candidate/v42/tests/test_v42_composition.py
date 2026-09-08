import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import generate_artifacts
import validate_v42


class CandidateV42CompositionTests(unittest.TestCase):
    def setUp(self):
        self.pipeline = generate_artifacts.positive_pipeline()

    def replace(self, kind, **updates):
        for i, item in enumerate(self.pipeline):
            if item["record_type"] == kind:
                value = copy.deepcopy(item); value.update(updates); value["record_id"] = validate_v42.record_id(value); self.pipeline[i] = value; return
        raise AssertionError(kind)

    def errors(self): return validate_v42.validate_pipeline(self.pipeline)

    def test_full_pipeline(self): self.assertEqual([], self.errors())

    def test_one_governed_object(self):
        self.replace("return_record", object_id=generate_artifacts.ref("other"), returned_object_id=generate_artifacts.ref("other"))
        self.assertIn("GOVERNED_OBJECT_IDENTITY_DIVERGED", self.errors())

    def test_harmony_cannot_raise_ceiling(self):
        self.replace("harmony_interpretation", evidence_ceiling="TRUTH")
        self.assertIn("HARMONY_EVIDENCE_CEILING_RAISED", self.errors())

    def test_router_cannot_invent_mission(self):
        self.replace("pressure_route", mission_question="A different question")
        self.assertIn("ROUTER_INVENTED_MISSION", self.errors())

    def test_carrier_substitution(self):
        self.replace("execution_trace", carrier_id="goblin:other")
        self.assertIn("CARRIER_SUBSTITUTED", self.errors())

    def test_return_object_replacement(self):
        self.replace("return_record", returned_object_id=generate_artifacts.ref("replacement"), object_continuity="BROKEN")
        self.assertIn("OBJECT_REPLACED_ON_RETURN", self.errors())

    def test_lossless_closure_requires_every_record(self):
        closure = next(r for r in self.pipeline if r["record_type"] == "aggregate_closure")
        self.replace("aggregate_closure", stage_records=closure["stage_records"][:-1])
        self.assertIn("LOSSLESS_CLOSURE_DROPPED_RECORD", self.errors())

    def test_remove_each_control_fails_closed(self):
        for kind in generate_artifacts.RECORDS:
            reduced = [r for r in self.pipeline if r["record_type"] != kind]
            self.assertTrue(validate_v42.validate_pipeline(reduced), kind)


if __name__ == "__main__": unittest.main()

