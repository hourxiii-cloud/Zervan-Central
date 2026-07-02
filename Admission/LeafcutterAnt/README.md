# LeafcutterAnt — Conditional Admission Capability

**Layer:** Admission (Unified Authority Surface)  
**Capability Type:** Conditional Evidence Admission Pre-Gate  
**Lifecycle Position:** Before Beagle (only when required)  
**Authority Scope:** Admissibility and routing only  
**Fail-Closed:** Yes  
**Default Path:** No (Beagle-First)

---

## Purpose

**LeafcutterAnt** is a bounded **Admission capability** invoked **only when direct admission to Beagle is infeasible** due to declared constraints (e.g., channel size limits, multi-file evidence sets, unsupported file types, declared compression infeasibility).

LeafcutterAnt answers exactly one question:

> **“Is Beagle-first infeasible under declared constraints, and what conditional handling is required to preserve admissibility?”**

It does **not** determine meaning, identity, correctness, or governance.  
It determines **whether conditional handling is required before Beagle**.

---

## Position in Admission Economy (Critical)

> **Beagle is the primary admission capability.  
> LeafcutterAnt is exceptional and conditional.**

LeafcutterAnt SHALL NOT run if evidence can be admitted directly to Beagle.

Its existence is justified **only** to bridge physical or channel constraints
(e.g., mobile upload limits), while preserving authority, replayability, and operator fluidity.

---

## Capability Scope

LeafcutterAnt operates strictly in the **control plane**.

### LeafcutterAnt DOES
- Evaluate declared bounds (byte size, evidence set count, per-file types)
- Evaluate deterministic admission thresholds (`thresholds.json`)
- Participate in **routing decisions** (direct vs staged vs halt)
- Decide **chunking vs no-chunking** *only when staging is required*
- Select chunking engine/profile *when required*
- Orchestrate **ephemeral staging** *only when routed*
- Enforce **purge after representation**
- Emit control-plane artifacts and integrity bindings:
  - `admission_route.json` (schema v2, hash-bound)
  - `admission_declaration.json` (hash-bound)
  - associated `.sha512` files (for both artifacts)
- Fail-closed on missing, ambiguous, or contradictory inputs

### LeafcutterAnt DOES NOT
- Run by default
- Replace Beagle
- Seal authoritative evidence identity
- Analyze or interpret data
- Infer schema or semantics
- Decide governance posture or risk
- Persist raw evidence beyond declared ephemeral bounds
- Interact with LLMs

LeafcutterAnt produces **constraints and routing**, not conclusions.

---

## Control-Plane Artifacts (Authoritative for Routing)

### Admission Route (Mandatory)

LeafcutterAnt MAY run **only** when authorized by routing.

Artifacts:
- `admission_route.json`
- `admission_route.sha512`

This artifact binds:
- selected route
- reason codes
- declared evidence bounds
- channel limits snapshot (including supported file types + compression policy)
- validation check outcomes (file types, channel known, compression policy satisfied)
- routing timestamp
- routing canonicalization method identifier
- routing SHA-512 integrity hash

**Schema Authority**
- `Admission/admission_route.schema.v2.json`

**Without a valid Admission Route authorizing staging, LeafcutterAnt MUST HARD HALT.**

---

### Admission Declaration (Mandatory When LeafcutterAnt Runs)

When invoked, LeafcutterAnt emits an Admission Declaration.

Artifacts:
- `admission_declaration.json`
- `admission_declaration.sha512`

The declaration hash binds:
- declared bounds and evidence metadata used for decisions
- threshold rules evaluated (thresholds version binding)
- routing configuration inputs used (hash-bound)
- chunking decision (if any)
- staging bounds and purge requirements
- declarer responsibility / operator accountability surface

**This hash protects the decision, not the data.**  
Authoritative evidence identity hashing occurs downstream in Beagle.

---

## Chunking Decisions

LeafcutterAnt decides **whether** chunking is required **only when staging is invoked**, by evaluating:

- declared byte size
- evidence set count
- threshold rules in `thresholds.json`
- channel constraints in `active_channel_limits.json`

If chunking is required:
- a chunking engine/profile is selected
- chunk execution occurs outside LeafcutterAnt
- chunk manifests are emitted by the executor path and consumed by downstream admission/identity sealing

Chunking engines are **pure executors** and do not evaluate admission policy.

---

## Relationship to the Admission Layer

LeafcutterAnt is **one bounded capability** within the unified Admission layer.

Admission may include additional capabilities over time
(e.g., manifest validators, envelope verifiers, external attestations).

LeafcutterAnt does **not** represent the entirety of Admission.

---

## Relationship to Beagle (Primary)

| Component | Responsibility |
|---------|----------------|
| Admission Router | Determine feasible admission path (explicit, fail-closed) |
| LeafcutterAnt | Bridge infeasible intake (conditional), emit route + declaration artifacts |
| Beagle | Seal authoritative evidence identity (SHA-512), validate admissions, compute canonical receipts |

Beagle:
- computes authoritative dataset and/or chunk SHA-512
- seals evidence identity
- validates admission declarations and routing artifacts
- **HARD HALTS** if admission constraints are violated or artifacts are missing/mismatched

LeafcutterAnt never replaces Beagle and must never weaken Beagle-first economy.

---

## Relationship to Chunking Executors

LeafcutterAnt:
- decides **if** chunking is required
- selects **which** chunking engine/profile to use

Chunking executors:
- execute deterministically
- do not infer bounds
- do not evaluate admission policy
- emit manifests and receipts for downstream verification

LeafcutterAnt MUST NOT live under `Chunking/`.

---

## Relationship to Accelerator / LLM Intake

LeafcutterAnt operates **before any LLM interaction**.

LLM intake gates:
- may require valid Admission artifacts
- MUST NOT perform admission logic
- MUST NOT infer admissibility

**The LLM never decides admissibility.**

---

## Fail-Closed Conditions (Hard)

LeafcutterAnt MUST HARD HALT if:
- invoked without a valid `admission_route.json` authorizing staging
- declared byte size is missing or invalid
- evidence set count is missing or ambiguous
- file types are not explicitly checked or unsupported types are detected
- active channel is unknown
- compression is used but determinism is not explicitly declared
- compression policy is violated under the active channel limits
- thresholds cannot be evaluated
- routing inputs are contradictory or inconsistent
- staging is required but configuration is incomplete
- purge confirmation cannot be produced

There are no fallbacks.  
There is no inference.

---

## Design Principles (Non-Negotiable)

- Beagle-first economy
- Explicit bounds over inferred safety
- Conditional complexity only when forced
- Deterministic decisions over heuristics
- Integrity over convenience
- Mobile-first operation preserved
- Separation of concerns is non-negotiable

---

## Canonical Rule

> **Admission decides admissibility and routing.  
> Beagle seals identity.  
> LeafcutterAnt bridges infeasible intake only.  
> Everything else operates downstream.**

---

## Directory Placement (Authority by Placement)

zervan-core/  
→ Admission/  
→ → LeafcutterAnt/  
→ → → README.md  
→ → → admission_declaration.schema.json  
→ → → admission_route.schema.v2.json  
→ → → thresholds.json  
→ → → decision_tree.md  

LeafcutterAnt does not represent the entirety of Admission.

---

## Status

- Capability: **LeafcutterAnt**
- Layer: **Admission**
- Invocation: **Conditional Only**
- Doctrine: **Locked**
- Dependencies: **Admission Router**
- Downstream Consumers:
  - Beagle
  - Chunking Executors
  - Accelerator Intake Gates

END
