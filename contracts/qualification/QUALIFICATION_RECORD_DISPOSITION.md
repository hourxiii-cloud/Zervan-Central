# R3-B — Qualification Record / Disposition

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R3-B
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R3-B defines the Qualification Record and qualification disposition for a
Canonical Room Object.

The Qualification Record preserves what qualification actually observed,
tested, could not resolve, and concluded about mission fitness.

R3-B consumes:

- complete Rings 1 and 2;
- R3-A Qualification Request / Mission Fitness.

R3-B does not redefine the Qualification Request.

R3-B does not yet define:

- Room lifecycle transition;
- READY transition;
- formation selection;
- analytical occupation;
- capability mission execution;
- Goblin Signal propagation.

---

## 1. Qualification Record Principle

Qualification produces an attributable record.

The record preserves evidence and bounded findings.

The record does not erase uncertainty merely to obtain a disposition.

Disposition is evidence-bounded.

Disposition is not truth ownership.

---

## 2. Qualification Record

Every Qualification Record MUST preserve:

- `qualification_record_id`;
- `qualification_request_reference`;
- canonical `object_id`;
- `provisional_room_id`;
- Origin reference;
- Ingress reference;
- qualification mission;
- active question;
- qualification lead;
- participating capabilities;
- occupied Zone;
- occupied Space;
- included evidence;
- excluded evidence;
- evidence boundary;
- evidence ceiling;
- observed geometry;
- Cartographic changes;
- provenance anchors;
- uncertainty frontiers;
- unresolved contradictions;
- restricted or inaccessible surfaces;
- adjoining-object candidates;
- distinct-object test result;
- recommended formation or next reconnaissance action;
- qualification disposition;
- disposition basis;
- return coordinates;
- replay route;
- provenance route;
- completion time.

---

## 3. Qualification Record Identity

Native-v41 `qualification_record_id` is deterministic SHA-512 over the complete
declared Qualification Record except `qualification_record_id`.

A material change to qualification findings changes the Record identity.

Qualification Record identity is not Room Object identity.

Qualification Record identity is not Qualification Request identity.

---

## 4. Request Binding

Every Qualification Record MUST resolve to the Qualification Request that
authorized and bounded the qualification activity.

The Record may refine findings.

The Record MUST NOT silently broaden:

- mission;
- question;
- evidence boundary;
- evidence ceiling;
- prohibited assumptions;
- permitted representation.

Record != Request.

Finding != request mutation.

---

## 5. Object Identity

The Qualification Record preserves canonical `object_id`.

Qualification does not manufacture another Room merely because:

- evidence disagrees;
- geometry fractures;
- uncertainty remains;
- another perspective appears;
- qualification fails.

Distinct-object handling remains governed by the R1-F and R2-J contracts.

---

## 6. Provisional Room Identifier

The Record preserves `provisional_room_id` because qualification may have begun
against a provisional workflow coordinate.

The provisional identifier does not replace canonical object identity.

Provisional Room ID != object identity.

---

## 7. Qualification Mission and Question

The Record preserves the exact qualification mission and active question under
which observations were made.

Findings MUST remain attributable to that bounded inquiry.

A materially different mission or question requires another Qualification
Request rather than silent reinterpretation.

---

## 8. Qualification Lead and Participants

The Record preserves the qualification lead and participating capabilities.

Lead != truth owner.

Participant != authority.

Multiple participants may return independent observations.

Independent observations MUST NOT be forced into false consensus.

---

## 9. Qualification Occupation

The Record preserves the Zone and Space occupied during qualification.

Qualification occupation is bounded provisional presence for qualification.

It does not imply analytical occupation.

Qualification occupation != analytical occupation.

Presence != truth ownership.

---

## 10. Included and Excluded Evidence

Included and excluded evidence remain explicit.

Excluded != absent.

Restricted != absent.

The Record MUST NOT rewrite inaccessible evidence as nonexistent.

---

## 11. Evidence Boundary and Ceiling

The Qualification Record preserves the evidence boundary and evidence ceiling
under which qualification occurred.

A disposition MUST NOT exceed that evidence ceiling.

Qualification cannot manufacture a higher claim ceiling.

Disposition strength <= evidence support.

---

## 12. Observed Geometry

Qualification tests identity, boundary, provenance, geometry, fractures,
shadows, corners, instability, restricted objects, adjoining relationships, and
discriminating evidence needs.

Observed geometry records what qualification actually encountered.

Observed geometry != complete geometry.

---

## 13. Cartographic Changes

Cartography records qualification effects including geometry, uncertainty
frontiers, and return routes.

The Qualification Record preserves references to those Cartographic changes.

Qualification Record != Cartography.

---

## 14. Provenance Anchors

The Record preserves provenance anchors supporting qualification findings.

A finding without resolvable provenance remains bounded accordingly.

Provenance != endorsement.

---

## 15. Uncertainty Frontiers

Qualification MUST preserve uncertainty frontiers.

A QUALIFIED disposition may contain bounded uncertainty when the Room is still
sufficiently established for the declared mission and evidence ceiling.

QUALIFIED != complete certainty.

Unknown remains unknown.

---

## 16. Unresolved Contradictions

Unresolved contradictions MUST remain explicit.

Contradiction MUST NOT be averaged away or silently converted into confidence.

Repeating `.333333/.666667` unresolved patterns remain scar/error signals under
the controlling architecture.

Scar != confidence.

---

## 17. Restricted / Inaccessible Surfaces

Restricted or inaccessible surfaces remain explicit.

A restriction may lower mission fitness or evidence ceiling.

Restriction MUST NOT silently become absence.

Restricted != nonexistent.

---

## 18. Adjoining-Object Candidates

Qualification may identify adjoining-object candidates.

Candidate adjoining object != distinct object.

Only the governed distinct-object test may establish a distinct object.

Relationship signal != new Room.

---

## 19. Distinct-Object Test Result

The Qualification Record preserves one R1-F distinct-object result:

- `SAME_OBJECT`;
- `DISTINCT_OBJECT`;
- `UNRESOLVED`.

R3-B consumes that result.

R3-B does not redefine distinct-object semantics.

Perspective difference != distinct object.

---

## 20. Recommended Next Action

The Qualification Record preserves a recommended formation or next
reconnaissance action.

A recommendation is advisory.

Recommendation != formation selection.

Recommendation != execution.

TOC remains responsible for later proportional capability coordination.

---

## 21. Qualification Disposition

R3-B defines exactly four qualification dispositions:

- `QUALIFIED`;
- `PROVISIONAL`;
- `REJECTED`;
- `DEGRADED`.

No additional disposition may be silently invented.

---

## 22. QUALIFIED

`QUALIFIED` means the Room is sufficiently established for the declared mission
and evidence ceiling.

QUALIFIED does not mean:

- every fact is known;
- uncertainty is zero;
- every surface is reachable;
- publication is authorized;
- execution is authorized;
- Room lifecycle is READY;
- analytical occupation has begun.

QUALIFIED != READY.

QUALIFIED != ACTIVE.

QUALIFIED != publication authority.

QUALIFIED != execution authority.

---

## 23. PROVISIONAL

`PROVISIONAL` means qualification has produced bounded useful knowledge, but the
Room is not yet sufficiently established for the declared mission and evidence
ceiling.

The Record MUST preserve what remains unresolved and what evidence or
reconnaissance could discriminate.

PROVISIONAL != failure.

PROVISIONAL != QUALIFIED.

---

## 24. REJECTED

`REJECTED` means qualification failed for the declared qualification problem or
the candidate does not support treatment as a legitimate analytical object
under the current evidence and governing boundary.

REJECTED MUST preserve the reason and evidence basis.

Rejected != erased.

Rejected history remains provenance.

---

## 25. DEGRADED

`DEGRADED` means the Room remains identifiable, but current evidence, integrity,
access, or qualification conditions cannot support the operation previously or
currently sought.

DEGRADED MUST identify the degradation.

DEGRADED != nonexistent.

DEGRADED != REJECTED by default.

---

## 26. Disposition Basis

Every Qualification Record MUST preserve an explicit `disposition_basis`.

The basis explains why the evidence supports the selected disposition.

Disposition without basis is invalid.

Disposition basis MUST NOT invent unavailable evidence.

---

## 27. Return Coordinates and Replay Route

Qualification preserves return coordinates and replay route.

A later observer must be able to resolve where qualification occurred and how
to return to its preserved analytical coordinate.

Return coordinate != replay execution.

R3-B records replayability.

It does not execute Replay.

---

## 28. Registry Finalization Boundary

Registry finalizes or rejects Room qualification state downstream from the
qualification evidence.

R3-B records the qualification disposition.

R3-B does not itself perform the Room lifecycle transition.

Disposition != lifecycle mutation.

---

## 29. Goblin Signal Boundary

Goblin Signal later announces:

- qualification;
- rejection;
- instability;
- branch availability;
- need for further reconnaissance.

R3-B does not propagate those events.

Record != event propagation.

---

## 30. Formation / Occupation Boundary

Only after qualification state is finalized may formation selection and
analytical occupation proceed.

R3-B does not select formation.

R3-B does not establish analytical occupation.

Qualification Record != Formation Selection Record.

Qualification Record != Occupancy Witness.

---

## 31. Authority Boundary

Qualification disposition does not authorize:

- canonical mutation;
- publication;
- external execution;
- downstream action.

Authority remains governed by Ring 1.

Write capability != authority.

---

## 32. R3-B Lock

Qualification produces an attributable Record.

Record != Request.

Finding != request mutation.

Qualification Record identity is not Room Object identity.

Qualification Record identity is not Qualification Request identity.

Provisional Room ID != object identity.

Lead != truth owner.

Participant != authority.

Qualification occupation != analytical occupation.

Excluded != absent.

Restricted != absent.

Disposition strength <= evidence support.

Observed geometry != complete geometry.

Qualification Record != Cartography.

QUALIFIED != complete certainty.

Unknown remains unknown.

Scar != confidence.

Restricted != nonexistent.

Candidate adjoining object != distinct object.

Perspective difference != distinct object.

Recommendation != formation selection.

Recommendation != execution.

QUALIFIED / PROVISIONAL / REJECTED / DEGRADED are the complete R3-B
qualification disposition vocabulary.

QUALIFIED != READY.

QUALIFIED != ACTIVE.

QUALIFIED != publication authority.

QUALIFIED != execution authority.

PROVISIONAL != failure.

PROVISIONAL != QUALIFIED.

Rejected != erased.

DEGRADED != nonexistent.

DEGRADED != REJECTED by default.

Disposition != lifecycle mutation.

Record != event propagation.

Qualification Record != Formation Selection Record.

Qualification Record != Occupancy Witness.

Write capability != authority.

No Room lifecycle transition yet.

No formation selection yet.

No analytical occupation yet.
