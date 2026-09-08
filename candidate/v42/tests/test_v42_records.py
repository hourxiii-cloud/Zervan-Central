import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import generate_artifacts
import validate_v42


class CandidateV42RecordTests(unittest.TestCase):
    def setUp(self):
        self.records = generate_artifacts.positive_pipeline()
        self.by_type = {r["record_type"]: r for r in self.records}

    def mutate(self, kind, **updates):
        item = copy.deepcopy(self.by_type[kind]); item.update(updates)
        item["record_id"] = validate_v42.record_id(item)
        return item

    def assertRejected(self, record, reason):
        self.assertIn(reason, validate_v42.validate_record(record))

    def test_every_positive_record(self):
        for record in self.records:
            self.assertEqual([], validate_v42.validate_record(record), record["record_type"])

    def test_authority_none(self):
        self.assertRejected(self.mutate("trigger_evaluation", authority_state="SYSTEM"), "CONTROL_STATE_INVALID:authority_state")

    def test_harmony_cannot_schedule(self):
        self.assertRejected(self.mutate("harmony_interpretation", provocation_authority="SCHEDULER"), "HARMONY_SCHEDULER_FORBIDDEN")

    def test_pseudo_trigger_rejected(self):
        self.assertRejected(self.mutate("trigger_evaluation", expected_discriminating_value="INACTIVITY"), "PSEUDO_TRIGGER_ELIGIBLE")

    def test_platoon_requires_question_geometry(self):
        self.assertRejected(self.mutate("pressure_route", selected_force="PLATOON"), "FORCE_ESCALATION_WITHOUT_CAPABILITY_GAP")

    def test_animalkingdom_requires_canonical_synthetic_work(self):
        self.assertRejected(self.mutate("pressure_route", selected_force="ANIMALKINGDOM"), "ANIMALKINGDOM_CONTRACT_MISMATCH")

    def test_animalkingdom_rejects_candidate_input(self):
        self.assertRejected(self.mutate("carrier_admissibility", carrier_id="AnimalKingdom:v41", input_class="CANDIDATE_READ_ONLY"), "ANIMALKINGDOM_INPUT_INADMISSIBLE")

    def test_external_action_rejected(self):
        self.assertRejected(self.mutate("execution_authorization", external_action="ENABLED"), "EXTERNAL_ACTION_FORBIDDEN")

    def test_in_run_expansion_rejected(self):
        self.assertRejected(self.mutate("execution_trace", steps=["inspect", "expand-mission"]), "IN_RUN_ENVELOPE_VIOLATION")

    def test_contamination_cannot_be_laundered(self):
        record = self.mutate("termination_record", contamination_status="CONTAMINATED", object_evidence_admissibility="QUALIFICATION_REQUIRED")
        self.assertRejected(record, "CONTAMINATED_OBJECT_EVIDENCE_LAUNDERED")

    def test_replacement_is_not_return(self):
        record = self.mutate("return_record", returned_object_id=generate_artifacts.ref("replacement"))
        self.assertRejected(record, "FALSE_OBJECT_RESTORATION")

    def test_truth_promotion_rejected(self):
        self.assertRejected(self.mutate("evidence_qualification", disposition="TRUTH"), "FALSE_RESULT_PROMOTION")

    def test_standing_delegation_rejected(self):
        self.assertRejected(self.mutate("delegation_envelope", execution_limit=1001), "STANDING_DELEGATION_FORBIDDEN")

    def test_lossy_recollapse_rejected(self):
        self.assertRejected(self.mutate("aggregate_closure", lossless_recollapse=False), "LOSSLESS_RECOLLAPSE_NOT_PASSED")


if __name__ == "__main__": unittest.main()

