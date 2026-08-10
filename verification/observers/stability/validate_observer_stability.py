#!/usr/bin/env python3

from pathlib import Path

import subprocess

import sys

import os

import json

import hashlib

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

CAP_ROOT = (

    ROOT

    / "canonical/observers/capabilities"

)

INDEX = (

    ROOT

    / "verification/observers/stability/"

      "OBSERVER_STABILITY_REGRESSION_INDEX.json"

)

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

OR15 = (

    ROOT

    / "verification/observers/ac_revalidation/"

      "AC01_AC12_OBSERVER_REVALIDATION.json"

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

def canonical_bytes(value):

    return json.dumps(

        value,

        ensure_ascii=False,

        sort_keys=True,

        separators=(",", ":")

    ).encode("utf-8")

def sha_bytes(data):

    return hashlib.sha512(

        data

    ).hexdigest()

def sha(path):

    return hashlib.sha512(

        path.read_bytes()

    ).hexdigest()

def load(path):

    return json.loads(

        path.read_text(

            encoding="utf-8"

        )

    )

def fail(message):

    print(

        "OR-16 STABILITY VALIDATOR: FAIL"

    )

    print(

        message

    )

    return 1

def main():

    # --------------------------------------------------------

    # 1. Tracked implementation state must equal HEAD.

    # OR-16's own files may be untracked during first run.

    # --------------------------------------------------------

    if run(

        [

            "git",

            "diff",

            "--quiet"

        ]

    ).returncode != 0:

        return fail(

            "Tracked unstaged state differs from HEAD."

        )

    if run(

        [

            "git",

            "diff",

            "--cached",

            "--quiet"

        ]

    ).returncode != 0:

        return fail(

            "Tracked staged state differs from HEAD."

        )

    if not INDEX.exists():

        return fail(

            "OR-16 stability index missing."

        )

    index = load(

        INDEX

    )

    if (

        index.get(

            "authority"

        )

        != "NONE"

    ):

        return fail(

            "Authority NONE lost."

        )

    if (

        index.get(

            "human_gate"

        )

        != "ACTIVE"

    ):

        return fail(

            "Human Gate ACTIVE lost."

        )

    if (

        index.get(

            "canonical_status"

        )

        != "CANDIDATE_NOT_PROMOTED"

    ):

        return fail(

            "Candidate state lost."

        )

    # --------------------------------------------------------

    # 2. Load exact ten source contracts.

    # --------------------------------------------------------

    live = {}

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

        if not oid:

            return fail(

                "Capability missing observer_id."

            )

        if oid in live:

            return fail(

                "Duplicate Observer identity: "

                + oid

            )

        live[

            oid

        ] = {

            "path":

                path,

            "contract":

                obj

        }

    if set(

        live

    ) != ALL:

        return fail(

            "Observer identity set mismatch."

        )

    # --------------------------------------------------------

    # 3. Rebuild deterministic collapse.

    # --------------------------------------------------------

    observers = []

    for oid in sorted(

        ALL

    ):

        path = live[

            oid

        ]["path"]

        observers.append({

            "observer_id":

                oid,

            "source_path":

                str(

                    path.relative_to(

                        ROOT

                    )

                ),

            "source_sha512":

                sha(path),

            "contract":

                live[

                    oid

                ]["contract"]

        })

    collapse = {

        "collapse_type":

            "ZERVAN_V41_LOSSLESS_OBSERVER_COLLAPSE",

        "collapse_version":

            "1.0",

        "observer_count":

            10,

        "primary_count":

            7,

        "controlled_count":

            3,

        "observers":

            observers

    }

    expected = index.get(

        "lossless_collapse"

    )

    if collapse != expected:

        return fail(

            "Live collapse differs from OR-16 snapshot."

        )

    actual_sha = sha_bytes(

        canonical_bytes(

            collapse

        )

    )

    if (

        actual_sha

        != index.get(

            "lossless_collapse_sha512"

        )

    ):

        return fail(

            "Lossless collapse SHA-512 mismatch."

        )

    # --------------------------------------------------------

    # 4. Reconstruct every full contract.

    # --------------------------------------------------------

    reconstructed = {

        entry[

            "observer_id"

        ]:

            entry[

                "contract"

            ]

        for entry in collapse[

            "observers"

        ]

    }

    if set(

        reconstructed

    ) != ALL:

        return fail(

            "Reconstructed identity set mismatch."

        )

    for oid in ALL:

        if (

            reconstructed[

                oid

            ]

            != live[

                oid

            ][

                "contract"

            ]

        ):

            return fail(

                oid

                + ": reconstructed contract differs from source."

            )

    # --------------------------------------------------------

    # 5. Re-execute OR-15 AC test surface.

    # --------------------------------------------------------

    or15 = load(

        OR15

    )

    ac_tests = or15.get(

        "test_results",

        {}

    )

    if not ac_tests:

        return fail(

            "OR-15 test surface missing."

        )

    total_tests = 0

    for relpath in sorted(

        ac_tests

    ):

        path = ROOT / relpath

        if not path.exists():

            return fail(

                "OR-15 test file missing: "

                + relpath

            )

        command = [

            sys.executable,

            "-m",

            "unittest",

            "discover",

            "-s",

            str(

                path.parent.relative_to(

                    ROOT

                )

            ),

            "-p",

            path.name,

            "-v"

        ]

        result = run(

            command

        )

        if result.returncode != 0:

            return fail(

                "AC regression failed: "

                + relpath

                + "\n"

                + result.stdout

                + "\n"

                + result.stderr

            )

        combined = (

            result.stdout

            + "\n"

            + result.stderr

        )

        import re

        match = re.search(

            r"Ran\s+(\d+)\s+tests?",

            combined

        )

        if match is None:

            return fail(

                "Unable to establish test count: "

                + relpath

            )

        count = int(

            match.group(1)

        )

        if count < 1:

            return fail(

                "Zero tests executed: "

                + relpath

            )

        total_tests += count

    # --------------------------------------------------------

    # 6. Re-execute Observer validation chain.

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

    ]

    for command, marker in checks:

        result = run(

            command

        )

        if result.returncode != 0:

            return fail(

                "Observer regression command failed:\n"

                + result.stdout

                + "\n"

                + result.stderr

            )

        combined = (

            result.stdout

            + "\n"

            + result.stderr

        )

        if marker not in combined:

            return fail(

                "Expected regression marker missing: "

                + marker

            )

    print(

        "OR-16 STABILITY VALIDATOR: PASS"

    )

    print(

        "OBSERVER INVENTORY: 10/10 PASS"

    )

    print(

        "LOSSLESS RECONSTRUCTION: 10/10 PASS"

    )

    print(

        "COLLAPSE SHA-512: PASS"

    )

    print(

        "AC UNITTEST EXECUTIONS:",

        total_tests,

        "PASS"

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

    sys.exit(

        main()

    )
