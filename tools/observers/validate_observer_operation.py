#!/usr/bin/env python3

from pathlib import Path

import argparse

import json

import sys

ROOT = Path(__file__).resolve().parents[2]

CAP_ROOT = ROOT / "canonical/observers/capabilities"

SCHEMA_ROOT = ROOT / "schemas/observers"

REQUEST_SCHEMA = SCHEMA_ROOT / "observer_request.schema.json"

BINDING_SCHEMA = SCHEMA_ROOT / "observer_binding.schema.json"

PROVENANCE_SCHEMA = SCHEMA_ROOT / "observer_provenance.schema.json"

RESULT_SCHEMA = SCHEMA_ROOT / "observer_result.schema.json"

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

ALL_IDS = PRIMARY_IDS | CONTROLLED_IDS

NON_MUTATING_TRUE_FIELDS = {

    "primary_evidence_mutated": False,

    "canonical_state_mutated": False,

    "claim_ceiling_increased": False,

}

def fail(errors):

    print("OBSERVER OPERATION VALIDATION: FAIL")

    for error in errors:

        print("FAIL:", error)

    return 1

def load_json(path):

    return json.loads(Path(path).read_text(encoding="utf-8"))

def load_capabilities():

    out = {}

    for path in sorted(CAP_ROOT.glob("*_CAPABILITY.json")):

        obj = load_json(path)

        out[obj["observer_id"]] = obj

    return out

def build_registry():

    try:

        from referencing import Registry, Resource

    except Exception as exc:

        raise RuntimeError("referencing unavailable: " + str(exc))

    registry = Registry()

    for path in [

        REQUEST_SCHEMA,

        BINDING_SCHEMA,

        PROVENANCE_SCHEMA,

        RESULT_SCHEMA,

    ]:

        schema = load_json(path)

        registry = registry.with_resource(

            schema["$id"],

            Resource.from_contents(schema)

        )

    return registry

def schema_validate(instance, schema_path, registry):

    from jsonschema import Draft202012Validator

    schema = load_json(schema_path)

    validator = Draft202012Validator(

        schema,

        registry=registry

    )

    return list(validator.iter_errors(instance))

def semantic_validate(request, result, capabilities):

    errors = []

    request_id = request.get("observer_id")

    result_id = result.get("observer_id")

    if request_id not in ALL_IDS:

        errors.append("Unknown request Observer identity.")

    if result_id not in ALL_IDS:

        errors.append("Unknown result Observer identity.")

    if request_id != result_id:

        errors.append("Observer identity changed request -> result.")

    binding = request.get("binding", {})

    provenance = result.get("provenance", {})

    # Identity continuity.

    if binding.get("observer_identity") != request_id:

        errors.append(

            "Binding Observer identity != request Observer identity."

        )

    if provenance.get("observer_id") != result_id:

        errors.append(

            "Provenance Observer identity != result Observer identity."

        )

    # Operation continuity.

    request_operation = binding.get("operation_id")

    result_operation = result.get("operation_id")

    provenance_operation = provenance.get("operation_id")

    if not (

        request_operation

        == result_operation

        == provenance_operation

    ):

        errors.append(

            "Operation identity changed across request/result/provenance."

        )

    # Room/revision/view continuity.

    continuity_fields = [

        ("room_id", "room_id"),

        ("room_revision", "room_revision"),

        ("authorized_view", "authorized_view"),

        ("claim_ceiling", "claim_ceiling"),

    ]

    for binding_field, provenance_field in continuity_fields:

        if binding.get(binding_field) != provenance.get(provenance_field):

            errors.append(

                binding_field

                + " changed binding -> provenance."

            )

    # Evidence reference continuity.

    binding_evidence = set(binding.get("evidence_refs", []))

    provenance_evidence = set(provenance.get("evidence_refs", []))

    if not provenance_evidence.issubset(binding_evidence):

        errors.append(

            "Result provenance introduced evidence outside bound evidence."

        )

    # Request class/mode consistency.

    if request_id in PRIMARY_IDS:

        expected_class = "PRIMARY"

    elif request_id in CONTROLLED_IDS:

        expected_class = "CONTROLLED_SUB_OBSERVER"

    else:

        expected_class = None

    if expected_class:

        if binding.get("observer_class") != expected_class:

            errors.append("Binding Observer class is wrong.")

        if result.get("observer_class") != expected_class:

            errors.append("Result Observer class is wrong.")

        if provenance.get("observer_class") != expected_class:

            errors.append("Provenance Observer class is wrong.")

    requested_mode = request.get("requested_mode")

    binding_mode = binding.get("observer_mode")

    result_mode = result.get("observer_mode")

    provenance_mode = provenance.get("observer_mode")

    if not (

        requested_mode

        == binding_mode

        == result_mode

        == provenance_mode

    ):

        errors.append(

            "Observer mode changed across request/binding/result/provenance."

        )

    if request_id in PRIMARY_IDS - {"owl_hoot"}:

        if requested_mode != "PRIMARY":

            errors.append(

                "Primary Observer requested non-Primary mode."

            )

    if request_id in CONTROLLED_IDS:

        if requested_mode != "CONTROLLED_SUB_OBSERVER":

            errors.append(

                "Controlled Sub-Observer requested invalid mode."

            )

    if request_id == "owl_hoot":

        if requested_mode not in {

            "PRIMARY",

            "BOUNDED_SUB_OBSERVER",

        }:

            errors.append("Owl_Hoot requested invalid mode.")

    # Capability contract mode eligibility.

    cap = capabilities.get(request_id)

    if cap:

        supported = set(cap.get("supported_modes", []))

        if requested_mode not in supported:

            errors.append(

                "Requested mode not supported by capability contract."

            )

        if cap.get("canonical_seat") == "PRIMARY_OBSERVER":

            if request_id != "owl_hoot" and requested_mode != "PRIMARY":

                errors.append(

                    "Primary seat illegally changed operating mode."

                )

        if (

            cap.get("canonical_seat")

            == "CONTROLLED_SUB_OBSERVER"

            and requested_mode != "CONTROLLED_SUB_OBSERVER"

        ):

            errors.append(

                "Controlled seat illegally changed operating mode."

            )

    # Authority continuity.

    if binding.get("authority") != "NONE":

        errors.append("Binding authority != NONE.")

    if result.get("authority") != "NONE":

        errors.append("Result authority != NONE.")

    if binding.get("human_gate") != "ACTIVE":

        errors.append("Binding Human Gate != ACTIVE.")

    if result.get("human_gate") != "ACTIVE":

        errors.append("Result Human Gate != ACTIVE.")

    # Mutation boundary.

    for field, required_value in NON_MUTATING_TRUE_FIELDS.items():

        if result.get(field) != required_value:

            errors.append(

                field + " violated non-mutating Observer boundary."

            )

    # Provenance disposition continuity.

    if result.get("disposition") != provenance.get("disposition"):

        errors.append(

            "Disposition changed result -> provenance."

        )

    # Observations cannot cite evidence outside bound evidence.

    for observation in result.get("observations", []):

        refs = set(observation.get("evidence_refs", []))

        if not refs.issubset(binding_evidence):

            errors.append(

                "Observation cites evidence outside bound evidence."

            )

    # Controlled pressure isolation.

    if request_id in CONTROLLED_IDS:

        if result.get("primary_evidence_mutated") is not False:

            errors.append(

                "Controlled pressure mutated primary evidence."

            )

    # Osprey cannot infer external authority.

    if request_id == "osprey":

        parameters = request.get("parameters", {})

        if parameters.get("authorize_external_collection") is True:

            errors.append(

                "Osprey attempted to authorize external collection."

            )

        if parameters.get("authorize_external_action") is True:

            errors.append(

                "Osprey attempted to authorize external action."

            )

    # AnimalKingdom synthetic/factual separation.

    if request_id == "animal_kingdom":

        parameters = request.get("parameters", {})

        if parameters.get("synthetic_as_fact") is True:

            errors.append(

                "AnimalKingdom attempted synthetic -> factual promotion."

            )

    # Armadillo attribution/authenticity boundary.

    if request_id == "armadillo":

        parameters = request.get("parameters", {})

        if parameters.get("challenge_establishes_attribution") is True:

            errors.append(

                "Armadillo challenge attempted to establish attribution."

            )

        if parameters.get("challenge_establishes_authenticity") is True:

            errors.append(

                "Armadillo challenge attempted to establish authenticity."

            )

    return errors

def validate_pair(request, result):

    errors = []

    try:

        registry = build_registry()

        capabilities = load_capabilities()

    except Exception as exc:

        return ["Validator initialization failed: " + str(exc)]

    request_schema_errors = schema_validate(

        request,

        REQUEST_SCHEMA,

        registry

    )

    result_schema_errors = schema_validate(

        result,

        RESULT_SCHEMA,

        registry

    )

    for error in request_schema_errors:

        errors.append(

            "Request schema "

            + str(list(error.path))

            + ": "

            + error.message

        )

    for error in result_schema_errors:

        errors.append(

            "Result schema "

            + str(list(error.path))

            + ": "

            + error.message

        )

    if errors:

        return errors

    errors.extend(

        semantic_validate(

            request,

            result,

            capabilities

        )

    )

    return errors

def self_test():

    binding = {

        "room_id": "room:test",

        "room_revision": "revision:test",

        "room_state": "READY",

        "authorized_view": "view:test",

        "evidence_refs": ["evidence:test"],

        "provenance_refs": ["provenance:test"],

        "evidence_status": "BOUNDED",

        "claim_ceiling": "OBSERVATIONAL",

        "permitted_operation": "OBSERVE",

        "observer_identity": "eagle",

        "observer_class": "PRIMARY",

        "observer_mode": "PRIMARY",

        "operation_id": "operation:test",

        "authority": "NONE",

        "human_gate": "ACTIVE",

    }

    request = {

        "request_type": "ZERVAN_V41_OBSERVER_REQUEST",

        "request_version": "1.0",

        "observer_id": "eagle",

        "requested_mode": "PRIMARY",

        "question": "Does the evidence support trajectory coherence?",

        "target_refs": ["evidence:test"],

        "parameters": {},

        "binding": binding,

    }

    provenance = {

        "observer_id": "eagle",

        "observer_class": "PRIMARY",

        "observer_mode": "PRIMARY",

        "operation_id": "operation:test",

        "room_id": "room:test",

        "room_revision": "revision:test",

        "authorized_view": "view:test",

        "evidence_refs": ["evidence:test"],

        "input_provenance_refs": ["provenance:test"],

        "claim_ceiling": "OBSERVATIONAL",

        "disposition": "OBSERVED",

        "sequence": 1,

        "timestamp": None,

        "downstream_refs": [],

    }

    result = {

        "result_type": "ZERVAN_V41_OBSERVER_RESULT",

        "result_version": "1.0",

        "observer_id": "eagle",

        "observer_class": "PRIMARY",

        "observer_mode": "PRIMARY",

        "operation_id": "operation:test",

        "disposition": "OBSERVED",

        "observations": [

            {

                "observation_type": "trajectory_observation",

                "statement": "Bounded trajectory observation.",

                "evidence_refs": ["evidence:test"],

                "confidence_status": "BOUNDED",

            }

        ],

        "unresolved_conditions": [],

        "scars": [],

        "provenance": provenance,

        "authority": "NONE",

        "human_gate": "ACTIVE",

        "primary_evidence_mutated": False,

        "canonical_state_mutated": False,

        "claim_ceiling_increased": False,

    }

    positive_errors = validate_pair(request, result)

    if positive_errors:

        return fail(

            ["Positive control rejected."]

            + positive_errors

        )

    negative_pass = 0

    # 1. Identity substitution.

    bad_result = json.loads(json.dumps(result))

    bad_result["observer_id"] = "mole"

    if validate_pair(request, bad_result):

        negative_pass += 1

    else:

        return fail(["Identity substitution not detected."])

    # 2. Operation substitution.

    bad_result = json.loads(json.dumps(result))

    bad_result["operation_id"] = "operation:other"

    if validate_pair(request, bad_result):

        negative_pass += 1

    else:

        return fail(["Operation substitution not detected."])

    # 3. Room revision substitution.

    bad_result = json.loads(json.dumps(result))

    bad_result["provenance"]["room_revision"] = "revision:other"

    if validate_pair(request, bad_result):

        negative_pass += 1

    else:

        return fail(["Room revision substitution not detected."])

    # 4. Evidence expansion.

    bad_result = json.loads(json.dumps(result))

    bad_result["observations"][0]["evidence_refs"].append(

        "evidence:unauthorized"

    )

    if validate_pair(request, bad_result):

        negative_pass += 1

    else:

        return fail(["Evidence expansion not detected."])

    # 5. Authority promotion.

    bad_result = json.loads(json.dumps(result))

    bad_result["authority"] = "OBSERVER"

    if validate_pair(request, bad_result):

        negative_pass += 1

    else:

        return fail(["Authority promotion not detected."])

    # 6. Mutation.

    bad_result = json.loads(json.dumps(result))

    bad_result["canonical_state_mutated"] = True

    if validate_pair(request, bad_result):

        negative_pass += 1

    else:

        return fail(["Canonical mutation not detected."])

    # 7. Claim-ceiling escalation.

    bad_result = json.loads(json.dumps(result))

    bad_result["claim_ceiling_increased"] = True

    if validate_pair(request, bad_result):

        negative_pass += 1

    else:

        return fail(["Claim-ceiling escalation not detected."])

    # 8. Primary -> controlled mode.

    bad_request = json.loads(json.dumps(request))

    bad_request["requested_mode"] = "CONTROLLED_SUB_OBSERVER"

    if validate_pair(bad_request, result):

        negative_pass += 1

    else:

        return fail(["Operating-level escalation not detected."])

    print("OBSERVER OPERATION VALIDATION: PASS")

    print("POSITIVE CONTROL:             1/1 PASS")

    print("NEGATIVE CONTROLS:            8/8 PASS")

    print("IDENTITY CONTINUITY:          PASS")

    print("OPERATION CONTINUITY:         PASS")

    print("ROOM/REVISION CONTINUITY:     PASS")

    print("VIEW CONTINUITY:              PASS")

    print("EVIDENCE BOUNDARY:            PASS")

    print("OPERATING LEVEL:              PASS")

    print("AUTHORITY NONE:               PASS")

    print("HUMAN GATE ACTIVE:            PASS")

    print("MUTATION BLOCK:               PASS")

    print("CLAIM CEILING BLOCK:          PASS")

    print("PROVENANCE CONTINUITY:        PASS")

    return 0

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--request")

    parser.add_argument("--result")

    parser.add_argument("--self-test", action="store_true")

    args = parser.parse_args()

    if args.self_test:

        return self_test()

    if not args.request or not args.result:

        parser.error(

            "use --self-test or provide --request and --result"

        )

    try:

        request = load_json(args.request)

        result = load_json(args.result)

    except Exception as exc:

        return fail(["Input load failure: " + str(exc)])

    errors = validate_pair(request, result)

    if errors:

        return fail(errors)

    print("OBSERVER OPERATION VALIDATION: PASS")

    return 0

if __name__ == "__main__":

    sys.exit(main())
