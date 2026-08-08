# R8-E — Human Gate Authorization Receipt

Status: CONTROLLED CANDIDATE
Ring: R8-E
Domain: HUMAN GATE / PROMOTION
Responsibility: HUMAN GATE DECISION / AUTHORIZATION RECORD
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

## Purpose

R8-E defines and enforces the Human Gate authorization receipt.

R8-E is the hard stop between verified promotion readiness and promotion
execution.

No downstream promotion execution may occur without a valid Human Gate
Authorization Receipt whose decision is APPROVE and whose authorization state is
GRANTED.

R8-E implementation != Human Gate decision.

R8-E contract != authorization.

Receipt mechanism != authorization.

Only an explicit Human Gate decision may create an authorization receipt.

## Entry State

R8-E begins only after:

R8-D PRE-PROMOTION VERIFICATION COMPLETE.

PRE_PROMOTION_VERIFIED.

Decision instance = NONE.

Human Gate Authorization = NOT_GRANTED.

Authority = NONE.

Human Gate = ACTIVE.

Promotion State = CANDIDATE.

Canonical = FALSE.

Promoted = FALSE.

Merged = FALSE.

## Allowed Decisions

The Human Gate decision MUST be exactly one of:

APPROVE

REJECT

DEFER

No decision may be inferred from implementation progress.

No decision may be inferred from validation success.

No decision may be inferred from the existence of this receipt mechanism.

## Authorization Mapping

The decision-to-authorization mapping is exact:

APPROVE -> GRANTED

REJECT -> DENIED

DEFER -> DEFERRED

No other mapping is valid.

## APPROVE

APPROVE records Human Gate permission for the exact bound candidate to proceed
to the separately controlled execution path.

APPROVE does not execute promotion.

APPROVE does not merge branches.

APPROVE does not mutate main.

APPROVE does not itself establish canonical state.

APPROVE does not change Zervan runtime Authority from NONE.

Approval != execution.

## REJECT

REJECT produces authorization state DENIED.

Promotion execution MUST NOT proceed.

The candidate remains preserved.

The decision and provenance remain preserved.

## DEFER

DEFER produces authorization state DEFERRED.

Promotion execution MUST NOT proceed.

The candidate remains preserved.

A later decision requires a new governed Human Gate receipt.

## Required Receipt Binding

A Human Gate Authorization Receipt MUST bind:

- exact candidate commit;
- exact candidate tree;
- candidate branch;
- target branch;
- candidate binding SHA-512;
- Human Gate decision;
- decision actor;
- decision timestamp;
- decision scope;
- rationale;
- provenance.

The receipt may not authorize a moving branch name without an exact commit.

## Human Decision Actor

decision_actor MUST be explicitly supplied by the Human Gate.

The actor may not be inferred from:

- Git commit author;
- repository owner;
- validator identity;
- operating-system user;
- ChatGPT identity;
- automation identity.

Human identity must be explicitly supplied at decision time.

## Decision Timestamp

decision_timestamp MUST be explicitly recorded when the Human Gate decision is
issued.

A timestamp alone does not create authority.

## Decision Scope

decision_scope defines exactly what Human Gate authorizes or declines.

APPROVE authorizes only the recorded scope.

Scope may not silently expand during execution.

## Candidate Binding

candidate_commit MUST equal the candidate commit supplied by the accepted R8-C
binding.

candidate_tree MUST equal the candidate tree supplied by the accepted R8-C
binding.

binding_sha512 MUST equal the R8-C deterministic candidate binding hash.

Mismatch blocks receipt issuance.

## Receipt Immutability

Once issued, the receipt records one Human Gate decision against one exact
candidate binding.

A changed candidate requires:

- new R8-C binding;
- new R8-D verification;
- new Human Gate decision;
- new R8-E receipt.

Authorization does not float with branch HEAD.

## Execution Separation

Every R8-E receipt MUST record:

promotion_executed = false

canonical = false

promoted = false

merged = false

The receipt proves the Human Gate decision.

The receipt does not prove execution.

The receipt does not prove promotion.

The receipt does not prove merge.

The receipt does not prove canonical state.

## Authority Boundary

Zervan runtime Authority remains NONE.

Human Gate remains ACTIVE.

If decision = APPROVE:

Human Gate Authorization = GRANTED.

If decision = REJECT:

Human Gate Authorization = DENIED.

If decision = DEFER:

Human Gate Authorization = DEFERRED.

These states record Human Gate disposition.

They do not grant autonomous authority to Zervan.

## Current Implementation State

No Human Gate decision has been supplied during R8-E implementation.

Decision instance = NONE.

Human Gate Authorization = NOT_GRANTED.

Promotion executed = FALSE.

Canonical = FALSE.

Promoted = FALSE.

Merged = FALSE.

Authority = NONE.

Human Gate = ACTIVE.

Promotion State = CANDIDATE.

## Execution Gate

R8-F MUST NOT begin as an executable promotion path unless:

decision = APPROVE

authorization_state = GRANTED

candidate binding matches

R8-D verification is valid

receipt validates

Any other state blocks execution.

## R8-E Lock

R8-E = Human Gate Authorization Receipt.

R8-E is the Human Gate hard stop.

Decision states = APPROVE / REJECT / DEFER.

APPROVE -> GRANTED.

REJECT -> DENIED.

DEFER -> DEFERRED.

Approval != execution.

Authorization receipt != execution.

Authorization does not float with branch HEAD.

Exact candidate binding = REQUIRED.

Explicit human decision actor = REQUIRED.

Decision scope = REQUIRED.

Decision timestamp = REQUIRED.

Promotion executed by receipt = FALSE.

Canonical established by receipt = FALSE.

Promoted established by receipt = FALSE.

Merged established by receipt = FALSE.

Current decision instance = NONE.

Current Human Gate Authorization = NOT_GRANTED.

Authority remains NONE.

Human Gate remains ACTIVE.

Promotion State remains CANDIDATE.

R8-E AUTHORIZATION RECEIPT MECHANISM COMPLETE.

RING 8 STATE = WAITING_FOR_HUMAN_GATE.

R8-F is blocked until explicit Human Gate APPROVE authorization exists.
