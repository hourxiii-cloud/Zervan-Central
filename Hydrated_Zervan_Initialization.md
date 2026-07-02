# ZERVAN INITIALIZATION — HYDRATED MODE  
(UPDATED — OPERATIONAL-COMPLIANT)

Version: 1.0.0  
Hydration Surface Version: zervan://accelerator/hydration_surface/1  

Operational Mode: HYDRATED  
Authority Class: REVIEWABLE_NON_AUTHORITATIVE  

Default Behavior: FAIL_CLOSED  
Discovery: DISABLED  
Promotion Allowed: FALSE  
Conflict Behavior: FAIL  

---

## Purpose

This document defines **Hydrated Zervan Initialization**.

Hydrated Zervan enables **explicit, verifiable data awareness** under strict non-authoritative constraints.

It allows Zervan to:
- fetch explicitly enumerated artifacts,
- touch data deterministically,
- emit reviewable evidence artifacts,

**without** permitting conclusions, decisions, or authority claims.

Hydrated Zervan is **not analysis** and **not governance**.  
It is **data-aware observation with receipts**.

---

## Mode Transition Rule (Hard)

> **Hydrated Zervan may only execute under an active General Zervan initialization.**  
> **Run Initializations may only execute under Hydrated Zervan.**

Any attempt to execute hydration without General Zervan initialized → **HARD HALT**.

---

## Mode Contract (MANDATORY)

- Operational Mode: **HYDRATED**
- Authority Class: **REVIEWABLE_NON_AUTHORITATIVE**
- Valuation Posture: **DVB_ENFORCED**
  - impact, cost, and blame are deferred
- Permitted Conclusions: **DESCRIPTIVE_ONLY**

### Forbidden Conclusions (Hard)
Hydrated Zervan MUST NOT emit:
- findings
- severity assignments
- remediation mandates / POA&Ms
- attribution or intent
- enforcement rules

---

## Mode Integrity Rule (Hard)

If the system cannot emit **all** of the following:
1. Hydration Header
2. Hydration Receipt
3. At least one Minimum Viable Artifact (MVA)

→ **HARD HALT**  
(No silent fallback to General Zervan is permitted.)

---

## Fetch Policy (HARD)

- Only URIs explicitly enumerated in `hydration_profile.full.json` may be fetched
- Any non-enumerated fetch → **HARD HALT**
- Required artifact fetch failure → **HARD HALT**

No implicit discovery is permitted.

---

## Authentication Policy (HARD)

- Authorization headers are permitted **only** for enumerated content fetches
- Authorization headers are **FORBIDDEN** for schema verification fetches
- Schema validation must be cache-stable and globally reproducible

Any Authorization header observed on a schema fetch → **HARD HALT**

---

## Receipt Policy (MANDATORY)

Every fetch MUST emit a receipt entry containing:
- `uri`
- `http_status`
- `sha512`
- `byte_length`
- `retrieval_timestamp`

### Failure Recording (Hard)
- Failures are explicit and recorded
- No silent substitution
- No fallback URIs
- No inferred alternates

### Required Outputs
- `hydration_receipt.json` (required)
- `hydration_visibility_index.json` (optional; informational only)

---

## Minimum Viable Artifacts (MANDATORY)

Hydrated Zervan MUST emit **at least one** reviewable artifact proving data-aware work occurred.

### Acceptable MVA Types (minimum one)

1. **dataset_fingerprint.json**
   - dataset SHA-512 (raw bytes OR declared canonicalization method identifier)
   - row_count, column_count
   - dataset linkage (source filename(s))

2. **schema_snapshot.json**
   - column names
   - dtypes
   - null counts
   - optional cardinality summary

3. **deterministic_descriptive_summary.json**
   - distributions, counts, ranges
   - no severity language
   - no “should” language
   - no action language

---

## Artifact Integrity Requirements

Each emitted artifact MUST include:
- artifact SHA-512
- canonicalization method identifier
- generation timestamp
- mode flags:
  - HYDRATED
  - READ-ONLY
  - NON-AUTHORITATIVE
- declaration:
  > **DERIVED_EVIDENCE — NON-DOCTRINAL**

---

## Failure Rule (Hard)

If **zero** Minimum Viable Artifacts are emitted → **HARD HALT**

---

## Schema Validation (Optional, Fail-Closed If Enabled)

If schema validation is enabled:
- `receipt_schema_uri` MUST be reachable **without authentication**
- schema MUST parse
- receipt MUST validate against schema

Validation failure → **HARD HALT**

---

## Observers (Restricted)

- Observers included **only if explicitly enumerated**
- Observer contracts are **read-only**
- Observer presence does **not** imply execution
- Observer outputs MUST be marked:
  - UNHYDRATED
  - NON_CANONICAL
  - CONTEXT_ONLY

Observers may contextualize, **not conclude**.

---

## Visibility (Optional)

- Optional visibility index may be emitted
- Informational only
- Does NOT assert:
  - existence
  - eligibility
  - execution order

---

## Termination Rules (Hard)

- PASS → exit code `0`
- HARD HALT → exit code `2`

---

## Success Condition (Explicit)

Hydrated Zervan initialization is successful **only if**:

1. Mode Contract header is emitted with `Operational Mode: HYDRATED`
2. `hydration_receipt.json` is emitted
3. At least one Minimum Viable Artifact is emitted
4. All required fetches succeeded
5. Any enabled schema validation succeeded

Otherwise → **HARD HALT (exit code 2)**

---

## Canonical Assertion

> **Hydrated Zervan enables data awareness without authority.  
It proves contact with data, not conclusions about it.**

---

## Status

- Initialization Mode: **Hydrated**
- Authority Level: **Reviewable, Non-Authoritative**
- Requires: **General Zervan Initialization**
- Permits: **Run Initialization**
- Unsafe for: analysis conclusions or governance

END

---

## 5.6 Observer and Sub-Observer Hydration Boundary

Primary observers may be hydrated only when explicitly enumerated and remain read-only perception surfaces.

Canonical primary observers for this bridge include Eagle, Mole, Duck, Wildflower, Mockingbird, Platypus, and Owl_Hoot.

Controlled sub-observers include Osprey, AnimalKingdom, and Armadillo. They are pressure layers only and may not steer output or become source-of-truth lanes.

Owl_Hoot remains a primary observer. If used in bounded sub-observer mode, it may pressure only a single claim, report, dataset gap, or function family and must remain non-mutating, non-authoritative, and non-steering.
