# R1-D — Manifest Architecture

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R1-D
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R1-D defines the manifest classes used by native v41.

It consumes:

- R1-A Authority and Canonical Resolution
- R1-B Version Identity and Promotion
- R1-C Identity, Integrity, and Provenance

R1-D does not redefine them.

R1-D separates system/doctrine manifests from analytical-object manifests and
separates immutable establishment/revision records from mutable location
pointers.

R1-D does not define Room state roots, authorized-view roots, branch semantics,
merge semantics, or lifecycle semantics.

---

## 1. Manifest Class Separation

The term "manifest" does not identify one universal object.

The following manifest classes remain distinct:

1. Doctrine / System Manifest
2. Genesis Manifest
3. Revision Manifest
4. Manifest Pointer

A single mutable manifest MUST NOT carry all identity, definition, current
state, authorized view, and operational position.

That model is deprecated.

---

## 2. Doctrine / System Manifest

`DoctrineOps/DOCTRINE_MANIFEST.md` remains the system-level doctrine existence
and load-control surface.

It answers questions such as:

- Which doctrine and governance-critical surfaces exist?
- Which artifacts are required?
- What load order applies?
- Which missing artifacts cause hard halt?

It does not become:

- a Genesis Manifest;
- a Revision Manifest;
- a Room/Object state container;
- a state root;
- an authorized-view root;
- an active analytical pointer.

System governance manifests and analytical-object manifests MUST NOT silently
impersonate one another.

---

## 3. Genesis Manifest

A Genesis Manifest is an immutable establishment record.

It records the minimum accepted definition necessary to establish an
analytical-object lineage without encoding downstream mutable state.

A Genesis Manifest MUST preserve:

- manifest schema version;
- manifest type;
- creation timestamp;
- originating canonical SHA-512 content identity;
- ingress-envelope reference;
- provenance origin reference;
- declared establishment boundary;
- declared definition payload;
- authority posture at establishment;
- Human Gate posture at establishment;
- manifest content identity when materialized.

The Genesis Manifest establishes the first accepted definition record.

It does not independently establish:

- analytical truth;
- state root;
- authorized view;
- qualification result;
- branch identity;
- merge identity;
- execution permission.

A Genesis Manifest is immutable after acceptance.

Correction requires a later Revision Manifest or an explicitly governed
replacement process.

---

## 4. Revision Manifest

A Revision Manifest is an immutable record of one accepted definition-changing
revision associated with an existing Genesis Manifest lineage.

It MUST preserve:

- manifest schema version;
- manifest type;
- creation timestamp;
- Genesis Manifest reference;
- immediate predecessor manifest reference;
- revision sequence;
- reason for revision;
- changed definition payload;
- preserved provenance route;
- authority posture;
- Human Gate posture;
- manifest content identity when materialized.

A Revision Manifest records definition change.

It does not overwrite the Genesis Manifest.

It does not mutate an earlier Revision Manifest.

It does not itself define runtime state.

Revision semantics beyond definition continuity remain downstream where object
identity and branch semantics are resolved.

---

## 5. Manifest Immutability

Accepted Genesis and Revision Manifests are immutable records.

An immutable manifest may be:

- read;
- verified;
- referenced;
- replayed as historical evidence.

It may not be silently rewritten in place.

If accepted definition changes, produce a new Revision Manifest.

Historical manifests remain addressable.

Immutability applies to the accepted record, not to temporary draft material
that has not crossed the applicable acceptance gate.

---

## 6. Manifest Content Identity

When materialized, each Genesis or Revision Manifest may receive a canonical
R1-C SHA-512 content identity.

That identity identifies the manifest bytes.

It does not automatically become:

- Room ID;
- object identity;
- lineage identity;
- state identity.

Manifest content identity != analytical-object identity.

The eventual object-identity contract may reference manifest identities, but
R1-D does not define that relationship yet.

---

## 7. Definition Payload

A manifest definition payload contains only the definition necessary for the
manifest's responsibility.

Genesis definition payload describes establishment.

Revision definition payload describes the accepted definition change.

The payload MUST NOT become a dumping ground for:

- runtime state;
- occupancy state;
- analytical findings;
- authorized-view state;
- capability-local state;
- report rendering state.

Outer concerns consume the manifest definition.

They do not redefine it.

---

## 8. Manifest Pointer

The Manifest Pointer is a mutable locator.

It identifies:

- the Genesis Manifest reference;
- the currently selected accepted manifest reference;
- the current revision sequence;
- the time the pointer was changed;
- the governance evidence authorizing pointer movement.

The pointer does not contain the complete object definition.

The pointer does not rewrite historical manifests.

Changing the pointer changes which accepted definition is selected as current.

It does not alter the bytes or history of the referenced manifests.

---

## 9. Pointer Mutation Boundary

Manifest Pointer mutation is governed by R1-A.

Technical write capability is insufficient.

Pointer movement MUST preserve:

- prior pointer value;
- new pointer value;
- mutation reason;
- mutation timestamp;
- authorization reference;
- provenance route.

R1-D defines the requirement.

The later state/transition architecture will define how those mutation events
are operationally witnessed.

---

## 10. Provenance

Every Revision Manifest MUST preserve a traversable route to:

- its immediate predecessor;
- its Genesis Manifest;
- the originating evidence/provenance route defined by R1-C.

Manifest history MUST be reconstructible without overwriting prior records.

Missing provenance remains missing.

It MUST NOT be invented.

No Compression Out applies.

---

## 11. Unknown and Deferred Fields

R1-D permits explicit unresolved values where downstream architecture has not
yet defined semantics.

Unknown MUST remain distinguishable from absent.

A field whose meaning belongs to R1-E or R1-F MUST NOT be guessed merely to
make a manifest look complete.

---

## 12. State Root Boundary

State roots are intentionally excluded from R1-D.

A Manifest records accepted definition.

A State Root will later identify current state.

Definition != state.

R1-E owns that distinction.

---

## 13. Authorized-View Boundary

Authorized-view roots are intentionally excluded from R1-D.

A Manifest does not define what an individual occupant may see.

Definition != projection.

R1-E owns authorized-view semantics.

---

## 14. Branch and Merge Boundary

R1-D does not resolve branch or merge identity.

A Revision Manifest is not automatically a branch.

A Manifest Pointer movement is not automatically a branch.

A new Genesis Manifest is not automatically proof that a distinct analytical
object exists.

Those relationships remain blocked pending R1-F.

---

## 15. R1-D Lock

Doctrine manifests govern system/doctrine existence and loading.

Genesis Manifest records immutable establishment.

Revision Manifest records immutable accepted definition change.

Manifest Pointer identifies the currently selected accepted definition.

Historical manifests are never rewritten in place.

Manifest content identity is SHA-512 byte identity, not automatically Room or
object identity.

Definition is not state.

Definition is not projection.

Revision is not automatically branch.

Pointer movement is governed mutation.

No outer capability may collapse these manifest classes back into one mutable
manifest.
