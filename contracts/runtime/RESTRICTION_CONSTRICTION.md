# R4-A — Restriction / Constriction Record

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R4-A
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R4-A defines native-v41 Restriction and Constriction as Runtime State
operations on the supported states of one Room Object.

R4-A consumes:

- complete Rings 1 through 3;
- canonical Room Object identity;
- active question / perspective / mission context;
- current representation;
- current evidence boundary;
- current evidence ceiling;
- attributable evidence;
- provenance;
- Stick continuity.

R4-A does not define Collapse.

---

## 1. Source Sequence

The source analytical sequence is:

One Room Object

-> Multiple Evidence-Compatible States

-> Question / Perspective / Mission

-> Evidence

-> Restriction

-> Fewer Supported States

-> Further Evidence

-> Constriction

-> Most Correct Supported State

This sequence is preserved.

---

## 2. Governing Principle

Analytical systems become more correct by responsibly restricting the set of
evidence-compatible states of one object while preserving:

- provenance;
- representation history;
- continuity.

Every valid analytical operation shall reduce uncertainty without reducing
provenance.

Restriction is not deletion.

Perspective is not authority.

---

## 3. One Object

Restriction and Constriction operate on one canonical Room Object.

They do not create another Room.

They do not replace object identity.

They do not replace Origin.

They do not clone reality.

Supported-state change != object-identity change.

---

## 4. Native Operation Types

R4-A defines two operation types:

- `RESTRICTION`;
- `CONSTRICTION`.

`RESTRICTION` reduces a broader evidence-compatible state set to fewer supported
states using attributable evidence.

`CONSTRICTION` applies further attributable evidence to an already restricted
or otherwise prior supported-state condition and produces a more tightly
supported state set.

Operation type != lifecycle state.

---

## 5. Restriction

Restriction records that current evidence can no longer support every prior
evidence-compatible state.

Restriction MUST preserve:

- the pre-operation supported-state set;
- evidence used;
- states retained;
- states removed from current support;
- unresolved states where applicable;
- representation context;
- provenance;
- route back to the prior supported-state condition.

Removed from current support != deleted.

Removed from current support != impossible forever.

---

## 6. Constriction

Constriction records additional narrowing after further evidence.

Constriction MUST preserve:

- the prior operation or prior supported-state reference;
- further evidence;
- the pre-constriction supported-state set;
- the post-constriction supported-state set;
- states removed from current support;
- remaining uncertainty;
- provenance;
- continuity.

Constriction aims toward the most correct supported state available under the
current evidence.

Most correct supported != absolute truth.

Most correct supported != decision authority.

---

## 7. Restriction / Constriction Record

Every record MUST preserve:

- `restriction_constriction_id`;
- canonical `object_id`;
- `operation_type`;
- active question;
- mission reference;
- representation reference;
- prior operation reference where applicable;
- evidence references;
- further evidence references where applicable;
- pre-supported states;
- post-supported states;
- removed-from-support states;
- unresolved states;
- operation basis;
- evidence boundary;
- evidence ceiling;
- provenance anchors;
- representation-history references;
- Cartography reference;
- Stick reference;
- return-state reference;
- Governance reference;
- authorization reference;
- Human Gate reference where applicable;
- provenance route;
- operation time.

---

## 8. Record Identity

Native-v41 `restriction_constriction_id` is deterministic SHA-512 over the
complete record except the ID itself.

A material change to:

- operation type;
- question;
- evidence;
- supported-state sets;
- representation;
- evidence boundary;
- evidence ceiling;
- operation basis

changes record identity.

Record identity != Room Object identity.

Record identity != State Root.

---

## 9. State-Set Reduction

Post-operation supported states MUST be a subset of pre-operation supported
states.

R4-A MUST NOT manufacture a newly supported state during Restriction or
Constriction.

Newly supported state requires separately attributable evidence/state handling.

Restriction / Constriction narrows current support.

It does not invent a new possibility merely to preserve symmetry.

---

## 10. Removed-State Integrity

A state listed as removed from current support MUST have existed in the
pre-operation supported set.

A state retained after the operation MUST remain in the pre-operation set.

A state MUST NOT be simultaneously:

- post-supported; and
- removed from support.

State bookkeeping MUST remain reconstructible.

---

## 11. No Deletion

Restriction is not deletion.

Constriction is not deletion.

A state removed from current support remains historically attributable.

Its prior support, evidence context, representation, and removal basis remain
reconstructible.

Historical support != current support.

---

## 12. Evidence

Restriction requires attributable evidence.

Constriction requires further attributable evidence.

Evidence drives narrowing.

Preference does not.

Perspective does not.

Convenience does not.

Narrative neatness does not.

---

## 13. Further Evidence

`CONSTRICTION` MUST preserve non-empty `further_evidence_references`.

Constriction without further evidence is prohibited.

Repeated assertion != further evidence.

Repeated notification != further evidence.

Agreement != further evidence.

---

## 14. Question / Perspective / Mission

Question, perspective, and mission establish analytical context.

They may determine what evidence is relevant to the bounded operation.

They do not own truth.

They do not independently remove supported states.

Perspective is not authority.

Mission is not evidence.

Question is not evidence.

---

## 15. Evidence Boundary

Restriction / Constriction MUST remain inside the applicable evidence boundary.

Excluded evidence MUST NOT silently become included.

Restricted evidence MUST NOT silently become available.

Evidence outside the boundary cannot be used merely because it would simplify
the state set.

Excluded != absent.

Restricted != nonexistent.

---

## 16. Evidence Ceiling

Restriction / Constriction MUST preserve the applicable evidence ceiling.

Narrower state count does not raise claim authority.

One remaining supported state does not automatically prove certainty beyond the
evidence ceiling.

State-count reduction != confidence promotion.

State-count reduction != publication authority.

---

## 17. Provenance

Every state reduction preserves provenance.

The record MUST retain attributable evidence and provenance anchors explaining
why each reduction occurred.

Every valid analytical operation shall reduce uncertainty without reducing
provenance.

No provenance loss for analytical convenience.

---

## 18. Representation History

Restriction / Constriction preserves representation history.

The record retains which Zone, Space, perspective, transform, or representation
exposed the relevant evidence.

Representation may affect what becomes visible.

Representation does not create truth authority.

---

## 19. Cartography

Cartography may preserve:

- supported-state geometry;
- uncertainty frontiers;
- evidence boundaries;
- deformation;
- the effect of Restriction / Constriction.

Restriction / Constriction does not replace Cartography.

State reduction != Cartographic deletion.

---

## 20. Stick

Restriction / Constriction MUST preserve the Stick.

The operation remains connected to:

- canonical object identity;
- Origin;
- representation history;
- provenance;
- evidence lineage;
- return route.

Reduction MUST NOT sever analytical continuity.

---

## 21. Return State

Every operation preserves a `return_state_reference`.

This is the attributable route to the pre-operation supported-state condition.

Return-state preservation does not automatically authorize rollback.

Reconstructibility != mutation authority.

---

## 22. Governance

Governance preserves:

- evidence obligations;
- claim ceilings;
- prohibited assumptions;
- Human Gate requirements;
- operation constraints.

Restriction / Constriction MUST remain inside Governance constraints.

Evidence narrowing cannot override policy.

---

## 23. Authorization

Analytical ability to narrow a state set does not create mutation authority.

Applicable authorization remains separately attributable.

Technical capability != authority.

Write capability != authority.

Operation record != authorization.

---

## 24. Human Gate

Where Human Gate applies, its reference remains preserved.

Human Gate approval MUST NOT be fabricated.

Human Gate decision != analytical evidence.

Human Gate decision != execution authority.

---

## 25. Lifecycle Separation

Restriction / Constriction does not itself mutate Room lifecycle state.

Runtime-state operation != lifecycle transition.

Restriction != QUALIFIED.

Restriction != READY.

Constriction != ACTIVE.

Constriction != SEALED.

---

## 26. Occupancy Separation

Restriction / Constriction does not establish or terminate occupancy.

Evidence may be produced by occupants.

Operation record != Occupancy Witness.

State narrowing != presence.

---

## 27. Formation Separation

Restriction / Constriction does not select formation.

A changed supported-state set may later justify formation re-evaluation.

Restriction != Formation Selection.

Constriction != Formation Selection.

---

## 28. Hydration Separation

Hydration changes active payload availability.

Restriction / Constriction changes the currently supported analytical state set.

Hydration != Restriction.

Hydration != Constriction.

More hydrated payload does not itself justify state narrowing.

Evidence does.

---

## 29. Goblin Signal Separation

Goblin Signal may communicate an attributable Restriction / Constriction event.

Goblin Signal does not perform the narrowing.

Signal != Restriction.

Signal != Constriction.

Notification != evidence.

---

## 30. Collapse Boundary

R4-A does not define Collapse.

Restriction / Constriction may reduce supported states without invoking
Collapse.

Collapse is a separate evidence-driven signal and refinement event.

Restriction != Collapse.

Constriction != Collapse.

R4-B owns Collapse Boundary.

---

## 31. No Compression-Out Substitution

Restriction / Constriction MUST NOT be implemented as:

- summary compression;
- deletion;
- lossy simplification;
- confidence-only scoring;
- replacement of the Room with a conclusion.

Reducing the supported-state set is not permission to erase the analytical
journey.

Narrowing != compression out.

---

## 32. Failure Conditions

R4-A MUST reject:

- post-supported states not present in the pre-supported set;
- removed states that were never previously supported;
- a state simultaneously retained and removed;
- Restriction without evidence;
- Constriction without further evidence;
- provenance loss;
- representation-history loss;
- object-identity substitution;
- state narrowing based solely on perspective or preference;
- evidence-boundary broadening;
- evidence-ceiling promotion caused only by narrowing;
- silent lifecycle mutation;
- silent occupancy mutation;
- silent formation selection;
- Collapse semantics pulled forward.

---

## 33. R4-A Lock

One Room Object.

Multiple Evidence-Compatible States.

Evidence.

Restriction.

Fewer Supported States.

Further Evidence.

Constriction.

Most Correct Supported State.

Every valid analytical operation shall reduce uncertainty without reducing
provenance.

Restriction is not deletion.

Perspective is not authority.

Supported-state change != object-identity change.

Operation type != lifecycle state.

Removed from current support != deleted.

Removed from current support != impossible forever.

Most correct supported != absolute truth.

Most correct supported != decision authority.

Post-operation supported states MUST be a subset of pre-operation supported
states.

Restriction / Constriction narrows current support.

Historical support != current support.

Evidence drives narrowing.

Preference does not.

Perspective does not.

Convenience does not.

Narrative neatness does not.

Constriction without further evidence is prohibited.

Repeated assertion != further evidence.

Agreement != further evidence.

Mission is not evidence.

Question is not evidence.

Excluded != absent.

Restricted != nonexistent.

Narrower state count does not raise claim authority.

State-count reduction != confidence promotion.

State-count reduction != publication authority.

No provenance loss for analytical convenience.

Representation does not create truth authority.

State reduction != Cartographic deletion.

Reduction MUST NOT sever analytical continuity.

Reconstructibility != mutation authority.

Evidence narrowing cannot override policy.

Technical capability != authority.

Write capability != authority.

Runtime-state operation != lifecycle transition.

State narrowing != presence.

Restriction != Formation Selection.

Constriction != Formation Selection.

Hydration != Restriction.

Hydration != Constriction.

Notification != evidence.

Restriction != Collapse.

Constriction != Collapse.

R4-B owns Collapse Boundary.

Narrowing != compression out.

No Collapse semantics yet.

No Landing semantics yet.

No Reflight semantics yet.

No Closing Witness semantics yet.

No Replay semantics yet.

No Scar Replay semantics yet.
