# R5-C — PMC -> CCR Candidate Commitment Lineage

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R5-C
Version: vTemporal.41.0
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

R5-C binds PMC output into a Canonical Commitment Record.

CCR means Canonical Commitment Record.

CCR is the deterministic candidate commitment / report record produced after PMC
evaluation and before MC response-admissibility gating.

R5-C does not redefine PMC.

R5-C does not redefine MC.

R5-C does not authorize action.

R5-C preserves PMC analytical state without reinterpreting it.

Commitment record != canonical promotion.

Candidate commitment != action commitment.

---

## 1. Pipeline Position

Native-v41 sequence remains:

Evidence
-> PMC
-> CCR
-> MC
-> Raven
-> Human Gate

R5-C owns only:

PMC Output
-> CCR

R5-C does not implement CCR -> MC.

R5-D owns CCR -> MC.

Direct PMC -> MC routing is not valid native-v41 pipeline execution.

---

## 2. CCR Meaning

CCR means Canonical Commitment Record.

The word `Canonical` in the CCR name identifies the defined record type.

It does not mean the record has been promoted into canonical doctrine, canonical
Room state, Git main, or authority-bearing truth.

CCR != canonical promotion.

CCR != Human Gate approval.

CCR != Registry state mutation.

---

## 3. PMC Source Binding

Every CCR MUST identify the PMC analytical artifact from which it was produced.

The CCR MUST preserve attributable PMC output state, including where applicable:

- PMC run identifier;
- PMC intake binding identifier;
- selected world identifier or explicit null selection;
- deterministic candidate ordering;
- rejected-world references or rejection reasons;
- uncertainty annotations;
- unresolved contradiction references;
- evidence references;
- evidence boundary;
- evidence ceiling / Maximum Justified Claim;
- invariants checked;
- replay / reconstruction reference;
- provenance.

CCR may record PMC output.

CCR may not reinterpret PMC output.

---

## 4. No Truth Reinterpretation

CCR construction is deterministic transcription / commitment of admissible PMC
output into the downstream candidate record form.

CCR MUST NOT:

- create a new selected world;
- change selected world;
- rank worlds differently;
- remove a PMC rejection;
- create new evidence;
- remove uncertainty;
- resolve contradiction by assumption;
- raise the evidence ceiling;
- broaden the evidence boundary;
- invent governance context;
- invent attribution;
- convert advisory interpretation into authority.

CCR construction may not reinterpret PMC truth.

---

## 5. Null / Denied PMC Outcome

PMC may validly produce NULL collapse or denial.

CCR MUST preserve that outcome.

A null selection MUST NOT be silently replaced by:

- a winner;
- a default world;
- the highest-confidence world;
- a prior result;
- a convenient narrative.

NULL PMC outcome != pipeline error.

A CCR representing NULL PMC outcome may continue only as allowed by downstream
contracts.

CCR does not manufacture success.

---

## 6. Room Identity Binding

CCR MUST preserve the canonical Room Object identity associated with the PMC
intake.

CCR does not own Room identity.

CCR does not create a new Room.

PMC -> CCR handoff MUST NOT silently change Room Object identity.

Same analytical result under another Room Object requires a separately
attributable pipeline instance.

---

## 7. Room Revision / State / View

CCR MUST preserve:

- Room revision identity;
- Room state root;
- Authorized View Root.

These values identify the Room state under which PMC operated.

CCR creation does not mutate those values.

CCR may reference state.

CCR does not own state.

---

## 8. Evidence Lineage

CCR MUST preserve traceability to the Room-bound evidence admitted to PMC.

The route remains:

Room-Bound Evidence
-> PMC Intake
-> PMC Output
-> CCR

Evidence lineage MUST remain available for downstream MC, Raven, Human Gate,
decision-option, and report-contract bindings.

CCR MUST NOT replace evidence lineage with a summary-only representation.

---

## 9. Coordinate Continuity

CCR MUST preserve the observational coordinate or coordinate reference
associated with the PMC analysis.

CCR does not own Cartography.

CCR may reference coordinate state without changing it.

Coordinate reference != Cartography ownership.

---

## 10. Representation Continuity

CCR MUST preserve the representation / transform context under which PMC
evaluated the evidence.

CCR MUST NOT silently substitute another perspective.

CCR MUST NOT broaden the Authorized View.

Representation preservation != representation ownership.

---

## 11. Evidence Boundary

CCR MUST preserve the PMC evidence boundary.

CCR MUST NOT admit new evidence.

CCR MUST NOT silently widen historical evidence access.

Evidence available later != evidence admitted to PMC.

CCR records the PMC-bound boundary.

---

## 12. Evidence Ceiling

CCR MUST preserve the PMC evidence ceiling / Maximum Justified Claim.

CCR MUST NOT raise claim authority.

High confidence != higher claim ceiling.

Selected world != unrestricted claim authority.

CCR commitment != certainty.

---

## 13. Uncertainty

CCR MUST preserve PMC uncertainty annotations.

Uncertainty may include:

- ambiguity;
- confidence limits;
- unresolved alternatives;
- contradiction;
- conditions under which truth becomes unavailable;
- evidence insufficiency.

Uncertainty MUST NOT disappear merely because a CCR exists.

Commitment record != uncertainty elimination.

---

## 14. Rejections

PMC rejection history MUST remain attributable.

CCR MUST preserve the rejected candidate route or references sufficient to
reconstruct it.

Rejected != deleted.

Rejected != nonexistent.

Selected != only world that ever existed.

No Compression Out applies to rejected-world lineage.

---

## 15. Deterministic Candidate Commitment

Equivalent PMC outputs and equivalent Room-bound lineage MUST produce the same
CCR identity.

CCR construction MUST use deterministic canonicalization.

No random fields.

No hidden defaults.

No hidden heuristic winner selection.

No timestamp may participate in CCR identity unless it is an attributable input
to the record.

---

## 16. CCR Record

Every CCR MUST preserve:

- `ccr_id`;
- `object_id`;
- `room_revision_id`;
- `room_state_root`;
- `authorized_view_root`;
- `pmc_intake_binding_id`;
- `pmc_run_id`;
- `pmc_output_reference`;
- `selected_world_id`;
- `candidate_ordering`;
- `rejection_references`;
- `evidence_references`;
- `evidence_boundary_reference`;
- `evidence_ceiling_reference`;
- `coordinate_reference`;
- `representation_reference`;
- `transform_references`;
- `uncertainty_references`;
- `unresolved_state_references`;
- `invariants_checked_references`;
- `replay_reference`;
- `lineage_reference`;
- `provenance_route`;
- `commitment_disposition`;
- `blocking_reasons`;
- `authority_state`;
- `human_gate_state`.

---

## 17. Commitment Disposition

Native R5-C defines:

- `CANDIDATE_RECORDED`;
- `NULL_RECORDED`;
- `BLOCKED`.

`CANDIDATE_RECORDED` means a non-null PMC candidate selection has been
deterministically bound into CCR.

`NULL_RECORDED` means PMC produced a valid null / denied selection and the CCR
preserves that state.

`BLOCKED` means a defensible CCR cannot be constructed because required PMC or
lineage state is incomplete, contradictory, or non-reconstructible.

CANDIDATE_RECORDED != canonical promotion.

NULL_RECORDED != failure.

BLOCKED != PMC truth reversal.

---

## 18. Selected World

When `selected_world_id` is non-null:

- it MUST derive from the PMC output;
- it MUST appear in the candidate ordering;
- CCR MUST NOT substitute another candidate.

When PMC selection is null:

- `selected_world_id` MUST remain null;
- disposition MUST NOT be `CANDIDATE_RECORDED`.

CCR does not select the world.

PMC selects or denies.

CCR records.

---

## 19. Candidate Ordering

CCR preserves the deterministic PMC candidate ordering.

Ordering MUST NOT be changed to improve presentation.

Ordering MUST NOT be changed to favor an admissible response.

Ordering MUST NOT be changed by MC.

PMC ordering remains PMC ordering.

---

## 20. Replayability

CCR MUST preserve sufficient replay / reconstruction reference to recover the
PMC state from which it was constructed.

If the source PMC state cannot be reconstructed, CCR is BLOCKED.

CCR identity without reconstructability is insufficient.

Receipt != truth.

Hash != truth.

---

## 21. CCR -> MC Boundary

R5-C prepares the exact downstream candidate record that R5-D may bind into MC.

MC receives CCR.

MC does not receive permission to bypass CCR and reinterpret raw PMC output as
the native-v41 path.

CCR is mandatory between PMC and MC in Ring 5.

R5-C does not perform MC admissibility.

---

## 22. Legacy Direct PMC -> MC Collision

`Doctrine/PMC_MC_INTERFACE.md` contains historical direct PMC -> MC wording.

R5-A records this as an interface collision requiring CCR preservation.

R5-C enforces the native route by making CCR an explicit deterministic
artifact.

The legacy interface artifact remains preserved.

It is not deleted.

It is not silently rewritten.

It is not executable as a CCR bypass in native Ring 5.

Historical artifact != active native route.

---

## 23. Responsibility Separation

PMC owns epistemic evaluation.

CCR owns deterministic candidate commitment record construction.

MC owns response / output admissibility.

Registry owns Room state.

Governance owns boundaries and claim ceilings.

Audit verifies.

Raven renders.

Human Gate governs authority-bearing action where required.

CCR does not absorb any of those responsibilities.

---

## 24. Authority Boundary

CCR creates no action authority.

CCR creates no publication authority.

CCR creates no certification authority.

CCR creates no canonical promotion authority.

Authority remains NONE.

Human Gate remains ACTIVE.

Write capability != authority.

Deterministic record != authority.

---

## 25. No Compression Out

CCR may use references rather than embed all source content.

References MUST preserve reconstructability.

CCR MUST preserve independently meaningful:

- evidence lineage;
- candidate ordering;
- rejections;
- uncertainty;
- unresolved states;
- boundary;
- claim ceiling;
- coordinate;
- representation;
- replay route;
- provenance.

CCR is not permission to flatten PMC history into the selected world alone.

---

## 26. Failure Conditions

R5-C MUST reject:

- missing PMC intake binding;
- missing PMC run identifier;
- missing PMC output reference;
- Room identity mismatch;
- revision/state/view loss;
- evidence-lineage loss;
- coordinate loss;
- representation loss;
- evidence-boundary change;
- evidence-ceiling promotion;
- selected world not present in PMC candidate ordering;
- null PMC result converted into candidate selection;
- uncertainty removed;
- rejection history silently discarded;
- replay reference absent;
- provenance absent;
- CCR used as canonical promotion;
- CCR used as action authority;
- direct PMC -> MC native bypass.

Fail closed.

Do not reinterpret PMC output to repair the record.

---

## 27. R5-C Lock

CCR means Canonical Commitment Record.

CCR is the deterministic candidate commitment / report record produced after PMC
evaluation and before MC response-admissibility gating.

R5-C does not redefine PMC.

R5-C does not redefine MC.

R5-C does not authorize action.

R5-C preserves PMC analytical state without reinterpreting it.

Commitment record != canonical promotion.

Candidate commitment != action commitment.

Direct PMC -> MC routing is not valid native-v41 pipeline execution.

CCR != canonical promotion.

CCR != Human Gate approval.

CCR != Registry state mutation.

CCR may record PMC output.

CCR may not reinterpret PMC output.

CCR construction may not reinterpret PMC truth.

NULL PMC outcome != pipeline error.

CCR does not manufacture success.

CCR does not own Room identity.

PMC -> CCR handoff MUST NOT silently change Room Object identity.

CCR may reference state.

CCR does not own state.

CCR MUST NOT replace evidence lineage with a summary-only representation.

Coordinate reference != Cartography ownership.

CCR MUST NOT silently substitute another perspective.

CCR MUST NOT admit new evidence.

CCR MUST NOT raise claim authority.

High confidence != higher claim ceiling.

CCR commitment != certainty.

Uncertainty MUST NOT disappear merely because a CCR exists.

Commitment record != uncertainty elimination.

Rejected != deleted.

Rejected != nonexistent.

Selected != only world that ever existed.

No Compression Out applies to rejected-world lineage.

Equivalent PMC outputs and equivalent Room-bound lineage MUST produce the same
CCR identity.

No hidden defaults.

No hidden heuristic winner selection.

CANDIDATE_RECORDED != canonical promotion.

NULL_RECORDED != failure.

BLOCKED != PMC truth reversal.

CCR does not select the world.

PMC selects or denies.

CCR records.

PMC ordering remains PMC ordering.

If the source PMC state cannot be reconstructed, CCR is BLOCKED.

Receipt != truth.

Hash != truth.

MC receives CCR.

CCR is mandatory between PMC and MC in Ring 5.

R5-C does not perform MC admissibility.

Historical artifact != active native route.

CCR creates no action authority.

CCR creates no publication authority.

CCR creates no certification authority.

CCR creates no canonical promotion authority.

Authority remains NONE.

Human Gate remains ACTIVE.

Write capability != authority.

Deterministic record != authority.

CCR is not permission to flatten PMC history into the selected world alone.

Fail closed.

Do not reinterpret PMC output to repair the record.

R5-D owns CCR -> MC Response / Output Admissibility Binding.
