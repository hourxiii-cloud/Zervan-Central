# R4-I — Runtime-State Continuity / Cross-Operation Integrity

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R4-I
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R4-I validates continuity across native-v41 Runtime State Operations.

R4-I does not introduce another analytical operation.

R4-I verifies that independently valid runtime operations remain mutually
coherent when composed.

Local correctness is insufficient if cross-operation continuity breaks.

Operation PASS != chain PASS.

---

## 1. Source Boundary

The source defines Tranche 6 Runtime State Operations as:

- hydration;
- restriction;
- constriction;
- collapse;
- landing;
- reflight;
- closure;
- replay;
- Scar Replay.

Native Ring 3 already owns the bounded Hydration handoff.

Native Ring 4 implements:

- R4-A Restriction / Constriction;
- R4-B Collapse Boundary;
- R4-C Landing Witness;
- R4-D Reflight Trigger;
- R4-E Post-Convergence Closure / Closing Witness;
- R4-F Replay Envelope;
- R4-G Scar Record;
- R4-H Scar Replay.

R4-I validates continuity across that implemented runtime surface.

The source does not require a separately named
Runtime-State Continuity Record.

That record is native implementation structure used to validate source
invariants.

Implementation structure != new doctrine.

---

## 2. Governing Integrity Rule

The same Room Object must remain identifiable across runtime operations.

Object identity may not drift merely because:

- supported states narrow;
- Collapse occurs;
- movement lands;
- Reflight becomes eligible;
- an interval closes;
- history is replayed;
- a Scar is recorded;
- Scar history is revisited.

Runtime change != object replacement.

---

## 3. State-Domain Separation

Room state, representation state, and execution state MUST remain distinct.

R4-I explicitly rejects conflation of:

- Room lifecycle state;
- representation / observational state;
- execution / movement state.

Room state != representation state.

Room state != execution state.

Representation state != execution state.

A transition in one domain does not silently mutate another domain.

---

## 4. Runtime Operation Order

R4-I recognizes canonical Ring 4 operation order:

1. `R4-A`
2. `R4-B`
3. `R4-C`
4. `R4-D`
5. `R4-E`
6. `R4-F`
7. `R4-G`
8. `R4-H`

A Runtime-State Continuity Record may contain a valid ordered subsequence.

Operations MUST NOT appear out of canonical order.

Operations MUST NOT appear more than once in one continuity chain unless a
separately identified later operation instance is represented by a distinct
continuity record.

Ordering != mandatory execution of every operation.

---

## 5. Runtime-State Continuity Record

Every Runtime-State Continuity Record MUST preserve:

- `continuity_record_id`;
- canonical `object_id`;
- ordered runtime operation bindings;
- Room-state reference;
- representation-state reference;
- execution-state reference;
- evidence-boundary reference;
- evidence-ceiling reference;
- Cartography reference;
- Stick reference;
- lineage reference;
- provenance route;
- continuity status;
- blocking reasons;
- Governance reference;
- authorization reference;
- Human Gate reference where applicable;
- validation time.

Each runtime operation binding MUST preserve:

- operation identifier;
- artifact reference;
- bound object identity;
- input coordinate reference where applicable;
- output coordinate reference where applicable;
- evidence-boundary reference;
- evidence-ceiling reference;
- lineage reference;
- provenance reference.

---

## 6. Continuity Identity

Native-v41 `continuity_record_id` is deterministic SHA-512 over the complete
Runtime-State Continuity Record except its own ID.

A material change to:

- object identity;
- operation order;
- operation binding;
- coordinates;
- evidence boundary;
- evidence ceiling;
- state-domain references;
- lineage;
- Cartography;
- Stick;
- provenance;
- continuity status

changes continuity identity.

Continuity Record identity is not Room Object identity.

---

## 7. Object Identity Continuity

Every runtime operation binding MUST identify the same canonical `object_id`
unless an independently governed distinct-object transition has already
established another Room outside this continuity chain.

R4-I does not perform that distinct-object transition.

Within one continuity record:

one chain = one Room Object.

Object mismatch = continuity failure.

---

## 8. Origin Continuity

Runtime operations do not manufacture a new Origin.

Restriction does not create Origin.

Collapse does not create Origin.

Landing does not create Origin.

Reflight does not create Origin.

Closure does not create Origin.

Replay does not create Origin.

Scar does not create Origin.

Scar Replay does not create Origin.

Runtime operation != genesis.

---

## 9. Representation Continuity

Representation may turn while object identity remains fixed.

A runtime operation may bind a different valid representation when separately
authorized and attributable.

Representation change MUST preserve transform history.

Representation change != Room replacement.

No silent default substitution.

---

## 10. Coordinate Continuity

Where an operation exposes coordinates, those coordinates MUST remain
attributably connected through Cartography and Stick.

Landing preserves coordinates.

Closure preserves replay coordinates.

Replay reopens preserved coordinates.

Scar preserves historical coordinates.

Scar Replay revisits preserved historical coordinates.

Approximate reconstruction is not continuity.

---

## 11. Cartography Continuity

Cartography remains the navigational substrate across runtime operations.

R4-I verifies that operation transitions do not silently:

- erase historical geometry;
- discard Collapse Boundaries;
- discard unresolved terrain;
- lose replay coordinates;
- lose Scar coordinates;
- lose return routes.

Runtime evolution may add geometry.

Runtime evolution MUST NOT silently destroy attributable geometry.

---

## 12. Stick Continuity

Stick continuity MUST survive all runtime operations.

The system must remain able to trace:

Room Object
-> representation
-> operation
-> evidence
-> coordinate
-> finding/effect
-> return/replay route.

Stick break = continuity failure.

---

## 13. Evidence Boundary Continuity

Evidence boundaries MUST remain attributable across operation transitions.

A later operation may use a changed evidence boundary only when that change is
separately attributable.

No runtime operation may silently broaden historical evidence access.

Current boundary != historical boundary.

Boundary change != retroactive evidence use.

---

## 14. Evidence Ceiling Continuity

Evidence ceilings MUST remain attributable across runtime transitions.

Changed ceiling requires attributable change.

A later higher ceiling does not retroactively elevate an earlier finding.

Historical claim authority remains historical.

Runtime continuity != retrospective promotion.

---

## 15. Restriction / Constriction Continuity

Restriction and Constriction narrow supported states.

Subsequent operations MUST preserve that narrowing history.

Landing does not undo narrowing.

Closure does not undo narrowing.

Replay does not erase narrowing.

Scar does not overwrite narrowing.

Scar Replay does not rewrite narrowing history.

---

## 16. Collapse Continuity

Collapse remains an attributable historical refinement event.

Subsequent operations MUST preserve:

- Collapse justification;
- governing evidence;
- removed possibilities;
- retained possibilities;
- deferred possibilities;
- surviving uncertainty;
- frontier;
- return route.

Collapse history survives Landing, Closure, Replay, Scar, and Scar Replay.

---

## 17. Landing Continuity

Landing stops movement without ending occupation.

Subsequent operations MUST NOT reinterpret Landing as:

- EXITED;
- deleted;
- closed by implication;
- new Room;
- reset state.

Landing preserves the state required for later closure, Reflight, and Replay.

---

## 18. Reflight Continuity

Reflight Trigger establishes eligibility for renewed movement.

Trigger does not execute movement.

Subsequent continuity MUST preserve:

- trigger basis;
- evidence;
- prior landed state;
- same Room identity;
- authorization boundaries.

Trigger != execution.

---

## 19. Closure Continuity

Closing Witness closes the current operational interval while preserving:

- Room identity;
- lineage;
- representation state;
- replay coordinates;
- unresolved terrain;
- evidence history.

Closure does not destroy Replay capability.

Closure does not erase future Reflight eligibility where separately valid.

---

## 20. Replay Continuity

Replay reopens the same Room at a preserved observational coordinate.

Replay MUST preserve historical:

- question;
- inquiry envelope;
- Zone;
- Space;
- transform;
- evidence use;
- movement;
- restrictions;
- Collapse;
- findings;
- rendering;
- return route.

Replay reconstructing an approximation = continuity failure.

---

## 21. Scar Continuity

Scar records evidence that Terrain previously affected movement.

Scar MUST remain attached to:

- the same Room;
- attributable Terrain;
- prior movement;
- effect evidence;
- historical coordinate;
- provenance.

Scar does not replace the underlying history.

---

## 22. Scar Replay Continuity

Scar Replay preserves both:

- the original Scar;
- the Replay substrate.

Replay, summarize, continue, branch, challenge, and ignore-with-evidence MUST
remain attributable to historical state.

Challenge does not delete history.

Ignore-with-evidence does not delete history.

Continue does not bypass Reflight Trigger.

Branch does not manufacture distinct-object identity.

---

## 23. Provenance Continuity

Every operation transition MUST preserve attributable provenance.

Provenance cannot disappear merely because analytical state changes.

Later interpretation MUST NOT overwrite earlier provenance.

No Compression Out applies to provenance history.

---

## 24. Lineage Continuity

Lineage remains continuous through runtime-state changes.

Closure preserves lineage.

Replay consumes preserved lineage.

Scar attaches to lineage.

Scar Replay preserves lineage.

A chain that cannot identify its historical route is not continuous.

---

## 25. Authority Continuity

Runtime operations do not accumulate authority merely through sequence.

Restriction authority does not become Collapse authority.

Collapse does not become closure authority.

Closure does not become Replay authority.

Replay does not become Scar Replay authority.

Technical success != governing authority.

Authority NONE remains NONE unless valid governing state resolves otherwise.

Human Gate remains separately attributable.

---

## 26. Ownership Continuity

Runtime composition MUST NOT cause one component to silently absorb another
component's responsibility.

Registry remains Registry.

Governance remains Governance.

Audit remains Audit.

TOC remains TOC.

Capabilities remain bounded capabilities.

Raven remains rendering / forward translation.

Human Gate remains Human Gate.

Composition != ownership collapse.

---

## 27. No State Conflation

R4-I MUST reject any model in which:

- Room lifecycle state is treated as representation state;
- representation state is treated as execution state;
- execution state is treated as Room lifecycle state;
- Landing automatically means SEALED;
- Replay automatically means REOPENED lifecycle transition;
- Reflight Trigger automatically means ACTIVE;
- Closing Witness automatically mutates Registry state.

State-domain conflation is a constitutional runtime defect.

---

## 28. Continuity Status

R4-I defines:

- `VALID`;
- `BLOCKED`.

`VALID` means the represented runtime operation chain preserves required
cross-operation invariants.

`BLOCKED` means one or more continuity invariants cannot be established.

VALID != analytical truth.

VALID != canonical promotion.

BLOCKED != nonexistent Room.

---

## 29. Fail Closed

If identity, coordinate, lineage, evidence boundary, evidence ceiling, Stick, or
provenance continuity cannot be established, the continuity chain is BLOCKED.

Do not guess the missing link.

Do not reconstruct an approximate link.

Do not silently repair history.

Surface the break.

---

## 30. R4-J Boundary

R4-I validates cross-operation integrity.

R4-I does not close Ring 4.

R4-J owns aggregate Ring 4 closure.

R4-I PASS is necessary but not sufficient for Ring 4 aggregate closure.

---

## 31. Failure Conditions

R4-I MUST reject:

- operation chain with mismatched Room identity;
- operation chain out of canonical order;
- duplicate operation identifiers in one continuity chain;
- empty operation chain;
- Room / representation / execution state conflation;
- missing evidence boundary;
- missing evidence ceiling;
- missing Cartography;
- missing Stick;
- missing lineage;
- missing provenance;
- coordinate continuity reconstructed approximately;
- historical evidence boundary silently broadened;
- historical evidence ceiling silently promoted;
- Landing interpreted as EXITED;
- Reflight Trigger interpreted as execution;
- Closing Witness interpreted as lifecycle mutation;
- Replay interpreted as duplicate Room;
- Scar interpreted as confidence;
- Scar Replay deleting or replacing Scar history;
- runtime sequence accumulating unauthorized authority;
- component ownership silently collapsing;
- BLOCKED status without blocking reason.

---

## 32. R4-I Lock

Operation PASS != chain PASS.

Implementation structure != new doctrine.

Runtime change != object replacement.

Room state != representation state.

Room state != execution state.

Representation state != execution state.

A transition in one domain does not silently mutate another domain.

Operations MUST NOT appear out of canonical order.

Ordering != mandatory execution of every operation.

one chain = one Room Object.

Object mismatch = continuity failure.

Runtime operation != genesis.

Representation change != Room replacement.

No silent default substitution.

Approximate reconstruction is not continuity.

Stick break = continuity failure.

No runtime operation may silently broaden historical evidence access.

Boundary change != retroactive evidence use.

Runtime continuity != retrospective promotion.

Landing does not undo narrowing.

Closure does not undo narrowing.

Replay does not erase narrowing.

Collapse history survives Landing, Closure, Replay, Scar, and Scar Replay.

Landing stops movement without ending occupation.

Trigger != execution.

Closure does not destroy Replay capability.

Replay reconstructing an approximation = continuity failure.

Scar does not replace the underlying history.

Challenge does not delete history.

Ignore-with-evidence does not delete history.

Continue does not bypass Reflight Trigger.

Branch does not manufacture distinct-object identity.

No Compression Out applies to provenance history.

A chain that cannot identify its historical route is not continuous.

Runtime operations do not accumulate authority merely through sequence.

Technical success != governing authority.

Composition != ownership collapse.

State-domain conflation is a constitutional runtime defect.

VALID != analytical truth.

VALID != canonical promotion.

BLOCKED != nonexistent Room.

Do not guess the missing link.

Do not reconstruct an approximate link.

Do not silently repair history.

Surface the break.

R4-J owns aggregate Ring 4 closure.

R4-I PASS is necessary but not sufficient for Ring 4 aggregate closure.
