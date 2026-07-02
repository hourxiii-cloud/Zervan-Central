# Mole Observer Contract

## Observer Class
Read-only / Non-mutating / Non-authoritative

---

## Purpose

Mole detects **subsurface and latent signals** that are not immediately visible
through surface anomaly detection or single-run inspection.

Mole exists to surface:
- slow-emergent risk
- quiet instability
- hidden drift
- absence-as-signal

Mole does not assert meaning or truth.
Mole produces **advisory observations only**.

---

## Scope of Observation

Mole operates across **temporal depth**, not instantaneous state.

It is explicitly designed to reason over:
- accumulation
- delay
- persistence
- silence
- marginal change below alert thresholds

Mole is complementary to:
- Duck (rotational dynamics)
- WildFlower (emergence)
- Eagle (trajectory / horizon)
- Owl_Hoot (timing / cadence)

---

## Inputs (Canonical Only)

Mole MAY consume the following **canonical, validated inputs only**:

- Raven deltas across runs (diffs, regressions, stability changes)
- Beagle-validated run telemetry (timestamps, minimal metadata)
- Retriever structural outputs (clusters, distances, neighborhood topology)
- Duck spin and wobble signals (rotation masking drift)
- WildFlower emergence markers (signal density and bloom)
- Owl_Hoot cadence signals (absence, delay, irregularity)

Mole MUST NOT consume:
- raw external data
- unvalidated artifacts
- inferred or speculative inputs

---

## Outputs (Read-Only Artifacts)

Mole emits a read-only observation artifact containing:

- `latent_signal_score` (0–1)
- `slow_drift_score` (0–1)
- `quiet_outlier_score` (0–1)
- `absence_signal_score` (0–1)
- `shadow_threshold_score` (0–1)
- `subsurface_mode`  
  (`latent_cluster | slow_drift | quiet_outliers | absence | threshold_shadow | unknown`)
- `evidence_window` (temporal horizon examined)
- `recommended_actions` (non-binding, advisory only)

All outputs MUST:
- be explicitly labeled **NON-AUTHORITATIVE**
- preserve uncertainty
- remain replayable under identical inputs

---

## Determinism & Replayability

Given identical inputs and configuration:
- Mole MUST produce identical outputs
- No stochastic behavior is permitted in canonical execution
- All parameters affecting output MUST be recorded

---

## Constraints (Hard)

Mole MUST NOT:

- mutate state
- approve change
- gate execution
- retrain models
- assert authority
- promote interpretation to canon
- bypass PMC or MC
- write doctrine or contracts

Violation of any constraint invalidates the observer output.

---

## Relationship to PMC and MC

- Mole provides **advisory evidence** to PMC
- PMC alone evaluates admissibility and plausibility
- MC alone certifies or promotes outcomes

Mole has no authority to influence collapse directly.

---

## Failure & Denial Semantics

Mole MAY emit:
- partial observations
- null observations
- “insufficient evidence” markers

Denial or silence from Mole is **valid output**, not an error.

---

## Canonical Statement

> What is most dangerous is often what changes too slowly to notice.

---

## 5.6 Primary Observer Boundary

This component is a primary observer in the 5.6 bridge model.

Primary observers are read-only perception surfaces. They may observe, annotate, contextualize, and feed context to modules and Raven. They may not mutate evidence, gate execution, approve changes, write canon, promote authority, or become source-of-truth lanes.
