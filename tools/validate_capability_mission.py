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
    / "CAPABILITY_MISSION_REQUEST_RETURN.md"
)

MISSION_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "capability_mission_request.schema.json"
)

RETURN_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "capability_return.schema.json"
)

OCCUPANCY_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "occupancy_witness.schema.json"
)

STICK_SCHEMA = (
    ROOT
    / "schemas"
    / "geography"
    / "stick_continuity_record.schema.json"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

COMPLETION_STATES = {
    "COMPLETED",
    "PARTIAL",
    "BLOCKED",
}

CONTINUITY_STATES = {
    "CONTINUOUS",
    "DEGRADED",
    "BROKEN",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_mission_request_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "capability_mission_request_id"
    }

    return (
        "sha512:"
        + hashlib.sha512(
            canonical_bytes(preimage)
        ).hexdigest()
    )


def compute_capability_return_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "capability_return_id"
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


def validate_mission_request(record):
    errors = []

    expected = compute_mission_request_id(
        record
    )

    if (
        record.get("capability_mission_request_id")
        != expected
    ):
        errors.append(
            "capability_mission_request_id does not recompute from request"
        )

    for field in (
        "object_id",
        "occupancy_witness_reference",
        "active_question",
        "mission_objective",
        "mission_justification",
        "target_zone_id",
        "target_space_id",
        "orientation_reference",
        "cartography_reference",
        "stick_reference",
        "territory_reference",
        "permitted_movement",
        "permitted_actions",
        "prohibited_actions",
        "evidence_boundary",
        "evidence_ceiling",
        "evidence_obligations",
        "expected_return_obligations",
        "completion_conditions",
        "governance_reference",
        "toc_coordination_reference",
        "authorization_reference",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Capability Mission Request requires {field}"
            )

    return errors


def validate_capability_return(record):
    errors = []

    expected = compute_capability_return_id(
        record
    )

    if (
        record.get("capability_return_id")
        != expected
    ):
        errors.append(
            "capability_return_id does not recompute from return"
        )

    if record.get(
        "completion_assessment"
    ) not in COMPLETION_STATES:
        errors.append(
            "invalid capability return completion assessment"
        )

    if record.get(
        "continuity_state"
    ) not in CONTINUITY_STATES:
        errors.append(
            "invalid capability return continuity state"
        )

    for field in (
        "capability_mission_request_reference",
        "object_id",
        "occupancy_witness_reference",
        "returning_capability",
        "stick_reference",
        "final_coordinates",
        "return_coordinates",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Capability Return requires {field}"
            )

    if (
        record.get("completion_assessment")
        == "BLOCKED"
        and not (
            record.get("restriction_findings")
            or record.get("unresolved_signals")
        )
    ):
        errors.append(
            "BLOCKED Capability Return must preserve blocking restriction "
            "or unresolved signal"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R3-E mission contract"
        ),
        (
            MISSION_SCHEMA,
            "R3-E Capability Mission Request schema"
        ),
        (
            RETURN_SCHEMA,
            "R3-E Capability Return schema"
        ),
        (
            OCCUPANCY_SCHEMA,
            "R3-D Occupancy Witness schema"
        ),
        (
            STICK_SCHEMA,
            "R2-I Stick schema"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    try:
        mission_schema = load(
            MISSION_SCHEMA
        )
        return_schema = load(
            RETURN_SCHEMA
        )
        stick_schema = load(
            STICK_SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid schema JSON: {exc}"
        ]

    completion_states = set(
        return_schema
        .get("properties", {})
        .get("completion_assessment", {})
        .get("enum", [])
    )

    if completion_states != COMPLETION_STATES:
        errors.append(
            "Capability Return completion vocabulary is not locked"
        )

    continuity_states = set(
        return_schema
        .get("properties", {})
        .get("continuity_state", {})
        .get("enum", [])
    )

    stick_states = set(
        stick_schema
        .get("properties", {})
        .get("continuity_state", {})
        .get("enum", [])
    )

    if continuity_states != CONTINUITY_STATES:
        errors.append(
            "R3-E continuity vocabulary is not locked"
        )

    if stick_states and continuity_states != stick_states:
        errors.append(
            "R3-E continuity vocabulary diverges from R2-I Stick"
        )

    mission_properties = set(
        mission_schema.get(
            "properties",
            {}
        )
    )

    return_properties = set(
        return_schema.get(
            "properties",
            {}
        )
    )

    forbidden_mission = {
        "selected_force",
        "force_scale",
        "selected_formation",
        "formation_selection_id",
        "goblin_signal_event_id",
        "active_lifecycle_transition_id",
        "landing_witness_id",
    }

    leaked_mission = (
        mission_properties
        & forbidden_mission
    )

    if leaked_mission:
        errors.append(
            "R3-E Mission Request improperly absorbs downstream semantics: "
            + ", ".join(
                sorted(leaked_mission)
            )
        )

    forbidden_return = {
        "selected_force",
        "force_scale",
        "selected_formation",
        "formation_selection_id",
        "goblin_signal_event_id",
        "active_lifecycle_transition_id",
        "landing_witness_id",
        "reflight_trigger_id",
    }

    leaked_return = (
        return_properties
        & forbidden_return
    )

    if leaked_return:
        errors.append(
            "R3-E Capability Return improperly absorbs downstream semantics: "
            + ", ".join(
                sorted(leaked_return)
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
        "Mission establishes movement.",
        "Capability Mission Request declares the mission requirement.",
        "Mission Request != Proportional Force Selection.",
        "Mission Request != Formation Selection Record.",
        "Presence precedes mission execution.",
        "Presence != mission.",
        "Mission Request != Occupancy Witness.",
        "Question != force selection.",
        "Question != authority.",
        "Mission objective != conclusion.",
        "Mission objective != result.",
        "Permitted movement != executed movement.",
        "Capability availability != permission.",
        "Technical capability != mission permission.",
        "Movement does not broaden evidence access.",
        "Capability confidence != evidence authority.",
        "Obligation != satisfaction.",
        "Mission Request defines expected return.",
        "Capability Return records actual return.",
        "Governance != mission executor.",
        "TOC != truth owner.",
        "TOC != canonical state owner.",
        "TOC != object identity owner.",
        "TOC != policy owner.",
        "Mission Request != authorization invention.",
        "Write capability != authority.",
        "Authorization != execution.",
        "Human Gate decision != mission execution.",
        "Capability Return records what came back.",
        "Capability Return identity is not Room Object identity.",
        "Capability Return identity is not Capability Mission Request identity.",
        "Bounded finding != canonical truth.",
        "Finding != publication.",
        "Finding != decision.",
        "Returned evidence != automatically promoted evidence.",
        "Return != Cartography.",
        "Unknown remains unknown.",
        "Discriminating evidence need != evidence itself.",
        "Restricted != absent.",
        "Inaccessible != nonexistent.",
        "Movement MUST NOT sever analytical contact.",
        "COMPLETED != analytical truth.",
        "PARTIAL != failure.",
        "BLOCKED != nonexistent.",
        "Capability Return != Occupancy EXITED witness.",
        "Return != exit.",
        "Capability Return != Goblin Signal event.",
        "Return != propagation.",
        "R3-F determines proportional force.",
        "Need determines force downstream.",
        "Mission Request != formation.",
        "Capability Return != formation.",
        "Capability Mission Request != ACTIVE.",
        "Capability Return != ACTIVE transition.",
        "Mission result != publication.",
        "Mission result != decision authority.",
        "No proportional-force selection yet.",
        "No formation selection yet.",
        "No Goblin Signal propagation yet.",
        "No ACTIVE lifecycle transition yet.",
        "No Landing semantics yet.",
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
                f"missing R3-E lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    mission = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "occupancy_witness_reference":
            "occupancy:a",
        "active_question":
            "what evidence would discriminate the unresolved signal?",
        "mission_objective":
            "inspect bounded terrain and return discriminating evidence needs",
        "mission_justification": [
            "unresolved terrain signal remains"
        ],
        "target_zone_id":
            "sha512:" + "2" * 128,
        "target_space_id":
            "sha512:" + "3" * 128,
        "orientation_reference":
            "orientation:a",
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "territory_reference":
            "territory:a",
        "permitted_movement": {
            "scope": "declared reachable terrain only"
        },
        "permitted_actions": [
            "observe terrain",
            "test boundary",
            "identify discriminating evidence"
        ],
        "prohibited_actions": [
            "canonical mutation",
            "publication",
            "external execution"
        ],
        "evidence_boundary": {
            "scope": "mission-bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "evidence_obligations": [
            "preserve provenance",
            "preserve unresolved conditions"
        ],
        "expected_return_obligations": [
            "bounded findings",
            "evidence references",
            "return coordinates"
        ],
        "completion_conditions": [
            "bounded mission exhausted or blocked"
        ],
        "governance_reference":
            "governance:a",
        "toc_coordination_reference":
            "toc:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "occupancy:a",
            "orientation:a",
            "stick:a"
        ],
        "requested_at":
            "2026-08-07T19:28:00-04:00",
    }

    mission[
        "capability_mission_request_id"
    ] = compute_mission_request_id(
        mission
    )

    if not SHA512_RE.fullmatch(
        mission[
            "capability_mission_request_id"
        ]
    ):
        errors.append(
            "capability_mission_request_id is not canonical SHA-512"
        )

    errors.extend(
        validate_mission_request(
            mission
        )
    )

    returned = {
        "schema_version":
            "1.0",
        "capability_mission_request_reference":
            mission[
                "capability_mission_request_id"
            ],
        "object_id":
            object_id,
        "occupancy_witness_reference":
            "occupancy:a",
        "returning_capability":
            "Goblin:a",
        "bounded_findings": [
            "two unresolved signal routes remain"
        ],
        "evidence_references": [
            "evidence:a"
        ],
        "observed_effects": [
            {
                "effect": "uncertainty frontier refined"
            }
        ],
        "unresolved_signals": [
            {
                "signal": "route-b"
            }
        ],
        "discriminating_evidence_needs": [
            {
                "need": "additional provenance-bearing sample"
            }
        ],
        "cartographic_change_references": [
            "cartography:update:a"
        ],
        "restriction_findings": [],
        "continuity_state":
            "CONTINUOUS",
        "stick_reference":
            "stick:a",
        "final_coordinates": {
            "position": "terrain-edge"
        },
        "return_coordinates": {
            "position": "occupied-origin"
        },
        "completion_assessment":
            "PARTIAL",
        "provenance_route": [
            object_id,
            mission[
                "capability_mission_request_id"
            ],
            "evidence:a",
            "stick:a"
        ],
        "returned_at":
            "2026-08-07T19:28:00-04:00",
    }

    returned[
        "capability_return_id"
    ] = compute_capability_return_id(
        returned
    )

    if not SHA512_RE.fullmatch(
        returned[
            "capability_return_id"
        ]
    ):
        errors.append(
            "capability_return_id is not canonical SHA-512"
        )

    errors.extend(
        validate_capability_return(
            returned
        )
    )

    if (
        mission[
            "capability_mission_request_id"
        ]
        == object_id
    ):
        errors.append(
            "Mission Request identity collapsed into object identity"
        )

    if (
        returned[
            "capability_return_id"
        ]
        == object_id
    ):
        errors.append(
            "Capability Return identity collapsed into object identity"
        )

    if (
        returned[
            "capability_return_id"
        ]
        == mission[
            "capability_mission_request_id"
        ]
    ):
        errors.append(
            "Capability Return identity collapsed into mission identity"
        )

    changed = dict(
        mission
    )

    changed[
        "active_question"
    ] = (
        "which evidence route should be tested next?"
    )

    changed[
        "capability_mission_request_id"
    ] = compute_mission_request_id(
        changed
    )

    if (
        changed[
            "capability_mission_request_id"
        ]
        == mission[
            "capability_mission_request_id"
        ]
    ):
        errors.append(
            "material mission change did not change Mission Request identity"
        )

    blocked = dict(
        returned
    )

    blocked[
        "completion_assessment"
    ] = "BLOCKED"

    blocked[
        "restriction_findings"
    ] = []

    blocked[
        "unresolved_signals"
    ] = []

    blocked[
        "capability_return_id"
    ] = compute_capability_return_id(
        blocked
    )

    blocked_errors = validate_capability_return(
        blocked
    )

    if not any(
        "BLOCKED Capability Return"
        in error
        for error in blocked_errors
    ):
        errors.append(
            "BLOCKED return incorrectly permitted without blocking basis"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-E CAPABILITY MISSION REQUEST / RETURN: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-E CAPABILITY MISSION REQUEST / RETURN: PASS"
    )
    print(
        "Question -> mission / mission -> movement boundary: BOUND"
    )
    print(
        "Governance / TOC / authorization / evidence constraints: PRESERVED"
    )
    print(
        "Bounded findings / evidence / unresolved signals / return route: PRESERVED"
    )
    print(
        "COMPLETED / PARTIAL / BLOCKED return assessment: LOCKED"
    )
    print(
        "Proportional force / formation / Goblin Signal / ACTIVE: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
