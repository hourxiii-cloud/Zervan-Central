"""Integrity and cross-reference controls for v40 reporting inventories."""

from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from candidate.v40.runtime.reporting_records import (
    canonical_digest,
    validate_analysis_record,
)
from candidate.v40.runtime.schema_validation import SchemaValidationError, validate_schema


ROOT = Path(__file__).resolve().parents[3]
REQUIREMENT_SCHEMA_PATH = (
    ROOT / "candidate/v40/contracts/reporting_requirement_inventory.schema.json"
)
FREEZE_SCHEMA_PATH = ROOT / "candidate/v40/contracts/analytical_inventory_freeze.schema.json"


class ReportingInventoryError(RuntimeError):
    """A reporting inventory failed integrity or cross-reference validation."""

    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@lru_cache(maxsize=2)
def _load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def requirement_inventory_digest(record: dict[str, Any]) -> str:
    """Hash canonical JSON excluding only the requirement inventory digest field."""

    return canonical_digest(record, "requirement_inventory_sha512")


def analytical_inventory_freeze_digest(record: dict[str, Any]) -> str:
    """Hash canonical JSON excluding only the analytical freeze digest field."""

    return canonical_digest(record, "freeze_sha512")


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


def validate_requirement_inventory(record: Any) -> list[str]:
    """Validate one closed requirement inventory and its independent digest."""

    try:
        validate_schema(record, _load_schema(REQUIREMENT_SCHEMA_PATH))
    except (OSError, json.JSONDecodeError, SchemaValidationError) as exc:
        return [f"Requirement inventory schema invalid: {exc}"]

    errors: list[str] = []
    requirements = _index_unique(
        record["requirements"], "requirement_id", "requirement", errors
    )

    sequence_positions: list[int] = []
    for requirement_id, requirement in requirements.items():
        constraint = requirement["ordering_constraint"]
        if constraint is None:
            continue
        sequence_index = constraint["sequence_index"]
        if constraint["constraint_class"] == "SEQUENCE":
            if sequence_index is None:
                errors.append(
                    f"Sequence ordering requirement lacks sequence_index: {requirement_id}"
                )
            else:
                sequence_positions.append(sequence_index)
        elif sequence_index is not None:
            errors.append(
                f"Non-sequence ordering requirement carries sequence_index: {requirement_id}"
            )

    if sequence_positions:
        expected_positions = list(range(1, len(sequence_positions) + 1))
        if sorted(sequence_positions) != expected_positions:
            errors.append(
                "Requirement sequence indexes must be unique and contiguous from 1"
            )

    previous_ref = record["previous_requirement_inventory_ref"]
    if previous_ref == record["requirement_inventory_id"]:
        errors.append("Requirement inventory cannot reference itself as previous")

    try:
        expected_digest = requirement_inventory_digest(record)
    except (TypeError, ValueError) as exc:
        errors.append(f"Requirement inventory canonicalization failed: {exc}")
    else:
        if record["requirement_inventory_sha512"] != expected_digest:
            errors.append(
                f"Requirement inventory digest mismatch: {record['requirement_inventory_id']}"
            )
    return errors


def seal_requirement_inventory(record: dict[str, Any]) -> dict[str, Any]:
    """Return an independently sealed copy of a requirement inventory."""

    sealed = copy.deepcopy(record)
    sealed["requirement_inventory_sha512"] = requirement_inventory_digest(sealed)
    errors = validate_requirement_inventory(sealed)
    if errors:
        raise ReportingInventoryError(errors)
    return sealed


def _analysis_material_refs(
    analysis: dict[str, Any],
) -> tuple[dict[str, set[str]], set[str]]:
    by_class: dict[str, set[str]] = {
        "FINDING": set(analysis["finding_refs"]),
        "COUNT": set(analysis["count_refs"]),
        "DENOMINATOR": set(),
        "IDENTITY": set(analysis["identity_refs"]),
        "METHOD": set(analysis["method_refs"]),
        "LIMITATION": {
            limitation["limitation_id"] for limitation in analysis["limitation_objects"]
        },
        "EVIDENCE": set(analysis["evidence_refs"]),
        "UNCERTAINTY": {
            uncertainty["uncertainty_id"] for uncertainty in analysis["uncertainty_objects"]
        },
        "CONTRADICTION": set(analysis["contradiction_refs"]),
        "CLASSIFICATION": set(analysis["classification_refs"]),
        "FRAMEWORK_MAPPING": set(analysis["framework_mapping_refs"]),
        "RISK_INHERITANCE": {
            edge["edge_id"] for edge in analysis["risk_inheritance_edges"]
        },
        "ORDERING_REQUIREMENT": set(),
    }
    all_refs = {
        analysis["analysis_id"],
        *analysis["eliminated_world_refs"],
        *analysis["surviving_world_refs"],
        *analysis["provenance_refs"],
    }
    for claim in analysis["claim_objects"]:
        all_refs.add(claim["claim_id"])
        semantic = claim["semantic"]
        all_refs.add(semantic["ordering_ref"])
        by_class["ORDERING_REQUIREMENT"].add(semantic["ordering_ref"])
        denominator_ref = semantic["denominator_ref"]
        if denominator_ref is not None:
            all_refs.add(denominator_ref)
            by_class["DENOMINATOR"].add(denominator_ref)
        value_ref = semantic["quantitative"]["value_ref"]
        if value_ref is not None:
            all_refs.add(value_ref)
    for refs in by_class.values():
        all_refs.update(refs)
    return by_class, all_refs


def _expected_material_by_class(
    analyses: Iterable[dict[str, Any]],
) -> tuple[dict[str, set[str]], dict[str, set[str]], set[str]]:
    combined: dict[str, set[str]] = {}
    per_analysis: dict[str, set[str]] = {}
    all_refs: set[str] = set()
    for analysis in analyses:
        by_class, analysis_refs = _analysis_material_refs(analysis)
        per_analysis[analysis["analysis_id"]] = analysis_refs
        all_refs.update(analysis_refs)
        for item_class, refs in by_class.items():
            combined.setdefault(item_class, set()).update(refs)
    return combined, per_analysis, all_refs


def _validate_material_coverage(
    expected_by_class: dict[str, set[str]],
    items: Iterable[dict[str, Any]],
    errors: list[str],
) -> None:
    covered_by_class: dict[str, set[str]] = {}
    for item in items:
        if item["availability_state"] != "AVAILABLE":
            continue
        covered_by_class.setdefault(item["item_class"], set()).add(item["item_ref"])

    for item_class, expected_refs in expected_by_class.items():
        if item_class == "IDENTITY":
            covered = covered_by_class.get("IDENTITY", set()) | covered_by_class.get(
                "RANKED_ENTITY", set()
            )
        else:
            covered = covered_by_class.get(item_class, set())
        missing = sorted(expected_refs - covered)
        if missing:
            errors.append(
                f"Analytical inventory omits {item_class} references: {', '.join(missing)}"
            )


def _validate_requirement_coverage(
    requirements: dict[str, dict[str, Any]],
    items: Iterable[dict[str, Any]],
    errors: list[str],
) -> None:
    referenced_requirements = {
        requirement_ref for item in items for requirement_ref in item["requirement_refs"]
    }
    missing_requirements = sorted(set(requirements) - referenced_requirements)
    if missing_requirements:
        errors.append(
            "Analytical inventory omits requirement references: "
            + ", ".join(missing_requirements)
        )

    class_to_item_classes = {
        "ORDERING": {"ORDERING_REQUIREMENT"},
        "REPORT_ARTIFACT": {"REQUESTED_ARTIFACT"},
        "EVIDENCE_ARTIFACT": {"APPENDIX_OR_EVIDENCE_FILE"},
        "COMPLETION_CRITERION": {"COMPLETION_CRITERION"},
    }
    for requirement_id, requirement in requirements.items():
        if requirement["status"] == "BLOCKED_UNAVAILABLE" and not any(
            item["item_class"] == "KNOWN_UNAVAILABLE"
            and requirement_id in item["requirement_refs"]
            for item in items
        ):
            errors.append(
                f"Blocked requirement lacks KNOWN_UNAVAILABLE inventory item: {requirement_id}"
            )

        expected_item_classes = class_to_item_classes.get(requirement["requirement_class"])
        if expected_item_classes is None:
            continue
        matching_classes = {
            item["item_class"]
            for item in items
            if requirement_id in item["requirement_refs"]
        }
        if not matching_classes & expected_item_classes:
            errors.append(
                f"Requirement {requirement_id} lacks inventory class "
                + "/".join(sorted(expected_item_classes))
            )


def _validate_exclusions(
    items: dict[str, dict[str, Any]],
    exclusions: dict[str, dict[str, Any]],
    requirements: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    decision_sources: dict[tuple[str, str], set[str]] = {}
    for requirement_id, requirement in requirements.items():
        if requirement["status"] != "EXPLICITLY_EXCLUDED":
            continue
        for candidate in (
            requirement_id,
            requirement["source_ref"],
            requirement["exclusion_ref"],
        ):
            if candidate is None:
                continue
            decision_sources.setdefault(
                (candidate, requirement["source_class"]), set()
            ).add(requirement_id)

    for item_id, item in items.items():
        exclusion_ref = item["exclusion_ref"]
        if item["inclusion_state"] == "EXCLUDED":
            if exclusion_ref not in exclusions:
                errors.append(f"Excluded item has unresolved exclusion: {item_id}")
            elif item_id not in exclusions[exclusion_ref]["inventory_item_refs"]:
                errors.append(
                    f"Excluded item is absent from reciprocal exclusion: {item_id}"
                )

    for exclusion_id, exclusion in exclusions.items():
        for item_ref in exclusion["inventory_item_refs"]:
            item = items.get(item_ref)
            if item is None:
                errors.append(
                    f"Exclusion {exclusion_id} has unresolved inventory item: {item_ref}"
                )
                continue
            if item["inclusion_state"] != "EXCLUDED":
                errors.append(
                    f"Exclusion {exclusion_id} references included item: {item_ref}"
                )
            elif item["exclusion_ref"] != exclusion_id:
                errors.append(
                    f"Exclusion {exclusion_id} is not carried reciprocally by item {item_ref}"
                )
        decision_key = (
            exclusion["decision_ref"],
            exclusion["decision_source_class"],
        )
        decision_requirement_ids = decision_sources.get(decision_key, set())
        if not decision_requirement_ids:
            errors.append(f"Exclusion decision is unresolved: {exclusion_id}")
            continue
        for item_ref in exclusion["inventory_item_refs"]:
            item = items.get(item_ref)
            if item is not None and not (
                set(item["requirement_refs"]) & decision_requirement_ids
            ):
                errors.append(
                    f"Excluded item lacks its exclusion requirement: {item_ref}"
                )


def _validate_cross_analysis_object_ids(
    analyses: Iterable[dict[str, Any]],
    errors: list[str],
) -> None:
    seen: dict[tuple[str, str], str] = {}
    object_sets = (
        ("claim", "claim_objects", "claim_id"),
        ("uncertainty", "uncertainty_objects", "uncertainty_id"),
        ("limitation", "limitation_objects", "limitation_id"),
        ("risk-inheritance edge", "risk_inheritance_edges", "edge_id"),
    )
    for analysis in analyses:
        analysis_id = analysis["analysis_id"]
        for label, collection_field, identifier_field in object_sets:
            for value in analysis[collection_field]:
                identifier = value[identifier_field]
                key = (label, identifier)
                prior_analysis = seen.get(key)
                if prior_analysis is not None:
                    errors.append(
                        f"Duplicate cross-Analysis {label} identifier: {identifier} "
                        f"({prior_analysis}, {analysis_id})"
                    )
                else:
                    seen[key] = analysis_id


def _validate_ambiguities(
    items: dict[str, dict[str, Any]],
    ambiguities: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    for item_id, item in items.items():
        for ambiguity_ref in item["ambiguity_refs"]:
            ambiguity = ambiguities.get(ambiguity_ref)
            if ambiguity is None:
                errors.append(
                    f"Item {item_id} has unresolved ambiguity: {ambiguity_ref}"
                )
            elif item_id not in ambiguity["inventory_item_refs"]:
                errors.append(
                    f"Item {item_id} is absent from reciprocal ambiguity {ambiguity_ref}"
                )

    for ambiguity_id, ambiguity in ambiguities.items():
        for item_ref in ambiguity["inventory_item_refs"]:
            item = items.get(item_ref)
            if item is None:
                errors.append(
                    f"Ambiguity {ambiguity_id} has unresolved inventory item: {item_ref}"
                )
            elif ambiguity_id not in item["ambiguity_refs"]:
                errors.append(
                    f"Ambiguity {ambiguity_id} is not carried reciprocally by item {item_ref}"
                )


def validate_analytical_inventory_freeze(
    freeze: Any,
    requirement_inventory: Any,
    analysis_records: Iterable[dict[str, Any]],
    evidence_records: Iterable[dict[str, Any]],
    *,
    expected_canonical_binding: dict[str, Any],
    expected_candidate_binding: dict[str, Any],
) -> list[str]:
    """Validate a freeze against its requirements, analyses, evidence, and Git bindings."""

    analyses = list(analysis_records)
    evidence = list(evidence_records)
    requirement_errors = validate_requirement_inventory(requirement_inventory)
    errors = [
        f"requirement_inventory: {error}"
        for error in requirement_errors
    ]

    analysis_index: dict[str, dict[str, Any]] = {}
    for position, analysis in enumerate(analyses):
        analysis_errors = validate_analysis_record(analysis, evidence)
        errors.extend(f"analysis[{position}]: {error}" for error in analysis_errors)
        if isinstance(analysis, dict) and isinstance(analysis.get("analysis_id"), str):
            analysis_id = analysis["analysis_id"]
            if analysis_id in analysis_index:
                errors.append(f"Duplicate source Analysis identifier: {analysis_id}")
            elif not analysis_errors:
                analysis_index[analysis_id] = analysis

    try:
        validate_schema(freeze, _load_schema(FREEZE_SCHEMA_PATH))
    except (OSError, json.JSONDecodeError, SchemaValidationError) as exc:
        errors.append(f"Analytical inventory freeze schema invalid: {exc}")
        return errors

    if not isinstance(requirement_inventory, dict):
        errors.append("Requirement inventory is unavailable for freeze binding")
        return errors
    if any(
        error.startswith("Requirement inventory schema invalid:")
        for error in requirement_errors
    ):
        return errors

    requirements = _index_unique(
        requirement_inventory.get("requirements", []),
        "requirement_id",
        "requirement",
        errors,
    )
    declared_analyses = _index_unique(
        freeze["source_analysis_records"],
        "analysis_id",
        "freeze source Analysis",
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

    item_refs: dict[str, str] = {}
    for item_id, item in items.items():
        prior = item_refs.get(item["item_ref"])
        if prior is not None:
            errors.append(
                f"Duplicate inventory item_ref: {item['item_ref']} ({prior}, {item_id})"
            )
        else:
            item_refs[item["item_ref"]] = item_id

    expected_positions = list(range(1, len(freeze["ordered_inventory_items"]) + 1))
    actual_positions = [
        item["ordering_index"] for item in freeze["ordered_inventory_items"]
    ]
    if actual_positions != expected_positions:
        errors.append("Inventory ordering indexes must match contiguous array order from 1")

    if freeze["previous_freeze_ref"] == freeze["freeze_id"]:
        errors.append("Analytical inventory freeze cannot reference itself as previous")

    if freeze["canonical_git_binding"] != expected_canonical_binding:
        errors.append("Analytical inventory canonical Git binding mismatch")
    if freeze["candidate_git_binding"] != expected_candidate_binding:
        errors.append("Analytical inventory candidate Git binding mismatch")

    bindings = (
        ("contract_ref", "contract_ref"),
        ("reporting_request_ref", "reporting_request_ref"),
        ("route_ref", "route_ref"),
    )
    for freeze_field, requirement_field in bindings:
        if freeze[freeze_field] != requirement_inventory.get(requirement_field):
            errors.append(f"Freeze {freeze_field} differs from requirement inventory")

    if freeze["requirement_inventory_ref"] != requirement_inventory.get(
        "requirement_inventory_id"
    ):
        errors.append("Freeze requirement inventory identifier mismatch")
    if freeze["requirement_inventory_sha512"] != requirement_inventory.get(
        "requirement_inventory_sha512"
    ):
        errors.append("Freeze requirement inventory digest mismatch")

    _require_refs(
        set(declared_analyses),
        set(analysis_index),
        "freeze.source_analysis_records",
        errors,
    )
    _require_refs(
        set(analysis_index),
        set(declared_analyses),
        "provided source analyses absent from freeze",
        errors,
    )
    for analysis_id, declaration in declared_analyses.items():
        analysis = analysis_index.get(analysis_id)
        if analysis is None:
            continue
        if declaration["analysis_sha512"] != analysis.get("analysis_sha512"):
            errors.append(f"Freeze source Analysis digest mismatch: {analysis_id}")
        if declaration["status"] != analysis.get("status"):
            errors.append(f"Freeze source Analysis status mismatch: {analysis_id}")
        if declaration["status"] != "FROZEN":
            errors.append(f"Freeze source Analysis is not FROZEN: {analysis_id}")
        actual_claim_refs = {
            claim["claim_id"] for claim in analysis.get("claim_objects", [])
        }
        if set(declaration["claim_refs"]) != actual_claim_refs:
            errors.append(f"Freeze source Analysis claim set mismatch: {analysis_id}")
        if analysis.get("contract_ref") != freeze["contract_ref"]:
            errors.append(f"Source Analysis contract mismatch: {analysis_id}")
        if analysis.get("route_ref") != freeze["route_ref"]:
            errors.append(f"Source Analysis route mismatch: {analysis_id}")

    _validate_cross_analysis_object_ids(analysis_index.values(), errors)

    expected_by_class, per_analysis_refs, analytical_refs = _expected_material_by_class(
        analysis_index.values()
    )
    requirement_ids = set(requirements)
    inventory_ids = set(items)
    inventory_item_refs = set(item_refs)
    ambiguity_ids = set(ambiguities)
    exclusion_ids = set(exclusions)
    resolvable_refs = (
        analytical_refs
        | requirement_ids
        | inventory_ids
        | inventory_item_refs
        | ambiguity_ids
        | exclusion_ids
    )

    for requirement_id, requirement in requirements.items():
        _require_refs(
            requirement["claim_or_inventory_refs"],
            analytical_refs | inventory_ids | inventory_item_refs,
            f"requirement {requirement_id}.claim_or_inventory_refs",
            errors,
        )

    for item_id, item in items.items():
        _require_refs(
            item["requirement_refs"],
            requirement_ids,
            f"inventory item {item_id}.requirement_refs",
            errors,
        )
        _require_refs(
            item["dependency_refs"],
            resolvable_refs,
            f"inventory item {item_id}.dependency_refs",
            errors,
        )
        source_ref = item["source_ref"]
        if source_ref in analysis_index:
            analysis = analysis_index[source_ref]
            if item["availability_state"] == "AVAILABLE":
                if item["source_sha512"] != analysis["analysis_sha512"]:
                    errors.append(f"Inventory item source digest mismatch: {item_id}")
                if item["item_ref"] not in per_analysis_refs[source_ref]:
                    errors.append(
                        f"Inventory item is absent from source Analysis: {item_id}"
                    )
        elif source_ref in requirements:
            if item["availability_state"] == "AVAILABLE" and item[
                "source_sha512"
            ] != requirement_inventory.get("requirement_inventory_sha512"):
                errors.append(f"Inventory item requirement digest mismatch: {item_id}")
            if source_ref not in item["requirement_refs"]:
                errors.append(
                    f"Requirement-sourced item omits its source requirement: {item_id}"
                )
        else:
            errors.append(f"Inventory item has unresolved source_ref: {item_id}")

    _validate_material_coverage(
        expected_by_class, freeze["ordered_inventory_items"], errors
    )
    _validate_requirement_coverage(
        requirements, freeze["ordered_inventory_items"], errors
    )
    _validate_exclusions(items, exclusions, requirements, errors)
    _validate_ambiguities(items, ambiguities, errors)

    try:
        expected_digest = analytical_inventory_freeze_digest(freeze)
    except (TypeError, ValueError) as exc:
        errors.append(f"Analytical inventory canonicalization failed: {exc}")
    else:
        if freeze["freeze_sha512"] != expected_digest:
            errors.append(f"Analytical inventory digest mismatch: {freeze['freeze_id']}")
    return errors


def validate_reporting_inventories(
    freeze: Any,
    requirement_inventory: Any,
    analysis_records: Iterable[dict[str, Any]],
    evidence_records: Iterable[dict[str, Any]],
    *,
    expected_canonical_binding: dict[str, Any],
    expected_candidate_binding: dict[str, Any],
) -> list[str]:
    """Validate the complete pre-projection reporting inventory boundary."""

    return validate_analytical_inventory_freeze(
        freeze,
        requirement_inventory,
        analysis_records,
        evidence_records,
        expected_canonical_binding=expected_canonical_binding,
        expected_candidate_binding=expected_candidate_binding,
    )


def seal_analytical_inventory_freeze(
    freeze: dict[str, Any],
    requirement_inventory: dict[str, Any],
    analysis_records: Iterable[dict[str, Any]],
    evidence_records: Iterable[dict[str, Any]],
    *,
    expected_canonical_binding: dict[str, Any],
    expected_candidate_binding: dict[str, Any],
) -> dict[str, Any]:
    """Return a sealed copy after all freeze bindings validate."""

    analyses = list(analysis_records)
    evidence = list(evidence_records)
    sealed = copy.deepcopy(freeze)
    sealed["freeze_sha512"] = analytical_inventory_freeze_digest(sealed)
    errors = validate_analytical_inventory_freeze(
        sealed,
        requirement_inventory,
        analyses,
        evidence,
        expected_canonical_binding=expected_canonical_binding,
        expected_candidate_binding=expected_candidate_binding,
    )
    if errors:
        raise ReportingInventoryError(errors)
    return sealed
