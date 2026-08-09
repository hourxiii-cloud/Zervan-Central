# AC-05 — Explicit Semantic-State Geometry

Status: CONTROLLED ACTIVATION PATCH
Version: vTemporal.41.0
Activation Branch: ac/v41-activation
Authority: NONE
Human Gate: ACTIVE

## 0. Purpose

AC-05 defines the multidimensional semantic-state algebra used to preserve
analytical geometry across existence, epistemic state, accessibility, topology,
hydration, operation, decision, and representation.

Semantic state is not one flat status.

Semantic state is not one serial enum.

Semantic state is a governed coordinate across independently meaningful
analytical dimensions.

Flattening those dimensions destroys analytical geometry.

## 1. Governing Law

An analytical object occupies a semantic-state coordinate.

The coordinate preserves independently meaningful dimensions.

A change in one dimension MUST NOT silently mutate another dimension.

Projection MUST NOT mutate existence.

Restriction MUST NOT imply absence.

Unknown MUST NOT imply absence.

Denial MUST NOT imply absence.

Blocked operation MUST NOT imply denial.

Partial hydration MUST NOT imply completeness.

Hidden topology MUST NOT imply nonexistent topology.

Rendering MUST NOT rewrite analytical state.

No Compression Out applies across semantic dimensions.

## 2. Required Dimensions

Native AC-05 semantic-state coordinates preserve:

1. existence;
2. epistemic state;
3. accessibility;
4. topology;
5. hydration;
6. operational state;
7. decision state;
8. representation state.

These dimensions are analytically distinct.

They MAY interact through governed transition rules.

They MUST NOT collapse into one serial state axis.

## 3. Existence Dimension

Existence states are:

- KNOWN_PRESENT
- KNOWN_ABSENT
- UNRESOLVED_EXISTENCE

KNOWN_PRESENT means existence is established within the governed evidence
boundary.

KNOWN_ABSENT means absence is affirmatively established within the governed
evidence boundary.

UNRESOLVED_EXISTENCE means available evidence does not establish presence or
absence.

UNKNOWN is not automatically KNOWN_ABSENT.

Restricted is not KNOWN_ABSENT.

Unavailable is not KNOWN_ABSENT.

Denied is not KNOWN_ABSENT.

Blocked is not KNOWN_ABSENT.

Omitted from a representation is not KNOWN_ABSENT.

## 4. Epistemic Dimension

Epistemic states are:

- KNOWN
- UNKNOWN
- UNRESOLVED
- CONTRADICTED

KNOWN means the represented proposition is supported at the declared evidence
boundary and ceiling.

UNKNOWN means the proposition is not established from available evidence.

UNRESOLVED means evidence exists but does not yet permit a defensible
resolution.

CONTRADICTED means attributable evidence supports incompatible states that have
not been defensibly resolved.

UNKNOWN != ABSENT.

UNRESOLVED != ABSENT.

CONTRADICTED != UNKNOWN.

Contradiction MUST NOT be normalized into certainty.

## 5. Accessibility Dimension

Accessibility states are:

- AVAILABLE
- RESTRICTED
- UNAVAILABLE

AVAILABLE means the governed payload or relationship surface is accessible to
the current operation or Authorized View.

RESTRICTED means existence may be known while access is intentionally limited.

UNAVAILABLE means the referenced material is known or expected but cannot
currently be accessed.

RESTRICTED != ABSENT.

UNAVAILABLE != ABSENT.

Accessibility does not own existence.

Accessibility does not own topology.

## 6. Topology Dimension

Topology states are:

- TOPOLOGY_KNOWN
- TOPOLOGY_RESTRICTED
- TOPOLOGY_UNRESOLVED
- TOPOLOGY_ABSENT

TOPOLOGY_KNOWN means an attributable relationship is established and visible.

TOPOLOGY_RESTRICTED means relationship existence is established but some or all
relationship detail is restricted.

TOPOLOGY_UNRESOLVED means relationship state cannot yet be established
defensibly.

TOPOLOGY_ABSENT means absence of the relationship is affirmatively established
within the governed boundary.

A restricted relationship MUST NOT disappear.

A hidden relationship MUST NOT become nonexistent.

Restricted topology MUST preserve an existence-aware marker and attributable
return route.

Projection may hide relationship payload.

Projection may not erase known relationship existence.

## 7. Hydration Dimension

Hydration states are:

- UNHYDRATED
- PARTIAL
- COMPLETE

Hydration state is always relative to a declared hydration boundary.

PARTIAL means only a proper subset of the declared required territory is
hydrated.

COMPLETE means all material required territory inside the declared hydration
boundary is resolved sufficiently for the declared operation.

PARTIAL != COMPLETE.

Payload availability outside the declared hydration boundary does not
automatically change hydration state.

A PARTIAL state MUST preserve:

- hydrated surface;
- unresolved surface;
- restricted surface;
- unavailable surface;
- hydration boundary;
- evidence ceiling;
- provenance.

Partial hydration MUST NOT render as complete.

## 8. Operational Dimension

Operational states include:

- PERMITTED
- BLOCKED
- INACTIVE
- ACTIVE
- COMPLETED
- FAILED

BLOCKED means the operation cannot defensibly proceed under current constraints.

BLOCKED does not mean the object is absent.

BLOCKED does not mean Human Gate denied the operation.

BLOCKED does not erase evidence.

Operational state does not own existence.

Operational state does not own decision state.

## 9. Decision Dimension

Decision states are:

- NOT_REQUIRED
- PENDING
- APPROVED
- DENIED

DENIED means an attributable governing decision rejected the explicitly bounded
transition or request.

DENIED != BLOCKED.

DENIED != ABSENT.

DENIED != FALSE.

PENDING != APPROVED.

No decision state may be inferred from silence.

## 10. Representation Dimension

Representation states include:

- FULL
- REDACTED
- EXISTENCE_ONLY
- SUMMARY
- OMITTED_BY_VIEW

Representation controls what is exposed.

Representation does not own underlying analytical state.

OMITTED_BY_VIEW does not mean absent.

REDACTED does not mean unknown.

EXISTENCE_ONLY preserves established existence while withholding governed
payload.

SUMMARY MUST preserve material semantic-state distinctions.

Rendering MUST NOT convert:

- UNKNOWN -> KNOWN;
- UNRESOLVED -> KNOWN;
- RESTRICTED -> ABSENT;
- UNAVAILABLE -> ABSENT;
- TOPOLOGY_RESTRICTED -> TOPOLOGY_ABSENT;
- PARTIAL -> COMPLETE;
- BLOCKED -> DENIED;
- PENDING -> APPROVED.

Representation transform != semantic-state mutation.

## 11. Semantic-State Coordinate

Every semantic-state coordinate MUST preserve:

- semantic_state_id;
- subject_reference;
- existence_state;
- epistemic_state;
- accessibility_state;
- topology_state;
- hydration_state;
- hydration_boundary_reference;
- operational_state;
- decision_state;
- representation_state;
- evidence_boundary_reference;
- evidence_ceiling_reference;
- restriction_references;
- unresolved_references;
- provenance_route;
- authority_state;
- human_gate_state.

The coordinate is one analytical position across multiple dimensions.

Coordinate identity is not subject identity.

Coordinate identity is not truth authority.

## 12. Coordinate Identity

semantic_state_id SHALL be deterministic SHA-512 over the complete material
semantic-state coordinate except its own ID.

Equivalent material coordinates produce equivalent identity.

A material change in any semantic dimension changes coordinate identity.

Changing representation alone changes the semantic-state coordinate when the
representation binding is material, but it MUST NOT silently change the
underlying existence, epistemic, accessibility, topology, hydration,
operational, or decision coordinates.

Hash != truth.

## 13. Transition Algebra

A semantic transition is movement from one attributable coordinate to another.

Every transition MUST identify:

- prior semantic_state_id;
- resulting semantic_state_id;
- dimensions requested to change;
- dimensions actually changed;
- evidence references supporting epistemic movement;
- authorization references supporting access or decision movement;
- hydration evidence supporting hydration movement;
- provenance;
- transition reason.

Unchanged dimensions MUST remain invariant.

A transition in one dimension MUST NOT silently drag another dimension with it.

## 14. Illegal Cross-Dimension Collapse

AC-05 MUST reject:

- UNKNOWN -> KNOWN_ABSENT without attributable absence evidence;
- UNRESOLVED_EXISTENCE -> KNOWN_ABSENT without attributable absence evidence;
- RESTRICTED -> KNOWN_ABSENT;
- UNAVAILABLE -> KNOWN_ABSENT;
- DENIED -> KNOWN_ABSENT;
- BLOCKED -> KNOWN_ABSENT;
- OMITTED_BY_VIEW -> KNOWN_ABSENT;
- TOPOLOGY_RESTRICTED -> TOPOLOGY_ABSENT because of projection;
- PARTIAL -> COMPLETE without hydration evidence;
- BLOCKED -> DENIED without an attributable decision;
- PENDING -> APPROVED without an attributable Human Gate decision;
- UNKNOWN -> KNOWN because a renderer omitted uncertainty;
- CONTRADICTED -> KNOWN without attributable resolution.

These are geometric collapses.

They are not presentation changes.

## 15. Authorized View Boundary

Authorized Views consume semantic-state coordinates.

An Authorized View may change representation and accessibility according to its
authorization.

It MUST preserve known existence.

It MUST preserve existence-aware restricted topology.

It MUST preserve material unknown, unresolved, contradicted, restricted,
unavailable, partial, blocked, pending, and denied states where omission would
change analytical meaning.

Different visibility does not create different reality.

## 16. Hydration Boundary

Hydration consumes and produces semantic-state coordinates.

Hydration may change hydration state and accessibility where justified.

Hydration MUST NOT silently mutate:

- existence;
- topology;
- epistemic certainty;
- decision state;
- authority.

Hydration may reveal evidence that supports a separately attributable semantic
transition.

Hydration itself does not manufacture truth.

## 17. Raven / Reporting Boundary

Raven and report rendering consume semantic-state coordinates.

Rendering may change representation.

Rendering MUST NOT improve the underlying semantic coordinate.

Material unknowns remain visible.

Material uncertainty remains visible.

Restricted existence remains existence-aware.

Restricted topology remains topology-aware.

Partial hydration remains partial.

Blocked remains blocked.

Denied remains denied.

Report cleanliness is not permission to flatten analytical geometry.

## 18. Replay Boundary

Replay preserves the historical semantic-state coordinate.

Current knowledge MUST NOT rewrite historical UNKNOWN.

Current access MUST NOT rewrite historical RESTRICTED.

Current topology MUST NOT rewrite historical TOPOLOGY_UNRESOLVED.

Current hydration MUST NOT rewrite historical PARTIAL.

Current approval MUST NOT rewrite historical PENDING or DENIED.

Historical semantic geometry remains historical semantic geometry.

Replay != retrospective semantic promotion.

## 19. Fail Closed

If a semantic-state dimension cannot be resolved, preserve the appropriate
unknown, unresolved, restricted, unavailable, partial, blocked, or pending
state.

Do not guess.

Do not substitute defaults.

Do not flatten dimensions to obtain a cleaner state.

Do not erase topology because payload is restricted.

Do not represent partial hydration as complete.

Do not suppress material uncertainty during rendering.

Surface the unresolved geometry.

## 20. Authority Boundary

Authority remains NONE.

Human Gate remains ACTIVE.

External Runtime remains DISABLED.

External Action remains DISABLED.

System Population remains DISALLOWED.

Semantic-state evaluation creates no authority.

Semantic-state transition creates no authority unless a separately governed
authority-bearing transition is explicitly authorized.

Human Gate approval does not manufacture evidence.

## 21. AC-05 Lock

Semantic state is multidimensional analytical geometry.

Semantic state is not one flat enum.

Semantic state is not one serial status line.

Existence != epistemic state.

Existence != accessibility.

Existence != topology.

Existence != hydration.

Existence != operational state.

Existence != decision state.

Existence != representation.

UNKNOWN != ABSENT.

RESTRICTED != ABSENT.

UNAVAILABLE != ABSENT.

DENIED != BLOCKED.

PARTIAL != COMPLETE.

Restricted topology remains existent.

Projection does not mutate reality.

Rendering does not improve analytical state.

Replay does not retrospectively promote semantic state.

A change in one dimension MUST NOT silently mutate another dimension.

No Compression Out applies across semantic dimensions.

Authority remains NONE.

Human Gate remains ACTIVE.
