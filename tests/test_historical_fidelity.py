from __future__ import annotations

from dataclasses import replace
import unittest

from tools.historical_fidelity import (
    BLOCKED,
    PROVEN,
    HistoricalWitness,
    LineageEdge,
    evaluate,
    make_valid_record,
)


class HistoricalFidelityTests(unittest.TestCase):

    def setUp(self):
        self.valid = make_valid_record()

    def assertBlocked(self, record, reason):
        result = evaluate(record)
        self.assertEqual(
            result.proof_disposition,
            BLOCKED,
        )
        self.assertIn(
            reason,
            result.blocking_reasons,
        )

    def test_valid_historical_state_is_proven(self):
        result = evaluate(self.valid)
        self.assertEqual(
            result.proof_disposition,
            PROVEN,
        )
        self.assertEqual(
            result.blocking_reasons,
            (),
        )

    # AR-015
    def test_ar015_current_resolution_is_not_historical_proof(self):
        witnesses = tuple(
            witness
            for witness in self.valid.proof_witnesses
            if witness.reference != "evidence:a"
        )

        self.assertBlocked(
            replace(
                self.valid,
                proof_witnesses=witnesses,
            ),
            "HISTORICAL_EXISTENCE_UNPROVEN",
        )

    # AR-033
    def test_ar033_referent_wrong_asof_root_blocks(self):
        witnesses = tuple(
            replace(
                witness,
                historical_state_root=(
                    "sha512:" + "9" * 128
                ),
            )
            if witness.reference == "finding:a"
            else witness
            for witness in self.valid.proof_witnesses
        )

        self.assertBlocked(
            replace(
                self.valid,
                proof_witnesses=witnesses,
            ),
            "HISTORICAL_EXISTENCE_UNPROVEN",
        )

    # AR-031
    def test_ar031_provenance_graft_blocks(self):
        self.assertBlocked(
            replace(
                self.valid,
                replay_provenance_route=(
                    "origin:a",
                    "evidence:new",
                    "finding:a",
                ),
            ),
            "PROVENANCE_GRAFT",
        )

    # AR-030
    def test_ar030_provenance_truncation_blocks(self):
        self.assertBlocked(
            replace(
                self.valid,
                replay_provenance_route=(
                    "origin:a",
                    "finding:a",
                ),
            ),
            "PROVENANCE_TRUNCATED",
        )

    # AR-032
    def test_ar032_provenance_temporal_reordering_blocks(self):
        self.assertBlocked(
            replace(
                self.valid,
                replay_provenance_route=(
                    "finding:a",
                    "evidence:a",
                    "origin:a",
                ),
            ),
            "PROVENANCE_TEMPORAL_REORDER",
        )

    # AR-002
    def test_ar002_false_chain_with_fields_present_blocks(self):
        bad_edges = (
            LineageEdge(
                "origin:a",
                "evidence:a",
                "sha512:" + "8" * 128,
                1,
            ),
            self.valid.historical_lineage_edges[1],
        )

        self.assertBlocked(
            replace(
                self.valid,
                historical_lineage_edges=bad_edges,
                replay_lineage_edges=bad_edges,
            ),
            "PROVENANCE_CHAIN_FALSE",
        )

    # AR-006
    def test_ar006_current_evidence_rebound_blocks(self):
        self.assertBlocked(
            replace(
                self.valid,
                replay_evidence_used_references=(
                    "evidence:current",
                ),
            ),
            "CURRENT_EVIDENCE_REBOUND",
        )

    # AR-005
    def test_ar005_current_question_substitution_blocks(self):
        self.assertBlocked(
            replace(
                self.valid,
                replay_question_reference="question:current",
            ),
            "CURRENT_QUESTION_SUBSTITUTED",
        )

    # AR-013
    def test_ar013_later_evidence_cannot_strengthen_history(self):
        self.assertBlocked(
            replace(
                self.valid,
                later_evidence_used_to_strengthen_history=True,
            ),
            "LATER_EVIDENCE_STRENGTHENED_HISTORY",
        )

    # AR-045
    def test_ar045_replay_reflight_evidence_mix_blocks(self):
        self.assertBlocked(
            replace(
                self.valid,
                replay_reflight_evidence_mixed=True,
            ),
            "REPLAY_REFLIGHT_EVIDENCE_MIXED",
        )

    # AR-007
    def test_ar007_collapse_history_mutation_blocks(self):
        self.assertBlocked(
            replace(
                self.valid,
                replay_collapse_references=(
                    "collapse:current",
                ),
            ),
            "COLLAPSE_HISTORY_MUTATED",
        )

    # AR-043
    def test_ar043_eliminated_alternatives_must_survive(self):
        self.assertBlocked(
            replace(
                self.valid,
                replay_eliminated_alternatives=(),
            ),
            "ELIMINATED_ALTERNATIVES_LOST",
        )

    # AR-014
    def test_ar014_regenerated_rendering_cannot_impersonate_history(self):
        self.assertBlocked(
            replace(
                self.valid,
                regenerated_rendering_claimed_historical=True,
            ),
            "REGENERATED_RENDERING_IMPERSONATES_HISTORICAL",
        )

    def test_missing_historical_rendering_stays_missing(self):
        witnesses = tuple(
            witness
            for witness in self.valid.proof_witnesses
            if witness.reference != "rendering:a"
        )

        record = replace(
            self.valid,
            historical_rendering_reference=None,
            replay_rendering_reference=None,
            proof_witnesses=witnesses,
        )

        result = evaluate(record)

        self.assertEqual(
            result.proof_disposition,
            PROVEN,
        )

    def test_synthetic_rendering_for_absent_history_blocks(self):
        witnesses = tuple(
            witness
            for witness in self.valid.proof_witnesses
            if witness.reference != "rendering:a"
        )

        self.assertBlocked(
            replace(
                self.valid,
                historical_rendering_reference=None,
                replay_rendering_reference="rendering:synthetic",
                proof_witnesses=witnesses,
            ),
            "REGENERATED_RENDERING_IMPERSONATES_HISTORICAL",
        )

    def test_proof_identity_is_deterministic(self):
        first = evaluate(self.valid)
        second = evaluate(self.valid)

        self.assertEqual(
            first.proof_id,
            second.proof_id,
        )

    def test_missing_proof_witnesses_blocks(self):
        self.assertBlocked(
            replace(
                self.valid,
                proof_witnesses=(),
            ),
            "PROOF_WITNESS_MISSING",
        )


if __name__ == "__main__":
    unittest.main()
