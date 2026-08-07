# R3-I — Hydration Request / Release

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R3-I
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R3-I defines native-v41 Hydration Request and Hydration Release behavior.

Hydration is not merely loading files.

Hydration restores only verified operational territory required by the active
mission and representation.

Payload remains at rest except where mission-scoped access is justified.

Unnecessary active payload is released while Room identity and state remain
preserved.

---

## 1. Inputs

R3-I consumes:

- complete Rings 1 and 2;
- R3-A through R3-H;
- canonical Room Object identity;
- active question;
- Capability Mission Request;
- current occupied Zone and Space;
- current representation coordinates;
- current Territory;
- evidence boundary;
- evidence ceiling;
- restrictions;
- provenance;
- Stick continuity.

Hydration does not redefine those inputs.

---

## 2. Hydration Principle

Identity travels.

Payload rests.

Hydration restores verified operational territory only when current mission
need justifies access.

Hydrate what the question requires.

Leave unnecessary payload at rest.

---

## 3. Verified Territory Only

Hydration MUST operate only on territory already verified for operational use
under the applicable Room, representation, mission, and evidence constraints.

Hydration does not convert unverified material into verified territory.

Hydration does not qualify the Room.

Hydration does not create reachability.

Hydration does not manufacture evidence.

---

## 4. Mission Requirement

Every hydration request MUST resolve to an active mission and active question.

The request MUST explain why the requested territory or payload is needed for
that mission.

Mission-required != potentially interesting.

Available != necessary.

Possible relevance != hydration justification.

---

## 5. Representation Binding

Hydration is representation-bound.

Every request preserves:

- Room Object;
- Zone;
- Space;
- Orientation;
- Territory;
- evidence boundary;
- evidence ceiling.

Hydration does not broaden representation scope.

Hydration does not create another Room.

---

## 6. Hydration Request

Every Hydration Request MUST preserve:

- `hydration_request_id`;
- canonical `object_id`;
- active question;
- Capability Mission Request reference;
- Formation Selection reference where applicable;
- Occupancy Witness reference;
- Zone reference;
- Space reference;
- Orientation reference;
- Territory reference;
- requested verified-territory references;
- requested payload references;
- payload scope;
- mission-necessity basis;
- evidence boundary;
- evidence ceiling;
- restriction references;
- Stick reference;
- Governance reference;
- authorization reference;
- Human Gate reference when applicable;
- provenance route;
- request time.

The request asks for bounded restoration.

Request != restored payload.

---

## 7. Hydration Request Identity

Native-v41 `hydration_request_id` is deterministic SHA-512 over the complete
Hydration Request except its own ID.

A material change to mission, question, requested territory, requested payload,
representation, evidence boundary, or necessity basis changes request identity.

Hydration Request identity is not Room Object identity.

Hydration Request identity is not content identity.

---

## 8. Payload Scope

Native R3-I defines one permissible hydration scope:

`MISSION_REQUIRED`

There is no `FULL_PAYLOAD` hydration mode.

There is no `LOAD_EVERYTHING` hydration mode.

Full payload hydration without question-driven necessity is prohibited.

---

## 9. Requested Verified Territory

Each requested territory reference MUST already belong to verified operational
territory available under current constraints.

Requesting territory does not establish verification.

Requested != verified by request.

Hydration consumes verification.

It does not create verification.

---

## 10. Requested Payload

Payload references identify content whose active availability is required by the
mission.

Payload identity and Room identity remain distinct.

Payload access does not redefine Room identity.

Payload restoration does not imply canonical mutation.

---

## 11. Necessity Basis

Every request preserves an explicit `mission_necessity_basis`.

The basis explains why the requested hydration is required for the current
question and mission.

A generic desire for completeness is insufficient.

"Load everything" is not a mission necessity.

Convenience != necessity.

---

## 12. Evidence Boundary

Hydration MUST remain inside the active evidence boundary.

Hydration MUST NOT silently expose excluded evidence.

Excluded != absent.

Restricted != absent.

Hydrated != admissible beyond the existing boundary.

---

## 13. Evidence Ceiling

Hydration does not raise the evidence ceiling.

More accessible payload != stronger claim authority.

More data != automatic analytical promotion.

Hydration changes active availability, not epistemic authority.

---

## 14. Restrictions

Restricted or inaccessible surfaces remain explicit.

Hydration MUST NOT reinterpret restricted content as nonexistent.

A blocked payload remains represented as blocked.

Restriction != absence.

---

## 15. Authorization

Hydration capability does not create authorization.

Requested access requires applicable authorization.

Authorization reference != invented authority.

Technical accessibility != authorized hydration.

Write capability != authority.

---

## 16. Human Gate

Where Human Gate applies, the request preserves its reference.

Human Gate approval MUST NOT be fabricated.

Approval != hydration execution.

---

## 17. Hydration Release Record

Every Hydration Release Record MUST preserve:

- `hydration_release_id`;
- Hydration Request reference;
- canonical `object_id`;
- release state;
- restored verified-territory references;
- restored payload references;
- denied or blocked references;
- payload references retained at rest;
- payload references released from active hydration;
- release basis;
- restriction findings;
- evidence boundary;
- evidence ceiling;
- Room state reference;
- representation-state reference;
- Stick reference;
- final active payload scope;
- provenance route;
- release time.

The Release Record states what became actively available and what remained or
returned to rest.

---

## 18. Hydration Release Identity

Native-v41 `hydration_release_id` is deterministic SHA-512 over the complete
Hydration Release Record except its own ID.

A material change to restored territory, payload, blocked material, released
material, or active scope changes Release identity.

Hydration Release identity is not Room Object identity.

Hydration Release identity is not Hydration Request identity.

---

## 19. Release States

R3-I defines three native Release states:

- `RELEASED`;
- `PARTIAL`;
- `BLOCKED`.

`RELEASED` means the justified mission-required hydration was restored within
the declared constraints.

`PARTIAL` means only part of the justified request could be restored.

`BLOCKED` means the requested hydration could not be restored under current
constraints.

RELEASED != unrestricted access.

PARTIAL != failure.

BLOCKED != nonexistent.

---

## 20. Exact Request Binding

A Hydration Release MUST resolve to one Hydration Request.

The Release MUST NOT silently restore payload not requested by that Request.

Restored payload must be a subset of requested payload.

Restored verified territory must be a subset of requested verified territory.

Release cannot broaden request scope.

---

## 21. Payload at Rest

Payload not needed by the current mission remains at rest.

The Release Record preserves payload intentionally retained at rest.

At rest != absent.

At rest != deleted.

At rest != inaccessible forever.

---

## 22. Releasing Unnecessary Active Payload

Hydration also releases unnecessary active payload.

When mission need ends or narrows, payload may be released from active hydration
without changing Room identity.

Release from active hydration != deletion.

Release from active hydration != evidence destruction.

Release from active hydration != Room closure.

---

## 23. Identity Preservation

Hydration MUST preserve:

- canonical Room Object identity;
- Origin continuity;
- state lineage;
- representation identity;
- evidence lineage;
- provenance;
- return coordinates through Stick.

Hydration does not replace the Room.

Payload loading does not become object identity.

---

## 24. State Preservation

Hydration preserves Room state.

Hydration preserves representation state except for attributable active-payload
availability.

Hydration MUST NOT silently mutate lifecycle state.

Hydration MUST NOT silently mutate Occupancy.

Hydration MUST NOT silently mutate Formation.

Hydration state != Room lifecycle state.

---

## 25. Occupancy

Hydration does not establish presence.

An Occupancy Witness remains the evidence of presence.

Hydrated payload != occupant.

Hydration Request != Occupancy Witness.

---

## 26. Mission

Hydration supports a mission.

Hydration does not create a mission.

Capability Mission Request remains the mission contract.

Hydration Request != Capability Mission Request.

Payload need follows mission.

Mission does not follow payload availability.

---

## 27. Formation

A formation may create justified need for multiple bounded surfaces.

Formation does not automatically authorize full hydration.

Formation Selection != hydration authority.

Swarm != load everything.

Expanded Analysis != full payload.

---

## 28. Cartography

Hydration may restore payload needed to operate against verified territory
represented in Cartography.

Hydration does not redefine Cartography.

Hydration does not establish geometry merely by loading content.

Loaded content != mapped truth.

---

## 29. Stick

Hydration MUST preserve the Stick.

Changing active payload availability MUST NOT break:

- object identity;
- Origin route;
- transform history;
- provenance;
- evidence lineage;
- return coordinates.

Payload movement must not break analytical continuity.

---

## 30. Goblin Signal

Goblin Signal may communicate attributable hydration-related events later if
needed by Room-aware participants.

Goblin Signal does not grant hydration.

Signal != hydration authorization.

Hydration Request != Goblin Signal event.

---

## 31. Landing

Landing may release unnecessary active payload while preserving identity,
orientation, representation position, Cartography, provenance, unresolved
terrain, and readiness.

R3-I defines payload release mechanics only.

R3-I does not define Landing Witness semantics.

Payload release != Landing.

---

## 32. Replay

Replay may later require mission-scoped hydration at a preserved observational
coordinate.

R3-I does not define Replay.

Hydration != replay.

Hydration MUST NOT reconstruct an approximate duplicate Room.

---

## 33. Restriction / Constriction Boundary

R3-I preserves current restrictions.

It does not yet define Restriction / Constriction state transitions.

Hydration cannot bypass restriction.

Hydration cannot silently collapse inaccessible terrain.

---

## 34. Failure Conditions

R3-I MUST reject:

- full-payload hydration without question-driven necessity;
- payload restoration outside the request;
- territory restoration outside verified requested territory;
- hydration without an active mission;
- hydration without an active question;
- evidence-boundary broadening;
- evidence-ceiling elevation by hydration;
- restriction bypass;
- Room identity replacement by content identity;
- silent lifecycle mutation;
- silent occupancy mutation;
- silent formation mutation.

---

## 35. R3-I Lock

Hydration is not merely loading files.

Hydration restores only verified operational territory required by the active
mission and representation.

Payload remains at rest except where mission-scoped access is justified.

Identity travels.

Payload rests.

Hydrate what the question requires.

Leave unnecessary payload at rest.

Hydration does not convert unverified material into verified territory.

Hydration does not qualify the Room.

Hydration does not create reachability.

Hydration does not manufacture evidence.

Mission-required != potentially interesting.

Available != necessary.

Possible relevance != hydration justification.

Hydration does not broaden representation scope.

Hydration does not create another Room.

Request != restored payload.

There is no FULL_PAYLOAD hydration mode.

There is no LOAD_EVERYTHING hydration mode.

Full payload hydration without question-driven necessity is prohibited.

Requested != verified by request.

Hydration consumes verification.

It does not create verification.

Payload identity and Room identity remain distinct.

Payload restoration does not imply canonical mutation.

A generic desire for completeness is insufficient.

Convenience != necessity.

Hydration MUST NOT silently expose excluded evidence.

Hydration does not raise the evidence ceiling.

More accessible payload != stronger claim authority.

More data != automatic analytical promotion.

Restriction != absence.

Technical accessibility != authorized hydration.

Write capability != authority.

Approval != hydration execution.

Restored payload must be a subset of requested payload.

Restored verified territory must be a subset of requested verified territory.

Release cannot broaden request scope.

At rest != absent.

At rest != deleted.

Release from active hydration != deletion.

Release from active hydration != evidence destruction.

Release from active hydration != Room closure.

Hydration does not replace the Room.

Payload loading does not become object identity.

Hydration MUST NOT silently mutate lifecycle state.

Hydration MUST NOT silently mutate Occupancy.

Hydration MUST NOT silently mutate Formation.

Hydration state != Room lifecycle state.

Hydrated payload != occupant.

Hydration Request != Occupancy Witness.

Hydration Request != Capability Mission Request.

Payload need follows mission.

Mission does not follow payload availability.

Formation Selection != hydration authority.

Swarm != load everything.

Expanded Analysis != full payload.

Loaded content != mapped truth.

Hydration MUST preserve the Stick.

Signal != hydration authorization.

Hydration Request != Goblin Signal event.

Payload release != Landing.

Hydration != replay.

Hydration cannot bypass restriction.

No Landing Witness semantics yet.

No Replay semantics yet.

No Restriction / Constriction transitions yet.
