# AC-09 — Atomic Canonical State Mutation

Status: CONTROLLED CANDIDATE CONTRACT
Activation Control: AC-09
Version: vTemporal.41.0
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

AC-09 defines the atomic canonical-state mutation boundary.

Canonical mutation MUST behave as one serialized transition from one
authoritative accepted state to exactly one admissible successor state.

Validation success does not reserve a successor.

Technical write capability does not establish mutation authority.

Atomic file publication does not by itself establish atomic state transition.

---

## 1. Governing Invariant

For one canonical state lineage:

one accepted current state
->
zero or one accepted direct successor per mutation decision.

Two writers MUST NOT independently commit competing successors from the same
accepted predecessor.

The mutation boundary MUST serialize:

1. authoritative-current-state resolution;
2. expected-current comparison;
3. successor validation;
4. successor sequence allocation;
5. successor publication;
6. authoritative-current-state advancement.

No competing writer may enter that critical transition concurrently for the
same mutation domain.

---

## 2. Authoritative Current State

A mutation MUST resolve authoritative current state after entering the
serialization boundary.

Writer-local cached state is not authoritative current state.

Construction-time state is not necessarily mutation-time state.

The authoritative current-state binding MUST include, where applicable:

- active manifest reference;
- active State Root;
- current state sequence;
- current transition-witness head;
- current transition-witness sequence.

Current state MUST NOT be inferred from stale writer-local memory.

---

## 3. Expected-Current Binding

Every mutation request MUST bind the state it expects to mutate.

The expected-current binding MUST preserve sufficient identity to reject a
stale mutation request.

For canonical State Pointer movement this includes:

- expected active State Root;
- expected state sequence.

For transition-witness advancement this includes:

- expected prior event SHA-512;
- expected prior event sequence.

A mutation may proceed only when expected current state equals authoritative
current state inside the serialization boundary.

Expected current != authoritative current
->
mutation rejected as stale.

---

## 4. Compare-and-Swap Semantics

AC-09 uses compare-and-swap semantics.

Conceptually:

CAS(
    expected_current,
    authoritative_current,
    proposed_successor
)

The comparison and successor acceptance MUST occur while the mutation
serialization boundary is held.

Comparison before acquiring serialization is insufficient.

Publication after releasing serialization is insufficient.

The critical section MUST cover the complete authoritative
read -> compare -> validate -> publish -> advance transition.

---

## 5. Successor Sequence

A valid successor MUST advance monotonically by exactly one.

For transition witnesses:

successor.sequence = authoritative_head.sequence + 1

and:

successor.previous_event_sha512 =
    authoritative_head.event_sha512

For canonical state:

successor.state_sequence =
    authoritative_state.state_sequence + 1

and:

successor.prior_state_root =
    authoritative_state.active_state_root

Sequence allocation from stale writer-local state is invalid.

No sequence gap.

No rollback.

No competing accepted successor at the same sequence.

---

## 6. Single-Writer Serialization

The implementation MUST provide an inter-process serialization primitive for
each governed mutation domain.

The primitive MUST coordinate independently constructed writer instances.

A process-local object field is insufficient.

A route identifier is not a lock.

A timestamp callback is not a lock.

A filename-existence check is not a lock.

The serialization mechanism MUST have explicit acquisition and release
semantics and MUST release on failure.

---

## 7. Publication Atomicity

Successor artifact publication MUST remain durable and atomic.

The existing durability sequence is preserved in principle:

1. create exclusive temporary artifact;
2. write complete successor;
3. flush;
4. fsync artifact;
5. publish successor atomically;
6. fsync containing directory.

Publication MUST NOT silently overwrite a different accepted successor.

A pre-publication existence check alone is insufficient protection against
concurrent publication.

Serialization and expected-current validation provide the state-transition
boundary.

Atomic publication provides the artifact durability boundary.

These are distinct responsibilities.

---

## 8. Idempotent Retry

A repeated request representing the exact already-accepted successor MAY return
the previously accepted result without creating another transition.

Idempotent retry requires exact attributable equivalence.

At minimum, the implementation MUST distinguish:

- exact retry of accepted successor;
- stale retry from prior state;
- competing different successor;
- duplicate event identifier;
- duplicate sequence with different content.

Exact retry != new mutation.

Different content at an occupied successor position MUST fail closed.

---

## 9. Failure Atomicity

A failed mutation MUST NOT partially advance canonical state.

Failure before publication:

- no successor accepted;
- authoritative state unchanged.

Failure during publication:

- mutation disposition is failure;
- authoritative advancement MUST NOT be inferred;
- recovery MUST resolve durable state before another mutation proceeds.

Failure after durable successor publication but before in-memory writer state
update MUST be recoverable by authoritative re-resolution.

Writer-local memory MUST NOT become recovery authority.

---

## 10. State Pointer Boundary

State Pointer movement remains canonical mutation.

AC-09 does not redefine State Root semantics.

AC-09 does not redefine Manifest Pointer semantics.

AC-09 governs the atomic movement from one accepted State Pointer binding to
one accepted successor binding.

Manifest Pointer and State Pointer remain distinct.

Definition != state.

State != execution.

---

## 11. Transition Witness Boundary

The existing transition-witness ledger is historical implementation substrate.

AC-09 preserves its useful invariants:

- monotonically increasing sequence;
- previous-event SHA-512 linkage;
- deterministic event digest;
- exclusive temporary creation;
- artifact fsync;
- directory fsync;
- overwrite rejection intent.

AC-09 does not preserve stale writer-local head authority.

AC-09 does not preserve unprotected target.exists() -> rename() as a
concurrency guarantee.

Historical implementation != native mutation authority.

---

## 12. Authority Boundary

Atomic mutation mechanics do not grant mutation authority.

A request MUST already be admissible under applicable:

- Governance;
- authorization;
- Human Gate;
- canonical mutation policy;
- evidence boundary;
- evidence ceiling;
- provenance requirements.

Lock acquired != authorized.

CAS success != truth.

Durable write != authority.

Authority remains NONE.

Human Gate remains ACTIVE.

---

## 13. Required Failure Conditions

AC-09 MUST fail closed on:

- stale expected State Root;
- stale expected sequence;
- stale expected transition head;
- sequence gap;
- rollback;
- competing successor;
- occupied successor with different content;
- duplicate event identifier with different content;
- inability to acquire the mutation serialization primitive;
- inability to resolve authoritative current state;
- authoritative state changing outside the governed serialization boundary;
- publication collision;
- partial or unverifiable durable publication;
- missing authorization;
- missing provenance;
- Human Gate violation;
- attempted authority promotion.

No silent retry as a different mutation.

No last-writer-wins canonical semantics.

---

## 14. Validation Requirements

AC-09 validation MUST include at minimum:

1. single writer succeeds;
2. exact idempotent retry returns the accepted successor;
3. two writers constructed at the same predecessor cannot both commit distinct
   successors;
4. stale writer is rejected after another writer advances state;
5. concurrent competing successor attempts produce exactly one accepted
   successor;
6. sequence remains contiguous;
7. previous-event linkage remains exact;
8. publication does not overwrite an accepted successor;
9. failed publication does not silently advance authoritative state;
10. restart re-resolves durable authoritative state;
11. process-local cached head cannot override durable head;
12. lock release occurs after exceptions;
13. Authority remains NONE;
14. Human Gate remains ACTIVE.

The concurrency fixture MUST use independently constructed writer instances.

A test using only one writer object does not prove AC-09.

---

## 15. AC-09 Lock

Atomic publication != atomic state mutation.

Writer-local state != authoritative current state.

Route lock != concurrency lock.

Existence check != compare-and-swap.

Validation success != successor reservation.

Expected current MUST equal authoritative current inside serialization.

One predecessor may have at most one accepted direct successor in one governed
mutation lineage.

Sequence advances exactly once.

Exact retry != new mutation.

Competing successor fails closed.

No last-writer-wins canonical semantics.

Failure does not silently advance state.

Recovery resolves durable state.

Lock acquired != authorized.

CAS success != truth.

Durable write != authority.

Authority remains NONE.

Human Gate remains ACTIVE.
