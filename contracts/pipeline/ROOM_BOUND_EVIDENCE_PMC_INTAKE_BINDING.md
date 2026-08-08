# R5-B — Room-Bound Evidence -> PMC Intake Binding

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R5-B
Version: vTemporal.41.0
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

R5-B binds qualified Room-context evidence to PMC intake.

R5-B does not redefine PMC.

R5-B does not perform PMC collapse.

R5-B does not create candidate worlds.

R5-B establishes the attributable intake envelope through which PMC may consume
Room-bound evidence.

Binding != analysis.

Binding != truth.

Binding != authority.

---

## 1. Pipeline Position

Native-v41 sequence remains:

Evidence
-> PMC
-> CCR
-> MC
-> Raven
-> Human Gate

R5-B owns only:

Room-Bound Evidence
-> PMC Intake

R5-B does not implement PMC -> CCR.

R5-C owns PMC -> CCR.

---

## 2. Room-Bound Evidence

Evidence presented to PMC MUST remain bound to the Room context in which it is
admissible.

The intake binding MUST preserve:

- canonical Room Object identity;
- Room revision identity;
- Room state root;
- Authorized View Root;
- evidence references;
- evidence hashes / integrity references where available;
- evidence classes;
- evidence boundary;
- evidence ceiling / Maximum Justified Claim;
- observational coordinate or coordinate reference;
- representation / transform reference;
- lineage;
- unresolved states / contradictions;
- qualification reference;
- provenance route.

PMC receives bounded evidence context.

PMC does not become the owner of that context.

---

## 3. Canonical Room Identity

Every PMC intake binding MUST identify one canonical Room Object.

PMC intake MUST NOT silently combine evidence from unrelated Room Objects.

Cross-Room evidence requires separately attributable relationship or passageway
controls.

Similar evidence != same Room.

PMC consumption != Room identity mutation.

---

## 4. Revision and State Binding

PMC intake MUST preserve the Room revision and state root applicable when the
evidence was admitted.

Later Room state does not rewrite historical PMC intake.

Current Room state != historical intake state.

State reference != lifecycle ownership.

PMC does not mutate Registry state by consuming the binding.

---

## 5. Authorized View Binding

PMC intake MUST identify the Authorized View Root under which the evidence was
available.

Authorized View Root constrains visibility.

Authorized View Root does not create truth.

PMC MUST NOT infer restricted evidence that is absent from its authorized view.

Restricted != nonexistent.

Unavailable to PMC != nonexistent in the Room.

---

## 6. Evidence References

PMC intake uses attributable evidence references.

Evidence MUST NOT be silently replaced by narrative summary.

Where payload hydration is required, existing Hydration controls remain in
force.

Identity travels.

Payload rests.

PMC intake != full-payload hydration authority.

---

## 7. Evidence Integrity

Evidence integrity references MUST remain attributable.

Hash != truth.

Signature != correctness.

Integrity != semantic correctness.

A valid hash permits identity/integrity reasoning.

A valid hash does not certify the analytical claim carried by the evidence.

---

## 8. Evidence Classes

PMC distinguishes structural evidence from interpretive evidence.

Structural evidence may define:

- partitions;
- neighborhoods;
- topology;
- candidate routes;
- feasibility;
- boundary conditions.

Interpretive evidence may:

- weigh plausibility;
- reduce variance;
- express uncertainty.

Interpretive evidence MUST remain advisory.

Interpretation is not authority.

---

## 9. Pinned Inputs

PMC intake MUST identify pinned evidence inputs.

Pinned inputs may include:

- dataset identifiers;
- artifact identifiers;
- content hashes;
- immutable evidence references;
- deterministic parameter references.

Unpinned material is not valid native-v41 PMC intake.

Pinned != true.

Pinned != authoritative.

Pinned means attributable and replayable.

---

## 10. Evidence Boundary

PMC intake MUST preserve the evidence boundary.

PMC may evaluate only evidence admitted to the binding.

PMC MUST NOT silently broaden the evidence boundary.

Boundary change requires a separately attributable operation.

Current availability != historical admissibility.

---

## 11. Evidence Ceiling

PMC intake MUST preserve the evidence ceiling / Maximum Justified Claim.

PMC may reason only inside that ceiling.

PMC MUST NOT silently promote claim authority merely because evidence is
computationally convenient or strongly correlated.

Evidence ceiling != confidence score.

Confidence does not override claim ceiling.

---

## 12. Coordinates

PMC intake MUST preserve the relevant observational coordinate or coordinate
reference.

Coordinate binds evidence to analytical geography.

Coordinate != truth.

Coordinate != authority.

PMC may use coordinate context without owning Cartography.

Coordinate reference != Cartography ownership.

---

## 13. Representation / Transform

PMC intake MUST preserve the representation / transform under which evidence
was observed or admitted.

Representation may affect visibility.

Representation MUST NOT alter Room identity.

Representation MUST NOT silently broaden evidence access.

Perspective != evidence.

Perspective != authority.

---

## 14. Lineage

PMC intake MUST preserve evidence lineage back to the Room-bound source.

The lineage must support forward traceability into:

PMC
-> CCR
-> MC
-> Raven
-> Human Gate

PMC output that cannot identify its admitted evidence route is invalid for
native-v41 pipeline integration.

---

## 15. Unresolved States and Contradictions

PMC intake MUST preserve unresolved states, contradictions, ambiguity flags,
and known unknowns applicable to the evidence.

PMC MUST NOT convert missing resolution into certainty at intake.

Unknown remains unknown.

Contradiction remains attributable.

Admission != resolution.

---

## 16. Qualification

PMC intake MUST bind qualification state sufficient to establish that the Room
and evidence are operationally admissible for the requested analysis.

Qualification precedes analysis.

Qualification != analytical truth.

Qualification != PMC selection.

Qualification != authority.

---

## 17. Determinism

PMC intake MUST be reconstructible from attributable references.

Equivalent binding inputs MUST canonicalize deterministically.

No hidden defaults.

No hidden heuristics.

No silent substitution.

Replayability precedes downstream trust.

---

## 18. PMC Existing Semantics

R5-B preserves existing PMC semantics.

PMC may:

- evaluate plausible worlds;
- apply recursive constraint;
- rank plausibility;
- deny candidates;
- perform bounded epistemic collapse;
- emit replayable analytical artifacts.

PMC may not:

- authorize action;
- promote to canon by itself;
- certify authority;
- bypass CCR;
- bypass MC;
- assume evidence not present in the binding.

Room binding does not expand PMC ownership.

---

## 19. Intake Disposition

Native R5-B defines:

- `ADMISSIBLE`;
- `BLOCKED`.

`ADMISSIBLE` means the Room-bound evidence envelope contains sufficient
identity, integrity, boundary, coordinate, lineage, qualification, and
replayability information for PMC intake.

`BLOCKED` means the binding is insufficient or contradictory for defensible PMC
intake.

ADMISSIBLE != true.

ADMISSIBLE != PMC-selected.

ADMISSIBLE != action-authorized.

BLOCKED != evidence nonexistent.

---

## 20. Fail-Closed Conditions

R5-B MUST block intake when required bindings are absent, including:

- Room Object identity;
- Room revision identity;
- state root;
- Authorized View Root;
- evidence references;
- evidence classes;
- evidence boundary;
- evidence ceiling;
- coordinate reference;
- lineage;
- qualification reference;
- provenance.

R5-B MUST block intake when:

- evidence belongs to a different Room without explicit relationship control;
- restricted evidence is silently inferred;
- evidence boundary is silently broadened;
- evidence ceiling is silently raised;
- interpretive evidence is promoted to authority;
- unresolved contradiction is silently discarded;
- payload hydration is assumed without need;
- provenance is missing;
- reconstruction is impossible.

Fail closed.

Do not fabricate missing intake state.

---

## 21. Responsibility Boundary

Registry retains Room identity / state ownership.

Governance retains boundary / claim-ceiling ownership.

Audit retains verification responsibility.

Cartography remains Cartography.

PMC retains epistemic computation.

R5-B is an integration binding.

R5-B does not absorb any of those functions.

Binding != ownership.

---

## 22. Authority Boundary

PMC intake creates no authority.

PMC evaluation creates no action authority.

An admissible intake does not authorize:

- mutation;
- publication;
- external execution;
- canonical promotion;
- system population.

Authority remains NONE.

Human Gate remains ACTIVE.

---

## 23. No Compression Out

PMC intake MUST preserve independently relevant evidence references,
contradictions, unknowns, boundaries, transforms, and provenance.

A compact machine envelope may reference those structures.

It may not erase them.

Reference != compression out.

Envelope != summary substitution.

---

## 24. R5-B Lock

R5-B binds qualified Room-context evidence to PMC intake.

R5-B does not redefine PMC.

R5-B does not perform PMC collapse.

Binding != analysis.

Binding != truth.

Binding != authority.

PMC receives bounded evidence context.

PMC does not become the owner of that context.

Similar evidence != same Room.

Current Room state != historical intake state.

Authorized View Root constrains visibility.

Restricted != nonexistent.

Unavailable to PMC != nonexistent in the Room.

Evidence MUST NOT be silently replaced by narrative summary.

Identity travels.

Payload rests.

PMC intake != full-payload hydration authority.

Hash != truth.

Signature != correctness.

Integrity != semantic correctness.

Interpretive evidence MUST remain advisory.

Interpretation is not authority.

Unpinned material is not valid native-v41 PMC intake.

Pinned != true.

Pinned != authoritative.

PMC MUST NOT silently broaden the evidence boundary.

Evidence ceiling != confidence score.

Confidence does not override claim ceiling.

Coordinate != truth.

Coordinate != authority.

Coordinate reference != Cartography ownership.

Representation MUST NOT alter Room identity.

Perspective != evidence.

Perspective != authority.

Unknown remains unknown.

Admission != resolution.

Qualification precedes analysis.

Qualification != analytical truth.

Qualification != PMC selection.

No hidden defaults.

No silent substitution.

PMC may not authorize action.

PMC may not bypass CCR.

PMC may not bypass MC.

Room binding does not expand PMC ownership.

ADMISSIBLE != true.

ADMISSIBLE != PMC-selected.

ADMISSIBLE != action-authorized.

BLOCKED != evidence nonexistent.

Fail closed.

Do not fabricate missing intake state.

Binding != ownership.

Authority remains NONE.

Human Gate remains ACTIVE.

Reference != compression out.

Envelope != summary substitution.

R5-C owns PMC -> CCR Candidate Commitment Lineage.
