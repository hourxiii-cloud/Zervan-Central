# R1-C — Identity, Integrity, and Provenance

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R1-C
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R1-C defines the primitives used to identify admitted information, witness
integrity, preserve attribution, and retain traversable provenance.

R1-C consumes R1-A authority/canonical-resolution rules and R1-B version
identity/promotion rules.

R1-C does not redefine them.

R1-C does not define Room identity, manifests, state roots, authorized views,
revision semantics, branch semantics, merge semantics, or lifecycle state.

---

## 1. Core Separation

The following remain distinct:

- source identity
- content identity
- storage or content address
- schema identity
- serialization identity
- attestation
- provenance
- authority
- interpretation
- truth

No one field may silently impersonate another.

---

## 2. Origin Information

Origin Information is the informational payload admitted for analysis before
interpretation.

The payload exists independently from:

- its storage location;
- its hash;
- its schema;
- its serialization;
- its interpretation;
- its rendering;
- any later analytical object constructed from it.

Metadata does not replace payload.

---

## 3. Canonical Content Identity

The canonical Zervan content identity algorithm is SHA-512.

Canonical representation:

`sha512:<128 lowercase hexadecimal characters>`

The digest is calculated over the admitted byte sequence.

SHA-512 establishes:

- the byte sequence admitted;
- whether later bytes are identical to those admitted bytes.

SHA-512 does not independently establish:

- semantic correctness;
- factual truth;
- source reliability;
- authority;
- interpretation permission;
- storage availability;
- ownership;
- admissibility;
- Room identity.

Hash != truth.

---

## 4. Integrity

Integrity answers:

> Does this payload still resolve to the same admitted byte identity?

Verification compares a calculated SHA-512 digest with the recorded canonical
content identity.

Successful verification proves byte-level sameness under the declared
serialization.

Integrity does not prove correctness, completeness, currency, admissibility,
authority, reliability, or truth.

---

## 5. Storage and Content Address

Storage location and content identity remain separate.

A storage URI, filesystem path, repository path, object-store key, database
key, URL, or other locator answers:

> Where may the payload be retrieved?

SHA-512 answers:

> Which admitted bytes are expected?

Moving identical bytes does not create a new content identity.

Changing bytes requires a new content identity.

Storage presence does not confer authority or truth.

AWS-specific checksum, signing, transport, object metadata, and storage
requirements belong to the integration/ingress layer and MUST NOT redefine
Zervan canonical content identity.

---

## 6. Schema and Serialization Identity

Schema identity identifies the declared structural contract.

Serialization identity identifies the admitted representation, including
format and encoding where applicable.

Semantically equivalent content serialized differently may have different
SHA-512 identities.

Semantic equivalence != byte identity.

R1-C does not define semantic-equivalence rules.

---

## 7. Attestation and Signature Semantics

An attestation or cryptographic signature, when present, is evidence that an
identified actor or key asserted or signed an identified payload or statement.

A valid signature proves attestation within its verified cryptographic
context.

It does not independently prove:

- factual correctness;
- semantic correctness;
- truth;
- admissibility;
- analytical conclusion;
- authority beyond the signer's actual authority.

Signature != correctness.

Absence of attestation remains distinguishable from failed attestation.

---

## 8. Ingress Envelope

The Ingress Envelope binds the minimum identity, integrity, provenance, and
control information required to admit Origin Information without confusing
payload with metadata.

It MUST preserve:

- source identity;
- canonical SHA-512 content identity;
- storage or content address;
- schema identity;
- serialization identity;
- provenance;
- admission boundary;
- ownership or custody;
- time information;
- applicable controls;
- evidence restrictions;
- authorization posture.

Unknown values remain explicit.

Unknown MUST NOT silently become absent, false, unrestricted, or unauthorized.

---

## 9. Provenance

Provenance is structural and traversable.

Every downstream derived artifact must retain a resolvable route toward its
originating evidence identity.

At minimum provenance supports resolution of:

- origin reference;
- parent evidence or artifact references;
- transformation or derivation event;
- responsible actor or capability when known;
- time or sequence when known;
- referenced content identity where applicable.

Incomplete provenance remains incomplete.

Missing lineage MUST NOT be invented.

No Compression Out applies to provenance.

---

## 10. Lineage

Lineage records derivational relationships.

A child artifact may reference one or more parents.

Lineage does not imply correctness, endorsement, authority, or semantic
agreement.

A derived artifact MUST NOT replace its parent evidence identity.

Every valid derivation preserves a return route toward its parent references.

---

## 11. Identity Travels; Payload Rests

The runtime may carry lightweight identity and provenance references without
transporting the complete payload.

Identity travels.
Payload rests.

This MUST NOT sever:

- content identity;
- storage resolution;
- provenance route;
- integrity verification capability.

Hydration remains downstream from R1-C.

---

## 12. Restricted and Unavailable Evidence

Restricted evidence remains existentially represented even when its payload
cannot currently be accessed.

The system distinguishes:

- KNOWN_AVAILABLE
- KNOWN_RESTRICTED
- KNOWN_UNAVAILABLE
- UNRESOLVED
- ABSENT

Restricted MUST NOT silently become nonexistent.

Unavailable payload does not invalidate an otherwise established canonical
content identity.

---

## 13. Truth Boundary

The following are locked:

Hash != truth.

Signature != correctness.

Storage != authority.

Presence != admissibility.

Provenance != endorsement.

Identity != interpretation.

Integrity != semantic correctness.

No outer capability may redefine these relationships.

---

## 14. Integration Boundary

External integrations consume the canonical Zervan identity.

They may add transport-specific, platform-specific, checksum, signing, storage,
or service metadata required for their operation.

Those integration values are evidence about the integration event.

They do not become competing Zervan canonical identities.

The inner identity contract remains SHA-512.

---

## 15. Downstream Boundary

R1-C does not define:

- Canonical Room Object identity;
- Genesis Manifest;
- Revision Manifest;
- state root;
- authorized-view root;
- active pointer;
- revision identity;
- branch identity;
- merge identity;
- lifecycle state;
- qualification state.

Those remain blocked.

---

## 16. R1-C Lock

Origin precedes interpretation.

Canonical content identity is SHA-512 byte identity.

Integrity witnesses sameness, not truth.

Attestation witnesses assertion, not correctness.

Storage locates payload; it does not define identity.

Schema and serialization remain explicit.

Provenance remains traversable.

Unknown remains unknown.

Restricted remains existent.

Every downstream derivation retains a route toward origin.

Integration adapts outward.
Identity is defined inward.
