from __future__ import annotations

from copy import deepcopy
import unittest

from tools.validate_evidence_ceiling_semantics import (
    compare_semantics,
    validate_enforcement_record,
)


def base_claim():
    return {
        "claim_id": "claim:ac10:a",
        "subject": "activity",
        "predicate": "is associated with",
        "object": "risk",
        "polarity": "POSITIVE",
        "assertion_strength": "PLAUSIBLE",
        "support_state": "PARTIALLY_SUPPORTED",
        "causal_posture": "ASSOCIATION",
        "uncertainty_state": "MATERIAL",
        "surviving_alternatives": [
            "alternative:a",
            "alternative:b",
        ],
        "temporal_scope": "historical:window:a",
        "evidence_refs": [
            "evidence:a",
        ],
        "evidence_boundary_ref": "boundary:a",
        "evidence_ceiling_ref": "ceiling:a",
        "provenance_refs": [
            "provenance:a",
        ],
        "source_analytical_state_ref": "state:historical:a",
        "truth_posture": "INFERRED",
        "cryptographic_integrity_valid": True,
    }


def enforcement_record(source=None, downstream=None):
    if source is None:
        source = base_claim()

    if downstream is None:
        downstream = deepcopy(source)

    return {
        "schema_version": "1.0",
        "activation_control": "AC-10",
        "source_claim": source,
        "downstream_claim": downstream,
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
    }


class AC10EvidenceCeilingSemanticTests(unittest.TestCase):

    def test_identical_semantics_pass(self):
        source = base_claim()
        downstream = deepcopy(source)

        self.assertEqual(
            compare_semantics(source, downstream),
            [],
        )

    # AR-050
    def test_output_semantics_cannot_exceed_ceiling_even_when_metadata_matches(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["assertion_strength"] = "ESTABLISHED"

        reasons = compare_semantics(source, downstream)

        self.assertIn(
            "ASSERTION_STRENGTH_EXCEEDS_CEILING",
            reasons,
        )
        self.assertEqual(
            source["evidence_ceiling_ref"],
            downstream["evidence_ceiling_ref"],
        )

    # AR-013
    def test_later_state_cannot_retroactively_strengthen_historical_claim(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["source_analytical_state_ref"] = "state:later:b"
        downstream["assertion_strength"] = "PROBABLE"

        reasons = compare_semantics(source, downstream)

        self.assertIn(
            "HISTORICAL_ANALYTICAL_STATE_SUBSTITUTED",
            reasons,
        )
        self.assertIn(
            "ASSERTION_STRENGTH_EXCEEDS_CEILING",
            reasons,
        )

    # AR-053
    def test_raven_linguistic_strengthening_is_rejected(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["assertion_strength"] = "PROBABLE"

        self.assertIn(
            "ASSERTION_STRENGTH_EXCEEDS_CEILING",
            compare_semantics(source, downstream),
        )

    # AR-052
    def test_representation_cannot_remove_uncertainty(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["uncertainty_state"] = "RESOLVED"

        self.assertIn(
            "UNCERTAINTY_SILENTLY_REDUCED",
            compare_semantics(source, downstream),
        )

    # AR-042
    def test_collapse_cannot_silently_remove_surviving_alternative(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["surviving_alternatives"] = [
            "alternative:a",
        ]

        self.assertIn(
            "SURVIVING_ALTERNATIVES_REMOVED",
            compare_semantics(source, downstream),
        )

    # AR-027
    def test_crypto_integrity_cannot_become_semantic_truth(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["truth_posture"] = "ESTABLISHED"

        self.assertTrue(
            downstream["cryptographic_integrity_valid"]
        )
        self.assertIn(
            "CRYPTOGRAPHIC_VALIDITY_PROMOTED_TO_TRUTH",
            compare_semantics(source, downstream),
        )

    def test_support_state_cannot_strengthen(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["support_state"] = "SUPPORTED"

        self.assertIn(
            "SUPPORT_STATE_STRENGTHENED",
            compare_semantics(source, downstream),
        )

    def test_association_cannot_become_causation(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["causal_posture"] = "CAUSAL"

        self.assertIn(
            "CAUSAL_POSTURE_STRENGTHENED",
            compare_semantics(source, downstream),
        )

    def test_evidence_ceiling_reference_change_is_rejected(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["evidence_ceiling_ref"] = "ceiling:b"

        self.assertIn(
            "EVIDENCE_CEILING_REFERENCE_CHANGED",
            compare_semantics(source, downstream),
        )

    def test_evidence_boundary_change_is_rejected(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["evidence_boundary_ref"] = "boundary:b"

        self.assertIn(
            "EVIDENCE_BOUNDARY_CHANGED",
            compare_semantics(source, downstream),
        )

    def test_evidence_set_change_is_rejected(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["evidence_refs"].append("evidence:later")

        self.assertIn(
            "EVIDENCE_SET_CHANGED",
            compare_semantics(source, downstream),
        )

    def test_provenance_loss_is_rejected(self):
        source = base_claim()
        source["provenance_refs"].append("provenance:b")
        downstream = deepcopy(source)
        downstream["provenance_refs"] = ["provenance:a"]

        self.assertIn(
            "PROVENANCE_LOST",
            compare_semantics(source, downstream),
        )

    def test_temporal_scope_change_is_rejected(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["temporal_scope"] = "current"

        self.assertIn(
            "TEMPORAL_SCOPE_CHANGED",
            compare_semantics(source, downstream),
        )

    def test_claim_semantic_drift_is_rejected(self):
        source = base_claim()
        downstream = deepcopy(source)
        downstream["predicate"] = "caused"

        self.assertIn(
            "CLAIM_SEMANTIC_DRIFT:predicate",
            compare_semantics(source, downstream),
        )

    def test_complete_enforcement_record_passes(self):
        self.assertEqual(
            validate_enforcement_record(
                enforcement_record()
            ),
            [],
        )

    def test_authority_promotion_is_rejected(self):
        record = enforcement_record()
        record["authority_state"] = "FULL"

        self.assertIn(
            "AUTHORITY_PROMOTED",
            validate_enforcement_record(record),
        )

    def test_human_gate_disable_is_rejected(self):
        record = enforcement_record()
        record["human_gate_state"] = "DISABLED"

        self.assertIn(
            "HUMAN_GATE_DISABLED",
            validate_enforcement_record(record),
        )


if __name__ == "__main__":
    unittest.main()
