# Determinism Contract — FastCDC Baseline Profile A

This document defines the **determinism guarantees and requirements** for
`FastCDC Baseline Profile A`.

Determinism is **not an optimization**.
It is a **hard correctness constraint**.

Any implementation that cannot satisfy this contract **MUST NOT** claim
conformance with this profile.

---

## Scope

This determinism contract applies **only** to:

- Chunk boundary selection
- Chunk size behavior within declared limits
- Replayability of chunk boundaries for identical content

It explicitly does **not** govern:
- Hashing algorithms
- Storage layout
- Transport
- Compression
- Encryption
- Execution scheduling

---

## Determinism Definition (Zervan)

An implementation is deterministic **if and only if**:

> Given identical byte content, the implementation produces
> identical chunk boundaries, regardless of execution context.

---

## Required Deterministic Properties

### 1. Content-Only Boundary Selection

Chunk boundaries MUST be determined exclusively by:

- The content byte stream
- The FastCDC rolling fingerprint logic
- The declared profile parameters

Boundaries MUST NOT depend on:
- File offsets
- Chunk indices
- Record counts
- External metadata
- Prior chunk results

---

### 2. Offset Independence

Given the same content bytes:

- Starting at byte 0
- Starting at byte N (streamed)
- Processed as a whole
- Processed in segments

The resulting **boundary locations relative to content MUST be identical**.

---

### 3. Environment Independence

Chunk boundaries MUST be invariant across:

- CPU architectures
- Operating systems
- Endianness
- Thread counts
- Process counts
- Containerization or virtualization

---

### 4. Parallelism Independence

Chunk boundaries MUST NOT change based on:

- Parallel vs sequential execution
- Worker count
- Sharding strategy
- Buffer sizes (beyond algorithmic window constraints)

Parallel implementations MUST converge on identical results.

---

### 5. Deterministic Replay

Given:
- Identical input bytes
- Identical profile parameters

The implementation MUST be capable of:
- Reproducing chunk boundaries exactly
- Producing identical chunk size distributions
- Supporting deterministic verification

Non-replayable behavior is **non-conformant**.

---

## Explicitly Forbidden Sources of Non-Determinism

The following invalidate conformance immediately:

- Time-based seeds
- Randomized cut points
- Adaptive parameter tuning
- Hardware-specific optimizations that alter results
- Heuristic shortcuts that change boundaries
- Floating-point fingerprinting

---

## Parameter Stability

The following parameters are **fixed for this profile**:

- Minimum chunk size: 2 MiB
- Target (average) chunk size: 8 MiB
- Maximum chunk size: 32 MiB

Any change to these parameters requires:
- A new profile version
- A new directory
- A new determinism contract

---

## Validation Requirements

An implementation claiming conformance MUST be able to:

1. Produce identical chunk boundaries across multiple runs
2. Demonstrate replay determinism
3. Verify boundaries against a reference implementation
4. Reject execution if determinism cannot be guaranteed

Failure at any step → **MUST FAIL CLOSED**

---

## Conformance Statement

Only implementations that satisfy **all** requirements in this document
may claim conformance with **FastCDC Baseline Profile A**.

All others MUST either:
- Declare non-conformance
- Use a different profile
- Introduce a new profile version

---

## Design Rationale (Non-Normative)

Determinism enables:
- Stable chunk identity
- Incremental reprocessing
- Distributed analysis
- Large-file slicing
- LLM-assisted recomposition
- Audit defensibility

Without determinism, chunking is not infrastructure — it is guesswork.

---

## Authority

This document derives authority from:

- `profile.json`
- `README.md`
- DoctrineOps determinism requirements

Repository location is transport only.
Authority is explicit or it does not exist.
