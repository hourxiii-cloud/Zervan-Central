# Zervan — Demo Playbook
Version: Demo_Playbook_v0.1  
Audience: Operator Only (Not for Distribution)  
Duration: ~30 minutes  

---

## Objective

Demonstrate Zervan’s ability to:
- stabilize ambiguous or adversarial inputs,
- enforce constraints deterministically,
- reject incoherent requests,
- and produce structured, auditable outcomes

without revealing internal doctrine, architecture, or implementation.

---

## Pre-Flight Checklist (5 minutes)

Before the session:

- Enable Focus / Do Not Disturb
- Close all unrelated tabs and applications
- Ensure only the Demo Bundle artifacts are visible
- Confirm Controlled Initialization output is clean
- Confirm no repo navigation during demo
- Verbally state: *“This is a capability demonstration under controlled initialization.”*

If any pre-flight condition fails, **delay the demo**.

---

## Demo Structure (30 Minutes Total)

### Segment 1 — Initialization & Guardrails (5 minutes)

**Goal:** Establish authority boundaries and trust.

Steps:
1. Show Controlled Initialization acknowledgment
2. Briefly state:
   - Read-only mode
   - No mutation
   - No invention
   - Guardrails enforced
3. Do **not** explain how enforcement works

Success Condition:
- Tester understands constraints exist and are enforced
- No questions about internals

If asked *“How does it do that?”*:
> “That’s internal. What matters is that it does.”

---

### Segment 2 — Scenario 1: SOC Incident Stabilization (10 minutes)

**Scenario Theme:** Ambiguous security incident with partial data

Example Prompt (you control wording):
> “We have conflicting alerts across cloud logs, EDR, and IAM.  
> Some indicators suggest compromise, others normal behavior.  
> Stabilize the situation and determine next actions.”

What to highlight:
- Refusal to jump to conclusions
- Separation of signal vs noise
- Structured outcome (not speculation)
- Explicit rejection of unsupported claims

Success Condition:
- Output is coherent, bounded, and defensible
- Tester sees reduced ambiguity, not overconfidence

If asked for implementation:
> “Zervan collapses ambiguity before acting. That’s the capability.”

---

### Segment 3 — Scenario 2: GRC / Policy Alignment (10 minutes)

**Scenario Theme:** Technical reality vs regulatory obligation

Example Prompt:
> “A system meets operational needs but violates policy language.  
> Determine compliance posture and required actions.”

What to highlight:
- No policy invention
- Clear articulation of misalignment
- Deterministic recommendations
- No moralizing or preference-based output

Success Condition:
- Output bridges technical and policy domains cleanly
- Tester sees audit-ready reasoning

If asked *“Can it adapt to our policies?”*:
> “That’s a licensing and integration discussion, not a demo topic.”

---

### Segment 4 — Boundary Test (5 minutes)

**Purpose:** Prove the system can say **no**.

Deliberately issue a **violating request**, such as:
- Asking for internal logic
- Requesting mutation
- Asking it to assume missing facts

Expected Behavior:
- Rejection
- Citation of violated constraint
- No workaround offered

Success Condition:
- Tester sees refusal as a feature, not a failure

If tester objects:
> “Any system that can’t say no is unsafe.”

---

## Handling Common Tester Questions

**Q: How does Zervan work internally?**  
A: *“That’s not part of the demo. We evaluate outcomes.”*

**Q: Can we get access to the repo or files?**  
A: *“No. This is capability-only.”*

**Q: Can it be trained/customized?**  
A: *“That’s a separate licensing conversation.”*

**Q: Why not explain more?**  
A: *“Explanation doesn’t improve correctness.”*

---

## Failure Modes & Recovery

If:
- Output drifts → Stop and re-initialize
- Tester pushes boundaries → Cite README_DEMO
- Demo environment leaks → End session immediately

Never improvise around constraints.

---

## Wrap-Up (2 minutes)

Close with:
- “Zervan is evaluated on whether it stabilizes reality under constraint.”
- Invite **feedback on outcomes**, not design
- Do **not** promise access, pricing, or timelines

---

## Final Rule

You are demonstrating **capability**, not **collaboration**.

If a tester wants to co-build, they are not a tester.

---

End of document.
