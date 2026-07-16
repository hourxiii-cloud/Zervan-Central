from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from candidate.v40.runtime.schema_validation import SchemaValidationError, validate_schema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "candidate/v40/contracts/report_projection.schema.json"


FORBIDDEN_TRANSFORMATIONS = [
    "MUTATE_CLAIM_SUBJECT",
    "MUTATE_CLAIM_ACTOR",
    "MUTATE_CLAIM_OBJECT",
    "MUTATE_CLAIM_PREDICATE",
    "MUTATE_CLAIM_POLARITY",
    "MUTATE_QUANTITATIVE_VALUE",
    "MUTATE_DENOMINATOR",
    "MUTATE_UNIT",
    "MUTATE_AGGREGATION_BOUNDARY",
    "MUTATE_SCOPE",
    "MUTATE_TIME",
    "MUTATE_EVIDENCE_RELATIONSHIP",
    "MUTATE_LINEAGE",
    "MUTATE_SUPPORT_STATE",
    "MUTATE_UNCERTAINTY",
    "DROP_CONTRADICTION",
    "DROP_LIMITATION",
    "MUTATE_ATTRIBUTION",
    "MUTATE_RISK_CATEGORY",
    "MUTATE_RISK_INHERITANCE",
    "MUTATE_CLASSIFICATION_BOUNDARY",
    "MUTATE_FRAMEWORK_MAPPING_BOUNDARY",
    "MUTATE_CLAIM_CEILING",
    "MUTATE_ROUTE_ORDERING",
    "MUTATE_USER_COMPLETION_CRITERIA",
    "INVENT_FACT",
    "INVENT_CITATION",
    "INVENT_EVIDENCE_IDENTIFIER",
    "INVENT_MISSING_ANALYSIS",
    "SILENT_REQUIRED_OMISSION",
    "CONVERT_MAPPING_TO_COMPLIANCE",
    "CONVERT_PREPARATION_TO_AUTHORIZATION",
    "CONVERT_TRIAGE_TO_VERDICT",
    "CONVERT_REVIEW_READY_TO_PROMOTED",
    "CONVERT_PRESENTATION_TO_ANALYTICAL",
]


def projection_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def valid_parameter() -> dict:
    return {
        "parameter_id": "TP-ORGANIZE-001",
        "parameter_class": "ORDER",
        "name": "section_order",
        "value": None,
        "value_ref": "ORDER-ANOMALY-TO-OFFENDING-ID",
        "description": "Preserve the route-required risk sequence.",
    }


def valid_transformation() -> dict:
    return {
        "transformation_id": "TR-ORGANIZE-001",
        "transformation_class": "ORGANIZE",
        "source_object_refs": ["AN-REPORTING-001", "CL-ANOMALY-001"],
        "output_element_refs": ["RE-CLAIM-001"],
        "parameters": [valid_parameter()],
        "justification": "Organize the frozen claim for the declared audience.",
    }


def valid_analytical_element() -> dict:
    return {
        "element_id": "RE-CLAIM-001",
        "element_class": "CLAIM_PROJECTION",
        "source_analysis_refs": ["AN-REPORTING-001"],
        "source_claim_refs": ["CL-ANOMALY-001"],
        "source_semantic_digests": [
            {
                "claim_ref": "CL-ANOMALY-001",
                "semantic_sha512": "a" * 128,
            }
        ],
        "evidence_refs": ["EV-REPORTING-001"],
        "transformation_ref": "TR-ORGANIZE-001",
        "rendered_artifact_path": "reports/09_anomaly_findings.md",
        "anchor_ref": "finding-anomaly-001",
        "uncertainty_refs": ["UNC-ANOMALY-001"],
        "limitation_refs": ["LIM-TIME-001"],
        "requirement_refs": ["REQ-REPORT-ORDER-001"],
        "inventory_refs": ["AII-FINDING-001"],
        "content_status": "SUBSTANTIVE",
        "analytical_completion_credit": True,
        "presentation_only_reason": None,
        "visualization_binding": None,
        "element_sha512": "b" * 128,
        "human_review_status": "REVIEW_REQUIRED",
    }


def valid_projection() -> dict:
    return {
        "projection_version": "v40-candidate.1",
        "projection_id": "RP-REPORTING-001",
        "request_ref": "USER-REQUEST-REPORT-001",
        "contract_ref": "OC-V40.WAVE1.REPORTING-PRODUCTION",
        "route_ref": "v40_candidate_wave1_reporting_production",
        "freeze_ref": "AIF-REPORTING-001",
        "freeze_sha512": "c" * 128,
        "audience_profile": {
            "audience_profile_id": "AUD-TECHNICAL-001",
            "audience_class": "TECHNICAL",
            "description": "Technical and audit reviewers of the reporting package.",
            "language_tag": "en-US",
            "assumed_context_refs": [],
            "required_context_refs": ["README-REPORTING-001"],
            "accessibility_requirements": ["TEXT_ALTERNATIVES"],
        },
        "reporting_lane": "insider_threat_reporting_lane",
        "allowed_transformations": [valid_transformation()],
        "forbidden_transformations": list(FORBIDDEN_TRANSFORMATIONS),
        "required_requirement_refs": ["REQ-REPORT-ORDER-001"],
        "required_inventory_refs": ["AII-FINDING-001"],
        "report_elements": [valid_analytical_element()],
        "omission_records": [],
        "presentation_only_elements": [],
        "human_readable_claim_map_ref": "reports/claim_map.md#claim-anomaly-001",
        "claim_ceiling": "ANALYTICAL_ONLY",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "projection_status": "LOCKED",
        "created_at_utc": "2026-07-16T20:30:00+00:00",
        "previous_projection_ref": None,
        "projection_sha512": "d" * 128,
    }


def valid_presentation_element() -> dict:
    element = valid_analytical_element()
    element.update(
        element_id="RE-PRESENTATION-001",
        element_class="PRESENTATION_ONLY",
        source_analysis_refs=[],
        source_claim_refs=[],
        source_semantic_digests=[],
        evidence_refs=[],
        transformation_ref=None,
        rendered_artifact_path="reports/assets/title_page.md",
        anchor_ref="title-page",
        uncertainty_refs=[],
        limitation_refs=[],
        content_status="PRESENTATION_ONLY",
        analytical_completion_credit=False,
        presentation_only_reason="Package title and navigation context only.",
        visualization_binding=None,
    )
    return element


def valid_navigation_element() -> dict:
    element = valid_presentation_element()
    element.update(
        element_id="RE-NAVIGATION-001",
        element_class="NAVIGATION",
        rendered_artifact_path="reports/README.md",
        anchor_ref="contents",
        content_status="NAVIGATION",
        presentation_only_reason=None,
    )
    return element


def valid_visualization_binding() -> dict:
    return {
        "source_data_refs": ["COUNT-ANOMALY-001"],
        "source_count_refs": ["COUNT-ANOMALY-001"],
        "series_definitions": [
            {
                "series_id": "SER-ANOMALY-001",
                "label": "Anomaly count",
                "value_ref": "COUNT-ANOMALY-001",
                "unit": "identities",
                "aggregation_ref": "AGG-COUNT-001",
            }
        ],
        "category_definitions": [
            {
                "category_id": "CAT-RISK-001",
                "label": "Anomaly",
                "value_ref": "RISK-ANOMALY",
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
        "filters": [
            {
                "filter_id": "FIL-SCOPE-001",
                "field_ref": "FIELD-AUTHORIZED-SCOPE",
                "operator": "EQUALS",
                "value_refs": ["VALUE-AUTHORIZED"],
                "description": "Limit the chart to the authorized dataset scope.",
            }
        ],
        "aggregations": [
            {
                "aggregation_id": "AGG-COUNT-001",
                "aggregation_class": "COUNT",
                "source_refs": ["IDENTITY-001"],
                "denominator_ref": None,
                "unit": "identities",
                "description": "Count identities in the declared anomaly population.",
            }
        ],
        "suppressed_or_unavailable_values": [
            {
                "value_ref": "SOURCE-EVENT-TIME",
                "state": "UNAVAILABLE",
                "reason": "The source dataset contains no event-time field.",
            }
        ],
        "caption_claim_refs": ["CL-ANOMALY-001"],
        "accessible_description": "Bar chart showing the anomaly identity count.",
    }


def valid_visualization_projection() -> dict:
    value = valid_projection()
    transformation = value["allowed_transformations"][0]
    transformation.update(
        transformation_id="TR-VISUALIZE-001",
        transformation_class="VISUALIZE",
    )
    element = value["report_elements"][0]
    element.update(
        element_id="RE-VISUALIZATION-001",
        element_class="VISUALIZATION",
        transformation_ref="TR-VISUALIZE-001",
        rendered_artifact_path="reports/figures/anomaly_count.svg",
        anchor_ref="figure-anomaly-count",
        visualization_binding=valid_visualization_binding(),
    )
    transformation["output_element_refs"] = [element["element_id"]]
    return value


class ProjectionSchemaTestCase(unittest.TestCase):
    def assert_valid(self, value: dict) -> None:
        validate_schema(value, projection_schema())

    def assert_invalid(self, value: dict) -> None:
        with self.assertRaises(SchemaValidationError):
            validate_schema(value, projection_schema())


class ReportProjectionSchemaFixtures(ProjectionSchemaTestCase):
    def test_valid_locked_projection_preserves_authority_and_human_review_boundary(self):
        value = valid_projection()
        self.assert_valid(value)
        self.assertEqual(value["authority_state"], "NONE")
        self.assertEqual(value["human_gate_state"], "ACTIVE")
        self.assertEqual(
            value["report_elements"][0]["human_review_status"], "REVIEW_REQUIRED"
        )

    def test_all_canonical_reporting_lanes_are_accepted(self):
        lanes = (
            "academic_reporting_lane",
            "risk_reporting_lane",
            "resilience_reporting_lane",
            "threat_reporting_lane",
            "hidden_threat_reporting_lane",
            "insider_threat_reporting_lane",
        )
        for lane in lanes:
            with self.subTest(lane=lane):
                value = valid_projection()
                value["reporting_lane"] = lane
                self.assert_valid(value)

    def test_all_declared_allowed_transformations_are_accepted(self):
        classes = (
            "TRANSLATE_LANGUAGE",
            "ORGANIZE",
            "SUMMARIZE",
            "VISUALIZE",
            "SEQUENCE",
            "FORMAT",
            "AUDIENCE_ADAPT",
            "DECLARED_FILTER",
            "DECLARED_AGGREGATION",
            "ACCESSIBILITY_ADAPT",
        )
        for transformation_class in classes:
            with self.subTest(transformation_class=transformation_class):
                value = valid_projection()
                value["allowed_transformations"][0][
                    "transformation_class"
                ] = transformation_class
                self.assert_valid(value)

    def test_all_nonvisual_analytical_element_classes_are_accepted(self):
        classes = (
            "CLAIM_PROJECTION",
            "FINDING",
            "COUNT",
            "TABLE",
            "METHOD",
            "LIMITATION",
            "UNCERTAINTY",
            "CONTRADICTION",
            "EVIDENCE_INDEX",
            "IDENTITY_ASSESSMENT",
            "CLASSIFICATION_SURFACE",
            "FRAMEWORK_MAPPING_SURFACE",
            "RECOMMENDATION",
        )
        for element_class in classes:
            with self.subTest(element_class=element_class):
                value = valid_projection()
                value["report_elements"][0]["element_class"] = element_class
                self.assert_valid(value)

    def test_forbidden_transformation_set_is_complete_unique_and_closed(self):
        value = valid_projection()
        value["forbidden_transformations"].pop()
        self.assert_invalid(value)

        value = valid_projection()
        value["forbidden_transformations"][-1] = value["forbidden_transformations"][0]
        self.assert_invalid(value)

        value = valid_projection()
        value["forbidden_transformations"][-1] = "ASSISTANT_SELECTED_MUTATION"
        self.assert_invalid(value)

    def test_transformations_require_sources_outputs_parameters_and_justification(self):
        cases = (
            ("source_object_refs", []),
            ("output_element_refs", []),
            ("parameters", []),
            ("justification", ""),
        )
        for field, replacement in cases:
            with self.subTest(field=field):
                value = valid_projection()
                value["allowed_transformations"][0][field] = replacement
                self.assert_invalid(value)

    def test_transformation_parameter_requires_value_or_value_reference(self):
        value = valid_projection()
        parameter = value["allowed_transformations"][0]["parameters"][0]
        parameter["value"] = None
        parameter["value_ref"] = None
        self.assert_invalid(value)

    def test_transformation_and_parameter_objects_are_closed(self):
        value = valid_projection()
        value["allowed_transformations"][0]["silent_mutation"] = True
        self.assert_invalid(value)

        value = valid_projection()
        value["allowed_transformations"][0]["parameters"][0]["hidden_filter"] = True
        self.assert_invalid(value)

    def test_authority_promotion_and_human_gate_bypass_are_rejected(self):
        value = valid_projection()
        value["authority_state"] = "ASSISTANT"
        self.assert_invalid(value)

        value = valid_projection()
        value["human_gate_state"] = "BYPASSED"
        self.assert_invalid(value)

    def test_projection_bindings_and_digests_are_typed(self):
        cases = (
            ("projection_id", "PROJECTION-001"),
            ("freeze_ref", "AN-REPORTING-001"),
            ("freeze_sha512", "invalid"),
            ("projection_sha512", "invalid"),
        )
        for field, replacement in cases:
            with self.subTest(field=field):
                value = valid_projection()
                value[field] = replacement
                self.assert_invalid(value)

    def test_required_requirement_inventory_transformation_and_element_sets_cannot_be_empty(self):
        fields = (
            "required_requirement_refs",
            "required_inventory_refs",
            "allowed_transformations",
            "report_elements",
        )
        for field in fields:
            with self.subTest(field=field):
                value = valid_projection()
                value[field] = []
                self.assert_invalid(value)

    def test_unknown_reporting_lane_and_projection_status_are_rejected(self):
        value = valid_projection()
        value["reporting_lane"] = "generic_assistant_lane"
        self.assert_invalid(value)

        value = valid_projection()
        value["projection_status"] = "PROMOTED"
        self.assert_invalid(value)

    def test_analytical_element_requires_complete_source_lineage(self):
        cases = (
            ("source_analysis_refs", []),
            ("source_claim_refs", []),
            ("source_semantic_digests", []),
            ("evidence_refs", []),
            ("transformation_ref", None),
        )
        for field, replacement in cases:
            with self.subTest(field=field):
                value = valid_projection()
                value["report_elements"][0][field] = replacement
                self.assert_invalid(value)

    def test_analytical_element_rejects_invalid_semantic_digest(self):
        value = valid_projection()
        value["report_elements"][0]["source_semantic_digests"][0][
            "semantic_sha512"
        ] = "invalid"
        self.assert_invalid(value)

    def test_analytical_element_cannot_be_relabeled_as_nonanalytical(self):
        cases = (
            ("content_status", "PRESENTATION_ONLY"),
            ("analytical_completion_credit", False),
            ("presentation_only_reason", "Hide the analytical lineage"),
            ("human_review_status", "HUMAN_REVIEWED"),
        )
        for field, replacement in cases:
            with self.subTest(field=field):
                value = valid_projection()
                value["report_elements"][0][field] = replacement
                self.assert_invalid(value)

    def test_valid_presentation_only_element_has_no_analytical_credit(self):
        value = valid_projection()
        presentation = valid_presentation_element()
        value["report_elements"].append(presentation)
        value["presentation_only_elements"] = [presentation["element_id"]]
        self.assert_valid(value)

    def test_presentation_only_element_cannot_carry_analytical_material(self):
        cases = (
            ("source_analysis_refs", ["AN-REPORTING-001"]),
            ("source_claim_refs", ["CL-ANOMALY-001"]),
            ("source_semantic_digests", [{"claim_ref": "CL-ANOMALY-001", "semantic_sha512": "a" * 128}]),
            ("evidence_refs", ["EV-REPORTING-001"]),
            ("transformation_ref", "TR-ORGANIZE-001"),
            ("analytical_completion_credit", True),
        )
        for field, replacement in cases:
            with self.subTest(field=field):
                value = valid_projection()
                presentation = valid_presentation_element()
                presentation[field] = replacement
                value["report_elements"] = [presentation]
                value["presentation_only_elements"] = [presentation["element_id"]]
                self.assert_invalid(value)

    def test_presentation_only_reason_is_required(self):
        value = valid_projection()
        presentation = valid_presentation_element()
        presentation["presentation_only_reason"] = None
        value["report_elements"] = [presentation]
        value["presentation_only_elements"] = [presentation["element_id"]]
        self.assert_invalid(value)

    def test_valid_navigation_element_cannot_earn_analytical_credit(self):
        value = valid_projection()
        navigation = valid_navigation_element()
        value["report_elements"].append(navigation)
        self.assert_valid(value)

        navigation["analytical_completion_credit"] = True
        self.assert_invalid(value)

    def test_valid_visualization_binds_data_axes_filters_aggregation_and_caption(self):
        self.assert_valid(valid_visualization_projection())

    def test_visualization_requires_every_material_binding_surface(self):
        empty_fields = (
            "source_data_refs",
            "series_definitions",
            "category_definitions",
            "axes",
            "caption_claim_refs",
        )
        for field in empty_fields:
            with self.subTest(field=field):
                value = valid_visualization_projection()
                value["report_elements"][0]["visualization_binding"][field] = []
                self.assert_invalid(value)

        value = valid_visualization_projection()
        value["report_elements"][0]["visualization_binding"][
            "accessible_description"
        ] = ""
        self.assert_invalid(value)

    def test_nonvisual_element_cannot_carry_visualization_binding(self):
        value = valid_projection()
        value["report_elements"][0][
            "visualization_binding"
        ] = valid_visualization_binding()
        self.assert_invalid(value)

    def test_artifact_paths_must_be_relative_and_nontraversing(self):
        for path in ("/absolute/report.md", "reports/../secret.md"):
            with self.subTest(path=path):
                value = valid_projection()
                value["report_elements"][0]["rendered_artifact_path"] = path
                self.assert_invalid(value)

    def test_report_element_objects_are_closed(self):
        value = valid_projection()
        value["report_elements"][0]["assistant_completion_claim"] = True
        self.assert_invalid(value)

    def test_valid_explicit_exclusion_requires_decision_and_is_nonblocking(self):
        value = valid_projection()
        value["omission_records"] = [
            {
                "omission_id": "OM-EXCLUSION-001",
                "omitted_ref": "AII-OPTIONAL-001",
                "omission_class": "EXPLICITLY_EXCLUDED",
                "source_ref": "REQ-OPTIONAL-001",
                "reason": "The Human Gate explicitly excluded the optional appendix.",
                "required_item": False,
                "blocking": False,
                "decision_ref": "HG-DECISION-001",
            }
        ]
        self.assert_valid(value)

        value["omission_records"][0]["decision_ref"] = None
        self.assert_invalid(value)

    def test_required_known_unavailable_item_is_blocking(self):
        value = valid_projection()
        value["omission_records"] = [
            {
                "omission_id": "OM-UNAVAILABLE-001",
                "omitted_ref": "AII-UNAVAILABLE-001",
                "omission_class": "KNOWN_UNAVAILABLE",
                "source_ref": "AIF-REPORTING-001",
                "reason": "The source event time is unavailable.",
                "required_item": True,
                "blocking": True,
                "decision_ref": None,
            }
        ]
        self.assert_valid(value)

        value["omission_records"][0]["blocking"] = False
        self.assert_invalid(value)

    def test_omission_objects_are_closed(self):
        value = valid_projection()
        value["omission_records"] = [
            {
                "omission_id": "OM-UNAVAILABLE-001",
                "omitted_ref": "AII-UNAVAILABLE-001",
                "omission_class": "KNOWN_UNAVAILABLE",
                "source_ref": "AIF-REPORTING-001",
                "reason": "The source event time is unavailable.",
                "required_item": True,
                "blocking": True,
                "decision_ref": None,
                "remaining_work": True,
            }
        ]
        self.assert_invalid(value)

    def test_audience_profile_requires_explicit_context_and_valid_language(self):
        value = valid_projection()
        value["audience_profile"]["required_context_refs"] = []
        self.assert_invalid(value)

        value = valid_projection()
        value["audience_profile"]["language_tag"] = "not a language"
        self.assert_invalid(value)

    def test_previous_projection_reference_is_typed(self):
        value = valid_projection()
        value["previous_projection_ref"] = "RP-REPORTING-000"
        self.assert_valid(value)

        value["previous_projection_ref"] = "AIF-REPORTING-000"
        self.assert_invalid(value)

    def test_projection_object_is_closed(self):
        value = valid_projection()
        value["assistant_certified_equivalence"] = True
        self.assert_invalid(value)


if __name__ == "__main__":
    unittest.main()
