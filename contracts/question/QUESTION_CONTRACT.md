# R7-B — Question Contract

Status: CONTROLLED CANDIDATE
Ring: R7-B
Domain: DOCUMENTATION AND PROMOTION
Surface: QUESTION_CONTRACT
Version: vTemporal.41.0
Implementation Identity: v41 Complete
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

R7-B implements the native-v41 machine-readable Question Contract.

Recurring inquiries SHALL become version-controlled Question Contracts.

Humans and machines may execute the same Question Contract without semantic
change.

Issuing a Question Contract SHALL NOT mutate analytical state.

Question Contract != write operation.

Question Contract != authority.

---

## 1. Contract Role

A Question Contract defines a reproducible inquiry against a governed analytical
object.

It binds:

- question;
- scope;
- time;
- included analytical objects;
- required artifacts;
- exclusions;
- evidence thresholds;
- evidence boundary;
- evidence ceiling;
- audience;
- rendering requirements;
- personalization policy;
- decision-option requirements;
- Human Gate requirements;
- provenance.

It does not create analytical truth.

It does not create evidence.

It does not create authority.

---

## 2. Identity

Every Question Contract SHALL preserve:

- question_contract_id;
- version.

question_contract_id is deterministic SHA-512 identity over material contract
content.

Same material contract + same version -> same identity.

Material semantic change requires a new version.

Hash != truth.

Hash != authority.

---

## 3. Question

Every contract SHALL contain a non-empty question.

Question != conclusion.

Question wording does not change object identity.

Question wording does not broaden evidence access.

Question wording does not raise the evidence ceiling.

---

## 4. Scope

A Question Contract SHALL declare exactly one scope type:

- ROOM;
- ZONE;
- TERRITORY.

The contract SHALL preserve:

- room_object_id;
- room_revision_id;
- scope_reference.

Scope != new object.

Zone != new Room.

Territory != new Room.

Scope declaration != evidence expansion.

---

## 5. Temporal Window

Supported temporal modes:

- CURRENT;
- HISTORICAL;
- BOUNDED_RANGE.

BOUNDED_RANGE requires valid start and end timestamps.

HISTORICAL requires either:

- historical_reference;
- or a valid bounded historical range.

Historical inquiry != Replay automatically.

Time window != new Room.

---

## 6. Included Analytical Objects

The contract may identify included analytical objects.

Included reference != object creation.

Question execution SHALL NOT silently expand the included-object set.

---

## 7. Required Artifacts

The contract may identify required artifacts.

Missing required artifact SHALL NOT be silently fabricated.

Required artifact != evidence truth.

---

## 8. Exclusions

The contract SHALL preserve explicit exclusions.

Excluded != absent.

Restricted != nonexistent.

Rendering omission MUST NOT erase the existence of excluded or restricted
material.

---

## 9. Evidence Thresholds

Evidence thresholds constrain inquiry execution.

Thresholds do not create evidence.

Threshold satisfied != truth authority.

Threshold unmet MUST NOT be silently normalized to satisfied.

---

## 10. Evidence Boundary

Every Question Contract SHALL preserve an evidence_boundary_reference.

Question execution MUST remain within the governed evidence boundary.

A Question Contract cannot broaden the evidence boundary merely by asking for
more.

Question != evidence expansion.

---

## 11. Evidence Ceiling

Every Question Contract SHALL preserve an evidence_ceiling_reference.

Question execution MUST NOT raise the evidence ceiling.

Audience choice MUST NOT raise the evidence ceiling.

Rendering choice MUST NOT raise the evidence ceiling.

Decision-option requirements MUST NOT raise the evidence ceiling.

Question != claim authority.

---

## 12. Audience

Audience may affect representation.

Audience MUST NOT alter:

- evidence;
- identity;
- provenance;
- boundary;
- ceiling;
- analytical meaning.

Audience != truth frame.

---

## 13. Rendering

A Question Contract may specify rendering_format.

Rendering may change presentation.

Rendering MUST NOT change analytical meaning.

Rendering != analysis.

Rendering != evidence mutation.

---

## 14. Personalization

Supported personalization policies:

- ALLOWED;
- DISABLED;
- MEETING_MODE.

Personalization belongs at the point of consumption.

Personalization MUST NOT change canonical meaning.

MEETING_MODE MUST NOT require re-analysis.

---

## 15. Decision Options

A Question Contract may request decision-option output.

Decision option != decision.

Decision-option requirements MUST preserve:

- uncertainty;
- evidence lineage;
- evidence boundary;
- evidence ceiling;
- Human Gate.

The system prepares options.

Human Gate decides.

---

## 16. Read-Only Invariant

Every native Question Contract SHALL preserve:

read_only = true

Every native Question Contract SHALL preserve:

write_operation_requested = false

The contract, query, and rendering are read-only unless a separately authorized
write operation passes Human Gate.

A Question Contract cannot grant itself write authority.

Question Contract != action contract.

---

## 17. Human / Machine Equivalence

Executor type may be:

- HUMAN;
- MACHINE.

Executor type MUST NOT change contract semantics.

The same contract executed by a human or machine SHALL preserve identical:

- identity;
- version;
- question;
- scope;
- temporal window;
- included objects;
- artifacts;
- exclusions;
- thresholds;
- evidence boundary;
- evidence ceiling;
- audience;
- rendering;
- personalization;
- decision-option requirements;
- read-only state;
- provenance;
- Human Gate requirements.

Executor != semantic mutation.

---

## 18. Reproducibility

Questions become version-controlled.

Renderings become reproducible.

Same Question Contract + same eligible Room state + same evidence state + same
renderer version SHALL preserve the same semantic inquiry envelope.

Reproducibility != identical prose.

---

## 19. Replay Boundary

Question Contract != Replay Envelope.

Replay may preserve and reuse the historical Question Contract reference.

Historical Question Contract reference does not itself reopen historical state.

Replay remains governed by Replay semantics.

---

## 20. Provenance

Every Question Contract SHALL preserve provenance_route.

Provenance SHALL remain attributable.

Missing provenance blocks valid Question Contract state.

Provenance != endorsement.

---

## 21. Human Gate

Human Gate remains ACTIVE.

Ordinary read-only inquiry does not require authority promotion.

A separately requested write or external action remains outside the Question
Contract and requires its own authorization path.

Human Gate state MUST NOT be disabled by Question Contract execution.

---

## 22. Validation

R7-B dispositions:

- VALID;
- BLOCKED.

VALID means the Question Contract preserves all required inquiry semantics and
read-only boundaries.

VALID != answered.

VALID != true.

VALID != promoted.

---

## 23. Failure Reasons

R7-B recognizes:

- CONTRACT_IDENTITY_INVALID;
- VERSION_INVALID;
- QUESTION_MISSING;
- SCOPE_INVALID;
- ROOM_IDENTITY_MISSING;
- ROOM_REVISION_MISSING;
- SCOPE_REFERENCE_MISSING;
- TEMPORAL_WINDOW_INVALID;
- HISTORICAL_REFERENCE_MISSING;
- BOUNDED_RANGE_INVALID;
- EVIDENCE_BOUNDARY_MISSING;
- EVIDENCE_CEILING_MISSING;
- PERSONALIZATION_POLICY_INVALID;
- PROVENANCE_MISSING;
- READ_ONLY_VIOLATED;
- WRITE_OPERATION_EMBEDDED;
- HUMAN_GATE_DISABLED;
- SEMANTIC_VERSION_DRIFT;
- EXECUTOR_SEMANTIC_DRIFT;
- AUTHORITY_PROMOTED.

Failure reasons accumulate.

No Compression Out applies.

---

## 24. Machine-Readable Fields

The Question Contract SHALL preserve:

- schema_version;
- question_contract_id;
- version;
- question;
- scope;
- temporal_window;
- included_analytical_objects;
- required_artifacts;
- exclusions;
- evidence_thresholds;
- evidence_boundary_reference;
- evidence_ceiling_reference;
- audience;
- rendering_format;
- personalization_policy;
- decision_option_requirements;
- read_only;
- write_operation_requested;
- human_gate_requirements;
- provenance_route;
- authority_state;
- human_gate_state;
- validation_disposition;
- failure_reasons.

---

## 25. R7-B Lock

R7-B = Question Contract.

Recurring inquiries SHALL be version-controlled Question Contracts.

Humans and machines may execute the same Question Contract without semantic
change.

Issuing a Question Contract SHALL NOT mutate analytical state.

Question Contract != write operation.

Question Contract != authority.

Question != conclusion.

Scope != new object.

Scope declaration != evidence expansion.

Historical inquiry != Replay automatically.

Included reference != object creation.

Required artifact != evidence truth.

Excluded != absent.

Restricted != nonexistent.

Threshold satisfied != truth authority.

Question != evidence expansion.

Question != claim authority.

Audience != truth frame.

Rendering != analysis.

Personalization belongs at the point of consumption.

MEETING_MODE MUST NOT require re-analysis.

Decision option != decision.

Human Gate decides.

read_only = true.

write_operation_requested = false.

A Question Contract cannot grant itself write authority.

Question Contract != action contract.

Executor != semantic mutation.

Questions become version-controlled.

Renderings become reproducible.

Reproducibility != identical prose.

Question Contract != Replay Envelope.

Provenance != endorsement.

Human Gate state MUST NOT be disabled by Question Contract execution.

VALID != answered.

VALID != true.

VALID != promoted.

Authority remains NONE.

Human Gate remains ACTIVE.

Promotion State remains CANDIDATE.

R7-C owns README / Version Authority / Native-v41 Entry Surfaces.
