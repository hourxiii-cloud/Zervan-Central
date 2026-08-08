# R4-C — Landing Witness

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R4-C
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R4-C defines native-v41 Landing Witness.

Capabilities may cease movement without ceasing occupation.

Landing preserves the Room and its operational position while movement stops.

Landing is not exit.

Landing is not closure.

Landing is not replay.

---

## 1. Source Invariant

Capabilities may cease movement without ceasing occupation.

Landing preserves:

- object identity;
- orientation;
- representation position;
- Cartography;
- provenance;
- prior question;
- prior rendering;
- unresolved terrain;
- readiness.

Landing may release unnecessary active payload.

---

## 2. Dependency

R4-C consumes:

- complete Rings 1 through 3;
- R4-A Restriction / Constriction;
- R4-B Collapse Boundary where applicable;
- current Occupancy Witness;
- active Room identity;
- active Zone and Space;
- Orientation;
- Cartography;
- Stick continuity;
- Hydration state;
- current question;
- current rendering where applicable;
- unresolved terrain;
- readiness state.

R4-C does not redefine those substrates.

---

## 3. Landing Witness

Every Landing Witness MUST preserve:

- `landing_witness_id`;
- canonical `object_id`;
- occupant capability;
- occupancy witness reference;
- mission reference;
- formation reference where applicable;
- Zone reference;
- Space reference;
- Orientation reference;
- Cartography reference;
- Stick reference;
- prior question;
- prior rendering reference where applicable;
- unresolved-terrain references;
- readiness reference;
- restriction / constriction references where applicable;
- Collapse Boundary references where applicable;
- active payload before Landing;
- payload released at Landing;
- active payload retained after Landing;
- current coordinates;
- return coordinates;
- landing basis;
- Governance reference;
- authorization reference;
- Human Gate reference where applicable;
- provenance route;
- landed time.

---

## 4. Landing Witness Identity

Native-v41 `landing_witness_id` is deterministic SHA-512 over the complete
Landing Witness except its own ID.

A material change to:

- occupant;
- Room identity;
- mission;
- representation;
- coordinates;
- preserved question;
- unresolved terrain;
- readiness;
- payload disposition;
- landing basis

changes Landing Witness identity.

Landing Witness identity is not Room Object identity.

Landing Witness identity is not Occupancy Witness identity.

---

## 5. Movement Stops

Landing means current capability movement has ceased.

Landing records a stable operational coordinate.

Landing does not imply that occupation has ended.

Movement state != occupancy state.

Stopped movement != exited Room.

---

## 6. Occupation Persists

Landing MUST preserve a valid Occupancy Witness reference.

The capability remains an attributable occupant unless a separate EXITED
Occupancy Witness exists.

Landing cannot manufacture presence.

Landing cannot terminate presence.

Landing != Occupancy EXITED.

---

## 7. Object Identity

Landing preserves canonical Room Object identity.

Landing does not create a new Room.

Landing does not create a snapshot object.

Landing does not clone the Room for later restart.

The Room remains the Room.

---

## 8. Orientation

Landing preserves Orientation.

The system retains where the capability is relative to:

- Room;
- Zone;
- Space;
- Cartography;
- current mission geometry.

Landing MUST NOT require re-orientation from scratch merely because movement
stopped.

Stopped movement != lost orientation.

---

## 9. Representation Position

Landing preserves the capability's representation position.

Zone and Space remain attributable.

Perspective / transform context remains resolvable.

Landing does not reset representation to a default.

No default substitution.

---

## 10. Cartography

Landing preserves Cartography.

The Landing coordinate remains part of navigable analytical geometry.

Cartography preserves:

- position;
- route;
- prior movement;
- unresolved terrain;
- Collapse boundaries where applicable;
- return route.

Landing != Cartography reset.

---

## 11. Provenance

Landing preserves provenance.

The system retains:

- how the capability arrived;
- what evidence was used;
- what operations occurred;
- what restrictions were active;
- what Collapse events occurred;
- what payload was active;
- what payload was released.

Landing MUST NOT reduce provenance.

---

## 12. Prior Question

Landing preserves the prior active question.

The prior question remains attributable even if no question is currently
executing.

Landing does not automatically create another question.

Landing does not automatically re-ask the prior question.

Question preservation != reflight.

---

## 13. Prior Rendering

Where a rendering exists, Landing preserves its reference.

The prior rendering remains historical context.

Landing does not automatically regenerate the rendering.

Rendering preservation != rendering execution.

---

## 14. Unresolved Terrain

Landing preserves unresolved terrain.

Unknown remains unknown.

Landing does not require unresolved terrain to be artificially resolved before
movement stops.

Unresolved != failed Landing.

Landing does not erase uncertainty.

---

## 15. Readiness

Landing preserves readiness without forcing continued movement.

Readiness means the Room and operational coordinate remain capable of valid
future continuation under applicable constraints.

Readiness != movement.

Readiness != automatic reflight.

Readiness != execution authority.

---

## 16. Payload Release

Landing may release unnecessary active payload.

Payload released at Landing is no longer actively hydrated.

Released payload remains attributable.

Release from active hydration != deletion.

Released payload != absent.

Released payload != destroyed evidence.

---

## 17. Payload Retention

Payload still required to preserve the Landing state may remain active.

Retained active payload MUST remain mission-justified.

Landing does not authorize full-payload retention.

Payload necessity still governs active availability.

---

## 18. Payload Partition

The active payload set before Landing MUST be partitioned into:

- payload released at Landing;
- payload retained active after Landing.

A payload reference MUST NOT appear in both sets.

The union of released and retained payload MUST exactly equal the active payload
set before Landing.

Landing MUST NOT silently lose active-payload history.

---

## 19. Restriction / Constriction

Landing preserves active Restriction / Constriction references where applicable.

Landing does not reverse analytical narrowing.

Landing does not create new Restriction or Constriction.

Landing != Restriction.

Landing != Constriction.

---

## 20. Collapse

Landing preserves Collapse Boundary references where applicable.

Landing does not reverse Collapse.

Landing does not execute re-expansion.

Landing != Collapse.

Collapse history remains attributable.

---

## 21. Coordinates

Every Landing Witness preserves:

- current coordinates;
- return coordinates.

Current coordinates identify where movement ceased.

Return coordinates preserve the route back through analytical continuity.

Landing coordinate != new origin.

---

## 22. Stick

Landing MUST preserve the Stick.

The Landing state remains connected to:

- canonical object identity;
- Origin;
- representation history;
- evidence lineage;
- provenance;
- current coordinate;
- return coordinate.

Landing MUST NOT sever analytical continuity.

---

## 23. Governance

Governance constraints remain active at Landing.

Landing does not erase:

- evidence obligations;
- claim ceilings;
- prohibited assumptions;
- Human Gate requirements;
- movement constraints;
- publication constraints.

Stopping movement != policy reset.

---

## 24. Authorization

Landing does not create future execution authority.

An authorized mission may land.

Future Reflight requires its own valid trigger and applicable authorization.

Landing Witness != reflight authorization.

---

## 25. Human Gate

Where Human Gate applies, its reference remains preserved.

Landing does not fabricate approval.

Landing does not bypass Human Gate.

Human Gate state remains attributable.

---

## 26. Lifecycle

Source lifecycle recognizes LANDED as a Room condition where movement has
ceased while occupation, coordinates, unresolved terrain, and readiness remain
preserved.

R4-C records the Landing Witness.

R4-C does not silently mutate lifecycle by witness creation alone.

Landing Witness != lifecycle transition.

A Registry transition to LANDED remains separately attributable where the
runtime lifecycle surface requires it.

---

## 27. Capability Mission

Landing may occur after or during a bounded capability mission.

Landing does not rewrite the mission.

Landing does not mark a mission complete merely because movement stopped.

Mission completion != Landing.

Landing != Capability Return.

---

## 28. Formation

A formation may land in whole or in part.

R4-C records an attributable capability Landing Witness.

Formation-wide Landing requires independently attributable participating
Landing states.

One occupant Landing != whole formation Landing.

Landing does not select formation.

---

## 29. Goblin Signal

Goblin Signal may communicate an attributable Landing event.

Signal does not perform Landing.

Notification != Landing.

Landing first.

Notify second.

---

## 30. Reflight Boundary

Landing establishes the preserved state from which Reflight may later occur.

Reflight requires a real analytical trigger.

Landing does not itself create that trigger.

Landing != Reflight.

R4-D owns Reflight Trigger.

---

## 31. Post-Convergence Boundary

Landing supports post-convergence control.

Acknowledgment, celebration, repetition, affect, or conversational continuation
does not itself authorize renewed analytical movement.

Landing preserves state so the system does not need to rebuild the Room merely
to remain conversational.

R4-E owns post-convergence closure / Closing Witness.

---

## 32. Replay Boundary

Landing preserves coordinates needed for future Replay.

Replay may later reopen the same Room at a preserved observational coordinate.

Landing does not perform Replay.

Landing != Replay Envelope.

---

## 33. Failure Conditions

R4-C MUST reject:

- Landing without attributable Room identity;
- Landing without Occupancy Witness;
- Landing that silently terminates occupation;
- Landing that loses Orientation;
- Landing that resets Zone or Space;
- Landing that loses Cartography;
- Landing that loses provenance;
- Landing that erases prior question;
- Landing that erases unresolved terrain;
- Landing that destroys readiness;
- payload release represented as deletion;
- payload retained without bounded necessity;
- active payload silently omitted from release/retain partition;
- Landing that severs Stick continuity;
- Landing used as automatic Reflight authorization;
- Landing used as automatic mission completion;
- Landing used as lifecycle mutation by witness alone;
- Landing used as Replay reconstruction.

---

## 34. R4-C Lock

Capabilities may cease movement without ceasing occupation.

Landing preserves object identity.

Landing preserves orientation.

Landing preserves representation position.

Landing preserves Cartography.

Landing preserves provenance.

Landing preserves prior question.

Landing preserves prior rendering.

Landing preserves unresolved terrain.

Landing preserves readiness.

Landing may release unnecessary active payload.

Landing is not exit.

Landing is not closure.

Landing is not replay.

Movement state != occupancy state.

Stopped movement != exited Room.

Landing MUST preserve a valid Occupancy Witness reference.

Landing cannot manufacture presence.

Landing cannot terminate presence.

Landing != Occupancy EXITED.

The Room remains the Room.

Stopped movement != lost orientation.

Landing does not reset representation to a default.

No default substitution.

Landing != Cartography reset.

Landing MUST NOT reduce provenance.

Question preservation != reflight.

Rendering preservation != rendering execution.

Unresolved != failed Landing.

Landing does not erase uncertainty.

Readiness != movement.

Readiness != automatic reflight.

Readiness != execution authority.

Release from active hydration != deletion.

Released payload != absent.

Released payload != destroyed evidence.

Landing does not authorize full-payload retention.

The union of released and retained payload MUST exactly equal the active payload
set before Landing.

Landing != Restriction.

Landing != Constriction.

Landing != Collapse.

Landing coordinate != new origin.

Landing MUST preserve the Stick.

Landing MUST NOT sever analytical continuity.

Stopping movement != policy reset.

Landing Witness != reflight authorization.

Landing Witness != lifecycle transition.

Mission completion != Landing.

Landing != Capability Return.

One occupant Landing != whole formation Landing.

Landing does not select formation.

Notification != Landing.

Landing first.

Notify second.

Landing != Reflight.

R4-D owns Reflight Trigger.

Landing preserves state so the system does not need to rebuild the Room merely
to remain conversational.

Landing != Replay Envelope.

No Reflight Trigger semantics yet.

No Closing Witness semantics yet.

No Replay semantics yet.

No Scar Replay semantics yet.
