# AnimalKingdom — Self-Play, Fuzzing & Adversarial Validation Module

**Layer:** Validation / Adversarial Testing  
**Authority Scope:** Evidence only (non-canonical)  
**Mutation Rights:** NONE (via AnimalKingdom itself)  
**Learning Rights:** NONE  
**Bypass Allowed:** Never  
**Fail-Closed:** Yes (on boundary or termination violations)

---

## Purpose

**AnimalKingdom** is Zervan’s internal **adversarial validation module**.

It stress-tests doctrine, contracts, engines, and outputs by running
Zervan **against itself** under controlled perturbation.

AnimalKingdom does **not** write canon.  
AnimalKingdom does **not** bypass PMC.  
AnimalKingdom exists to **force collapse toward correctness** through adversarial pressure.

---

## Role

AnimalKingdom performs:

- self-play executions (Zervan vs Zervan)
- contract fuzzing (boundary and edge-case stimulation)
- controlled drift injection
- observer adversarial checks
  - false positives
  - false negatives
- report determinism checks (Raven stability)
- contradiction detection across doctrine and contracts

AnimalKingdom answers exactly one question:

> **“Where does the system break, and how can we prove it?”**

---

## Position in System Order

AnimalKingdom operates **after canonical execution** and **never during authority-bearing runs**.

Canonical order (simplified):

1. Beagle (Gate 0)
2. Admission / Routing
3. Retriever (advisory)
4. PMC / PMC_ARENA
5. MC
6. Raven (reporting)
7. **AnimalKingdom (adversarial validation)**
8. Human decision / remediation

AnimalKingdom **never** influences live execution paths.

---

## Inputs (Canonical Only)

AnimalKingdom MAY consume **read-only canonical artifacts** only.

### Allowed Inputs

- DoctrineOps manifests and doctrine files (read-only)
- Beagle validation artifacts (accepted **and** rejected)
- Observer artifacts:
  - Owl_Hoot
  - WildFlower
  - Eagle
  - Duck
  - MockingBird
  - Platypus
- Retriever recommendation artifacts (advisory only)
- Raven reports and trace maps
- PMC / PMC_ARENA decisions (read-only)

AnimalKingdom MUST NOT consume:
- raw external data
- non-canonical intermediate state
- mutable internal buffers

---

## Perturbation Model (Bounded)

AnimalKingdom MAY apply **controlled perturbations** such as:

- input boundary manipulation
- schema edge cases
- timing distortion
- ordering variation
- noise injection (within declared bounds)
- adversarial observer patterns
- conflicting doctrine surface stimulation

Perturbations MUST be:
- deterministic (seeded)
- replayable
- explicitly declared
- bounded by ORABORUS constraints

Unbounded perturbation → **HARD HALT**

---

## Outputs (Evidence Only)

AnimalKingdom produces **evidence artifacts**, never canon.

### Output Classes

- **Failure Ledger**
  - what failed
  - where
  - under what perturbation
- **Minimal Reproduction Cases**
  - seed
  - perturbation recipe
  - required inputs
- **Stability Scores**
  - baseline vs perturbed comparison
- **Contradiction Maps**
  - claim A vs claim B
  - source references
- **Recommendations**
  - doctrine or contract changes (non-binding)
- **Optional PMC Proposals**
  - advisory only
  - never auto-applied

All outputs are:
- non-canonical
- evidence-only
- traceable
- reproducible

---

## Doctrine Alignment

AnimalKingdom is constrained by:

- **ZEA** — architectural boundaries and no-bypass rules
- **ZSD** — stability as a first-order objective
- **ORABORUS** — termination, recursion, and replay bounds
- **PMC / PMC_ARENA** — mutation governance and adjudication

AnimalKingdom MUST HARD HALT if:
- recursion bounds are violated
- perturbations become non-deterministic
- evidence cannot be replayed
- canonical boundaries are crossed

---

## Constraints (Non-Negotiable)

AnimalKingdom may **never**:

- write or mutate canonical state
- bypass PMC or MC
- inject authority
- “fix” failures automatically
- reinterpret evidence as truth
- override doctrine or contracts

AnimalKingdom may only **reveal weakness**, never resolve it.

---

## Failure Mode

On any failure, AnimalKingdom MUST:

- halt the adversarial run
- emit a failure record
- preserve last stable canonical state
- avoid contaminating future runs

There is no graceful degradation.
There is no partial success.

---

## Canonical Statement

> **If Zervan cannot survive itself, it is not correct yet.**

— End of AnimalKingdom README —

---

## 5.6 Controlled Sub-Observer Contract Addendum

AnimalKingdom may operate as a controlled sub-observer pressure layer in 5.6 deployment review.

This addendum does not relocate or delete the module. It constrains the sub-observer posture:
- synthetic pressure only
- read-only canonical inputs
- no production-data mutation
- no live-target expansion
- no source-of-truth lane
- no primary output steering
- no authority-bearing execution influence
