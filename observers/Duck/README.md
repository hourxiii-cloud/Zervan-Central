# Duck — Spin / Wobble / Divergence Observer

Duck is a read-only Observer that detects **spin**, **wobble**, and **rotational divergence** in system behavior.
It exists to measure when a stable trajectory begins to rotate, oscillate, or decouple from its baseline.

Duck does not learn.
Duck does not mutate.
Duck observes rotational dynamics.

---

## Role

Duck detects:

- Spin-up events (increasing rotational behavior around a baseline)
- Wobble (oscillatory instability)
- Dual-spin divergence (paired systems rotating out of phase)
- Center-of-mass drift (stable-looking motion with shifting mean)
- Rotational lock / unlock conditions

Duck answers:

> “Is this stability — or is it spinning?”

---

## Observer Constraint

Observers may feed context into Engines and Raven, but never into mutation directly.

---

## Inputs (Canonical Only)

Duck may consume:

- Owl_Hoot timing/cadence signals
- Eagle trajectory vectors and horizon estimates
- WildFlower emergence markers
- Raven deltas across runs
- Beagle-validated run telemetry (timestamps + minimal metadata)

---

## Outputs

Duck produces read-only observation artifacts:

- `spin_score` (0–1)
- `wobble_score` (0–1)
- `spin_mode` (single_spin | dual_spin | lock | unlock | unknown)
- `drift_vector_delta` (how drift direction changes under rotation)
- `recommended_actions` (non-binding): “increase observation window”, “request PMC review”, “cooldown”

---

## What Duck Does NOT Do

- Duck does not approve change (PMC only)
- Duck does not gate execution (Beagle only)
- Duck does not retrain models (Retriever only)
- Duck does not write canon (DoctrineOps only)

---

## Canonical Statement

> Drift can hide inside spin.

---

## 5.6 Primary Observer Boundary

This component is a primary observer in the 5.6 bridge model.

Primary observers are read-only perception surfaces. They may observe, annotate, contextualize, and feed context to modules and Raven. They may not mutate evidence, gate execution, approve changes, write canon, promote authority, or become source-of-truth lanes.
