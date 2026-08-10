#!/usr/bin/env python3

from pathlib import Path

import json

import subprocess

import sys

ROOT = Path(__file__).resolve().parents[3]

PRIMARY = {

    "eagle",

    "mole",

    "duck",

    "wildflower",

    "mockingbird",

    "platypus",

    "owl_hoot",

}

CONTROLLED = {

    "osprey",

    "animal_kingdom",

    "armadillo",

}

ALL = PRIMARY | CONTROLLED

CAP_ROOT = ROOT / "canonical/observers/capabilities"

INDEXES = [

    ROOT / "canonical/observers/capabilities/OBSERVER_CAPABILITY_INDEX.json",

    ROOT / "schemas/observers/observer_schema_index.json",

    ROOT / "tools/observers/OBSERVER_VALIDATOR_INDEX.json",

    ROOT / "routes/observers/OBSERVER_ROUTING_INDEX.json",

    ROOT / "observers/composition/OBSERVER_COMPOSITION_INDEX.json",

    ROOT / "observers/integration/OBSERVER_INTEGRATION_INDEX.json",

    ROOT / "observers/pressure/CONTROLLED_PRESSURE_INDEX.json",

    ROOT / "observers/failure/OBSERVER_FAILURE_SCAR_INDEX.json",

    ROOT / "tests/observers/functional/OBSERVER_FUNCTIONAL_TEST_INDEX.json",

]

EXECUTABLES = [

    [sys.executable, str(ROOT / "tools/observers/validate_observer_capabilities.py"), "--quiet"],

    [sys.executable, str(ROOT / "tools/observers/validate_observer_operation.py"), "--self-test"],

    [sys.executable, str(ROOT / "routes/observers/observer_router.py"), "--self-test"],

    [sys.executable, str(ROOT / "observers/composition/observer_composer.py"), "--self-test"],

    [sys.executable, str(ROOT / "observers/integration/observer_integration.py"), "--self-test"],

    [sys.executable, str(ROOT / "observers/pressure/controlled_pressure_isolator.py"), "--self-test"],

    [sys.executable, str(ROOT / "observers/failure/observer_failure_semantics.py"), "--self-test"],

    [sys.executable, str(ROOT / "tests/observers/functional/run_observer_functional_tests.py")],

]

def load(path):

    return json.loads(path.read_text(encoding="utf-8"))

def main():

    tests = []

    # 1. Nine restoration indexes exist.

    tests.append(

        len(INDEXES) == 9

        and all(path.exists() for path in INDEXES)

    )

    # 2. Nine restoration indexes parse.

    try:

        indexes = [load(path) for path in INDEXES]

        tests.append(True)

    except Exception:

        indexes = []

        tests.append(False)

    # 3. Authority NONE across indexes that declare authority.

    tests.append(

        bool(indexes)

        and all(

            obj.get("authority", "NONE") == "NONE"

            for obj in indexes

        )

    )

    # 4. Human Gate ACTIVE across indexes that declare gate state.

    tests.append(

        bool(indexes)

        and all(

            obj.get("human_gate", "ACTIVE") == "ACTIVE"

            for obj in indexes

        )

    )

    # Load ten capability contracts.

    try:

        caps = {}

        for path in CAP_ROOT.glob("*_CAPABILITY.json"):

            obj = load(path)

            caps[obj["observer_id"]] = obj

        cap_load = True

    except Exception:

        caps = {}

        cap_load = False

    # 5. Exact ten capability identities.

    tests.append(

        cap_load and set(caps) == ALL

    )

    # 6. Seven Primary classes.

    tests.append(

        cap_load

        and all(

            caps[oid].get("operating_class") == "PRIMARY"

            for oid in PRIMARY

        )

    )

    # 7. Seven Primary seats.

    tests.append(

        cap_load

        and all(

            caps[oid].get("canonical_seat") == "PRIMARY_OBSERVER"

            for oid in PRIMARY

        )

    )

    # 8. Three controlled classes.

    tests.append(

        cap_load

        and all(

            caps[oid].get("operating_class")

            == "CONTROLLED_SUB_OBSERVER"

            for oid in CONTROLLED

        )

    )

    # 9. Three controlled seats.

    tests.append(

        cap_load

        and all(

            caps[oid].get("canonical_seat")

            == "CONTROLLED_SUB_OBSERVER"

            for oid in CONTROLLED

        )

    )

    # 10. Owl_Hoot remains Primary.

    tests.append(

        cap_load

        and caps["owl_hoot"].get("operating_class") == "PRIMARY"

        and caps["owl_hoot"].get("canonical_seat") == "PRIMARY_OBSERVER"

    )

    # 11. Owl_Hoot bounded mode preserved.

    tests.append(

        cap_load

        and "BOUNDED_SUB_OBSERVER"

        in caps["owl_hoot"].get("supported_modes", [])

    )

    # 12. Ten distinctive invariants.

    tests.append(

        cap_load

        and all(

            bool(caps[oid].get("distinctive_invariant"))

            for oid in ALL

        )

    )

    # 13. Ten signal contracts.

    tests.append(

        cap_load

        and all(

            bool(caps[oid].get("signals"))

            for oid in ALL

        )

    )

    # 14. Ten output contracts.

    tests.append(

        cap_load

        and all(

            bool(caps[oid].get("outputs"))

            for oid in ALL

        )

    )

    # 15. OR-10 binds exactly ten suites.

    functional = load(

        ROOT

        / "tests/observers/functional/OBSERVER_FUNCTIONAL_TEST_INDEX.json"

    )

    suites = functional.get("suites", [])

    tests.append(

        len(suites) == 10

        and {

            item.get("observer_id")

            for item in suites

        } == ALL

    )

    # 16. OR-10 recorded 120/120.

    controls = functional.get("control_counts", {})

    tests.append(

        controls.get("aggregate") == 120

        and controls.get("passed") == 120

    )

    # 17-24. Full executable restoration chain.

    for command in EXECUTABLES:

        result = subprocess.run(

            command,

            cwd=ROOT,

            text=True,

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE

        )

        tests.append(result.returncode == 0)

    # 25. OR-5 routing remains available.

    tests.append(

        (

            ROOT

            / "routes/observers/observer_router.py"

        ).exists()

    )

    # 26. OR-6 composition remains available.

    tests.append(

        (

            ROOT

            / "observers/composition/observer_composer.py"

        ).exists()

    )

    # 27. OR-7 integration remains available.

    integration = load(

        ROOT

        / "observers/integration/OBSERVER_INTEGRATION_INDEX.json"

    )

    tests.append(

        set(

            integration.get("integration_surfaces", {})

        ) == {

            "PMC",

            "CCR",

            "MC",

            "RAVEN",

            "AUDIT",

        }

    )

    # 28. OR-8 preserves exactly three controlled identities.

    pressure = load(

        ROOT

        / "observers/pressure/CONTROLLED_PRESSURE_INDEX.json"

    )

    tests.append(

        set(

            pressure.get("controlled_sub_observers", {})

        ) == CONTROLLED

    )

    # 29. OR-9 preserves all thirteen failure semantics.

    failure = load(

        ROOT

        / "observers/failure/OBSERVER_FAILURE_SCAR_INDEX.json"

    )

    tests.append(

        len(set(failure.get("failure_semantics", []))) == 13

    )

    # 30. Candidate has not self-promoted.

    tests.append(

        all(

            obj.get(

                "canonical_status",

                "CANDIDATE_NOT_PROMOTED"

            ) != "CANONICAL"

            for obj in indexes

        )

    )

    if not all(tests):

        failed = [

            i + 1

            for i, ok in enumerate(tests)

            if not ok

        ]

        print(

            "OR-11 COMPLETENESS VALIDATOR: FAIL",

            failed

        )

        return 1

    print("OR-11 COMPLETENESS VALIDATOR: 30/30 PASS")

    print("PRIMARY OBSERVERS: 7/7 PASS")

    print("CONTROLLED SUB-OBSERVERS: 3/3 PASS")

    print("TOTAL OBSERVERS: 10/10 PASS")

    print("FUNCTIONAL CONTROLS: 120/120 PASS")

    print("AUTHORITY: NONE")

    print("HUMAN GATE: ACTIVE")

    print("CANONICAL PROMOTION: NOT PERFORMED")

    return 0

if __name__ == "__main__":

    sys.exit(main())
