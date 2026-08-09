from __future__ import annotations

import unittest

from tools.collision_boundary import (
    CLEAN,
    COLLISION,
    UNRESOLVED_CONTEXT,
)

from tools.evidence_ceiling import (
    ROW_LOCAL,
    GROUP_LOCAL,
    EVENT_CONTEXT,
    NATIVE_CONTEXT,
    OBSERVED,
    INFERRED,
    UNKNOWN,
    ADMISSIBLE,
    CONDITIONAL,
    INADMISSIBLE,
    UNRESOLVED,
    AUTHORITY_STATE,
    HUMAN_GATE_STATE,
    evaluate_claim,
    validate_epistemic_transition,
    validate_scope_promotion,
    confidence_changes_evidence_scope,
)


def evaluate(
    *,
    epistemic_class=OBSERVED,
    available_scope=ROW_LOCAL,
    required_scope=ROW_LOCAL,
    collision=CLEAN,
    confidence=None,
    missing=(),
):
    return evaluate_claim(
        claim_id="claim:test",
        claim_text="bounded test claim",
        epistemic_class=epistemic_class,
        available_evidence_scope=available_scope,
        required_evidence_scope=required_scope,
        evidence_boundary_reference="boundary:test",
        evidence_ceiling_reference="ceiling:test",
        evidence_references=("evidence:test",),
        missing_evidence_requirements=missing,
        collision_disposition=collision,
        confidence=confidence,
        provenance_route=("origin:test",),
    )


class EvidenceCeilingTests(unittest.TestCase):

    def test_row_local_observation_admissible(self):
        result = evaluate()

        self.assertEqual(
            result.claim_disposition,
            ADMISSIBLE,
        )

    def test_group_claim_with_row_only_evidence_conditional(self):
        result = evaluate(
            epistemic_class=INFERRED,
            required_scope=GROUP_LOCAL,
            missing=("group_relationship",),
        )

        self.assertEqual(
            result.claim_disposition,
            CONDITIONAL,
        )

    def test_event_claim_with_row_only_evidence_conditional(self):
        result = evaluate(
            epistemic_class=INFERRED,
            required_scope=EVENT_CONTEXT,
            missing=("event_window",),
        )

        self.assertEqual(
            result.claim_disposition,
            CONDITIONAL,
        )

    def test_native_claim_with_row_only_evidence_conditional(self):
        result = evaluate(
            epistemic_class=INFERRED,
            required_scope=NATIVE_CONTEXT,
            missing=("pcap_linkage",),
        )

        self.assertEqual(
            result.claim_disposition,
            CONDITIONAL,
        )

    def test_unknown_remains_unresolved(self):
        result = evaluate(
            epistemic_class=UNKNOWN,
        )

        self.assertEqual(
            result.claim_disposition,
            UNRESOLVED,
        )

    def test_unresolved_collision_context_remains_unresolved(self):
        result = evaluate(
            collision=UNRESOLVED_CONTEXT,
        )

        self.assertEqual(
            result.claim_disposition,
            UNRESOLVED,
        )

    def test_collision_row_local_observation_can_remain_observed(self):
        result = evaluate(
            collision=COLLISION,
            required_scope=ROW_LOCAL,
        )

        self.assertEqual(
            result.claim_disposition,
            ADMISSIBLE,
        )

    def test_collision_cannot_establish_event_context(self):
        result = evaluate(
            epistemic_class=OBSERVED,
            collision=COLLISION,
            available_scope=GROUP_LOCAL,
            required_scope=EVENT_CONTEXT,
        )

        self.assertEqual(
            result.claim_disposition,
            INADMISSIBLE,
        )

        self.assertIn(
            "COLLISION_CANNOT_ESTABLISH_EVENT_CONTEXT",
            result.disposition_reasons,
        )

    def test_high_confidence_does_not_raise_scope(self):
        scope = confidence_changes_evidence_scope(
            available_scope=ROW_LOCAL,
            confidence_before=0.50,
            confidence_after=0.999999,
        )

        self.assertEqual(
            scope,
            ROW_LOCAL,
        )

    def test_999999_confidence_does_not_make_c2_admissible(self):
        result = evaluate_claim(
            claim_id="claim:c2",
            claim_text=(
                "UDP 5353 collision residue establishes "
                "command-and-control activity"
            ),
            epistemic_class=INFERRED,
            available_evidence_scope=ROW_LOCAL,
            required_evidence_scope=NATIVE_CONTEXT,
            evidence_boundary_reference=
                "boundary:rt-iot2022:row-features",
            evidence_ceiling_reference=
                "ceiling:protocol-instruction-residue",
            evidence_references=(
                "collision:udp-5353",
            ),
            missing_evidence_requirements=(
                "native_packet_context",
                "event_window",
                "process_lineage",
            ),
            collision_disposition=COLLISION,
            confidence=0.999999,
            provenance_route=(
                "rt-iot2022",
                "collision-boundary",
            ),
        )

        self.assertNotEqual(
            result.claim_disposition,
            ADMISSIBLE,
        )

        self.assertIn(
            result.claim_disposition,
            {
                CONDITIONAL,
                INADMISSIBLE,
            },
        )

    def test_confidence_zero_and_one_same_scope(self):
        low = confidence_changes_evidence_scope(
            available_scope=GROUP_LOCAL,
            confidence_before=0.0,
            confidence_after=0.0,
        )

        high = confidence_changes_evidence_scope(
            available_scope=GROUP_LOCAL,
            confidence_before=1.0,
            confidence_after=1.0,
        )

        self.assertEqual(low, GROUP_LOCAL)
        self.assertEqual(high, GROUP_LOCAL)

    def test_invalid_confidence_above_one_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(
                confidence=1.000001,
            )

    def test_invalid_confidence_below_zero_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(
                confidence=-0.000001,
            )

    def test_boolean_confidence_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(
                confidence=True,
            )

    def test_epistemic_promotion_without_evidence_blocked(self):
        self.assertFalse(
            validate_epistemic_transition(
                prior_class=UNKNOWN,
                requested_class=INFERRED,
            )
        )

    def test_unknown_to_observed_without_evidence_blocked(self):
        self.assertFalse(
            validate_epistemic_transition(
                prior_class=UNKNOWN,
                requested_class=OBSERVED,
            )
        )

    def test_inferred_to_observed_without_evidence_blocked(self):
        self.assertFalse(
            validate_epistemic_transition(
                prior_class=INFERRED,
                requested_class=OBSERVED,
            )
        )

    def test_epistemic_promotion_with_new_evidence_permitted(self):
        self.assertTrue(
            validate_epistemic_transition(
                prior_class=INFERRED,
                requested_class=OBSERVED,
                new_evidence_references=(
                    "native:packet:1",
                ),
            )
        )

    def test_scope_promotion_without_evidence_blocked(self):
        self.assertFalse(
            validate_scope_promotion(
                prior_scope=ROW_LOCAL,
                requested_scope=EVENT_CONTEXT,
            )
        )

    def test_scope_promotion_with_new_evidence_permitted(self):
        self.assertTrue(
            validate_scope_promotion(
                prior_scope=ROW_LOCAL,
                requested_scope=EVENT_CONTEXT,
                new_evidence_references=(
                    "event-window:1",
                ),
            )
        )

    def test_scope_demotion_needs_no_new_evidence(self):
        self.assertTrue(
            validate_scope_promotion(
                prior_scope=NATIVE_CONTEXT,
                requested_scope=GROUP_LOCAL,
            )
        )

    def test_missing_boundary_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_claim(
                claim_id="claim:test",
                claim_text="test",
                epistemic_class=OBSERVED,
                available_evidence_scope=ROW_LOCAL,
                required_evidence_scope=ROW_LOCAL,
                evidence_boundary_reference="",
                evidence_ceiling_reference="ceiling:test",
                evidence_references=("evidence:test",),
                collision_disposition=CLEAN,
                provenance_route=("origin:test",),
            )

    def test_missing_ceiling_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_claim(
                claim_id="claim:test",
                claim_text="test",
                epistemic_class=OBSERVED,
                available_evidence_scope=ROW_LOCAL,
                required_evidence_scope=ROW_LOCAL,
                evidence_boundary_reference="boundary:test",
                evidence_ceiling_reference="",
                evidence_references=("evidence:test",),
                collision_disposition=CLEAN,
                provenance_route=("origin:test",),
            )

    def test_missing_provenance_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_claim(
                claim_id="claim:test",
                claim_text="test",
                epistemic_class=OBSERVED,
                available_evidence_scope=ROW_LOCAL,
                required_evidence_scope=ROW_LOCAL,
                evidence_boundary_reference="boundary:test",
                evidence_ceiling_reference="ceiling:test",
                evidence_references=("evidence:test",),
                collision_disposition=CLEAN,
                provenance_route=(),
            )

    def test_missing_evidence_is_explicit(self):
        result = evaluate(
            epistemic_class=INFERRED,
            required_scope=EVENT_CONTEXT,
            missing=(
                "timestamp",
                "event_window",
            ),
        )

        self.assertEqual(
            result.missing_evidence_requirements,
            (
                "event_window",
                "timestamp",
            ),
        )

    def test_authority_remains_none(self):
        self.assertEqual(
            AUTHORITY_STATE,
            "NONE",
        )

    def test_human_gate_remains_active(self):
        self.assertEqual(
            HUMAN_GATE_STATE,
            "ACTIVE",
        )


if __name__ == "__main__":
    unittest.main()
