# mockingbird_contract — Zervan Observer Contract (MockingBird)

**Component Type:** Observer (read-only)  
**Authority:** Perception only  
**Mutation Rights:** NONE

---

## 1) Purpose

MockingBird detects echo, reflection loops, narrative drift, and contradiction surfaces in Zervan outputs.
It provides non-binding observation artifacts to Engines and Raven for stabilization and governance awareness.

---

## 2) Allowed Inputs

MockingBird MAY consume:

- `raven.report.*` (human-readable + structured report artifacts)
- `retriever.recommendation.*` (recommendations + confidence traces)
- `oraborus.recursion_log.*` (observation-safe recursion telemetry)
- `run_archive.*` (prior run outputs for diff)

MockingBird MUST NOT consume:

- raw mutation proposals not yet published as observation artifacts
- secret material (keys, credentials, private tokens)

---

## 3) Allowed Outputs (Read-Only Artifacts)

MockingBird MUST emit:

- `mockingbird.echo_score` : float [0..1]
- `mockingbird.recurrence_signature` : string (hash/fingerprint)
- `mockingbird.drift_flags` : array[string]
- `mockingbird.contradiction_markers` : array[string]
- `mockingbird.recommended_actions` : array[string] (non-binding)

All outputs are **context**, not canon.

---

## 4) Constraints (Non-Negotiable)

- MockingBird MUST NOT mutate doctrine, code, schemas, or state.
- MockingBird MUST NOT write to canonical stores.
- MockingBird MUST NOT gate execution.
- MockingBird MUST remain deterministic given identical inputs (tolerance only for timestamp formatting).

---

## 5) Routing Rules

MockingBird outputs MAY be routed to:

- Raven (report enrichment)
- Retriever (recommendation calibration)
- Eagle/WildFlower (cross-observer correlation)

MockingBird outputs MUST NOT be routed to:

- direct mutation or commit paths
- DoctrineOps write paths
- PMC approval signals (PMC consumes observations, but MockingBird cannot “approve”)

---

## 6) Failure Modes

If MockingBird detects:

- `echo_score` above threshold
- contradictions above threshold
- rationale drift without evidence

It MUST emit a recommendation such as:

- `request_pmc_review`
- `require_evidence_surface`
- `cooldown_retraining`

---

## Canonical Clause

> Recurrence is not proof. Echo is not truth.

---

## 5.6 Primary Observer Boundary

This component is a primary observer in the 5.6 bridge model.

Primary observers are read-only perception surfaces. They may observe, annotate, contextualize, and feed context to modules and Raven. They may not mutate evidence, gate execution, approve changes, write canon, promote authority, or become source-of-truth lanes.
