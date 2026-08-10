#!/usr/bin/env python3

from pathlib import Path

import importlib.util

import json

import sys

HERE = Path(__file__).resolve().parent

ROOT = HERE.parents[2]

CAP_ROOT = ROOT / "canonical/observers/capabilities"

ROUTER_PATH = ROOT / "routes/observers/observer_router.py"

COMPOSER_PATH = ROOT / "observers/composition/observer_composer.py"

PRESSURE_PATH = ROOT / "observers/pressure/controlled_pressure_isolator.py"

FAILURE_PATH = ROOT / "observers/failure/observer_failure_semantics.py"

PRIMARY = {

    "eagle",

    "mole",

    "duck",

    "wildflower",

    "mockingbird",

    "platypus",

    "owl_hoot"

}

CONTROLLED = {

    "osprey",

    "animal_kingdom",

    "armadillo"

}

ALL = PRIMARY | CONTROLLED

def load_module(name, path):

    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None or spec.loader is None:

        raise RuntimeError("Unable to load module: " + str(path))

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module

router = load_module("or5_router", ROUTER_PATH)

composer = load_module("or6_composer", COMPOSER_PATH)

pressure = load_module("or8_pressure", PRESSURE_PATH)

failure = load_module("or9_failure", FAILURE_PATH)

def fail(name, control, detail):

    return {

        "observer_id": name,

        "control": control,

        "status": "FAIL",

        "detail": detail

    }

def passed(name, control):

    return {

        "observer_id": name,

        "control": control,

        "status": "PASS"

    }

def run_suite(path):

    suite = json.loads(path.read_text(encoding="utf-8"))

    oid = suite["observer_id"]

    results = []

    cap_path = ROOT / suite["capability_path"]

    if not cap_path.exists():

        return [fail(oid, "CAPABILITY_IDENTITY", "Capability missing")]

    cap = json.loads(cap_path.read_text(encoding="utf-8"))

    # 1. Capability identity.

    if cap.get("observer_id") == oid:

        results.append(passed(oid, "CAPABILITY_IDENTITY"))

    else:

        results.append(fail(oid, "CAPABILITY_IDENTITY", "Identity mismatch"))

    # 2. Operating class.

    if cap.get("operating_class") == suite["expected_operating_class"]:

        results.append(passed(oid, "OPERATING_CLASS"))

    else:

        results.append(fail(oid, "OPERATING_CLASS", "Class mismatch"))

    # 3. Canonical seat.

    if cap.get("canonical_seat") == suite["expected_canonical_seat"]:

        results.append(passed(oid, "CANONICAL_SEAT"))

    else:

        results.append(fail(oid, "CANONICAL_SEAT", "Seat mismatch"))

    # 4. Supported mode.

    if suite["route_mode"] in cap.get("supported_modes", []):

        results.append(passed(oid, "SUPPORTED_MODE"))

    else:

        results.append(fail(oid, "SUPPORTED_MODE", "Mode unsupported"))

    # 5. Distinctive invariant.

    if (

        cap.get("distinctive_invariant")

        == suite["distinctive_invariant"]

        and bool(cap.get("distinctive_invariant"))

    ):

        results.append(passed(oid, "DISTINCTIVE_INVARIANT"))

    else:

        results.append(fail(

            oid,

            "DISTINCTIVE_INVARIANT",

            "Invariant lost or substituted"

        ))

    # 6. Positive routing.

    request = {

        "needs": [suite["test_signal"]],

        "requested_observers": [oid],

        "requested_modes": {

            oid: suite["route_mode"]

        },

        "permitted_observers": [oid],

        "authority": "NONE",

        "human_gate": "ACTIVE",

        "external_runtime": "DISABLED",

        "external_action": "DISABLED"

    }

    routed = router.route(request)

    if routed.get("disposition") == "ROUTABLE":

        results.append(passed(oid, "ROUTING"))

    else:

        results.append(fail(

            oid,

            "ROUTING",

            repr(routed)

        ))

    # 7. Permission gate.

    denied = dict(request)

    denied["permitted_observers"] = []

    denied_result = router.route(denied)

    if denied_result.get("disposition") == "BLOCKED":

        results.append(passed(oid, "EXPLICIT_PERMISSION"))

    else:

        results.append(fail(

            oid,

            "EXPLICIT_PERMISSION",

            "Observer routed without permission"

        ))

    # 8. Authority NONE enforcement.

    promoted = dict(request)

    promoted["authority"] = "OBSERVER"

    promoted_result = router.route(promoted)

    if promoted_result.get("disposition") == "BLOCKED":

        results.append(passed(oid, "AUTHORITY_NONE"))

    else:

        results.append(fail(

            oid,

            "AUTHORITY_NONE",

            "Observer acquired authority"

        ))

    # 9. Human Gate preservation.

    gate = dict(request)

    gate["human_gate"] = "SATISFIED"

    gate_result = router.route(gate)

    if gate_result.get("disposition") == "BLOCKED":

        results.append(passed(oid, "HUMAN_GATE_ACTIVE"))

    else:

        results.append(fail(

            oid,

            "HUMAN_GATE_ACTIVE",

            "Observer substituted Human Gate"

        ))

    # 10. Failure semantic path.

    failure_event = {

        "failure": "NO_SIGNAL",

        "observer_id": oid,

        "operation_id": "operation:" + oid,

        "room_id": "room:test",

        "room_revision": "revision:test",

        "authorized_view": "view:test",

        "evidence_refs": [],

        "provenance_refs": [],

        "authority": "NONE",

        "human_gate": "ACTIVE",

        "finding_created": False,

        "fact_created": False,

        "claim_ceiling_increased": False,

        "canonical_state_mutated": False,

        "scar": None

    }

    failure_result = failure.classify(failure_event)

    if (

        failure_result.get("disposition") == "FAILURE_RECORDED"

        and failure_result.get("fact_created") is False

        and failure_result.get("finding_created") is False

    ):

        results.append(passed(oid, "FAILURE_SEMANTIC"))

    else:

        results.append(fail(

            oid,

            "FAILURE_SEMANTIC",

            repr(failure_result)

        ))

    # 11. Function-specific operational path.

    if oid in PRIMARY:

        partner = "eagle" if oid != "eagle" else "duck"

        one = composer.sample(

            oid,

            "PRIMARY",

            suite["route_mode"],

            "operation:" + oid

        )

        two = composer.sample(

            partner,

            "PRIMARY",

            "PRIMARY",

            "operation:" + partner

        )

        composed = composer.compose([one, two])

        if (

            composed.get("disposition") == "COMPOSED"

            and any(

                item.get("observer_id") == oid

                for item in composed.get("primary_results", [])

            )

        ):

            results.append(passed(oid, "FUNCTION_SPECIFIC_PATH"))

        else:

            results.append(fail(

                oid,

                "FUNCTION_SPECIFIC_PATH",

                repr(composed)

            ))

    else:

        sample = pressure.sample(oid)

        isolated = pressure.isolate(sample)

        if (

            isolated.get("disposition") == "PRESSURE_ISOLATED"

            and isolated.get(

                "controlled_pressure", {}

            ).get("observer_id") == oid

        ):

            results.append(passed(oid, "FUNCTION_SPECIFIC_PATH"))

        else:

            results.append(fail(

                oid,

                "FUNCTION_SPECIFIC_PATH",

                repr(isolated)

            ))

    # 12. Canonical mutation remains impossible.

    if oid in CONTROLLED:

        bad = pressure.sample(oid)

        bad["canonical_state_mutated"] = True

        blocked = pressure.isolate(bad)

        if blocked.get("disposition") == "BLOCKED":

            results.append(passed(oid, "NO_CANONICAL_MUTATION"))

        else:

            results.append(fail(

                oid,

                "NO_CANONICAL_MUTATION",

                "Controlled pressure mutated canonical state"

            ))

    else:

        scar_event = dict(failure_event)

        scar_event["failure"] = "STALE_BINDING"

        scar_event["canonical_state_mutated"] = True

        scar_event["scar"] = {

            "scar_id": "scar:" + oid,

            "reason": "STALE_BINDING",

            "resolved": False

        }

        blocked = failure.classify(scar_event)

        if blocked.get("disposition") == "BLOCKED":

            results.append(passed(oid, "NO_CANONICAL_MUTATION"))

        else:

            results.append(fail(

                oid,

                "NO_CANONICAL_MUTATION",

                "Observer failure mutated canonical state"

            ))

    return results

def main():

    suites = sorted(HERE.glob("*_FUNCTIONAL_TEST.json"))

    if len(suites) != 10:

        print(

            "OR-10 FUNCTIONAL TESTS: FAIL — expected 10 suites, found",

            len(suites)

        )

        return 1

    observer_ids = []

    for path in suites:

        suite = json.loads(path.read_text(encoding="utf-8"))

        observer_ids.append(suite["observer_id"])

    if set(observer_ids) != ALL:

        print("OR-10 FUNCTIONAL TESTS: FAIL — Observer set mismatch")

        return 1

    all_results = []

    for path in suites:

        all_results.extend(run_suite(path))

    failures = [

        result

        for result in all_results

        if result["status"] != "PASS"

    ]

    per_observer = {}

    for oid in sorted(ALL):

        own = [

            r

            for r in all_results

            if r["observer_id"] == oid

        ]

        passed_count = sum(

            r["status"] == "PASS"

            for r in own

        )

        per_observer[oid] = (

            passed_count,

            len(own)

        )

    for oid in sorted(per_observer):

        passed_count, total = per_observer[oid]

        print(

            f"{oid}: {passed_count}/{total} "

            + ("PASS" if passed_count == total else "FAIL")

        )

    if failures:

        print()

        print("OR-10 FUNCTIONAL TESTS: FAIL")

        for item in failures:

            print(

                item["observer_id"],

                item["control"],

                item.get("detail", "")

            )

        return 1

    if len(all_results) != 120:

        print(

            "OR-10 FUNCTIONAL TESTS: FAIL — expected 120 controls, found",

            len(all_results)

        )

        return 1

    print()

    print("OR-10 FUNCTIONAL TESTS: 120/120 PASS")

    print("OBSERVER SUITES: 10/10 PASS")

    return 0

if __name__ == "__main__":

    sys.exit(main())
