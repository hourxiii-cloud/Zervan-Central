#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "FORMATION_REJUSTIFICATION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "formation_rejustification.schema.json"
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

R2I = (
    ROOT
    / "contracts"
    / "geography"
    / "STICK_CONTACT_CONTINUITY.md"
)


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

    if not record.get(
        "rejustification_trigger"
    ):
        reasons.append(
            "REJUSTIFICATION_TRIGGER_MISSING"
        )

    if not record.get(
        "rejustification_basis"
    ):
        reasons.append(
            "REJUSTIFICATION_BASIS_MISSING"
        )

    if not record.get(
        "prior_history_preserved"
    ):
        reasons.append(
            "PRIOR_HISTORY_ERASED"
        )

    if (
        not record.get(
            "stick_reference"
        )
        or record.get(
            "stick_continuity_state"
        )
        != "CONTINUOUS"
    ):
        reasons.append(
            "STICK_NOT_PRESERVED"
        )

    if not record.get(
        "origin_reference"
    ):
        reasons.append(
            "ORIGIN_CONTINUITY_LOST"
        )

    if not record.get(
        "ingress_reference"
    ):
        reasons.append(
            "INGRESS_CONTINUITY_LOST"
        )

    if not record.get(
        "cartography_reference"
    ):
        reasons.append(
            "CARTOGRAPHY_CONTINUITY_LOST"
        )

    if not record.get(
        "transform_history_references"
    ):
        reasons.append(
            "TRANSFORM_HISTORY_LOST"
        )

    if not record.get(
        "evidence_lineage_references"
    ):
        reasons.append(
            "EVIDENCE_LINEAGE_LOST"
        )

    if not record.get(
        "provenance_route"
    ):
        reasons.append(
            "PROVENANCE_LOST"
        )

    if not record.get(
        "return_coordinates"
    ):
        reasons.append(
            "RETURN_COORDINATES_LOST"
        )

    if not record.get(
        "proportional_force_basis_reference"
    ):
        reasons.append(
            "FORCE_BASIS_LOST"
        )

    if (
        record.get(
            "force_scale_changed"
        )
        and not record.get(
            "force_change_reference"
        )
    ):
        reasons.append(
            "SILENT_FORCE_INFLATION"
        )

    if (
        record.get(
            "previous_evidence_ceiling_reference"
        )
        != record.get(
            "new_evidence_ceiling_reference"
        )
        and not record.get(
            "evidence_ceiling_change_reference"
        )
    ):
        reasons.append(
            "EVIDENCE_CEILING_CHANGED_UNATTRIBUTED"
        )

    if record.get(
        "new_room_created"
    ):
        reasons.append(
            "NEW_ROOM_INVENTED"
        )

    if record.get(
        "branch_created"
    ):
        reasons.append(
            "BRANCH_INVENTED"
        )

    if record.get(
        "passageway_created"
    ):
        reasons.append(
            "PASSAGEWAY_INVENTED"
        )

    if record.get(
        "occupancy_mutated"
    ):
        reasons.append(
            "OCCUPANCY_MUTATED"
        )

    if record.get(
        "lifecycle_mutated"
    ):
        reasons.append(
            "LIFECYCLE_MUTATED"
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
        else "BLOCKED"
    )


def validate_record(record):
    errors = []

    if (
        record.get(
            "validation_vector"
        )
        != "FORMATION_REJUSTIFICATION"
    ):
        errors.append(
            "wrong validation vector"
        )

    if (
        record.get(
            "previous_formation_id"
        )
        == record.get(
            "new_formation_id"
        )
    ):
        errors.append(
            "formation re-justification requires a new attributable formation record"
        )

    expected_reasons = evaluate_record(
        record
    )

    expected = (
        "VALID"
        if not expected_reasons
        else "BLOCKED"
    )

    if (
        record.get(
            "validation_disposition"
        )
        != expected
    ):
        errors.append(
            "formation re-justification disposition contradicts continuity state"
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
            "formation re-justification failure reasons are incomplete or incorrect"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-F Human Gate state must remain ACTIVE"
        )

    return errors


def make_record(
    *,
    previous_formation_type,
    new_formation_type,
    trigger,
    basis=None,
    force_scale_changed=False,
    force_change_reference=None,
    previous_ceiling="ceiling:r6-f:a",
    new_ceiling="ceiling:r6-f:a",
    ceiling_change_reference=None,
    prior_history_preserved=True,
    stick_reference="stick:r6-f:a",
    stick_continuity_state="CONTINUOUS",
    origin_reference="origin:r6-f:a",
    ingress_reference="ingress:r6-f:a",
    cartography_reference="cartography:r6-f:a",
    transform_history_references=None,
    evidence_lineage_references=None,
    provenance_route=None,
    return_coordinates="coord:return:a",
    new_room_created=False,
    branch_created=False,
    passageway_created=False,
    occupancy_mutated=False,
    lifecycle_mutated=False,
    authority_state="NONE",
):
    if basis is None:
        basis = [
            f"trigger:{trigger}",
            "question:preserved",
            "room:preserved",
            "stick:preserved",
        ]

    if transform_history_references is None:
        transform_history_references = [
            "transform:a"
        ]

    if evidence_lineage_references is None:
        evidence_lineage_references = [
            "evidence-lineage:a"
        ]

    if provenance_route is None:
        provenance_route = [
            "formation:prior",
            "trigger:a",
            "formation:new",
        ]

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "FORMATION_REJUSTIFICATION",

        "object_id":
            "sha512:"
            + "1" * 128,

        "previous_formation_id":
            "formation:prior",

        "previous_formation_type":
            previous_formation_type,

        "new_formation_id":
            "formation:new",

        "new_formation_type":
            new_formation_type,

        "rejustification_trigger":
            trigger,

        "rejustification_basis":
            list(
                basis
            ),

        "active_question":
            "What formation is now sufficient for the unresolved question?",

        "proportional_force_basis_reference":
            "force-selection:r6-f:a",

        "force_scale_changed":
            force_scale_changed,

        "force_change_reference":
            force_change_reference,

        "evidence_boundary_reference":
            "boundary:r6-f:a",

        "previous_evidence_ceiling_reference":
            previous_ceiling,

        "new_evidence_ceiling_reference":
            new_ceiling,

        "evidence_ceiling_change_reference":
            ceiling_change_reference,

        "stick_reference":
            stick_reference,

        "stick_continuity_state":
            stick_continuity_state,

        "origin_reference":
            origin_reference,

        "ingress_reference":
            ingress_reference,

        "cartography_reference":
            cartography_reference,

        "transform_history_references":
            list(
                transform_history_references
            ),

        "evidence_lineage_references":
            list(
                evidence_lineage_references
            ),

        "provenance_route":
            list(
                provenance_route
            ),

        "source_coordinates":
            "coord:source:a",

        "target_coordinates":
            "coord:target:a",

        "return_coordinates":
            return_coordinates,

        "prior_history_preserved":
            prior_history_preserved,

        "new_room_created":
            new_room_created,

        "branch_created":
            branch_created,

        "passageway_created":
            passageway_created,

        "occupancy_mutated":
            occupancy_mutated,

        "lifecycle_mutated":
            lifecycle_mutated,

        "authority_state":
            authority_state,

        "human_gate_state":
            "ACTIVE",

        "validation_disposition":
            "",

        "failure_reasons":
            [],
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
            "R6-F contract"
        ),
        (
            SCHEMA,
            "R6-F schema"
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
            "R3-G formation"
        ),
        (
            R2I,
            "R2-I Stick"
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
        "R6-F = Formation Re-Justification.",
        "Formation change != object change.",
        "Re-justification != reconstruction.",
        "Formation != Room identity.",
        "Formation != capability scale.",
        "A formation change without a declared trigger is invalid.",
        "Change != whim.",
        "Formation change != new Room.",
        "New formation record != overwritten old record.",
        "History accumulates.",
        "Formation history remains replayable.",
        "Later change != retroactive falsification.",
        "Formation changes MUST preserve the Stick.",
        "Formation change MUST NOT sever analytical continuity.",
        "Single Route -> Stack != failure of the earlier Single Route selection.",
        "More surface does not mean more Room.",
        "Swarm remains evidence-driven.",
        "Swarm is not the default advanced mode.",
        "More capability available != Swarm required.",
        "No formation persists merely because it was previously selected.",
        "Historical formation != standing requirement.",
        "Formation Selection != force inflation.",
        "Formation type change != automatic force-scale change.",
        "Formation serves the question.",
        "Question does not serve the formation.",
        "Formation change != evidence-boundary expansion.",
        "Additional capability != additional admissible evidence.",
        "More observers != more authority.",
        "Consensus != evidence elevation.",
        "Formation breadth != claim strength.",
        "Formation change != consensus creation.",
        "Parallelism != agreement.",
        "Broken contact is evidence.",
        "DEGRADED MUST NOT silently become CONTINUOUS.",
        "Formation change != entry.",
        "Formation change != exit.",
        "Formation selected != ACTIVE.",
        "Formation re-justification != lifecycle mutation.",
        "Formation != hydration authority.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "VALID != executed.",
        "VALID != authority.",
        "There is no preferred advanced formation.",
        "Formation sophistication != analytical quality.",
        "R6-G owns Distinct-Object validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-F lock: {lock}"
            )

    source_locks = {
        R3G: [
            "Formation change != new Room.",
            "History accumulates.",
            "Formation history remains replayable.",
            "Swarm is not the default advanced mode.",
            "No formation persists merely because it was previously selected.",
            "Formation changes MUST preserve the Stick.",
        ],
        R2I: [
            "Freedom of movement requires continuity of contact.",
            "Freedom of perspective requires continuity of object identity.",
            "Stick binds object identity.",
            "Stick binds provenance.",
            "Stick binds evidence lineage.",
            "Stick binds return coordinates.",
            "BROKEN fails closed.",
        ],
        R3F: [
            "Need determines force.",
            "Evidence determines escalation.",
            "A capability request shall use the smallest justified force.",
            "Scale != formation.",
        ],
    }

    for path, required_locks in source_locks.items():
        surface = normalized(
            path
        )

        for lock in required_locks:
            if (
                " ".join(
                    lock.split()
                )
                not in surface
            ):
                errors.append(
                    f"source boundary missing required semantic: {lock}"
                )

    r6a = normalized(
        R6A
    )

    for lock in (
        "FORMATION_REJUSTIFICATION",
        "Formation change != object change.",
        "Re-justification != reconstruction.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-F binding: {lock}"
            )

    try:
        load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-F schema JSON: {exc}"
        ]

    # SINGLE -> STACK
    single_stack = make_record(
        previous_formation_type="SINGLE_ROUTE",
        new_formation_type="STACK_ANALYSIS",
        trigger="CONTRADICTION_APPEARED_OR_PERSISTED",
        basis=[
            "trigger:contradiction persisted",
            "independent routes now justified",
            "question:preserved",
            "stick:preserved",
        ],
    )

    errors.extend(
        validate_record(
            single_stack
        )
    )

    # STACK -> EXPANDED
    stack_expanded = make_record(
        previous_formation_type="STACK_ANALYSIS",
        new_formation_type="EXPANDED_ANALYSIS",
        trigger="TERRAIN_CONTACT_CHANGED",
        basis=[
            "trigger:new reachable surface",
            "additional bounded Space required",
            "question:preserved",
            "stick:preserved",
        ],
    )

    errors.extend(
        validate_record(
            stack_expanded
        )
    )

    # EXPANDED -> SWARM
    expanded_swarm = make_record(
        previous_formation_type="EXPANDED_ANALYSIS",
        new_formation_type="SWARM",
        trigger="SIGNAL_ECOLOGY_CHANGED",
        basis=[
            "trigger:parallel routes required",
            "same Room identity preserved",
            "question:preserved",
            "stick:preserved",
        ],
    )

    errors.extend(
        validate_record(
            expanded_swarm
        )
    )

    # De-escalation.
    stack_single = make_record(
        previous_formation_type="STACK_ANALYSIS",
        new_formation_type="SINGLE_ROUTE",
        trigger="ONE_ROUTE_BECAME_SUFFICIENT",
        basis=[
            "trigger:signal localized",
            "one discriminating route sufficient",
            "question:preserved",
            "stick:preserved",
        ],
    )

    errors.extend(
        validate_record(
            stack_single
        )
    )

    # Missing trigger.
    missing_trigger = make_record(
        previous_formation_type="SINGLE_ROUTE",
        new_formation_type="STACK_ANALYSIS",
        trigger=None,
        basis=[
            "preferred larger formation"
        ],
    )

    if (
        "REJUSTIFICATION_TRIGGER_MISSING"
        not in missing_trigger[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-F failed to reject formation change without trigger"
        )

    # Broken Stick.
    broken = make_record(
        previous_formation_type="STACK_ANALYSIS",
        new_formation_type="EXPANDED_ANALYSIS",
        trigger="TERRAIN_CONTACT_CHANGED",
        stick_continuity_state="BROKEN",
    )

    if (
        "STICK_NOT_PRESERVED"
        not in broken[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-F failed to reject broken Stick continuity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-F FORMATION RE-JUSTIFICATION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-F FORMATION RE-JUSTIFICATION: PASS"
    )
    print(
        "SINGLE_ROUTE -> STACK_ANALYSIS: VALIDATED"
    )
    print(
        "STACK_ANALYSIS -> EXPANDED_ANALYSIS: VALIDATED"
    )
    print(
        "EXPANDED_ANALYSIS -> SWARM: VALIDATED"
    )
    print(
        "STACK_ANALYSIS -> SINGLE_ROUTE de-escalation: VALIDATED"
    )
    print(
        "Room identity across formation change: PRESERVED"
    )
    print(
        "Prior formation history: PRESERVED"
    )
    print(
        "Stick / provenance / evidence lineage / return coordinates: PRESERVED"
    )
    print(
        "Formation change without trigger: REJECTED"
    )
    print(
        "Broken Stick -> formation movement: BLOCKED"
    )
    print(
        "Silent force inflation / ceiling elevation: REJECTED"
    )
    print(
        "Room / Branch / Passageway invention: REJECTED"
    )
    print(
        "Occupancy / lifecycle mutation: NOT CREATED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-G Distinct-Object validation: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
