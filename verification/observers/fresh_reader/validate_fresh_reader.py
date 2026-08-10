#!/usr/bin/env python3

from pathlib import Path

import subprocess

import hashlib

import json

import sys

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

OR11_INDEX = (

    "tools/observers/completeness/"

    "OBSERVER_RESTORATION_COMPLETENESS_INDEX.json"

)

OR0 = (

    "canonical/observers/"

    "OBSERVER_RECOVERY_INVENTORY.md"

)

OR1 = (

    "canonical/observers/"

    "OBSERVER_CONTRACT_V41.md"

)

CAP_ROOT = "canonical/observers/capabilities"

def git(*args, text=True):

    return subprocess.run(

        ["git", *args],

        cwd=ROOT,

        text=text,

        stdout=subprocess.PIPE,

        stderr=subprocess.PIPE

    )

def require_git(*args):

    p = git(*args)

    if p.returncode:

        raise RuntimeError(

            p.stderr.strip()

            or p.stdout.strip()

        )

    return p.stdout

def head_text(path):

    return require_git(

        "show",

        "HEAD:" + path

    )

def head_bytes(path):

    p = git(

        "show",

        "HEAD:" + path,

        text=False

    )

    if p.returncode:

        raise RuntimeError(

            p.stderr.decode(

                "utf-8",

                errors="replace"

            )

        )

    return p.stdout

def head_json(path):

    return json.loads(

        head_text(path)

    )

def head_sha512(path):

    return hashlib.sha512(

        head_bytes(path)

    ).hexdigest()

def main():

    tests = []

    # --------------------------------------------------------

    # 1. Tracked working state equals committed HEAD.

    #

    # Untracked OR-12 artifacts are intentionally allowed.

    # Reconstruction must not depend on them.

    # --------------------------------------------------------

    unstaged = git(

        "diff",

        "--quiet"

    )

    staged = git(

        "diff",

        "--cached",

        "--quiet"

    )

    tests.append(

        unstaged.returncode == 0

        and staged.returncode == 0

    )

    # --------------------------------------------------------

    # 2. OR-11 completeness index reads from HEAD.

    # --------------------------------------------------------

    try:

        completeness = head_json(

            OR11_INDEX

        )

        tests.append(True)

    except Exception:

        completeness = {}

        tests.append(False)

    # 3. Candidate has not self-promoted.

    tests.append(

        completeness.get(

            "canonical_status"

        ) == "CANDIDATE_NOT_PROMOTED"

    )

    # 4. Authority reconstructs as NONE.

    tests.append(

        completeness.get(

            "authority"

        ) == "NONE"

    )

    # 5. Human Gate reconstructs as ACTIVE.

    tests.append(

        completeness.get(

            "human_gate"

        ) == "ACTIVE"

    )

    # 6. OR-0 exists at committed HEAD.

    try:

        tests.append(

            bool(

                head_text(OR0).strip()

            )

        )

    except Exception:

        tests.append(False)

    # 7. OR-1 exists at committed HEAD.

    try:

        tests.append(

            bool(

                head_text(OR1).strip()

            )

        )

    except Exception:

        tests.append(False)

    # --------------------------------------------------------

    # Discover capability contracts from HEAD only.

    # --------------------------------------------------------

    listing = require_git(

        "ls-tree",

        "-r",

        "--name-only",

        "HEAD",

        CAP_ROOT

    )

    cap_paths = sorted(

        line.strip()

        for line in listing.splitlines()

        if line.strip().endswith(

            "_CAPABILITY.json"

        )

    )

    # 8. Exactly ten capability contracts.

    tests.append(

        len(cap_paths) == 10

    )

    caps = {}

    try:

        for path in cap_paths:

            obj = head_json(path)

            oid = obj["observer_id"]

            if oid in caps:

                raise RuntimeError(

                    "duplicate observer_id"

                )

            caps[oid] = obj

        cap_load = True

    except Exception:

        caps = {}

        cap_load = False

    # 9. Exact ten identities.

    tests.append(

        cap_load

        and set(caps) == ALL

    )

    # 10. Seven Primary classes.

    tests.append(

        cap_load

        and all(

            caps[oid].get(

                "operating_class"

            ) == "PRIMARY"

            for oid in PRIMARY

        )

    )

    # 11. Seven Primary seats.

    tests.append(

        cap_load

        and all(

            caps[oid].get(

                "canonical_seat"

            ) == "PRIMARY_OBSERVER"

            for oid in PRIMARY

        )

    )

    # 12. Three controlled classes.

    tests.append(

        cap_load

        and all(

            caps[oid].get(

                "operating_class"

            )

            == "CONTROLLED_SUB_OBSERVER"

            for oid in CONTROLLED

        )

    )

    # 13. Three controlled seats.

    tests.append(

        cap_load

        and all(

            caps[oid].get(

                "canonical_seat"

            )

            == "CONTROLLED_SUB_OBSERVER"

            for oid in CONTROLLED

        )

    )

    # 14. Owl_Hoot remains Primary.

    tests.append(

        cap_load

        and caps[

            "owl_hoot"

        ].get(

            "canonical_seat"

        ) == "PRIMARY_OBSERVER"

    )

    # 15. Owl_Hoot bounded mode remains available.

    tests.append(

        cap_load

        and "BOUNDED_SUB_OBSERVER"

        in caps[

            "owl_hoot"

        ].get(

            "supported_modes",

            []

        )

    )

    # 16. Ten distinctive invariants.

    tests.append(

        cap_load

        and all(

            bool(

                caps[oid].get(

                    "distinctive_invariant"

                )

            )

            for oid in ALL

        )

    )

    # 17. Ten signal contracts.

    tests.append(

        cap_load

        and all(

            bool(

                caps[oid].get(

                    "signals"

                )

            )

            for oid in ALL

        )

    )

    # 18. Ten output contracts.

    tests.append(

        cap_load

        and all(

            bool(

                caps[oid].get(

                    "outputs"

                )

            )

            for oid in ALL

        )

    )

    # 19. OR-11 artifact manifest verifies against HEAD.

    manifest = completeness.get(

        "artifact_manifest",

        []

    )

    manifest_ok = bool(manifest)

    if manifest_ok:

        for entry in manifest:

            path = entry.get("path")

            expected = entry.get("sha512")

            try:

                actual = head_sha512(path)

            except Exception:

                manifest_ok = False

                break

            if actual != expected:

                manifest_ok = False

                break

    tests.append(

        manifest_ok

    )

    # 20. Entire OR-0 through OR-11 chain reconstructs.

    chain = completeness.get(

        "restoration_chain",

        {}

    )

    tests.append(

        set(chain)

        == {

            "OR-0",

            "OR-1",

            "OR-2",

            "OR-3",

            "OR-4",

            "OR-5",

            "OR-6",

            "OR-7",

            "OR-8",

            "OR-9",

            "OR-10",

            "OR-11",

        }

    )

    if not all(tests):

        failed = [

            i + 1

            for i, ok in enumerate(tests)

            if not ok

        ]

        print(

            "OR-12 FRESH-READER VALIDATION: FAIL",

            failed

        )

        return 1

    print(

        "OR-12 FRESH-READER VALIDATION: 20/20 PASS"

    )

    print(

        "SOURCE OF RECONSTRUCTION: COMMITTED HEAD ONLY"

    )

    print(

        "TRACKED WORKSPACE DEPENDENCY: NONE"

    )

    print(

        "PRIMARY OBSERVERS: 7/7 RECOVERED"

    )

    print(

        "CONTROLLED SUB-OBSERVERS: 3/3 RECOVERED"

    )

    print(

        "TOTAL OBSERVERS: 10/10 RECOVERED"

    )

    print(

        "DISTINCTIVE INVARIANTS: 10/10 RECOVERED"

    )

    print(

        "OWL_HOOT PRIMARY SEAT: RECOVERED"

    )

    print(

        "OWL_HOOT BOUNDED MODE: RECOVERED"

    )

    print(

        "OR-11 MANIFEST: VERIFIED AGAINST HEAD"

    )

    print(

        "AUTHORITY: NONE"

    )

    print(

        "HUMAN GATE: ACTIVE"

    )

    print(

        "CANONICAL PROMOTION: NOT PERFORMED"

    )

    return 0

if __name__ == "__main__":

    sys.exit(main())
