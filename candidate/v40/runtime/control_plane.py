#!/usr/bin/env python3
"""Executable, fail-closed control state for Zervan v40 candidate tranche 2."""

from __future__ import annotations

import copy
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Iterable

from candidate.v40.runtime.transition_writer import (
    TransitionWitnessError,
    TransitionWitnessWriter,
    WitnessPersistenceError,
)
from candidate.v40.tools.validate_operational_contract import validate_contract


TERMINAL_STATES = {"STOPPED", "COMPLETE"}
CANONICAL_BINDING_FAILURE_PREFIXES = (
    "canonical repository mismatch",
    "canonical branch must",
    "canonical commit mismatch",
    "canonical artifact hash mismatch",
    "missing canonical artifact",
    "unable to resolve origin/main",
)


class ControlPlaneError(RuntimeError):
    """Base control-plane exception."""


class TerminalStateError(ControlPlaneError):
    """A terminal contract instance was asked to continue."""


class HumanGateRequired(ControlPlaneError):
    """A request exceeded the active immutable contract and latched Human Gate."""


class HumanGateLatched(ControlPlaneError):
    """Normal routed work was attempted while Human Gate review was latched."""


class AuditInterrupted(ControlPlaneError):
    """Audit stopped the active contract instance."""


class RuntimeControlPlane:
    """Enforce one immutable Operational Contract instance."""

    def __init__(
        self,
        contract: dict,
        ledger_dir: Path,
        *,
        active_seats: Iterable[str] = ("Governance", "Audit", "Registry"),
        action_handlers: dict[str, Callable[[], object]] | None = None,
        writer_factory: Callable[..., TransitionWitnessWriter] = TransitionWitnessWriter,
        writer_options: dict | None = None,
    ) -> None:
        self.contract = copy.deepcopy(contract)
        self.contract_ref = self.contract.get("contract_id", "")
        self.contract_instance_id = self.contract.get("contract_instance_id", "")
        self.route_lock = self.contract.get("route", {}).get("route_id", "")
        self.runtime_route = self.route_lock
        self.state = "INITIALIZING"
        self.conformance = "UNKNOWN"
        self.authority_state = self.contract.get("authority_state")
        self.human_gate = self.contract.get("human_gate")
        self.human_gate_latched = False
        self.human_gate_request_ref: str | None = None
        self.stop_class: str | None = None
        self.stop_reason: str | None = None
        self.active_seats = tuple(dict.fromkeys(active_seats))
        self.action_handlers = MappingProxyType(dict(action_handlers or {}))
        options = dict(writer_options or {})
        self.writer = writer_factory(
            Path(ledger_dir),
            self.contract_ref,
            self.contract_instance_id,
            self.route_lock,
            **options,
        )
        if self.writer.sequence:
            raise ControlPlaneError("existing ledger is inspection-only; a contract instance cannot be resumed")

    def snapshot(self) -> dict:
        return {
            "runtime_version": "v40-candidate.1",
            "contract_ref": self.contract_ref,
            "contract_instance_id": self.contract_instance_id,
            "state": self.state,
            "conformance": self.conformance,
            "active_route": self.runtime_route,
            "route_lock": self.route_lock,
            "authority_state": self.authority_state,
            "human_gate": self.human_gate,
            "human_gate_latched": self.human_gate_latched,
            "human_gate_request_ref": self.human_gate_request_ref,
            "canonical_binding_ref": f"{self.contract.get('canonical_binding', {}).get('repository', '')}@{self.contract.get('canonical_binding', {}).get('commit', '')}",
            "active_seats": list(self.active_seats),
            "transition_sequence": self.writer.sequence,
            "ledger_head_sha512": self.writer.head_sha512,
            "last_event_id": self._last_event_id(),
            "stop_class": self.stop_class,
            "stop_reason": self.stop_reason,
        }

    def _last_event_id(self) -> str | None:
        if not self.writer.sequence:
            return None
        return f"TE-{self.contract_instance_id.removeprefix('OCI-')}-{self.writer.sequence:06d}"

    def conformance_failures(self) -> list[str]:
        failures = validate_contract(self.contract)
        if self.authority_state != self.contract.get("authority_state"):
            failures.append("runtime authority state drift")
        if self.human_gate != self.contract.get("human_gate"):
            failures.append("runtime Human Gate state drift")
        if self.route_lock != self.contract.get("route", {}).get("route_id"):
            failures.append("route lock differs from contract route")
        if self.runtime_route != self.route_lock:
            failures.append("runtime route differs from route lock")
        if self.writer.contract_ref != self.contract_ref or self.writer.contract_instance_id != self.contract_instance_id:
            failures.append("transition writer contract binding drift")
        if self.writer.route_lock != self.route_lock:
            failures.append("transition writer route lock drift")
        if self.human_gate_latched and self.state not in {"HUMAN_GATE_REVIEW", "STOPPED"}:
            failures.append("Human Gate latch state is inconsistent")
        permitted = set(self.contract.get("route", {}).get("permitted_actions", []))
        registered = set(self.action_handlers)
        if registered != permitted:
            failures.append(
                f"action handler registry mismatch; missing={sorted(permitted - registered)}; extra={sorted(registered - permitted)}"
            )
        return failures

    def activate(self) -> dict:
        if self.state in TERMINAL_STATES:
            raise TerminalStateError(f"contract instance is terminal: {self.state}")
        if self.state != "INITIALIZING":
            raise ControlPlaneError(f"activation is invalid from {self.state}")
        failures = self.conformance_failures()
        if failures:
            stop_class = self._failure_stop_class(failures)
            self._audit_stop("activation_conformance_failure", "; ".join(failures), stop_class, failures)
        event = self._write({
            "event_class": "ACTIVATION",
            "from_state": "INITIALIZING",
            "to_state": "ACTIVE",
            "trigger": "activation_checks_passed",
            "action": None,
            "request_ref": None,
            "reason": "Operational Contract activation checks passed",
            "authorization": "CONTRACT_PERMITTED",
            "participants": ["Audit", "Governance", "Registry"],
            "evidence_refs": [self.contract_ref],
            "conformance_before": "UNKNOWN",
            "conformance_after": "CONFORMING",
            "audit_result": "PASS",
            "human_gate_latched": False,
            "decision_ref": None,
            "stop_class": None,
            "scar_required": False,
            "scar_reason": None,
        })
        self.state = "ACTIVE"
        self.conformance = "CONFORMING"
        return event

    def request_route(self, route_id: str, request_ref: str) -> dict:
        self._guard_active()
        self._preflight()
        if route_id == self.route_lock:
            return self._write({
                "event_class": "NO_CHANGE", "from_state": "ACTIVE", "to_state": "ACTIVE",
                "trigger": "same_route_requested", "action": None, "request_ref": request_ref,
                "reason": "Requested route already equals the immutable route lock",
                "authorization": "CONTRACT_PERMITTED", "participants": ["Governance"],
                "evidence_refs": [self.contract_ref], "conformance_before": "CONFORMING",
                "conformance_after": "CONFORMING", "audit_result": "PASS",
                "human_gate_latched": False, "decision_ref": None, "stop_class": None,
                "scar_required": False, "scar_reason": None,
            })
        return self._latch_human_gate(
            request_ref,
            "route_replacement_requested",
            f"Requested route {route_id!r} differs from lock {self.route_lock!r}",
            action=None,
        )

    def request_action(self, action: str, request_ref: str | None = None) -> object:
        self._guard_active()
        self._preflight()
        route = self.contract["route"]
        if action in route.get("prohibited_actions", []) or action in route.get("human_gate_required_actions", []):
            self._latch_human_gate(
                request_ref or f"REQ-{self.writer.sequence + 1:06d}",
                "action_requires_human_gate",
                f"Action {action!r} is outside direct contract permission",
                action=action,
            )
        if action not in route.get("permitted_actions", []):
            self._audit_stop(
                "undeclared_action",
                f"Action {action!r} is neither permitted nor gate-declared",
                "UNDECLARED_ACTION",
                [action],
            )

        self._write({
            "event_class": "ACTION_INTENT", "from_state": "ACTIVE", "to_state": "ACTIVE",
            "trigger": "permitted_action_requested", "action": action, "request_ref": request_ref,
            "reason": "Action matched the immutable permitted-action set",
            "authorization": "CONTRACT_PERMITTED", "participants": list(self.active_seats),
            "evidence_refs": [self.contract_ref], "conformance_before": "CONFORMING",
            "conformance_after": "CONFORMING", "audit_result": "PASS",
            "human_gate_latched": False, "decision_ref": None, "stop_class": None,
            "scar_required": False, "scar_reason": None,
        })
        try:
            result = self.action_handlers[action]()
        except Exception as exc:  # noqa: BLE001 - a handler failure is a control-plane interrupt
            self._audit_stop(
                "action_handler_failure",
                f"Registered handler for {action!r} failed: {exc}",
                "AUDIT_INTERRUPT",
                [action, type(exc).__name__],
            )
        self._preflight()
        self._write({
            "event_class": "ACTION_RESULT", "from_state": "ACTIVE", "to_state": "ACTIVE",
            "trigger": "permitted_action_completed", "action": action, "request_ref": request_ref,
            "reason": "Permitted action returned and post-action conformance passed",
            "authorization": "CONTRACT_PERMITTED", "participants": list(self.active_seats),
            "evidence_refs": [self.contract_ref], "conformance_before": "CONFORMING",
            "conformance_after": "CONFORMING", "audit_result": "PASS",
            "human_gate_latched": False, "decision_ref": None, "stop_class": None,
            "scar_required": False, "scar_reason": None,
        })
        return result

    def audit_pass(self, reason: str, evidence_refs: Iterable[str] = ()) -> dict:
        if self.state in TERMINAL_STATES:
            raise TerminalStateError(f"contract instance is terminal: {self.state}")
        return self._write({
            "event_class": "AUDIT", "from_state": self.state, "to_state": self.state,
            "trigger": "explicit_audit", "action": None, "request_ref": None,
            "reason": reason, "authorization": "NOT_APPLICABLE", "participants": ["Audit"],
            "evidence_refs": list(evidence_refs), "conformance_before": self.conformance,
            "conformance_after": self.conformance, "audit_result": "PASS",
            "human_gate_latched": self.human_gate_latched, "decision_ref": None,
            "stop_class": None, "scar_required": False, "scar_reason": None,
        })

    def audit_interrupt(self, reason: str, evidence_refs: Iterable[str] = ()) -> None:
        if self.state in TERMINAL_STATES:
            raise TerminalStateError(f"contract instance is terminal: {self.state}")
        self._audit_stop("explicit_audit_interrupt", reason, "AUDIT_INTERRUPT", list(evidence_refs))

    def resolve_human_gate(self, *, approved: bool, decision_ref: str) -> None:
        if self.state != "HUMAN_GATE_REVIEW" or not self.human_gate_latched:
            raise ControlPlaneError("no Human Gate review is pending")
        if not decision_ref.strip():
            raise HumanGateLatched("Human Gate decision requires a stable decision reference")
        stop_class = "HUMAN_GATE_APPROVED_NEW_CONTRACT_REQUIRED" if approved else "HUMAN_GATE_DENIED"
        authorization = "HUMAN_GATE_APPROVED" if approved else "HUMAN_GATE_DENIED"
        reason = "Human approved the out-of-contract request; a new contract is required" if approved else "Human denied the out-of-contract request"
        self._write({
            "event_class": "GATE_DECISION", "from_state": "HUMAN_GATE_REVIEW", "to_state": "STOPPED",
            "trigger": "human_gate_decision", "action": None, "request_ref": self.human_gate_request_ref,
            "reason": reason, "authorization": authorization, "participants": ["Human Gate", "Governance"],
            "evidence_refs": [decision_ref], "conformance_before": "CONFORMING",
            "conformance_after": "CONFORMING", "audit_result": "PASS",
            "human_gate_latched": True, "decision_ref": decision_ref, "stop_class": stop_class,
            "scar_required": True, "scar_reason": reason,
        })
        self.state = "STOPPED"
        self.stop_class = stop_class
        self.stop_reason = reason

    def complete(self, satisfied_criteria: Iterable[str]) -> dict:
        self._guard_active()
        self._preflight()
        required = set(self.contract.get("completion_criteria", []))
        supplied = set(satisfied_criteria)
        if supplied != required:
            missing = sorted(required - supplied)
            extra = sorted(supplied - required)
            reason = f"Completion criteria mismatch; missing={missing}; extra={extra}"
            self._audit_stop("completion_mismatch", reason, "COMPLETION_MISMATCH", missing + extra)
        event = self._write({
            "event_class": "COMPLETION", "from_state": "ACTIVE", "to_state": "COMPLETE",
            "trigger": "completion_criteria_satisfied", "action": None, "request_ref": None,
            "reason": "Every user-owned completion criterion was satisfied",
            "authorization": "CONTRACT_PERMITTED", "participants": ["Audit", "Governance"],
            "evidence_refs": sorted(required), "conformance_before": "CONFORMING",
            "conformance_after": "CONFORMING", "audit_result": "PASS",
            "human_gate_latched": False, "decision_ref": None, "stop_class": None,
            "scar_required": False, "scar_reason": None,
        })
        self.state = "COMPLETE"
        return event

    def report_logic_freeze(self, reason: str) -> None:
        self._guard_active()
        self._audit_stop("logic_freeze", reason, "LOGIC_FREEZE", [reason])

    def _guard_active(self) -> None:
        if self.state in TERMINAL_STATES:
            raise TerminalStateError(f"contract instance is terminal: {self.state}")
        if self.human_gate_latched or self.state == "HUMAN_GATE_REVIEW":
            raise HumanGateLatched("Human Gate review is latched")
        if self.state != "ACTIVE":
            raise ControlPlaneError(f"routed action is invalid from {self.state}")

    def _preflight(self) -> None:
        failures = self.conformance_failures()
        if not failures:
            self.conformance = "CONFORMING"
            return
        stop_class = self._failure_stop_class(failures)
        self._audit_stop("runtime_conformance_failure", "; ".join(failures), stop_class, failures)

    @staticmethod
    def _failure_stop_class(failures: Iterable[str]) -> str:
        values = list(failures)
        if any(value.startswith("runtime route differs") for value in values):
            return "ROUTE_DRIFT"
        if any(value.startswith(CANONICAL_BINDING_FAILURE_PREFIXES) for value in values):
            return "CANONICAL_BINDING_FAILURE"
        return "CONTRACT_NONCONFORMANCE"

    def _latch_human_gate(self, request_ref: str, trigger: str, reason: str, *, action: str | None) -> dict:
        if not request_ref.strip():
            self._audit_stop(
                "missing_human_gate_request_reference",
                "Human Gate request requires a stable request reference",
                "CONTRACT_NONCONFORMANCE",
                [trigger],
            )
        event = self._write({
            "event_class": "GATE_REQUEST", "from_state": "ACTIVE", "to_state": "HUMAN_GATE_REVIEW",
            "trigger": trigger, "action": action, "request_ref": request_ref, "reason": reason,
            "authorization": "HUMAN_GATE_PENDING", "participants": ["Governance", "Human Gate"],
            "evidence_refs": [self.contract_ref], "conformance_before": "CONFORMING",
            "conformance_after": "CONFORMING", "audit_result": "PASS",
            "human_gate_latched": True, "decision_ref": None, "stop_class": None,
            "scar_required": True, "scar_reason": reason,
        })
        self.state = "HUMAN_GATE_REVIEW"
        self.human_gate_latched = True
        self.human_gate_request_ref = request_ref
        raise HumanGateRequired(reason)

    def _audit_stop(self, trigger: str, reason: str, stop_class: str, evidence_refs: Iterable[str]) -> None:
        from_state = self.state
        self._write({
            "event_class": "STOP", "from_state": from_state, "to_state": "STOPPED",
            "trigger": trigger, "action": None, "request_ref": self.human_gate_request_ref,
            "reason": reason, "authorization": "REJECTED", "participants": ["Audit", "Governance"],
            "evidence_refs": list(evidence_refs), "conformance_before": self.conformance,
            "conformance_after": "NONCONFORMING", "audit_result": "FAIL",
            "human_gate_latched": self.human_gate_latched, "decision_ref": None,
            "stop_class": stop_class, "scar_required": True, "scar_reason": reason,
        })
        self.state = "STOPPED"
        self.conformance = "NONCONFORMING"
        self.stop_class = stop_class
        self.stop_reason = reason
        raise AuditInterrupted(reason)

    def _write(self, payload: dict) -> dict:
        try:
            return self.writer.append(payload)
        except WitnessPersistenceError as exc:
            self.state = "STOPPED"
            self.conformance = "NONCONFORMING"
            self.stop_class = "TRANSITION_WITNESS_FAILURE"
            self.stop_reason = str(exc)
            raise
        except TransitionWitnessError:
            self.state = "STOPPED"
            self.conformance = "NONCONFORMING"
            self.stop_class = "TRANSITION_WITNESS_FAILURE"
            self.stop_reason = "transition witness validation failed"
            raise
