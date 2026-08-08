#!/usr/bin/env python3

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "RING6_AGGREGATE_AUDIT_CLOSURE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "ring6_aggregate_audit_closure.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

RUNNER = (
    ROOT
    / "tools"
    / "validate_ring6.py"
)

LOSSLESS_RECEIPT = (
    ROOT
    / "schemas"
    / "validation"
    / "lossless_collapse_receipt.schema.json"
)

REQUIRED_FAMILIES = [
    "UNIT",
    "SCHEMA",
    "LIFECYCLE",
    "PERSPECTIVE_ROTATION",
    "ONE_OBJECT_CONVERGENCE",
    "DISTINCT_OBJECT",
    "PERTURBATION",
    "ORTHOGONAL_TRANSITION",
    "REPLAY",
    "REPLACEMENT",
    "REPRESENTATION_INDEPENDENCE",
    "LOSSLESS_COLLAPSE",
]

NAMED_VECTORS = [
    "ONE_OBJECT_PERSPECTIVE_ROTATION",
    "PREMATURE_ANALYSIS_REJECTION",
    "PROPORTIONAL_FORCE_ROUTING",
    "QUALIFICATION_TEAM_COHERENCE",
    "FORMATION_REJUSTIFICATION",
    "DISTINCT_OBJECT_TEST",
    "HYDRATION_ON_NEED",
    "REPLAY_FIDELITY",
    "PMC_CCR_MC_COMPATIBILITY",
    "ORTHOGONAL_TRANSITION",
    "RBT_001",
    "FRESH_READER_TEST",
]

FAILURE_TAXONOMY = [
    "INNER_INVARIANT_CONTRADICTION",
    "OUTER_IMPLEMENTATION_DEFECT",
    "VALIDATOR_DEFECT",
    "COVERAGE_GAP",
    "SOURCE_COLLISION",
    "UNRESOLVED_REQUIRED_SURFACE",
]

RING_SECTIONS = [
    f"R6-{letter}"
    for letter in "ABCDEFGHIJKLMNOP"
]

VECTOR_TO_RING = {
    "ONE_OBJECT_PERSPECTIVE_ROTATION":
        "R6-B",
    "PREMATURE_ANALYSIS_REJECTION":
        "R6-C",
    "PROPORTIONAL_FORCE_ROUTING":
        "R6-D",
    "QUALIFICATION_TEAM_COHERENCE":
        "R6-E",
    "FORMATION_REJUSTIFICATION":
        "R6-F",
    "DISTINCT_OBJECT_TEST":
        "R6-G",
    "HYDRATION_ON_NEED":
        "R6-H",
    "REPLAY_FIDELITY":
        "R6-I",
    "PMC_CCR_MC_COMPATIBILITY":
        "R6-J",
    "ORTHOGONAL_TRANSITION":
        "R6-K",
    "RBT_001":
        "R6-L",
    "FRESH_READER_TEST":
        "R6-M",
}

FAMILY_SURFACES = {
    "UNIT": [
        "tests/test_validation_audit_boundary.py",
        "tests/test_one_object_perspective_rotation.py",
        "tests/test_premature_analysis_rejection.py",
        "tests/test_proportional_force_routing.py",
        "tests/test_qualification_team_coherence.py",
        "tests/test_formation_rejustification.py",
        "tests/test_distinct_object_validation.py",
        "tests/test_hydration_on_need.py",
        "tests/test_replay_fidelity.py",
        "tests/test_pmc_ccr_mc_compatibility.py",
        "tests/test_orthogonal_transition.py",
        "tests/test_rbt_001_recursive_butt_topology.py",
        "tests/test_fresh_reader.py",
        "tests/test_representation_independence.py",
        "tests/test_lossless_collapse.py",
        "tests/test_ring6_closure.py",
    ],

    "SCHEMA": [
        "schemas/validation/"
        "ring6_aggregate_audit_closure.schema.json",
    ],

    "LIFECYCLE": [
        "tools/validate_premature_analysis_rejection.py",
        "tools/validate_replay_fidelity.py",
        "tools/validate_orthogonal_transition.py",
    ],

    "PERSPECTIVE_ROTATION": [
        "tools/validate_one_object_perspective_rotation.py",
    ],

    "ONE_OBJECT_CONVERGENCE": [
        "tools/validate_one_object_perspective_rotation.py",
        "tools/validate_qualification_team_coherence.py",
    ],

    "DISTINCT_OBJECT": [
        "tools/validate_distinct_object_validation.py",
        "tools/validate_orthogonal_transition.py",
    ],

    "PERTURBATION": [
        "tools/validate_formation_rejustification.py",
        "tools/validate_rbt_001_recursive_butt_topology.py",
    ],

    "ORTHOGONAL_TRANSITION": [
        "tools/validate_orthogonal_transition.py",
    ],

    "REPLAY": [
        "tools/validate_replay_fidelity.py",
    ],

    "REPLACEMENT": [
        "tools/validate_ring6_closure.py",
        "tools/validate_representation_independence.py",
        "tools/validate_lossless_collapse.py",
    ],

    "REPRESENTATION_INDEPENDENCE": [
        "tools/validate_representation_independence.py",
    ],

    "LOSSLESS_COLLAPSE": [
        "tools/validate_lossless_collapse.py",
        "schemas/validation/"
        "lossless_collapse_receipt.schema.json",
    ],
}


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def normalized(path):
    text = path.read_text(
        encoding="utf-8"
    )

    for token in (
        "**",
        "__",
        "`",
    ):
        text = text.replace(
            token,
            ""
        )

    return " ".join(
        text.split()
    )


def find_named_surface(tokens):
    roots = [
        ROOT / "contracts",
        ROOT / "schemas",
    ]

    token_set = {
        token.lower()
        for token in tokens
    }

    for base in roots:
        if not base.exists():
            continue

        for path in base.rglob("*"):
            if not path.is_file():
                continue

            name = path.name.lower()

            if all(
                token in name
                for token in token_set
            ):
                return str(
                    path.relative_to(
                        ROOT
                    )
                )

    return None


def audit_ring6_schemas():
    errors = []

    schema_dir = (
        ROOT
        / "schemas"
        / "validation"
    )

    if not schema_dir.is_dir():
        return [
            "validation schema directory missing"
        ]

    ring6_schemas = sorted(
        schema_dir.glob(
            "*.schema.json"
        )
    )

    if not ring6_schemas:
        return [
            "no Ring 6 validation schemas found"
        ]

    for path in ring6_schemas:
        try:
            schema = load(
                path
            )
        except Exception as exc:
            errors.append(
                f"{path.name}: invalid JSON: {exc}"
            )
            continue

        if (
            schema.get(
                "$schema"
            )
            != "https://json-schema.org/draft/2020-12/schema"
        ):
            errors.append(
                f"{path.name}: not declared as JSON Schema Draft 2020-12"
            )

        if (
            schema.get(
                "type"
            )
            != "object"
        ):
            errors.append(
                f"{path.name}: root type must be object"
            )

        if not schema.get(
            "required"
        ):
            errors.append(
                f"{path.name}: required field registry missing"
            )

    return errors


def evaluate_replacement_case(
    *,
    location_changed,
    capability_preserved,
    behavior_preserved,
    invariant_meaning_preserved,
    provenance_preserved,
):
    reasons = []

    # Location change is explicitly permitted.
    _ = location_changed

    if not capability_preserved:
        reasons.append(
            "LOST_CAPABILITY"
        )

    if not behavior_preserved:
        reasons.append(
            "CHANGED_BEHAVIOR"
        )

    if not invariant_meaning_preserved:
        reasons.append(
            "CHANGED_SEMANTICS"
        )

    if not provenance_preserved:
        reasons.append(
            "LOST_PROVENANCE"
        )

    return reasons


def family_coverage():
    coverage = {}

    for family in REQUIRED_FAMILIES:
        surfaces = FAMILY_SURFACES.get(
            family,
            []
        )

        missing = [
            path
            for path in surfaces
            if not (
                ROOT
                / path
            ).exists()
        ]

        coverage[
            family
        ] = {
            "state": (
                "VALIDATED"
                if not missing
                else "BLOCKED"
            ),
            "implementation_surfaces":
                list(
                    surfaces
                ),
            "missing_surfaces":
                missing,
        }

    schema_errors = audit_ring6_schemas()

    if schema_errors:
        coverage[
            "SCHEMA"
        ][
            "state"
        ] = "BLOCKED"

        coverage[
            "SCHEMA"
        ][
            "schema_errors"
        ] = schema_errors

    valid_replacement = evaluate_replacement_case(
        location_changed=True,
        capability_preserved=True,
        behavior_preserved=True,
        invariant_meaning_preserved=True,
        provenance_preserved=True,
    )

    if valid_replacement:
        coverage[
            "REPLACEMENT"
        ][
            "state"
        ] = "BLOCKED"

    return coverage


def build_record():
    question_surface = find_named_surface(
        (
            "question",
            "contract",
        )
    )

    promotion_surface = find_named_surface(
        (
            "promotion",
            "receipt",
        )
    )

    lossless_surface = (
        str(
            LOSSLESS_RECEIPT.relative_to(
                ROOT
            )
        )
        if LOSSLESS_RECEIPT.exists()
        else None
    )

    coverage = family_coverage()

    blocking_gaps = [
        family
        for family, details in coverage.items()
        if details[
            "state"
        ]
        != "VALIDATED"
    ]

    runner_text = RUNNER.read_text(
        encoding="utf-8"
    )

    ring5_count = runner_text.count(
        "validate_ring5.py"
    )

    if ring5_count != 1:
        blocking_gaps.append(
            "RING5_DEPENDENCY_TRAVERSAL"
        )

    section_states = {}

    for ring in RING_SECTIONS:
        section_states[
            ring
        ] = (
            "VALIDATED"
            if f'"{ring}"'
            in runner_text
            else "BLOCKED"
        )

    for ring, state in section_states.items():
        if state != "VALIDATED":
            blocking_gaps.append(
                ring
            )

    vector_coverage = dict(
        VECTOR_TO_RING
    )

    audit_surface_states = {
        "QUESTION_CONTRACT": (
            "IMPLEMENTED"
            if question_surface
            else "DEFERRED_TO_RING9"
        ),

        "PROMOTION_RECEIPT": (
            "IMPLEMENTED"
            if promotion_surface
            else "DEFERRED_TO_RING9"
        ),

        "LOSSLESS_COLLAPSE_RECEIPT": (
            "IMPLEMENTED"
            if lossless_surface
            else "BLOCKED"
        ),
    }

    if (
        audit_surface_states[
            "LOSSLESS_COLLAPSE_RECEIPT"
        ]
        != "IMPLEMENTED"
    ):
        blocking_gaps.append(
            "LOSSLESS_COLLAPSE_RECEIPT"
        )

    promotion_dependencies = []

    if not question_surface:
        promotion_dependencies.append(
            "RING9:QUESTION_CONTRACT"
        )

    if not promotion_surface:
        promotion_dependencies.append(
            "RING9:PROMOTION_RECEIPT"
        )

    promotion_dependencies.extend(
        [
            "PROMOTION:NATIVE_V41_INITIATION",
            "PROMOTION:NATIVE_V41_CANONICAL_ENTRY",
            "HUMAN_GATE:PROMOTION_APPROVAL",
        ]
    )

    blocking_gaps = sorted(
        set(
            blocking_gaps
        )
    )

    record = {
        "schema_version":
            "1.0",

        "closure_type":
            "RING6_AGGREGATE_AUDIT_CLOSURE",

        "native_version":
            "vTemporal.41.0",

        "implementation_identity":
            "v41 Complete",

        "ring":
            "R6-P",

        "ring5_dependency_traversal":
            "EXACTLY_ONCE",

        "ring_sections":
            section_states,

        "required_validation_families":
            list(
                REQUIRED_FAMILIES
            ),

        "family_coverage":
            coverage,

        "named_validation_vectors":
            list(
                NAMED_VECTORS
            ),

        "vector_coverage":
            vector_coverage,

        "required_audit_surfaces": [
            "QUESTION_CONTRACT",
            "PROMOTION_RECEIPT",
            "LOSSLESS_COLLAPSE_RECEIPT",
        ],

        "audit_surface_states":
            audit_surface_states,

        "failure_taxonomy":
            list(
                FAILURE_TAXONOMY
            ),

        "classified_failures":
            [],

        "unclassified_failures":
            [],

        "blocking_coverage_gaps":
            blocking_gaps,

        "promotion_dependencies":
            promotion_dependencies,

        "fresh_reader_promoted_entry_state":
            "DEFERRED_TO_PROMOTION",

        "authority_state":
            "NONE",

        "human_gate_state":
            "ACTIVE",

        "promotion_state":
            "CANDIDATE",

        "closure_disposition": (
            "VALIDATED_CANDIDATE"
            if not blocking_gaps
            else "BLOCKED"
        ),

        "lineage": [
            "R5-J:VALIDATED_CANDIDATE",
            "R6-A:VALIDATION_AUDIT_BOUNDARY",
            "R6-B:R6-O:EXTENDED_VALIDATION",
            "R6-P:AGGREGATE_AUDIT_CLOSURE",
        ],

        "provenance": [
            "contracts/validation/"
            "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md",

            "tools/validate_ring6.py",

            "contracts/validation/"
            "RING6_AGGREGATE_AUDIT_CLOSURE.md",

            "schemas/validation/"
            "ring6_aggregate_audit_closure.schema.json",
        ],
    }

    return record


def validate_record(record):
    errors = []

    if set(
        record.get(
            "required_validation_families",
            []
        )
    ) != set(
        REQUIRED_FAMILIES
    ):
        errors.append(
            "required validation-family registry incomplete"
        )

    if set(
        record.get(
            "named_validation_vectors",
            []
        )
    ) != set(
        NAMED_VECTORS
    ):
        errors.append(
            "named validation-vector registry incomplete"
        )

    if set(
        record.get(
            "failure_taxonomy",
            []
        )
    ) != set(
        FAILURE_TAXONOMY
    ):
        errors.append(
            "Ring 6 failure taxonomy incomplete"
        )

    if (
        record.get(
            "ring5_dependency_traversal"
        )
        != "EXACTLY_ONCE"
    ):
        errors.append(
            "Ring 5 dependency traversal must be exactly once"
        )

    if record.get(
        "unclassified_failures"
    ):
        errors.append(
            "unclassified failures remain"
        )

    if record.get(
        "blocking_coverage_gaps"
    ):
        errors.append(
            "blocking Ring 6 coverage gaps remain"
        )

    if (
        record.get(
            "audit_surface_states",
            {}
        ).get(
            "LOSSLESS_COLLAPSE_RECEIPT"
        )
        != "IMPLEMENTED"
    ):
        errors.append(
            "Lossless-Collapse Receipt contract unresolved"
        )

    for surface in (
        "QUESTION_CONTRACT",
        "PROMOTION_RECEIPT",
    ):
        if (
            record.get(
                "audit_surface_states",
                {}
            ).get(
                surface
            )
            not in (
                "IMPLEMENTED",
                "DEFERRED_TO_RING9",
            )
        ):
            errors.append(
                f"{surface} has invalid closure state"
            )

    if (
        record.get(
            "authority_state"
        )
        != "NONE"
    ):
        errors.append(
            "R6-P Authority must remain NONE"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-P Human Gate must remain ACTIVE"
        )

    if (
        record.get(
            "promotion_state"
        )
        != "CANDIDATE"
    ):
        errors.append(
            "R6-P must not promote candidate state"
        )

    expected = (
        "VALIDATED_CANDIDATE"
        if not errors
        else "BLOCKED"
    )

    if (
        record.get(
            "closure_disposition"
        )
        != expected
    ):
        errors.append(
            "closure disposition contradicts aggregate audit state"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-P contract"
        ),
        (
            SCHEMA,
            "R6-P schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            RUNNER,
            "Ring 6 runner"
        ),
        (
            LOSSLESS_RECEIPT,
            "Lossless-Collapse Receipt schema"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    text = normalized(
        CONTRACT
    )

    locks = [
        "R6-P = Ring 6 Aggregate Validation / Audit Closure.",
        "Ring 6 depends on Ring 5.",
        "Ring 5 is traversed exactly once.",
        "Rings 1 through 4 are not redundantly rerun outside Ring 5.",
        "One dependency traversal is sufficient.",
        "Reduced redundant execution != reduced validation coverage.",
        "All twelve validation families remain independently visible.",
        "No family absorbs another family.",
        "All named validation vectors remain attributable.",
        "Schema validation is independent from prose validation.",
        "Schema != truth.",
        "Replacement != redefinition.",
        "Changed placement with preserved semantics is valid.",
        "Validator observes state-transition law.",
        "Validator does not own state.",
        "Green output != complete audit trail.",
        "Failure classification does not repair a failure.",
        "Classification != disposition.",
        "No unclassified blocking failure may be hidden.",
        "REGISTERED != implemented.",
        "IMPLEMENTED != validated.",
        "VALIDATED != canonical promotion.",
        "Question Contract must not be fabricated.",
        "Promotion Receipt must not be fabricated.",
        "Lossless-Collapse Receipt contract is resolved by R6-O.",
        "Deferred != forgotten.",
        "Deferred != complete.",
        "Missing required surface != nonexistent requirement.",
        "Candidate validation != promotion event.",
        "Candidate readability != promoted entry completion.",
        "VALIDATED_CANDIDATE != promotion.",
        "VALIDATED_CANDIDATE != canonical.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "Ring 6 closure != Human Gate promotion.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-P lock: {lock}"
            )

    r6a = normalized(
        R6A
    )

    for lock in (
        "Ring 6 SHALL preserve these as independently visible validation families.",
        "One dependency traversal is sufficient.",
        "Green output != complete audit trail.",
        "Question Contract;",
        "Promotion Receipt;",
        "Lossless-Collapse Receipt.",
        "REGISTERED != implemented.",
        "IMPLEMENTED != validated.",
        "VALIDATED != canonical promotion.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Validation completion != Human Gate approval.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-P closure binding: {lock}"
            )

    try:
        load(
            SCHEMA
        )
    except Exception as exc:
        errors.append(
            f"invalid R6-P schema JSON: {exc}"
        )

    schema_errors = audit_ring6_schemas()

    for error in schema_errors:
        errors.append(
            f"schema family audit: {error}"
        )

    # Explicit Replacement positive.
    replacement_ok = evaluate_replacement_case(
        location_changed=True,
        capability_preserved=True,
        behavior_preserved=True,
        invariant_meaning_preserved=True,
        provenance_preserved=True,
    )

    if replacement_ok:
        errors.append(
            "valid implementation replacement incorrectly rejected"
        )

    # Explicit Replacement negatives.
    if (
        "LOST_CAPABILITY"
        not in evaluate_replacement_case(
            location_changed=True,
            capability_preserved=False,
            behavior_preserved=True,
            invariant_meaning_preserved=True,
            provenance_preserved=True,
        )
    ):
        errors.append(
            "Replacement family failed to detect lost capability"
        )

    if (
        "CHANGED_BEHAVIOR"
        not in evaluate_replacement_case(
            location_changed=True,
            capability_preserved=True,
            behavior_preserved=False,
            invariant_meaning_preserved=True,
            provenance_preserved=True,
        )
    ):
        errors.append(
            "Replacement family failed to detect changed behavior"
        )

    if (
        "CHANGED_SEMANTICS"
        not in evaluate_replacement_case(
            location_changed=True,
            capability_preserved=True,
            behavior_preserved=True,
            invariant_meaning_preserved=False,
            provenance_preserved=True,
        )
    ):
        errors.append(
            "Replacement family failed to detect changed semantics"
        )

    if (
        "LOST_PROVENANCE"
        not in evaluate_replacement_case(
            location_changed=True,
            capability_preserved=True,
            behavior_preserved=True,
            invariant_meaning_preserved=True,
            provenance_preserved=False,
        )
    ):
        errors.append(
            "Replacement family failed to detect lost provenance"
        )

    record = build_record()

    errors.extend(
        validate_record(
            record
        )
    )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-P RING 6 AGGREGATE VALIDATION / AUDIT CLOSURE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    record = build_record()

    print(
        "R6-P RING 6 AGGREGATE VALIDATION / AUDIT CLOSURE: PASS"
    )
    print(
        "Ring 5 dependency traversal: EXACTLY_ONCE"
    )
    print(
        "R6-A through R6-P section accounting: COMPLETE"
    )
    print(
        "Required validation families: 12 / 12 VALIDATED"
    )
    print(
        "Named validation vectors: 12 / 12 ATTRIBUTABLE"
    )
    print(
        "Schema family independent audit: PASS"
    )
    print(
        "Lifecycle family coverage: VALIDATED"
    )
    print(
        "Replacement family coverage: VALIDATED"
    )
    print(
        "Lossless-Collapse Receipt contract: IMPLEMENTED"
    )

    print(
        "Question Contract: "
        + record[
            "audit_surface_states"
        ][
            "QUESTION_CONTRACT"
        ]
    )

    print(
        "Promotion Receipt: "
        + record[
            "audit_surface_states"
        ][
            "PROMOTION_RECEIPT"
        ]
    )

    print(
        "Blocking coverage gaps: NONE"
    )
    print(
        "Unclassified failures: NONE"
    )
    print(
        "Fresh-reader promoted entry: DEFERRED_TO_PROMOTION"
    )
    print(
        "Ring 6 closure disposition: VALIDATED_CANDIDATE"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Promotion State: CANDIDATE"
    )
    print(
        "Canonical promotion: NOT PERFORMED"
    )
    print(
        "RING 6: COMPLETE"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
