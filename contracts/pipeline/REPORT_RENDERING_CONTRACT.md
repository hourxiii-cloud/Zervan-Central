# R5-H — Report / Rendering Contract

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R5-H
Version: vTemporal.41.0
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

R5-H defines the native-v41 Report / Rendering Contract.

A report is a bounded rendering of attributable analytical state.

Report != analytical state.

Report != truth authority.

Report != publication authority.

Report != certification.

Rendering != mutation.

---

## 1. Pipeline Position

Native-v41 evidence-to-publication sequence remains:

Evidence
-> PMC
-> CCR
-> MC
-> Raven
-> Human Gate

Report/rendering is a representation surface over attributable pipeline state.

R5-H does not create a new truth-producing pipeline stage.

R5-H does not replace Raven.

R5-H does not replace Human Gate.

---

## 2. Report Source

Every report MUST bind to an attributable Raven representation.

Where applicable, the report MUST preserve lineage to:

- Decision Option records;
- Human Gate transition decisions;
- MC evaluation;
- CCR;
- PMC state;
- Room-bound evidence.

A report MUST NOT begin its lineage at rendered prose alone.

Rendered text is not source-of-truth.

---

## 3. Canonical Room Identity

Every report MUST preserve the canonical Room Object identity of the analytical
state being rendered.

A report does not create a new Room.

PDF != new Room.

JSON != new Room.

Markdown != new Room.

Audience-specific rendering != new Room.

Report copy != analytical clone.

---

## 4. Revision / State / Authorized View

Every report MUST preserve applicable:

- Room revision identity;
- Room state root;
- Authorized View Root.

The report MUST NOT silently use a broader Authorized View than its source
representation.

Rendering != access expansion.

Export != authorization expansion.

---

## 5. Evidence Boundary

Every report MUST preserve the evidence boundary applicable to its source state.

The renderer MUST NOT add evidence.

The renderer MUST NOT silently consume external material to improve the report.

Formatting source material != admitting new evidence.

Presentation convenience != evidence admission.

---

## 6. Evidence Ceiling

Every report MUST preserve the evidence ceiling / Maximum Justified Claim.

The renderer MUST NOT increase claim strength for:

- executive readability;
- persuasive effect;
- brevity;
- visual polish;
- audience preference;
- chart formatting;
- narrative flow.

Better presentation != stronger evidence.

Rendered confidence != higher claim ceiling.

---

## 7. Representation Transform

A report may transform representation.

Permitted rendering transforms may include:

- format;
- layout;
- section ordering;
- typography instructions;
- table representation;
- chart representation;
- audience profile;
- density;
- language;
- machine-readable serialization.

Every transform MUST remain attributable.

Rendering transform != analytical transform.

---

## 8. Meaning Preservation

A rendering MUST preserve upstream analytical meaning.

The renderer MUST NOT alter:

- evidence;
- Room identity;
- Room geometry;
- coordinate meaning;
- upstream transform history;
- PMC result;
- CCR state;
- MC disposition;
- Raven finding classification;
- uncertainty;
- decision-option status;
- Human Gate state;
- evidence boundary;
- evidence ceiling;
- provenance.

Presentation may change.

Supported meaning may not.

---

## 9. Observed / Inferred / Unknown

Reports MUST preserve the distinction among:

- `OBSERVED`;
- `INFERRED`;
- `UNKNOWN`.

A renderer MUST NOT promote:

- inferred -> observed;
- unknown -> inferred;
- unknown -> observed.

Unknown != false.

Unknown != omission permission.

---

## 10. MC Admissibility

A report containing response/output classes MUST preserve the upstream MC
disposition.

The report MUST preserve applicable:

- `ADMISSIBLE`;
- `CONDITIONAL`;
- `INADMISSIBLE`;
- required conditions;
- inadmissibility reasons.

Conditional MUST NOT render as approved.

Inadmissible MUST NOT render as recommended.

Admissible MUST NOT render as authorized.

---

## 11. Decision Options

A report may contain Decision Option records.

The report MUST preserve option status:

- `AVAILABLE`;
- `CONDITIONAL`;
- `UNAVAILABLE`;
- `BLOCKED`.

Rendering order MUST NOT silently become analytical rank.

First displayed option != preferred option.

Visual emphasis != decision authority.

---

## 12. Human Gate State

Where a report includes authority-bearing transition state, it MUST preserve the
Human Gate decision exactly as attributable:

- `PENDING`;
- `APPROVED`;
- `DENIED`.

PENDING MUST NOT render as likely approval.

APPROVED MUST NOT render as execution completed.

DENIED MUST NOT render as false analysis.

Rendering Human Gate state != changing Human Gate state.

---

## 13. Publication State

A report may be:

- drafted;
- rendered;
- publication-ready;
- publication-approved where separately bound.

R5-H does not itself publish.

Rendered != published.

Publication-ready != published.

Publication-ready != approved.

Report existence != publication.

---

## 14. Report Classes

Native R5-H recognizes report classes including:

- `HUMAN_READABLE`;
- `STRUCTURED`;
- `EXECUTIVE`;
- `TECHNICAL`;
- `AUDIT`;
- `GOVERNANCE`;
- `DECISION_SUPPORT`.

A report may carry more than one audience characteristic through its rendering
profile.

Report class changes presentation obligations.

Report class does not change analytical truth.

---

## 15. Human-Readable Report

Human-readable reports may include:

- executive summary;
- findings;
- evidence / trace references;
- stability / coherence state;
- uncertainty / unknowns;
- MC-admissible response classes;
- conditional requirements;
- explicitly inadmissible actions;
- Decision Options;
- Human Gate state where applicable.

Human-readable != less attributable.

Readable != compressed out.

---

## 16. Structured Report

Structured reports MUST preserve machine-addressable lineage.

A structured report MUST include identifiers sufficient to bind back to
applicable source state.

Structured serialization does not create a second analytical object.

JSON identity != Room identity.

Serialization != canonical promotion.

---

## 17. Trace Map

Every material report claim MUST preserve traceability.

The trace map MUST bind output claims to attributable upstream references.

Traceability may include:

- Room-bound evidence;
- PMC intake;
- PMC output;
- CCR;
- MC evaluation;
- Raven representation;
- Decision Option;
- Human Gate decision;
- relevant qualification / runtime / observer records.

A material claim without trace is invalid unless explicitly rendered as unknown.

Trace map != certification.

---

## 18. Findings

Every material finding MUST preserve:

- finding identifier;
- classification;
- source reference(s);
- applicable uncertainty;
- applicable evidence boundary / ceiling.

A renderer MUST NOT silently merge materially distinct findings.

Similar findings != same finding.

Summary grouping MUST preserve individual traceability.

---

## 19. Unknowns

Material unknowns MUST remain visible.

A report MUST NOT remove unknowns simply because:

- the audience is executive;
- the document is short;
- the renderer prefers a cleaner story;
- a conclusion is inconvenient;
- the unknown weakens recommendation language.

No Compression Out applies to unknowns.

---

## 20. Conditional State

Conditional analytical or governance state MUST remain conditional.

Conditions MUST remain attributable and visible enough to constrain downstream
interpretation.

Footnote placement MUST NOT erase operational significance.

Condition != decoration.

---

## 21. Inadmissible State

Inadmissible state may be rendered for explanation, governance, or audit.

Inadmissible state MUST remain clearly distinguishable from allowed or
recommended state.

Showing inadmissible state != endorsing it.

Omission of inadmissible state is allowed only when the report contract and
Authorized View permit omission without changing material meaning.

---

## 22. Redaction

A report may redact restricted material when required by its Authorized View or
governance constraint.

Redaction MUST remain existence-aware.

Restricted content MUST NOT silently become nonexistent.

A redaction marker may preserve:

- existence;
- restricted status;
- source reference;
- reason / governing reference.

Redaction != deletion.

Restricted != absent.

---

## 23. Coordinate / Cartography

Reports may render Room coordinates and Cartography.

Reports do not own Cartography.

Visual layout MUST NOT silently change coordinate meaning.

Map rotation != Room mutation.

Chart axis selection != evidence mutation.

Coordinate rendering != spatial truth authority.

---

## 24. Charts / Tables / Visual Encoding

Visual encoding MUST remain faithful to source state.

A chart or table MUST NOT:

- omit material categories to manufacture a trend;
- alter scale to imply unsupported magnitude;
- merge unknown with zero;
- merge unavailable with absent;
- convert conditional into affirmative;
- visually rank Decision Options without an attributable ranking source.

Visualization != new analysis.

Aesthetic emphasis != evidence.

---

## 25. Determinism

Given equivalent source state and equivalent rendering profile, report content
MUST be semantically equivalent.

Structured field ordering and governed section ordering SHOULD remain stable.

No random fact selection.

No hidden truth changes by audience.

Different formatting may preserve identical supported meaning.

Semantic equivalence != byte identity.

---

## 26. Report Identity

Every native report rendering record MUST have a deterministic `report_id`.

Material changes to the report binding MUST change report identity.

Material changes include:

- source Raven representation;
- Decision Option references;
- Human Gate decision reference;
- Room revision/state/view;
- evidence boundary;
- evidence ceiling;
- rendering profile;
- report class;
- material claim set;
- trace map;
- redaction state.

Cosmetic byte changes MAY leave the underlying analytical state unchanged.

Report identity != Room identity.

Report identity != truth.

---

## 27. Required Report Binding

Every native R5-H report record MUST preserve:

- `report_id`;
- `report_class`;
- `rendering_profile`;
- `raven_representation_id`;
- `decision_option_references`;
- `human_gate_decision_reference`;
- `object_id`;
- `room_revision_id`;
- `room_state_root`;
- `authorized_view_root`;
- `evidence_boundary_reference`;
- `evidence_ceiling_reference`;
- `coordinate_reference`;
- `findings`;
- `unknowns`;
- `mc_response_class_results`;
- `trace_map`;
- `redaction_references`;
- `lineage_reference`;
- `provenance_route`;
- `report_status`;
- `publication_state`;
- `authority_state`;
- `human_gate_state`.

---

## 28. Report Status

Native R5-H recognizes:

- `OK`;
- `DEGRADED`;
- `FAILED_TRACEABILITY`;
- `INSUFFICIENT_EVIDENCE`;
- `BLOCKED`.

`OK` means the report satisfies its rendering contract.

`DEGRADED` means the report remains valid with explicitly preserved limitations.

`FAILED_TRACEABILITY` means material claims cannot be defensibly traced.

`INSUFFICIENT_EVIDENCE` means the requested rendering cannot support the
requested content.

`BLOCKED` means rendering is prohibited or impossible under governing state.

OK != approved.

DEGRADED != false.

BLOCKED != nonexistent report request.

---

## 29. Publication State

Native R5-H recognizes:

- `DRAFT`;
- `RENDERED`;
- `PUBLICATION_READY`;
- `PUBLICATION_APPROVED`.

`PUBLICATION_APPROVED` requires an attributable Human Gate decision reference.

PUBLICATION_APPROVED != published.

RENDERED != publication approval.

DRAFT != analytically invalid.

---

## 30. Human Gate Binding

If `publication_state` is `PUBLICATION_APPROVED`, the report MUST bind to an
attributable Human Gate approval for the exact material report state.

A Human Gate approval for a different report identity MUST NOT silently carry
forward.

Changed report != previously approved report.

Prior approval != standing publication approval.

---

## 31. Authority Boundary

A report does not create:

- execution authority;
- publication authority;
- certification authority;
- compliance truth;
- legal truth;
- canonical promotion;
- Room mutation.

Authority remains NONE.

Human Gate remains ACTIVE.

Report validation != authority.

Render success != authority.

---

## 32. No Compression Out

Rendering may compress presentation density.

Rendering MUST NOT compress away independently meaningful:

- evidence;
- findings;
- uncertainty;
- unknowns;
- MC dispositions;
- conditions;
- inadmissibility reasons;
- Decision Option statuses;
- Human Gate state;
- evidence boundary;
- evidence ceiling;
- Room identity;
- coordinates;
- redaction existence markers;
- lineage;
- provenance.

Summary != erasure.

Compact != incomplete truth lineage.

---

## 33. Failure Conditions

R5-H MUST reject:

- missing Raven representation;
- missing Room identity;
- missing revision/state/view;
- missing evidence boundary;
- missing evidence ceiling;
- missing coordinate;
- unsupported material finding;
- material claim without trace;
- unknown promoted to fact;
- MC disposition altered by rendering;
- conditional state rendered as unconditional;
- inadmissible state rendered as recommended;
- Decision Option status altered;
- presentation order treated as decision rank;
- Human Gate state altered;
- PUBLICATION_APPROVED without attributable Human Gate approval;
- prior approval reused after material report change;
- redacted content treated as nonexistent;
- report identity treated as Room identity;
- report treated as certification;
- report treated as truth authority;
- report treated as execution authority;
- provenance loss;
- lineage loss.

Fail closed.

Do not improve analytical meaning through rendering.

---

## 34. R5-H Lock

A report is a bounded rendering of attributable analytical state.

Report != analytical state.

Report != truth authority.

Report != publication authority.

Report != certification.

Rendering != mutation.

R5-H does not create a new truth-producing pipeline stage.

Rendered text is not source-of-truth.

A report does not create a new Room.

PDF != new Room.

JSON != new Room.

Markdown != new Room.

Audience-specific rendering != new Room.

Report copy != analytical clone.

Rendering != access expansion.

Export != authorization expansion.

Formatting source material != admitting new evidence.

Presentation convenience != evidence admission.

Better presentation != stronger evidence.

Rendered confidence != higher claim ceiling.

Rendering transform != analytical transform.

Presentation may change.

Supported meaning may not.

Unknown != false.

Unknown != omission permission.

Conditional MUST NOT render as approved.

Inadmissible MUST NOT render as recommended.

Admissible MUST NOT render as authorized.

Rendering order MUST NOT silently become analytical rank.

First displayed option != preferred option.

Visual emphasis != decision authority.

PENDING MUST NOT render as likely approval.

APPROVED MUST NOT render as execution completed.

DENIED MUST NOT render as false analysis.

Rendered != published.

Publication-ready != published.

Publication-ready != approved.

Report existence != publication.

Report class does not change analytical truth.

Human-readable != less attributable.

Readable != compressed out.

JSON identity != Room identity.

Serialization != canonical promotion.

Trace map != certification.

Similar findings != same finding.

Summary grouping MUST preserve individual traceability.

No Compression Out applies to unknowns.

Condition != decoration.

Showing inadmissible state != endorsing it.

Restricted content MUST NOT silently become nonexistent.

Redaction != deletion.

Restricted != absent.

Reports do not own Cartography.

Visualization != new analysis.

Aesthetic emphasis != evidence.

Semantic equivalence != byte identity.

Report identity != Room identity.

Report identity != truth.

OK != approved.

DEGRADED != false.

PUBLICATION_APPROVED != published.

Changed report != previously approved report.

Prior approval != standing publication approval.

Authority remains NONE.

Human Gate remains ACTIVE.

Report validation != authority.

Render success != authority.

Summary != erasure.

Compact != incomplete truth lineage.

Fail closed.

Do not improve analytical meaning through rendering.

R5-I owns Pipeline Cross-Stage Integrity / No-Responsibility-Absorption.
