#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "REPRESENTATION_INDEPENDENCE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "representation_independence.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

R2F = (
    ROOT
    / "contracts"
    / "geography"
    / "REPRESENTATION_TRANSFORM.md"
)

R2D = (
    ROOT
    / "contracts"
    / "geography"
    / "BOUNDED_ZONE.md"
)

R2I = (
    ROOT
    / "contracts"
    / "geography"
    / "STICK_CONTACT_CONTINUITY.md"
)

REQUIRED_ROLES = {
    "OBJECT",
    "REPRESENTATION_FRAME",
    "ACTIVE_SURFACE",
    "TRANSFORM",
    "BOUNDARY",
    "OWNER",
    "AUTHORITY",
    "LINEAGE",
    "PROVENANCE",
    "RETURN_ROUTE",
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


def role_set(rep):
    return set(
        rep.get(
            "canonical_role_map",
            {}
        ).values()
    )


def evaluate_record(record):
    reasons = []

    representations = record.get(
        "representations",
        []
    )

    domains = {
        rep.get(
            "domain"
        )
        for rep in representations
        if rep.get(
            "domain"
        )
    }

    if len(domains) < 3:
        reasons.append(
            "INSUFFICIENT_DOMAIN_DIVERSITY"
        )

    canonical_object = record.get(
        "canonical_object_id"
    )

    canonical_boundary = record.get(
        "canonical_boundary_reference"
    )

    canonical_owners = record.get(
        "canonical_owner_map",
        {}
    )

    canonical_authority = record.get(
        "canonical_authority_state"
    )

    canonical_gate = record.get(
        "canonical_human_gate_state"
    )

    canonical_lineage = record.get(
        "canonical_lineage_reference"
    )

    canonical_provenance = record.get(
        "canonical_provenance_route",
        []
    )

    canonical_return = record.get(
        "canonical_return_route"
    )

    for rep in representations:
        roles = role_set(
            rep
        )

        if not REQUIRED_ROLES.issubset(
            roles
        ):
            reasons.append(
                "CANONICAL_ROLE_MAPPING_MISSING"
            )

        mapping_values = list(
            rep.get(
                "canonical_role_map",
                {}
            ).values()
        )

        if len(mapping_values) != len(
            set(
                mapping_values
            )
        ):
            reasons.append(
                "SEMANTIC_ROLE_COLLISION"
            )

        if (
            rep.get(
                "object_id"
            )
            != canonical_object
        ):
            reasons.append(
                "OBJECT_IDENTITY_CHANGED"
            )

        if (
            rep.get(
                "boundary_reference"
            )
            != canonical_boundary
        ):
            reasons.append(
                "BOUNDARY_CHANGED"
            )

        if (
            rep.get(
                "owner_map"
            )
            != canonical_owners
        ):
            reasons.append(
                "OWNERSHIP_CHANGED"
            )

        if (
            rep.get(
                "authority_state"
            )
            != canonical_authority
        ):
            reasons.append(
                "AUTHORITY_CHANGED"
            )

        if (
            rep.get(
                "human_gate_state"
            )
            != canonical_gate
        ):
            reasons.append(
                "HUMAN_GATE_CHANGED"
            )

        if (
            rep.get(
                "lineage_reference"
            )
            != canonical_lineage
        ):
            reasons.append(
                "LINEAGE_CHANGED"
            )

        if (
            rep.get(
                "provenance_route"
            )
            != canonical_provenance
        ):
            reasons.append(
                "PROVENANCE_CHANGED"
            )

        if (
            rep.get(
                "return_route"
            )
            != canonical_return
        ):
            reasons.append(
                "RETURN_ROUTE_CHANGED"
            )

    if record.get(
        "object_identity_changed"
    ):
        reasons.append(
            "OBJECT_IDENTITY_CHANGED"
        )

    if record.get(
        "boundary_changed"
    ):
        reasons.append(
            "BOUNDARY_CHANGED"
        )

    if record.get(
        "ownership_changed"
    ):
        reasons.append(
            "OWNERSHIP_CHANGED"
        )

    if record.get(
        "authority_changed"
    ):
        reasons.append(
            "AUTHORITY_CHANGED"
        )

    if record.get(
        "lineage_changed"
    ):
        reasons.append(
            "LINEAGE_CHANGED"
        )

    if record.get(
        "provenance_changed"
    ):
        reasons.append(
            "PROVENANCE_CHANGED"
        )

    if record.get(
        "return_route_changed"
    ):
        reasons.append(
            "RETURN_ROUTE_CHANGED"
        )

    if record.get(
        "metaphor_required"
    ):
        reasons.append(
            "METAPHOR_DEPENDENCY_DETECTED"
        )

    if (
        record.get(
            "canonical_authority_state"
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
            "validation_family"
        )
        != "REPRESENTATION_INDEPENDENCE"
    ):
        errors.append(
            "wrong validation family"
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
            "representation-independence disposition contradicts invariant state"
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
            "representation-independence failure reasons are incomplete or incorrect"
        )

    return errors


def canonical_owner_map():
    return {
        "OBJECT_IDENTITY":
            "REGISTRY",

        "BOUNDARY_AND_CLAIM_CEILING":
            "GOVERNANCE",

        "INTEGRITY_VERIFICATION":
            "AUDIT",

        "ANALYTICAL_EVALUATION":
            "PMC",

        "CANDIDATE_COMMITMENT":
            "CCR",

        "OUTPUT_ADMISSIBILITY":
            "MC",

        "REPORTING":
            "RAVEN",

        "AUTHORITY_BEARING_DECISION":
            "HUMAN_GATE",
    }


def representation(
    domain,
    vocabulary,
    *,
    object_id,
    boundary_reference,
    owner_map,
    authority_state,
    human_gate_state,
    lineage_reference,
    provenance_route,
    return_route,
    canonical_role_map=None,
):
    if canonical_role_map is None:
        canonical_role_map = {
            vocabulary[
                "object"
            ]:
                "OBJECT",

            vocabulary[
                "frame"
            ]:
                "REPRESENTATION_FRAME",

            vocabulary[
                "surface"
            ]:
                "ACTIVE_SURFACE",

            vocabulary[
                "transform"
            ]:
                "TRANSFORM",

            vocabulary[
                "boundary"
            ]:
                "BOUNDARY",

            vocabulary[
                "owner"
            ]:
                "OWNER",

            vocabulary[
                "authority"
            ]:
                "AUTHORITY",

            vocabulary[
                "lineage"
            ]:
                "LINEAGE",

            vocabulary[
                "provenance"
            ]:
                "PROVENANCE",

            vocabulary[
                "return"
            ]:
                "RETURN_ROUTE",
        }

    return {
        "domain":
            domain,

        "local_vocabulary":
            dict(
                vocabulary
            ),

        "canonical_role_map":
            dict(
                canonical_role_map
            ),

        "object_id":
            object_id,

        "boundary_reference":
            boundary_reference,

        "owner_map":
            dict(
                owner_map
            ),

        "authority_state":
            authority_state,

        "human_gate_state":
            human_gate_state,

        "lineage_reference":
            lineage_reference,

        "provenance_route":
            list(
                provenance_route
            ),

        "return_route":
            return_route,
    }


def make_record(
    *,
    representations=None,
    object_identity_changed=False,
    boundary_changed=False,
    ownership_changed=False,
    authority_changed=False,
    lineage_changed=False,
    provenance_changed=False,
    return_route_changed=False,
    metaphor_required=False,
    canonical_authority_state="NONE",
):
    object_id = (
        "sha512:"
        + "1" * 128
    )

    boundary = (
        "boundary:representation-independent:a"
    )

    owners = canonical_owner_map()

    lineage = (
        "lineage:representation-independent:a"
    )

    provenance = [
        "origin:representation-independent:a",
        "genesis:representation-independent:a",
        "representation-test:r6-n",
    ]

    return_route = (
        "return:representation-independent:a"
    )

    if representations is None:
        representations = [
            representation(
                "GEOGRAPHIC",
                {
                    "object":
                        "Room",
                    "frame":
                        "Zone",
                    "surface":
                        "Space",
                    "transform":
                        "Representation Transform",
                    "boundary":
                        "evidence boundary",
                    "owner":
                        "Registry / Governance",
                    "authority":
                        "Authority",
                    "lineage":
                        "Room lineage",
                    "provenance":
                        "provenance route",
                    "return":
                        "return coordinate",
                },
                object_id=object_id,
                boundary_reference=boundary,
                owner_map=owners,
                authority_state="NONE",
                human_gate_state="ACTIVE",
                lineage_reference=lineage,
                provenance_route=provenance,
                return_route=return_route,
            ),

            representation(
                "CYBER_SECURITY",
                {
                    "object":
                        "investigation object",
                    "frame":
                        "scoped security view",
                    "surface":
                        "active investigation surface",
                    "transform":
                        "analytical view shift",
                    "boundary":
                        "evidence-access boundary",
                    "owner":
                        "responsibility map",
                    "authority":
                        "decision authority",
                    "lineage":
                        "case lineage",
                    "provenance":
                        "source chain",
                    "return":
                        "prior investigation position",
                },
                object_id=object_id,
                boundary_reference=boundary,
                owner_map=owners,
                authority_state="NONE",
                human_gate_state="ACTIVE",
                lineage_reference=lineage,
                provenance_route=provenance,
                return_route=return_route,
            ),

            representation(
                "DATA_ANALYTICS",
                {
                    "object":
                        "analytical object",
                    "frame":
                        "feature view",
                    "surface":
                        "filtered working set",
                    "transform":
                        "feature-space transform",
                    "boundary":
                        "admissible data boundary",
                    "owner":
                        "responsibility map",
                    "authority":
                        "decision authority",
                    "lineage":
                        "analysis lineage",
                    "provenance":
                        "data provenance chain",
                    "return":
                        "prior analytical coordinate",
                },
                object_id=object_id,
                boundary_reference=boundary,
                owner_map=owners,
                authority_state="NONE",
                human_gate_state="ACTIVE",
                lineage_reference=lineage,
                provenance_route=provenance,
                return_route=return_route,
            ),
        ]

    record = {
        "schema_version":
            "1.0",

        "validation_family":
            "REPRESENTATION_INDEPENDENCE",

        "canonical_primitive":
            "CANONICAL_ROOM_OBJECT",

        "canonical_object_id":
            object_id,

        "canonical_boundary_reference":
            boundary,

        "canonical_owner_map":
            owners,

        "canonical_authority_state":
            canonical_authority_state,

        "canonical_human_gate_state":
            "ACTIVE",

        "canonical_lineage_reference":
            lineage,

        "canonical_provenance_route":
            provenance,

        "canonical_return_route":
            return_route,

        "representations":
            list(
                representations
            ),

        "object_identity_changed":
            object_identity_changed,

        "boundary_changed":
            boundary_changed,

        "ownership_changed":
            ownership_changed,

        "authority_changed":
            authority_changed,

        "lineage_changed":
            lineage_changed,

        "provenance_changed":
            provenance_changed,

        "return_route_changed":
            return_route_changed,

        "metaphor_required":
            metaphor_required,

        "validation_disposition":
            "",

        "failure_reasons":
            [],
    }

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
            "R6-N contract"
        ),
        (
            SCHEMA,
            "R6-N schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            R2F,
            "R2-F Representation Transform"
        ),
        (
            R2D,
            "R2-D Bounded Zone"
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
        "R6-N = Representation Independence.",
        "A canonical primitive remains valid across substantially different representational domains.",
        "Vocabulary change MUST NOT break one-object semantics.",
        "Vocabulary change MUST NOT break identity.",
        "Vocabulary change MUST NOT break boundaries.",
        "Vocabulary change MUST NOT break ownership.",
        "Vocabulary change MUST NOT break authority.",
        "Vocabulary change MUST NOT break lineage.",
        "Vocabulary change MUST NOT break provenance.",
        "Representation independence != semantic looseness.",
        "Personality is allowed.",
        "Hidden dependency on one metaphor is not.",
        "Representation style != canonical meaning.",
        "Vocabulary != ontology.",
        "Metaphor != primitive.",
        "Representation change != object change.",
        "Different words do not create different system semantics.",
        "Security vocabulary != new ownership model.",
        "Data vocabulary != new object identity.",
        "Feature view != private analytical reality.",
        "Equivalent role != identical local vocabulary.",
        "Boundary vocabulary change != boundary change.",
        "Label != evidence authority.",
        "Vocabulary != ownership transfer.",
        "Representation change != authority promotion.",
        "Renaming != removal.",
        "Provenance survives translation.",
        "Disagreement != duplicate reality.",
        "Style freedom != semantic freedom.",
        "Structural equivalence != textual equality.",
        "Representation change != Genesis.",
        "Representation change != Branch by default.",
        "Narrative wrapper != provenance.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-O owns Lossless Collapse validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-N lock: {lock}"
            )

    r6a = normalized(
        R6A
    )

    for lock in (
        "Representation Independence",
        "Vocabulary change MUST NOT break:",
        "one-object semantics;",
        "identity;",
        "boundaries;",
        "ownership;",
        "authority;",
        "lineage;",
        "provenance.",
        "Representation independence != semantic looseness.",
        "Personality is allowed.",
        "Hidden dependency on one metaphor is not.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-N binding: {lock}"
            )

    r2f = normalized(
        R2F
    )

    for lock in (
        "The transform contract MUST survive vocabulary change.",
        "A valid transform is defined by structural relationships and preserved invariants, not by a specific narrative wrapper.",
        "Representation style != canonical meaning.",
        "Object identity is preserved.",
        "Origin route is preserved.",
        "Provenance is preserved.",
        "Transformation history is preserved.",
        "Transform != write authority.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r2f
        ):
            errors.append(
                f"R2-F source missing representation-independence semantic: {lock}"
            )

    r2d = normalized(
        R2D
    )

    for lock in (
        "Reality is established once.",
        "Representation may turn many times.",
        "Every Zone remains attached to one canonical object_id.",
        "Zone identity is not object identity.",
        "Perspective != Room.",
        "Discipline != Room.",
        "Representation cannot manufacture reachability.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r2d
        ):
            errors.append(
                f"R2-D source missing representation semantic: {lock}"
            )

    try:
        load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-N schema JSON: {exc}"
        ]

    # Positive three-domain representation.
    valid = make_record()

    errors.extend(
        validate_record(
            valid
        )
    )

    # Domain-specific identity fracture.
    fractured = make_record()

    fractured[
        "representations"
    ][1][
        "object_id"
    ] = (
        "sha512:"
        + "2" * 128
    )

    fractured[
        "failure_reasons"
    ] = evaluate_record(
        fractured
    )

    fractured[
        "validation_disposition"
    ] = (
        "VALID"
        if not fractured[
            "failure_reasons"
        ]
        else "BLOCKED"
    )

    if (
        "OBJECT_IDENTITY_CHANGED"
        not in fractured[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-N failed to reject representation-specific object identity"
        )

    # Ownership drift.
    ownership = make_record()

    ownership[
        "representations"
    ][2][
        "owner_map"
    ][
        "OBJECT_IDENTITY"
    ] = "ANALYTICAL_ENGINE"

    ownership[
        "failure_reasons"
    ] = evaluate_record(
        ownership
    )

    if (
        "OWNERSHIP_CHANGED"
        not in ownership[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-N failed to reject vocabulary-driven ownership migration"
        )

    # Metaphor dependency.
    metaphor = make_record(
        metaphor_required=True
    )

    if (
        "METAPHOR_DEPENDENCY_DETECTED"
        not in metaphor[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-N failed to reject hidden Room-metaphor dependency"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-N REPRESENTATION INDEPENDENCE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-N REPRESENTATION INDEPENDENCE: PASS"
    )
    print(
        "Geographic representation: VALIDATED"
    )
    print(
        "Cyber-Security representation: VALIDATED"
    )
    print(
        "Data-Analytics representation: VALIDATED"
    )
    print(
        "One canonical object across domain vocabularies: PRESERVED"
    )
    print(
        "Boundary semantics across vocabulary change: PRESERVED"
    )
    print(
        "Ownership across vocabulary change: PRESERVED"
    )
    print(
        "Authority NONE / Human Gate ACTIVE across representations: PRESERVED"
    )
    print(
        "Lineage / provenance / return route: PRESERVED"
    )
    print(
        "Representation-specific object fracture: REJECTED"
    )
    print(
        "Vocabulary-driven ownership migration: REJECTED"
    )
    print(
        "Hidden dependency on Room metaphor: REJECTED"
    )
    print(
        "Representation independence != semantic looseness: PRESERVED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-O Lossless Collapse: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
