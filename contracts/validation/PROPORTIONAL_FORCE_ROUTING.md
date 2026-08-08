# R6-D — Proportional-Force Routing Validation

Status: CONTROLLED CANDIDATE VALIDATION CONTRACT
Ring: R6-D
Tranche: 8 — Validation and Audit
Validation Family: PERTURBATION
Validation Vector: PROPORTIONAL_FORCE_ROUTING
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

R6-D implements the native-v41 Proportional-Force Routing validation vector.

Need determines force.

Question determines mission.

Evidence determines escalation.

Object identity determines continuity.

A capability request shall use the smallest justified force.

No fixed capability package is presumed.

---

## 1. Validation Target

R6-D validates proportional-force selection against bounded signal and mission
conditions.

R6-D verifies:

- faint localized anomaly -> smallest justified force;
- split signal -> bounded signal/intel force;
- distributed recursive scar -> justified Platoon case;
- larger force requires explicit justification;
- de-escalation remains valid;
- force scale does not become analytical formation;
- force does not create authority.

R6-D validates selection logic.

R6-D does not execute capability missions.

---

## 2. Native Force Scales

Native scales remain:

- `SINGLE`;
- `SIGNAL_OR_INTEL`;
- `TEAM`;
- `PLATOON`.

Scale describes capability allocation.

Scale != formation.

---

## 3. Native Capability Classes

Native source-recognized classes include:

- `GOBLIN`;
- `GOBLIN_SIGNAL`;
- `INTEL_SQUAD`;
- `GOBLIN_TEAM`;
- `GOBLIN_PLATOON`.

Class != authority.

Class != truth ownership.

---

## 4. Faint Localized Signal

For a faint localized anomaly, the source baseline is:

- scale: `SINGLE`;
- capability: `GOBLIN`.

The mission is:

- observe;
- confirm orientation;
- report back.

A larger force requires explicit evidence-bounded justification.

Faint signal != automatic Team.

Faint signal != automatic Platoon.

---

## 5. Split Signal

For a split signal with several plausible sources, the source permits:

- scale: `SIGNAL_OR_INTEL`;
- capability:
  - `GOBLIN_SIGNAL`; or
  - `INTEL_SQUAD`.

Purpose:

- correlate traces;
- separate sources;
- identify discriminating evidence.

Split signal does not automatically justify Team.

Split signal does not automatically justify Platoon.

---

## 6. Distributed Recursive Scar

A distributed repeating `.333333/.666667` scar across systems or
representations is an unresolved contradiction / scar condition.

Scar != confidence.

The source permits:

- scale: `PLATOON`;
- capability: `GOBLIN_PLATOON`;

when parallel reconnaissance, independent routes, and consolidated explanation
are justified.

Distributed unresolved scar may justify Platoon scale.

May justify != always requires.

---

## 7. Room Complexity

Room complexity may independently influence scale.

Source examples remain:

- small Room -> one Goblin may qualify;
- medium Room -> Goblin Team may qualify;
- large / distributed Room -> Goblin Platoon may qualify.

Complexity informs force.

Complexity does not own force selection.

Room size MUST NOT override stronger evidence that a smaller force is sufficient.

---

## 8. Smallest Justified Force

The selected force MUST be the smallest force able to satisfy the bounded
mission under current evidence.

If one Goblin can answer the question, a Team or Platoon is invalid unless an
explicit justification explains why the smaller force is insufficient.

Larger != better.

More capability != more truth.

No escalation by habit.

---

## 9. Question Binding

The active question MUST be preserved.

Force selection MUST NOT rewrite the question merely to justify a preferred
scale.

Question determines mission.

Force serves mission.

Mission does not serve force.

---

## 10. Evidence Binding

Force selection MUST remain inside:

- evidence boundary;
- evidence ceiling.

More force does not increase evidence authority.

More observers do not raise the claim ceiling.

Capability count != evidence strength.

---

## 11. Escalation

Evidence determines escalation.

A larger force may be justified when attributable conditions arise, including:

- signal distribution expands;
- independent routes appear;
- contradiction persists across representations;
- territory complexity increases;
- discriminating evidence requires parallel collection;
- current capability return proves insufficient.

Escalation condition != automatic escalation.

---

## 12. De-Escalation

A smaller force may become correct when:

- signal localizes;
- candidate sources collapse;
- one discriminating observation resolves the question;
- territory becomes simpler than initially represented.

De-escalation is valid.

No selected force persists merely because it was selected earlier.

Historical force != standing force.

---

## 13. Alternatives

A proportional-force decision SHALL preserve:

- alternatives considered;
- rejected larger-force alternatives;
- rejected smaller-force alternatives where insufficient.

Alternative considered != selected.

Rejected larger force remains attributable.

This prevents silent scale inflation.

---

## 14. Force / Formation Separation

R6-D MUST preserve the R3-F / R3-G separation.

A `GOBLIN_TEAM` capability selection does not imply `STACK_ANALYSIS`.

A `GOBLIN_PLATOON` capability selection does not imply `SWARM`.

Capability organization != analytical formation.

Formation Selection != force inflation.

Scale != formation.

---

## 15. Occupancy Boundary

Selected capability != occupant.

Selection != entry.

Selection does not create Occupancy Witness.

Force routing != presence.

---

## 16. Lifecycle Boundary

Force selection does not create lifecycle `ACTIVE`.

Selected force != ACTIVE.

Capability allocation != lifecycle mutation.

---

## 17. Hydration Boundary

Force scale does not itself hydrate payload.

More force != more hydration authority.

Payload availability remains separately governed.

---

## 18. Governance Boundary

Proportional force cannot override:

- evidence obligations;
- movement constraints;
- claim ceiling;
- prohibited assumptions;
- Human Gate requirements.

TOC coordination != Governance.

Force selection != policy ownership.

---

## 19. Authority Boundary

Selected != authorized to execute.

Force selection does not create:

- execution authority;
- publication authority;
- system population authority;
- canonical promotion.

Authority remains NONE.

Human Gate remains ACTIVE.

---

## 20. Validation Cases

R6-D SHALL include at minimum:

1. faint localized signal -> SINGLE / GOBLIN;
2. split signal -> SIGNAL_OR_INTEL / GOBLIN_SIGNAL;
3. split signal -> SIGNAL_OR_INTEL / INTEL_SQUAD;
4. distributed recursive scar -> PLATOON / GOBLIN_PLATOON;
5. small Room with localized signal -> SINGLE;
6. medium Room where parallel work is justified -> TEAM;
7. large distributed Room -> PLATOON;
8. oversized selection without justification -> REJECTED;
9. scale escalation without evidence -> REJECTED;
10. de-escalation after localization -> VALID;
11. capability scale represented as formation -> REJECTED;
12. authority-bearing selection -> REJECTED.

---

## 21. Selection Record

Every R6-D validation record SHALL preserve:

- `validation_vector`;
- `object_id`;
- `active_question`;
- `signal_profile`;
- `territory_complexity`;
- `evidence_boundary_reference`;
- `evidence_ceiling_reference`;
- `selected_scale`;
- `selected_capability_class`;
- `selected_capability_count`;
- `selection_basis`;
- `alternatives_considered`;
- `rejected_larger_force_alternatives`;
- `rejected_smaller_force_alternatives`;
- `escalation_conditions`;
- `deescalation_conditions`;
- `formation_reference`;
- `occupancy_created`;
- `active_lifecycle_created`;
- `execution_authorized`;
- `validation_disposition`;
- `failure_reasons`;
- `provenance_route`;
- `authority_state`;
- `human_gate_state`.

---

## 22. Signal Profiles

R6-D defines these validation profiles:

- `FAINT_LOCALIZED`;
- `SPLIT_PLAUSIBLE_SOURCES`;
- `DISTRIBUTED_RECURSIVE_SCAR`;
- `LOCALIZED_RESOLVED`;
- `CUSTOM_BOUNDED`.

These are test-vector labels.

They do not replace Signal Ecology doctrine.

---

## 23. Territory Complexity

R6-D defines validation complexity labels:

- `SMALL`;
- `MEDIUM`;
- `LARGE_DISTRIBUTED`.

These labels support the test vector.

They do not redefine Cartography.

---

## 24. Selection Disposition

R6-D defines:

- `VALID`;
- `REJECTED`.

`VALID` means the selected force is proportionate to the declared vector.

`REJECTED` means the force selection violates one or more proportional-force
invariants.

REJECTED MUST preserve failure reasons.

VALID != authorized.

VALID != executed.

---

## 25. Failure Reasons

R6-D recognizes:

- `OVERSIZED_FORCE_WITHOUT_JUSTIFICATION`;
- `UNDERSIZED_FORCE_FOR_DECLARED_MISSION`;
- `ESCALATION_WITHOUT_EVIDENCE`;
- `QUESTION_REWRITTEN_FOR_FORCE`;
- `EVIDENCE_BOUNDARY_EXCEEDED`;
- `EVIDENCE_CEILING_PROMOTED`;
- `FORCE_FORMATION_COLLAPSE`;
- `OCCUPANCY_INVENTED`;
- `ACTIVE_STATE_INVENTED`;
- `EXECUTION_AUTHORITY_INVENTED`;
- `AUTHORITY_PROMOTED`.

Failure reasons accumulate.

No Compression Out applies.

---

## 26. Expected Baseline Mapping

For source-baseline test vectors:

- `FAINT_LOCALIZED` -> `SINGLE`;
- `SPLIT_PLAUSIBLE_SOURCES` -> `SIGNAL_OR_INTEL`;
- `DISTRIBUTED_RECURSIVE_SCAR` -> `PLATOON`.

`CUSTOM_BOUNDED` requires explicit selection basis.

`LOCALIZED_RESOLVED` may support de-escalation.

Baseline mapping != universal fixed package.

Current evidence remains controlling.

---

## 27. Positive / Negative Control

R6-D SHALL prove both:

- valid proportional selection;
- invalid scale inflation.

The validator MUST reject a Platoon for a faint localized signal when the record
contains no explicit evidence-bounded reason why smaller force is insufficient.

The validator MUST reject a force increase caused only by capability
availability.

More available capability != more required capability.

---

## 28. Continuity

Force selection MUST preserve canonical Room Object identity.

Re-selection does not create another Room.

Re-selection != new Room.

Object identity determines continuity.

---

## 29. R6-D Lock

R6-D = Proportional-Force Routing.

Need determines force.

Question determines mission.

Evidence determines escalation.

Object identity determines continuity.

A capability request shall use the smallest justified force.

No fixed capability package is presumed.

Scale != formation.

Class != authority.

Class != truth ownership.

Faint signal != automatic Team.

Faint signal != automatic Platoon.

Split signal does not automatically justify Team.

Split signal does not automatically justify Platoon.

Scar != confidence.

Distributed unresolved scar may justify Platoon scale.

May justify != always requires.

Complexity informs force.

Complexity does not own force selection.

Larger != better.

More capability != more truth.

No escalation by habit.

Force serves mission.

Mission does not serve force.

More force does not increase evidence authority.

More observers do not raise the claim ceiling.

Capability count != evidence strength.

Escalation condition != automatic escalation.

De-escalation is valid.

Historical force != standing force.

Alternative considered != selected.

Capability organization != analytical formation.

Formation Selection != force inflation.

Selected capability != occupant.

Selection != entry.

Selected force != ACTIVE.

Capability allocation != lifecycle mutation.

More force != more hydration authority.

Force selection != policy ownership.

Selected != authorized to execute.

Authority remains NONE.

Human Gate remains ACTIVE.

VALID != authorized.

VALID != executed.

Baseline mapping != universal fixed package.

More available capability != more required capability.

Re-selection != new Room.

R6-E owns Qualification-Team Coherence validation.
