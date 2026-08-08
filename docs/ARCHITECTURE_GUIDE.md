# Zervan v41 Architecture Guide

Status: CONTROLLED CANDIDATE DOCUMENTATION
Ring: R7-E
Responsibility: RATIONALE AND PRIMITIVES
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Stability Baseline: ae8dd9e22a34589f546f64ed452c0eee976cf299
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 1. Purpose

This guide explains the rationale and core primitives of native Zervan v41.

It describes why the architecture is structured as implemented at the R7-J
stability baseline.

It does not replace implementation contracts.

It does not redefine runtime semantics.

It does not create new architectural authority.

Current Git remains implementation truth.

---

## 2. Architectural Problem

Zervan is built to preserve analytical meaning while evidence, perspective,
scope, representation, and user need change.

The central architectural problem is avoiding silent loss of:

- object identity;
- evidence boundaries;
- provenance;
- uncertainty;
- operational position;
- transition history;
- authority boundaries.

Native v41 solves this by separating object identity, operational geography,
representation, analytical computation, rendering, and authority.

---

## 3. One Analytical Object

The central primitive is the Room.

The Room represents one governed analytical object.

Multiple views may exist over the Room without creating multiple analytical
worlds.

The architecture therefore distinguishes:

- object;
- representation;
- perspective;
- Zone;
- Space;
- Branch;
- distinct object.

This prevents representation changes from silently becoming identity changes.

---

## 4. Why the Room Exists

The Room provides a durable container for analytical continuity.

Without a stable object boundary, every analytical transform could fragment the
world into disconnected outputs.

The Room preserves continuity across:

- qualification;
- analysis;
- representation turns;
- restriction;
- collapse;
- landing;
- replay;
- reporting.

The Room is therefore both an identity boundary and an operational continuity
boundary.

---

## 5. Origin, Ingress, and Genesis

Origin preserves where material came from.

Ingress preserves governed entry.

Genesis establishes the initial object identity.

These are separate because provenance, entry, and identity are not the same
thing.

A source may be known without a valid Genesis.

Material may enter without yet becoming a qualified Room.

Genesis establishes identity, not truth.

---

## 6. Revision and Branch

Revision changes the governed state of the same object.

Branch preserves alternate lineage.

Neither automatically creates a distinct analytical object.

This distinction prevents history and experimentation from being confused with
new reality.

Branching is therefore a lineage operation first.

Distinct-object creation requires stronger evidence.

---

## 7. Operational Geography

Native v41 adds explicit operational geography because reasoning must preserve
where it is operating.

The principal geography is:

Origin
->
Ingress
->
Genesis
->
Room
->
Territory
->
Terrain
->
Zone
->
Space
->
Representation Transform
->
Cartography
->
Stick continuity

This architecture separates reachability, encountered conditions, orientation,
restriction, and navigation.

---

## 8. Territory and Terrain

Territory represents reachable governed analytical space.

Terrain represents what is actually encountered.

The distinction matters because reachability does not imply examination.

A system may have access to Territory while only a subset of Terrain has been
encountered.

This preserves the difference between potential reach and observed evidence.

---

## 9. Zone

A Zone is an analytical orientation over the same object.

Zone enables perspective change without identity fracture.

The architectural principle is that reality is established once, while
perspective may turn many times.

Zone therefore belongs to representation and navigation rather than object
creation.

---

## 10. Space

Space is a more restrictive operational boundary inside the current geography.

Space exists so analysis may narrow safely without changing object identity.

Restriction of visibility or operation is not equivalent to deleting the
underlying material.

This is essential for preserving existence-aware restricted state.

---

## 11. Representation Transform

Representation Transform changes how the same object is expressed or examined.

A transform may change:

- analytical orientation;
- output form;
- dimensional emphasis;
- audience representation.

It must preserve the relationship to the underlying Room.

Representation is intentionally separated from identity.

---

## 12. Cartography

Cartography preserves navigable geometry.

It records enough structure to know:

- current position;
- prior positions;
- representation turns;
- reachable neighboring views;
- return paths.

Cartography exists because analytical continuity requires more than an object
identifier.

The system must also preserve where reasoning occurred.

---

## 13. Stick Continuity

Stick continuity preserves route continuity through navigation and
representation change.

Its purpose is to prevent analytical movement from losing the thread back to the
governed object.

Identity continuity and navigation continuity are related but distinct.

The Stick exists to preserve the latter.

---

## 14. Qualification Before Analysis

Qualification is architecturally separate from analysis.

This prevents the system from reasoning deeply over an object whose boundaries,
relationships, provenance, or permitted operation have not yet been established.

Qualification answers whether analysis may proceed.

Analysis answers questions inside the qualified environment.

The separation prevents premature analytical authority.

---

## 15. Request State and Room State

Request readiness and Room readiness are separate state domains.

A user request can be well-formed while the Room remains unqualified.

A Room can be qualified while a particular operation remains disallowed.

The architecture therefore avoids collapsing all readiness into one Boolean.

This preserves precise failure and blocking conditions.

---

## 16. Occupancy

Occupancy models governed presence in a Room.

Occupancy is separated from Room lifecycle because entering an object does not
change the object's identity.

It is separated from authority because presence does not grant permission.

This allows the architecture to track who or what is operating where without
conflating location with control.

---

## 17. Question Contract

The Question Contract makes recurring inquiry explicit and version-controlled.

It separates:

- what is being asked;
- where it is being asked;
- what evidence may participate;
- how strong claims may become;
- how results may be rendered;
- what authority remains required.

This prevents natural-language inquiry from silently changing system state.

---

## 18. Evidence Boundary

The evidence boundary defines admissible analytical input.

It exists so analysis cannot silently expand its evidence universe simply
because more material is technically reachable.

Evidence access and evidence admissibility are therefore distinct.

This keeps analytical conclusions bounded to governed evidence.

---

## 19. Evidence Ceiling

The evidence ceiling limits claim strength.

It exists because representation, confidence language, or audience adaptation
must not create stronger evidence than the system possesses.

The ceiling is therefore a claim-governance primitive.

It prevents linguistic confidence from outrunning evidence.

---

## 20. Capability Routing

Capability routing is proportional rather than fixed.

The architecture treats capabilities as callable resources.

Need determines how much capability is justified.

Question defines the mission.

Evidence determines escalation.

This prevents both under-response and habitual over-escalation.

---

## 21. Scale and Formation

Scale and formation are separate primitives.

Scale describes how much capability is required.

Formation describes how capability is arranged.

Keeping them separate allows the system to change one without silently changing
the other.

This makes capability movement more explainable and auditable.

---

## 22. Hydration

Hydration separates identity availability from payload availability.

Identity may move through the system while payload remains at rest.

Hydration occurs only when mission need justifies releasing material.

This reduces unnecessary exposure and preserves authorization boundaries.

---

## 23. Restriction and Constriction

Restriction and constriction are narrowing operations.

They exist because secure analytical systems must be able to operate over a
partial authorized view without pretending excluded material does not exist.

The architecture therefore preserves existence separately from visibility.

This is critical for auditability and claim ceilings.

---

## 24. Collapse

Collapse represents a governed analytical convergence state.

It is intentionally not equivalent to:

- truth;
- authority;
- publication;
- execution;
- new object creation.

Collapse exists so convergence can be recorded without granting it powers it
does not possess.

---

## 25. Landing

Landing records where an operation arrives.

It preserves enough analytical context to support future continuation, audit, or
recovery.

Landing is separated from Replay because arrival state and historical
re-observation are different operations.

---

## 26. Reflight

Reflight represents justified renewed movement after a prior convergence or
landing.

It requires a trigger because endless re-analysis would otherwise destroy
stability.

The Reflight primitive makes renewed work explicit and attributable.

---

## 27. Replay

Replay reconstructs a historical observational coordinate of the same Room.

It exists to make analytical history reproducible without creating another
object.

Replay is distinct from reconstruction-by-guess.

It must preserve historical context rather than silently applying present
defaults.

---

## 28. Scar

Scar is a first-class record of unresolved contradiction, failure, or important
analytical damage.

Scar exists because system failure is evidence.

Suppressing failure knowledge would destroy auditability and future learning.

Scar therefore persists independently of whether later operations succeed.

---

## 29. Scar Replay

Scar Replay makes preserved failure conditions inspectable.

It allows the system to return to the conditions under which the Scar occurred.

This supports debugging, resilience, audit, and analytical learning without
rewriting the original history.

---

## 30. Distinct Object Test

Native v41 separates same-object reasoning from distinct-object creation.

The valid identity outcomes are:

- SAME_OBJECT;
- DISTINCT_OBJECT;
- UNRESOLVED.

UNRESOLVED is preserved because uncertainty about identity must not be forced
into false sameness or false distinction.

---

## 31. Passageways

Passageways connect distinct Rooms.

They preserve relationship without collapsing identity.

This allows cross-object analysis while maintaining independent provenance,
state, and lineage.

Passageway is therefore a relationship primitive, not a merge primitive.

---

## 32. Analytical Pipeline

The native analytical pipeline is:

Evidence
->
PMC
->
CCR
->
MC
->
Raven
->
Human Gate

Each stage has a distinct responsibility.

The separation exists to prevent computation, candidate commitment, output
admissibility, reporting, and authority from collapsing into one opaque step.

---

## 33. PMC

PMC performs bounded epistemic computation.

PMC explores analytical possibilities inside the governed evidence environment.

It does not own object identity.

It does not own publication.

It does not own authority.

This keeps analytical computation powerful without making it sovereign.

---

## 34. CCR

CCR records deterministic candidate commitment.

It exists between PMC and MC so analytical selection remains attributable.

CCR preserves candidate lineage, rejection history, uncertainty, and the
evidence context supporting the candidate state.

Candidate commitment is therefore explicit rather than implicit.

---

## 35. MC

MC governs response and output admissibility.

Its role is not to decide truth.

Its role is to decide whether and how analytical state may become admissible
output.

This separates epistemic computation from communication control.

---

## 36. Raven

Raven owns reporting and forward translation.

Raven converts governed analytical state into consumer-facing representation.

It does not become the analytical object.

It does not create evidence.

It does not create authority.

This keeps reporting downstream from analysis.

---

## 37. Human Gate

Human Gate is the explicit authority boundary.

The architecture separates analytical capability from authority-bearing action.

This prevents model success, validator success, report production, or receipt
production from silently authorizing execution.

Authority remains human-governed.

---

## 38. Validation Architecture

Ring 6 separates validation into independent families and vectors.

This prevents a single green aggregate from hiding untested behavior.

Validation includes identity, lifecycle, perspective, replay, replacement,
representation independence, collapse, and cross-pipeline behavior.

The architecture treats validation as attributable evidence rather than a binary
badge.

---

## 39. Failure Taxonomy

Native v41 uses:

- INNER_INVARIANT_CONTRADICTION;
- OUTER_IMPLEMENTATION_DEFECT;
- VALIDATOR_DEFECT;
- COVERAGE_GAP;
- SOURCE_COLLISION;
- UNRESOLVED_REQUIRED_SURFACE.

The taxonomy exists so repair targets the actual failing layer.

Without classification, a validator defect may incorrectly trigger doctrine
changes, or an implementation defect may be hidden by weakening validation.

---

## 40. Stability Before Documentation

R7-J establishes the documentation freeze.

This architectural ordering exists because documentation must describe a stable
implementation.

Implementation leads.

Documentation follows.

Documentation is therefore downstream representation of implemented state.

It is not a source of missing behavior.

---

## 41. Documentation Separation

Ring 7 separates documentation responsibilities:

README:

ORIENTATION

User Manual:

UNDERSTANDING AND OPERATION

Architecture Guide:

RATIONALE AND PRIMITIVES

Developer Guide:

IMPLEMENTATION AND EXTENSION

Audit Guide:

VERIFICATION / REPLACEMENT / RESILIENCE / PROVENANCE / COMPLETION CRITERIA

Operations Guide:

CONSISTENT RUNTIME OPERATION

The separation prevents one document from becoming an ungoverned alternate
canonical body.

---

## 42. Version and Promotion Separation

Version identity and promotion state are separate.

Native version:

vTemporal.41.0

Promotion State:

CANDIDATE

Canonical promotion is a later governed transition.

This separation prevents repository location or validation success from silently
changing version identity or authority state.

---

## 43. Authority Model

Current candidate posture:

Authority: NONE

Human Gate: ACTIVE

External Runtime: DISABLED

External Action: DISABLED

System Population: DISALLOWED

Canonical Mutation: HUMAN_GATE_ONLY

The system is designed to preserve analytical capability while controlling
authority.

---

## 44. Architecture Closure

Native v41 architecture preserves:

- one analytical object;
- explicit operational geography;
- governed qualification;
- controlled occupancy;
- versioned inquiry;
- bounded evidence;
- proportional capability routing;
- mission-required hydration;
- representation independence;
- attributable convergence;
- reproducible history;
- failure memory;
- explicit pipeline separation;
- human-controlled authority.

This guide explains the stabilized architecture.

It does not redefine it.

It does not create new implementation.

It does not create promotion authority.

ARCHITECTURE GUIDE COMPLETE.

R7-F owns the Developer Guide.
