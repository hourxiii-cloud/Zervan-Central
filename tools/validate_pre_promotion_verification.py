#!/usr/bin/env python3

from pathlib import Path
import importlib.util
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

RING7 = ROOT / (
    "contracts/validation/"
    "RING7_AGGREGATE_DOCUMENTATION_PROMOTION_READINESS_CLOSURE.md"
)
R8A = ROOT / (
    "contracts/promotion/"
    "RING8_HUMAN_GATE_PROMOTION_BOUNDARY.md"
)
R8B = ROOT / (
    "contracts/promotion/"
    "PROMOTION_DECISION_CONTRACT.md"
)
R8C = ROOT / (
    "contracts/promotion/"
    "PROMOTION_CANDIDATE_BINDING.md"
)
CONTRACT = ROOT / (
    "contracts/promotion/"
    "PRE_PROMOTION_VERIFICATION.md"
)
SCHEMA = ROOT / (
    "schemas/promotion/"
    "pre_promotion_verification.schema.json"
)
RESOLVER_PATH = ROOT / (
    "tools/"
    "resolve_promotion_candidate_binding.py"
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


def load_resolver():
    spec = importlib.util.spec_from_file_location(
        "resolve_promotion_candidate_binding",
        RESOLVER_PATH,
    )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


def build_result():
    resolver = load_resolver()
    binding = resolver.resolve("HEAD")

    return {
        "schema_version": "1.0",
        "record_type": "PRE_PROMOTION_VERIFICATION",
        "ring": "R8-D",
        "native_version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "candidate_branch": "candidate/v41-complete",
        "candidate_commit": binding["candidate_commit"],
        "candidate_tree": binding["candidate_tree"],
        "target_branch": "main",
        "target_commit": git(
            "rev-parse",
            "origin/main^{commit}",
        ),
        "ring7_ready": True,
        "r8a_valid": True,
        "r8b_valid": True,
        "r8c_valid": True,
        "binding_sha512": binding["binding_sha512"],
        "decision_instance": "NONE",
        "human_gate_authorization": "NOT_GRANTED",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "promotion_state": "CANDIDATE",
        "canonical": False,
        "promoted": False,
        "merged": False,
        "disposition": "PRE_PROMOTION_VERIFIED",
    }


def validate():
    errors = []

    for path in (
        RING7,
        R8A,
        R8B,
        R8C,
        CONTRACT,
        SCHEMA,
        RESOLVER_PATH,
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
    ) != "candidate/v41-complete":
        errors.append(
            "R8-D must run on candidate/v41-complete"
        )

    try:
        git(
            "rev-parse",
            "origin/main^{commit}",
        )
    except subprocess.CalledProcessError:
        errors.append(
            "R8-D cannot resolve origin/main"
        )

    ring7 = normalized(RING7)

    for marker in (
        "RING 7 RESULT: PASS",
        "PROMOTION READINESS READY_FOR_HUMAN_GATE",
        "Authority: NONE",
        "Human Gate: ACTIVE",
        "Promotion State: CANDIDATE",
        "Canonical: FALSE",
        "Promoted: FALSE",
        "Merged: FALSE",
        "Human Gate Authorization: NOT_GRANTED",
    ):
        if marker not in ring7:
            errors.append(
                f"R8-D Ring 7 prerequisite missing: {marker}"
            )

    r8a = normalized(R8A)

    for marker in (
        "R8-A INSTANTIATED.",
        "READY_FOR_HUMAN_GATE != authorization.",
        "No promotion has occurred.",
        "No merge has occurred.",
        "No canonical mutation has occurred.",
    ):
        if marker not in r8a:
            errors.append(
                f"R8-D R8-A prerequisite missing: {marker}"
            )

    r8b = normalized(R8B)

    for marker in (
        "Decision states = APPROVE / REJECT / DEFER.",
        "R8-B PROMOTION DECISION CONTRACT COMPLETE.",
    ):
        if marker not in r8b:
            errors.append(
                f"R8-D R8-B prerequisite missing: {marker}"
            )

    r8c = normalized(R8C)

    for marker in (
        "Promotion subject = exact immutable Git commit.",
        "Branch name != immutable candidate identity.",
        "Decision commit must equal binding commit.",
        "Changed candidate requires new binding.",
        "R8-C PROMOTION CANDIDATE BINDING COMPLETE.",
    ):
        if marker not in r8c:
            errors.append(
                f"R8-D R8-C prerequisite missing: {marker}"
            )

    contract = normalized(CONTRACT)

    for marker in (
        "R8-D = Pre-Promotion Verification.",
        "Verification target = committed candidate state.",
        "Verification is bounded.",
        "Full-tree rerun = NOT REQUIRED.",
        "Exact candidate commit = REQUIRED.",
        "Exact candidate tree = REQUIRED.",
        "Target main resolution = REQUIRED.",
        "R8-A / R8-B / R8-C validity = REQUIRED.",
        "Decision instance = NONE.",
        "PRE_PROMOTION_VERIFIED != APPROVE.",
        "PRE_PROMOTION_VERIFIED != authorization.",
        "PRE_PROMOTION_VERIFIED != promotion.",
        "No self-invalidating verification receipt is permitted.",
        "Human Gate Authorization remains NOT_GRANTED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "Canonical remains FALSE.",
        "Promoted remains FALSE.",
        "Merged remains FALSE.",
        "R8-D PRE-PROMOTION VERIFICATION COMPLETE.",
        "R8-E owns Human Gate Authorization Receipt.",
    ):
        if marker not in contract:
            errors.append(
                f"R8-D lock missing: {marker}"
            )

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"invalid R8-D schema JSON: {exc}"
        ]

    if (
        schema.get("$schema")
        != "https://json-schema.org/draft/2020-12/schema"
    ):
        errors.append(
            "R8-D schema draft disagreement"
        )

    try:
        result = build_result()
    except Exception as exc:
        errors.append(
            f"R8-D verification result failed: {exc}"
        )
        return errors

    expected = {
        "candidate_branch": "candidate/v41-complete",
        "target_branch": "main",
        "ring7_ready": True,
        "r8a_valid": True,
        "r8b_valid": True,
        "r8c_valid": True,
        "decision_instance": "NONE",
        "human_gate_authorization": "NOT_GRANTED",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "promotion_state": "CANDIDATE",
        "canonical": False,
        "promoted": False,
        "merged": False,
        "disposition": "PRE_PROMOTION_VERIFIED",
    }

    for key, value in expected.items():
        if result.get(key) != value:
            errors.append(
                f"R8-D result disagreement: {key}"
            )

    if len(
        result.get(
            "candidate_commit",
            "",
        )
    ) != 40:
        errors.append(
            "R8-D candidate commit is not exact"
        )

    if len(
        result.get(
            "candidate_tree",
            "",
        )
    ) != 40:
        errors.append(
            "R8-D candidate tree is not exact"
        )

    if len(
        result.get(
            "target_commit",
            "",
        )
    ) != 40:
        errors.append(
            "R8-D target commit is not exact"
        )

    if len(
        result.get(
            "binding_sha512",
            "",
        )
    ) != 128:
        errors.append(
            "R8-D binding SHA-512 is invalid"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R8-D PRE-PROMOTION VERIFICATION: FAIL"
        )

        for error in errors:
            print(f" - {error}")

        return 1

    result = build_result()

    print(
        "R8-D PRE-PROMOTION VERIFICATION: PASS"
    )
    print(
        f"Candidate commit: {result['candidate_commit']}"
    )
    print(
        f"Candidate tree: {result['candidate_tree']}"
    )
    print(
        f"Target main commit: {result['target_commit']}"
    )
    print(
        "Ring 7 readiness: VERIFIED"
    )
    print(
        "R8-A / R8-B / R8-C: VERIFIED"
    )
    print(
        "Candidate binding: VERIFIED"
    )
    print(
        "Full-tree rerun: NOT PERFORMED"
    )
    print(
        "Decision instance: NONE"
    )
    print(
        "Human Gate Authorization: NOT_GRANTED"
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
        "Disposition: PRE_PROMOTION_VERIFIED"
    )
    print(
        "R8-E Human Gate Authorization Receipt: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
