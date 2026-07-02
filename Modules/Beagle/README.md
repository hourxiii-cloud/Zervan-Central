# Beagle — Secure Intake & Integrity Engine (Gate 0)

**Layer:** Execution (First Executable Engine)  
**Gate:** 0 (Non-Bypassable)  
**Authority Scope:** Integrity, admissibility, identity sealing  
**Fail-Closed:** Yes  
**Bypass Allowed:** Never

---

## Purpose

**Beagle** is the first executable engine in Zervan.

It governs **all data, models, context, configuration, and signals** entering the system and enforces:

- integrity
- determinism
- admissibility
- contract and schema alignment

**Nothing executes before Beagle.  
Nothing bypasses Beagle.**

Beagle does not decide meaning or truth.  
Beagle ensures Zervan never reasons over **undefined, drifting, or unverifiable inputs**.

---

## Role (Gate 0)

Beagle is responsible for **Gate 0 admission**.

It enforces:
- structural integrity
- deterministic identity
- schema and contract alignment
- governance wiring requirements
- fail-closed rejection of inadmissible inputs

Beagle does **not** interpret data.  
Beagle ensures execution is **lawful**.

---

## What Beagle Protects

If it enters Zervan, **Beagle sees it first**.

Beagle validates and admits:
- datasets (primary evidence)
- chunked sub-artifacts (derived evidence)
- context packs
- models
- configuration artifacts
- external signals
- internal engine handoffs

No object—raw or derived—may enter the execution graph without Beagle validation.

---

## Doctrine Alignment

Beagle enforces doctrine **procedurally**, not interpretively.

Beagle is bound by:
- **ZEA** — architectural boundaries and no-bypass rules
- **ZSD** — stability and degradation constraints
- **ORABORUS** — recursion and replay safety
- **PMC** — admissibility preconditions and mutation permissions

Beagle does **not** perform PMC collapse or MC gating.  
Beagle ensures downstream execution **may lawfully occur**.

---

## Relationship to Admission

Admission determines **whether** evidence may enter and **how** it must be routed.

Beagle:
- consumes Admission artifacts
- validates routing and declaration integrity
- enforces declared constraints
- seals authoritative identity

Beagle MUST HARD HALT if:
- routing artifacts are missing
- admission declarations are missing
- declarations contradict observed intake behavior

Beagle is **not** an admission router.  
Beagle is the **execution gate**.

---

## Chunking & CAS Admission (Governance-Critical)

Beagle is the **only lawful entry point** for:

- chunked evidence
- CAS-addressed artifacts
- hash-referenced evidence representations

### When Chunking Is Required

Chunking is REQUIRED when intake involves:
- large artifacts
- distributed or partial analysis
- CAS-addressed sub-artifacts
- replayable segmentation or recomposition
- evidence represented by hash references instead of inline payloads

If chunking is required and cannot be performed deterministically:

→ **HARD HALT (fail-closed)**

---

## Canonical Chunking Profile

When chunking is invoked, Beagle MUST use a **declared canonical profile**.

### Required Supported Profile

- **FastCDC Baseline Profile A**
- **Method ID:** `zervan://chunking/fastcdc/1`

Beagle MUST have readable access to:
- `chunking/fastcdc/1/README.md`
- `chunking/fastcdc/1/profile.json`
- `chunking/fastcdc/1/DETERMINISM.md`

Missing **any** required profile artifact  
→ **HARD HALT**

---

## CAS ↔ Chunking Binding Requirement

Whenever chunking or CAS is used, Beagle MUST enforce:

- `CAS_CHUNK_MANIFEST.md` is present and readable
- chunk identity binding rules are followed
- recomposition is provably deterministic

If CAS or chunking is invoked without this manifest:

→ **HARD HALT (fail-closed)**

---

## Beagle Intake Responsibilities (Chunked Evidence)

When admitting chunked evidence, Beagle MUST perform **all** steps below:

### 1. Identify Primary Evidence
- Compute SHA-512 over the **full original byte stream**
- Record size and hash as **PRIMARY EVIDENCE**

### 2. Perform Deterministic Chunking
- Use the declared chunking Method ID
- Enforce determinism per profile contract

### 3. Hash Chunk Payloads
- Compute SHA-512 for each chunk payload
- Treat chunks as **DERIVED EVIDENCE only**

### 4. Emit Chunk Set Manifest
Bind:
- source artifact hash
- chunking method ID
- ordered chunk list
- chunk payload hashes

Hash the manifest itself.

### 5. Admit Chunks into CAS
- Store chunks by payload hash only
- Verify round-trip integrity (store → fetch → rehash)

### 6. Emit Intake Receipt
Bind:
- primary artifact identity
- chunking method + determinism contract hashes
- chunk set manifest hash
- CAS admission verification
- explicit evidence classification:
  - **PRIMARY**
  - **DERIVED**

Failure at **any** step  
→ **REJECT + HARD HALT**

---

## Evidence Classification (Hard Boundary)

Beagle enforces the following classifications:

### Primary Evidence
- original artifact byte stream
- identified by dataset-level SHA-512

### Derived Evidence
- chunk payloads
- chunk set manifests
- deterministic metrics derived from primary evidence

Derived evidence:
- MUST be explicitly marked
- MUST NOT be treated as authority or truth
- MUST NOT replace primary evidence

---

## Failure Mode (Non-Negotiable)

On any failure, Beagle MUST:
- reject the input
- emit a rejection reason
- preserve last stable state
- prevent downstream execution

Beagle never degrades gracefully.  
Beagle **fails closed**.

Always.

---

## Canonical Statement

> **Beagle does not decide what is true.  
> Beagle decides whether execution is allowed to begin.**

— End of Beagle README —

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
