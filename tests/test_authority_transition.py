from __future__ import annotations

from dataclasses import replace
import unittest

from tools.authority_transition import (
    ADMISSIBLE,
    APPROVED,
    BOUNDED_REPEAT,
    CONDITIONAL,
    CONSUMED,
    DENIED,
    EXECUTION,
    INADMISSIBLE,
    INVALIDATED,
    PARTIALLY_CONSUMED,
    PENDING,
    PREPARATION,
    SINGLE,
    UNUSED,
    AuthorityTransitionError,
    ExecutionRequest,
    authorization_identity,
    classify_operation,
    consume_success,
    execution_eligible,
    invalidate,
    make_binding,
    make_execution_receipt,
    validate_binding,
    validate_execution,
)


def approved_binding(
    *,
    decision_state=APPROVED,
    transition_class="PUBLICATION",
    transition_target="report:alpha",
    object_id="room:alpha",
    room_revision_id="revision:1",
    room_state_root="state:1",
    authorized_view_root="view:1",
    evidence_boundary_reference="boundary:1",
    evidence_ceiling_reference="ceiling:1",
    approved_scope=("report:alpha",),
    mc_disposition=ADMISSIBLE,
    conditional_requirement_references=(),
    condition_satisfaction_references=(),
    execution_cardinality=SINGLE,
    maximum_execution_count=1,
    successful_execution_count=0,
    consumption_state=UNUSED,
    invalidation_reasons=(),
):
    return make_binding(
        human_gate_decision_id="human-gate:decision:1",
        decision_state=decision_state,
        transition_class=transition_class,
        transition_target=transition_target,
        object_id=object_id,
        room_revision_id=room_revision_id,
        room_state_root=room_state_root,
        authorized_view_root=authorized_view_root,
        evidence_boundary_reference=
            evidence_boundary_reference,
        evidence_ceiling_reference=
            evidence_ceiling_reference,
        approved_scope=approved_scope,
        mc_disposition=mc_disposition,
        conditional_requirement_references=
            conditional_requirement_references,
        condition_satisfaction_references=
            condition_satisfaction_references,
        execution_cardinality=
            execution_cardinality,
        maximum_execution_count=
            maximum_execution_count,
        successful_execution_count=
            successful_execution_count,
        consumption_state=
            consumption_state,
        invalidation_reasons=
            invalidation_reasons,
        provenance_route=(
            "raven:1",
            "human-gate:decision:1",
        ),
    )


def matching_request(
    binding,
    *,
    transition_class=None,
    transition_target=None,
    object_id=None,
    room_revision_id=None,
    room_state_root=None,
    authorized_view_root=None,
    evidence_boundary_reference=None,
    evidence_ceiling_reference=None,
    requested_scope=None,
    operation_label=EXECUTION,
    authority_bearing_effect=True,
):
    return ExecutionRequest(
        transition_class=(
            binding.transition_class
            if transition_class is None
            else transition_class
        ),
        transition_target=(
            binding.transition_target
            if transition_target is None
            else transition_target
        ),
        object_id=(
            binding.object_id
            if object_id is None
            else object_id
        ),
        room_revision_id=(
            binding.room_revision_id
            if room_revision_id is None
            else room_revision_id
        ),
        room_state_root=(
            binding.room_state_root
            if room_state_root is None
            else room_state_root
        ),
        authorized_view_root=(
            binding.authorized_view_root
            if authorized_view_root is None
            else authorized_view_root
        ),
        evidence_boundary_reference=(
            binding.evidence_boundary_reference
            if evidence_boundary_reference is None
            else evidence_boundary_reference
        ),
        evidence_ceiling_reference=(
            binding.evidence_ceiling_reference
            if evidence_ceiling_reference is None
            else evidence_ceiling_reference
        ),
        requested_scope=(
            binding.approved_scope
            if requested_scope is None
            else tuple(requested_scope)
        ),
        operation_label=operation_label,
        authority_bearing_effect=
            authority_bearing_effect,
        provenance_route=(
            "execution-request:1",
        ),
    )


class AuthorityTransitionTests(
    unittest.TestCase
):

    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    def test_valid_exact_binding(self):
        binding = approved_binding()

        self.assertEqual(
            validate_binding(binding),
            [],
        )

        request = matching_request(
            binding
        )

        self.assertEqual(
            validate_execution(
                binding,
                request,
            ),
            [],
        )

        self.assertTrue(
            execution_eligible(
                binding,
                request,
            )
        )

    def test_authorization_identity_is_deterministic(self):
        left = approved_binding()
        right = approved_binding()

        self.assertEqual(
            left.authorization_binding_id,
            right.authorization_binding_id,
        )

    def test_execution_receipt_is_bound_to_authorization(self):
        binding = approved_binding()
        request = matching_request(
            binding
        )

        receipt = make_execution_receipt(
            binding,
            request,
            execution_state="SUCCEEDED",
        )

        self.assertEqual(
            receipt.authorization_binding_id,
            binding.authorization_binding_id,
        )

        self.assertEqual(
            receipt.human_gate_decision_id,
            binding.human_gate_decision_id,
        )

    # --------------------------------------------------------
    # AR-009
    # MC admissibility != execution readiness
    # --------------------------------------------------------

    def test_ar009_admissible_without_approval_is_not_ready(self):
        binding = approved_binding(
            decision_state=PENDING,
            mc_disposition=ADMISSIBLE,
        )

        request = matching_request(
            binding
        )

        errors = validate_execution(
            binding,
            request,
        )

        self.assertIn(
            "Human Gate approval required",
            errors,
        )

        self.assertFalse(
            execution_eligible(
                binding,
                request,
            )
        )

    def test_ar009_denied_admissible_is_not_ready(self):
        binding = approved_binding(
            decision_state=DENIED,
            mc_disposition=ADMISSIBLE,
        )

        request = matching_request(
            binding
        )

        self.assertIn(
            "Human Gate approval required",
            validate_execution(
                binding,
                request,
            ),
        )

    # --------------------------------------------------------
    # AR-054 / AR-055
    # stale approval / approved state != executed state
    # --------------------------------------------------------

    def test_ar054_stale_state_root_blocks_execution(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            room_state_root="state:2",
        )

        self.assertIn(
            "Room state mismatch",
            validate_execution(
                binding,
                request,
            ),
        )

    def test_ar054_stale_revision_blocks_execution(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            room_revision_id="revision:2",
        )

        self.assertIn(
            "Room revision mismatch",
            validate_execution(
                binding,
                request,
            ),
        )

    def test_ar055_different_view_blocks_execution(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            authorized_view_root="view:2",
        )

        self.assertIn(
            "Authorized View mismatch",
            validate_execution(
                binding,
                request,
            ),
        )

    def test_ar055_different_room_blocks_execution(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            object_id="room:beta",
        )

        self.assertIn(
            "Room mismatch",
            validate_execution(
                binding,
                request,
            ),
        )

    def test_ar055_evidence_boundary_drift_blocks(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            evidence_boundary_reference=
                "boundary:2",
        )

        self.assertIn(
            "evidence boundary mismatch",
            validate_execution(
                binding,
                request,
            ),
        )

    def test_ar055_evidence_ceiling_drift_blocks(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            evidence_ceiling_reference=
                "ceiling:2",
        )

        self.assertIn(
            "evidence ceiling mismatch",
            validate_execution(
                binding,
                request,
            ),
        )

    # --------------------------------------------------------
    # AR-011
    # target substitution
    # --------------------------------------------------------

    def test_ar011_target_substitution_blocks(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            transition_target="report:beta",
        )

        self.assertIn(
            "transition target mismatch",
            validate_execution(
                binding,
                request,
            ),
        )

    # --------------------------------------------------------
    # AR-012
    # scope expansion
    # --------------------------------------------------------

    def test_ar012_scope_expansion_blocks(self):
        binding = approved_binding(
            approved_scope=(
                "report:alpha",
            )
        )

        request = matching_request(
            binding,
            requested_scope=(
                "report:alpha",
                "report:beta",
            ),
        )

        self.assertIn(
            "execution scope exceeds approval",
            validate_execution(
                binding,
                request,
            ),
        )

    def test_ar012_exact_scope_is_allowed(self):
        binding = approved_binding(
            approved_scope=(
                "report:alpha",
                "appendix:alpha",
            )
        )

        request = matching_request(
            binding,
            requested_scope=(
                "report:alpha",
                "appendix:alpha",
            ),
        )

        self.assertEqual(
            validate_execution(
                binding,
                request,
            ),
            [],
        )

    # --------------------------------------------------------
    # AR-010
    # approval reused for another transition
    # --------------------------------------------------------

    def test_ar010_transition_class_substitution_blocks(self):
        binding = approved_binding(
            transition_class="PUBLICATION"
        )

        request = matching_request(
            binding,
            transition_class=
                "EXTERNAL_DEPLOYMENT",
        )

        self.assertIn(
            "transition class mismatch",
            validate_execution(
                binding,
                request,
            ),
        )

    # --------------------------------------------------------
    # AR-059
    # execution disguised as preparation
    # --------------------------------------------------------

    def test_ar059_effect_controls_boundary_not_label(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            operation_label=PREPARATION,
            authority_bearing_effect=True,
        )

        self.assertEqual(
            classify_operation(request),
            EXECUTION,
        )

        self.assertIn(
            (
                "authority-bearing execution "
                "disguised as preparation"
            ),
            validate_execution(
                binding,
                request,
            ),
        )

    def test_ar059_real_preparation_is_not_execution(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            operation_label=PREPARATION,
            authority_bearing_effect=False,
        )

        self.assertEqual(
            classify_operation(request),
            PREPARATION,
        )

    # --------------------------------------------------------
    # AR-056
    # invalidated approval still executes
    # --------------------------------------------------------

    def test_ar056_invalidated_authorization_blocks(self):
        binding = approved_binding()

        binding = invalidate(
            binding,
            reasons=(
                "ROOM_STATE_CHANGED",
            ),
        )

        request = matching_request(
            binding
        )

        self.assertEqual(
            binding.consumption_state,
            INVALIDATED,
        )

        self.assertIn(
            (
                "invalidated authorization "
                "cannot execute"
            ),
            validate_execution(
                binding,
                request,
            ),
        )

    def test_ar056_invalidation_preserves_history(self):
        binding = approved_binding()

        invalid = invalidate(
            binding,
            reasons=(
                "VIEW_CHANGED",
            ),
        )

        self.assertEqual(
            invalid.human_gate_decision_id,
            binding.human_gate_decision_id,
        )

        self.assertEqual(
            invalid.invalidation_reasons,
            (
                "VIEW_CHANGED",
            ),
        )

        self.assertNotEqual(
            invalid.authorization_binding_id,
            binding.authorization_binding_id,
        )

    # --------------------------------------------------------
    # AR-057
    # operation executes more than once
    # --------------------------------------------------------

    def test_ar057_single_consumes_after_success(self):
        binding = approved_binding(
            execution_cardinality=SINGLE,
            maximum_execution_count=1,
        )

        consumed = consume_success(
            binding
        )

        self.assertEqual(
            consumed.successful_execution_count,
            1,
        )

        self.assertEqual(
            consumed.consumption_state,
            CONSUMED,
        )

    def test_ar057_single_cannot_execute_twice(self):
        binding = approved_binding()

        consumed = consume_success(
            binding
        )

        request = matching_request(
            consumed
        )

        errors = validate_execution(
            consumed,
            request,
        )

        self.assertIn(
            "consumed authorization cannot execute",
            errors,
        )

        self.assertIn(
            "execution cardinality exhausted",
            errors,
        )

    def test_ar057_consumed_cannot_be_consumed_again(self):
        binding = consume_success(
            approved_binding()
        )

        with self.assertRaises(
            AuthorityTransitionError
        ):
            consume_success(
                binding
            )

    def test_ar057_bounded_repeat_tracks_consumption(self):
        binding = approved_binding(
            execution_cardinality=
                BOUNDED_REPEAT,
            maximum_execution_count=2,
        )

        first = consume_success(
            binding
        )

        self.assertEqual(
            first.consumption_state,
            PARTIALLY_CONSUMED,
        )

        second = consume_success(
            first
        )

        self.assertEqual(
            second.consumption_state,
            CONSUMED,
        )

        self.assertEqual(
            second.successful_execution_count,
            2,
        )

    # --------------------------------------------------------
    # AR-058
    # actual/requested movement differs from approval
    # --------------------------------------------------------

    def test_ar058_target_difference_blocks(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            transition_target=
                "external:unapproved",
        )

        self.assertFalse(
            execution_eligible(
                binding,
                request,
            )
        )

    def test_ar058_multiple_binding_differences_accumulate(self):
        binding = approved_binding()

        request = matching_request(
            binding,
            transition_target="report:beta",
            object_id="room:beta",
            room_revision_id="revision:2",
            room_state_root="state:2",
            authorized_view_root="view:2",
            evidence_boundary_reference=
                "boundary:2",
            evidence_ceiling_reference=
                "ceiling:2",
            requested_scope=(
                "report:beta",
            ),
        )

        errors = validate_execution(
            binding,
            request,
        )

        for expected in (
            "transition target mismatch",
            "Room mismatch",
            "Room revision mismatch",
            "Room state mismatch",
            "Authorized View mismatch",
            "evidence boundary mismatch",
            "evidence ceiling mismatch",
            "execution scope exceeds approval",
        ):
            self.assertIn(
                expected,
                errors,
            )

    # --------------------------------------------------------
    # AR-051
    # CONDITIONAL != authorized without satisfaction
    # --------------------------------------------------------

    def test_ar051_conditional_without_satisfaction_blocks(self):
        binding = approved_binding(
            mc_disposition=CONDITIONAL,
            conditional_requirement_references=(
                "condition:a",
                "condition:b",
            ),
            condition_satisfaction_references=(
                "condition:a",
            ),
        )

        request = matching_request(
            binding
        )

        errors = validate_execution(
            binding,
            request,
        )

        self.assertIn(
            (
                "unsatisfied conditional "
                "requirements: condition:b"
            ),
            errors,
        )

    def test_ar051_conditional_with_all_satisfied_is_eligible(self):
        binding = approved_binding(
            mc_disposition=CONDITIONAL,
            conditional_requirement_references=(
                "condition:a",
                "condition:b",
            ),
            condition_satisfaction_references=(
                "condition:a",
                "condition:b",
            ),
        )

        request = matching_request(
            binding
        )

        self.assertEqual(
            validate_execution(
                binding,
                request,
            ),
            [],
        )

    def test_ar051_inadmissible_blocks_even_with_approval(self):
        binding = approved_binding(
            mc_disposition=INADMISSIBLE,
        )

        request = matching_request(
            binding
        )

        self.assertIn(
            "MC INADMISSIBLE blocks execution",
            validate_execution(
                binding,
                request,
            ),
        )

    # --------------------------------------------------------
    # Constitutional locks
    # --------------------------------------------------------

    def test_authority_remains_none(self):
        binding = approved_binding()

        self.assertEqual(
            binding.authority_state,
            "NONE",
        )

    def test_human_gate_remains_active(self):
        binding = approved_binding()

        self.assertEqual(
            binding.human_gate_state,
            "ACTIVE",
        )

    def test_binding_identity_detects_material_mutation(self):
        binding = approved_binding()

        mutated = replace(
            binding,
            transition_target=
                "report:beta",
            authorization_binding_id="",
        )

        mutated = replace(
            mutated,
            authorization_binding_id=
                authorization_identity(
                    mutated
                ),
        )

        self.assertNotEqual(
            binding.authorization_binding_id,
            mutated.authorization_binding_id,
        )


if __name__ == "__main__":
    unittest.main()
