# R3-F — Proportional Force / Qualification Scale

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R3-F
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R3-F defines proportional-force selection for qualification and bounded
capability missions.

R3-F consumes:

- complete Rings 1 and 2;
- R3-A through R3-E;
- unresolved signal characteristics;
- territory complexity;
- the active question;
- the bounded Capability Mission Request.

R3-F decides the smallest justified capability force.

R3-F does not yet define formation selection or formation integration.

---

## 1. Governing Law

Need determines force.

Question determines mission.

Evidence determines escalation.

Object identity determines continuity.

A capability request shall use the smallest justified force.

No fixed capability package is presumed.

---

## 2. Proportional Force

Proportional force is the smallest capability allocation justified by:

- unresolved signal;
- territory complexity;
- mission requirement;
- evidence boundary;
- evidence ceiling;
- reachable surfaces;
- uncertainty;
- restrictions;
- current Cartography;
- continuity requirements.

Force is selected to answer the question.

Force is not selected by habit.

---

## 3. Source Qualification Scale

Native v41 preserves the source qualification examples:

- faint, localized anomaly:
  one Goblin with binoculars — observe, confirm orientation, report back;
- split signal with several plausible sources:
  Goblin Signal or an Intel squad — correlate traces, separate sources, identify
  discriminating evidence;
- distributed `.333333/.666667` scar across systems or representations:
  Goblin Platoon — parallel reconnaissance, independent routes, consolidated
  explanation of why the signal will not resolve;
- small Room:
  one Goblin may qualify it;
- medium Room:
  a Goblin Team may qualify it;
- large or distributed Room:
  a Goblin Platoon may qualify it.

These are preserved source scaling vectors.

They are not permission to ignore current evidence.

---

## 4. Selection Record

Every Proportional Force Selection Record MUST preserve:

- `proportional_force_selection_id`;
- canonical `object_id`;
- Capability Mission Request reference;
- active question;
- unresolved signal profile;
- territory complexity;
- evidence boundary;
- evidence ceiling;
- current Cartography reference;
- current Stick reference;
- force-selection basis;
- selected scale;
- selected capability class;
- selected capability count or bounded allocation;
- alternatives considered;
- rejected larger-force alternatives;
- escalation conditions;
- de-escalation conditions;
- TOC reference;
- Governance reference;
- authorization reference;
- provenance route;
- selection time.

---

## 5. Selection Identity

Native-v41 `proportional_force_selection_id` is deterministic SHA-512 over the
complete declared selection except the ID itself.

A material change to signal profile, mission, evidence, selected capability, or
selection basis changes selection identity.

Proportional Force Selection identity is not Room Object identity.

Proportional Force Selection identity is not Capability Mission Request
identity.

---

## 6. Selection Scale

R3-F defines four native force scales:

- `SINGLE`;
- `SIGNAL_OR_INTEL`;
- `TEAM`;
- `PLATOON`.

These scales describe capability allocation.

They do not define analytical formation.

Scale != formation.

---

## 7. Selected Capability Class

The selected capability class MUST identify the actual bounded capability
requested.

Native source-recognized classes include:

- `GOBLIN`;
- `GOBLIN_SIGNAL`;
- `INTEL_SQUAD`;
- `GOBLIN_TEAM`;
- `GOBLIN_PLATOON`.

The class is selected from need.

Class != authority.

Class != truth ownership.

---

## 8. Faint Localized Signal

For a faint localized anomaly, one Goblin is the source baseline.

The mission is observation, orientation confirmation, and bounded return.

A larger force requires an explicit reason.

Faint signal != automatic Platoon.

---

## 9. Split Signal

For a split signal with several plausible sources, the source permits:

- Goblin Signal; or
- Intel squad.

The purpose is correlation, source separation, and identification of
discriminating evidence.

Split signal does not automatically justify a Platoon.

---

## 10. Distributed Recursive Scar

A distributed repeating `.333333/.666667` scar across systems or
representations is an unresolved contradiction / scar condition.

It is not confidence.

The source qualification scale permits a Goblin Platoon for parallel
reconnaissance, independent routes, and consolidated explanation of why the
signal will not resolve.

Scar != confidence.

Distributed unresolved scar may justify Platoon scale.

---

## 11. Room Complexity

Room complexity may independently justify scale:

- small Room → one Goblin may qualify;
- medium Room → Goblin Team may qualify;
- large or distributed Room → Goblin Platoon may qualify.

Room size does not override stronger evidence showing a smaller force is
sufficient.

Complexity informs force.

Complexity does not own force selection.

---

## 12. Smallest Justified Force

The selected force MUST be the smallest force that can reasonably satisfy the
bounded mission under current evidence.

If one capability can answer the question, a larger package requires an
explicit justification.

If a larger package is required, the Record MUST preserve why the smaller force
is insufficient.

Larger != better.

More capability != more truth.

---

## 13. Alternatives Considered

The Record preserves plausible smaller and larger alternatives.

A force selection without considered alternatives is insufficient when
multiple scales are viable.

Alternative considered != selected.

---

## 14. Rejected Larger-Force Alternatives

When a larger force is not justified, that rejection is preserved.

This prevents silent scale inflation.

No escalation by habit.

No Platoon because Platoon exists.

No Team because Team is convenient.

---

## 15. Escalation Conditions

Evidence determines escalation.

The selection records conditions that would justify a larger force.

Examples may include:

- signal distribution expands;
- independent routes appear;
- contradiction persists across representations;
- territory complexity increases;
- evidence discriminators require parallel collection;
- current capability return proves insufficient.

Escalation condition != automatic escalation.

---

## 16. De-escalation Conditions

The selection records conditions supporting a smaller force.

Examples may include:

- signal localizes;
- candidate sources collapse;
- one discriminating observation resolves the question;
- territory becomes simpler than initially represented.

De-escalation preserves economy of force.

---

## 17. Evidence Boundary and Ceiling

Force selection MUST remain inside the mission evidence boundary and ceiling.

More force does not increase evidence authority.

More observers do not raise the claim ceiling.

Capability count != evidence strength.

---

## 18. Cartography

Force selection may use Cartography to understand:

- reachable surfaces;
- distributed terrain;
- uncertainty frontiers;
- deformation;
- return routes.

Cartography informs force.

Cartography does not select force by itself.

---

## 19. Stick

Force selection preserves Stick continuity.

Scaling capability does not permit identity loss, provenance loss, transform
loss, evidence-lineage loss, or loss of return coordinates.

More capability MUST NOT weaken continuity.

---

## 20. TOC

TOC coordinates proportional capability selection.

TOC records the bounded operational selection.

TOC does not own truth.

TOC does not own policy.

TOC does not own object identity.

TOC coordination != analytical authority.

---

## 21. Governance

Governance preserves:

- movement constraints;
- evidence obligations;
- claim ceiling;
- prohibited assumptions;
- Human Gate requirements;
- authority boundaries.

TOC selection MUST remain inside Governance constraints.

Proportional force cannot override policy.

---

## 22. Authorization

Selection does not create execution authority.

Applicable authorization remains separately resolvable.

Selected != authorized to execute.

Write capability != authority.

---

## 23. Mission Binding

Every force selection resolves to one Capability Mission Request.

Question determines mission before force is selected.

R3-F MUST NOT rewrite the mission merely to justify a preferred force.

Force serves mission.

Mission does not serve force.

---

## 24. Occupancy Boundary

Force selection does not establish presence.

Selected capability != occupant.

Each actual occupant still requires the applicable Occupancy Witness.

Selection != entry.

---

## 25. Formation Boundary

R3-F does not select:

- Single-route analytical formation;
- Stack Analysis;
- Expanded Analysis;
- Swarm.

Those are formation semantics owned downstream by R3-G.

A selected Goblin Team is a capability scale.

It is not automatically Stack Analysis.

A Goblin Platoon is a capability scale.

It is not automatically Swarm.

Force scale != analytical formation.

---

## 26. Capability Return Boundary

A Capability Return may later show that the selected force was:

- sufficient;
- insufficient;
- excessive;
- blocked.

Return evidence may justify re-selection.

Return does not retroactively falsify the attributable basis of the earlier
selection.

Selection records what was justified then.

Return records what happened.

---

## 27. Re-Justification

Terrain contact, contradiction, evidence-ceiling change, or signal ecology may
require force re-justification.

Re-justification creates another attributable selection.

Re-justification does not change Room Object identity.

Re-selection != new Room.

---

## 28. No Fixed Package

Pups and K9 do not request a fixed package merely because a signal is strange.

Need determines force.

The correct response may be:

- one Goblin;
- Goblin Signal;
- Intel squad;
- Team;
- Platoon.

The smallest capability able to improve orientation or the next question is
preferred.

---

## 29. R3-F Lock

Need determines force.

Question determines mission.

Evidence determines escalation.

Object identity determines continuity.

A capability request shall use the smallest justified force.

No fixed capability package is presumed.

Force is selected to answer the question.

Force is not selected by habit.

Scale != formation.

Class != authority.

Class != truth ownership.

Faint signal != automatic Platoon.

Split signal does not automatically justify a Platoon.

Scar != confidence.

Distributed unresolved scar may justify Platoon scale.

Complexity informs force.

Complexity does not own force selection.

Larger != better.

More capability != more truth.

Alternative considered != selected.

No escalation by habit.

Escalation condition != automatic escalation.

More force does not increase evidence authority.

More observers do not raise the claim ceiling.

Capability count != evidence strength.

Cartography informs force.

Cartography does not select force by itself.

More capability MUST NOT weaken continuity.

TOC does not own truth.

TOC does not own policy.

TOC does not own object identity.

Proportional force cannot override policy.

Selected != authorized to execute.

Write capability != authority.

Force serves mission.

Mission does not serve force.

Selected capability != occupant.

Selection != entry.

A selected Goblin Team is a capability scale.

It is not automatically Stack Analysis.

A Goblin Platoon is a capability scale.

It is not automatically Swarm.

Force scale != analytical formation.

Selection records what was justified then.

Return records what happened.

Re-selection != new Room.

The smallest capability able to improve orientation or the next question is
preferred.

No formation selection yet.

No Goblin Signal propagation yet.

No ACTIVE lifecycle transition yet.
