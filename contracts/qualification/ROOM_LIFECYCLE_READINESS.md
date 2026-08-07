# R3-C — Room Lifecycle / Readiness

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R3-C
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R3-C defines native-v41 Room lifecycle transition and readiness behavior.

R3-C consumes:

- complete Rings 1 and 2;
- R3-A Qualification Request;
- R3-B Qualification Record and disposition.

R3-C establishes when a qualified Room becomes READY for later formation
selection and analytical occupation.

R3-C does not yet define:

- analytical Occupation;
- Occupancy Witness;
- capability mission execution;
- formation selection;
- landing;
- reflight;
- closing;
- replay;
- supersession execution.

---

## 1. Lifecycle Principle

Qualification precedes analysis.

Lifecycle state records operational condition.

Lifecycle state does not own truth.

Lifecycle transition MUST be attributable.

A later lifecycle state MUST NOT silently rewrite prior state.

History accumulates.

---

## 2. Source Lifecycle Behavior

Native v41 preserves the following lifecycle meanings:

- `DETECTED` — a terrain signal exists, but object identity and boundary are not
  yet sufficient.
- `PROVISIONAL` — a candidate Room Object and initial coordinates have been
  assigned for bounded qualification.
- `QUALIFYING` — permitted capabilities are establishing identity, geometry,
  boundary, provenance, and mission fitness.
- `QUALIFIED` — the Room is sufficiently established for the declared mission
  and evidence ceiling.
- `READY` — the qualified Room is available for formation selection and
  analytical occupation.
- `ACTIVE` — one or more capabilities are operating within declared Zones and
  Spaces.
- `LANDED` — movement has ceased while occupation, coordinates, unresolved
  terrain, and readiness remain preserved.
- `DEGRADED` — the Room remains identifiable but current evidence, integrity,
  or access cannot support prior operations.
- `SEALED` — the current operational interval is closed with closing witness,
  preserved lineage, and replay coordinates.
- `REOPENED` — a sealed Room is reopened at a preserved state because a valid
  reflight trigger exists.
- `REJECTED` — qualification failed or the candidate was determined not to
  represent a legitimate analytical object.
- `SUPERSEDED` — object identity remains historically resolvable but a later
  authorized state or corrected object definition controls future operation.

R3-C recognizes all source lifecycle states.

R3-C implements only the qualification-to-readiness transition surface.

---

## 3. Lifecycle Transition Record

Every lifecycle transition MUST declare:

- `lifecycle_transition_id`;
- canonical `object_id`;
- source state;
- target state;
- Qualification Request reference when applicable;
- Qualification Record reference when applicable;
- qualification disposition when applicable;
- declared mission;
- evidence ceiling;
- readiness requirements;
- unresolved readiness blockers;
- transition basis;
- Registry reference;
- Audit reference;
- authorization reference;
- Human Gate reference when applicable;
- provenance route;
- transition time.

---

## 4. Transition Identity

Native-v41 `lifecycle_transition_id` is deterministic SHA-512 over the complete
declared lifecycle transition except `lifecycle_transition_id`.

A material transition change produces another transition identity.

Lifecycle transition identity is not Room Object identity.

Lifecycle transition identity is not Qualification Record identity.

---

## 5. Registry Ownership

Registry defines and resolves Room lifecycle state.

R3-C records a Registry-attributable transition.

Registry state ownership does not create truth authority.

Registry != truth owner.

---

## 6. Audit Boundary

Audit verifies transition integrity.

A lifecycle transition MUST preserve an Audit reference when required by the
native transition path.

Audit verification != transition ownership.

Audit != Registry.

---

## 7. Qualification-to-Lifecycle Binding

The Qualification Record disposition constrains qualification-stage lifecycle
transition.

The record does not itself mutate lifecycle state.

Disposition != lifecycle mutation.

A lifecycle transition MUST preserve the Qualification Record reference that
supports it.

---

## 8. Native Qualification Transition Surface

R3-C permits the following qualification-stage transitions:

- `DETECTED -> PROVISIONAL`
- `PROVISIONAL -> QUALIFYING`
- `QUALIFYING -> QUALIFIED`
- `QUALIFYING -> PROVISIONAL`
- `QUALIFYING -> REJECTED`
- `QUALIFYING -> DEGRADED`
- `QUALIFIED -> READY`

These transitions define only the current Ring 3 lifecycle surface.

No other transition is silently inferred.

---

## 9. DETECTED

`DETECTED` means a terrain signal exists but object identity and boundary remain
insufficient.

DETECTED != PROVISIONAL.

Signal existence != qualified Room.

---

## 10. PROVISIONAL

`PROVISIONAL` means a candidate Room Object and initial coordinates exist for
bounded qualification.

PROVISIONAL may arise before active qualification or as a bounded outcome of
qualification that still requires more evidence.

PROVISIONAL != QUALIFIED.

PROVISIONAL != READY.

---

## 11. QUALIFYING

`QUALIFYING` means permitted capabilities are establishing:

- identity;
- geometry;
- boundary;
- provenance;
- mission fitness.

QUALIFYING != QUALIFIED.

Work in progress != qualification success.

---

## 12. QUALIFIED

`QUALIFIED` means the Room is sufficiently established for the declared mission
and evidence ceiling.

A transition from `QUALIFYING` to `QUALIFIED` requires a Qualification Record
with disposition:

`QUALIFIED`

No other R3-B disposition can establish lifecycle `QUALIFIED`.

QUALIFIED != READY.

QUALIFIED != ACTIVE.

---

## 13. PROVISIONAL Disposition Mapping

A Qualification Record disposition of `PROVISIONAL` may support:

`QUALIFYING -> PROVISIONAL`

It MUST NOT support:

- `QUALIFYING -> QUALIFIED`;
- `QUALIFIED -> READY`.

PROVISIONAL disposition != qualification success.

---

## 14. REJECTED Disposition Mapping

A Qualification Record disposition of `REJECTED` supports:

`QUALIFYING -> REJECTED`

REJECTED MUST remain historically resolvable.

Rejected != erased.

REJECTED does not silently transition to READY.

---

## 15. DEGRADED Disposition Mapping

A Qualification Record disposition of `DEGRADED` supports:

`QUALIFYING -> DEGRADED`

DEGRADED preserves Room identifiability while recording that evidence,
integrity, access, or current conditions cannot support the intended operation.

DEGRADED != nonexistent.

DEGRADED != READY.

---

## 16. READY

`READY` means a qualified Room is available for:

- formation selection;
- analytical occupation.

READY does not mean either has occurred.

READY != ACTIVE.

READY != occupied.

Availability != presence.

---

## 17. READY Preconditions

Native v41 requires `QUALIFIED -> READY` to preserve:

- canonical object identity;
- Qualification Record reference;
- Qualification disposition `QUALIFIED`;
- declared mission;
- evidence ceiling;
- explicit readiness requirements;
- zero unresolved readiness blockers;
- Registry transition attribution;
- Audit transition-integrity reference;
- provenance route.

READY MUST NOT be inferred merely because a Qualification Record exists.

QUALIFIED is necessary for READY.

QUALIFIED alone is not sufficient for READY.

---

## 18. Readiness Requirements

`readiness_requirements` declare what must remain satisfied for the Room to be
made available for formation selection and analytical occupation.

R3-C does not prescribe one universal mission-independent readiness checklist.

Readiness remains mission-bounded.

No defaults unless undefined.

Never stay at the default unless asked.

---

## 19. Readiness Blockers

Any unresolved readiness blocker prevents transition to READY.

Blockers may include unresolved:

- qualification integrity;
- provenance;
- evidence-boundary conflict;
- evidence-ceiling conflict;
- representation inconsistency;
- transition-integrity failure;
- applicable authorization condition.

A blocker MUST remain explicit.

Blocked != absent.

---

## 20. Authorization

Lifecycle transition capability does not create authorization.

Applicable authorization remains governed by Ring 1.

Write capability != authority.

Authorization reference != authorization invention.

---

## 21. Human Gate

Where Human Gate applies, the transition preserves its reference.

Human Gate approval MUST NOT be fabricated.

Approval != execution.

READY does not itself authorize external execution.

---

## 22. ACTIVE Boundary

`ACTIVE` is recognized as a source lifecycle state.

R3-C does not transition a Room to ACTIVE.

ACTIVE requires analytical occupation, which is downstream.

READY != ACTIVE.

No ACTIVE transition yet.

---

## 23. LANDED Boundary

`LANDED` is recognized as a source lifecycle state.

R3-C does not define landing behavior.

Landing remains downstream.

No LANDED transition yet.

---

## 24. SEALED / REOPENED Boundary

`SEALED` and `REOPENED` are recognized source lifecycle states.

R3-C does not define closing, replay, or reflight mechanics.

No SEALED transition yet.

No REOPENED transition yet.

---

## 25. SUPERSEDED Boundary

`SUPERSEDED` is recognized as a source lifecycle state.

R3-C does not define supersession execution.

Object identity remains historically resolvable.

No SUPERSEDED transition yet.

---

## 26. Formation Boundary

READY makes the qualified Room available for formation selection.

R3-C does not select a formation.

READY != formation selected.

Lifecycle transition != formation selection.

---

## 27. Occupation Boundary

READY makes the qualified Room available for analytical occupation.

R3-C does not establish occupation.

READY != occupied.

Lifecycle transition != Occupancy Witness.

---

## 28. Publication Boundary

Lifecycle READY does not authorize publication.

Room qualification and occupation remain upstream and underneath the existing
publication sequence.

READY != publication authority.

---

## 29. R3-C Lock

Qualification precedes analysis.

Lifecycle state does not own truth.

Lifecycle transition MUST be attributable.

History accumulates.

Registry defines and resolves Room lifecycle state.

Audit verifies transition integrity.

Disposition != lifecycle mutation.

DETECTED != PROVISIONAL.

Signal existence != qualified Room.

PROVISIONAL != QUALIFIED.

PROVISIONAL != READY.

QUALIFYING != QUALIFIED.

Work in progress != qualification success.

Only QUALIFIED disposition may support lifecycle QUALIFIED.

QUALIFIED != READY.

QUALIFIED != ACTIVE.

PROVISIONAL disposition != qualification success.

Rejected != erased.

DEGRADED != nonexistent.

DEGRADED != READY.

READY means available for formation selection and analytical occupation.

READY != ACTIVE.

READY != occupied.

Availability != presence.

QUALIFIED is necessary for READY.

QUALIFIED alone is not sufficient for READY.

Blocked != absent.

Write capability != authority.

Approval != execution.

READY != formation selected.

Lifecycle transition != formation selection.

Lifecycle transition != Occupancy Witness.

READY != publication authority.

No ACTIVE transition yet.

No LANDED transition yet.

No SEALED transition yet.

No REOPENED transition yet.

No SUPERSEDED transition yet.
