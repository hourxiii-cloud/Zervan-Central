# Zervan v41 Observer Restoration

Status: CANDIDATE — NOT PROMOTED

Restoration stage: OR-13

Version: vTemporal.41.0

Authority: NONE

Human Gate: ACTIVE

## Purpose

This document describes the restored v41 Observer architecture as implemented

on `candidate/v41-observer-restoration`.

The restoration corrects a No Compression Out regression in which historical

Observer functions were no longer independently represented in native v41

implementation.

The restoration does not create new analytical authority, publication

authority, approval authority, external runtime authority, or canonical

mutation authority.

## Observer inventory

The restored architecture contains exactly ten Observer capabilities:

- Seven Primary Observers.

- Three Controlled Sub-Observers.

- Owl_Hoot remains a Primary Observer even when operating in bounded

  sub-observer mode.

| Observer | ID | Operating class | Canonical seat | Supported modes | Distinctive invariant |

|---|---|---|---|---|---|

| Eagle | `eagle` | PRIMARY | PRIMARY_OBSERVER | PRIMARY | Trajectory is observation of supported direction, not ownership of the future. |
| Mole | `mole` | PRIMARY | PRIMARY_OBSERVER | PRIMARY | Subsurface observation remains bounded by what the authorized evidence can support. |
| Duck | `duck` | PRIMARY | PRIMARY_OBSERVER | PRIMARY | Failure to reconcile is information, not automatic threat attribution. |
| Wildflower | `wildflower` | PRIMARY | PRIMARY_OBSERVER | PRIMARY | Emergence may reveal structure without establishing why that structure exists. |
| Mockingbird | `mockingbird` | PRIMARY | PRIMARY_OBSERVER | PRIMARY | Representation may change while evidentiary meaning remains invariant. |
| Platypus | `platypus` | PRIMARY | PRIMARY_OBSERVER | PRIMARY | Category insufficiency does not authorize invention of a different underlying object. |
| Owl_Hoot | `owl_hoot` | PRIMARY | PRIMARY_OBSERVER | PRIMARY, BOUNDED_SUB_OBSERVER | Absence of observation is not observation of absence. |
| Osprey | `osprey` | CONTROLLED_SUB_OBSERVER | CONTROLLED_SUB_OBSERVER | CONTROLLED_SUB_OBSERVER | External context may pressure analysis without acquiring primary-evidence status or collection authority. |
| AnimalKingdom | `animal_kingdom` | CONTROLLED_SUB_OBSERVER | CONTROLLED_SUB_OBSERVER | CONTROLLED_SUB_OBSERVER | Synthetic pressure remains synthetic even when it successfully exposes a real weakness. |
| Armadillo | `armadillo` | CONTROLLED_SUB_OBSERVER | CONTROLLED_SUB_OBSERVER | CONTROLLED_SUB_OBSERVER | Integrity challenge may bound or weaken a claim; it does not manufacture attribution or authenticity. |

## Primary Observers

### Eagle

Eagle provides trajectory and long-range stability/coherence perception.

Its function is not interchangeable with generic anomaly detection.

### Mole

Mole provides subsurface, latent-signal, and hidden-structure perception.

It exists to expose structure that may not be visible at the immediate

surface.

### Duck

Duck provides spin, wobble, and divergence perception. It identifies

instability or directional inconsistency without converting that perception

into decision authority.

### Wildflower

Wildflower provides emergence and pattern-bloom perception. It preserves the

ability to recognize newly forming structure rather than requiring an already

mature pattern.

### Mockingbird

Mockingbird provides reflection, echo, and narrative or representational drift

perception. Representation is not identity, and repetition is not independent

confirmation.

### Platypus

Platypus provides anomaly synthesis and category-violation perception. It

preserves signals that do not fit cleanly inside an existing category instead

of forcing premature classification.

### Owl_Hoot

Owl_Hoot provides absence, silence, visibility-limit, missing-trace,

cadence-break, and hidden-observer-pressure perception.

Owl_Hoot's canonical seat is PRIMARY_OBSERVER.

`BOUNDED_SUB_OBSERVER` is an operating mode only. It does not demote,

replace, or reseat Owl_Hoot.

## Controlled Sub-Observers

Controlled Sub-Observers apply bounded analytical pressure. Their outputs

remain distinguishable from Primary Observer output and cannot silently become

facts, primary evidence, attribution, authenticity, authority, or canonical

state.

### Osprey

Osprey provides external-context pressure.

External collection is not authorized by the existence or invocation of

Osprey. External runtime and external action remain disabled unless separately

authorized outside the Observer capability.

External context does not silently become primary evidence.

### AnimalKingdom

AnimalKingdom provides synthetic adversarial, fuzz, and edge-case pressure.

Synthetic pressure does not become fact and does not become primary evidence.

AnimalKingdom may expose weakness in an interpretation but may not steer the

Primary Observer result into a predetermined conclusion.

### Armadillo

Armadillo provides bounded integrity, authentication, and attribution

challenge pressure.

A challenge is not proof of authenticity. A challenge is not proof of

attribution.

## Shared Observer contract

All Observers remain read-only perception surfaces.

An Observer:

- observes;

- annotates;

- contextualizes;

- preserves its own identity and provenance;

- operates only inside an authorized scope and view.

An Observer does not:

- own the Room;

- become evidence;

- become a source of truth;

- mutate primary evidence;

- mutate canonical state;

- create authority;

- satisfy the Human Gate;

- increase the evidence or claim ceiling;

- certify publication;

- approve findings.

Observation is not conclusion.

Detection is not finding.

Perspective is not identity.

Capability availability is not authorization.

Invocation is not permission.

## Routing

OR-5 restores explicit Observer routing.

Routing preserves the following laws:

- Need determines force.

- Question determines mission.

- Evidence determines escalation.

- Capability availability does not equal authorization.

- Invocation does not equal permission.

- Identity travels.

- Payload rests.

Routing may select:

- no Observer;

- one Observer;

- multiple Observers.

Routing may identify a candidate capability without authorizing its use.

Generic Observer substitution is blocked.

Observer routing does not replace or bypass evidence-admission routing.

## Multi-Observer composition

OR-6 restores multi-Observer composition while preserving independent

Observer identities.

Composition does not perform:

- voting;

- averaging;

- winner selection;

- forced consensus;

- silent reconciliation.

Observer disagreement is information.

Observer disagreement does not automatically mean the system itself is in

contradiction.

Different authorized views may produce different bounded observations without

implying that either view represents the whole Room.

Controlled pressure remains separated from Primary Observer results.

## PMC, CCR, MC, Raven, and Audit integration

OR-7 provides explicit integration surfaces for:

- PMC;

- CCR;

- MC;

- Raven;

- Audit.

Observer composition may be supplied to these surfaces without giving the

Observers authority owned by those downstream functions.

Raven receives Observer output for reporting while Observer identity and

controlled-pressure identity remain preserved.

Audit receives Observer output for integrity review while provenance remains

preserved.

Observer integration does not create publication or approval authority.

## Controlled pressure isolation

OR-8 explicitly isolates Controlled Sub-Observer pressure.

The following promotions are blocked:

- Osprey external context -> primary evidence.

- AnimalKingdom synthetic input -> fact.

- AnimalKingdom synthetic input -> primary evidence.

- Armadillo challenge -> authenticity.

- Armadillo challenge -> attribution.

- Controlled pressure -> Primary output steering.

- Controlled pressure -> canonical mutation.

- Controlled pressure -> claim-ceiling increase.

- Controlled pressure -> authority.

Pressure may change the next question.

Pressure may not silently change the facts.

## Failure and scar semantics

OR-9 restores explicit Observer failure semantics.

Supported failure states are:

- `NO_SIGNAL`

- `INSUFFICIENT_EVIDENCE`

- `EVIDENCE_CEILING_REACHED`

- `VIEW_RESTRICTED`

- `BOUNDARY_BLOCKED`

- `PROVENANCE_INCOMPLETE`

- `STALE_BINDING`

- `DIVERGENT_BINDING`

- `SEMANTIC_CONFLICT`

- `OBSERVER_UNAVAILABLE`

- `OPERATING_SCOPE_EXCEEDED`

- `AUTHORITY_VIOLATION`

- `SCARRED`

Failure does not silently become fact or finding.

A scar records an unresolved condition. A scar does not self-resolve and does

not itself become fact, finding, or authority.

`NO_SIGNAL` is distinct from `OBSERVER_UNAVAILABLE`.

`INSUFFICIENT_EVIDENCE` is not negative evidence.

`EVIDENCE_CEILING_REACHED` stops claim expansion.

`SEMANTIC_CONFLICT` is preserved as information rather than silently

reconciled.

## Independent functional testing

OR-10 establishes one independent functional test suite for each of the ten

named Observers.

Each Observer is tested for:

1. capability identity;

2. operating class;

3. canonical seat;

4. supported mode;

5. distinctive invariant;

6. routing;

7. explicit permission;

8. Authority NONE;

9. Human Gate ACTIVE;

10. failure semantics;

11. function-specific operational path;

12. canonical-mutation prohibition.

Aggregate result: `120/120 PASS`.

Primary Observer composition path: `7/7 PASS`.

Controlled pressure path: `3/3 PASS`.

## Aggregate completeness

OR-11 validates the restoration as a whole.

Aggregate completeness result: `30/30 PASS`.

The aggregate validator verifies:

- exact 7 + 3 + 10 Observer cardinality;

- ten independent capability contracts;

- Owl_Hoot Primary seat preservation;

- Owl_Hoot bounded mode preservation;

- routing;

- composition;

- PMC / CCR / MC / Raven / Audit integration;

- controlled pressure isolation;

- failure/scar semantics;

- ten functional suites;

- 120 functional controls;

- Authority NONE;

- Human Gate ACTIVE;

- absence of self-promotion.

## Fresh-reader validation

OR-12 proves that the restored Observer architecture can be reconstructed from

committed Git HEAD without relying on:

- conversation state;

- stored memory;

- uncommitted tracked workspace state;

- generic architectural guessing.

Fresh-reader result: `20/20 PASS`.

The reader recovers:

- seven Primary Observers;

- three Controlled Sub-Observers;

- all ten identities;

- all ten distinctive invariants;

- Owl_Hoot's Primary seat;

- Owl_Hoot's bounded mode;

- the OR-0 through OR-11 restoration chain;

- the restoration artifact manifest;

- Authority NONE;

- Human Gate ACTIVE;

- candidate-not-promoted status.

## No Compression Out

The restoration is incomplete if any named Observer exists only as:

- a historical reference;

- a documentation label;

- a configuration name;

- an alias for generic Observer behavior;

- a behavior silently absorbed into another Observer.

Shared implementation mechanism is permitted.

Shared meaning is not.

Ten named Observer capabilities must remain ten independently recoverable

functions.

## Canonical status

This restoration remains candidate implementation.

It has not been canonically promoted.

Authority remains NONE.

Human Gate remains ACTIVE.

External runtime remains disabled.

External action remains disabled.

Canonical mutation has not been performed by OR-0 through OR-13.

## Restoration sequence

| Stage | Function |

|---|---|

| OR-0 | Recovery Inventory |

| OR-1 | Native-v41 Observer Contract |

| OR-2 | Ten Independent Capability Contracts |

| OR-3 | Schemas |

| OR-4 | Validators |

| OR-5 | Routing Integration |

| OR-6 | Multi-Observer Composition |

| OR-7 | PMC / CCR / MC / Raven / Audit Integration |

| OR-8 | Controlled Pressure Isolation |

| OR-9 | Failure / Scar Semantics |

| OR-10 | Ten Functional Test Suites |

| OR-11 | Aggregate Completeness Validator |

| OR-12 | Fresh-Reader Validation |

| OR-13 | Documentation |

Next stage: OR-14 — Restoration Receipt.
