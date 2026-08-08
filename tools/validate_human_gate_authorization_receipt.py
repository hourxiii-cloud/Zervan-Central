#!/usr/bin/env python3

from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]

R8D = ROOT / (
    "contracts/promotion/"
    "PRE_PROMOTION_VERIFICATION.md"
)
CONTRACT = ROOT / (
    "contracts/promotion/"
    "HUMAN_GATE_AUTHORIZATION_RECEIPT.md"
)
SCHEMA = ROOT / (
    "schemas/promotion/"
    "human_gate_authorization_receipt.schema.json"
)
ISSUER_PATH = ROOT / (
    "tools/"
    "issue_human_gate_authorization_receipt.py"
)


def normalized(path):
    return " ".join(
        path.read_text(
            encoding="utf-8"
        ).split()
    )


def load_issuer():
    spec = importlib.util.spec_from_file_location(
        "issue_human_gate_authorization_receipt",
        ISSUER_PATH,
    )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


def validate():
    errors = []

    for path in (
        R8D,
        CONTRACT,
        SCHEMA,
        ISSUER_PATH,
    ):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    r8d = normalized(R8D)

    for marker in (
        "R8-D PRE-PROMOTION VERIFICATION COMPLETE.",
        "Decision instance = NONE.",
        "Human Gate Authorization remains NOT_GRANTED.",
        "R8-E owns Human Gate Authorization Receipt.",
    ):
        if marker not in r8d:
            errors.append(
                f"R8-E R8-D prerequisite missing: {marker}"
            )

    contract = normalized(CONTRACT)

    for marker in (
        "R8-E = Human Gate Authorization Receipt.",
        "R8-E is the Human Gate hard stop.",
        "Decision states = APPROVE / REJECT / DEFER.",
        "APPROVE -> GRANTED.",
        "REJECT -> DENIED.",
        "DEFER -> DEFERRED.",
        "Approval != execution.",
        "Authorization receipt != execution.",
        "Authorization does not float with branch HEAD.",
        "Exact candidate binding = REQUIRED.",
        "Explicit human decision actor = REQUIRED.",
        "Decision scope = REQUIRED.",
        "Decision timestamp = REQUIRED.",
        "Promotion executed by receipt = FALSE.",
        "Canonical established by receipt = FALSE.",
        "Promoted established by receipt = FALSE.",
        "Merged established by receipt = FALSE.",
        "Current decision instance = NONE.",
        "Current Human Gate Authorization = NOT_GRANTED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "R8-E AUTHORIZATION RECEIPT MECHANISM COMPLETE.",
        "RING 8 STATE = WAITING_FOR_HUMAN_GATE.",
        (
            "R8-F is blocked until explicit Human Gate "
            "APPROVE authorization exists."
        ),
    ):
        if marker not in contract:
            errors.append(
                f"R8-E lock missing: {marker}"
            )

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"invalid R8-E schema JSON: {exc}"
        ]

    decisions = (
        schema.get(
            "properties",
            {},
        )
        .get(
            "decision",
            {},
        )
        .get(
            "enum",
            [],
        )
    )

    if decisions != [
        "APPROVE",
        "REJECT",
        "DEFER",
    ]:
        errors.append(
            "R8-E decision enum disagreement"
        )

    issuer = load_issuer()

    if issuer.AUTHORIZATION_MAP != {
        "APPROVE": "GRANTED",
        "REJECT": "DENIED",
        "DEFER": "DEFERRED",
    }:
        errors.append(
            "R8-E authorization mapping disagreement"
        )

    for decision, expected in (
        (
            "APPROVE",
            "GRANTED",
        ),
        (
            "REJECT",
            "DENIED",
        ),
        (
            "DEFER",
            "DEFERRED",
        ),
    ):
        try:
            receipt = issuer.issue(
                decision=decision,
                actor="TEST_HUMAN",
                scope="TEST_SCOPE",
                rationale="TEST_RATIONALE",
                timestamp="2026-01-01T00:00:00+00:00",
            )
        except Exception as exc:
            errors.append(
                f"R8-E issuer failed for {decision}: {exc}"
            )
            continue

        if (
            receipt[
                "authorization_state"
            ]
            != expected
        ):
            errors.append(
                f"R8-E wrong mapping for {decision}"
            )

        if receipt[
            "authority_state"
        ] != "NONE":
            errors.append(
                "R8-E improperly changed runtime authority"
            )

        if receipt[
            "promotion_executed"
        ]:
            errors.append(
                "R8-E improperly claims promotion execution"
            )

        if receipt[
            "canonical"
        ]:
            errors.append(
                "R8-E improperly claims canonical state"
            )

        if receipt[
            "promoted"
        ]:
            errors.append(
                "R8-E improperly claims promoted state"
            )

        if receipt[
            "merged"
        ]:
            errors.append(
                "R8-E improperly claims merged state"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R8-E HUMAN GATE AUTHORIZATION RECEIPT: FAIL"
        )

        for error in errors:
            print(f" - {error}")

        return 1

    print(
        "R8-E HUMAN GATE AUTHORIZATION RECEIPT: PASS"
    )
    print(
        "Receipt mechanism: VALIDATED"
    )
    print(
        "Decision states: APPROVE / REJECT / DEFER"
    )
    print(
        "APPROVE -> GRANTED"
    )
    print(
        "REJECT -> DENIED"
    )
    print(
        "DEFER -> DEFERRED"
    )
    print(
        "Current decision instance: NONE"
    )
    print(
        "Current Human Gate Authorization: NOT_GRANTED"
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
        "RING 8 STATE: WAITING_FOR_HUMAN_GATE"
    )
    print(
        "R8-F Promotion Execution Manifest: BLOCKED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
