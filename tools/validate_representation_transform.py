#!/usr/bin/env python3

from pathlib import Path

import hashlib

import json

import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (

    ROOT

    / "contracts"

    / "geography"

    / "REPRESENTATION_TRANSFORM.md"

)

SCHEMA = (

    ROOT

    / "schemas"

    / "geography"

    / "representation_transform.schema.json"

)

SHA512_RE = re.compile(

    r"^sha512:[0-9a-f]{128}$"

)

REQUIRED_INVARIANTS = {

    "object_identity",

    "origin_route",

    "provenance",

    "preserved_evidence",

    "transformation_history",

}

def canonical_bytes(value):

    return json.dumps(

        value,

        sort_keys=True,

        separators=(",", ":"),

        ensure_ascii=False

    ).encode("utf-8")

def compute_transform_id(

    object_id,

    source_orientation,

    target_orientation,

    shifted_dimensions,

    preserved_invariants,

    included_evidence,

    excluded_evidence,

    assumptions,

    prohibited_assumptions,

    evidence_ceiling,

    return_coordinates

):

    preimage = {

        "object_id": object_id,

        "source_orientation": source_orientation,

        "target_orientation": target_orientation,

        "shifted_dimensions": shifted_dimensions,

        "preserved_invariants": preserved_invariants,

        "included_evidence": included_evidence,

        "excluded_evidence": excluded_evidence,

        "assumptions": assumptions,

        "prohibited_assumptions": prohibited_assumptions,

        "evidence_ceiling": evidence_ceiling,

        "return_coordinates": return_coordinates,

    }

    return (

        "sha512:"

        + hashlib.sha512(

            canonical_bytes(preimage)

        ).hexdigest()

    )

def load_schema():

    return json.loads(

        SCHEMA.read_text(

            encoding="utf-8"

        )

    )

def validate_transform(transform):

    errors = []

    expected = compute_transform_id(

        transform.get("object_id"),

        transform.get("source_orientation"),

        transform.get("target_orientation"),

        transform.get("shifted_dimensions"),

        transform.get("preserved_invariants"),

        transform.get("included_evidence"),

        transform.get("excluded_evidence"),

        transform.get("assumptions"),

        transform.get("prohibited_assumptions"),

        transform.get("evidence_ceiling"),

        transform.get("return_coordinates"),

    )

    if transform.get("transform_id") != expected:

        errors.append(

            "transform_id does not recompute from declared transform contract"

        )

    preserved = set(

        transform.get(

            "preserved_invariants",

            []

        )

    )

    missing = REQUIRED_INVARIANTS - preserved

    if missing:

        errors.append(

            "required transform invariants missing: "

            + ", ".join(sorted(missing))

        )

    included = set(

        transform.get(

            "included_evidence",

            []

        )

    )

    excluded = set(

        transform.get(

            "excluded_evidence",

            []

        )

    )

    overlap = included & excluded

    if overlap:

        errors.append(

            "evidence cannot be both included and excluded: "

            + ", ".join(sorted(overlap))

        )

    assumptions = set(

        transform.get(

            "assumptions",

            []

        )

    )

    prohibited = set(

        transform.get(

            "prohibited_assumptions",

            []

        )

    )

    conflict = assumptions & prohibited

    if conflict:

        errors.append(

            "assumption is simultaneously active and prohibited: "

            + ", ".join(sorted(conflict))

        )

    for field in (

        "source_orientation",

        "target_orientation",

        "evidence_ceiling",

        "return_coordinates",

    ):

        if transform.get(field) in (

            None,

            "",

            {},

        ):

            errors.append(

                f"{field} is undefined"

            )

    return errors

def validate():

    errors = []

    if not CONTRACT.exists():

        errors.append(

            "missing R2-F Representation Transform contract"

        )

    if not SCHEMA.exists():

        errors.append(

            "missing Representation Transform schema"

        )

    if errors:

        return errors

    try:

        schema = load_schema()

    except Exception as exc:

        return [

            f"invalid R2-F schema JSON: {exc}"

        ]

    required = set(

        schema.get("required", [])

    )

    expected = {

        "transform_id",

        "object_id",

        "source_orientation",

        "target_orientation",

        "shifted_dimensions",

        "preserved_invariants",

        "included_evidence",

        "excluded_evidence",

        "assumptions",

        "prohibited_assumptions",

        "evidence_ceiling",

        "return_coordinates",

    }

    missing = expected - required

    if missing:

        errors.append(

            "Transform Record missing required fields: "

            + ", ".join(sorted(missing))

        )

    properties = set(

        schema.get(

            "properties",

            {}

        )

    )

    forbidden = {

        "cartography_id",

        "stick_id",

        "occupation_id",

        "passageway_id",

        "capability_position",

    }

    leaked = properties & forbidden

    if leaked:

        errors.append(

            "R2-F improperly absorbs downstream fields: "

            + ", ".join(sorted(leaked))

        )

    contract_text = CONTRACT.read_text(

        encoding="utf-8"

    )

    locks = [

        "A perspective is not a truth claim.",

        "A perspective is not a separate Room.",

        "TURN THE OBJECT.",

        "DO NOT CLONE THE WORLD.",

        "Transform identity is not object identity.",

        "Transform != branch.",

        "Excluded != absent.",

        "Disagreement != duplicate reality.",

        "Disagreement is preserved.",

        "Transform != write authority.",

        "No full Orientation semantics yet.",

        "No Cartography yet.",

        "No Stick yet.",

        "No Occupation yet.",

    ]

    for lock in locks:

        if lock not in contract_text:

            errors.append(

                f"missing R2-F lock: {lock}"

            )

    object_id = (

        "sha512:"

        + "1" * 128

    )

    transform_id = compute_transform_id(

        object_id,

        {"reference": "orientation:a"},

        {"reference": "orientation:b"},

        ["observer", "discipline"],

        sorted(REQUIRED_INVARIANTS),

        ["evidence:a"],

        ["evidence:b"],

        ["assumption:a"],

        ["assumption:b"],

        "CEILING:A",

        {"reference": "return:a"},

    )

    if not SHA512_RE.fullmatch(

        transform_id

    ):

        errors.append(

            "transform_id is not canonical SHA-512"

        )

    changed = compute_transform_id(

        object_id,

        {"reference": "orientation:a"},

        {"reference": "orientation:c"},

        ["observer", "discipline"],

        sorted(REQUIRED_INVARIANTS),

        ["evidence:a"],

        ["evidence:b"],

        ["assumption:a"],

        ["assumption:b"],

        "CEILING:A",

        {"reference": "return:a"},

    )

    if transform_id == changed:

        errors.append(

            "material transform change did not change transform_id"

        )

    if transform_id == object_id:

        errors.append(

            "Transform identity collapsed into object identity"

        )

    return errors

def main():

    errors = validate()

    if errors:

        print(

            "R2-F PERSPECTIVE / REPRESENTATION TRANSFORM: FAIL"

        )

        for error in errors:

            print(f" - {error}")

        return 1

    print(

        "R2-F PERSPECTIVE / REPRESENTATION TRANSFORM: PASS"

    )

    print(

        "Perspective: BOUNDED REPRESENTATION, NOT SEPARATE REALITY"

    )

    print(

        "Shifted dimensions: EXPLICIT"

    )

    print(

        "Preserved invariants: LOCKED"

    )

    print(

        "Disagreement: PRESERVED, NOT AVERAGED OR CLONED"

    )

    print(

        "Orientation semantics / Cartography / Stick / Occupation: DEFERRED"

    )

    return 0

if __name__ == "__main__":

    raise SystemExit(main())

