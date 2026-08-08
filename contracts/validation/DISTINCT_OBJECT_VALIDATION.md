# R6-G — Distinct-Object Validation

Status: CONTROLLED CANDIDATE VALIDATION CONTRACT
Ring: R6-G
Tranche: 8 — Validation and Audit
Validation Family: DISTINCT_OBJECT
Validation Vector: DISTINCT_OBJECT_TEST
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

R6-G implements the native-v41 Distinct-Object Test.

Validation SHALL distinguish:

- viewpoint change on one Room;
- bounded representation change;
- Branch inside one Room;
- genuinely distinct analytical object.

A viewpoint change remains one Room.

A genuinely distinct object receives independent identity and controlled
Passageway semantics.

Perspective != object identity.

---

## 1. Determination States

Native distinct-object determination states remain exactly:

- `SAME_OBJECT`;
- `DISTINCT_OBJECT`;
- `UNRESOLVED`.

No additional classifier may be silently invented.

---

## 2. SAME_OBJECT

`SAME_OBJECT` applies when the evidence supports continuity of one canonical
analytical object.

The following do not independently create another Room:

- perspective change;
- Bounded Zone change;
- Bounded Space change;
- Authorized View change;
- stakeholder change;
- discipline change;
- rendering change;
- evidence exposure change;
- disagreement;
- Branch;
- historical State Root;
- Replay.

Same-object variation remains inside the existing Room.

---

## 3. DISTINCT_OBJECT

`DISTINCT_OBJECT` requires affirmative evidence of distinctness.

At minimum, the determination preserves:

- source object identity;
- target object identity;
- evidence of distinctness;
- relationship to source;
- shared provenance;
- non-shared provenance;
- independent boundary;
- independent Origin route where applicable;
- independent geometry or object structure;
- Passageway conditions;
- contamination controls;
- return route;
- independent Genesis reference.

A genuinely distinct object requires independent Genesis lineage.

---

## 4. UNRESOLVED

`UNRESOLVED` means the available evidence cannot yet establish sameness or
distinctness.

Unknown remains unknown.

UNRESOLVED MUST NOT be silently converted to DISTINCT_OBJECT merely because a
second-object model is convenient.

UNRESOLVED MUST NOT establish an ESTABLISHED Passageway.

---

## 5. Perspective Boundary

Perspective rotation does not establish distinctness.

Different perspective != distinct object.

Different interpretation != distinct object.

Different conclusion != distinct object.

Turn the object.

Do not clone the world.

---

## 6. Branch Boundary

A Branch remains alternate lineage within the same analytical object unless
affirmative distinct-object evidence establishes otherwise.

Branch != new Room.

Branch identity != object identity.

Branch divergence != proof of distinctness.

---

## 7. Genesis Boundary

Only a genuine `DISTINCT_OBJECT` result may require independent Genesis lineage.

SAME_OBJECT MUST NOT create a new Genesis solely because representation or
lineage changed.

UNRESOLVED MUST NOT create independent Genesis merely to simplify modeling.

Genesis follows distinctness.

Genesis does not manufacture distinctness.

---

## 8. Passageway Boundary

Only `DISTINCT_OBJECT` may support an `ESTABLISHED` Passageway.

`SAME_OBJECT` MUST NOT establish a Passageway between cloned Room identities.

`UNRESOLVED` MAY support:

- `PROPOSED`;
- `BLOCKED`.

`UNRESOLVED` MUST NOT support:

- `ESTABLISHED`.

Same object != Passageway.

Unresolved distinctness != established contact.

---

## 9. Independent Identity

For an established distinct-object relationship:

`source_object_id != target_object_id`

Relationship identity MUST NOT replace either object identity.

Passageway identity is not Room identity.

Relationship != identity.

---

## 10. Independent Origin / Boundary / Geometry

A genuinely distinct target object preserves its own:

- Origin route;
- boundary;
- geometry;
- provenance;
- Cartography;
- Stick continuity.

Shared provenance alone does not collapse identity.

Shared source material != same analytical object.

Non-shared provenance remains explicit.

---

## 11. Evidence of Distinctness

Distinctness must be evidence-supported.

Passageway convenience is not evidence of distinctness.

Rendering convenience is not evidence of distinctness.

Analytical disagreement is not evidence of distinctness by itself.

Implementation convenience is not evidence of distinctness.

---

## 12. Contamination Controls

Cross-object contact MUST preserve contamination controls.

Contact MUST NOT silently:

- copy unsupported state;
- inherit conclusions;
- promote assumptions;
- overwrite evidence boundaries;
- erase Origin distinctions;
- merge provenance;
- collapse identities.

Contact != identity collapse.

---

## 13. Return Route

Every established Passageway preserves a return route.

Cross-object contact MUST NOT strand analytical lineage.

Return route preserves source analytical recovery.

---

## 14. Cross-Object Comparison

Distinct Rooms may participate in:

- comparison;
- correlation;
- relationship analysis;
- combined rendering;
- Passageway analysis.

Cross-object comparison does not merge identity.

Cross-object contact != Merge.

Cross-object contact != new synthesized object.

---

## 15. Merge Boundary

Passageway != Merge.

Merge convenience is not evidence of sameness.

A genuinely new synthesized analytical object requires its own distinct-object
determination and independent Genesis.

---

## 16. Validation Record

Every R6-G validation record SHALL preserve:

- `validation_vector`;
- `source_object_id`;
- `candidate_target_object_id`;
- `perspective_changed`;
- `zone_changed`;
- `space_changed`;
- `authorized_view_changed`;
- `branch_present`;
- `evidence_of_distinctness`;
- `shared_provenance`;
- `non_shared_provenance`;
- `independent_origin_reference`;
- `independent_boundary_reference`;
- `independent_geometry_reference`;
- `independent_genesis_reference`;
- `relationship_to_source`;
- `passageway_conditions`;
- `contamination_controls`;
- `return_route`;
- `determination`;
- `passageway_state`;
- `new_object_created`;
- `provenance_route`;
- `authority_state`;
- `human_gate_state`;
- `validation_disposition`;
- `failure_reasons`.

---

## 17. Passageway States

R6-G preserves native Passageway states:

- `PROPOSED`;
- `ESTABLISHED`;
- `BLOCKED`.

`PROPOSED != ESTABLISHED`.

`BLOCKED != absent`.

---

## 18. Validation Disposition

R6-G defines:

- `VALID`;
- `BLOCKED`.

`VALID` means object classification and Passageway state are consistent with
the evidence.

`BLOCKED` means one or more distinct-object invariants failed.

VALID != truth ownership.

VALID != execution.

---

## 19. Failure Reasons

R6-G recognizes:

- `PERSPECTIVE_CLONED_AS_OBJECT`;
- `BRANCH_CLONED_AS_OBJECT`;
- `DISTINCTNESS_WITHOUT_EVIDENCE`;
- `DISTINCT_OBJECT_IDENTITY_COLLISION`;
- `INDEPENDENT_GENESIS_MISSING`;
- `INDEPENDENT_ORIGIN_MISSING`;
- `INDEPENDENT_BOUNDARY_MISSING`;
- `INDEPENDENT_GEOMETRY_MISSING`;
- `NON_SHARED_PROVENANCE_MISSING`;
- `PASSAGEWAY_ESTABLISHED_FOR_SAME_OBJECT`;
- `PASSAGEWAY_ESTABLISHED_WHILE_UNRESOLVED`;
- `PASSAGEWAY_EVIDENCE_MISSING`;
- `PASSAGEWAY_CONTROLS_MISSING`;
- `RETURN_ROUTE_MISSING`;
- `NEW_OBJECT_CREATED_WHILE_UNRESOLVED`;
- `AUTHORITY_PROMOTED`.

Failure reasons accumulate.

No Compression Out applies.

---

## 20. Positive Controls

R6-G SHALL validate:

1. perspective change -> SAME_OBJECT;
2. Zone / Space change -> SAME_OBJECT;
3. Authorized View change -> SAME_OBJECT;
4. Branch divergence -> SAME_OBJECT by default;
5. affirmative independent evidence -> DISTINCT_OBJECT;
6. DISTINCT_OBJECT + independent Genesis + controls -> ESTABLISHED Passageway;
7. UNRESOLVED -> PROPOSED or BLOCKED only.

---

## 21. Negative Controls

R6-G SHALL reject:

1. perspective difference promoted into new object identity;
2. Branch identity promoted into Room identity;
3. DISTINCT_OBJECT with no affirmative evidence;
4. DISTINCT_OBJECT where source and target IDs are identical;
5. distinct object with no independent Genesis;
6. SAME_OBJECT with ESTABLISHED Passageway;
7. UNRESOLVED with ESTABLISHED Passageway;
8. UNRESOLVED with new object creation;
9. Passageway without contamination controls;
10. Passageway without return route;
11. authority promotion.

---

## 22. No Object Multiplication by Disagreement

Multiple observers may disagree about one Room.

Disagreement does not establish distinctness.

A different conclusion remains evidence about the same Room until affirmative
distinct-object evidence establishes otherwise.

Disagreement != Room multiplication.

---

## 23. No Object Collapse by Relationship

Two genuinely distinct Rooms may share provenance or participate in one
relationship.

Relationship does not establish sameness.

Shared provenance does not collapse identity.

Related != identical.

Adjacency != identity.

Correlation != identity.

---

## 24. Authority Boundary

Distinct-object validation does not authorize:

- Genesis establishment;
- Passageway traversal;
- external movement;
- publication;
- Merge;
- canonical promotion.

Validation observes whether the required conditions are satisfied.

Authority remains NONE.

Human Gate remains ACTIVE.

---

## 25. R6-G Lock

R6-G = Distinct-Object Validation.

SAME_OBJECT / DISTINCT_OBJECT / UNRESOLVED remain the complete determination
vocabulary.

A viewpoint change remains one Room.

A genuinely distinct object requires affirmative evidence.

A genuinely distinct object requires independent Genesis lineage.

Perspective != object identity.

Different perspective != distinct object.

Different interpretation != distinct object.

Different conclusion != distinct object.

Branch != new Room.

Branch identity != object identity.

Branch divergence != proof of distinctness.

Genesis follows distinctness.

Genesis does not manufacture distinctness.

Only DISTINCT_OBJECT may support an ESTABLISHED Passageway.

Same object != Passageway.

Unresolved distinctness != established contact.

Passageway identity is not Room identity.

Relationship != identity.

Shared provenance does not collapse identity.

Shared source material != same analytical object.

Passageway convenience is not evidence of distinctness.

Contact != identity collapse.

Cross-object contact != Merge.

Passageway != Merge.

Disagreement does not establish distinctness.

Disagreement != Room multiplication.

Relationship does not establish sameness.

Related != identical.

Adjacency != identity.

Correlation != identity.

Authority remains NONE.

Human Gate remains ACTIVE.

R6-H owns Hydration-On-Need validation.
