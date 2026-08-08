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
    / "qualification"
    / "RING3_QUALIFICATION_OCCUPATION_CLOSURE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "ring3_closure_receipt.schema.json"
)

RUNNER = (
    ROOT
    / "tools"
    / "validate_ring3.py"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

CORE = [
    (
        "R3-A",
        "tools/validate_qualification_request.py",
        "tests/test_qualification_request.py",
    ),
    (
        "R3-B",
        "tools/validate_qualification_record.py",
        "tests/test_qualification_record.py",
    ),
    (
        "R3-C",
        "tools/validate_room_lifecycle_readiness.py",
        "tests/test_room_lifecycle_readiness.py",
    ),
    (
        "R3-D",
        "tools/validate_occupancy_witness.py",
        "tests/test_occupancy_witness.py",
    ),
    (
        "R3-E",
        "tools/validate_capability_mission.py",
        "tests/test_capability_mission.py",
    ),
    (
        "R3-F",
        "tools/validate_proportional_force.py",
        "tests/test_proportional_force.py",
    ),
    (
        "R3-G",
        "tools/validate_formation_selection.py",
        "tests/test_formation_selection.py",
    ),
    (
        "R3-H",
        "tools/validate_goblin_signal.py",
        "tests/test_goblin_signal.py",
    ),
]

HANDOFF = [
    (
        "R3-I",
        "tools/validate_hydration.py",
        "tests/test_hydration.py",
    ),
]

ALL_COMPONENTS = CORE + HANDOFF


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
        if key != "ring3_closure_receipt_id"
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

    expected = compute_receipt_id(
        record
    )

    if (
        record.get(
            "ring3_closure_receipt_id"
        )
        != expected
    ):
        errors.append(
            "ring3_closure_receipt_id does not recompute from receipt"
        )

    exact = {
        "native_version":
            "vTemporal.41.0",
        "ring":
            "R3",
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
        "qualification_occupation_core_state":
            "PASS",
        "runtime_state_handoff_state":
            "BOUND",
        "source_tranche_boundary_state":
            "PRESERVED",
        "responsibility_integrity_state":
            "PRESERVED",
        "one_object_continuity_state":
            "PRESERVED",
        "state_separation_state":
            "PRESERVED",
        "failure_lock_state":
            "PRESERVED",
        "closure_state":
            "VALIDATED_CANDIDATE",
    }

    for field, expected_value in exact.items():
        if record.get(field) != expected_value:
            errors.append(
                f"{field} must be {expected_value}"
            )

    states = record.get(
        "component_states",
        {}
    )

    expected_components = {
        item[0]
        for item in ALL_COMPONENTS
    }

    if set(states) != expected_components:
        errors.append(
            "component_states must contain exactly R3-A through R3-I"
        )
    else:
        for name in sorted(
            expected_components
        ):
            if states.get(name) != "PASS":
                errors.append(
                    f"{name} closure state must be PASS"
                )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "Ring 3 Closure Receipt requires provenance_route"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R3-J closure contract"
        ),
        (
            SCHEMA,
            "R3-J closure schema"
        ),
        (
            RUNNER,
            "Ring 3 aggregate runner"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    for name, validator, tests in ALL_COMPONENTS:
        if not (
            ROOT / validator
        ).exists():
            errors.append(
                f"missing {name} validator"
            )

        if not (
            ROOT / tests
        ).exists():
            errors.append(
                f"missing {name} tests"
            )

    if errors:
        return errors

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid closure schema JSON: {exc}"
        ]

    # --------------------------------------------------------
    # Inner ring dependencies must actually pass.
    # --------------------------------------------------------

    for ring in (
        1,
        2,
    ):
        result = run_python(
            f"tools/validate_ring{ring}.py"
        )

        if result.returncode != 0:
            errors.append(
                f"Ring {ring} dependency validation failed"
            )

    # --------------------------------------------------------
    # Every R3-A through R3-I contract and test must pass
    # independently, not merely be listed in the aggregate.
    # --------------------------------------------------------

    for name, validator_path, tests_path in ALL_COMPONENTS:
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
    # Aggregate runner ordering/state through R3-I.
    # R3-J will be inserted by the patch after this validator
    # is written, so inspect for exact component ordering.
    # --------------------------------------------------------

    runner_text = RUNNER.read_text(
        encoding="utf-8"
    )

    positions = []

    for name, _, _ in ALL_COMPONENTS:
        token = f'"{name}"'

        pos = runner_text.find(
            token
        )

        if pos == -1:
            errors.append(
                f"Ring 3 runner does not contain {name}"
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
        == len(ALL_COMPONENTS)
    ):
        ordered = [
            name
            for name, _ in sorted(
                positions,
                key=lambda item: item[1]
            )
        ]

        expected = [
            item[0]
            for item in ALL_COMPONENTS
        ]

        if ordered != expected:
            errors.append(
                "Ring 3 component order is not R3-A through R3-I"
            )

    # --------------------------------------------------------
    # Source/tranche boundary must remain explicit.
    # --------------------------------------------------------

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    normalized = " ".join(
        contract_text.split()
    )

    locks = [
        "R3-J introduces no new analytical primitive.",
        "R3-A through R3-H form the Qualification / Occupation core.",
        "R3-I is the bounded Hydration Request / Release handoff into Runtime State Operations.",
        "Hydration MUST NOT be misrepresented as a source Tranche 5 primitive.",
        "Implementation ring placement != source tranche redefinition.",
        "Ring 3 depends on complete Rings 1 and 2.",
        "Outer closure != permission to mutate inner doctrine.",
        "Qualification precedes analysis.",
        "QUALIFIED != READY.",
        "READY != occupied.",
        "Occupied != mission-authorized.",
        "Mission-authorized != publication-authorized.",
        "THE ROOM IS ONE ANALYTICAL OBJECT.",
        "TURN THE OBJECT.",
        "DO NOT CLONE THE WORLD.",
        "Capabilities are occupants and observers.",
        "Capabilities are not owners of truth.",
        "Occupation establishes presence.",
        "Representation establishes position.",
        "Mission establishes movement.",
        "Evidence establishes escalation.",
        "Question determines mission.",
        "Need determines force.",
        "A capability request shall use the smallest justified force.",
        "More capability != more truth.",
        "Independent findings are preserved before correlation.",
        "Formation changes preserve the Stick.",
        "Goblin Signal communicates.",
        "Communication != ownership.",
        "Signal != truth.",
        "Source record first.",
        "Propagation second.",
        "Hydration restores only verified operational territory required by the active mission and representation.",
        "Payload remains at rest except where mission-scoped access is justified.",
        "Full payload hydration without question-driven necessity is prohibited.",
        "No component may silently absorb another component's responsibility.",
        "Qualification != evidence promotion.",
        "Occupation != evidence promotion.",
        "Formation != evidence promotion.",
        "Hydration != evidence promotion.",
        "State domains MUST NOT be silently conflated.",
        "VALIDATED_CANDIDATE != canonical promotion.",
        "Closed candidate != canonical promotion.",
        "Write capability != authority.",
        "Validation != authority.",
        "Closure != authority.",
        "Closure of Ring 3 does not claim Tranche 6 completion.",
        "No Restriction / Constriction transitions yet.",
        "No Collapse Boundary yet.",
        "No Landing Witness yet.",
        "No Reflight Trigger yet.",
        "No Closing Witness yet.",
        "No Replay Envelope yet.",
        "No Scar Replay yet.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in normalized
        ):
            errors.append(
                f"missing R3-J lock: {lock}"
            )

    # --------------------------------------------------------
    # Schema must fail closed to candidate closure only.
    # --------------------------------------------------------

    props = schema.get(
        "properties",
        {}
    )

    if (
        props
        .get("closure_state", {})
        .get("const")
        != "VALIDATED_CANDIDATE"
    ):
        errors.append(
            "R3-J closure schema does not fail closed to VALIDATED_CANDIDATE"
        )

    if (
        props
        .get("promotion_state", {})
        .get("const")
        != "CANDIDATE"
    ):
        errors.append(
            "R3-J closure schema improperly permits promotion state"
        )

    forbidden = {
        "restriction_transition_id",
        "constriction_transition_id",
        "collapse_boundary_id",
        "landing_witness_id",
        "reflight_trigger_id",
        "closing_witness_id",
        "replay_envelope_id",
        "scar_replay_id",
        "canonical_promotion",
        "execution_authorization",
    }

    leaked = (
        set(props)
        & forbidden
    )

    if leaked:
        errors.append(
            "R3-J improperly absorbs downstream Runtime State / "
            "promotion semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    # --------------------------------------------------------
    # Deterministic closure receipt probe.
    # --------------------------------------------------------

    receipt = {
        "schema_version":
            "1.0",
        "native_version":
            "vTemporal.41.0",
        "ring":
            "R3",
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
        "component_states": {
            name: "PASS"
            for name, _, _ in ALL_COMPONENTS
        },
        "qualification_occupation_core_state":
            "PASS",
        "runtime_state_handoff_state":
            "BOUND",
        "source_tranche_boundary_state":
            "PRESERVED",
        "responsibility_integrity_state":
            "PRESERVED",
        "one_object_continuity_state":
            "PRESERVED",
        "state_separation_state":
            "PRESERVED",
        "failure_lock_state":
            "PRESERVED",
        "closure_state":
            "VALIDATED_CANDIDATE",
        "provenance_route": [
            "ring1:validated",
            "ring2:validated",
            "r3-a",
            "r3-b",
            "r3-c",
            "r3-d",
            "r3-e",
            "r3-f",
            "r3-g",
            "r3-h",
            "r3-i",
        ],
        "closed_at":
            "2026-08-07T19:51:00-04:00",
    }

    receipt[
        "ring3_closure_receipt_id"
    ] = compute_receipt_id(
        receipt
    )

    if not SHA512_RE.fullmatch(
        receipt[
            "ring3_closure_receipt_id"
        ]
    ):
        errors.append(
            "Ring 3 Closure Receipt ID is not canonical SHA-512"
        )

    errors.extend(
        validate_receipt(
            receipt
        )
    )

    changed = dict(
        receipt
    )

    changed[
        "source_tranche_boundary_state"
    ] = "BROKEN"

    changed[
        "ring3_closure_receipt_id"
    ] = compute_receipt_id(
        changed
    )

    changed_errors = validate_receipt(
        changed
    )

    if not any(
        "source_tranche_boundary_state"
        in error
        for error in changed_errors
    ):
        errors.append(
            "R3-J incorrectly permitted broken source tranche boundary"
        )

    promoted = dict(
        receipt
    )

    promoted[
        "promotion_state"
    ] = "CANONICAL"

    promoted[
        "ring3_closure_receipt_id"
    ] = compute_receipt_id(
        promoted
    )

    promoted_errors = validate_receipt(
        promoted
    )

    if not any(
        "promotion_state"
        in error
        for error in promoted_errors
    ):
        errors.append(
            "R3-J incorrectly treated closure as canonical promotion"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-J RING 3 QUALIFICATION & OCCUPATION CLOSURE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-J RING 3 QUALIFICATION & OCCUPATION CLOSURE: PASS"
    )
    print(
        "R3-A through R3-H Qualification / Occupation core: CLOSED"
    )
    print(
        "R3-I Hydration Runtime-State handoff: BOUND"
    )
    print(
        "Source Tranche 5 / Tranche 6 boundary: PRESERVED"
    )
    print(
        "One Room / responsibility / state separation: PRESERVED"
    )
    print(
        "Failure locks / inner-ring dependencies: PRESERVED"
    )
    print(
        "Ring 3 closure state: VALIDATED_CANDIDATE"
    )
    print(
        "Canonical promotion / downstream Runtime State operations: NOT CLAIMED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
