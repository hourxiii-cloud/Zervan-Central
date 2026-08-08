#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "runtime"
    / "RING4_RUNTIME_STATE_OPERATIONS_CLOSURE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "runtime"
    / "ring4_closure_receipt.schema.json"
)

RUNNER = (
    ROOT
    / "tools"
    / "validate_ring4.py"
)

HYDRATION = (
    "R3-I",
    "tools/validate_hydration.py",
    "tests/test_hydration.py",
)

COMPONENTS = [
    (
        "R4-A",
        "tools/validate_restriction_constriction.py",
        "tests/test_restriction_constriction.py",
    ),
    (
        "R4-B",
        "tools/validate_collapse_boundary.py",
        "tests/test_collapse_boundary.py",
    ),
    (
        "R4-C",
        "tools/validate_landing_witness.py",
        "tests/test_landing_witness.py",
    ),
    (
        "R4-D",
        "tools/validate_reflight_trigger.py",
        "tests/test_reflight_trigger.py",
    ),
    (
        "R4-E",
        "tools/validate_closing_witness.py",
        "tests/test_closing_witness.py",
    ),
    (
        "R4-F",
        "tools/validate_replay_envelope.py",
        "tests/test_replay_envelope.py",
    ),
    (
        "R4-G",
        "tools/validate_scar_record.py",
        "tests/test_scar_record.py",
    ),
    (
        "R4-H",
        "tools/validate_scar_replay.py",
        "tests/test_scar_replay.py",
    ),
    (
        "R4-I",
        "tools/validate_runtime_state_continuity.py",
        "tests/test_runtime_state_continuity.py",
    ),
]

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


def compute_receipt_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "ring4_closure_receipt_id"
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


def run_python(path):
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def run_tests(path):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            str(ROOT / path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def validate_receipt(record):
    errors = []

    if (
        record.get("ring4_closure_receipt_id")
        != compute_receipt_id(record)
    ):
        errors.append(
            "ring4_closure_receipt_id does not recompute from receipt"
        )

    exact = {
        "native_version":
            "vTemporal.41.0",
        "ring":
            "R4",
        "promotion_state":
            "CANDIDATE",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "ring1_dependency_state":
            "PASS",
        "ring2_dependency_state":
            "PASS",
        "ring3_dependency_state":
            "PASS",
        "hydration_handoff_state":
            "BOUND",
        "tranche6_coverage_state":
            "COMPLETE",
        "source_boundary_state":
            "PRESERVED",
        "one_object_continuity_state":
            "PRESERVED",
        "state_domain_separation_state":
            "PRESERVED",
        "coordinate_continuity_state":
            "PRESERVED",
        "lineage_continuity_state":
            "PRESERVED",
        "evidence_boundary_continuity_state":
            "PRESERVED",
        "evidence_ceiling_continuity_state":
            "PRESERVED",
        "cartography_continuity_state":
            "PRESERVED",
        "stick_continuity_state":
            "PRESERVED",
        "provenance_continuity_state":
            "PRESERVED",
        "responsibility_integrity_state":
            "PRESERVED",
        "post_convergence_control_state":
            "PRESERVED",
        "replay_fidelity_state":
            "PRESERVED",
        "scar_integrity_state":
            "PRESERVED",
        "failure_lock_state":
            "PRESERVED",
        "closure_state":
            "VALIDATED_CANDIDATE",
    }

    for field, expected in exact.items():
        if record.get(field) != expected:
            errors.append(
                f"{field} must be {expected}"
            )

    states = record.get(
        "component_states",
        {}
    )

    expected_names = {
        item[0]
        for item in COMPONENTS
    }

    if set(states) != expected_names:
        errors.append(
            "component_states must contain exactly R4-A through R4-I"
        )
    else:
        for name in sorted(expected_names):
            if states.get(name) != "PASS":
                errors.append(
                    f"{name} closure state must be PASS"
                )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "Ring 4 Closure Receipt requires provenance_route"
        )

    return errors


def validate():
    errors = []

    # --------------------------------------------------------
    # Required closure artifacts
    # --------------------------------------------------------

    for path, label in (
        (
            CONTRACT,
            "R4-J closure contract"
        ),
        (
            SCHEMA,
            "R4-J closure schema"
        ),
        (
            RUNNER,
            "Ring 4 aggregate runner"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    # --------------------------------------------------------
    # Hydration handoff + every R4 component must exist.
    # --------------------------------------------------------

    for name, validator_path, tests_path in (
        [HYDRATION] + COMPONENTS
    ):
        if not (
            ROOT / validator_path
        ).exists():
            errors.append(
                f"missing {name} validator"
            )

        if not (
            ROOT / tests_path
        ).exists():
            errors.append(
                f"missing {name} tests"
            )

    if errors:
        return errors

    # --------------------------------------------------------
    # Schema
    # --------------------------------------------------------

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R4-J schema JSON: {exc}"
        ]

    # --------------------------------------------------------
    # Inner rings must independently pass.
    # --------------------------------------------------------

    for ring in (
        1,
        2,
        3,
    ):
        result = run_python(
            f"tools/validate_ring{ring}.py"
        )

        if result.returncode != 0:
            errors.append(
                f"Ring {ring} dependency validation failed"
            )

    # --------------------------------------------------------
    # R3-I Hydration handoff must independently pass.
    # --------------------------------------------------------

    hydration_validation = run_python(
        HYDRATION[1]
    )

    hydration_tests = run_tests(
        HYDRATION[2]
    )

    if hydration_validation.returncode != 0:
        errors.append(
            "R3-I Hydration validator failed"
        )

    if hydration_tests.returncode != 0:
        errors.append(
            "R3-I Hydration tests failed"
        )

    # --------------------------------------------------------
    # Every R4-A through R4-I validator/test independently
    # passes. R4-J does NOT recursively invoke itself.
    # --------------------------------------------------------

    for name, validator_path, tests_path in COMPONENTS:
        validation = run_python(
            validator_path
        )

        testing = run_tests(
            tests_path
        )

        if validation.returncode != 0:
            errors.append(
                f"{name} validator failed"
            )

        if testing.returncode != 0:
            errors.append(
                f"{name} tests failed"
            )

    # --------------------------------------------------------
    # Aggregate runner must contain exact R4-A -> R4-J order.
    # --------------------------------------------------------

    runner_text = RUNNER.read_text(
        encoding="utf-8"
    )

    expected_order = [
        item[0]
        for item in COMPONENTS
    ] + [
        "R4-J"
    ]

    positions = []

    for name in expected_order:
        token = f'"{name}"'

        pos = runner_text.find(
            token
        )

        if pos == -1:
            errors.append(
                f"Ring 4 runner does not contain {name}"
            )
        else:
            positions.append(
                (
                    name,
                    pos,
                )
            )

    if (
        len(positions)
        == len(expected_order)
    ):
        actual_order = [
            name
            for name, _ in sorted(
                positions,
                key=lambda item: item[1]
            )
        ]

        if actual_order != expected_order:
            errors.append(
                "Ring 4 aggregate order is not R4-A through R4-J"
            )

    # --------------------------------------------------------
    # Contract locks
    # --------------------------------------------------------

    normalized = " ".join(
        CONTRACT.read_text(
            encoding="utf-8"
        ).split()
    )

    locks = [
        "R4-J introduces no new analytical primitive.",
        "Ring 4 depends on complete Rings 1, 2, and 3.",
        "Outer closure != permission to mutate inner doctrine.",
        "Implementation ring placement != source tranche redefinition.",
        "Hydration remains the R3-I handoff into Runtime State Operations.",
        "THE ROOM IS ONE ANALYTICAL OBJECT.",
        "Runtime change != object replacement.",
        "Restriction is not deletion.",
        "Narrowing != compression out.",
        "Most correct supported state != absolute truth.",
        "Collapse != compression.",
        "Collapse != summary.",
        "Collapse != deletion.",
        "Collapse != new world.",
        "Capabilities may cease movement without ceasing occupation.",
        "Landing != EXITED.",
        "Landing does not manufacture Reflight.",
        "Acknowledgment does not authorize Reflight.",
        "Emotion does not authorize Reflight.",
        "Celebration does not authorize Reflight.",
        "Laughter does not authorize Reflight.",
        "Repetition does not authorize Reflight.",
        "Conversational continuation does not authorize Reflight.",
        "Trigger != execution.",
        "Trigger != authority.",
        "After convergence, do not rebuild or re-explain the Room without a new analytical trigger.",
        "Smallest sufficient response != compression of the Room.",
        "Closing Witness MUST bind the same Room identity.",
        "Replay is not creation of a duplicate world.",
        "Replay is reopening the same Room at a preserved observational coordinate.",
        "Replay reconstructing an approximation is a failure.",
        "A Scar is evidence that Terrain has previously affected movement.",
        "Scar != warning label.",
        "Scar != confidence score.",
        "Challenge does not erase history.",
        "Ignore-with-evidence does not erase history.",
        "Branch does not manufacture distinct-object identity.",
        "Operation PASS != chain PASS.",
        "Ring 4 closure requires R4-I PASS.",
        "Room state != representation state.",
        "Room state != execution state.",
        "Representation state != execution state.",
        "State-domain conflation is a runtime defect.",
        "Communication != ownership.",
        "Validation != authority.",
        "Composition != ownership collapse.",
        "Authority remains NONE unless valid governing state resolves otherwise.",
        "Human Gate remains ACTIVE.",
        "Write capability != authority.",
        "Closure != authority.",
        "Ring closure != execution authority.",
        "Ring closure != publication authority.",
        "Ring closure != certification authority.",
        "Ring closure != canonical promotion.",
        "VALIDATED_CANDIDATE != canonical promotion.",
        "Candidate closure != Git-main promotion.",
        "Human Gate promotion remains separately required.",
        "Tranche 6 coverage complete != complete v41 promotion.",
        "Tranche completion != canonical promotion.",
        "Aggregate closure adds proof.",
        "Aggregate closure does not erase structure.",
        "Hash != truth.",
        "Validation hash != authority.",
        "Receipt identity != promotion.",
        "Fail closed.",
        "Do not infer PASS through missing evidence.",
        "R4-J closes Ring 4 only.",
        "R4-J does not implement Tranche 7.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in normalized
        ):
            errors.append(
                f"missing R4-J lock: {lock}"
            )

    # --------------------------------------------------------
    # Closure schema must fail closed to candidate.
    # --------------------------------------------------------

    props = schema.get(
        "properties",
        {}
    )

    required_consts = {
        "native_version":
            "vTemporal.41.0",
        "ring":
            "R4",
        "promotion_state":
            "CANDIDATE",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "tranche6_coverage_state":
            "COMPLETE",
        "closure_state":
            "VALIDATED_CANDIDATE",
    }

    for field, expected in required_consts.items():
        if (
            props
            .get(field, {})
            .get("const")
            != expected
        ):
            errors.append(
                f"R4-J schema {field} must fail closed to {expected}"
            )

    forbidden = {
        "canonical_promotion",
        "execution_authorization",
        "publication_authorization",
        "certification_authorization",
        "main_branch_promotion",
        "tranche7_completion",
        "pmc_redefinition",
        "ccr_redefinition",
        "mc_redefinition",
        "raven_redefinition",
    }

    leaked = (
        set(props)
        & forbidden
    )

    if leaked:
        errors.append(
            "R4-J improperly absorbs promotion or downstream "
            "Tranche 7 semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    # --------------------------------------------------------
    # Deterministic closure receipt
    # --------------------------------------------------------

    receipt = {
        "schema_version":
            "1.0",
        "native_version":
            "vTemporal.41.0",
        "ring":
            "R4",
        "promotion_state":
            "CANDIDATE",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "ring1_dependency_state":
            "PASS",
        "ring2_dependency_state":
            "PASS",
        "ring3_dependency_state":
            "PASS",
        "hydration_handoff_state":
            "BOUND",
        "component_states": {
            name: "PASS"
            for name, _, _ in COMPONENTS
        },
        "tranche6_coverage_state":
            "COMPLETE",
        "source_boundary_state":
            "PRESERVED",
        "one_object_continuity_state":
            "PRESERVED",
        "state_domain_separation_state":
            "PRESERVED",
        "coordinate_continuity_state":
            "PRESERVED",
        "lineage_continuity_state":
            "PRESERVED",
        "evidence_boundary_continuity_state":
            "PRESERVED",
        "evidence_ceiling_continuity_state":
            "PRESERVED",
        "cartography_continuity_state":
            "PRESERVED",
        "stick_continuity_state":
            "PRESERVED",
        "provenance_continuity_state":
            "PRESERVED",
        "responsibility_integrity_state":
            "PRESERVED",
        "post_convergence_control_state":
            "PRESERVED",
        "replay_fidelity_state":
            "PRESERVED",
        "scar_integrity_state":
            "PRESERVED",
        "failure_lock_state":
            "PRESERVED",
        "closure_state":
            "VALIDATED_CANDIDATE",
        "provenance_route": [
            "ring1:validated",
            "ring2:validated",
            "ring3:validated",
            "r3-i:hydration-handoff",
            "r4-a:restriction-constriction",
            "r4-b:collapse-boundary",
            "r4-c:landing-witness",
            "r4-d:reflight-trigger",
            "r4-e:closing-witness",
            "r4-f:replay-envelope",
            "r4-g:scar-record",
            "r4-h:scar-replay",
            "r4-i:cross-operation-integrity",
            "r4-j:aggregate-closure",
        ],
        "closed_at":
            "2026-08-07T21:10:00-04:00",
    }

    receipt[
        "ring4_closure_receipt_id"
    ] = compute_receipt_id(
        receipt
    )

    if not SHA512_RE.fullmatch(
        receipt[
            "ring4_closure_receipt_id"
        ]
    ):
        errors.append(
            "Ring 4 Closure Receipt ID is not canonical SHA-512"
        )

    errors.extend(
        validate_receipt(
            receipt
        )
    )

    # --------------------------------------------------------
    # Negative probes
    # --------------------------------------------------------

    broken_component = json.loads(
        json.dumps(receipt)
    )

    broken_component[
        "component_states"
    ][
        "R4-F"
    ] = "FAIL"

    broken_component[
        "ring4_closure_receipt_id"
    ] = compute_receipt_id(
        broken_component
    )

    component_errors = validate_receipt(
        broken_component
    )

    if not any(
        "R4-F closure state must be PASS"
        in error
        for error in component_errors
    ):
        errors.append(
            "R4-J incorrectly permitted failed component closure"
        )

    promoted = dict(
        receipt
    )

    promoted[
        "promotion_state"
    ] = "CANONICAL"

    promoted[
        "ring4_closure_receipt_id"
    ] = compute_receipt_id(
        promoted
    )

    promotion_errors = validate_receipt(
        promoted
    )

    if not any(
        "promotion_state must be CANDIDATE"
        in error
        for error in promotion_errors
    ):
        errors.append(
            "R4-J incorrectly permitted canonical promotion"
        )

    authority_promoted = dict(
        receipt
    )

    authority_promoted[
        "authority_state"
    ] = "WRITE"

    authority_promoted[
        "ring4_closure_receipt_id"
    ] = compute_receipt_id(
        authority_promoted
    )

    authority_errors = validate_receipt(
        authority_promoted
    )

    if not any(
        "authority_state must be NONE"
        in error
        for error in authority_errors
    ):
        errors.append(
            "R4-J incorrectly permitted authority promotion"
        )

    broken_boundary = dict(
        receipt
    )

    broken_boundary[
        "source_boundary_state"
    ] = "BROKEN"

    broken_boundary[
        "ring4_closure_receipt_id"
    ] = compute_receipt_id(
        broken_boundary
    )

    boundary_errors = validate_receipt(
        broken_boundary
    )

    if not any(
        "source_boundary_state must be PRESERVED"
        in error
        for error in boundary_errors
    ):
        errors.append(
            "R4-J incorrectly permitted broken source boundary"
        )

    broken_continuity = dict(
        receipt
    )

    broken_continuity[
        "one_object_continuity_state"
    ] = "BROKEN"

    broken_continuity[
        "ring4_closure_receipt_id"
    ] = compute_receipt_id(
        broken_continuity
    )

    continuity_errors = validate_receipt(
        broken_continuity
    )

    if not any(
        "one_object_continuity_state must be PRESERVED"
        in error
        for error in continuity_errors
    ):
        errors.append(
            "R4-J incorrectly permitted broken one-object continuity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-J RING 4 RUNTIME STATE OPERATIONS "
            "AGGREGATE CLOSURE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-J RING 4 RUNTIME STATE OPERATIONS "
        "AGGREGATE CLOSURE: PASS"
    )
    print(
        "Rings 1 / 2 / 3 dependencies: PASS"
    )
    print(
        "R3-I Hydration handoff: BOUND"
    )
    print(
        "R4-A -> R4-I independent validators/tests: PASS"
    )
    print(
        "Tranche 6 runtime coverage: COMPLETE"
    )
    print(
        "One Room / state-domain / coordinate / lineage continuity: PRESERVED"
    )
    print(
        "Evidence boundary / ceiling / Cartography / Stick: PRESERVED"
    )
    print(
        "Replay / Scar / post-convergence fidelity: PRESERVED"
    )
    print(
        "Responsibility / provenance / failure locks: PRESERVED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Promotion: CANDIDATE"
    )
    print(
        "Closure: VALIDATED_CANDIDATE"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
