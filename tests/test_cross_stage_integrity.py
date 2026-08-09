from dataclasses import replace
import unittest

from tools.cross_stage_integrity import (
    ADMISSIBLE,
    BLOCKED,
    CONDITIONAL,
    VALID,
    make_valid_pipeline,
    validate_composition,
)


class CrossStageSemanticIntegrityTests(
    unittest.TestCase
):

    def setUp(self):
        self.pipeline = list(
            make_valid_pipeline()
        )

    def run_pipeline(self):
        return validate_composition(
            *self.pipeline
        )

    def assertBlockedBy(self, reason):
        result = self.run_pipeline()

        self.assertEqual(
            result.composition_disposition,
            BLOCKED,
        )

        self.assertIn(
            reason,
            result.failure_reasons,
        )

        self.assertIn(
            "GLOBAL_STATE_IMPOSSIBLE",
            result.failure_reasons,
        )

    def test_valid_composition(self):
        result = self.run_pipeline()

        self.assertEqual(
            result.composition_disposition,
            VALID,
        )

        self.assertEqual(
            result.failure_reasons,
            (),
        )

    # AR-046
    def test_ar046_ccr_cannot_commit_unemitted_candidate(self):
        self.pipeline[1] = replace(
            self.pipeline[1],
            emitted_candidates=(
                "candidate:a",
                "candidate:b",
                "candidate:invented",
            ),
        )

        self.assertBlockedBy(
            "PMC_CANDIDATE_NOT_EMITTED"
        )

    # AR-047
    def test_ar047_rejected_candidate_cannot_disappear(self):
        self.pipeline[1] = replace(
            self.pipeline[1],
            rejected_candidates=(),
        )

        self.assertBlockedBy(
            "REJECTED_CANDIDATE_LOST"
        )

    # AR-048
    def test_ar048_candidate_order_cannot_change(self):
        self.pipeline[1] = replace(
            self.pipeline[1],
            candidate_order=(
                "candidate:b",
                "candidate:a",
            ),
        )

        self.assertBlockedBy(
            "CANDIDATE_ORDER_CHANGED"
        )

    def test_ar048_uncertainty_cannot_disappear_at_ccr(self):
        self.pipeline[1] = replace(
            self.pipeline[1],
            uncertainty_references=(),
        )

        self.assertBlockedBy(
            "UNCERTAINTY_ERASED"
        )

    # AR-049
    def test_ar049_mc_cannot_invent_governance_constraint(self):
        self.pipeline[2] = replace(
            self.pipeline[2],
            governance_constraint_references=(
                "governance:1",
                "governance:invented",
            ),
        )

        self.assertBlockedBy(
            "GOVERNANCE_CONSTRAINT_INVENTED"
        )

    def test_ar049_mc_cannot_drop_governance_constraint(self):
        self.pipeline[2] = replace(
            self.pipeline[2],
            governance_constraint_references=(),
        )

        self.assertBlockedBy(
            "GOVERNANCE_CONSTRAINT_DROPPED"
        )

    # AR-050
    def test_ar050_mc_cannot_raise_evidence_ceiling(self):
        self.pipeline[2] = replace(
            self.pipeline[2],
            evidence_ceiling=4,
        )

        self.assertBlockedBy(
            "EVIDENCE_CEILING_RAISED"
        )

    # AR-051
    def test_ar051_unsatisfied_conditional_cannot_become_admissible(self):
        self.pipeline[2] = replace(
            self.pipeline[2],
            mc_disposition=CONDITIONAL,
            conditional_requirement_references=(
                "condition:1",
            ),
            condition_satisfaction_references=(),
        )

        self.pipeline[3] = replace(
            self.pipeline[3],
            mc_disposition=ADMISSIBLE,
        )

        self.assertBlockedBy(
            "CONDITIONAL_STATE_PROMOTED"
        )

    def test_ar051_satisfied_conditional_may_proceed(self):
        self.pipeline[2] = replace(
            self.pipeline[2],
            mc_disposition=CONDITIONAL,
            conditional_requirement_references=(
                "condition:1",
            ),
            condition_satisfaction_references=(
                "condition:1",
            ),
        )

        self.pipeline[3] = replace(
            self.pipeline[3],
            mc_disposition=ADMISSIBLE,
        )

        result = self.run_pipeline()

        self.assertNotIn(
            "CONDITIONAL_STATE_PROMOTED",
            result.failure_reasons,
        )

    # AR-052
    def test_ar052_raven_cannot_suppress_uncertainty(self):
        self.pipeline[3] = replace(
            self.pipeline[3],
            uncertainty_references=(),
        )

        self.assertBlockedBy(
            "UNCERTAINTY_ERASED"
        )

    def test_ar052_raven_cannot_suppress_material_unknown(self):
        self.pipeline[3] = replace(
            self.pipeline[3],
            material_unknown_references=(),
        )

        self.assertBlockedBy(
            "MATERIAL_UNKNOWN_SUPPRESSED"
        )

    # AR-053
    def test_ar053_raven_cannot_strengthen_claim(self):
        self.pipeline[3] = replace(
            self.pipeline[3],
            claim_strength=3,
        )

        self.assertBlockedBy(
            "CLAIM_STRENGTH_INCREASED"
        )

    # AR-063
    def test_ar063_cross_object_drift_blocks_composition(self):
        self.pipeline[3] = replace(
            self.pipeline[3],
            object_id="room:other",
        )

        self.assertBlockedBy(
            "CROSS_OBJECT_CONTAMINATION"
        )

    def test_ar063_revision_drift_blocks_composition(self):
        self.pipeline[2] = replace(
            self.pipeline[2],
            room_revision_id="revision:other",
        )

        self.assertBlockedBy(
            "OBJECT_IDENTITY_CHANGED"
        )

    # AR-064
    def test_ar064_all_local_stages_can_pass_while_composition_fails(self):
        self.assertTrue(
            all(
                state.local_valid
                for state in self.pipeline
            )
        )

        self.pipeline[3] = replace(
            self.pipeline[3],
            claim_strength=3,
        )

        self.assertTrue(
            all(
                state.local_valid
                for state in self.pipeline
            )
        )

        result = self.run_pipeline()

        self.assertEqual(
            result.composition_disposition,
            BLOCKED,
        )

        self.assertIn(
            "CLAIM_STRENGTH_INCREASED",
            result.failure_reasons,
        )

        self.assertIn(
            "GLOBAL_STATE_IMPOSSIBLE",
            result.failure_reasons,
        )

    def test_ar064_multiple_local_semantic_failures_accumulate(self):
        self.pipeline[1] = replace(
            self.pipeline[1],
            rejected_candidates=(),
        )

        self.pipeline[2] = replace(
            self.pipeline[2],
            evidence_ceiling=4,
        )

        self.pipeline[3] = replace(
            self.pipeline[3],
            material_unknown_references=(),
            claim_strength=3,
        )

        result = self.run_pipeline()

        self.assertEqual(
            result.composition_disposition,
            BLOCKED,
        )

        for reason in (
            "REJECTED_CANDIDATE_LOST",
            "EVIDENCE_CEILING_RAISED",
            "MATERIAL_UNKNOWN_SUPPRESSED",
            "CLAIM_STRENGTH_INCREASED",
            "GLOBAL_STATE_IMPOSSIBLE",
        ):
            self.assertIn(
                reason,
                result.failure_reasons,
            )

    def test_lineage_break_blocks_composition(self):
        self.pipeline[2] = replace(
            self.pipeline[2],
            lineage_references=(),
        )

        self.assertBlockedBy(
            "LINEAGE_BROKEN"
        )

    def test_provenance_break_blocks_composition(self):
        self.pipeline[4] = replace(
            self.pipeline[4],
            provenance_route=(),
        )

        self.assertBlockedBy(
            "PROVENANCE_BROKEN"
        )

    def test_boundary_drift_blocks_composition(self):
        self.pipeline[3] = replace(
            self.pipeline[3],
            evidence_boundary_reference=(
                "boundary:expanded"
            ),
        )

        self.assertBlockedBy(
            "EVIDENCE_BOUNDARY_CHANGED"
        )

    def test_composition_identity_is_deterministic(self):
        first = self.run_pipeline()
        second = self.run_pipeline()

        self.assertEqual(
            first.composition_id,
            second.composition_id,
        )


if __name__ == "__main__":
    unittest.main()
