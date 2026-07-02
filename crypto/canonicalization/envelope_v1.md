# Zervan Envelope Canonicalization — v1

**Status:** Canonical  
**Scope:** All Zervan envelopes that are signed or hashed (manifest, run plan IR, proof references, diagnostics refs)  
**Purpose:** Define the deterministic byte representation of an envelope for hashing and PKI/ECC signing.

This document answers one question:

> **What exact bytes are signed?**

If two implementations produce the same canonical bytes, they must produce the same hash and signatures verify across machines.

---

## 1. Terminology

- **Envelope**: A structured object that may contain references to evidence, policies, code artifacts, outputs, and proofs.
- **Canonical bytes**: A deterministic serialization of an envelope (or signed subset) as UTF-8 bytes.
- **Canonical hash**: `SHA-512(canonical_bytes)`.
- **Signed scope**: The exact canonical bytes that are hashed and then signed.
- **CAS reference**: Content-addressed identifier for a blob (e.g., `sha512:<hex>`), not the blob contents.

---

## 2. Inputs Covered

This canonicalization applies to any JSON object that is:
- validated against a Zervan envelope schema, and
- used for hashing and/or signing.

Common envelope types include:
- `manifest.schema.json`
- `run_plan.ir.schema.json`
- `proof.schema.json` (proof signs *other* scopes; proof itself may be signed in chained mode)
- `diagnostics.schema.json` (normally referenced by hash, not signed inline)

---

## 3. Canonical Serialization Rules (JSON → bytes)

### 3.1 Character encoding
- Serialize as **UTF-8** bytes.
- No BOM.

### 3.2 JSON form
- Output must be a single JSON value (an object for envelopes).
- No comments.
- No trailing commas.

### 3.3 Whitespace
- No insignificant whitespace.
- Use the minimal JSON form:
  - separators: `,` and `:`
  - no spaces, newlines, or tabs

### 3.4 Object key ordering
- All JSON object keys MUST be sorted **lexicographically by Unicode code point** (ascending).
- Ordering is applied **recursively** at every nested object.

### 3.5 Arrays
- Array element order is **preserved exactly**.
- Arrays are never sorted by canonicalization.

### 3.6 Null vs missing
- A missing field is **not equivalent** to `null`.
- If a schema allows omission, omission remains omission.
- If present as `null`, it remains `null`.

### 3.7 Strings
- Strings must be valid Unicode.
- Normalize strings to **Unicode NFC** prior to serialization.
- Escape rules follow JSON:
  - Control characters must be escaped.
  - No optional escaping beyond what JSON requires.
  - Forward slashes `/` MUST NOT be escaped.

---

## 4. Numeric Canonicalization (Critical)

### 4.1 Integers
- Integers are serialized in base-10 with:
  - no leading zeros (except `0`)
  - optional leading `-` for negatives

### 4.2 Floats / decimals
To avoid cross-language float drift, **v1 forbids binary floating ambiguity** in signed scopes.

Rules:
- Envelopes intended for signing MUST NOT contain JSON numbers that require fractional precision unless they are encoded as **strings**.
- Any value requiring decimals (scores, probabilities, distances, money-like figures, etc.) MUST be represented as:
  - a string with an explicit format, OR
  - a fixed-point integer + scale metadata

**Allowed signed numeric forms:**
- integer JSON numbers
- decimal strings, e.g. `"0.913500000000"` (precision must be stable within the producing engine)

**Disallowed in signed scope:**
- JSON floating numbers like `0.9135`

Rationale:
- JSON has no native decimal type
- IEEE-754 formatting differences cause unverifiable signatures

---

## 5. Signed Scopes

A Zervan envelope may be signed as a whole or as explicit scopes.

### 5.1 Default signing mode (recommended)
Sign the canonical bytes of an explicit **scope object** containing only:
- identity/provenance fields
- input bindings (artifact hashes/refs)
- policy binding (policy hash/ref)
- engine/version binding (code hash/ref)
- output bindings (CAS refs + hashes)
- determinism hooks

Diagnostics payloads MUST be referenced by hash/ref, not inlined.

### 5.2 Scope selection rule
If a schema defines a `signed_scope` object, the signer MUST:
- canonicalize the `signed_scope` object only, and
- record its canonical hash in proof.

If a schema does not define a `signed_scope`, the signer MAY:
- sign the entire validated envelope object,
- but must declare this explicitly in proof (`signature_scope: "full_envelope"`).

---

## 6. Canonical Hash

- Hash algorithm: **SHA-512**
- Canonical hash is computed as:

`canonical_hash = SHA-512(canonical_bytes)`

Representation:
- Lowercase hex, 128 chars
- Stored as: `sha512:<hex>`

---

## 7. Signature Preimage and Algorithm

### 7.1 Preimage
- The signature preimage is the canonical hash bytes of the signed scope:
  - compute `canonical_hash` as above
  - sign the raw 64-byte digest (not the hex string)

### 7.2 Algorithms (declared by policy)
- Allowed signature algorithms are defined in `crypto/policies/crypto_policy.yaml`.
- Proof objects MUST record:
  - algorithm identifier
  - signer key id (fingerprint)
  - canonical hash (`sha512:<hex>`)
  - signature bytes (base64)

---

## 8. CAS References (Pointers, not payloads)

To keep envelopes small and replayable:
- large payloads MUST be stored in CAS and referenced by `sha512:<hex>`.
- the signed scope MUST include the CAS reference id(s), and may include size metadata.

Example:
```json
{
  "trace_ref": { "alg": "sha512", "id": "sha512:<hex>", "bytes": 19333 }
}
