# R8-C — Promotion Candidate Binding

Status: CONTROLLED CANDIDATE
Ring: R8-C
Domain: HUMAN GATE / PROMOTION
Responsibility: EXACT PROMOTION SUBJECT BINDING
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

## Purpose

R8-C defines how a future Human Gate promotion decision is bound to one exact
candidate object in Git.

The decision must authorize an immutable candidate commit.

The decision must not authorize a moving branch name.

Candidate binding != decision.

Candidate binding != authorization.

Candidate binding != execution.

## Entry State

R8-C begins from completed R8-B Promotion Decision Contract.

R8-B requires:

candidate_branch = candidate/v41-complete

candidate_commit = exact 40-character Git commit SHA

target_branch = main

Human Gate Authorization remains NOT_GRANTED.

## Binding Object

A Promotion Candidate Binding contains:

- schema_version;
- record_type;
- ring;
- native_version;
- implementation_identity;
- repository;
- candidate_branch;
- candidate_commit;
- candidate_tree;
- target_branch;
- ring7_closure_path;
- ring7_closure_blob;
- r8a_boundary_path;
- r8a_boundary_blob;
- r8b_decision_contract_path;
- r8b_decision_contract_blob;
- binding_serialization;
- binding_sha512;
- authority_state;
- human_gate_state.

## Exact Candidate Commit

candidate_commit identifies the immutable Git commit proposed for promotion.

The commit must exist.

The commit must resolve from the candidate branch at binding time.

Branch identity alone is insufficient.

candidate/v41-complete != immutable candidate identity.

The exact commit is the promotion subject.

## Candidate Tree

candidate_tree records the Git tree referenced by candidate_commit.

The tree provides an additional integrity coordinate for the candidate content.

Commit identity remains the promotion subject.

Tree identity does not replace commit identity.

## Source Branch

candidate_branch is:

candidate/v41-complete

The branch identifies source lineage.

The branch is not the authorization subject.

A later branch movement does not change an existing binding.

## Target Branch

target_branch is:

main

Target branch identity does not imply mutation.

Target branch identity does not imply canonical state.

## Ring 7 Closure Binding

The candidate binding preserves the exact Git blob identity for:

contracts/validation/RING7_AGGREGATE_DOCUMENTATION_PROMOTION_READINESS_CLOSURE.md

This proves which Ring 7 readiness closure was visible in the candidate being
presented.

## R8-A Binding

The candidate binding preserves the exact Git blob identity for:

contracts/promotion/RING8_HUMAN_GATE_PROMOTION_BOUNDARY.md

This preserves the Human Gate boundary used by the promotion process.

## R8-B Binding

The candidate binding preserves the exact Git blob identity for:

contracts/promotion/PROMOTION_DECISION_CONTRACT.md

This preserves the decision semantics under which a later Human Gate decision
is made.

## Deterministic Binding

The binding serialization is deterministic JSON using:

- UTF-8;
- sorted keys;
- compact separators;
- no implicit fields.

binding_sha512 is SHA-512 over that deterministic serialization.

SHA-512 proves integrity of the binding representation.

Hash != truth.

Hash != authority.

Hash != approval.

## Binding-Time Resolution

The binding is resolved from Git at the time the promotion subject is prepared.

R8-C does not persist a live binding instance into the candidate during its own
construction.

Doing so would change the candidate commit after the binding was calculated.

R8-C therefore defines and validates the binding mechanism without creating a
false self-referential candidate identity.

## Branch Movement

After a binding is created:

candidate/v41-complete may later move.

The binding does not move with it.

A decision bound to commit A does not authorize commit B.

A changed candidate requires a new binding and a new governed decision path.

## Decision Binding

The candidate_commit field in a future Promotion Decision MUST equal the
candidate_commit in the accepted Promotion Candidate Binding.

The candidate_branch MUST also agree.

The target_branch MUST also agree.

Mismatch blocks promotion.

## Verification

A binding verifier must be able to establish:

- candidate commit exists;
- candidate tree exists;
- bound paths exist at that commit;
- bound blob identities match;
- deterministic serialization reproduces binding_sha512;
- branch lineage is declared;
- target is main;
- authority has not been promoted by the binding.

## No Decision Instance

R8-C creates no Human Gate decision.

R8-C creates no APPROVE.

R8-C creates no REJECT.

R8-C creates no DEFER.

R8-C creates no authorization receipt.

R8-C performs no merge.

R8-C performs no canonical mutation.

## Authority Boundary

Authority remains NONE.

Human Gate remains ACTIVE.

Human Gate Authorization remains NOT_GRANTED.

Promotion State remains CANDIDATE.

Canonical remains FALSE.

Promoted remains FALSE.

Merged remains FALSE.

## R8-C Lock

R8-C = Promotion Candidate Binding.

Promotion subject = exact immutable Git commit.

Branch name != immutable candidate identity.

Decision commit must equal binding commit.

Changed candidate requires new binding.

Binding != decision.

Binding != authorization.

Binding != execution.

Hash != truth.

Hash != authority.

Hash != approval.

No self-referential candidate binding is permitted.

Human Gate Authorization remains NOT_GRANTED.

Authority remains NONE.

Human Gate remains ACTIVE.

Promotion State remains CANDIDATE.

Canonical remains FALSE.

Promoted remains FALSE.

Merged remains FALSE.

R8-C PROMOTION CANDIDATE BINDING COMPLETE.

R8-D owns Pre-Promotion Verification.
