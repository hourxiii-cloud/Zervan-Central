"""Integrity, lineage, and mutation controls for v40 Report Projections."""

from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from candidate.v40.runtime.reporting_inventories import validate_reporting_inventories
from candidate.v40.runtime.reporting_records import canonical_digest
from candidate.v40.runtime.schema_validation import SchemaValidationError, validate_schema


ROOT = Path(__file__).resolve().parents[3]
PROJECTION_SCHEMA_PATH = ROOT / "candidate/v40/contracts/report_projection.schema.json"


class ReportingProjectionError(RuntimeError):
    """A Report Projection failed integrity, lineage, or mutation validation."""

    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@lru_cache(maxsize=1)
def _load_schema() -> dict[str, Any]:
    return json.loads(PROJECTION_SCHEMA_PATH.read_text(encoding="utf-8"))


def projection_digest(projection: dict[str, Any]) -> str:
    """Hash canonical JSON excluding only the projection digest field."""

    return canonical_digest(projection, "projection_sha512")


def report_element_digest(element: dict[str, Any]) -> str:
    """Hash canonical JSON excluding only the report-element digest field."""

    return canonical_digest(element, "element_sha512")


def _index_unique(
    values: Iterable[dict[str, Any]],
    id_field: str,
    label: str,
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for value in values:
        identifier = value[id_field]
        if identifier in index:
            errors.append(f"Duplicate {label} identifier: {identifier}")
            continue
        index[identifier] = value
    return index


def _require_refs(
    refs: Iterable[str],
    available: set[str],
    label: str,
    errors: list[str],
) -> None:
    missing = sorted(set(refs) - available)
    if missing:
        errors.append(f"{label} has unresolved references: {', '.join(missing)}")


def _analysis_indexes(
    analyses: Iterable[dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, str],
    set[str],
    dict[str, str],
    dict[str, str | None],
]:
    analysis_index: dict[str, dict[str, Any]] = {}
    claim_index: dict[str, dict[str, Any]] = {}
    claim_owner: dict[str, str] = {}
    analytical_refs: set[str] = set()
    quantitative_units: dict[str, str] = {}
    quantitative_denominators: dict[str, str | None] = {}

    for analysis in analyses:
        analysis_id = analysis["analysis_id"]
        analysis_index[analysis_id] = analysis
        analytical_refs.add(analysis_id)
        collections = (
            analysis["method_refs"],
            analysis["finding_refs"],
            analysis["count_refs"],
            analysis["identity_refs"],
            analysis["evidence_refs"],
            analysis["contradiction_refs"],
            analysis["classification_refs"],
            analysis["framework_mapping_refs"],
            analysis["eliminated_world_refs"],
            analysis["surviving_world_refs"],
            analysis["provenance_refs"],
        )
        for collection in collections:
            analytical_refs.update(collection)
        analytical_refs.update(
            value["uncertainty_id"] for value in analysis["uncertainty_objects"]
        )
        analytical_refs.update(
            value["limitation_id"] for value in analysis["limitation_objects"]
        )
        analytical_refs.update(
            value["edge_id"] for value in analysis["risk_inheritance_edges"]
        )

        for claim in analysis["claim_objects"]:
            claim_id = claim["claim_id"]
            claim_index[claim_id] = claim
            claim_owner[claim_id] = analysis_id
            analytical_refs.add(claim_id)
            semantic = claim["semantic"]
            analytical_refs.add(semantic["ordering_ref"])
            denominator_ref = semantic["denominator_ref"]
            if denominator_ref is not None:
                analytical_refs.add(denominator_ref)
            quantitative = semantic["quantitative"]
            value_ref = quantitative["value_ref"]
            if value_ref is not None:
                analytical_refs.add(value_ref)
                if quantitative["unit"] is not None:
                    quantitative_units[value_ref] = quantitative["unit"]
                quantitative_denominators[value_ref] = denominator_ref
            if quantitative["unit"] is not None:
                quantitative_units[claim_id] = quantitative["unit"]
            quantitative_denominators[claim_id] = denominator_ref

    return (
        analysis_index,
        claim_index,
        claim_owner,
        analytical_refs,
        quantitative_units,
        quantitative_denominators,
    )


def _validate_element_lineage(
    element_id: str,
    element: dict[str, Any],
    analysis_ids: set[str],
    claim_index: dict[str, dict[str, Any]],
    claim_owner: dict[str, str],
    evidence_ids: set[str],
    errors: list[str],
) -> None:
    source_analysis_refs = set(element["source_analysis_refs"])
    source_claim_refs = set(element["source_claim_refs"])
    _require_refs(
        source_analysis_refs,
        analysis_ids,
        f"report element {element_id}.source_analysis_refs",
        errors,
    )
    _require_refs(
        source_claim_refs,
        set(claim_index),
        f"report element {element_id}.source_claim_refs",
        errors,
    )

    for claim_ref in source_claim_refs & set(claim_index):
        owner = claim_owner[claim_ref]
        if owner not in source_analysis_refs:
            errors.append(
                f"Report element {element_id} omits source Analysis {owner} for {claim_ref}"
            )

    semantic_entries = _index_unique(
        element["source_semantic_digests"],
        "claim_ref",
        f"report element {element_id} semantic digest",
        errors,
    )
    if set(semantic_entries) != source_claim_refs:
        errors.append(f"Report element semantic claim set mismatch: {element_id}")
    for claim_ref, entry in semantic_entries.items():
        claim = claim_index.get(claim_ref)
        if claim is not None and entry["semantic_sha512"] != claim["semantic"][
            "semantic_sha512"
        ]:
            errors.append(f"Report element semantic digest mismatch: {element_id}/{claim_ref}")

    claims = [claim_index[ref] for ref in source_claim_refs if ref in claim_index]
    expected_evidence = {ref for claim in claims for ref in claim["evidence_refs"]}
    expected_uncertainty = {ref for claim in claims for ref in claim["uncertainty_refs"]}
    expected_limitations = {ref for claim in claims for ref in claim["limitation_refs"]}

    actual_evidence = set(element["evidence_refs"])
    actual_uncertainty = set(element["uncertainty_refs"])
    actual_limitations = set(element["limitation_refs"])
    if actual_evidence != expected_evidence:
        errors.append(f"Report element evidence carriage mismatch: {element_id}")
    if actual_uncertainty != expected_uncertainty:
        errors.append(f"Report element uncertainty carriage mismatch: {element_id}")
    if actual_limitations != expected_limitations:
        errors.append(f"Report element limitation carriage mismatch: {element_id}")
    _require_refs(
        actual_evidence,
        evidence_ids,
        f"report element {element_id}.evidence_refs",
        errors,
    )


def _validate_visualization(
    element_id: str,
    element: dict[str, Any],
    resolvable_refs: set[str],
    quantitative_units: dict[str, str],
    quantitative_denominators: dict[str, str | None],
    errors: list[str],
) -> None:
    binding = element["visualization_binding"]
    if binding is None:
        return

    _require_refs(
        binding["source_data_refs"],
        resolvable_refs,
        f"visualization {element_id}.source_data_refs",
        errors,
    )
    _require_refs(
        binding["source_count_refs"],
        resolvable_refs,
        f"visualization {element_id}.source_count_refs",
        errors,
    )
    source_claim_refs = set(element["source_claim_refs"])
    caption_claim_refs = set(binding["caption_claim_refs"])
    _require_refs(
        caption_claim_refs,
        source_claim_refs,
        f"visualization {element_id}.caption_claim_refs",
        errors,
    )

    aggregations = _index_unique(
        binding["aggregations"],
        "aggregation_id",
        f"visualization {element_id} aggregation",
        errors,
    )
    aggregation_ids = set(aggregations)
    series_units: set[str] = set()
    for series in binding["series_definitions"]:
        value_ref = series["value_ref"]
        _require_refs(
            [value_ref],
            resolvable_refs,
            f"visualization {element_id} series value_ref",
            errors,
        )
        aggregation_ref = series["aggregation_ref"]
        if aggregation_ref is not None:
            _require_refs(
                [aggregation_ref],
                aggregation_ids,
                f"visualization {element_id} series aggregation_ref",
                errors,
            )
        expected_unit = quantitative_units.get(value_ref)
        if expected_unit is not None and series["unit"] != expected_unit:
            errors.append(f"Visualization series unit mutation: {element_id}/{value_ref}")
        series_units.add(series["unit"])

    for category in binding["category_definitions"]:
        _require_refs(
            [category["value_ref"]],
            resolvable_refs,
            f"visualization {element_id} category value_ref",
            errors,
        )
    for filter_definition in binding["filters"]:
        _require_refs(
            [filter_definition["field_ref"]],
            resolvable_refs,
            f"visualization {element_id} filter field_ref",
            errors,
        )
        _require_refs(
            filter_definition["value_refs"],
            resolvable_refs,
            f"visualization {element_id} filter value_refs",
            errors,
        )
    for aggregation_id, aggregation in aggregations.items():
        _require_refs(
            aggregation["source_refs"],
            resolvable_refs,
            f"visualization {element_id} aggregation {aggregation_id}.source_refs",
            errors,
        )
        denominator_ref = aggregation["denominator_ref"]
        if denominator_ref is not None:
            _require_refs(
                [denominator_ref],
                resolvable_refs,
                f"visualization {element_id} aggregation {aggregation_id}.denominator_ref",
                errors,
            )
        for source_ref in aggregation["source_refs"]:
            expected_denominator = quantitative_denominators.get(source_ref)
            if expected_denominator is not None and denominator_ref != expected_denominator:
                errors.append(
                    f"Visualization aggregation denominator mutation: "
                    f"{element_id}/{aggregation_id}"
                )
            expected_unit = quantitative_units.get(source_ref)
            if expected_unit is not None and aggregation["unit"] != expected_unit:
                errors.append(
                    f"Visualization aggregation unit mutation: {element_id}/{aggregation_id}"
                )

    for axis in binding["axes"]:
        if axis["axis_role"] in {"Y", "SIZE"} and series_units:
            if axis["unit"] not in series_units:
                errors.append(f"Visualization axis unit mutation: {element_id}/{axis['axis_id']}")

    for unavailable in binding["suppressed_or_unavailable_values"]:
        _require_refs(
            [unavailable["value_ref"]],
            resolvable_refs,
            f"visualization {element_id} unavailable value_ref",
            errors,
        )


def _validate_omissions(
    omissions: dict[str, dict[str, Any]],
    requirements: dict[str, dict[str, Any]],
    items: dict[str, dict[str, Any]],
    exclusions: dict[str, dict[str, Any]],
    ambiguities: dict[str, dict[str, Any]],
    required_refs: set[str],
    errors: list[str],
) -> None:
    resolvable = set(requirements) | set(items) | set(exclusions) | set(ambiguities)
    for omission_id, omission in omissions.items():
        omitted_ref = omission["omitted_ref"]
        _require_refs(
            [omitted_ref],
            resolvable,
            f"omission {omission_id}.omitted_ref",
            errors,
        )
        _require_refs(
            [omission["source_ref"]],
            resolvable,
            f"omission {omission_id}.source_ref",
            errors,
        )
        if omitted_ref in required_refs:
            errors.append(f"Locked projection omits required item: {omitted_ref}")
        if omission["blocking"]:
            errors.append(f"Locked projection contains blocking omission: {omission_id}")
        if omission["omission_class"] == "EXPLICITLY_EXCLUDED":
            decision_ref = omission["decision_ref"]
            valid_decisions = {
                requirement["exclusion_ref"]
                for requirement in requirements.values()
                if requirement["status"] == "EXPLICITLY_EXCLUDED"
            }
            valid_decisions.update(
                exclusion["decision_ref"] for exclusion in exclusions.values()
            )
            if decision_ref not in valid_decisions:
                errors.append(f"Projection omission decision is unresolved: {omission_id}")


def validate_report_projection(
    projection: Any,
    freeze: Any,
    requirement_inventory: Any,
    analysis_records: Iterable[dict[str, Any]],
    evidence_records: Iterable[dict[str, Any]],
    *,
    expected_canonical_binding: dict[str, Any],
    expected_candidate_binding: dict[str, Any],
) -> list[str]:
    """Validate a locked projection against the exact frozen analytical boundary."""

    analyses = list(analysis_records)
    evidence = list(evidence_records)
    inventory_errors = validate_reporting_inventories(
        freeze,
        requirement_inventory,
        analyses,
        evidence,
        expected_canonical_binding=expected_canonical_binding,
        expected_candidate_binding=expected_candidate_binding,
    )
    errors = [f"inventory_boundary: {error}" for error in inventory_errors]

    try:
        validate_schema(projection, _load_schema())
    except (OSError, json.JSONDecodeError, SchemaValidationError) as exc:
        errors.append(f"Report projection schema invalid: {exc}")
        return errors

    transformations = _index_unique(
        projection["allowed_transformations"],
        "transformation_id",
        "transformation",
        errors,
    )
    elements = _index_unique(
        projection["report_elements"], "element_id", "report element", errors
    )
    omissions = _index_unique(
        projection["omission_records"], "omission_id", "omission", errors
    )

    for element_id, element in elements.items():
        try:
            expected_element_digest = report_element_digest(element)
        except (TypeError, ValueError) as exc:
            errors.append(f"Report element canonicalization failed for {element_id}: {exc}")
        else:
            if element["element_sha512"] != expected_element_digest:
                errors.append(f"Report element digest mismatch: {element_id}")
    try:
        expected_projection_digest = projection_digest(projection)
    except (TypeError, ValueError) as exc:
        errors.append(f"Report projection canonicalization failed: {exc}")
    else:
        if projection["projection_sha512"] != expected_projection_digest:
            errors.append(f"Report projection digest mismatch: {projection['projection_id']}")

    if inventory_errors:
        return errors
    if not isinstance(freeze, dict) or not isinstance(requirement_inventory, dict):
        errors.append("Frozen inventory boundary is unavailable")
        return errors

    requirements = _index_unique(
        requirement_inventory["requirements"],
        "requirement_id",
        "requirement",
        errors,
    )
    items = _index_unique(
        freeze["ordered_inventory_items"],
        "inventory_item_id",
        "inventory item",
        errors,
    )
    exclusions = _index_unique(
        freeze["known_exclusions"], "exclusion_id", "exclusion", errors
    )
    ambiguities = _index_unique(
        freeze["unresolved_ambiguities"], "ambiguity_id", "ambiguity", errors
    )
    (
        analysis_index,
        claim_index,
        claim_owner,
        analytical_refs,
        quantitative_units,
        quantitative_denominators,
    ) = _analysis_indexes(analyses)
    evidence_ids = {record["evidence_id"] for record in evidence}

    if projection["projection_status"] != "LOCKED":
        errors.append("Production projection is not LOCKED")
    if projection["previous_projection_ref"] == projection["projection_id"]:
        errors.append("Report projection cannot reference itself as previous")

    binding_pairs = (
        ("request_ref", freeze["reporting_request_ref"]),
        ("contract_ref", freeze["contract_ref"]),
        ("route_ref", freeze["route_ref"]),
        ("freeze_ref", freeze["freeze_id"]),
        ("freeze_sha512", freeze["freeze_sha512"]),
    )
    for field, expected in binding_pairs:
        if projection[field] != expected:
            errors.append(f"Projection {field} differs from frozen boundary")

    analysis_ceilings = {analysis["claim_ceiling"] for analysis in analyses}
    if analysis_ceilings != {projection["claim_ceiling"]}:
        errors.append("Projection claim ceiling differs from source Analysis boundary")

    expected_required_requirements = {
        requirement_id
        for requirement_id, requirement in requirements.items()
        if requirement["required"]
        and requirement["status"] != "EXPLICITLY_EXCLUDED"
    }
    expected_required_items = {
        item_id
        for item_id, item in items.items()
        if item["required"] and item["inclusion_state"] == "INCLUDED"
    }
    if set(projection["required_requirement_refs"]) != expected_required_requirements:
        errors.append("Projection required requirement set mismatch")
    if set(projection["required_inventory_refs"]) != expected_required_items:
        errors.append("Projection required inventory set mismatch")

    for requirement_id in expected_required_requirements:
        status = requirements[requirement_id]["status"]
        if status != "ACTIVE":
            errors.append(f"Required requirement is not ACTIVE: {requirement_id}")
    for item_id in expected_required_items:
        item = items[item_id]
        if item["availability_state"] != "AVAILABLE":
            errors.append(f"Required inventory item is unavailable: {item_id}")
    if ambiguities:
        errors.append("Unresolved analytical ambiguity blocks locked projection")

    transformation_ids = set(transformations)
    element_ids = set(elements)
    requirement_ids = set(requirements)
    inventory_ids = set(items)
    inventory_item_refs = {item["item_ref"] for item in items.values()}
    resolvable_sources = (
        analytical_refs | requirement_ids | inventory_ids | inventory_item_refs
    )
    for transformation_id, transformation in transformations.items():
        _require_refs(
            transformation["source_object_refs"],
            resolvable_sources,
            f"transformation {transformation_id}.source_object_refs",
            errors,
        )
        _require_refs(
            transformation["output_element_refs"],
            element_ids,
            f"transformation {transformation_id}.output_element_refs",
            errors,
        )
        for output_ref in set(transformation["output_element_refs"]) & element_ids:
            output = elements[output_ref]
            if output["transformation_ref"] != transformation_id:
                errors.append(
                    f"Transformation {transformation_id} is not carried by output {output_ref}"
                )

    mapped_required_requirements: set[str] = set()
    mapped_required_items: set[str] = set()
    actual_presentation_only: set[str] = set()
    for element_id, element in elements.items():
        _require_refs(
            element["requirement_refs"],
            requirement_ids,
            f"report element {element_id}.requirement_refs",
            errors,
        )
        _require_refs(
            element["inventory_refs"],
            inventory_ids,
            f"report element {element_id}.inventory_refs",
            errors,
        )

        if element["element_class"] == "PRESENTATION_ONLY":
            actual_presentation_only.add(element_id)
        if element["analytical_completion_credit"]:
            mapped_required_requirements.update(
                set(element["requirement_refs"]) & expected_required_requirements
            )
            mapped_required_items.update(
                set(element["inventory_refs"]) & expected_required_items
            )

        if element["element_class"] in {"PRESENTATION_ONLY", "NAVIGATION"}:
            continue

        _validate_element_lineage(
            element_id,
            element,
            set(analysis_index),
            claim_index,
            claim_owner,
            evidence_ids,
            errors,
        )
        transformation_ref = element["transformation_ref"]
        transformation = transformations.get(transformation_ref)
        if transformation is None:
            errors.append(f"Report element has unresolved transformation: {element_id}")
        else:
            required_sources = set(element["source_analysis_refs"]) | set(
                element["source_claim_refs"]
            )
            if not required_sources <= set(transformation["source_object_refs"]):
                errors.append(f"Transformation source carriage mismatch: {element_id}")
            if element_id not in transformation["output_element_refs"]:
                errors.append(f"Report element absent from transformation output: {element_id}")

        for inventory_ref in element["inventory_refs"]:
            item = items.get(inventory_ref)
            if item is None:
                continue
            if item["source_ref"] in analysis_index and item["source_ref"] not in element[
                "source_analysis_refs"
            ]:
                errors.append(
                    f"Report element omits inventory source Analysis: {element_id}/{inventory_ref}"
                )
            if item["source_ref"] in requirements and item["source_ref"] not in element[
                "requirement_refs"
            ]:
                errors.append(
                    f"Report element omits inventory source requirement: "
                    f"{element_id}/{inventory_ref}"
                )

        _validate_visualization(
            element_id,
            element,
            resolvable_sources,
            quantitative_units,
            quantitative_denominators,
            errors,
        )

    if mapped_required_requirements != expected_required_requirements:
        missing = sorted(expected_required_requirements - mapped_required_requirements)
        errors.append(
            "Required requirements lack analytical completion coverage: "
            + ", ".join(missing)
        )
    if mapped_required_items != expected_required_items:
        missing = sorted(expected_required_items - mapped_required_items)
        errors.append(
            "Required inventory items lack analytical completion coverage: "
            + ", ".join(missing)
        )
    if set(projection["presentation_only_elements"]) != actual_presentation_only:
        errors.append("Projection presentation-only element set mismatch")

    for requirement_id, requirement in requirements.items():
        if not requirement["required"] or requirement["status"] != "ACTIVE":
            continue
        related_elements = [
            element
            for element in elements.values()
            if element["analytical_completion_credit"]
            and requirement_id in element["requirement_refs"]
        ]
        carried_refs = {
            ref
            for element in related_elements
            for ref in (
                element["source_claim_refs"] + element["inventory_refs"]
            )
        }
        missing = set(requirement["claim_or_inventory_refs"]) - carried_refs
        if missing:
            errors.append(
                f"Requirement {requirement_id} source carriage mismatch: "
                + ", ".join(sorted(missing))
            )

    _validate_omissions(
        omissions,
        requirements,
        items,
        exclusions,
        ambiguities,
        expected_required_requirements | expected_required_items,
        errors,
    )
    return errors


def seal_report_projection(
    projection: dict[str, Any],
    freeze: dict[str, Any],
    requirement_inventory: dict[str, Any],
    analysis_records: Iterable[dict[str, Any]],
    evidence_records: Iterable[dict[str, Any]],
    *,
    expected_canonical_binding: dict[str, Any],
    expected_candidate_binding: dict[str, Any],
) -> dict[str, Any]:
    """Return a sealed copy after every projection binding validates."""

    analyses = list(analysis_records)
    evidence = list(evidence_records)
    sealed = copy.deepcopy(projection)
    for element in sealed.get("report_elements", []):
        if isinstance(element, dict):
            element["element_sha512"] = report_element_digest(element)
    sealed["projection_sha512"] = projection_digest(sealed)
    errors = validate_report_projection(
        sealed,
        freeze,
        requirement_inventory,
        analyses,
        evidence,
        expected_canonical_binding=expected_canonical_binding,
        expected_candidate_binding=expected_candidate_binding,
    )
    if errors:
        raise ReportingProjectionError(errors)
    return sealed
