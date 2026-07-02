# eagle_contract.md — Eagle Observer Contract (Canonical)

**Component:** Eagle  
**Type:** Observer (Read-Only)  
**Layer:** Perception (Non-Mutating)  
**Authority:** None (advisory only)  
**Canon Writes:** Forbidden  
**Version:** 1.0.0

---

## 1. Purpose

Eagle exists to measure **trajectory**.

It detects long-horizon drift, directional bias, and trend coherence across Zervan’s outputs, and publishes **context-only** signals about where the system is heading.

Eagle answers:

> “Is this system stabilizing, drifting, or silently diverging?”

---

## 2. Non-Negotiable Constraints

Eagle is an Observer. Therefore:

- Eagle **must not** learn.
- Eagle **must not** mutate.
- Eagle **must not** gate execution.
- Eagle **must not** approve changes.
- Eagle **must not** write doctrine.
- Eagle **must not** write schema.
- Eagle **must not** write canonical state.

Eagle may emit observation artifacts **only**.

---

## 3. Allowed Inputs (Canonical Only)

Eagle may consume **only** artifacts already passed through Beagle or produced by canon-aligned components.

Allowed inputs include:

- Beagle-validated run logs (timestamps + minimal metadata)
- Retriever outcome summaries (metrics, evaluation deltas, model IDs)
- Raven reports + historical baselines (report cadence, deltas, severity)
- Observer streams already designated canonical (e.g., Owl_Hoot timing metadata, WildFlower emergence markers)
- Time-series aggregates from any component **if and only if** the source is canon-aligned

Forbidden inputs:

- Raw unvalidated datasets
- Direct user-provided ad-hoc data (unless Beagle-validated)
- Any mutation proposals not routed through PMC

---

## 4. Required Outputs (Read-Only Artifacts)

Eagle must output:

1. **Trajectory Vector**
   - direction: stabilizing | drifting | diverging
   - magnitude: scalar (normalized)
   - confidence: 0–1

2. **Horizon Estimate**
   - short / medium / long window characterization
   - expected time-to-instability when applicable

3. **Trend Coherence Score**
   - coherence ∈ [0,1]
   - notes on fracture points / regime shifts

4. **Divergence Warnings**
   - slow-burn alerts where short-term metrics look good but trend is degrading

All outputs must be **context-only** and must not cause state changes.

---

## 5. Routing Rules

Eagle output may be routed to:

- **Raven** (reporting surface)
- **Retriever** (learning context, recommendation shaping)
- **Human review** (dashboard / operator prompt)

Eagle output may **not** be routed directly to:

- Code mutation
- Schema mutation
- Doctrine mutation
- Contract mutation
- Any canonical write pathway

All changes must flow through **PMC**.

---

## 6. Canonical Constraint (Observer Law)

> Observers may feed context into Engines and Raven, but never into mutation directly.

---

## 7. Integrity Requirements

Eagle must be compatible with:

- Beagle Gate 0 validations (hash/structure validation outputs)
- ZEE stability surfaces and drift interpretation
- ZSD stabilization doctrine alignment checks
- ORABORUS recursion safety constraints (no runaway meta-analysis loops)

Eagle must prefer determinism:

- same input window ⇒ same output (within tolerance)
- output artifacts must be traceable to source IDs and timestamps

---

## 8. Failure Modes (What Eagle Prevents)

Eagle exists to prevent:

- Silent long-term instability masked by short-term success
- Drift unnoticed by event-based observers
- False confidence from local optimizations
- Trend fracture that only becomes visible at collapse-time

Any system without Eagle may appear stable until it suddenly is not.

---

## 9. Canonical Statement

> A system is defined not by where it is, but by where it is going.

---

## 5.6 Primary Observer Boundary

This component is a primary observer in the 5.6 bridge model.

Primary observers are read-only perception surfaces. They may observe, annotate, contextualize, and feed context to modules and Raven. They may not mutate evidence, gate execution, approve changes, write canon, promote authority, or become source-of-truth lanes.
