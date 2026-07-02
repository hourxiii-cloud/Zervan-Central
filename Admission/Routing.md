# Admission Routing — Beagle-First, Fail-Closed

## Purpose

This document defines the **mandatory routing logic** for evidence admission in Zervan.

Routing determines **how evidence enters the system**, not whether it is valid, meaningful, or actionable.

Routing exists to:
- preserve authority
- enforce economy
- prevent unnecessary infrastructure
- protect mobile-first operation
- ensure deterministic, replayable behavior

Routing is a **governance control**, not an optimization.

---

## Core Routing Principle (Hard)

> **Admission MUST route evidence through the simplest admissible path that preserves authority.**

In practice:

- **Beagle is always the default**
- **LeafcutterAnt is invoked only when Beagle is infeasible**
- **Routing decisions are explicit, hash-bound, and fail-closed**

No implicit routing is allowed.  
No downstream override is allowed.

---

## Required Inputs (Fail-Closed)

Routing MUST NOT proceed unless all required inputs are present, readable, and internally consistent.

### Required Artifacts

- `admission_declaration.json`
- `thresholds.json`
- `active_channel_limits.json`

If **any** required artifact is:
- missing
- malformed
- contradictory
- ambiguous

→ **HARD HALT**

No routing decision may be inferred.

---

## Routing Decision Timing (Hard)

Routing SHALL be determined **before any data-plane action occurs**, including:

- hashing
- chunking
- staging
- manifest generation
- analysis
- persistence

No raw bytes may be processed until routing is explicitly authorized.

---

## Routing Decision Logic (Canonical)

Routing is determined by **declared evidence metadata** and **declared channel constraints only**.

### Canonical Decision Table

| Condition | Route |
|---------|------|
| Evidence fits declared channel limits AND evidence_set_count == 1 AND file types supported AND compression policy satisfied | **DIRECT_TO_BEAGLE** |
| Evidence exceeds declared channel size limits | **LEAFCUTTERANT_STAGING** |
| Evidence is a multi-file evidence set (evidence_set_count > 1) | **LEAFCUTTERANT_STAGING** |
| Evidence file types unsupported | **HARD HALT** |
| Compression used but policy disallows or determinism not declared | **HARD HALT** |
| Required routing inputs missing or ambiguous | **HARD HALT** |
| Active channel unknown | **HARD HALT** |

Beagle feasibility is **strictly evaluated**.  
If Beagle is feasible, LeafcutterAnt MUST NOT be invoked.

---

## Routing Outcomes

### Route: DIRECT_TO_BEAGLE

**Description**  
Evidence is admitted directly to Beagle via the active intake channel.

**Characteristics**
- Single-file evidence set only
- Fits declared channel limits
- Supported file type
- Compression (if used) is allowed and deterministically declared
- No staging chamber
- No chunking
- Minimal receipts
- Canonical dataset SHA-512 computed by Beagle

This is the **preferred and default path**.

---

### Route: LEAFCUTTERANT_STAGING

**Description**  
Evidence cannot be admitted directly and must be processed through an ephemeral staging chamber.

**Invocation Conditions**
- Declared channel size limits exceeded
- Multi-file evidence set declared
- Direct admission declared infeasible

**LeafcutterAnt Responsibilities**
- ephemeral staging of raw bytes
- deterministic hashing
- chunking (if required)
- representation generation
- purge enforcement
- emission of manifests and receipts

LeafcutterAnt **does not replace Beagle**.  
It exists solely to bridge **physical or channel constraints**.

**LeafcutterAnt SHALL NOT be invoked without explicit routing authorization.**

---

### Route: HARD_HALT

**Description**  
Routing cannot proceed safely or deterministically.

**Mandatory Conditions**
- required routing inputs missing
- routing inputs ambiguous
- channel limits inconsistent
- active channel unknown
- unsupported file types
- declared compression infeasible
- policy violation detected

HARD_HALT is **terminal** for the routing attempt.

---

## Routing Output (Mandatory Artifact)

Routing MUST emit a hash-bound routing artifact.

### `admission_route.json`

This artifact is **authoritative for downstream enforcement** and MUST conform to:

- `Admission/admission_route.schema.v2.json`

### Required Properties (Non-Exhaustive)

The routing artifact MUST declare:

- `route_selected`
- `reason_codes[]` (non-empty, explainable)
- `evidence`:
  - evidence_set_count
  - declared_total_bytes
  - declared file types
  - size_basis (compressed vs decompressed)
  - compression usage and determinism declaration
  - validation_checks results
- `channel_limits` snapshot used:
  - active channel name
  - byte limits
  - file count limits
  - supported file types
  - compression policy
- `inputs`:
  - thresholds SHA-512
  - admission declaration SHA-512
  - active channel limits SHA-512
- `integrity`:
  - routing_sha512
  - canonicalization_method_id
- `mode_flags`:
  - CONTROLLED
  - READ_ONLY
  - discovery DISABLED
  - mutation / invention / authority inference DISALLOWED
  - fail_closed ENABLED

If this artifact cannot be produced  
→ **HARD HALT**

---

## Enforcement Rules (Hard)

- **LeafcutterAnt MUST reject any invocation without a valid `admission_route.json`**
- **Beagle MUST reject any attempt to bypass routing**
- **Routing decisions MUST NOT be inferred, recomputed, or overridden downstream**
- **Any mismatch between routing artifact and execution path**
  → **HARD HALT**

Routing authority is consumed, not advisory.

---

## Why This Exists

Without explicit routing:

- complexity becomes ambient
- infrastructure grows unnecessarily
- mobile operation degrades
- authority boundaries blur
- replay and auditability collapse

Routing is not optional.  
Routing is not best-effort.  
Routing is **foundational control**.

---

## Non-Goals

Routing does NOT:
- analyze evidence
- inspect content
- infer schema
- determine governance posture
- decide risk or severity

Routing decides **path only**.

---

## Status

- Routing Policy: **LOCKED**
- Default Route: **DIRECT_TO_BEAGLE**
- Conditional Route: **LEAFCUTTERANT_STAGING**
- Terminal Route: **HARD_HALT**
- Enforcement: **Fail-Closed**
- Schema Authority: **admission_route.schema.v2.json**
- Applies to: **all evidence admission flows**

---

### Final Assertion

> **If LeafcutterAnt is running, Beagle must have been infeasible.  
If Beagle was feasible, LeafcutterAnt must not run.**

No exceptions.
