#!/usr/bin/env python3

from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "contracts/promotion/STABILITY_RECEIPT.md"
SCHEMA = ROOT / "schemas/promotion/stability_receipt.schema.json"
RECEIPT = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"
VERSION = ROOT / "VERSION"
VERSION_JSON = ROOT / "VERSION.json"
R6 = ROOT / "contracts/validation/RING6_AGGREGATE_AUDIT_CLOSURE.md"
R7I = ROOT / "receipts/promotion/R7_I_TRANSITION_RECEIPT.json"


def norm(path):
    text = path.read_text(encoding="utf-8")

    for token in ("**", "__", "`"):
        text = text.replace(token, "")

    return " ".join(text.split())


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def validate():
    errors = []

    for path in (
        CONTRACT,
        SCHEMA,
        RECEIPT,
        VERSION,
        VERSION_JSON,
        R6,
        R7I,
    ):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    receipt = json.loads(
        RECEIPT.read_text(encoding="utf-8")
    )

    schema = json.loads(
        SCHEMA.read_text(encoding="utf-8")
    )

    version_json = json.loads(
        VERSION_JSON.read_text(encoding="utf-8")
    )

    transition = json.loads(
        R7I.read_text(encoding="utf-8")
    )

    baseline = receipt.get(
        "baseline_commit",
        "",
    )

    if not re.fullmatch(
        r"[0-9a-f]{40}",
        baseline,
    ):
        errors.append(
            "invalid stability baseline commit"
        )
    else:
        try:
            git(
                "cat-file",
                "-e",
                f"{baseline}^{{commit}}",
            )
        except subprocess.CalledProcessError:
            errors.append(
                "stability baseline commit not present in Git"
            )

    if VERSION.read_text(
        encoding="utf-8"
    ).strip() != "vTemporal.41.0":
        errors.append(
            "VERSION disagreement"
        )

    if version_json.get(
        "version"
    ) != "vTemporal.41.0":
        errors.append(
            "VERSION.json disagreement"
        )

    if version_json.get(
        "promotion_state"
    ) != "CANDIDATE":
        errors.append(
            "promotion state disagreement"
        )

    if version_json.get(
        "canonical"
    ) is not False:
        errors.append(
            "candidate falsely canonical"
        )

    if transition.get(
        "transition_disposition"
    ) != "ACCOUNTED":
        errors.append(
            "R7-I transition is not ACCOUNTED"
        )

    if transition.get(
        "future_transition",
        {},
    ).get(
        "performed"
    ) is not False:
        errors.append(
            "R7-I future promotion already performed"
        )

    if "VALIDATED_CANDIDATE" not in norm(R6):
        errors.append(
            "Ring 6 validated-candidate evidence missing"
        )

    expected = {
        "schema_version":
            "1.0",

        "receipt_type":
            "STABILITY_RECEIPT",

        "ring":
            "R7-J",

        "baseline_branch":
            "candidate/v41-complete",

        "native_version":
            "vTemporal.41.0",

        "implementation_identity":
            "v41 Complete",

        "ring6_state":
            "VALIDATED_CANDIDATE",

        "transition_state":
            "ACCOUNTED",

        "documentation_freeze":
            True,

        "authority_state":
            "NONE",

        "human_gate_state":
            "ACTIVE",

        "promotion_state":
            "CANDIDATE",

        "disposition":
            "STABLE_BASELINE",
    }

    for key, expected_value in expected.items():
        if receipt.get(key) != expected_value:
            errors.append(
                f"receipt disagreement: {key}"
            )

    runtime = receipt.get(
        "runtime_assumptions",
        {},
    )

    if runtime.get(
        "external_runtime"
    ) != "DISABLED":
        errors.append(
            "external runtime assumption drift"
        )

    if runtime.get(
        "external_action"
    ) != "DISABLED":
        errors.append(
            "external action assumption drift"
        )

    if runtime.get(
        "system_population"
    ) != "DISALLOWED":
        errors.append(
            "system population assumption drift"
        )

    if runtime.get(
        "canonical_mutation"
    ) != "HUMAN_GATE_ONLY":
        errors.append(
            "canonical mutation boundary drift"
        )

    if not receipt.get(
        "known_conditions"
    ):
        errors.append(
            "known conditions not preserved"
        )

    if not receipt.get(
        "provenance"
    ):
        errors.append(
            "stability provenance missing"
        )

    if schema.get(
        "$schema"
    ) != "https://json-schema.org/draft/2020-12/schema":
        errors.append(
            "schema draft disagreement"
        )

    contract = norm(
        CONTRACT
    )

    for marker in (
        "R7-J = Stability Receipt.",
        "Implementation freeze precedes final documentation.",
        "Implementation leads.",
        "Documentation follows.",
        "Substantive implementation change requires stability revalidation.",
        "Stability != completeness.",
        "Stability != promotion.",
        "Receipt != authority.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "R7-D through R7-H may now complete against the stabilized baseline.",
    ):
        if marker not in contract:
            errors.append(
                f"stability contract lock missing: {marker}"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R7-J STABILITY RECEIPT: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    receipt = json.loads(
        RECEIPT.read_text(encoding="utf-8")
    )

    print(
        "R7-J STABILITY RECEIPT: PASS"
    )
    print(
        f"Baseline commit: {receipt['baseline_commit']}"
    )
    print(
        "Baseline branch: candidate/v41-complete"
    )
    print(
        "Native version: vTemporal.41.0"
    )
    print(
        "Ring 6: VALIDATED_CANDIDATE"
    )
    print(
        "Transition accounting: ACCOUNTED"
    )
    print(
        "Documentation freeze: ESTABLISHED"
    )
    print(
        "Known conditions: PRESERVED"
    )
    print(
        "Runtime assumptions: BOUNDED"
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
        "STABILITY VALIDATED"
    )
    print(
        "R7-D through R7-H: RELEASED FOR FINAL DOCUMENTATION"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
