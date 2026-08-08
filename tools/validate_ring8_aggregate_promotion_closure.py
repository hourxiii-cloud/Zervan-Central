#!/usr/bin/env python3

from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

APPROVED = "2d1013304c6c13efd08fc3a9d7aed7804642cde2"
R8H = "62bd3c9f54d46034181c9d94a443757a857423c1"
R8I = "e4ce260198fa962f9915f1af7f227454856a96ed"
R8J = "676e03e98b94f0461596f13605195242ba7290fc"
R8K = "be3e098fd4e50ed152a8f3060c6ba310aa096510"

VERSION_JSON = ROOT / "VERSION.json"

K_RECEIPT = ROOT / (
    "receipts/promotion/"
    "R8_K_PROMOTION_COMPLETION_RECEIPT.json"
)

CONTRACT = ROOT / (
    "contracts/promotion/"
    "RING8_AGGREGATE_HUMAN_GATE_PROMOTION_CLOSURE.md"
)

RECEIPT = ROOT / (
    "receipts/promotion/"
    "R8_L_AGGREGATE_PROMOTION_CLOSURE.json"
)

SCHEMA = ROOT / (
    "schemas/promotion/"
    "ring8_aggregate_promotion_closure.schema.json"
)


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def ancestor(base, head="HEAD"):
    return subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            base,
            head,
        ],
        cwd=ROOT,
    ).returncode == 0


def normalized(path):
    return " ".join(
        path.read_text(
            encoding="utf-8"
        ).split()
    )


def validate():
    errors = []

    for path in (
        VERSION_JSON,
        K_RECEIPT,
        CONTRACT,
        RECEIPT,
        SCHEMA,
    ):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    if git(
        "branch",
        "--show-current",
    ) != "main":
        errors.append(
            "R8-L must validate on main"
        )

    chain = [
        APPROVED,
        R8H,
        R8I,
        R8J,
        R8K,
    ]

    for left, right in zip(
        chain,
        chain[1:],
    ):
        if not ancestor(
            left,
            right,
        ):
            errors.append(
                f"promotion ancestry broken: {left} -> {right}"
            )

    if not ancestor(
        R8K,
        "HEAD",
    ):
        errors.append(
            "committed R8-K is not in current main lineage"
        )

    try:
        candidate = git(
            "rev-parse",
            "origin/candidate/v41-complete",
        )

        if candidate != APPROVED:
            errors.append(
                "preserved approved candidate moved"
            )
    except Exception as exc:
        errors.append(
            f"cannot resolve preserved candidate: {exc}"
        )

    metadata = json.loads(
        VERSION_JSON.read_text(
            encoding="utf-8"
        )
    )

    if metadata.get(
        "promotion_state"
    ) != "CANONICAL":
        errors.append(
            "promotion state is not CANONICAL"
        )

    if metadata.get(
        "canonical"
    ) is not True:
        errors.append(
            "canonical flag is not true"
        )

    if metadata.get(
        "canonical_branch"
    ) != "main":
        errors.append(
            "canonical branch is not main"
        )

    k = json.loads(
        K_RECEIPT.read_text(
            encoding="utf-8"
        )
    )

    for key, expected in {
        "approved_candidate_commit": APPROVED,
        "human_gate_decision": "APPROVE",
        "human_gate_authorization": "GRANTED",
        "promotion_executed": True,
        "candidate_preserved": True,
        "promotion_state": "CANONICAL",
        "canonical": True,
        "post_promotion_integrity": "VERIFIED",
        "post_promotion_fresh_reader": "VALIDATED",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "disposition": "PROMOTION_COMPLETED",
    }.items():
        if k.get(key) != expected:
            errors.append(
                f"R8-K completion disagreement: {key}"
            )

    receipt = json.loads(
        RECEIPT.read_text(
            encoding="utf-8"
        )
    )

    expected_receipt = {
        "approved_candidate_commit": APPROVED,
        "r8h_commit": R8H,
        "r8i_commit": R8I,
        "r8j_commit": R8J,
        "r8k_commit": R8K,
        "human_gate_decision": "APPROVE",
        "human_gate_authorization": "GRANTED",
        "r8f_disposition": "SKIPPED_BY_HUMAN_DIRECTION",
        "promotion_executed": True,
        "candidate_preserved": True,
        "fast_forward_promotion": True,
        "merge_commit_created": False,
        "promotion_state": "CANONICAL",
        "canonical": True,
        "canonical_branch": "main",
        "post_promotion_integrity": "VERIFIED",
        "post_promotion_fresh_reader": "VALIDATED",
        "promotion_completion": "RECORDED",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "external_runtime": "DISABLED",
        "external_action": "DISABLED",
        "system_population": "DISALLOWED",
        "disposition": "RING8_CLOSED_CANONICAL",
    }

    for key, expected in expected_receipt.items():
        if receipt.get(key) != expected:
            errors.append(
                f"R8-L receipt disagreement: {key}"
            )

    contract = normalized(
        CONTRACT
    )

    for marker in (
        "R8-L = Aggregate Human Gate / Promotion Closure.",
        f"Approved candidate = {APPROVED}.",
        f"R8-K committed completion anchor = {R8K}.",
        "Human Gate Decision = APPROVE.",
        "Human Gate Authorization = GRANTED.",
        "R8-F = SKIPPED BY HUMAN DIRECTION.",
        "Promotion executed = TRUE.",
        "Candidate preserved = TRUE.",
        "Fast-forward promotion = TRUE.",
        "Merge commit created = FALSE.",
        "Promotion State = CANONICAL.",
        "Canonical = TRUE.",
        "Post-Promotion Integrity = VERIFIED.",
        "Post-Promotion Fresh Reader = VALIDATED.",
        "Promotion Completion = RECORDED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Disposition = RING8_CLOSED_CANONICAL.",
        "RING 8 HUMAN GATE / PROMOTION = CLOSED.",
        (
            "R8-L AGGREGATE HUMAN GATE / "
            "PROMOTION CLOSURE COMPLETE."
        ),
    ):
        if marker not in contract:
            errors.append(
                f"R8-L closure marker missing: {marker}"
            )

    schema = json.loads(
        SCHEMA.read_text(
            encoding="utf-8"
        )
    )

    if (
        schema.get(
            "properties",
            {},
        ).get(
            "disposition",
            {},
        ).get(
            "const"
        )
        != "RING8_CLOSED_CANONICAL"
    ):
        errors.append(
            "R8-L schema disposition disagreement"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R8-L AGGREGATE HUMAN GATE / PROMOTION CLOSURE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R8-L AGGREGATE HUMAN GATE / PROMOTION CLOSURE: PASS"
    )
    print(
        f"Approved candidate: {APPROVED}"
    )
    print(
        f"R8-K completion anchor: {R8K}"
    )
    print(
        "Human Gate Decision: APPROVE"
    )
    print(
        "Human Gate Authorization: GRANTED"
    )
    print(
        "R8-F: SKIPPED BY HUMAN DIRECTION"
    )
    print(
        "Promotion executed: TRUE"
    )
    print(
        "Candidate preserved: TRUE"
    )
    print(
        "Fast-forward promotion: TRUE"
    )
    print(
        "Merge commit created: FALSE"
    )
    print(
        "Promotion State: CANONICAL"
    )
    print(
        "Canonical: TRUE"
    )
    print(
        "Post-Promotion Integrity: VERIFIED"
    )
    print(
        "Post-Promotion Fresh Reader: VALIDATED"
    )
    print(
        "Promotion Completion: RECORDED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Disposition: RING8_CLOSED_CANONICAL"
    )
    print(
        "RING 8 HUMAN GATE / PROMOTION: CLOSED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
