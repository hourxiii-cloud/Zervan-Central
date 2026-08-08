# R4-G — Scar Record

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R4-G
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R4-G defines native-v41 Scar Record.

A Scar is evidence that Terrain has previously affected movement.

A Scar records attributable historical contact between Terrain and analytical
movement.

Scar != warning label.

Scar != confidence score.

Scar != conclusion.

Scar != new Room.

---

## 1. Source Boundary

The source requires a machine-readable Scar Record.

The source defines Scar semantically but does not prescribe the complete
machine-state field vocabulary.

The field structure below is native implementation structure constrained by
source invariants.

Implementation structure != new doctrine.

---

## 2. Dependency

R4-G consumes:

- complete Rings 1 through 3;
- R4-A Restriction / Constriction;
- R4-B Collapse Boundary;
- R4-C Landing Witness;
- R4-D Reflight Trigger;
- R4-E Closing Witness;
- R4-F Replay Envelope;
- canonical Room Object identity;
- Terrain;
- historical analytical movement;
- preserved coordinates;
- representation history;
- evidence lineage;
- Cartography;
- Stick continuity;
- provenance.

R4-G does not redefine those substrates.

---

## 3. Governing Definition

A Scar is evidence that Terrain has previously affected movement.

Therefore a valid Scar MUST establish all three:

1. identifiable Terrain;
2. identifiable prior movement;
3. attributable evidence that the Terrain affected that movement.

Terrain alone is not a Scar.

Movement alone is not a Scar.

Evidence alone is not a Scar.

The relationship is the Scar.

---

## 4. Scar Record

Every Scar Record MUST preserve:

- `scar_record_id`;
- canonical `object_id`;
- Terrain reference;
- affected movement references;
- effect evidence references;
- effect description;
- observational coordinate;
- question contract reference where applicable;
- inquiry envelope reference where applicable;
- occupied Zone reference;
- occupied Space reference;
- transform references;
- capability-route references;
- Restriction / Constriction references;
- Collapse Boundary references;
- finding references;
- evidence boundary;
- evidence ceiling;
- Cartography reference;
- Stick reference;
- replay-envelope reference where applicable;
- effect persistence;
- unresolved implications;
- provenance route;
- Governance reference;
- authorization reference;
- Human Gate reference where applicable;
- recording time.

---

## 5. Scar Identity

Native-v41 `scar_record_id` is deterministic SHA-512 over the complete Scar
Record except its own ID.

A material change to:

- Room identity;
- Terrain;
- affected movement;
- effect evidence;
- effect description;
- observational coordinate;
- representation;
- capability route;
- restrictions;
- Collapse history;
- evidence boundary;
- unresolved implications

changes Scar Record identity.

Scar Record identity is not Room Object identity.

Scar Record identity is not Terrain identity.

Scar Record identity is not Replay Envelope identity.

---

## 6. Same Room Identity

Scar remains attached to the canonical Room Object in which the Terrain affected
movement.

Recording a Scar does not create a new Room.

Historical difficulty != distinct object.

Prior disturbance != distinct object.

Scar != branch.

---

## 7. Terrain

Every Scar MUST reference identifiable Terrain.

Terrain means encountered informational reality within the Room.

The Scar does not replace the Terrain.

The Scar records evidence about prior interaction with that Terrain.

Scar != Terrain.

---

## 8. Movement

Every Scar MUST reference one or more attributable prior movement records.

Movement may include:

- capability route;
- bounded traversal;
- representation movement;
- analytical approach;
- return movement;
- interrupted or redirected movement.

A Scar cannot be created from hypothetical movement.

Prior movement MUST be attributable.

---

## 9. Effect Evidence

Every Scar MUST contain non-empty effect evidence.

The evidence must support the claim that the referenced Terrain affected the
referenced movement.

Effect evidence may preserve:

- contradiction;
- blockage;
- route change;
- delayed movement;
- forced restriction;
- constriction;
- Collapse;
- unresolved split;
- redirected capability movement;
- altered analytical geometry.

The evidence determines what may be claimed.

Scar existence does not raise the evidence ceiling.

---

## 10. Effect Description

Every Scar records a bounded description of the observed effect.

The description MUST remain inside the evidence boundary.

Effect description != attribution beyond evidence.

Effect description != causal certainty unless evidence supports causal
certainty.

Observed effect may be preserved without overclaim.

---

## 11. Historical Coordinate

Every Scar preserves the observational coordinate at which the effect is
attributable.

Scar coordinate permits future navigation back to the relevant geometry.

Scar coordinate != new Origin.

Scar coordinate != reconstructed approximation.

---

## 12. Representation

Scar preserves the representation context in which the Terrain affected
movement.

Zone, Space, and transforms remain attributable.

A Scar seen under one representation does not automatically become universal
under every representation.

Representation != truth authority.

---

## 13. Capability Route

Scar preserves the capability route involved in the affected movement.

The system must be able to determine:

- who or what moved;
- through which bounded route;
- where movement changed;
- what evidence recorded the effect.

Scar MUST NOT reduce movement history to only a final finding.

---

## 14. Restriction / Constriction

A Scar may reference prior Restriction or Constriction when Terrain contact
caused or contributed to narrowing supported states.

Scar does not itself perform Restriction.

Scar does not itself perform Constriction.

Scar != Restriction.

Scar != Constriction.

---

## 15. Collapse

A Scar may reference prior Collapse Boundary when Terrain contact contributed to
an evidence-driven Collapse.

Scar does not itself perform Collapse.

Scar does not erase Collapse history.

Scar != Collapse.

---

## 16. Findings

Scar may preserve finding references associated with the historical movement.

A finding is not required to establish that movement was affected when the
effect evidence itself is sufficient.

Finding != Scar.

Scar != final answer.

---

## 17. Evidence Boundary

Scar preserves the historical evidence boundary.

Scar recording cannot retroactively broaden that boundary.

Evidence outside the historical boundary remains outside the historical
observation unless separately admitted through a new operation.

Scar != evidence-boundary expansion.

---

## 18. Evidence Ceiling

Scar preserves the evidence ceiling applicable to the recorded effect.

The existence of a Scar does not raise claim authority.

Scar != confidence promotion.

Scar != certainty.

Scar != truth certification.

---

## 19. Cartography

Scar is preserved in Cartography as historical Terrain that affected movement.

Scar contributes navigable historical geometry.

Scar does not overwrite current Terrain.

Scar does not freeze Cartography permanently.

Historical effect remains attributable even if later evidence changes current
understanding.

---

## 20. Stick

Scar MUST preserve the Stick.

The Scar remains connected to:

- canonical Room identity;
- Origin;
- Terrain;
- representation history;
- movement history;
- evidence lineage;
- observational coordinate;
- return route;
- provenance.

Scar MUST NOT sever analytical continuity.

---

## 21. Replay Relationship

A Scar may be recorded independently of an active Replay operation.

When a Replay Envelope exists for the relevant journey, the Scar may reference
it.

Replay Envelope reference is therefore optional in R4-G.

Replay may expose a Scar.

Replay does not manufacture a Scar.

Scar requires evidence that Terrain previously affected movement.

---

## 22. Effect Persistence

R4-G records whether the historical effect is currently understood as:

- still materially relevant;
- historically relevant but currently inactive;
- unresolved.

The native machine values are:

- `ACTIVE`;
- `HISTORICAL`;
- `UNRESOLVED`.

Effect persistence describes current relationship to the historical Scar.

Persistence != truth authority.

Persistence != lifecycle state.

---

## 23. Unresolved Implications

Scar may preserve unresolved implications.

An unresolved implication remains explicitly unresolved.

Scar recording MUST NOT force unresolved implications into conclusions.

Unknown remains unknown.

---

## 24. Scar Is Evidence-Bearing

Scar is not merely metadata.

Scar MUST have attributable effect evidence.

A label such as:

- difficult;
- suspicious;
- weird;
- risky;
- important

without movement-effect evidence is not a Scar.

Narrative concern != Scar.

---

## 25. Scar Is Historical

Scar states that Terrain previously affected movement.

Scar does not by itself assert that the same effect will recur.

Past effect != guaranteed future effect.

Scar may inform future navigation without predetermining it.

---

## 26. No Confidence Substitution

Scar MUST NOT be represented as a probability or confidence score.

A repeating uncertainty pattern may contribute evidence to a Scar where it
actually affected movement, but the Scar is the historical evidence-bearing
movement effect, not the numeric pattern itself.

Signal != Scar.

Score != Scar.

Confidence != Scar.

---

## 27. No Silent Generalization

A Scar is bounded to the evidence-bearing historical contact that established
it.

Scar MUST NOT silently generalize from:

- one capability to all capabilities;
- one Zone to all Zones;
- one Space to all Spaces;
- one transform to all transforms;
- one question to all questions;
- one historical interval to all future intervals.

Generalization requires evidence.

---

## 28. Governance

Governance constraints remain active.

Scar recording does not create:

- decision authority;
- publication authority;
- execution authority;
- canonical promotion authority.

Scar is evidence-bearing state, not governing authority.

---

## 29. Human Gate

Where Human Gate applies, its state remains attributable.

Scar recording does not fabricate approval.

Scar recording does not bypass Human Gate.

Scar != Human Gate decision.

---

## 30. Lifecycle

Scar Record creation does not itself mutate Room lifecycle state.

Scar may be present in:

- ACTIVE;
- LANDED;
- DEGRADED;
- SEALED;
- REOPENED

operational history where otherwise valid.

Scar != lifecycle transition.

---

## 31. Reflight

A Scar may later contribute evidence relevant to a valid Reflight Trigger.

Scar existence alone does not automatically authorize Reflight.

Historical effect != current Reflight trigger.

R4-D remains authoritative for Reflight Trigger.

---

## 32. Scar Replay Boundary

R4-G records Scar.

R4-G does not define Scar Replay behavior.

Scar Replay may later allow a future observer to:

- replay;
- summarize;
- continue;
- branch;
- challenge;
- ignore with evidence

without creating a new world merely to revisit the old one.

R4-H owns Scar Replay.

---

## 33. Publication Boundary

Scar recording does not publish.

Scar does not alter:

Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate

Scar Record != publication record.

Scar evidence may later enter publication lineage through the existing
evidence-to-publication sequence.

---

## 34. Failure Conditions

R4-G MUST reject:

- Scar without canonical Room identity;
- Scar without Terrain reference;
- Scar without prior movement;
- Scar without effect evidence;
- Scar without bounded effect description;
- Scar without observational coordinate;
- Scar that invents movement;
- Scar that invents Terrain;
- Scar that raises evidence ceiling;
- Scar represented only as a confidence score;
- Scar represented only as a warning label;
- Scar that silently generalizes across representations;
- Scar that creates a new Room;
- Scar that overwrites Cartography;
- Scar that severs Stick continuity;
- Scar treated as Reflight authorization;
- Scar treated as lifecycle mutation;
- Scar treated as publication;
- Scar Replay semantics pulled forward.

---

## 35. R4-G Lock

A Scar is evidence that Terrain has previously affected movement.

Terrain alone is not a Scar.

Movement alone is not a Scar.

Evidence alone is not a Scar.

The relationship is the Scar.

Scar != warning label.

Scar != confidence score.

Scar != conclusion.

Scar != new Room.

Implementation structure != new doctrine.

Scar Record identity is not Room Object identity.

Scar Record identity is not Terrain identity.

Scar Record identity is not Replay Envelope identity.

Historical difficulty != distinct object.

Prior disturbance != distinct object.

Scar != branch.

Scar != Terrain.

A Scar cannot be created from hypothetical movement.

Prior movement MUST be attributable.

Every Scar MUST contain non-empty effect evidence.

The evidence determines what may be claimed.

Scar existence does not raise the evidence ceiling.

Effect description != attribution beyond evidence.

Scar coordinate != new Origin.

Scar coordinate != reconstructed approximation.

Representation != truth authority.

Scar MUST NOT reduce movement history to only a final finding.

Scar != Restriction.

Scar != Constriction.

Scar != Collapse.

Finding != Scar.

Scar != final answer.

Scar != evidence-boundary expansion.

Scar != confidence promotion.

Scar != certainty.

Scar != truth certification.

Historical effect remains attributable even if later evidence changes current
understanding.

Scar MUST preserve the Stick.

Scar MUST NOT sever analytical continuity.

Replay may expose a Scar.

Replay does not manufacture a Scar.

Persistence != truth authority.

Persistence != lifecycle state.

Unknown remains unknown.

Scar is not merely metadata.

Narrative concern != Scar.

Past effect != guaranteed future effect.

Signal != Scar.

Score != Scar.

Confidence != Scar.

Generalization requires evidence.

Scar is evidence-bearing state, not governing authority.

Scar != Human Gate decision.

Scar != lifecycle transition.

Scar existence alone does not automatically authorize Reflight.

Historical effect != current Reflight trigger.

R4-H owns Scar Replay.

Scar Record != publication record.

No Scar Replay execution semantics yet.
