#!/usr/bin/env python3
"""Fail-closed transition witness writer for the v40 candidate control plane."""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


STATES = {"INITIALIZING", "ACTIVE", "HUMAN_GATE_REVIEW", "STOPPED", "COMPLETE"}
CONFORMANCE = {"UNKNOWN", "CONFORMING", "NONCONFORMING"}
EVENT_CLASSES = {"ACTIVATION", "ACTION_INTENT", "ACTION_RESULT", "AUDIT", "GATE_REQUEST", "GATE_DECISION", "COMPLETION", "STOP", "NO_CHANGE"}
AUTHORIZATIONS = {"CONTRACT_PERMITTED", "HUMAN_GATE_PENDING", "HUMAN_GATE_APPROVED", "HUMAN_GATE_DENIED", "REJECTED", "NOT_APPLICABLE"}
AUDIT_RESULTS = {"PASS", "FAIL", "NOT_INVOKED"}
STOP_CLASSES = {"CONTRACT_NONCONFORMANCE", "CANONICAL_BINDING_FAILURE", "ROUTE_DRIFT", "UNDECLARED_ACTION", "AUDIT_INTERRUPT", "TRANSITION_WITNESS_FAILURE", "COMPLETION_MISMATCH", "HUMAN_GATE_DENIED", "HUMAN_GATE_APPROVED_NEW_CONTRACT_REQUIRED", "LOGIC_FREEZE"}
ALLOWED_TRANSITIONS = {
    ("INITIALIZING", "INITIALIZING"),
    ("INITIALIZING", "ACTIVE"),
    ("INITIALIZING", "STOPPED"),
    ("ACTIVE", "ACTIVE"),
    ("ACTIVE", "HUMAN_GATE_REVIEW"),
    ("ACTIVE", "STOPPED"),
    ("ACTIVE", "COMPLETE"),
    ("HUMAN_GATE_REVIEW", "HUMAN_GATE_REVIEW"),
    ("HUMAN_GATE_REVIEW", "STOPPED"),
}
ACTION_PATTERN = re.compile(r"^[a-z][a-z0-9_.-]*$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{128}$")


class TransitionWitnessError(RuntimeError):
    """The transition ledger or requested witness is invalid."""


class WitnessPersistenceError(TransitionWitnessError):
    """A witness could not be durably published."""

    def __init__(self, message: str, emergency_record: dict):
        super().__init__(message)
        self.emergency_record = emergency_record


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def event_digest(event: dict) -> str:
    unhashed = dict(event)
    unhashed.pop("event_sha512", None)
    return hashlib.sha512(canonical_bytes(unhashed)).hexdigest()


def publish_no_overwrite(temporary: Path, target: Path) -> None:
    """Atomically rename a same-filesystem file and synchronize its directory."""

    if target.exists():
        raise FileExistsError(f"witness overwrite refused: {target.name}")
    os.rename(temporary, target)
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    directory_fd = os.open(target.parent, flags)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def validate_event(event: dict) -> list[str]:
    errors: list[str] = []
    required = {
        "event_version", "event_id", "contract_ref", "contract_instance_id", "sequence",
        "timestamp_utc", "event_class", "from_state", "to_state", "trigger", "action",
        "request_ref", "reason", "route_lock", "authorization", "participants", "evidence_refs",
        "conformance_before", "conformance_after", "audit_result", "human_gate_latched",
        "decision_ref", "previous_event_sha512", "event_sha512", "stop_class", "scar_required",
        "scar_reason",
    }
    missing = sorted(required - set(event))
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
        return errors
    if event["event_version"] != "v40-candidate.2":
        errors.append("event_version mismatch")
    if not re.fullmatch(r"TE-[A-Z0-9._-]+", str(event["event_id"])):
        errors.append("event_id malformed")
    if not re.fullmatch(r"OC-[A-Z0-9._-]+", str(event["contract_ref"])):
        errors.append("contract_ref malformed")
    if not re.fullmatch(r"OCI-[A-Z0-9._-]+", str(event["contract_instance_id"])):
        errors.append("contract_instance_id malformed")
    if not isinstance(event["sequence"], int) or event["sequence"] < 1:
        errors.append("sequence must be a positive integer")
    try:
        timestamp = datetime.fromisoformat(str(event["timestamp_utc"]).replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            errors.append("timestamp_utc must include a timezone")
    except ValueError:
        errors.append("timestamp_utc invalid")
    if event["event_class"] not in EVENT_CLASSES:
        errors.append("event_class invalid")
    if event["from_state"] not in STATES or event["to_state"] not in STATES:
        errors.append("state invalid")
    elif (event["from_state"], event["to_state"]) not in ALLOWED_TRANSITIONS:
        errors.append("state transition is not permitted")
    expected_class_transitions = {
        "ACTIVATION": {("INITIALIZING", "ACTIVE")},
        "ACTION_INTENT": {("ACTIVE", "ACTIVE")},
        "ACTION_RESULT": {("ACTIVE", "ACTIVE")},
        "GATE_REQUEST": {("ACTIVE", "HUMAN_GATE_REVIEW")},
        "GATE_DECISION": {("HUMAN_GATE_REVIEW", "STOPPED")},
        "COMPLETION": {("ACTIVE", "COMPLETE")},
        "STOP": {("INITIALIZING", "STOPPED"), ("ACTIVE", "STOPPED"), ("HUMAN_GATE_REVIEW", "STOPPED")},
        "NO_CHANGE": {("INITIALIZING", "INITIALIZING"), ("ACTIVE", "ACTIVE"), ("HUMAN_GATE_REVIEW", "HUMAN_GATE_REVIEW")},
    }
    allowed_for_class = expected_class_transitions.get(event["event_class"])
    if allowed_for_class is not None and (event["from_state"], event["to_state"]) not in allowed_for_class:
        errors.append("event class does not match state transition")
    if not str(event["trigger"]).strip() or not str(event["reason"]).strip():
        errors.append("trigger and reason are required")
    if event["action"] is not None and not ACTION_PATTERN.fullmatch(str(event["action"])):
        errors.append("action identifier invalid")
    if event["authorization"] not in AUTHORIZATIONS:
        errors.append("authorization invalid")
    if event["conformance_before"] not in CONFORMANCE or event["conformance_after"] not in CONFORMANCE:
        errors.append("conformance invalid")
    if event["audit_result"] not in AUDIT_RESULTS:
        errors.append("audit_result invalid")
    if event["previous_event_sha512"] is not None and not HASH_PATTERN.fullmatch(str(event["previous_event_sha512"])):
        errors.append("previous_event_sha512 invalid")
    if not HASH_PATTERN.fullmatch(str(event["event_sha512"])):
        errors.append("event_sha512 invalid")
    elif event_digest(event) != event["event_sha512"]:
        errors.append("event_sha512 mismatch")
    if event["stop_class"] is not None and event["stop_class"] not in STOP_CLASSES:
        errors.append("stop_class invalid")
    if event["to_state"] == "STOPPED":
        if event["stop_class"] not in STOP_CLASSES:
            errors.append("STOPPED event requires stop_class")
        if event["scar_required"] is not True:
            errors.append("STOPPED event requires Scar")
    if event["scar_required"] and not str(event["scar_reason"] or "").strip():
        errors.append("Scar-required event requires scar_reason")
    if not isinstance(event["participants"], list) or len(event["participants"]) != len(set(event["participants"])):
        errors.append("participants must be a unique array")
    if not isinstance(event["evidence_refs"], list) or len(event["evidence_refs"]) != len(set(event["evidence_refs"])):
        errors.append("evidence_refs must be a unique array")
    return errors


class TransitionWitnessWriter:
    """Append immutable, ordered, SHA-512-chained transition witnesses."""

    def __init__(
        self,
        ledger_dir: Path,
        contract_ref: str,
        contract_instance_id: str,
        route_lock: str,
        *,
        clock: Callable[[], str] = utc_now,
        publisher: Callable[[Path, Path], None] = publish_no_overwrite,
    ) -> None:
        self.ledger_dir = Path(ledger_dir)
        self.contract_ref = contract_ref
        self.contract_instance_id = contract_instance_id
        self.route_lock = route_lock
        self.clock = clock
        self.publisher = publisher
        self.sequence = 0
        self.head_sha512: str | None = None
        self.event_ids: set[str] = set()
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        self._load_and_validate()

    def _load_and_validate(self) -> None:
        expected_sequence = 1
        expected_previous = None
        for path in sorted(self.ledger_dir.glob("*.json")):
            try:
                event = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise TransitionWitnessError(f"invalid witness file {path.name}: {exc}") from exc
            errors = validate_event(event)
            if errors:
                raise TransitionWitnessError(f"invalid witness file {path.name}: {'; '.join(errors)}")
            if event["sequence"] != expected_sequence:
                raise TransitionWitnessError(f"sequence gap or rollback at {path.name}: expected {expected_sequence}, got {event['sequence']}")
            if not path.name.startswith(f"{expected_sequence:06d}_"):
                raise TransitionWitnessError(f"filename sequence mismatch: {path.name}")
            if event["previous_event_sha512"] != expected_previous:
                raise TransitionWitnessError(f"previous-event hash mismatch at {path.name}")
            if event["contract_ref"] != self.contract_ref or event["contract_instance_id"] != self.contract_instance_id:
                raise TransitionWitnessError(f"contract binding mismatch at {path.name}")
            if event["route_lock"] != self.route_lock:
                raise TransitionWitnessError(f"route lock mismatch at {path.name}")
            if event["event_id"] in self.event_ids:
                raise TransitionWitnessError(f"duplicate event identifier: {event['event_id']}")
            self.event_ids.add(event["event_id"])
            expected_previous = event["event_sha512"]
            expected_sequence += 1
        self.sequence = expected_sequence - 1
        self.head_sha512 = expected_previous

    def append(self, payload: dict) -> dict:
        sequence = self.sequence + 1
        expected_id = f"TE-{self.contract_instance_id.removeprefix('OCI-')}-{sequence:06d}"
        event_id = payload.get("event_id", expected_id)
        if event_id in self.event_ids:
            raise TransitionWitnessError(f"duplicate event identifier: {event_id}")
        if "sequence" in payload and payload["sequence"] != sequence:
            raise TransitionWitnessError(f"sequence gap or rollback: expected {sequence}, got {payload['sequence']}")

        event = {
            "event_version": "v40-candidate.2",
            "event_id": event_id,
            "contract_ref": self.contract_ref,
            "contract_instance_id": self.contract_instance_id,
            "sequence": sequence,
            "timestamp_utc": self.clock(),
            "route_lock": self.route_lock,
            "previous_event_sha512": self.head_sha512,
            **{key: value for key, value in payload.items() if key not in {"event_id", "sequence", "event_sha512", "previous_event_sha512"}},
        }
        event["event_sha512"] = event_digest(event)
        errors = validate_event(event)
        if errors:
            raise TransitionWitnessError("invalid transition witness: " + "; ".join(errors))

        target = self.ledger_dir / f"{sequence:06d}_{event_id}.json"
        temporary = self.ledger_dir / f".{target.name}.tmp-{os.getpid()}"
        if target.exists():
            raise TransitionWitnessError(f"witness overwrite refused: {target.name}")
        try:
            with temporary.open("x", encoding="utf-8") as handle:
                handle.write(json.dumps(event, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self.publisher(temporary, target)
        except OSError as exc:
            if temporary.exists():
                temporary.unlink()
            emergency = {
                "state": "STOPPED",
                "stop_class": "TRANSITION_WITNESS_FAILURE",
                "reason": str(exc),
                "durable": False,
                "contract_instance_id": self.contract_instance_id,
                "attempted_sequence": sequence,
            }
            raise WitnessPersistenceError(f"unable to persist transition witness: {exc}", emergency) from exc

        self.sequence = sequence
        self.head_sha512 = event["event_sha512"]
        self.event_ids.add(event_id)
        return event
