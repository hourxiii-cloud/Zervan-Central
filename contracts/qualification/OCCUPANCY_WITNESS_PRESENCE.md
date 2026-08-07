# R3-D — Occupancy Witness / Presence

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R3-D
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R3-D defines the Occupancy Witness for bounded capability presence in one
Canonical Room Object.

Occupation occurs before interpretation.

R3-D consumes:

- complete Rings 1 and 2;
- R3-A Qualification Request;
- R3-B Qualification Record;
- R3-C Room Lifecycle / Readiness.

R3-D does not yet define:

- capability mission assignment;
- capability movement;
- formation selection;
- proportional force;
- Goblin Signal propagation;
- lifecycle transition to ACTIVE;
- landing;
- hydration.

---

## 1. Occupation Principle

Information is occupied before it is interpreted.

Capabilities occupy the same Room Object through permitted Zones and Spaces.

They do not create private copies of informational reality.

Duplicate capability.

Do not duplicate the Room Object.

---

## 2. Presence

Occupation establishes presence.

Presence means an identified capability is boundedly present against a declared
representation of the same Room Object.

Presence does not establish truth.

Presence does not establish authority.

Presence does not establish movement.

Presence does not establish escalation.

---

## 3. Representation / Mission / Evidence Separation

Occupation establishes presence.

Representation establishes position.

Mission establishes movement.

Evidence establishes escalation.

These are separate state dimensions.

Room state, representation state, occupancy state, and execution state MUST NOT
be conflated.

---

## 4. Occupancy Witness

Every Occupancy Witness MUST preserve:

- `occupancy_witness_id`;
- canonical `object_id`;
- occupant capability;
- occupancy event;
- lifecycle readiness reference;
- Qualification Record reference;
- occupied Zone;
- occupied Space;
- Orientation reference;
- Cartography reference;
- Stick reference;
- entry authorization reference;
- applicable Governance constraint reference;
- Human Gate reference when applicable;
- evidence boundary;
- evidence ceiling;
- current coordinates;
- return coordinates;
- occupancy basis;
- provenance route;
- witness time.

The witness records bounded presence.

It does not create a private Room.

---

## 5. Occupancy Witness Identity

Native-v41 `occupancy_witness_id` is deterministic SHA-512 over the complete
declared Occupancy Witness except `occupancy_witness_id`.

A material occupancy change produces another witness identity.

Occupancy Witness identity is not Room Object identity.

Occupancy Witness identity is not capability identity.

---

## 6. Occupant Capability

The witness identifies the capability occupying the Room representation.

A capability is an occupant and observer.

Capability != truth owner.

Capability != Room identity.

Capability duplication does not imply Room duplication.

---

## 7. Occupancy Event

R3-D defines exactly three occupancy witness events:

- `ENTERED`;
- `PRESENT`;
- `EXITED`.

`ENTERED` records establishment of bounded presence.

`PRESENT` records continued bounded presence at the declared coordinates.

`EXITED` records termination of that bounded presence.

These are witness events, not a complete runtime occupancy state machine.

---

## 8. Readiness Dependency

Analytical occupation requires a Room that is lifecycle `READY`.

An Occupancy Witness for analytical presence MUST preserve the lifecycle
readiness transition reference.

READY makes occupation available.

READY does not itself establish presence.

Occupancy Witness establishes presence.

READY != occupied.

---

## 9. Qualification Dependency

The witness preserves the Qualification Record supporting the qualified Room
surface being occupied.

Qualification Record != Occupancy Witness.

Qualification success does not imply occupation.

QUALIFIED != occupied.

---

## 10. Same-Object Rule

Every Occupancy Witness resolves to one canonical `object_id`.

Zone, Space, Orientation, Cartography, Stick, and capability position MUST
resolve against that same Room Object.

Occupation MUST NOT create another Room Object.

Occupant perspective != new Room.

Observer != object.

---

## 11. Zone

Capabilities occupy through permitted Zones.

The witness preserves the occupied `zone_id`.

The Zone constrains representation.

Occupation does not redefine the Zone.

Zone != occupant.

---

## 12. Space

Capabilities occupy through permitted Spaces.

The witness preserves the occupied `space_id`.

The Space constrains the active mission surface.

Occupation does not redefine the Space.

Space != occupant.

---

## 13. Orientation

The witness preserves Orientation.

Representation establishes position.

Occupancy must therefore remain resolvable to the analytical position from
which the capability is present.

Presence without position is insufficiently witnessed.

---

## 14. Cartography

Cartography preserves capability positions.

The Occupancy Witness records the Cartography reference under which the
capability position is resolvable.

Cartography != occupation.

Mapped position != presence unless witnessed.

---

## 15. Stick

Occupancy preserves contact continuity.

The witness records the Stick reference binding presence to:

- object identity;
- Origin;
- Ingress;
- Cartography;
- provenance;
- transform history;
- evidence lineage;
- return coordinates.

Presence MUST NOT sever continuity.

---

## 16. Entry Authorization

Reconnaissance or analytical capability does not automatically possess Room
entry authority.

The Occupancy Witness preserves the applicable entry authorization reference.

Technical ability to enter != authorization to enter.

Entry authorization != truth authority.

---

## 17. Governance Constraints

Governance defines entry and movement rules, evidence obligations, claim
ceilings, prohibited assumptions, Human Gate requirements, publication
constraints, and promotion conditions.

The Occupancy Witness preserves the applicable Governance constraint reference.

Occupation MUST NOT silently broaden those constraints.

---

## 18. Human Gate

Where Human Gate applies to entry or occupation, the witness preserves its
reference.

Human Gate approval MUST NOT be fabricated.

Approval != presence.

Presence requires the Occupancy Witness itself.

---

## 19. Evidence Boundary and Ceiling

Occupation preserves the evidence boundary and ceiling applicable to the
occupied representation.

Presence does not expand evidence access.

Presence does not raise the evidence ceiling.

Occupation != evidence promotion.

---

## 20. Coordinates

The witness preserves:

- current coordinates;
- return coordinates.

Current coordinates locate the occupied representation.

Return coordinates preserve the route back.

Occupancy coordinate != object identity.

---

## 21. Provenance

Every Occupancy Witness preserves a traversable provenance route.

Presence MUST remain attributable to:

- the same Room Object;
- readiness basis;
- qualification basis;
- bounded representation;
- capability;
- time.

Unattributed presence is invalid.

---

## 22. Observation Boundary

An occupant may later observe.

Occupation itself does not invent an observation.

Presence != interpretation.

Presence != finding.

Presence != conclusion.

Observation semantics remain separately attributable.

---

## 23. Mission Boundary

R3-D does not assign a capability mission.

Mission establishes movement.

R3-E will define Capability Mission Request / Return.

Occupancy Witness != Capability Mission Request.

Presence != mission.

---

## 24. Movement Boundary

R3-D does not move the capability.

Occupation establishes presence.

Movement remains downstream.

ENTERED does not imply unrestricted movement.

PRESENT does not imply movement.

EXITED records ended presence, not how movement occurred.

---

## 25. Formation Boundary

R3-D does not select or create a formation.

One or more occupancy witnesses may later support formation execution.

Occupancy Witness != Formation Selection Record.

Multiple occupants != formation by default.

---

## 26. Lifecycle ACTIVE Boundary

The source defines lifecycle `ACTIVE` as one or more capabilities operating
within declared Zones and Spaces.

R3-D provides the presence witness required by that later transition.

R3-D does not itself mutate Room lifecycle to ACTIVE.

Occupancy Witness != lifecycle mutation.

Presence may support ACTIVE.

Presence != ACTIVE transition.

---

## 27. Goblin Signal Boundary

Goblin Signal carries occupancy changes.

R3-D creates the occupancy evidence that may later be announced.

R3-D does not propagate the event.

Occupancy Witness != Goblin Signal event.

Witness != propagation.

---

## 28. Landing Boundary

Landing may preserve occupation while movement ceases.

R3-D does not define Landing.

EXITED is not Landing.

Landing != exit.

No Landing semantics yet.

---

## 29. Authority Boundary

Occupation does not confer:

- truth authority;
- canonical mutation authority;
- publication authority;
- execution authority.

Authority remains governed by Ring 1.

Write capability != authority.

Occupant != authority.

---

## 30. R3-D Lock

Information is occupied before it is interpreted.

Capabilities occupy the same Room Object through permitted Zones and Spaces.

They do not create private copies of informational reality.

Occupation establishes presence.

Representation establishes position.

Mission establishes movement.

Evidence establishes escalation.

Room state, representation state, occupancy state, and execution state are
distinct.

Capability != truth owner.

Capability != Room identity.

Occupancy Witness identity is not Room Object identity.

Occupancy Witness identity is not capability identity.

READY != occupied.

Occupancy Witness establishes presence.

QUALIFIED != occupied.

Qualification Record != Occupancy Witness.

Occupant perspective != new Room.

Observer != object.

Zone != occupant.

Space != occupant.

Cartography != occupation.

Mapped position != presence unless witnessed.

Presence MUST NOT sever continuity.

Technical ability to enter != authorization to enter.

Entry authorization != truth authority.

Approval != presence.

Presence does not expand evidence access.

Presence does not raise the evidence ceiling.

Occupation != evidence promotion.

Presence != interpretation.

Presence != finding.

Presence != conclusion.

Occupancy Witness != Capability Mission Request.

Presence != mission.

Occupancy Witness != Formation Selection Record.

Multiple occupants != formation by default.

Occupancy Witness != lifecycle mutation.

Presence != ACTIVE transition.

Occupancy Witness != Goblin Signal event.

Witness != propagation.

EXITED is not Landing.

Landing != exit.

Write capability != authority.

Occupant != authority.

No capability mission yet.

No movement execution yet.

No formation selection yet.

No Goblin Signal propagation yet.

No ACTIVE lifecycle transition yet.

No Landing semantics yet.
