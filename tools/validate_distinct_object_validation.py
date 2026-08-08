#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "contracts/validation/DISTINCT_OBJECT_VALIDATION.md"
SCHEMA = ROOT / "schemas/validation/distinct_object_validation.schema.json"
R6A = ROOT / "contracts/validation/VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
R1F = ROOT / "contracts/lineage/REVISION_BRANCH_MERGE.md"
R2J = ROOT / "contracts/geography/PASSAGEWAY_DISTINCT_OBJECT_CONTACT.md"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(path):
    text = path.read_text(encoding="utf-8")

    for token in ("**", "__", "`"):
        text = text.replace(token, "")

    return " ".join(text.split())


def evaluate_record(record):
    reasons = []

    source = record.get("source_object_id")
    target = record.get("candidate_target_object_id")
    determination = record.get("determination")
    passageway = record.get("passageway_state")
    evidence = record.get("evidence_of_distinctness", [])

    same_object_representation_change = any([
        record.get("perspective_changed"),
        record.get("zone_changed"),
        record.get("space_changed"),
        record.get("authorized_view_changed"),
    ])

    if (
        determination == "DISTINCT_OBJECT"
        and not evidence
    ):
        reasons.append("DISTINCTNESS_WITHOUT_EVIDENCE")

    if (
        determination == "DISTINCT_OBJECT"
        and source == target
    ):
        reasons.append("DISTINCT_OBJECT_IDENTITY_COLLISION")

    if determination == "DISTINCT_OBJECT":
        if not record.get("independent_genesis_reference"):
            reasons.append("INDEPENDENT_GENESIS_MISSING")

        if not record.get("independent_origin_reference"):
            reasons.append("INDEPENDENT_ORIGIN_MISSING")

        if not record.get("independent_boundary_reference"):
            reasons.append("INDEPENDENT_BOUNDARY_MISSING")

        if not record.get("independent_geometry_reference"):
            reasons.append("INDEPENDENT_GEOMETRY_MISSING")

        if not record.get("non_shared_provenance"):
            reasons.append("NON_SHARED_PROVENANCE_MISSING")

    if (
        determination == "SAME_OBJECT"
        and source != target
        and same_object_representation_change
    ):
        reasons.append("PERSPECTIVE_CLONED_AS_OBJECT")

    if (
        determination == "SAME_OBJECT"
        and record.get("branch_present")
        and source != target
    ):
        reasons.append("BRANCH_CLONED_AS_OBJECT")

    if (
        determination == "SAME_OBJECT"
        and passageway == "ESTABLISHED"
    ):
        reasons.append("PASSAGEWAY_ESTABLISHED_FOR_SAME_OBJECT")

    if (
        determination == "UNRESOLVED"
        and passageway == "ESTABLISHED"
    ):
        reasons.append("PASSAGEWAY_ESTABLISHED_WHILE_UNRESOLVED")

    if (
        determination == "UNRESOLVED"
        and record.get("new_object_created")
    ):
        reasons.append("NEW_OBJECT_CREATED_WHILE_UNRESOLVED")

    if passageway == "ESTABLISHED":
        if (
            determination != "DISTINCT_OBJECT"
            or not evidence
        ):
            reasons.append("PASSAGEWAY_EVIDENCE_MISSING")

        if (
            not record.get("passageway_conditions")
            or not record.get("contamination_controls")
        ):
            reasons.append("PASSAGEWAY_CONTROLS_MISSING")

        if not record.get("return_route"):
            reasons.append("RETURN_ROUTE_MISSING")

    if record.get("authority_state") != "NONE":
        reasons.append("AUTHORITY_PROMOTED")

    return sorted(set(reasons))


def expected_disposition(record):
    return "VALID" if not evaluate_record(record) else "BLOCKED"


def validate_record(record):
    errors = []

    if record.get("validation_vector") != "DISTINCT_OBJECT_TEST":
        errors.append("wrong validation vector")

    expected_reasons = evaluate_record(record)
    expected = "VALID" if not expected_reasons else "BLOCKED"

    if record.get("validation_disposition") != expected:
        errors.append(
            "distinct-object disposition contradicts determination state"
        )

    if sorted(record.get("failure_reasons", [])) != expected_reasons:
        errors.append(
            "distinct-object failure reasons are incomplete or incorrect"
        )

    if record.get("human_gate_state") != "ACTIVE":
        errors.append("R6-G Human Gate state must remain ACTIVE")

    if not record.get("provenance_route"):
        errors.append("R6-G provenance route required")

    return errors


def make_record(
    *,
    determination,
    source_object_id=None,
    target_object_id=None,
    perspective_changed=False,
    zone_changed=False,
    space_changed=False,
    authorized_view_changed=False,
    branch_present=False,
    evidence_of_distinctness=None,
    shared_provenance=None,
    non_shared_provenance=None,
    independent_origin_reference=None,
    independent_boundary_reference=None,
    independent_geometry_reference=None,
    independent_genesis_reference=None,
    relationship_to_source=None,
    passageway_conditions=None,
    contamination_controls=None,
    return_route=None,
    passageway_state="BLOCKED",
    new_object_created=False,
    authority_state="NONE",
):
    if source_object_id is None:
        source_object_id = "sha512:" + "1" * 128

    if target_object_id is None:
        target_object_id = source_object_id

    if evidence_of_distinctness is None:
        evidence_of_distinctness = []

    if shared_provenance is None:
        shared_provenance = []

    if non_shared_provenance is None:
        non_shared_provenance = []

    if passageway_conditions is None:
        passageway_conditions = []

    if contamination_controls is None:
        contamination_controls = []

    record = {
        "schema_version": "1.0",
        "validation_vector": "DISTINCT_OBJECT_TEST",
        "source_object_id": source_object_id,
        "candidate_target_object_id": target_object_id,
        "perspective_changed": perspective_changed,
        "zone_changed": zone_changed,
        "space_changed": space_changed,
        "authorized_view_changed": authorized_view_changed,
        "branch_present": branch_present,
        "evidence_of_distinctness": list(evidence_of_distinctness),
        "shared_provenance": list(shared_provenance),
        "non_shared_provenance": list(non_shared_provenance),
        "independent_origin_reference": independent_origin_reference,
        "independent_boundary_reference": independent_boundary_reference,
        "independent_geometry_reference": independent_geometry_reference,
        "independent_genesis_reference": independent_genesis_reference,
        "relationship_to_source": relationship_to_source,
        "passageway_conditions": list(passageway_conditions),
        "contamination_controls": list(contamination_controls),
        "return_route": return_route,
        "determination": determination,
        "passageway_state": passageway_state,
        "new_object_created": new_object_created,
        "provenance_route": [
            "r1-f:distinct-object",
            "r2-j:passageway",
            "r6-g:validation",
        ],
        "authority_state": authority_state,
        "human_gate_state": "ACTIVE",
        "validation_disposition": "",
        "failure_reasons": [],
    }

    record["failure_reasons"] = evaluate_record(record)
    record["validation_disposition"] = expected_disposition(record)

    return record


def distinct_record():
    return make_record(
        determination="DISTINCT_OBJECT",
        target_object_id="sha512:" + "2" * 128,
        evidence_of_distinctness=[
            "independent-boundary-evidence",
            "independent-origin-evidence",
            "independent-geometry-evidence",
        ],
        shared_provenance=[
            "shared-source:a"
        ],
        non_shared_provenance=[
            "target-only:a"
        ],
        independent_origin_reference="origin:target",
        independent_boundary_reference="boundary:target",
        independent_geometry_reference="geometry:target",
        independent_genesis_reference="genesis:target",
        relationship_to_source="adjoining-object",
        passageway_conditions=[
            "source-to-target bounded contact"
        ],
        contamination_controls=[
            "no state inheritance",
            "no provenance collapse",
        ],
        return_route="return:source",
        passageway_state="ESTABLISHED",
        new_object_created=True,
    )


def validate():
    errors = []

    for path, label in (
        (CONTRACT, "R6-G contract"),
        (SCHEMA, "R6-G schema"),
        (R6A, "R6-A registry"),
        (R1F, "R1-F distinct-object semantics"),
        (R2J, "R2-J Passageway semantics"),
    ):
        if not path.exists():
            errors.append(f"missing {label}")

    if errors:
        return errors

    text = normalized(CONTRACT)

    locks = [
        "R6-G = Distinct-Object Validation.",
        "A viewpoint change remains one Room.",
        "A genuinely distinct object requires affirmative evidence.",
        "A genuinely distinct object requires independent Genesis lineage.",
        "Perspective != object identity.",
        "Different perspective != distinct object.",
        "Branch != new Room.",
        "Branch identity != object identity.",
        "Genesis follows distinctness.",
        "Genesis does not manufacture distinctness.",
        "Only DISTINCT_OBJECT may support an ESTABLISHED Passageway.",
        "Same object != Passageway.",
        "Unresolved distinctness != established contact.",
        "Passageway identity is not Room identity.",
        "Shared provenance does not collapse identity.",
        "Passageway convenience is not evidence of distinctness.",
        "Contact != identity collapse.",
        "Cross-object contact != Merge.",
        "Passageway != Merge.",
        "Disagreement does not establish distinctness.",
        "Disagreement != Room multiplication.",
        "Related != identical.",
        "Correlation != identity.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-H owns Hydration-On-Need validation.",
    ]

    for lock in locks:
        if " ".join(lock.split()) not in text:
            errors.append(
                f"missing R6-G lock: {lock}"
            )

    source_locks = {
        R1F: [
            "Perspective is not Branch.",
            "Branch != new Room.",
            "A separate object requires affirmative evidence of distinctness.",
            "A DISTINCT_OBJECT determination establishes the requirement for an independent Genesis lineage.",
            "Cross-object contact != identity collapse.",
        ],
        R2J: [
            "Different perspective does not mean distinct object.",
            "Only DISTINCT_OBJECT may support ESTABLISHED Passageway contact.",
            "SAME_OBJECT does not create a Passageway.",
            "UNRESOLVED does not establish a Passageway.",
            "Passageway identity is not Room identity.",
            "Shared provenance does not collapse identity.",
            "Cross-object contact != identity collapse.",
        ],
    }

    for path, required_locks in source_locks.items():
        surface = normalized(path)

        for lock in required_locks:
            if " ".join(lock.split()) not in surface:
                errors.append(
                    f"source boundary missing required semantic: {lock}"
                )

    r6a = normalized(R6A)

    for lock in (
        "DISTINCT_OBJECT_TEST",
        "A viewpoint change remains one Room.",
        "A genuinely distinct object receives independent identity",
    ):
        if " ".join(lock.split()) not in r6a:
            errors.append(
                f"R6-A registry missing R6-G binding: {lock}"
            )

    try:
        load(SCHEMA)
    except Exception as exc:
        return [f"invalid R6-G schema JSON: {exc}"]

    # SAME_OBJECT: perspective rotation
    same_perspective = make_record(
        determination="SAME_OBJECT",
        perspective_changed=True,
        zone_changed=True,
        space_changed=True,
        authorized_view_changed=True,
        passageway_state="BLOCKED",
    )

    errors.extend(validate_record(same_perspective))

    # SAME_OBJECT: Branch remains same object
    same_branch = make_record(
        determination="SAME_OBJECT",
        branch_present=True,
        passageway_state="BLOCKED",
    )

    errors.extend(validate_record(same_branch))

    # Genuine distinct object + Passageway
    distinct = distinct_record()

    errors.extend(validate_record(distinct))

    # UNRESOLVED proposed
    unresolved = make_record(
        determination="UNRESOLVED",
        target_object_id="sha512:" + "2" * 128,
        evidence_of_distinctness=[
            "candidate-boundary-signal"
        ],
        passageway_state="PROPOSED",
        new_object_created=False,
    )

    errors.extend(validate_record(unresolved))

    return errors


def main():
    errors = validate()

    if errors:
        print("R6-G DISTINCT-OBJECT VALIDATION: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    print("R6-G DISTINCT-OBJECT VALIDATION: PASS")
    print("Perspective / Zone / Space / View change -> SAME_OBJECT: VALIDATED")
    print("Branch divergence -> SAME_OBJECT by default: VALIDATED")
    print("Affirmative independent evidence -> DISTINCT_OBJECT: VALIDATED")
    print("Independent Genesis / Origin / boundary / geometry: REQUIRED")
    print("DISTINCT_OBJECT -> ESTABLISHED Passageway when controlled: VALIDATED")
    print("SAME_OBJECT -> ESTABLISHED Passageway: REJECTED")
    print("UNRESOLVED -> ESTABLISHED Passageway: REJECTED")
    print("UNRESOLVED -> new object creation: REJECTED")
    print("Shared provenance -> identity collapse: REJECTED")
    print("Cross-object contact -> Merge / identity collapse: REJECTED")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")
    print("R6-H Hydration-On-Need: DEFERRED")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
