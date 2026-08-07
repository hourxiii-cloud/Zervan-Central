# R2-J — Passageways and Distinct-Object Contact

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R2-J
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R2-J defines Passageways and controlled contact between genuinely distinct
Canonical Room Objects.

R2-J closes Ring 2 Operational Geography.

R2-J consumes:

- complete Ring 1;
- R1-F distinct-object semantics;
- R2-A through R2-I Operational Geography.

R2-J does not redefine the distinct-object test.

R2-J does not define Occupation or capability movement execution.

---

## 1. Passageway

A Passageway is a controlled, attributable relationship through which two
genuinely distinct Room Objects may be placed into analytical contact while
preserving their independent identities, origins, boundaries, geometry,
provenance, and return routes.

A Passageway connects.

A Passageway does not collapse.

Contact != identity collapse.

---

## 2. Adjoining Room

An adjoining Room is legitimate only when evidence supports a genuinely
distinct analytical object.

The adjoining object MUST preserve its own:

- canonical object identity;
- independent Genesis lineage;
- Origin route;
- boundary;
- geometry;
- provenance.

Related does not mean identical.

Different perspective does not mean distinct object.

---

## 3. Distinct-Object Dependency

R2-J consumes the R1-F Distinct Object Determination.

The determination states are:

- `SAME_OBJECT`;
- `DISTINCT_OBJECT`;
- `UNRESOLVED`.

R2-J MUST NOT invent another distinct-object classifier.

R2-J MUST NOT reinterpret a SAME_OBJECT determination as cross-object contact.

Only `DISTINCT_OBJECT` can support an ESTABLISHED Passageway.

---

## 4. Independent Identity

A Passageway MUST carry:

- source `object_id`;
- target `object_id`.

For an ESTABLISHED Passageway:

`source_object_id != target_object_id`

A Passageway MUST NOT substitute relationship identity for either Room Object.

Passageway identity is not Room identity.

Relationship != identity.

---

## 5. Independent Genesis

A target object participating in an ESTABLISHED Passageway MUST already satisfy
the R1-F requirement for independent Genesis lineage.

Passageway creation does not establish the target Room Object.

Contact cannot manufacture object identity.

Passageway != Genesis.

---

## 6. Passageway Record

Every Passageway Record MUST preserve:

- `passageway_id`;
- source object identity;
- target object identity;
- distinct-object determination reference;
- distinct-object result;
- relationship to source;
- source Origin reference;
- target Origin reference;
- source Cartography reference;
- target Cartography reference;
- source Stick reference;
- target Stick reference;
- shared provenance;
- non-shared provenance;
- evidence-of-distinctness references;
- passageway conditions;
- contamination controls;
- return route;
- authorization reference;
- Human Gate reference when applicable;
- Passageway state;
- provenance route;
- recorded time.

---

## 7. Passageway Identity

Native-v41 `passageway_id` is deterministic SHA-512 over the complete declared
Passageway Record except `passageway_id`.

The Passageway identity identifies the contact contract.

Passageway identity is not source object identity.

Passageway identity is not target object identity.

---

## 8. Passageway State

R2-J defines three Passageway states:

- `PROPOSED`;
- `ESTABLISHED`;
- `BLOCKED`.

PROPOSED means a candidate adjoining-object relationship has been identified
but cross-object contact is not yet established.

ESTABLISHED means the distinct-object and contact prerequisites have resolved.

BLOCKED means the Passageway may not currently be established under the
available evidence, controls, or authority.

PROPOSED != ESTABLISHED.

BLOCKED != absent.

---

## 9. ESTABLISHED Preconditions

A Passageway may become ESTABLISHED only when:

1. source object identity is present;
2. target object identity is present;
3. source and target identities differ;
4. the R1-F result is `DISTINCT_OBJECT`;
5. the Distinct Object Determination reference is preserved;
6. evidence of distinctness is preserved;
7. relationship to the source is explicit;
8. shared provenance is preserved;
9. non-shared provenance is preserved;
10. source Origin is preserved;
11. target Origin is preserved;
12. source Cartography is preserved;
13. target Cartography is preserved;
14. source continuity is preserved through Stick;
15. target continuity is preserved through Stick;
16. passageway conditions are explicit;
17. contamination controls are explicit;
18. return route is explicit;
19. provenance is explicit;
20. applicable authorization resolves.

Missing evidence MUST NOT be fabricated to satisfy establishment.

---

## 10. SAME_OBJECT Boundary

If the Distinct Object Determination is `SAME_OBJECT`, R2-J MUST NOT establish a
Passageway between separate Room identities.

The correct route remains inside the existing Room Object through its lawful
Zone, Space, Transform, Orientation, Cartography, Branch, or other
same-object mechanism.

Same object != Passageway.

Do not clone the Room to create a Passageway.

---

## 11. UNRESOLVED Boundary

If the Distinct Object Determination is `UNRESOLVED`, a Passageway may remain
PROPOSED or become BLOCKED.

It MUST NOT become ESTABLISHED.

Unresolved distinctness != permission to create another Room.

Unknown remains unknown.

---

## 12. Relationship

Every Passageway preserves the relationship between the source and target
objects.

The relationship may establish contact.

It does not establish sameness.

Related != identical.

Correlation != identity.

Adjacency != identity.

---

## 13. Shared Provenance

Distinct Room Objects may share provenance.

Shared provenance MUST remain explicit.

Shared provenance does not collapse object identity.

Shared source material != same analytical object.

---

## 14. Non-Shared Provenance

Distinct-object contact MUST also preserve non-shared provenance where known.

Non-shared provenance helps preserve the independent boundaries and origin
histories of the objects.

No cross-object operation may erase non-shared provenance for convenience.

---

## 15. Evidence of Distinctness

Every ESTABLISHED Passageway MUST preserve references to the evidence supporting
the `DISTINCT_OBJECT` determination.

The Passageway does not own that determination.

It consumes it.

Passageway convenience is not evidence of distinctness.

---

## 16. Passageway Conditions

Every Passageway MUST declare its conditions.

Conditions describe the bounded circumstances under which contact is valid.

A Passageway MUST NOT silently broaden those conditions.

Contact outside declared conditions is not established contact.

---

## 17. Contamination Controls

Every Passageway MUST preserve contamination controls.

Cross-object contact MUST NOT silently:

- copy unsupported state;
- inherit conclusions;
- promote assumptions;
- overwrite evidence boundaries;
- erase origin distinctions;
- merge provenance;
- collapse object identities.

Contact does not mean contamination is acceptable.

---

## 18. Bidirectionality

A Passageway relationship does not automatically imply unrestricted
bidirectional movement.

Any permitted directionality MUST be declared as a Passageway condition.

A -> B does not silently authorize B -> A.

Directionality != identity.

---

## 19. Return Route

Every Passageway MUST preserve a return route to the source analytical
position.

The return route MUST retain enough information to recover:

- source object;
- source Cartography;
- source Orientation or coordinates where applicable;
- source provenance context.

Cross-object contact must not strand analytical lineage.

---

## 20. Cartography

Both objects retain independent Cartography.

A Passageway may be represented on both maps.

The Passageway does not fuse the maps into one object.

Connected maps != merged reality.

---

## 21. Stick / Contact Continuity

Stick preserves continuity on each side of the Passageway.

A Passageway MUST preserve source and target Stick references for ESTABLISHED
contact.

The Passageway does not replace Stick.

Stick != Passageway.

Passageway connects continuity domains without collapsing them.

---

## 22. Cross-Object Comparison

Cross-object:

- comparison;
- correlation;
- relationship analysis;
- combined rendering;
- Passageway analysis

may reference both objects while preserving their identities.

Cross-object contact != Merge.

Cross-object contact != new synthesized object.

---

## 23. Merge Boundary

A Passageway does not perform Merge.

If lineages are later merged, R1-F Merge semantics govern.

Merge convenience is not evidence that two objects are identical.

Passageway != Merge.

---

## 24. Synthesized-Object Boundary

If later evidence supports a genuinely new synthesized analytical object, that
object requires its own:

- `DISTINCT_OBJECT` determination;
- independent Genesis establishment;
- provenance;
- source-object references;
- applicable authorization;
- Human Gate where required.

A Passageway alone cannot create the synthesized object.

---

## 25. Authorization

Passageway establishment is governed.

Technical ability to connect references does not authorize contact.

Authorization resolves through R1-A.

Write capability != authority.

---

## 26. Human Gate

Where Human Gate applies, the Passageway Record preserves the approval
reference.

Approval != execution.

A Passageway MUST NOT invent Human Gate approval.

---

## 27. Provenance

Every Passageway preserves a traversable provenance route.

The route MUST preserve both:

- relationship provenance;
- independent object provenance.

Contact provenance MUST NOT overwrite object provenance.

---

## 28. History

Passageway establishment, blocking, or replacement MUST remain historical
evidence.

A later relationship state MUST NOT silently erase an earlier contact state.

History accumulates.

---

## 29. Occupation Boundary

R2-J does not define Occupation.

An ESTABLISHED Passageway means controlled analytical contact exists.

It does not mean:

- a capability occupies the source Room;
- a capability occupies the target Room;
- a capability traversed the Passageway;
- movement was executed.

Passageway established != Passageway traversed.

Contact != presence.

---

## 30. Movement Boundary

R2-J defines the cross-object contact contract.

It does not execute movement.

Need, mission, evidence, authority, Occupation, and later capability-movement
contracts govern execution.

Passageway availability != movement authorization.

---

## 31. R2-J Lock

An adjoining Room requires evidence of a genuinely distinct object.

Distinct objects preserve independent identity.

Distinct objects preserve independent Genesis lineage.

Distinct objects preserve independent Origin.

Distinct objects preserve independent boundary.

Distinct objects preserve independent geometry.

A Passageway may connect Rooms while preserving their independence.

Related does not mean identical.

Different perspective does not mean distinct object.

Only DISTINCT_OBJECT may support ESTABLISHED Passageway contact.

SAME_OBJECT does not create a Passageway.

UNRESOLVED does not establish a Passageway.

Passageway identity is not Room identity.

Shared provenance does not collapse identity.

Non-shared provenance is preserved.

Evidence of distinctness is preserved.

Passageway conditions are explicit.

Contamination controls are explicit.

Return route is explicit.

Cartography remains independent.

Stick continuity remains independent.

Cross-object contact != identity collapse.

Cross-object contact != Merge.

Passageway != Merge.

Passageway != Genesis.

Passageway established != Passageway traversed.

Passageway availability != movement authorization.

Contact != presence.

History accumulates.

RING 2 OPERATIONAL GEOGRAPHY: COMPLETE WHEN R2-A THROUGH R2-J PASS.
