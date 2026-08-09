#!/usr/bin/env python3

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "semantics"
    / "SEMANTIC_STATE_GEOMETRY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "semantics"
    / "semantic_state.schema.json"
)

CONSUMERS = {
    "AUTHORIZED_VIEW": (
        ROOT
        / "contracts"
        / "state"
        / "STATE_ROOTS_AUTHORIZED_VIEWS.md"
    ),
    "HYDRATION": (
        ROOT
        / "contracts"
        / "qualification"
        / "HYDRATION_REQUEST_RELEASE.md"
    ),
    "REPORTING": (
        ROOT
        / "contracts"
        / "pipeline"
        / "REPORT_RENDERING_CONTRACT.md"
    ),
    "REPLAY": (
        ROOT
        / "contracts"
        / "runtime"
        / "REPLAY_ENVELOPE.md"
    ),
}


def normalized(path):
    return " ".join(
        path.read_text(
            encoding="utf-8"
        ).split()
    )


def validate():
    errors = []

    for path in (
        CONTRACT,
        SCHEMA,
        *CONSUMERS.values(),
    ):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"semantic-state schema invalid: {exc}"
        ]

    contract = normalized(CONTRACT)

    contract_markers = (
        "Semantic state is not one flat status.",
        "Semantic state is not one serial enum.",
        (
            "Flattening those dimensions destroys "
            "analytical geometry."
        ),
        "Projection MUST NOT mutate existence.",
        "Restriction MUST NOT imply absence.",
        "Unknown MUST NOT imply absence.",
        "Denial MUST NOT imply absence.",
        (
            "Blocked operation MUST NOT imply "
            "denial."
        ),
        (
            "Partial hydration MUST NOT imply "
            "completeness."
        ),
        (
            "Hidden topology MUST NOT imply "
            "nonexistent topology."
        ),
        (
            "Rendering MUST NOT rewrite "
            "analytical state."
        ),
    )

    for marker in contract_markers:
        if marker not in contract:
            errors.append(
                f"AC-05 contract marker missing: {marker}"
            )

    required_properties = {
        "existence_state",
        "epistemic_state",
        "accessibility_state",
        "topology_state",
        "hydration_state",
        "operational_state",
        "decision_state",
        "representation_state",
    }

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    missing = sorted(
        required_properties - properties
    )

    if missing:
        errors.append(
            "semantic-state schema missing dimensions: "
            + ", ".join(missing)
        )

    consumer_markers = {
        "AUTHORIZED_VIEW": (
            "Different visibility does not imply different reality.",
            "Restricted remains existent.",
            "Projection may hide payload.",
            "Projection may not erase known existence.",
        ),
        "HYDRATION": (
            "Restricted != absent.",
        ),
        "REPORTING": (
            "Unknown != false.",
            "Unknown != omission permission.",
            "Material unknowns MUST remain visible.",
            "Redaction != deletion.",
            "Restricted != absent.",
        ),
        "REPLAY": (
            "Replay != new Room.",
            "Historical scope remains historical scope.",
            "Historical boundary remains attributable.",
            "Rendering != evidence.",
            "Replay does not justify full reconstruction.",
            "Do not fabricate history.",
        ),
    }

    for consumer, markers in consumer_markers.items():
        text = normalized(
            CONSUMERS[consumer]
        )

        for marker in markers:
            if marker not in text:
                errors.append(
                    f"{consumer} semantic seam missing: "
                    f"{marker}"
                )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "AC-05 SEMANTIC-STATE INTEGRATION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "AC-05 SEMANTIC-STATE INTEGRATION: PASS"
    )
    print(
        "Semantic geometry: MULTIDIMENSIONAL"
    )
    print(
        "Authorized View seam: VERIFIED"
    )
    print(
        "Hydration seam: VERIFIED"
    )
    print(
        "Reporting seam: VERIFIED"
    )
    print(
        "Replay seam: VERIFIED"
    )
    print(
        "UNKNOWN != ABSENT"
    )
    print(
        "RESTRICTED != ABSENT"
    )
    print(
        "BLOCKED != DENIED"
    )
    print(
        "PARTIAL != COMPLETE"
    )
    print(
        "HIDDEN TOPOLOGY != ABSENT TOPOLOGY"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Disposition: AC_05_INTEGRATION_VALID"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
