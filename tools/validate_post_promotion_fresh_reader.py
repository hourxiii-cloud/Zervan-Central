#!/usr/bin/env python3

from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

VERSION = ROOT / "VERSION"
VERSION_JSON = ROOT / "VERSION.json"
VERSION_AUTHORITY = ROOT / "VERSION_AUTHORITY.md"
README = ROOT / "README.md"
INIT = ROOT / "call/INITIATION_STATEMENT_V41_0.md"
ENTRY = ROOT / "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md"
R8I = ROOT / (
    "contracts/promotion/"
    "POST_PROMOTION_INTEGRITY_VERIFICATION.md"
)
CONTRACT = ROOT / (
    "contracts/promotion/"
    "POST_PROMOTION_FRESH_READER.md"
)
SCHEMA = ROOT / (
    "schemas/promotion/"
    "post_promotion_fresh_reader.schema.json"
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
        INIT,
        ENTRY,
        R8I,
        CONTRACT,
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
            "R8-J must validate on main"
        )

    if VERSION.read_text(
        encoding="utf-8"
    ).strip() != "vTemporal.41.0":
        errors.append(
            "fresh reader cannot resolve expected active version"
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
                f"fresh-reader VERSION.json disagreement: {key}"
            )

    readme = normalized(
        README
    )

    for marker in (
        "This branch: `main`",
        "Promotion state: `CANONICAL`",
        "Canonical branch: `main`",
        "`CONTROLLED / CANONICAL / PROMOTED`",
        "Native v41 does not require prior v39 or v40 knowledge to initialize.",
    ):
        if marker not in readme:
            errors.append(
                f"README fresh-reader marker missing: {marker}"
            )

    init = normalized(
        INIT
    )

    for marker in (
        "Promotion State: CANONICAL",
        "Canonical: TRUE",
        "CONTROLLED / CANONICAL / PROMOTED",
        "Promotion State remains CANONICAL.",
        "Current Git is implementation truth.",
        "Do not use stored memory as implementation authority.",
        (
            "Do not use prior conversation as implementation "
            "authority when Git can answer."
        ),
        "Native-v41 initialization MUST NOT require v39 or v40 knowledge.",
    ):
        if marker not in init:
            errors.append(
                f"initiation fresh-reader marker missing: {marker}"
            )

    for stale in (
        "Promotion State: CANDIDATE",
        "Canonical: FALSE",
        "CONTROLLED / CANDIDATE / PRE-PROMOTION",
        "Promotion State remains CANDIDATE.",
    ):
        if stale in init:
            errors.append(
                f"active initiation candidate residue: {stale}"
            )

    entry = normalized(
        ENTRY
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
                f"canonical entry fresh-reader marker missing: {marker}"
            )

    r8i = normalized(
        R8I
    )

    for marker in (
        "Disposition = POST_PROMOTION_INTEGRITY_VERIFIED.",
        "R8-I POST-PROMOTION INTEGRITY VERIFICATION COMPLETE.",
        "R8-J owns Post-Promotion Fresh Reader.",
    ):
        if marker not in r8i:
            errors.append(
                f"R8-I prerequisite missing: {marker}"
            )

    contract = normalized(
        CONTRACT
    )

    for marker in (
        "R8-J = Post-Promotion Fresh Reader.",
        "Repository-only initialization = REQUIRED.",
        "Main-only canonical resolution = REQUIRED.",
        "Candidate-branch dependency = REJECTED.",
        "Prior-conversation dependency = REJECTED.",
        "Stored-memory dependency = REJECTED.",
        "Original-architect dependency = REJECTED.",
        "v39 dependency = REJECTED.",
        "v40 dependency = REJECTED.",
        "Historical artifact substitution = REJECTED.",
        "Active initiation candidate-state residue = REJECTED.",
        "Canonical version resolution = VALIDATED.",
        "Canonical entry resolution = VALIDATED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Disposition = POST_PROMOTION_FRESH_READER_VALIDATED.",
        "R8-J POST-PROMOTION FRESH READER COMPLETE.",
        "R8-K owns Promotion Completion Receipt.",
    ):
        if marker not in contract:
            errors.append(
                f"R8-J lock missing: {marker}"
            )

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"R8-J schema invalid: {exc}"
        ]

    properties = schema.get(
        "properties",
        {},
    )

    expected_consts = {
        "version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "active_branch": "main",
        "promotion_state": "CANONICAL",
        "canonical": True,
        "candidate_dependency": False,
        "conversation_dependency": False,
        "stored_memory_dependency": False,
        "original_architect_dependency": False,
        "historical_v39_dependency": False,
        "historical_v40_dependency": False,
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "disposition": "POST_PROMOTION_FRESH_READER_VALIDATED",
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
                f"R8-J schema disagreement: {field}"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R8-J POST-PROMOTION FRESH READER: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R8-J POST-PROMOTION FRESH READER: PASS"
    )
    print(
        "Repository-only initialization: VALIDATED"
    )
    print(
        "Main-only canonical resolution: VALIDATED"
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
        "Candidate-branch dependency: REJECTED"
    )
    print(
        "Prior-conversation dependency: REJECTED"
    )
    print(
        "Stored-memory dependency: REJECTED"
    )
    print(
        "Original-architect dependency: REJECTED"
    )
    print(
        "v39 / v40 dependency: REJECTED"
    )
    print(
        "Active initiation candidate residue: NONE"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Disposition: POST_PROMOTION_FRESH_READER_VALIDATED"
    )
    print(
        "NEXT: R8-K Promotion Completion Receipt"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
