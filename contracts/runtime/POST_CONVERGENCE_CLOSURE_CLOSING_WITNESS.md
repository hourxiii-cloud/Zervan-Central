# R4-E — Post-Convergence Closure / Closing Witness

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R4-E
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R4-E defines native-v41 Post-Convergence Closure and Closing Witness.

After convergence, do not rebuild or re-explain the Room without a new
analytical trigger.

When the message has landed:

- land;
- preserve object and representation state;
- remain naturally conversational;
- do not rebuild The Room in prose;
- prefer the smallest sufficient response.

R4-E closes the current operational interval without deleting the Room,
destroying occupation history, or fabricating a Reflight condition.

---

## 1. Source Boundary

The source requires a machine-readable Closing Witness.

The source does not prescribe the complete machine-state field vocabulary of
that witness.

The field structure below is native implementation structure constrained by
source invariants.

Implementation structure != new doctrine.

---

## 2. Dependency

R4-E consumes:

- complete Rings 1 through 3;
- R4-A Restriction / Constriction;
- R4-B Collapse Boundary;
- R4-C Landing Witness;
- R4-D Reflight Trigger;
- canonical Room Object identity;
- representation state;
- Cartography;
- Stick continuity;
- evidence boundary;
- evidence ceiling;
- unresolved terrain;
- lineage;
- replay coordinates;
- attributable provenance.

Closure MUST bind the same Room identity.

---

## 3. Governing Principle

Convergence does not authorize unnecessary reprocessing.

Closure preserves state.

Closure does not reconstruct state.

Closure does not delete state.

Closure does not promote state.

Closed interval != destroyed Room.

---

## 4. Post-Convergence Control

After convergence, no rebuild or re-explanation of the Room occurs without a
new analytical trigger.

Importance does not authorize Reflight.

Emotion does not authorize Reflight.

Acknowledgment does not authorize Reflight.

Celebration does not authorize Reflight.

Laughter does not authorize Reflight.

Repetition of a settled point does not authorize Reflight.

Conversation may continue naturally while analytical movement remains stopped.

---

## 5. Smallest Sufficient Response

Post-convergence communication SHOULD prefer the smallest sufficient response.

Smallest sufficient response is a communication rule.

It is not analytical compression.

It MUST NOT erase:

- object identity;
- evidence;
- provenance;
- geometry;
- representation history;
- unresolved terrain;
- lineage;
- replay coordinates.

Small response != compressed Room.

---

## 6. Closing Witness

Every Closing Witness MUST preserve:

- `closing_witness_id`;
- canonical `object_id`;
- Landing Witness reference;
- convergence-state reference;
- closure basis;
- current question reference or preserved question;
- current representation reference;
- Zone reference;
- Space reference;
- Cartography reference;
- Stick reference;
- evidence boundary;
- evidence ceiling;
- unresolved-terrain references;
- Restriction / Constriction references;
- Collapse Boundary references;
- relevant Reflight Trigger references;
- outstanding analytical obligations;
- preserved lineage reference;
- replay coordinates;
- return coordinates;
- current rendering reference where applicable;
- closure disposition;
- blocking reasons;
- Audit witness reference;
- Registry reference;
- Governance reference;
- Human Gate reference where applicable;
- provenance route;
- closure time.

---

## 7. Closing Witness Identity

Native-v41 `closing_witness_id` is deterministic SHA-512 over the complete
Closing Witness except its own ID.

A material change to:

- closure basis;
- Room identity;
- Landing Witness;
- representation;
- evidence boundary;
- evidence ceiling;
- unresolved terrain;
- analytical obligations;
- lineage;
- replay coordinates;
- closure disposition

changes Closing Witness identity.

Closing Witness identity is not Room Object identity.

Closing Witness identity is not State Root.

---

## 8. Closure Disposition

R4-E defines two native implementation dispositions:

- `CLOSED`;
- `BLOCKED`.

`CLOSED` means the current operational interval has sufficient closing evidence
to stop analytical movement while preserving state and replayability.

`BLOCKED` means current unresolved operational obligations prevent defensible
closure.

CLOSED != canonical promotion.

BLOCKED != analytical failure.

---

## 9. Same Room Identity

A Closing Witness MUST bind the same canonical Room Object as the interval being
closed.

Closing Witness cannot silently substitute another Room identity.

Closing Witness cannot create another Room.

Closing Witness cannot create a snapshot-world replacement.

Close the interval.

Do not clone the object.

---

## 10. Landing Dependency

Closure requires an attributable Landing Witness.

Landing establishes the preserved stopped-movement state.

Closing Witness binds that Landing state.

Landing first.

Closing Witness second.

Closure MUST NOT infer an approximate landing state.

---

## 11. Convergence

Closure requires an attributable convergence or completion basis.

Convergence means the current analytical movement has reached its bounded
stopping condition under the current question, evidence boundary, and evidence
ceiling.

Convergence != absolute truth.

Convergence != certainty.

Convergence != publication approval.

---

## 12. Reflight Relationship

A new valid Reflight Trigger may later justify renewed movement.

Closing Witness does not disable future Reflight.

Closing Witness does not manufacture a Reflight Trigger.

Closing Witness preserves any relevant trigger history.

Closure now != never analyze again.

---

## 13. Outstanding Analytical Obligations

A `CLOSED` witness MUST NOT contain unresolved outstanding analytical
obligations that require current movement.

If such obligations remain active, closure MUST be `BLOCKED`.

Unresolved terrain may remain preserved without blocking closure when current
mission/evidence conditions do not require immediate movement.

Unresolved terrain != outstanding movement obligation.

---

## 14. Unresolved Terrain

Closing preserves unresolved terrain.

Closure does not require every unknown to disappear.

Closure does not convert unknown into known.

Closure does not convert inaccessible into absent.

Unknown may remain when the current operational interval is defensibly closed.

---

## 15. Evidence Boundary

Closure preserves the active evidence boundary.

Closing Witness cannot silently broaden evidence scope.

Closure does not admit excluded evidence retroactively.

Excluded != absent.

---

## 16. Evidence Ceiling

Closure preserves the active evidence ceiling.

Closure does not raise claim authority.

Closure does not convert convergence into certainty.

Closed interval != higher evidence ceiling.

---

## 17. Restriction / Constriction History

Closing preserves relevant Restriction / Constriction records.

Current narrowed support remains attributable.

Closure does not erase previously supported states.

Closure does not rewrite narrowing history.

---

## 18. Collapse History

Closing preserves relevant Collapse Boundaries.

Removed, retained, deferred, and surviving uncertainty remain attributable.

Closure does not flatten Collapse into a final summary.

Collapse history remains replayable.

---

## 19. Lineage

The source defines SEALED as an operational interval closed with preserved
lineage.

Closing Witness MUST preserve lineage.

Closure without lineage is incomplete.

Historical route MUST remain reconstructible.

---

## 20. Replay Coordinates

The source defines SEALED as preserving replay coordinates.

Closing Witness MUST preserve replay coordinates.

Replay coordinates identify the preserved observational state that later Replay
may reopen.

Closing coordinates != new Origin.

Replay coordinates != duplicate Room.

---

## 21. Return Coordinates

Closing preserves return coordinates through the Stick.

Return coordinates preserve analytical continuity and challengeability.

Return route != automatic rollback authority.

---

## 22. Cartography

Closing preserves Cartography.

Cartography retains:

- final operational position;
- unresolved terrain;
- Restriction / Constriction geometry;
- Collapse Boundaries;
- replay coordinates;
- return routes.

Closure != Cartography reset.

---

## 23. Stick

Closing MUST preserve the Stick.

The closed interval remains connected to:

- canonical Room identity;
- Origin;
- representation history;
- evidence lineage;
- provenance;
- Landing state;
- replay coordinate;
- return route.

Closing MUST NOT sever analytical continuity.

---

## 24. Representation State

When the message has landed, preserve object and representation state.

Closing Witness records the current representation.

Closure does not reset perspective, Zone, Space, or transform to defaults.

No default substitution.

Closed interval retains where it was observed from.

---

## 25. Natural Conversation

After closure, conversation may continue naturally.

Natural conversation does not require Room reconstruction.

Natural conversation does not require re-explanation of settled terrain.

Natural conversation does not authorize Reflight.

Conversation != analytical movement.

---

## 26. Do Not Rebuild The Room In Prose

The source explicitly prohibits rebuilding The Room in prose merely because the
conversation continues after convergence.

A Closing Witness preserves the structured state required for continuation.

Structured preservation replaces needless prose reconstruction.

No unnecessary rebuild.

No unnecessary re-analysis.

---

## 27. Audit

Audit verifies closing witnesses.

Every `CLOSED` Closing Witness MUST preserve an Audit witness reference.

Audit verifies closure integrity.

Audit does not own Room truth.

Audit verification != canonical promotion.

---

## 28. Registry

Registry remains responsible for lifecycle state and lineage.

Closing Witness supplies attributable evidence for a separately governed
lifecycle transition to SEALED where applicable.

Closing Witness creation alone MUST NOT silently mutate lifecycle state.

Closing Witness != Registry lifecycle transition.

---

## 29. SEALED

The source lifecycle defines `SEALED` as:

the current operational interval is closed with:

- Closing Witness;
- preserved lineage;
- replay coordinates.

R4-E provides the Closing Witness substrate.

R4-E does not reopen or rewrite R3-C lifecycle mechanics.

SEALED transition remains separately attributable to Registry.

---

## 30. REOPENED

The source lifecycle defines `REOPENED` as a sealed Room reopened at preserved
state because a valid Reflight Trigger exists.

R4-E does not implement REOPENED.

R4-E preserves what REOPENED will require:

- same Room identity;
- preserved state;
- Closing Witness;
- replay coordinates;
- Reflight Trigger lineage.

REOPENED remains downstream.

---

## 31. Governance

Governance constraints remain preserved at closure.

Closing does not erase:

- evidence obligations;
- claim ceilings;
- prohibited assumptions;
- Human Gate conditions;
- publication constraints;
- promotion conditions.

Closure != policy reset.

---

## 32. Human Gate

Human Gate remains ACTIVE.

Closing Witness does not fabricate approval.

Closing Witness does not imply promotion.

Closing Witness does not imply publication authority.

Closing Witness does not imply execution authority.

---

## 33. Publication Boundary

Closure remains upstream of:

Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate

Closing a Room interval does not publish it.

Closing Witness != publication record.

Closed != published.

---

## 34. Raven Boundary

Post-convergence response may later be rendered by Raven / The Unkindness.

R4-E does not define Raven rendering semantics.

Smallest sufficient response does not authorize Raven to alter analytical
meaning.

Closing Witness != rendering contract.

---

## 35. Replay Boundary

Closing Witness preserves replay coordinates and lineage.

R4-E does not implement Replay.

Replay reopens the same Room at a preserved observational coordinate.

Closing Witness != Replay Envelope.

R4-F owns Replay Envelope.

---

## 36. Scar Boundary

Closing Witness may preserve Scar references later where applicable.

R4-E does not define Scar Record.

R4-E does not define Scar Replay.

No Scar semantics pulled forward.

---

## 37. Failure Conditions

R4-E MUST reject:

- Closing Witness without Room identity;
- Closing Witness without Landing Witness;
- Closing Witness not bound to the same Room;
- CLOSED witness without preserved lineage;
- CLOSED witness without replay coordinates;
- CLOSED witness without Audit witness;
- CLOSED witness with active outstanding movement obligations;
- closure that erases unresolved terrain;
- closure that broadens evidence boundary;
- closure that raises evidence ceiling;
- closure that loses Restriction / Constriction history;
- closure that loses Collapse history;
- closure that resets representation state;
- closure that severs Stick continuity;
- acknowledgment used to authorize Reflight;
- celebration used to authorize Reflight;
- affect used to authorize Reflight;
- repetition used to authorize Reflight;
- conversational continuation used to authorize Reflight;
- closure treated as publication;
- closure treated as canonical promotion;
- closure treated as lifecycle mutation by witness alone;
- closure implemented as prose reconstruction.

---

## 38. R4-E Lock

After convergence, do not rebuild or re-explain the Room without a new
analytical trigger.

Importance does not authorize Reflight.

Emotion does not authorize Reflight.

Acknowledgment does not authorize Reflight.

Celebration does not authorize Reflight.

Laughter does not authorize Reflight.

Repetition of a settled point does not authorize Reflight.

When the message has landed: land.

Preserve object and representation state.

Remain naturally conversational.

Do not rebuild The Room in prose.

Prefer the smallest sufficient response.

Small response != compressed Room.

Closure preserves state.

Closure does not reconstruct state.

Closure does not delete state.

Closure does not promote state.

Closed interval != destroyed Room.

CLOSED != canonical promotion.

BLOCKED != analytical failure.

Close the interval.

Do not clone the object.

Landing first.

Closing Witness second.

Convergence != absolute truth.

Convergence != certainty.

Convergence != publication approval.

Closing Witness does not disable future Reflight.

Closing Witness does not manufacture a Reflight Trigger.

Closure now != never analyze again.

Unresolved terrain != outstanding movement obligation.

Closure does not convert unknown into known.

Closure does not convert inaccessible into absent.

Closed interval != higher evidence ceiling.

Closure does not flatten Collapse into a final summary.

Closure without lineage is incomplete.

Closing Witness MUST preserve replay coordinates.

Replay coordinates != duplicate Room.

Closure != Cartography reset.

Closing MUST preserve the Stick.

No default substitution.

Natural conversation does not require Room reconstruction.

Natural conversation does not authorize Reflight.

Conversation != analytical movement.

No unnecessary rebuild.

No unnecessary re-analysis.

Audit verifies closing witnesses.

Audit does not own Room truth.

Audit verification != canonical promotion.

Closing Witness creation alone MUST NOT silently mutate lifecycle state.

Closing Witness != Registry lifecycle transition.

SEALED transition remains separately attributable to Registry.

REOPENED remains downstream.

Closure != policy reset.

Closing Witness does not imply publication authority.

Closing Witness does not imply execution authority.

Closing a Room interval does not publish it.

Closed != published.

Closing Witness != rendering contract.

Closing Witness != Replay Envelope.

R4-F owns Replay Envelope.

No Replay semantics yet.

No Scar Record semantics yet.

No Scar Replay semantics yet.
