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
    / "QUALIFICATION_RECORD_DISPOSITION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "qualification_record.schema.json"
)

DISTINCT_SCHEMA = (
    ROOT
    / "schemas"
    / "lineage"
    / "distinct_object_record.schema.json"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

DISPOSITIONS = {
    "QUALIFIED",
    "PROVISIONAL",
    "REJECTED",
    "DEGRADED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_qualification_record_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "qualification_record_id"
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


def validate_record(record):
    errors = []

    expected = compute_qualification_record_id(
        record
    )

    if (
        record.get("qualification_record_id")
        != expected
    ):
        errors.append(
            "qualification_record_id does not recompute from Record"
        )

    disposition = record.get(
        "qualification_disposition"
    )

    if disposition not in DISPOSITIONS:
        errors.append(
            "invalid qualification disposition"
        )

    for field in (
        "qualification_request_reference",
        "object_id",
        "provisional_room_id",
        "origin_reference",
        "ingress_reference",
        "qualification_mission",
        "active_question",
        "qualification_lead",
        "participating_capabilities",
        "evidence_boundary",
        "evidence_ceiling",
        "observed_geometry",
        "provenance_anchors",
        "disposition_basis",
        "return_coordinates",
        "replay_route",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Qualification Record requires {field}"
            )

    included = set(
        record.get(
            "included_evidence",
            []
        )
    )

    excluded = set(
        record.get(
            "excluded_evidence",
            []
        )
    )

    overlap = included & excluded

    if overlap:
        errors.append(
            "evidence cannot be both included and excluded: "
            + ", ".join(
                sorted(overlap)
            )
        )

    if (
        disposition == "PROVISIONAL"
        and not (
            record.get("unresolved_contradictions")
            or record.get("uncertainty_frontiers")
            or record.get(
                "recommended_formation_or_next_reconnaissance_action"
            )
        )
    ):
        errors.append(
            "PROVISIONAL disposition must preserve unresolved basis "
            "or next reconnaissance"
        )

    if (
        disposition == "DEGRADED"
        and not (
            record.get("restricted_or_inaccessible_surfaces")
            or record.get("unresolved_contradictions")
            or any(
                "degrad" in item.lower()
                for item in record.get(
                    "disposition_basis",
                    []
                )
            )
        )
    ):
        errors.append(
            "DEGRADED disposition must identify degradation"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R3-B Qualification Record contract"
        ),
        (
            SCHEMA,
            "R3-B Qualification Record schema"
        ),
        (
            DISTINCT_SCHEMA,
            "R1-F Distinct Object schema"
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
        distinct_schema = load(
            DISTINCT_SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid schema JSON: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            []
        )
    )

    expected = {
        "qualification_record_id",
        "qualification_request_reference",
        "object_id",
        "provisional_room_id",
        "origin_reference",
        "ingress_reference",
        "qualification_mission",
        "active_question",
        "qualification_lead",
        "participating_capabilities",
        "occupied_zone_id",
        "occupied_space_id",
        "included_evidence",
        "excluded_evidence",
        "evidence_boundary",
        "evidence_ceiling",
        "observed_geometry",
        "cartographic_change_references",
        "provenance_anchors",
        "uncertainty_frontiers",
        "unresolved_contradictions",
        "restricted_or_inaccessible_surfaces",
        "adjoining_object_candidates",
        "distinct_object_result",
        "recommended_formation_or_next_reconnaissance_action",
        "qualification_disposition",
        "disposition_basis",
        "return_coordinates",
        "replay_route",
        "provenance_route",
        "completed_at",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Qualification Record missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    dispositions = set(
        schema
        .get("properties", {})
        .get("qualification_disposition", {})
        .get("enum", [])
    )

    if dispositions != DISPOSITIONS:
        errors.append(
            "Qualification dispositions are not source-locked"
        )

    r3b_distinct = set(
        schema
        .get("properties", {})
        .get("distinct_object_result", {})
        .get("enum", [])
    )

    r1f_distinct = set(
        distinct_schema
        .get("properties", {})
        .get("determination", {})
        .get("enum", [])
    )

    if r3b_distinct != r1f_distinct:
        errors.append(
            "R3-B distinct-object vocabulary diverges from R1-F"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "room_lifecycle_state",
        "ready_state",
        "formation_selection_id",
        "selected_formation",
        "analytical_occupancy_id",
        "occupancy_witness_id",
        "goblin_signal_event_id",
        "capability_mission_id",
        "execution_authorization",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R3-B improperly absorbs downstream semantics: "
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
        "Qualification produces an attributable Record.",
        "Record != Request.",
        "Finding != request mutation.",
        "Qualification Record identity is not Room Object identity.",
        "Qualification Record identity is not Qualification Request identity.",
        "Provisional Room ID != object identity.",
        "Lead != truth owner.",
        "Participant != authority.",
        "Qualification occupation != analytical occupation.",
        "Excluded != absent.",
        "Restricted != absent.",
        "Disposition strength <= evidence support.",
        "Observed geometry != complete geometry.",
        "Qualification Record != Cartography.",
        "QUALIFIED != complete certainty.",
        "Unknown remains unknown.",
        "Scar != confidence.",
        "Restricted != nonexistent.",
        "Candidate adjoining object != distinct object.",
        "Perspective difference != distinct object.",
        "Recommendation != formation selection.",
        "Recommendation != execution.",
        "QUALIFIED / PROVISIONAL / REJECTED / DEGRADED are the complete R3-B qualification disposition vocabulary.",
        "QUALIFIED != READY.",
        "QUALIFIED != ACTIVE.",
        "QUALIFIED != publication authority.",
        "QUALIFIED != execution authority.",
        "PROVISIONAL != failure.",
        "PROVISIONAL != QUALIFIED.",
        "Rejected != erased.",
        "DEGRADED != nonexistent.",
        "DEGRADED != REJECTED by default.",
        "Disposition != lifecycle mutation.",
        "Record != event propagation.",
        "Qualification Record != Formation Selection Record.",
        "Qualification Record != Occupancy Witness.",
        "Write capability != authority.",
        "No Room lifecycle transition yet.",
        "No formation selection yet.",
        "No analytical occupation yet.",
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
                f"missing R3-B lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    request_id = (
        "sha512:"
        + "2" * 128
    )

    probe = {
        "schema_version": "1.0",
        "qualification_request_reference":
            request_id,
        "object_id":
            object_id,
        "provisional_room_id":
            "room:provisional:a",
        "origin_reference":
            "origin:a",
        "ingress_reference":
            "ingress:a",
        "qualification_mission":
            "establish mission fitness",
        "active_question":
            "is the Room sufficiently established?",
        "qualification_lead":
            "Goblin:lead",
        "participating_capabilities": [
            "Goblin:lead"
        ],
        "occupied_zone_id":
            "sha512:" + "3" * 128,
        "occupied_space_id":
            "sha512:" + "4" * 128,
        "included_evidence": [
            "evidence:a"
        ],
        "excluded_evidence": [
            "evidence:b"
        ],
        "evidence_boundary": {
            "included": [
                "evidence:a"
            ],
            "excluded": [
                "evidence:b"
            ],
        },
        "evidence_ceiling":
            "CEILING:QUALIFICATION",
        "observed_geometry": {
            "stable_regions": [
                "region:a"
            ]
        },
        "cartographic_change_references": [
            "cartography:update:a"
        ],
        "provenance_anchors": [
            "provenance:a"
        ],
        "uncertainty_frontiers": [
            {
                "surface": "frontier:a"
            }
        ],
        "unresolved_contradictions": [],
        "restricted_or_inaccessible_surfaces": [
            {
                "surface": "restricted:a"
            }
        ],
        "adjoining_object_candidates": [],
        "distinct_object_result":
            "SAME_OBJECT",
        "recommended_formation_or_next_reconnaissance_action":
            "single-route analytical formation may be considered",
        "qualification_disposition":
            "QUALIFIED",
        "disposition_basis": [
            "identity sufficiently resolved",
            "boundary sufficiently resolved",
            "provenance sufficiently resolved",
            "geometry sufficient for declared mission",
        ],
        "return_coordinates": {
            "position": "qualification-origin"
        },
        "replay_route": [
            "orientation:a",
            "cartography:update:a",
        ],
        "provenance_route": [
            object_id,
            "origin:a",
            "ingress:a",
            request_id,
        ],
        "completed_at":
            "2026-08-07T19:19:00-04:00",
    }

    probe[
        "qualification_record_id"
    ] = compute_qualification_record_id(
        probe
    )

    if not SHA512_RE.fullmatch(
        probe[
            "qualification_record_id"
        ]
    ):
        errors.append(
            "qualification_record_id is not canonical SHA-512"
        )

    errors.extend(
        validate_record(
            probe
        )
    )

    if (
        probe["qualification_record_id"]
        == object_id
    ):
        errors.append(
            "Qualification Record identity collapsed into object identity"
        )

    if (
        probe["qualification_record_id"]
        == request_id
    ):
        errors.append(
            "Qualification Record identity collapsed into request identity"
        )

    changed = dict(
        probe
    )

    changed[
        "qualification_disposition"
    ] = "PROVISIONAL"

    changed[
        "recommended_formation_or_next_reconnaissance_action"
    ] = "additional reconnaissance required"

    changed[
        "qualification_record_id"
    ] = compute_qualification_record_id(
        changed
    )

    if (
        probe["qualification_record_id"]
        == changed["qualification_record_id"]
    ):
        errors.append(
            "material qualification finding change did not change Record identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-B QUALIFICATION RECORD / DISPOSITION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-B QUALIFICATION RECORD / DISPOSITION: PASS"
    )
    print(
        "Qualification evidence / findings: ATTRIBUTABLE"
    )
    print(
        "QUALIFIED / PROVISIONAL / REJECTED / DEGRADED: LOCKED"
    )
    print(
        "Uncertainty / restrictions / contradictions: PRESERVED"
    )
    print(
        "Distinct-object result / return / replay route: PRESERVED"
    )
    print(
        "Lifecycle / formation / analytical occupation: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
