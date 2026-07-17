#!/usr/bin/env python3
"""Immutable Scar and minimum Replay continuity for the Zervan v40 candidate."""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

from candidate.v40.runtime.transition_writer import HASH_PATTERN, STOP_CLASSES, validate_event


SCAR_CLASSES = {
    "CONTRACT_CONTROL_STOP",
    "HUMAN_GATE_STOP",
    "EVIDENCE_BOUNDARY_EXHAUSTION",
    "UNRESOLVED_CONTRADICTION",
    "RECURSIVE_ANALYTICAL_FAILURE",
    "TRANSITION_WITNESS_FAILURE",
    "UNCLASSIFIED_CONTROL_STOP",
}
EVIDENCE_BOUNDARY_STATES = {
    "AVAILABLE",
    "PARTIAL",
    "EXHAUSTED",
    "CONTRADICTORY",
    "INVALID",
    "UNKNOWN",
}
THIRDS_MARKER_KINDS = {"REPEATING_ONE_THIRD", "REPEATING_TWO_THIRDS"}
THIRDS_CONDITION_TO_SCAR_CLASS = {
    "UNRESOLVED_CONTRADICTION": "UNRESOLVED_CONTRADICTION",
    "EVIDENCE_BOUNDARY_EXHAUSTION": "EVIDENCE_BOUNDARY_EXHAUSTION",
    "RECURSIVE_ANALYTICAL_FAILURE": "RECURSIVE_ANALYTICAL_FAILURE",
    "UNKNOWN": "UNCLASSIFIED_CONTROL_STOP",
}
SCAR_ID_PATTERN = re.compile(r"^SC-[A-Z0-9._-]+$")
CONTRACT_ID_PATTERN = re.compile(r"^OC-[A-Z0-9._-]+$")
CONTRACT_INSTANCE_ID_PATTERN = re.compile(r"^OCI-[A-Z0-9._-]+$")
EVENT_ID_PATTERN = re.compile(r"^TE-[A-Z0-9._-]+$")


SCAR_FIELDS = {
    "scar_version",
    "scar_id",
    "contract_ref",
    "contract_instance_id",
    "route_id",
    "route_lock",
    "canonical_binding_ref",
    "terminal_event_id",
    "terminal_event_sequence",
    "terminal_event_sha512",
    "transition_ledger_head_sha512",
    "recorded_at_utc",
    "authority_state",
    "human_gate_state",
    "scar_class",
    "stop_class",
    "trigger",
    "reason",
    "evidence_boundary",
    "analysis_state",
    "continuation",
    "provenance_refs",
    "scar_sha512",
}
EVIDENCE_BOUNDARY_FIELDS = {
    "boundary_state",
    "available_evidence_refs",
    "missing_evidence_refs",
    "contradiction_refs",
    "invalid_evidence_refs",
    "scope_exclusions",
    "boundary_reason",
    "evidence_time_utc",
}
ANALYSIS_STATE_FIELDS = {
    "inquiry_ref",
    "claim_refs",
    "unresolved_claim_refs",
    "eliminated_world_refs",
    "surviving_world_refs",
    "function_participation_refs",
    "last_supported_conclusion_refs",
    "state_summary",
}
CONTINUATION_FIELDS = {
    "replay_eligible",
    "replay_blockers",
    "replay_preconditions",
    "new_contract_required",
    "continuation_ref",
    "human_gate_decision_required",
}
REPLAY_FIELDS = {
    "replay_version",
    "replay_id",
    "replay_sequence",
    "decision_of_replay_id",
    "requested_at_utc",
    "prepared_at_utc",
    "scar_ref",
    "scar_sha512",
    "source_contract_ref",
    "source_contract_instance_id",
    "source_route_id",
    "source_route_lock",
    "terminal_event_id",
    "terminal_event_sha512",
    "transition_ledger_head_sha512",
    "scar_ledger_sha512",
    "source_canonical_binding_ref",
    "current_canonical_binding_ref",
    "canonical_comparison",
    "authority_state",
    "restored_context",
    "unavailable_context",
    "continuation_proposal",
    "human_gate",
    "status",
    "previous_replay_sha512",
    "replay_sha512",
}
REPLAY_STATUSES = {
    "PREPARED",
    "BLOCKED",
    "HUMAN_GATE_REVIEW",
    "AUTHORIZED_NEW_CONTRACT_REQUIRED",
    "DENIED",
}
CANONICAL_COMPARISONS = {
    "UNCHANGED",
    "ADVANCED_REVALIDATION_REQUIRED",
    "DRIFTED",
    "UNAVAILABLE",
    "INVALID",
}
CONTEXT_CLASSES = {
    "ROUTE_CONTRACT",
    "CANONICAL_BINDING",
    "TRANSITION_LEDGER",
    "TERMINAL_EVENT",
    "SCAR",
    "EVIDENCE_BOUNDARY",
    "ANALYTICAL_STATE",
    "FUNCTION_PARTICIPATION",
    "PRIOR_DECISION",
}
CONTINUATION_PROPOSAL_FIELDS = {
    "proposed_route_id",
    "proposed_scope",
    "proposed_completion_criteria",
    "required_evidence_refs",
    "new_contract_required",
    "new_contract_ref",
    "new_contract_instance_id",
    "continuation_ref",
}
HUMAN_GATE_FIELDS = {"state", "decision", "decision_ref", "decided_at_utc", "decision_owner"}
REPLAY_ID_PATTERN = re.compile(r"^RP-[A-Z0-9._-]+$")
CONTINUATION_ID_PATTERN = re.compile(r"^CONT-[A-Z0-9._-]+$")


class ContinuityError(RuntimeError):
    """A continuity record, binding, or ledger is invalid."""


class ScarPersistenceError(ContinuityError):
    """A Scar could not be durably published."""


class UnreadableContinuityRecord(ContinuityError):
    """A required transition, Scar, or Replay record could not be decoded."""


class ContinuityIntegrityError(ContinuityError):
    """A decoded continuity record failed structural or cryptographic validation."""


class ReplayPersistenceError(ContinuityError):
    """A Replay receipt could not be durably published."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def scar_digest(scar: dict[str, Any]) -> str:
    unhashed = dict(scar)
    unhashed.pop("scar_sha512", None)
    return hashlib.sha512(canonical_bytes(unhashed)).hexdigest()


def replay_digest(receipt: dict[str, Any]) -> str:
    unhashed = dict(receipt)
    unhashed.pop("replay_sha512", None)
    return hashlib.sha512(canonical_bytes(unhashed)).hexdigest()


def _valid_time(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return "T" in value and parsed.tzinfo is not None


def _validate_exact_object(value: Any, fields: set[str], label: str, errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return False
    missing = sorted(fields - set(value))
    extra = sorted(set(value) - fields)
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} has unexpected fields: {', '.join(extra)}")
    return not missing and not extra


def _validate_unique_refs(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return
    if any(not isinstance(item, str) or not item for item in value):
        errors.append(f"{label} must contain non-empty strings")
    if len(value) != len(set(value)):
        errors.append(f"{label} must contain unique references")


def validate_scar(scar: Any) -> list[str]:
    errors: list[str] = []
    if not _validate_exact_object(scar, SCAR_FIELDS, "Scar", errors):
        return errors

    if scar["scar_version"] != "v40-candidate.1":
        errors.append("scar_version mismatch")
    for field, pattern in (
        ("scar_id", SCAR_ID_PATTERN),
        ("contract_ref", CONTRACT_ID_PATTERN),
        ("contract_instance_id", CONTRACT_INSTANCE_ID_PATTERN),
        ("terminal_event_id", EVENT_ID_PATTERN),
    ):
        if not isinstance(scar[field], str) or pattern.fullmatch(scar[field]) is None:
            errors.append(f"{field} malformed")
    for field in ("route_id", "route_lock", "canonical_binding_ref"):
        if not isinstance(scar[field], str) or len(scar[field]) < 3:
            errors.append(f"{field} must be a non-empty binding")
    if not isinstance(scar["terminal_event_sequence"], int) or isinstance(scar["terminal_event_sequence"], bool) or scar["terminal_event_sequence"] < 1:
        errors.append("terminal_event_sequence must be a positive integer")
    for field in ("terminal_event_sha512", "transition_ledger_head_sha512", "scar_sha512"):
        if not isinstance(scar[field], str) or HASH_PATTERN.fullmatch(scar[field]) is None:
            errors.append(f"{field} invalid")
    if not _valid_time(scar["recorded_at_utc"]):
        errors.append("recorded_at_utc invalid")
    if scar["authority_state"] != "NONE":
        errors.append("authority_state must remain NONE")
    if scar["human_gate_state"] != "ACTIVE":
        errors.append("human_gate_state must remain ACTIVE")
    if scar["scar_class"] not in SCAR_CLASSES:
        errors.append("scar_class invalid")
    if scar["stop_class"] not in STOP_CLASSES:
        errors.append("stop_class invalid")
    for field in ("trigger", "reason"):
        if not isinstance(scar[field], str) or not scar[field].strip():
            errors.append(f"{field} must be a non-empty string")

    evidence = scar["evidence_boundary"]
    if _validate_exact_object(evidence, EVIDENCE_BOUNDARY_FIELDS, "evidence_boundary", errors):
        if evidence["boundary_state"] not in EVIDENCE_BOUNDARY_STATES:
            errors.append("evidence_boundary.boundary_state invalid")
        for field in (
            "available_evidence_refs",
            "missing_evidence_refs",
            "contradiction_refs",
            "invalid_evidence_refs",
            "scope_exclusions",
        ):
            _validate_unique_refs(evidence[field], f"evidence_boundary.{field}", errors)
        if not isinstance(evidence["boundary_reason"], str) or not evidence["boundary_reason"].strip():
            errors.append("evidence_boundary.boundary_reason must be non-empty")
        if evidence["evidence_time_utc"] is not None and not _valid_time(evidence["evidence_time_utc"]):
            errors.append("evidence_boundary.evidence_time_utc invalid")

    analysis = scar["analysis_state"]
    if _validate_exact_object(analysis, ANALYSIS_STATE_FIELDS, "analysis_state", errors):
        if analysis["inquiry_ref"] is not None and not isinstance(analysis["inquiry_ref"], str):
            errors.append("analysis_state.inquiry_ref must be a string or null")
        for field in (
            "claim_refs",
            "unresolved_claim_refs",
            "eliminated_world_refs",
            "surviving_world_refs",
            "function_participation_refs",
            "last_supported_conclusion_refs",
        ):
            _validate_unique_refs(analysis[field], f"analysis_state.{field}", errors)
        if not isinstance(analysis["state_summary"], str) or not analysis["state_summary"].strip():
            errors.append("analysis_state.state_summary must be non-empty")

    continuation = scar["continuation"]
    if _validate_exact_object(continuation, CONTINUATION_FIELDS, "continuation", errors):
        if not isinstance(continuation["replay_eligible"], bool):
            errors.append("continuation.replay_eligible must be boolean")
        for field in ("replay_blockers", "replay_preconditions"):
            _validate_unique_refs(continuation[field], f"continuation.{field}", errors)
        if continuation["new_contract_required"] is not True:
            errors.append("continuation.new_contract_required must be true")
        if continuation["continuation_ref"] is not None:
            errors.append("Scar continuation_ref must remain null")
        if continuation["human_gate_decision_required"] is not True:
            errors.append("continuation.human_gate_decision_required must be true")

    _validate_unique_refs(scar["provenance_refs"], "provenance_refs", errors)
    if isinstance(scar["scar_sha512"], str) and HASH_PATTERN.fullmatch(scar["scar_sha512"]):
        if scar_digest(scar) != scar["scar_sha512"]:
            errors.append("scar_sha512 mismatch")
    return errors


def _validate_context_items(value: Any, label: str, *, unavailable: bool, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return
    canonical_items = [canonical_bytes(item) for item in value]
    if len(canonical_items) != len(set(canonical_items)):
        errors.append(f"{label} must contain unique items")
    required = {"context_class", "ref", "reason"} if unavailable else {"context_class", "ref"}
    for index, item in enumerate(value):
        item_label = f"{label}[{index}]"
        if not _validate_exact_object(item, required, item_label, errors):
            continue
        if item["context_class"] not in CONTEXT_CLASSES:
            errors.append(f"{item_label}.context_class invalid")
        if unavailable:
            if item["ref"] is not None and (not isinstance(item["ref"], str) or not item["ref"]):
                errors.append(f"{item_label}.ref must be a non-empty string or null")
            if not isinstance(item["reason"], str) or not item["reason"].strip():
                errors.append(f"{item_label}.reason must be non-empty")
        elif not isinstance(item["ref"], str) or not item["ref"]:
            errors.append(f"{item_label}.ref must be non-empty")


def validate_replay_receipt(receipt: Any) -> list[str]:
    errors: list[str] = []
    if not _validate_exact_object(receipt, REPLAY_FIELDS, "Replay receipt", errors):
        return errors
    if receipt["replay_version"] != "v40-candidate.1":
        errors.append("replay_version mismatch")
    if not isinstance(receipt["replay_id"], str) or REPLAY_ID_PATTERN.fullmatch(receipt["replay_id"]) is None:
        errors.append("replay_id malformed")
    if not isinstance(receipt["replay_sequence"], int) or isinstance(receipt["replay_sequence"], bool) or receipt["replay_sequence"] < 1:
        errors.append("replay_sequence must be a positive integer")
    decision_of = receipt["decision_of_replay_id"]
    if decision_of is not None and (not isinstance(decision_of, str) or REPLAY_ID_PATTERN.fullmatch(decision_of) is None):
        errors.append("decision_of_replay_id malformed")
    for field in ("requested_at_utc", "prepared_at_utc"):
        if not _valid_time(receipt[field]):
            errors.append(f"{field} invalid")
    if not isinstance(receipt["scar_ref"], str) or SCAR_ID_PATTERN.fullmatch(receipt["scar_ref"]) is None:
        errors.append("scar_ref malformed")
    if not isinstance(receipt["source_contract_ref"], str) or CONTRACT_ID_PATTERN.fullmatch(receipt["source_contract_ref"]) is None:
        errors.append("source_contract_ref malformed")
    if not isinstance(receipt["source_contract_instance_id"], str) or CONTRACT_INSTANCE_ID_PATTERN.fullmatch(receipt["source_contract_instance_id"]) is None:
        errors.append("source_contract_instance_id malformed")
    if not isinstance(receipt["terminal_event_id"], str) or EVENT_ID_PATTERN.fullmatch(receipt["terminal_event_id"]) is None:
        errors.append("terminal_event_id malformed")
    for field in ("source_route_id", "source_route_lock", "source_canonical_binding_ref"):
        if not isinstance(receipt[field], str) or len(receipt[field]) < 3:
            errors.append(f"{field} invalid")
    current_binding = receipt["current_canonical_binding_ref"]
    if current_binding is not None and (not isinstance(current_binding, str) or len(current_binding) < 3):
        errors.append("current_canonical_binding_ref invalid")
    for field in (
        "scar_sha512",
        "terminal_event_sha512",
        "transition_ledger_head_sha512",
        "scar_ledger_sha512",
        "replay_sha512",
    ):
        if not isinstance(receipt[field], str) or HASH_PATTERN.fullmatch(receipt[field]) is None:
            errors.append(f"{field} invalid")
    previous = receipt["previous_replay_sha512"]
    if previous is not None and (not isinstance(previous, str) or HASH_PATTERN.fullmatch(previous) is None):
        errors.append("previous_replay_sha512 invalid")
    if receipt["canonical_comparison"] not in CANONICAL_COMPARISONS:
        errors.append("canonical_comparison invalid")
    if receipt["authority_state"] != "NONE":
        errors.append("authority_state must remain NONE")
    if receipt["status"] not in REPLAY_STATUSES:
        errors.append("status invalid")
    _validate_context_items(receipt["restored_context"], "restored_context", unavailable=False, errors=errors)
    _validate_context_items(receipt["unavailable_context"], "unavailable_context", unavailable=True, errors=errors)

    proposal = receipt["continuation_proposal"]
    if _validate_exact_object(proposal, CONTINUATION_PROPOSAL_FIELDS, "continuation_proposal", errors):
        if not isinstance(proposal["proposed_route_id"], str) or len(proposal["proposed_route_id"]) < 3:
            errors.append("continuation_proposal.proposed_route_id invalid")
        for field in ("proposed_scope", "proposed_completion_criteria", "required_evidence_refs"):
            _validate_unique_refs(proposal[field], f"continuation_proposal.{field}", errors)
        if proposal["new_contract_required"] is not True:
            errors.append("continuation_proposal.new_contract_required must be true")
        if proposal["new_contract_ref"] is not None or proposal["new_contract_instance_id"] is not None:
            errors.append("Replay cannot create a new contract or contract instance")
        continuation_ref = proposal["continuation_ref"]
        if continuation_ref is not None and (
            not isinstance(continuation_ref, str) or CONTINUATION_ID_PATTERN.fullmatch(continuation_ref) is None
        ):
            errors.append("continuation_proposal.continuation_ref malformed")

    gate = receipt["human_gate"]
    if _validate_exact_object(gate, HUMAN_GATE_FIELDS, "human_gate", errors):
        if gate["state"] != "ACTIVE":
            errors.append("human_gate.state must remain ACTIVE")
        if gate["decision"] not in {"PENDING", "APPROVED", "DENIED"}:
            errors.append("human_gate.decision invalid")
        if gate["decision_ref"] is not None and not isinstance(gate["decision_ref"], str):
            errors.append("human_gate.decision_ref must be string or null")
        if gate["decided_at_utc"] is not None and not _valid_time(gate["decided_at_utc"]):
            errors.append("human_gate.decided_at_utc invalid")
        if gate["decision_owner"] not in {None, "HUMAN"}:
            errors.append("human_gate.decision_owner invalid")

    preparation_statuses = {"PREPARED", "BLOCKED", "HUMAN_GATE_REVIEW"}
    if receipt["status"] in preparation_statuses:
        if decision_of is not None:
            errors.append("preparation receipt decision_of_replay_id must be null")
        if isinstance(proposal, dict) and proposal.get("continuation_ref") is not None:
            errors.append("preparation receipt continuation_ref must be null")
        if isinstance(gate, dict) and any(
            (
                gate.get("decision") != "PENDING",
                gate.get("decision_ref") is not None,
                gate.get("decided_at_utc") is not None,
                gate.get("decision_owner") is not None,
            )
        ):
            errors.append("preparation receipt cannot contain a Human Gate decision")
    if receipt["status"] == "HUMAN_GATE_REVIEW" and receipt["canonical_comparison"] != "UNCHANGED":
        errors.append("HUMAN_GATE_REVIEW requires unchanged canonical binding")
    if receipt["status"] in {"AUTHORIZED_NEW_CONTRACT_REQUIRED", "DENIED"}:
        if decision_of is None:
            errors.append("decision receipt must reference its preparation receipt")
        expected_decision = "APPROVED" if receipt["status"] == "AUTHORIZED_NEW_CONTRACT_REQUIRED" else "DENIED"
        if not isinstance(gate, dict) or any(
            (
                gate.get("decision") != expected_decision,
                not isinstance(gate.get("decision_ref"), str) or not gate.get("decision_ref", "").strip(),
                not _valid_time(gate.get("decided_at_utc")),
                gate.get("decision_owner") != "HUMAN",
            )
        ):
            errors.append("decision receipt requires explicit human-owned decision metadata")
    if receipt["status"] == "AUTHORIZED_NEW_CONTRACT_REQUIRED":
        continuation_ref = proposal.get("continuation_ref") if isinstance(proposal, dict) else None
        if not isinstance(continuation_ref, str) or CONTINUATION_ID_PATTERN.fullmatch(continuation_ref) is None:
            errors.append("authorized Replay requires a continuation_ref")
        if receipt["canonical_comparison"] != "UNCHANGED":
            errors.append("authorized Replay requires unchanged canonical binding")
    if receipt["status"] == "DENIED" and isinstance(proposal, dict) and proposal.get("continuation_ref") is not None:
        errors.append("denied Replay cannot contain a continuation_ref")
    if isinstance(receipt["replay_sha512"], str) and HASH_PATTERN.fullmatch(receipt["replay_sha512"]):
        if replay_digest(receipt) != receipt["replay_sha512"]:
            errors.append("replay_sha512 mismatch")
    return errors


def publish_no_overwrite(temporary: Path, target: Path) -> None:
    """Publish a complete file atomically without permitting replacement."""

    os.link(temporary, target)
    temporary.unlink()
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    directory_fd = os.open(target.parent, flags)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def load_transition_ledger(
    ledger_dir: Path,
    contract_ref: str,
    contract_instance_id: str,
    route_lock: str,
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    event_ids: set[str] = set()
    expected_sequence = 1
    expected_previous = None
    for path in sorted(Path(ledger_dir).glob("*.json")):
        try:
            event = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise UnreadableContinuityRecord(f"unreadable transition witness {path.name}: {exc}") from exc
        errors = validate_event(event)
        if errors:
            raise ContinuityIntegrityError(f"invalid transition witness {path.name}: {'; '.join(errors)}")
        if event["sequence"] != expected_sequence:
            raise ContinuityIntegrityError(
                f"transition sequence gap or rollback at {path.name}: expected {expected_sequence}, got {event['sequence']}"
            )
        if not path.name.startswith(f"{expected_sequence:06d}_"):
            raise ContinuityIntegrityError(f"transition filename sequence mismatch: {path.name}")
        if event["previous_event_sha512"] != expected_previous:
            raise ContinuityIntegrityError(f"transition previous-event hash mismatch at {path.name}")
        if event["contract_ref"] != contract_ref or event["contract_instance_id"] != contract_instance_id:
            raise ContinuityIntegrityError(f"transition contract binding mismatch at {path.name}")
        if event["route_lock"] != route_lock:
            raise ContinuityIntegrityError(f"transition route-lock mismatch at {path.name}")
        if event["event_id"] in event_ids:
            raise ContinuityIntegrityError(f"duplicate transition event identifier: {event['event_id']}")
        event_ids.add(event["event_id"])
        events.append(event)
        expected_previous = event["event_sha512"]
        expected_sequence += 1
    return events


def scar_ledger_digest(scars: Iterable[dict[str, Any]]) -> str:
    ordered = sorted(scars, key=lambda scar: (scar["terminal_event_sequence"], scar["scar_id"]))
    return hashlib.sha512(canonical_bytes(ordered)).hexdigest()


def detect_repeating_thirds_marker(value: Any) -> dict[str, Any] | None:
    """Detect only an explicit structured thirds marker; never infer one from content."""

    if not isinstance(value, dict) or value.get("marker_kind") not in THIRDS_MARKER_KINDS:
        return None
    required = {"marker_kind", "condition_class", "source_ref", "observation_time_utc", "evidence_refs"}
    missing = sorted(required - set(value))
    extra = sorted(set(value) - required)
    if missing or extra:
        raise ContinuityError(f"malformed thirds marker; missing={missing}; extra={extra}")
    condition = value["condition_class"]
    if condition not in THIRDS_CONDITION_TO_SCAR_CLASS:
        raise ContinuityError(f"unsupported thirds condition_class: {condition!r}")
    if not isinstance(value["source_ref"], str) or not value["source_ref"].strip():
        raise ContinuityError("thirds marker source_ref must be a non-empty string")
    if not _valid_time(value["observation_time_utc"]):
        raise ContinuityError("thirds marker observation_time_utc invalid")
    marker_errors: list[str] = []
    _validate_unique_refs(value["evidence_refs"], "thirds marker evidence_refs", marker_errors)
    if marker_errors:
        raise ContinuityError("; ".join(marker_errors))
    return {
        "detected": True,
        "marker_kind": value["marker_kind"],
        "condition_class": condition,
        "source_ref": value["source_ref"],
        "observation_time_utc": value["observation_time_utc"],
        "evidence_refs": list(value["evidence_refs"]),
        "self_observation": "SUCCESSFUL",
        "confidence_interpretation": "NOT_CONFIDENCE",
        "required_scar_class": THIRDS_CONDITION_TO_SCAR_CLASS[condition],
        "termination_required": True,
        "replay_required_for_later_continuation": True,
    }


def reconcile_scars(
    transition_ledger_dir: Path,
    scar_ledger_dir: Path,
    contract_ref: str,
    contract_instance_id: str,
    route_lock: str,
    canonical_binding_ref: str,
    *,
    route_id: str | None = None,
) -> dict[str, Any]:
    """Reconcile every terminal transition and Scar without mutating either ledger."""

    selected_route_id = route_id or route_lock
    result: dict[str, Any] = {
        "state": "UNREADABLE",
        "terminal_event_ids": [],
        "scar_ids": [],
        "missing_terminal_event_ids": [],
        "orphan_scar_ids": [],
        "duplicate_terminal_event_ids": [],
        "binding_mismatch_scar_ids": [],
        "errors": [],
        "scar_ledger_sha512": None,
    }
    try:
        events = load_transition_ledger(
            transition_ledger_dir,
            contract_ref,
            contract_instance_id,
            route_lock,
        )
    except UnreadableContinuityRecord as exc:
        result["errors"].append(str(exc))
        return result
    except ContinuityIntegrityError as exc:
        result["state"] = "INTEGRITY_FAILURE"
        result["errors"].append(str(exc))
        return result

    scars: list[dict[str, Any]] = []
    for path in sorted(Path(scar_ledger_dir).glob("*.json")):
        try:
            scar = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            result["errors"].append(f"unreadable Scar {path.name}: {exc}")
            return result
        errors = validate_scar(scar)
        if errors:
            result["state"] = "INTEGRITY_FAILURE"
            result["errors"].append(f"invalid Scar {path.name}: {'; '.join(errors)}")
            return result
        if not path.name.startswith(f"{scar['terminal_event_sequence']:06d}_{scar['scar_id']}"):
            result["state"] = "INTEGRITY_FAILURE"
            result["errors"].append(f"Scar filename binding mismatch: {path.name}")
            return result
        scars.append(scar)

    result["scar_ledger_sha512"] = scar_ledger_digest(scars)
    terminal_events = {
        event["event_id"]: event
        for event in events
        if event["to_state"] == "STOPPED" and event["scar_required"] is True
    }
    all_events = {event["event_id"]: event for event in events}
    result["terminal_event_ids"] = sorted(terminal_events)
    result["scar_ids"] = sorted(scar["scar_id"] for scar in scars)

    scar_ids: set[str] = set()
    scars_by_event: dict[str, list[dict[str, Any]]] = {}
    for scar in scars:
        if scar["scar_id"] in scar_ids:
            result["state"] = "DUPLICATE_SCAR"
            result["errors"].append(f"duplicate Scar identifier: {scar['scar_id']}")
            return result
        scar_ids.add(scar["scar_id"])
        scars_by_event.setdefault(scar["terminal_event_id"], []).append(scar)

    duplicate_events = sorted(event_id for event_id, values in scars_by_event.items() if len(values) > 1)
    if duplicate_events:
        result["state"] = "DUPLICATE_SCAR"
        result["duplicate_terminal_event_ids"] = duplicate_events
        result["errors"].append(f"multiple Scars bind terminal events: {duplicate_events}")
        return result

    mismatch_ids: list[str] = []
    orphan_ids: list[str] = []
    ledger_head = events[-1]["event_sha512"] if events else None
    for scar in scars:
        event = all_events.get(scar["terminal_event_id"])
        if event is None:
            orphan_ids.append(scar["scar_id"])
            continue
        if event["event_id"] not in terminal_events:
            mismatch_ids.append(scar["scar_id"])
            continue
        if any(
            (
                scar["contract_ref"] != contract_ref,
                scar["contract_instance_id"] != contract_instance_id,
                scar["route_id"] != selected_route_id,
                scar["route_lock"] != route_lock,
                scar["canonical_binding_ref"] != canonical_binding_ref,
                scar["terminal_event_sequence"] != event["sequence"],
                scar["terminal_event_sha512"] != event["event_sha512"],
                scar["transition_ledger_head_sha512"] != ledger_head,
                scar["stop_class"] != event["stop_class"],
                scar["trigger"] != event["trigger"],
                scar["reason"] != event["scar_reason"],
            )
        ):
            mismatch_ids.append(scar["scar_id"])

    if mismatch_ids:
        result["state"] = "BINDING_MISMATCH"
        result["binding_mismatch_scar_ids"] = sorted(mismatch_ids)
        result["errors"].append(f"Scar bindings disagree with terminal witnesses: {sorted(mismatch_ids)}")
        return result
    if orphan_ids:
        result["state"] = "ORPHAN_SCAR"
        result["orphan_scar_ids"] = sorted(orphan_ids)
        result["errors"].append(f"Scars do not resolve to transition witnesses: {sorted(orphan_ids)}")
        return result

    missing = sorted(set(terminal_events) - set(scars_by_event))
    if missing:
        result["state"] = "MISSING_SCAR"
        result["missing_terminal_event_ids"] = missing
        result["errors"].append(f"terminal witnesses lack Scars: {missing}")
        return result

    result["state"] = "COMPLETE"
    return result


class ScarLedgerWriter:
    """Publish one immutable Scar for an explicitly selected terminal witness."""

    def __init__(
        self,
        scar_ledger_dir: Path,
        transition_ledger_dir: Path,
        contract_ref: str,
        contract_instance_id: str,
        route_lock: str,
        canonical_binding_ref: str,
        *,
        route_id: str | None = None,
        clock: Callable[[], str] = utc_now,
        publisher: Callable[[Path, Path], None] = publish_no_overwrite,
    ) -> None:
        self.scar_ledger_dir = Path(scar_ledger_dir)
        self.transition_ledger_dir = Path(transition_ledger_dir)
        self.contract_ref = contract_ref
        self.contract_instance_id = contract_instance_id
        self.route_id = route_id or route_lock
        self.route_lock = route_lock
        self.canonical_binding_ref = canonical_binding_ref
        self.clock = clock
        self.publisher = publisher
        self.scar_ledger_dir.mkdir(parents=True, exist_ok=True)
        self.scars: list[dict[str, Any]] = []
        self.scar_ids: set[str] = set()
        self.terminal_event_ids: set[str] = set()
        self._load_and_validate_scars()

    def _load_and_validate_scars(self) -> None:
        scars: list[dict[str, Any]] = []
        scar_ids: set[str] = set()
        terminal_event_ids: set[str] = set()
        for path in sorted(self.scar_ledger_dir.glob("*.json")):
            try:
                scar = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ContinuityError(f"invalid Scar file {path.name}: {exc}") from exc
            errors = validate_scar(scar)
            if errors:
                raise ContinuityError(f"invalid Scar file {path.name}: {'; '.join(errors)}")
            if not path.name.startswith(f"{scar['terminal_event_sequence']:06d}_{scar['scar_id']}"):
                raise ContinuityError(f"Scar filename binding mismatch: {path.name}")
            if scar["contract_ref"] != self.contract_ref or scar["contract_instance_id"] != self.contract_instance_id:
                raise ContinuityError(f"Scar contract binding mismatch: {path.name}")
            if scar["route_id"] != self.route_id or scar["route_lock"] != self.route_lock:
                raise ContinuityError(f"Scar route binding mismatch: {path.name}")
            if scar["canonical_binding_ref"] != self.canonical_binding_ref:
                raise ContinuityError(f"Scar canonical binding mismatch: {path.name}")
            if scar["scar_id"] in scar_ids:
                raise ContinuityError(f"duplicate Scar identifier: {scar['scar_id']}")
            if scar["terminal_event_id"] in terminal_event_ids:
                raise ContinuityError(f"duplicate Scar terminal-event binding: {scar['terminal_event_id']}")
            scar_ids.add(scar["scar_id"])
            terminal_event_ids.add(scar["terminal_event_id"])
            scars.append(scar)
        self.scars = scars
        self.scar_ids = scar_ids
        self.terminal_event_ids = terminal_event_ids

    def append(
        self,
        terminal_event_id: str,
        *,
        scar_class: str,
        evidence_boundary: dict[str, Any],
        analysis_state: dict[str, Any],
        continuation: dict[str, Any],
        provenance_refs: Iterable[str] = (),
        scar_id: str | None = None,
    ) -> dict[str, Any]:
        events = load_transition_ledger(
            self.transition_ledger_dir,
            self.contract_ref,
            self.contract_instance_id,
            self.route_lock,
        )
        event_by_id = {event["event_id"]: event for event in events}
        event = event_by_id.get(terminal_event_id)
        if event is None:
            raise ContinuityError(f"terminal transition not found: {terminal_event_id}")
        if event["to_state"] != "STOPPED" or event["scar_required"] is not True:
            raise ContinuityError("Scar requires a terminal STOPPED transition with scar_required=true")
        if terminal_event_id in self.terminal_event_ids:
            raise ContinuityError(f"duplicate Scar terminal-event binding: {terminal_event_id}")
        if not events or event["event_sha512"] != events[-1]["event_sha512"]:
            raise ContinuityError("terminal transition is not the transition-ledger head")

        selected_id = scar_id or f"SC-{self.contract_instance_id.removeprefix('OCI-')}-{event['sequence']:06d}"
        if selected_id in self.scar_ids:
            raise ContinuityError(f"duplicate Scar identifier: {selected_id}")
        scar = {
            "scar_version": "v40-candidate.1",
            "scar_id": selected_id,
            "contract_ref": self.contract_ref,
            "contract_instance_id": self.contract_instance_id,
            "route_id": self.route_id,
            "route_lock": self.route_lock,
            "canonical_binding_ref": self.canonical_binding_ref,
            "terminal_event_id": event["event_id"],
            "terminal_event_sequence": event["sequence"],
            "terminal_event_sha512": event["event_sha512"],
            "transition_ledger_head_sha512": events[-1]["event_sha512"],
            "recorded_at_utc": self.clock(),
            "authority_state": "NONE",
            "human_gate_state": "ACTIVE",
            "scar_class": scar_class,
            "stop_class": event["stop_class"],
            "trigger": event["trigger"],
            "reason": event["scar_reason"],
            "evidence_boundary": evidence_boundary,
            "analysis_state": analysis_state,
            "continuation": continuation,
            "provenance_refs": list(provenance_refs),
        }
        scar["scar_sha512"] = scar_digest(scar)
        errors = validate_scar(scar)
        if errors:
            raise ContinuityError("invalid Scar: " + "; ".join(errors))

        target = self.scar_ledger_dir / f"{event['sequence']:06d}_{selected_id}.json"
        temporary = self.scar_ledger_dir / f".{target.name}.tmp-{os.getpid()}"
        if target.exists():
            raise ContinuityError(f"Scar overwrite refused: {target.name}")
        try:
            with temporary.open("x", encoding="utf-8") as handle:
                handle.write(json.dumps(scar, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self.publisher(temporary, target)
        except OSError as exc:
            if temporary.exists():
                temporary.unlink()
            raise ScarPersistenceError(f"unable to persist Scar: {exc}") from exc

        self._load_and_validate_scars()
        return scar


class ReplayLedgerWriter:
    """Append immutable, ordered, SHA-512-chained Replay receipts."""

    def __init__(
        self,
        replay_ledger_dir: Path,
        source_contract_ref: str,
        source_contract_instance_id: str,
        *,
        publisher: Callable[[Path, Path], None] = publish_no_overwrite,
    ) -> None:
        self.replay_ledger_dir = Path(replay_ledger_dir)
        self.source_contract_ref = source_contract_ref
        self.source_contract_instance_id = source_contract_instance_id
        self.publisher = publisher
        self.replay_ledger_dir.mkdir(parents=True, exist_ok=True)
        self.receipts: list[dict[str, Any]] = []
        self.sequence = 0
        self.head_sha512: str | None = None
        self._load_and_validate()

    @staticmethod
    def _validate_decision_binding(decision: dict[str, Any], preparation: dict[str, Any]) -> None:
        inherited_fields = REPLAY_FIELDS - {
            "replay_id",
            "replay_sequence",
            "decision_of_replay_id",
            "human_gate",
            "status",
            "previous_replay_sha512",
            "replay_sha512",
            "continuation_proposal",
        }
        mismatches = sorted(field for field in inherited_fields if decision[field] != preparation[field])
        decision_proposal = dict(decision["continuation_proposal"])
        preparation_proposal = dict(preparation["continuation_proposal"])
        decision_proposal["continuation_ref"] = None
        if decision_proposal != preparation_proposal:
            mismatches.append("continuation_proposal")
        if mismatches:
            raise ContinuityIntegrityError(f"Replay decision binding mismatch: {mismatches}")

    def _load_and_validate(self) -> None:
        receipts: list[dict[str, Any]] = []
        by_id: dict[str, dict[str, Any]] = {}
        decided: set[str] = set()
        expected_sequence = 1
        expected_previous = None
        for path in sorted(self.replay_ledger_dir.glob("*.json")):
            try:
                receipt = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise UnreadableContinuityRecord(f"unreadable Replay receipt {path.name}: {exc}") from exc
            errors = validate_replay_receipt(receipt)
            if errors:
                raise ContinuityIntegrityError(f"invalid Replay receipt {path.name}: {'; '.join(errors)}")
            if receipt["replay_sequence"] != expected_sequence:
                raise ContinuityIntegrityError(
                    f"Replay sequence gap or rollback at {path.name}: expected {expected_sequence}, got {receipt['replay_sequence']}"
                )
            if not path.name.startswith(f"{expected_sequence:06d}_{receipt['replay_id']}"):
                raise ContinuityIntegrityError(f"Replay filename sequence mismatch: {path.name}")
            if receipt["previous_replay_sha512"] != expected_previous:
                raise ContinuityIntegrityError(f"Replay previous-receipt hash mismatch at {path.name}")
            if receipt["source_contract_ref"] != self.source_contract_ref or receipt["source_contract_instance_id"] != self.source_contract_instance_id:
                raise ContinuityIntegrityError(f"Replay source contract binding mismatch at {path.name}")
            if receipt["replay_id"] in by_id:
                raise ContinuityIntegrityError(f"duplicate Replay identifier: {receipt['replay_id']}")
            decision_of = receipt["decision_of_replay_id"]
            if decision_of is not None:
                preparation = by_id.get(decision_of)
                if preparation is None or preparation["status"] != "HUMAN_GATE_REVIEW":
                    raise ContinuityIntegrityError(f"Replay decision does not resolve to a review receipt: {decision_of}")
                if decision_of in decided:
                    raise ContinuityIntegrityError(f"Replay preparation already has a decision: {decision_of}")
                self._validate_decision_binding(receipt, preparation)
                decided.add(decision_of)
            by_id[receipt["replay_id"]] = receipt
            receipts.append(receipt)
            expected_previous = receipt["replay_sha512"]
            expected_sequence += 1
        self.receipts = receipts
        self.sequence = expected_sequence - 1
        self.head_sha512 = expected_previous

    def append(self, payload: dict[str, Any]) -> dict[str, Any]:
        sequence = self.sequence + 1
        default_id = f"RP-{self.source_contract_instance_id.removeprefix('OCI-')}-{sequence:06d}"
        replay_id = payload.get("replay_id", default_id)
        protected = {"replay_version", "replay_sequence", "previous_replay_sha512", "replay_sha512"}
        if protected & set(payload):
            raise ContinuityError(f"caller cannot override Replay integrity fields: {sorted(protected & set(payload))}")
        if replay_id in {receipt["replay_id"] for receipt in self.receipts}:
            raise ContinuityError(f"duplicate Replay identifier: {replay_id}")
        receipt = {
            "replay_version": "v40-candidate.1",
            "replay_id": replay_id,
            "replay_sequence": sequence,
            "previous_replay_sha512": self.head_sha512,
            **{key: value for key, value in payload.items() if key != "replay_id"},
        }
        receipt["replay_sha512"] = replay_digest(receipt)
        errors = validate_replay_receipt(receipt)
        if errors:
            raise ContinuityError("invalid Replay receipt: " + "; ".join(errors))

        target = self.replay_ledger_dir / f"{sequence:06d}_{replay_id}.json"
        temporary = self.replay_ledger_dir / f".{target.name}.tmp-{os.getpid()}"
        if target.exists():
            raise ContinuityError(f"Replay receipt overwrite refused: {target.name}")
        try:
            with temporary.open("x", encoding="utf-8") as handle:
                handle.write(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self.publisher(temporary, target)
        except OSError as exc:
            if temporary.exists():
                temporary.unlink()
            raise ReplayPersistenceError(f"unable to persist Replay receipt: {exc}") from exc
        self._load_and_validate()
        return receipt


class MinimumReplay:
    """Prepare non-executable Replay receipts from explicit continuity records."""

    def __init__(
        self,
        transition_ledger_dir: Path,
        scar_ledger_dir: Path,
        replay_ledger_dir: Path,
        contract_ref: str,
        contract_instance_id: str,
        route_lock: str,
        canonical_binding_ref: str,
        *,
        route_id: str | None = None,
        clock: Callable[[], str] = utc_now,
        replay_publisher: Callable[[Path, Path], None] = publish_no_overwrite,
    ) -> None:
        self.transition_ledger_dir = Path(transition_ledger_dir)
        self.scar_ledger_dir = Path(scar_ledger_dir)
        self.contract_ref = contract_ref
        self.contract_instance_id = contract_instance_id
        self.route_id = route_id or route_lock
        self.route_lock = route_lock
        self.canonical_binding_ref = canonical_binding_ref
        self.clock = clock
        self.writer = ReplayLedgerWriter(
            replay_ledger_dir,
            contract_ref,
            contract_instance_id,
            publisher=replay_publisher,
        )

    def _validated_scar(self, scar_ref: str) -> tuple[dict[str, Any], dict[str, Any]]:
        reconciliation = reconcile_scars(
            self.transition_ledger_dir,
            self.scar_ledger_dir,
            self.contract_ref,
            self.contract_instance_id,
            self.route_lock,
            self.canonical_binding_ref,
            route_id=self.route_id,
        )
        if reconciliation["state"] != "COMPLETE":
            raise ContinuityError(f"Replay preparation requires COMPLETE Scar reconciliation; got {reconciliation['state']}")
        selected: dict[str, Any] | None = None
        for path in sorted(self.scar_ledger_dir.glob("*.json")):
            scar = json.loads(path.read_text(encoding="utf-8"))
            if scar["scar_id"] == scar_ref:
                selected = scar
                break
        if selected is None:
            raise ContinuityError(f"Replay Scar not found: {scar_ref}")
        return selected, reconciliation

    @staticmethod
    def _validate_context_coverage(restored: list[dict[str, Any]], unavailable: list[dict[str, Any]]) -> None:
        supplied = {item.get("context_class") for item in [*restored, *unavailable] if isinstance(item, dict)}
        missing = sorted(CONTEXT_CLASSES - supplied)
        if missing:
            raise ContinuityError(f"Replay context coverage incomplete: {missing}")

    def prepare(
        self,
        scar_ref: str,
        *,
        requested_at_utc: str,
        current_canonical_binding_ref: str | None,
        canonical_comparison: str,
        restored_context: list[dict[str, Any]],
        unavailable_context: list[dict[str, Any]],
        proposed_route_id: str,
        proposed_scope: Iterable[str],
        proposed_completion_criteria: Iterable[str],
        required_evidence_refs: Iterable[str],
    ) -> dict[str, Any]:
        if not _valid_time(requested_at_utc):
            raise ContinuityError("Replay requested_at_utc invalid")
        if canonical_comparison not in CANONICAL_COMPARISONS:
            raise ContinuityError("canonical comparison invalid")
        if canonical_comparison == "UNCHANGED" and current_canonical_binding_ref != self.canonical_binding_ref:
            raise ContinuityError("UNCHANGED canonical comparison disagrees with binding references")
        if canonical_comparison == "UNAVAILABLE" and current_canonical_binding_ref is not None:
            raise ContinuityError("UNAVAILABLE canonical comparison requires a null current binding")
        self._validate_context_coverage(restored_context, unavailable_context)
        scar, reconciliation = self._validated_scar(scar_ref)

        blocked = bool(
            scar["continuation"]["replay_eligible"] is not True
            or scar["continuation"]["replay_blockers"]
            or unavailable_context
            or canonical_comparison in {"DRIFTED", "UNAVAILABLE", "INVALID"}
        )
        if blocked:
            status = "BLOCKED"
        elif canonical_comparison == "ADVANCED_REVALIDATION_REQUIRED":
            status = "PREPARED"
        else:
            status = "HUMAN_GATE_REVIEW"
        payload = {
            "decision_of_replay_id": None,
            "requested_at_utc": requested_at_utc,
            "prepared_at_utc": self.clock(),
            "scar_ref": scar["scar_id"],
            "scar_sha512": scar["scar_sha512"],
            "source_contract_ref": self.contract_ref,
            "source_contract_instance_id": self.contract_instance_id,
            "source_route_id": self.route_id,
            "source_route_lock": self.route_lock,
            "terminal_event_id": scar["terminal_event_id"],
            "terminal_event_sha512": scar["terminal_event_sha512"],
            "transition_ledger_head_sha512": scar["transition_ledger_head_sha512"],
            "scar_ledger_sha512": reconciliation["scar_ledger_sha512"],
            "source_canonical_binding_ref": self.canonical_binding_ref,
            "current_canonical_binding_ref": current_canonical_binding_ref,
            "canonical_comparison": canonical_comparison,
            "authority_state": "NONE",
            "restored_context": list(restored_context),
            "unavailable_context": list(unavailable_context),
            "continuation_proposal": {
                "proposed_route_id": proposed_route_id,
                "proposed_scope": list(proposed_scope),
                "proposed_completion_criteria": list(proposed_completion_criteria),
                "required_evidence_refs": list(required_evidence_refs),
                "new_contract_required": True,
                "new_contract_ref": None,
                "new_contract_instance_id": None,
                "continuation_ref": None,
            },
            "human_gate": {
                "state": "ACTIVE",
                "decision": "PENDING",
                "decision_ref": None,
                "decided_at_utc": None,
                "decision_owner": None,
            },
            "status": status,
        }
        return self.writer.append(payload)

    def record_human_decision(
        self,
        preparation_replay_id: str,
        *,
        approved: bool,
        decision_ref: str,
        decided_at_utc: str,
        decision_owner: str,
    ) -> dict[str, Any]:
        """Append one explicit human decision without creating or activating a contract."""

        self.writer._load_and_validate()
        preparation = next(
            (receipt for receipt in self.writer.receipts if receipt["replay_id"] == preparation_replay_id),
            None,
        )
        if preparation is None or preparation["status"] != "HUMAN_GATE_REVIEW":
            raise ContinuityError("Human Gate decision requires an existing HUMAN_GATE_REVIEW receipt")
        if any(receipt["decision_of_replay_id"] == preparation_replay_id for receipt in self.writer.receipts):
            raise ContinuityError("Replay preparation already has an immutable Human Gate decision")
        if decision_owner != "HUMAN":
            raise ContinuityError("runtime-generated or non-human Replay approval is forbidden")
        if not isinstance(decision_ref, str) or not decision_ref.strip():
            raise ContinuityError("Human Gate decision requires a stable decision_ref")
        if not _valid_time(decided_at_utc):
            raise ContinuityError("Human Gate decided_at_utc invalid")

        payload = {
            key: json.loads(json.dumps(value))
            for key, value in preparation.items()
            if key
            not in {
                "replay_version",
                "replay_id",
                "replay_sequence",
                "decision_of_replay_id",
                "previous_replay_sha512",
                "replay_sha512",
                "human_gate",
                "status",
                "continuation_proposal",
            }
        }
        payload["decision_of_replay_id"] = preparation_replay_id
        payload["continuation_proposal"] = json.loads(json.dumps(preparation["continuation_proposal"]))
        payload["human_gate"] = {
            "state": "ACTIVE",
            "decision": "APPROVED" if approved else "DENIED",
            "decision_ref": decision_ref,
            "decided_at_utc": decided_at_utc,
            "decision_owner": "HUMAN",
        }
        if approved:
            next_sequence = self.writer.sequence + 1
            continuation_ref = (
                f"CONT-{self.contract_instance_id.removeprefix('OCI-')}-{next_sequence:06d}"
            )
            payload["continuation_proposal"]["continuation_ref"] = continuation_ref
            payload["status"] = "AUTHORIZED_NEW_CONTRACT_REQUIRED"
        else:
            payload["continuation_proposal"]["continuation_ref"] = None
            payload["status"] = "DENIED"
        return self.writer.append(payload)
