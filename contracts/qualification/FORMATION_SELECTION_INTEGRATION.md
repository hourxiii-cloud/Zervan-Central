# R3-G — Formation Selection / Integration

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R3-G
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R3-G defines native-v41 Formation Selection and Integration.

R3-G consumes:

- complete Rings 1 and 2;
- R3-A through R3-F;
- qualified Room identity;
- bounded capability missions;
- proportional-force selection;
- Occupancy Witnesses;
- representation coordinates;
- Stick continuity.

R3-G selects the analytical operating arrangement.

R3-G does not redefine capability scale.

R3-G does not create another Room Object.

---

## 1. Formation Doctrine

Room doctrine does not replace formation doctrine.

It makes the formation target explicit.

Formation operates against:

- one qualified Room Object; or
- in Swarm only, a declared family of genuinely distinct but related Rooms.

Formation != Room identity.

Formation != capability scale.

---

## 2. Native Formation Types

R3-G defines exactly four native formation types:

- `SINGLE_ROUTE`;
- `STACK_ANALYSIS`;
- `EXPANDED_ANALYSIS`;
- `SWARM`.

These preserve the source meanings:

- Single-route operation:
  one capability can answer the bounded question within the qualified Room.
- Stack Analysis:
  multiple capabilities operate against the same Room and compatible
  representation coordinates, preserving independent findings before
  correlation.
- Expanded Analysis:
  the Room remains one object while additional bounded Spaces, questions,
  evidence types, or reachable surfaces are activated.
- Swarm:
  parallel capabilities occupy coordinated surfaces of the same qualified Room
  or a declared family of genuinely distinct but related Rooms.

---

## 3. Formation Selection Record

Every Formation Selection Record MUST preserve:

- `formation_selection_id`;
- canonical `object_id`;
- formation type;
- Capability Mission Request references;
- Proportional Force Selection references;
- Occupancy Witness references;
- active question or questions;
- selected capability references;
- target Room references;
- Zone references;
- Space references;
- representation-coordinate references;
- evidence boundary;
- evidence ceiling;
- independent-finding policy;
- correlation policy;
- integration basis;
- re-justification triggers;
- Stick reference;
- TOC reference;
- Governance reference;
- authorization reference;
- provenance route;
- selection time.

---

## 4. Formation Identity

Native-v41 `formation_selection_id` is deterministic SHA-512 over the complete
Formation Selection Record except `formation_selection_id`.

Material change to formation type, mission set, capability set, Room target,
representation coordinates, or integration basis changes formation identity.

Formation Selection identity is not Room Object identity.

Formation Selection identity is not Proportional Force Selection identity.

---

## 5. Capability Scale Separation

R3-F selects proportional capability scale.

R3-G selects analytical formation.

A Goblin Team is not automatically Stack Analysis.

A Goblin Platoon is not automatically Swarm.

One Goblin may participate in Single-route operation.

Multiple individual capabilities may participate in Stack Analysis.

Capability organization != analytical formation.

---

## 6. Single-Route Operation

`SINGLE_ROUTE` means one capability can answer the bounded question within the
qualified Room.

Single-route requires:

- one canonical Room Object;
- one bounded mission route;
- one selected capability;
- one or more compatible occupied representations only as needed;
- preserved Stick continuity.

Single-route != weak analysis.

Single-route is correct when one route is sufficient.

No forced multiplication of capability.

---

## 7. Stack Analysis

`STACK_ANALYSIS` means multiple capabilities operate against the same Room and
compatible representation coordinates.

Independent findings MUST be preserved before correlation.

Stack does not permit false consensus.

Stack does not create multiple Rooms.

Stack does not erase disagreement.

Same Room.

Multiple bounded observations.

Correlation occurs after independent findings are preserved.

---

## 8. Expanded Analysis

`EXPANDED_ANALYSIS` keeps one Room Object while activating additional:

- bounded Spaces;
- questions;
- evidence types;
- reachable surfaces.

Expansion changes active analytical surface.

Expansion does not change Room identity.

Additional Space != additional Room.

Additional question != additional Room.

Additional evidence type != additional Room.

Additional reachable surface != additional Room.

---

## 9. Swarm

`SWARM` means parallel capabilities occupy coordinated surfaces.

Swarm may operate against:

- the same qualified Room Object; or
- a declared family of genuinely distinct but related Rooms.

When multiple Rooms are involved, each Room MUST retain:

- independent object identity;
- independent Origin route;
- independent boundary;
- independent geometry;
- independent provenance;
- controlled Passageway relationships where applicable.

Related != identical.

Swarm MUST NOT collapse distinct Rooms into one object.

Swarm MUST NOT clone one Room merely because perspectives differ.

---

## 10. Same-Room Stack Rule

Stack Analysis requires one canonical Room Object.

Every capability mission in a Stack MUST resolve to the same `object_id`.

Different perspective does not create another Room.

Different discipline does not create another Room.

Different stakeholder does not create another Room.

Disagreement does not create another Room.

---

## 11. Compatible Representation Coordinates

Stack capabilities operate against compatible representation coordinates.

Compatible does not require identical representation.

Compatibility means their coordinates can be reconciled against the same Room
Object without silent identity fracture.

Compatible != identical.

Representation transform != new Room.

---

## 12. Independent Findings

Multiple capabilities MUST preserve independent findings before correlation.

The system MUST NOT force agreement merely because capabilities share a
formation.

Independent observation remains attributable.

Disagreement is preserved as analytical geometry and evidence.

Independent findings != consensus.

Correlation != averaging away contradiction.

---

## 13. Correlation

Correlation may compare independent bounded findings after their provenance,
question, representation, evidence boundary, and capability identity remain
preserved.

Correlation does not retroactively erase independent returns.

Correlation != truth ownership.

Correlation != canonical mutation.

---

## 14. Expansion

Expanded Analysis activates more bounded analytical surface only when justified.

Expansion MUST preserve:

- object identity;
- Origin route;
- transform history;
- provenance;
- evidence lineage;
- return coordinates.

Expand the analysis.

Do not duplicate the Room.

---

## 15. Swarm Across One Room

A Swarm may coordinate parallel capability surfaces within one qualified Room.

Each occupant remains independently witnessed.

Each mission remains bounded.

Parallel operation does not create multiple Room identities.

Parallelism != cloning.

---

## 16. Swarm Across Distinct Rooms

A Swarm may operate across a declared family of genuinely distinct related
Rooms.

Each Room MUST already satisfy distinct-object requirements.

R3-G does not establish distinctness.

R3-G consumes established distinct-object identity and Passageway controls.

Formation cannot manufacture a family of Rooms.

---

## 17. Proportional Force Binding

Every formation must preserve its R3-F proportional-force basis.

Formation selection MUST NOT silently inflate force.

Formation may integrate already justified capability allocations.

Formation Selection != force inflation.

---

## 18. Mission Binding

Every participating capability remains bound to a Capability Mission Request.

Formation does not create unlimited movement permission.

Formation does not broaden a mission merely because capabilities cooperate.

Cooperation != scope expansion.

---

## 19. Occupancy Binding

Participating capabilities require attributable Occupancy Witnesses.

Selected formation != presence.

Formation Selection Record does not manufacture occupants.

Selection != occupation.

---

## 20. Evidence Boundary and Ceiling

Formation integration preserves evidence boundaries and ceilings.

Multiple capabilities do not raise the evidence ceiling merely by agreement.

More observers != more authority.

Consensus != evidence elevation.

---

## 21. Stick Preservation

Formation changes MUST preserve the Stick:

- object identity;
- Origin route;
- transform history;
- provenance;
- evidence lineage;
- return coordinates.

Formation change MUST NOT sever analytical continuity.

---

## 22. Re-Justification

Formation may require re-justification when:

- terrain contact changes;
- contradiction appears or persists;
- evidence ceiling changes;
- signal ecology changes.

Re-justification may change formation without changing Room Object identity.

Re-justification creates a new attributable Formation Selection Record.

Formation change != new Room.

---

## 23. Formation Change

A valid formation change preserves prior formation history.

The new formation does not overwrite the earlier selection.

History accumulates.

Formation history remains replayable.

---

## 24. Single Route to Stack

A Single-route operation may become Stack Analysis when independent capability
routes are justified.

This transition does not imply the earlier Single-route selection was invalid.

New evidence may justify greater analytical breadth.

---

## 25. Stack to Expanded

Stack Analysis may become Expanded Analysis when the unresolved question
requires activation of additional Spaces, questions, evidence types, or
reachable surfaces.

More surface does not mean more Room.

---

## 26. Expanded to Swarm

Expanded Analysis may become Swarm when justified parallel capability
coordination is required.

Swarm remains evidence-driven.

Swarm is not the default advanced mode.

---

## 27. De-escalation

Formation may also simplify.

If one route becomes sufficient, a larger formation need not remain active.

No formation persists merely because it was previously selected.

Need determines continued force and formation.

---

## 28. TOC

TOC coordinates:

- proportional capability selection;
- mission assignment;
- timing;
- bounded cooperation;
- formation integration.

TOC does not own truth.

TOC does not own policy.

TOC does not own Room identity.

TOC does not own canonical analytical state.

---

## 29. Governance

Governance preserves:

- entry and movement rules;
- evidence obligations;
- claim ceilings;
- prohibited assumptions;
- Human Gate requirements;
- publication constraints;
- promotion conditions.

Formation cannot override Governance.

Coordination != authority.

---

## 30. ACTIVE Boundary

A selected formation may later participate in lifecycle `ACTIVE`.

R3-G does not itself mutate lifecycle state to ACTIVE.

Formation selected != ACTIVE.

Formation operating evidence may support later lifecycle transition.

---

## 31. Goblin Signal Boundary

Goblin Signal may later announce:

- formation change;
- qualification change;
- occupancy change;
- capability return;
- adjoining-object signal.

R3-G does not propagate those events.

Formation Selection Record != Goblin Signal event.

---

## 32. Hydration Boundary

Formation may influence what verified territory is needed.

R3-G does not hydrate payload.

Formation != hydration authority.

Hydration remains downstream.

---

## 33. Publication Boundary

Formation does not alter publication semantics.

Room qualification and occupation remain upstream of:

Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate

Formation result != publication authority.

Formation result != decision authority.

---

## 34. R3-G Lock

Room doctrine does not replace formation doctrine.

It makes the formation target explicit.

Formation != Room identity.

Formation != capability scale.

A Goblin Team is not automatically Stack Analysis.

A Goblin Platoon is not automatically Swarm.

Capability organization != analytical formation.

Single-route is correct when one route is sufficient.

No forced multiplication of capability.

Independent findings MUST be preserved before correlation.

Stack does not permit false consensus.

Stack does not create multiple Rooms.

Stack does not erase disagreement.

Additional Space != additional Room.

Additional question != additional Room.

Additional evidence type != additional Room.

Additional reachable surface != additional Room.

Related != identical.

Swarm MUST NOT collapse distinct Rooms into one object.

Swarm MUST NOT clone one Room merely because perspectives differ.

Different perspective does not create another Room.

Different discipline does not create another Room.

Different stakeholder does not create another Room.

Disagreement does not create another Room.

Compatible != identical.

Representation transform != new Room.

Independent findings != consensus.

Correlation != averaging away contradiction.

Correlation != truth ownership.

Correlation != canonical mutation.

Expand the analysis.

Do not duplicate the Room.

Parallelism != cloning.

R3-G does not establish distinctness.

Formation cannot manufacture a family of Rooms.

Formation Selection != force inflation.

Cooperation != scope expansion.

Selected formation != presence.

Selection != occupation.

More observers != more authority.

Consensus != evidence elevation.

Formation changes MUST preserve the Stick.

Formation change MUST NOT sever analytical continuity.

Formation change != new Room.

History accumulates.

More surface does not mean more Room.

Swarm is not the default advanced mode.

No formation persists merely because it was previously selected.

TOC does not own truth.

TOC does not own policy.

TOC does not own Room identity.

Formation cannot override Governance.

Coordination != authority.

Formation selected != ACTIVE.

Formation Selection Record != Goblin Signal event.

Formation != hydration authority.

Formation result != publication authority.

Formation result != decision authority.

No Goblin Signal propagation yet.

No ACTIVE lifecycle transition yet.

No Hydration semantics yet.
