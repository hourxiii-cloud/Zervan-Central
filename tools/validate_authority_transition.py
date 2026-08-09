#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.authority_transition import (
    ADMISSIBLE,
    APPROVED,
    EXECUTION,
    SINGLE,
    AuthorityTransitionError,
    ExecutionRequest,
    consume_success,
    execution_eligible,
    make_binding,
    make_execution_receipt,
    validate_binding,
    validate_execution,
)


CONTRACT = (
    ROOT
    / "contracts"
    / "authority"
    / "AUTHORITY_BEARING_TRANSITION_CAPABILITY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "authority"
    / "authority_transition_binding.schema.json"
)

ENGINE = (
    ROOT
    / "tools"
    / "authority_transition.py"
)

R5F = (
    ROOT
    / "contracts"
    / "pipeline"
    / "RAVEN_HUMAN_GATE_PUBLICATION_ACTION_BOUNDARY.md"
)

R5D = (
    ROOT
    / "contracts"
    / "pipeline"
    / "CCR_MC_RESPONSE_OUTPUT_ADMISSIBILITY_BINDING.md"
)

R5H = (
    ROOT
    / "contracts"
    / "pipeline"
    / "REPORT_RENDERING_CONTRACT.md"
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


def build_fixture():
    binding = make_binding(
        human_gate_decision_id=
            "human-gate:ac06:1",
        decision_state=APPROVED,
        transition_class="PUBLICATION",
        transition_target="report:ac06:1",
        object_id="room:ac06:1",
        room_revision_id="revision:ac06:1",
        room_state_root="state:ac06:1",
        authorized_view_root="view:ac06:1",
        evidence_boundary_reference=
            "boundary:ac06:1",
        evidence_ceiling_reference=
            "ceiling:ac06:1",
        approved_scope=(
            "report:ac06:1",
        ),
        mc_disposition=ADMISSIBLE,
        execution_cardinality=SINGLE,
        maximum_execution_count=1,
        provenance_route=(
            "ccr:ac06:1",
            "mc:ac06:1",
            "raven:ac06:1",
            "human-gate:ac06:1",
        ),
    )

    request = ExecutionRequest(
        transition_class="PUBLICATION",
        transition_target="report:ac06:1",
        object_id="room:ac06:1",
        room_revision_id="revision:ac06:1",
        room_state_root="state:ac06:1",
        authorized_view_root="view:ac06:1",
        evidence_boundary_reference=
            "boundary:ac06:1",
        evidence_ceiling_reference=
            "ceiling:ac06:1",
        requested_scope=(
            "report:ac06:1",
        ),
        operation_label=EXECUTION,
        authority_bearing_effect=True,
        provenance_route=(
            "execution-request:ac06:1",
        ),
    )

    return binding, request


def validate() -> list[str]:
    errors: list[str] = []

    for path in (
        CONTRACT,
        SCHEMA,
        ENGINE,
        R5F,
        R5D,
        R5H,
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
            f"AC-06 schema invalid: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            [],
        )
    )

    for field in (
        "authorization_binding_id",
        "human_gate_decision_id",
        "transition_class",
        "transition_target",
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "approved_scope",
        "mc_disposition",
        "execution_cardinality",
        "successful_execution_count",
        "consumption_state",
        "authority_state",
        "human_gate_state",
    ):
        if field not in required:
            errors.append(
                f"AC-06 schema missing required field: {field}"
            )

    contract = normalized(
        CONTRACT
    )

    for marker in (
        "Human Gate is not a status field.",
        "Approval != execution.",
        "Admissibility != authorization.",
        "Prior approval != standing approval.",
        "Stale approval != executable approval.",
        "Invalidated approval != executable approval.",
        "Consumed approval != reusable approval.",
        "Approved state MUST equal executed state.",
        "Zervan's own authority remains: NONE.",
        "Human Gate remains: ACTIVE.",
    ):
        if marker not in contract:
            errors.append(
                f"AC-06 contract marker missing: {marker}"
            )

    r5f = normalized(
        R5F
    )

    for marker in (
        "Human Gate decision != execution.",
        "Approval != execution.",
        "Prior approval != standing approval.",
        "Human Gate approval does not silently rewrite MC classification.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
    ):
        if marker not in r5f:
            errors.append(
                f"R5-F seam marker missing: {marker}"
            )

    r5d = normalized(
        R5D
    )

    for marker in (
        "Admissibility != authority.",
        "MC does not authorize execution.",
        "ADMISSIBLE != execute.",
        "CONDITIONAL != execute.",
    ):
        if marker not in r5d:
            errors.append(
                f"R5-D seam marker missing: {marker}"
            )

    r5h = normalized(
        R5H
    )

    for marker in (
        "Report != publication authority.",
        "Rendered != published.",
        "Publication-ready != published.",
        "Publication-ready != approved.",
    ):
        if marker not in r5h:
            errors.append(
                f"R5-H seam marker missing: {marker}"
            )

    try:
        binding, request = build_fixture()
    except AuthorityTransitionError as exc:
        errors.append(
            f"AC-06 valid fixture rejected: {exc}"
        )

        return errors

    errors.extend(
        validate_binding(
            binding
        )
    )

    execution_errors = validate_execution(
        binding,
        request,
    )

    if execution_errors:
        errors.extend(
            "valid execution rejected: "
            + error
            for error in execution_errors
        )

    if not execution_eligible(
        binding,
        request,
    ):
        errors.append(
            "exact approved movement is not execution eligible"
        )

    try:
        receipt = make_execution_receipt(
            binding,
            request,
            execution_state="SUCCEEDED",
        )
    except AuthorityTransitionError as exc:
        errors.append(
            f"execution receipt rejected: {exc}"
        )

        return errors

    if (
        receipt.authorization_binding_id
        != binding.authorization_binding_id
    ):
        errors.append(
            "execution receipt lost authorization binding"
        )

    if (
        receipt.human_gate_decision_id
        != binding.human_gate_decision_id
    ):
        errors.append(
            "execution receipt lost Human Gate decision"
        )

    consumed = consume_success(
        binding
    )

    if execution_eligible(
        consumed,
        request,
    ):
        errors.append(
            "consumed SINGLE authorization remained executable"
        )

    return sorted(
        set(errors)
    )


def main() -> int:
    errors = validate()

    if errors:
        print(
            "AC-06 AUTHORITY-BEARING TRANSITION INTEGRATION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "AC-06 AUTHORITY-BEARING TRANSITION INTEGRATION: PASS"
    )
    print(
        "R5-D MC admissibility boundary: PRESERVED"
    )
    print(
        "R5-F Human Gate decision boundary: PRESERVED"
    )
    print(
        "R5-H rendering/publication boundary: PRESERVED"
    )
    print(
        "Exact authorization binding: VERIFIED"
    )
    print(
        "Approved-state / execution-state equality: VERIFIED"
    )
    print(
        "Single-execution consumption: VERIFIED"
    )
    print(
        "Approval != execution: VERIFIED"
    )
    print(
        "Admissibility != authorization: VERIFIED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Disposition: AC_06_INTEGRATION_VALID"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
