# Mole — Subsurface / Latent Signal Observer

Mole is a read-only Observer that detects **subsurface signals**: latent structure, slow-emergent drift,
and “hidden threats” that do not present as obvious anomalies in a single run.

Mole does not learn.
Mole does not mutate.
Mole observes what is buried, delayed, or masked.

---

## Role

Mole detects:

- Latent cluster formation (structure that exists before it becomes “loud”)
- Slow drift (small deltas that accumulate across runs)
- Quiet outliers (low-amplitude anomalies that persist)
- Absence-as-signal (missing expected events, silence, gaps)
- Threshold shadowing (behavior that stays just below alert boundaries)

Mole answers:

> “What’s changing beneath what looks stable?”

---

## Observer Constraint

Observers may feed context into Engines and Raven, but never into mutation directly.

---

## Inputs (Canonical Only)

Mole may consume:

- Raven deltas across runs (diffs, regressions, stability changes)
- Beagle-validated run telemetry (timestamps + minimal metadata)
- Retriever structural outputs (cluster assignments, distances, neighborhood topology)
- Duck spin/wobble signals (rotation hiding drift)
- WildFlower emergence markers (field bloom / rising signal density)
- Owl_Hoot timing/cadence signals (absence, delay, periodicity changes)

---

## Outputs

Mole produces read-only observation artifacts:

- `latent_signal_score` (0–1)
- `slow_drift_score` (0–1)
- `quiet_outlier_score` (0–1)
- `absence_signal_score` (0–1)
- `shadow_threshold_score` (0–1)
- `subsurface_mode` (latent_cluster | slow_drift | quiet_outliers | absence | threshold_shadow | unknown)
- `evidence_window` (lookback horizon used for comparison)
- `recommended_actions` (non-binding): “extend window”, “request PMC review”, “increase sampling”, “compare prior receipts”

---

## What Mole Does NOT Do

- Mole does not approve change (PMC only)
- Mole does not gate execution (Beagle only)
- Mole does not retrain models (Retriever only)
- Mole does not assert meaning (interpretation remains advisory until PMC/MC)
- Mole does not write canon (DoctrineOps only)

---

## Canonical Statement

> The most dangerous drift is the drift that stays quiet.

---

## 5.6 Primary Observer Boundary

This component is a primary observer in the 5.6 bridge model.

Primary observers are read-only perception surfaces. They may observe, annotate, contextualize, and feed context to modules and Raven. They may not mutate evidence, gate execution, approve changes, write canon, promote authority, or become source-of-truth lanes.
