# duck_contract — Zervan Observer Contract (Duck)

**Component Type:** Observer (read-only)  
**Authority:** Perception only  
**Mutation Rights:** NONE

---

## 1) Purpose

Duck detects rotational instability: spin, wobble, and divergence that can masquerade as stability.
It emits context-only artifacts for Engines and Raven.

---

## 2) Allowed Inputs (Canonical Only)

Duck MAY consume:

- `owl_hoot.*` (timing / silence / cadence)
- `eagle.*` (trajectory vectors, horizons)
- `wildflower.*` (emergence markers)
- `raven.report.*` (cross-run deltas)
- `beagle.run_telemetry.*` (validated run metadata)

Duck MUST NOT consume raw unvalidated data.

---

## 3) Required Outputs (Read-Only)

Duck MUST emit:

- `duck.spin_score` : float [0..1]
- `duck.wobble_score` : float [0..1]
- `duck.spin_mode` : string
- `duck.drift_vector_delta` : object | null
- `duck.recommended_actions` : array[string] (non-binding)
- `duck.status` : OK | DEGRADED | INSUFFICIENT_EVIDENCE
- `duck.trace_map` : array[object] (output → source pointers)

All outputs are context, not canon.

---

## 4) Constraints (Non-Negotiable)

- Duck MUST NOT mutate doctrine, code, schemas, models, or state.
- Duck MUST NOT gate execution.
- Duck MUST remain deterministic for identical inputs.

---

## 5) Routing Rules

Duck outputs MAY be routed to:

- Raven (report enrichment)
- Retriever (learning context)
- Eagle/WildFlower (cross-observer correlation)

Duck outputs MUST NOT be routed directly to mutation or PMC approval signals.

---

## Canonical Clause

> Spin is signal, not authority.

---

## 5.6 Primary Observer Boundary

This component is a primary observer in the 5.6 bridge model.

Primary observers are read-only perception surfaces. They may observe, annotate, contextualize, and feed context to modules and Raven. They may not mutate evidence, gate execution, approve changes, write canon, promote authority, or become source-of-truth lanes.
