# Zervan v40 Candidate — Wave 0 Tranche 2 Receipt

Receipt State: LOCAL VERIFICATION COMPLETE

Candidate State: CANDIDATE ONLY

Authority: NONE

Human Gate: ACTIVE

Canonical Promotion: NOT REQUESTED

External Runtime: DISABLED

System Population: DISALLOWED

## Specification Checkpoint

- Specification: `candidate/v40/specifications/tranche2_control_state_specification.md`
- Specification commit: `6d2a170109013432825918c0472954ccb489835e`
- Tranche-1 baseline commit: `5b5111db479823db43c5c583d938fe49627e9262`
- Implementation branch: `candidate/v40-wave0`

The specification was committed before schema or runtime implementation began.

## Implemented Units

1. Operational Contract schema reconciliation:
   - contract-instance identity;
   - normalized action identifiers;
   - disjoint permitted, prohibited, and Human-Gate-required action sets;
   - canonicalization policy;
   - transition-ledger policy;
   - Audit policy.
2. Runtime-state schema reconciliation:
   - immutable route lock;
   - Human Gate latch and request reference;
   - stop class and reason;
   - ledger head and last-event identity;
   - contract-instance identity.
3. Transition-witness schema reconciliation:
   - strict states and event classes;
   - conformance before and after;
   - decision, stop, and Scar fields;
   - previous-event and event SHA-512 fields.
4. Transition witness writer:
   - one canonical JSON object per event;
   - ordered sequence;
   - SHA-512 hash chain;
   - synchronized atomic publication;
   - overwrite refusal;
   - duplicate, gap, rollback, and tamper rejection;
   - non-durable emergency stop record on persistence failure.
5. Runtime conformance monitor:
   - contract, authority, Human Gate, route, canonical binding, writer binding, and handler-registry checks;
   - fail-closed `UNKNOWN` or failed checks;
   - explicit stop classification.
6. Route and action controls:
   - immutable route lock;
   - explicit route change separated from observed route drift;
   - normalized action classification;
   - handlers bound at controller initialization rather than injected per request;
   - action intent and result witnesses.
7. Audit interrupt:
   - PASS records no additional authority;
   - FAIL prevents action, records stop evidence, requires Scar, and makes the instance terminal.
8. Human Gate stop:
   - explicit out-of-contract requests latch review;
   - routed work remains frozen;
   - no synthesized decision;
   - denial stops;
   - approval of an out-of-contract request also stops and requires a new contract.
9. Completion enforcement:
   - exact user-owned criteria required;
   - missing or substituted criteria cause Audit stop;
   - `COMPLETE` is terminal and does not promote authority.

## Acceptance Fixtures

All 23 specified fixtures pass:

- 01–04: activation and canonical/invariant failure;
- 05–09: permitted action, route replacement, route drift, prohibited action, undeclared action;
- 10–14: Audit interrupt and non-bypassable Human Gate;
- 15–18: witness duplication, sequence, hash, and persistence failure;
- 19–23: completion, terminal re-entry, and no repository side effects.

Total candidate regression tests: 44.

Additional regression controls pass for:

- unbound action-handler registry;
- registered handler failure;
- inline-code and plain-text posture markers;
- negated and wrong-value marker rejection;
- read-only Python validation;
- P0 inventory stability;
- action-set overlap and identifier normalization.

## Verification Commands

```text
PYTHONDONTWRITEBYTECODE=1 make test-v40-candidate
PYTHONDONTWRITEBYTECODE=1 make validate-v40-candidate
PYTHONDONTWRITEBYTECODE=1 python call/verify_local_call.py
PYTHONDONTWRITEBYTECODE=1 python tools/validate_zervan_5_6_bridge.py --root .
```

## Claim Boundary

This receipt establishes local candidate implementation and verification only.

It does not close P0-040 or dependent findings. It does not implement full Scar or Replay. It does not promote v40, push Git, open a PR, activate external runtime, populate systems, or authorize production execution.

## Required Continuation

The next architectural dependency is full Scar and Replay continuity around the terminal records produced here, followed by the reporting-production boundary controls. Any continuation begins from a new reviewed specification and a separate candidate checkpoint.
