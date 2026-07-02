# Retriever Contract — Learning & Proposal Boundaries

**Status:** CANONICAL  
**Layer:** Learning & Synthesis  
**Authority Scope:** Advisory only (non-authoritative)  
**Mutation Rights:** NONE (canonical) • Learning permitted (internal only)  
**Canonical Collapse:** PMC required  
**Fail-Closed:** Yes (on envelope, determinism, or trace contamination)

---

## 0. Purpose

This contract defines how learning, interpretation, and proposal occur
**without destabilization** and **without unauthorized mutation**.

Retriever operates as a learning and advisory engine.  
Authority remains external.

---

## 1. Allowed Actions

Retriever MAY:

- Train models (internal / non-canonical)
- Update internal representations (non-canonical)
- Generate insights (advisory)
- Propose mutations (non-authoritative proposals only)
- Apply interpretive smoothing to improve stability and confidence estimation
- Emit **advisory** routing, classification smoothing, and score smoothing outputs
  **only inside a finished PKI/ECC trust envelope**

All outputs remain advisory until accepted through PMC.

---

## 2. Interpretive Smoothing Order (Required)

When performing structural learning and local interpretation, Retriever MUST apply stages
in the following order:

### 2.1 K-Means — Structural Discovery / Routing
Establish coarse structure and routing surfaces within feature space.

- Defines the **candidate universe** for subsequent smoothing
- Emits advisory routing weights (if applicable)

Reordering → **HARD FAIL**

---

### 2.2 DM-KNN — Classification Smoothing
Apply neighbor-based smoothing to estimate:

- soft membership weights
- boundary uncertainty
- classification stability

Classification smoothing:
- MUST remain advisory
- MUST NOT overwrite canonical labels
- MUST NOT assert hard reassignment as truth

---

### 2.3 DM-KNN — Score Smoothing
Apply local score diffusion within the routed candidate set to:

- reduce ranking jitter
- stabilize relative ordering
- expose local consistency

Score smoothing:
- MUST occur only after classification smoothing
- MUST remain local to the routed candidate set
- MUST NOT global-smear scores across unrelated regions

All smoothing outputs are interpretive evidence artifacts, not decisions.

---

## 3. Decision vs Trace Separation  
*(Authority Leakage Hard Stop)*

Retriever outputs MUST be split into separate artifacts with separate schemas and references:

- **Decision Artifact (advisory):** ranked list reference (`decision_ref`)
- **Trace Artifact (witness):** verification evidence (`trace_ref`) that MUST NOT recreate the decision

---

### 3.1 Trace Prohibitions (MUST NOT)

Trace schemas MUST NOT include decision-bearing fields such as:

- `rank`
- `final_score`
- `top_k`
- `winner_id`
- ordered lists matching decision output
- “helpful duplicates” that reconstruct ordering
  (e.g., full score vectors aligned to IDs)

Trace must remain a witness.

---

### 3.2 Verifier Semantics (Hard)

A verifier MAY consume `decision_ref` and `trace_ref` and check consistency with:

- claimed algorithms
- parameters
- determinism hooks
- envelope bindings

But:

> **Verifier MUST NOT be able to derive the decision from trace alone.**

---

### 3.3 Regression Gate (Required)

A regression test MUST FAIL if trace contains:

- ordered ID lists matching the decision output
- embedded ranking vectors
- explicit “winner” markers
- duplicate score lists that reconstruct output ordering

---

## 4. PKI/ECC Envelope Binding (Required)

All Retriever smoothing outputs MUST be bound to a PKI/ECC envelope using
**Envelope Canonicalization v1** rules.

The envelope attests:
- provenance and identity
- binding to inputs/config/version
- integrity of outputs + referenced traces
- determinism hooks for reproducibility

The envelope does **not** assert truth.

---

### 4.1 Envelope MUST Bind

#### Identity + Provenance
- `engine_id = "Retriever"`
- `engine_version` (code hash / container digest)
- `config_hash` (includes smoothing params)
- `embedder_version_hash`
- `timestamp`
- `run_id` (monotonic) or `nonce`

#### Input Binding
- dataset envelope ID + hash (Beagle-style)
- query canonical hash + embedder/version binding
- K-Means centroids artifact hash/ref
- KNN artifact hash/ref (if precomputed)
- candidate set definition hash/ref (if applicable)

#### Output Binding
- `decision_ref` (CAS pointer; advisory)
- `trace_ref` (CAS pointer; witness)
- delta refs (before/after summaries) when applicable

#### Determinism Hooks
- seed(s), if any
- explicit tie-break strategy
- iteration / convergence bounds

#### Signature Block
- signer identity (cert/key id)
- signature over canonical serialized scope (per canonicalization v1)
- optional chained signatures (engine → verifier)

---

## 5. Witness Models (Optional, Advisory-Only)

Retriever MAY compute additional models (e.g., calibrated logistic regression, SVM, random forest,
isolation forest) **only as advisory witnesses**.

Witness models:
- MUST NOT bypass the smoothing order
- MUST NOT mutate canonical state
- MUST NOT collapse into authoritative truth
- MUST be bound in the envelope (model version + params + pipeline hashes)
- MUST respect decision vs trace separation (no decision reconstruction via trace)

---

## 6. Forbidden Actions

Retriever MUST NOT:

- Modify canonical state
- Bypass PMC
- Self-authorize changes
- Alter Doctrine or Architecture
- Collapse interpretive evidence into authoritative classification or scoring
- Emit smoothing outputs without PKI/ECC envelope binding
- Leak authority by embedding decision-bearing artifacts in trace

Any violation → **HARD FAIL**

---

## 7. Required Outputs (Per Run)

Every Retriever run MUST produce:

- model/version identifiers (or refs)
- confidence metrics
- stability and uncertainty estimates
- structural and boundary diagnostics (when applicable)
- change proposal artifact (if applicable; non-authoritative)
- **advisory `decision_ref`** (ranked list pointer)
- **`trace_ref`** (non-decision witness evidence)
- **signed envelope** binding `decision_ref` + `trace_ref`
  (Envelope Canonicalization v1)

Outputs remain advisory until accepted through PMC.

---

## 8. Escalation Path

All mutation proposals MUST be submitted to:

- **PMC**
- **PMC_ARENA** (if contested)

Retriever has no escalation authority.

---

## 9. Binding Clause

Learning without permission is allowed.  
Interpretation without permission is allowed.  
Change without permission is not.

— End of Retriever Contract —

---

## 5.6 Evidence-Engine Boundary

Retriever is part of the primary evidence engine inside the full Zervan spine.

This component does not replace the spine and does not confer authority by existence. The full spine remains INIT → SIGNAL / Signal Ecology → DELTA → K9 / Pups → FAMILY / Teams → TRAVERSAL → VERIFICATION → ANALYTICAL → CREATIVE → GOVERNANCE.

5.6 control line:
- Primary modules produce evidence.
- Primary observers perceive evidence and context.
- Controlled sub-observers pressure evidence.
- Raven reports what survives.
- Audit records what fails.
