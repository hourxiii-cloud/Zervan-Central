# R4-H — Scar Replay

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R4-H
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R4-H defines native-v41 Scar Replay.

Scar Replay allows a future observer to:

- replay;
- summarize;
- continue;
- branch;
- challenge;
- ignore with evidence

without creating a new world merely to revisit the old one.

Scar Replay consumes preserved Scar evidence and Replay state.

Scar Replay does not erase historical movement.

Scar Replay does not clone the Room.

---

## 1. Dependency

R4-H consumes:

- complete Rings 1 through 3;
- R4-A Restriction / Constriction;
- R4-B Collapse Boundary;
- R4-C Landing Witness;
- R4-D Reflight Trigger;
- R4-E Closing Witness;
- R4-F Replay Envelope;
- R4-G Scar Record;
- canonical Room Object identity;
- preserved historical observational coordinate;
- historical question;
- historical representation;
- prior movement;
- evidence;
- recorded effects;
- Cartography;
- Stick continuity;
- provenance.

Scar Replay MUST preserve the Scar Record.

Scar Replay MUST NOT replace it.

---

## 2. Governing Source Rule

A Scar is evidence that Terrain has previously affected movement.

Scar Replay allows a future observer to:

- replay;
- summarize;
- continue;
- branch;
- challenge;
- ignore with evidence

without creating a new world merely to revisit the old one.

These six action classes are native-v41 Scar Replay actions.

---

## 3. Native Action Types

R4-H defines exactly:

- `REPLAY`;
- `SUMMARIZE`;
- `CONTINUE`;
- `BRANCH`;
- `CHALLENGE`;
- `IGNORE_WITH_EVIDENCE`.

No other action is silently inferred.

Action type != authority.

Action type != execution.

---

## 4. Scar Replay Record

Every Scar Replay Record MUST preserve:

- `scar_replay_id`;
- canonical `object_id`;
- Scar Record reference;
- Replay Envelope reference;
- observer reference;
- requested action;
- action basis;
- historical observational coordinate;
- historical question-contract reference;
- historical Zone reference;
- historical Space reference;
- historical transform references;
- prior movement references;
- Scar effect evidence references;
- recorded effect references;
- evidence boundary;
- evidence ceiling;
- Cartography reference;
- Stick reference;
- Reflight Trigger reference where applicable;
- branch-control reference where applicable;
- challenge evidence where applicable;
- ignore evidence where applicable;
- action eligibility;
- blocking reasons;
- Governance reference;
- authorization reference;
- Human Gate reference where applicable;
- provenance route;
- request time.

---

## 5. Scar Replay Identity

Native-v41 `scar_replay_id` is deterministic SHA-512 over the complete Scar
Replay Record except its own ID.

A material change to:

- Scar Record;
- Replay Envelope;
- observer;
- action;
- action basis;
- coordinate;
- question;
- representation;
- movement;
- evidence;
- Reflight reference;
- branch control;
- challenge evidence;
- ignore evidence;
- eligibility

changes Scar Replay identity.

Scar Replay identity is not Room Object identity.

Scar Replay identity is not Scar Record identity.

Scar Replay identity is not Replay Envelope identity.

---

## 6. Same Object

Scar Replay revisits historical state of the same analytical object.

Scar Replay does not create a duplicate Room merely because a prior Scar is
being reconsidered.

Revisit != new world.

Historical observation != new object.

Scar Replay != new Room.

---

## 7. Future Observer

Scar Replay is explicitly future-observer capable.

The observer may differ from the original capability or observer.

Observer change does not change Room identity.

Observer change does not erase historical perspective.

The new observer receives attributable historical coordinates rather than an
approximate reconstruction.

---

## 8. Historical Coordinate

Scar Replay MUST bind the preserved historical observational coordinate.

The observer returns to the attributable location where Terrain affected prior
movement.

Scar Replay does not guess where the Scar was.

Scar Replay does not regenerate the coordinate from prose.

Preserved coordinate != reconstructed coordinate.

---

## 9. Historical Question

Scar Replay preserves the historical question contract.

The future observer must be able to distinguish:

- the question active when the Scar formed;
- any current question;
- any later continuation question.

Historical question != present question.

Scar Replay MUST NOT rewrite the old question.

---

## 10. Historical Representation

Scar Replay preserves historical:

- Zone;
- Space;
- transforms.

A future observer may later turn the same object through another valid
representation.

The historical representation remains historical fact.

Current perspective MUST NOT overwrite prior perspective.

---

## 11. Prior Movement

Scar Replay preserves prior movement.

The observer must be able to recover:

- the movement that encountered Terrain;
- where movement was affected;
- how movement changed;
- the route after the effect;
- the return route where applicable.

Scar Replay MUST NOT reduce the journey to only a warning or conclusion.

---

## 12. Evidence and Effects

Scar Replay preserves:

- effect evidence;
- recorded effects;
- evidence boundary;
- evidence ceiling.

Historical effect != current conclusion.

Historical evidence remains historical evidence.

New evidence may be added only through a separately attributable operation.

---

## 13. REPLAY

`REPLAY` reopens the preserved observational coordinate through the existing
Replay Envelope.

REPLAY requires a Replay Envelope reference.

REPLAY does not create another Room.

REPLAY does not execute new analysis merely by reopening history.

Replay != Reflight.

---

## 14. SUMMARIZE

`SUMMARIZE` permits a bounded rendering of the preserved Scar history.

Summary MUST remain traceable to:

- Scar Record;
- Replay Envelope;
- movement;
- evidence;
- recorded effects;
- historical representation;
- provenance.

Summary != replacement.

Summary != deletion.

Summary != new canonical state.

No Compression Out.

The complete Scar history remains available behind the summary.

---

## 15. CONTINUE

`CONTINUE` means renewed analytical movement from the preserved historical
state.

CONTINUE requires a valid attributable Reflight Trigger reference.

Scar existence alone is insufficient.

Historical interest alone is insufficient.

CONTINUE != automatic Reflight.

Reflight Trigger first.

Continuation second.

---

## 16. BRANCH

`BRANCH` routes a Scar-informed continuation into existing branch controls.

Scar Replay does not itself mint branch identity.

BRANCH requires an attributable branch-control reference.

Branch semantics remain governed by existing Ring 1 and Ring 2 controls.

A same-object branch remains attached to the same Room lineage unless the
distinct-object test establishes otherwise.

Scar Replay BRANCH != new world.

Perspective alone != branch.

---

## 17. CHALLENGE

`CHALLENGE` permits a future observer to contest:

- the historical interpretation;
- the recorded effect;
- the evidence relationship;
- the significance of the Scar;
- the later use of the Scar.

CHALLENGE requires non-empty challenge evidence.

Challenge does not erase the original Scar.

Challenge does not overwrite prior evidence.

Challenge creates attributable analytical contest, not retrospective deletion.

---

## 18. IGNORE WITH EVIDENCE

`IGNORE_WITH_EVIDENCE` permits a future observer to decline using the Scar as a
routing constraint when evidence supports that choice.

IGNORE_WITH_EVIDENCE requires non-empty ignore evidence.

Ignoring the Scar does not delete it.

Ignoring the Scar does not make it nonexistent.

Ignoring the Scar does not rewrite the historical effect.

The Scar remains available for later audit, challenge, Replay, or comparison.

Ignore != erase.

Ignore != absent.

Ignore requires evidence.

---

## 19. Action Eligibility

R4-H defines:

- `ELIGIBLE`;
- `BLOCKED`.

`ELIGIBLE` means the requested Scar Replay action has the required preserved
state, evidence, controls, and references to be considered.

`BLOCKED` means the action cannot defensibly proceed under current evidence,
authorization, continuity, or required action-specific prerequisites.

ELIGIBLE != execution.

ELIGIBLE != authority.

BLOCKED != nonexistent Scar.

---

## 20. Action-Specific Requirements

R4-H MUST enforce:

- REPLAY requires Replay Envelope;
- SUMMARIZE requires preserved Scar and Replay provenance;
- CONTINUE requires Reflight Trigger;
- BRANCH requires branch-control reference;
- CHALLENGE requires challenge evidence;
- IGNORE_WITH_EVIDENCE requires ignore evidence.

No generic action request may bypass these requirements.

---

## 21. Scar Preservation

Every Scar Replay action preserves the original Scar Record reference.

Scar Replay does not mutate the historical Scar merely because a future
observer disagrees with it.

Historical record remains attributable.

Current interpretation may differ.

History != current interpretation.

---

## 22. Replay Preservation

Scar Replay binds the Replay Envelope where required to reopen historical
coordinates.

Replay preserves the analytical journey.

Scar Replay adds a Scar-aware future-observer operation on top of that preserved
journey.

Scar Replay MUST NOT reconstruct an approximation.

---

## 23. Cartography

Scar Replay preserves Cartography.

The Scar remains a historical navigational feature.

Future movement may add Cartography.

Future movement does not silently delete the prior Scar coordinate.

Historical geometry remains attributable.

---

## 24. Stick

Scar Replay MUST preserve the Stick.

The operation remains connected to:

- canonical Room identity;
- Origin;
- Scar;
- Replay Envelope;
- historical question;
- historical representation;
- movement;
- evidence;
- effect;
- coordinate;
- provenance.

Scar Replay MUST NOT sever analytical continuity.

---

## 25. Evidence Boundary

Scar Replay preserves the historical evidence boundary.

A future observer does not retroactively gain historical access merely because
the observer currently has broader access.

Historical evidence boundary remains historical fact.

Current access != historical evidence use.

---

## 26. Evidence Ceiling

Scar Replay preserves the historical evidence ceiling.

A new observer does not silently raise historical claim authority.

Current evidence ceiling may differ only through a separately attributable
operation.

Scar Replay != retrospective promotion.

---

## 27. Reflight Boundary

Scar Replay CONTINUE may consume a valid Reflight Trigger.

Other Scar Replay actions do not automatically authorize renewed movement.

REPLAY != CONTINUE.

SUMMARIZE != CONTINUE.

CHALLENGE != automatic CONTINUE.

IGNORE_WITH_EVIDENCE != automatic CONTINUE.

BRANCH routing still requires applicable movement authority.

---

## 28. Branch Boundary

Scar Replay can request branch routing.

It does not redefine branch identity.

It does not collapse same-object branch into distinct-object identity.

It does not manufacture a genuinely distinct Room.

Distinct object still requires affirmative evidence.

---

## 29. Hydration

Scar Replay does not authorize full-payload hydration.

Only verified mission-required historical territory may be hydrated for the
requested action.

Identity travels.

Payload rests.

Scar Replay != full reconstruction.

---

## 30. Governance

Governance remains active for every Scar Replay action.

Scar Replay does not create:

- decision authority;
- publication authority;
- execution authority;
- canonical promotion authority.

Historical access != governing authority.

---

## 31. Authorization

Technical ability to revisit a Scar does not create authorization.

Future-observer access remains bounded.

Scar Replay eligibility does not imply execution authorization.

ELIGIBLE != authorized execution.

---

## 32. Human Gate

Human Gate remains ACTIVE where applicable.

Scar Replay does not fabricate approval.

Scar Replay does not bypass Human Gate.

Scar Replay Record != Human Gate decision.

---

## 33. Lifecycle

Scar Replay Record creation does not itself mutate lifecycle.

Scar Replay does not silently transition:

- SEALED -> REOPENED;
- LANDED -> ACTIVE;
- READY -> ACTIVE.

Registry lifecycle changes remain separately attributable.

Scar Replay != lifecycle transition.

---

## 34. Publication Boundary

Scar Replay does not publish.

SUMMARIZE is not publication.

CHALLENGE is not publication.

IGNORE_WITH_EVIDENCE is not publication.

Scar Replay does not alter:

Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate

Scar Replay Record != publication record.

---

## 35. No Silent Deletion

No Scar Replay action deletes the original Scar.

Even IGNORE_WITH_EVIDENCE preserves:

- Scar identity;
- evidence;
- movement history;
- effect history;
- coordinate;
- provenance.

Historical evidence remains auditable.

---

## 36. No New World

Scar Replay exists specifically so historical Terrain can be revisited without
creating a new world merely to revisit the old one.

Replay the history.

Turn the object if justified.

Continue if triggered.

Branch if governed.

Challenge with evidence.

Ignore with evidence.

Do not clone reality.

---

## 37. Failure Conditions

R4-H MUST reject:

- Scar Replay without canonical Room identity;
- Scar Replay without Scar Record;
- Scar Replay without historical coordinate;
- Scar Replay without historical question;
- Scar Replay without representation context;
- Scar Replay without prior movement;
- Scar Replay without effect evidence;
- REPLAY without Replay Envelope;
- CONTINUE without Reflight Trigger;
- BRANCH without branch-control reference;
- CHALLENGE without challenge evidence;
- IGNORE_WITH_EVIDENCE without ignore evidence;
- BLOCKED action without blocking reason;
- Scar Replay that deletes Scar history;
- Scar Replay that reconstructs an approximate coordinate;
- Scar Replay that silently raises evidence ceiling;
- Scar Replay that creates a new Room merely to revisit history;
- Scar Replay used as lifecycle mutation;
- Scar Replay used as publication authority;
- Scar Replay used as full-payload hydration authority.

---

## 38. R4-H Lock

A Scar is evidence that Terrain has previously affected movement.

Scar Replay allows a future observer to replay, summarize, continue, branch,
challenge, or ignore with evidence without creating a new world merely to
revisit the old one.

These six action classes are native-v41 Scar Replay actions.

Action type != authority.

Action type != execution.

Scar Replay MUST preserve the Scar Record.

Scar Replay MUST NOT replace it.

Revisit != new world.

Historical observation != new object.

Scar Replay != new Room.

Observer change does not change Room identity.

Preserved coordinate != reconstructed coordinate.

Historical question != present question.

Current perspective MUST NOT overwrite prior perspective.

Scar Replay MUST NOT reduce the journey to only a warning or conclusion.

Historical effect != current conclusion.

REPLAY requires a Replay Envelope reference.

Replay != Reflight.

Summary != replacement.

Summary != deletion.

Summary != new canonical state.

No Compression Out.

CONTINUE requires a valid attributable Reflight Trigger reference.

Scar existence alone is insufficient.

CONTINUE != automatic Reflight.

Reflight Trigger first.

Continuation second.

Scar Replay does not itself mint branch identity.

BRANCH requires an attributable branch-control reference.

Scar Replay BRANCH != new world.

Perspective alone != branch.

CHALLENGE requires non-empty challenge evidence.

Challenge does not erase the original Scar.

IGNORE_WITH_EVIDENCE requires non-empty ignore evidence.

Ignoring the Scar does not delete it.

Ignoring the Scar does not make it nonexistent.

Ignore != erase.

Ignore != absent.

Ignore requires evidence.

ELIGIBLE != execution.

ELIGIBLE != authority.

BLOCKED != nonexistent Scar.

Historical record remains attributable.

Current interpretation may differ.

History != current interpretation.

Scar Replay MUST NOT reconstruct an approximation.

Historical geometry remains attributable.

Scar Replay MUST preserve the Stick.

Scar Replay MUST NOT sever analytical continuity.

Current access != historical evidence use.

Scar Replay != retrospective promotion.

REPLAY != CONTINUE.

SUMMARIZE != CONTINUE.

CHALLENGE != automatic CONTINUE.

IGNORE_WITH_EVIDENCE != automatic CONTINUE.

Distinct object still requires affirmative evidence.

Identity travels.

Payload rests.

Scar Replay != full reconstruction.

Historical access != governing authority.

ELIGIBLE != authorized execution.

Scar Replay Record != Human Gate decision.

Scar Replay != lifecycle transition.

SUMMARIZE is not publication.

CHALLENGE is not publication.

IGNORE_WITH_EVIDENCE is not publication.

Scar Replay Record != publication record.

No Scar Replay action deletes the original Scar.

Historical evidence remains auditable.

Do not clone reality.

R4-I owns Runtime-State Continuity / Cross-Operation Integrity.
