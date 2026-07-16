from __future__ import annotations

import copy
import unittest

from candidate.v40.runtime.reporting_inventories import (
    analytical_inventory_freeze_digest,
    seal_analytical_inventory_freeze,
    seal_requirement_inventory,
)
from candidate.v40.runtime.reporting_projection import (
    ReportingProjectionError,
    projection_digest,
    report_element_digest,
    seal_report_projection,
    validate_report_projection,
)
from candidate.v40.runtime.reporting_records import seal_analysis_record, semantic_digest
from tests.test_v40_candidate_report_projection_schema import valid_projection
from tests.test_v40_candidate_reporting_inventory_runtime import (
    inventory_item,
    runtime_bundle,
)


def build_projection(
    requirement: dict,
    freeze: dict,
    analyses: list[dict],
    evidence: list[dict],
    canonical_binding: dict,
    candidate_binding: dict,
    *,
    element_class: str = "CLAIM_PROJECTION",
    visualization_binding: dict | None = None,
) -> dict:
    analysis = analyses[0]
    claims = analysis["claim_objects"]
    claim_refs = [claim["claim_id"] for claim in claims]
    projection = valid_projection()
    projection.update(
        request_ref=freeze["reporting_request_ref"],
        contract_ref=freeze["contract_ref"],
        route_ref=freeze["route_ref"],
        freeze_ref=freeze["freeze_id"],
        freeze_sha512=freeze["freeze_sha512"],
        required_requirement_refs=[
            value["requirement_id"]
            for value in requirement["requirements"]
            if value["required"] and value["status"] != "EXPLICITLY_EXCLUDED"
        ],
        required_inventory_refs=[
            item["inventory_item_id"]
            for item in freeze["ordered_inventory_items"]
            if item["required"] and item["inclusion_state"] == "INCLUDED"
        ],
        claim_ceiling=analysis["claim_ceiling"],
    )
    transformation = projection["allowed_transformations"][0]
    transformation.update(
        source_object_refs=[analysis["analysis_id"], *claim_refs],
        transformation_class=(
            "VISUALIZE" if element_class == "VISUALIZATION" else "ORGANIZE"
        ),
    )
    element = projection["report_elements"][0]
    element.update(
        element_class=element_class,
        source_analysis_refs=[analysis["analysis_id"]],
        source_claim_refs=claim_refs,
        source_semantic_digests=[
            {
                "claim_ref": claim["claim_id"],
                "semantic_sha512": claim["semantic"]["semantic_sha512"],
            }
            for claim in claims
        ],
        evidence_refs=sorted(
            {ref for claim in claims for ref in claim["evidence_refs"]}
        ),
        uncertainty_refs=sorted(
            {ref for claim in claims for ref in claim["uncertainty_refs"]}
        ),
        limitation_refs=sorted(
            {ref for claim in claims for ref in claim["limitation_refs"]}
        ),
        requirement_refs=list(projection["required_requirement_refs"]),
        inventory_refs=list(projection["required_inventory_refs"]),
        visualization_binding=visualization_binding,
    )
    if element_class == "VISUALIZATION":
        element.update(
            element_id="RE-VISUALIZATION-RUNTIME-001",
            rendered_artifact_path="reports/figures/runtime.svg",
            anchor_ref="figure-runtime",
        )
        transformation.update(
            transformation_id="TR-VISUALIZE-RUNTIME-001",
            output_element_refs=[element["element_id"]],
        )
        element["transformation_ref"] = transformation["transformation_id"]
    return seal_report_projection(
        projection,
        freeze,
        requirement,
        analyses,
        evidence,
        expected_canonical_binding=canonical_binding,
        expected_candidate_binding=candidate_binding,
    )


def projection_bundle() -> tuple[dict, dict, list[dict], list[dict], dict, dict, dict]:
    requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
    projection = build_projection(
        requirement,
        freeze,
        analyses,
        evidence,
        canonical,
        candidate,
    )
    return requirement, freeze, analyses, evidence, canonical, candidate, projection


def reseal_projection(projection: dict) -> None:
    for element in projection["report_elements"]:
        element["element_sha512"] = report_element_digest(element)
    projection["projection_sha512"] = projection_digest(projection)


def projection_errors(
    requirement: dict,
    freeze: dict,
    analyses: list[dict],
    evidence: list[dict],
    canonical: dict,
    candidate: dict,
    projection: dict,
) -> list[str]:
    return validate_report_projection(
        projection,
        freeze,
        requirement,
        analyses,
        evidence,
        expected_canonical_binding=canonical,
        expected_candidate_binding=candidate,
    )


def quantitative_visualization_bundle() -> tuple[
    dict,
    dict,
    list[dict],
    list[dict],
    dict,
    dict,
    dict,
]:
    requirement, prior_freeze, analyses, evidence, canonical, candidate = runtime_bundle()
    analysis = copy.deepcopy(analyses[0])
    claim = analysis["claim_objects"][0]
    claim["semantic"]["quantitative"] = {
        "applicable": True,
        "magnitude": 1,
        "unit": "identities",
        "value_ref": "COUNT-VALUE-001",
    }
    claim["semantic"]["denominator_ref"] = "DENOMINATOR-POPULATION-001"
    analysis["count_refs"] = ["COUNT-VALUE-001"]
    analysis = seal_analysis_record(analysis, evidence)

    freeze = copy.deepcopy(prior_freeze)
    freeze.update(
        freeze_id="AIF-REPORTING-QUANTITATIVE-001",
        previous_freeze_ref=prior_freeze["freeze_id"],
    )
    freeze["source_analysis_records"][0].update(
        analysis_sha512=analysis["analysis_sha512"],
        claim_refs=[claim["claim_id"]],
    )
    for item in freeze["ordered_inventory_items"]:
        item["source_sha512"] = analysis["analysis_sha512"]
    start = len(freeze["ordered_inventory_items"]) + 1
    freeze["ordered_inventory_items"].extend(
        [
            inventory_item(
                "AII-RUNTIME-COUNT",
                "COUNT",
                "COUNT-VALUE-001",
                start,
                analysis,
            ),
            inventory_item(
                "AII-RUNTIME-DENOMINATOR",
                "DENOMINATOR",
                "DENOMINATOR-POPULATION-001",
                start + 1,
                analysis,
            ),
        ]
    )
    freeze["freeze_sha512"] = analytical_inventory_freeze_digest(freeze)
    freeze = seal_analytical_inventory_freeze(
        freeze,
        requirement,
        [analysis],
        evidence,
        expected_canonical_binding=canonical,
        expected_candidate_binding=candidate,
    )
    visualization = {
        "source_data_refs": ["COUNT-VALUE-001"],
        "source_count_refs": ["COUNT-VALUE-001"],
        "series_definitions": [
            {
                "series_id": "SER-COUNT-001",
                "label": "Identity count",
                "value_ref": "COUNT-VALUE-001",
                "unit": "identities",
                "aggregation_ref": "AGG-COUNT-001",
            }
        ],
        "category_definitions": [
            {
                "category_id": "CAT-CLAIM-001",
                "label": "Anomaly",
                "value_ref": claim["claim_id"],
            }
        ],
        "axes": [
            {
                "axis_id": "AX-X-001",
                "axis_role": "X",
                "label": "Risk category",
                "unit": "category",
                "scale": "NOMINAL",
            },
            {
                "axis_id": "AX-Y-001",
                "axis_role": "Y",
                "label": "Identity count",
                "unit": "identities",
                "scale": "LINEAR",
            },
        ],
        "filters": [],
        "aggregations": [
            {
                "aggregation_id": "AGG-COUNT-001",
                "aggregation_class": "COUNT",
                "source_refs": ["COUNT-VALUE-001"],
                "denominator_ref": "DENOMINATOR-POPULATION-001",
                "unit": "identities",
                "description": "Count identities against the declared population.",
            }
        ],
        "suppressed_or_unavailable_values": [],
        "caption_claim_refs": [claim["claim_id"]],
        "accessible_description": "Bar chart of the identity count.",
    }
    projection = build_projection(
        requirement,
        freeze,
        [analysis],
        evidence,
        canonical,
        candidate,
        element_class="VISUALIZATION",
        visualization_binding=visualization,
    )
    return requirement, freeze, [analysis], evidence, canonical, candidate, projection


class ReportingProjectionRuntimeFixtures(unittest.TestCase):
    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            msg=f"Expected error containing {fragment!r}; observed {errors!r}",
        )

    def test_fixture_17_valid_projection_preserves_frozen_semantics(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        self.assertEqual(
            projection_errors(
                requirement,
                freeze,
                analyses,
                evidence,
                canonical,
                candidate,
                projection,
            ),
            [],
        )

    def test_projection_sealer_returns_copy_and_detects_element_tamper(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        source = valid_projection()
        source_before = copy.deepcopy(source)
        with self.assertRaises(ReportingProjectionError):
            seal_report_projection(
                source,
                freeze,
                requirement,
                analyses,
                evidence,
                expected_canonical_binding=canonical,
                expected_candidate_binding=candidate,
            )
        self.assertEqual(source, source_before)

        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["report_elements"][0]["anchor_ref"] = "tampered-after-seal"
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "Report element digest mismatch")
        self.assert_error(errors, "Report projection digest mismatch")

    def test_projection_binding_drift_is_rejected_after_outer_rehash(self):
        fields = (
            ("request_ref", "REQUEST-DIFFERENT"),
            ("contract_ref", "OC-V40.DIFFERENT"),
            ("route_ref", "different_route"),
            ("freeze_ref", "AIF-DIFFERENT"),
            ("freeze_sha512", "f" * 128),
        )
        for field, replacement in fields:
            with self.subTest(field=field):
                requirement, freeze, analyses, evidence, canonical, candidate, projection = (
                    projection_bundle()
                )
                projection[field] = replacement
                reseal_projection(projection)
                errors = projection_errors(
                    requirement,
                    freeze,
                    analyses,
                    evidence,
                    canonical,
                    candidate,
                    projection,
                )
                self.assert_error(errors, f"Projection {field} differs")

    def test_required_requirement_and_inventory_sets_are_exact(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["required_requirement_refs"] = ["REQ-NOT-PRESENT"]
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "required requirement set mismatch")

        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["required_inventory_refs"] = ["AII-NOT-PRESENT"]
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "required inventory set mismatch")

    def test_duplicate_transformation_element_and_omission_ids_are_rejected(self):
        cases = (
            ("allowed_transformations", "transformation_id", "Duplicate transformation"),
            ("report_elements", "element_id", "Duplicate report element"),
        )
        for collection, id_field, fragment in cases:
            with self.subTest(collection=collection):
                requirement, freeze, analyses, evidence, canonical, candidate, projection = (
                    projection_bundle()
                )
                duplicate = copy.deepcopy(projection[collection][0])
                duplicate["justification" if collection == "allowed_transformations" else "anchor_ref"] = (
                    "Different body"
                )
                projection[collection].append(duplicate)
                reseal_projection(projection)
                errors = projection_errors(
                    requirement,
                    freeze,
                    analyses,
                    evidence,
                    canonical,
                    candidate,
                    projection,
                )
                self.assert_error(errors, fragment)

        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        omitted_ref = projection["required_inventory_refs"][0]
        omission = {
            "omission_id": "OM-DUPLICATE-001",
            "omitted_ref": omitted_ref,
            "omission_class": "KNOWN_UNAVAILABLE",
            "source_ref": omitted_ref,
            "reason": "First duplicate omission record.",
            "required_item": True,
            "blocking": True,
            "decision_ref": None,
        }
        duplicate = copy.deepcopy(omission)
        duplicate["reason"] = "Second duplicate omission record."
        projection["omission_records"] = [omission, duplicate]
        reseal_projection(projection)
        errors = projection_errors(
            requirement,
            freeze,
            analyses,
            evidence,
            canonical,
            candidate,
            projection,
        )
        self.assert_error(errors, "Duplicate omission")

    def test_transformation_sources_outputs_and_reciprocity_must_resolve(self):
        cases = (
            ("source_object_refs", ["AN-NOT-PRESENT"], "source_object_refs"),
            ("output_element_refs", ["RE-NOT-PRESENT"], "output_element_refs"),
        )
        for field, replacement, fragment in cases:
            with self.subTest(field=field):
                requirement, freeze, analyses, evidence, canonical, candidate, projection = (
                    projection_bundle()
                )
                projection["allowed_transformations"][0][field] = replacement
                reseal_projection(projection)
                errors = projection_errors(
                    requirement,
                    freeze,
                    analyses,
                    evidence,
                    canonical,
                    candidate,
                    projection,
                )
                self.assert_error(errors, fragment)

        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["report_elements"][0]["transformation_ref"] = "TR-NOT-PRESENT"
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "unresolved transformation")

    def test_report_element_claim_must_belong_to_declared_source_analysis(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["report_elements"][0]["source_analysis_refs"] = ["AN-NOT-PRESENT"]
        projection["allowed_transformations"][0]["source_object_refs"].append(
            "AN-NOT-PRESENT"
        )
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "source_analysis_refs has unresolved")
        self.assert_error(errors, "omits source Analysis")

    def test_fixtures_20_21_structured_semantic_mutations_are_rejected(self):
        mutations = {
            "polarity": lambda semantic: semantic.update(polarity="NEGATED"),
            "actor": lambda semantic: semantic.update(subject_ref="IDENTITY-DIFFERENT"),
            "scope": lambda semantic: semantic.update(scope="Different scope"),
            "time": lambda semantic: semantic["temporal_boundary"].update(
                as_of_utc="2026-07-17T00:00:00+00:00"
            ),
            "magnitude": lambda semantic: semantic["quantitative"].update(
                applicable=True,
                magnitude=999,
                unit="identities",
                value_ref=None,
            ),
            "denominator": lambda semantic: semantic.update(
                denominator_ref="DENOMINATOR-DIFFERENT"
            ),
            "unit": lambda semantic: semantic["quantitative"].update(unit="systems"),
            "risk": lambda semantic: semantic.update(risk_category="THREAT"),
        }
        for label, mutate in mutations.items():
            with self.subTest(mutation=label):
                requirement, freeze, analyses, evidence, canonical, candidate, projection = (
                    projection_bundle()
                )
                changed = copy.deepcopy(analyses[0]["claim_objects"][0]["semantic"])
                mutate(changed)
                digest_entry = projection["report_elements"][0][
                    "source_semantic_digests"
                ][0]
                digest_entry["semantic_sha512"] = semantic_digest(changed)
                reseal_projection(projection)
                errors = projection_errors(
                    requirement,
                    freeze,
                    analyses,
                    evidence,
                    canonical,
                    candidate,
                    projection,
                )
                self.assert_error(errors, "semantic digest mismatch")

    def test_fixture_22_evidence_uncertainty_and_limitation_removal_is_rejected(self):
        cases = (
            ("evidence_refs", ["EV-NOT-PRESENT"], "evidence carriage mismatch"),
            ("uncertainty_refs", [], "uncertainty carriage mismatch"),
            ("limitation_refs", [], "limitation carriage mismatch"),
        )
        for field, replacement, fragment in cases:
            with self.subTest(field=field):
                requirement, freeze, analyses, evidence, canonical, candidate, projection = (
                    projection_bundle()
                )
                projection["report_elements"][0][field] = replacement
                reseal_projection(projection)
                errors = projection_errors(
                    requirement,
                    freeze,
                    analyses,
                    evidence,
                    canonical,
                    candidate,
                    projection,
                )
                self.assert_error(errors, fragment)

    def test_semantic_digest_claim_set_must_equal_source_claim_set(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["report_elements"][0]["source_semantic_digests"][0][
            "claim_ref"
        ] = "CL-NOT-PRESENT"
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "semantic claim set mismatch")

    def test_fixture_23_presentation_only_cannot_satisfy_required_coverage(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        element = projection["report_elements"][0]
        element.update(
            element_class="PRESENTATION_ONLY",
            source_analysis_refs=[],
            source_claim_refs=[],
            source_semantic_digests=[],
            evidence_refs=[],
            transformation_ref=None,
            uncertainty_refs=[],
            limitation_refs=[],
            content_status="PRESENTATION_ONLY",
            analytical_completion_credit=False,
            presentation_only_reason="Formatting context only.",
        )
        projection["presentation_only_elements"] = [element["element_id"]]
        projection["allowed_transformations"] = [
            {
                **projection["allowed_transformations"][0],
                "output_element_refs": ["RE-NOT-PRESENT"],
            }
        ]
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "lack analytical completion coverage")

    def test_presentation_only_registry_must_match_actual_elements(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["presentation_only_elements"] = ["RE-NOT-PRESENT"]
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "presentation-only element set mismatch")

    def test_requirement_source_carriage_cannot_be_dropped(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        requirement["requirements"][0]["claim_or_inventory_refs"] = [
            "AII-RUNTIME-001"
        ]
        requirement = seal_requirement_inventory(requirement)
        freeze["requirement_inventory_sha512"] = requirement[
            "requirement_inventory_sha512"
        ]
        freeze = seal_analytical_inventory_freeze(
            freeze,
            requirement,
            analyses,
            evidence,
            expected_canonical_binding=canonical,
            expected_candidate_binding=candidate,
        )
        projection["freeze_sha512"] = freeze["freeze_sha512"]
        projection["report_elements"][0]["inventory_refs"].remove("AII-RUNTIME-001")
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "source carriage mismatch")

    def test_projection_claim_ceiling_cannot_exceed_source_analysis(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["claim_ceiling"] = "NO_AUTHORITY"
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "claim ceiling differs")

    def test_fixture_19_valid_quantitative_visualization_preserves_lineage(self):
        bundle = quantitative_visualization_bundle()
        requirement, freeze, analyses, evidence, canonical, candidate, projection = bundle
        self.assertEqual(
            projection_errors(
                requirement,
                freeze,
                analyses,
                evidence,
                canonical,
                candidate,
                projection,
            ),
            [],
        )

    def test_visualization_unit_denominator_and_caption_mutations_are_rejected(self):
        cases = (
            (
                lambda binding: binding["series_definitions"][0].update(unit="systems"),
                "series unit mutation",
            ),
            (
                lambda binding: binding["aggregations"][0].update(
                    denominator_ref="COUNT-VALUE-001"
                ),
                "denominator mutation",
            ),
            (
                lambda binding: binding.update(caption_claim_refs=["CL-NOT-PRESENT"]),
                "caption_claim_refs",
            ),
        )
        for mutate, fragment in cases:
            with self.subTest(fragment=fragment):
                bundle = quantitative_visualization_bundle()
                requirement, freeze, analyses, evidence, canonical, candidate, projection = (
                    bundle
                )
                binding = projection["report_elements"][0]["visualization_binding"]
                mutate(binding)
                reseal_projection(projection)
                errors = projection_errors(
                    requirement,
                    freeze,
                    analyses,
                    evidence,
                    canonical,
                    candidate,
                    projection,
                )
                self.assert_error(errors, fragment)

    def test_blocking_or_required_omission_rejects_locked_projection(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["omission_records"] = [
            {
                "omission_id": "OM-REQUIRED-001",
                "omitted_ref": projection["required_inventory_refs"][0],
                "omission_class": "KNOWN_UNAVAILABLE",
                "source_ref": projection["required_inventory_refs"][0],
                "reason": "Attempted omission of required material.",
                "required_item": True,
                "blocking": True,
                "decision_ref": None,
            }
        ]
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "omits required item")
        self.assert_error(errors, "contains blocking omission")

    def test_nonlocked_and_self_chained_projection_are_rejected(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        projection["projection_status"] = "DRAFT"
        projection["previous_projection_ref"] = projection["projection_id"]
        reseal_projection(projection)
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "not LOCKED")
        self.assert_error(errors, "cannot reference itself")

    def test_fixture_26_callback_cannot_mutate_frozen_analysis(self):
        requirement, freeze, analyses, evidence, canonical, candidate, projection = (
            projection_bundle()
        )
        analyses[0]["claim_objects"][0]["semantic"]["polarity"] = "NEGATED"
        errors = projection_errors(
            requirement, freeze, analyses, evidence, canonical, candidate, projection
        )
        self.assert_error(errors, "Analysis digest mismatch")

    def test_fixture_27_revised_analysis_requires_new_freeze_and_projection(self):
        requirement, old_freeze, analyses, evidence, canonical, candidate, old_projection = (
            projection_bundle()
        )
        revised = copy.deepcopy(analyses[0])
        revised["finding_refs"] = ["FINDING-ANOMALY-REVISED"]
        revised = seal_analysis_record(revised, evidence)
        old_errors = projection_errors(
            requirement,
            old_freeze,
            [revised],
            evidence,
            canonical,
            candidate,
            old_projection,
        )
        self.assert_error(old_errors, "Freeze source Analysis digest mismatch")

        new_freeze = copy.deepcopy(old_freeze)
        new_freeze.update(
            freeze_id="AIF-REPORTING-REVISED-001",
            previous_freeze_ref=old_freeze["freeze_id"],
        )
        new_freeze["source_analysis_records"][0]["analysis_sha512"] = revised[
            "analysis_sha512"
        ]
        for item in new_freeze["ordered_inventory_items"]:
            item["source_sha512"] = revised["analysis_sha512"]
            if item["item_class"] == "FINDING":
                item["item_ref"] = "FINDING-ANOMALY-REVISED"
        new_freeze["freeze_sha512"] = analytical_inventory_freeze_digest(new_freeze)
        new_freeze = seal_analytical_inventory_freeze(
            new_freeze,
            requirement,
            [revised],
            evidence,
            expected_canonical_binding=canonical,
            expected_candidate_binding=candidate,
        )
        new_projection = build_projection(
            requirement,
            new_freeze,
            [revised],
            evidence,
            canonical,
            candidate,
        )
        new_projection["projection_id"] = "RP-REPORTING-REVISED-001"
        new_projection["previous_projection_ref"] = old_projection["projection_id"]
        reseal_projection(new_projection)
        self.assertEqual(
            projection_errors(
                requirement,
                new_freeze,
                [revised],
                evidence,
                canonical,
                candidate,
                new_projection,
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
