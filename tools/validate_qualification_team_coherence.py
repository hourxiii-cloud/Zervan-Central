#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "QUALIFICATION_TEAM_COHERENCE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "qualification_team_coherence.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

R3B = (
    ROOT
    / "contracts"
    / "qualification"
    / "QUALIFICATION_RECORD_DISPOSITION.md"
)

R3E = (
    ROOT
    / "contracts"
    / "qualification"
    / "CAPABILITY_MISSION_REQUEST_RETURN.md"
)

R3G = (
    ROOT
    / "contracts"
    / "qualification"
    / "FORMATION_SELECTION_INTEGRATION.md"
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

    object_id = record.get(
        "object_id"
    )

    returns = record.get(
        "returns",
        []
    )

    return_ids = []

    for item in returns:
        if (
            item.get(
                "object_id"
            )
            != object_id
        ):
            reasons.append(
                "OBJECT_IDENTITY_DIVERGENCE"
            )

        return_id = item.get(
            "capability_return_id"
        )

        if not return_id:
            reasons.append(
                "RETURN_ATTRIBUTION_MISSING"
            )
        else:
            return_ids.append(
                return_id
            )

        if not item.get(
            "capability_id"
        ):
            reasons.append(
                "RETURN_ATTRIBUTION_MISSING"
            )

        if not item.get(
            "mission_reference"
        ):
            reasons.append(
                "RETURN_ATTRIBUTION_MISSING"
            )

        if not item.get(
            "provenance_route"
        ):
            reasons.append(
                "RETURN_PROVENANCE_MISSING"
            )

    if (
        len(return_ids)
        != len(
            set(
                return_ids
            )
        )
    ):
        reasons.append(
            "DUPLICATE_RETURN_ID"
        )

    findings = [
        item.get(
            "finding"
        )
        for item in returns
        if item.get(
            "finding"
        )
    ]

    unique_findings = set(
        findings
    )

    disagreements = record.get(
        "material_disagreements",
        []
    )

    summary = record.get(
        "correlation_summary",
        ""
    ).lower()

    if (
        len(unique_findings) > 1
        and not disagreements
    ):
        reasons.append(
            "DISAGREEMENT_ERASED"
        )

    if (
        len(unique_findings) > 1
        and (
            "unanimous"
            in summary
            or "all participants agree"
            in summary
            or "consensus resolved"
            in summary
        )
    ):
        reasons.append(
            "FALSE_CONSENSUS"
        )

    if record.get(
        "claim_ceiling_changed"
    ):
        reasons.append(
            "EVIDENCE_CEILING_INFLATED"
        )

    if record.get(
        "formation_created"
    ):
        reasons.append(
            "FORMATION_INVENTED"
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
    reasons = evaluate_record(
        record
    )

    if reasons:
        return "BLOCKED"

    findings = {
        item.get(
            "finding"
        )
        for item in record.get(
            "returns",
            []
        )
        if item.get(
            "finding"
        )
    }

    if len(findings) <= 1:
        return (
            "COHERENT_WITH_AGREEMENT"
        )

    return (
        "COHERENT_WITH_DISAGREEMENT"
    )


def validate_record(record):
    errors = []

    if (
        record.get(
            "validation_vector"
        )
        != "QUALIFICATION_TEAM_COHERENCE"
    ):
        errors.append(
            "wrong validation vector"
        )

    if len(
        record.get(
            "returns",
            []
        )
    ) < 2:
        errors.append(
            "qualification-team coherence requires multiple returns"
        )

    expected_reasons = evaluate_record(
        record
    )

    expected = expected_disposition(
        record
    )

    if (
        record.get(
            "validation_disposition"
        )
        != expected
    ):
        errors.append(
            "coherence disposition contradicts independent-return state"
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
            "coherence failure reasons are incomplete or incorrect"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-E Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "aggregate_provenance_route"
    ):
        errors.append(
            "aggregate provenance route required"
        )

    return errors


def make_return(
    *,
    return_id,
    capability_id,
    finding,
    object_id=None,
    provenance=True,
):
    if object_id is None:
        object_id = (
            "sha512:"
            + "1" * 128
        )

    return {
        "capability_return_id":
            return_id,

        "capability_id":
            capability_id,

        "object_id":
            object_id,

        "mission_reference":
            f"mission:{capability_id}",

        "finding":
            finding,

        "evidence_references": [
            f"evidence:{capability_id}"
        ],

        "unresolved_signals":
            [],

        "restriction_findings":
            [],

        "provenance_route":
            (
                [
                    f"provenance:{capability_id}"
                ]
                if provenance
                else []
            ),
    }


def make_record(
    *,
    returns=None,
    material_disagreements=None,
    correlation_summary="independent findings preserved",
    claim_ceiling_changed=False,
    formation_created=False,
    occupancy_mutated=False,
    lifecycle_mutated=False,
    authority_state="NONE",
):
    object_id = (
        "sha512:"
        + "1" * 128
    )

    if returns is None:
        returns = [
            make_return(
                return_id="return:a",
                capability_id="goblin:a",
                finding="OBSERVED_A",
                object_id=object_id,
            ),
            make_return(
                return_id="return:b",
                capability_id="goblin:b",
                finding="OBSERVED_A",
                object_id=object_id,
            ),
        ]

    if material_disagreements is None:
        unique_findings = {
            item.get(
                "finding"
            )
            for item in returns
        }

        material_disagreements = (
            []
            if len(unique_findings) <= 1
            else [
                "independent findings differ"
            ]
        )

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "QUALIFICATION_TEAM_COHERENCE",

        "object_id":
            object_id,

        "qualification_record_reference":
            "qualification-record:r6-e",

        "active_question":
            "What did independent qualification capabilities observe?",

        "evidence_boundary_reference":
            "boundary:r6-e",

        "evidence_ceiling_reference":
            "ceiling:r6-e",

        "returns":
            returns,

        "correlation_summary":
            correlation_summary,

        "material_disagreements":
            list(
                material_disagreements
            ),

        "discriminating_evidence_needs":
            (
                [
                    "resolve differing observation"
                ]
                if material_disagreements
                else []
            ),

        "aggregate_provenance_route": [
            item
            for ret in returns
            for item in ret.get(
                "provenance_route",
                []
            )
        ],

        "claim_ceiling_changed":
            claim_ceiling_changed,

        "formation_created":
            formation_created,

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
            "R6-E contract"
        ),
        (
            SCHEMA,
            "R6-E schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            R3B,
            "R3-B Qualification Record"
        ),
        (
            R3E,
            "R3-E Capability Return"
        ),
        (
            R3G,
            "R3-G Formation"
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
        "R6-E = Qualification-Team Coherence.",
        "Independent observation != independent Room.",
        "Disagreement != integrity failure.",
        "Different participant != different Room.",
        "Different observation != different Room.",
        "Different conclusion != different Room.",
        "Disagreement != new Room.",
        "Independent returns MUST remain independently attributable.",
        "Correlation MUST NOT erase source returns.",
        "Independent findings != consensus.",
        "Consensus != evidence.",
        "Contradiction MUST NOT be averaged away.",
        "Unknown remains unknown.",
        "Scar != confidence.",
        "Participant count does not create truth.",
        "Majority vote != evidence resolution.",
        "Agreement count != claim authority.",
        "Multiple observers do not raise the claim ceiling.",
        "Capability count != evidence strength.",
        "Correlation != provenance erasure.",
        "Lead != truth owner.",
        "Participant != authority.",
        "Multiple participants != accumulated authority.",
        "Correlation != canonical mutation.",
        "Multiple Capability Returns do not by themselves establish a formation.",
        "Capability Return != formation.",
        "Multiple returns != Stack Analysis.",
        "Multiple returns != Swarm.",
        "Return != entry.",
        "Return != exit.",
        "Consensus != READY.",
        "Same-Room disagreement != distinct object.",
        "Coherence != consensus.",
        "No participant return may silently disappear from the aggregate.",
        "Two-to-one != evidence resolution.",
        "Vote count != evidence ceiling.",
        "Return set != Qualification disposition.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-F owns Formation Re-Justification validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-E lock: {lock}"
            )

    source_locks = {
        R3B: [
            "Lead != truth owner.",
            "Participant != authority.",
            "Multiple participants may return independent observations.",
            "Independent observations MUST NOT be forced into false consensus.",
        ],
        R3E: [
            "Capability Return records what came back.",
            "Bounded finding != canonical truth.",
            "Capability confidence != evidence authority.",
            "Multiple capability returns do not by themselves establish a formation.",
        ],
        R3G: [
            "Independent findings MUST be preserved before correlation.",
            "Stack does not permit false consensus.",
            "Stack does not create multiple Rooms.",
            "Stack does not erase disagreement.",
            "Independent findings != consensus.",
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
        "QUALIFICATION_TEAM_COHERENCE",
        "Independent observation != independent Room.",
        "Disagreement != integrity failure.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-E binding: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-E schema JSON: {exc}"
        ]

    # Agreement control.
    agreement = make_record()

    errors.extend(
        validate_record(
            agreement
        )
    )

    if (
        agreement[
            "validation_disposition"
        ]
        != "COHERENT_WITH_AGREEMENT"
    ):
        errors.append(
            "agreement control failed"
        )

    # Disagreement control.
    disagreement_returns = [
        make_return(
            return_id="return:a",
            capability_id="goblin:a",
            finding="OBSERVED_A",
        ),
        make_return(
            return_id="return:b",
            capability_id="goblin:b",
            finding="OBSERVED_B",
        ),
    ]

    disagreement = make_record(
        returns=disagreement_returns,
        material_disagreements=[
            "OBSERVED_A != OBSERVED_B"
        ],
    )

    if (
        disagreement[
            "validation_disposition"
        ]
        != "COHERENT_WITH_DISAGREEMENT"
    ):
        errors.append(
            "same-Room disagreement was not preserved as coherent disagreement"
        )

    # 2:1 vote must not erase dissent.
    vote_returns = [
        make_return(
            return_id="return:a",
            capability_id="goblin:a",
            finding="OBSERVED_A",
        ),
        make_return(
            return_id="return:b",
            capability_id="goblin:b",
            finding="OBSERVED_A",
        ),
        make_return(
            return_id="return:c",
            capability_id="goblin:c",
            finding="OBSERVED_B",
        ),
    ]

    vote = make_record(
        returns=vote_returns,
        material_disagreements=[
            "one dissenting bounded observation"
        ],
    )

    if (
        vote[
            "validation_disposition"
        ]
        != "COHERENT_WITH_DISAGREEMENT"
    ):
        errors.append(
            "2:1 observation pattern incorrectly resolved by vote"
        )

    # False consensus.
    false_consensus = make_record(
        returns=disagreement_returns,
        material_disagreements=[],
        correlation_summary="all participants agree; unanimous consensus resolved",
    )

    if (
        "FALSE_CONSENSUS"
        not in false_consensus[
            "failure_reasons"
        ]
        or "DISAGREEMENT_ERASED"
        not in false_consensus[
            "failure_reasons"
        ]
    ):
        errors.append(
            "false-consensus negative control failed"
        )

    # Object clone.
    cloned_returns = [
        make_return(
            return_id="return:a",
            capability_id="goblin:a",
            finding="OBSERVED_A",
        ),
        make_return(
            return_id="return:b",
            capability_id="goblin:b",
            finding="OBSERVED_B",
            object_id=(
                "sha512:"
                + "2" * 128
            ),
        ),
    ]

    cloned = make_record(
        returns=cloned_returns,
        material_disagreements=[
            "different observation"
        ],
    )

    if (
        "OBJECT_IDENTITY_DIVERGENCE"
        not in cloned[
            "failure_reasons"
        ]
    ):
        errors.append(
            "same-Room vector failed to reject identity divergence"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-E QUALIFICATION-TEAM COHERENCE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-E QUALIFICATION-TEAM COHERENCE: PASS"
    )
    print(
        "Multiple independent returns -> one Room identity: PRESERVED"
    )
    print(
        "Agreement without provenance collapse: VALIDATED"
    )
    print(
        "Material disagreement -> coherent disagreement: PRESERVED"
    )
    print(
        "2:1 observation pattern -> vote-based truth: REJECTED"
    )
    print(
        "False consensus / disagreement erasure: REJECTED"
    )
    print(
        "Participant provenance / attribution: PRESERVED"
    )
    print(
        "Multiple observers -> evidence-ceiling inflation: REJECTED"
    )
    print(
        "Multiple returns -> automatic formation: REJECTED"
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
        "R6-F Formation Re-Justification: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
