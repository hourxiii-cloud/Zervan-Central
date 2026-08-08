# R8-I — Post-Promotion Integrity Verification

Status: CONTROLLED CANONICAL
Ring: R8-I
Domain: HUMAN GATE / PROMOTION
Responsibility: POST-PROMOTION INTEGRITY VERIFICATION
Authority: NONE
Human Gate: ACTIVE

## Purpose

R8-I verifies that the canonical state resulting from R8-G and R8-H preserves
the exact Human Gate-approved promotion subject and contains no unauthorized
promotion delta.

R8-I is verification-only.

R8-I does not perform another promotion.

R8-I does not move the preserved candidate branch.

R8-I does not grant new authority.

Integrity verification != authority.

Integrity verification != promotion.

## Promotion Anchors

Approved candidate commit:

2d1013304c6c13efd08fc3a9d7aed7804642cde2

R8-H canonical-transition commit:

62bd3c9f54d46034181c9d94a443757a857423c1

The approved candidate MUST be an ancestor of the R8-H canonical-transition
commit.

The R8-H commit MUST remain in canonical main lineage.

## Candidate Preservation

origin/candidate/v41-complete MUST remain exactly:

2d1013304c6c13efd08fc3a9d7aed7804642cde2

The candidate branch is the preserved approved promotion subject.

Post-promotion canonical work belongs to main.

Candidate preservation prevents post-approval mutation from being silently
reclassified as part of the approved candidate.

## Canonical Main

The canonical main lineage MUST contain:

1. the exact approved candidate;
2. the R8-H canonical-transition commit;
3. any later governed post-promotion verification commits.

The current VERSION.json state MUST resolve:

promotion_state = CANONICAL

canonical = true

canonical_branch = main

## Authorized R8-H Delta

The complete authorized delta between the approved candidate and the R8-H
canonical-transition commit is exactly:

- README.md
- VERSION.json
- VERSION_AUTHORITY.md
- VERSION_REFERENCES.json
- canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md
- contracts/promotion/CANONICAL_VERSION_AUTHORITY_TRANSITION.md
- receipts/promotion/R8_E_HUMAN_GATE_AUTHORIZATION_RECEIPT.json
- schemas/promotion/canonical_version_authority_transition.schema.json
- tests/test_canonical_version_authority_transition.py
- tools/validate_canonical_version_authority_transition.py
- tools/validate_ring8.py

No additional file belongs to the R8-H canonical-transition delta.

The R8-H delta count is exactly 11 files.

## Human Gate Provenance

The preserved Human Gate Authorization Receipt MUST remain bound to:

decision = APPROVE

authorization_state = GRANTED

candidate_commit = 2d1013304c6c13efd08fc3a9d7aed7804642cde2

target_branch = main

decision_actor = human

decision_scope = complete

rationale = I approve

The receipt's historical pre-execution fields remain immutable.

They are not rewritten to claim post-execution state.

## R8-H Integrity

The R8-H canonical-transition contract MUST continue to state:

Promotion State = CANONICAL.

Canonical = TRUE.

Candidate preserved = TRUE.

Human Gate Authorization = GRANTED.

Authority remains NONE.

Human Gate remains ACTIVE.

## Runner State Integrity

The Ring 8 runner MUST no longer report stale pre-promotion state after R8-H.

The active Ring 8 footer MUST report:

R8-G: PROMOTION EXECUTED

R8-H: CANONICAL TRANSITION COMPLETE

R8-E Human Gate Authorization: GRANTED

Post-Promotion Integrity: VERIFIED

Candidate preserved: TRUE

Canonical: TRUE

Authority: NONE

Human Gate: ACTIVE

Promotion State: CANONICAL

The active footer MUST NOT report:

Human Gate Authorization: NOT_GRANTED

Promotion State: CANDIDATE

## Authority Boundary

Authority remains NONE.

Human Gate remains ACTIVE.

Canonical state does not create autonomous runtime authority.

External runtime remains disabled.

External action remains disabled.

System population remains disallowed.

## Disposition

Successful R8-I verification produces:

POST_PROMOTION_INTEGRITY_VERIFIED

This means:

- approved candidate ancestry is preserved;
- candidate branch remains frozen;
- canonical main contains the governed transition;
- Human Gate provenance is preserved;
- authorized R8-H delta is exact;
- canonical/version state agrees;
- stale pre-promotion runner state is removed.

POST_PROMOTION_INTEGRITY_VERIFIED != new authority.

## R8-I Lock

R8-I = Post-Promotion Integrity Verification.

Approved candidate ancestry = REQUIRED.

R8-H canonical-transition ancestry = REQUIRED.

Candidate branch preservation = REQUIRED.

Authorized R8-H delta = EXACT.

Authorized R8-H delta count = 11.

Human Gate provenance = PRESERVED.

Canonical state agreement = REQUIRED.

Stale pre-promotion runner state = REJECTED.

Authority remains NONE.

Human Gate remains ACTIVE.

Disposition = POST_PROMOTION_INTEGRITY_VERIFIED.

R8-I POST-PROMOTION INTEGRITY VERIFICATION COMPLETE.

R8-J owns Post-Promotion Fresh Reader.
