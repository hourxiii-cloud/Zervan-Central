#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REPOSITORY = "hourxiii-cloud/Zervan-Central"
CANDIDATE_BRANCH = "candidate/v41-complete"
TARGET_BRANCH = "main"

RING7_PATH = (
    "contracts/validation/"
    "RING7_AGGREGATE_DOCUMENTATION_PROMOTION_READINESS_CLOSURE.md"
)
R8A_PATH = (
    "contracts/promotion/"
    "RING8_HUMAN_GATE_PROMOTION_BOUNDARY.md"
)
R8B_PATH = (
    "contracts/promotion/"
    "PROMOTION_DECISION_CONTRACT.md"
)


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def resolve(ref="HEAD"):
    commit = git(
        "rev-parse",
        f"{ref}^{{commit}}",
    )

    tree = git(
        "rev-parse",
        f"{commit}^{{tree}}",
    )

    def blob(path):
        return git(
            "rev-parse",
            f"{commit}:{path}",
        )

    payload = {
        "schema_version": "1.0",
        "record_type": "PROMOTION_CANDIDATE_BINDING",
        "ring": "R8-C",
        "native_version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "repository": REPOSITORY,
        "candidate_branch": CANDIDATE_BRANCH,
        "candidate_commit": commit,
        "candidate_tree": tree,
        "target_branch": TARGET_BRANCH,
        "ring7_closure_path": RING7_PATH,
        "ring7_closure_blob": blob(RING7_PATH),
        "r8a_boundary_path": R8A_PATH,
        "r8a_boundary_blob": blob(R8A_PATH),
        "r8b_decision_contract_path": R8B_PATH,
        "r8b_decision_contract_blob": blob(R8B_PATH),
        "binding_serialization": "JSON_SORTED_KEYS_COMPACT_UTF8",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
    }

    serialized = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    payload["binding_sha512"] = hashlib.sha512(
        serialized
    ).hexdigest()

    return payload


def main():
    ref = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "HEAD"
    )

    try:
        binding = resolve(ref)
    except subprocess.CalledProcessError as exc:
        print(
            "R8-C PROMOTION CANDIDATE BINDING RESOLUTION: FAIL",
            file=sys.stderr,
        )
        return exc.returncode or 1

    print(
        json.dumps(
            binding,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
