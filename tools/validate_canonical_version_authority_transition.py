#!/usr/bin/env python3

from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

APPROVED = "2d1013304c6c13efd08fc3a9d7aed7804642cde2"

VERSION = ROOT / "VERSION"
VERSION_JSON = ROOT / "VERSION.json"
VERSION_AUTHORITY = ROOT / "VERSION_AUTHORITY.md"
README = ROOT / "README.md"
CANONICAL_ENTRY = ROOT / (
    "canonical/"
    "ZERVAN_v41_0_CANONICAL_ENTRY.md"
)
CONTRACT = ROOT / (
    "contracts/promotion/"
    "CANONICAL_VERSION_AUTHORITY_TRANSITION.md"
)
SCHEMA = ROOT / (
    "schemas/promotion/"
    "canonical_version_authority_transition.schema.json"
)
RECEIPT = ROOT / (
    "receipts/promotion/"
    "R8_E_HUMAN_GATE_AUTHORIZATION_RECEIPT.json"
)


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


def validate():
    errors = []

    for path in (
        VERSION,
        VERSION_JSON,
        VERSION_AUTHORITY,
        README,
        CANONICAL_ENTRY,
        CONTRACT,
        SCHEMA,
        RECEIPT,
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
            "R8-H must validate on main"
        )

    ancestry = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            APPROVED,
            "HEAD",
        ],
        cwd=ROOT,
    )

    if ancestry.returncode != 0:
        errors.append(
            "approved promotion subject is not an ancestor of main HEAD"
        )

    try:
        candidate = git(
            "rev-parse",
            "origin/candidate/v41-complete",
        )

        if candidate != APPROVED:
            errors.append(
                "preserved candidate no longer equals approved subject"
            )
    except Exception as exc:
        errors.append(
            f"cannot resolve preserved candidate: {exc}"
        )

    if VERSION.read_text(
        encoding="utf-8"
    ).strip() != "vTemporal.41.0":
        errors.append(
            "VERSION identity changed during promotion"
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

    expected_metadata = {
        "version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "promotion_state": "CANONICAL",
        "canonical": True,
        "canonical_branch": "main",
    }

    for key, expected in expected_metadata.items():
        if metadata.get(key) != expected:
            errors.append(
                f"VERSION.json disagreement: {key}"
            )

    authority = normalized(
        VERSION_AUTHORITY
    )

    for marker in (
        "Status: CONTROLLED CANONICAL CONTRACT",
        "Promotion State: CANONICAL",
        "Canonical: TRUE",
        "Authority: NONE",
        "Human Gate: ACTIVE",
        "Its current promotion state is: `CANONICAL`",
    ):
        if marker not in authority:
            errors.append(
                f"VERSION_AUTHORITY disagreement: {marker}"
            )

    readme = normalized(
        README
    )

    for marker in (
        "This branch: `main`",
        "Promotion state: `CANONICAL`",
        "Canonical branch: `main`",
        "`CONTROLLED / CANONICAL / PROMOTED`",
    ):
        if marker not in readme:
            errors.append(
                f"README canonical orientation missing: {marker}"
            )

    entry = normalized(
        CANONICAL_ENTRY
    )

    for marker in (
        "Status: CONTROLLED CANONICAL ENTRY",
        "Promotion State: CANONICAL",
        "Canonical: TRUE",
        "Authority: NONE",
        "Human Gate: ACTIVE",
    ):
        if marker not in entry:
            errors.append(
                f"canonical entry disagreement: {marker}"
            )

    try:
        receipt = json.loads(
            RECEIPT.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"R8-E authorization receipt invalid: {exc}"
        ]

    expected_receipt = {
        "decision": "APPROVE",
        "authorization_state": "GRANTED",
        "decision_actor": "human",
        "decision_scope": "complete",
        "rationale": "I approve",
        "candidate_commit": APPROVED,
        "target_branch": "main",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "promotion_executed": False,
        "canonical": False,
        "promoted": False,
        "merged": False,
    }

    for key, expected in expected_receipt.items():
        if receipt.get(key) != expected:
            errors.append(
                f"R8-E preserved receipt disagreement: {key}"
            )

    contract = normalized(
        CONTRACT
    )

    for marker in (
        "R8-H = Canonical / Version Authority Transition.",
        f"Approved promotion subject = {APPROVED}.",
        "Active branch = main.",
        "Version = vTemporal.41.0.",
        "Implementation Identity = v41 Complete.",
        "Promotion State = CANONICAL.",
        "Canonical = TRUE.",
        "Canonical Branch = main.",
        "Candidate preserved = TRUE.",
        "Human Gate Authorization = GRANTED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "External runtime remains DISABLED.",
        "External action remains DISABLED.",
        "System population remains DISALLOWED.",
        "Promotion does not manufacture a new version.",
        "Authorization receipt history is immutable.",
        (
            "R8-H CANONICAL / VERSION AUTHORITY "
            "TRANSITION COMPLETE."
        ),
        "R8-I owns Post-Promotion Integrity Verification.",
    ):
        if marker not in contract:
            errors.append(
                f"R8-H lock missing: {marker}"
            )

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"R8-H schema invalid: {exc}"
        ]

    properties = schema.get(
        "properties",
        {}
    )

    expected_consts = {
        "version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "promotion_subject_commit": APPROVED,
        "active_branch": "main",
        "promotion_state": "CANONICAL",
        "canonical": True,
        "canonical_branch": "main",
        "candidate_preserved": True,
        "human_gate_authorization": "GRANTED",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "external_runtime": "DISABLED",
        "external_action": "DISABLED",
        "system_population": "DISALLOWED",
        "disposition": "CANONICAL_TRANSITION_VALIDATED",
    }

    for field, expected in expected_consts.items():
        if (
            properties.get(
                field,
                {},
            ).get("const")
            != expected
        ):
            errors.append(
                f"R8-H schema disagreement: {field}"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R8-H CANONICAL / VERSION AUTHORITY TRANSITION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R8-H CANONICAL / VERSION AUTHORITY TRANSITION: PASS"
    )
    print(
        f"Approved promotion subject: {APPROVED}"
    )
    print(
        "Active branch: main"
    )
    print(
        "Version: vTemporal.41.0"
    )
    print(
        "Implementation Identity: v41 Complete"
    )
    print(
        "Promotion State: CANONICAL"
    )
    print(
        "Canonical: TRUE"
    )
    print(
        "Human Gate Authorization: GRANTED"
    )
    print(
        "Authorization receipt: PRESERVED"
    )
    print(
        "Candidate preserved: TRUE"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "External Runtime: DISABLED"
    )
    print(
        "External Action: DISABLED"
    )
    print(
        "System Population: DISALLOWED"
    )
    print(
        "NEXT: R8-I Post-Promotion Integrity Verification"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
