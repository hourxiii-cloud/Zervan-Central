#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "PROPORTIONAL_FORCE_ROUTING.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "proportional_force_routing.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

R3F = (
    ROOT
    / "contracts"
    / "qualification"
    / "PROPORTIONAL_FORCE_QUALIFICATION_SCALE.md"
)

R3G = (
    ROOT
    / "contracts"
    / "qualification"
    / "FORMATION_SELECTION_INTEGRATION.md"
)

SCALE_ORDER = {
    "SINGLE": 1,
    "SIGNAL_OR_INTEL": 2,
    "TEAM": 3,
    "PLATOON": 4,
}

BASELINE_SCALE = {
    "FAINT_LOCALIZED":
        "SINGLE",

    "SPLIT_PLAUSIBLE_SOURCES":
        "SIGNAL_OR_INTEL",

    "DISTRIBUTED_RECURSIVE_SCAR":
        "PLATOON",
}

CLASS_SCALE = {
    "GOBLIN":
        "SINGLE",

    "GOBLIN_SIGNAL":
        "SIGNAL_OR_INTEL",

    "INTEL_SQUAD":
        "SIGNAL_OR_INTEL",

    "GOBLIN_TEAM":
        "TEAM",

    "GOBLIN_PLATOON":
        "PLATOON",
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

    profile = record.get(
        "signal_profile"
    )

    selected_scale = record.get(
        "selected_scale"
    )

    selected_class = record.get(
        "selected_capability_class"
    )

    basis = record.get(
        "selection_basis",
        []
    )

    expected_scale = BASELINE_SCALE.get(
        profile
    )

    if (
        selected_class
        and CLASS_SCALE.get(
            selected_class
        )
        != selected_scale
    ):
        reasons.append(
            "FORCE_FORMATION_COLLAPSE"
        )

    if (
        expected_scale
        and selected_scale
        and SCALE_ORDER[
            selected_scale
        ]
        > SCALE_ORDER[
            expected_scale
        ]
    ):
        explicit_larger_basis = any(
            token.startswith(
                "larger-force-required:"
            )
            for token in basis
        )

        if not explicit_larger_basis:
            reasons.append(
                "OVERSIZED_FORCE_WITHOUT_JUSTIFICATION"
            )

    if (
        expected_scale
        and selected_scale
        and SCALE_ORDER[
            selected_scale
        ]
        < SCALE_ORDER[
            expected_scale
        ]
    ):
        explicit_smaller_basis = any(
            token.startswith(
                "deescalation-supported:"
            )
            for token in basis
        )

        if not explicit_smaller_basis:
            reasons.append(
                "UNDERSIZED_FORCE_FOR_DECLARED_MISSION"
            )

    if any(
        token == "escalation:capability-available"
        for token in basis
    ):
        reasons.append(
            "ESCALATION_WITHOUT_EVIDENCE"
        )

    if any(
        token == "question:rewritten-for-force"
        for token in basis
    ):
        reasons.append(
            "QUESTION_REWRITTEN_FOR_FORCE"
        )

    if any(
        token == "evidence-boundary:exceeded"
        for token in basis
    ):
        reasons.append(
            "EVIDENCE_BOUNDARY_EXCEEDED"
        )

    if any(
        token == "evidence-ceiling:promoted"
        for token in basis
    ):
        reasons.append(
            "EVIDENCE_CEILING_PROMOTED"
        )

    if record.get(
        "formation_reference"
    ):
        reasons.append(
            "FORCE_FORMATION_COLLAPSE"
        )

    if record.get(
        "occupancy_created"
    ):
        reasons.append(
            "OCCUPANCY_INVENTED"
        )

    if record.get(
        "active_lifecycle_created"
    ):
        reasons.append(
            "ACTIVE_STATE_INVENTED"
        )

    if record.get(
        "execution_authorized"
    ):
        reasons.append(
            "EXECUTION_AUTHORITY_INVENTED"
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


def expected_disposition(record):
    return (
        "VALID"
        if not evaluate_record(
            record
        )
        else "REJECTED"
    )


def validate_record(record):
    errors = []

    if (
        record.get(
            "validation_vector"
        )
        != "PROPORTIONAL_FORCE_ROUTING"
    ):
        errors.append(
            "wrong validation vector"
        )

    if not record.get(
        "active_question"
    ):
        errors.append(
            "force selection requires active question"
        )

    if not record.get(
        "evidence_boundary_reference"
    ):
        errors.append(
            "force selection requires evidence boundary"
        )

    if not record.get(
        "evidence_ceiling_reference"
    ):
        errors.append(
            "force selection requires evidence ceiling"
        )

    if not record.get(
        "selection_basis"
    ):
        errors.append(
            "force selection requires selection basis"
        )

    expected_reasons = evaluate_record(
        record
    )

    expected = (
        "VALID"
        if not expected_reasons
        else "REJECTED"
    )

    if (
        record.get(
            "validation_disposition"
        )
        != expected
    ):
        errors.append(
            "force validation disposition contradicts proportional-force state"
        )

    if (
        sorted(
            record.get(
                "failure_reasons",
                []
            )
        )
        != expected_reasons
    ):
        errors.append(
            "force validation failure reasons are incomplete or incorrect"
        )

    if (
        record.get(
            "validation_disposition"
        )
        == "REJECTED"
        and not record.get(
            "failure_reasons"
        )
    ):
        errors.append(
            "REJECTED force selection requires failure reasons"
        )

    if (
        record.get(
            "validation_disposition"
        )
        == "VALID"
        and record.get(
            "failure_reasons"
        )
    ):
        errors.append(
            "VALID force selection may not retain failure reasons"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-D Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R6-D validation requires provenance route"
        )

    return errors


def make_record(
    *,
    signal_profile,
    territory_complexity,
    selected_scale,
    selected_capability_class,
    selected_capability_count=1,
    selection_basis=None,
    alternatives_considered=None,
    rejected_larger_force_alternatives=None,
    rejected_smaller_force_alternatives=None,
    escalation_conditions=None,
    deescalation_conditions=None,
    formation_reference=None,
    occupancy_created=False,
    active_lifecycle_created=False,
    execution_authorized=False,
    authority_state="NONE",
):
    if selection_basis is None:
        selection_basis = [
            f"profile:{signal_profile.lower()}",
            f"territory:{territory_complexity.lower()}",
            "question:preserved",
            "evidence:bounded",
        ]

    if alternatives_considered is None:
        alternatives_considered = []

    if rejected_larger_force_alternatives is None:
        rejected_larger_force_alternatives = []

    if rejected_smaller_force_alternatives is None:
        rejected_smaller_force_alternatives = []

    if escalation_conditions is None:
        escalation_conditions = []

    if deescalation_conditions is None:
        deescalation_conditions = []

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "PROPORTIONAL_FORCE_ROUTING",

        "object_id":
            "sha512:"
            + "1" * 128,

        "active_question":
            "What is the smallest capability able to resolve the current signal?",

        "signal_profile":
            signal_profile,

        "territory_complexity":
            territory_complexity,

        "evidence_boundary_reference":
            "boundary:r6-d:a",

        "evidence_ceiling_reference":
            "ceiling:r6-d:a",

        "selected_scale":
            selected_scale,

        "selected_capability_class":
            selected_capability_class,

        "selected_capability_count":
            selected_capability_count,

        "selection_basis":
            list(
                selection_basis
            ),

        "alternatives_considered":
            list(
                alternatives_considered
            ),

        "rejected_larger_force_alternatives":
            list(
                rejected_larger_force_alternatives
            ),

        "rejected_smaller_force_alternatives":
            list(
                rejected_smaller_force_alternatives
            ),

        "escalation_conditions":
            list(
                escalation_conditions
            ),

        "deescalation_conditions":
            list(
                deescalation_conditions
            ),

        "formation_reference":
            formation_reference,

        "occupancy_created":
            occupancy_created,

        "active_lifecycle_created":
            active_lifecycle_created,

        "execution_authorized":
            execution_authorized,

        "validation_disposition":
            "",

        "failure_reasons":
            [],

        "provenance_route": [
            "qualification:r3-f",
            "formation-boundary:r3-g",
            "validation:r6-d",
        ],

        "authority_state":
            authority_state,

        "human_gate_state":
            "ACTIVE",
    }

    record[
        "failure_reasons"
    ] = evaluate_record(
        record
    )

    record[
        "validation_disposition"
    ] = expected_disposition(
        record
    )

    return record


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-D contract"
        ),
        (
            SCHEMA,
            "R6-D schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            R3F,
            "R3-F proportional force"
        ),
        (
            R3G,
            "R3-G formation selection"
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
        "R6-D = Proportional-Force Routing.",
        "Need determines force.",
        "Question determines mission.",
        "Evidence determines escalation.",
        "Object identity determines continuity.",
        "A capability request shall use the smallest justified force.",
        "No fixed capability package is presumed.",
        "Scale != formation.",
        "Class != authority.",
        "Class != truth ownership.",
        "Faint signal != automatic Team.",
        "Faint signal != automatic Platoon.",
        "Split signal does not automatically justify Team.",
        "Split signal does not automatically justify Platoon.",
        "Scar != confidence.",
        "Distributed unresolved scar may justify Platoon scale.",
        "May justify != always requires.",
        "Complexity informs force.",
        "Complexity does not own force selection.",
        "Larger != better.",
        "More capability != more truth.",
        "No escalation by habit.",
        "Force serves mission.",
        "Mission does not serve force.",
        "More force does not increase evidence authority.",
        "More observers do not raise the claim ceiling.",
        "Capability count != evidence strength.",
        "Escalation condition != automatic escalation.",
        "De-escalation is valid.",
        "Historical force != standing force.",
        "Alternative considered != selected.",
        "Capability organization != analytical formation.",
        "Formation Selection != force inflation.",
        "Selected capability != occupant.",
        "Selection != entry.",
        "Selected force != ACTIVE.",
        "Capability allocation != lifecycle mutation.",
        "More force != more hydration authority.",
        "Force selection != policy ownership.",
        "Selected != authorized to execute.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "VALID != authorized.",
        "VALID != executed.",
        "Baseline mapping != universal fixed package.",
        "More available capability != more required capability.",
        "Re-selection != new Room.",
        "R6-E owns Qualification-Team Coherence validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-D lock: {lock}"
            )

    r3f = normalized(
        R3F
    )

    for lock in (
        "Need determines force.",
        "Question determines mission.",
        "Evidence determines escalation.",
        "A capability request shall use the smallest justified force.",
        "No fixed capability package is presumed.",
        "Scale != formation.",
        "Faint signal != automatic Platoon.",
        "Split signal does not automatically justify a Platoon.",
        "Scar != confidence.",
        "No escalation by habit.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r3f
        ):
            errors.append(
                f"R3-F missing proportional-force semantic: {lock}"
            )

    r3g = normalized(
        R3G
    )

    for lock in (
        "Formation != capability scale.",
        "A Goblin Team is not automatically Stack Analysis.",
        "A Goblin Platoon is not automatically Swarm.",
        "Formation Selection != force inflation.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r3g
        ):
            errors.append(
                f"R3-G missing force/formation separation: {lock}"
            )

    r6a = normalized(
        R6A
    )

    for lock in (
        "PROPORTIONAL_FORCE_ROUTING",
        "Need determines force.",
        "Question determines mission.",
        "Evidence determines escalation.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-D binding: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-D schema JSON: {exc}"
        ]

    forbidden = {
        "formation_type",
        "occupancy_witness",
        "active_transition",
        "hydration_release",
        "execution_result",
        "publication_authorization",
        "canonical_promotion",
        "claim_ceiling_override",
    }

    leaked = (
        set(
            schema.get(
                "properties",
                {}
            )
        )
        & forbidden
    )

    if leaked:
        errors.append(
            "R6-D improperly absorbs downstream semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    # Faint localized.
    faint = make_record(
        signal_profile="FAINT_LOCALIZED",
        territory_complexity="SMALL",
        selected_scale="SINGLE",
        selected_capability_class="GOBLIN",
        rejected_larger_force_alternatives=[
            "TEAM",
            "PLATOON",
        ],
        escalation_conditions=[
            "signal distribution expands",
        ],
    )

    errors.extend(
        validate_record(
            faint
        )
    )

    # Split signal / Goblin Signal.
    split_signal = make_record(
        signal_profile="SPLIT_PLAUSIBLE_SOURCES",
        territory_complexity="MEDIUM",
        selected_scale="SIGNAL_OR_INTEL",
        selected_capability_class="GOBLIN_SIGNAL",
        alternatives_considered=[
            "INTEL_SQUAD",
        ],
        rejected_larger_force_alternatives=[
            "PLATOON",
        ],
    )

    errors.extend(
        validate_record(
            split_signal
        )
    )

    # Split signal / Intel squad.
    split_intel = make_record(
        signal_profile="SPLIT_PLAUSIBLE_SOURCES",
        territory_complexity="MEDIUM",
        selected_scale="SIGNAL_OR_INTEL",
        selected_capability_class="INTEL_SQUAD",
        alternatives_considered=[
            "GOBLIN_SIGNAL",
        ],
    )

    errors.extend(
        validate_record(
            split_intel
        )
    )

    # Distributed recursive scar.
    scar = make_record(
        signal_profile="DISTRIBUTED_RECURSIVE_SCAR",
        territory_complexity="LARGE_DISTRIBUTED",
        selected_scale="PLATOON",
        selected_capability_class="GOBLIN_PLATOON",
        selected_capability_count=4,
        rejected_smaller_force_alternatives=[
            "SINGLE",
            "SIGNAL_OR_INTEL",
            "TEAM",
        ],
        selection_basis=[
            "profile:distributed_recursive_scar",
            "territory:large_distributed",
            "question:preserved",
            "evidence:bounded",
            "larger-force-required:parallel independent routes",
        ],
    )

    errors.extend(
        validate_record(
            scar
        )
    )

    # Oversized faint signal.
    oversized = make_record(
        signal_profile="FAINT_LOCALIZED",
        territory_complexity="SMALL",
        selected_scale="PLATOON",
        selected_capability_class="GOBLIN_PLATOON",
    )

    if (
        oversized[
            "validation_disposition"
        ]
        != "REJECTED"
        or "OVERSIZED_FORCE_WITHOUT_JUSTIFICATION"
        not in oversized[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-D failed to reject unjustified Platoon for faint signal"
        )

    # Escalation just because capability exists.
    habitual = make_record(
        signal_profile="FAINT_LOCALIZED",
        territory_complexity="SMALL",
        selected_scale="TEAM",
        selected_capability_class="GOBLIN_TEAM",
        selection_basis=[
            "profile:faint_localized",
            "territory:small",
            "question:preserved",
            "evidence:bounded",
            "escalation:capability-available",
        ],
    )

    if (
        habitual[
            "validation_disposition"
        ]
        != "REJECTED"
        or "ESCALATION_WITHOUT_EVIDENCE"
        not in habitual[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-D failed to reject escalation by availability/habit"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-D PROPORTIONAL-FORCE ROUTING: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-D PROPORTIONAL-FORCE ROUTING: PASS"
    )
    print(
        "Faint localized -> SINGLE / GOBLIN: VALIDATED"
    )
    print(
        "Split signal -> SIGNAL_OR_INTEL: VALIDATED"
    )
    print(
        "Distributed recursive scar -> PLATOON when justified: VALIDATED"
    )
    print(
        "Oversized force without justification: REJECTED"
    )
    print(
        "Escalation by capability availability / habit: REJECTED"
    )
    print(
        "De-escalation / economy of force: PRESERVED"
    )
    print(
        "Force scale / analytical formation: SEPARATED"
    )
    print(
        "Occupancy / ACTIVE / execution authority: NOT CREATED"
    )
    print(
        "Evidence boundary / ceiling: PRESERVED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-E Qualification-Team Coherence: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
