#!/usr/bin/env python3

from pathlib import Path
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]

R8B = ROOT / (
    "contracts/promotion/"
    "PROMOTION_DECISION_CONTRACT.md"
)
CONTRACT = ROOT / (
    "contracts/promotion/"
    "PROMOTION_CANDIDATE_BINDING.md"
)
SCHEMA = ROOT / (
    "schemas/promotion/"
    "promotion_candidate_binding.schema.json"
)
RESOLVER_PATH = ROOT / (
    "tools/"
    "resolve_promotion_candidate_binding.py"
)


def normalized(text):
    return " ".join(
        text.split()
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


def validate():
    errors = []

    for path in (
        R8B,
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

    r8b = normalized(
        R8B.read_text(
            encoding="utf-8"
        )
    )

    contract = normalized(
        CONTRACT.read_text(
            encoding="utf-8"
        )
    )

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"invalid R8-C schema JSON: {exc}"
        ]

    for marker in (
        "Candidate commit must be exact.",
        "The decision does not float with branch HEAD.",
        "Human Gate Authorization remains NOT_GRANTED.",
    ):
        if marker not in r8b:
            errors.append(
                f"R8-B prerequisite missing: {marker}"
            )

    for marker in (
        "R8-C = Promotion Candidate Binding.",
        "Promotion subject = exact immutable Git commit.",
        "Branch name != immutable candidate identity.",
        "Decision commit must equal binding commit.",
        "Changed candidate requires new binding.",
        "Binding != decision.",
        "Binding != authorization.",
        "Binding != execution.",
        "Hash != truth.",
        "Hash != authority.",
        "Hash != approval.",
        "No self-referential candidate binding is permitted.",
        "Human Gate Authorization remains NOT_GRANTED.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "Canonical remains FALSE.",
        "Promoted remains FALSE.",
        "Merged remains FALSE.",
        "R8-C PROMOTION CANDIDATE BINDING COMPLETE.",
        "R8-D owns Pre-Promotion Verification.",
    ):
        if marker not in contract:
            errors.append(
                f"R8-C lock missing: {marker}"
            )

    if (
        schema.get("$schema")
        != "https://json-schema.org/draft/2020-12/schema"
    ):
        errors.append(
            "R8-C schema draft disagreement"
        )

    properties = schema.get(
        "properties",
        {}
    )

    expected_consts = {
        "candidate_branch": "candidate/v41-complete",
        "target_branch": "main",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "binding_serialization": "JSON_SORTED_KEYS_COMPACT_UTF8",
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
                f"R8-C schema disagreement: {field}"
            )

    try:
        resolver = load_resolver()
        binding = resolver.resolve("HEAD")
    except Exception as exc:
        errors.append(
            f"R8-C resolver failed: {exc}"
        )
        return errors

    commit = binding.get(
        "candidate_commit",
        ""
    )

    tree = binding.get(
        "candidate_tree",
        ""
    )

    if len(commit) != 40:
        errors.append(
            "R8-C candidate commit is not exact SHA-1 length"
        )

    if len(tree) != 40:
        errors.append(
            "R8-C candidate tree is not exact SHA-1 length"
        )

    supplied_hash = binding.get(
        "binding_sha512",
        ""
    )

    payload = dict(binding)
    payload.pop(
        "binding_sha512",
        None,
    )

    serialized = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    expected_hash = hashlib.sha512(
        serialized
    ).hexdigest()

    if supplied_hash != expected_hash:
        errors.append(
            "R8-C deterministic binding SHA-512 disagreement"
        )

    prohibited = (
        "Human Gate Authorization: GRANTED",
        "Canonical: TRUE",
        "Promoted: TRUE",
        "Merged: TRUE",
    )

    raw = CONTRACT.read_text(
        encoding="utf-8"
    )

    for marker in prohibited:
        if marker in raw:
            errors.append(
                f"R8-C improperly claims state: {marker}"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R8-C PROMOTION CANDIDATE BINDING: FAIL"
        )

        for error in errors:
            print(f" - {error}")

        return 1

    resolver = load_resolver()
    binding = resolver.resolve("HEAD")

    print(
        "R8-C PROMOTION CANDIDATE BINDING: PASS"
    )
    print(
        f"Current candidate commit: "
        f"{binding['candidate_commit']}"
    )
    print(
        f"Current candidate tree: "
        f"{binding['candidate_tree']}"
    )
    print(
        "Binding mechanism: DETERMINISTIC"
    )
    print(
        "Persistent binding instance: NOT YET CREATED"
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
        "R8-C PROMOTION CANDIDATE BINDING COMPLETE"
    )
    print(
        "R8-D Pre-Promotion Verification: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
