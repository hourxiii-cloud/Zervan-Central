# PMC → MC Interface Contract

Status: **Canonical • Non-Optional • Binding**  
Scope: Defines the **only admissible interface** between **Probabilistic Multiverse Computation (PMC)** and **Meta Collapse (MC)**.

This contract is an executable doctrinal constraint, not guidance.

---

## 1. Authority & Precedence

This interface is governed exclusively by the following canonical artifacts, in load order:

1. Accelerator/CONTEXT_PACK.md  
2. Accelerator/LLM_INIT.md  
3. Doctrine/PMC.md  
4. Doctrine/MC.md  

If any conflict exists, earlier artifacts dominate.

---

## 2. Purpose

The PMC → MC interface exists to ensure that:

- **Truth collapse (PMC)** is strictly separated from  
- **Response admissibility gating (MC)**

No logic, inference, or authority may cross this boundary except as explicitly defined below.

---

## 3. Directionality (Non-Reversible)

- **PMC → MC** is the only permitted flow.
- MC may never feed back into PMC.
- MC may not alter, reinterpret, or extend PMC output.

Violation of directionality is a doctrine failure.

---

## 4. PMC Output Contract (Required Fields)

PMC MUST emit a structured output containing **all** of the following fields
for MC to operate without inference:

### 4.1 Structural Truth
- Collapsed truth representation(s)
- Reduced, stable epistemic structure(s)
- Candidate state(s) when operating under read-only constraints

### 4.2 Uncertainty Annotations
- Explicit uncertainty boundaries
- Confidence limits
- Known ambiguity flags
- Conditions under which truth becomes unavailable

Unstated uncertainty is invalid.

### 4.3 Evidence & Eligibility Basis
- Evidence classes used in collapse
- Eligibility constraints applied
- Exclusions or disqualifications enforced

MC may not infer evidence sufficiency.

### 4.4 Governance Context
- Known legal, ethical, organizational constraints supplied **explicitly**
- No inferred or implied governance is permitted

### 4.5 Traceability
- PMC decision identifier
- Validation references (ZEA / ZEE / ZSD / Oraborus)
- Timestamp
- Reconstructability guarantee

If PMC output cannot be reconstructed, it is invalid.

---

## 5. Mode Constraint (Read-Only Enforcement)

When initialization mode is **CONTROLLED / READ-ONLY** (per LLM_INIT.md):

- PMC may evaluate candidate truths and mutations
- PMC may **not** promote or record canonical change
- Mutation lifecycle stages beyond evaluation are non-executable
- All mutation outputs are emitted as **proposed, non-canonical states**

This constraint is mandatory and non-bypassable.

---

## 6. MC Input Constraints

MC may consume **only**:

- PMC output as defined in Section 4
- Explicit uncertainty annotations
- Explicit governance constraints supplied upstream

MC may **not**:
- Access raw data
- Introduce new facts
- Resolve ambiguity by assumption
- Infer intent or attribution
- Retain state or memory

---

## 7. MC Function (Exclusive Responsibility)

MC answers exactly one question:

> “Given what is structurally true, which **response classes** are admissible?”

MC does not determine:
- Fault
- Attribution
- Urgency
- Execution
- Remediation

---

## 8. MC Output Contract

MC MUST produce:

- List of **admissible response classes**
- List of **explicitly inadmissible actions**
- Conditions required to unlock restricted classes
- Uncertainty boundaries (propagated, not invented)
- Governance-safe posture statements

MC outputs are **ephemeral** and non-retained.

---

## 9. Hard Refusal Conditions

MC MUST refuse progression if:

- PMC output is incomplete
- Uncertainty annotations are missing
- Evidence or eligibility basis is absent
- Governance constraints are undefined
- Any MC constraint cannot be satisfied

Refusal halts execution.  
No downstream artifact may be produced.

---

## 10. Prohibited Cross-Layer Behavior

The following are doctrine violations:

- MC generating truth
- MC classifying threats
- MC mandating action
- PMC emitting response recommendations
- Any layer bypassing PMC or MC
- Any implicit inference across the boundary

Violations require execution rejection per LLM_INIT.md.

---

## 11. Canonical Statement

> PMC collapses **what is true**.  
> MC collapses **what is allowed**.  
> Neither may impersonate the other.

This interface is mandatory for all Zervan executions.
