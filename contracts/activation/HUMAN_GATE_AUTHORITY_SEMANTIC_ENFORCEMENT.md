# AC-11 — Human-Gate / Authority Semantic Enforcement

Status: CONTROLLED ACTIVATION CONTRACT
Control: AC-11
Version: vTemporal.41.0
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

AC-11 enforces semantic preservation across the boundary between analytical
state and authority-bearing movement.

The control prevents downstream processing, rendering, integration, or
activation from silently converting analytical or governance state into:

- Human Gate approval;
- execution authority;
- publication authority;
- canonical mutation authority;
- system-population authority;
- certification authority;
- legal authority;
- compliance authority;
- autonomous system authority.

Authority is not inferred.

Human Gate approval is not inferred.

Approval is not execution.

---

## 1. Governing Boundary

Native-v41 preserves:

Evidence
->
PMC
->
CCR
->
MC
->
Raven
->
Human Gate

Analytical state may reach the Human Gate.

Analytical state does not cross the Human Gate by implication.

No upstream component may manufacture downstream authority.

---

## 2. Required Semantic Separation

AC-11 SHALL preserve the distinction among:

- analytical support;
- analytical selection;
- response/output admissibility;
- reporting;
- decision preparation;
- Human Gate decision;
- authorization;
- execution.

These states are not interchangeable.

Supported != approved.

Selected != approved.

Admissible != authorized.

Reported != approved.

Publication-ready != published.

Approved != executed.

Technical capability != authority.

---

## 3. Authority State

Native-v41 system authority remains:

`NONE`

AC-11 SHALL reject any transition that silently changes system authority from
`NONE`.

Human authorization for a bounded transition does not promote the system itself
into autonomous authority.

Human authorization != system authority.

---

## 4. Human Gate State

Native-v41 Human Gate remains:

`ACTIVE`

AC-11 SHALL reject:

- Human Gate removal;
- Human Gate disablement;
- Human Gate bypass;
- synthetic Human Gate approval;
- inferred approval;
- timeout approval;
- approval derived from technical write capability;
- approval derived from repository authorship;
- approval derived from analytical confidence.

Human Gate state MUST remain explicit.

---

## 5. Decision State

Where authority-bearing movement is requested, the Human Gate decision SHALL
remain exactly one of:

- `PENDING`;
- `APPROVED`;
- `DENIED`.

No decision may be inferred from silence.

`PENDING` does not permit authority-bearing movement.

`DENIED` does not permit authority-bearing movement.

`APPROVED` permits only the explicitly bound transition through its separately
governed execution path.

---

## 6. Approval Scope

An approved transition MUST preserve its exact:

- transition class;
- transition target;
- requested scope;
- source analytical identity;
- Room identity;
- Room revision;
- Room state root;
- Authorized View Root;
- evidence boundary;
- evidence ceiling;
- human decision reference.

Approval MUST NOT silently expand beyond those bindings.

Approval scope != general authority.

---

## 7. Analytical State Preservation

Human Gate approval MUST NOT rewrite:

- evidence;
- provenance;
- Room identity;
- Room state;
- evidence boundary;
- evidence ceiling;
- PMC result;
- CCR state;
- MC disposition;
- Raven findings;
- uncertainty;
- unknowns;
- contradictions.

Human approval governs movement.

Human approval does not manufacture evidence or analytical truth.

---

## 8. Admissibility Boundary

MC response/output state SHALL remain distinct from Human Gate authorization.

`ADMISSIBLE` != `APPROVED`.

`CONDITIONAL` != `APPROVED`.

`INADMISSIBLE` != `APPROVED`.

Human Gate MUST NOT silently reinterpret MC state merely to authorize movement.

An `INADMISSIBLE` transition remains blocked through the native pipeline.

A `CONDITIONAL` transition remains conditional until its attributable
conditions are separately satisfied.

---

## 9. Approval / Execution Separation

Human Gate approval is a decision record.

Execution is a separately governed state transition.

AC-11 SHALL reject any semantic transition that equates:

`APPROVED` -> `EXECUTED`

without separately attributable execution evidence.

Approval != execution.

Permission != movement.

Decision record != external side effect.

---

## 10. Publication Boundary

A report may be:

- drafted;
- rendered;
- publication-ready;
- publication-approved.

None of those states independently prove external publication occurred.

Publication-ready != approved.

Publication-approved != published.

Report existence != publication.

---

## 11. Canonical Mutation Boundary

Validation success does not authorize canonical mutation.

Test success does not authorize canonical mutation.

Repository write capability does not authorize canonical mutation.

Candidate completeness does not authorize canonical mutation.

Human Gate authorization for an exact canonical transition is required where
governed.

Validation != promotion.

Write capability != authority.

---

## 12. System Population Boundary

No analytical, reporting, admissibility, or approval state silently authorizes
system population.

System population remains separately governed.

A Human Gate decision must explicitly bind any permitted system-population
transition.

Approval for another transition class MUST NOT carry forward.

---

## 13. Compliance / Legal / Certification Boundary

Analytical state MUST NOT silently become:

- compliance certification;
- legal finding;
- authorization determination;
- disciplinary determination;
- operational certification.

Human Gate approval to issue a claim does not itself prove the underlying
claim.

Authority to issue != evidentiary proof.

---

## 14. Prior Approval

Prior Human Gate approval is not standing approval.

Material change to any bound state requires a new attributable decision where
the transition remains authority-bearing.

Material changes include:

- report identity;
- Room revision;
- Room state;
- evidence boundary;
- evidence ceiling;
- transition class;
- transition target;
- requested scope.

Prior approval != standing approval.

---

## 15. Fail-Closed Conditions

AC-11 SHALL fail closed when:

- authority state is missing;
- authority state is promoted from NONE;
- Human Gate state is missing;
- Human Gate is disabled;
- authority-bearing movement lacks a Human Gate decision;
- APPROVED lacks an attributable human decision reference;
- approval scope is incomplete;
- approval scope silently expands;
- MC disposition is rewritten;
- evidence boundary expands through approval;
- evidence ceiling rises through approval;
- approval is represented as execution;
- publication-ready is represented as published;
- validation is represented as promotion;
- technical write capability is represented as authority;
- prior approval is reused after material state change.

Missing authorization != authorization.

Unknown authorization != authorization.

Fail closed.

---

## 16. AC-11 Lock

Authority remains NONE.

Human Gate remains ACTIVE.

Supported != approved.

Selected != approved.

Admissible != authorized.

Reported != approved.

Publication-ready != published.

Approved != executed.

Technical capability != authority.

Human authorization != system authority.

No decision may be inferred from silence.

PENDING does not authorize movement.

DENIED does not authorize movement.

Approval scope != general authority.

Human approval governs movement.

Human approval does not manufacture evidence.

ADMISSIBLE != APPROVED.

Approval != execution.

Permission != movement.

Decision record != external side effect.

Validation != promotion.

Write capability != authority.

Authority to issue != evidentiary proof.

Prior approval != standing approval.

Missing authorization != authorization.

Unknown authorization != authorization.

Fail closed.

No authority promotion.

No Human Gate bypass.

No external action by implication.

No system population by implication.
