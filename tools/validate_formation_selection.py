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
    / "FORMATION_SELECTION_INTEGRATION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "formation_selection_record.schema.json"
)

FORCE_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "proportional_force_selection.schema.json"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

FORMATION_TYPES = {
    "SINGLE_ROUTE",
    "STACK_ANALYSIS",
    "EXPANDED_ANALYSIS",
    "SWARM",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_formation_selection_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "formation_selection_id"
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

    expected = compute_formation_selection_id(
        record
    )

    if (
        record.get("formation_selection_id")
        != expected
    ):
        errors.append(
            "formation_selection_id does not recompute from selection"
        )

    formation = record.get(
        "formation_type"
    )

    if formation not in FORMATION_TYPES:
        errors.append(
            "invalid formation type"
        )

    for field in (
        "object_id",
        "capability_mission_request_references",
        "proportional_force_selection_references",
        "occupancy_witness_references",
        "active_questions",
        "selected_capability_references",
        "target_room_references",
        "zone_references",
        "space_references",
        "representation_coordinate_references",
        "evidence_boundary",
        "evidence_ceiling",
        "independent_finding_policy",
        "correlation_policy",
        "integration_basis",
        "stick_reference",
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
                f"Formation Selection requires {field}"
            )

    capabilities = record.get(
        "selected_capability_references",
        []
    )

    rooms = record.get(
        "target_room_references",
        []
    )

    spaces = record.get(
        "space_references",
        []
    )

    if (
        formation == "SINGLE_ROUTE"
        and len(capabilities) != 1
    ):
        errors.append(
            "SINGLE_ROUTE requires exactly one selected capability"
        )

    if (
        formation == "STACK_ANALYSIS"
        and len(capabilities) < 2
    ):
        errors.append(
            "STACK_ANALYSIS requires multiple capabilities"
        )

    if (
        formation == "STACK_ANALYSIS"
        and len(set(rooms)) != 1
    ):
        errors.append(
            "STACK_ANALYSIS requires one canonical Room target"
        )

    if (
        formation == "EXPANDED_ANALYSIS"
        and len(set(rooms)) != 1
    ):
        errors.append(
            "EXPANDED_ANALYSIS requires one canonical Room target"
        )

    if (
        formation == "EXPANDED_ANALYSIS"
        and (
            len(spaces) < 2
            and len(
                record.get(
                    "active_questions",
                    []
                )
            ) < 2
        )
    ):
        errors.append(
            "EXPANDED_ANALYSIS requires expanded bounded analytical surface"
        )

    if (
        formation in {
            "STACK_ANALYSIS",
            "SWARM",
        }
        and (
            "independent"
            not in record.get(
                "independent_finding_policy",
                ""
            ).lower()
        )
    ):
        errors.append(
            f"{formation} must preserve independent findings"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R3-G formation contract"
        ),
        (
            SCHEMA,
            "R3-G formation schema"
        ),
        (
            FORCE_SCHEMA,
            "R3-F proportional-force schema"
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

    formations = set(
        schema
        .get("properties", {})
        .get("formation_type", {})
        .get("enum", [])
    )

    if formations != FORMATION_TYPES:
        errors.append(
            "R3-G formation vocabulary is not source-locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "goblin_signal_event_id",
        "active_lifecycle_transition_id",
        "hydration_request_id",
        "landing_witness_id",
        "closing_witness_id",
        "replay_envelope_id",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R3-G improperly absorbs downstream semantics: "
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
        "Room doctrine does not replace formation doctrine.",
        "It makes the formation target explicit.",
        "Formation != Room identity.",
        "Formation != capability scale.",
        "A Goblin Team is not automatically Stack Analysis.",
        "A Goblin Platoon is not automatically Swarm.",
        "Capability organization != analytical formation.",
        "Single-route is correct when one route is sufficient.",
        "No forced multiplication of capability.",
        "Independent findings MUST be preserved before correlation.",
        "Stack does not permit false consensus.",
        "Stack does not create multiple Rooms.",
        "Stack does not erase disagreement.",
        "Additional Space != additional Room.",
        "Additional question != additional Room.",
        "Additional evidence type != additional Room.",
        "Additional reachable surface != additional Room.",
        "Related != identical.",
        "Swarm MUST NOT collapse distinct Rooms into one object.",
        "Swarm MUST NOT clone one Room merely because perspectives differ.",
        "Different perspective does not create another Room.",
        "Different discipline does not create another Room.",
        "Different stakeholder does not create another Room.",
        "Disagreement does not create another Room.",
        "Compatible != identical.",
        "Representation transform != new Room.",
        "Independent findings != consensus.",
        "Correlation != averaging away contradiction.",
        "Correlation != truth ownership.",
        "Correlation != canonical mutation.",
        "Expand the analysis.",
        "Do not duplicate the Room.",
        "Parallelism != cloning.",
        "R3-G does not establish distinctness.",
        "Formation cannot manufacture a family of Rooms.",
        "Formation Selection != force inflation.",
        "Cooperation != scope expansion.",
        "Selected formation != presence.",
        "Selection != occupation.",
        "More observers != more authority.",
        "Consensus != evidence elevation.",
        "Formation changes MUST preserve the Stick.",
        "Formation change MUST NOT sever analytical continuity.",
        "Formation change != new Room.",
        "History accumulates.",
        "More surface does not mean more Room.",
        "Swarm is not the default advanced mode.",
        "No formation persists merely because it was previously selected.",
        "TOC does not own truth.",
        "TOC does not own policy.",
        "TOC does not own Room identity.",
        "Formation cannot override Governance.",
        "Coordination != authority.",
        "Formation selected != ACTIVE.",
        "Formation Selection Record != Goblin Signal event.",
        "Formation != hydration authority.",
        "Formation result != publication authority.",
        "Formation result != decision authority.",
        "No Goblin Signal propagation yet.",
        "No ACTIVE lifecycle transition yet.",
        "No Hydration semantics yet.",
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
                f"missing R3-G lock: {lock}"
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
        "formation_type":
            "SINGLE_ROUTE",
        "capability_mission_request_references": [
            "mission:a"
        ],
        "proportional_force_selection_references": [
            "force:a"
        ],
        "occupancy_witness_references": [
            "occupancy:a"
        ],
        "active_questions": [
            "what is producing the bounded signal?"
        ],
        "selected_capability_references": [
            "Goblin:a"
        ],
        "target_room_references": [
            object_id
        ],
        "zone_references": [
            "zone:a"
        ],
        "space_references": [
            "space:a"
        ],
        "representation_coordinate_references": [
            "orientation:a"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "independent_finding_policy":
            "preserve independent findings before correlation",
        "correlation_policy":
            "correlate only after attributable return",
        "integration_basis": [
            "one capability can answer the bounded question"
        ],
        "rejustification_triggers": [
            "terrain contact changes",
            "contradiction appears",
            "evidence ceiling changes",
            "signal ecology changes"
        ],
        "stick_reference":
            "stick:a",
        "toc_reference":
            "toc:a",
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "provenance_route": [
            object_id,
            "mission:a",
            "force:a",
            "occupancy:a",
            "stick:a"
        ],
        "selected_at":
            "2026-08-07T19:37:00-04:00",
    }

    single[
        "formation_selection_id"
    ] = compute_formation_selection_id(
        single
    )

    if not SHA512_RE.fullmatch(
        single[
            "formation_selection_id"
        ]
    ):
        errors.append(
            "formation_selection_id is not canonical SHA-512"
        )

    errors.extend(
        validate_selection(
            single
        )
    )

    stack = dict(
        single
    )

    stack[
        "formation_type"
    ] = "STACK_ANALYSIS"

    stack[
        "capability_mission_request_references"
    ] = [
        "mission:a",
        "mission:b"
    ]

    stack[
        "proportional_force_selection_references"
    ] = [
        "force:a",
        "force:b"
    ]

    stack[
        "occupancy_witness_references"
    ] = [
        "occupancy:a",
        "occupancy:b"
    ]

    stack[
        "selected_capability_references"
    ] = [
        "Goblin:a",
        "Goblin:b"
    ]

    stack[
        "representation_coordinate_references"
    ] = [
        "orientation:a",
        "orientation:b"
    ]

    stack[
        "integration_basis"
    ] = [
        "multiple independent capabilities required",
        "same Room and compatible representation coordinates"
    ]

    stack[
        "formation_selection_id"
    ] = compute_formation_selection_id(
        stack
    )

    errors.extend(
        validate_selection(
            stack
        )
    )

    expanded = dict(
        stack
    )

    expanded[
        "formation_type"
    ] = "EXPANDED_ANALYSIS"

    expanded[
        "space_references"
    ] = [
        "space:a",
        "space:b"
    ]

    expanded[
        "active_questions"
    ] = [
        "what is producing the bounded signal?",
        "which additional reachable surface discriminates the signal?"
    ]

    expanded[
        "integration_basis"
    ] = [
        "same Room requires additional bounded Spaces and questions"
    ]

    expanded[
        "formation_selection_id"
    ] = compute_formation_selection_id(
        expanded
    )

    errors.extend(
        validate_selection(
            expanded
        )
    )

    swarm = dict(
        stack
    )

    swarm[
        "formation_type"
    ] = "SWARM"

    swarm[
        "selected_capability_references"
    ] = [
        "Goblin:a",
        "Goblin:b",
        "Goblin:c"
    ]

    swarm[
        "occupancy_witness_references"
    ] = [
        "occupancy:a",
        "occupancy:b",
        "occupancy:c"
    ]

    swarm[
        "integration_basis"
    ] = [
        "parallel capability surfaces are justified",
        "independent findings preserved"
    ]

    swarm[
        "formation_selection_id"
    ] = compute_formation_selection_id(
        swarm
    )

    errors.extend(
        validate_selection(
            swarm
        )
    )

    invalid_stack = dict(
        stack
    )

    invalid_stack[
        "target_room_references"
    ] = [
        object_id,
        "sha512:" + "9" * 128
    ]

    invalid_stack[
        "formation_selection_id"
    ] = compute_formation_selection_id(
        invalid_stack
    )

    stack_errors = validate_selection(
        invalid_stack
    )

    if not any(
        "one canonical Room target"
        in error
        for error in stack_errors
    ):
        errors.append(
            "STACK_ANALYSIS incorrectly permitted multiple Room targets"
        )

    changed = dict(
        single
    )

    changed[
        "formation_type"
    ] = "STACK_ANALYSIS"

    changed[
        "selected_capability_references"
    ] = [
        "Goblin:a",
        "Goblin:b"
    ]

    changed[
        "formation_selection_id"
    ] = compute_formation_selection_id(
        changed
    )

    if (
        changed[
            "formation_selection_id"
        ]
        == single[
            "formation_selection_id"
        ]
    ):
        errors.append(
            "material formation change did not change formation identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-G FORMATION SELECTION / INTEGRATION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-G FORMATION SELECTION / INTEGRATION: PASS"
    )
    print(
        "Single-route / Stack / Expanded / Swarm: LOCKED"
    )
    print(
        "Capability scale != analytical formation: LOCKED"
    )
    print(
        "Independent findings before correlation: ENFORCED"
    )
    print(
        "Same-object / distinct-object formation boundaries: PRESERVED"
    )
    print(
        "Re-justification preserves Stick / object identity: LOCKED"
    )
    print(
        "Goblin Signal / ACTIVE / Hydration: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
