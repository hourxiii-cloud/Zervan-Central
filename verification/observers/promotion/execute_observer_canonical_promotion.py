#!/usr/bin/env python3

from pathlib import Path

import subprocess

import sys

import os

import json

import hashlib

ROOT = Path(__file__).resolve().parents[3]

BRANCH = "candidate/v41-observer-restoration"

CANONICAL_BRANCH = "main"

HERE = Path(__file__).resolve().parent

CONTRACT = (

    HERE

    / "OBSERVER_CANONICAL_PROMOTION_CONTRACT.json"

)

CAP_ROOT = (

    ROOT

    / "canonical/observers/capabilities"

)

PRIMARY = {

    "eagle",

    "mole",

    "duck",

    "wildflower",

    "mockingbird",

    "platypus",

    "owl_hoot",

}

CONTROLLED = {

    "osprey",

    "animal_kingdom",

    "armadillo",

}

ALL = PRIMARY | CONTROLLED

ENV = os.environ.copy()

existing = ENV.get(

    "PYTHONPATH",

    ""

)

ENV["PYTHONPATH"] = (

    str(ROOT)

    + (

        os.pathsep + existing

        if existing

        else ""

    )

)

ENV["PYTHONDONTWRITEBYTECODE"] = "1"

def run(command):

    return subprocess.run(

        command,

        cwd=ROOT,

        env=ENV,

        text=True,

        stdout=subprocess.PIPE,

        stderr=subprocess.PIPE

    )

def git(*args):

    p = run(

        ["git", *args]

    )

    if p.returncode:

        raise RuntimeError(

            p.stderr.strip()

            or p.stdout.strip()

        )

    return p.stdout.strip()

def load(path):

    return json.loads(

        path.read_text(

            encoding="utf-8"

        )

    )

def fail(message):

    print()

    print("=== OR-18 PROMOTION BLOCKED ===")

    print(message)

    return 1

def main():

    approval_path = os.environ.get(

        "ZERVAN_OR18_APPROVAL_FILE"

    )

    if not approval_path:

        return fail(

            "Explicit approval file not supplied."

        )

    approval_file = Path(

        approval_path

    )

    if not approval_file.exists():

        return fail(

            "Explicit approval file does not exist."

        )

    if not CONTRACT.exists():

        return fail(

            "OR-18 promotion contract missing."

        )

    contract = load(

        CONTRACT

    )

    approval = load(

        approval_file

    )

    branch = git(

        "branch",

        "--show-current"

    )

    approved_head = git(

        "rev-parse",

        "HEAD"

    )

    if branch != BRANCH:

        return fail(

            "Promotion must begin on exact candidate branch."

        )

    if git(

        "status",

        "--porcelain"

    ):

        return fail(

            "Working tree must be completely clean before promotion."

        )

    required = {

        "approval_type":

            "ZERVAN_V41_OBSERVER_HUMAN_GATE_APPROVAL",

        "decision":

            "APPROVE_CANONICAL_PROMOTION",

        "restoration_target":

            "V41_OBSERVER_RESTORATION",

        "candidate_branch":

            BRANCH,

        "candidate_head":

            approved_head,

        "canonical_destination":

            CANONICAL_BRANCH,

        "promotion_stage":

            "OR-18",

        "single_use":

            True,

        "consumed":

            False,

        "authority":

            "NONE",

        "human_gate":

            "ACTIVE"

    }

    for key, expected in required.items():

        if approval.get(key) != expected:

            return fail(

                "Approval mismatch: "

                + key

            )

    if (

        approval.get(

            "promotion_contract_sha512"

        )

        != hashlib.sha512(

            CONTRACT.read_bytes()

        ).hexdigest()

    ):

        return fail(

            "Approval does not bind exact OR-18 contract."

        )

    # Exact ten-Observer boundary before movement.

    caps = {}

    for path in sorted(

        CAP_ROOT.glob(

            "*_CAPABILITY.json"

        )

    ):

        obj = load(

            path

        )

        oid = obj.get(

            "observer_id"

        )

        if oid:

            caps[

                oid

            ] = obj

    if set(caps) != ALL:

        return fail(

            "Ten-Observer inventory incomplete."

        )

    if any(

        caps[oid].get(

            "operating_class"

        )

        != "PRIMARY"

        for oid in PRIMARY

    ):

        return fail(

            "Primary Observer boundary failed."

        )

    if any(

        caps[oid].get(

            "operating_class"

        )

        != "CONTROLLED_SUB_OBSERVER"

        for oid in CONTROLLED

    ):

        return fail(

            "Controlled Observer boundary failed."

        )

    owl = caps[

        "owl_hoot"

    ]

    if (

        owl.get(

            "canonical_seat"

        )

        != "PRIMARY_OBSERVER"

    ):

        return fail(

            "Owl_Hoot Primary seat lost."

        )

    if (

        "BOUNDED_SUB_OBSERVER"

        not in owl.get(

            "supported_modes",

            []

        )

    ):

        return fail(

            "Owl_Hoot bounded mode lost."

        )

    # Synchronize remote canonical knowledge.

    fetch = run(

        [

            "git",

            "fetch",

            "origin",

            CANONICAL_BRANCH

        ]

    )

    if fetch.returncode:

        return fail(

            "Unable to fetch origin/main:\n"

            + fetch.stdout

            + fetch.stderr

        )

    origin_main = git(

        "rev-parse",

        "origin/" + CANONICAL_BRANCH

    )

    ancestry = run(

        [

            "git",

            "merge-base",

            "--is-ancestor",

            origin_main,

            approved_head

        ]

    )

    if ancestry.returncode != 0:

        return fail(

            "origin/main is not an ancestor of approved candidate HEAD. "

            "Fast-forward promotion is impossible."

        )

    local_main_check = run(

        [

            "git",

            "show-ref",

            "--verify",

            "--quiet",

            "refs/heads/" + CANONICAL_BRANCH

        ]

    )

    if local_main_check.returncode == 0:

        local_main = git(

            "rev-parse",

            CANONICAL_BRANCH

        )

        local_relation = run(

            [

                "git",

                "merge-base",

                "--is-ancestor",

                local_main,

                approved_head

            ]

        )

        if local_relation.returncode != 0:

            return fail(

                "Local main is not an ancestor of approved candidate HEAD."

            )

    checkout = run(

        [

            "git",

            "checkout",

            CANONICAL_BRANCH

        ]

    )

    if checkout.returncode:

        return fail(

            "Unable to checkout main:\n"

            + checkout.stdout

            + checkout.stderr

        )

    if git(

        "status",

        "--porcelain"

    ):

        return fail(

            "main is dirty after checkout."

        )

    # First synchronize local main to origin/main.

    sync = run(

        [

            "git",

            "merge",

            "--ff-only",

            "origin/" + CANONICAL_BRANCH

        ]

    )

    if sync.returncode:

        return fail(

            "Unable to synchronize local main to origin/main:\n"

            + sync.stdout

            + sync.stderr

        )

    main_before = git(

        "rev-parse",

        "HEAD"

    )

    promote = run(

        [

            "git",

            "merge",

            "--ff-only",

            approved_head

        ]

    )

    if promote.returncode:

        return fail(

            "Fast-forward promotion failed:\n"

            + promote.stdout

            + promote.stderr

        )

    promoted_head = git(

        "rev-parse",

        "HEAD"

    )

    if promoted_head != approved_head:

        return fail(

            "Local canonical HEAD differs from approved HEAD."

        )

    if git(

        "status",

        "--porcelain"

    ):

        return fail(

            "Canonical tree dirty after fast-forward."

        )

    push = run(

        [

            "git",

            "push",

            "origin",

            CANONICAL_BRANCH

        ]

    )

    if push.returncode:

        return fail(

            "Canonical push failed:\n"

            + push.stdout

            + push.stderr

        )

    verify_fetch = run(

        [

            "git",

            "fetch",

            "origin",

            CANONICAL_BRANCH

        ]

    )

    if verify_fetch.returncode:

        return fail(

            "Unable to verify origin/main after push."

        )

    remote_head = git(

        "rev-parse",

        "origin/" + CANONICAL_BRANCH

    )

    if remote_head != approved_head:

        return fail(

            "origin/main does not equal approved promotion HEAD."

        )

    print()

    print(

        "=== OR-18 CANONICAL PROMOTION COMPLETE ==="

    )

    print(

        "Previous canonical HEAD:",

        main_before

    )

    print(

        "Approved promotion HEAD:",

        approved_head

    )

    print(

        "Local main HEAD:",

        promoted_head

    )

    print(

        "origin/main HEAD:",

        remote_head

    )

    print(

        "Promotion mode: FAST-FORWARD ONLY"

    )

    print(

        "Ten Observers: 10/10 PRESENT"

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

        "NEXT: OR-19 — POST-PROMOTION INDEPENDENT VERIFICATION"

    )

    return 0

if __name__ == "__main__":

    sys.exit(

        main()

    )
