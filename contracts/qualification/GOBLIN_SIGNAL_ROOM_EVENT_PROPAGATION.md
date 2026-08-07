# R3-H — Goblin Signal / Room Event Propagation

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R3-H
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R3-H defines native-v41 Goblin Signal Room-event propagation.

Goblin Signal communicates attributable changes and disturbances across the
bounded Room-aware mesh.

R3-H consumes:

- complete Rings 1 and 2;
- R3-A through R3-G;
- attributable source records for the event being propagated.

R3-H does not own or manufacture the underlying state change.

---

## 1. Responsibility

Registry defines.

Governance directs.

TOC coordinates.

Goblin Signal communicates.

Audit verifies.

Goblin Signal carries:

- Room events;
- disturbances;
- qualification changes;
- occupancy changes;
- branch or adjoining-object signals;
- capability-return notifications.

Communication != ownership.

---

## 2. Event Principle

An event MUST have an attributable source before Goblin Signal propagates it.

Goblin Signal announces what occurred.

Goblin Signal does not decide that it occurred.

Propagation != source-state mutation.

Signal != truth.

---

## 3. Goblin Signal Event Record

Every Goblin Signal Event MUST preserve:

- `goblin_signal_event_id`;
- canonical `object_id`;
- event class;
- event subtype;
- source-record type;
- source-record reference;
- source component;
- event subject;
- prior-state reference where applicable;
- resulting-state reference where applicable;
- Zone references where applicable;
- Space references where applicable;
- Cartography reference where applicable;
- Stick reference;
- evidence boundary;
- evidence ceiling;
- propagation scope;
- intended recipients;
- delivery state;
- sequence coordinate;
- provenance route;
- emitted time.

---

## 4. Event Identity

Native-v41 `goblin_signal_event_id` is deterministic SHA-512 over the complete
Goblin Signal Event except the ID itself.

A material change to event meaning, source, subject, propagation scope,
recipients, or sequence changes event identity.

Goblin Signal Event identity is not Room Object identity.

Goblin Signal Event identity is not source-record identity.

---

## 5. Native Event Classes

R3-H defines six native event classes:

- `ROOM_EVENT`;
- `DISTURBANCE`;
- `QUALIFICATION_CHANGE`;
- `OCCUPANCY_CHANGE`;
- `BRANCH_OR_ADJOINING_OBJECT_SIGNAL`;
- `CAPABILITY_RETURN_NOTIFICATION`.

These preserve the source responsibility vocabulary.

---

## 6. Qualification Announcement Subtypes

Qualification-change propagation recognizes:

- `QUALIFIED`;
- `REJECTED`;
- `INSTABILITY`;
- `BRANCH_AVAILABLE`;
- `FURTHER_RECONNAISSANCE_NEEDED`.

Goblin Signal may announce these only from attributable upstream records.

Announcement != qualification decision.

---

## 7. Qualification Ordering

Registry finalizes or rejects Room qualification state before Goblin Signal
announces the qualification change.

Goblin Signal MUST NOT announce a qualification result as established merely
because qualification activity is underway.

QUALIFYING != QUALIFIED.

Signal cannot outrun Registry state.

---

## 8. Room Events

A Room event is an attributable change relevant to Room-aware participants.

The event record preserves the source record and provenance route.

Room event != Room Object.

Event history becomes part of the evolving object's attributable history
without becoming object identity.

---

## 9. Disturbance

A disturbance communicates a material signal that may affect:

- orientation;
- qualification;
- movement;
- formation;
- evidence requirements;
- current analytical geometry.

Disturbance != finding.

Disturbance != automatic escalation.

Disturbance != lifecycle mutation.

---

## 10. Qualification Change

A qualification-change event carries an already attributable qualification
change.

It may announce:

- qualification;
- rejection;
- instability;
- branch availability;
- need for further reconnaissance.

Qualification Change Event != Qualification Record.

Qualification Change Event != Registry transition.

---

## 11. Occupancy Change

An occupancy-change event carries an attributable occupancy change.

The source SHOULD resolve to an Occupancy Witness.

Goblin Signal does not create presence.

Goblin Signal does not terminate presence.

Occupancy Witness establishes presence state.

Signal communicates the change.

---

## 12. Branch / Adjoining-Object Signal

Goblin Signal may communicate:

- branch availability;
- adjoining-object signal;
- distinct-object concern;
- controlled relationship availability.

A signal of possible distinctness does not establish distinct-object identity.

Branch signal != branch creation.

Adjoining-object signal != new Room.

Distinct-object determination remains upstream.

---

## 13. Capability Return Notification

Goblin Signal carries capability-return notifications.

The underlying Capability Return remains authoritative for what the capability
actually returned.

Notification != Capability Return.

Notification does not rewrite bounded findings.

Returned evidence != automatically promoted evidence.

---

## 14. Source Record Binding

Every event MUST preserve a resolvable `source_record_reference`.

Source records may include:

- Qualification Record;
- lifecycle transition;
- Occupancy Witness;
- Capability Return;
- Formation Selection Record;
- distinct-object or branch-related record;
- other attributable Room event record.

Goblin Signal MUST NOT synthesize a source record when one is required.

No fake source.

---

## 15. Source Component

The event preserves the component that owns the underlying source action.

Examples:

- Registry for lifecycle or qualification-state finalization;
- capability / Goblin / Team / Platoon for return evidence;
- occupancy subsystem / Registry for occupancy state;
- TOC for formation or mission coordination record;
- governed lineage control for branch-related state.

Goblin Signal remains communicator.

Source ownership != communication ownership.

---

## 16. Event Subject

The event subject states what changed or what signal must be communicated.

The subject MUST be bounded.

Event subject != interpretation authority.

Event subject != decision.

---

## 17. Prior and Resulting State

Where an event concerns a state transition, prior and resulting state references
remain explicit.

Goblin Signal MUST NOT rewrite transition history.

Event propagation preserves ordering.

History accumulates.

---

## 18. Representation References

Where relevant, Goblin Signal preserves:

- Zone;
- Space;
- Cartography;
- Stick.

Propagation MUST NOT strip the coordinates needed to understand where the event
occurred.

Signal without resolvable context is insufficient.

---

## 19. Stick Preservation

Goblin Signal propagation preserves continuity through:

- object identity;
- Origin route via provenance;
- transform history where relevant;
- evidence lineage;
- return coordinates where relevant.

Propagation MUST NOT fracture object continuity.

---

## 20. Evidence Boundary and Ceiling

An event carries the evidence boundary and ceiling applicable to the source
observation or state change.

Propagation does not broaden access.

Propagation does not raise claim ceiling.

Receiving an event != authorization to see restricted source content.

---

## 21. Propagation Scope

Every event declares its propagation scope.

Native-v41 scopes are:

- `LOCAL`;
- `ROOM`;
- `FORMATION`;
- `FAMILY`;
- `CONTROL_PLANE`.

Scope declares where the event may travel.

Scope != authority.

---

## 22. Intended Recipients

The event preserves intended recipients or recipient classes.

Recipient declaration MUST remain bounded by:

- authorized view;
- evidence restrictions;
- Governance constraints;
- mission need.

Broadcast capability != permission to broadcast.

---

## 23. Delivery State

R3-H defines transport-state vocabulary:

- `EMITTED`;
- `DELIVERED`;
- `PARTIAL`;
- `BLOCKED`.

`EMITTED` means the event was created for propagation.

`DELIVERED` means intended bounded delivery completed.

`PARTIAL` means some intended bounded recipients received the event.

`BLOCKED` means propagation could not proceed under current constraints.

Delivery state != source-event truth.

---

## 24. Partial Delivery

Partial delivery MUST remain explicit.

Partial delivery MUST NOT be represented as full propagation.

Undelivered recipient != nonexistent recipient.

Restricted recipient != absent recipient.

---

## 25. Blocked Delivery

Blocked propagation preserves the reason through attributable event/provenance
context.

Blocked communication does not erase the source event.

Source event persists independently of delivery success.

---

## 26. Sequence Coordinate

Every Goblin Signal Event preserves an attributable sequence coordinate.

Event ordering matters.

A later announcement MUST NOT silently precede its source state.

Sequence != wall-clock truth by itself.

---

## 27. No Ownership Promotion

Goblin Signal does not own:

- Room identity;
- qualification truth;
- lifecycle state;
- occupancy;
- formation selection;
- capability findings;
- canonical mutation;
- publication;
- execution.

Communicator != authority.

---

## 28. No Mutation by Propagation

Propagation alone MUST NOT cause:

- lifecycle transition;
- occupancy transition;
- formation change;
- branch creation;
- distinct-object establishment;
- evidence promotion;
- canonical mutation.

Signal may trigger consideration.

Signal does not perform the governed action.

---

## 29. No False Consensus

Multiple Goblin Signal events do not become truth by repetition.

Repeated notification != independent evidence.

Event count != confidence.

Consensus-by-broadcast is prohibited.

---

## 30. Failure Isolation

A local propagation failure should produce local communication degradation.

It MUST NOT silently invalidate the underlying source record.

Transport failure != analytical erasure.

---

## 31. Capability Return Ordering

Capability Return exists before the corresponding return notification.

Return first.

Notify second.

Notification cannot replace Return.

---

## 32. Occupancy Ordering

Occupancy Witness exists before an attributable occupancy-change announcement.

Presence first.

Notify second.

Notification cannot manufacture presence.

---

## 33. Formation Ordering

Formation Selection Record exists before an attributable formation-change
announcement.

Selection first.

Notify second.

Notification cannot select formation.

---

## 34. Hydration Boundary

R3-H does not hydrate payload.

An event may later indicate that hydration should be considered.

Signal != hydration request.

Signal != payload release.

Hydration remains R3-I.

---

## 35. ACTIVE Lifecycle Boundary

R3-H does not itself transition lifecycle to ACTIVE.

An event may announce an attributable lifecycle transition after that transition
exists.

Signal != lifecycle transition.

---

## 36. Publication Boundary

Goblin Signal does not alter:

Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate

Event propagation != publication.

Event propagation != decision authority.

---

## 37. R3-H Lock

Goblin Signal communicates.

Communication != ownership.

Goblin Signal announces what occurred.

Goblin Signal does not decide that it occurred.

Propagation != source-state mutation.

Signal != truth.

Signal cannot outrun Registry state.

Announcement != qualification decision.

Room event != Room Object.

Disturbance != finding.

Disturbance != automatic escalation.

Qualification Change Event != Qualification Record.

Qualification Change Event != Registry transition.

Goblin Signal does not create presence.

Goblin Signal does not terminate presence.

Occupancy Witness establishes presence state.

Branch signal != branch creation.

Adjoining-object signal != new Room.

Notification != Capability Return.

Notification does not rewrite bounded findings.

Goblin Signal MUST NOT synthesize a source record when one is required.

No fake source.

Goblin Signal remains communicator.

Source ownership != communication ownership.

Propagation does not broaden access.

Propagation does not raise claim ceiling.

Scope != authority.

Broadcast capability != permission to broadcast.

Partial delivery MUST NOT be represented as full propagation.

Blocked communication does not erase the source event.

Source event persists independently of delivery success.

Event ordering matters.

Communicator != authority.

Signal may trigger consideration.

Signal does not perform the governed action.

Repeated notification != independent evidence.

Event count != confidence.

Consensus-by-broadcast is prohibited.

Transport failure != analytical erasure.

Return first.

Notify second.

Presence first.

Notify second.

Selection first.

Notify second.

Signal != hydration request.

Signal != payload release.

Signal != lifecycle transition.

Event propagation != publication.

Event propagation != decision authority.

No Hydration semantics yet.

No ACTIVE lifecycle transition execution yet.
