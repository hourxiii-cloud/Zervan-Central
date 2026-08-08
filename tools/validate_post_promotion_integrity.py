#!/usr/bin/env python3

from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

APPROVED = "2d1013304c6c13efd08fc3a9d7aed7804642cde2"
R8H_COMMIT = "62bd3c9f54d46034181c9d94a443757a857423c1"

VERSION_JSON = ROOT / "VERSION.json"
R8H = ROOT / (
    "contracts/promotion/"
    "CANONICAL_VERSION_AUTHORITY_TRANSITION.md"
)
RECEIPT = ROOT / (
    "receipts/promotion/"
    "R8_E_HUMAN_GATE_AUTHORIZATION_RECEIPT.json"
)
CONTRACT = ROOT / (
    "contracts/promotion/"
    "POST_PROMOTION_INTEGRITY_VERIFICATION.md"
)
SCHEMA = ROOT / (
    "schemas/promotion/"
    "post_promotion_integrity_verification.schema.json"
)
RUNNER = ROOT / "tools/validate_ring8.py"

AUTHORIZED_R8H_DELTA = {
    "README.md",
    "VERSION.json",
    "VERSION_AUTHORITY.md",
    "VERSION_REFERENCES.json",
    "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md",
    "contracts/promotion/CANONICAL_VERSION_AUTHORITY_TRANSITION.md",
    "receipts/promotion/R8_E_HUMAN_GATE_AUTHORIZATION_RECEIPT.json",
    "schemas/promotion/canonical_version_authority_transition.schema.json",
    "tests/test_canonical_version_authority_transition.py",
    "tools/validate_canonical_version_authority_transition.py",
    "tools/validate_ring8.py",
}


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def normalized(path):
    return " ".join(
        path.read_text(
            encoding="utf-8"
        ).split()
    )


def is_ancestor(base, head):
    result = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            base,
            head,
        ],
        cwd=ROOT,
    )

    return result.returncode == 0


def committed_r8h_delta():
    text = git(
        "diff",
        "--name-only",
        APPROVED,
        R8H_COMMIT,
    )

    return set(
        filter(
            None,
            text.splitlines(),
        )
    )


def build_result():
    return {
        "schema_version": "1.0",
        "record_type": "POST_PROMOTION_INTEGRITY_VERIFICATION",
        "ring": "R8-I",
        "approved_candidate_commit": APPROVED,
        "canonical_transition_commit": R8H_COMMIT,
        "candidate_preserved": (
            git(
                "rev-parse",
                "origin/candidate/v41-complete",
            )
            == APPROVED
        ),
        "approved_candidate_in_main": is_ancestor(
            APPROVED,
            "HEAD",
        ),
        "canonical_transition_in_main": is_ancestor(
            R8H_COMMIT,
            "HEAD",
        ),
        "authorized_delta_exact": (
            committed_r8h_delta()
            == AUTHORIZED_R8H_DELTA
        ),
        "authorized_delta_count": len(
            committed_r8h_delta()
        ),
        "human_gate_authorization": "GRANTED",
        "canonical": True,
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "disposition": "POST_PROMOTION_INTEGRITY_VERIFIED",
    }


def validate():
    errors = []

    for path in (
        VERSION_JSON,
        R8H,
        RECEIPT,
        CONTRACT,
        SCHEMA,
        RUNNER,
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
            "R8-I must validate on main"
        )

    try:
        if git(
            "rev-parse",
            "origin/candidate/v41-complete",
        ) != APPROVED:
            errors.append(
                "preserved candidate branch moved"
            )
    except Exception as exc:
        errors.append(
            f"cannot resolve preserved candidate: {exc}"
        )

    if not is_ancestor(
        APPROVED,
        R8H_COMMIT,
    ):
        errors.append(
            "approved candidate is not ancestor of R8-H"
        )

    if not is_ancestor(
        R8H_COMMIT,
        "HEAD",
    ):
        errors.append(
            "R8-H canonical transition is not in current main lineage"
        )

    actual_delta = committed_r8h_delta()

    if actual_delta != AUTHORIZED_R8H_DELTA:
        missing = sorted(
            AUTHORIZED_R8H_DELTA
            - actual_delta
        )

        extra = sorted(
            actual_delta
            - AUTHORIZED_R8H_DELTA
        )

        if missing:
            errors.append(
                "authorized R8-H delta missing: "
                + ", ".join(missing)
            )

        if extra:
            errors.append(
                "unauthorized R8-H delta: "
                + ", ".join(extra)
            )

    try:
        metadata = json.loads(
            VERSION_JSON.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"VERSION.json invalid: {exc}"
        ]

    if metadata.get(
        "promotion_state"
    ) != "CANONICAL":
        errors.append(
            "VERSION.json promotion state is not canonical"
        )

    if metadata.get(
        "canonical"
    ) is not True:
        errors.append(
            "VERSION.json canonical is not true"
        )

    if metadata.get(
        "canonical_branch"
    ) != "main":
        errors.append(
            "VERSION.json canonical branch is not main"
        )

    r8h = normalized(
        R8H
    )

    for marker in (
        "Promotion State = CANONICAL.",
        "Canonical = TRUE.",
        "Candidate preserved = TRUE.",
        "Human Gate Authorization = GRANTED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        (
            "R8-H CANONICAL / VERSION AUTHORITY "
            "TRANSITION COMPLETE."
        ),
    ):
        if marker not in r8h:
            errors.append(
                f"R8-H integrity marker missing: {marker}"
            )

    try:
        receipt = json.loads(
            RECEIPT.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"authorization receipt invalid: {exc}"
        ]

    expected_receipt = {
        "decision": "APPROVE",
        "authorization_state": "GRANTED",
        "candidate_commit": APPROVED,
        "target_branch": "main",
        "decision_actor": "human",
        "decision_scope": "complete",
        "rationale": "I approve",
        "promotion_executed": False,
        "canonical": False,
        "promoted": False,
        "merged": False,
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
    }

    for key, expected in expected_receipt.items():
        if receipt.get(
            key
        ) != expected:
            errors.append(
                f"authorization receipt disagreement: {key}"
            )

    runner = RUNNER.read_text(
        encoding="utf-8"
    )

    footer_start = runner.find(
        'print("CURRENT: R8-I PASS")'
    )

    if footer_start == -1:
        errors.append(
            "R8-I runner footer missing"
        )
    else:
        footer = runner[
            footer_start:
        ]

        for marker in (
            'print("R8-G: PROMOTION EXECUTED")',
            (
                'print("R8-H: CANONICAL '
                'TRANSITION COMPLETE")'
            ),
            (
                'print("R8-E Human Gate '
                'Authorization: GRANTED")'
            ),
            (
                'print("Post-Promotion '
                'Integrity: VERIFIED")'
            ),
            'print("Candidate preserved: TRUE")',
            'print("Canonical: TRUE")',
            'print("Authority: NONE")',
            'print("Human Gate: ACTIVE")',
            'print("Promotion State: CANONICAL")',
        ):
            if marker not in footer:
                errors.append(
                    f"canonical Ring 8 footer missing: {marker}"
                )

        for stale in (
            'print("Human Gate Authorization: NOT_GRANTED")',
            'print("Promotion State: CANDIDATE")',
        ):
            if stale in footer:
                errors.append(
                    f"stale Ring 8 footer state: {stale}"
                )

    contract = normalized(
        CONTRACT
    )

    for marker in (
        "R8-I = Post-Promotion Integrity Verification.",
        "Approved candidate ancestry = REQUIRED.",
        "R8-H canonical-transition ancestry = REQUIRED.",
        "Candidate branch preservation = REQUIRED.",
        "Authorized R8-H delta = EXACT.",
        "Authorized R8-H delta count = 11.",
        "Human Gate provenance = PRESERVED.",
        "Canonical state agreement = REQUIRED.",
        "Stale pre-promotion runner state = REJECTED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Disposition = POST_PROMOTION_INTEGRITY_VERIFIED.",
        (
            "R8-I POST-PROMOTION INTEGRITY "
            "VERIFICATION COMPLETE."
        ),
        "R8-J owns Post-Promotion Fresh Reader.",
    ):
        if marker not in contract:
            errors.append(
                f"R8-I lock missing: {marker}"
            )

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"R8-I schema invalid: {exc}"
        ]

    properties = schema.get(
        "properties",
        {},
    )

    expected_consts = {
        "approved_candidate_commit": APPROVED,
        "canonical_transition_commit": R8H_COMMIT,
        "candidate_preserved": True,
        "approved_candidate_in_main": True,
        "canonical_transition_in_main": True,
        "authorized_delta_exact": True,
        "authorized_delta_count": 11,
        "human_gate_authorization": "GRANTED",
        "canonical": True,
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "disposition": "POST_PROMOTION_INTEGRITY_VERIFIED",
    }

    for field, expected in expected_consts.items():
        if (
            properties.get(
                field,
                {},
            ).get(
                "const"
            )
            != expected
        ):
            errors.append(
                f"R8-I schema disagreement: {field}"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R8-I POST-PROMOTION INTEGRITY VERIFICATION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    result = build_result()

    print(
        "R8-I POST-PROMOTION INTEGRITY VERIFICATION: PASS"
    )
    print(
        f"Approved candidate: {APPROVED}"
    )
    print(
        f"R8-H canonical transition: {R8H_COMMIT}"
    )
    print(
        "Approved candidate ancestry: VERIFIED"
    )
    print(
        "R8-H canonical-transition ancestry: VERIFIED"
    )
    print(
        "Candidate preserved: TRUE"
    )
    print(
        "Authorized R8-H delta: EXACT"
    )
    print(
        f"Authorized R8-H delta count: "
        f"{result['authorized_delta_count']}"
    )
    print(
        "Human Gate provenance: PRESERVED"
    )
    print(
        "Canonical state agreement: VERIFIED"
    )
    print(
        "Stale runner state: REMOVED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Disposition: POST_PROMOTION_INTEGRITY_VERIFIED"
    )
    print(
        "NEXT: R8-J Post-Promotion Fresh Reader"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
