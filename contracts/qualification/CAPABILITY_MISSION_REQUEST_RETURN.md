# R3-E — Capability Mission Request / Return

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R3-E
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R3-E defines native-v41 Capability Mission Request and Capability Return
contracts.

R3-E consumes:

- complete Rings 1 and 2;
- R3-A through R3-D;
- a qualified and READY Room;
- attributable bounded capability presence.

R3-E binds why an occupying capability may act, the bounded mission it may
perform, and what it must return.

R3-E does not yet select proportional force or formation.

---

## 1. Capability Movement Law

Need determines force.

Question determines mission.

Evidence determines escalation.

Object identity determines continuity.

Mission establishes movement.

Movement remains bounded by Governance, representation, evidence, continuity,
and authorization constraints.

---

## 2. Request / Selection Separation

A Capability Mission Request declares the mission requirement.

It does not itself select proportional force.

It does not itself select formation.

Mission Request != Proportional Force Selection.

Mission Request != Formation Selection Record.

R3-F owns proportional-force determination.

R3-G owns formation selection and integration.

---

## 3. Capability Mission Request

Every Capability Mission Request MUST preserve:

- `capability_mission_request_id`;
- canonical `object_id`;
- Occupancy Witness reference;
- requesting question;
- mission objective;
- mission justification;
- target Zone;
- target Space;
- Orientation reference;
- Cartography reference;
- Stick reference;
- Territory reference;
- permitted movement;
- permitted actions;
- prohibited actions;
- evidence boundary;
- evidence ceiling;
- evidence obligations;
- expected return obligations;
- completion conditions;
- Governance reference;
- TOC coordination reference;
- authorization reference;
- Human Gate reference when applicable;
- provenance route;
- request time.

The request establishes a bounded mission.

It does not establish mission success.

---

## 4. Mission Request Identity

Native-v41 `capability_mission_request_id` is deterministic SHA-512 over the
complete declared Capability Mission Request except the ID itself.

A material change to mission, question, representation, evidence boundary,
movement envelope, or obligations changes mission request identity.

Capability Mission Request identity is not Room Object identity.

Capability Mission Request identity is not Occupancy Witness identity.

---

## 5. Occupancy Dependency

Capability Mission Request requires attributable bounded presence.

The mission request preserves the Occupancy Witness reference.

Presence precedes mission execution.

Presence != mission.

Mission Request != Occupancy Witness.

A capability MUST NOT silently execute a mission merely because it is present.

---

## 6. Active Question

Question determines mission.

Every mission MUST remain attributable to a bounded question.

The mission may seek to:

- improve object definition;
- improve transform definition;
- improve Cartography;
- improve the next question;
- identify evidence requirements;
- test bounded terrain;
- return discriminating evidence.

Question != force selection.

Question != authority.

---

## 7. Mission Objective

The mission objective states what the capability is being asked to accomplish.

Mission objective MUST be bounded.

The objective MUST NOT silently broaden beyond the active question.

Mission objective != conclusion.

Mission objective != result.

---

## 8. Mission Justification

Every mission request preserves why the mission is necessary.

Mission justification describes unresolved analytical need.

Need does not itself choose force in R3-E.

Need is carried forward for R3-F proportional-force routing.

---

## 9. Representation Binding

The mission request preserves:

- target Zone;
- target Space;
- Orientation;
- Cartography;
- Territory;
- Stick.

The mission occurs against the same canonical Room Object.

Mission movement MUST NOT create a private copy of informational reality.

Turn or move within declared representation.

Do not clone the Room.

---

## 10. Movement Boundary

Mission establishes movement.

`permitted_movement` declares the movement envelope permitted by the mission.

It does not assert that movement occurred.

Permitted movement != executed movement.

Capability movement MUST remain within permitted Territory, Zone, Space,
Orientation, Governance constraints, and Stick continuity.

---

## 11. Permitted Actions

The request explicitly records actions permitted for the bounded mission.

Permission is mission-specific.

Capability availability != permission.

Technical capability != mission permission.

---

## 12. Prohibited Actions

The request explicitly records prohibited actions.

Reconnaissance does not automatically authorize:

- Room entry beyond the already witnessed occupation;
- object mutation;
- perspective promotion;
- analytical promotion;
- canonical mutation;
- publication;
- external execution.

Prohibited action MUST remain prohibited unless separately governed.

---

## 13. Evidence Boundary

The mission preserves the applicable evidence boundary.

Movement does not broaden evidence access.

Mission does not silently make excluded evidence admissible.

Excluded != absent.

---

## 14. Evidence Ceiling

The mission preserves the evidence ceiling.

Evidence determines escalation.

Mission execution MUST NOT silently raise that ceiling.

Capability confidence != evidence authority.

---

## 15. Evidence Obligations

The mission records evidence obligations required during capability operation.

These may include:

- provenance preservation;
- discriminating evidence capture;
- unresolved-condition preservation;
- restriction preservation;
- return-coordinate preservation;
- Cartographic effect preservation.

Obligation != satisfaction.

---

## 16. Expected Return Obligations

Every mission declares what the capability must return.

At minimum the return must remain capable of carrying:

- bounded findings;
- evidence references;
- observed effects;
- unresolved signals;
- discriminating evidence needs;
- Cartographic change references;
- restriction findings;
- continuity state;
- return coordinates;
- provenance.

Mission Request defines expected return.

Capability Return records actual return.

---

## 17. Completion Conditions

The mission records bounded completion conditions.

Completion condition defines when the requested work may stop.

Completion condition != analytical convergence by default.

Completion condition != publication.

Completion condition != decision.

---

## 18. Governance

Governance directs permitted movement, representation change, policy, authority
boundaries, evidence obligations, Human Gate requirements, prohibited action,
and promotion requirements.

The mission request preserves the governing reference.

Governance != mission executor.

---

## 19. TOC

TOC coordinates capability movement, mission allocation, proportional scale,
landing, reflight, transform timing, and bounded cooperation.

R3-E preserves a TOC coordination reference.

TOC != truth owner.

TOC != canonical state owner.

TOC != object identity owner.

TOC != policy owner.

---

## 20. Authorization

Mission request does not create authority.

Applicable authorization must remain resolvable.

Mission Request != authorization invention.

Write capability != authority.

Authorization != execution.

---

## 21. Human Gate

Where Human Gate applies, the mission preserves its reference.

Human Gate approval MUST NOT be fabricated.

Human Gate decision != mission execution.

---

## 22. Capability Return

Every Capability Return MUST preserve:

- `capability_return_id`;
- Capability Mission Request reference;
- canonical `object_id`;
- Occupancy Witness reference;
- returning capability;
- bounded findings;
- evidence references;
- observed effects;
- unresolved signals;
- discriminating evidence needs;
- Cartographic change references;
- restriction findings;
- continuity state;
- Stick reference;
- final coordinates;
- return coordinates;
- completion assessment;
- provenance route;
- return time.

Capability Return records what came back.

It does not silently turn findings into canonical truth.

---

## 23. Capability Return Identity

Native-v41 `capability_return_id` is deterministic SHA-512 over the complete
Capability Return except `capability_return_id`.

A material change to findings, evidence, observed effects, unresolved signals,
coordinates, or completion assessment changes Return identity.

Capability Return identity is not Room Object identity.

Capability Return identity is not Capability Mission Request identity.

---

## 24. Bounded Findings

Goblin / Team / Platoon capabilities return bounded findings.

Findings MUST remain attributable to the mission, evidence boundary, evidence
ceiling, representation, capability, and provenance route.

Bounded finding != canonical truth.

Finding != publication.

Finding != decision.

---

## 25. Evidence Return

Capability Return may carry evidence references.

Returned evidence remains subject to provenance, integrity, evidence boundary,
and evidence ceiling.

Returned evidence != automatically promoted evidence.

Material evidence may later create a legitimate reflight trigger.

R3-E does not execute reflight.

---

## 26. Observed Effects

Capability Return preserves observed effects on the Room representation and
analytical geometry.

Observed effect MUST remain attributable.

Observed effect != automatic canonical mutation.

Cartography may later preserve accepted geometry changes.

Return != Cartography.

---

## 27. Unresolved Signals

Capability Return MUST preserve unresolved signals.

Unresolved does not mean failed.

Unresolved does not mean confidence.

Unknown remains unknown.

Repeating `.333333/.666667` scar conditions remain error / unresolved
contradiction signals, not confidence values.

---

## 28. Discriminating Evidence Needs

A capability may return the evidence required to distinguish unresolved
possibilities.

Discriminating evidence need != evidence itself.

The next mission may be driven by that need.

R3-E does not automatically launch another mission.

---

## 29. Restriction Findings

Capability Return preserves restrictions encountered during the mission.

Restricted != absent.

Inaccessible != nonexistent.

Mission return MUST NOT erase surfaces it could not access.

---

## 30. Continuity

Object identity determines continuity.

Mission and return preserve Stick continuity.

Return MUST retain resolvable routes to:

- Room Object;
- Origin;
- representation;
- evidence lineage;
- final coordinates;
- return coordinates.

Movement MUST NOT sever analytical contact.

---

## 31. Completion Assessment

Capability Return records whether the bounded mission completion conditions were
met.

Native R3-E uses:

- `COMPLETED`;
- `PARTIAL`;
- `BLOCKED`.

`COMPLETED` means the bounded mission conditions were met.

`PARTIAL` means useful bounded work returned but mission conditions were not
fully met.

`BLOCKED` means the mission could not proceed sufficiently under its current
constraints.

COMPLETED != analytical truth.

PARTIAL != failure.

BLOCKED != nonexistent.

---

## 32. Return and Occupation

A capability may return findings without automatically terminating occupation.

Capability Return != Occupancy EXITED witness.

Return != exit.

Landing may later cease movement while preserving occupation.

R3-E does not define Landing.

---

## 33. Return and Goblin Signal

Goblin Signal later carries capability-return notifications.

R3-E produces the attributable Return that may be announced.

Capability Return != Goblin Signal event.

Return != propagation.

---

## 34. Proportional Force Boundary

A capability request shall use the smallest justified force.

R3-E preserves the unresolved need and mission requirement.

R3-F determines proportional force.

R3-E MUST NOT hard-code:

- one Goblin;
- Team;
- Intel squad;
- Platoon;
- Stack;
- Expanded Analysis;
- Swarm

as the automatically selected force or formation.

Need determines force downstream.

---

## 35. Formation Boundary

R3-E does not select formation.

Formation Selection Record remains downstream.

Mission Request != formation.

Capability Return != formation.

Multiple capability returns do not by themselves establish a formation.

---

## 36. Lifecycle ACTIVE Boundary

R3-E may provide evidence that an occupying capability is operating within a
declared Zone and Space.

R3-E does not itself mutate lifecycle state to ACTIVE.

Mission execution evidence may support a later ACTIVE transition.

Capability Mission Request != ACTIVE.

Capability Return != ACTIVE transition.

---

## 37. Publication / Decision Boundary

Capability Mission Request and Capability Return remain upstream of:

- PMC;
- CCR;
- MC;
- Raven;
- Human Gate publication;
- decision support;
- external execution.

Mission result != publication.

Mission result != decision authority.

---

## 38. R3-E Lock

Need determines force.

Question determines mission.

Evidence determines escalation.

Object identity determines continuity.

Mission establishes movement.

Capability Mission Request declares the mission requirement.

Mission Request != Proportional Force Selection.

Mission Request != Formation Selection Record.

Presence precedes mission execution.

Presence != mission.

Mission Request != Occupancy Witness.

Question != force selection.

Question != authority.

Mission objective != conclusion.

Mission objective != result.

Permitted movement != executed movement.

Capability availability != permission.

Technical capability != mission permission.

Movement does not broaden evidence access.

Capability confidence != evidence authority.

Obligation != satisfaction.

Mission Request defines expected return.

Capability Return records actual return.

Governance != mission executor.

TOC != truth owner.

TOC != canonical state owner.

TOC != object identity owner.

TOC != policy owner.

Mission Request != authorization invention.

Write capability != authority.

Authorization != execution.

Human Gate decision != mission execution.

Capability Return records what came back.

Capability Return identity is not Room Object identity.

Capability Return identity is not Capability Mission Request identity.

Bounded finding != canonical truth.

Finding != publication.

Finding != decision.

Returned evidence != automatically promoted evidence.

Return != Cartography.

Unknown remains unknown.

Discriminating evidence need != evidence itself.

Restricted != absent.

Inaccessible != nonexistent.

Movement MUST NOT sever analytical contact.

COMPLETED != analytical truth.

PARTIAL != failure.

BLOCKED != nonexistent.

Capability Return != Occupancy EXITED witness.

Return != exit.

Capability Return != Goblin Signal event.

Return != propagation.

R3-F determines proportional force.

Need determines force downstream.

Mission Request != formation.

Capability Return != formation.

Capability Mission Request != ACTIVE.

Capability Return != ACTIVE transition.

Mission result != publication.

Mission result != decision authority.

No proportional-force selection yet.

No formation selection yet.

No Goblin Signal propagation yet.

No ACTIVE lifecycle transition yet.

No Landing semantics yet.
