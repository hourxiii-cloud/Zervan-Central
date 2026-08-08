# R6-F — Formation Re-Justification Validation

Status: CONTROLLED CANDIDATE VALIDATION CONTRACT
Ring: R6-F
Tranche: 8 — Validation and Audit
Validation Family: PERTURBATION
Validation Vector: FORMATION_REJUSTIFICATION
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

R6-F implements the native-v41 Formation Re-Justification validation vector.

Validation SHALL verify that:

- Single Route;
- Stack Analysis;
- Expanded Analysis;
- Swarm

may change after terrain contact while preserving the Stick.

Formation change != object change.

Re-justification != reconstruction.

---

## 1. Formation Vocabulary

Native formation types remain exactly:

- `SINGLE_ROUTE`;
- `STACK_ANALYSIS`;
- `EXPANDED_ANALYSIS`;
- `SWARM`.

Formation != Room identity.

Formation != capability scale.

---

## 2. Re-Justification Triggers

Formation may require re-justification when attributable conditions change.

Native trigger classes include:

- `TERRAIN_CONTACT_CHANGED`;
- `CONTRADICTION_APPEARED_OR_PERSISTED`;
- `EVIDENCE_CEILING_CHANGED`;
- `SIGNAL_ECOLOGY_CHANGED`;
- `ONE_ROUTE_BECAME_SUFFICIENT`.

A formation change without a declared trigger is invalid.

Change != whim.

---

## 3. Same Room

For this vector, formation changes occur against one canonical Room Object.

The `object_id` MUST remain unchanged.

Formation change MUST NOT create:

- new Room identity;
- new Origin merely because formation changed;
- branch merely because formation changed;
- Passageway merely because formation changed.

Formation change != new Room.

---

## 4. New Formation Record

A valid re-justification creates a new attributable Formation Selection Record.

The new record MUST preserve reference to the prior formation record.

New formation record != overwritten old record.

History accumulates.

Formation history remains replayable.

---

## 5. Prior History

The prior formation MUST remain explicitly resolvable.

A new selection MUST NOT:

- delete;
- replace;
- rewrite;
- silently normalize

the earlier selection.

A previously justified formation does not become invalid merely because later
evidence supports another formation.

Later change != retroactive falsification.

---

## 6. Stick Preservation

Formation changes MUST preserve the Stick.

R6-F validates preservation of:

- canonical object identity;
- Origin reference;
- Ingress reference;
- Cartography reference;
- provenance route;
- transform history;
- evidence lineage;
- source coordinates;
- target coordinates;
- return coordinates.

Formation change MUST NOT sever analytical continuity.

Stick continuity MUST remain `CONTINUOUS` for the pure valid control cases.

---

## 7. Single Route -> Stack

`SINGLE_ROUTE` may become `STACK_ANALYSIS` when independent capability routes
become justified.

The new evidence MUST explain why one route is no longer sufficient.

Single Route -> Stack != failure of the earlier Single Route selection.

New evidence may justify greater analytical breadth.

---

## 8. Stack -> Expanded

`STACK_ANALYSIS` may become `EXPANDED_ANALYSIS` when the unresolved question
requires activation of additional:

- Spaces;
- questions;
- evidence types;
- reachable surfaces.

More surface does not mean more Room.

Expanded Analysis MUST preserve one Room identity.

---

## 9. Expanded -> Swarm

`EXPANDED_ANALYSIS` may become `SWARM` when justified parallel capability
coordination is required.

Swarm remains evidence-driven.

Swarm is not the default advanced mode.

More capability available != Swarm required.

---

## 10. De-Escalation

Formation may simplify.

If one route becomes sufficient, a larger formation need not remain active.

A valid example is:

`STACK_ANALYSIS -> SINGLE_ROUTE`

when discriminating evidence localizes the unresolved question to one sufficient
route.

No formation persists merely because it was previously selected.

Historical formation != standing requirement.

---

## 11. Proportional-Force Basis

Every formation preserves its R3-F proportional-force basis.

Formation re-justification MUST NOT silently inflate capability force.

A formation change may require a separately attributable proportional-force
re-selection.

Formation Selection != force inflation.

Formation type change != automatic force-scale change.

---

## 12. Question Binding

Re-justification remains bound to the active question.

A formation MUST NOT be changed merely by rewriting the question to fit a
preferred operating arrangement.

Question change, when material, must remain attributable.

Formation serves the question.

Question does not serve the formation.

---

## 13. Evidence Boundary

Formation re-justification MUST preserve the evidence boundary unless a
separately governed attributable change exists.

Formation change != evidence-boundary expansion.

Additional capability != additional admissible evidence.

---

## 14. Evidence Ceiling

Formation change MUST NOT silently raise the evidence ceiling.

More observers != more authority.

Consensus != evidence elevation.

Formation breadth != claim strength.

If the evidence ceiling changes, that change itself must be an attributable
re-justification trigger.

---

## 15. Independent Findings

A change into Stack or Swarm MUST NOT erase independent findings.

Independent findings remain independently attributable before correlation.

Formation change != consensus creation.

Parallelism != agreement.

---

## 16. Continuity Failure

If Stick continuity becomes `BROKEN`, formation movement requiring continuity
fails closed.

BROKEN Stick MUST NOT be repaired by:

- inventing identity;
- inventing provenance;
- inventing coordinates;
- inventing evidence lineage;
- inventing Origin.

Broken contact is evidence.

---

## 17. Degraded Continuity

`DEGRADED` Stick remains explicitly degraded.

DEGRADED MUST NOT silently become CONTINUOUS.

A formation change requiring unavailable continuity evidence is BLOCKED unless
the governing operation explicitly permits the degraded state.

For R6-F positive controls, Stick remains CONTINUOUS.

---

## 18. Occupancy Boundary

Formation Selection does not manufacture occupants.

Formation change != entry.

Formation change != exit.

Formation re-justification does not mutate Occupancy Witness state.

---

## 19. Lifecycle Boundary

Formation change does not itself create lifecycle `ACTIVE`.

Formation selected != ACTIVE.

Formation re-justification != lifecycle mutation.

---

## 20. Hydration Boundary

Formation change may alter what verified territory is needed.

Formation change does not itself hydrate payload.

Formation != hydration authority.

---

## 21. Authority Boundary

Formation re-justification does not create:

- publication authority;
- execution authority;
- canonical promotion authority;
- truth ownership.

Authority remains NONE.

Human Gate remains ACTIVE.

---

## 22. Validation Record

Every R6-F validation record SHALL preserve:

- `validation_vector`;
- `object_id`;
- `previous_formation_id`;
- `previous_formation_type`;
- `new_formation_id`;
- `new_formation_type`;
- `rejustification_trigger`;
- `rejustification_basis`;
- `active_question`;
- `proportional_force_basis_reference`;
- `force_scale_changed`;
- `force_change_reference`;
- `evidence_boundary_reference`;
- `previous_evidence_ceiling_reference`;
- `new_evidence_ceiling_reference`;
- `evidence_ceiling_change_reference`;
- `stick_reference`;
- `stick_continuity_state`;
- `origin_reference`;
- `ingress_reference`;
- `cartography_reference`;
- `transform_history_references`;
- `evidence_lineage_references`;
- `provenance_route`;
- `source_coordinates`;
- `target_coordinates`;
- `return_coordinates`;
- `prior_history_preserved`;
- `new_room_created`;
- `branch_created`;
- `passageway_created`;
- `occupancy_mutated`;
- `lifecycle_mutated`;
- `authority_state`;
- `human_gate_state`;
- `validation_disposition`;
- `failure_reasons`.

---

## 23. Validation Disposition

R6-F defines:

- `VALID`;
- `BLOCKED`.

`VALID` means the formation change is attributable and preserves all required
continuity invariants.

`BLOCKED` means one or more formation-re-justification invariants failed.

VALID != executed.

VALID != authority.

---

## 24. Failure Reasons

R6-F recognizes:

- `REJUSTIFICATION_TRIGGER_MISSING`;
- `REJUSTIFICATION_BASIS_MISSING`;
- `OBJECT_IDENTITY_CHANGED`;
- `PRIOR_HISTORY_ERASED`;
- `STICK_NOT_PRESERVED`;
- `ORIGIN_CONTINUITY_LOST`;
- `INGRESS_CONTINUITY_LOST`;
- `CARTOGRAPHY_CONTINUITY_LOST`;
- `TRANSFORM_HISTORY_LOST`;
- `EVIDENCE_LINEAGE_LOST`;
- `PROVENANCE_LOST`;
- `RETURN_COORDINATES_LOST`;
- `FORCE_BASIS_LOST`;
- `SILENT_FORCE_INFLATION`;
- `EVIDENCE_CEILING_CHANGED_UNATTRIBUTED`;
- `NEW_ROOM_INVENTED`;
- `BRANCH_INVENTED`;
- `PASSAGEWAY_INVENTED`;
- `OCCUPANCY_MUTATED`;
- `LIFECYCLE_MUTATED`;
- `AUTHORITY_PROMOTED`.

Failure reasons accumulate.

No Compression Out applies.

---

## 25. Positive Controls

R6-F SHALL prove:

1. `SINGLE_ROUTE -> STACK_ANALYSIS`;
2. `STACK_ANALYSIS -> EXPANDED_ANALYSIS`;
3. `EXPANDED_ANALYSIS -> SWARM`;
4. `STACK_ANALYSIS -> SINGLE_ROUTE` de-escalation.

Each positive control preserves:

- one Room;
- prior history;
- Stick;
- provenance;
- evidence lineage;
- coordinates;
- proportional-force basis;
- authority NONE.

---

## 26. Negative Controls

R6-F SHALL reject:

1. formation change without trigger;
2. formation change without basis;
3. changed Room identity;
4. erased prior formation history;
5. broken Stick;
6. lost provenance;
7. lost return coordinates;
8. silent force inflation;
9. unattributed evidence-ceiling change;
10. invented Room / Branch / Passageway;
11. occupancy mutation;
12. lifecycle mutation;
13. authority promotion.

---

## 27. No Default Escalation

There is no preferred "advanced" formation.

`SWARM` is not intrinsically better than `SINGLE_ROUTE`.

`STACK_ANALYSIS` is not intrinsically better than `SINGLE_ROUTE`.

The correct formation is the smallest arrangement justified by the current
question and evidence.

Formation sophistication != analytical quality.

---

## 28. Re-Justification Is Not Reconstruction

The system does not rebuild the Room when the formation changes.

It changes the attributable operating arrangement around the same Room.

Re-justification != reconstruction.

Formation change != object change.

Return to a prior formation != replay of a different Room.

---

## 29. R6-F Lock

R6-F = Formation Re-Justification.

Formation change != object change.

Re-justification != reconstruction.

Formation != Room identity.

Formation != capability scale.

A formation change without a declared trigger is invalid.

Change != whim.

Formation change != new Room.

New formation record != overwritten old record.

History accumulates.

Formation history remains replayable.

Later change != retroactive falsification.

Formation changes MUST preserve the Stick.

Formation change MUST NOT sever analytical continuity.

Single Route -> Stack != failure of the earlier Single Route selection.

More surface does not mean more Room.

Swarm remains evidence-driven.

Swarm is not the default advanced mode.

More capability available != Swarm required.

No formation persists merely because it was previously selected.

Historical formation != standing requirement.

Formation Selection != force inflation.

Formation type change != automatic force-scale change.

Formation serves the question.

Question does not serve the formation.

Formation change != evidence-boundary expansion.

Additional capability != additional admissible evidence.

More observers != more authority.

Consensus != evidence elevation.

Formation breadth != claim strength.

Formation change != consensus creation.

Parallelism != agreement.

Broken contact is evidence.

DEGRADED MUST NOT silently become CONTINUOUS.

Formation change != entry.

Formation change != exit.

Formation selected != ACTIVE.

Formation re-justification != lifecycle mutation.

Formation != hydration authority.

Authority remains NONE.

Human Gate remains ACTIVE.

VALID != executed.

VALID != authority.

There is no preferred advanced formation.

Formation sophistication != analytical quality.

R6-G owns Distinct-Object validation.
