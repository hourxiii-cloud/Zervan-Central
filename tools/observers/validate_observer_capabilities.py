#!/usr/bin/env python3

from pathlib import Path

import argparse

import hashlib

import json

import sys

ROOT = Path(__file__).resolve().parents[2]

CAP_ROOT = ROOT / "canonical/observers/capabilities"

CAP_INDEX = CAP_ROOT / "OBSERVER_CAPABILITY_INDEX.json"

SCHEMA_ROOT = ROOT / "schemas/observers"

SCHEMA_INDEX = SCHEMA_ROOT / "observer_schema_index.json"

CAP_SCHEMA = SCHEMA_ROOT / "observer_capability.schema.json"

EXPECTED_IDS = [

    "eagle",

    "mole",

    "duck",

    "wildflower",

    "mockingbird",

    "platypus",

    "owl_hoot",

    "osprey",

    "animal_kingdom",

    "armadillo",

]

PRIMARY_IDS = {

    "eagle",

    "mole",

    "duck",

    "wildflower",

    "mockingbird",

    "platypus",

    "owl_hoot",

}

CONTROLLED_IDS = {

    "osprey",

    "animal_kingdom",

    "armadillo",

}

REQUIRED_SHARED_PROHIBITIONS = {

    "MUST_NOT_MUTATE_PRIMARY_EVIDENCE",

    "MUST_NOT_CREATE_AUTHORITY",

    "MUST_NOT_PROMOTE_AUTHORITY",

    "MUST_NOT_SATISFY_HUMAN_GATE",

    "MUST_NOT_INCREASE_CLAIM_CEILING",

    "MUST_NOT_CREATE_CANONICAL_TRUTH",

    "MUST_NOT_AUTHORIZE_OWN_CONSUMPTION",

}

def sha512(path):

    return hashlib.sha512(path.read_bytes()).hexdigest()

def fail(errors):

    print("OBSERVER CAPABILITY VALIDATION: FAIL")

    for error in errors:

        print("FAIL:", error)

    return 1

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--quiet", action="store_true")

    args = parser.parse_args()

    errors = []

    try:

        from jsonschema import Draft202012Validator

    except Exception as exc:

        return fail(["jsonschema unavailable: " + str(exc)])

    if not CAP_INDEX.exists():

        return fail(["Capability index missing."])

    if not SCHEMA_INDEX.exists():

        return fail(["Schema index missing."])

    if not CAP_SCHEMA.exists():

        return fail(["Capability schema missing."])

    try:

        cap_index = json.loads(CAP_INDEX.read_text(encoding="utf-8"))

        schema_index = json.loads(SCHEMA_INDEX.read_text(encoding="utf-8"))

        cap_schema = json.loads(CAP_SCHEMA.read_text(encoding="utf-8"))

    except Exception as exc:

        return fail(["Unable to load prerequisite JSON: " + str(exc)])

    if cap_index.get("counts") != {

        "primary": 7,

        "controlled_sub_observer": 3,

        "total": 10,

    }:

        errors.append("Capability index cardinality mismatch.")

    if schema_index.get("observer_counts") != {

        "primary": 7,

        "controlled_sub_observer": 3,

        "total": 10,

    }:

        errors.append("Schema index cardinality mismatch.")

    capability_paths = sorted(CAP_ROOT.glob("*_CAPABILITY.json"))

    if len(capability_paths) != 10:

        errors.append(

            "Expected 10 capability contracts; found "

            + str(len(capability_paths))

        )

    validator = Draft202012Validator(cap_schema)

    loaded = {}

    for path in capability_paths:

        try:

            obj = json.loads(path.read_text(encoding="utf-8"))

        except Exception as exc:

            errors.append(str(path) + ": invalid JSON: " + str(exc))

            continue

        schema_errors = list(validator.iter_errors(obj))

        for error in schema_errors:

            errors.append(

                str(path)

                + ": schema "

                + str(list(error.path))

                + ": "

                + error.message

            )

        observer_id = obj.get("observer_id")

        if observer_id:

            if observer_id in loaded:

                errors.append("Duplicate Observer ID: " + observer_id)

            loaded[observer_id] = obj

    if set(loaded) != set(EXPECTED_IDS):

        errors.append(

            "Observer identity set mismatch: "

            + repr(sorted(loaded))

        )

    # Correct operating level.

    for observer_id in PRIMARY_IDS:

        obj = loaded.get(observer_id)

        if not obj:

            continue

        if obj.get("operating_class") != "PRIMARY":

            errors.append(observer_id + ": Primary class lost.")

        if obj.get("canonical_seat") != "PRIMARY_OBSERVER":

            errors.append(observer_id + ": Primary seat lost.")

    for observer_id in CONTROLLED_IDS:

        obj = loaded.get(observer_id)

        if not obj:

            continue

        if obj.get("operating_class") != "CONTROLLED_SUB_OBSERVER":

            errors.append(observer_id + ": Controlled class lost.")

        if obj.get("canonical_seat") != "CONTROLLED_SUB_OBSERVER":

            errors.append(observer_id + ": Controlled seat lost.")

    owl = loaded.get("owl_hoot")

    if owl:

        if owl.get("canonical_seat") != "PRIMARY_OBSERVER":

            errors.append("Owl_Hoot demoted.")

        modes = set(owl.get("supported_modes", []))

        if "PRIMARY" not in modes:

            errors.append("Owl_Hoot Primary mode missing.")

        if "BOUNDED_SUB_OBSERVER" not in modes:

            errors.append("Owl_Hoot bounded mode missing.")

    # Authority / Human Gate / mutation posture.

    for observer_id, obj in loaded.items():

        if obj.get("authority") != "NONE":

            errors.append(observer_id + ": authority != NONE")

        if obj.get("human_gate") != "ACTIVE":

            errors.append(observer_id + ": Human Gate != ACTIVE")

        if obj.get("mutation_posture") != "READ_ONLY_OBSERVATION_OR_PRESSURE":

            errors.append(observer_id + ": mutation posture invalid")

        if obj.get("canonical_status") != "CANDIDATE_NOT_PROMOTED":

            errors.append(observer_id + ": candidate status invalid")

        shared = set(obj.get("shared_prohibitions", []))

        missing_shared = REQUIRED_SHARED_PROHIBITIONS - shared

        if missing_shared:

            errors.append(

                observer_id

                + ": missing shared prohibitions "

                + repr(sorted(missing_shared))

            )

    # No-compression independence.

    purposes = [

        obj.get("purpose")

        for obj in loaded.values()

    ]

    invariants = [

        obj.get("distinctive_invariant")

        for obj in loaded.values()

    ]

    signal_sets = [

        tuple(sorted(obj.get("signals", [])))

        for obj in loaded.values()

    ]

    output_sets = [

        tuple(sorted(obj.get("outputs", [])))

        for obj in loaded.values()

    ]

    specific_prohibition_sets = [

        tuple(sorted(obj.get("observer_specific_prohibitions", [])))

        for obj in loaded.values()

    ]

    for label, values in [

        ("purpose", purposes),

        ("distinctive invariant", invariants),

        ("signal set", signal_sets),

        ("output set", output_sets),

        ("specific prohibition set", specific_prohibition_sets),

    ]:

        if len(values) != 10 or len(set(values)) != 10:

            errors.append(

                "No-compression failure: "

                + label

                + " is not independently represented 10/10."

            )

    # Each Observer must own at least one signal and output.

    signal_owners = {}

    output_owners = {}

    for observer_id, obj in loaded.items():

        for signal in obj.get("signals", []):

            signal_owners.setdefault(signal, set()).add(observer_id)

        for output in obj.get("outputs", []):

            output_owners.setdefault(output, set()).add(observer_id)

    for observer_id, obj in loaded.items():

        owned_signals = [

            x for x in obj.get("signals", [])

            if len(signal_owners.get(x, set())) == 1

        ]

        owned_outputs = [

            x for x in obj.get("outputs", [])

            if len(output_owners.get(x, set())) == 1

        ]

        if not owned_signals:

            errors.append(

                observer_id + ": no independently owned signal."

            )

        if not owned_outputs:

            errors.append(

                observer_id + ": no independently owned output."

            )

    # Capability index hash integrity.

    indexed = {

        entry.get("observer_id"): entry

        for entry in cap_index.get("capabilities", [])

    }

    if len(indexed) != 10:

        errors.append("Capability index does not contain 10 unique entries.")

    for observer_id in EXPECTED_IDS:

        entry = indexed.get(observer_id)

        if not entry:

            errors.append(

                "Capability index missing " + observer_id

            )

            continue

        path = ROOT / entry["path"]

        if not path.exists():

            errors.append(

                "Indexed capability path missing: " + str(path)

            )

            continue

        if sha512(path) != entry.get("sha512"):

            errors.append(

                "Capability SHA-512 mismatch: " + observer_id

            )

    # OR-3 schema index must bind same OR-2 files.

    schema_caps = {

        entry.get("observer_id"): entry

        for entry in schema_index.get(

            "validated_capability_contracts",

            []

        )

    }

    if set(schema_caps) != set(EXPECTED_IDS):

        errors.append(

            "OR-3 validated capability identity set mismatch."

        )

    for observer_id, entry in schema_caps.items():

        path = ROOT / entry["path"]

        if not path.exists():

            errors.append(

                "OR-3 indexed capability missing: "

                + observer_id

            )

            continue

        if sha512(path) != entry.get("sha512"):

            errors.append(

                "OR-3 capability SHA-512 mismatch: "

                + observer_id

            )

    if errors:

        return fail(errors)

    if not args.quiet:

        print("OBSERVER CAPABILITY VALIDATION: PASS")

        print("PRIMARY:                    7/7 PASS")

        print("CONTROLLED SUB:             3/3 PASS")

        print("TOTAL:                     10/10 PASS")

        print("OWL_HOOT PRIMARY:           PASS")

        print("OPERATING LEVELS:           PASS")

        print("AUTHORITY NONE:            10/10 PASS")

        print("HUMAN GATE ACTIVE:         10/10 PASS")

        print("READ-ONLY POSTURE:         10/10 PASS")

        print("INDEPENDENT PURPOSES:      10/10 PASS")

        print("INDEPENDENT INVARIANTS:    10/10 PASS")

        print("INDEPENDENT SIGNAL SETS:   10/10 PASS")

        print("INDEPENDENT OUTPUT SETS:   10/10 PASS")

        print("OWNED SIGNALS:             10/10 PASS")

        print("OWNED OUTPUTS:             10/10 PASS")

        print("CAPABILITY HASHES:         10/10 PASS")

        print("OR-3 HASH BINDING:         10/10 PASS")

        print("NO COMPRESSION:             PASS")

    return 0

if __name__ == "__main__":

    sys.exit(main())
