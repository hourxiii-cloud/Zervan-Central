# AC-07 — Cross-Stage Semantic Integrity

Status: ACTIVATION CORRECTION
Version: vTemporal.41.0
Authority: NONE
Human Gate: ACTIVE

## 0. Purpose

AC-07 mechanically enforces semantic integrity across the composed native-v41
analytical pipeline:

PMC
-> CCR
-> MC
-> Raven
-> Human Gate

AC-07 does not redefine any stage.

AC-07 does not transfer responsibility between stages.

AC-07 validates that independently valid stages compose into one globally
possible analytical state.

Local validity != composed validity.

Stage PASS != composition PASS.

## 1. Governing Law

A composed analytical transition is valid only when:

1. every represented stage is locally attributable;
2. every adjacent stage transition preserves its required semantic invariants;
3. the end-to-end composition preserves its global invariants; and
4. no stage output claims a state impossible under its upstream lineage.

Every stage may be locally valid while the composition is invalid.

AC-07 therefore validates both seams and composition.

## 2. Pipeline Order

The governed composition order is:

PMC
-> CCR
-> MC
-> Raven
-> Human Gate

A stage MUST NOT be silently skipped.

A downstream stage MUST NOT manufacture an upstream state that never existed.

## 3. Cross-Stage Coordinate

The composition preserves independently meaningful dimensions including:

- canonical object / Room identity;
- Room revision identity;
- Room state root;
- Authorized View Root;
- candidate identities;
- candidate membership;
- candidate ordering;
- rejected-candidate state;
- uncertainty and material unknowns;
- evidence boundary;
- evidence ceiling / Maximum Justified Claim;
- governance constraints;
- analytical claim strength;
- stage-specific disposition;
- transformation lineage;
- provenance;
- Human Gate state.

These dimensions are not one flat pipeline status.

A change in one dimension MUST NOT silently mutate another.

## 4. PMC -> CCR

CCR MUST commit only attributable PMC output.

CCR MUST NOT:

- commit a candidate PMC did not emit;
- reorder candidates while claiming preserved commitment identity;
- remove rejected candidates from attributable history;
- erase uncertainty;
- strengthen candidate state;
- broaden the evidence boundary;
- raise the evidence ceiling.

Equivalent PMC candidate state and equivalent Room-bound lineage MUST produce
equivalent CCR semantic commitment.

AR-046 is BLOCKED by candidate provenance.

AR-047 is BLOCKED by rejected-candidate preservation.

AR-048 is BLOCKED by candidate-order and uncertainty preservation.

## 5. CCR -> MC

MC MUST consume the attributable CCR state.

MC MUST NOT:

- invent or remove governance constraints;
- reorder or reinterpret committed analytical state;
- erase uncertainty;
- raise the evidence ceiling;
- broaden the evidence boundary;
- treat CONDITIONAL as ADMISSIBLE without attributable condition satisfaction;
- manufacture analytical truth from admissibility.

MC disposition is a new governed dimension.

MC disposition does not rewrite CCR analytical state.

AR-049 is BLOCKED by governance-constraint lineage.

AR-050 is BLOCKED by evidence-ceiling continuity.

AR-051 is BLOCKED by conditional-state continuity.

## 6. MC -> Raven

Raven MUST preserve the supported meaning of the MC-bound analytical state.

Raven MUST NOT:

- strengthen a claim without an attributable analytical-state change;
- suppress material uncertainty;
- suppress material unknowns;
- change evidence boundary;
- raise evidence ceiling;
- change MC disposition;
- convert presentation emphasis into analytical rank;
- replace lineage with rendered prose.

Different wording may preserve identical bounded meaning.

Rendering != analytical mutation.

AR-052 is BLOCKED by material-unknown and uncertainty preservation.

AR-053 is BLOCKED by claim-strength continuity.

## 7. Raven -> Human Gate

Human Gate receives attributable Raven representation.

Human Gate review MUST preserve:

- upstream analytical lineage;
- Room identity;
- revision;
- state root;
- Authorized View Root;
- evidence boundary;
- evidence ceiling;
- material uncertainty;
- MC disposition;
- governance constraints.

Human Gate approval governs movement.

Human Gate approval does not rewrite analytical meaning.

Human Gate decision != analytical mutation.

## 8. Cross-Object Integrity

One composed pipeline chain MUST remain bound to one canonical Room Object unless
an explicit governed cross-object relationship or transition is represented.

Evidence or state from another object MUST NOT silently enter the composition.

Similar content != same object.

Cross-object contamination = composition failure.

AR-063 is BLOCKED by object-continuity enforcement.

## 9. Global Possibility

The final composed state MUST be possible under all preserved upstream state.

A composition is globally impossible when, for example:

- CCR commits a candidate absent from PMC;
- a rejected candidate disappears;
- MC exceeds the inherited evidence ceiling;
- MC invents or drops a governance constraint;
- CONDITIONAL becomes effectively ADMISSIBLE without satisfaction;
- Raven strengthens a claim without analytical change;
- Raven removes material uncertainty or unknowns;
- object identity changes without governed transition;
- Human Gate receives a state not attributable to Raven and its upstream chain.

A globally impossible state MUST be BLOCKED even when every individual stage
record independently validates.

AR-064 is BLOCKED by aggregate composition validation.

## 10. Composition Disposition

AC-07 recognizes:

- VALID;
- BLOCKED.

VALID requires both:

LOCAL_STAGE_VALIDITY
and
CROSS_STAGE_SEMANTIC_INTEGRITY.

BLOCKED requires one or more attributable failure reasons.

No silent repair.

No inferred missing stage.

No synthetic lineage.

## 11. Failure Reasons

AC-07 recognizes at minimum:

- STAGE_SEQUENCE_INVALID;
- PMC_CANDIDATE_NOT_EMITTED;
- REJECTED_CANDIDATE_LOST;
- CANDIDATE_ORDER_CHANGED;
- UNCERTAINTY_ERASED;
- MATERIAL_UNKNOWN_SUPPRESSED;
- EVIDENCE_BOUNDARY_CHANGED;
- EVIDENCE_CEILING_RAISED;
- GOVERNANCE_CONSTRAINT_INVENTED;
- GOVERNANCE_CONSTRAINT_DROPPED;
- CONDITIONAL_STATE_PROMOTED;
- CLAIM_STRENGTH_INCREASED;
- OBJECT_IDENTITY_CHANGED;
- CROSS_OBJECT_CONTAMINATION;
- LINEAGE_BROKEN;
- PROVENANCE_BROKEN;
- GLOBAL_STATE_IMPOSSIBLE.

Failure reasons accumulate.

## 12. Existing-Semantics Boundary

AC-07 activates existing native-v41 semantics.

R5-B remains Room-Bound Evidence -> PMC Intake.

R5-C remains PMC -> CCR Candidate Commitment Lineage.

R5-D remains CCR -> MC Response / Output Admissibility.

R5-E remains MC -> Raven Representation.

R5-F remains Raven -> Human Gate.

R5-I remains Pipeline Cross-Stage Integrity / No-Responsibility-Absorption.

AC-07 does not absorb those responsibilities.

Composition validation != stage ownership.

## 13. Authority Boundary

Cross-stage validation creates no authority.

VALID != publication approval.

VALID != execution readiness.

VALID != Human Gate approval.

Authority remains NONE.

Human Gate remains ACTIVE.

## 14. AC-07 Lock

Local validity != composed validity.

Stage PASS != composition PASS.

PMC -> CCR -> MC -> Raven -> Human Gate MUST preserve attributable analytical
meaning across the complete composition.

Candidate identity survives commitment.

Rejected candidates remain attributable.

Candidate ordering remains attributable.

Uncertainty remains uncertainty.

Material unknowns remain visible.

Evidence boundary remains bounded.

Evidence ceiling remains bounded.

Governance constraints remain attributable.

CONDITIONAL remains conditional until attributable satisfaction.

Rendering does not strengthen analysis.

One chain does not silently become another Room.

Every stage may pass while the composition fails.

Globally impossible analytical state = BLOCKED.

No silent repair.

No responsibility absorption.

Authority remains NONE.

Human Gate remains ACTIVE.
