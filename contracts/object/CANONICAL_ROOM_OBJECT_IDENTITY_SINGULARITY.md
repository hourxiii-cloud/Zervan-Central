# R2-A — Canonical Room Object Identity and Singularity

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R2-A
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R2-A defines the identity and singularity contract for the Canonical Room
Object.

R2-A consumes the complete Ring 1 substrate:

- R1-A Authority and Canonical Resolution;
- R1-B Version Identity and Promotion;
- R1-C Identity, Integrity, and Provenance;
- R1-D Manifest Architecture;
- R1-E State Roots and Authorized Views;
- R1-F Revision, Branch, Merge, and Distinct-Object Semantics.

R2-A does not redefine them.

R2-A does not yet define:

- Origin Establishment execution;
- Terrain;
- Territory;
- Bounded Zone;
- Bounded Space;
- Perspective / Representation Transform;
- Orientation;
- Cartography;
- Stick;
- Passageway.

Those remain downstream.

---

## 1. Canonical Room Object

The Canonical Room Object is the singular analytical object established for
the admitted informational world at the current legitimate level of collapse.

It is the coherent object against which bounded representations, analytical
state, lineage, observations, missions, and later renderings resolve.

A Canonical Room Object is not:

- a document;
- a report;
- a perspective;
- a Bounded Zone;
- a Bounded Space;
- a State Root;
- an Authorized View;
- a Branch;
- a Merge;
- a dataset copy;
- a conclusion.

THE ROOM IS ONE ANALYTICAL OBJECT.

---

## 2. Object Singularity

One legitimate analytical object has one canonical object identity.

The same object may later support:

- multiple Revision Manifests;
- multiple historical State Roots;
- multiple Authorized Views;
- alternate Branches;
- same-object Merges;
- multiple perspectives;
- multiple observers;
- multiple time windows;
- multiple renderings;
- multiple Zones;
- multiple Spaces.

None of those creates another object merely because representation, state,
definition, inquiry path, or observation changes.

ONE ROOM OBJECT.
MANY DECLARED REPRESENTATIONS.
ZERO SILENT CLONES.

---

## 3. Canonical Object Identity

The canonical object identity format is:

`sha512:<128 lowercase hexadecimal characters>`

Object identity is a deterministic SHA-512 identity over the immutable object
establishment preimage:

- Genesis Manifest reference;
- originating canonical content identity;
- object nonce.

The object nonce deliberately permits independently established analytical
objects to remain distinct even when related evidence or origin material is
shared.

Canonical serialization follows the deterministic JSON rules already locked
by Ring 1.

This construction is the native-v41 implementation mechanism for object
identity.

It does not redefine the R1-C content identity.

---

## 4. Object Identity Is Not Content Identity

Originating content identity answers:

> Which admitted bytes entered?

Object identity answers:

> Which singular analytical object was established from the governed
> establishment event?

Therefore:

Object identity != originating content identity.

The same origin material may participate in more than one analytical object
only when governance and distinct-object semantics legitimately establish
separate objects.

Shared evidence does not silently imply shared object identity.

---

## 5. Object Identity Is Not Manifest Identity

Genesis Manifest identity identifies the immutable establishment record bytes.

Canonical object identity identifies the analytical object established through
that Genesis lineage.

Therefore:

Manifest identity != object identity.

Revision Manifest creation does not replace object identity.

Manifest Pointer movement does not replace object identity.

---

## 6. Object Identity Is Not State Identity

State Root identifies canonical state under an accepted definition.

Object identity identifies the continuing analytical object whose state is
being represented.

Therefore:

State Root != object identity.

A new State Root does not create a new Room Object.

Historical State Roots remain states of the same object unless independent
distinct-object evidence establishes otherwise.

---

## 7. Object Identity Is Not Authorized-View Identity

Authorized View Root identifies a controlled projection of canonical state.

It does not identify another analytical object.

Therefore:

Authorized View Root != object identity.

Different visibility does not create different reality.

---

## 8. Object Identity Is Not Branch Identity

Branch identity identifies alternate lineage within the same object by
default.

Therefore:

Branch identity != object identity.

A Branch remains attached to the parent Canonical Room Object unless an
affirmative distinct-object determination establishes another object.

Branch divergence alone is insufficient.

---

## 9. Object Identity Is Not Merge Identity

Merge identity identifies a governed lineage reconciliation event/result.

Same-object Merge preserves the same canonical object identity.

Therefore:

Merge identity != object identity.

Merge convenience does not create a new object.

---

## 10. Revision Continuity

A Revision Manifest changes accepted definition while preserving the same
object unless distinct-object semantics establish otherwise.

Object identity persists across Revision Manifests.

Revision != replacement object.

---

## 11. State Continuity

Canonical object state may change repeatedly.

Object identity persists across legitimate state transitions.

State change != object replacement.

---

## 12. Representation Continuity

Perspective, discipline, observer, language, evidence access, scale, time
window, rendering, and later Zone/Space representation may change.

Object identity persists.

Representation changes how the object is encountered.

Representation does not manufacture another object.

TURN THE OBJECT.
DO NOT CLONE THE WORLD.

---

## 13. Observation Continuity

Every material observation may change what must thereafter be represented
about the analytical object.

Observation does not automatically replace object identity.

History accumulates against the continuing object.

The object may evolve without ceasing to be the same object.

Continuous identity does not mean frozen state.

---

## 14. Object Establishment Boundary

Object identity may be established only when the required Ring 1 identity,
provenance, manifest, authority, and lineage prerequisites are available.

R2-A defines identity structure.

R2-B will define the governed Origin -> Ingress -> Canonical Room Object
establishment operation.

R2-A MUST NOT fabricate an object merely because an object identifier can be
computed.

Computable != established.

---

## 15. Distinct-Object Boundary

A new canonical object identity is legitimate only when:

- the distinct-object test supports DISTINCT_OBJECT;
- an independent Genesis lineage is established;
- provenance to source material is preserved;
- applicable authorization is satisfied.

A new viewpoint, role, discipline, question, Branch, rendering, disagreement,
or State Root is insufficient.

Distinctness requires affirmative evidence.

---

## 16. Identity Persistence

Once legitimately established, canonical object identity remains invariant
through the object's continuing lineage.

The following MUST NOT change object identity by themselves:

- Revision;
- state transition;
- Authorized View;
- Branch;
- same-object Merge;
- Replay;
- perspective change;
- observer change;
- time-window change;
- rendering change;
- later Zone change;
- later Space change.

Identity persists.
History accumulates.

---

## 17. Replacement Boundary

If evidence establishes that a presumed object was incorrectly bounded, the
system MUST NOT silently rewrite its identity history.

Correction must preserve:

- the prior object identity;
- the evidence that challenged it;
- the distinct-object or replacement determination;
- provenance;
- applicable authorization;
- successor relationships.

R2-A does not yet define replacement workflow.

It prohibits silent identity substitution.

---

## 18. Object Reference Contract

Every downstream canonical structure that operates on a Room Object MUST carry
or resolve a canonical `object_id`.

A downstream structure may add its own identity.

It MUST NOT substitute that local identity for `object_id`.

Outer identity never redefines inner identity.

---

## 19. Forbidden Identity Collapses

The following collapses are forbidden:

`object_id = content_identity`

`object_id = manifest_identity`

`object_id = state_root`

`object_id = authorized_view_root`

`object_id = branch_id`

`object_id = merge_id`

`object_id = report_id`

`object_id = perspective_id`

unless byte equality occurs accidentally as an uninterpreted coincidence.

Semantic identity MUST still remain distinct.

---

## 20. R2-A Lock

THE ROOM IS ONE ANALYTICAL OBJECT.

Canonical Room Object identity is singular and persistent.

Object identity is established from immutable Genesis lineage, originating
content identity, and deliberate object separation.

Object identity is not content identity.

Object identity is not Manifest identity.

Object identity is not State Root.

Object identity is not Authorized View Root.

Object identity is not Branch identity.

Object identity is not Merge identity.

Revision preserves object identity.

State change preserves object identity.

Representation change preserves object identity.

Observation changes history, not identity by default.

A genuinely distinct object requires affirmative distinct-object evidence and
independent Genesis lineage.

Computable does not mean established.

Outer layers consume object identity.

They do not redefine it.

TURN THE OBJECT.
DO NOT CLONE THE WORLD.
