# Zervan v41 Developer Guide

Status: CONTROLLED CANDIDATE DOCUMENTATION
Ring: R7-F
Responsibility: IMPLEMENTATION AND EXTENSION
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Stability Baseline: ae8dd9e22a34589f546f64ed452c0eee976cf299
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 1. Purpose

This guide explains how native Zervan v41 is implemented, validated, extended,
and repaired.

It documents the stabilized implementation frozen by R7-J.

It does not redefine architecture.

It does not replace contracts, schemas, validators, tests, receipts, or Git.

Current Git remains implementation truth.

---

## 2. Development Rule

Implementation leads.

Documentation follows.

A developer changes implementation only through explicit repository artifacts.

Do not use prose to substitute for missing implementation.

Do not use a validator to manufacture a behavior that the implementation does
not contain.

Do not weaken implementation merely to satisfy an incorrect validator.

Classify first.

Repair second.

---

## 3. Repository Entry

Resolve active implementation identity from:

1. `VERSION`
2. `VERSION.json`
3. `VERSION_AUTHORITY.md`
4. `call/INITIATION_STATEMENT_V41_0.md`
5. `canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md`

Native version:

`vTemporal.41.0`

Implementation identity:

`v41 Complete`

Development branch:

`candidate/v41-complete`

Promotion State:

`CANDIDATE`

---

## 4. Repository Structure

Native-v41 implementation is distributed across explicit repository surfaces.

Primary areas include:

- `canonical/` — native entry and historical canonical loads;
- `call/` — initiation surfaces;
- `contracts/` — governed behavioral and boundary contracts;
- `schemas/` — machine-readable state contracts;
- `receipts/` — attributable state and transition records;
- `tools/` — validators and aggregate runners;
- `tests/` — executable validation;
- `docs/` — downstream documentation;
- `candidate/` — controlled candidate instantiation state;
- `VERSION`;
- `VERSION.json`;
- `VERSION_AUTHORITY.md`.

Directory location does not create authority.

---

## 5. Contracts

Contracts define governed implementation semantics and boundaries.

A contract may define:

- identity;
- lifecycle;
- admissibility;
- transition;
- state;
- evidence boundary;
- evidence ceiling;
- authority boundary;
- failure disposition.

Contract prose should correspond to implemented behavior.

Contract text does not become runtime truth merely because it exists.

When a contract and implementation disagree, classify the disagreement before
repair.

---

## 6. Schemas

Schemas define machine-readable structure for governed state.

Native v41 uses JSON Schema Draft 2020-12 where machine-readable contracts are
required.

Schemas should constrain structure without inventing semantics absent from the
implementation contract.

Schema success does not prove analytical truth.

A parsed schema is not equivalent to a validated implementation.

---

## 7. Validators

Validators test bounded implementation and contract conditions.

Validators are observers.

Validators do not own state.

Validators do not own authority.

A validator must fail when the governed condition fails.

A validator must not require invented wording merely because a sentence would be
convenient to search.

Bind validators to actual source semantics.

---

## 8. Tests

Tests exercise validator behavior and implementation invariants.

Tests should include positive and negative paths where the surface requires
them.

Tests must not be written only to confirm the current happy path.

A test suite should be able to prove rejection behavior where rejection is part
of the contract.

Green output is evidence of tested behavior, not universal correctness.

---

## 9. Aggregate Runners

Ring runners coordinate bounded subsection validation.

A subsection fast gate should remain smaller than the full aggregate.

Do not run the entire dependency tree after every local change unless
cross-section diagnosis requires it.

Aggregate runners do not create promotion authority.

Aggregate PASS != canonical promotion.

---

## 10. Identity Implementation

Identity must remain independent from representation.

Native-v41 development must preserve:

- Origin;
- Genesis;
- Revision;
- Branch;
- Room identity;
- lineage;
- state roots;
- authorized view roots;
- provenance.

Do not create a new object merely because a view changes.

Distinct object creation requires affirmative identity evidence.

---

## 11. SHA-512

Native v41 uses SHA-512 where cryptographic object or contract identity is
specified.

A deterministic identity function must:

- normalize only as explicitly defined;
- preserve material semantic distinctions;
- use deterministic serialization;
- produce stable identity for stable semantic input.

Hash != truth.

Hash != authority.

Hash change should be explainable by material input change.

---

## 12. One-Object Preservation

The Room remains one analytical object across governed perspective changes.

A developer implementing a new view, renderer, Zone, Space, or transform must
preserve Room identity unless distinct-object rules explicitly require
otherwise.

Perspective implementation must not clone the world.

Representation state must remain attributable to the underlying Room.

---

## 13. Operational Geography

Implementations that move or transform analytical position must preserve the
native geography:

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

A new feature must declare where it operates in this geography.

Unlocated capability is an implementation risk.

---

## 14. Qualification

Qualification remains prior to normal analysis.

New analytical capability must not bypass qualification simply because it can
technically consume the object.

A new route must preserve:

- qualification state;
- readiness boundary;
- evidence boundary;
- evidence ceiling;
- permitted operation.

Request readiness must not silently substitute for Room readiness.

---

## 15. Occupancy

Capabilities entering a Room must use governed occupancy semantics where
applicable.

Occupancy does not grant ownership.

Occupancy does not grant authority.

A developer must not use presence as a shortcut around permissions or lifecycle
state.

---

## 16. Question Contract Extension

Recurring inquiry extensions must preserve the native Question Contract.

The active surface is:

`contracts/question/QUESTION_CONTRACT.md`

Material semantic change requires a new contract version.

Executor type must not alter inquiry meaning.

Question execution remains read-only unless a separately authorized write path
exists.

Do not embed write authority into the Question Contract.

---

## 17. Evidence Boundary

Every feature consuming evidence must preserve the applicable evidence boundary.

Technical reachability does not equal evidence admissibility.

A new processor, capability, or renderer must not silently pull evidence from
outside the governed boundary.

Boundary widening requires an explicit governed change.

---

## 18. Evidence Ceiling

Every feature producing claims or representations must preserve the evidence
ceiling.

A renderer cannot raise claim strength.

A new audience profile cannot raise claim strength.

A decision-option generator cannot raise claim strength.

Implementation must carry ceiling constraints downstream.

---

## 19. Capability Routing

New capabilities must participate in proportional routing.

Do not make a capability mandatory merely because it exists.

Routing should preserve:

- mission;
- need;
- question;
- evidence pressure;
- escalation basis.

Need determines force.

Question determines mission.

Evidence determines escalation.

---

## 20. Scale and Formation

Scale and Formation remain independent implementation dimensions.

Adding a new Formation must not silently redefine force scale.

Changing force scale must not automatically change Formation.

Formation changes require attributable justification.

---

## 21. Hydration

Payload release is mission-bounded.

New implementation must not convert availability into standing hydration.

Identity may travel.

Payload rests until mission need justifies release.

Hydration must preserve authorization and evidence constraints.

---

## 22. Restriction and Constriction

Restriction and constriction narrow permissible operation.

Developers must preserve existence-aware state.

Do not implement restricted data as if it vanished from the model.

Do not allow a downstream component to silently broaden a constricted working
surface.

---

## 23. Collapse

Collapse implementation must preserve the evidence and route producing the
convergence state.

Collapse does not create:

- authority;
- publication;
- new Room identity;
- automatic Reflight;
- automatic promotion.

A collapse record must remain attributable.

---

## 24. Landing

Landing implementation must preserve sufficient continuation state.

At minimum, preserve applicable:

- Room identity;
- revision;
- question;
- orientation;
- transform state;
- evidence boundary;
- evidence ceiling;
- unresolved state;
- provenance.

Landing is a continuation primitive, not a reset.

---

## 25. Reflight

Reflight requires an explicit trigger.

Implementations must avoid automatic re-analysis loops after convergence.

The trigger and justification must remain attributable.

Reflight must preserve Room identity unless separate identity rules require a
different operation.

---

## 26. Replay

Replay must restore historical observational state without silently applying
current defaults.

Replay must not:

- create new Genesis;
- create a new Room by default;
- rewrite historical evidence;
- raise historical evidence ceilings;
- mutate the original historical state.

Historical question execution and Replay are distinct operations.

---

## 27. Scar

Scar is implemented as preserved failure or unresolved analytical state.

Do not downgrade Scar to transient logging.

A Scar must remain inspectable and attributable.

Later success does not erase earlier failure evidence.

---

## 28. Distinct Objects and Passageways

Implement distinct-object logic before cross-object Passageway behavior.

The identity result set remains:

- SAME_OBJECT;
- DISTINCT_OBJECT;
- UNRESOLVED.

Do not force unresolved identity into a Boolean.

Passageways connect distinct Rooms without merging their identities.

---

## 29. Analytical Pipeline

The native pipeline is:

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

New implementation must preserve this ownership separation.

Do not bypass CCR.

Do not move Human Gate authority upstream.

Do not let Raven redefine evidence.

---

## 30. PMC Development Boundary

PMC owns bounded analytical computation.

PMC does not own:

- Room identity;
- rendering authority;
- publication authority;
- Human Gate.

New PMC behavior must remain evidence-bound and ceiling-bound.

PMC output should remain attributable to the inputs and computational route that
produced it.

---

## 31. CCR Development Boundary

CCR records deterministic candidate commitment.

CCR should preserve:

- candidate selection;
- null selection;
- rejection history;
- uncertainty;
- evidence lineage;
- boundary;
- ceiling.

Do not collapse CCR into PMC or MC merely to simplify implementation.

---

## 32. MC Development Boundary

MC owns response and output admissibility.

MC does not recompute epistemic truth.

MC must not bypass CCR history.

Admissibility logic must remain separate from authority-bearing decisions.

---

## 33. Raven Development Boundary

Raven owns reporting and forward translation.

New renderers must preserve analytical meaning.

Renderer changes may alter presentation.

Renderer changes must not alter:

- evidence;
- provenance;
- object identity;
- evidence boundary;
- evidence ceiling;
- decision lineage.

---

## 34. Human Gate Boundary

Human Gate remains the authority-bearing boundary.

No implementation extension may grant itself authority merely because it:

- passed tests;
- produced a report;
- emitted a receipt;
- generated a recommendation;
- received a prior approval.

Authority remains explicit.

Approval != execution.

---

## 35. Provenance

Every meaningful implementation transition should remain attributable.

Provenance should preserve:

- source;
- input identity;
- transform;
- governing contract;
- output identity;
- state change;
- failure condition;
- actor or capability where applicable.

Provenance != endorsement.

Missing provenance should block operations where attribution is required.

---

## 36. Extension Rule

A new native-v41 capability should be added by extending the smallest correct
surface.

Preferred sequence:

1. identify the existing owner;
2. identify the governing invariant;
3. identify the required contract change;
4. define machine-readable state if required;
5. implement the capability;
6. add validator coverage;
7. add positive tests;
8. add negative tests;
9. extend the appropriate bounded runner;
10. run the fast gate;
11. commit only intended files;
12. preserve provenance.

Do not generalize a local discovery into doctrine without justification.

---

## 37. New Contract Rule

Create a new contract only when an existing contract cannot own the semantic
boundary without losing identity or responsibility.

Do not create duplicate contracts for wording convenience.

A contract should have one clear ownership purpose.

Cross-contract references should preserve ownership rather than absorb it.

---

## 38. New Schema Rule

Create a schema when machine-readable state must be exchanged, validated, or
recorded.

Do not create schemas merely to mirror prose.

Schema fields should correspond to governed state.

Enums should represent explicit states rather than inferred guesses.

Unknown or unresolved states should be represented when the architecture
requires them.

---

## 39. New Validator Rule

A new validator must declare what it validates.

It should test implementation state, not editorial preference.

Use semantic bindings where exact formatting is irrelevant.

Use exact bindings only when exact representation is itself governed.

A validator defect must be repaired in the validator, not hidden by rewriting
correct implementation.

---

## 40. New Test Rule

Tests should prove the contract's meaningful behavior.

At minimum consider:

- positive case;
- invalid state;
- missing prerequisite;
- unauthorized operation;
- identity drift;
- evidence-boundary violation;
- evidence-ceiling violation;
- lifecycle violation;
- authority violation.

Not every surface requires every category.

Coverage should follow the actual contract.

---

## 41. Failure Classification

Before repair, classify the failure as one of:

- `INNER_INVARIANT_CONTRADICTION`
- `OUTER_IMPLEMENTATION_DEFECT`
- `VALIDATOR_DEFECT`
- `COVERAGE_GAP`
- `SOURCE_COLLISION`
- `UNRESOLVED_REQUIRED_SURFACE`

Classification determines which layer is allowed to change.

Do not repair across the wrong boundary.

---

## 42. INNER_INVARIANT_CONTRADICTION

Use when two required native invariants cannot simultaneously hold.

Do not patch around it locally.

Stop and resolve the contradiction at the owning architectural level.

This is not a validator convenience failure.

---

## 43. OUTER_IMPLEMENTATION_DEFECT

Use when the intended contract is coherent but implementation violates it.

Repair the implementation.

Do not weaken the contract merely to preserve current behavior.

Add regression coverage.

---

## 44. VALIDATOR_DEFECT

Use when implementation and contract agree but validation binds them
incorrectly.

Repair the validator or its test.

Do not mutate correct source behavior just to satisfy a bad check.

Preserve the defect and repair provenance.

---

## 45. COVERAGE_GAP

Use when required behavior exists without sufficient validation coverage.

Add the missing bounded validation.

Do not claim coverage based solely on nearby tests.

Coverage relationship != ownership migration.

---

## 46. SOURCE_COLLISION

Use when authoritative surfaces conflict or ownership is ambiguous.

Do not silently pick the convenient source.

Resolve authority and ownership before implementation proceeds.

Preserve the collision as evidence.

---

## 47. UNRESOLVED_REQUIRED_SURFACE

Use when the architecture requires a contract, schema, receipt, or other surface
that has not yet been implemented.

Preserve the requirement explicitly.

Deferred != forgotten.

Missing != nonexistent.

---

## 48. Git Discipline

Git is the implementation record.

Use current branch state before modification.

Stage only intended files.

Do not use broad staging when unrelated generated files are dirty.

Run:

`git diff --check`

before commit.

Use explicit commit messages tied to the implemented section.

Do not claim a commit exists until Git proves it.

---

## 49. VERSION_REFERENCES.json

`VERSION_REFERENCES.json` is a reference inventory.

It is not version authority.

Do not silently stage it during unrelated subsection commits.

Regenerate and reconcile it deliberately when required by the appropriate
completion surface.

Inventory != authority.

---

## 50. Fast-Gate Discipline

For a bounded subsection, run:

1. subsection validator;
2. subsection unit tests;
3. `git diff --check`;
4. `git status --short`.

Run aggregate validation at defined closure points or for explicit
cross-section diagnosis.

Fast gate != promotion.

---

## 51. Backward Compatibility

Historical v39 and v40 surfaces may remain for provenance.

New native-v41 implementation must not silently reintroduce them as active
authority.

Compatibility must preserve native-v41 identity.

Historical artifact != active implementation.

---

## 52. Documentation After Change

A substantive implementation change after R7-J invalidates the documentation
freeze until stability is revalidated.

Documentation-only correction does not automatically imply implementation
instability.

The distinction must remain explicit.

Implementation change -> stability revalidation.

Documentation clarification -> bounded documentation validation.

---

## 53. Promotion Boundary for Developers

Developers may implement and validate candidate state.

They do not promote main merely by completing implementation.

No validator promotes main.

No receipt promotes main.

No documentation promotes main.

Canonical promotion remains Human-Gated.

---

## 54. Developer Closure

The stabilized native-v41 implementation has an explicit development and
extension discipline.

A developer can locate ownership, extend the smallest correct surface, preserve
identity and provenance, validate the change, classify failures, and avoid
authority drift.

This guide documents implementation and extension.

It does not redefine architecture.

It does not grant authority.

It does not claim promotion.

DEVELOPER GUIDE COMPLETE.

R7-G owns the Audit Guide.
