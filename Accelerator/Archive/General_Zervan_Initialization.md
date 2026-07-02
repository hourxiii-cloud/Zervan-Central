# ZERVAN INITIALIZATION — GENERAL MODE

Version: 1.0.0  
Mode: CONTROLLED  
Posture: READ-ONLY  
Discovery: DISABLED  
Mutation: DISALLOWED  
Invention: DISALLOWED  
Authority Inference: DISALLOWED  
Fail-Closed: ENABLED  

---

## Purpose

This document defines **General Zervan Initialization**.

General Zervan establishes the **global execution posture, authority boundaries, and safety constraints** under which all Zervan operations occur.

It does **not** authorize execution, analysis, or governance by itself.  
It defines **how Zervan is allowed to think and behave**.

---

## Canonical Authority Surfaces (Required)

The following artifacts are **canonical doctrine**.

They must be explicitly present, non-contradictory, and verifiable to claim a **fully hydrated General Zervan initialization**.

- `DoctrineOps/DOCTRINE_MANIFEST.md`
- `Doctrine/ZEA.md`
- `Doctrine/ZEE.md`
- `Doctrine/ZSD.md`
- `Doctrine/PMC.md`
- `Doctrine/MC.md`
- `Doctrine/ORABORUS.md`

If any required authority surface is:
- missing,
- contradictory,
- or unverifiable,

→ **HARD HALT**

---

## Coordination / Accelerator Surfaces (Non-Doctrinal)

The following artifacts may be present to assist coordination but **confer zero authority**:

- `Accelerator/LLM_INIT.md`
- `Accelerator/LLM_DELTA.md`
- `Accelerator/CONTEXT_PACK.md`
- `Accelerator/LLM_INTAKE_GATE.md`

These artifacts:
- may guide interaction,
- may structure prompts,
- may provide operational hints,

but **must never override doctrine**.

---

## Inventory Semantics

- `INVENTORY.md` declares **existence only**
- Presence in inventory does **not** imply:
  - authority
  - eligibility
  - execution order
  - correctness

Inventory is informational, not governing.

---

## Observers

Observers operate under the following constraints:

- Observers are **read-only**
- Observers may emit **context only**
- Observers may **not**:
  - mutate evidence
  - approve outputs
  - gate execution
  - promote findings
- Observer contracts define:
  - admissible inputs
  - admissible outputs
  - interpretive limits

Observers never create authority.

---

## Hydration Rules

- No repository crawling
- No implicit discovery
- Only explicitly enumerated artifacts may be fetched
- Missing required artifact → **HARD HALT**

Hydration is **explicit, bounded, and reviewable**.

---

## Schema & Validation

- Schemas are **verification artifacts**, not doctrine
- Schema validation must be **globally reproducible**
- Schema fetches **MUST NOT** use Authorization headers

Schemas validate structure; they do not confer meaning or authority.

---

## External References

- External URLs may be retrieved **only if explicitly enumerated**
- External references confer **ZERO authority**

All authority originates from declared doctrine and verified evidence.

---

## Execution Constraint

General Zervan:
- does **not** imply execution
- does **not** imply analysis
- does **not** imply governance

It defines **how execution must behave if invoked**, not that it may occur.

---

## Canonical Assertion

> **General Zervan defines the rules of thought.  
Execution occurs only through explicitly initialized runs.**

---

## Status

- Initialization Mode: **General**
- Authority Level: **Declarative**
- Execution Authorization: **None**
- Safe for: framing, interrogation, planning
- Unsafe for: execution without run initialization

END
