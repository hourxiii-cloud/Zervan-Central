# R4-F — Replay Envelope

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R4-F
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R4-F defines native-v41 Replay Envelope.

Replay is not the creation of a duplicate world.

Replay is the reopening of the same Room at a preserved observational
coordinate.

Replay preserves the analytical journey across object-state and representation
changes.

Replay reopens.

Replay does not reconstruct an approximation.

---

## 1. Dependency

R4-F consumes:

- complete Rings 1 through 3;
- R4-A Restriction / Constriction;
- R4-B Collapse Boundary;
- R4-C Landing Witness;
- R4-D Reflight Trigger;
- R4-E Closing Witness;
- canonical Room Object identity;
- preserved lineage;
- preserved observational coordinates;
- representation history;
- evidence lineage;
- capability movement;
- findings;
- rendering;
- return route;
- Stick continuity.

Replay MUST begin from preserved attributable state.

---

## 2. Source Replay Invariant

Replay must preserve:

- object identity;
- question contract;
- inquiry envelope;
- departure coordinate;
- occupied Zone and Space;
- transforms applied;
- evidence used;
- capability movement;
- evidence boundary;
- restrictions;
- collapse events;
- findings;
- rendering;
- return coordinate.

No listed element may be silently substituted by a summary.

---

## 3. Same Object

Replay opens the same canonical Room Object.

Replay does not mint another `object_id`.

Replay does not create a snapshot Room.

Replay does not infer a replacement object from similar content.

Same history revisited != new world.

Replay != new Room.

---

## 4. Preserved Coordinate

Replay MUST bind an exact preserved observational coordinate.

The coordinate must be attributable to the prior analytical journey.

An approximate remembered position is insufficient.

A prose description of where analysis probably was is insufficient.

Preserved coordinate != reconstructed coordinate.

---

## 5. Replay Envelope

Every Replay Envelope MUST preserve:

- `replay_envelope_id`;
- canonical `object_id`;
- Closing Witness reference;
- preserved lineage reference;
- question contract reference;
- inquiry envelope reference;
- departure coordinate;
- replay observational coordinate;
- occupied Zone reference;
- occupied Space reference;
- transform references;
- evidence-used references;
- capability-movement references;
- evidence boundary;
- evidence ceiling;
- restriction / constriction references;
- Collapse Boundary references;
- finding references;
- rendering reference where applicable;
- return coordinate;
- Cartography reference;
- Stick reference;
- replay purpose;
- replay eligibility;
- blocking reasons;
- Governance reference;
- authorization reference;
- Human Gate reference where applicable;
- provenance route;
- envelope creation time.

---

## 6. Replay Envelope Identity

Native-v41 `replay_envelope_id` is deterministic SHA-512 over the complete
Replay Envelope except its own ID.

A material change to:

- Room identity;
- Closing Witness;
- lineage;
- question contract;
- inquiry envelope;
- observational coordinate;
- representation;
- evidence;
- capability movement;
- restrictions;
- Collapse history;
- findings;
- rendering;
- return coordinate;
- replay purpose;
- eligibility

changes Replay Envelope identity.

Replay Envelope identity is not Room Object identity.

Replay Envelope identity is not Closing Witness identity.

---

## 7. Replay Eligibility

R4-F defines:

- `ELIGIBLE`;
- `BLOCKED`.

`ELIGIBLE` means the preserved historical state is sufficiently attributable
and bounded to permit reopening consideration.

`BLOCKED` means required replay identity, coordinates, lineage, evidence,
representation, authorization, or provenance are insufficient.

ELIGIBLE != reopened.

ELIGIBLE != execution authority.

BLOCKED != nonexistent historical state.

---

## 8. Closing Witness Binding

Replay MUST bind a Closing Witness.

The Closing Witness provides preserved lineage and replay coordinates for the
closed operational interval.

Closing first.

Replay Envelope second.

Replay MUST NOT invent closure history.

---

## 9. Question Contract

Replay preserves the prior question contract.

The question contract explains what inquiry was being performed at the replayed
coordinate.

Replay does not silently replace the historical question with the current
observer's question.

Historical question != current question.

A new question may later be issued separately.

---

## 10. Inquiry Envelope

Replay preserves the historical inquiry envelope.

The inquiry envelope preserves the bounded operational context in which the
historical question was executed.

Replay MUST NOT widen the old inquiry merely because more context is available
now.

Historical scope remains historical scope.

---

## 11. Departure Coordinate

Replay preserves the original departure coordinate of the replayable inquiry.

Departure coordinate explains where the bounded analytical journey began.

Departure coordinate != Origin.

Departure coordinate != replay coordinate.

---

## 12. Zone and Space

Replay preserves the occupied Zone and Space.

These identify the bounded representation and mission surface in which the
historical observation occurred.

Replay MUST NOT substitute the current default Zone or Space.

No default substitution.

---

## 13. Transform

Replay preserves transforms applied to the Room Object.

Transform history explains how the same object was turned when the observation
was produced.

Replay MUST NOT flatten transform history.

Transform != new object.

---

## 14. Evidence Used

Replay preserves the evidence actually used in the historical inquiry.

Current evidence availability does not rewrite historical evidence use.

Evidence available now != evidence used then.

Replay fidelity requires that distinction.

---

## 15. Capability Movement

Replay preserves capability movement.

The envelope records the route through which capabilities occupied, moved,
observed, and returned.

Capability route is part of analytical history.

Replay MUST NOT replace movement history with the final finding alone.

---

## 16. Evidence Boundary

Replay preserves the historical evidence boundary.

Replay does not retroactively expose excluded material.

Excluded then != included then merely because it is available now.

Historical boundary remains attributable.

---

## 17. Evidence Ceiling

Replay preserves the evidence ceiling applicable to the historical state.

Replay does not upgrade old conclusions using a later evidence ceiling unless a
new analytical operation explicitly does so.

Replay fidelity != retrospective promotion.

---

## 18. Restriction / Constriction

Replay preserves Restriction / Constriction history.

The observer must be able to recover:

- prior supported states;
- narrowed states;
- evidence that caused narrowing;
- provenance.

Replay does not erase states because they were later removed from support.

---

## 19. Collapse Events

Replay preserves Collapse Boundaries.

The observer must be able to recover:

- collapse trigger;
- governing evidence;
- removed possibilities;
- retained possibilities;
- deferred possibilities;
- surviving uncertainty;
- newly available frontier;
- route back.

Replay does not flatten Collapse into the eventual answer.

---

## 20. Findings

Replay preserves findings attributable to the historical inquiry.

Finding != truth authority.

Finding != publication.

Replay MUST distinguish historical finding from later interpretation.

---

## 21. Rendering

Replay preserves the historical rendering where one exists.

Rendering captures how the Room state was presented at the time.

Rendering != Room Object.

Rendering != evidence.

A missing historical rendering MUST remain explicitly missing rather than being
silently regenerated and represented as original.

---

## 22. Return Coordinate

Replay preserves the return coordinate.

The return coordinate records where the historical inquiry returned after its
bounded movement.

Return coordinate preserves analytical continuity.

Return coordinate != automatic rollback authority.

---

## 23. Cartography

Replay binds preserved Cartography.

Cartography makes the historical observational coordinate navigable.

Replay MUST NOT reconstruct approximate analytical geometry when preserved
Cartography exists.

Replay fidelity requires geometry fidelity.

---

## 24. Stick

Replay MUST preserve the Stick.

The reopened historical coordinate remains connected to:

- canonical Room identity;
- Origin;
- lineage;
- question;
- representation;
- transform history;
- evidence;
- movement;
- findings;
- return route.

Replay MUST NOT sever analytical continuity.

---

## 25. Prior Movement and Effects

Replay / Scar Replay reopen historical observational coordinates of the same
object and preserve prior movement, questions, transforms, evidence, and
effects.

R4-F implements base Replay preservation of prior movement, questions,
transforms, evidence, and recorded analytical effects.

Scar-specific effect semantics remain R4-G / R4-H.

---

## 26. Replay Purpose

Every Replay Envelope declares a bounded replay purpose.

Examples include:

- audit reconstruction;
- analytical challenge;
- historical comparison;
- continuation preparation;
- validation;
- explanation of prior movement.

Replay purpose does not change the historical state.

Purpose != evidence.

---

## 27. Authorization

Replay capability does not create authority.

Historical visibility remains bounded by applicable authorization.

Technical ability to reopen a coordinate != permission to expose its content.

ELIGIBLE != authorized execution.

---

## 28. Human Gate

Where Human Gate applies, its reference remains preserved.

Replay does not fabricate Human Gate approval.

Replay does not promote candidate state.

Replay Envelope != Human Gate decision.

---

## 29. Lifecycle

The source recognizes REOPENED as a sealed Room reopened at a preserved state
because a valid Reflight Trigger exists.

R4-F defines Replay Envelope, not Registry lifecycle mutation.

Replay Envelope creation does not itself transition SEALED -> REOPENED.

Replay Envelope != lifecycle transition.

---

## 30. Reflight

Replay and Reflight are related but distinct.

Reflight requires a real trigger for renewed analytical movement.

Replay reopens a preserved observational coordinate.

Replay may support challenge, validation, or later continuation without itself
executing Reflight.

Replay != Reflight Trigger.

Replay != Reflight execution.

---

## 31. Hydration

Replay does not justify full reconstruction or full hydration.

Only mission-required verified territory may be hydrated for an authorized
Replay operation.

Reflight does not justify full reconstruction.

Replay does not justify full reconstruction.

Payload rests.

---

## 32. No Approximate Reconstruction

Replay MUST reject substitution of:

- remembered prose;
- current defaults;
- reconstructed coordinates;
- guessed transforms;
- inferred evidence history;
- synthetic capability routes;
- regenerated historical renderings represented as original.

If preserved state is insufficient, Replay is BLOCKED.

Fail closed.

Do not fabricate history.

---

## 33. No New World

Replay is not creation of a duplicate world.

Replay reopens the same Room.

A replayed historical state is not another canonical object.

Historical coordinate != alternate reality.

Observation history accumulates on one object.

---

## 34. Branch Boundary

Replay does not itself create a branch.

A later authorized analytical continuation may branch while preserving
same-object lineage.

Replay Envelope != Branch.

Branching remains governed by existing Ring 1 / Ring 2 controls.

---

## 35. Scar Boundary

R4-F does not define Scar.

A Scar is evidence that Terrain has previously affected movement.

R4-G owns Scar Record.

R4-H owns Scar Replay.

Base Replay MUST NOT silently invent Scar semantics.

---

## 36. Publication Boundary

Replay does not publish.

Replay does not alter:

Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate

Historical finding != current publication authorization.

Replay Envelope != publication record.

---

## 37. Failure Conditions

R4-F MUST reject:

- Replay without canonical Room identity;
- Replay without Closing Witness;
- Replay without preserved lineage;
- Replay without exact observational coordinate;
- Replay without question contract;
- Replay without inquiry envelope;
- Replay that substitutes current Zone or Space for historical position;
- Replay that loses transform history;
- Replay that loses evidence-used history;
- Replay that loses capability movement;
- Replay that loses evidence boundary;
- Replay that loses Restriction / Constriction history;
- Replay that loses Collapse history;
- Replay that loses findings;
- Replay that loses return coordinate;
- Replay that reconstructs approximation instead of reopening preserved state;
- Replay that creates a new Room;
- Replay that silently raises historical evidence ceiling;
- Replay that treats regenerated rendering as historical original;
- Replay Envelope used as lifecycle mutation;
- Replay Envelope used as Reflight execution;
- Replay used as full-payload hydration authority;
- Scar semantics pulled forward.

---

## 38. R4-F Lock

Replay is not the creation of a duplicate world.

Replay is the reopening of the same Room at a preserved observational
coordinate.

Replay preserves analytical journeys across object state and representation
changes.

Replay reopens.

Replay does not reconstruct an approximation.

No listed element may be silently substituted by a summary.

Same history revisited != new world.

Replay != new Room.

Preserved coordinate != reconstructed coordinate.

ELIGIBLE != reopened.

ELIGIBLE != execution authority.

BLOCKED != nonexistent historical state.

Closing first.

Replay Envelope second.

Replay MUST NOT invent closure history.

Historical question != current question.

Historical scope remains historical scope.

Departure coordinate != Origin.

Departure coordinate != replay coordinate.

No default substitution.

Transform != new object.

Evidence available now != evidence used then.

Capability route is part of analytical history.

Historical boundary remains attributable.

Replay fidelity != retrospective promotion.

Replay does not flatten Collapse into the eventual answer.

Finding != truth authority.

Rendering != Room Object.

Rendering != evidence.

Return coordinate != automatic rollback authority.

Replay fidelity requires geometry fidelity.

Replay MUST preserve the Stick.

Replay MUST NOT sever analytical continuity.

Purpose != evidence.

Technical ability to reopen a coordinate != permission to expose its content.

Replay Envelope != Human Gate decision.

Replay Envelope creation does not itself transition SEALED -> REOPENED.

Replay Envelope != lifecycle transition.

Replay != Reflight Trigger.

Replay != Reflight execution.

Reflight does not justify full reconstruction.

Replay does not justify full reconstruction.

Payload rests.

Fail closed.

Do not fabricate history.

Historical coordinate != alternate reality.

Observation history accumulates on one object.

Replay Envelope != Branch.

R4-G owns Scar Record.

R4-H owns Scar Replay.

Replay Envelope != publication record.

No Scar Record semantics yet.

No Scar Replay semantics yet.
