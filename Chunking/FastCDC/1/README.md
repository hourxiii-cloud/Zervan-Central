# FastCDC Chunking Profile — v1 (Baseline Profile A)

Path: zervan-core/chunking/fastcdc/1  
Method ID: zervan://chunking/fastcdc/1  
Status: CANONICAL · IMMUTABLE  
Scope: Content-defined chunking (CDC) profile definition

---

## 1. Purpose

This directory defines FastCDC Profile v1, the baseline, canonical
content-defined chunking profile used by Zervan for large-scale data
ingestion, slicing, and recomposition.

This profile exists to provide:

- Stable, content-defined chunk boundaries
- Deterministic chunk identity across runs
- High resilience to insertions, deletions, and shifts
- Predictable I/O behavior under constrained memory conditions

This profile is an algorithmic contract, not executable code.

---

## 2. Authority & Immutability

- This profile is canonical once sealed
- Parameters MUST NOT be altered in-place
- Any modification requires a new versioned profile (e.g. fastcdc/2)
- Implementations MUST conform to the declared parameters exactly

Repository presence does not confer authority.

Authority is derived only from explicit reference to this profile by
DoctrineOps or execution manifests.

---

## 3. Algorithm Family

- Chunking Method: Content-Defined Chunking (CDC)
- Algorithm Lineage: FastCDC (Rabin fingerprint–derived)
- Boundary Selection: Rolling hash with content-dependent cut points

This profile does not mandate a specific programming language or library.

---

## 4. Canonical Parameters (Baseline Profile A)

The following parameters are fixed and immutable for this profile:

- Minimum chunk size: 2 MiB
- Target (average) chunk size: 8 MiB
- Maximum chunk size: 32 MiB
- Hash basis: Content-defined rolling hash
- Cut condition: FastCDC-style anchor mask
- Window size: Implementation-defined, but MUST be deterministic

All sizes are binary units (MiB).

Any deviation requires a new profile version.

---

## 5. Determinism Requirements

Implementations MUST ensure:

- Identical input bytes produce identical chunk boundaries
- Chunk boundaries are independent of:
  - File offsets
  - Container size
  - Execution environment
  - Parallelism strategy
- Boundary decisions are purely content-derived

Any deviation breaks canonical equivalence.

See DETERMINISM.md for the binding determinism contract.

---

## 6. Chunk Identity & CAS Integration

This profile defines chunk boundaries only.

When used within Zervan execution, chunk boundaries produced by this
profile MAY be elevated to evidence-addressable units under the
CAS & Evidence subsystem.

When chunk identity is materialized, higher layers MUST:

- Bind each chunk to a stable content hash (e.g. SHA-256 or SHA-512)
- Record explicit linkage to this Method ID:
  zervan://chunking/fastcdc/1
- Preserve ordering metadata sufficient for deterministic recomposition
- Treat chunk identity as DERIVED EVIDENCE, not doctrine

This profile does not define:

- Hash algorithms
- CAS storage layout
- Evidence retention policy
- Proof chaining semantics

Those concerns are governed elsewhere in Zervan.

---

## 7. Intended Use

This profile is designed for:

- Large file ingestion (multi-GB scale)
- Streaming or slice-based analysis
- Incremental re-analysis
- Distributed or constrained-memory environments
- LLM-assisted analysis pipelines requiring deterministic recomposition

The profile prioritizes stability and auditability over maximal throughput.

---

## 8. Reference Implementation Note (Non-Authoritative)

One or more reference implementations MAY exist to demonstrate correct
behavior under this profile.

Reference implementations are:

- Non-canonical
- Non-authoritative
- Provided for validation and comparison only

No implementation becomes canonical by existence or adoption.

Implementations that diverge in behavior MUST declare non-conformance.

---

## 9. Non-Goals

This profile does NOT define:

- Encryption
- Compression
- Transport
- Storage layout
- Execution scheduling
- Security policy
- Trust or authority semantics

Those concerns are addressed elsewhere in Zervan.

---

## 10. Versioning Rules

- fastcdc/1 is Baseline Profile A
- Future variants MUST be:
  - Versioned
  - Isolated
  - Explicitly referenced
- No profile is ever implicitly upgraded

---

## 11. Summary

FastCDC Profile v1 provides a stable, deterministic,
content-defined chunking contract suitable for Zervan’s analysis,
governance, and recomposition workflows.

If an implementation cannot meet these constraints,
it MUST NOT claim conformance.
