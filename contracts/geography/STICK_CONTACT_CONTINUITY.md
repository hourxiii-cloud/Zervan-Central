# R2-I — Stick / Contact Continuity

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R2-I
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R2-I defines Stick / Contact Continuity for one Canonical Room Object.

Stick preserves analytical continuity across:

- movement;
- perspective shift;
- Representation Transform;
- Bounded Space operation;
- observation;
- restriction;
- coordinate change.

R2-I consumes complete Ring 1 and R2-A through R2-H.

R2-I does not redefine those inner contracts.

R2-I does not yet define:

- Passageway semantics;
- Occupation semantics;
- capability movement execution.

---

## 1. Stick

Movement and representation change shall never require loss of analytical
continuity.

The preserved relationship between movement, perspective shift, Space
operation, and the originating Room Object is the Stick.

Stick preserves contact with the same analytical object.

---

## 2. Contact Continuity

Contact Continuity means every meaningful analytical change remains resolvably
bound to the object and its established lineage.

Continuity does not require representation immobility.

Continuity does require preserved contact.

Freedom of movement requires continuity of contact.

Freedom of perspective requires continuity of object identity.

---

## 3. Stick Record

Every Stick Continuity Record MUST preserve:

- `stick_id`;
- canonical `object_id`;
- origin identity/reference;
- ingress envelope reference;
- Cartography reference;
- source orientation reference;
- target orientation reference;
- transform reference when applicable;
- Space reference when applicable;
- evidence-lineage references;
- provenance route;
- observation/restriction references;
- source coordinates;
- target coordinates;
- return coordinates;
- continuity state;
- continuity reason;
- recorded time.

---

## 4. Stick Identity

Native-v41 `stick_id` is deterministic SHA-512 over the complete declared
continuity record except `stick_id`.

The Stick identity identifies one continuity binding.

Stick identity is not object identity.

Stick != Room Object.

---

## 5. Object Identity

Every Stick MUST preserve the canonical `object_id`.

Movement MUST NOT replace object identity.

Perspective change MUST NOT replace object identity.

Space operation MUST NOT replace object identity.

Transform execution MUST NOT replace object identity.

Continuity fails closed if the record cannot resolve the same object.

---

## 6. Origin Identity

Every Stick MUST preserve a resolvable Origin identity or Origin reference.

Distance from ingress does not erase Origin.

Representation complexity does not erase Origin.

Origin continuity MUST remain reconstructible.

---

## 7. Ingress Envelope

Every Stick MUST preserve the Ingress Envelope reference associated with the
originating admitted world.

Ingress establishes the admission boundary.

Later movement does not silently rewrite ingress.

---

## 8. Cartography

Every Stick MUST preserve the relevant Cartography reference.

Cartography explains the navigable geometry.

Stick explains continuity of contact across that geometry.

Cartography != Stick.

Map != continuity contract.

---

## 9. Orientation Continuity

A Stick MUST preserve source and target Orientation references.

The continuity record explains how analytical position changed without losing
contact with the same object.

Orientation change != contact loss.

---

## 10. Transform Continuity

When movement includes Representation Transform, Stick MUST preserve the
transform reference.

The transform explains what shifted.

Stick explains that contact survived the shift.

Transform != Stick.

---

## 11. Space Continuity

When movement or observation occurs through a Bounded Space, Stick MUST
preserve the Space reference.

Space defines the bounded mission surface.

Stick binds that mission activity back to the same Room Object.

Mission change != identity fracture.

---

## 12. Evidence Lineage

Every Stick MUST preserve evidence-lineage references relevant to the movement,
observation, or restriction.

Evidence may become:

- included;
- excluded;
- restricted;
- unavailable;
- unresolved.

Its lineage MUST NOT disappear merely because representation changes.

Evidence visibility change != evidence-history deletion.

---

## 13. Provenance

Every Stick MUST preserve a traversable provenance route.

A continuity record MUST NOT invent provenance merely to appear complete.

Unresolved provenance remains unresolved.

Continuity != fabricated certainty.

---

## 14. Observation Binding

Every meaningful observation occurring during movement or representation change
MUST remain attributable through Stick.

Observation MUST resolve to:

- the same `object_id`;
- relevant representation;
- relevant evidence lineage;
- relevant coordinates;
- provenance.

Observation changes history.

Observation does not silently sever continuity.

---

## 15. Restriction Binding

Every meaningful restriction encountered during movement or representation
change MUST remain attributable through Stick.

Restriction MUST NOT silently become absence.

Restriction MUST NOT disappear simply because a later representation cannot
display the restricted content.

Restriction continuity is part of analytical continuity.

---

## 16. Coordinates

Stick preserves:

- source coordinates;
- target coordinates;
- return coordinates.

Coordinates describe movement.

Stick binds the movement.

Coordinate change != continuity loss.

---

## 17. Return Coordinates

Return coordinates MUST remain resolvable after movement or perspective shift.

The system MUST preserve enough information to explain how to resolve back
toward a known prior analytical position.

Return route continuity MUST NOT be discarded for convenience.

---

## 18. Continuity State

R2-I defines three continuity states:

- `CONTINUOUS`;
- `DEGRADED`;
- `BROKEN`.

CONTINUOUS means required continuity bindings remain resolvable.

DEGRADED means contact remains identifiable but one or more continuity elements
are incomplete, restricted, stale, or unresolved.

BROKEN means the system cannot establish required continuity to the originating
Room Object.

BROKEN MUST fail closed for movement that requires preserved continuity.

---

## 19. Degraded Continuity

DEGRADED continuity MUST preserve exactly what is degraded.

The record MUST identify:

- missing reference;
- restricted evidence;
- unresolved provenance;
- stale Cartography;
- unresolved return coordinate;
- other explicit continuity defect.

DEGRADED MUST NOT silently become CONTINUOUS.

---

## 20. Broken Continuity

BROKEN means required object/contact continuity cannot be established.

The system MUST NOT invent:

- object identity;
- Origin;
- ingress;
- Cartography;
- transform history;
- evidence lineage;
- return coordinates

to force continuity.

Broken contact is evidence.

---

## 21. Movement Boundary

R2-I defines the condition required for movement continuity.

It does not define movement execution.

Capability Movement remains downstream.

Stick permits continuity validation.

Stick does not itself move anything.

---

## 22. Perspective Freedom

Perspective may change freely only while required invariants remain bound.

Freedom of perspective requires continuity of object identity.

Perspective freedom != object cloning.

---

## 23. Movement Freedom

Movement may occur only while required continuity remains preserved or
explicitly degraded under governing constraints.

Freedom of movement requires continuity of contact.

Movement convenience != permission to lose lineage.

---

## 24. No Premature Passageway

Stick may later bind continuity across a Passageway.

R2-I does not define:

- Passageway establishment;
- adjoining-object contact;
- cross-object authorization;
- passage direction;
- passage state.

Stick != Passageway.

Continuity reference != passage authorization.

---

## 25. No Premature Occupation

Stick may later bind continuity for occupied capabilities.

R2-I does not define:

- occupancy state;
- occupant identity;
- presence;
- capability authorization.

Stick continuity != occupation.

Contact != presence.

---

## 26. R2-I Lock

Movement and representation change shall never require loss of analytical
continuity.

Stick preserves the relationship between movement, perspective shift, Space
operation, and the originating Room Object.

Freedom of movement requires continuity of contact.

Freedom of perspective requires continuity of object identity.

Stick binds object identity.

Stick binds Origin.

Stick binds Ingress.

Stick binds Cartography.

Stick binds provenance.

Stick binds Transform history.

Stick binds evidence lineage.

Stick binds meaningful observation.

Stick binds meaningful restriction.

Stick binds source coordinates.

Stick binds target coordinates.

Stick binds return coordinates.

Stick identity is not object identity.

Cartography != Stick.

Transform != Stick.

Coordinate change != continuity loss.

Restriction != absence.

DEGRADED does not silently become CONTINUOUS.

BROKEN fails closed.

Stick does not move anything.

Stick != Passageway.

Stick continuity != occupation.

No Passageway semantics yet.

No Occupation semantics yet.
