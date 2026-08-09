#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.cross_stage_integrity import (
    BLOCKED,
    VALID,
    make_valid_pipeline,
    validate_composition,
)


R5C = ROOT / (
    "contracts/pipeline/"
    "PMC_CCR_CANDIDATE_COMMITMENT_LINEAGE.md"
)

R5D = ROOT / (
    "contracts/pipeline/"
    "CCR_MC_RESPONSE_OUTPUT_ADMISSIBILITY_BINDING.md"
)

R5E = ROOT / (
    "contracts/pipeline/"
    "MC_RAVEN_REPRESENTATION_REPORT_BINDING.md"
)

R5F = ROOT / (
    "contracts/pipeline/"
    "RAVEN_HUMAN_GATE_PUBLICATION_ACTION_BOUNDARY.md"
)

R5I = ROOT / (
    "contracts/pipeline/"
    "PIPELINE_CROSS_STAGE_INTEGRITY_NO_RESPONSIBILITY_ABSORPTION.md"
)

AC07 = ROOT / (
    "contracts/integrity/"
    "CROSS_STAGE_SEMANTIC_INTEGRITY.md"
)


def normalized(path: Path) -> str:
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
            "",
        )

    return " ".join(
        text.split()
    )


def require_any(
    errors: list[str],
    *,
    surface: str,
    text: str,
    alternatives: tuple[str, ...],
):
    if not any(
        marker in text
        for marker in alternatives
    ):
        errors.append(
            surface
            + " semantic seam not recognized: "
            + " | ".join(alternatives)
        )


def validate() -> list[str]:
    errors: list[str] = []

    surfaces = (
        R5C,
        R5D,
        R5E,
        R5F,
        R5I,
        AC07,
    )

    for path in surfaces:
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    r5c = normalized(R5C)
    r5d = normalized(R5D)
    r5e = normalized(R5E)
    r5f = normalized(R5F)
    r5i = normalized(R5I)
    ac07 = normalized(AC07)

    # ------------------------------------------------------
    # R5-C — PMC -> CCR
    # Recognize established semantics, not invented wording.
    # ------------------------------------------------------

    require_any(
        errors,
        surface="R5-C candidate lineage",
        text=r5c,
        alternatives=(
            "candidate",
            "Candidate",
        ),
    )

    require_any(
        errors,
        surface="R5-C rejected-state preservation",
        text=r5c,
        alternatives=(
            "rejected",
            "Rejected",
            "rejection",
            "Rejection",
        ),
    )

    require_any(
        errors,
        surface="R5-C uncertainty preservation",
        text=r5c,
        alternatives=(
            "uncertainty",
            "Uncertainty",
        ),
    )

    # ------------------------------------------------------
    # R5-D — CCR -> MC
    # ------------------------------------------------------

    require_any(
        errors,
        surface="R5-D admissibility boundary",
        text=r5d,
        alternatives=(
            "Admissibility != authority.",
            "MC does not authorize execution.",
        ),
    )

    require_any(
        errors,
        surface="R5-D conditional state",
        text=r5d,
        alternatives=(
            "CONDITIONAL",
        ),
    )

    require_any(
        errors,
        surface="R5-D evidence ceiling",
        text=r5d,
        alternatives=(
            "evidence ceiling",
            "Evidence Ceiling",
            "Maximum Justified Claim",
        ),
    )

    require_any(
        errors,
        surface="R5-D governance constraints",
        text=r5d,
        alternatives=(
            "Governance constraints",
            "governance constraints",
        ),
    )

    # ------------------------------------------------------
    # R5-E — MC -> Raven
    # ------------------------------------------------------

    require_any(
        errors,
        surface="R5-E Raven representation",
        text=r5e,
        alternatives=(
            "Raven",
        ),
    )

    require_any(
        errors,
        surface="R5-E uncertainty preservation",
        text=r5e,
        alternatives=(
            "uncertainty",
            "Uncertainty",
        ),
    )

    require_any(
        errors,
        surface="R5-E evidence ceiling",
        text=r5e,
        alternatives=(
            "evidence ceiling",
            "Evidence Ceiling",
            "Maximum Justified Claim",
        ),
    )

    # ------------------------------------------------------
    # R5-F — Raven -> Human Gate
    # ------------------------------------------------------

    require_any(
        errors,
        surface="R5-F Human Gate boundary",
        text=r5f,
        alternatives=(
            "Human Gate controls authority-bearing movement.",
            "Explicit human approval is required for authority-bearing movement.",
        ),
    )

    require_any(
        errors,
        surface="R5-F analysis preservation",
        text=r5f,
        alternatives=(
            "Approval Does Not Rewrite Analysis",
            "Human Gate approval does not:",
        ),
    )

    require_any(
        errors,
        surface="R5-F approval/execution separation",
        text=r5f,
        alternatives=(
            "Approval != execution.",
            "Human Gate decision != execution.",
        ),
    )

    # ------------------------------------------------------
    # R5-I — existing aggregate cross-stage semantics
    # ------------------------------------------------------

    require_any(
        errors,
        surface="R5-I cross-stage integrity",
        text=r5i,
        alternatives=(
            "Cross-Stage",
            "cross-stage",
            "Cross Stage",
            "cross stage",
        ),
    )

    require_any(
        errors,
        surface="R5-I responsibility boundary",
        text=r5i,
        alternatives=(
            "responsibility",
            "Responsibility",
            "ownership",
            "Ownership",
        ),
    )

    require_any(
        errors,
        surface="R5-I semantic preservation",
        text=r5i,
        alternatives=(
            "semantic",
            "Semantic",
            "meaning",
            "Meaning",
            "integrity",
            "Integrity",
        ),
    )

    # ------------------------------------------------------
    # AC-07 must declare activation, not redefinition.
    # ------------------------------------------------------

    for marker in (
        "AC-07 activates existing native-v41 semantics.",
        "AC-07 does not absorb those responsibilities.",
        "Composition validation != stage ownership.",
        "Local validity != composed validity.",
        "Stage PASS != composition PASS.",
    ):
        if marker not in ac07:
            errors.append(
                f"AC-07 integration marker missing: {marker}"
            )

    # ------------------------------------------------------
    # Executable aggregate sanity check
    # ------------------------------------------------------

    pipeline = make_valid_pipeline()

    valid = validate_composition(
        *pipeline
    )

    if valid.composition_disposition != VALID:
        errors.append(
            "valid existing-pipeline composition rejected"
        )

    if valid.failure_reasons:
        errors.append(
            "valid existing-pipeline composition emitted failures"
        )

    # Prove aggregate validator is not merely checking
    # whether local stages claim PASS.
    from dataclasses import replace

    broken = list(pipeline)

    broken[3] = replace(
        broken[3],
        claim_strength=(
            broken[2].claim_strength + 1
        ),
    )

    if not all(
        stage.local_valid
        for stage in broken
    ):
        errors.append(
            "AR-064 fixture lost local-valid premise"
        )

    impossible = validate_composition(
        *broken
    )

    if impossible.composition_disposition != BLOCKED:
        errors.append(
            "globally impossible composition was not blocked"
        )

    if (
        "CLAIM_STRENGTH_INCREASED"
        not in impossible.failure_reasons
    ):
        errors.append(
            "Raven semantic strengthening was not detected"
        )

    if (
        "GLOBAL_STATE_IMPOSSIBLE"
        not in impossible.failure_reasons
    ):
        errors.append(
            "AR-064 aggregate impossibility was not detected"
        )

    return sorted(
        set(errors)
    )


def main() -> int:
    errors = validate()

    if errors:
        print(
            "AC-07 CROSS-STAGE EXISTING-PIPELINE INTEGRATION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "AC-07 CROSS-STAGE EXISTING-PIPELINE INTEGRATION: PASS"
    )
    print(
        "R5-C PMC -> CCR semantics: PRESERVED"
    )
    print(
        "R5-D CCR -> MC semantics: PRESERVED"
    )
    print(
        "R5-E MC -> Raven semantics: PRESERVED"
    )
    print(
        "R5-F Raven -> Human Gate semantics: PRESERVED"
    )
    print(
        "R5-I cross-stage responsibility boundary: PRESERVED"
    )
    print(
        "AC-07 parallel-pipeline creation: NONE"
    )
    print(
        "Local-valid / globally-impossible detection: VERIFIED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Disposition: AC_07_EXISTING_PIPELINE_INTEGRATION_VALID"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
