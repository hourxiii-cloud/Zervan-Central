# LeafcutterAnt — Admission Decision Tree (Conditional Staging Only)

Version: 1.1.1  
Layer: Admission (Unified Authority Surface)  
Capability: LeafcutterAnt (Conditional Admission Pre-Gate)  
Mode: CONTROLLED • Posture: READ-ONLY  
Fail-Closed: ENABLED  
Default Path: Beagle-First (LeafcutterAnt is conditional only)

---

## Purpose

Define the deterministic decision procedure LeafcutterAnt uses **only when it has been explicitly routed to run**.

LeafcutterAnt exists to bridge **infeasible Beagle-first intake**
(e.g., channel limits, multi-file evidence sets, declared compression infeasibility)
while preserving:

- Beagle-first economy
- deterministic replay
- integrity of control-plane declarations
- fail-closed behavior

LeafcutterAnt does **not** decide meaning, identity, correctness, or governance.  
LeafcutterAnt decides **conditional handling requirements before Beagle**.

---

## Precondition (Non-Negotiable)

LeafcutterAnt MAY execute **only** if authorized by a valid routing artifact:

> **Without a valid `admission_route.json` explicitly selecting `LEAFCUTTERANT_STAGING`,
> LeafcutterAnt MUST HARD HALT.**

This is the single most important rule in this file.

---

## Inputs (Required)

LeafcutterAnt must obtain all inputs deterministically.

### Route Input (Mandatory)

- `admission_route.json`
- `route_selected` (must equal `LEAFCUTTERANT_STAGING`)
- `reason_codes`
- `channel_limits` snapshot
- `declared_evidence_set` (logical evidence items + declared sizes)

### Evidence Inputs (Per Item; Mandatory)

For each evidence item `E[i]`:

- `filename` (logical name only; no paths)
- `byte_size` (measured; integer; > 0)

Optional (informational only, non-authoritative):
- `row_count`

### Configuration Inputs (Mandatory)

- `thresholds.json`
- `default_rule` from `thresholds.json`

Optional (only if referenced by thresholds):
- chunking engine/profile mapping

---

## Outputs (Control-Plane Only)

LeafcutterAnt MUST emit **control-plane artifacts only**:

- `admission_declaration.json`
- `admission_declaration.sha512`

LeafcutterAnt MUST NOT emit:
- authoritative dataset identity hashes
- chunk hashes
- analysis artifacts
- persistence artifacts beyond ephemeral staging receipts (if implemented elsewhere)

---

## Hard Fail-Closed Conditions (HARD HALT)

LeafcutterAnt MUST HARD HALT if **any** condition below is met.

### H0 — Missing or Unauthorized Route (Critical)

- `admission_route.json` missing, unreadable, or schema-invalid
- `route_selected` missing
- `route_selected != "LEAFCUTTERANT_STAGING"`
- Route indicates Beagle-first is feasible, but LeafcutterAnt was invoked anyway

---

### H1 — Missing or Ambiguous Evidence Set

- `declared_evidence_set` missing or empty
- Duplicate logical filenames
- Missing evidence items
- Contradictory evidence counts or totals

---

### H2 — Missing or Invalid Bounds

For any evidence item:

- `byte_size` missing
- `byte_size` not an integer
- `byte_size <= 0`

---

### H3 — Missing Threshold Rules

- `thresholds.json` missing or unreadable
- `default_rule` missing
- `default_rule` not present in `rules`

---

### H4 — Rule Cannot Be Evaluated

The selected rule is missing any required field:

- `decision.type`
- `decision.operator`
- `decision.max_inline_bytes`

---

### H5 — Contradictory Declaration

- `chunking_required = true` but:
  - `chunking.engine_ref` missing, or
  - `chunking.profile_ref` missing, or
  - `chunking.target_chunk_bytes` missing
- `chunking_required = false` but a `chunking{}` object is present
- Routing artifact contradicts declared channel limits **without** a valid non-size reason
  (e.g., multi-file restriction)

---

### H6 — Ephemeral Staging Cannot Be Confirmed (If Implemented)

If a staging chamber exists and purge confirmation is required by policy:

- purge confirmation cannot be produced

(If purge confirmation is not implemented in this capability, this condition MUST NOT be referenced.)

---

## Decision Procedure (Deterministic)

### Step 0 — Validate Route Authorization (Mandatory)

- Load `admission_route.json`
- Verify `route_selected == "LEAFCUTTERANT_STAGING"`
- Verify `declared_evidence_set` entries are complete and well-formed

If any check fails → HARD HALT.

---

### Step 1 — Load Configuration (Mandatory)

- Load `thresholds.json`
- Select `rule_id = thresholds.default_rule`

Rule override is permitted **only** if explicitly authorized upstream.  
Unauthorized override attempts → HARD HALT.

---

### Step 2 — Determine Chunking Requirement (Per Evidence Item)

For each evidence item `E[i]`:

Given:
- `b = E[i].byte_size`
- `m = rules[rule_id].decision.max_inline_bytes`
- `op = rules[rule_id].decision.operator` (expected `>`)

Compute:
