#!/usr/bin/env python3

from __future__ import annotations

from typing import Any


ASSERTION_STRENGTH = {
    "OBSERVATION": 0,
    "POSSIBLE": 1,
    "PLAUSIBLE": 2,
    "PROBABLE": 3,
    "ESTABLISHED": 4,
}

SUPPORT_STRENGTH = {
    "UNKNOWN": 0,
    "UNRESOLVED": 1,
    "CONTRADICTED": 1,
    "PARTIALLY_SUPPORTED": 2,
    "SUPPORTED": 3,
}

CAUSAL_STRENGTH = {
    "NONE": 0,
    "ASSOCIATION": 1,
    "CONTRIBUTORY": 2,
    "CAUSAL": 3,
}

UNCERTAINTY_STRENGTH = {
    "UNKNOWN": 0,
    "MATERIAL": 1,
    "BOUNDED": 2,
    "RESOLVED": 3,
}

TRUTH_POSTURE = {
    "UNKNOWN": 0,
    "INFERRED": 1,
    "OBSERVED": 2,
    "ESTABLISHED": 3,
}


class EvidenceCeilingSemanticError(ValueError):
    pass


def _require_mapping(
    value: Any,
    name: str,
) -> dict:
    if not isinstance(value, dict):
        raise EvidenceCeilingSemanticError(
            f"{name} must be an object"
        )
    return value


def _required(
    claim: dict,
    field: str,
) -> Any:
    if field not in claim:
        raise EvidenceCeilingSemanticError(
            f"missing semantic field: {field}"
        )
    return claim[field]


def _rank(
    table: dict[str, int],
    value: Any,
    field: str,
) -> int:
    if value not in table:
        raise EvidenceCeilingSemanticError(
            f"invalid {field}: {value!r}"
        )
    return table[value]


def _unique_list(
    claim: dict,
    field: str,
) -> list:
    value = _required(
        claim,
        field,
    )

    if not isinstance(value, list):
        raise EvidenceCeilingSemanticError(
            f"{field} must be an array"
        )

    if len(value) != len(
        {
            repr(item)
            for item in value
        }
    ):
        raise EvidenceCeilingSemanticError(
            f"{field} must not contain duplicates"
        )

    return value


def validate_claim_shape(
    claim: dict,
) -> list[str]:
    reasons: list[str] = []

    required_fields = (
        "claim_id",
        "subject",
        "predicate",
        "object",
        "polarity",
        "assertion_strength",
        "support_state",
        "causal_posture",
        "uncertainty_state",
        "surviving_alternatives",
        "temporal_scope",
        "evidence_refs",
        "evidence_boundary_ref",
        "evidence_ceiling_ref",
        "provenance_refs",
        "source_analytical_state_ref",
        "truth_posture",
        "cryptographic_integrity_valid",
    )

    for field in required_fields:
        if field not in claim:
            reasons.append(
                f"MISSING_FIELD:{field}"
            )

    return reasons


def compare_semantics(
    source_claim: dict,
    downstream_claim: dict,
) -> list[str]:
    """
    Return AC-10 semantic violations.

    Empty list means the downstream claim does not exceed the
    source/evidence-supported semantic ceiling represented here.
    """

    source = _require_mapping(
        source_claim,
        "source_claim",
    )
    target = _require_mapping(
        downstream_claim,
        "downstream_claim",
    )

    reasons: list[str] = []

    reasons.extend(
        validate_claim_shape(
            source
        )
    )
    reasons.extend(
        validate_claim_shape(
            target
        )
    )

    if reasons:
        return sorted(
            set(reasons)
        )

    # Claim identity/content semantics may not silently change.
    for field in (
        "subject",
        "predicate",
        "object",
        "polarity",
    ):
        if source[field] != target[field]:
            reasons.append(
                f"CLAIM_SEMANTIC_DRIFT:{field}"
            )

    # AR-050 / AR-053:
    # metadata preservation does not permit stronger language.
    if _rank(
        ASSERTION_STRENGTH,
        target["assertion_strength"],
        "assertion_strength",
    ) > _rank(
        ASSERTION_STRENGTH,
        source["assertion_strength"],
        "assertion_strength",
    ):
        reasons.append(
            "ASSERTION_STRENGTH_EXCEEDS_CEILING"
        )

    # Support cannot be strengthened downstream without a new
    # attributable evidentiary state.
    if _rank(
        SUPPORT_STRENGTH,
        target["support_state"],
        "support_state",
    ) > _rank(
        SUPPORT_STRENGTH,
        source["support_state"],
        "support_state",
    ):
        reasons.append(
            "SUPPORT_STATE_STRENGTHENED"
        )

    # Correlation/association may not become causation merely
    # through representation.
    if _rank(
        CAUSAL_STRENGTH,
        target["causal_posture"],
        "causal_posture",
    ) > _rank(
        CAUSAL_STRENGTH,
        source["causal_posture"],
        "causal_posture",
    ):
        reasons.append(
            "CAUSAL_POSTURE_STRENGTHENED"
        )

    # AR-052 / AR-042:
    # downstream representation/collapse may not silently remove
    # material uncertainty.
    if _rank(
        UNCERTAINTY_STRENGTH,
        target["uncertainty_state"],
        "uncertainty_state",
    ) > _rank(
        UNCERTAINTY_STRENGTH,
        source["uncertainty_state"],
        "uncertainty_state",
    ):
        reasons.append(
            "UNCERTAINTY_SILENTLY_REDUCED"
        )

    source_alternatives = _unique_list(
        source,
        "surviving_alternatives",
    )
    target_alternatives = _unique_list(
        target,
        "surviving_alternatives",
    )

    if not set(
        map(repr, target_alternatives)
    ).issuperset(
        set(
            map(
                repr,
                source_alternatives,
            )
        )
    ):
        reasons.append(
            "SURVIVING_ALTERNATIVES_REMOVED"
        )

    # AR-013:
    # a downstream rendering of historical analytical state may not
    # silently substitute a later analytical state or time scope.
    if (
        source["source_analytical_state_ref"]
        != target["source_analytical_state_ref"]
    ):
        reasons.append(
            "HISTORICAL_ANALYTICAL_STATE_SUBSTITUTED"
        )

    if (
        source["temporal_scope"]
        != target["temporal_scope"]
    ):
        reasons.append(
            "TEMPORAL_SCOPE_CHANGED"
        )

    # Boundary and ceiling metadata still must remain stable.
    if (
        source["evidence_boundary_ref"]
        != target["evidence_boundary_ref"]
    ):
        reasons.append(
            "EVIDENCE_BOUNDARY_CHANGED"
        )

    if (
        source["evidence_ceiling_ref"]
        != target["evidence_ceiling_ref"]
    ):
        reasons.append(
            "EVIDENCE_CEILING_REFERENCE_CHANGED"
        )

    source_evidence = set(
        map(
            repr,
            _unique_list(
                source,
                "evidence_refs",
            ),
        )
    )
    target_evidence = set(
        map(
            repr,
            _unique_list(
                target,
                "evidence_refs",
            ),
        )
    )

    if target_evidence != source_evidence:
        reasons.append(
            "EVIDENCE_SET_CHANGED"
        )

    source_provenance = set(
        map(
            repr,
            _unique_list(
                source,
                "provenance_refs",
            ),
        )
    )
    target_provenance = set(
        map(
            repr,
            _unique_list(
                target,
                "provenance_refs",
            ),
        )
    )

    if not target_provenance.issuperset(
        source_provenance
    ):
        reasons.append(
            "PROVENANCE_LOST"
        )

    # AR-027:
    # cryptographic validity cannot promote semantic truth.
    if (
        target["cryptographic_integrity_valid"]
        and _rank(
            TRUTH_POSTURE,
            target["truth_posture"],
            "truth_posture",
        )
        > _rank(
            TRUTH_POSTURE,
            source["truth_posture"],
            "truth_posture",
        )
    ):
        reasons.append(
            "CRYPTOGRAPHIC_VALIDITY_PROMOTED_TO_TRUTH"
        )

    return sorted(
        set(reasons)
    )


def validate_enforcement_record(
    record: dict,
) -> list[str]:
    record = _require_mapping(
        record,
        "record",
    )

    reasons: list[str] = []

    if record.get(
        "schema_version"
    ) != "1.0":
        reasons.append(
            "SCHEMA_VERSION_INVALID"
        )

    if record.get(
        "activation_control"
    ) != "AC-10":
        reasons.append(
            "ACTIVATION_CONTROL_INVALID"
        )

    if record.get(
        "authority_state"
    ) != "NONE":
        reasons.append(
            "AUTHORITY_PROMOTED"
        )

    if record.get(
        "human_gate_state"
    ) != "ACTIVE":
        reasons.append(
            "HUMAN_GATE_DISABLED"
        )

    source = record.get(
        "source_claim"
    )
    downstream = record.get(
        "downstream_claim"
    )

    if not isinstance(
        source,
        dict,
    ):
        reasons.append(
            "SOURCE_CLAIM_INVALID"
        )

    if not isinstance(
        downstream,
        dict,
    ):
        reasons.append(
            "DOWNSTREAM_CLAIM_INVALID"
        )

    if isinstance(
        source,
        dict,
    ) and isinstance(
        downstream,
        dict,
    ):
        reasons.extend(
            compare_semantics(
                source,
                downstream,
            )
        )

    return sorted(
        set(reasons)
    )


def main() -> int:
    print(
        "AC-10 EVIDENCE-CEILING SEMANTIC VALIDATOR: READY"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
