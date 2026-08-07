# R1-F — Revision, Branch, Merge, and Distinct-Object Semantics

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R1-F
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R1-F defines the relationships among revision, branch, merge, replay, and
genuinely distinct analytical objects.

R1-F consumes:

- R1-A Authority and Canonical Resolution;
- R1-B Version Identity and Promotion;
- R1-C Identity, Integrity, and Provenance;
- R1-D Manifest Architecture;
- R1-E State Roots and Authorized Views.

R1-F does not redefine them.

---

## 1. Core Separation

Revision, Branch, Merge, Replay, perspective change, historical state, and
distinct-object establishment are separate operations.

They MUST NOT be treated as interchangeable merely because each may create a
new record, State Root, Manifest, or lineage coordinate.

---

## 2. Revision

A Revision is an accepted definition-changing continuation of the same
analytical object.

Revision:

- preserves object continuity;
- preserves Genesis lineage;
- produces a new immutable Revision Manifest;
- references its predecessor;
- preserves provenance;
- does not rewrite prior Manifests;
- does not automatically create a Branch;
- does not create a new analytical object merely because definition changed.

Revision sequence is definition lineage.

State sequence is state lineage.

Revision sequence != State sequence.

---

## 3. Branch

A Branch is an alternate evidence-compatible lineage within the same
analytical object unless affirmative distinct-object evidence establishes
otherwise.

A Branch may preserve:

- an alternative hypothesis path;
- a historical-state continuation;
- a bounded inquiry;
- a challenged conclusion;
- an alternate evidence-compatible route;
- a controlled experimental continuation.

Branch creation MUST identify:

- parent Manifest reference;
- parent State Root;
- Branch identity;
- Branch reason;
- Branch nonce;
- creation time;
- authorization reference;
- provenance route.

Branch identity identifies alternate lineage.

Branch identity is not object identity.

Branch != new Room.

---

## 4. Branch Anchor

Every Branch begins at an immutable fork coordinate.

The fork coordinate consists, at minimum, of:

- parent Manifest reference;
- parent State Root.

The parent coordinate remains unchanged.

Branch movement creates new records downstream from that coordinate.

Branching MUST NOT mutate parent history.

---

## 5. Perspective Is Not Branch

A new:

- perspective;
- Bounded Zone;
- Bounded Space;
- Authorized View;
- observer;
- discipline;
- stakeholder;
- rendering;
- evidence exposure

is not automatically a Branch.

Representation change turns the same object.

Branching establishes alternate lineage.

Perspective != branch.

Authorized View != branch.

---

## 6. Historical State Is Not Branch

Multiple historical State Roots do not themselves establish Branches.

A linear sequence such as:

State 1 -> State 2 -> State 3

remains one lineage unless an explicit Branch operation forks from a preserved
coordinate.

Historical state != branch.

---

## 7. Distinct Object

A genuinely distinct analytical object is not created merely because:

- perspectives disagree;
- Branches diverge;
- questions differ;
- evidence visibility differs;
- stakeholders differ;
- disciplines differ;
- renderings differ;
- analytical conclusions differ.

A separate object requires affirmative evidence of distinctness.

At minimum, a distinct-object determination MUST record:

- evidence of distinctness;
- relationship to the source object;
- shared provenance;
- non-shared provenance;
- independent boundary;
- independent origin route where applicable;
- independent geometry or object structure;
- passageway conditions;
- contamination controls;
- return route;
- determination state;
- authorization reference.

A determination may be:

- SAME_OBJECT;
- DISTINCT_OBJECT;
- UNRESOLVED.

A DISTINCT_OBJECT determination establishes the requirement for an independent
Genesis lineage.

Distinct object != branch.

---

## 8. Merge

A Merge combines compatible lineage material under explicit provenance and
governance.

Merge MUST NOT silently overwrite either parent.

Every Merge MUST retain:

- left lineage reference;
- right lineage reference;
- left Manifest reference;
- right Manifest reference;
- left State Root;
- right State Root;
- common ancestry when known;
- Merge identity;
- Merge rationale;
- conflicts;
- unresolved differences;
- authorization reference;
- provenance route;
- creation time.

Silent merge is forbidden.

---

## 9. Same-Object Merge

Branches attached to the same analytical object may be reconciled without
creating a new analytical object merely because a Merge occurred.

A same-object Merge produces a new accepted lineage result.

Depending on what changed, acceptance may require:

- a new State Record;
- a new Revision Manifest;
- both;
- neither until the result crosses the applicable acceptance boundary.

R1-D and R1-E determine which lower-level records are required.

The Merge operation itself does not manufacture new object identity.

Same-object merge != new object.

---

## 10. Cross-Object Merge Boundary

Material belonging to genuinely distinct analytical objects MUST NOT be
silently collapsed into one identity.

Cross-object:

- comparison;
- correlation;
- passageway analysis;
- relationship analysis;
- combined rendering

may preserve references to both objects while their identities remain
independent.

Cross-object contact != identity collapse.

If evidence supports creation of a genuinely new synthesized analytical object,
that object requires:

- explicit DISTINCT_OBJECT determination;
- independent Genesis establishment;
- preserved references to source objects;
- preserved provenance;
- applicable authorization;
- Human Gate where required.

Merge convenience is not evidence of object identity.

---

## 11. Parent Preservation

Revision, Branch, and Merge preserve historical parents.

No such operation may:

- rewrite an accepted Genesis Manifest;
- rewrite an accepted Revision Manifest;
- rewrite historical State Records;
- erase parent State Roots;
- erase Branch ancestry;
- erase Merge parents;
- invent missing ancestry.

History accumulates.

---

## 12. Branch Identity

Branch identity is a deterministic SHA-512 identity over exactly:

- parent Manifest reference;
- parent State Root;
- Branch reason;
- Branch nonce.

The nonce deliberately separates independently requested Branches originating
from the same coordinate.

Canonical serialization follows the deterministic JSON rules established in
R1-E.

Branch identity identifies lineage only.

Branch identity MUST NOT be interpreted as Room or object identity.

---

## 13. Merge Identity

Merge identity is a deterministic SHA-512 identity over exactly:

- left lineage reference;
- right lineage reference;
- left State Root;
- right State Root;
- Merge rationale;
- Merge nonce.

Merge identity identifies the Merge event/result lineage.

Merge identity MUST NOT be interpreted as Room or object identity.

Parent ordering is preserved.

A -> B and B -> A are not silently treated as the same Merge record.

---

## 14. Authority and Human Gate

Branch and Merge creation are governed mutations.

Technical write capability does not authorize either operation.

Authorization is resolved under R1-A.

Where Human Gate applies:

Approval != execution.

Distinct-object establishment MUST NOT occur merely because a capability,
observer, renderer, or runtime prefers a simpler model.

---

## 15. Replay Boundary

Replay reopens a preserved historical coordinate.

Replay is not a Branch by default.

Replay becomes Branch only when an explicit Branch operation departs from the
reopened coordinate into alternate lineage.

Replay != duplicate world.

---

## 16. Supersession of Earlier Branch Semantics

Earlier candidate material stated that every Branch receives a new Room ID.

That rule is superseded for native v41.

The controlling native-v41 rule is:

A Branch remains attached to the same analytical object unless affirmative
distinct-object evidence establishes another object.

A genuinely distinct object receives independent Genesis lineage.

The historical rule remains provenance.

It is not active native-v41 semantics.

---

## 17. Merge Supersession Boundary

Earlier candidate material stated that Merge creates a new Room.

That rule is not retained as a universal native-v41 rule.

The controlling native-v41 rule is:

- Merge never overwrites parents.
- Same-object Merge remains associated with the same analytical object.
- Cross-object material retains independent identities.
- A genuinely new analytical object requires affirmative distinct-object
  evidence and independent Genesis establishment.

Merge alone is insufficient evidence for new object identity.

---

## 18. Failure Conditions

Invalid R1-F behavior includes:

- treating every Revision as a Branch;
- treating every Branch as a new Room;
- creating new object identity from perspective disagreement;
- treating every State Root as a Branch;
- treating every Authorized View as a Branch;
- overwriting Merge parents;
- silently collapsing distinct object identities;
- losing parent provenance;
- fabricating common ancestry;
- treating Merge identity as object identity;
- treating Branch identity as object identity;
- treating Replay as automatic Branch;
- treating Merge itself as proof of a new object.

---

## 19. R1-F Lock

Revision continues the same analytical object.

Branch preserves alternate lineage inside the same analytical object by
default.

Perspective is not Branch.

Authorized View is not Branch.

Historical State Root is not Branch.

Replay is not Branch by default.

Branch identity is not object identity.

Merge preserves every parent.

Same-object Merge remains the same analytical object.

Cross-object contact does not collapse identities.

A new analytical object requires affirmative distinct-object evidence and an
independent Genesis lineage.

No silent merge.

No parent overwrite.

No perspective cloning.
