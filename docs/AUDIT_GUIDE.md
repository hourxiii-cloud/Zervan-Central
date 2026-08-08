# Zervan v41 Audit Guide

Status: CONTROLLED CANDIDATE DOCUMENTATION
Ring: R7-G
Responsibility: VERIFICATION / REPLACEMENT / RESILIENCE / PROVENANCE / COMPLETION CRITERIA
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Stability Baseline: ae8dd9e22a34589f546f64ed452c0eee976cf299
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 1. Purpose

This guide defines how native Zervan v41 is independently verified.

Audit verifies implementation state.

Audit does not create implementation.

Audit does not replace Governance, Registry, runtime operation, or Human Gate.

Current Git remains implementation truth.

---

## 2. Audit Objective

Audit determines whether the implemented system can demonstrate:

- identity continuity;
- state integrity;
- provenance;
- boundary preservation;
- replay fidelity;
- replacement correctness;
- resilience;
- representation independence;
- completion evidence;
- authority separation.

Audit asks whether the system can prove what it claims to have done.

---

## 3. Evidence First

Audit begins from repository and runtime evidence.

Do not infer completion from documentation alone.

Do not infer correctness from a hash alone.

Do not infer authority from a receipt alone.

Do not infer truth from successful validation alone.

Evidence must remain attributable.

---

## 4. Audit Source Order

For candidate-state audit, inspect:

1. `VERSION`
2. `VERSION.json`
3. `VERSION_AUTHORITY.md`
4. native-v41 entry surfaces
5. implementation contracts
6. schemas
7. validators
8. tests
9. receipts
10. documentation
11. Git history

Source order does not eliminate the need to resolve collisions.

---

## 5. Version Verification

Verify that native identity resolves consistently to:

`vTemporal.41.0`

Verify implementation identity:

`v41 Complete`

Verify promotion state:

`CANDIDATE`

Verify canonical state remains false until authorized promotion.

Version identity and promotion state must remain separate.

---

## 6. Authority Verification

Verify:

Authority: NONE

Human Gate: ACTIVE

External Runtime: DISABLED

External Action: DISABLED

System Population: DISALLOWED

Canonical Mutation: HUMAN_GATE_ONLY

No subordinate receipt, validator, renderer, or analytical stage may override
these boundaries.

---

## 7. Room Identity Verification

Verify that the Room remains one analytical object through ordinary changes in:

- perspective;
- Zone;
- Space;
- representation;
- rendering;
- restriction;
- replay.

Identity fracture without distinct-object evidence is an audit failure.

---

## 8. Distinct Object Verification

When a distinct object is asserted, verify affirmative identity evidence.

Allowed identity outcomes remain:

- SAME_OBJECT;
- DISTINCT_OBJECT;
- UNRESOLVED.

Audit must reject forced Boolean resolution where evidence remains unresolved.

---

## 9. Genesis and Revision Verification

Verify Genesis establishes object identity.

Verify Revision modifies the governed definition of the same object.

Verify Revision does not silently create new Genesis.

Verify Branch preserves lineage.

Verify lineage remains reconstructible.

---

## 10. Cryptographic Verification

Verify required SHA-512 identities are deterministic.

Verify serialization is stable where required.

Verify changed hashes correspond to material changed inputs.

Hash != truth.

Signature != correctness.

Integrity != semantic correctness.

---

## 11. Operational Geography Verification

Verify the implementation preserves the declared geography:

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

Audit should be able to determine where an operation occurred.

---

## 12. Qualification Verification

Verify qualification precedes normal analysis.

Verify request readiness does not silently substitute for Room readiness.

Verify qualified state does not silently imply every operation is authorized.

Verify blocked, provisional, degraded, and rejected outcomes remain available
where required.

---

## 13. Occupancy Verification

Verify occupancy state is distinct from Room lifecycle.

Verify presence does not grant ownership.

Verify presence does not grant authority.

Verify exit does not erase Room state.

---

## 14. Question Contract Verification

Verify recurring inquiries use the governed Question Contract where required.

Verify material semantic changes produce a new version.

Verify human and machine execution preserve equivalent question semantics.

Verify Question Contract execution remains read-only.

Question != authority.

---

## 15. Evidence Boundary Verification

Verify analytical inputs remain inside the governed evidence boundary.

Technical reachability outside the boundary must not silently become analytical
admissibility.

Verify boundary changes are explicit and attributable.

---

## 16. Evidence Ceiling Verification

Verify claims remain at or below the evidence ceiling.

Audit should test whether rendering, audience selection, personalization, or
decision-option generation can improperly raise claim strength.

They must not.

---

## 17. Capability Routing Verification

Verify proportional capability routing.

Need determines force.

Question determines mission.

Evidence determines escalation.

Audit should reject mandatory escalation caused only by capability availability.

---

## 18. Formation Verification

Verify Scale and Formation remain separate.

Verify Formation changes preserve trigger and justification.

Verify escalation does not automatically imply Swarm or another larger
Formation.

---

## 19. Hydration Verification

Verify hydration remains mission-required.

Identity may travel while payload remains at rest.

Audit should confirm that data availability does not create blanket payload
release.

---

## 20. Restriction Verification

Verify restricted content remains existence-aware.

Restricted != nonexistent.

Verify constriction cannot silently widen downstream.

Verify exclusions remain attributable.

---

## 21. Collapse Verification

Verify Collapse preserves:

- identity;
- evidence;
- route;
- constraints;
- provenance.

Collapse must not silently become:

- authority;
- publication;
- new Room;
- promotion.

---

## 22. Landing Verification

Verify Landing preserves enough state for continuation and audit.

Applicable state includes:

- Room identity;
- revision;
- question;
- orientation;
- evidence boundary;
- evidence ceiling;
- unresolved state;
- provenance.

Landing != Replay.

---

## 23. Reflight Verification

Verify Reflight has an explicit trigger.

Verify trigger and justification remain attributable.

Verify Reflight does not silently rebuild the object or create a new Room.

---

## 24. Replay Verification

Verify Replay returns to a historical observational coordinate.

Verify Replay does not silently apply current defaults.

Verify Replay does not recreate Genesis.

Verify Replay does not mutate the historical record.

Replay fidelity is an audit requirement.

---

## 25. Scar Verification

Verify Scar preserves meaningful unresolved or failed conditions.

Later successful operation must not erase prior Scar evidence.

Verify Scar remains attributable and replayable where supported.

Failure is evidence.

---

## 26. Representation Independence Verification

Verify behavior survives representation changes without identity loss.

Audit across materially different representations where possible.

Representation change must not alter semantic identity merely because format
changes.

---

## 27. Replacement Verification

Replacement testing asks whether one implementation component can be replaced
without violating the contract it owns.

Replacement must preserve:

- interface;
- governed semantics;
- identity expectations;
- provenance;
- boundary behavior;
- failure behavior.

Replacement success is evidence of implementation separation.

---

## 28. Resilience Verification

Resilience testing asks whether the system preserves governed state under
failure, restart, replay, replacement, and constrained operation.

Resilience does not mean every operation succeeds.

A correct blocked or degraded result may demonstrate greater resilience than an
invented success.

---

## 29. Pipeline Verification

Verify the native pipeline:

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

Verify no stage silently absorbs the ownership of another stage.

Verify authority does not move upstream.

---

## 30. PMC Verification

Verify PMC performs bounded analytical computation.

Verify PMC remains evidence-bound and ceiling-bound.

Verify PMC does not own publication or Human Gate authority.

---

## 31. CCR Verification

Verify CCR preserves deterministic candidate commitment.

Audit:

- candidate;
- null result;
- rejected alternatives;
- uncertainty;
- evidence lineage;
- boundary;
- ceiling.

CCR must remain distinguishable from PMC and MC.

---

## 32. MC Verification

Verify MC governs output admissibility.

Verify MC does not silently recompute epistemic truth.

Verify MC preserves CCR history.

---

## 33. Raven Verification

Verify Raven renders governed analytical state.

Verify Raven does not alter evidence, identity, provenance, evidence boundary, or
evidence ceiling.

Report != Room.

Rendering != truth creation.

---

## 34. Human Gate Verification

Verify authority-bearing decisions remain at Human Gate.

Verify:

approval != execution.

Verify no validator, report, recommendation, or receipt performs canonical
promotion by itself.

---

## 35. Provenance Verification

Every meaningful transition should be traceable.

Audit provenance for:

- source;
- identity;
- governing contract;
- transformation;
- state transition;
- output;
- failure;
- replacement;
- replay;
- decision lineage.

Provenance != endorsement.

---

## 36. Transition Verification

Verify R7-I records transition accounting without performing promotion.

Transition accounting != promotion.

Verify historical canonical baseline remains preserved.

Verify future transition remains unperformed until explicit authorization.

---

## 37. Stability Verification

Verify R7-J identifies a committed baseline.

Verify the stability baseline commit exists in Git.

Verify documentation is bound to that baseline.

Verify substantive implementation change after baseline would require stability
revalidation.

Stability != completeness.

---

## 38. Documentation Verification

Verify documentation ownership remains separated.

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

No single documentation surface should silently become a replacement canonical
body.

---

## 39. Failure Classification

Audit uses the Ring 6 failure taxonomy:

- `INNER_INVARIANT_CONTRADICTION`
- `OUTER_IMPLEMENTATION_DEFECT`
- `VALIDATOR_DEFECT`
- `COVERAGE_GAP`
- `SOURCE_COLLISION`
- `UNRESOLVED_REQUIRED_SURFACE`

Classification determines which layer may correctly change.

---

## 40. Validator Defect Audit

When validation fails, determine whether the validator correctly represents the
source.

A validator that demands nonexistent source wording is defective.

Correct implementation must not be rewritten solely to satisfy a defective
validator.

Preserve the failure and repair provenance.

---

## 41. Coverage Audit

Verify required behavior has explicit coverage.

Do not treat nearby tests as proof of direct coverage.

Coverage must map to the contract or behavior being claimed.

Coverage gap != implementation defect unless implementation is also wrong.

---

## 42. Source Collision Audit

When repository sources disagree:

1. preserve the collision;
2. identify each source;
3. determine ownership;
4. resolve authority;
5. repair only the correct surface;
6. rerun bounded validation.

Do not silently choose whichever source makes the test pass.

---

## 43. Replacement Test Criteria

A replacement test passes only when the replacement preserves all governed
behavior owned by the replaced component.

Test both success and rejection paths.

A replacement that produces the same happy-path output but loses provenance or
failure behavior does not pass.

---

## 44. Replay Test Criteria

Replay testing should verify:

- same Room identity;
- historical coordinate;
- historical boundaries;
- historical question where applicable;
- historical ceiling;
- historical exclusions;
- no silent present-default substitution.

Replay must be attributable.

---

## 45. Representation Test Criteria

Representation testing should compare at least materially distinct
representations.

Verify preservation of:

- identity;
- evidence meaning;
- boundary;
- ceiling;
- provenance;
- decision lineage.

Presentation may differ.

Governed meaning must not.

---

## 46. Resilience Test Criteria

Resilience tests should exercise:

- blocked input;
- partial evidence;
- restricted data;
- missing prerequisite;
- replay;
- replacement;
- restart or re-entry where supported;
- unresolved identity;
- validator failure.

Correct failure handling counts as system behavior.

---

## 47. Completion Criteria

A surface is complete only when its required:

- implementation;
- contract;
- schema where required;
- validation;
- tests;
- provenance;
- documentation where required

are present and mutually consistent.

Completion != promotion.

Completion != authority.

---

## 48. Ring Completion Criteria

Ring completion requires all owned subrings to satisfy their declared
obligations.

A deferred required surface blocks final closure.

A known deferred item must remain explicit.

Deferred != forgotten.

---

## 49. Fresh-Reader Criterion

A fresh reader must be able to recover candidate identity, operating boundaries,
documentation ownership, validation surfaces, and promotion posture from the
repository without private conversational context.

If private conversation is required, the package is incomplete.

---

## 50. Lossless-Collapse Criterion

Audit should verify that collapse has not discarded required:

- identity;
- capability;
- behavior;
- rationale;
- provenance;
- coordinates;
- transforms;
- contracts;
- tests;
- evidence boundaries;
- failure conditions.

Lossless collapse is preservation, not compression for convenience.

---

## 51. Historical Provenance Criterion

Historical v39 and v40 materials may remain.

Audit must verify they remain historical and are not silently reactivated as
native-v41 authority.

Historical artifact != active implementation.

---

## 52. Git Verification

Git history should support reconstruction of implementation progression.

Audit should inspect:

- intended files;
- commit boundaries;
- branch;
- commit lineage;
- uncommitted changes;
- generated inventory drift where relevant.

Do not claim a commit or promotion that Git does not prove.

---

## 53. VERSION_REFERENCES.json Audit

`VERSION_REFERENCES.json` is a reference inventory.

It is not version authority.

Audit should verify deliberate regeneration and reconciliation at the proper
completion point.

Unstaged inventory drift does not itself redefine active version identity.

---

## 54. Audit Independence

Audit may detect a defect.

Audit may classify a defect.

Audit may reject a claimed completion state.

Audit does not silently rewrite the owning implementation.

Repair returns to the owning layer.

Verification and implementation remain separate.

---

## 55. Audit Result States

Useful audit dispositions include:

PASS

FAIL

BLOCKED

SCARRED

UNRESOLVED

A result should reflect evidence rather than pressure to produce PASS.

Null or unresolved states are legitimate when evidence requires them.

---

## 56. Promotion Audit Boundary

Audit may determine whether a promotion package is complete.

Audit does not perform promotion.

Audit does not create Human Gate approval.

Audit does not mutate main.

Promotion remains separately governed.

---

## 57. Audit Closure

Native-v41 audit can verify:

- version identity;
- authority;
- Room continuity;
- object distinction;
- qualification;
- occupancy;
- Question Contract behavior;
- evidence boundaries and ceilings;
- routing;
- hydration;
- restriction;
- collapse;
- Landing;
- Reflight;
- Replay;
- Scar;
- representation independence;
- replacement;
- resilience;
- pipeline ownership;
- provenance;
- documentation;
- completion evidence.

This guide defines verification responsibility.

It does not absorb implementation ownership.

It does not perform promotion.

AUDIT GUIDE COMPLETE.

R7-H owns the Operations Guide.
