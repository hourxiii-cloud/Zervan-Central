# R8-D — Pre-Promotion Verification

Status: CONTROLLED CANDIDATE
Ring: R8-D
Domain: HUMAN GATE / PROMOTION
Responsibility: PRE-PROMOTION READINESS VERIFICATION
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

## Purpose

R8-D performs bounded verification immediately before the Human Gate decision
and later promotion execution path.

R8-D verifies the candidate that exists in committed Git at verification time.

R8-D does not grant authorization.

R8-D does not create a Human Gate decision.

R8-D does not execute promotion.

R8-D does not merge branches.

R8-D does not mutate canonical state.

Verification != authorization.

Verification != execution.

## Entry State

R8-D requires:

- R7-N aggregate closure exists;
- R8-A Human Gate / Promotion Boundary exists;
- R8-B Promotion Decision Contract exists;
- R8-C Promotion Candidate Binding mechanism exists;
- current branch is candidate/v41-complete;
- target branch main resolves;
- candidate commit resolves;
- candidate tree resolves;
- candidate binding can be deterministically generated.

## Bounded Verification

R8-D is intentionally bounded.

It does not rerun the full Ring 6 or Ring 7 dependency tree.

It verifies the committed promotion-facing surfaces required for the next
decision boundary.

No full-tree rerun is required by R8-D.

## Candidate Commit Verification

The current candidate commit MUST resolve from:

candidate/v41-complete

The exact commit is recorded in the ephemeral verification result.

The verification result is not persisted into the candidate as a final binding.

Persisting that result during R8-D would create a new commit and invalidate the
candidate SHA it claimed to verify.

No self-invalidating verification receipt is permitted.

## Candidate Tree Verification

The candidate tree MUST resolve from the candidate commit.

The candidate tree provides a second immutable Git coordinate.

## Candidate Binding Verification

R8-D invokes the R8-C binding resolver against committed Git state.

The binding MUST preserve:

- exact candidate commit;
- exact candidate tree;
- candidate branch;
- target branch;
- Ring 7 closure blob;
- R8-A boundary blob;
- R8-B decision-contract blob;
- deterministic SHA-512 binding.

## Ring 7 Verification

The committed candidate MUST contain:

RING 7 RESULT: PASS

PROMOTION READINESS READY_FOR_HUMAN_GATE

Authority: NONE

Human Gate: ACTIVE

Promotion State: CANDIDATE

Canonical: FALSE

Promoted: FALSE

Merged: FALSE

Human Gate Authorization: NOT_GRANTED

R8-D does not reinterpret those states.

## R8-A Verification

R8-D verifies R8-A remains instantiated and preserves:

READY_FOR_HUMAN_GATE != authorization.

No promotion has occurred.

No merge has occurred.

No canonical mutation has occurred.

## R8-B Verification

R8-D verifies the Promotion Decision Contract still permits exactly:

APPROVE

REJECT

DEFER

R8-D does not choose one.

Decision instance remains NONE.

## R8-C Verification

R8-D verifies:

Promotion subject = exact immutable Git commit.

Branch name != immutable candidate identity.

Decision commit must equal binding commit.

Changed candidate requires new binding.

## Target Verification

The target branch is:

main

R8-D verifies main can be resolved from Git.

Target resolution does not authorize mutation.

Target resolution does not establish canonical transition.

## Working Tree Boundary

A promotion decision or execution MUST NOT proceed from an ambiguous working
tree.

At actual decision-binding time, unrelated uncommitted changes must be absent.

VERSION_REFERENCES.json drift must not be silently ignored at actual promotion
execution.

R8-D's development-time validator may run while R8-D itself is being authored,
but final decision-time verification must operate against committed state.

## Verification Result Fields

An ephemeral R8-D verification result contains:

- schema_version;
- record_type;
- ring;
- native_version;
- implementation_identity;
- candidate_branch;
- candidate_commit;
- candidate_tree;
- target_branch;
- target_commit;
- ring7_ready;
- r8a_valid;
- r8b_valid;
- r8c_valid;
- binding_sha512;
- decision_instance;
- human_gate_authorization;
- authority_state;
- human_gate_state;
- promotion_state;
- canonical;
- promoted;
- merged;
- disposition.

## Disposition

Successful bounded verification produces:

PRE_PROMOTION_VERIFIED

This means the candidate is structurally ready to be presented to the Human
Gate decision path.

PRE_PROMOTION_VERIFIED != APPROVE.

PRE_PROMOTION_VERIFIED != authorization.

PRE_PROMOTION_VERIFIED != promotion.

PRE_PROMOTION_VERIFIED != canonical.

## Authority Boundary

Decision instance remains NONE.

Human Gate Authorization remains NOT_GRANTED.

Authority remains NONE.

Human Gate remains ACTIVE.

Promotion State remains CANDIDATE.

Canonical remains FALSE.

Promoted remains FALSE.

Merged remains FALSE.

## R8-D Lock

R8-D = Pre-Promotion Verification.

Verification target = committed candidate state.

Verification is bounded.

Full-tree rerun = NOT REQUIRED.

Exact candidate commit = REQUIRED.

Exact candidate tree = REQUIRED.

Target main resolution = REQUIRED.

R8-A / R8-B / R8-C validity = REQUIRED.

Decision instance = NONE.

PRE_PROMOTION_VERIFIED != APPROVE.

PRE_PROMOTION_VERIFIED != authorization.

PRE_PROMOTION_VERIFIED != promotion.

No self-invalidating verification receipt is permitted.

Human Gate Authorization remains NOT_GRANTED.

Authority remains NONE.

Human Gate remains ACTIVE.

Promotion State remains CANDIDATE.

Canonical remains FALSE.

Promoted remains FALSE.

Merged remains FALSE.

R8-D PRE-PROMOTION VERIFICATION COMPLETE.

R8-E owns Human Gate Authorization Receipt.
