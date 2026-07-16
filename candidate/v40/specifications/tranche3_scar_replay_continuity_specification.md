# Zervan v40 Candidate — Tranche 3 Scar and Minimum Replay Continuity Specification

## 0. Control Status

- Version target: `vTemporal.40.0-candidate`
- Candidate branch: `candidate/v40-wave0`
- Authority: `NONE`
- Human Gate: `ACTIVE`
- Canonical v39 mutation: `DISALLOWED`
- External runtime: `DISABLED`
- System population: `DISALLOWED`
- Operating mode: `DISCUSSION / TECH / NONE / NON-DOCTRINAL / STABLE`
- Candidate posture: `CONTROLLED / LOCAL IMPLEMENTATION / FAIL-CLOSED`
- Specification status: `PRE-IMPLEMENTATION`

This document is a candidate engineering specification. It does not modify the v39 canonical body, promote v40, authorize external action, populate a system, or grant runtime authority.

## 1. Grounding and Dependency

This specification is grounded in:

- public Git `main` at `b9460bf2955246ff3b1f61ed0b398496d7ad49c1`;
- published candidate branch `candidate/v40-wave0` at `2d75db540cd330f79e27a3baeb9ba7e4d04f30f1`;
- Tranche 1 contract controls at `5b5111db479823db43c5c583d938fe49627e9262`;
- Tranche 2 control-state specification at `6d2a170109013432825918c0472954ccb489835e`;
- Tranche 2 executable control state at `2d75db540cd330f79e27a3baeb9ba7e4d04f30f1`;
- `candidate/v40/receipts/wave0_tranche2_receipt.md`; and
- the Zervan v40 Final Consolidated Implementation Plan.

The Tranche 2 receipt freezes the next dependency as full Scar and minimum Replay continuity around the terminal records already produced, followed by reporting-production boundary controls.

Tranche 2 also establishes a controlling invariant: `STOPPED` and `COMPLETE` contract instances cannot re-enter execution. Tranche 3 must preserve that invariant. Replay restores context for a possible new contract; Replay does not reopen the stopped contract.

## 2. Purpose

Tranche 3 implements the minimum continuity loop required after governed execution stops:

```text
Terminal transition witness
        ↓
Immutable Scar
        ↓
Validated Replay preparation
        ↓
Human Gate decision
        ↓
Continuation reference for a new contract, or BLOCKED
```

The tranche has four purposes:

1. make every Scar-required terminal transition resolve to one immutable Scar;
2. preserve why movement stopped, what evidence was present or absent, and what remains unresolved;
3. detect the repeating-thirds runtime marker and terminate the affected route correctly; and
4. reconstruct a bounded, integrity-checked continuation record without relying on hidden conversation state.

## 3. Architectural Rule

Replay restores context. Scar preserves reasoning. Neither grants authority.

A stopped contract instance remains stopped forever. A Replay authorization can only support creation of a new Operational Contract with a new contract instance identifier and a new route lock. Until that contract exists and passes its own activation controls, no analytical or external action may resume.

## 4. Scope

Tranche 3 is limited to:

1. a Scar record schema;
2. a Replay receipt schema;
3. an immutable Scar writer and Scar ledger validator;
4. reconciliation between terminal transition witnesses and Scar records;
5. structured repeating-thirds marker detection and termination;
6. a minimum Replay preparer and validator;
7. a Human-Gated continuation decision record;
8. adversarial and continuity fixtures; and
9. a Tranche 3 implementation receipt.

## 5. Explicit Non-Goals

Tranche 3 does not implement:

- report projection or publication gates;
- typed Evidence → Analysis → Reporting records;
- analytical inventory freeze or conversation-to-artifact reconciliation;
- a complete inquiry-envelope architecture;
- dynamic team formation or functional-seat normalization;
- Analysis Persona canonization;
- execution of a resumed analytical route;
- automatic Operational Contract creation;
- external runtime activation;
- external mutation;
- system population;
- canonical promotion; or
- closure of any P0 finding by assertion.

The Replay receipt contains the minimum explicit context needed to evaluate continuation. The complete inquiry-envelope architecture remains a later continuity unit.

## 6. Terms

### 6.1 Terminal transition

A valid Tranche 2 transition witness whose `to_state` is `STOPPED` and whose `scar_required` field is `true`.

### 6.2 Scar

An immutable, integrity-bound record explaining why a route stopped, what evidence boundary was reached, which contradictions or uncertainties remain, and what must be true before later continuation can be considered.

### 6.3 Replay

A validation and reconstruction operation that restores explicit context from canonical records, transition witnesses, Scar records, and referenced evidence. Replay does not rerun computation by default and does not authorize action.

### 6.4 Continuation reference

An identifier emitted by an authorized Replay receipt. It is an input to a later new-contract proposal. It is not an executable route, authority token, approval substitute, or reopened runtime state.

### 6.5 Evidence boundary

The explicit boundary between evidence available to the stopped inquiry and evidence absent, exhausted, contradictory, invalid, or outside authorized scope.

### 6.6 Hidden conversation state

Any material route, evidence, conclusion, uncertainty, decision, or participation fact that is necessary for continuation but is not carried by an explicit referenced artifact.

Replay must not depend on hidden conversation state.

## 7. Required Candidate Artifacts

Implementation of this specification is expected to add:

- `candidate/v40/contracts/scar.schema.json`;
- `candidate/v40/contracts/replay_receipt.schema.json`;
- `candidate/v40/runtime/continuity.py`;
- `candidate/v40/tools/validate_continuity.py`;
- `tests/test_v40_candidate_continuity.py`; and
- `candidate/v40/receipts/wave0_tranche3_receipt.md`.

Existing Tranche 2 schemas may be changed only where this specification identifies a required compatibility change. Every schema change must retain fail-closed validation and must not enable re-entry from `STOPPED` or `COMPLETE`.

## 8. Scar Record Contract

### 8.1 Required identity and binding fields

Every Scar record must include:

- `scar_version`;
- `scar_id`;
- `contract_ref`;
- `contract_instance_id`;
- `route_id`;
- `route_lock`;
- `canonical_binding_ref`;
- `terminal_event_id`;
- `terminal_event_sequence`;
- `terminal_event_sha512`;
- `transition_ledger_head_sha512`;
- `recorded_at_utc`;
- `authority_state`;
- `human_gate_state`;
- `scar_class`;
- `stop_class`;
- `trigger`;
- `reason`;
- `evidence_boundary`;
- `analysis_state`;
- `continuation`;
- `provenance_refs`;
- `scar_sha512`.

`authority_state` must be `NONE`. `human_gate_state` must be `ACTIVE`.

### 8.2 Identifier rules

- `scar_id` must match `^SC-[A-Z0-9._-]+$`.
- The default identifier is derived from the contract instance and terminal event sequence.
- A Scar identifier cannot be reused.
- A terminal transition cannot have more than one Scar.
- A Scar cannot bind to more than one terminal transition.

### 8.3 Scar classes

`scar_class` must be one of:

- `CONTRACT_CONTROL_STOP`;
- `HUMAN_GATE_STOP`;
- `EVIDENCE_BOUNDARY_EXHAUSTION`;
- `UNRESOLVED_CONTRADICTION`;
- `RECURSIVE_ANALYTICAL_FAILURE`;
- `TRANSITION_WITNESS_FAILURE`; or
- `UNCLASSIFIED_CONTROL_STOP`.

An unknown condition is not silently forced into a more specific class. It remains `UNCLASSIFIED_CONTROL_STOP`, with the uncertainty preserved.

### 8.4 Evidence boundary object

`evidence_boundary` must contain:

- `boundary_state`: `AVAILABLE`, `PARTIAL`, `EXHAUSTED`, `CONTRADICTORY`, `INVALID`, or `UNKNOWN`;
- `available_evidence_refs`: a unique array;
- `missing_evidence_refs`: a unique array;
- `contradiction_refs`: a unique array;
- `invalid_evidence_refs`: a unique array;
- `scope_exclusions`: a unique array;
- `boundary_reason`: a non-empty string; and
- `evidence_time_utc`: an explicit observation time or `null` when unknown.

Empty arrays are permitted. Missing fields are not. Unknown evidence must remain unknown; it cannot be represented as absent evidence without support.

### 8.5 Analysis state object

`analysis_state` must contain:

- `inquiry_ref`: a string or `null`;
- `claim_refs`: a unique array;
- `unresolved_claim_refs`: a unique array;
- `eliminated_world_refs`: a unique array;
- `surviving_world_refs`: a unique array;
- `function_participation_refs`: a unique array;
- `last_supported_conclusion_refs`: a unique array; and
- `state_summary`: a non-empty evidence-bound summary.

The summary cannot introduce claims absent from the referenced analytical record. Tranche 3 preserves references; it does not create the later typed analytical model.

### 8.6 Continuation object

`continuation` must contain:

- `replay_eligible`: boolean;
- `replay_blockers`: a unique array;
- `replay_preconditions`: a unique array;
- `new_contract_required`: `true`;
- `continuation_ref`: a string or `null`; and
- `human_gate_decision_required`: `true`.

A Scar is immutable, so its `continuation_ref` remains `null`. A continuation reference exists only in an authorized Replay receipt; the Scar is never updated to carry it.

### 8.7 Scar integrity

Scar records use canonical JSON and SHA-512.

- `scar_sha512` is calculated over the complete canonical record excluding `scar_sha512` itself.
- The Scar ledger validates every record independently and enforces unique Scar and terminal-event bindings.
- Any digest mismatch, overwrite attempt, duplicate binding, contract mismatch, route-lock mismatch, or terminal-event mismatch invalidates the Scar ledger.

## 9. Scar Write Protocol

The write protocol is:

1. load and validate the complete transition ledger;
2. resolve the referenced terminal event;
3. prove that the event is terminal and Scar-required;
4. prove that no Scar already resolves that event;
5. prove contract, instance, route-lock, canonical-binding, sequence, and hash agreement;
6. build the Scar from explicit supplied records;
7. validate the complete Scar object;
8. write to a same-filesystem temporary file;
9. flush the file;
10. publish with no-overwrite atomic rename;
11. synchronize the containing directory; and
12. reload and validate the resulting Scar ledger.

Failure at any point leaves the runtime stopped. A failed Scar write cannot authorize Replay and cannot be represented as successful continuity.

No terminal transition witness is mutated to add the Scar. The Scar points to the immutable terminal event. Reconciliation proves the relationship in both directions.

## 10. Scar Reconciliation Gate

For a contract instance to be continuity-complete:

- every valid terminal event with `scar_required=true` must resolve to exactly one valid Scar;
- every Scar must resolve to exactly one valid terminal event;
- the event and Scar bindings must agree;
- every Scar record must be digest-valid and uniquely bound;
- no terminal event may be omitted; and
- no orphan Scar may exist.

Reconciliation states are:

- `COMPLETE`;
- `MISSING_SCAR`;
- `ORPHAN_SCAR`;
- `DUPLICATE_SCAR`;
- `BINDING_MISMATCH`;
- `INTEGRITY_FAILURE`; or
- `UNREADABLE`.

Only `COMPLETE` permits Replay preparation.

For Replay binding, `scar_ledger_sha512` is the SHA-512 digest of a canonical JSON array containing the reconciled Scar records sorted by `terminal_event_sequence` and then `scar_id`. This digest binds Replay to the complete reconciled Scar set without inventing a mutable Scar chain.

## 11. Repeating-Thirds Runtime Marker

The controlling interpretation is:

> Repeating .333… / .666… is not confidence. It is a runtime control marker indicating unresolved contradiction, evidence-boundary exhaustion, or recursive analytical failure. Detecting the marker is successful self-observation; the underlying condition still requires termination, Scar, and later Replay.

### 11.1 Structured detection only

The detector consumes an explicit structured marker, not arbitrary prose and not ordinary numeric values.

Accepted marker kinds are:

- `REPEATING_ONE_THIRD`; and
- `REPEATING_TWO_THIRDS`.

The marker must include:

- `marker_kind`;
- `condition_class`;
- `source_ref`;
- `observation_time_utc`; and
- `evidence_refs`.

`condition_class` is one of:

- `UNRESOLVED_CONTRADICTION`;
- `EVIDENCE_BOUNDARY_EXHAUSTION`;
- `RECURSIVE_ANALYTICAL_FAILURE`; or
- `UNKNOWN`.

The detector must not infer a marker from:

- a normal decimal near one-third or two-thirds;
- an ordinary fraction in a dataset;
- quoted historical text;
- prose containing `.333` or `.666`; or
- a confidence score.

### 11.2 Required behavior

Detection must:

1. record successful self-observation;
2. prevent continued execution on the affected route;
3. invoke the Tranche 2 Audit interrupt path;
4. enter terminal `STOPPED`;
5. map the condition to the appropriate Scar class, preserving `UNKNOWN` when necessary;
6. require a Scar; and
7. make later Replay subject to the complete continuity and Human Gate rules.

Detection is not resolution. A marker cannot be cleared by relabeling it as confidence.

## 12. Replay Receipt Contract

### 12.1 Required fields

Every Replay receipt must include:

- `replay_version`;
- `replay_id`;
- `replay_sequence`;
- `decision_of_replay_id`;
- `requested_at_utc`;
- `prepared_at_utc`;
- `scar_ref`;
- `scar_sha512`;
- `source_contract_ref`;
- `source_contract_instance_id`;
- `source_route_id`;
- `source_route_lock`;
- `terminal_event_id`;
- `terminal_event_sha512`;
- `transition_ledger_head_sha512`;
- `scar_ledger_sha512`;
- `source_canonical_binding_ref`;
- `current_canonical_binding_ref`;
- `canonical_comparison`;
- `authority_state`;
- `restored_context`;
- `unavailable_context`;
- `continuation_proposal`;
- `human_gate`;
- `status`;
- `previous_replay_sha512`; and
- `replay_sha512`.

`authority_state` must remain `NONE` for every Replay receipt.

### 12.2 Replay identity and ordering

- `replay_id` must match `^RP-[A-Z0-9._-]+$`.
- `replay_sequence` must be a positive integer with no gap or rollback in the Replay ledger.
- Replay identifiers cannot be reused.
- `decision_of_replay_id` is `null` for preparation receipts.
- `decision_of_replay_id` must reference the decided preparation receipt for `AUTHORIZED_NEW_CONTRACT_REQUIRED` and `DENIED` receipts.
- A preparation receipt can have no more than one Human Gate decision receipt.

### 12.3 Replay statuses

`status` is one of:

- `PREPARED`;
- `BLOCKED`;
- `HUMAN_GATE_REVIEW`;
- `AUTHORIZED_NEW_CONTRACT_REQUIRED`; or
- `DENIED`.

No Replay status is named `ACTIVE`, `RUNNING`, or `RESUMED` in this tranche.

### 12.4 Canonical comparison

`canonical_comparison` must distinguish:

- `UNCHANGED`;
- `ADVANCED_REVALIDATION_REQUIRED`;
- `DRIFTED`;
- `UNAVAILABLE`; or
- `INVALID`.

Only `UNCHANGED` may proceed directly to Human Gate review. `ADVANCED_REVALIDATION_REQUIRED` requires explicit revalidation evidence. `DRIFTED`, `UNAVAILABLE`, and `INVALID` are blocked.

### 12.5 Restored context

`restored_context` must be an explicit unique array of typed references. At minimum it must carry available references for:

- route and contract;
- canonical binding;
- transition ledger;
- terminal event;
- Scar;
- evidence boundary;
- analytical state;
- participants or function participation; and
- prior decisions.

`unavailable_context` records every required reference that could not be restored and why. Missing context is not silently reconstructed from conversation memory.

### 12.6 Continuation proposal

The proposal must contain:

- `proposed_route_id`;
- `proposed_scope`;
- `proposed_completion_criteria`;
- `required_evidence_refs`;
- `new_contract_required`: `true`;
- `new_contract_ref`: `null` until separately created;
- `new_contract_instance_id`: `null` until separately created; and
- `continuation_ref`: a new immutable identifier only after authorization.

The proposal is non-executable.

### 12.7 Human Gate object

The Human Gate object must include:

- `state`: `ACTIVE`;
- `decision`: `PENDING`, `APPROVED`, or `DENIED`;
- `decision_ref`: string or `null`;
- `decided_at_utc`: string or `null`; and
- `decision_owner`: `HUMAN` when a decision exists.

Approval cannot be synthesized, inferred from tone, inherited from a prior action, or copied from the stopped contract.

## 13. Minimum Replay Protocol

Replay preparation proceeds in this order:

1. accept an explicit Replay request referencing one Scar;
2. validate the transition ledger;
3. validate the Scar ledger;
4. run terminal-event-to-Scar reconciliation;
5. verify all contract, route, hash, and canonical bindings;
6. compare the source and current canonical bindings;
7. restore only explicitly referenced context;
8. record unavailable or invalid context;
9. evaluate Replay blockers and preconditions;
10. create a non-executable continuation proposal;
11. write an integrity-bound Replay receipt in `PREPARED`, `BLOCKED`, or `HUMAN_GATE_REVIEW`;
12. if reviewable, latch the Human Gate;
13. record an explicit Human Gate decision in a new Replay receipt; and
14. on approval, emit `AUTHORIZED_NEW_CONTRACT_REQUIRED` with a continuation reference.

An approval does not create or activate the new contract in Tranche 3. A later controlled operation must create, validate, review, and activate that contract.

## 14. Replay Integrity and Immutability

- Replay receipts use canonical JSON and SHA-512.
- `replay_sha512` excludes only itself from digest calculation.
- Receipts are append-only and linked by `previous_replay_sha512`.
- A later Human Gate decision creates a new receipt; it does not mutate the prepared receipt.
- Replay identifiers cannot be reused.
- A decision receipt must resolve to the prepared receipt it decides.
- Overwrite, truncation, sequence gaps, and hash disagreement fail closed.

## 15. Temporal Consistency

Tranche 3 must preserve separate times for:

- source evidence observation;
- terminal transition;
- Scar recording;
- Replay request;
- Replay preparation;
- canonical comparison; and
- Human Gate decision.

These times cannot be collapsed into a single generated timestamp. Unknown source time remains `null` and is described as unknown.

## 16. Authority and Mutation Rules

Tranche 3 inherits all active invariants:

- Authority remains `NONE`.
- Human Gate remains `ACTIVE`.
- Canonical mutation remains disallowed.
- External runtime remains disabled.
- System population remains disallowed.
- Candidate records remain non-doctrinal.

Permitted local actions are limited to candidate schema editing, candidate runtime editing, local tests, read-only validation, and candidate receipts.

Replay authorization is not authority promotion.

## 17. Failure Behavior

The continuity system fails closed on:

- unreadable transition or Scar records;
- invalid schema;
- missing required terminal event;
- missing, orphaned, or duplicate Scar;
- contract, instance, route, or canonical mismatch;
- hash-chain failure;
- overwrite attempt;
- partial persistence;
- hidden-state dependency;
- canonical drift without revalidation;
- missing Human Gate decision evidence;
- inferred approval;
- attempt to reopen a stopped or completed contract;
- attempt to execute a continuation proposal; or
- attempted external action or system population.

Failure returns a bounded status and evidence. It does not enter an explanatory loop that substitutes commentary for the failed operation.

## 18. Acceptance Fixtures

Implementation must include at least these fixtures:

1. A valid terminal event produces one valid Scar.
2. A terminal event missing a Scar reconciles as `MISSING_SCAR`.
3. An orphan Scar reconciles as `ORPHAN_SCAR`.
4. A duplicate Scar for one terminal event is rejected.
5. A Scar bound to a nonterminal event is rejected.
6. A terminal-event hash mismatch is rejected.
7. A transition-ledger-head mismatch is rejected.
8. A contract-instance mismatch is rejected.
9. A route-lock mismatch is rejected.
10. A canonical-binding mismatch is rejected.
11. A Scar digest mismatch is rejected.
12. A malformed or unsupported Scar class is rejected.
13. A Scar overwrite attempt is rejected.
14. Scar persistence failure leaves no published partial record.
15. Unknown evidence remains unknown rather than absent.
16. Missing evidence is carried explicitly in the evidence boundary.
17. A structured repeating-one-third marker terminates and requires Scar.
18. A structured repeating-two-thirds marker terminates and requires Scar.
19. A normal numeric one-third value does not trigger the detector.
20. Free-form prose containing `.333` or `.666` does not trigger the detector.
21. Detection is recorded as successful self-observation, not confidence.
22. An unknown thirds condition terminates without fabricated classification.
23. Replay preparation fails when Scar reconciliation is incomplete.
24. Replay preparation fails on invalid Scar integrity.
25. Replay preparation blocks on canonical drift.
26. Replay preparation records unavailable context without reconstructing it from conversation memory.
27. Replay cannot reopen the source stopped contract instance.
28. Replay cannot execute the continuation proposal.
29. Human Gate remains latched before a continuation decision.
30. Runtime-generated approval is rejected.
31. Human Gate denial produces an immutable `DENIED` receipt.
32. Human Gate approval produces `AUTHORIZED_NEW_CONTRACT_REQUIRED`, not `ACTIVE`.
33. Approval produces a continuation reference but no new contract or route execution.
34. Replay receipt overwrite is rejected.
35. Replay receipt sequence gap or hash-chain failure is rejected.
36. Temporal fields preserve observation, transition, Scar, Replay, and decision times separately.
37. Default validation leaves the repository tree clean.
38. No fixture activates an external runtime, mutates canonical v39, or populates a system.

## 19. Implementation Units and Commit Discipline

After this specification is reviewed and committed separately, implementation proceeds in this order:

1. add and test the Scar schema;
2. add and test the Replay receipt schema;
3. implement and test the immutable Scar ledger writer;
4. implement and test terminal-event-to-Scar reconciliation;
5. implement and test the structured thirds-marker detector and stop integration;
6. implement and test minimum Replay preparation;
7. implement and test Human Gate Replay decisions and continuation references;
8. run all Tranche 1, Tranche 2, Tranche 3, v39, and 5.6 validation;
9. write the Tranche 3 receipt;
10. review the complete implementation diff; and
11. commit Tranche 3 implementation separately from this specification.

No architectural improvisation is permitted inside the code phase. Any required change to this specification must be made explicitly, reviewed, and committed before dependent implementation.

## 20. Definition of Done

Tranche 3 is complete only when:

- all required schemas and runtime units exist;
- every Scar-required terminal event reconciles to exactly one immutable Scar;
- Scar records validate uniqueness and SHA-512 integrity;
- Replay receipts validate ordering and SHA-512 chain integrity;
- the repeating-thirds marker terminates correctly without being interpreted as confidence;
- ordinary decimals and prose do not create false marker events;
- minimum Replay reconstructs explicit context without hidden conversation state;
- missing context, evidence exhaustion, contradiction, and recursive failure remain distinct;
- Replay cannot reopen a stopped or completed source contract;
- Human Gate decisions remain explicit and human-owned;
- approval produces only a continuation reference for a new contract;
- all 38 fixtures pass;
- all earlier candidate and canonical validators still pass;
- the default validation route leaves a clean working tree;
- a substantive receipt records the evidence;
- the implementation is committed separately from this specification; and
- no PR, merge, promotion, external runtime activation, canonical mutation, or system population occurs without a later explicit Human Gate action.

## 21. Failure Mapping

This tranche primarily addresses:

- `P0-020` Audit Bypass;
- `P0-021` Replay Scar Omission;
- `P0-022` Logic Freeze;
- `P0-027` Scientific Validation Damage;
- `P0-038` Temporal Consistency Failure;
- `P0-039` Execution Ownership Confusion; and
- `P0-040` Contract Enforcement Failure.

It supplies supporting continuity evidence for other findings but does not close them automatically.

## 22. Closure and Next Dependency

Passing Tranche 3 does not promote v40 and does not close the parent failure operation. Closure requires finding-to-control traceability, passing fixtures, review evidence, and explicit Human Gate disposition.

After Tranche 3 implementation is complete and independently committed, the next planned dependency is the typed Evidence → Analysis → Reporting boundary and production-gate specification. That later tranche must preserve claim meaning, lineage, evidence relationships, and uncertainty while allowing controlled audience adaptation.
