#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "PIPELINE_INTEGRATION_BOUNDARY_EXISTING_SEMANTICS_LOCK.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "pipeline_integration_boundary_record.schema.json"
)

NAMING_LOCK = (
    ROOT
    / "Doctrine"
    / "PMC_MC_NAMING_LOCK.md"
)

INTERFACE = (
    ROOT
    / "Doctrine"
    / "PMC_MC_INTERFACE.md"
)

RAVEN = (
    ROOT
    / "Modules"
    / "Raven"
    / "raven_contract.md"
)

HUMAN_GATE = (
    ROOT
    / "governance"
    / "human_gate_authority_boundary.md"
)

PIPELINE = [
    "EVIDENCE",
    "PMC",
    "CCR",
    "MC",
    "RAVEN",
    "HUMAN_GATE",
]


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_boundary_record_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "boundary_record_id"
    }

    return (
        "sha512:"
        + hashlib.sha512(
            canonical_bytes(preimage)
        ).hexdigest()
    )


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def normalized(path):
    text = path.read_text(
        encoding="utf-8"
    )

    # Validation concerns semantic text, not Markdown decoration.
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


def validate_record(record):
    errors = []

    if (
        record.get("boundary_record_id")
        != compute_boundary_record_id(record)
    ):
        errors.append(
            "boundary_record_id does not recompute from record"
        )

    exact = {
        "native_version":
            "vTemporal.41.0",
        "promotion_state":
            "CANDIDATE",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "pmc_meaning":
            "PROBABILISTIC_MULTIVERSE_COMPUTATION",
        "ccr_meaning":
            "CANONICAL_COMMITMENT_RECORD",
        "mc_meaning":
            "META_COLLAPSE_RESPONSE_ADMISSIBILITY",
        "unkindness_disposition":
            "RAVEN_ASSOCIATED_FORWARD_TRANSLATION",
        "pmc_mc_interface_collision":
            "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION",
        "room_binding_state":
            "BOUNDARY_LOCKED",
        "evidence_lineage_state":
            "PRESERVED",
        "coordinate_binding_state":
            "PRESERVED",
        "responsibility_separation_state":
            "PRESERVED",
    }

    for field, expected in exact.items():
        if record.get(field) != expected:
            errors.append(
                f"{field} must be {expected}"
            )

    if record.get(
        "pipeline_sequence"
    ) != PIPELINE:
        errors.append(
            "pipeline_sequence must be "
            "EVIDENCE -> PMC -> CCR -> MC -> RAVEN -> HUMAN_GATE"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R5-A boundary record requires provenance_route"
        )

    return errors


def validate():
    errors = []

    required = [
        CONTRACT,
        SCHEMA,
        NAMING_LOCK,
        INTERFACE,
        RAVEN,
        HUMAN_GATE,
    ]

    for path in required:
        if not path.exists():
            errors.append(
                f"missing required R5-A artifact: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    # --------------------------------------------------------
    # Inner-ring execution belongs to tools/validate_ring5.py.
    #
    # R5-A validates only its own integration boundary.
    # Dependency artifacts must exist, but this validator does not
    # recursively execute Rings 1-4.
    # --------------------------------------------------------

    dependency_artifacts = [
        ROOT / "tools" / "validate_ring1.py",
        ROOT / "tools" / "validate_ring2.py",
        ROOT / "tools" / "validate_ring3.py",
        ROOT / "tools" / "validate_ring4.py",
        ROOT / "tools" / "validate_ring4_closure.py",
        ROOT / "contracts" / "runtime"
        / "RING4_RUNTIME_STATE_OPERATIONS_CLOSURE.md",
    ]

    for dependency in dependency_artifacts:
        if not dependency.exists():
            errors.append(
                "missing required inner-ring dependency artifact: "
                + str(dependency.relative_to(ROOT))
            )

    # --------------------------------------------------------
    # Live naming control must preserve CCR.
    # --------------------------------------------------------

    naming = normalized(
        NAMING_LOCK
    )

    naming_locks = [
        "PMC means Probabilistic Multiverse Computation only.",
        "MC means Meta Collapse (Response Admissibility Layer) only.",
        "CCR means Canonical Commitment Record",
        "PMC may not authorize response or action.",
        "CCR construction may not reinterpret PMC truth.",
        "MC may not create truth, alter PMC output, or generate CCR content.",
        "Human Gate alone controls whether an admissible action is taken.",
    ]

    for lock in naming_locks:
        if (
            " ".join(lock.split())
            not in naming
        ):
            errors.append(
                f"existing PMC/CCR/MC naming lock missing: {lock}"
            )

    # Canonical-flow verification.
    #
    # Do not use first-occurrence positions across the whole doctrine:
    # PMC / CCR / MC are defined earlier in the file and therefore
    # legitimately appear before the Canonical Flow section.
    canonical_flow_locks = [
        "Evidence",
        "-> PMC: plausible-world evaluation and epistemic collapse",
        "-> CCR: deterministic candidate commitment/report record",
        "-> MC: response/output admissibility gate",
        "-> Raven / downstream representation",
        "-> Human Gate: action authority",
    ]

    flow_positions = []
    flow_start = naming.find(
        "Canonical Flow"
    )

    if flow_start == -1:
        errors.append(
            "existing naming control is missing Canonical Flow"
        )
    else:
        flow_text = naming[
            flow_start:
        ]

        for token in canonical_flow_locks:
            flow_positions.append(
                flow_text.find(
                    token
                )
            )

        if (
            any(
                pos == -1
                for pos in flow_positions
            )
            or flow_positions
            != sorted(
                flow_positions
            )
        ):
            errors.append(
                "existing naming control does not preserve "
                "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate"
            )

    # --------------------------------------------------------
    # Existing PMC->MC direct-flow collision must remain visible.
    # --------------------------------------------------------

    interface = normalized(
        INTERFACE
    )

    if (
        "PMC → MC is the only permitted flow."
        not in interface
    ):
        errors.append(
            "R5-A expected PMC->MC interface collision is not attributable"
        )

    # --------------------------------------------------------
    # Raven / Unkindness existing semantics
    # --------------------------------------------------------

    raven = normalized(
        RAVEN
    )

    raven_locks = [
        "Authority Scope: REPORTING ONLY",
        "Raven is the system’s voice — not its will.",
        "The Unkindness is Raven's reporting brand and output voice.",
        "It is not a separate module",
        "reporting only, no mutation, no learning, no gating",
    ]

    for lock in raven_locks:
        if (
            " ".join(lock.split())
            not in raven
        ):
            errors.append(
                f"existing Raven / Unkindness boundary missing: {lock}"
            )

    # --------------------------------------------------------
    # Human Gate authority boundary
    # --------------------------------------------------------

    human_gate = normalized(
        HUMAN_GATE
    )

    human_locks = [
        "Human Gate preserves the boundary between analysis and authority-bearing action.",
        "Zervan does not authorize action by itself.",
        "Authority-bearing movement requires explicit human approval.",
        "Human Gate controls authority.",
    ]

    for lock in human_locks:
        if (
            " ".join(lock.split())
            not in human_gate
        ):
            errors.append(
                f"existing Human Gate boundary missing: {lock}"
            )

    # --------------------------------------------------------
    # R5-A contract locks
    # --------------------------------------------------------

    text = normalized(
        CONTRACT
    )

    locks = [
        "Integration != redefinition.",
        "Binding != ownership.",
        "Binding != authority.",
        "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate.",
        "PMC means Probabilistic Multiverse Computation only.",
        "CCR means Canonical Commitment Record.",
        "MC means Meta Collapse (Response Admissibility Layer) only.",
        "PMC may not authorize response or action.",
        "CCR construction may not reinterpret PMC truth.",
        "CCR MUST NOT be silently omitted from native-v41 pipeline routing.",
        "MC may not create truth.",
        "MC may not alter PMC output.",
        "MC may not generate CCR content.",
        "MC does not authorize execution.",
        "Raven is reporting.",
        "Raven is not governance.",
        "Raven is not truth authority.",
        "Raven may transform presentation.",
        "Raven may not transform justified substance.",
        "The Unkindness is not inserted as a separate evidence-to-publication stage.",
        "Human Gate decision != execution itself.",
        "Pipeline stages MUST bind to Room state without becoming Room components.",
        "No stage receives authority merely because it receives Room bindings.",
        "Downstream representation MUST NOT erase upstream evidence provenance.",
        "No Compression Out applies across pipeline lineage.",
        "Coordinate reference != Cartography ownership.",
        "Decision option != decision authority.",
        "Decision option != execution.",
        "Report != truth authority.",
        "Report != publication authority.",
        "Report != certification.",
        "Native-v41 integration MUST NOT use the older direct-flow wording to bypass CCR.",
        "Collision record != silent rewrite.",
        "Preserve artifact.",
        "Preserve provenance.",
        "Prevent bypass.",
        "Convenience != ownership.",
        "Write capability != authority.",
        "Validation != authority.",
        "Pipeline completion != authority.",
        "Fail closed.",
        "Surface collisions.",
        "Do not normalize them away.",
        "R5-B owns Room-Bound Evidence -> PMC Intake Binding.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in text
        ):
            errors.append(
                f"missing R5-A lock: {lock}"
            )

    # --------------------------------------------------------
    # Schema boundary
    # --------------------------------------------------------

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-A schema JSON: {exc}"
        ]

    props = schema.get(
        "properties",
        {}
    )

    forbidden = {
        "pmc_output",
        "ccr_content",
        "mc_decision",
        "raven_report",
        "human_gate_decision",
        "decision_option",
        "publication_authorization",
        "execution_authorization",
        "canonical_promotion",
    }

    leaked = (
        set(props)
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-A improperly implements downstream pipeline semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    # --------------------------------------------------------
    # Deterministic boundary record
    # --------------------------------------------------------

    record = {
        "schema_version":
            "1.0",
        "native_version":
            "vTemporal.41.0",
        "promotion_state":
            "CANDIDATE",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "pipeline_sequence":
            PIPELINE,
        "pmc_meaning":
            "PROBABILISTIC_MULTIVERSE_COMPUTATION",
        "ccr_meaning":
            "CANONICAL_COMMITMENT_RECORD",
        "mc_meaning":
            "META_COLLAPSE_RESPONSE_ADMISSIBILITY",
        "unkindness_disposition":
            "RAVEN_ASSOCIATED_FORWARD_TRANSLATION",
        "pmc_mc_interface_collision":
            "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION",
        "room_binding_state":
            "BOUNDARY_LOCKED",
        "evidence_lineage_state":
            "PRESERVED",
        "coordinate_binding_state":
            "PRESERVED",
        "responsibility_separation_state":
            "PRESERVED",
        "provenance_route": [
            "Doctrine/PMC.md",
            "Doctrine/PMC_MC_INTERFACE.md",
            "Doctrine/PMC_MC_NAMING_LOCK.md",
            "Doctrine/MC.md",
            "Modules/Raven/raven_contract.md",
            "governance/human_gate_authority_boundary.md",
            "contracts/object/CANONICAL_ROOM_OBJECT_IDENTITY_SINGULARITY.md",
            "contracts/state/STATE_ROOTS_AUTHORIZED_VIEWS.md",
            "contracts/geography/ORIENTATION_COORDINATES.md",
            "contracts/geography/CARTOGRAPHY.md",
            "contracts/geography/STICK_CONTACT_CONTINUITY.md",
        ],
        "recorded_at":
            "2026-08-07T21:27:00-04:00",
    }

    record[
        "boundary_record_id"
    ] = compute_boundary_record_id(
        record
    )

    errors.extend(
        validate_record(
            record
        )
    )

    # CCR removal must fail.
    bypass = dict(
        record
    )

    bypass[
        "pipeline_sequence"
    ] = [
        "EVIDENCE",
        "PMC",
        "MC",
        "RAVEN",
        "HUMAN_GATE",
    ]

    bypass[
        "boundary_record_id"
    ] = compute_boundary_record_id(
        bypass
    )

    bypass_errors = validate_record(
        bypass
    )

    if not any(
        "pipeline_sequence"
        in error
        for error in bypass_errors
    ):
        errors.append(
            "R5-A incorrectly permitted direct PMC->MC bypass"
        )

    # Unkindness as independent stage must fail.
    separate_unkindness = dict(
        record
    )

    separate_unkindness[
        "unkindness_disposition"
    ] = "INDEPENDENT_PIPELINE_STAGE"

    separate_unkindness[
        "boundary_record_id"
    ] = compute_boundary_record_id(
        separate_unkindness
    )

    unkindness_errors = validate_record(
        separate_unkindness
    )

    if not any(
        "unkindness_disposition"
        in error
        for error in unkindness_errors
    ):
        errors.append(
            "R5-A incorrectly permitted independent Unkindness pipeline stage"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-A PIPELINE INTEGRATION BOUNDARY / "
            "EXISTING-SEMANTICS LOCK: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-A PIPELINE INTEGRATION BOUNDARY / "
        "EXISTING-SEMANTICS LOCK: PASS"
    )
    print(
        "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate: LOCKED"
    )
    print(
        "PMC / CCR / MC functional ownership: PRESERVED"
    )
    print(
        "Raven / Human Gate responsibility boundaries: PRESERVED"
    )
    print(
        "The Unkindness -> Raven-associated forward translation: LOCKED"
    )
    print(
        "Direct PMC -> MC bypass collision: RECORDED / REJECTED"
    )
    print(
        "Room / evidence lineage / coordinate binding boundary: ESTABLISHED"
    )
    print(
        "R5-B stage implementation: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
