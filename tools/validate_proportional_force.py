#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "qualification"
    / "PROPORTIONAL_FORCE_QUALIFICATION_SCALE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "proportional_force_selection.schema.json"
)

MISSION_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "capability_mission_request.schema.json"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

SCALES = {
    "SINGLE",
    "SIGNAL_OR_INTEL",
    "TEAM",
    "PLATOON",
}

CLASSES = {
    "GOBLIN",
    "GOBLIN_SIGNAL",
    "INTEL_SQUAD",
    "GOBLIN_TEAM",
    "GOBLIN_PLATOON",
}

SCALE_CLASS = {
    "SINGLE": {
        "GOBLIN",
    },
    "SIGNAL_OR_INTEL": {
        "GOBLIN_SIGNAL",
        "INTEL_SQUAD",
    },
    "TEAM": {
        "GOBLIN_TEAM",
    },
    "PLATOON": {
        "GOBLIN_PLATOON",
    },
}

SOURCE_BASELINES = {
    "FAINT_LOCALIZED": {
        "SINGLE",
    },
    "SPLIT_PLAUSIBLE_SOURCES": {
        "SIGNAL_OR_INTEL",
    },
    "DISTRIBUTED_RECURSIVE_SCAR": {
        "PLATOON",
    },
}

ROOM_BASELINES = {
    "SMALL": {
        "SINGLE",
    },
    "MEDIUM": {
        "TEAM",
    },
    "LARGE_DISTRIBUTED": {
        "PLATOON",
    },
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_selection_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "proportional_force_selection_id"
    }

    return (
        "sha512:"
        + hashlib.sha512(
            canonical_bytes(preimage)
        ).hexdigest()
    )


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def validate_selection(record):
    errors = []

    expected = compute_selection_id(
        record
    )

    if (
        record.get("proportional_force_selection_id")
        != expected
    ):
        errors.append(
            "proportional_force_selection_id does not recompute from selection"
        )

    scale = record.get(
        "selected_scale"
    )

    capability_class = record.get(
        "selected_capability_class"
    )

    if scale not in SCALES:
        errors.append(
            "invalid proportional-force scale"
        )

    if capability_class not in CLASSES:
        errors.append(
            "invalid selected capability class"
        )

    if (
        scale in SCALE_CLASS
        and capability_class not in SCALE_CLASS[
            scale
        ]
    ):
        errors.append(
            "selected capability class does not match selected scale"
        )

    for field in (
        "object_id",
        "capability_mission_request_reference",
        "active_question",
        "unresolved_signal_profile",
        "territory_complexity",
        "evidence_boundary",
        "evidence_ceiling",
        "cartography_reference",
        "stick_reference",
        "selection_basis",
        "selected_scale",
        "selected_capability_class",
        "selected_capability_allocation",
        "toc_reference",
        "governance_reference",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Proportional Force Selection requires {field}"
            )

    signal_profile = record.get(
        "unresolved_signal_profile"
    )

    if (
        signal_profile in SOURCE_BASELINES
        and scale not in SOURCE_BASELINES[
            signal_profile
        ]
    ):
        if not any(
            "departure from source baseline"
            in item.lower()
            for item in record.get(
                "selection_basis",
                []
            )
        ):
            errors.append(
                "departure from source signal baseline requires explicit basis"
            )

    complexity = record.get(
        "territory_complexity"
    )

    if (
        signal_profile == "ROOM_COMPLEXITY"
        and complexity in ROOM_BASELINES
        and scale not in ROOM_BASELINES[
            complexity
        ]
    ):
        if not any(
            "departure from source baseline"
            in item.lower()
            for item in record.get(
                "selection_basis",
                []
            )
        ):
            errors.append(
                "departure from source Room-complexity baseline "
                "requires explicit basis"
            )

    if scale in {
        "TEAM",
        "PLATOON",
    }:
        if not record.get(
            "alternatives_considered"
        ):
            errors.append(
                "larger force selection requires alternatives considered"
            )

        if not any(
            "smaller" in str(item).lower()
            for item in record.get(
                "selection_basis",
                []
            )
        ):
            errors.append(
                "larger force selection must explain why smaller force is insufficient"
            )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R3-F proportional-force contract"
        ),
        (
            SCHEMA,
            "R3-F proportional-force schema"
        ),
        (
            MISSION_SCHEMA,
            "R3-E Capability Mission Request schema"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid schema JSON: {exc}"
        ]

    scales = set(
        schema
        .get("properties", {})
        .get("selected_scale", {})
        .get("enum", [])
    )

    classes = set(
        schema
        .get("properties", {})
        .get("selected_capability_class", {})
        .get("enum", [])
    )

    if scales != SCALES:
        errors.append(
            "R3-F force-scale vocabulary is not locked"
        )

    if classes != CLASSES:
        errors.append(
            "R3-F capability-class vocabulary is not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "formation_selection_id",
        "formation_type",
        "single_route",
        "stack_analysis",
        "expanded_analysis",
        "swarm",
        "goblin_signal_event_id",
        "active_lifecycle_transition_id",
        "occupancy_witness_id",
        "landing_witness_id",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R3-F improperly absorbs downstream semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    normalized_contract_text = " ".join(
        contract_text.split()
    )

    locks = [
        "Need determines force.",
        "Question determines mission.",
        "Evidence determines escalation.",
        "Object identity determines continuity.",
        "A capability request shall use the smallest justified force.",
        "No fixed capability package is presumed.",
        "Force is selected to answer the question.",
        "Force is not selected by habit.",
        "Scale != formation.",
        "Class != authority.",
        "Class != truth ownership.",
        "Faint signal != automatic Platoon.",
        "Split signal does not automatically justify a Platoon.",
        "Scar != confidence.",
        "Distributed unresolved scar may justify Platoon scale.",
        "Complexity informs force.",
        "Complexity does not own force selection.",
        "Larger != better.",
        "More capability != more truth.",
        "Alternative considered != selected.",
        "No escalation by habit.",
        "Escalation condition != automatic escalation.",
        "More force does not increase evidence authority.",
        "More observers do not raise the claim ceiling.",
        "Capability count != evidence strength.",
        "Cartography informs force.",
        "Cartography does not select force by itself.",
        "More capability MUST NOT weaken continuity.",
        "TOC does not own truth.",
        "TOC does not own policy.",
        "TOC does not own object identity.",
        "Proportional force cannot override policy.",
        "Selected != authorized to execute.",
        "Write capability != authority.",
        "Force serves mission.",
        "Mission does not serve force.",
        "Selected capability != occupant.",
        "Selection != entry.",
        "A selected Goblin Team is a capability scale.",
        "It is not automatically Stack Analysis.",
        "A Goblin Platoon is a capability scale.",
        "It is not automatically Swarm.",
        "Force scale != analytical formation.",
        "Selection records what was justified then.",
        "Return records what happened.",
        "Re-selection != new Room.",
        "The smallest capability able to improve orientation or the next question is preferred.",
        "No formation selection yet.",
        "No Goblin Signal propagation yet.",
        "No ACTIVE lifecycle transition yet.",
    ]

    for lock in locks:
        normalized_lock = " ".join(
            lock.split()
        )

        if (
            normalized_lock
            not in normalized_contract_text
        ):
            errors.append(
                f"missing R3-F lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    single = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "capability_mission_request_reference":
            "mission:a",
        "active_question":
            "what is producing the localized anomaly?",
        "unresolved_signal_profile":
            "FAINT_LOCALIZED",
        "territory_complexity":
            "NOT_PRIMARY",
        "evidence_boundary": {
            "scope": "localized"
        },
        "evidence_ceiling":
            "CEILING:A",
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "selection_basis": [
            "faint localized anomaly",
            "one capability can improve orientation"
        ],
        "selected_scale":
            "SINGLE",
        "selected_capability_class":
            "GOBLIN",
        "selected_capability_allocation":
            1,
        "alternatives_considered": [
            "Goblin Team"
        ],
        "rejected_larger_force_alternatives": [
            "Team exceeds current unresolved need",
            "Platoon exceeds current unresolved need"
        ],
        "escalation_conditions": [
            "signal splits",
            "signal becomes distributed"
        ],
        "deescalation_conditions": [],
        "toc_reference":
            "toc:a",
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "provenance_route": [
            object_id,
            "mission:a",
            "cartography:a",
            "stick:a"
        ],
        "selected_at":
            "2026-08-07T19:33:00-04:00",
    }

    single[
        "proportional_force_selection_id"
    ] = compute_selection_id(
        single
    )

    if not SHA512_RE.fullmatch(
        single[
            "proportional_force_selection_id"
        ]
    ):
        errors.append(
            "proportional_force_selection_id is not canonical SHA-512"
        )

    errors.extend(
        validate_selection(
            single
        )
    )

    split = dict(
        single
    )

    split[
        "unresolved_signal_profile"
    ] = "SPLIT_PLAUSIBLE_SOURCES"

    split[
        "selection_basis"
    ] = [
        "split signal with several plausible sources"
    ]

    split[
        "selected_scale"
    ] = "SIGNAL_OR_INTEL"

    split[
        "selected_capability_class"
    ] = "INTEL_SQUAD"

    split[
        "selected_capability_allocation"
    ] = "one bounded Intel squad"

    split[
        "proportional_force_selection_id"
    ] = compute_selection_id(
        split
    )

    errors.extend(
        validate_selection(
            split
        )
    )

    platoon = dict(
        single
    )

    platoon[
        "unresolved_signal_profile"
    ] = "DISTRIBUTED_RECURSIVE_SCAR"

    platoon[
        "territory_complexity"
    ] = "LARGE_DISTRIBUTED"

    platoon[
        "selection_basis"
    ] = [
        "distributed repeating .333333/.666667 scar",
        "smaller force is insufficient for independent parallel routes"
    ]

    platoon[
        "selected_scale"
    ] = "PLATOON"

    platoon[
        "selected_capability_class"
    ] = "GOBLIN_PLATOON"

    platoon[
        "selected_capability_allocation"
    ] = "one bounded Goblin Platoon"

    platoon[
        "alternatives_considered"
    ] = [
        "single Goblin",
        "Goblin Team"
    ]

    platoon[
        "proportional_force_selection_id"
    ] = compute_selection_id(
        platoon
    )

    errors.extend(
        validate_selection(
            platoon
        )
    )

    changed = dict(
        single
    )

    changed[
        "selected_scale"
    ] = "TEAM"

    changed[
        "selected_capability_class"
    ] = "GOBLIN_TEAM"

    changed[
        "selection_basis"
    ] = [
        "departure from source baseline because new evidence "
        "shows multiple independent surfaces",
        "smaller force is insufficient"
    ]

    changed[
        "proportional_force_selection_id"
    ] = compute_selection_id(
        changed
    )

    if (
        changed[
            "proportional_force_selection_id"
        ]
        == single[
            "proportional_force_selection_id"
        ]
    ):
        errors.append(
            "material force selection change did not change selection identity"
        )

    unjustified_large = dict(
        single
    )

    unjustified_large[
        "selected_scale"
    ] = "PLATOON"

    unjustified_large[
        "selected_capability_class"
    ] = "GOBLIN_PLATOON"

    unjustified_large[
        "alternatives_considered"
    ] = []

    unjustified_large[
        "selection_basis"
    ] = [
        "Platoon available"
    ]

    unjustified_large[
        "proportional_force_selection_id"
    ] = compute_selection_id(
        unjustified_large
    )

    large_errors = validate_selection(
        unjustified_large
    )

    if not any(
        (
            "alternatives considered"
            in error
            or "smaller force is insufficient"
            in error
        )
        for error in large_errors
    ):
        errors.append(
            "R3-F incorrectly permitted unjustified force inflation"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-F PROPORTIONAL FORCE / QUALIFICATION SCALE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-F PROPORTIONAL FORCE / QUALIFICATION SCALE: PASS"
    )
    print(
        "Need -> force / Question -> mission / Evidence -> escalation: LOCKED"
    )
    print(
        "Smallest justified force: ENFORCED"
    )
    print(
        "Localized / split / distributed / Room-complexity vectors: PRESERVED"
    )
    print(
        "Force inflation / fixed package selection: REJECTED"
    )
    print(
        "Formation / Goblin Signal / ACTIVE transition: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
