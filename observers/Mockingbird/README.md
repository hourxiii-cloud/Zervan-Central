# MockingBird — Reflection / Echo / Narrative Drift Observer

MockingBird is a read-only Observer that detects **echo**, **reflection loops**, and **narrative drift** inside Zervan outputs.
It exists to notice when a system starts repeating itself, amplifying its own language, or confusing recurrence for truth.

MockingBird does not learn.  
MockingBird does not mutate.  
MockingBird observes recursion tone.

---

## Role

MockingBird detects:

- Echo loops (self-quotation, repeated claims, repeated justifications)
- Narrative drift (explanations that change while facts stay constant)
- Self-amplification (“confidence inflation” without new evidence)
- Contradictory story surfaces (two incompatible narratives coexisting)
- Degeneration into rhetoric (style increases while signal decreases)

MockingBird answers:

> “Is the system repeating itself — and calling it progress?”

---

## Observer Constraint

Observers may feed context into Engines and Raven, but never into mutation directly.

---

## Inputs (Canonical Only)

MockingBird may consume:

- Raven report artifacts (summaries, conclusions, recommendations)
- Retriever output metadata (confidence traces, feature notes, rationale strings)
- PMC/Oraborus recursion logs (if exposed as observation artifacts)
- Prior run reports for comparison (run N vs run N-1)

---

## Outputs

MockingBird produces read-only observation artifacts:

- `echo_score` (0–1)
- `recurrence_signature` (hash or fingerprint of repeated phrasing/claims)
- `drift_flags` (e.g., “rationale changed”, “conclusion unchanged”, “confidence inflation”)
- `contradiction_markers` (IDs of conflicting statements)
- `recommended_actions` (non-binding): “request PMC review”, “require evidence”, “cooldown”

---

## What MockingBird Does NOT Do

- It does not approve changes (PMC only)
- It does not gate execution (Beagle only)
- It does not update models (Retriever only)
- It does not write canon (DoctrineOps only)

---

## Canonical Statement

> If the story changes without new evidence, the system is drifting.

---

## 5.6 Primary Observer Boundary

This component is a primary observer in the 5.6 bridge model.

Primary observers are read-only perception surfaces. They may observe, annotate, contextualize, and feed context to modules and Raven. They may not mutate evidence, gate execution, approve changes, write canon, promote authority, or become source-of-truth lanes.
