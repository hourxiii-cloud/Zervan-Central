# platypus_contract — Zervan Observer Contract (Platypus)

**Component Type:** Observer (read-only)  
**Authority:** Perception only  
**Mutation Rights:** NONE

---

## 1) Purpose

Platypus detects category violations and hybrid/novel signatures that do not fit current schema, labels, or taxonomy.
It publishes observation artifacts that allow Engines and Raven to represent “unknowns” without forcing false certainty.

---

## 2) Allowed Inputs

Platypus MAY consume:

- `beagle.schema_summary.*`
- `beagle.validation_results.*` (including rejection reasons as artifacts)
- `retriever.feature_space.*` (distances, embeddings, confidence spreads)
- `raven.report.*` (cross-run recurrence patterns)
- `taxonomy.snapshot.*` (read-only master schema/taxonomy)

Platypus MUST NOT consume:

- direct mutation proposals not published as observation artifacts
- privileged secrets

---

## 3) Allowed Outputs (Read-Only Artifacts)

Platypus MUST emit:

- `platypus.category_violation_flags` : array[string]
- `platypus.novelty_score` : float [0..1]
- `platypus.coherence_score` : float [0..1]
- `platypus.candidate_new_class` : string | null (non-binding)
- `platypus.recommended_actions` : array[string] (non-binding)

All outputs are **context**, not canon.

---

## 4) Constraints (Non-Negotiable)

- Platypus MUST NOT mutate doctrine, code, schemas, or state.
- Platypus MUST NOT write canon.
- Platypus MUST NOT gate execution.
- Platypus MUST remain deterministic given identical inputs.

---

## 5) Routing Rules

Platypus outputs MAY be routed to:

- Raven (report enrichment + “unknown” surfaces)
- Retriever (training recommendation surfaces, not training execution)
- DoctrineOps (as evidence only, never as direct edits)

Platypus outputs MUST NOT be routed to:

- direct schema mutation paths
- PMC approval signals (PMC may review, Platypus cannot approve)

---

## 6) Failure Modes

If Platypus detects persistent novelty across runs, it MUST recommend one of:

- `request_schema_review`
- `propose_new_label`
- `collect_more_samples`
- `quarantine_unknown_class`

---

## Canonical Clause

> Do not force a label onto what you do not understand.

---

## 5.6 Primary Observer Boundary

This component is a primary observer in the 5.6 bridge model.

Primary observers are read-only perception surfaces. They may observe, annotate, contextualize, and feed context to modules and Raven. They may not mutate evidence, gate execution, approve changes, write canon, promote authority, or become source-of-truth lanes.
