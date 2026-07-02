# Beagle Contract — Gate 0 Integrity & Admission Requirements

**Component:** Beagle (Gate 0)  
**Layer:** Execution  
**Authority Scope:** Integrity, admissibility, identity sealing  
**Fail-Closed:** Mandatory  
**Bypass Allowed:** Never  

---

## Purpose

This contract defines the **mandatory integrity, determinism, and governance requirements**
that **any artifact MUST satisfy** to enter the Zervan system through **Beagle (Gate 0)**.

> **If an artifact does not satisfy this contract, it does not exist to Zervan.**

No downstream engine executes without Beagle admission.  
No artifact bypasses this contract.

---

## 1. Scope (Non-Negotiable)

This contract applies to **all inbound artifacts**, including but not limited to:

- datasets (primary evidence)
- chunked sub-artifacts (derived evidence)
- chunk set manifests
- context packs
- models
- configuration artifacts
- external signals
- internal engine-to-engine handoffs

Nothing enters execution without Beagle validation.  
Nothing downstream executes without Beagle admission.

---

## 2. Required Inputs (Minimum Admission Set)

Every artifact presented to Beagle **MUST explicitly declare** the following:

### 2.1 Artifact Identity & Intent

- **Artifact Type**
  - dataset, chunk, manifest, model, context, config, signal, etc.
- **Intended Consumer**
  - engine, module, or execution surface expected to receive the artifact
- **Evidence Class**
  - `PRIMARY` or `DERIVED` (explicit)

### 2.2 Structure & Origin

- **Structural Definition**
  - schema, shape, or explicit structure declaration
- **Source Identifier**
  - originating system, operator, or process
- **Declared Version(s)**
  - schema, model, or contract version where applicable

### 2.3 Hashability

- **Hash or Hashable Content**
  - raw bytes **or**
  - a representation Beagle can hash deterministically
- **Permitted Hash Algorithm**
  - must comply with active crypto policy (e.g., SHA-512)

Artifacts lacking **any required field**  
→ **REJECT (fail-closed)**

---

## 3. Mandatory Validation Checks

Beagle MUST successfully verify **all** checks below before admitting an artifact.

Failure at **any** step  
→ **REJECT + HARD HALT**

---

### 3.1 Structural Integrity

Beagle MUST verify:

- schema validity (if schema-governed)
- shape and type correctness
- presence of all required fields
- no ambiguous or polymorphic structure

---

### 3.2 Canonical Alignment

Beagle MUST verify:

- alignment with active doctrine and contracts
- compatibility with current Admission and Routing artifacts
- no implicit authority inference
- no bypass or shadow admission path

---

### 3.3 Hash Integrity

Beagle MUST verify:

- deterministic hashing behavior
- hash consistency across:
  - intake
  - storage (if applicable)
  - verification
- declared hash algorithm is permitted

Hash mismatch or nondeterminism  
→ **REJECT**

---

### 3.4 Version Compatibility

Beagle MUST verify:

- declared versions are supported
- no implicit upgrades or downgrades
- no silent fallback to older contracts

Version ambiguity  
→ **REJECT**

---

### 3.5 Recursion & Replay Safety

When applicable, Beagle MUST verify:

- no unbounded recursion
- replayable identity where required
- ORABORUS constraints are satisfied
- recomposition (if used) is deterministic

Violation  
→ **REJECT**

---

## 4. Chunking-Specific Requirements (When Applicable)

Chunking rules apply **only when chunking or CAS is used**, including cases where:

- large artifacts are segmented
- CAS-addressed sub-artifacts are introduced
- evidence is represented by hashes instead of inline payloads
- replayable segmentation or recomposition is required

---

### 4.1 Canonical Chunking Profile

When chunking is invoked, Beagle MUST enforce:

- use of a **declared canonical chunking profile**
- deterministic behavior per the profile’s contract

#### Required Supported Profile

- **FastCDC Baseline Profile A**
- **Method ID:** `zervan://chunking/fastcdc/1`

Beagle MUST have readable access to:
- `chunking/fastcdc/1/README.md`
- `chunking/fastcdc/1/profile.json`
- `chunking/fastcdc/1/DETERMINISM.md`

Missing any required profile artifact  
→ **REJECT**

---

### 4.2 CAS ↔ Chunking Binding

When chunking or CAS is used, Beagle MUST verify:

- `CAS_CHUNK_MANIFEST.md` is present and readable
- chunk identity includes:
  - chunk payload hash
  - hash algorithm identifier
  - chunking Method ID
  - ordering information
- a valid Chunk Set Manifest exists
- recomposition is provably deterministic

Missing binding or recomposition capability  
→ **REJECT**

---

### 4.3 Evidence Classification (Hard Boundary)

Beagle MUST enforce **strict evidence classification**:

#### Primary Evidence
- original artifact byte stream
- identified by dataset-level identity (e.g., SHA-512)

#### Derived Evidence
- chunk payloads
- chunk set manifests
- deterministic metrics derived from primary evidence

Derived evidence MUST:
- be explicitly marked as DERIVED
- never be treated as authority
- never replace primary evidence identity

Misclassification  
→ **REJECT**

---

## 5. Output on Successful Admission

On successful admission, Beagle MUST emit:

- **Validated Artifact**
- **Integrity Report**, binding:
  - hashes computed
  - validation steps performed
  - determinism assertions (if applicable)
- **Canonical Reference ID**
- **Admission Receipt**, binding:
  - primary artifact identity
  - derived artifacts (if any)
  - chunking method ID (if used)
  - CAS references (if used)

Only these outputs are admissible for downstream execution.

---

## 6. Output on Failure

On failure, Beagle MUST emit:

- explicit rejection
- diagnostic reason
- logged event
- no downstream propagation

There is **no partial admission**.  
There is **no degraded mode**.

---

## 7. Binding Clause (Hard)

If Beagle rejects an artifact:

- Zervan does not see it
- no engine may reference it
- no analysis may proceed
- no report may include it

There is **no appeal path inside execution**.

---

## Canonical Statement

> **Beagle does not judge meaning.  
> Beagle judges admissibility.**

If it passes Beagle, execution may begin.  
If it fails Beagle, execution does not exist.

— End of Beagle Contract —

---

## 5.6 Evidence-Engine Boundary

Beagle is part of the primary evidence engine inside the full Zervan spine.

This component does not replace the spine and does not confer authority by existence. The full spine remains INIT → SIGNAL / Signal Ecology → DELTA → K9 / Pups → FAMILY / Teams → TRAVERSAL → VERIFICATION → ANALYTICAL → CREATIVE → GOVERNANCE.

5.6 control line:
- Primary modules produce evidence.
- Primary observers perceive evidence and context.
- Controlled sub-observers pressure evidence.
- Raven reports what survives.
- Audit records what fails.
