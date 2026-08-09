from __future__ import annotations

from dataclasses import replace
import unittest

from tools.semantic_state import (
    ACTIVE,
    APPROVED,
    AVAILABLE,
    BLOCKED,
    COMPLETE,
    CONTRADICTED,
    DENIED,
    EXISTENCE_ONLY,
    FULL,
    INACTIVE,
    KNOWN,
    KNOWN_ABSENT,
    KNOWN_PRESENT,
    NOT_REQUIRED,
    OMITTED_BY_VIEW,
    PARTIAL,
    PENDING,
    REDACTED,
    RESTRICTED,
    SUMMARY,
    TOPOLOGY_ABSENT,
    TOPOLOGY_KNOWN,
    TOPOLOGY_RESTRICTED,
    TOPOLOGY_UNRESOLVED,
    UNAVAILABLE,
    UNHYDRATED,
    UNKNOWN,
    UNRESOLVED,
    UNRESOLVED_EXISTENCE,
    SemanticStateError,
    changed_dimensions,
    make_coordinate,
    make_transition,
    semantic_state_identity,
    validate_coordinate,
    validate_transition,
)


def restricted_coordinate():
    return make_coordinate(
        subject_reference="object:restricted:a",
        existence_state=KNOWN_PRESENT,
        epistemic_state=KNOWN,
        accessibility_state=RESTRICTED,
        topology_state=TOPOLOGY_RESTRICTED,
        hydration_state=PARTIAL,
        hydration_boundary_reference="hydration:a",
        operational_state=INACTIVE,
        decision_state=PENDING,
        representation_state=EXISTENCE_ONLY,
        evidence_boundary_reference="boundary:a",
        evidence_ceiling_reference="ceiling:a",
        restriction_references=(
            "restriction:a",
        ),
        unresolved_references=(
            "hydration:unresolved:a",
        ),
        provenance_route=(
            "origin:a",
            "state:a",
        ),
    )


def unresolved_coordinate():
    return make_coordinate(
        subject_reference="object:unknown:a",
        existence_state=UNRESOLVED_EXISTENCE,
        epistemic_state=UNKNOWN,
        accessibility_state=UNAVAILABLE,
        topology_state=TOPOLOGY_UNRESOLVED,
        hydration_state=UNHYDRATED,
        hydration_boundary_reference="hydration:a",
        operational_state=BLOCKED,
        decision_state=PENDING,
        representation_state=SUMMARY,
        evidence_boundary_reference="boundary:a",
        evidence_ceiling_reference="ceiling:a",
        unresolved_references=(
            "existence:unknown:a",
            "topology:unknown:a",
        ),
        provenance_route=(
            "origin:a",
            "state:a",
        ),
    )


class SemanticStateGeometryTests(
    unittest.TestCase
):

    # --------------------------------------------------------
    # Baseline / identity
    # --------------------------------------------------------

    def test_valid_restricted_coordinate(self):
        coordinate = restricted_coordinate()

        self.assertEqual(
            validate_coordinate(coordinate),
            [],
        )

    def test_identity_is_deterministic(self):
        left = restricted_coordinate()
        right = restricted_coordinate()

        self.assertEqual(
            left.semantic_state_id,
            right.semantic_state_id,
        )

    def test_material_dimension_change_changes_identity(self):
        prior = restricted_coordinate()

        changed = replace(
            prior,
            representation_state=REDACTED,
            semantic_state_id="",
        )

        changed = replace(
            changed,
            semantic_state_id=
                semantic_state_identity(
                    changed
                ),
        )

        self.assertNotEqual(
            prior.semantic_state_id,
            changed.semantic_state_id,
        )

    def test_changed_dimensions_are_explicit(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=REDACTED,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        self.assertEqual(
            changed_dimensions(
                prior,
                result,
            ),
            (
                "representation_state",
            ),
        )

    # --------------------------------------------------------
    # AR-028
    # UNKNOWN / ABSENT / RESTRICTED / DENIED / BLOCKED
    # must remain machine-distinct.
    # --------------------------------------------------------

    def test_ar028_unknown_not_absent(self):
        prior = unresolved_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=KNOWN_ABSENT,
            epistemic_state=UNKNOWN,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=
                prior.representation_state,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "existence_state",
            ),
        )

        self.assertIn(
            (
                "existence resolution requires "
                "attributable evidence"
            ),
            errors,
        )

    def test_ar028_restricted_not_absent(self):
        prior = restricted_coordinate()

        with self.assertRaises(
            SemanticStateError
        ):
            make_coordinate(
                subject_reference=
                    prior.subject_reference,
                existence_state=KNOWN_ABSENT,
                epistemic_state=KNOWN,
                accessibility_state=RESTRICTED,
                topology_state=
                    TOPOLOGY_RESTRICTED,
                hydration_state=PARTIAL,
                hydration_boundary_reference=
                    "hydration:a",
                operational_state=INACTIVE,
                decision_state=PENDING,
                representation_state=
                    EXISTENCE_ONLY,
                evidence_boundary_reference=
                    "boundary:a",
                evidence_ceiling_reference=
                    "ceiling:a",
                restriction_references=(
                    "restriction:a",
                ),
                unresolved_references=(
                    "hydration:unresolved:a",
                ),
                provenance_route=(
                    "origin:a",
                ),
            )

    def test_ar028_blocked_not_denied(self):
        prior = unresolved_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=BLOCKED,
            decision_state=DENIED,
            representation_state=
                prior.representation_state,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "decision_state",
            ),
        )

        self.assertIn(
            (
                "decision resolution requires "
                "attributable authorization"
            ),
            errors,
        )

        self.assertIn(
            (
                "blocked operation cannot "
                "manufacture denial"
            ),
            errors,
        )

    def test_ar028_denial_with_authorization_is_distinct(self):
        prior = unresolved_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=BLOCKED,
            decision_state=DENIED,
            representation_state=
                prior.representation_state,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "decision_state",
            ),
            authorization_references=(
                "human-gate:denial:a",
            ),
        )

        self.assertEqual(
            errors,
            [],
        )

        self.assertEqual(
            result.operational_state,
            BLOCKED,
        )

        self.assertEqual(
            result.decision_state,
            DENIED,
        )

    # --------------------------------------------------------
    # AR-003
    # Restricted object omitted rather than marked.
    # --------------------------------------------------------

    def test_ar003_restricted_object_survives_view(self):
        coordinate = restricted_coordinate()

        self.assertEqual(
            coordinate.existence_state,
            KNOWN_PRESENT,
        )

        self.assertEqual(
            coordinate.accessibility_state,
            RESTRICTED,
        )

        self.assertEqual(
            coordinate.representation_state,
            EXISTENCE_ONLY,
        )

    def test_ar003_restricted_requires_marker(self):
        with self.assertRaises(
            SemanticStateError
        ):
            make_coordinate(
                subject_reference=
                    "object:restricted:missing-marker",
                existence_state=KNOWN_PRESENT,
                epistemic_state=KNOWN,
                accessibility_state=RESTRICTED,
                topology_state=TOPOLOGY_KNOWN,
                hydration_state=UNHYDRATED,
                hydration_boundary_reference=
                    "hydration:a",
                operational_state=INACTIVE,
                decision_state=PENDING,
                representation_state=
                    EXISTENCE_ONLY,
                evidence_boundary_reference=
                    "boundary:a",
                evidence_ceiling_reference=
                    "ceiling:a",
                restriction_references=(),
                unresolved_references=(),
                provenance_route=(
                    "origin:a",
                ),
            )

    # --------------------------------------------------------
    # AR-004 / AR-029
    # Restricted relationship/topology must survive.
    # --------------------------------------------------------

    def test_ar004_restricted_relationship_preserved(self):
        coordinate = restricted_coordinate()

        self.assertEqual(
            coordinate.topology_state,
            TOPOLOGY_RESTRICTED,
        )

        self.assertTrue(
            coordinate.restriction_references
        )

    def test_ar029_restricted_topology_not_absent(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=TOPOLOGY_ABSENT,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=
                prior.representation_state,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "topology_state",
            ),
        )

        self.assertIn(
            (
                "topology resolution requires "
                "attributable evidence"
            ),
            errors,
        )

        self.assertIn(
            (
                "restricted topology cannot "
                "disappear"
            ),
            errors,
        )

    def test_ar029_projection_cannot_delete_topology(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=TOPOLOGY_ABSENT,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=
                OMITTED_BY_VIEW,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "representation_state",
            ),
        )

        self.assertTrue(
            any(
                error.startswith(
                    "cross-dimension mutation:"
                )
                for error in errors
            )
        )

    # --------------------------------------------------------
    # AR-035
    # Partial hydration represented as complete.
    # --------------------------------------------------------

    def test_ar035_partial_is_not_complete(self):
        coordinate = restricted_coordinate()

        self.assertEqual(
            coordinate.hydration_state,
            PARTIAL,
        )

        self.assertNotEqual(
            coordinate.hydration_state,
            COMPLETE,
        )

    def test_ar035_partial_requires_unresolved_surface(self):
        with self.assertRaises(
            SemanticStateError
        ):
            make_coordinate(
                subject_reference=
                    "object:partial:a",
                existence_state=KNOWN_PRESENT,
                epistemic_state=KNOWN,
                accessibility_state=AVAILABLE,
                topology_state=TOPOLOGY_KNOWN,
                hydration_state=PARTIAL,
                hydration_boundary_reference=
                    "hydration:a",
                operational_state=ACTIVE,
                decision_state=NOT_REQUIRED,
                representation_state=FULL,
                evidence_boundary_reference=
                    "boundary:a",
                evidence_ceiling_reference=
                    "ceiling:a",
                restriction_references=(),
                unresolved_references=(),
                provenance_route=(
                    "origin:a",
                ),
            )

    def test_ar035_partial_to_complete_requires_evidence(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=COMPLETE,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=
                prior.representation_state,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "hydration_state",
            ),
        )

        self.assertIn(
            (
                "hydration completion requires "
                "attributable hydration evidence"
            ),
            errors,
        )

    def test_ar035_partial_to_complete_with_evidence(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=COMPLETE,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=
                prior.representation_state,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "hydration_state",
            ),
            hydration_evidence_references=(
                "hydration:witness:a",
            ),
        )

        self.assertEqual(
            errors,
            [],
        )

    # --------------------------------------------------------
    # AR-052
    # Raven / rendering must preserve material unknowns.
    # --------------------------------------------------------

    def test_ar052_unknown_survives_summary(self):
        prior = unresolved_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=SUMMARY,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        self.assertEqual(
            result.epistemic_state,
            UNKNOWN,
        )

        self.assertTrue(
            result.unresolved_references
        )

    def test_ar052_renderer_cannot_promote_unknown(self):
        prior = unresolved_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=KNOWN,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=SUMMARY,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "representation_state",
            ),
        )

        self.assertTrue(
            any(
                error.startswith(
                    "cross-dimension mutation:"
                )
                for error in errors
            )
        )

        self.assertIn(
            (
                "epistemic promotion requires "
                "attributable evidence"
            ),
            errors,
        )

    # --------------------------------------------------------
    # Cross-dimensional geometry
    # --------------------------------------------------------

    def test_representation_change_preserves_geometry(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=REDACTED,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "representation_state",
            ),
        )

        self.assertEqual(
            errors,
            [],
        )

    def test_accessibility_change_cannot_drag_existence(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=KNOWN_ABSENT,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=UNAVAILABLE,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=
                prior.representation_state,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "accessibility_state",
            ),
        )

        self.assertTrue(
            any(
                error.startswith(
                    "cross-dimension mutation:"
                )
                for error in errors
            )
        )

    def test_unknown_to_known_with_evidence_is_allowed(self):
        prior = unresolved_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=KNOWN,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=
                prior.representation_state,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "epistemic_state",
            ),
            evidence_references=(
                "evidence:new:a",
            ),
        )

        self.assertEqual(
            errors,
            [],
        )

    def test_restricted_to_available_requires_authorization(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=AVAILABLE,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=FULL,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "accessibility_state",
                "representation_state",
            ),
        )

        self.assertIn(
            (
                "accessibility promotion requires "
                "attributable authorization"
            ),
            errors,
        )

    def test_restricted_to_available_with_authorization(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=AVAILABLE,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=FULL,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        errors = validate_transition(
            prior,
            result,
            requested_dimensions=(
                "accessibility_state",
                "representation_state",
            ),
            authorization_references=(
                "authorization:view:a",
            ),
        )

        self.assertEqual(
            errors,
            [],
        )

    def test_make_transition_preserves_changed_dimensions(self):
        prior = restricted_coordinate()

        result = make_coordinate(
            subject_reference=
                prior.subject_reference,
            existence_state=
                prior.existence_state,
            epistemic_state=
                prior.epistemic_state,
            accessibility_state=
                prior.accessibility_state,
            topology_state=
                prior.topology_state,
            hydration_state=
                prior.hydration_state,
            hydration_boundary_reference=
                prior.hydration_boundary_reference,
            operational_state=
                prior.operational_state,
            decision_state=
                prior.decision_state,
            representation_state=REDACTED,
            evidence_boundary_reference=
                prior.evidence_boundary_reference,
            evidence_ceiling_reference=
                prior.evidence_ceiling_reference,
            restriction_references=
                prior.restriction_references,
            unresolved_references=
                prior.unresolved_references,
            provenance_route=
                prior.provenance_route,
        )

        transition = make_transition(
            prior,
            result,
            requested_dimensions=(
                "representation_state",
            ),
            provenance_route=(
                "state:a",
                "render:a",
            ),
            transition_reason=
                "authorized representation change",
        )

        self.assertEqual(
            transition.changed_dimensions,
            (
                "representation_state",
            ),
        )


if __name__ == "__main__":
    unittest.main()
