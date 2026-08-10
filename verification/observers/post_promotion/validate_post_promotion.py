#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import os
import json
import hashlib
import re

ROOT = Path(__file__).resolve().parents[3]

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

CAP_ROOT = "canonical/observers/capabilities"

OR10 = (
    ROOT
    / "tests/observers/functional/"
      "run_observer_functional_tests.py"
)

OR11 = (
    ROOT
    / "tools/observers/completeness/"
      "validate_observer_restoration.py"
)

OR12 = (
    ROOT
    / "verification/observers/fresh_reader/"
      "validate_fresh_reader.py"
)

OR16 = (
    ROOT
    / "verification/observers/stability/"
      "validate_observer_stability.py"
)

OR18_CONTRACT = (
    "verification/observers/promotion/"
    "OBSERVER_CANONICAL_PROMOTION_CONTRACT.json"
)

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


def head_text(path):
    return git(
        "show",
        "HEAD:" + path
    )


def head_json(path):
    return json.loads(
        head_text(path)
    )


def fail(message):
    print(
        "OR-19 POST-PROMOTION VALIDATOR: FAIL"
    )
    print(
        message
    )
    return 1


def main():
    tests = []

    # 1. Canonical branch is main.
    tests.append(
        git(
            "branch",
            "--show-current"
        )
        == "main"
    )

    # 2. Tracked state equals HEAD.
    tests.append(
        run(
            [
                "git",
                "diff",
                "--quiet"
            ]
        ).returncode == 0
    )

    # 3. No staged delta.
    tests.append(
        run(
            [
                "git",
                "diff",
                "--cached",
                "--quiet"
            ]
        ).returncode == 0
    )

    # 4. Refresh origin/main.
    fetch = run(
        [
            "git",
            "fetch",
            "origin",
            "main"
        ]
    )

    tests.append(
        fetch.returncode == 0
    )

    local_head = git(
        "rev-parse",
        "HEAD"
    )

    remote_head = git(
        "rev-parse",
        "origin/main"
    )

    # 5. Local main == public canonical origin/main.
    tests.append(
        local_head == remote_head
    )

    # 6. OR-18 promotion control is current HEAD.
    subject = git(
        "log",
        "-1",
        "--format=%s"
    )

    tests.append(
        "OR-18" in subject
        and "Observer canonical promotion control"
        in subject
    )

    # 7. OR-18 contract reconstructs from HEAD.
    try:
        promotion = head_json(
            OR18_CONTRACT
        )
        tests.append(True)
    except Exception:
        promotion = {}
        tests.append(False)

    # 8. Authority remains NONE.
    tests.append(
        promotion.get(
            "authority"
        )
        == "NONE"
    )

    # 9. Human Gate remains ACTIVE.
    tests.append(
        promotion.get(
            "human_gate"
        )
        == "ACTIVE"
    )

    # 10. Human Gate approval was explicit.
    tests.append(
        promotion.get(
            "human_gate_decision"
        )
        == "EXPLICIT_APPROVAL_RECEIVED_2026-08-10"
    )

    # 11. Promotion destination was main.
    tests.append(
        promotion.get(
            "approval_scope",
            {}
        ).get(
            "canonical_destination"
        )
        == "main"
    )

    # 12. Promotion mode was FF-only.
    tests.append(
        promotion.get(
            "approval_scope",
            {}
        ).get(
            "promotion_mode"
        )
        == "FAST_FORWARD_ONLY"
    )

    # 13. Approval was single-use.
    tests.append(
        promotion.get(
            "approval_scope",
            {}
        ).get(
            "single_use"
        )
        is True
    )

    # --------------------------------------------------------
    # Reconstruct ten capabilities from HEAD only.
    # --------------------------------------------------------

    listing = git(
        "ls-tree",
        "-r",
        "--name-only",
        "HEAD",
        CAP_ROOT
    )

    paths = sorted(
        line.strip()
        for line in listing.splitlines()
        if line.strip().endswith(
            "_CAPABILITY.json"
        )
    )

    # 14. Exactly ten capability contracts.
    tests.append(
        len(paths) == 10
    )

    capabilities = {}

    try:
        for path in paths:
            obj = head_json(
                path
            )

            oid = obj[
                "observer_id"
            ]

            if oid in capabilities:
                raise RuntimeError(
                    "duplicate observer_id"
                )

            capabilities[
                oid
            ] = obj

        cap_ok = True

    except Exception:
        capabilities = {}
        cap_ok = False

    # 15. Exact identity set.
    tests.append(
        cap_ok
        and set(
            capabilities
        )
        == ALL
    )

    # 16. Seven Primary classes.
    tests.append(
        cap_ok
        and all(
            capabilities[
                oid
            ].get(
                "operating_class"
            )
            == "PRIMARY"
            for oid in PRIMARY
        )
    )

    # 17. Seven Primary seats.
    tests.append(
        cap_ok
        and all(
            capabilities[
                oid
            ].get(
                "canonical_seat"
            )
            == "PRIMARY_OBSERVER"
            for oid in PRIMARY
        )
    )

    # 18. Three controlled classes.
    tests.append(
        cap_ok
        and all(
            capabilities[
                oid
            ].get(
                "operating_class"
            )
            == "CONTROLLED_SUB_OBSERVER"
            for oid in CONTROLLED
        )
    )

    # 19. Three controlled seats.
    tests.append(
        cap_ok
        and all(
            capabilities[
                oid
            ].get(
                "canonical_seat"
            )
            == "CONTROLLED_SUB_OBSERVER"
            for oid in CONTROLLED
        )
    )

    # 20. Owl_Hoot remains Primary.
    tests.append(
        cap_ok
        and capabilities[
            "owl_hoot"
        ].get(
            "canonical_seat"
        )
        == "PRIMARY_OBSERVER"
    )

    # 21. Owl_Hoot bounded mode survives promotion.
    tests.append(
        cap_ok
        and "BOUNDED_SUB_OBSERVER"
        in capabilities[
            "owl_hoot"
        ].get(
            "supported_modes",
            []
        )
    )

    # 22. Ten distinctive invariants survive.
    tests.append(
        cap_ok
        and all(
            bool(
                capabilities[
                    oid
                ].get(
                    "distinctive_invariant"
                )
            )
            for oid in ALL
        )
    )

    # --------------------------------------------------------
    # 23-26. Execute regression chain from promoted main.
    # --------------------------------------------------------

    checks = [
        (
            [
                sys.executable,
                str(OR10)
            ],
            "120/120"
        ),
        (
            [
                sys.executable,
                str(OR11)
            ],
            "30/30"
        ),
        (
            [
                sys.executable,
                str(OR12)
            ],
            "20/20"
        ),
        (
            [
                sys.executable,
                str(OR16)
            ],
            "OR-16 STABILITY VALIDATOR: PASS"
        ),
    ]

    for command, marker in checks:
        result = run(
            command
        )

        combined = (
            result.stdout
            + "\n"
            + result.stderr
        )

        tests.append(
            result.returncode == 0
            and marker in combined
        )

    # 27. External runtime remains disabled.
    tests.append(
        promotion.get(
            "external_runtime"
        )
        == "DISABLED"
    )

    # 28. External action remains disabled.
    tests.append(
        promotion.get(
            "external_action"
        )
        == "DISABLED"
    )

    # 29. Promotion contains no authority escalation.
    invariants = set(
        promotion.get(
            "promotion_invariants",
            []
        )
    )

    tests.append(
        "AUTHORITY_REMAINS_NONE"
        in invariants
    )

    # 30. Promotion contains Human Gate preservation.
    tests.append(
        "HUMAN_GATE_REMAINS_ACTIVE"
        in invariants
    )

    if not all(
        tests
    ):
        failed = [
            i + 1
            for i, ok in enumerate(
                tests
            )
            if not ok
        ]

        return fail(
            "Failed controls: "
            + repr(
                failed
            )
        )

    print(
        "OR-19 POST-PROMOTION VALIDATOR: 30/30 PASS"
    )
    print(
        "LOCAL MAIN == ORIGIN/MAIN: PASS"
    )
    print(
        "PROMOTED HEAD:",
        local_head
    )
    print(
        "PRIMARY OBSERVERS: 7/7 PASS"
    )
    print(
        "CONTROLLED SUB-OBSERVERS: 3/3 PASS"
    )
    print(
        "TOTAL OBSERVERS: 10/10 PASS"
    )
    print(
        "OWL_HOOT PRIMARY SEAT: PASS"
    )
    print(
        "OWL_HOOT BOUNDED MODE: PASS"
    )
    print(
        "DISTINCTIVE INVARIANTS: 10/10 PASS"
    )
    print(
        "OR-10: 120/120 PASS"
    )
    print(
        "OR-11: 30/30 PASS"
    )
    print(
        "OR-12: 20/20 PASS"
    )
    print(
        "OR-16 STABILITY: PASS"
    )
    print(
        "AUTHORITY: NONE"
    )
    print(
        "HUMAN GATE: ACTIVE"
    )
    print(
        "EXTERNAL RUNTIME: DISABLED"
    )
    print(
        "EXTERNAL ACTION: DISABLED"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
