# R3-A — Qualification Request / Mission Fitness

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R3-A
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R3-A defines the Qualification Request boundary for a provisional Canonical
Room Object.

A Qualification Request declares what must be established before the Room may
be considered sufficiently defined, bounded, attributable, and navigable for a
proposed mission.

R3-A consumes complete Rings 1 and 2.

R3-A does not redefine:

- Room identity;
- Origin or Ingress;
- Zone;
- Space;
- Territory;
- Orientation;
- Cartography;
- Stick;
- Passageway.

R3-A does not produce the Qualification disposition.

---

## 1. Qualification Principle

Qualification precedes analysis.

Qualification is the controlled act of establishing whether a Room is
sufficiently defined, bounded, attributable, and navigable for the proposed
mission.

Qualification does not prove every fact inside the Room.

Qualification does not authorize publication.

Qualification does not authorize execution.

---

## 2. Request Boundary

A Qualification Request declares:

- the provisional Room Object to be qualified;
- the proposed qualification mission;
- the active question;
- the representation in which qualification is permitted;
- the evidence boundary and ceiling;
- the governing entry constraints;
- the evidence obligations;
- prohibited assumptions;
- Human Gate conditions;
- qualification requirements that must be tested.

The request describes the problem.

It does not claim the answer.

---

## 3. Qualification Request Record

Every Qualification Request MUST declare:

- `qualification_request_id`;
- `object_id`;
- `provisional_room_reference`;
- `origin_reference`;
- `ingress_reference`;
- `zone_id`;
- `space_id`;
- `orientation_reference`;
- `territory_reference`;
- `qualification_mission`;
- `active_question`;
- `entry_constraints`;
- `evidence_obligations`;
- `included_evidence`;
- `excluded_evidence`;
- `evidence_boundary`;
- `evidence_ceiling`;
- `prohibited_assumptions`;
- `human_gate_conditions`;
- `qualification_requirements`;
- `request_state`;
- `provenance_route`;
- `requested_at`.

---

## 4. Qualification Request Identity

Native-v41 `qualification_request_id` is deterministic SHA-512 over the complete
declared Qualification Request except `qualification_request_id`.

Identical canonical request declarations produce the same request identity.

A material change to the requested qualification problem produces another
request identity.

Qualification Request identity is not Room Object identity.

---

## 5. Provisional Object

Qualification operates against a provisional or otherwise qualification-eligible
Room Object.

The request MUST preserve canonical `object_id`.

The request MAY carry a provisional Room reference used by qualification
workflow.

A provisional workflow reference MUST NOT substitute for canonical object
identity.

Provisional reference != object identity.

---

## 6. Origin and Ingress

Qualification MUST remain resolvably attached to Origin and Ingress.

Qualification does not create a new origin.

Qualification does not broaden the ingress admission boundary.

Missing evidence MUST NOT be invented during qualification.

---

## 7. Representation Boundary

The request identifies the Zone, Space, Orientation, and Territory against
which qualification is proposed.

These references establish the bounded representation to test.

Qualification work MUST NOT silently escape the permitted representation.

Qualification request != representation mutation.

---

## 8. Qualification Mission

The `qualification_mission` states what the qualification activity is intended
to establish.

The mission MUST be bounded.

The mission does not itself establish fitness.

Mission declared != mission fit.

---

## 9. Active Question

The active question identifies the inquiry that justifies qualification.

Qualification MUST remain attributable to that question.

A change in question that materially changes the qualification problem requires
a changed Qualification Request.

Question != authority.

---

## 10. Entry Constraints

Governance supplies qualification entry constraints.

Entry constraints define the conditions under which qualification activity may
enter or inspect the permitted representation.

Entry constraint != occupation.

Entry constraint != execution authority.

---

## 11. Evidence Obligations

Governance supplies evidence obligations.

The request records what evidence categories, provenance, integrity, boundary,
or accessibility conditions must be evaluated to determine mission fitness.

Evidence obligation != evidence satisfaction.

Required evidence != available evidence.

---

## 12. Evidence Boundary

The request declares the evidence boundary applicable to qualification.

Qualification MUST NOT silently reason outside that boundary.

Evidence outside the permitted boundary remains outside the permitted boundary
unless a governed change occurs.

---

## 13. Evidence Ceiling

The request declares the maximum claim/evidence ceiling available to the
qualification mission.

Qualification cannot silently raise that ceiling.

Qualification result may narrow supported operation.

It cannot manufacture stronger evidence authority.

---

## 14. Included and Excluded Evidence

Included evidence is evidence permitted for the qualification mission.

Excluded evidence remains existentially represented where known.

Excluded != absent.

Restriction != absence.

Qualification MUST NOT silently convert excluded evidence into usable evidence.

---

## 15. Prohibited Assumptions

The request preserves prohibited assumptions supplied by governing constraints.

Qualification MUST NOT use a prohibited assumption to fill:

- missing evidence;
- unresolved geometry;
- unknown provenance;
- inaccessible surfaces;
- object distinctness;
- mission fitness.

Assumption != evidence.

---

## 16. Human Gate Conditions

The request records applicable Human Gate conditions.

Human Gate conditions do not imply approval.

Approval MUST NOT be invented.

Approval != execution.

---

## 17. Qualification Requirements

`qualification_requirements` identifies the dimensions that qualification must
test.

Native v41 requires the request to account for, where applicable:

- object identity;
- boundary;
- provenance;
- geometry;
- mission fitness;
- uncertainty;
- restrictions;
- reachable surfaces;
- fractures;
- adjoining relationships;
- discriminating evidence needs.

A requirement may remain unresolved.

Unresolved != passed.

---

## 18. Mission Fitness

Mission fitness is the question:

Is this Room sufficiently established for the declared mission and evidence
ceiling?

R3-A records the mission-fitness requirements.

R3-A does not answer them.

Mission fitness is determined downstream by Qualification evidence and
disposition.

Requested != fit.

---

## 19. Information Dominance Boundary

Qualification seeks enough knowledge about:

- object identity;
- boundary;
- geometry;
- provenance;
- uncertainty;
- restrictions;
- reachable surfaces

to choose the next justified operation without pretending completeness.

Information dominance does not mean omniscience.

Sufficient != complete.

---

## 20. Request State

R3-A defines three request states:

- `DRAFT`;
- `READY`;
- `BLOCKED`.

DRAFT means the request is being assembled and is not yet suitable for
qualification routing.

READY means the required request inputs are sufficiently declared for
qualification routing.

BLOCKED means qualification routing cannot proceed under the current request.

Request READY != Room READY.

Request READY != QUALIFIED.

---

## 21. READY Request Requirements

A Qualification Request may be `READY` only when it declares:

- canonical object identity;
- Origin;
- Ingress;
- permitted representation references;
- qualification mission;
- active question;
- evidence boundary;
- evidence ceiling;
- entry constraints;
- evidence obligations;
- prohibited assumptions;
- Human Gate conditions;
- qualification requirements;
- provenance route.

READY means the qualification question is routable.

READY does not mean the Room passed qualification.

---

## 22. BLOCKED Request

A Qualification Request becomes or remains BLOCKED when required request inputs
cannot be resolved sufficiently for qualification routing.

BLOCKED MUST preserve the unresolved condition.

BLOCKED MUST NOT be converted to READY through invented defaults.

No defaults unless undefined.

Never stay at the default unless asked.

---

## 23. Capability Boundary

R3-A does not select qualification capability.

TOC later coordinates the smallest justified qualification capability.

Request != formation selection.

Request != capability assignment.

Need determines force downstream.

---

## 24. Occupation Boundary

R3-A does not establish occupation.

A later qualification capability may occupy only the permitted provisional
representation.

Qualification Request READY != occupied.

Entry permission != presence.

---

## 25. Qualification Record Boundary

R3-A does not produce:

- qualification observations;
- Cartographic changes;
- uncertainty findings;
- restricted-surface findings;
- adjoining-object findings;
- distinct-object result;
- recommended formation;
- qualification disposition;
- replay route.

Those belong to downstream qualification execution and the Qualification
Record.

Request != Record.

---

## 26. Publication / Execution Boundary

Qualification Request creation does not authorize:

- publication;
- canonical mutation;
- analytical promotion;
- execution;
- external action.

Authority remains governed by Ring 1.

Write capability != authority.

---

## 27. R3-A Lock

Qualification precedes analysis.

The Qualification Request declares what must be qualified.

The Qualification Request does not claim qualification success.

Qualification does not prove every fact inside the Room.

Qualification does not authorize publication.

Qualification does not authorize execution.

Mission declared != mission fit.

Requested != fit.

Requested != QUALIFIED.

Request READY != Room READY.

Request READY != QUALIFIED.

Provisional reference != object identity.

Excluded != absent.

Restriction != absence.

Assumption != evidence.

Unresolved != passed.

Sufficient != complete.

Approval != execution.

Entry permission != presence.

Request != formation selection.

Request != capability assignment.

Request != Record.

Write capability != authority.

No qualification disposition yet.

No analytical occupation yet.
