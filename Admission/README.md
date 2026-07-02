# Admission Layer — Authority, Economy, and Scope

## What This Layer Is

`Admission/` is a **unified authority surface** responsible for **evidence admissibility** in Zervan.

Any logic that determines:

- **whether evidence may enter the Zervan pipeline**, and
- **under what declared constraints**

belongs **exclusively** within this layer.

Admission governs **entry and routing**, not identity, analysis, meaning, or governance.

---

## Core Admission Principle (Economy First)

> **Admission MUST prefer the simplest, lowest-surface, lowest-dependency path that preserves authority.**

In practice:

- **Beagle is the primary admission path**
- **LeafcutterAnt is invoked only when Beagle is infeasible**

Complexity is **conditional**, not ambient.

---

## Admission Capabilities

Admission is composed of **multiple bounded capabilities**, each with a narrow, explicit role.

### Primary Capability (Default)

- **Beagle (Direct Admission)**  
  Used whenever evidence can be admitted directly through the active channel.

Beagle provides:
- canonical dataset identity (SHA-512)
- admission receipt artifacts
- deterministic analysis substrate
- minimal surface area
- least infrastructure dependency

Beagle-first admission is the **default and preferred economy**, and is what enables Zervan’s **mobile-first operation**.

---

### Conditional Capability (Exceptional)

- **LeafcutterAnt**  
  An admission *pre-gate* invoked **only when direct admission to Beagle is infeasible** due to declared constraints (e.g., file size limits, multi-file evidence sets, unsupported file types, declared compression infeasibility).

LeafcutterAnt is responsible for:
- explicit bounds declaration
- routing decisions (direct vs staged vs halt)
- ephemeral staging orchestration (when required)
- chunking vs no-chunking decisions
- purge enforcement after representation

LeafcutterAnt **does not replace Beagle**.  
It exists solely to bridge **physical or channel constraints**.

---

### Future Capabilities (Examples)

- Manifest validators  
- Envelope verifiers  
- External evidence attestations  
- Policy-based admission filters  

All such capabilities **must live under `Admission/`** and adhere to the same constraints.

---

## Canonical Rule

> **Admission is a unified authority surface.  
Beagle is the primary admission capability.  
LeafcutterAnt is a bounded, conditional capability within that surface.  
No admission logic belongs anywhere else.**

This rule is **architectural**, not stylistic.

---

## Admission Routing (Hard Requirement)

Admission SHALL perform an explicit routing decision **before any data-plane action**.

### Routes

- **DIRECT_TO_BEAGLE**  
  Used only when evidence is eligible for direct admission under declared constraints.

- **LEAFCUTTERANT_STAGING**  
  Used only when DIRECT_TO_BEAGLE is infeasible but staged admission is allowed.

- **HARD_HALT**  
  Used when routing inputs are missing/ambiguous, limits are inconsistent, the channel is unknown, file types are unsupported, or declared compression policy cannot be satisfied.

Routing MUST be:
- explicit
- hash-bound
- fail-closed
- explainable (reason codes)

LeafcutterAnt SHALL NOT be invoked without an explicit routing authorization artifact.

---

## Routing Artifact Contract (Authoritative Output)

Admission routing MUST emit an `admission_route.json` artifact that conforms to the authoritative schema:

- `Admission/admission_route.schema.v2.json`

This routing artifact is **authoritative for downstream routing enforcement** and MUST be:

- **mode-locked** (CONTROLLED / READ_ONLY; discovery disabled; mutation/invention/authority inference disallowed; fail-closed enabled)
- **hash-bound** (canonicalized and SHA-512 hashed)
- **provenance-bound** (hashes of routing inputs)
- **fail-closed by construction** (required fields prevent silent routing)

### Required Routing Evidence (Minimum)

The routing artifact MUST declare:

- `route_selected` (DIRECT_TO_BEAGLE | LEAFCUTTERANT_STAGING | HARD_HALT)
- `reason_codes[]` (non-empty; explainable)
- `evidence` metadata:
  - declared byte counts
  - per-file types
  - size basis (compressed vs decompressed)
  - compression declaration and determinism declaration
  - validation checks and outcomes
- `channel_limits` snapshot used:
  - active channel name
  - byte and file limits
  - supported file types allowlist
  - compression policy
- `inputs` provenance hashes:
  - thresholds SHA-512
  - admission declaration SHA-512
  - active channel limits SHA-512
- `integrity`:
  - routing_sha512
  - canonicalization_method_id

### Enforcement Notes (v2)

- **supported file types must be checked and proven**
  - `validation_checks.file_types_checked = true`
  - `validation_checks.file_types_supported` must reflect the allowlist
  - if unsupported types exist ⇒ HARD_HALT + `UNSUPPORTED_FILE_TYPE` + `unsupported_file_types[]`

- **unknown channel must be explicit**
  - if channel is unknown ⇒ HARD_HALT + `UNKNOWN_CHANNEL`

- **compression must be explicit**
  - evidence MUST declare compression usage, method, and whether determinism is declared
  - size basis MUST be declared (`compressed` vs `decompressed`)
  - if compression is used when disallowed ⇒ HARD_HALT + infeasibility reason

---

## Why Placement Matters

In Zervan, **directory structure conveys authority and lifecycle order**.

Placing admission logic outside the unified Admission layer:
- weakens authority boundaries
- introduces lifecycle ambiguity
- creates brittle, order-dependent behavior
- undermines mobile-first operation
- makes future admission extensions unsafe

Authority is enforced by **placement**, not convention.

---

## What Admission Does *Not* Do

The Admission layer does **not**:

- analyze or interpret data
- infer meaning or intent
- determine governance posture
- attribute behavior
- make risk decisions
- operate as a general data store

It also does **not**:
- persist raw evidence beyond declared ephemeral bounds

Raw bytes may exist **only transiently** to produce representations and must be purged once admissibility artifacts are emitted.

---

## Status

- Authority Surface: **Admission**
- Default Path: **Beagle-First**
- Conditional Path: **LeafcutterAnt (Exceptional)**
- Routing Artifact: **admission_route.json (schema v2)**
- Layering: **Locked**
- Scope: **Evidence admissibility and routing only**
- Applies to: **all current and future admission capabilities**

---

### Final Note

> **Admission complexity must never degrade operator fluidity.  
Mobile-first operation is a design constraint, not an optimization.**
