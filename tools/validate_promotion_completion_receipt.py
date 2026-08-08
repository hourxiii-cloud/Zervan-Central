#!/usr/bin/env python3

from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

APPROVED = "2d1013304c6c13efd08fc3a9d7aed7804642cde2"
R8H_COMMIT = "62bd3c9f54d46034181c9d94a443757a857423c1"
R8I_COMMIT = "e4ce260198fa962f9915f1af7f227454856a96ed"
R8J_COMMIT = "676e03e98b94f0461596f13605195242ba7290fc"

CONTRACT = ROOT / (
    "contracts/promotion/"
    "PROMOTION_COMPLETION_RECEIPT.md"
)
RECEIPT = ROOT / (
    "receipts/promotion/"
    "R8_K_PROMOTION_COMPLETION_RECEIPT.json"
)
SCHEMA = ROOT / (
    "schemas/promotion/"
    "promotion_completion_receipt.schema.json"
)
R8J = ROOT / (
    "contracts/promotion/"
    "POST_PROMOTION_FRESH_READER.md"
)
VERSION_JSON = ROOT / "VERSION.json"


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
        CONTRACT,
        RECEIPT,
        SCHEMA,
        R8J,
        VERSION_JSON,
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
            "R8-K must validate on main"
        )

    if git(
        "rev-parse",
        "HEAD",
    ) != R8J_COMMIT:
        errors.append(
            "R8-K development-time validation must begin from committed R8-J"
        )

    for commit, name in (
        (
            APPROVED,
            "approved candidate",
        ),
        (
            R8H_COMMIT,
            "R8-H canonical transition",
        ),
        (
            R8I_COMMIT,
            "R8-I integrity verification",
        ),
        (
            R8J_COMMIT,
            "R8-J fresh-reader validation",
        ),
    ):
        if not ancestor(
            commit,
            "HEAD",
        ):
            errors.append(
                f"{name} is not in main lineage"
            )

    try:
        candidate = git(
            "rev-parse",
            "origin/candidate/v41-complete",
        )

        if candidate != APPROVED:
            errors.append(
                "preserved candidate moved"
            )
    except Exception as exc:
        errors.append(
            f"cannot resolve preserved candidate: {exc}"
        )

    receipt = json.loads(
        RECEIPT.read_text(
            encoding="utf-8"
        )
    )

    expected = {
        "receipt_type": "PROMOTION_COMPLETION_RECEIPT",
        "ring": "R8-K",
        "version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "approved_candidate_commit": APPROVED,
        "r8h_canonical_transition_commit": R8H_COMMIT,
        "r8i_integrity_verification_commit": R8I_COMMIT,
        "r8j_fresh_reader_commit": R8J_COMMIT,
        "completion_anchor_commit": R8J_COMMIT,
        "source_branch": "candidate/v41-complete",
        "target_branch": "main",
        "human_gate_decision": "APPROVE",
        "human_gate_authorization": "GRANTED",
        "decision_actor": "human",
        "decision_scope": "complete",
        "rationale": "I approve",
        "promotion_executed": True,
        "candidate_preserved": True,
        "fast_forward_promotion": True,
        "merge_commit_created": False,
        "promotion_state": "CANONICAL",
        "canonical": True,
        "canonical_branch": "main",
        "post_promotion_integrity": "VERIFIED",
        "post_promotion_fresh_reader": "VALIDATED",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "external_runtime": "DISABLED",
        "external_action": "DISABLED",
        "system_population": "DISALLOWED",
        "disposition": "PROMOTION_COMPLETED",
    }

    for key, value in expected.items():
        if receipt.get(
            key
        ) != value:
            errors.append(
                f"R8-K receipt disagreement: {key}"
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
            "active promotion state is not CANONICAL"
        )

    if metadata.get(
        "canonical"
    ) is not True:
        errors.append(
            "active canonical flag is not true"
        )

    r8j = normalized(
        R8J
    )

    for marker in (
        "Disposition = POST_PROMOTION_FRESH_READER_VALIDATED.",
        "R8-J POST-PROMOTION FRESH READER COMPLETE.",
        "R8-K owns Promotion Completion Receipt.",
    ):
        if marker not in r8j:
            errors.append(
                f"R8-J prerequisite missing: {marker}"
            )

    contract = normalized(
        CONTRACT
    )

    for marker in (
        "R8-K = Promotion Completion Receipt.",
        f"Approved candidate = {APPROVED}.",
        f"R8-H canonical transition = {R8H_COMMIT}.",
        f"R8-I integrity verification = {R8I_COMMIT}.",
        f"R8-J fresh-reader validation = {R8J_COMMIT}.",
        "Human Gate Decision = APPROVE.",
        "Human Gate Authorization = GRANTED.",
        "Promotion executed = TRUE.",
        "Candidate preserved = TRUE.",
        "Fast-forward promotion = TRUE.",
        "Merge commit created = FALSE.",
        "Promotion State = CANONICAL.",
        "Canonical = TRUE.",
        "Canonical Branch = main.",
        "Post-Promotion Integrity = VERIFIED.",
        "Post-Promotion Fresh Reader = VALIDATED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Disposition = PROMOTION_COMPLETED.",
        "No self-referential completion receipt is permitted.",
        "R8-K PROMOTION COMPLETION RECEIPT COMPLETE.",
        "R8-L owns Aggregate Human Gate / Promotion Closure.",
    ):
        if marker not in contract:
            errors.append(
                f"R8-K lock missing: {marker}"
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
        != "PROMOTION_COMPLETED"
    ):
        errors.append(
            "R8-K schema disposition disagreement"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R8-K PROMOTION COMPLETION RECEIPT: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R8-K PROMOTION COMPLETION RECEIPT: PASS"
    )
    print(
        f"Approved candidate: {APPROVED}"
    )
    print(
        f"Completion anchor: {R8J_COMMIT}"
    )
    print(
        "Human Gate Decision: APPROVE"
    )
    print(
        "Human Gate Authorization: GRANTED"
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
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Disposition: PROMOTION_COMPLETED"
    )
    print(
        "NEXT: R8-L Aggregate Human Gate / Promotion Closure"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
