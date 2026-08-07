# R2-D — Bounded Zone

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R2-D
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R2-D defines the Bounded Zone as a persistent, declared representation frame
for one established Canonical Room Object.

R2-D consumes:

- complete Ring 1;
- R2-A Canonical Room Object identity and singularity;
- R2-B Origin Establishment and Object Binding;
- R2-C Terrain and Territory.

R2-D does not redefine them.

R2-D does not yet define:

- Bounded Space;
- Perspective / Representation Transform semantics;
- Orientation semantics;
- Cartography;
- Stick;
- Passageway;
- Occupation;
- capability movement.

---

## 1. Bounded Zone

A Bounded Zone is a persistent, declared representation frame for the
Canonical Room Object.

A Zone preserves one object under explicitly bounded representational
conditions.

A Zone does not create another informational reality.

Reality is established once.

Representation may turn many times.

---

## 2. Object Binding

Every Zone MUST carry the canonical `object_id`.

The Zone belongs to that object.

`zone_id` identifies the declared representation frame.

`zone_id` is not object identity.

Zone identity != object identity.

A new Zone does not create a new Room Object.

---

## 3. Zone Declaration

Every Zone MUST declare:

- `object_id`;
- `zone_id`;
- `transform_type`;
- `perspective_owner_or_discipline`;
- included evidence;
- excluded evidence;
- time frame;
- evidence ceiling;
- prohibited assumptions;
- provenance route;
- return coordinates.

These fields constitute the minimum Zone frame.

No Zone may silently omit a boundary merely because a local capability does
not need to display it.

---

## 4. Zone Identity

Native-v41 `zone_id` is deterministic SHA-512 identity over exactly the
declared Zone frame:

- canonical `object_id`;
- transform type;
- perspective owner or discipline;
- included evidence;
- excluded evidence;
- time frame;
- evidence ceiling;
- prohibited assumptions;
- provenance route;
- return coordinates.

The Zone identity therefore identifies the representation contract itself.

Identical canonical declarations produce the same `zone_id`.

A material change to the representation frame produces another `zone_id`.

Zone identity is not Room identity.

---

## 5. Persistence

A Zone is persistent as a declared representation frame.

Persistence means the Zone declaration remains addressable and replayable after
an active mission ends.

Persistence does not mean:

- permanently active;
- permanently occupied;
- frozen evidence;
- frozen interpretation;
- authority to mutate canonical state.

Zone persistence != occupation.

---

## 6. Included Evidence

Included evidence declares what evidence is admitted into the Zone's
representation frame.

Included evidence MUST remain traceable to provenance.

Inclusion in a Zone does not promote evidence to truth.

Inclusion != canonical acceptance.

---

## 7. Excluded Evidence

Excluded evidence declares evidence known to exist but intentionally outside
the current representation frame.

Excluded evidence MUST NOT silently become nonexistent.

Exclusion may arise from:

- scope;
- time;
- evidence access;
- restriction;
- discipline;
- mission relevance;
- other declared representation constraints.

Excluded != absent.

---

## 8. Evidence Boundary

The union of included evidence, excluded evidence, restrictions, and unresolved
availability defines the explicit evidence boundary of the Zone.

The Zone MUST NOT silently reason beyond its declared evidence boundary.

Known restricted evidence remains known restricted evidence.

Unknown remains unknown.

---

## 9. Time Frame

Every Zone declares a time frame.

The time frame bounds representation.

It does not redefine the underlying object.

Different time frames may expose different Terrain while remaining attached to
the same Room Object.

Time-window change != object change.

---

## 10. Evidence Ceiling

Every Zone declares an evidence ceiling.

R2-D requires the ceiling to be present and attributable.

R2-D does not yet define the complete Evidence Ceiling doctrine.

The value is therefore consumed as an explicit declared boundary and MUST NOT
be locally broadened.

Outer capabilities may operate below the ceiling.

They may not silently raise it.

---

## 11. Prohibited Assumptions

Every Zone declares assumptions that are prohibited within that representation.

A prohibited assumption MUST NOT be reintroduced by:

- a capability;
- a renderer;
- a later Space;
- a local analytical shortcut;
- a perspective-specific convenience.

Outer layers consume the Zone prohibition contract.

They do not rewrite it.

---

## 12. Provenance Route

Every Zone preserves a traversable provenance route back toward:

- Canonical Room Object;
- Genesis lineage;
- Ingress;
- Origin.

Zone-local observations may extend provenance.

They may not replace origin provenance.

---

## 13. Return Coordinates

Every Zone declares return coordinates sufficient to resolve a route back to a
known prior analytical position.

R2-D requires the coordinate declaration.

R2-D does not yet define Orientation or Cartographic coordinate semantics.

Return coordinates therefore remain an opaque declared structure until those
later contracts are locked.

Missing downstream semantics MUST NOT be guessed.

---

## 14. Transform-Type Boundary

Every Zone declares a `transform_type`.

R2-D records the requested or governing transform category.

R2-D does not yet define the full Perspective / Representation Transform
contract.

`transform_type` therefore does not imply a valid `transform_id`.

Transform semantics remain downstream.

---

## 15. Perspective / Discipline Boundary

Every Zone declares the perspective owner or discipline under which the frame
is established.

A perspective or discipline is a representation condition.

It is not a truth owner.

It is not object identity.

Perspective != Room.

Discipline != Room.

---

## 16. Terrain Relationship

Terrain is encountered through representation.

A Zone may expose Terrain different from another Zone while both remain bound
to the same object.

Different Terrain exposure does not create competing realities.

Zone difference != object difference.

---

## 17. Territory Relationship

A Zone may constrain which current Territory is visible or relevant from that
representation frame.

R2-D does not redefine R2-C reachability.

A Zone MUST NOT mark an UNRESOLVED or UNREACHABLE surface as REACHABLE merely
for representational convenience.

Representation cannot manufacture reachability.

---

## 18. Zone-Specific Observation

A Zone may preserve representation-specific observations and interpretations.

Such material MUST remain attributable to the Zone from which it arose.

Zone-specific observation != canonical geometry change.

Zone-specific interpretation != canonical truth.

---

## 19. Canonical Geometry Mutation Boundary

If a Zone produces evidence supporting a change to canonical Room geometry,
the proposed change MUST identify:

- the originating `zone_id`;
- relevant evidence;
- provenance;
- the proposed effect.

Any canonical mutation remains governed by inner authority and state contracts,
including Human Gate where required.

Zone observation does not itself authorize mutation.

Question != permission to mutate state.

---

## 20. Zone Lifecycle Boundary

R2-D defines Zone declaration and identity.

It does not yet define a full Zone lifecycle.

A Zone may be declared and persisted without implying:

- active Space;
- occupation;
- active capability;
- active mission;
- canonical state mutation.

Those relationships remain downstream.

---

## 21. Space Boundary

A Zone is a persistent representation frame.

A Space will later define an active mission surface within a Zone or declared
direct transform.

R2-D MUST NOT absorb Space semantics.

Zone != Space.

Persistent frame != active mission.

R2-E owns Bounded Space.

---

## 22. No Premature Transform

R2-D declares enough transform information to make the Zone boundary explicit.

It does not implement Perspective / Representation Transform behavior.

Transform history, source orientation, target orientation, shifted dimensions,
and preserved invariants remain downstream.

---

## 23. No Premature Orientation

R2-D requires return coordinates but does not define Orientation.

A Zone cannot invent orientation semantics merely because it contains a
coordinate field.

Coordinates declared != Orientation resolved.

---

## 24. No Premature Cartography

A Zone may later appear in Cartography.

The Zone is not itself Cartography.

Zone != map.

Zone != Cartography.

---

## 25. No Premature Occupation

A Zone may later be occupied by authorized capabilities.

Zone existence does not imply occupation.

Zone declared != Zone occupied.

Occupation remains downstream.

---

## 26. R2-D Lock

A Bounded Zone is a persistent declared representation frame.

Reality is established once.

Representation may turn many times.

Every Zone remains attached to one canonical `object_id`.

Zone identity is not object identity.

A Zone does not create a new Room Object.

Included evidence is explicit.

Excluded evidence is explicit.

Excluded != absent.

Time frame is explicit.

Evidence ceiling is explicit.

Prohibited assumptions are explicit.

Provenance route is explicit.

Return coordinates are explicit.

Zone-local observations remain attributable to the Zone.

Zone observation does not authorize canonical mutation.

Zone != Space.

Persistent frame != active mission.

Representation cannot manufacture reachability.

No Space semantics yet.

No full Transform semantics yet.

No Orientation semantics yet.

No Cartography yet.

No Stick yet.

No Occupation yet.
