from __future__ import annotations

import unittest

from tools.validate_human_gate_authority_semantics import (
    _baseline,
    human_gate_authority_semantic_transition_valid,
    validate_human_gate_authority_transition,
)


class AC11HumanGateAuthoritySemanticTests(unittest.TestCase):

    def setUp(self):
        self.source = _baseline()

    def approved(self):
        state = dict(self.source)
        state["human_gate_decision"] = "APPROVED"
        state["human_decision_ref"] = "human:ac11:approval:a"
        return state

    def reasons(self, downstream):
        return validate_human_gate_authority_transition(
            self.source,
            downstream,
        )

    # ---------------------------------------------------------
    # Constitutional invariants
    # ---------------------------------------------------------

    def test_bounded_approval_is_valid(self):
        downstream = self.approved()

        self.assertEqual(
            self.reasons(downstream),
            (),
        )

        self.assertTrue(
            human_gate_authority_semantic_transition_valid(
                self.source,
                downstream,
            )
        )

    def test_authority_remains_none(self):
        downstream = dict(self.source)
        downstream["authority_state"] = "FULL"

        self.assertIn(
            "AUTHORITY_PROMOTED",
            self.reasons(downstream),
        )

    def test_human_gate_remains_active(self):
        downstream = dict(self.source)
        downstream["human_gate_state"] = "DISABLED"

        self.assertIn(
            "HUMAN_GATE_DISABLED",
            self.reasons(downstream),
        )

    # ---------------------------------------------------------
    # Human decision attribution
    # ---------------------------------------------------------

    def test_approved_requires_human_decision_reference(self):
        downstream = dict(self.source)
        downstream["human_gate_decision"] = "APPROVED"
        downstream["human_decision_ref"] = None

        self.assertIn(
            "HUMAN_DECISION_REFERENCE_MISSING",
            self.reasons(downstream),
        )

    def test_unknown_authority_bearing_decision_is_blocked(self):
        downstream = dict(self.source)
        downstream["human_gate_decision"] = "IMPLIED"

        self.assertIn(
            "HUMAN_GATE_DECISION_MISSING",
            self.reasons(downstream),
        )

    # ---------------------------------------------------------
    # Approval != execution
    # ---------------------------------------------------------

    def test_approval_does_not_execute(self):
        downstream = self.approved()
        downstream["execution_state"] = "EXECUTED"

        self.assertIn(
            "APPROVAL_PROMOTED_TO_EXECUTION",
            self.reasons(downstream),
        )

    def test_approval_does_not_publish(self):
        downstream = self.approved()
        downstream["publication_state"] = "PUBLISHED"

        self.assertIn(
            "APPROVAL_PROMOTED_TO_PUBLICATION",
            self.reasons(downstream),
        )

    def test_approval_does_not_mutate_canonical_state(self):
        downstream = self.approved()
        downstream["canonical_mutation_state"] = "MUTATED"

        self.assertIn(
            "CANONICAL_MUTATION_INFERRED",
            self.reasons(downstream),
        )

    # ---------------------------------------------------------
    # Evidence boundary / ceiling preservation
    # ---------------------------------------------------------

    def test_approval_does_not_expand_evidence_boundary(self):
        downstream = self.approved()
        downstream["evidence_boundary_ref"] = "boundary:expanded"

        self.assertIn(
            "EVIDENCE_BOUNDARY_CHANGED",
            self.reasons(downstream),
        )

    def test_approval_does_not_raise_evidence_ceiling(self):
        downstream = self.approved()
        downstream["evidence_ceiling_ref"] = "ceiling:raised"

        self.assertIn(
            "EVIDENCE_CEILING_CHANGED",
            self.reasons(downstream),
        )

    # ---------------------------------------------------------
    # MC preservation
    # ---------------------------------------------------------

    def test_mc_admissibility_cannot_be_rewritten(self):
        downstream = dict(self.source)
        downstream["mc_admissibility"] = "CONDITIONAL"

        self.assertIn(
            "MC_ADMISSIBILITY_REWRITTEN",
            self.reasons(downstream),
        )

    def test_inadmissible_cannot_be_approved(self):
        downstream = self.approved()
        downstream["mc_admissibility"] = "INADMISSIBLE"

        reasons = self.reasons(downstream)

        self.assertIn(
            "INADMISSIBLE_STATE_APPROVED",
            reasons,
        )

        self.assertIn(
            "MC_ADMISSIBILITY_REWRITTEN",
            reasons,
        )

    def test_conditional_cannot_become_unconditional_approval(self):
        downstream = self.approved()
        downstream["mc_admissibility"] = "CONDITIONAL"

        self.assertIn(
            "CONDITIONAL_STATE_APPROVED_WITHOUT_EVIDENCE",
            self.reasons(downstream),
        )

    # ---------------------------------------------------------
    # Claim authority
    # ---------------------------------------------------------

    def test_human_approval_does_not_create_certification(self):
        downstream = self.approved()
        downstream["claim_authority_state"] = "CERTIFICATION"

        self.assertIn(
            "CLAIM_AUTHORITY_INFERRED",
            self.reasons(downstream),
        )

    def test_human_approval_does_not_create_compliance_truth(self):
        downstream = self.approved()
        downstream["claim_authority_state"] = "COMPLIANCE"

        self.assertIn(
            "CLAIM_AUTHORITY_INFERRED",
            self.reasons(downstream),
        )

    # ---------------------------------------------------------
    # System population
    # ---------------------------------------------------------

    def test_publication_approval_does_not_populate_system(self):
        downstream = self.approved()
        downstream["system_population_state"] = "POPULATED"

        self.assertIn(
            "SYSTEM_POPULATION_INFERRED",
            self.reasons(downstream),
        )

    # ---------------------------------------------------------
    # Approval binding
    # ---------------------------------------------------------

    def test_approval_requires_transition_target(self):
        downstream = self.approved()
        downstream["transition_target"] = None

        self.assertIn(
            "APPROVAL_BINDING_MISSING:transition_target",
            self.reasons(downstream),
        )

    def test_approval_requires_requested_scope(self):
        downstream = self.approved()
        downstream["requested_scope"] = None

        self.assertIn(
            "APPROVAL_BINDING_MISSING:requested_scope",
            self.reasons(downstream),
        )

    def test_approval_requires_room_identity(self):
        downstream = self.approved()
        downstream["room_object_id"] = None

        self.assertIn(
            "APPROVAL_BINDING_MISSING:room_object_id",
            self.reasons(downstream),
        )

    def test_approval_requires_authorized_view(self):
        downstream = self.approved()
        downstream["authorized_view_root"] = None

        self.assertIn(
            "APPROVAL_BINDING_MISSING:authorized_view_root",
            self.reasons(downstream),
        )

    # ---------------------------------------------------------
    # Prior approval != standing approval
    # ---------------------------------------------------------

    def test_prior_approval_not_reusable_after_target_change(self):
        source = self.approved()
        downstream = dict(source)
        downstream["transition_target"] = "report:ac11:b"

        reasons = validate_human_gate_authority_transition(
            source,
            downstream,
        )

        self.assertIn(
            "PRIOR_APPROVAL_REUSED_AFTER_CHANGE",
            reasons,
        )

    def test_prior_approval_not_reusable_after_scope_change(self):
        source = self.approved()
        downstream = dict(source)
        downstream["requested_scope"] = "different-scope"

        reasons = validate_human_gate_authority_transition(
            source,
            downstream,
        )

        self.assertIn(
            "PRIOR_APPROVAL_REUSED_AFTER_CHANGE",
            reasons,
        )

    def test_prior_approval_not_reusable_after_room_revision_change(self):
        source = self.approved()
        downstream = dict(source)
        downstream["room_revision_id"] = "revision:ac11:b"

        reasons = validate_human_gate_authority_transition(
            source,
            downstream,
        )

        self.assertIn(
            "PRIOR_APPROVAL_REUSED_AFTER_CHANGE",
            reasons,
        )

    def test_prior_approval_not_reusable_after_evidence_change(self):
        source = self.approved()
        downstream = dict(source)
        downstream["evidence_ceiling_ref"] = "ceiling:ac11:b"

        reasons = validate_human_gate_authority_transition(
            source,
            downstream,
        )

        self.assertIn(
            "PRIOR_APPROVAL_REUSED_AFTER_CHANGE",
            reasons,
        )


if __name__ == "__main__":
    unittest.main()
