# R6-K — Orthogonal Transition Validation

Status: CONTROLLED CANDIDATE VALIDATION CONTRACT
Ring: R6-K
Tranche: 8 — Validation and Audit
Validation Family: ORTHOGONAL_TRANSITION
Validation Vector: ORTHOGONAL_TRANSITION
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

R6-K implements the native-v41 Orthogonal Transition validation vector.

Validation SHALL:

1. leave one Room;
2. occupy a genuinely different Room;
3. preserve distinct identity;
4. return to the first Room;
5. verify absence of contamination.

Orthogonal transition != perspective rotation.

Different Room != different view of same Room.

Return != reconstruction.

---

## 1. Transition Geometry

The canonical positive path is:

Room A
-> EXITED A
-> established Passageway A -> B
-> ENTERED B
-> PRESENT B
-> EXITED B
-> established return Passageway B -> A
-> ENTERED A

The final Room A identity MUST equal the original Room A identity.

The Room B identity MUST remain distinct from Room A throughout.

---

## 2. Distinct-Object Requirement

Orthogonal movement requires two genuinely distinct Canonical Room Objects.

The source and target MUST each preserve independent:

- `object_id`;
- Genesis lineage;
- Origin;
- boundary;
- Cartography;
- Stick;
- provenance.

`source_object_id != target_object_id`

Different perspective does not satisfy this requirement.

Different Zone does not satisfy this requirement.

Different Space does not satisfy this requirement.

Branch does not satisfy this requirement by itself.

---

## 3. Orthogonal != Perspective Rotation

Perspective rotation turns one Room.

Orthogonal transition changes occupied Room Object.

A perspective change MUST NOT be represented as orthogonal movement.

An orthogonal move MUST NOT be reduced to a Zone / Space transform inside one
Room.

Turn the object != leave the object.

---

## 4. Passageway

Cross-object movement requires an attributable ESTABLISHED Passageway.

The Passageway MUST preserve:

- source object;
- target object;
- DISTINCT_OBJECT determination;
- source and target Origin;
- source and target Cartography;
- source and target Stick;
- shared provenance;
- non-shared provenance;
- evidence of distinctness;
- passageway conditions;
- contamination controls;
- return route.

Passageway established != Passageway traversed.

R6-K validates traversal separately.

---

## 5. Directionality

A -> B does not silently authorize B -> A.

The outbound path and return path MUST each be permitted by declared Passageway
conditions.

Return directionality must be explicit.

Bidirectional technical connectivity != bidirectional movement authority.

---

## 6. Exit From Room A

Before Room B occupation is established for the bounded orthogonal transition,
the moving capability MUST preserve an attributable `EXITED` Occupancy Witness
for Room A.

EXITED ends bounded presence in Room A.

EXITED is not Landing.

EXITED does not destroy Room A.

EXITED does not delete Room A context.

Leave != destroy.

---

## 7. Enter Room B

Room B occupation requires a separate attributable `ENTERED` Occupancy Witness.

The Room B witness MUST bind:

- target Room B `object_id`;
- target readiness;
- target Qualification Record;
- target Zone;
- target Space;
- target Orientation;
- target Cartography;
- target Stick;
- target authorization;
- target evidence boundary;
- target evidence ceiling;
- target coordinates;
- provenance.

Entry into B MUST NOT reuse Room A identity.

---

## 8. Presence in Room B

`PRESENT` in Room B proves bounded presence in the genuinely different object.

Presence != truth.

Presence != authority.

Presence does not merge the Rooms.

Presence in B does not make B a representation of A.

---

## 9. Exit From Room B

Return to Room A requires an attributable `EXITED` witness from Room B.

Return MUST NOT be represented as simultaneous silent occupation change.

The B exit remains historical evidence.

History accumulates.

---

## 10. Return to Room A

Return to Room A requires a new attributable `ENTERED` witness against the
original Room A identity.

The returning Room A `object_id` MUST equal the pre-transition Room A
`object_id`.

Return != reconstruction.

Return != replacement object.

Return != new Genesis.

Return != snapshot Room.

---

## 11. Source Continuity

Return to Room A MUST preserve source continuity sufficient to resolve:

- Room A object identity;
- Room A Genesis lineage;
- Room A Origin;
- Room A Cartography;
- Room A Stick;
- Room A evidence boundary;
- Room A evidence ceiling;
- Room A return coordinates;
- Room A provenance context.

Leaving Room A does not make its identity disposable.

---

## 12. Target Continuity

Movement into and out of Room B MUST preserve:

- Room B object identity;
- Room B Genesis lineage;
- Room B Origin;
- Room B Cartography;
- Room B Stick;
- Room B evidence boundary;
- Room B evidence ceiling;
- Room B provenance context.

Return to A does not collapse or erase B.

---

## 13. Stick

Stick continuity remains independent on each side of the Passageway.

Room A preserves its Stick.

Room B preserves its Stick.

The Passageway does not replace Stick.

Stick != Passageway.

Cross-object movement MUST NOT create one fused continuity domain.

---

## 14. Cartography

Room A and Room B retain independent Cartography.

Outbound movement may reference both maps.

Return movement may reference both maps.

The maps MUST NOT silently merge.

Connected maps != merged reality.

---

## 15. Contamination

R6-K distinguishes contact from contamination.

Cross-object movement MUST NOT silently:

- copy unsupported state;
- inherit conclusions;
- promote assumptions;
- overwrite evidence boundaries;
- overwrite evidence ceilings;
- erase Origin distinctions;
- merge provenance;
- collapse identities.

Contact != contamination permission.

---

## 16. Allowed Shared Material

Distinct Rooms may legitimately share attributable provenance or explicitly
authorized evidence.

Shared provenance != contamination.

Shared provenance does not collapse identity.

R6-K contamination testing concerns unauthorized or unattributed transfer.

Authorized shared material MUST remain explicitly identified as shared.

---

## 17. Unauthorized Transfer

The validation record MUST preserve any unauthorized cross-object transfers.

A valid orthogonal transition requires:

`unauthorized_cross_object_transfers = []`

An unauthorized transfer blocks the vector.

No silent cleanup is permitted merely to produce PASS.

---

## 18. Evidence Boundary Independence

Room A and Room B preserve independent evidence boundaries.

Entering Room B MUST NOT broaden Room A's evidence boundary.

Returning to Room A MUST NOT silently import Room B's evidence boundary.

Cross-object access != inherited admissibility.

---

## 19. Evidence Ceiling Independence

Room A and Room B preserve independent evidence ceilings.

A stronger ceiling in one Room MUST NOT silently elevate the other.

Cross-object movement != claim-authority transfer.

Room B confidence != Room A claim authority.

---

## 20. Provenance Independence

Cross-object transition preserves:

- Room A provenance;
- Room B provenance;
- Passageway provenance;
- movement provenance.

Passageway provenance MUST NOT overwrite object provenance.

Movement provenance MUST NOT replace evidence provenance.

---

## 21. No Identity Collapse

At no point may:

`Room A == Room B`

The Passageway identity also MUST NOT substitute for either Room identity.

Relationship != identity.

Contact != identity collapse.

---

## 22. No Merge

Orthogonal transition is not Merge.

Returning to Room A does not merge B into A.

Leaving B does not merge A into B.

Passageway != Merge.

Cross-object contact != Merge.

---

## 23. No Synthesized Object

The A -> B -> A traversal MUST NOT silently produce a third synthesized Room.

A genuinely new synthesized object requires its own distinct-object
determination and independent Genesis.

Traversal != synthesis.

---

## 24. No Reconstruction

The return path MUST recover the original Room A identity and attributable
continuity.

The system MUST NOT create an approximate replacement Room because the
capability left.

Return != reconstruction.

Return != replay approximation.

Same Room returned to != similar Room recreated.

---

## 25. Occupancy Ordering

The bounded positive-control event order is:

1. `A:EXITED`;
2. `B:ENTERED`;
3. `B:PRESENT`;
4. `B:EXITED`;
5. `A:ENTERED`.

R6-K MUST reject illegal orderings that imply:

- B presence before B entry;
- return to A before B exit;
- silent Room replacement;
- missing source exit;
- missing target exit.

---

## 26. Occupancy Identity

Every Occupancy Witness remains bound to exactly one Room.

An A witness MUST reference Room A.

A B witness MUST reference Room B.

Occupancy Witness identity != Room Object identity.

Capability identity remains independent from both Room identities.

---

## 27. Authorization

Passageway availability does not authorize movement.

Technical ability to traverse != authorization to traverse.

Each governed movement must preserve applicable authorization references.

Approval != execution.

---

## 28. Human Gate

Where Human Gate applies, its references remain attributable.

R6-K does not fabricate approval.

R6-K does not create execution authority.

Authority remains NONE.

Human Gate remains ACTIVE.

---

## 29. Validation Record

Every R6-K validation record SHALL preserve:

- `validation_vector`;
- `source_object_id`;
- `target_object_id`;
- `returned_object_id`;
- `source_genesis_reference`;
- `target_genesis_reference`;
- `source_origin_reference`;
- `target_origin_reference`;
- `source_cartography_reference`;
- `target_cartography_reference`;
- `source_stick_reference`;
- `target_stick_reference`;
- `source_evidence_boundary_reference`;
- `target_evidence_boundary_reference`;
- `returned_source_evidence_boundary_reference`;
- `source_evidence_ceiling_reference`;
- `target_evidence_ceiling_reference`;
- `returned_source_evidence_ceiling_reference`;
- `outbound_passageway_state`;
- `return_passageway_state`;
- `outbound_direction_authorized`;
- `return_direction_authorized`;
- `occupancy_events`;
- `source_return_coordinate`;
- `returned_source_coordinate`;
- `shared_provenance`;
- `source_non_shared_provenance`;
- `target_non_shared_provenance`;
- `unauthorized_cross_object_transfers`;
- `source_contamination_detected`;
- `target_contamination_detected`;
- `merge_created`;
- `synthesized_object_created`;
- `reconstruction_used`;
- `provenance_route`;
- `authority_state`;
- `human_gate_state`;
- `validation_disposition`;
- `failure_reasons`.

---

## 30. Validation Disposition

R6-K defines:

- `VALID`;
- `BLOCKED`.

VALID means the capability completed the bounded A -> B -> A orthogonal
transition while preserving independent Room identity and contamination
controls.

BLOCKED means one or more orthogonal-transition invariants failed.

VALID != authority.

VALID != publication.

---

## 31. Failure Reasons

R6-K recognizes:

- `SOURCE_TARGET_IDENTITY_COLLISION`;
- `RETURNED_SOURCE_IDENTITY_CHANGED`;
- `SOURCE_GENESIS_MISSING`;
- `TARGET_GENESIS_MISSING`;
- `SOURCE_ORIGIN_MISSING`;
- `TARGET_ORIGIN_MISSING`;
- `SOURCE_CARTOGRAPHY_MISSING`;
- `TARGET_CARTOGRAPHY_MISSING`;
- `SOURCE_STICK_MISSING`;
- `TARGET_STICK_MISSING`;
- `OUTBOUND_PASSAGEWAY_NOT_ESTABLISHED`;
- `RETURN_PASSAGEWAY_NOT_ESTABLISHED`;
- `OUTBOUND_DIRECTION_UNAUTHORIZED`;
- `RETURN_DIRECTION_UNAUTHORIZED`;
- `OCCUPANCY_EVENT_ORDER_INVALID`;
- `OCCUPANCY_OBJECT_BINDING_INVALID`;
- `SOURCE_RETURN_COORDINATE_CHANGED`;
- `SOURCE_EVIDENCE_BOUNDARY_CONTAMINATED`;
- `SOURCE_EVIDENCE_CEILING_CONTAMINATED`;
- `UNAUTHORIZED_CROSS_OBJECT_TRANSFER`;
- `SOURCE_CONTAMINATION_DETECTED`;
- `TARGET_CONTAMINATION_DETECTED`;
- `MERGE_INVENTED`;
- `SYNTHESIZED_OBJECT_INVENTED`;
- `RECONSTRUCTION_USED`;
- `AUTHORITY_PROMOTED`.

Failure reasons accumulate.

No Compression Out applies.

---

## 32. Positive Control

R6-K SHALL prove:

Room A
-> EXITED
-> Passageway A -> B
-> Room B ENTERED
-> Room B PRESENT
-> Room B EXITED
-> Passageway B -> A
-> original Room A ENTERED

while preserving:

- A identity;
- B identity;
- independent Genesis;
- independent Origin;
- independent Cartography;
- independent Stick;
- independent evidence boundaries;
- independent evidence ceilings;
- provenance;
- return coordinate;
- contamination controls.

---

## 33. Negative Controls

R6-K SHALL reject:

1. source and target sharing one object identity;
2. return to a different source identity;
3. missing independent Genesis;
4. missing independent Origin;
5. missing Cartography;
6. missing Stick;
7. unestablished outbound Passageway;
8. unestablished return Passageway;
9. unauthorized direction;
10. invalid Occupancy order;
11. Occupancy Witness bound to wrong Room;
12. changed source return coordinate;
13. Room B boundary imported into Room A;
14. Room B ceiling imported into Room A;
15. unauthorized cross-object transfer;
16. contamination detected on either side;
17. Merge creation;
18. synthesized-object creation;
19. reconstruction;
20. authority promotion.

---

## 34. R6-K Lock

R6-K = Orthogonal Transition.

Leave one Room.

Occupy a genuinely different Room.

Preserve distinct identity.

Return to the first Room.

Verify absence of contamination.

Orthogonal transition != perspective rotation.

Different Room != different view of same Room.

Return != reconstruction.

source_object_id != target_object_id.

Different perspective does not satisfy orthogonal movement.

Different Zone does not satisfy orthogonal movement.

Different Space does not satisfy orthogonal movement.

Branch does not satisfy orthogonal movement by itself.

Passageway established != Passageway traversed.

A -> B does not silently authorize B -> A.

EXITED does not destroy Room A.

Leave != destroy.

Entry into B MUST NOT reuse Room A identity.

Presence does not merge the Rooms.

History accumulates.

The returning Room A object_id MUST equal the pre-transition Room A object_id.

Return != replacement object.

Return != new Genesis.

Room A preserves its Stick.

Room B preserves its Stick.

Stick != Passageway.

Connected maps != merged reality.

Contact != contamination permission.

Shared provenance != contamination.

Cross-object access != inherited admissibility.

Cross-object movement != claim-authority transfer.

Passageway provenance MUST NOT overwrite object provenance.

Relationship != identity.

Contact != identity collapse.

Orthogonal transition is not Merge.

Passageway != Merge.

Traversal != synthesis.

Same Room returned to != similar Room recreated.

Occupancy Witness identity != Room Object identity.

Passageway availability does not authorize movement.

Technical ability to traverse != authorization to traverse.

Approval != execution.

Authority remains NONE.

Human Gate remains ACTIVE.

R6-L owns RBT-001 validation.
