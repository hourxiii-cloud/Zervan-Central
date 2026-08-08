# R4-D — Reflight Trigger

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R4-D
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R4-D defines native-v41 Reflight Trigger.

Reflight means renewed analytical movement from a preserved landed state.

Reflight requires a real analytical trigger.

R4-D determines whether renewed movement is justified.

R4-D does not itself execute renewed movement.

Trigger != execution.

---

## 1. Dependency

R4-D consumes:

- complete Rings 1 through 3;
- R4-A Restriction / Constriction;
- R4-B Collapse Boundary;
- R4-C Landing Witness;
- canonical Room Object identity;
- preserved question;
- preserved representation position;
- preserved Cartography;
- preserved unresolved terrain;
- preserved readiness;
- evidence boundary;
- evidence ceiling;
- Stick continuity;
- attributable provenance.

Reflight MUST begin from preserved state.

It MUST NOT rebuild an approximate Room.

---

## 2. Governing Rule

Reflight requires a real trigger.

Native source-recognized Reflight triggers are:

- new evidence;
- contradiction;
- changed question;
- changed evidence ceiling;
- signal split;
- signal convergence;
- challenged conclusion;
- newly reachable surface;
- explicitly requested materially different rendering.

No other condition is a native valid trigger unless separately governed and
explicitly added through Human Gate-controlled evolution.

---

## 3. Native Trigger Types

R4-D defines exactly these trigger types:

- `NEW_EVIDENCE`;
- `CONTRADICTION`;
- `CHANGED_QUESTION`;
- `CHANGED_EVIDENCE_CEILING`;
- `SIGNAL_SPLIT`;
- `SIGNAL_CONVERGENCE`;
- `CHALLENGED_CONCLUSION`;
- `NEWLY_REACHABLE_SURFACE`;
- `MATERIALLY_DIFFERENT_RENDERING_REQUESTED`.

Trigger type is evidence of changed analytical condition.

Trigger type != authority.

---

## 4. Invalid Non-Triggers

The following do NOT justify Reflight by themselves:

- acknowledgment;
- repetition;
- celebration;
- affect;
- conversational continuation;
- restatement;
- curiosity without changed analytical condition;
- elapsed time alone;
- capability availability alone;
- stakeholder pressure alone.

Acknowledgment != Reflight trigger.

Repetition != Reflight trigger.

Celebration != Reflight trigger.

Affect != Reflight trigger.

Conversation continuing != Reflight trigger.

Capability availability != Reflight trigger.

---

## 5. Reflight Trigger Record

Every Reflight Trigger Record MUST preserve:

- `reflight_trigger_id`;
- canonical `object_id`;
- Landing Witness reference;
- trigger type;
- trigger subject;
- trigger evidence references;
- prior question;
- current question;
- prior evidence ceiling;
- current evidence ceiling;
- prior signal-state reference where applicable;
- current signal-state reference where applicable;
- challenged conclusion reference where applicable;
- newly reachable surface reference where applicable;
- requested rendering reference where applicable;
- material-change basis;
- evidence boundary;
- current representation reference;
- Cartography reference;
- Stick reference;
- readiness reference;
- reflight eligibility;
- blocking reasons;
- Governance reference;
- authorization reference;
- Human Gate reference where applicable;
- provenance route;
- trigger time.

---

## 6. Trigger Identity

Native-v41 `reflight_trigger_id` is deterministic SHA-512 over the complete
Reflight Trigger Record except its own ID.

A material change to:

- trigger type;
- trigger evidence;
- question;
- evidence ceiling;
- signal state;
- challenged conclusion;
- reachable surface;
- rendering request;
- material-change basis;
- eligibility

changes trigger identity.

Reflight Trigger identity is not Room Object identity.

Reflight Trigger identity is not Landing Witness identity.

---

## 7. Landing Dependency

A Reflight Trigger MUST bind a preserved Landing Witness.

The Landing Witness establishes where analytical movement stopped.

Reflight begins from that preserved state.

Reflight MUST NOT infer a landing coordinate from memory or reconstruct one
approximately.

Landing first.

Trigger second.

---

## 8. Same Room

Reflight preserves canonical Room Object identity.

Reflight does not create another Room.

Reflight does not clone the landed state into a new world.

Reflight resumes movement of the same analytical object unless an independently
established distinct-object condition routes elsewhere.

Reflight != new Room.

---

## 9. New Evidence

`NEW_EVIDENCE` requires attributable evidence that was not part of the prior
landed analytical condition.

Repeated presentation of existing evidence is not new evidence.

Reformatted existing evidence is not automatically new evidence.

New evidence must materially affect what operation is justified next.

---

## 10. Contradiction

`CONTRADICTION` requires an attributable contradiction relevant to the current
Room, question, evidence, geometry, or conclusion.

Contradiction must be preserved, not averaged away.

Contradiction may justify renewed investigation.

Contradiction != automatic conclusion reversal.

---

## 11. Changed Question

`CHANGED_QUESTION` requires a materially changed analytical question.

Rewording without material analytical change does not qualify.

Changed question may justify a new movement route.

Changed question does not create a new Room.

---

## 12. Changed Evidence Ceiling

`CHANGED_EVIDENCE_CEILING` requires an attributable change to the permitted
claim or evidence ceiling.

A changed ceiling may allow or require renewed movement.

The trigger MUST preserve both prior and current ceilings.

Changed evidence ceiling != automatic evidence promotion.

---

## 13. Signal Split

`SIGNAL_SPLIT` means a previously coherent or bounded signal now resolves into
multiple materially relevant routes or sources.

Signal split may require renewed reconnaissance, force re-justification, or
formation re-justification.

Signal split != confidence.

---

## 14. Signal Convergence

`SIGNAL_CONVERGENCE` means previously separate analytical routes become
materially reconcilable under new evidence or geometry.

Convergence may justify renewed movement to test or confirm the changed
condition.

Convergence != consensus by repetition.

Convergence != truth by vote.

---

## 15. Challenged Conclusion

`CHALLENGED_CONCLUSION` requires an attributable challenge to a prior analytical
conclusion.

Challenge alone does not erase the prior conclusion.

The prior conclusion remains part of analytical history.

Reflight may test the challenge.

Challenge != automatic reversal.

---

## 16. Newly Reachable Surface

`NEWLY_REACHABLE_SURFACE` requires a surface that was previously unavailable,
unreachable, or outside active Territory to become validly reachable under
current controls.

New reachability MUST be attributable.

Possible != reachable.

Reachable != authorized without applicable controls.

---

## 17. Materially Different Rendering

`MATERIALLY_DIFFERENT_RENDERING_REQUESTED` requires an explicit request for a
rendering that is materially different from the prior rendering.

A cosmetic restatement is insufficient.

A different format alone is insufficient unless the requested rendering
requires materially different analytical traversal.

Rendering request != automatic analysis.

---

## 18. Material Change

Every Reflight Trigger MUST preserve a non-empty `material_change_basis`.

The basis explains why the landed analytical condition is no longer sufficient
for the requested next operation.

No material change = no Reflight.

---

## 19. Reflight Eligibility

R4-D defines:

- `ELIGIBLE`;
- `BLOCKED`.

`ELIGIBLE` means a valid native trigger and sufficient attributable basis exist
to permit consideration of renewed analytical movement.

`BLOCKED` means a trigger candidate exists but current evidence, authorization,
restriction, readiness, or provenance is insufficient.

ELIGIBLE != executed.

BLOCKED != nonexistent.

---

## 20. Trigger-Specific Evidence

Every trigger requires evidence appropriate to its type.

At minimum:

- `NEW_EVIDENCE` requires non-empty trigger evidence;
- `CONTRADICTION` requires non-empty trigger evidence;
- `CHANGED_QUESTION` requires prior and current questions to differ materially;
- `CHANGED_EVIDENCE_CEILING` requires prior and current ceilings to differ;
- `SIGNAL_SPLIT` requires prior and current signal-state references;
- `SIGNAL_CONVERGENCE` requires prior and current signal-state references;
- `CHALLENGED_CONCLUSION` requires challenged conclusion reference;
- `NEWLY_REACHABLE_SURFACE` requires newly reachable surface reference;
- `MATERIALLY_DIFFERENT_RENDERING_REQUESTED` requires requested rendering
  reference.

No generic trigger placeholder may bypass these requirements.

---

## 21. Readiness

Reflight requires preserved readiness sufficient for the proposed continuation.

Landing preserves readiness.

Trigger consumes that preserved state.

If readiness is insufficient, eligibility MUST be `BLOCKED`.

Trigger does not manufacture readiness.

---

## 22. Evidence Boundary

Reflight remains inside the current evidence boundary unless Governance
explicitly changes it through a separately attributable action.

A trigger cannot silently broaden evidence access.

New evidence != unrestricted evidence access.

---

## 23. Evidence Ceiling

The Reflight Trigger preserves both prior and current evidence ceilings when
relevant.

A trigger may arise because the ceiling changed.

A trigger does not itself authorize the changed ceiling.

Evidence-ceiling change must remain attributable.

---

## 24. Cartography

Reflight begins from preserved Cartography.

The Trigger records the relevant Cartography reference.

Renewed movement may later update Cartography.

Trigger creation does not itself alter analytical geography.

Trigger != Cartography mutation.

---

## 25. Stick

Reflight MUST preserve the Stick.

The Trigger remains connected to:

- canonical object identity;
- Origin;
- Landing Witness;
- representation history;
- evidence lineage;
- provenance;
- landing coordinate;
- return route.

Reflight MUST NOT sever analytical continuity.

---

## 26. Restriction / Constriction

A Reflight Trigger does not automatically reverse Restriction or Constriction.

New evidence may later justify a new attributable narrowing or re-expansion.

Trigger != Restriction reversal.

Trigger != Constriction reversal.

---

## 27. Collapse

A Reflight Trigger does not erase prior Collapse Boundaries.

New evidence may challenge or expand beyond a prior Collapse.

Collapse history remains preserved.

Trigger != Collapse reversal.

---

## 28. Capability Mission

Reflight eligibility does not automatically reactivate a prior mission.

A new or revised Capability Mission Request may be required when the question,
scope, evidence boundary, or mission materially changes.

Trigger != Capability Mission Request.

---

## 29. Proportional Force

Reflight may require proportional-force re-justification.

The presence of a trigger does not determine force.

Need still determines force.

Trigger != force selection.

---

## 30. Formation

Reflight may require formation re-justification.

Terrain contact, contradiction, evidence-ceiling change, signal split, or signal
convergence may alter the correct formation.

Trigger does not select formation.

Trigger != Formation Selection Record.

---

## 31. Hydration

Reflight may require mission-scoped hydration.

Reflight does not authorize full-payload hydration.

Hydrate only verified operational territory required by the renewed mission.

Trigger != Hydration Request.

---

## 32. Goblin Signal

Goblin Signal may communicate an attributable Reflight Trigger.

Goblin Signal does not create Reflight eligibility.

Signal != trigger.

Notification != evidence.

Trigger first.

Notify second.

---

## 33. Authorization

A valid trigger does not create execution authority.

Reflight still requires applicable authorization.

ELIGIBLE != authorized execution.

Technical capability != authority.

Write capability != authority.

---

## 34. Human Gate

Where Human Gate applies, its state remains preserved.

Human Gate approval MUST NOT be fabricated.

Trigger eligibility does not bypass Human Gate.

Trigger != Human Gate decision.

---

## 35. Post-Convergence Control

Post-convergence conversational behavior MUST NOT cause unauthorized Reflight.

Acknowledgment, celebration, affect, repetition, or restatement preserve the
landed condition unless a real trigger appears.

Conversation can continue while analytical movement remains stopped.

No unnecessary re-analysis.

No unnecessary rebuild.

---

## 36. Reflight Execution Boundary

R4-D defines the Trigger only.

It does not define a Reflight execution record.

It does not mutate movement state.

It does not mutate lifecycle state.

It does not create Occupancy.

It does not select force.

It does not select formation.

It does not hydrate payload.

Trigger != Reflight execution.

---

## 37. Closing Witness Boundary

R4-D does not define Closing Witness.

A landed state may later close without Reflight.

A valid Reflight Trigger may prevent or interrupt closure where Governance
permits.

R4-E owns Closing Witness / Post-Convergence Closure.

---

## 38. Replay Boundary

R4-D does not define Replay.

Replay may later reopen a preserved observational coordinate.

Reflight resumes justified movement from preserved landed state.

Reflight != Replay.

Trigger != Replay Envelope.

---

## 39. Failure Conditions

R4-D MUST reject:

- trigger without Landing Witness;
- trigger without material-change basis;
- NEW_EVIDENCE without attributable evidence;
- CONTRADICTION without attributable evidence;
- CHANGED_QUESTION without actual question change;
- CHANGED_EVIDENCE_CEILING without actual ceiling change;
- SIGNAL_SPLIT without prior/current signal references;
- SIGNAL_CONVERGENCE without prior/current signal references;
- CHALLENGED_CONCLUSION without conclusion reference;
- NEWLY_REACHABLE_SURFACE without surface reference;
- MATERIALLY_DIFFERENT_RENDERING_REQUESTED without rendering reference;
- acknowledgment used as trigger;
- repetition used as trigger;
- celebration used as trigger;
- affect used as trigger;
- conversational continuation used as trigger;
- trigger used as execution authority;
- trigger used to manufacture readiness;
- trigger used to broaden evidence boundary;
- trigger used to erase Collapse history;
- trigger used to create a new Room;
- trigger used as formation selection;
- trigger used as full-payload hydration authority.

---

## 40. R4-D Lock

Reflight requires a real trigger.

New evidence is a valid trigger.

Contradiction is a valid trigger.

Changed question is a valid trigger.

Changed evidence ceiling is a valid trigger.

Signal split is a valid trigger.

Signal convergence is a valid trigger.

Challenged conclusion is a valid trigger.

Newly reachable surface is a valid trigger.

Explicitly requested materially different rendering is a valid trigger.

Acknowledgment != Reflight trigger.

Repetition != Reflight trigger.

Celebration != Reflight trigger.

Affect != Reflight trigger.

Conversation continuing != Reflight trigger.

Capability availability != Reflight trigger.

Trigger != execution.

Landing first.

Trigger second.

Reflight MUST NOT rebuild an approximate Room.

Reflight != new Room.

Repeated presentation of existing evidence is not new evidence.

Contradiction != automatic conclusion reversal.

Changed question does not create a new Room.

Changed evidence ceiling != automatic evidence promotion.

Signal split != confidence.

Convergence != consensus by repetition.

Convergence != truth by vote.

Challenge != automatic reversal.

Possible != reachable.

A different format alone is insufficient unless the requested rendering
requires materially different analytical traversal.

No material change = no Reflight.

ELIGIBLE != executed.

BLOCKED != nonexistent.

Trigger does not manufacture readiness.

A trigger cannot silently broaden evidence access.

Trigger != Cartography mutation.

Reflight MUST preserve the Stick.

Trigger != Restriction reversal.

Trigger != Constriction reversal.

Trigger != Collapse reversal.

Trigger != Capability Mission Request.

Trigger != force selection.

Trigger != Formation Selection Record.

Trigger != Hydration Request.

Signal != trigger.

Notification != evidence.

ELIGIBLE != authorized execution.

Trigger != Human Gate decision.

Conversation can continue while analytical movement remains stopped.

No unnecessary re-analysis.

No unnecessary rebuild.

Trigger != Reflight execution.

R4-E owns Closing Witness / Post-Convergence Closure.

Reflight != Replay.

Trigger != Replay Envelope.

No Closing Witness semantics yet.

No Replay semantics yet.

No Scar Replay semantics yet.
