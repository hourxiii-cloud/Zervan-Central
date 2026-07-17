"""Integrity and cross-reference controls for v40 Evidence and Analysis records."""

from __future__ import annotations

import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from candidate.v40.runtime.schema_validation import SchemaValidationError, validate_schema


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE_SCHEMA_PATH = ROOT / "candidate/v40/contracts/evidence_record.schema.json"
ANALYSIS_SCHEMA_PATH = ROOT / "candidate/v40/contracts/analysis_record.schema.json"
RISK_RANK = {
    "ANOMALY": 0,
    "THREAT": 1,
    "HIDDEN_THREAT": 2,
    "INSIDER_THREAT": 3,
    "OFFENDING_ID": 4,
}


class ReportingRecordError(RuntimeError):
    """A reporting-boundary record failed integrity or reference validation."""

    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@lru_cache(maxsize=2)
def _load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: Any) -> bytes:
    """Serialize canonical JSON without accepting NaN or Infinity."""

    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def canonical_digest(value: dict[str, Any], digest_field: str) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop(digest_field, None)
    return hashlib.sha512(canonical_bytes(unhashed)).hexdigest()


def evidence_digest(record: dict[str, Any]) -> str:
    return canonical_digest(record, "evidence_sha512")


def semantic_digest(semantic: dict[str, Any]) -> str:
    return canonical_digest(semantic, "semantic_sha512")


def analysis_digest(record: dict[str, Any]) -> str:
    return canonical_digest(record, "analysis_sha512")


def validate_evidence_record(record: Any) -> list[str]:
    errors: list[str] = []
    try:
        validate_schema(record, _load_schema(EVIDENCE_SCHEMA_PATH))
    except (OSError, json.JSONDecodeError, SchemaValidationError) as exc:
        return [f"Evidence schema invalid: {exc}"]
    try:
        expected = evidence_digest(record)
    except (TypeError, ValueError) as exc:
        errors.append(f"Evidence canonicalization failed: {exc}")
    else:
        if record["evidence_sha512"] != expected:
            errors.append(f"Evidence digest mismatch: {record['evidence_id']}")
    return errors


def _index_unique(
    values: list[dict[str, Any]],
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


def _validate_attribution(
    attribution: dict[str, Any],
    label: str,
    claim_ids: set[str],
    method_refs: set[str],
    errors: list[str],
) -> None:
    source_claim_ref = attribution["source_claim_ref"]
    if source_claim_ref is not None and source_claim_ref not in claim_ids:
        errors.append(f"{label}.source_claim_ref is unresolved: {source_claim_ref}")
    transformations = set(attribution["transformation_refs"])
    _require_refs(transformations, method_refs, f"{label}.transformation_refs", errors)
    if attribution["origin_class"] == "SYSTEM_DERIVED" and not transformations:
        errors.append(f"{label} SYSTEM_DERIVED origin requires a transformation reference")


def _validate_analysis_cross_references(
    analysis: dict[str, Any],
    evidence_ids: set[str],
    errors: list[str],
) -> None:
    claims = _index_unique(analysis["claim_objects"], "claim_id", "claim", errors)
    uncertainties = _index_unique(
        analysis["uncertainty_objects"], "uncertainty_id", "uncertainty", errors
    )
    limitations = _index_unique(
        analysis["limitation_objects"], "limitation_id", "limitation", errors
    )
    edges = _index_unique(
        analysis["risk_inheritance_edges"], "edge_id", "risk-inheritance edge", errors
    )

    claim_ids = set(claims)
    uncertainty_ids = set(uncertainties)
    limitation_ids = set(limitations)
    edge_ids = set(edges)
    analysis_evidence_ids = set(analysis["evidence_refs"])
    method_refs = set(analysis["method_refs"])

    _require_refs(
        analysis_evidence_ids,
        evidence_ids,
        "analysis.evidence_refs",
        errors,
    )
    _validate_attribution(
        analysis["attribution"],
        "analysis.attribution",
        claim_ids,
        method_refs,
        errors,
    )

    for claim_id, claim in claims.items():
        semantic = claim["semantic"]
        try:
            expected_semantic_digest = semantic_digest(semantic)
        except (TypeError, ValueError) as exc:
            errors.append(f"Claim semantic canonicalization failed for {claim_id}: {exc}")
        else:
            if semantic["semantic_sha512"] != expected_semantic_digest:
                errors.append(f"Claim semantic digest mismatch: {claim_id}")

        if semantic["claim_ceiling"] != analysis["claim_ceiling"]:
            errors.append(f"Claim ceiling differs from analysis ceiling: {claim_id}")

        claim_evidence = set(claim["evidence_refs"])
        _require_refs(claim_evidence, evidence_ids, f"claim {claim_id}.evidence_refs", errors)
        _require_refs(
            claim_evidence,
            analysis_evidence_ids,
            f"claim {claim_id}.evidence_refs outside analysis boundary",
            errors,
        )
        _require_refs(
            claim["uncertainty_refs"],
            uncertainty_ids,
            f"claim {claim_id}.uncertainty_refs",
            errors,
        )
        _require_refs(
            claim["limitation_refs"],
            limitation_ids,
            f"claim {claim_id}.limitation_refs",
            errors,
        )
        _require_refs(
            claim["contradiction_refs"],
            set(analysis["contradiction_refs"]),
            f"claim {claim_id}.contradiction_refs",
            errors,
        )
        _require_refs(
            semantic["inheritance_refs"],
            edge_ids,
            f"claim {claim_id}.semantic.inheritance_refs",
            errors,
        )
        for edge_ref in semantic["inheritance_refs"]:
            edge = edges.get(edge_ref)
            if edge is not None and edge["to_claim_ref"] != claim_id:
                errors.append(f"Claim {claim_id} references non-target inheritance edge: {edge_ref}")

        _validate_attribution(
            claim["attribution"],
            f"claim {claim_id}.attribution",
            claim_ids,
            method_refs,
            errors,
        )

    for uncertainty_id, uncertainty in uncertainties.items():
        affected_claims = set(uncertainty["affected_claim_refs"])
        _require_refs(
            affected_claims,
            claim_ids,
            f"uncertainty {uncertainty_id}.affected_claim_refs",
            errors,
        )
        uncertainty_evidence = set(uncertainty["evidence_refs"])
        _require_refs(
            uncertainty_evidence,
            evidence_ids,
            f"uncertainty {uncertainty_id}.evidence_refs",
            errors,
        )
        _require_refs(
            uncertainty_evidence,
            analysis_evidence_ids,
            f"uncertainty {uncertainty_id}.evidence_refs outside analysis boundary",
            errors,
        )
        for claim_id in affected_claims & claim_ids:
            if uncertainty_id not in claims[claim_id]["uncertainty_refs"]:
                errors.append(
                    f"Uncertainty {uncertainty_id} is not carried reciprocally by claim {claim_id}"
                )
    for claim_id, claim in claims.items():
        for uncertainty_ref in set(claim["uncertainty_refs"]) & uncertainty_ids:
            if claim_id not in uncertainties[uncertainty_ref]["affected_claim_refs"]:
                errors.append(
                    f"Claim {claim_id} is absent from uncertainty {uncertainty_ref}.affected_claim_refs"
                )

    for limitation_id, limitation in limitations.items():
        affected_claims = set(limitation["affected_claim_refs"])
        _require_refs(
            affected_claims,
            claim_ids,
            f"limitation {limitation_id}.affected_claim_refs",
            errors,
        )
        limitation_evidence = set(limitation["evidence_refs"])
        _require_refs(
            limitation_evidence,
            evidence_ids,
            f"limitation {limitation_id}.evidence_refs",
            errors,
        )
        _require_refs(
            limitation_evidence,
            analysis_evidence_ids,
            f"limitation {limitation_id}.evidence_refs outside analysis boundary",
            errors,
        )
        for claim_id in affected_claims & claim_ids:
            if limitation_id not in claims[claim_id]["limitation_refs"]:
                errors.append(
                    f"Limitation {limitation_id} is not carried reciprocally by claim {claim_id}"
                )
    for claim_id, claim in claims.items():
        for limitation_ref in set(claim["limitation_refs"]) & limitation_ids:
            if claim_id not in limitations[limitation_ref]["affected_claim_refs"]:
                errors.append(
                    f"Claim {claim_id} is absent from limitation {limitation_ref}.affected_claim_refs"
                )

    for edge_id, edge in edges.items():
        source_id = edge["from_claim_ref"]
        target_id = edge["to_claim_ref"]
        _require_refs([source_id], claim_ids, f"edge {edge_id}.from_claim_ref", errors)
        _require_refs([target_id], claim_ids, f"edge {edge_id}.to_claim_ref", errors)
        if source_id == target_id:
            errors.append(f"Risk-inheritance edge cannot self-reference: {edge_id}")

        edge_evidence = set(edge["evidence_refs"])
        _require_refs(edge_evidence, evidence_ids, f"edge {edge_id}.evidence_refs", errors)
        _require_refs(
            edge_evidence,
            analysis_evidence_ids,
            f"edge {edge_id}.evidence_refs outside analysis boundary",
            errors,
        )

        source = claims.get(source_id)
        target = claims.get(target_id)
        if source is not None:
            _require_refs(
                edge_evidence,
                set(source["evidence_refs"]),
                f"edge {edge_id}.evidence_refs absent from source claim",
                errors,
            )
        if target is not None:
            _require_refs(
                edge_evidence,
                set(target["evidence_refs"]),
                f"edge {edge_id}.evidence_refs absent from target claim",
                errors,
            )
            if edge_id not in target["semantic"]["inheritance_refs"]:
                errors.append(f"Target claim {target_id} does not carry inheritance edge {edge_id}")

        if edge["inheritance_class"] == "RISK_ESCALATION" and source is not None and target is not None:
            source_risk = source["semantic"]["risk_category"]
            target_risk = target["semantic"]["risk_category"]
            if source_risk not in RISK_RANK or target_risk not in RISK_RANK:
                errors.append(f"Risk-escalation edge uses a non-hierarchical category: {edge_id}")
            elif RISK_RANK[target_risk] <= RISK_RANK[source_risk]:
                errors.append(f"Risk-escalation edge does not advance risk: {edge_id}")


def validate_analysis_record(
    analysis: Any,
    evidence_records: Iterable[dict[str, Any]],
) -> list[str]:
    records = list(evidence_records)
    errors: list[str] = []
    evidence_index: dict[str, dict[str, Any]] = {}
    for position, record in enumerate(records):
        record_errors = validate_evidence_record(record)
        errors.extend(f"evidence[{position}]: {error}" for error in record_errors)
        if isinstance(record, dict) and isinstance(record.get("evidence_id"), str):
            identifier = record["evidence_id"]
            if identifier in evidence_index:
                errors.append(f"Duplicate Evidence identifier: {identifier}")
            else:
                evidence_index[identifier] = record

    try:
        validate_schema(analysis, _load_schema(ANALYSIS_SCHEMA_PATH))
    except (OSError, json.JSONDecodeError, SchemaValidationError) as exc:
        errors.append(f"Analysis schema invalid: {exc}")
        return errors

    _validate_analysis_cross_references(analysis, set(evidence_index), errors)
    try:
        expected = analysis_digest(analysis)
    except (TypeError, ValueError) as exc:
        errors.append(f"Analysis canonicalization failed: {exc}")
    else:
        if analysis["analysis_sha512"] != expected:
            errors.append(f"Analysis digest mismatch: {analysis['analysis_id']}")
    return errors


def validate_reporting_records(
    evidence_records: Iterable[dict[str, Any]],
    analysis: Any,
) -> list[str]:
    return validate_analysis_record(analysis, evidence_records)


def seal_evidence_record(record: dict[str, Any]) -> dict[str, Any]:
    sealed = copy.deepcopy(record)
    sealed["evidence_sha512"] = evidence_digest(sealed)
    errors = validate_evidence_record(sealed)
    if errors:
        raise ReportingRecordError(errors)
    return sealed


def seal_analysis_record(
    analysis: dict[str, Any],
    evidence_records: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    records = list(evidence_records)
    sealed = copy.deepcopy(analysis)
    for claim in sealed.get("claim_objects", []):
        semantic = claim.get("semantic") if isinstance(claim, dict) else None
        if isinstance(semantic, dict):
            semantic["semantic_sha512"] = semantic_digest(semantic)
    sealed["analysis_sha512"] = analysis_digest(sealed)
    errors = validate_analysis_record(sealed, records)
    if errors:
        raise ReportingRecordError(errors)
    return sealed
