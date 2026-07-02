# CAS_CHUNK_MANIFEST — CAS ↔ Chunking Binding Manifest

Status: CANONICAL • NON-OPTIONAL • GOVERNANCE-CRITICAL  
Authority Class: DoctrineOps / Governance-Critical Control Surface  
Scope: All Zervan executions that chunk, store, reference, verify, or recombine evidence  
Version: 1.0.0

⸻

## 0. Purpose

This manifest defines the **binding rules and required fields** between:

- Content-Defined Chunking (CDC) profiles (e.g., FastCDC)
- CAS (Content Addressable Storage / content addressing)
- Evidence references used by envelopes, proofs, reports, and replay

It answers one question only:

> When evidence is chunked, how do we represent chunk identity and deterministic
> recomposition *without* granting authority to storage, implementation, or convenience?

This file is **governance-critical wiring**.
It is not doctrine physics.
It is not an execution plan.

⸻

## 1. Non-Authority Clause (Hard)

This manifest does **not** confer interpretive meaning.

- CAS stores bytes and hash identities.
- Chunking defines deterministic boundaries under a declared profile.
- Evidence references bind identities to executions.

No component may treat:
- chunk membership
- chunk similarity
- chunk frequency
- chunk reuse

as meaning, attribution, confidence, or authority.

Meaning and admissibility remain governed exclusively by Doctrine (PMC → MC).

⸻

## 2. Activation Rule (Hard)

This manifest is REQUIRED when **any** of the following occur:

- Any dataset or artifact is chunked
- Any CAS reference is emitted, stored, or verified
- Any evidence is represented as chunk references
- Any recomposition or replay is required
- Any manifest / proof / run-plan binds evidence by hash instead of inline bytes

If any activation condition is met and this file is missing or unreadable:

→ **HARD HALT (fail-closed)**

⸻

## 3. Definitions

Chunking Profile  
A deterministic boundary-selection contract dividing a byte stream into chunks  
(e.g., `zervan://chunking/fastcdc/1`).

Chunk  
A byte range of the input stream produced under a declared chunking profile.

Chunk Payload Hash  
A cryptographic digest of the exact chunk bytes.

Chunk Identity  
A deterministic tuple binding:
- chunk payload hash
- hash algorithm
- chunking method ID

Chunk Set Manifest  
A structured record binding an original artifact to an ordered set of chunk identities
sufficient for exact recomposition.

Recomposition  
Deterministic reassembly of the original bytes from a chunk set manifest.

⸻

## 4. Canonical Chunking Method Registry

Chunking methods are identified **only** by Method ID.

### 4.1 FastCDC Baseline Profile A (Required Support)

Method ID:
- `zervan://chunking/fastcdc/1`

Profile Artifacts (transport only):
- `chunking/fastcdc/1/README.md`
- `chunking/fastcdc/1/profile.json`
- `chunking/fastcdc/1/DETERMINISM.md`

Determinism:
- Implementations MUST satisfy the determinism contract.
- Non-deterministic chunking MUST be rejected.

Failure → **MUST NOT claim conformance**

⸻

## 5. Chunk Identity (Canonical Requirements)

Each chunk MUST be representable with the following **identity fields**:

REQUIRED:
- `chunk_hash`
- `hash_alg`
- `method_id`
- `ordinal`

OPTIONAL:
- `size_bytes`

Chunk identity MUST NOT depend on:
- file paths
- timestamps
- environment metadata
- process state
- execution order

Chunk identity MUST be computable solely from:
- exact chunk bytes
- declared hash algorithm
- declared chunking method ID

⸻

## 6. Required Hash Algorithms

Chunk payload hashes MUST use an algorithm allowed by active crypto policy.

Minimum REQUIRED support:
- `sha512`

Hash identifiers MUST be canonical:
- `sha512:<hex>`

⸻

## 7. Chunk Set Manifest — **Required Fields (Hard Schema)**

If chunking is used, a Chunk Set Manifest **MUST exist** and **MUST include**:

### 7.1 Manifest Header (Required)

- `manifest_version`
- `generated_at` (ISO-8601)
- `chunking_method_id`
- `profile_hash` (hash of profile.json)
- `determinism_contract_hash`

### 7.2 Source Artifact Identity (Required)

- `source_artifact`:
  - `hash_alg`
  - `hash_id`
  - `size_bytes`

### 7.3 Chunk List (Required, Ordered)

An ordered array where **each entry MUST include**:

- `ordinal` (0-based, contiguous)
- `chunk_hash`
- `hash_alg`
- `size_bytes`
- `byte_offset` (starting offset in original artifact)

No gaps. No reordering.

### 7.4 Optional Summary (Allowed)

- `chunk_count`
- `total_bytes`

### 7.5 Classification

- MUST be marked: `DERIVED_EVIDENCE`
- MUST NOT assert meaning or interpretation

If any required field is missing:

→ **HARD HALT**

⸻

## 8. Recomposition Requirements (Hard)

Given:
- identical source bytes
- identical chunking method ID
- identical profile parameters
- identical hash rules

The system MUST:
- reproduce identical chunk boundaries
- reproduce identical chunk hashes
- reassemble to identical source bytes

Mismatch → **HARD HALT**

⸻

## 9. CAS Behavior Constraints

CAS MAY store:
- chunk payload bytes
- hash identifiers
- size metadata

CAS MUST NOT:
- infer meaning
- infer provenance
- collapse storage into authority
- substitute hash presence for evidence admission

CAS references are **pointers**, not proof.

⸻

## 10. Evidence Binding Rules

Whenever chunked evidence is referenced, bindings MUST include:

- source artifact hash
- chunking method ID
- chunk set manifest hash
- chunk hash algorithm
- declaration of DERIVED EVIDENCE

⸻

## 11. Versioning & Immutability

- This manifest is immutable once sealed.
- Chunking profiles are immutable once sealed.
- Changes require:
  - new version
  - explicit replacement
  - no implicit upgrade

⸻

## 12. Enforcement (Hard)

If chunking or CAS is invoked, the following MUST be present:

- this manifest
- referenced chunking profile
- determinism contract
- chunk set manifest (when chunking is used)

Missing anything → **HARD HALT**

⸻

## 13. Canonical Statement

Chunking defines boundaries.  
CAS defines identity.  
Neither defines meaning.

— End of Manifest —
