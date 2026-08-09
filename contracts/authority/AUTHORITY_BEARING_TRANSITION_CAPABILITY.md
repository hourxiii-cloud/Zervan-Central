# AC-06 — Authority-Bearing Transition Capability

Status: CONTROLLED ACTIVATION PATCH
Priority: CRITICAL
Version: vTemporal.41.0
Activation Branch: ac/v41-activation
Authority: NONE
Human Gate: ACTIVE

## 0. Purpose

AC-06 defines the machine-enforced capability boundary for authority-bearing
transition execution.

Human Gate is not a status field.

Human Gate authorization is an exact binding between an attributable decision
and one permitted movement.

Approval != execution.

Admissibility != authorization.

Preparation != execution.

Execution must resolve against the exact approved state.

## 1. Governing Binding

Every authority-bearing execution SHALL bind:

Decision
× Class
× Target
× Room
× Revision
× State
× View
× Evidence
× Scope
× Execution

No element may be silently substituted.

No element may be silently broadened.

No element may be silently inherited from another transition.

Exact authorization binding is required.

## 2. Decision Binding

Execution requires one attributable Human Gate decision.

Decision states remain:

- PENDING
- APPROVED
- DENIED

Only APPROVED may make the exact bound movement execution-eligible.

PENDING != APPROVED.

DENIED != APPROVED.

Approval identity != execution identity.

Approval existence != execution readiness by itself.

## 3. Transition Class Binding

Authorization SHALL bind exactly one transition class.

Authority-bearing classes include the classes governed by the active Human Gate
boundary, including:

- PUBLICATION
- EXTERNAL_DEPLOYMENT
- PRODUCTION_EXECUTION
- SYSTEM_POPULATION
- PACKAGE_PROMOTION
- COMPLIANCE_CLAIM
- LEGAL_FINDING
- CERTIFICATION_CLAIM
- OPERATIONAL_AUTHORITY
- DISCIPLINARY_OR_HR_ACTION
- AUTHORITY_BEARING_AUTOMATION
- IRREVERSIBLE_EXTERNAL_CHANGE

Approval for one class does not authorize another class.

Class substitution invalidates execution eligibility.

## 4. Target Binding

Authorization SHALL bind one exact transition target.

Target substitution is prohibited.

A technically reachable target is not an authorized target.

Approval target != target family.

Approval target != similar target.

Approval target != convenient replacement target.

## 5. Room Binding

Authorization SHALL bind the canonical Room Object identity.

Execution against another Room is prohibited.

Similar Room != approved Room.

Derived Room != approved Room unless separately authorized.

Branch != inherited approval.

## 6. Revision Binding

Authorization SHALL bind the exact Room revision identity reviewed by Human Gate.

A materially changed revision invalidates prior execution eligibility.

Prior approval != approval of later revision.

## 7. State Binding

Authorization SHALL bind the exact Room state root reviewed by Human Gate.

State drift invalidates execution eligibility unless a separately governed rule
explicitly permits and records that state movement.

Approval against historical state MUST NOT silently execute against current
state.

Stale approval is invalid for changed material state.

## 8. Authorized View Binding

Authorization SHALL bind the exact Authorized View Root reviewed by Human Gate.

Execution MUST NOT silently use a broader view.

A narrower or different view does not automatically inherit approval.

Visibility change != approval carry-forward.

## 9. Evidence Binding

Authorization SHALL bind:

- evidence boundary;
- evidence ceiling;
- material evidence state required by the approved movement.

Execution MUST NOT:

- broaden the evidence boundary;
- raise the evidence ceiling;
- substitute materially different evidence state;
- treat later evidence as retrospectively approved.

Human approval does not manufacture evidence.

## 10. Scope Binding

Authorization SHALL bind explicit requested scope.

Execution scope MUST be equal to or narrower than the exact authorized scope
only where narrowing preserves the approved movement semantics.

Scope expansion is prohibited.

Approval scope != general authority.

Unspecified scope != unlimited scope.

## 11. MC Admissibility Boundary

MC admissibility remains upstream analytical/governance state.

MC states include:

- ADMISSIBLE
- CONDITIONAL
- INADMISSIBLE

ADMISSIBLE != authorized.

ADMISSIBLE != execution-ready.

CONDITIONAL != authorized.

INADMISSIBLE != authorized.

Human Gate MUST NOT convert MC classification merely by approving a movement.

## 12. Conditional Satisfaction

A CONDITIONAL movement MUST NOT become execution-eligible until every required
condition is separately attributable as satisfied.

Condition satisfaction SHALL preserve:

- condition identity;
- satisfaction evidence;
- satisfaction time or sequence;
- provenance;
- applicable authorization context.

Missing condition satisfaction blocks execution.

Condition assumed satisfied != condition satisfied.

CONDITIONAL + approval != executable.

## 13. Preparation / Execution Separation

Preparation remains inert when it does not perform authority-bearing movement.

Preparation may include:

- drafting;
- rendering;
- assembling;
- validating;
- packaging;
- calculating;
- preparing movement requests;
- preparing execution plans.

An operation is execution when it performs or causes the authority-bearing
movement itself.

Naming execution "preparation" does not make it preparation.

Side effect determines boundary.

Authority-bearing effect disguised as preparation is execution and requires
exact authorization.

## 14. Execution Record

Every execution attempt SHALL preserve:

- execution_id;
- authorization_binding_id;
- human_gate_decision_id;
- transition_class;
- transition_target;
- object_id;
- room_revision_id;
- room_state_root;
- authorized_view_root;
- evidence_boundary_reference;
- evidence_ceiling_reference;
- approved_scope;
- requested_execution_scope;
- condition_satisfaction_references;
- execution_attempt;
- execution_state;
- execution_effect_reference where applicable;
- execution_time_reference;
- provenance_route;
- authority_state;
- human_gate_state.

Execution record != approval record.

## 15. Execution Identity

execution_id SHALL be deterministic over the material execution binding and
attempt identity.

A materially different execution requires a different execution identity.

Execution identity does not grant authority.

Hash != authority.

## 16. Single-Execution Law

An authorization binding SHALL declare execution cardinality.

Native AC-06 cardinalities are:

- SINGLE
- BOUNDED_REPEAT

SINGLE authorizes at most one successful authority-bearing execution.

A second successful execution under a consumed SINGLE authorization is
prohibited.

Retry after non-effectful failure MUST remain explicitly attributable and MUST
NOT be represented as another authorization.

BOUNDED_REPEAT requires an explicit maximum execution count greater than zero.

No unlimited implicit execution cardinality exists.

## 17. Consumption

Successful execution consumes one permitted execution from the authorization
binding.

Consumption state SHALL be machine-visible.

Consumption states are:

- UNUSED
- PARTIALLY_CONSUMED
- CONSUMED
- INVALIDATED

CONSUMED authorization cannot execute again.

INVALIDATED authorization cannot execute.

Consumption != revocation.

Invalidation != denial.

## 18. Invalidation

Authorization becomes invalid for execution when a material bound state no
longer matches, including:

- decision invalidated;
- transition class changed;
- target changed;
- Room changed;
- revision changed;
- state root changed;
- Authorized View changed;
- evidence boundary changed;
- evidence ceiling changed;
- approved scope no longer matches;
- required condition state changed;
- authorization explicitly revoked or invalidated.

Invalidated approval remains historical evidence.

Invalidated approval is not executable authority.

## 19. Approved-State / Executed-State Equality

Before execution, the execution capability SHALL compare approved state against
requested execution state.

The following MUST match the authorization binding:

- Human Gate decision;
- transition class;
- target;
- Room;
- revision;
- state root;
- Authorized View Root;
- evidence boundary;
- evidence ceiling;
- scope constraints;
- condition state;
- execution cardinality.

Mismatch blocks execution.

Approved state != executed state is a hard failure.

## 20. Movement Fidelity

Actual authority-bearing movement MUST remain within the approved movement.

Execution MUST NOT:

- affect an unapproved target;
- perform an unapproved transition class;
- exceed approved scope;
- perform additional authority-bearing side effects;
- broaden evidence access;
- mutate another Room;
- reuse authorization for another operation;
- exceed execution cardinality.

Execution effect must remain attributable to the authorization that permitted
it.

## 21. No Silent Carry-Forward

Authorization MUST NOT silently carry forward across:

- another transition;
- another target;
- another Room;
- another revision;
- another state root;
- another Authorized View;
- another evidence boundary;
- another evidence ceiling;
- another scope;
- another materially changed condition set;
- another execution after cardinality exhaustion.

Prior approval != standing approval.

## 22. Execution Eligibility

Execution eligibility requires all of:

1. Human Gate decision = APPROVED;
2. exact class match;
3. exact target match;
4. exact Room match;
5. exact revision match;
6. exact state match;
7. exact Authorized View match;
8. evidence boundary match;
9. evidence ceiling match;
10. requested scope within exact authorized scope;
11. MC state permits the movement;
12. all CONDITIONAL requirements are satisfied;
13. authorization is not stale;
14. authorization is not invalidated;
15. execution cardinality remains available;
16. requested movement equals the authorized movement;
17. provenance is intact.

Failure of any required condition blocks execution.

Fail closed.

## 23. Primary AR Closure Targets

AC-06 directly governs:

AR-009:
MC admissibility MUST NOT become execution readiness.

AR-054:
Stale Human Gate approval MUST NOT execute.

AR-055:
Approved state MUST match executed state.

AR-011:
Approval target substitution MUST fail.

AR-012:
Approval scope expansion MUST fail.

AR-010:
Approval MUST NOT be reused for another transition.

AR-059:
Authority-bearing action disguised as preparation MUST be treated as execution.

AR-056:
Invalidated approval MUST NOT execute.

AR-057:
Execution MUST NOT exceed authorized cardinality.

AR-058:
Execution MUST NOT exceed or differ from approved movement.

AR-051:
CONDITIONAL MUST NOT become effectively authorized without attributable
condition satisfaction.

## 24. Fail-Closed Conditions

AC-06 SHALL block execution for:

- missing Human Gate approval;
- stale approval;
- invalidated approval;
- consumed authorization;
- class mismatch;
- target mismatch;
- Room mismatch;
- revision mismatch;
- state mismatch;
- Authorized View mismatch;
- evidence-boundary mismatch;
- evidence-ceiling mismatch;
- scope expansion;
- transition substitution;
- approval reuse;
- unsatisfied conditional state;
- MC inadmissibility;
- execution cardinality exhaustion;
- requested movement differing from approved movement;
- authority-bearing side effect disguised as preparation;
- missing provenance.

No default approval.

No inferred authorization.

No best-effort authority.

## 25. Authority Boundary

Zervan Authority remains NONE.

Human Gate remains ACTIVE.

The capability validates and consumes externally attributable human
authorization.

It does not become the authority that issued that authorization.

Human authorization != autonomous system authority.

Execution capability != approval capability.

Technical ability != authority.

## 26. AC-06 Lock

Human Gate is a mechanically enforced authority boundary.

Human Gate is not a status field.

Decision × Class × Target × Room × Revision × State × View × Evidence × Scope
× Execution SHALL remain exactly bound.

Approval != execution.

Admissibility != authorization.

ADMISSIBLE != execution-ready.

CONDITIONAL != authorized.

CONDITIONAL + approval != executable without condition satisfaction.

Prior approval != standing approval.

Stale approval != executable approval.

Invalidated approval != executable approval.

Consumed approval != reusable approval.

Preparation != execution.

Naming execution preparation does not change its authority-bearing effect.

Approved state MUST equal executed state.

Actual movement MUST remain within approved movement.

Authority remains NONE.

Human Gate remains ACTIVE.
