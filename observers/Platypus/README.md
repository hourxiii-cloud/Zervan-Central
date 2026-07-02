# Platypus — Anomaly Synthesis & Category-Violation Observer

Platypus is a read-only Observer that detects **category violations** and **hybrid signals**:
events that do not fit the current schema, taxonomy, or expected class boundaries.

Platypus exists for the “what is this?” moment — when reality is mixed, misfiled, or new.

Platypus does not learn.  
Platypus does not mutate.  
Platypus observes category rupture.

---

## Role

Platypus detects:

- Mixed-class signatures (features strongly match multiple classes)
- Out-of-schema fields (unexpected columns / unexpected types / unexpected ranges)
- Boundary violations (values valid individually but invalid together)
- “New kind of thing” clusters (novelty that repeats across runs)
- Label incoherence (labels exist but don’t match feature geometry)

Platypus answers:

> “Is this event failing the taxonomy — or is the taxonomy failing the event?”

---

## Observer Constraint

Observers may feed context into Engines and Raven, but never into mutation directly.

---

## Inputs (Canonical Only)

Platypus may consume:

- Beagle-validated schema + structure summaries
- Beagle rejection reasons (as observation artifacts)
- Retriever feature-space telemetry (embeddings, distances, confidence spreads)
- Raven report artifacts for cross-run anomaly recurrence
- Master schema / taxonomy snapshots (read-only)

---

## Outputs

Platypus produces read-only observation artifacts:

- `category_violation_flags` (e.g., “out_of_schema”, “hybrid_signature”, “boundary_break”)
- `novelty_score` (0–1)
- `coherence_score` (0–1) against current taxonomy
- `candidate_new_class` (string, non-binding label suggestion)
- `recommended_actions` (non-binding): “schema review”, “new label proposal”, “collect more samples”

---

## What Platypus Does NOT Do

- It does not approve new labels (PMC only)
- It does not change schema (DoctrineOps only via PMC)
- It does not retrain models (Retriever only)
- It does not block ingestion (Beagle only)

---

## Canonical Statement

> When a thing cannot be named, stability depends on admitting it exists.

---

## 5.6 Primary Observer Boundary

This component is a primary observer in the 5.6 bridge model.

Primary observers are read-only perception surfaces. They may observe, annotate, contextualize, and feed context to modules and Raven. They may not mutate evidence, gate execution, approve changes, write canon, promote authority, or become source-of-truth lanes.
