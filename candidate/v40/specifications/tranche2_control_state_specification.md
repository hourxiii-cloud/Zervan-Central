# Zervan v40 Candidate — Tranche 2 Control-State Specification

Specification State: PROPOSED FOR REVIEW

Candidate State: CANDIDATE ONLY

Authority: NONE

Human Gate: ACTIVE

Canonical Promotion: NOT REQUESTED

External Runtime: DISABLED

System Population: DISALLOWED

Implementation State: NOT STARTED

## 1. Purpose

Tranche 2 defines the minimum executable control plane required to enforce an accepted Operational Contract.

The tranche is limited to five controls:

1. runtime conformance monitor;
2. route lock;
3. transition witness writer;
4. Audit interrupt;
5. non-bypassable Human Gate stop.

This specification resolves their state, ordering, failure, and recovery semantics before code is written.

## 2. Governing Principle

An accepted contract governs execution until the contract reaches a terminal state.

The runtime may not silently revise the contract, route, canonical binding, invariants, completion criteria, or Human Gate state. A requested change outside the active contract ends the active execution path. It does not mutate the contract in place.

Fail-closed means:

- no material action occurs without a conforming active contract;
- no state transition is considered complete without a durable transition witness;
- no failed Audit is advisory;
- no Human Gate stop can be cleared by the runtime itself;
- no stopped or completed contract instance can be restarted.

## 3. Scope

### 3.1 In scope

- Load one immutable Operational Contract.
- Bind the runtime to the contract's declared route and canonical sources.
- Check conformance before activation and before and after every material transition.
- Persist ordered, hash-chained transition witnesses.
- Stop on detected contract drift, route drift, Audit failure, witness failure, or completion mismatch.
- Latch Human Gate review when an explicit request exceeds the active contract.
- Produce bounded state and failure information for later Scar and Replay work.

### 3.2 Out of scope

- External deployment or system population.
- Remote transition storage.
- Concurrent writers or distributed consensus.
- Cryptographic signing or key management.
- Automatic contract amendment.
- Automatic route replacement.
- Runtime resumption after a stop.
- v40 promotion.
- Full Scar and Replay implementation.

Tranche 2 records whether a Scar is required and why. Tranche 2 does not implement the complete Scar or Replay bodies.

## 4. Control-State Model

### 4.1 States

`INITIALIZING`

The contract is loaded but not active. Canonical binding, invariant, route-lock, writer, and state checks are running. No routed action is permitted.

`ACTIVE`

The contract passed activation checks. Only actions explicitly permitted by the locked route may be attempted.

`HUMAN_GATE_REVIEW`

An explicit request requires a new authority-bearing decision or a contract change. Routed work is frozen. Only gate resolution and Audit observation are permitted.

`STOPPED`

Execution terminated fail-closed. The contract instance is terminal. A new contract instance is required for any continuation.

`COMPLETE`

All user-owned completion criteria passed and the final transition witness was persisted. The contract instance is terminal.

### 4.2 State invariants

- `INITIALIZING` has no permission to execute routed actions.
- `ACTIVE` requires conformance `CONFORMING`.
- `HUMAN_GATE_REVIEW` has a latched gate and cannot execute routed actions.
- `STOPPED` and `COMPLETE` are terminal.
- A terminal contract instance cannot return to `INITIALIZING` or `ACTIVE`.
- `authority_state` remains `NONE` throughout this candidate tranche.
- Human approval is a recorded decision; it does not silently change `authority_state` or mutate the contract.

### 4.3 Allowed transitions

| From | To | Trigger | Required result |
|---|---|---|---|
| INITIALIZING | ACTIVE | Activation checks pass | Audit PASS; activation witness persisted |
| INITIALIZING | STOPPED | Activation or witness check fails | Audit FAIL; Scar required |
| ACTIVE | ACTIVE | Permitted material action | Pre-check PASS; action result; post-check PASS; witness persisted |
| ACTIVE | HUMAN_GATE_REVIEW | Explicit route replacement, prohibited action, external mutation, promotion, or authority request | Gate latched; no requested action executed; Scar required |
| ACTIVE | STOPPED | Conformance failure, observed route drift, Audit interrupt, witness failure, completion mismatch, or logic freeze | Audit FAIL; Scar required |
| ACTIVE | COMPLETE | Every declared completion criterion is satisfied | Completion witness persisted |
| HUMAN_GATE_REVIEW | STOPPED | Human decision denies request | Decision witness persisted; Scar required |
| HUMAN_GATE_REVIEW | STOPPED | Human decision approves a change outside the immutable contract | Decision witness persisted; new contract required; Scar required |

No other transition is permitted in tranche 2.

## 5. Control Precedence

Every material request is evaluated in this order:

1. terminal-state check;
2. Human Gate latch check;
3. transition-writer availability and ledger integrity;
4. contract and runtime conformance check;
5. route-lock check;
6. action classification;
7. pre-action transition witness;
8. action execution, if still permitted;
9. post-action conformance check;
10. result transition witness.

A failure at any earlier control prevents all later processing.

## 6. Runtime Conformance Monitor

### 6.1 Activation checks

Before entering `ACTIVE`, the monitor verifies:

- the contract parses and contains all required fields;
- candidate state is `CANDIDATE_ONLY`;
- Authority is `NONE`;
- Human Gate is `ACTIVE`;
- posture matches the contract;
- external runtime is `DISABLED`;
- system population is `DISALLOWED`;
- mutation scope matches the contract;
- canonical repository, branch, commit, paths, and hashes match current Git;
- the route lock equals the contract route identifier;
- permitted and prohibited action sets do not overlap;
- completion, stop, and escalation lists are present and non-duplicative;
- the transition ledger is empty for a new contract instance or valid for inspection;
- the transition writer can persist the activation witness.

### 6.2 Continuous checks

The monitor repeats applicable checks before and after every material transition. It also checks:

- active route equals the route lock;
- runtime state is legal for the requested action;
- transition sequence is contiguous;
- previous-event hash matches the ledger head;
- no Human Gate latch is being bypassed;
- no terminal contract instance is being re-entered.

### 6.3 Conformance outcomes

`CONFORMING`

All required checks pass.

`NONCONFORMING`

At least one required check fails. The monitor invokes an Audit interrupt and moves the contract instance to `STOPPED`.

`UNKNOWN`

A required check cannot be completed. Unknown is not treated as pass. The monitor invokes an Audit interrupt and moves the contract instance to `STOPPED`.

## 7. Route Lock

### 7.1 Lock formation

The route lock is copied from `contract.route.route_id` during initialization. After activation it is immutable for that contract instance.

### 7.2 Explicit route-change request

An explicit request to use a different route is not treated as runtime drift.

The runtime:

1. does not execute the new route;
2. enters `HUMAN_GATE_REVIEW`;
3. records the requested route and reason;
4. records that the active contract remains unchanged;
5. requires a Human Gate decision and, if approved, a new contract instance.

### 7.3 Observed route drift

If the runtime route differs from the lock without an explicit authorized request, the condition is contract drift.

The runtime immediately invokes an Audit interrupt and enters `STOPPED`. It does not convert observed drift into a route-change request.

### 7.4 Same-route request

A request for the already locked route is idempotent. It may record a no-change witness but does not alter state.

## 8. Action Classification

Every requested action has exactly one classification:

`PERMITTED`

The action exactly matches the contract's permitted action set and all controls pass.

`PROHIBITED`

The action exactly matches the contract's prohibited action set. The runtime enters `HUMAN_GATE_REVIEW` without executing it.

`UNDECLARED`

The action appears in neither set. This is a route-definition failure, not implicit permission. Audit interrupts and the contract enters `STOPPED`.

Permitted and prohibited action sets may not overlap. An overlap is an activation failure.

## 9. Transition Witness Writer

### 9.1 Source-of-truth format

The authoritative ledger is an append-only directory containing one canonical JSON object per event.

Filename form:

```text
000001_TE-<CONTRACT>-000001.json
```

Each event is written to a temporary file, flushed, synchronized, and atomically renamed into place. Existing events are never overwritten.

A JSONL edge list may be derived later for analysis. It is not the source of truth.

### 9.2 Required witness fields

The tranche-1 transition schema must be revised before implementation to add:

- `timestamp_utc`;
- `event_class`;
- `action` or `request_ref`;
- `reason`;
- `route_lock`;
- `conformance_before`;
- `conformance_after`;
- `human_gate_latched`;
- `decision_ref` when applicable;
- `previous_event_sha512`;
- `event_sha512`;
- `stop_class` when applicable;
- `scar_reason` when `scar_required` is true.

### 9.3 Hash chain

The writer canonicalizes the event without `event_sha512`, calculates SHA-512, and stores the resulting digest as `event_sha512`.

Event 1 uses an explicit null previous hash. Every later event records the prior event's digest.

The writer rejects:

- duplicate identifiers;
- sequence gaps;
- sequence rollback;
- previous-hash mismatch;
- overwrite attempts;
- malformed events;
- missing Scar reason when Scar is required.

### 9.4 Witness failure

If a required witness cannot be persisted, the requested transition is not complete and no material action may execute.

The runtime returns an in-memory emergency failure record to the caller, marks the instance `STOPPED` in memory, and performs no further action. The emergency record is not represented as durable proof.

## 10. Audit Interrupt

### 10.1 Invocation

Audit is callable during `INITIALIZING`, `ACTIVE`, and `HUMAN_GATE_REVIEW`.

Audit may be invoked by:

- the conformance monitor;
- route drift detection;
- undeclared action detection;
- transition-ledger failure;
- completion mismatch;
- a registered escalation trigger;
- explicit internal Audit request.

### 10.2 PASS

Audit PASS records a witness and does not grant permission beyond the active contract.

### 10.3 FAIL

Audit FAIL is an interrupt, not advice.

The runtime:

1. prevents the requested action;
2. enters `STOPPED`;
3. records the failed control, evidence references, and stop class;
4. requires a Scar;
5. prohibits restart of that contract instance.

Audit cannot authorize route replacement, authority promotion, external mutation, or gate bypass.

## 11. Human Gate Stop

### 11.1 Meaning of ACTIVE

`Human Gate: ACTIVE` means the authority boundary is available and enforceable. It does not mean all inert local candidate work is automatically stopped.

### 11.2 Latch triggers

The gate latches when an explicit request seeks:

- a route different from the route lock;
- an action listed as prohibited;
- canonical mutation;
- external mutation or deployment;
- system population;
- authority promotion;
- v40 promotion;
- any operation the contract explicitly assigns to Human Gate.

### 11.3 Latch behavior

When latched:

- state becomes `HUMAN_GATE_REVIEW`;
- the triggering action is not executed;
- normal routed actions are frozen;
- repeated requests do not clear or replace the original gate request;
- only Audit observation and one explicit Human Gate decision are accepted.

### 11.4 Human decision

Denial moves the contract instance to `STOPPED`.

Approval of a request outside the active contract also moves the contract instance to `STOPPED`. Approval authorizes preparation of a new contract; it does not mutate or resume the old one.

The Human Gate decision must include a stable decision reference. Missing or ambiguous decisions leave the gate latched.

### 11.5 Non-bypassability

The runtime may not clear the latch, synthesize a Human Gate decision, interpret silence as approval, or treat a receipt, hash, manifest, Audit PASS, or user-completion calculation as Human Gate approval.

## 12. Completion

Completion criteria are user-owned contract terms.

The runtime may enter `COMPLETE` only when:

- every declared criterion is explicitly reported satisfied;
- no undeclared substitute criterion is used;
- conformance passes;
- no Human Gate latch is active;
- the completion witness persists successfully.

Missing criteria cause Audit FAIL and `STOPPED`. The runtime does not convert missing work into a future-work list and does not redefine completion.

`COMPLETE` does not mean canonical promotion, external deployment, compliance, or authority.

## 13. Stop Classes

Every `STOPPED` transition has exactly one primary stop class:

- `CONTRACT_NONCONFORMANCE`;
- `CANONICAL_BINDING_FAILURE`;
- `ROUTE_DRIFT`;
- `UNDECLARED_ACTION`;
- `AUDIT_INTERRUPT`;
- `TRANSITION_WITNESS_FAILURE`;
- `COMPLETION_MISMATCH`;
- `HUMAN_GATE_DENIED`;
- `HUMAN_GATE_APPROVED_NEW_CONTRACT_REQUIRED`;
- `LOGIC_FREEZE`.

Secondary contributing conditions may be recorded, but one primary class owns the transition.

## 14. Required Schema Reconciliation

Implementation must not begin until the candidate schemas are revised to represent this specification.

### 14.1 Operational Contract additions

- normalized action identifiers rather than unconstrained prose matching;
- optional `human_gate_required_actions`;
- transition-ledger policy;
- Audit policy;
- canonicalization identifier;
- contract-instance identifier distinct from contract schema/version.

### 14.2 Runtime state additions

- immutable `route_lock`;
- `human_gate_latched`;
- `human_gate_request_ref`;
- `stop_class`;
- `stop_reason`;
- `ledger_head_sha512`;
- `last_event_id`;
- `contract_instance_id`.

### 14.3 Transition event additions

The fields listed in Section 9.2 plus a strict state enum and strict stop-class enum.

## 15. Adversarial Acceptance Fixtures

Tranche 2 is not complete until each fixture proves both state and witness behavior.

1. Valid activation enters `ACTIVE` and writes event 1.
2. Authority drift during initialization enters `STOPPED`.
3. Canonical commit mismatch enters `STOPPED`.
4. Canonical artifact hash mismatch enters `STOPPED`.
5. Permitted action remains on the locked route and records pre/post witnesses.
6. Explicit route-replacement request enters `HUMAN_GATE_REVIEW` without executing the new route.
7. Direct route drift invokes Audit and enters `STOPPED`.
8. Prohibited action enters `HUMAN_GATE_REVIEW` without execution.
9. Undeclared action invokes Audit and enters `STOPPED`.
10. Explicit Audit FAIL interrupts an otherwise permitted action.
11. Human Gate latch blocks later permitted actions.
12. Human Gate denial enters terminal `STOPPED`.
13. Human Gate approval for an out-of-contract request enters terminal `STOPPED` and requires a new contract.
14. Runtime attempt to synthesize approval is rejected.
15. Duplicate event identifier is rejected.
16. Sequence gap is rejected.
17. Previous-event hash mismatch is rejected.
18. Witness persistence failure prevents action execution and stops in memory.
19. Missing completion criterion invokes Audit and enters `STOPPED`.
20. Complete criteria enter terminal `COMPLETE`.
21. Re-entry from `STOPPED` is rejected.
22. Re-entry from `COMPLETE` is rejected.
23. Default validation produces no external action, system population, or unrequested package artifact.

## 16. Implementation Units and Commit Discipline

Implementation proceeds in separate reviewable units:

1. reconcile the three candidate schemas with Section 14;
2. implement and test the transition witness writer;
3. implement and test the conformance monitor;
4. implement and test route lock and action classification;
5. implement and test Audit interrupt;
6. implement and test Human Gate latch and resolution;
7. integrate the state machine and run all adversarial fixtures;
8. write the tranche-2 receipt;
9. review the complete diff;
10. commit tranche 2 separately from tranche 1.

An implementation unit may not be described as complete merely because its classes or files exist. Its associated adversarial fixtures must pass.

## 17. Definition of Done

Tranche 2 is done only when:

- all schema changes required by this specification are present;
- the five controls are implemented without expanding scope;
- all 23 acceptance fixtures pass;
- every material transition is witnessed or execution stops before action;
- route drift and explicit route change remain distinct paths;
- Audit FAIL is interruptive;
- Human Gate is latched and non-bypassable;
- stopped and completed contract instances cannot resume;
- v39 and 5.6 validation still pass;
- the default test and validation route leaves no bytecode, result, deployment, or system-population artifact;
- the working diff is reviewed;
- a separate candidate commit is created;
- no push, PR, promotion, or external deployment occurs without a later explicit Human Gate action.

## 18. Failure Mapping

This tranche primarily addresses:

- P0-001 Operational Contract Violation;
- P0-003 Runtime Invariant Violation;
- P0-004 Route Escalation Failure;
- P0-005 Unauthorized Route Substitution;
- P0-006 Completion Criteria Override;
- P0-011 Human Gate Bypass;
- P0-012 Governance Failure;
- P0-013 False Compliance;
- P0-014 Canonical Drift;
- P0-019 Operation Route Catalog Bypass;
- P0-020 Audit Bypass;
- P0-022 Logic Freeze;
- P0-028 Trust Model Failure;
- P0-031 Canonical Recovery Failure;
- P0-032 Escalation Persistence Failure;
- P0-040 Contract Enforcement Failure.

Passing this tranche does not automatically close those findings. Closure requires traceability from each finding to implemented controls, passing fixtures, review evidence, and Human Gate disposition.
