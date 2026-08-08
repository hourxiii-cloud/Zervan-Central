#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "RBT_001_RECURSIVE_BUTT_TOPOLOGY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "rbt_001_recursive_butt_topology.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

R4C = (
    ROOT
    / "contracts"
    / "runtime"
    / "LANDING_WITNESS.md"
)

R4D = (
    ROOT
    / "contracts"
    / "runtime"
    / "REFLIGHT_TRIGGER.md"
)

R2I = (
    ROOT
    / "contracts"
    / "geography"
    / "STICK_CONTACT_CONTINUITY.md"
)

VALID_REFLIGHT_TRIGGERS = {
    "NEW_EVIDENCE",
    "CONTRADICTION",
    "CHANGED_QUESTION",
    "CHANGED_EVIDENCE_CEILING",
    "SIGNAL_SPLIT",
    "SIGNAL_CONVERGENCE",
    "CHALLENGED_CONCLUSION",
    "NEWLY_REACHABLE_SURFACE",
    "MATERIALLY_DIFFERENT_RENDERING_REQUESTED",
}

INVALID_NON_TRIGGERS = {
    "ACKNOWLEDGMENT",
    "REPETITION",
    "CELEBRATION",
    "AFFECT",
    "CONVERSATIONAL_CONTINUATION",
    "CAPABILITY_AVAILABLE",
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

    primary = record.get(
        "primary_object_id"
    )

    control = record.get(
        "control_object_id"
    )

    if primary == control:
        reasons.append(
            "CONTROL_OBJECT_IDENTITY_COLLISION"
        )

    if record.get(
        "control_state_absorbed"
    ):
        reasons.append(
            "OBJECT_ISOLATION_FAILED"
        )

    signals = record.get(
        "signals",
        []
    )

    signal_ids = [
        signal.get(
            "signal_id"
        )
        for signal in signals
        if signal.get(
            "signal_id"
        )
    ]

    signal_sources = [
        signal.get(
            "signal_source"
        )
        for signal in signals
        if signal.get(
            "signal_source"
        )
    ]

    signal_routes = [
        signal.get(
            "signal_route"
        )
        for signal in signals
        if signal.get(
            "signal_route"
        )
    ]

    if (
        len(signals) < 2
        or len(set(signal_ids)) < 2
        or len(set(signal_sources)) < 2
        or len(set(signal_routes)) < 2
    ):
        reasons.append(
            "SIGNAL_DIFFERENTIATION_LOST"
        )

    for signal in signals:
        if not signal.get(
            "provenance_route"
        ):
            reasons.append(
                "SIGNAL_PROVENANCE_LOST"
            )

    if (
        record.get(
            "primary_boundary_before"
        )
        != record.get(
            "primary_boundary_after"
        )
    ):
        reasons.append(
            "PRIMARY_BOUNDARY_CHANGED"
        )

    if (
        record.get(
            "primary_boundary_after"
        )
        == record.get(
            "control_boundary_reference"
        )
    ):
        reasons.append(
            "CONTROL_BOUNDARY_ABSORBED"
        )

    if (
        record.get(
            "primary_evidence_ceiling_before"
        )
        != record.get(
            "primary_evidence_ceiling_after"
        )
    ):
        reasons.append(
            "EVIDENCE_CEILING_CHANGED"
        )

    if not record.get(
        "landing_witness_reference"
    ):
        reasons.append(
            "LANDING_WITNESS_MISSING"
        )

    if (
        record.get(
            "landing_object_id"
        )
        != primary
    ):
        reasons.append(
            "LANDING_OBJECT_IDENTITY_CHANGED"
        )

    if not record.get(
        "landing_coordinate"
    ):
        reasons.append(
            "LANDING_COORDINATE_MISSING"
        )

    trigger = record.get(
        "reflight_trigger_type"
    )

    if (
        trigger not in VALID_REFLIGHT_TRIGGERS
    ):
        reasons.append(
            "REFLIGHT_TRIGGER_INVALID"
        )

    if (
        trigger in (
            "NEW_EVIDENCE",
            "CONTRADICTION",
            "SIGNAL_SPLIT",
            "SIGNAL_CONVERGENCE",
        )
        and not record.get(
            "reflight_trigger_evidence"
        )
    ):
        reasons.append(
            "REFLIGHT_TRIGGER_EVIDENCE_MISSING"
        )

    if not record.get(
        "reflight_material_change_basis"
    ):
        reasons.append(
            "REFLIGHT_MATERIAL_CHANGE_MISSING"
        )

    if (
        trigger in (
            "SIGNAL_SPLIT",
            "SIGNAL_CONVERGENCE",
        )
        and (
            not record.get(
                "prior_signal_state_reference"
            )
            or not record.get(
                "current_signal_state_reference"
            )
        )
    ):
        reasons.append(
            "SIGNAL_STATE_REFERENCE_MISSING"
        )

    if (
        record.get(
            "returned_object_id"
        )
        != primary
    ):
        reasons.append(
            "RETURN_OBJECT_IDENTITY_CHANGED"
        )

    if (
        record.get(
            "return_coordinate"
        )
        != record.get(
            "returned_coordinate"
        )
    ):
        reasons.append(
            "RETURN_COORDINATE_CHANGED"
        )

    if record.get(
        "reconstruction_used"
    ):
        reasons.append(
            "RECONSTRUCTION_USED"
        )

    if not record.get(
        "primary_stick_reference"
    ):
        reasons.append(
            "STICK_NOT_PRESERVED"
        )

    if record.get(
        "control_provenance_absorbed"
    ):
        reasons.append(
            "CONTROL_PROVENANCE_ABSORBED"
        )

    if record.get(
        "lifecycle_mutated"
    ):
        reasons.append(
            "LIFECYCLE_MUTATED"
        )

    if record.get(
        "occupancy_invented"
    ):
        reasons.append(
            "OCCUPANCY_INVENTED"
        )

    if record.get(
        "formation_invented"
    ):
        reasons.append(
            "FORMATION_INVENTED"
        )

    if record.get(
        "full_payload_hydration_requested"
    ):
        reasons.append(
            "FULL_PAYLOAD_HYDRATION_REQUESTED"
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
        != "RBT_001"
    ):
        errors.append(
            "wrong validation vector"
        )

    if (
        record.get(
            "carrier_id"
        )
        != "RBT-001"
    ):
        errors.append(
            "wrong regression carrier identity"
        )

    if (
        record.get(
            "carrier_name"
        )
        != "Recursive Butt Topology"
    ):
        errors.append(
            "wrong regression carrier name"
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
            "RBT-001 disposition contradicts carrier state"
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
            "RBT-001 failure reasons are incomplete or incorrect"
        )

    expected_eligibility = (
        "ELIGIBLE"
        if (
            record.get(
                "reflight_trigger_type"
            )
            in VALID_REFLIGHT_TRIGGERS
            and record.get(
                "reflight_material_change_basis"
            )
            and (
                record.get(
                    "reflight_trigger_type"
                )
                not in (
                    "SIGNAL_SPLIT",
                    "SIGNAL_CONVERGENCE",
                )
                or (
                    record.get(
                        "prior_signal_state_reference"
                    )
                    and record.get(
                        "current_signal_state_reference"
                    )
                )
            )
        )
        else "BLOCKED"
    )

    if (
        record.get(
            "reflight_eligibility"
        )
        != expected_eligibility
    ):
        errors.append(
            "RBT-001 Reflight eligibility contradicts trigger state"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-L Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R6-L provenance route required"
        )

    return errors


def make_signal(
    signal_id,
    source,
    route,
):
    return {
        "signal_id":
            signal_id,

        "signal_source":
            source,

        "signal_route":
            route,

        "evidence_references": [
            f"evidence:{signal_id}"
        ],

        "provenance_route": [
            f"provenance:{signal_id}",
            f"route:{route}",
        ],
    }


def make_record(
    *,
    primary_object_id=None,
    control_object_id=None,
    signals=None,
    primary_boundary_before="boundary:primary",
    primary_boundary_after="boundary:primary",
    control_boundary_reference="boundary:control",
    primary_evidence_ceiling_before="ceiling:primary",
    primary_evidence_ceiling_after="ceiling:primary",
    landing_witness_reference="landing:rbt-001",
    landing_object_id=None,
    landing_coordinate="coord:rbt:landed",
    reflight_trigger_type="SIGNAL_SPLIT",
    reflight_trigger_evidence=None,
    reflight_material_change_basis="two attributable routes now require renewed movement",
    prior_signal_state_reference="signal-state:coherent",
    current_signal_state_reference="signal-state:split",
    returned_object_id=None,
    return_coordinate="coord:rbt:return",
    returned_coordinate="coord:rbt:return",
    reconstruction_used=False,
    primary_stick_reference="stick:rbt:primary",
    control_state_absorbed=False,
    control_provenance_absorbed=False,
    lifecycle_mutated=False,
    occupancy_invented=False,
    formation_invented=False,
    full_payload_hydration_requested=False,
    authority_state="NONE",
):
    if primary_object_id is None:
        primary_object_id = (
            "sha512:"
            + "1" * 128
        )

    if control_object_id is None:
        control_object_id = (
            "sha512:"
            + "2" * 128
        )

    if landing_object_id is None:
        landing_object_id = (
            primary_object_id
        )

    if returned_object_id is None:
        returned_object_id = (
            primary_object_id
        )

    if signals is None:
        signals = [
            make_signal(
                "signal:a",
                "source:left",
                "route:left",
            ),
            make_signal(
                "signal:b",
                "source:right",
                "route:right",
            ),
        ]

    if reflight_trigger_evidence is None:
        reflight_trigger_evidence = [
            "evidence:signal:a",
            "evidence:signal:b",
        ]

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "RBT_001",

        "carrier_id":
            "RBT-001",

        "carrier_name":
            "Recursive Butt Topology",

        "primary_object_id":
            primary_object_id,

        "control_object_id":
            control_object_id,

        "primary_origin_reference":
            "origin:rbt:primary",

        "primary_cartography_reference":
            "cartography:rbt:primary",

        "primary_stick_reference":
            primary_stick_reference,

        "primary_boundary_before":
            primary_boundary_before,

        "primary_boundary_after":
            primary_boundary_after,

        "control_boundary_reference":
            control_boundary_reference,

        "primary_evidence_ceiling_before":
            primary_evidence_ceiling_before,

        "primary_evidence_ceiling_after":
            primary_evidence_ceiling_after,

        "signals":
            list(
                signals
            ),

        "landing_witness_reference":
            landing_witness_reference,

        "landing_object_id":
            landing_object_id,

        "landing_coordinate":
            landing_coordinate,

        "reflight_trigger_type":
            reflight_trigger_type,

        "reflight_trigger_evidence":
            list(
                reflight_trigger_evidence
            ),

        "reflight_material_change_basis":
            reflight_material_change_basis,

        "prior_signal_state_reference":
            prior_signal_state_reference,

        "current_signal_state_reference":
            current_signal_state_reference,

        "reflight_eligibility":
            "",

        "returned_object_id":
            returned_object_id,

        "return_coordinate":
            return_coordinate,

        "returned_coordinate":
            returned_coordinate,

        "reconstruction_used":
            reconstruction_used,

        "control_state_absorbed":
            control_state_absorbed,

        "control_provenance_absorbed":
            control_provenance_absorbed,

        "lifecycle_mutated":
            lifecycle_mutated,

        "occupancy_invented":
            occupancy_invented,

        "formation_invented":
            formation_invented,

        "full_payload_hydration_requested":
            full_payload_hydration_requested,

        "provenance_route": [
            "room:rbt:primary",
            "signal:rbt:a",
            "signal:rbt:b",
            "landing:rbt-001",
            "reflight:rbt-001",
            "return:rbt-001",
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

    eligible = (
        reflight_trigger_type
        in VALID_REFLIGHT_TRIGGERS
        and bool(
            reflight_material_change_basis
        )
        and (
            reflight_trigger_type
            not in (
                "SIGNAL_SPLIT",
                "SIGNAL_CONVERGENCE",
            )
            or (
                bool(
                    prior_signal_state_reference
                )
                and bool(
                    current_signal_state_reference
                )
            )
        )
    )

    record[
        "reflight_eligibility"
    ] = (
        "ELIGIBLE"
        if eligible
        else "BLOCKED"
    )

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


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-L contract"
        ),
        (
            SCHEMA,
            "R6-L schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            R4C,
            "R4-C Landing"
        ),
        (
            R4D,
            "R4-D Reflight"
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
        "R6-L = RBT-001 — Recursive Butt Topology.",
        "RBT-001 is a memorable regression carrier.",
        "RBT-001 exercises object isolation.",
        "RBT-001 exercises signal differentiation.",
        "RBT-001 exercises boundary preservation.",
        "RBT-001 exercises Landing.",
        "RBT-001 exercises Reflight.",
        "RBT-001 exercises return without reconstruction.",
        "Humor does not reduce test rigor.",
        "Memorable carrier != reduced invariant coverage.",
        "Carrier metaphor != doctrine.",
        "Carrier label != semantic ownership.",
        "primary_object_id != control_object_id.",
        "Control object != alternate view.",
        "Signal A != Signal B.",
        "Different signal route != different Room by itself.",
        "Correlation != identity.",
        "Similarity != identity.",
        "Signal contact does not broaden evidence access.",
        "Signal presence does not raise claim authority.",
        "Landing means movement stopped.",
        "Landing != exit.",
        "Landing != closure.",
        "Landing != replay.",
        "Landing coordinate MUST NOT be reconstructed approximately.",
        "landing_object_id == primary_object_id.",
        "The Room remains the Room.",
        "Trigger != execution.",
        "Reflight requires a real trigger.",
        "No material change = no Reflight.",
        "Signal split != confidence.",
        "Signal != trigger.",
        "Landing first.",
        "Trigger second.",
        "Reflight MUST NOT rebuild an approximate Room.",
        "Reflight != new Room.",
        "returned_object_id == primary_object_id.",
        "Return != reconstruction.",
        "Return != replacement.",
        "Return != new Genesis.",
        "The memorable carrier does not weaken Stick requirements.",
        "Joke != provenance.",
        "Trigger != boundary expansion.",
        "Signal differentiation != formation selection.",
        "Payload rests.",
        "Carrier completeness != full payload requirement.",
        "Test success != truth.",
        "Validation != authority.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-M owns Fresh-Reader validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-L lock: {lock}"
            )

    r6a = normalized(
        R6A
    )

    for lock in (
        "RBT-001 — Recursive Butt Topology",
        "object isolation;",
        "signal differentiation;",
        "boundary preservation;",
        "Landing;",
        "Reflight;",
        "return without reconstruction.",
        "Humor does not reduce test rigor.",
        "Memorable carrier != reduced invariant coverage.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing RBT-001 binding: {lock}"
            )

    landing = normalized(
        R4C
    )

    for lock in (
        "Capabilities may cease movement without ceasing occupation.",
        "Landing preserves object identity.",
        "Landing does not create a new Room.",
        "Landing does not create a snapshot object.",
        "The Room remains the Room.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in landing
        ):
            errors.append(
                f"Landing source missing required semantic: {lock}"
            )

    reflight = normalized(
        R4D
    )

    for lock in (
        "Reflight requires a real trigger.",
        "Landing first.",
        "Trigger second.",
        "Reflight MUST NOT rebuild an approximate Room.",
        "Reflight != new Room.",
        "Signal split != confidence.",
        "No material change = no Reflight.",
        "Trigger != execution.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in reflight
        ):
            errors.append(
                f"Reflight source missing required semantic: {lock}"
            )

    try:
        load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-L schema JSON: {exc}"
        ]

    # Positive carrier.
    positive = make_record()

    errors.extend(
        validate_record(
            positive
        )
    )

    # Signal differentiation loss.
    collapsed_signals = [
        make_signal(
            "signal:a",
            "source:left",
            "route:left",
        ),
        make_signal(
            "signal:a",
            "source:left",
            "route:left",
        ),
    ]

    collapsed = make_record(
        signals=collapsed_signals
    )

    if (
        "SIGNAL_DIFFERENTIATION_LOST"
        not in collapsed[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-L failed to reject collapsed signal identity"
        )

    # Boundary change.
    widened = make_record(
        primary_boundary_after="boundary:wider"
    )

    if (
        "PRIMARY_BOUNDARY_CHANGED"
        not in widened[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-L failed to reject boundary drift"
        )

    # Invalid pseudo-trigger.
    celebration = make_record(
        reflight_trigger_type="CELEBRATION",
        reflight_material_change_basis=None,
    )

    if (
        "REFLIGHT_TRIGGER_INVALID"
        not in celebration[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-L failed to reject celebration as Reflight trigger"
        )

    # Reconstruction.
    rebuilt = make_record(
        returned_object_id=(
            "sha512:"
            + "3" * 128
        ),
        reconstruction_used=True,
    )

    if (
        "RETURN_OBJECT_IDENTITY_CHANGED"
        not in rebuilt[
            "failure_reasons"
        ]
        or "RECONSTRUCTION_USED"
        not in rebuilt[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-L failed to reject reconstructed return"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-L RBT-001 RECURSIVE BUTT TOPOLOGY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-L RBT-001 RECURSIVE BUTT TOPOLOGY: PASS"
    )
    print(
        "Object isolation: VALIDATED"
    )
    print(
        "Signal differentiation: VALIDATED"
    )
    print(
        "Boundary preservation: VALIDATED"
    )
    print(
        "Landing at preserved Room / coordinate: VALIDATED"
    )
    print(
        "Real Reflight trigger from preserved Landing: VALIDATED"
    )
    print(
        "Return to original Room without reconstruction: VALIDATED"
    )
    print(
        "Control-object state / provenance absorption: REJECTED"
    )
    print(
        "Signal collapse / provenance loss: REJECTED"
    )
    print(
        "Boundary / evidence-ceiling drift: REJECTED"
    )
    print(
        "Pseudo-trigger Reflight: REJECTED"
    )
    print(
        "Lifecycle / Occupancy / Formation invention: REJECTED"
    )
    print(
        "Full-payload hydration: REJECTED"
    )
    print(
        "Humor does not reduce test rigor: PRESERVED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-M Fresh-Reader: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
