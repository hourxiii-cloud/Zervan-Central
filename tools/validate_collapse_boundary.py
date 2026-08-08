#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT / "contracts" / "runtime" / "COLLAPSE_BOUNDARY.md"
)

SCHEMA = (
    ROOT / "schemas" / "runtime" / "collapse_boundary.schema.json"
)

R4A = (
    ROOT / "tools" / "validate_restriction_constriction.py"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_collapse_boundary_id(record):
    preimage = {
        k: v
        for k, v in record.items()
        if k != "collapse_boundary_id"
    }

    return (
        "sha512:"
        + hashlib.sha512(
            canonical_bytes(preimage)
        ).hexdigest()
    )


def load(path):
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def validate_boundary(record):
    errors = []

    if (
        record.get("collapse_boundary_id")
        != compute_collapse_boundary_id(record)
    ):
        errors.append(
            "collapse_boundary_id does not recompute from boundary"
        )

    for field in (
        "object_id",
        "source_representation_references",
        "collapse_trigger",
        "collapse_justification",
        "governing_evidence_references",
        "pre_collapse_possibilities",
        "retained_possibilities",
        "surviving_uncertainty",
        "evidence_boundary",
        "evidence_ceiling",
        "preserved_invariants",
        "pre_collapse_state_reference",
        "return_route",
        "cartography_reference",
        "stick_reference",
        "provenance_anchors",
        "governance_reference",
        "authorization_reference",
        "provenance_route",
    ):
        if record.get(field) in (None, "", {}, []):
            errors.append(
                f"Collapse Boundary requires {field}"
            )

    pre = set(
        record.get(
            "pre_collapse_possibilities",
            []
        )
    )

    removed = set(
        record.get(
            "removed_possibilities",
            []
        )
    )

    retained = set(
        record.get(
            "retained_possibilities",
            []
        )
    )

    deferred = set(
        record.get(
            "deferred_possibilities",
            []
        )
    )

    for label, states in (
        ("removed", removed),
        ("retained", retained),
        ("deferred", deferred),
    ):
        if not states.issubset(pre):
            errors.append(
                f"{label} possibilities must originate in pre-collapse set"
            )

    if removed & retained:
        errors.append(
            "possibility cannot be both removed and retained"
        )

    if removed & deferred:
        errors.append(
            "possibility cannot be both removed and deferred"
        )

    if retained & deferred:
        errors.append(
            "possibility cannot be both retained and deferred"
        )

    partition = (
        removed
        | retained
        | deferred
    )

    if partition != pre:
        errors.append(
            "removed + retained + deferred must exactly partition pre-collapse possibilities"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (CONTRACT, "R4-B Collapse Boundary contract"),
        (SCHEMA, "R4-B Collapse Boundary schema"),
        (R4A, "R4-A validator"),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    r4a = subprocess.run(
        [
            sys.executable,
            str(R4A),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if r4a.returncode != 0:
        errors.append(
            "R4-A dependency validation failed"
        )

    try:
        schema = load(SCHEMA)
    except Exception as exc:
        return [
            f"invalid R4-B schema JSON: {exc}"
        ]

    properties = set(
        schema.get("properties", {})
    )

    forbidden = {
        "landing_witness_id",
        "reflight_trigger_id",
        "closing_witness_id",
        "replay_envelope_id",
        "scar_record_id",
        "lifecycle_transition_id",
        "occupancy_mutation",
        "formation_selection_id",
        "new_room_object_id",
        "canonical_promotion",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R4-B improperly absorbs downstream or foreign semantics: "
            + ", ".join(sorted(leaked))
        )

    normalized = " ".join(
        CONTRACT.read_text(
            encoding="utf-8"
        ).split()
    )

    locks = [
        "Collapse is an evidence-driven signal and refinement event within the Room Object.",
        "Collapse records why the object can no longer support the prior range of possibilities at the current evidence ceiling.",
        "Collapse is not merely compression.",
        "Collapse is not summary.",
        "Collapse is not deletion.",
        "Collapse is not creation of another world.",
        "Collapse without governing evidence is prohibited.",
        "Collapse != new Room.",
        "Evidence drives collapse.",
        "Preference does not.",
        "Every removed, retained, or deferred possibility MUST originate in the pre-collapse possibility set.",
        "A possibility MUST NOT occupy more than one disposition simultaneously.",
        "The union of removed, retained, and deferred possibilities MUST equal the pre-collapse possibility set.",
        "Collapse MUST NOT silently lose a prior possibility.",
        "Retained != canonical truth.",
        "Removed != deleted.",
        "Deferred != absent.",
        "Collapse MUST preserve surviving uncertainty.",
        "One surviving possibility != absolute truth.",
        "Collapse cannot broaden evidence access.",
        "Collapse does not raise the evidence ceiling merely because possibilities were removed.",
        "Fewer possibilities != greater authority.",
        "Representation does not create truth authority.",
        "Collapse MUST NOT erase the structure required to understand the analytical journey.",
        "New frontier != new Room.",
        "Collapse alone != distinct-object establishment.",
        "History accumulates.",
        "Re-expansion != reconstruction of an approximate Room.",
        "Return route != automatic rollback authority.",
        "Collapse != Cartography deletion.",
        "Collapse MUST preserve the Stick.",
        "Collapse MUST NOT sever analytical continuity.",
        "Restriction != Collapse.",
        "Constriction != Collapse.",
        "Collapse narrows support.",
        "It does not erase analytical history.",
        "Collapse != lifecycle transition.",
        "Collapse Boundary != Occupancy Witness.",
        "Collapse Boundary != Formation Selection Record.",
        "Hydration != Collapse.",
        "Notification != Collapse.",
        "Repeated notification != governing evidence.",
        "Collapse != Landing.",
        "R4-C owns Landing Witness.",
        "Collapse != Reflight Trigger.",
        "R4-D owns Reflight Trigger.",
        "Collapse != Replay Envelope.",
        "No Landing semantics yet.",
        "No Reflight execution semantics yet.",
        "No Closing Witness semantics yet.",
        "No Replay semantics yet.",
        "No Scar Replay semantics yet.",
    ]

    for lock in locks:
        if " ".join(lock.split()) not in normalized:
            errors.append(
                f"missing R4-B lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    boundary = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "restriction_constriction_reference":
            "restriction:a",
        "source_representation_references": [
            "representation:a"
        ],
        "collapse_trigger":
            "further evidence eliminates prior possibility range",
        "collapse_justification": [
            "evidence:b makes STATE_B unsupportable at current ceiling"
        ],
        "governing_evidence_references": [
            "evidence:a",
            "evidence:b"
        ],
        "pre_collapse_possibilities": [
            "STATE_A",
            "STATE_B",
            "STATE_C"
        ],
        "removed_possibilities": [
            "STATE_B"
        ],
        "retained_possibilities": [
            "STATE_A"
        ],
        "deferred_possibilities": [
            "STATE_C"
        ],
        "surviving_uncertainty": [
            "STATE_C remains deferred because required evidence is unavailable"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "preserved_invariants": [
            "object identity",
            "origin continuity",
            "provenance",
            "representation history",
            "evidence lineage",
            "Cartography",
            "Stick",
            "return route"
        ],
        "newly_available_frontier": {
            "frontier": "discriminating evidence for STATE_C"
        },
        "re_expansion_considerations": [
            "new evidence supporting removed or deferred states"
        ],
        "pre_collapse_state_reference":
            "state:pre-collapse:a",
        "return_route": {
            "reference": "state:pre-collapse:a"
        },
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "provenance_anchors": [
            "provenance:a"
        ],
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "restriction:a",
            "evidence:b",
            "representation:a",
            "stick:a"
        ],
        "collapsed_at":
            "2026-08-07T20:12:00-04:00",
    }

    boundary[
        "collapse_boundary_id"
    ] = compute_collapse_boundary_id(
        boundary
    )

    if not SHA512_RE.fullmatch(
        boundary[
            "collapse_boundary_id"
        ]
    ):
        errors.append(
            "collapse_boundary_id is not canonical SHA-512"
        )

    errors.extend(
        validate_boundary(
            boundary
        )
    )

    lost_state = dict(
        boundary
    )

    lost_state[
        "deferred_possibilities"
    ] = []

    lost_state[
        "collapse_boundary_id"
    ] = compute_collapse_boundary_id(
        lost_state
    )

    lost_errors = validate_boundary(
        lost_state
    )

    if not any(
        "exactly partition"
        in error
        for error in lost_errors
    ):
        errors.append(
            "R4-B incorrectly permitted silent loss of a pre-collapse possibility"
        )

    overlap = dict(
        boundary
    )

    overlap[
        "removed_possibilities"
    ] = [
        "STATE_A",
        "STATE_B"
    ]

    overlap[
        "collapse_boundary_id"
    ] = compute_collapse_boundary_id(
        overlap
    )

    overlap_errors = validate_boundary(
        overlap
    )

    if not any(
        "both removed and retained"
        in error
        for error in overlap_errors
    ):
        errors.append(
            "R4-B incorrectly permitted overlapping possibility disposition"
        )

    invented = dict(
        boundary
    )

    invented[
        "retained_possibilities"
    ] = [
        "STATE_A",
        "STATE_NEW"
    ]

    invented[
        "collapse_boundary_id"
    ] = compute_collapse_boundary_id(
        invented
    )

    invented_errors = validate_boundary(
        invented
    )

    if not any(
        "originate in pre-collapse set"
        in error
        for error in invented_errors
    ):
        errors.append(
            "R4-B incorrectly permitted invented retained possibility"
        )

    changed = dict(
        boundary
    )

    changed[
        "collapse_trigger"
    ] = (
        "contradiction resolves against prior possibility range"
    )

    changed[
        "collapse_boundary_id"
    ] = compute_collapse_boundary_id(
        changed
    )

    if (
        changed[
            "collapse_boundary_id"
        ]
        == boundary[
            "collapse_boundary_id"
        ]
    ):
        errors.append(
            "material Collapse Boundary change did not change identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-B COLLAPSE BOUNDARY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-B COLLAPSE BOUNDARY: PASS"
    )
    print(
        "Evidence-driven refinement / one Room identity: LOCKED"
    )
    print(
        "Removed / retained / deferred partition: ENFORCED"
    )
    print(
        "Surviving uncertainty / provenance / return route: PRESERVED"
    )
    print(
        "Compression / deletion / invented certainty: REJECTED"
    )
    print(
        "New frontier != new Room: LOCKED"
    )
    print(
        "Landing / Reflight / Closure / Replay: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
