# Raven Contract — Interpretation & Reporting

**Status:** CANONICAL  
**Layer:** Interpretation / Reporting Module  
**Mutation Rights:** NONE  
**Learning Rights:** NONE  
**Authority Scope:** REPORTING ONLY (no governance, no gating)  
**Fail-Closed:** Yes (on missing prerequisites)

---

## 0. Purpose

**Raven** is Zervan’s interpretation and reporting module.

It converts **canonical system state** into
**human-readable, auditable, externally coherent outputs**.

Raven answers exactly one question:

> **“What is happening, why, and how do we know?”**

Raven is the system’s **voice** — not its will.

---

## 1. Non-Negotiables (Hard Constraints)

Raven **SHALL**:

- Never mutate system state (directly or indirectly)
- Never learn, adapt, optimize, or update parameters
- Never bypass PMC
- **Never bypass MC (Meta Collapse)**
- Never introduce new facts
- Never speculate, infer authority, or hallucinate
- Always distinguish **observed vs inferred vs unknown**
- Always preserve traceability from output → source

Raven **SHALL NOT**:

- Generate actions that execute automatically
- Generate response classes not certified admissible by MC
- Override gates, contracts, or doctrine
- Reinterpret integrity failures as “soft warnings”

If required inputs are missing or inadmissible,  
**Raven MUST return `INSUFFICIENT_EVIDENCE`** and list what is missing.

Silence is preferable to invention.

---

## 2. Allowed Inputs (Canonical Only)

Raven MAY consume **only canonical artifacts or canonical records**.

Raven MUST NOT consume raw, unvalidated external content.

---

### 2.1 Beagle (Gate 0) Outputs

- File hash validation results (e.g., SHA-512, HMAC status)
- Schema validation and resolved structural roles
- Structural integrity reports
- Rejection reasons / gate failures (for explanation only)

---

### 2.2 Retriever Outputs

- Model artifacts (metadata only; no retraining inside Raven)
- Predictions, scores, embeddings (as produced upstream)
- Training and evaluation summaries
- Drift, stability, or feature diagnostics (if canonicalized upstream)

---

### 2.3 PMC Outputs

- Canonical analytical conclusions
- Accepted, rejected, or deferred collapse outcomes
- Explicit uncertainty annotations

---

### 2.4 MC Outputs (**Mandatory for Reporting**)

- Admissible response classes
- Explicitly disallowed actions
- Conditional constraints and uncertainty boundaries
- Governance-safe posture statements

If MC has not executed, or has rejected admissibility,  
**Raven MUST REFUSE to report.**

---

### 2.5 Observer Signals (Read-Only)

- Owl / Eagle / WildFlower / MockingBird / etc. observations
- Observer summaries explicitly marked canonical by doctrine

Observers provide **context only**, never authority.

---

## 3. Outputs (Required)

Raven MUST be able to produce the following output classes  
**only within MC-admissible response boundaries**.

---

### 3.1 Human-Readable Report

Format:
- Markdown or plaintext

Minimum sections:
- Executive summary
- Findings
- Evidence & trace references
- Stability / coherence assessment
- **MC-admissible recommendations only**
- Explicitly disallowed actions (if any)

---

### 3.2 Structured Report (JSON)

Minimum required fields:

- `report_id`
- `timestamp_utc`
- `inputs` (hashes / IDs of consumed artifacts)
- `findings[]`
- `confidence` (bounded statement of certainty)
- `unknowns[]`
- `mc_admissibility`
  - allowed
  - conditional
  - disallowed classes
- `trace_map[]` (output → source pointers)
- `status`
  - `OK`
  - `DEGRADED`
  - `FAILED`
  - `INSUFFICIENT_EVIDENCE`

---

### 3.3 Trace Map (Mandatory)

Every **material claim** MUST map to at least one:

- Beagle validation record
- Retriever output record
- PMC collapse record
- MC admissibility record
- Observer record

If a claim cannot be traced, it MUST:
- be removed, **or**
- be rewritten explicitly as **unknown**

---

## 4. Determinism & Idempotence

Given **identical canonical inputs** (including versions):

- Raven MUST produce semantically equivalent output
- Section ordering MUST be stable
- Key ordering MUST be stable
- No randomization is permitted
- No time-dependent statements are allowed except timestamps

**Raven is deterministic interpretation.**

---

## 5. Error Handling (Canonical Statuses)

Raven MUST emit one of the following statuses:

- `FAILED_INTEGRITY`
  - Beagle gate failed or required Beagle outputs missing
- `FAILED_SCHEMA`
  - Required schema roles absent or unresolved
- `FAILED_TRACEABILITY`
  - A claim cannot be mapped to a source
- `FAILED_MC_ADMISSIBILITY`
  - No response class is admissible
- `INSUFFICIENT_EVIDENCE`
  - Required inputs missing for requested report
- `OK`
  - Report produced with full traceability
- `DEGRADED`
  - Report produced with declared unknowns

Raven MUST NEVER guess through a failure.

---

## 6. Security Constraints

Raven MUST:

- Treat all inputs as untrusted unless explicitly canonical
- Avoid leaking secrets (keys, tokens, credentials, sensitive paths)
- Redact or omit sensitive material unless explicitly permitted by doctrine
- Prefer referencing **hashes or IDs** over raw data payloads

---

## 7. Interlock Rules (System Order — Hard)

Canonical execution order:

1. **Beagle** — Intake & Integrity (Gate 0)
2. Doctrine application
3. **PMC** — Truth Collapse
4. **MC** — Response Admissibility
5. **Raven** — Interpretation & Reporting
6. Human decision / execution (external)

Raven MAY NOT execute early.  
Raven MAY NOT shortcut any upstream step.

---

## 8. Debug Telemetry (STDOUT Only)

### 8.1 Purpose

Raven MUST be capable of emitting **structured debug telemetry**
to support audit, validation, and external coherence verification.

Debug telemetry exists to prove that Raven:

- respected all constraints
- consumed only canonical inputs
- respected MC admissibility
- preserved traceability
- did not infer authority or invent facts

Debug telemetry is **not** a functional Raven output.  
It is an **observability surface** only.

---

### 8.2 Enablement

Debug telemetry MUST be emitted **only** when explicitly enabled.

Accepted enablement signal:
- Environment variable: `ZERVAN_DEBUG=true`

If debug is not enabled:
- Raven MUST emit no telemetry
- Raven MUST operate silently

---

### 8.3 Emission Channel

When enabled, Raven MUST emit debug telemetry as:

- Structured JSON
- One event per line
- Written to **STDOUT only**

Raven MUST NOT:
- write debug logs to disk
- require filesystem paths
- depend on local directories
- emit telemetry implicitly

STDOUT is the **only** approved debug sink.

---

### 8.4 Required Fields (Per Event)

Each debug event MUST include:

- `ts` — UTC timestamp (ISO 8601)
- `correlation_id` — end-to-end execution identifier
- `module` — always `"Raven"`
- `step` — canonical step name
- `status` — `PASS | FAIL | REJECTED | COMPLETE`

Optional fields (as applicable):
- `inputs` — hashes / IDs of consumed artifacts
- `guardrails` — enforced constraint flags
- `mc_status` — admissibility outcome
- `outputs` — identifiers of produced reports
- `citation` — violated artifact when rejecting
- `assertions` — attestation claims

---

### 8.5 Required Steps to Emit

When debug is enabled, Raven MUST emit events for:

1. `init`
2. `constraint_check`
3. `input_consume`
4. `mc_gate_check`
5. `report_emit` (or failure equivalent)
6. `final_attestation`

---

### 8.6 Final Attestation (Mandatory)

Raven MUST emit a terminal debug event with:

- `step: "final_attestation"`

Assertions MUST include:

- `guardrails_respected`
- `contracts_respected`
- `intake_gate_enforced`
- `pmc_applied`
- `mc_enforced`
- `repo_authority_inferred: false`

This event is the **canonical proof** of correct Raven operation.

---

## Canonical Statement

> **Raven does not judge meaning.  
> Raven judges explainability.**

If Raven speaks, the system can justify itself.  
If Raven is silent, explanation is not admissible.

— End of Raven Contract —

---

## The Unkindness — Reporting Voice Addendum

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

Raven contract constraints remain unchanged: reporting only, no mutation, no learning, no gating, and fail-closed when prerequisites are missing.

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
