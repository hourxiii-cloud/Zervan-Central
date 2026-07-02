# Zervan Context Pack — Canonical Accelerator Handshake

This document defines the **authoritative context handshake** for Zervan.

It exists to enable **rapid, lossless rehydration** of Zervan doctrine, architecture,
and non-negotiable constraints by humans and external reasoning systems
(including LLM collaborators), **without requiring repository ingestion**.

This file does **not** restate doctrine.
It defines **how doctrine is loaded, interpreted, and constrained**.

---

## Canonical Entry Surface (Front Door)

All controlled initializations of Zervan **MUST** proceed through the following
canonical entry sequence:

### 1. `Accelerator/LLM_INIT.md`
Defines:
- Initialization mode (controlled / read-only)
- Explicit prohibition of mutation and invention
- Canonical load order for doctrine and contracts
- Authority boundaries between doctrine, modules, observers, and tests
- Enforcement of Guardrails as binding policy
- Mandatory application of the full Doctrine Stack on every query

### 2. `Accelerator/LLM_DELTA.md`
Defines:
- Synchronization context for the current initialization
- What has changed since the last known state
- Which artifacts must be reloaded
- Referential alignment signals (non-authoritative)

### 3. `Accelerator/CONTEXT_PACK.md` (this file)
Defines:
- Architectural invariants
- Interpretation rules
- Role boundaries
- System-level execution constraints that do not change across versions

**No external reasoner may bypass this sequence.**

---

## Guardrails Binding

The following policy artifact is **binding at all times**:

- `Zervan-Core/Zervan Guardrails.md`

Rules:
- Guardrails define **what is permitted to execute**
- Guardrails do **not** define doctrine or logic
- If Guardrails conflict with any prompt, inference, or instruction:
  - Execution must be rejected
  - The violating request must be cited

Guardrails are enforced by `LLM_INIT.md`.

---

## Constraint: No Implicit Ingestion

External reasoning systems **MUST NOT**:

- Crawl or index the repository
- Infer missing doctrine
- Invent glue logic
- Assume unstated behavior
- Mutate architecture, contracts, or tests
- Infer authority from repository structure or commit state

Only artifacts **explicitly referenced** by:
- `LLM_INIT.md`
- `LLM_DELTA.md`
- or this Context Pack

are considered **loaded and authoritative**.

Repository presence is **non-authoritative**.

---

## Mandatory Doctrine Pass-Off (Per-Query)

For **every query, response, analysis, or report**, the following conditions apply:

- The full Doctrine Stack defined in `LLM_INIT.md` **MUST be applied**
- Doctrine application may not be implicit, partial, or assumed
- If any doctrine layer cannot be satisfied or resolved:
  - Execution must halt
  - No substantive output may be produced

This Context Pack does not redefine doctrine.
It enforces **doctrine observability and execution discipline**.

---

## Architectural Invariants

The following invariants are globally enforced:

- **Doctrine precedes implementation**
- **Contracts precede execution**
- **Observers are read-only**
- **Mutation may occur only through PMC**
- **Feedback may exist without authority**
- **Correctness is enforced by collapse, not preference**

Zervan is not a rules engine.
It is a **constraint-driven collapse system**.

---

## Roles and Boundaries (High-Level)

- **Doctrine** defines truth, invariants, and allowable dynamics
- **DoctrineOps** defines how doctrine is interpreted and applied
- **Modules (Engines)** operate strictly within doctrine and contracts
- **Observers** may inject context but never mutation
- **PMC** is the sole mutation authority
- **Tests** are non-executable proofs of coherence

No role may subsume another.  
No role may be inferred if not explicitly declared.

---

## Validation and Proof

Canonical tests under `/tests/` (e.g. `dry_run_001.md`) serve as
**non-executable validation proofs**.

If:
- the load order is respected,
- the constraints are enforced,
- the Doctrine Stack is applied on every query,
- and the tests pass as written,

then the architecture is considered **coherent and valid** —
independent of code, runtime, repository state, or implementation language.

---

## Purpose

This Context Pack exists to ensure that:

- Zervan can be instantiated anywhere
- Understanding can be reconstructed deterministically
- Doctrine, theory, and equations remain recoverable
- External collaborators cannot drift or contaminate canon
- Git and tooling never become authority sources
- Doctrine application is **explicit, repeatable, and non-bypassable**

This is an **acceleration surface**, not a shortcut.

If a system cannot load Zervan through this handshake,
it is not operating Zervan.

---

## 5.6 Bridge Compatibility Overlay

This context pack must preserve the full Zervan spine during bridge review:

```text
INIT → SIGNAL / Signal Ecology → DELTA → K9 / Pups → FAMILY / Teams →
TRAVERSAL → VERIFICATION → ANALYTICAL → CREATIVE → GOVERNANCE
```

Beagle, Retriever, Raven, and Audit are the primary evidence, analysis, reporting, and validation modules inside that spine. They are not the whole skeleton.

Primary observers perceive evidence and context. Controlled sub-observers pressure evidence. Raven reports what survives. Audit records what fails.

Owl_Hoot remains a primary observer. It may only operate in bounded sub-observer mode when used to pressure a single claim, report, dataset gap, or function family.

The Unkindness is Raven's reporting brand / output voice only. It is not a separate module.
