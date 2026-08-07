# R2-H — Analytical Cartography

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R2-H
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R2-H defines Analytical Cartography for one Canonical Room Object.

Analytical Cartography is the canonical representation, measurement,
preservation, and communication of:

- the Room Object;
- its bounded representations;
- its analytical geometry;
- its evolution.

R2-H consumes complete Ring 1 and R2-A through R2-G.

R2-H does not redefine those inner contracts.

R2-H does not yet define:

- Stick / Contact Continuity;
- Passageway semantics;
- Occupation semantics;
- capability-position semantics;
- Collapse Boundary semantics;
- propagation-vector semantics.

Where Cartography must preserve those source-required concepts before their
native contracts exist, R2-H preserves opaque references only.

---

## 1. Canonical Cartography

Cartography preserves understanding as navigable geometry.

Analysis produces understanding.

Cartography preserves understanding as navigable geometry without cloning the
object.

Cartography does not create another analytical reality.

---

## 2. Object Binding

Every Cartography Record MUST resolve against one canonical `object_id`.

`cartography_id` identifies the Cartographic representation.

`cartography_id` is not object identity.

Cartography identity != object identity.

Map != Room Object.

---

## 3. Cartography Record

Every Cartography Record MUST preserve:

- `cartography_id`;
- canonical `object_id`;
- object topology;
- Room geometry;
- Zone references;
- Transform references;
- Space references;
- Orientation references;
- Terrain references;
- Territory references;
- provenance anchors;
- evidence boundaries;
- evidence ceilings;
- stable regions;
- uncertainty frontiers;
- deformation regions;
- invariant anchors;
- return routes;
- perspective overlays;
- evolution references;
- recorded time.

It MAY preserve opaque references to later-defined:

- capability positions;
- collapse boundaries;
- passageways;
- propagation vectors.

Those references do not define downstream semantics.

---

## 4. Cartography Identity

Native-v41 `cartography_id` is deterministic SHA-512 over the complete declared
Cartography Record payload except `cartography_id` itself.

The identity therefore binds the exact navigable geometry being preserved.

A material Cartographic change produces another `cartography_id`.

Cartography identity is not object identity.

---

## 5. Object Topology

Cartography preserves object topology.

Topology expresses structural relationships that remain navigable across
bounded representations.

Topology MUST NOT silently fracture merely because representation changes.

Representation difference != topology fracture.

---

## 6. Room Geometry

Cartography preserves Room geometry as currently supported by evidence.

Geometry may evolve.

A geometry change MUST remain attributable.

Prior geometry MUST NOT be silently rewritten out of history.

Geometry evolution != object replacement.

---

## 7. Zone Overlays

Bounded Zones are represented on the same Cartography.

Zone differences are overlays or bounded representation surfaces.

A Zone MUST NOT obtain a private Cartography merely because its perspective
differs.

Zone difference != separate map of reality.

---

## 8. Space Overlays

Bounded Spaces are represented as mission surfaces on the same Cartography.

Different missions may occupy different bounded surfaces.

Space plurality does not create Cartography plurality by default.

Parallel missions != parallel worlds.

---

## 9. Transform Preservation

Cartography preserves Representation Transform references and the coordinate
changes they produce.

The map MUST permit another observer to determine:

- what representation changed;
- what dimensions shifted;
- what remained invariant.

Transform history MUST remain navigable.

---

## 10. Orientation Preservation

Cartography preserves Orientation references and analytical coordinates.

Another observer MUST be able to resolve where prior work occurred without
requiring the original observer's mind, language, or conclusion.

Cartography supports portability.

---

## 11. Terrain

Cartography preserves encountered Terrain references and geometry.

Stable regions, uncertainty frontiers, and deformation regions remain
distinguishable.

Uncertainty MUST NOT be rendered as certainty for visual convenience.

Deformation MUST NOT be normalized away silently.

---

## 12. Territory

Cartography preserves reachable analytical Territory.

Reachable, unreachable, and unresolved geography MUST remain distinguishable
through the underlying R2-C contracts.

Map presence != reachability.

Displayed != reachable.

---

## 13. Provenance Anchors

Cartography preserves provenance anchors.

A mapped feature MUST remain attributable toward supporting evidence and origin
routes where available.

Map location does not replace provenance.

Geometry != provenance.

---

## 14. Evidence Boundaries and Ceilings

Cartography preserves evidence boundaries and ceilings applicable to mapped
representations and missions.

A map MUST NOT visually or structurally imply evidence beyond the declared
ceiling.

Rendering convenience != evidence expansion.

---

## 15. Stable Regions

Cartography may preserve regions currently supported as stable.

Stable does not mean permanently true.

Stable means sufficiently persistent under the current evidence and bounded
representation.

Stable != immutable.

---

## 16. Uncertainty Frontiers

Cartography MUST preserve uncertainty frontiers.

An uncertainty frontier marks geometry beyond which the current evidence does
not support ordinary continuation.

Unknown geography MUST NOT be filled merely for map completeness.

Unknown remains unknown.

---

## 17. Deformation Regions

Cartography preserves deformation regions where representation, evidence,
geometry, or analytical continuity is distorted or unstable.

Deformation is evidence.

It MUST NOT be cosmetically smoothed away.

---

## 18. Invariant Anchors

Cartography preserves invariant anchors required to compare representations.

Invariant anchors may include references to:

- object identity;
- Origin;
- provenance;
- preserved evidence;
- transformation history;
- other explicitly declared invariants.

Invariant anchors permit turning the object without losing what must remain
fixed.

---

## 19. Return Routes

Cartography preserves return routes derived from valid return coordinates.

A return route explains how an observer can resolve back toward a known prior
analytical position.

Return route != Stick.

R2-H maps the route.

R2-I will define continuity of contact across it.

---

## 20. Perspective Overlay Rule

Different Zones and Spaces are represented as:

- overlays;
- transforms;
- coordinate shifts;
- bounded surfaces

on the same Cartography.

The map MUST allow another observer to determine exactly what changed in
representation and what did not.

Perspective difference MUST NOT be resolved by cloning the world.

---

## 21. Disagreement Geometry

Perspective disagreement preserved by R2-F may appear on Cartography as
different overlays, bounded surfaces, evidence paths, or incompatible
interpretive geometry.

Cartography MUST NOT average disagreement into false consensus.

Disagreement remains attributable.

---

## 22. Evolution

Cartography preserves evolution of the Room Object's analytical geometry.

Later Cartography MUST retain references sufficient to reconstruct earlier
mapped states.

Evolution != overwrite.

History accumulates.

---

## 23. Representation Independence

Cartography describes navigable structure rather than requiring one narrative
or domain vocabulary.

A fresh observer should be able to resolve the same geometry even when
terminology or rendering changes.

Renderer != geometry.

Vocabulary != topology.

---

## 24. Capability-Position Reference Boundary

The source architecture requires Cartography to preserve capability positions.

R2-H therefore permits opaque capability-position references.

R2-H does not define:

- occupation;
- occupant identity;
- capability authorization;
- capability movement.

Reference != occupation semantics.

---

## 25. Collapse-Boundary Reference Boundary

The source architecture requires Cartography to preserve collapse boundaries.

R2-H permits opaque collapse-boundary references.

R2-H does not define collapse-boundary behavior.

Reference != collapse doctrine.

---

## 26. Passageway Reference Boundary

The source architecture requires Cartography to preserve passageways.

R2-H permits opaque passageway references.

R2-H does not define Passageway semantics.

Reference != passage authorization.

R2-J owns Passageway / distinct-object contact.

---

## 27. Propagation-Vector Reference Boundary

The source architecture requires Cartography to preserve propagation vectors.

R2-H permits opaque propagation-vector references.

R2-H does not define propagation behavior.

Reference != execution.

---

## 28. No Premature Stick

Cartography preserves object geometry, transforms, provenance, evidence
lineage references, and return routes that Stick will later bind into
continuity of contact.

Cartography != Stick.

Map continuity != Contact Continuity contract.

---

## 29. No Premature Occupation

Cartography may preserve opaque capability-position references.

That does not establish occupation.

Mapped position != occupied position.

Occupation remains downstream.

---

## 30. R2-H Lock

Analytical Cartography is canonical representation, measurement, preservation,
and communication of Room geometry and evolution.

Analysis produces understanding.

Cartography preserves understanding as navigable geometry without cloning the
object.

Cartography identity is not object identity.

Map != Room Object.

Zone differences remain overlays.

Space differences remain bounded mission surfaces.

Transform history is preserved.

Orientation is preserved.

Terrain is preserved.

Territory is preserved.

Provenance anchors are preserved.

Evidence boundaries are preserved.

Evidence ceilings are preserved.

Stable regions remain distinguishable.

Uncertainty frontiers remain distinguishable.

Deformation regions remain distinguishable.

Invariant anchors are preserved.

Return routes are preserved.

Perspective disagreement is not averaged into false consensus.

Evolution != overwrite.

Unknown remains unknown.

Renderer != geometry.

Vocabulary != topology.

Opaque downstream reference != downstream semantics.

Cartography != Stick.

Mapped position != occupied position.

No Stick yet.

No Passageway semantics yet.

No Occupation semantics yet.
