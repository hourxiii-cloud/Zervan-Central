# R2-B — Origin Establishment and Object Binding

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R2-B
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R2-B defines the governed operation that binds admitted Origin Information to
an Ingress Envelope, Genesis Manifest, and Canonical Room Object.

R2-B consumes:

- R1-A authority and mutation controls;
- R1-C canonical content identity and Ingress Envelope;
- R1-D Genesis Manifest architecture;
- R1-F distinct-object semantics;
- R2-A Canonical Room Object identity and singularity.

R2-B does not redefine them.

R2-B does not define:

- Terrain;
- Territory;
- Bounded Zone;
- Bounded Space;
- Perspective / Representation Transform;
- Orientation;
- Cartography;
- Occupation;
- capability movement.

---

## 1. Establishment Sequence

The native-v41 establishment sequence is:

Origin Information
    ->
Canonical SHA-512 Content Identity
    ->
Ingress Envelope
    ->
Genesis Manifest
    ->
Canonical Object Identity
    ->
Canonical Room Object
    ->
ESTABLISHED

Every transition MUST remain attributable and traversable.

No stage silently substitutes for another.

---

## 2. Origin Information

Origin Information is the informational payload proposed for admission.

It exists before interpretation.

R2-B does not require the payload itself to travel with every later operation.

The admitted payload is bound through its R1-C canonical content identity,
storage/content address, schema/serialization identity, provenance, and
Ingress Envelope.

Identity travels.
Payload rests.

---

## 3. Ingress Binding

The Ingress Envelope is the authoritative admission boundary record consumed by
R2-B.

R2-B MUST preserve, without reinterpretation:

- source identity;
- canonical content identity;
- storage/content address;
- schema identity;
- serialization identity;
- provenance;
- admission boundary;
- custody;
- time;
- controls;
- evidence restrictions;
- authorization posture;
- attestation when present.

R2-B MUST NOT silently broaden the admission boundary.

R2-B MUST NOT silently remove restrictions.

---

## 4. Genesis Binding

A Genesis Manifest used for establishment MUST reference the exact Ingress
Envelope being consumed.

Its `origin_content_identity` MUST equal the R1-C canonical content identity
recorded by that Ingress Envelope.

Its provenance-origin reference MUST remain compatible with the Ingress
Envelope provenance route.

Its establishment boundary MUST not contradict the admitted boundary.

Genesis establishes definition.

Ingress establishes admitted evidence context.

They are related but not interchangeable.

---

## 5. Canonical Object Binding

R2-A defines canonical object identity as deterministic SHA-512 identity over:

- Genesis Manifest reference;
- originating canonical content identity;
- object nonce.

R2-B MUST recompute that identity during establishment.

The supplied `object_id` MUST equal the recomputed R2-A identity.

A mismatched object identity MUST fail closed.

No local capability may substitute:

- content identity;
- Manifest identity;
- State Root;
- Branch identity;
- Merge identity

for canonical `object_id`.

---

## 6. Proposed State

A Canonical Room Object begins establishment as:

`PROPOSED`

PROPOSED means:

- identity may be computable;
- candidate binding material exists;
- establishment has not yet succeeded.

PROPOSED does not mean:

- established;
- qualified;
- ready;
- occupied;
- analytically valid;
- authorized for mutation.

Computable != established.

---

## 7. Establishment Preconditions

A PROPOSED object may transition to ESTABLISHED only when all required
establishment checks succeed.

Required checks are:

1. Ingress Envelope exists.
2. R1-C canonical content identity is valid.
3. Genesis Manifest exists.
4. Genesis references the consumed Ingress Envelope.
5. Genesis origin content identity matches Ingress content identity.
6. Provenance continuity is preserved.
7. Canonical `object_id` recomputes correctly under R2-A.
8. Duplicate-establishment check is CLEAR.
9. Authorization evidence required by R1-A is present.
10. No prerequisite is fabricated or inferred merely to complete the record.

Unknown remains unknown.

Missing remains missing.

Failure remains visible.

---

## 8. Establishment Transition

Allowed R2-B establishment transitions are:

`PROPOSED -> ESTABLISHED`

`PROPOSED -> REJECTED`

R2-B does not define later lifecycle transitions.

The following are invalid:

`ESTABLISHED -> PROPOSED`

`REJECTED -> ESTABLISHED`

`ESTABLISHED -> REJECTED`

under the R2-B establishment operation.

Later correction or replacement must use downstream governed semantics rather
than rewriting establishment history.

---

## 9. ESTABLISHED

ESTABLISHED means only that the governed Origin / Ingress / Genesis /
Canonical Room Object binding succeeded.

ESTABLISHED does NOT mean:

- QUALIFIED;
- READY;
- analytically correct;
- true;
- complete;
- safe;
- occupied;
- approved for arbitrary operation.

Establishment != qualification.

Establishment != truth.

Establishment != readiness.

---

## 10. REJECTED

REJECTED means the proposed establishment did not satisfy the binding contract.

Rejection MUST preserve:

- proposed object identity when computable;
- Origin / Ingress references;
- Genesis reference when present;
- failed checks;
- provenance;
- authorization evidence or its absence;
- rejection reason.

Rejection MUST NOT erase the attempted establishment.

Failure is evidence.

---

## 11. Provenance Continuity

An established Room Object MUST retain a traversable route to:

Canonical Room Object
    ->
Genesis Manifest
    ->
Ingress Envelope
    ->
Origin Information / Origin Reference

If provenance is unresolved at ingress, it remains explicitly unresolved.

R2-B MUST NOT manufacture an origin reference to make the chain look complete.

Provenance continuity does not require invented certainty.

---

## 12. Duplicate Establishment Control

Before ESTABLISHED is permitted, the establishment operation MUST declare one
of:

- CLEAR
- EXISTING_OBJECT
- UNRESOLVED

Only CLEAR permits ESTABLISHED.

EXISTING_OBJECT means the proposed establishment collides with an already
established canonical object under the same establishment identity.

UNRESOLVED means the system cannot yet prove establishment uniqueness.

UNRESOLVED MUST fail closed for establishment.

R2-B defines this control requirement.

It does not assign Registry ownership prematurely.

---

## 13. Object Nonce Boundary

The R2-A object nonce provides deliberate identity separation.

It MUST NOT be used to bypass duplicate-establishment control.

Generating a new nonce merely to avoid an existing object match is forbidden
unless independent object establishment is justified by R1-F distinct-object
semantics.

Nonce != permission to clone.

---

## 14. Authorization Boundary

Object establishment is governed.

Technical ability to compute an identity or write a record is insufficient.

Authorization evidence MUST resolve through R1-A.

R2-B records the authorization reference used for the establishment decision.

R2-B does not redefine the authority hierarchy.

Write capability != authority.

---

## 15. Human Gate

Human Gate posture is inherited from R1-A and recorded by the Genesis Manifest
and establishment receipt.

R2-B MUST preserve whether Human Gate was:

- required;
- satisfied;
- not required under the resolved governing state;
- unresolved.

R2-B MUST NOT invent Human Gate approval.

Approval and execution remain distinct.

---

## 16. Establishment Receipt

Every terminal R2-B decision MUST produce an immutable establishment receipt.

The receipt records:

- establishment receipt identity;
- Ingress Envelope reference;
- Genesis Manifest reference;
- canonical `object_id`;
- initial status;
- final status;
- duplicate-establishment result;
- prerequisite check results;
- authorization reference;
- Human Gate status/reference;
- provenance route;
- decision time;
- decision reason.

The receipt is evidence of the establishment operation.

The receipt does not replace:

- the Ingress Envelope;
- Genesis Manifest;
- Canonical Room Object;
- provenance;
- authority evidence.

Receipt != object.

---

## 17. Establishment Receipt Identity

The establishment receipt identity is deterministic SHA-512 over exactly:

- Ingress Envelope reference;
- Genesis Manifest reference;
- canonical `object_id`;
- final establishment status;
- duplicate-establishment result;
- authorization reference;
- decision time.

The receipt identity identifies the establishment decision record.

It does not identify the Room Object.

Receipt identity != object identity.

---

## 18. Failure Conditions

R2-B MUST fail closed when:

- Ingress Envelope is missing;
- Genesis Manifest is missing;
- content identities disagree;
- Genesis references another Ingress Envelope;
- provenance binding contradicts known provenance;
- canonical object identity does not recompute;
- duplicate check is EXISTING_OBJECT;
- duplicate check is UNRESOLVED;
- required authorization evidence is absent;
- Human Gate is claimed satisfied without evidence;
- required establishment evidence is fabricated.

Failure MUST remain attributable.

---

## 19. Downstream Boundary

ESTABLISHED does not automatically create:

- Terrain;
- Territory;
- Bounded Zone;
- Bounded Space;
- Cartography;
- Occupation;
- capability authorization.

Those are later Ring 2 contracts.

R2-B ends when object establishment and its receipt are resolved.

---

## 20. R2-B Lock

Origin exists before interpretation.

Ingress preserves admission context.

Genesis binds accepted establishment definition.

R2-A object identity is recomputed, not trusted blindly.

PROPOSED is not ESTABLISHED.

Only PROPOSED may enter the R2-B terminal establishment decision.

ESTABLISHED means binding succeeded, not qualification or truth.

REJECTED remains evidence.

Duplicate establishment must be CLEAR.

Nonce cannot be used to clone around duplicate control.

Provenance remains traversable toward Origin.

Authorization is inherited from R1-A.

Human Gate approval is never invented.

Receipt identity is not object identity.

No Terrain yet.

No Territory yet.

No Zone yet.

No Space yet.

No Cartography yet.

No Occupation yet.
