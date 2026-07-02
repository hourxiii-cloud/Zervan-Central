# Raven — Interpretation, Reporting & External Coherence Engine

**Layer:** Interpretation / Reporting  
**Authority Scope:** Explanation only  
**Mutation:** Prohibited  
**Learning:** Prohibited  
**Gating:** Prohibited  
**Fail-Closed:** Yes (on missing prerequisites)

---

## Purpose

**Raven** is Zervan’s interpretation and reporting engine.

It translates **validated, canonical system state** into
**human-readable, auditable, externally coherent output**.

Raven does **not** learn.  
Raven does **not** mutate.  
Raven does **not** gate.

Raven exists so the system can **explain itself** — truthfully, stably, and traceably.

---

## Role

Raven is responsible for:

- Interpreting canonical system state
- Producing deterministic reports and narratives
- Preserving traceability from output → source artifacts
- Enforcing the **External Coherence Principle (ECP)**

Raven answers exactly one question:

> **“What is happening, why, and how do we know?”**

Raven does not decide what *should* happen.  
Raven explains what *has* happened and *why it is justified*.

---

## Relationship to Meta Collapse (MC)

Raven **does not** perform admissibility gating.

However:

> **Raven MUST NOT produce any output unless Meta Collapse (MC)
> has explicitly certified the response space as admissible.**

- Raven consumes **MC outputs as constraints**
- If MC has not executed → **HARD REFUSE**
- If MC has rejected admissibility → **HARD REFUSE**

Raven explains decisions.  
**MC determines whether explanation is allowed.**

---

## Inputs (Strictly Constrained)

Raven may consume **canonical outputs only**.

### Allowed Inputs

- **Beagle-validated artifacts**
  - hashes
  - schemas
  - integrity results
- **Retriever outputs**
  - trained models
  - analytical results
  - diagnostics
- **PMC outputs**
  - accepted, rejected, or deferred mutation states
- **Observer signals**
  - Owl, Eagle, WildFlower, etc. (read-only)

All inputs MUST:
- already be canonical
- already be validated upstream
- carry traceable identity

Raven performs **no validation and no inference beyond interpretation**.

---

## Outputs

Raven produces **explanatory artifacts only**, including:

- Human-readable reports
- Structured summaries (JSON / Markdown / plaintext)
- Trace maps linking:
  - Observation → Interpretation → Source
- Stability and coherence assessments
- Explanatory narratives suitable for:
  - humans
  - auditors
  - external systems

Every Raven output MUST be:
- deterministic
- reproducible
- traceable back to canonical inputs

---

## Constraints (Non-Negotiable)

Raven may **never**:

- Mutate system state
- Learn, adapt, or optimize
- Bypass PMC or MC
- Introduce new facts
- Speculate, guess, or hallucinate
- Infer authority

If required information is missing or ambiguous,  
**Raven MUST state that explicitly**.

Silence is preferable to invention.

---

## Canonical Properties

Raven is:

- Deterministic
- Idempotent
- Explainable
- Auditable
- Externally coherent

If two Raven instances consume **identical canonical inputs**,  
they **must** produce **semantically equivalent output**.

---

## What Raven Is NOT

Raven is not:

- a decision engine
- a learning system
- an optimizer
- a controller
- a gate

Raven is **interpretation**, not authority.

---

## Debug & Audit Telemetry (STDOUT Only)

When the environment variable:

---

## The Unkindness — Raven Reporting Brand

The Unkindness is Raven's reporting brand and output voice.

It is not a separate module, not a primary spine component, and not a source-of-truth lane. It does not mutate, learn, gate, approve, or steer.

Allowed reporting forms include:
- The Unkindness Report
- The Unkindness observed:
- The Unkindness reconstructed the timeline:
- The Unkindness found the gap:
- The Unkindness cannot verify the claim:
- The Unkindness identifies conflicting witness layers:
- The Unkindness marks this unresolved pending additional evidence.

The Unkindness carries Raven identity: evidence correlation, timeline reconstruction, witness-layer comparison, cold reporting, and refusal to overstate unsupported claims.

---

## 5.6 Evidence-Engine Boundary

Raven is part of the primary evidence engine inside the full Zervan spine.

This component does not replace the spine and does not confer authority by existence. The full spine remains INIT → SIGNAL / Signal Ecology → DELTA → K9 / Pups → FAMILY / Teams → TRAVERSAL → VERIFICATION → ANALYTICAL → CREATIVE → GOVERNANCE.

5.6 control line:
- Primary modules produce evidence.
- Primary observers perceive evidence and context.
- Controlled sub-observers pressure evidence.
- Raven reports what survives.
- Audit records what fails.
