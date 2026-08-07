# R2-G — Orientation and Coordinates

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R2-G
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R2-G defines Orientation and Coordinates for one Canonical Room Object.

Orientation resolves the analytical position from which reasoning may proceed.

R2-G consumes:

- complete Ring 1;
- R2-A Canonical Room Object;
- R2-B Origin Establishment;
- R2-C Terrain and Territory;
- R2-D Bounded Zone;
- R2-E Bounded Space;
- R2-F Perspective / Representation Transform.

R2-G does not redefine them.

R2-G does not yet define:

- Cartography;
- Stick / Contact Continuity;
- Passageway;
- Occupation;
- capability movement.

---

## 1. Orientation Principle

Orientation precedes reasoning.

The first operational question is:

`Where am I?`

Reasoning MUST NOT silently begin from an unresolved analytical position when
the mission requires a resolved position.

Orient first.

Reason second.

---

## 2. First Orientation Sequence

The orientation sequence is:

Where am I?
    ->
What Origin?
    ->
Which Canonical Room Object?
    ->
What Bounded Zone currently frames it?
    ->
What Territory is reachable from this orientation?
    ->
What Bounded Space is active?
    ->
What perspective, discipline, time, and evidence constraints define this
representation?
    ->
What question or mission justifies turning or moving?
    ->
What evidence boundary and evidence ceiling apply?
    ->
Now reason.

The sequence preserves dependency order.

Later questions MUST NOT silently redefine earlier answers.

---

## 3. Orientation Record

An Orientation Record MUST declare:

- `orientation_id`;
- canonical `object_id`;
- origin reference;
- Zone reference when applicable;
- Territory reference;
- Space reference when applicable;
- Representation Transform reference when applicable;
- perspective or discipline;
- time constraint;
- evidence constraints;
- active question;
- active mission;
- evidence boundary;
- evidence ceiling;
- current coordinates;
- return coordinates;
- resolution state;
- provenance route.

The record answers where the analytical operation currently stands.

---

## 4. Orientation Identity

Native-v41 `orientation_id` is deterministic SHA-512 over exactly:

- canonical `object_id`;
- origin reference;
- Zone reference;
- Territory reference;
- Space reference;
- Representation Transform reference;
- perspective or discipline;
- time constraint;
- evidence constraints;
- active question;
- active mission;
- evidence boundary;
- evidence ceiling;
- current coordinates;
- return coordinates;
- resolution state;
- provenance route.

Identical canonical Orientation declarations produce the same
`orientation_id`.

A material Orientation change produces another `orientation_id`.

Orientation identity is not object identity.

---

## 5. Coordinates

Coordinates are resolvable analytical location data attached to the same Room
Object.

Coordinates locate representation and analytical position.

Coordinates do not create reality.

Coordinates do not create object identity.

Coordinate change != object change.

---

## 6. Coordinate Structure Boundary

R2-G requires coordinates to be explicit and resolvable.

R2-G intentionally permits structured coordinate payloads because later
Cartography will define richer geometry.

At R2-G, coordinates MUST identify sufficient references to explain current
analytical position without inventing Cartographic semantics.

Coordinates declared != Cartography complete.

---

## 7. Current Coordinates

Current coordinates identify the present bounded analytical position.

They MUST remain attributable to the same canonical `object_id`.

Current coordinates may change when:

- the object is turned;
- a Zone changes;
- a Space changes;
- a transform changes;
- the active evidence boundary changes;
- the mission legitimately moves.

None of those changes alone creates another Room Object.

---

## 8. Return Coordinates

Every resolved Orientation MUST preserve return coordinates.

Return coordinates provide a resolvable route toward a known prior analytical
position.

Return coordinates MUST NOT be silently discarded during:

- representation change;
- mission change;
- evidence restriction;
- later movement;
- later rendering.

Return coordinates support continuity.

They do not themselves define Stick.

---

## 9. Resolution State

Orientation has one of three R2-G resolution states:

- `RESOLVED`;
- `PROVISIONAL`;
- `UNRESOLVED`.

RESOLVED means sufficient orientation coordinates and boundaries exist for the
declared mission.

PROVISIONAL means bounded orientation exists but one or more declared elements
remain provisional.

UNRESOLVED means the analytical position is not sufficiently established for
reasoning that requires resolved orientation.

UNRESOLVED MUST NOT silently become RESOLVED.

---

## 10. Object Identity

Every Orientation Record resolves against one canonical `object_id`.

Perspective, coordinates, Zone, Space, or transform MUST NOT substitute for
Room Object identity.

Orientation != Room.

Coordinates != Room.

---

## 11. Origin

Orientation MUST preserve a resolvable route to Origin.

A later representation may move far from the ingress position while still
remaining tied to the same origin route.

Distance in analytical representation does not erase provenance.

---

## 12. Zone

When a Zone frames the current representation, Orientation MUST carry its
`zone_id`.

Orientation does not redefine the Zone.

Zone identity remains representation-frame identity.

---

## 13. Territory

Orientation MUST identify the Territory against which reachability is being
resolved.

The Orientation Record MUST NOT treat unresolved or unreachable geography as
reachable merely because the mission requests it.

Desired direction != reachable Territory.

---

## 14. Space

When an active bounded mission surface exists, Orientation MUST carry its
`space_id`.

The Space supplies mission restrictions.

Orientation locates the mission.

Orientation does not redefine the mission.

---

## 15. Representation Transform

When current position results from a Representation Transform, Orientation MUST
carry the relevant transform reference.

The transform explains what shifted and what remained invariant.

Orientation records the resulting analytical position.

Orientation != Transform.

---

## 16. Perspective / Discipline / Time

Orientation explicitly records applicable:

- perspective or discipline;
- time constraint;
- evidence constraints.

These are representation coordinates.

They do not own truth.

They do not create separate Rooms.

---

## 17. Question and Mission

Orientation records the active question and mission because movement or turning
must be justified by analytical need.

Question identifies inquiry.

Mission identifies bounded operational purpose.

Neither field grants authority.

Question != authority.

Mission != authority.

---

## 18. Evidence Boundary and Ceiling

Orientation MUST declare the evidence boundary and evidence ceiling applicable
at that analytical position.

Reasoning MUST remain inside those declared constraints.

A coordinate shift MUST NOT silently broaden the evidence ceiling.

Movement != evidence promotion.

---

## 19. Portability

Portability means another observer can resolve:

- the same object;
- the same Origin route;
- the relevant representation;
- the relevant mission;
- the relevant evidence boundary;
- the coordinates required to continue or challenge the work.

Portability does not require:

- the same observer;
- the same wording;
- the same affect;
- the same conclusion.

Same analytical world != same mind.

---

## 20. Replay Boundary

Historical coordinates remain historical positions of the same object.

Replay may later reopen the same Room at preserved historical coordinates.

Historical coordinate != duplicate reality.

R2-G preserves coordinate identity and referenceability.

It does not yet define replay execution.

---

## 21. Orientation Change

A change in Orientation may result from legitimate:

- transform;
- Zone shift;
- Space shift;
- time shift;
- evidence-boundary shift;
- mission shift;
- analytical movement.

Orientation change MUST be explicit.

It MUST NOT silently rewrite prior coordinates.

History accumulates.

---

## 22. No Premature Cartography

R2-G defines resolvable analytical coordinates.

R2-H will define Cartography as the canonical representation, measurement,
preservation, and communication of analytical geometry.

Orientation != Cartography.

Coordinates != map.

---

## 23. No Premature Stick

R2-G preserves current and return coordinates.

R2-I will define Stick / Contact Continuity across movement and representation
change.

Coordinates support continuity.

Coordinates != Stick.

---

## 24. No Premature Passageway

R2-G may identify a desired or reachable direction.

It does not define passage between distinct analytical objects.

Orientation != Passageway.

---

## 25. No Premature Occupation

Orientation answers where an analytical operation is positioned.

It does not establish capability presence.

Oriented != occupied.

Occupation remains downstream.

---

## 26. R2-G Lock

Where am I?

Orient first.

Reason second.

Orientation resolves against one Canonical Room Object.

Orientation identity is not object identity.

Coordinates locate analytical position.

Coordinates do not create reality.

Current coordinates are explicit.

Return coordinates are explicit.

Origin route is preserved.

Zone reference is explicit when applicable.

Territory reference is explicit.

Space reference is explicit when applicable.

Transform reference is explicit when applicable.

Perspective or discipline is explicit.

Time constraint is explicit.

Evidence constraints are explicit.

Question and mission are explicit.

Evidence boundary is explicit.

Evidence ceiling is explicit.

UNRESOLVED does not silently become RESOLVED.

Coordinate change does not create another Room.

Historical coordinate != duplicate reality.

Same analytical world != same mind.

Orientation != Cartography.

Coordinates != map.

Coordinates != Stick.

Orientation != Passageway.

Oriented != occupied.

No Cartography yet.

No Stick yet.

No Passageway yet.

No Occupation yet.
