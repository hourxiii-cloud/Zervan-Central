# R2-E — Bounded Space

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R2-E
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R2-E defines the Bounded Space as an active mission surface operating on one
Canonical Room Object through either:

- a declared Bounded Zone; or
- a direct transform contract reference.

R2-E consumes:

- complete Ring 1;
- R2-A Canonical Room Object identity and singularity;
- R2-B Origin Establishment and Object Binding;
- R2-C Terrain and Territory;
- R2-D Bounded Zone.

R2-E does not redefine them.

R2-E does not yet define:

- full Perspective / Representation Transform semantics;
- Orientation;
- Cartography;
- Stick;
- Passageway;
- Occupation;
- capability movement.

---

## 1. Bounded Space

A Bounded Space is an active mission surface operating on the same Canonical
Room Object through a declared Zone or direct transform contract.

A Space exists to bound operation.

A Space does not create another informational reality.

A Space does not own canonical truth.

---

## 2. Object Binding

Every Space MUST carry canonical `object_id`.

A Space remains attached to the same Room Object as its governing Zone or
direct transform.

`space_id` identifies the bounded mission contract.

`space_id` is not object identity.

Space identity != object identity.

Space creation != Room creation.

---

## 3. Zone / Direct-Transform Binding

Every Space MUST declare exactly one representation binding mode:

- `ZONE`
- `DIRECT_TRANSFORM`

When binding mode is `ZONE`:

- `zone_id` MUST be present;
- `direct_transform_reference` MUST be null.

When binding mode is `DIRECT_TRANSFORM`:

- `direct_transform_reference` MUST be present;
- `zone_id` MUST be null.

A Space MUST NOT silently float without a representation frame.

---

## 4. Zone and Space Distinction

A Zone persists a bounded representation frame.

A Space performs a bounded mission within that frame.

Both preserve the same object identity.

Zone != Space.

Persistent representation frame != active mission surface.

A Space MUST NOT redefine the Zone that contains it.

---

## 5. Space Mission Contract

A Space may define:

- field;
- discipline;
- question set;
- controls;
- capabilities;
- evidence ceiling;
- allowed mission;
- prohibited assumptions;
- rendering obligations.

These fields bound operation.

They do not grant authority.

---

## 6. Space Identity

Native-v41 `space_id` is deterministic SHA-512 over exactly:

- canonical `object_id`;
- representation binding mode;
- `zone_id` or direct transform reference;
- field;
- discipline;
- question set;
- controls;
- capabilities;
- evidence ceiling;
- allowed mission;
- prohibited assumptions;
- rendering obligations.

Identical canonical mission contracts produce the same `space_id`.

A material change to the mission contract produces a different `space_id`.

Space identity is mission identity.

Space identity is not Room identity.

---

## 7. Active Mission Surface

A Space is active because it defines current bounded operational purpose.

"Active" in R2-E means mission-bearing.

It does not yet mean:

- occupied;
- capability currently executing;
- authorized mutation;
- successful operation;
- analytical conclusion reached.

Mission-bearing != occupied.

Mission-bearing != executing.

---

## 8. Field

A Space may declare the analytical field relevant to the mission.

Field narrows operation.

Field does not create authority.

Field does not redefine object identity.

---

## 9. Discipline

A Space may declare the discipline under which the mission proceeds.

Discipline is an operational constraint.

Discipline does not own truth.

Discipline does not replace the governing Zone perspective or object identity.

---

## 10. Question Set

A Space may declare one or more questions that justify the mission.

A question defines inquiry.

A question does not authorize state mutation.

Question != authority.

Question != write permission.

---

## 11. Controls

A Space may declare controls applicable to the mission.

Controls constrain operation.

A Space MUST NOT weaken inherited inner controls.

Outer control may narrow.

Outer control may not silently broaden authority.

---

## 12. Capabilities

A Space may declare which capabilities are permitted for the mission.

Capability declaration indicates bounded mission eligibility.

It does not prove:

- capability availability;
- capability verification;
- capability occupation;
- capability execution;
- capability authority.

Declared capability != active capability.

Capability != authority.

---

## 13. Evidence Ceiling

Every Space MUST declare an evidence ceiling.

A Space ceiling MUST NOT exceed the governing Zone ceiling when bound through a
Zone.

A Space may narrow the Zone ceiling.

It may not silently raise it.

When using direct transform binding, the ceiling must remain explicit and
attributable to that transform contract.

---

## 14. Allowed Mission

Every Space MUST declare its allowed mission.

Operation outside the allowed mission is out of bounds.

A broad question does not silently expand mission scope.

Mission expansion requires a new or revised bounded mission contract.

---

## 15. Prohibited Assumptions

Every Space MUST declare prohibited assumptions.

Space prohibitions inherit all applicable Zone prohibitions.

A Space may add prohibitions.

It MUST NOT silently remove inherited prohibitions.

Inner prohibition survives outer operation.

---

## 16. Rendering Obligations

A Space may declare rendering obligations for outputs produced from the
mission.

Rendering obligations constrain presentation.

They do not own evidence, analytical truth, canonical geometry, or object
identity.

Rendering != reality.

---

## 17. Territory Relationship

A Space operates only against Territory legitimately reachable under the
governing representation.

A Space MUST NOT manufacture reachability.

A mission does not make an UNRESOLVED surface REACHABLE.

Question != passage.

Mission != reachability.

---

## 18. Terrain Relationship

A Space may encounter Terrain relevant to the bounded mission.

The Space may restrict which Terrain is considered.

It MUST NOT redefine encountered Terrain merely to satisfy the mission.

Mission boundary != evidence rewrite.

---

## 19. Authority Boundary

A Space does not possess authority.

The existence of:

- a Space;
- a question;
- a mission;
- a permitted capability;
- a control set

does not itself authorize canonical mutation.

Authority remains inherited from Ring 1.

Space != authority.

---

## 20. Canonical Mutation Boundary

A Space may produce observations or proposals that support canonical mutation.

Any such mutation remains governed by:

- provenance;
- state contracts;
- authority;
- Human Gate where required.

The Space MUST identify the mission and representation from which the proposed
change arose.

Space observation != canonical write.

---

## 21. Space Restriction Invariant

A Space restricts operation.

It does not fracture object identity.

Different Spaces may:

- ask different questions;
- use different disciplines;
- expose different evidence;
- permit different capabilities;
- impose different rendering obligations.

Those differences do not create different Rooms.

---

## 22. Multiple Spaces

One Zone may support multiple Spaces.

Multiple Spaces may operate against the same object under the same persistent
representation frame.

Space plurality != reality plurality.

Parallel missions != parallel worlds.

---

## 23. Direct Transform Boundary

The source permits a Space to operate through a declared Zone or direct
transform contract.

R2-E preserves that route.

R2-E does not yet define the transform contract itself.

A direct transform reference is therefore opaque but mandatory when that mode
is used.

Full transform semantics remain R2-F.

---

## 24. No Premature Orientation

A Space may later operate from a resolved Orientation.

R2-E does not define Orientation.

Mission location != Orientation contract.

---

## 25. No Premature Cartography

A Space may later occupy or traverse mapped analytical geography.

R2-E does not define Cartography.

Space != map.

Mission != Cartography.

---

## 26. No Premature Stick

Continuity between movement, perspective shifts, Space operation, and the
originating Room Object will later be governed by Stick / Contact Continuity.

R2-E does not define Stick.

Space binding != Stick.

---

## 27. No Premature Occupation

A Space may later be occupied by permitted capabilities.

Space existence does not mean an occupant is present.

Space active != capability active.

Occupation remains downstream.

---

## 28. R2-E Lock

A Bounded Space is an active mission surface.

It operates on the same Room Object.

It binds through a declared Zone or direct transform contract.

Zone persists the frame.

Space performs the mission.

Zone != Space.

Space identity is not object identity.

A Space restricts operation.

It does not fracture object identity.

Field may constrain.

Discipline may constrain.

Questions may constrain.

Controls may constrain.

Capabilities may be permitted.

Evidence ceiling may narrow.

Allowed mission is explicit.

Prohibited assumptions are explicit.

Rendering obligations are explicit.

Capability != authority.

Question != authority.

Mission != reachability.

Space observation != canonical write.

Parallel missions != parallel worlds.

No full Transform semantics yet.

No Orientation yet.

No Cartography yet.

No Stick yet.

No Occupation yet.
