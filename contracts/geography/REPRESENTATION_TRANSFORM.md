# R2-F — Perspective / Representation Transform

Status: CONTROLLED CANDIDATE CONTRACT

Ring: R2-F

Version: vTemporal.41.0

Promotion State: CANDIDATE

---

## 0. Purpose

R2-F defines how one Canonical Room Object may be deliberately turned through

bounded representation change without cloning reality.

R2-F consumes:

- complete Ring 1;

- R2-A through R2-E.

R2-F does not redefine object identity, Zone, Space, Terrain, Territory, state,

authority, or lineage.

R2-F does not yet define:

- full Orientation semantics;

- Cartography;

- Stick / Contact Continuity;

- Passageway;

- Occupation;

- capability movement.

---

## 1. Perspective

A perspective is not a truth claim.

A perspective is not a separate Room.

A perspective is a bounded representation applied to one Canonical Room

Object.

Perspective != reality.

Perspective != object identity.

Perspective change != object change.

---

## 2. Representation Transform

A Representation Transform is the explicit contract that turns one bounded

representation of the Room Object into another while preserving declared

invariants.

TURN THE OBJECT.

DO NOT CLONE THE WORLD.

---

## 3. Transform Record

Every Transform Record MUST declare:

- `transform_id`;

- `object_id`;

- source orientation;

- target orientation;

- shifted dimensions;

- preserved invariants;

- included evidence;

- excluded evidence;

- assumptions;

- prohibited assumptions;

- evidence ceiling;

- return coordinates.

No transform may remain implicit.

---

## 4. Transform Identity

Native-v41 `transform_id` is deterministic SHA-512 over exactly:

- canonical `object_id`;

- source orientation;

- target orientation;

- shifted dimensions;

- preserved invariants;

- included evidence;

- excluded evidence;

- assumptions;

- prohibited assumptions;

- evidence ceiling;

- return coordinates.

Identical canonical transform declarations produce the same `transform_id`.

A material transform-contract change produces another `transform_id`.

Transform identity is not object identity.

---

## 5. Shifted Dimensions

A valid transform explicitly identifies dimensions allowed to shift.

Shiftable dimensions may include:

- observer;

- role;

- discipline;

- time window;

- scale;

- sensory modality;

- evidence access;

- mission;

- language.

This list is extensible by explicit declaration.

A dimension MUST NOT shift silently.

---

## 6. Preserved Invariants

Every transform MUST preserve, at minimum:

- object identity;

- origin route;

- provenance;

- preserved evidence;

- declared transformation history.

A transform that cannot preserve required invariants is not a valid transform.

Representation change is subordinate to invariants.

---

## 7. Object Identity Continuity

The source and target representation MUST resolve to the same canonical

`object_id`.

A transform does not create another Room Object.

If evidence indicates a genuinely distinct object, R1-F distinct-object

semantics apply instead.

Transform != branch.

Transform != distinct object.

---

## 8. Evidence Inclusion and Exclusion

Every transform explicitly declares:

- included evidence;

- excluded evidence.

Excluded evidence remains existentially represented.

Excluded != absent.

A transform MUST NOT erase evidence merely because the target representation

does not expose it.

---

## 9. Assumptions

A Transform Record may declare assumptions active in the target

representation.

Assumptions MUST be explicit and attributable.

Assumption != evidence.

Assumption != fact.

---

## 10. Prohibited Assumptions

Every transform declares prohibited assumptions.

A target representation MUST NOT reintroduce a prohibited assumption inherited

from its source Zone, Space, or governing contract.

Transform freedom does not override inner prohibitions.

---

## 11. Evidence Ceiling

Every transform declares an evidence ceiling.

The target representation MUST NOT silently exceed the governing source

ceiling.

A transform may narrow visibility or analytical reach.

It may not manufacture additional evidence authority.

Representation change != evidence promotion.

---

## 12. Source Orientation

Every transform declares a source orientation.

R2-F treats source orientation as a declared coordinate/state reference.

R2-F does not yet define complete Orientation semantics.

The reference must remain explicit and resolvable.

---

## 13. Target Orientation

Every transform declares a target orientation.

The target orientation expresses where the representation intends to turn.

Target orientation does not imply analytical validity by itself.

Requested orientation != validated orientation.

Full Orientation semantics remain R2-G.

---

## 14. Return Coordinates

Every transform declares return coordinates.

Return coordinates preserve a route back toward the prior analytical position.

R2-F records and binds them.

R2-F does not yet define Cartographic coordinate mechanics.

Return coordinates MUST NOT be silently discarded.

---

## 15. Transformation History

A transform MUST preserve declared transformation history.

A later transform does not erase prior transforms.

Transform chaining MUST remain reconstructible.

History accumulates.

Representation change does not rewrite prior representation history.

---

## 16. Zone Relationship

A Zone may declare a transform type and representation boundary.

R2-F provides the full Transform Record that may govern or explain that Zone.

Zone != Transform.

A Zone persists a representation frame.

A Transform defines the change between representation states.

---

## 17. Space Relationship

A Space may bind directly to a transform contract or operate within a Zone.

R2-F provides the transform contract referenced by a direct-transform Space.

Space != Transform.

Mission != representation change.

---

## 18. Transform Validation

A transform is valid only when:

1. `object_id` is preserved.

2. source and target orientation are explicit.

3. shifted dimensions are explicit.

4. required invariants are preserved.

5. included/excluded evidence is explicit.

6. assumptions are explicit.

7. prohibited assumptions are preserved.

8. evidence ceiling is explicit.

9. return coordinates are explicit.

10. no prohibited identity fracture occurs.

---

## 19. Perspective Disagreement

Different bounded representations may produce incompatible interpretations.

The system MUST preserve disagreement as attributable geometry and evidence.

It MUST NOT resolve disagreement by:

- cloning the Room;

- silently selecting one perspective;

- averaging incompatible perspectives into false consensus;

- erasing minority evidence;

- collapsing incompatible interpretations without evidence.

Disagreement != duplicate reality.

Disagreement is preserved.

---

## 20. Canonical Mutation Boundary

A transform may expose evidence that supports a proposed canonical mutation.

The transform itself does not authorize mutation.

Any mutation remains governed by inner state, provenance, authority, and Human

Gate controls.

Transform != write authority.

---

## 21. Reversibility

Transforms SHOULD be reversible where possible.

When full reversal is impossible, the record MUST still preserve enough

history and return coordinates to explain:

- what changed;

- what did not;

- what was excluded;

- what cannot be reconstructed.

Irreversibility MUST NOT be hidden.

---

## 22. Representation Independence

The transform contract MUST survive vocabulary change.

A valid transform is defined by structural relationships and preserved

invariants, not by a specific narrative wrapper.

Representation style != canonical meaning.

---

## 23. No Premature Cartography

Transforms will later be represented on Cartography.

R2-F does not define the map.

Transform != Cartography.

R2-H owns Cartography.

---

## 24. No Premature Stick

Transforms must preserve continuity requirements that Stick will later bind

across movement and representation changes.

R2-F does not define Stick.

Transform history != Stick.

---

## 25. No Premature Occupation

A transform may be available without any capability occupying either source or

target representation.

Transform existence != occupation.

Occupation remains downstream.

---

## 26. R2-F Lock

A perspective is not a truth claim.

A perspective is not a separate Room.

A Representation Transform turns one object without cloning it.

Every transform declares what shifts.

Every transform declares what remains invariant.

Object identity is preserved.

Origin route is preserved.

Provenance is preserved.

Preserved evidence is preserved.

Transformation history is preserved.

Included evidence is explicit.

Excluded evidence is explicit.

Excluded != absent.

Assumptions are explicit.

Prohibited assumptions are explicit.

Evidence ceiling is explicit.

Source orientation is explicit.

Target orientation is explicit.

Return coordinates are explicit.

Transform identity is not object identity.

Transform != branch.

Disagreement != duplicate reality.

Disagreement is preserved.

Transform != write authority.

No full Orientation semantics yet.

No Cartography yet.

No Stick yet.

No Occupation yet.

