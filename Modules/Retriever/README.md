# Retriever — Learning, Synthesis, and Advisory Retrieval Refinement

**Layer:** Learning & Synthesis  
**Status:** Canonical (bounded by Doctrine)  
**Authority Model:** Advisory only (non-authoritative)  
**Mutation Rights:** Learning permitted; canonical mutation prohibited  
**Canonical Collapse:** Requires PMC  
**Fail-Closed:** Yes (on envelope, determinism, or trace violations)

---

## Purpose

**Retriever** is Zervan’s learning and synthesis engine.

It interprets **validated inputs** and produces:
- models
- insights
- predictions
- **advisory retrieval refinements**

Retriever outputs are **witnesses**, not truth.

All canonical impact routes through **PMC**.

---

## Authority & Constraints

Retriever **MAY**:
- learn from validated inputs
- recommend advisory outcomes
- emit advisory rankings, scores, and distributions
- produce witness evidence sufficient for verification

Retriever **MAY NOT**:
- mutate canonical state
- assert canonical truth
- bypass PMC
- bypass MC
- collapse advisory outputs into final authority
- leak decision authority via trace artifacts

Learning without permission is allowed.  
Change without permission is not.

---

## Scope of Capability

Retriever implements the following bounded capabilities:

1. Feature extraction  
2. Pattern learning / model training  
3. Insight generation  
4. Prediction and recommendation  
5. **Advisory retrieval refinement**, including:
   - **K-Means routing**
   - **DM-KNN classification smoothing**
   - **DM-KNN score smoothing**
   - Optional **witness-model channels** (advisory only)

All outputs are **advisory** unless collapsed by PMC.

---

## Canonical Doctrine — DM-KNN Extension  
*(Scoped Capability Doctrine v1)*

Retriever is permitted to compute advisory routing, classification smoothing,
and score smoothing **only inside a finished PKI/ECC trust envelope**.

Retriever **MAY emit**:
- advisory routing weights
- advisory label distributions
- advisory score refinements
- trace evidence sufficient for verification

Retriever **MAY NOT**:
- assert canonical truth
- mutate canonical state
- bypass PMC
- bypass MC
- emit unbound smoothing outputs

---

## Pipeline Ordering (Non-Negotiable)

Retriever smoothing MUST execute in the following order:

### 1. K-Means Routing
- Maps query → cluster routing weights
- Defines the **candidate universe**

### 2. DM-KNN Classification Smoothing
- Adjusts advisory label probabilities
- Defines **interpretive context**

### 3. DM-KNN Score Smoothing
- Refines advisory ranking scores
- Orders within the candidate set

This ordering is canonical because:
- routing defines candidates
- classification defines context
- scoring refines ordering

Reordering → **HARD FAIL**

---

## Decision vs Trace Separation  
*(Authority Leakage Hard Stop)*

Decision output and trace output MUST be **separate artifacts**, schemas, and references.

---

### Decision Artifact (Advisory)

The Decision Artifact is the **ranked list reference**:

- document IDs (or CAS pointers)
- advisory scores (if present)

Decision output:
- is advisory
- is **not canonical truth**
- MUST be bound in a PKI/ECC envelope

---

### Trace Artifact (Witness)

The Trace Artifact provides **verification evidence only**.

Trace artifacts MUST NOT contain:
- `rank`
- `final_score`
- `top_k`
- `winner_id`
- ordered ID lists matching decision output
- duplicated vectors that reconstruct ranking
- aligned score arrays that recreate ordering

Trace artifacts are **witnesses**, not decisions.

---

### Verifier Semantics (Hard)

A verifier consumes:
- `decision_ref`
- `trace_ref`

The verifier checks **consistency** with:
- declared algorithm
- parameters
- envelopes
- determinism hooks

> **The verifier MUST NOT be able to reconstruct the decision from trace alone.**

---

### Regression Gate (Required)

A regression test MUST FAIL if trace contains:
- ordered ID lists matching decision output
- embedded ranking vectors
- explicit “winner” markers
- duplicate score lists that reconstruct ordering

---

## PKI / ECC Envelope Requirements  
*(Retriever Outputs)*

All Retriever advisory outputs MUST be bound to a **PKI/ECC envelope**
using **Envelope Canonicalization v1**.

The envelope **attests**, but does not assert truth.

---

### Envelope MUST Bind

#### Identity & Provenance
- `engine_id = "Retriever"`
- `engine_version` (code hash / container digest)
- `config_hash` (smoothing + witness-model params)
- `embedder_version_hash`
- `timestamp`
- `run_id` or nonce

---

#### Input Binding
- dataset envelope ID + hash (Beagle-style)
- query canonical hash + embedder/version binding
- K-Means centroids artifact hash/ref
- KNN artifact hash/ref (if precomputed)
- candidate set definition hash/ref (if applicable)

---

#### Output Binding
- `decision_ref` (CAS pointer; advisory ranked list)
- `trace_ref` (CAS pointer; witness evidence)
- delta references (before/after summaries) when applicable

---

#### Determinism Hooks
- random seed(s), if any
- explicit tie-break strategy
- iteration / convergence bounds

---

#### Signature Block
- signer identity (cert / key ID)
- signature over canonical serialized scope
- optional chained signatures (engine → verifier)

---

### Economy via Invariance (Cache Safety)

If the envelope binds:
- evidence hash
- query hash
- engine version hash
- config hash
- model / artifact hashes

Then:

> **Equivalent envelope signature ⇒ reuse permitted without recomputation**

---

## Retriever Inputs (via Beagle)

Retriever accepts **validated inputs only**:

- Beagle-admitted datasets
- context packs
- historical state references
- validated observer outputs
- routing artifacts (K-Means centroids)
- neighbor artifacts (KNN refs or derived evidence)
- embedding / feature pipeline references

Unvalidated input → **REJECT**

---

## Retriever Outputs

### Advisory Outputs
- advisory routing weights
- advisory label distributions
- advisory score refinements
- optional witness-model outputs

### Artifacts
- PKI/ECC envelope (canonicalization v1)
- CAS references:
  - `decision_ref`
  - `trace_ref`

### Learning Outputs (Non-Canonical)
- updated models
- insight artifacts
- change proposals
- confidence / stability metrics

Canonical impact requires PMC.

---

## Witness Models (Advisory-Only)

Retriever MAY run additional models **as witnesses only**.

### Recommended Witness
**Calibrated Logistic Regression**
- Purpose: stable linear witness
- Output: `logreg_prob` (witness)
- Audit: top coefficients
- Constraint: must not reconstruct decision ordering

### Other Optional Witnesses
- Linear SVM (calibrated)
- Random Forest (dense/reduced)
- Isolation Forest (anomaly witness)
- LOF (local anomaly witness)
- Conformal prediction (uncertainty wrapper)

Witness channels:
- remain advisory
- are envelope-bound
- never bypass DM-KNN ordering
- never assert canonical truth

---

## Failure Mode (Fail-Closed)

On failure Retriever MUST:
- preserve last stable model
- emit diagnostics
- halt learning/refinement
- never corrupt prior state

Retriever MUST HARD FAIL if:
- envelope verification fails
- trace/decision contamination is detected
- nondeterminism is detected without declared controls

---

## Contract Alignment

Retriever is constrained by:
- **PMC** — canonical collapse and mutation control
- **PMC_ARENA** — adversarial testing
- **Envelope Canonicalization v1**
- **No Authority Leakage Doctrine**

Retriever may advise.  
PMC decides.  
Raven explains.

---

## Canonical Statement

> **Retriever proposes.  
> PMC decides.  
> Raven explains.**

— End of Retriever README —
A Decision Artifact is the **ranked list reference**:
- document IDs (or CAS pointers)
- advisory scores (if present)

Decision is **not canonical truth**.

### Trace Artifact (witness)
A Trace Artifact is evidence sufficient for verification. It must **not** recreate the decision.

Trace schemas MUST NOT include decision-bearing fields such as:
- `rank`
- `final_score`
- `top_k`
- `winner_id`
- ordered lists matching decision output
- duplicates that reconstruct output ordering (e.g., full score vectors aligned to IDs)

### Verifier Semantics
Verifier consumes:
- `decision_ref`
- `trace_ref`

Verifier checks **consistency** against claimed algorithm + parameters, but:

> Verifier MUST NOT derive the decision from trace alone.

### Regression Gate (Required)
A regression test MUST fail if trace contains:
- ordered ID lists matching the decision output
- embedded ranking vectors
- explicit “winner” markers
- duplicate score lists that reconstruct ordering

Trace remains a *witness*, not an alternate decision channel.

---

## PKI/ECC Envelope Requirements (Retriever Outputs)

All Retriever smoothing outputs MUST be bound to a PKI/ECC envelope using canonicalization rules (Envelope Canonicalization v1).

Envelope attests:
- identity/provenance
- binding to inputs/config/version
- integrity of outputs + referenced traces
- deterministic reproducibility hooks

Envelope does **not** assert truth.

### Envelope MUST bind

**Identity + Provenance**
- `engine_id` = "Retriever"
- `engine_version` (code hash / container digest)
- `config_hash` (includes smoothing params and witness-model params)
- `embedder_version_hash` (vectorizer/encoder/embedding pipeline identity)
- `timestamp` + `nonce` or monotonic `run_id`

**Input Binding**
- dataset envelope ID + hash (Beagle-style)
- query canonical hash + embedder/version binding
- K-Means centroids artifact hash/ref
- KNN artifact hash/ref (if precomputed)
- candidate set definition hash/ref (if relevant)

**Output Binding**
- `decision_ref` (CAS pointer to ranked list payload; advisory)
- `trace_ref` (CAS pointer; non-decision witness)
- delta refs (before/after summaries) when applicable

**Determinism Hooks**
- seed(s), if any
- tie-break strategy (explicit)
- iteration bounds / convergence bounds for smoothing

**Signature Block**
- signer identity (cert/key id)
- signature over canonical serialized scope (per canonicalization v1)
- optional chained signatures (engine → verifier)

### Economy via Invariance (Cache Safety)
If envelope binds:
- evidence hash + query hash + engine version hash + config hash + model/artifact hashes  
then reuse is permitted:

Same equivalence signature → reuse prior signed advisory result without recomputation.

---

## Retriever Inputs (via Beagle)

Retriever accepts only **validated** inputs (Beagle-admitted):

- validated datasets
- context packs
- historical state references
- observer outputs (validated)
- routing artifacts (K-Means centroids)
- neighbor artifacts (KNN references or derived neighbor evidence)
- feature/embedding pipeline references (vectorizer/encoder hashes)

---

## Retriever Outputs

Retriever may emit:

### Advisory outputs
- advisory routing weights (K-Means routing)
- advisory label distributions (DM-KNN classification smoothing)
- advisory score refinements (DM-KNN score smoothing)
- optional advisory witness-model outputs (see below)

### Artifacts + envelopes
- PKI/ECC-bound envelope (canonicalization v1)
- CAS references:
  - `decision_ref` (advisory ranked list pointer)
  - `trace_ref` (witness evidence pointer)

### Learning outputs (non-canonical)
- updated models (internal)
- insight artifacts
- change proposals (non-authoritative)
- confidence/stability metrics

All canonical impact routes through PMC.

---

## Witness Models (Advisory-Only Channels)

Retriever may run additional models **only as witnesses**, without creating authority leakage.

### Calibrated Logistic Regression (recommended witness)
- Purpose: stable linear witness for TF-IDF + structured features
- Output: `logreg_scam_prob` (witness), plus `top_coefficients` for audit
- Constraint: coefficients/probabilities must be trace-safe (no decision reconstruction)

### Other optional witnesses
- Linear SVM (calibrated probabilities)
- Random Forest (typically on reduced/dense features)
- Isolation Forest (anomaly witness)
- LOF (local anomaly witness)
- Conformal prediction (uncertainty wrapper)

Witness channels must:
- remain advisory
- be bound in the envelope (model + params + pipeline hashes)
- never bypass the DM-KNN ordering
- never appear as canonical truth without PMC

---

## Recommended Execution Shape (Conceptual)

1) Validate inputs and verify envelopes (fail closed on failure)
2) **K-Means routing** produces candidate universe + routing weights
3) Compute embeddings/features for candidates (bounded, deterministic)
4) **DM-KNN classification smoothing** produces advisory label distribution
5) Optional witness models compute advisory probabilities/anomaly scores
6) **DM-KNN score smoothing** refines advisory ranking
7) Emit:
   - `decision_ref` (ranked list pointer; advisory)
   - `trace_ref` (witness evidence; non-decision)
8) Seal with PKI/ECC envelope (canonicalization v1)

---

## Failure Mode (Fail Closed)

On failure Retriever must:
- preserve last stable model
- emit diagnostics
- halt learning/refinement
- never corrupt prior state
- fail closed if:
  - envelope verification fails
  - trace/decision contamination is detected
  - nondeterminism is detected without declared seeds/controls

---

## Contract Alignment

Retriever is constrained by:
- PMC — mutation control and canonical collapse
- PMC_ARENA — adversarial testing for smoothing failure modes
- Envelope Canonicalization v1 — deterministic signing bytes
- No authority leakage — trace cannot recreate decision

Learning without permission is allowed.  
Change without permission is not.  
Advisory smoothing without envelope binding is not allowed.

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
