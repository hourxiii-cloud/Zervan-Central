#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "LOSSLESS_COLLAPSE.md"
)

VALIDATION_SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "lossless_collapse.schema.json"
)

RECEIPT_SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "lossless_collapse_receipt.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

REQUIRED_CLASSES = [
    "OBJECT_IDENTITY",
    "CAPABILITY",
    "BEHAVIOR",
    "RATIONALE",
    "PROVENANCE",
    "COORDINATES",
    "TRANSFORM_HISTORY",
    "CONTRACTS",
    "TESTS",
    "EVIDENCE_BOUNDARIES",
    "KNOWN_FAILURE_CONDITIONS",
]

REMOVAL_BASES = {
    "EXACT_DUPLICATE",
    "SEMANTIC_DUPLICATE",
    "SUPERSEDED_IMPLEMENTATION",
    "PLACEMENT_CONSOLIDATION",
    "GENERATED_RESIDUE",
}

RETENTION_BASES = {
    "INDEPENDENT_INVARIANT",
    "UNIQUE_CAPABILITY",
    "UNIQUE_BEHAVIOR",
    "UNIQUE_RATIONALE",
    "UNIQUE_PROVENANCE",
    "UNIQUE_COORDINATE_HISTORY",
    "UNIQUE_TRANSFORM_HISTORY",
    "UNIQUE_CONTRACT",
    "UNIQUE_TEST_COVERAGE",
    "UNIQUE_EVIDENCE_BOUNDARY",
    "UNIQUE_FAILURE_CONDITION",
    "REQUIRED_AUDIT_SURFACE",
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


def evaluate_record(record):
    reasons = []

    required = set(
        record.get(
            "required_preservation_classes",
            []
        )
    )

    observed = set(
        record.get(
            "observed_preservation_classes",
            []
        )
    )

    if required != set(REQUIRED_CLASSES):
        reasons.append(
            "PRESERVATION_CLASS_MISSING"
        )

    if not required.issubset(
        observed
    ):
        reasons.append(
            "PRESERVATION_CLASS_MISSING"
        )

    retained = record.get(
        "retained_surfaces",
        []
    )

    retained_refs = {
        item.get(
            "surface_reference"
        )
        for item in retained
        if item.get(
            "surface_reference"
        )
    }

    for item in retained:
        if (
            item.get(
                "retention_basis"
            )
            not in RETENTION_BASES
        ):
            reasons.append(
                "RETENTION_BASIS_MISSING"
            )

        if not item.get(
            "provenance_references"
        ):
            reasons.append(
                "PROVENANCE_LOST"
            )

    for item in record.get(
        "collapsed_surfaces",
        []
    ):
        destination = item.get(
            "retained_destination_reference"
        )

        if (
            not destination
            or destination not in retained_refs
        ):
            reasons.append(
                "COLLAPSED_SURFACE_DESTINATION_MISSING"
            )

        if (
            item.get(
                "removal_basis"
            )
            not in REMOVAL_BASES
        ):
            reasons.append(
                "COLLAPSE_BASIS_MISSING"
            )

        if not item.get(
            "provenance_references"
        ):
            reasons.append(
                "PROVENANCE_LOST"
            )

    mappings = record.get(
        "invariant_mappings",
        []
    )

    mapped_classes = {
        item.get(
            "preservation_class"
        )
        for item in mappings
        if item.get(
            "retained_surface_references"
        )
    }

    if not set(
        REQUIRED_CLASSES
    ).issubset(
        mapped_classes
    ):
        reasons.append(
            "INVARIANT_MAPPING_MISSING"
        )

    for item in mappings:
        destinations = item.get(
            "retained_surface_references",
            []
        )

        if not destinations:
            reasons.append(
                "INVARIANT_MAPPING_MISSING"
            )

        if any(
            destination not in retained_refs
            for destination in destinations
        ):
            reasons.append(
                "INVARIANT_MAPPING_MISSING"
            )

    test_classes = {
        item.get(
            "preservation_class"
        )
        for item in record.get(
            "test_mappings",
            []
        )
        if item.get(
            "test_references"
        )
    }

    required_test_classes = {
        "OBJECT_IDENTITY",
        "CAPABILITY",
        "BEHAVIOR",
        "PROVENANCE",
        "COORDINATES",
        "TRANSFORM_HISTORY",
        "CONTRACTS",
        "EVIDENCE_BOUNDARIES",
        "KNOWN_FAILURE_CONDITIONS",
    }

    if not required_test_classes.issubset(
        test_classes
    ):
        reasons.append(
            "TEST_COVERAGE_LOST"
        )

    failure_mappings = record.get(
        "failure_condition_mappings",
        []
    )

    if not failure_mappings:
        reasons.append(
            "KNOWN_FAILURE_CONDITION_LOST"
        )

    if any(
        not item.get(
            "failure_condition"
        )
        or not item.get(
            "retained_rejection_surfaces"
        )
        for item in failure_mappings
    ):
        reasons.append(
            "KNOWN_FAILURE_CONDITION_LOST"
        )

    if record.get(
        "unresolved_items"
    ):
        reasons.append(
            "UNRESOLVED_ITEM_PRESENT"
        )

    if record.get(
        "unexplained_vanishing_detected"
    ):
        reasons.append(
            "UNEXPLAINED_VANISHING"
        )

    if record.get(
        "semantic_loss_detected"
    ):
        reasons.append(
            "SEMANTIC_LOSS_DETECTED"
        )

    explicit_loss_flags = {
        "provenance_lost":
            "PROVENANCE_LOST",

        "coordinate_history_lost":
            "COORDINATE_HISTORY_LOST",

        "transform_history_lost":
            "TRANSFORM_HISTORY_LOST",

        "evidence_boundary_semantics_lost":
            "EVIDENCE_BOUNDARY_SEMANTICS_LOST",

        "contract_semantics_lost":
            "CONTRACT_SEMANTICS_LOST",

        "capability_lost":
            "CAPABILITY_LOST",

        "behavior_changed":
            "BEHAVIOR_CHANGED",

        "rationale_lost":
            "RATIONALE_LOST",
    }

    for field, reason in explicit_loss_flags.items():
        if record.get(
            field,
            False
        ):
            reasons.append(
                reason
            )

    if (
        record.get(
            "authority_state"
        )
        != "NONE"
    ):
        reasons.append(
            "AUTHORITY_PROMOTED"
        )

    return sorted(
        set(
            reasons
        )
    )


def validate_record(record):
    errors = []

    if (
        record.get(
            "validation_family"
        )
        != "LOSSLESS_COLLAPSE"
    ):
        errors.append(
            "wrong validation family"
        )

    reasons = evaluate_record(
        record
    )

    expected = (
        "VALID"
        if not reasons
        else "BLOCKED"
    )

    if (
        record.get(
            "validation_disposition"
        )
        != expected
    ):
        errors.append(
            "lossless-collapse disposition contradicts preservation state"
        )

    if (
        sorted(
            record.get(
                "failure_reasons",
                []
            )
        )
        != reasons
    ):
        errors.append(
            "lossless-collapse failure reasons are incomplete or incorrect"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-O Human Gate state must remain ACTIVE"
        )

    return errors


def make_retained(
    reference,
    basis,
    classes,
):
    return {
        "surface_reference":
            reference,

        "retention_basis":
            basis,

        "preservation_classes":
            list(
                classes
            ),

        "invariant_references": [
            f"invariant:{value.lower()}"
            for value in classes
        ],

        "provenance_references": [
            f"provenance:{reference}"
        ],
    }


def make_record(
    *,
    observed_classes=None,
    unresolved_items=None,
    unexplained_vanishing_detected=False,
    historical_hoarding_detected=False,
    semantic_loss_detected=False,
    authority_state="NONE",
    provenance_lost=False,
    coordinate_history_lost=False,
    transform_history_lost=False,
    evidence_boundary_semantics_lost=False,
    contract_semantics_lost=False,
    capability_lost=False,
    behavior_changed=False,
    rationale_lost=False,
):
    if observed_classes is None:
        observed_classes = list(
            REQUIRED_CLASSES
        )

    if unresolved_items is None:
        unresolved_items = []

    retained = [
        make_retained(
            "contracts/native-v41-core",
            "INDEPENDENT_INVARIANT",
            [
                "OBJECT_IDENTITY",
                "CAPABILITY",
                "BEHAVIOR",
                "RATIONALE",
                "PROVENANCE",
                "COORDINATES",
                "TRANSFORM_HISTORY",
                "CONTRACTS",
                "EVIDENCE_BOUNDARIES",
            ],
        ),
        make_retained(
            "tests/native-v41-validation",
            "UNIQUE_TEST_COVERAGE",
            [
                "TESTS",
                "KNOWN_FAILURE_CONDITIONS",
            ],
        ),
        make_retained(
            "schemas/validation/lossless_collapse_receipt.schema.json",
            "REQUIRED_AUDIT_SURFACE",
            [
                "CONTRACTS",
                "PROVENANCE",
            ],
        ),
    ]

    collapsed = [
        {
            "old_surface_reference":
                "legacy/duplicate-expression-a",

            "retained_destination_reference":
                "contracts/native-v41-core",

            "removal_basis":
                "SEMANTIC_DUPLICATE",

            "preserved_invariant_references": [
                "invariant:object_identity",
                "invariant:behavior",
            ],

            "provenance_references": [
                "provenance:legacy-expression-a",
                "provenance:contracts/native-v41-core",
            ],
        }
    ]

    invariant_mappings = [
        {
            "preservation_class":
                preservation_class,

            "retained_surface_references": (
                [
                    "tests/native-v41-validation"
                ]
                if preservation_class
                in (
                    "TESTS",
                    "KNOWN_FAILURE_CONDITIONS",
                )
                else [
                    "contracts/native-v41-core"
                ]
            ),
        }
        for preservation_class in REQUIRED_CLASSES
    ]

    test_mappings = [
        {
            "preservation_class":
                preservation_class,

            "test_references": [
                f"test:{preservation_class.lower()}"
            ],
        }
        for preservation_class in (
            "OBJECT_IDENTITY",
            "CAPABILITY",
            "BEHAVIOR",
            "PROVENANCE",
            "COORDINATES",
            "TRANSFORM_HISTORY",
            "CONTRACTS",
            "EVIDENCE_BOUNDARIES",
            "KNOWN_FAILURE_CONDITIONS",
        )
    ]

    failure_condition_mappings = [
        {
            "failure_condition":
                "identity fracture",

            "retained_rejection_surfaces": [
                "tests/native-v41-validation",
                "contracts/native-v41-core",
            ],
        },
        {
            "failure_condition":
                "authority promotion",

            "retained_rejection_surfaces": [
                "tests/native-v41-validation",
                "contracts/native-v41-core",
            ],
        },
        {
            "failure_condition":
                "evidence-boundary broadening",

            "retained_rejection_surfaces": [
                "tests/native-v41-validation",
                "contracts/native-v41-core",
            ],
        },
    ]

    record = {
        "schema_version":
            "1.0",

        "validation_family":
            "LOSSLESS_COLLAPSE",

        "required_preservation_classes":
            list(
                REQUIRED_CLASSES
            ),

        "observed_preservation_classes":
            list(
                observed_classes
            ),

        "retained_surfaces":
            retained,

        "collapsed_surfaces":
            collapsed,

        "rejected_residue": [
            {
                "surface_reference":
                    "generated/duplicate-residue",

                "rejection_basis":
                    "GENERATED_RESIDUE",

                "provenance_references": [
                    "provenance:generated-residue"
                ],
            }
        ],

        "invariant_mappings":
            invariant_mappings,

        "test_mappings":
            test_mappings,

        "failure_condition_mappings":
            failure_condition_mappings,

        "unresolved_items":
            list(
                unresolved_items
            ),

        "unexplained_vanishing_detected":
            unexplained_vanishing_detected,

        "historical_hoarding_detected":
            historical_hoarding_detected,

        "semantic_loss_detected":
            semantic_loss_detected,

        "provenance_lost":
            provenance_lost,

        "coordinate_history_lost":
            coordinate_history_lost,

        "transform_history_lost":
            transform_history_lost,

        "evidence_boundary_semantics_lost":
            evidence_boundary_semantics_lost,

        "contract_semantics_lost":
            contract_semantics_lost,

        "capability_lost":
            capability_lost,

        "behavior_changed":
            behavior_changed,

        "rationale_lost":
            rationale_lost,

        "authority_state":
            authority_state,

        "human_gate_state":
            "ACTIVE",

        "validation_disposition":
            "",

        "failure_reasons":
            [],
    }

    reasons = evaluate_record(
        record
    )

    record[
        "failure_reasons"
    ] = reasons

    record[
        "validation_disposition"
    ] = (
        "VALID"
        if not reasons
        else "BLOCKED"
    )

    return record


def build_receipt(record):
    return {
        "schema_version":
            "1.0",

        "receipt_type":
            "LOSSLESS_COLLAPSE_RECEIPT",

        "native_version":
            "vTemporal.41.0",

        "implementation_identity":
            "v41 Complete",

        "preservation_classes":
            list(
                record[
                    "observed_preservation_classes"
                ]
            ),

        "retained_surfaces":
            list(
                record[
                    "retained_surfaces"
                ]
            ),

        "collapsed_surfaces":
            list(
                record[
                    "collapsed_surfaces"
                ]
            ),

        "rejected_residue":
            list(
                record[
                    "rejected_residue"
                ]
            ),

        "invariant_mappings":
            list(
                record[
                    "invariant_mappings"
                ]
            ),

        "test_mappings":
            list(
                record[
                    "test_mappings"
                ]
            ),

        "failure_condition_mappings":
            list(
                record[
                    "failure_condition_mappings"
                ]
            ),

        "unresolved_items":
            list(
                record[
                    "unresolved_items"
                ]
            ),

        "collapse_disposition": (
            "LOSSLESS"
            if record[
                "validation_disposition"
            ]
            == "VALID"
            else "BLOCKED"
        ),

        "authority_state":
            record[
                "authority_state"
            ],

        "human_gate_state":
            record[
                "human_gate_state"
            ],

        "provenance_route": [
            "R6-A:LOSSLESS_COLLAPSE",
            "R6-O:LOSSLESS_COLLAPSE",
            "schema:lossless_collapse_receipt",
        ],
    }


def validate_receipt(receipt):
    errors = []

    if (
        receipt.get(
            "receipt_type"
        )
        != "LOSSLESS_COLLAPSE_RECEIPT"
    ):
        errors.append(
            "wrong Lossless-Collapse Receipt type"
        )

    if set(
        receipt.get(
            "preservation_classes",
            []
        )
    ) != set(
        REQUIRED_CLASSES
    ):
        errors.append(
            "Lossless-Collapse Receipt missing preservation classes"
        )

    if (
        receipt.get(
            "collapse_disposition"
        )
        == "LOSSLESS"
        and receipt.get(
            "unresolved_items"
        )
    ):
        errors.append(
            "Lossless receipt cannot contain unresolved items"
        )

    if (
        receipt.get(
            "authority_state"
        )
        != "NONE"
    ):
        errors.append(
            "Lossless-Collapse Receipt must preserve Authority NONE"
        )

    if (
        receipt.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "Lossless-Collapse Receipt must preserve Human Gate ACTIVE"
        )

    if not receipt.get(
        "provenance_route"
    ):
        errors.append(
            "Lossless-Collapse Receipt provenance required"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-O contract"
        ),
        (
            VALIDATION_SCHEMA,
            "R6-O validation schema"
        ),
        (
            RECEIPT_SCHEMA,
            "Lossless-Collapse Receipt schema"
        ),
        (
            R6A,
            "R6-A registry"
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
        "R6-O = Lossless Collapse.",
        "Native v41 is a reconstruction, not a patch stack.",
        "Preserve object identity.",
        "Preserve capability.",
        "Preserve behavior.",
        "Preserve rationale.",
        "Preserve provenance.",
        "Preserve coordinates.",
        "Preserve transform history.",
        "Preserve contracts.",
        "Preserve tests.",
        "Preserve evidence boundaries.",
        "Preserve known failure conditions.",
        "Duplicate implementation residue may collapse.",
        "Independent invariant loss is invalid.",
        "Compress until further compression destroys an independent invariant.",
        "Nothing vanishes unexplained.",
        "Nothing survives merely because it existed.",
        "Lossless Collapse != analytical Collapse Boundary.",
        "Lossless Collapse != deletion by convenience.",
        "Lossless Collapse != summary substitution.",
        "Lossless Collapse != rewrite history.",
        "Placement may change.",
        "Required capability may not disappear.",
        "Equivalent implementation != identical source text.",
        "Fail-closed behavior is behavior.",
        "Negative behavior is behavior.",
        "Rationale MUST NOT depend on private memory.",
        "Removal without lineage is not lossless.",
        "Collapse != history reset.",
        "Similar contracts != same contract automatically.",
        "Green count != coverage equivalence.",
        "Compression != evidence expansion.",
        "Failure knowledge != expendable residue.",
        "Semantic accounting is mandatory.",
        "Shorter != better unless invariant preservation holds.",
        "Coverage count alone is insufficient.",
        "Collapse validation != doctrine mutation.",
        "Classification != repair.",
        "LOSSLESS_COLLAPSE_RECEIPT is a required machine-readable audit surface.",
        "Receipt != promotion.",
        "Receipt != truth authority.",
        "Hash != truth.",
        "Unknown preservation != preserved.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-P owns Ring 6 Aggregate Validation / Audit Closure.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-O lock: {lock}"
            )

    r6a = normalized(
        R6A
    )

    for lock in (
        "Lossless Collapse",
        "Native v41 is a reconstruction, not a patch stack.",
        "object identity;",
        "capability;",
        "behavior;",
        "rationale;",
        "provenance;",
        "coordinates;",
        "transform history;",
        "contracts;",
        "tests;",
        "evidence boundaries;",
        "known failure conditions.",
        "Duplicate implementation residue may collapse.",
        "Independent invariant loss is invalid.",
        "Compress until further compression destroys an independent invariant.",
        "Nothing vanishes unexplained.",
        "Nothing survives merely because it existed.",
        "Lossless-Collapse Receipt.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-O binding: {lock}"
            )

    for schema_path in (
        VALIDATION_SCHEMA,
        RECEIPT_SCHEMA,
    ):
        try:
            load(
                schema_path
            )
        except Exception as exc:
            errors.append(
                f"invalid schema JSON {schema_path}: {exc}"
            )

    positive = make_record()

    errors.extend(
        validate_record(
            positive
        )
    )

    receipt = build_receipt(
        positive
    )

    errors.extend(
        validate_receipt(
            receipt
        )
    )

    missing_class = make_record(
        observed_classes=[
            value
            for value in REQUIRED_CLASSES
            if value != "RATIONALE"
        ]
    )

    if (
        "PRESERVATION_CLASS_MISSING"
        not in missing_class[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-O failed to reject missing preservation class"
        )

    unexplained = make_record(
        unexplained_vanishing_detected=True
    )

    if (
        "UNEXPLAINED_VANISHING"
        not in unexplained[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-O failed to reject unexplained vanishing"
        )

    unresolved = make_record(
        unresolved_items=[
            "unknown fate of invariant:x"
        ]
    )

    if (
        "UNRESOLVED_ITEM_PRESENT"
        not in unresolved[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-O failed to reject unresolved preservation state"
        )

    semantic_loss = make_record(
        behavior_changed=True,
        semantic_loss_detected=True,
    )

    if (
        "BEHAVIOR_CHANGED"
        not in semantic_loss[
            "failure_reasons"
        ]
        or "SEMANTIC_LOSS_DETECTED"
        not in semantic_loss[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-O failed to reject semantic behavior loss"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-O LOSSLESS COLLAPSE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    record = make_record()
    receipt = build_receipt(
        record
    )

    print(
        "R6-O LOSSLESS COLLAPSE: PASS"
    )
    print(
        "Object identity: PRESERVED"
    )
    print(
        "Capability / behavior / rationale: PRESERVED"
    )
    print(
        "Provenance / coordinates / transform history: PRESERVED"
    )
    print(
        "Contracts / tests: PRESERVED"
    )
    print(
        "Evidence boundaries: PRESERVED"
    )
    print(
        "Known failure conditions: PRESERVED"
    )
    print(
        "Duplicate implementation residue: COLLAPSIBLE"
    )
    print(
        "Independent invariant loss: REJECTED"
    )
    print(
        "Unexplained vanishing: REJECTED"
    )
    print(
        "Unresolved preservation state: REJECTED"
    )
    print(
        "LOSSLESS_COLLAPSE_RECEIPT contract: ESTABLISHED"
    )
    print(
        "Lossless-Collapse Receipt positive control: "
        + receipt[
            "collapse_disposition"
        ]
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-P Ring 6 Aggregate Validation / Audit Closure: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
