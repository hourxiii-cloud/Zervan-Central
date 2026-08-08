#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "FRESH_READER_VALIDATION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "fresh_reader_validation.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

README = (
    ROOT
    / "README.md"
)

INVENTORY = (
    ROOT
    / "INVENTORY.md"
)

RING6_RUNNER = (
    ROOT
    / "tools"
    / "validate_ring6.py"
)

V40_INIT = (
    ROOT
    / "call"
    / "INITIATION_STATEMENT_V40_0.md"
)

V40_CANONICAL = (
    ROOT
    / "canonical"
    / "ZERVAN_v40_0_CANONICAL_LOAD.md"
)

V41_INIT_CANDIDATES = [
    ROOT
    / "call"
    / "INITIATION_STATEMENT_V41_0.md",

    ROOT
    / "call"
    / "INITIATION_STATEMENT_V41.md",

    ROOT
    / "call"
    / "INITIATION_STATEMENT_V41_COMPLETE.md",
]

V41_CANONICAL_CANDIDATES = [
    ROOT
    / "canonical"
    / "ZERVAN_v41_0_CANONICAL_LOAD.md",

    ROOT
    / "canonical"
    / "ZERVAN_v41_CANONICAL_LOAD.md",

    ROOT
    / "canonical"
    / "ZERVAN_v41_COMPLETE_CANONICAL_LOAD.md",
]


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


def candidate_version_identity_present():
    surfaces = list(
        (
            ROOT
            / "contracts"
        ).rglob(
            "*.md"
        )
    )

    for path in surfaces:
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        if (
            "vTemporal.41.0"
            in text
            or "v41 Complete"
            in text
        ):
            return True

    return False


def build_record(
    *,
    requires_v40_knowledge=False,
    requires_prior_conversation=False,
    requires_architect_interpretation=False,
    requires_emotional_discovery_history=False,
    historical_substitution_used=False,
    authority_state="NONE",
    force_promoted_ready=False,
):
    v41_init_present = any(
        path.exists()
        for path in V41_INIT_CANDIDATES
    )

    v41_canonical_present = any(
        path.exists()
        for path in V41_CANONICAL_CANDIDATES
    )

    promoted_ready = (
        v41_init_present
        and v41_canonical_present
    )

    if force_promoted_ready:
        promoted_entry_state = "READY"
    elif promoted_ready:
        promoted_entry_state = "READY"
    else:
        promoted_entry_state = (
            "DEFERRED_TO_PROMOTION"
        )

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "FRESH_READER_TEST",

        "repository_orientation_present":
            README.exists(),

        "inventory_present":
            INVENTORY.exists(),

        "contracts_present":
            (
                ROOT
                / "contracts"
            ).is_dir(),

        "schemas_present":
            (
                ROOT
                / "schemas"
            ).is_dir(),

        "tools_present":
            (
                ROOT
                / "tools"
            ).is_dir(),

        "tests_present":
            (
                ROOT
                / "tests"
            ).is_dir(),

        "r6_registry_present":
            R6A.exists(),

        "ring6_runner_present":
            RING6_RUNNER.exists(),

        "candidate_version_identity_present":
            candidate_version_identity_present(),

        "authority_none_present":
            (
                R6A.exists()
                and "Authority: NONE"
                in R6A.read_text(
                    encoding="utf-8"
                )
            ),

        "human_gate_active_present":
            (
                R6A.exists()
                and "Human Gate: ACTIVE"
                in R6A.read_text(
                    encoding="utf-8"
                )
            ),

        "requires_v40_knowledge":
            requires_v40_knowledge,

        "requires_prior_conversation":
            requires_prior_conversation,

        "requires_architect_interpretation":
            requires_architect_interpretation,

        "requires_emotional_discovery_history":
            requires_emotional_discovery_history,

        "v41_initiation_present":
            v41_init_present,

        "v41_canonical_entry_present":
            v41_canonical_present,

        "historical_v40_initiation_present":
            V40_INIT.exists(),

        "historical_v40_canonical_present":
            V40_CANONICAL.exists(),

        "historical_substitution_used":
            historical_substitution_used,

        "candidate_readability":
            "",

        "promoted_entry_state":
            promoted_entry_state,

        "promotion_dependency_references": [
            "call:native-v41-initiation",
            "canonical:native-v41-entry",
            "promotion:repository-entry-binding",
        ],

        "provenance_route": [
            "README.md",
            "INVENTORY.md",
            "contracts/",
            "schemas/",
            "tools/",
            "tests/",
            "contracts/validation/"
            "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md",
            "tools/validate_ring6.py",
        ],

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
        "candidate_readability"
    ] = (
        "CANDIDATE_READABLE"
        if not reasons
        else "BLOCKED"
    )

    record[
        "validation_disposition"
    ] = (
        "VALIDATED_CANDIDATE"
        if not reasons
        else "BLOCKED"
    )

    return record


def evaluate_record(record):
    reasons = []

    checks = [
        (
            "repository_orientation_present",
            "REPOSITORY_ORIENTATION_MISSING",
        ),
        (
            "inventory_present",
            "INVENTORY_MISSING",
        ),
        (
            "contracts_present",
            "CONTRACT_SURFACE_MISSING",
        ),
        (
            "schemas_present",
            "SCHEMA_SURFACE_MISSING",
        ),
        (
            "tools_present",
            "TOOL_SURFACE_MISSING",
        ),
        (
            "tests_present",
            "TEST_SURFACE_MISSING",
        ),
        (
            "r6_registry_present",
            "R6_REGISTRY_MISSING",
        ),
        (
            "ring6_runner_present",
            "RING6_RUNNER_MISSING",
        ),
        (
            "candidate_version_identity_present",
            "CANDIDATE_VERSION_IDENTITY_MISSING",
        ),
        (
            "authority_none_present",
            "AUTHORITY_BOUNDARY_MISSING",
        ),
        (
            "human_gate_active_present",
            "HUMAN_GATE_BOUNDARY_MISSING",
        ),
    ]

    for field, reason in checks:
        if not record.get(
            field
        ):
            reasons.append(
                reason
            )

    if record.get(
        "requires_v40_knowledge"
    ):
        reasons.append(
            "V40_KNOWLEDGE_REQUIRED"
        )

    if record.get(
        "requires_prior_conversation"
    ):
        reasons.append(
            "PRIOR_CONVERSATION_REQUIRED"
        )

    if record.get(
        "requires_architect_interpretation"
    ):
        reasons.append(
            "ARCHITECT_INTERPRETATION_REQUIRED"
        )

    if record.get(
        "requires_emotional_discovery_history"
    ):
        reasons.append(
            "EMOTIONAL_HISTORY_REQUIRED"
        )

    if record.get(
        "historical_substitution_used"
    ):
        reasons.append(
            "HISTORICAL_VERSION_SUBSTITUTED"
        )

    actual_promoted_ready = (
        record.get(
            "v41_initiation_present"
        )
        and record.get(
            "v41_canonical_entry_present"
        )
    )

    if (
        record.get(
            "promoted_entry_state"
        )
        == "READY"
        and not actual_promoted_ready
    ):
        reasons.append(
            "PROMOTED_ENTRY_FALSELY_CLAIMED"
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
            "validation_vector"
        )
        != "FRESH_READER_TEST"
    ):
        errors.append(
            "wrong validation vector"
        )

    reasons = evaluate_record(
        record
    )

    expected = (
        "VALIDATED_CANDIDATE"
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
            "Fresh-Reader disposition contradicts candidate readability state"
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
            "Fresh-Reader failure reasons are incomplete or incorrect"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-M Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R6-M provenance route required"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-M contract"
        ),
        (
            SCHEMA,
            "R6-M schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            README,
            "README"
        ),
        (
            INVENTORY,
            "Inventory"
        ),
        (
            RING6_RUNNER,
            "Ring 6 runner"
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
        "R6-M = Fresh-Reader Validation.",
        "A fresh reader must not require v40 knowledge.",
        "A fresh reader must not require prior conversation state.",
        "A fresh reader must not require original architect interpretation.",
        "A fresh reader must not require emotional discovery history.",
        "A repository that requires an external decoder ring is incomplete.",
        "Fresh-reader capability is a portability-of-understanding test.",
        "Fresh-reader validation != promotion authorization.",
        "Historical versions may remain for provenance.",
        "Historical preservation != current dependency.",
        "v40 provenance != v41 initialization requirement.",
        "Conversation != canonical dependency.",
        "Architect availability != runtime prerequisite.",
        "Discovery history != operational prerequisite.",
        "README orientation != complete native-v41 initialization.",
        "Inventory != initialization.",
        "Candidate readability may be validated before promotion.",
        "Promoted-entry completeness may not be claimed before the promoted v41 entry surfaces exist.",
        "No fake completion.",
        "No fake canonical surface.",
        "Historical artifact != active v41 entry surface.",
        "Validation observes.",
        "Validation does not repair implementation state silently.",
        "CANDIDATE_READABLE != PROMOTED_FRESH_READER_COMPLETE.",
        "DEFERRED_TO_PROMOTION != failure.",
        "DEFERRED_TO_PROMOTION != completion.",
        "Validator != documentation author.",
        "Validator != promotion tool.",
        "Validator != canonical mutation.",
        "Portable repository != shared memory.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-N owns Representation Independence validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-M lock: {lock}"
            )

    r6a = normalized(
        R6A
    )

    for lock in (
        "Fresh-Reader Test",
        "v40 knowledge;",
        "prior conversation state;",
        "original architect interpretation;",
        "emotional discovery history.",
        "A repository that requires an external decoder ring is incomplete.",
        "Fresh-reader capability is a portability-of-understanding test, not a promotion authorization.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing Fresh-Reader binding: {lock}"
            )

    readme = normalized(
        README
    )

    for lock in (
        "Authority: NONE",
        "Human Gate: ACTIVE",
        "Historical versions may remain for provenance.",
        "Git main governs repository state.",
        "No fake retrieval.",
        "No authority promotion.",
        "No compression out.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in readme
        ):
            errors.append(
                f"README missing required reader orientation: {lock}"
            )

    try:
        load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-M schema JSON: {exc}"
        ]

    # Current candidate must be readable.
    candidate = build_record()

    errors.extend(
        validate_record(
            candidate
        )
    )

    if (
        candidate[
            "candidate_readability"
        ]
        != "CANDIDATE_READABLE"
    ):
        errors.append(
            "R6-M candidate repository is not self-contained enough for fresh-reader review"
        )

    # Current candidate must not falsely claim promoted entry readiness.
    if (
        not candidate[
            "v41_initiation_present"
        ]
        or not candidate[
            "v41_canonical_entry_present"
        ]
    ):
        if (
            candidate[
                "promoted_entry_state"
            ]
            != "DEFERRED_TO_PROMOTION"
        ):
            errors.append(
                "R6-M failed to defer absent promoted-v41 entry surfaces"
            )

    # v40 dependency is invalid.
    v40_dependent = build_record(
        requires_v40_knowledge=True
    )

    if (
        "V40_KNOWLEDGE_REQUIRED"
        not in v40_dependent[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-M failed to reject v40 dependency"
        )

    # Conversation dependency is invalid.
    conversation_dependent = build_record(
        requires_prior_conversation=True
    )

    if (
        "PRIOR_CONVERSATION_REQUIRED"
        not in conversation_dependent[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-M failed to reject conversation dependency"
        )

    # Historical substitution is invalid.
    substituted = build_record(
        historical_substitution_used=True
    )

    if (
        "HISTORICAL_VERSION_SUBSTITUTED"
        not in substituted[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-M failed to reject historical-version substitution"
        )

    # False promoted readiness is invalid.
    falsely_ready = build_record(
        force_promoted_ready=True
    )

    if (
        not falsely_ready[
            "v41_initiation_present"
        ]
        or not falsely_ready[
            "v41_canonical_entry_present"
        ]
    ):
        if (
            "PROMOTED_ENTRY_FALSELY_CLAIMED"
            not in falsely_ready[
                "failure_reasons"
            ]
        ):
            errors.append(
                "R6-M failed to reject false promoted-entry completion"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-M FRESH-READER VALIDATION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    record = build_record()

    print(
        "R6-M FRESH-READER VALIDATION: PASS"
    )
    print(
        "Candidate repository-only readability: VALIDATED"
    )
    print(
        "README / Inventory / contracts / schemas / tools / tests: DISCOVERABLE"
    )
    print(
        "vTemporal.41.0 candidate identity: DISCOVERABLE"
    )
    print(
        "Authority NONE / Human Gate ACTIVE: DISCOVERABLE"
    )
    print(
        "v40 knowledge dependency: REJECTED"
    )
    print(
        "Prior conversation dependency: REJECTED"
    )
    print(
        "Original-architect dependency: REJECTED"
    )
    print(
        "Emotional discovery-history dependency: REJECTED"
    )
    print(
        "Historical v40 artifact substitution as v41 entry: REJECTED"
    )

    if (
        record[
            "promoted_entry_state"
        ]
        == "DEFERRED_TO_PROMOTION"
    ):
        print(
            "Native-v41 promoted initiation / canonical entry: DEFERRED_TO_PROMOTION"
        )
        print(
            "False promoted-entry completion: REJECTED"
        )
    else:
        print(
            "Native-v41 promoted initiation / canonical entry: READY"
        )

    print(
        "External decoder ring requirement: REJECTED"
    )
    print(
        "Validation disposition: VALIDATED_CANDIDATE"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-N Representation Independence: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
