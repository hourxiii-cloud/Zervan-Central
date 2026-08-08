#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

VERSION = ROOT / "VERSION"
VERSION_JSON = ROOT / "VERSION.json"
AUTHORITY = ROOT / "VERSION_AUTHORITY.md"
README = ROOT / "README.md"

CONTRACT = (
    ROOT
    / "contracts"
    / "promotion"
    / "NATIVE_V41_ENTRY_VERSION_AUTHORITY.md"
)

INIT = (
    ROOT
    / "call"
    / "INITIATION_STATEMENT_V41_0.md"
)

ENTRY = (
    ROOT
    / "canonical"
    / "ZERVAN_v41_0_CANONICAL_ENTRY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "promotion"
    / "native_v41_entry.schema.json"
)

HISTORICAL = [
    ROOT / "call" / "INITIATION_STATEMENT_V39_0.md",
    ROOT / "call" / "INITIATION_STATEMENT_V40_0.md",
    ROOT / "canonical" / "ZERVAN_v39_0_CANONICAL_LOAD.md",
    ROOT / "canonical" / "ZERVAN_v40_0_CANONICAL_LOAD.md",
]

ACTIVE_VERSION = "vTemporal.41.0"


def normalized(path):
    text = path.read_text(
        encoding="utf-8"
    )

    for token in (
        "**",
        "__",
        "`",
    ):
        text = text.replace(
            token,
            ""
        )

    return " ".join(
        text.split()
    )


def make_entry_record():
    return {
        "schema_version":
            "1.0",

        "version":
            ACTIVE_VERSION,

        "implementation_identity":
            "v41 Complete",

        "promotion_state":
            "CANDIDATE",

        "canonical":
            False,

        "canonical_branch":
            "main",

        "development_branch":
            "candidate/v41-complete",

        "version_surfaces": [
            "VERSION",
            "VERSION.json",
            "VERSION_AUTHORITY.md",
        ],

        "initiation_surface":
            "call/INITIATION_STATEMENT_V41_0.md",

        "canonical_entry_surface":
            "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md",

        "historical_entry_surfaces": [
            "call/INITIATION_STATEMENT_V39_0.md",
            "call/INITIATION_STATEMENT_V40_0.md",
            "canonical/ZERVAN_v39_0_CANONICAL_LOAD.md",
            "canonical/ZERVAN_v40_0_CANONICAL_LOAD.md",
        ],

        "authority_state":
            "NONE",

        "human_gate_state":
            "ACTIVE",

        "external_runtime":
            "DISABLED",

        "external_action":
            "DISABLED",

        "system_population":
            "DISALLOWED",

        "target_state":
            "READY_FOR_HUMAN_GATE",
    }


def validate():
    errors = []

    required = [
        VERSION,
        VERSION_JSON,
        AUTHORITY,
        README,
        CONTRACT,
        INIT,
        ENTRY,
        SCHEMA,
    ]

    for path in required:
        if not path.exists():
            errors.append(
                f"missing required R7-C surface: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    # --------------------------------------------------------
    # Active version declarations
    # --------------------------------------------------------

    version_text = VERSION.read_text(
        encoding="utf-8"
    ).strip()

    if version_text != ACTIVE_VERSION:
        errors.append(
            f"VERSION mismatch: {version_text!r}"
        )

    try:
        version_json = json.loads(
            VERSION_JSON.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"invalid VERSION.json: {exc}"
        ]

    expected_version_json = {
        "version":
            ACTIVE_VERSION,

        "release_line":
            "v41",

        "implementation_identity":
            "v41 Complete",

        "promotion_state":
            "CANDIDATE",

        "canonical":
            False,

        "canonical_branch":
            "main",

        "development_branch":
            "candidate/v41-complete",

        "authority_contract":
            "VERSION_AUTHORITY.md",

        "inferred_versioning_allowed":
            False,

        "mixed_version_identity_allowed":
            False,
    }

    for key, expected in expected_version_json.items():
        if version_json.get(key) != expected:
            errors.append(
                "VERSION.json mismatch for "
                f"{key}: expected {expected!r}, "
                f"got {version_json.get(key)!r}"
            )

    authority = normalized(
        AUTHORITY
    )

    authority_locks = [
        "Native v41 has one implementation version identity:",
        "vTemporal.41.0",
        "The human-readable declaration is:",
        "/VERSION",
        "The machine-readable declaration is:",
        "/VERSION.json",
        "One active version.",
        "One authority path.",
        "No inferred versioning.",
        "Promotion State: CANDIDATE",
        "Canonical: FALSE",
        "Canonical Branch: main",
        "Development Branch: candidate/v41-complete",
        "Human Gate remains required for canonical promotion.",
    ]

    for lock in authority_locks:
        if " ".join(
            lock.split()
        ) not in authority:
            errors.append(
                f"VERSION_AUTHORITY missing semantic: {lock}"
            )

    # --------------------------------------------------------
    # R7-C contract
    # --------------------------------------------------------

    contract = normalized(
        CONTRACT
    )

    contract_locks = [
        "R7-C = README / Version Authority / Native-v41 Entry Surfaces.",
        "VERSION remains authoritative.",
        "VERSION.json remains authoritative.",
        "VERSION_AUTHORITY.md remains authoritative.",
        "R7-C does not manufacture a new version.",
        "R7-C does not promote the candidate.",
        "One active version.",
        "One authority path.",
        "No inferred versioning.",
        "README owns orientation.",
        "The README shall not carry the entire civilization.",
        "Historical initiation != active initiation.",
        "Entry surface != promotion.",
        "Historical presence != active authority.",
        "Candidate strength != canonical status.",
        "Validation != promotion.",
        "Documentation != promotion.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "External Runtime remains DISABLED.",
        "External Action remains DISABLED.",
        "System Population remains DISALLOWED.",
        "No entry document grants authority.",
        "No README text grants authority.",
        "No version declaration grants authority.",
        "Version authority precedes interpretation.",
        "Historical artifacts do not precede active version authority.",
        "Entry orientation != doctrine duplication.",
        "Silent active-version disagreement is invalid.",
        "Inventory != version authority.",
        "R7-M owns final Fresh-Reader package validation.",
        "Promotion State remains CANDIDATE.",
        "R7-D owns User Manual.",
    ]

    for lock in contract_locks:
        if " ".join(
            lock.split()
        ) not in contract:
            errors.append(
                f"R7-C contract missing lock: {lock}"
            )

    # --------------------------------------------------------
    # README orientation
    # --------------------------------------------------------

    readme = normalized(
        README
    )

    readme_locks = [
        "vTemporal.41.0",
        "v41 Complete",
        "candidate/v41-complete",
        "CANDIDATE",
        "Canonical branch:",
        "main",
        "VERSION",
        "VERSION.json",
        "VERSION_AUTHORITY.md",
        "README owns orientation.",
        "README does not own version authority.",
        "call/INITIATION_STATEMENT_V41_0.md",
        "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md",
        "Native v41 does not require prior v39 or v40 knowledge to initialize.",
        "Authority:",
        "NONE",
        "Human Gate:",
        "ACTIVE",
        "The README shall not carry the entire civilization.",
        "Current Git is implementation truth.",
        "Documentation does not replace implementation.",
    ]

    for lock in readme_locks:
        if " ".join(
            lock.split()
        ) not in readme:
            errors.append(
                f"README missing orientation semantic: {lock}"
            )

    # README must not claim historical versions are active entry.
    forbidden_readme = [
        "Initialize v39",
        "Initialize v40",
        "Current version: v39",
        "Current version: v40",
    ]

    for forbidden in forbidden_readme:
        if forbidden in readme:
            errors.append(
                f"README contains active historical-version wording: {forbidden}"
            )

    # --------------------------------------------------------
    # Initiation
    # --------------------------------------------------------

    init = normalized(
        INIT
    )

    init_locks = [
        "Version: vTemporal.41.0",
        "Implementation Identity: v41 Complete",
        "Promotion State: CANDIDATE",
        "Canonical: FALSE",
        "Canonical Branch: main",
        "Development Branch: candidate/v41-complete",
        "Authority: NONE",
        "Human Gate: ACTIVE",
        "External Runtime: DISABLED",
        "External Action: DISABLED",
        "System Population: DISALLOWED",
        "DISCUSSION / TECH / NONE / NON-DOCTRINAL / STABLE",
        "CONTROLLED / CANDIDATE / PRE-PROMOTION",
        "/VERSION",
        "/VERSION.json",
        "/VERSION_AUTHORITY.md",
        "/canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md",
        "Current Git is implementation truth.",
        "Do not use stored memory as implementation authority.",
        "Do not infer version",
        "Native-v41 initialization MUST NOT require v39 or v40 knowledge.",
        "Do not fall back to v39.",
        "Do not fall back to v40.",
        "Promotion remains Human-Gated.",
    ]

    for lock in init_locks:
        if " ".join(
            lock.split()
        ) not in init:
            errors.append(
                f"v41 initiation missing semantic: {lock}"
            )

    # --------------------------------------------------------
    # Canonical entry
    # --------------------------------------------------------

    entry = normalized(
        ENTRY
    )

    entry_locks = [
        "Status: CONTROLLED CANDIDATE ENTRY",
        "Version: vTemporal.41.0",
        "Implementation Identity: v41 Complete",
        "Promotion State: CANDIDATE",
        "Canonical: FALSE",
        "Canonical Branch: main",
        "Development Branch: candidate/v41-complete",
        "Authority: NONE",
        "Human Gate: ACTIVE",
        "Canonical Entry != canonical promotion.",
        "THE ROOM IS ONE ANALYTICAL OBJECT.",
        "THE ROOM IS VERIFIED OPERATIONAL TERRITORY.",
        "TURN THE OBJECT. DO NOT CLONE THE WORLD.",
        "QUALIFICATION PRECEDES ANALYSIS.",
        "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate",
        "Question != mutation.",
        "Validation success != canonical promotion.",
        "READY_FOR_HUMAN_GATE",
        "Historical artifact != active authority.",
        "Do not use v39 as active entry.",
        "Do not use v40 as active entry.",
        "Do not infer version.",
        "Do not infer authority.",
        "Do not infer promotion.",
    ]

    for lock in entry_locks:
        if " ".join(
            lock.split()
        ) not in entry:
            errors.append(
                f"v41 canonical entry missing semantic: {lock}"
            )

    # --------------------------------------------------------
    # Historical preservation
    # --------------------------------------------------------

    for path in HISTORICAL:
        if not path.exists():
            errors.append(
                "historical provenance surface missing: "
                f"{path.relative_to(ROOT)}"
            )

    # --------------------------------------------------------
    # Schema
    # --------------------------------------------------------

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        errors.append(
            f"invalid R7-C schema JSON: {exc}"
        )
        schema = {}

    if (
        schema.get(
            "$schema"
        )
        != "https://json-schema.org/draft/2020-12/schema"
    ):
        errors.append(
            "R7-C schema must use JSON Schema Draft 2020-12"
        )

    record = make_entry_record()

    if record[
        "version"
    ] != version_text:
        errors.append(
            "machine-readable R7-C record disagrees with VERSION"
        )

    if record[
        "promotion_state"
    ] != "CANDIDATE":
        errors.append(
            "R7-C record promoted candidate state"
        )

    if record[
        "canonical"
    ] is not False:
        errors.append(
            "R7-C record falsely declares canonical state"
        )

    if record[
        "authority_state"
    ] != "NONE":
        errors.append(
            "R7-C authority must remain NONE"
        )

    if record[
        "human_gate_state"
    ] != "ACTIVE":
        errors.append(
            "R7-C Human Gate must remain ACTIVE"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R7-C README / VERSION AUTHORITY / NATIVE-v41 ENTRY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R7-C README / VERSION AUTHORITY / NATIVE-v41 ENTRY: PASS"
    )
    print(
        "Active version: vTemporal.41.0"
    )
    print(
        "Implementation identity: v41 Complete"
    )
    print(
        "VERSION / VERSION.json agreement: VALIDATED"
    )
    print(
        "VERSION_AUTHORITY: PRESERVED"
    )
    print(
        "One active version / one authority path: VALIDATED"
    )
    print(
        "README ownership: ORIENTATION"
    )
    print(
        "Native-v41 initiation: IMPLEMENTED"
    )
    print(
        "Native-v41 canonical entry: IMPLEMENTED"
    )
    print(
        "v39 / v40 historical entry surfaces: PRESERVED AS HISTORY"
    )
    print(
        "v39 / v40 active initialization dependency: REJECTED"
    )
    print(
        "Active-version disagreement: REJECTED"
    )
    print(
        "Candidate -> canonical confusion: REJECTED"
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
        "R7-D User Manual: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
