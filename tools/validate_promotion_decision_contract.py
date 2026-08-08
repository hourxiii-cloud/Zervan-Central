#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

R8A = ROOT / (
    "contracts/promotion/"
    "RING8_HUMAN_GATE_PROMOTION_BOUNDARY.md"
)

CONTRACT = ROOT / (
    "contracts/promotion/"
    "PROMOTION_DECISION_CONTRACT.md"
)

SCHEMA = ROOT / (
    "schemas/promotion/"
    "promotion_decision.schema.json"
)


def normalized(text):
    return " ".join(
        text.split()
    )


def validate():
    errors = []

    for path in (
        R8A,
        CONTRACT,
        SCHEMA,
    ):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    r8a = normalized(
        R8A.read_text(
            encoding="utf-8"
        )
    )

    contract = normalized(
        CONTRACT.read_text(
            encoding="utf-8"
        )
    )

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"invalid promotion-decision schema JSON: {exc}"
        ]

    for marker in (
        "R8-A INSTANTIATED.",
        "Ring 7 state = READY_FOR_HUMAN_GATE.",
        "Human Gate Authorization remains NOT_GRANTED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
    ):
        if marker not in r8a:
            errors.append(
                f"R8-A prerequisite missing: {marker}"
            )

    for marker in (
        "R8-B = Promotion Decision Contract.",
        "Decision states = APPROVE / REJECT / DEFER.",
        "Decision != execution.",
        "Approval != execution.",
        "Contract != decision instance.",
        "Decision actor must be explicitly supplied.",
        "Candidate commit must be exact.",
        "Target branch = main.",
        "R8-B creates no approval.",
        "R8-B creates no rejection.",
        "R8-B creates no deferral.",
        "Human Gate Authorization remains NOT_GRANTED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "Canonical remains FALSE.",
        "Promoted remains FALSE.",
        "Merged remains FALSE.",
        "R8-B PROMOTION DECISION CONTRACT COMPLETE.",
        "R8-C owns Promotion Candidate Binding.",
    ):
        if marker not in contract:
            errors.append(
                f"R8-B contract lock missing: {marker}"
            )

    if (
        schema.get("$schema")
        != "https://json-schema.org/draft/2020-12/schema"
    ):
        errors.append(
            "R8-B schema draft disagreement"
        )

    properties = schema.get(
        "properties",
        {}
    )

    decision = properties.get(
        "decision",
        {}
    )

    if decision.get("enum") != [
        "APPROVE",
        "REJECT",
        "DEFER",
    ]:
        errors.append(
            "R8-B decision enum disagreement"
        )

    if (
        properties.get(
            "candidate_branch",
            {},
        ).get("const")
        != "candidate/v41-complete"
    ):
        errors.append(
            "R8-B candidate branch disagreement"
        )

    if (
        properties.get(
            "target_branch",
            {},
        ).get("const")
        != "main"
    ):
        errors.append(
            "R8-B target branch disagreement"
        )

    if (
        properties.get(
            "authority_state",
            {},
        ).get("const")
        != "NONE"
    ):
        errors.append(
            "R8-B authority schema disagreement"
        )

    if (
        properties.get(
            "human_gate_state",
            {},
        ).get("const")
        != "ACTIVE"
    ):
        errors.append(
            "R8-B Human Gate schema disagreement"
        )

    prohibited_contract_states = (
        "Human Gate Authorization: GRANTED",
        "Promotion State: CANONICAL",
        "Canonical: TRUE",
        "Promoted: TRUE",
        "Merged: TRUE",
    )

    raw_contract = CONTRACT.read_text(
        encoding="utf-8"
    )

    for marker in prohibited_contract_states:
        if marker in raw_contract:
            errors.append(
                f"R8-B improperly claims state: {marker}"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R8-B PROMOTION DECISION CONTRACT: FAIL"
        )

        for error in errors:
            print(f" - {error}")

        return 1

    print(
        "R8-B PROMOTION DECISION CONTRACT: PASS"
    )
    print(
        "Decision states: APPROVE / REJECT / DEFER"
    )
    print(
        "Decision instance created: FALSE"
    )
    print(
        "Human Gate authorization: NOT_GRANTED"
    )
    print(
        "Promotion executed: FALSE"
    )
    print(
        "Canonical mutation: FALSE"
    )
    print(
        "Merge executed: FALSE"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Promotion State: CANDIDATE"
    )
    print(
        "R8-B PROMOTION DECISION CONTRACT COMPLETE"
    )
    print(
        "R8-C Promotion Candidate Binding: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
