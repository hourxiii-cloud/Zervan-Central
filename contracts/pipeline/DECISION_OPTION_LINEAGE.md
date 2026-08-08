# R5-G — Decision Option Lineage

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R5-G
Version: vTemporal.41.0
Promotion State: CANDIDATE
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

R5-G defines native-v41 Decision Option Lineage.

A decision option is a bounded, attributable possible course presented for
human consideration.

Decision option != decision.

Decision option != authority.

Decision option != approval.

Decision option != execution.

---

## 1. Pipeline Position

Native-v41 sequence remains:

Evidence
-> PMC
-> CCR
-> MC
-> Raven
-> Human Gate

Decision options are downstream analytical / reporting artifacts.

They do not become a new truth-producing pipeline stage.

A decision option MUST bind back through:

Raven
-> MC
-> CCR
-> PMC
-> Room-Bound Evidence

Option lineage MUST NOT begin at Raven alone.

---

## 2. Source Requirement

Every decision option MUST identify an attributable Raven representation.

That Raven representation MUST remain traceable to:

- MC evaluation;
- CCR;
- PMC analytical state;
- PMC intake;
- Room-bound evidence;
- canonical Room identity;
- provenance.

Decision option lineage is end-to-end lineage.

---

## 3. Room Identity

Every decision option MUST preserve the canonical Room Object identity.

An option does not create a new Room.

Alternative course != alternate Room.

Different recommendation != different Room.

Option variation != object variation.

---

## 4. Revision / State / Authorized View

A decision option MUST preserve:

- Room revision identity;
- Room state root;
- Authorized View Root.

The option MUST NOT assume evidence outside the bound Authorized View.

Decision option generation != access expansion.

---

## 5. Evidence Boundary

A decision option MUST remain inside the evidence boundary inherited from the
upstream pipeline.

The option MUST NOT rely on evidence not admitted upstream.

Possible action != permission to invent supporting evidence.

Option desirability does not widen evidence.

---

## 6. Evidence Ceiling

A decision option MUST remain inside the Maximum Justified Claim.

The option MUST NOT:

- convert correlation into causation;
- convert candidate classification into proof;
- convert analysis into compliance;
- convert uncertainty into certainty;
- convert MC admissibility into factual truth.

Decision utility != higher claim ceiling.

---

## 7. MC Admissibility

Every decision option MUST identify the MC response/output class to which it is
bound.

An option MUST NOT be presented as available when its MC disposition is
`INADMISSIBLE`.

A `CONDITIONAL` option MUST preserve all required conditions.

An `ADMISSIBLE` option remains merely admissible.

Admissible option != approved option.

---

## 8. Raven Representation

Raven may represent decision options.

Raven may change:

- wording;
- density;
- ordering;
- audience;
- presentation form.

Raven MUST NOT alter:

- option lineage;
- MC disposition;
- conditions;
- evidence boundary;
- evidence ceiling;
- Room identity;
- uncertainty;
- provenance.

Presentation ordering != decision ranking.

---

## 9. Option Description

Each decision option MUST describe one bounded possible course.

The description MUST NOT imply:

- mandatory execution;
- Human Gate approval;
- legal conclusion;
- compliance conclusion;
- certification;
- factual certainty beyond upstream support.

Option description != directive.

---

## 10. Option Status

Native R5-G defines:

- `AVAILABLE`;
- `CONDITIONAL`;
- `UNAVAILABLE`;
- `BLOCKED`.

`AVAILABLE` requires an upstream MC disposition of `ADMISSIBLE`.

`CONDITIONAL` requires an upstream MC disposition of `CONDITIONAL` and explicit
conditions.

`UNAVAILABLE` corresponds to upstream `INADMISSIBLE`.

`BLOCKED` means the option cannot be defensibly constructed because lineage or
required state is incomplete.

AVAILABLE != approved.

CONDITIONAL != approved.

UNAVAILABLE != nonexistent.

BLOCKED != false analysis.

---

## 11. No Automatic Ranking

R5-G does not require a preferred option.

Options MAY be ordered for presentation.

Presentation order MUST NOT silently become analytical rank or authority.

First option != recommended option.

Last option != rejected option.

No hidden default winner.

---

## 12. Recommendation Boundary

A representation may explicitly label an option as recommended only if that
recommendation is attributable to an upstream bounded analytical/reporting
record that supports such wording.

Recommendation != decision.

Recommendation != approval.

Recommendation != execution.

R5-G does not manufacture recommendation authority.

---

## 13. Human Gate Relationship

Decision options may be presented before Human Gate review.

Human Gate evaluates authority-bearing movement separately.

A Human Gate approval MUST reference the exact option or exact transition state
being approved where applicable.

Approval of one option MUST NOT silently approve another option.

Prior Human Gate approval MUST NOT silently carry forward to a materially changed
option.

---

## 14. Option Change

A material change to any of the following creates a materially changed option:

- proposed course;
- MC disposition;
- required conditions;
- Raven representation binding;
- Room revision;
- Room state root;
- Authorized View Root;
- evidence boundary;
- evidence ceiling;
- coordinate;
- upstream lineage.

A materially changed option requires a new deterministic option identity.

Changed option != previously approved option.

---

## 15. Coordinate Continuity

Decision options MUST preserve the applicable observational coordinate.

Option generation does not move the analytical object.

Decision option does not own Cartography.

Coordinate reference != Cartography ownership.

---

## 16. Uncertainty

Decision options MUST preserve uncertainty material to the proposed course.

An option MUST NOT erase unknowns merely to appear actionable.

Unknown remains unknown.

Conditional knowledge remains conditional.

Actionability != certainty.

---

## 17. Conditions

Every conditional option MUST preserve its required conditions exactly enough to
remain attributable.

A conditional option without conditions is invalid.

Conditions MUST NOT be silently converted into explanatory footnotes that no
longer constrain the option.

Condition != decoration.

---

## 18. Inadmissible / Unavailable Options

An MC-inadmissible option may be retained as `UNAVAILABLE` when useful for
explanation or audit.

Unavailable options MUST preserve their inadmissibility reason.

An unavailable option MUST NOT be rendered as executable.

Unavailable != deleted.

Unavailable != recommended.

---

## 19. Lineage Record

Every native Decision Option Lineage record MUST preserve:

- `decision_option_id`;
- `option_label`;
- `option_description`;
- `option_status`;
- `object_id`;
- `room_revision_id`;
- `room_state_root`;
- `authorized_view_root`;
- `coordinate_reference`;
- `evidence_boundary_reference`;
- `evidence_ceiling_reference`;
- `pmc_intake_binding_id`;
- `pmc_run_id`;
- `ccr_id`;
- `mc_evaluation_id`;
- `mc_response_class`;
- `mc_disposition`;
- `required_conditions`;
- `inadmissibility_reasons`;
- `raven_representation_id`;
- `human_gate_decision_reference`;
- `uncertainty_references`;
- `lineage_reference`;
- `provenance_route`;
- `authority_state`;
- `human_gate_state`.

---

## 20. Human Gate Decision Reference

A decision option may exist before a Human Gate decision.

Therefore `human_gate_decision_reference` may be null.

Null Human Gate decision reference means:

no Human Gate decision has been bound to this option.

Null != denied.

Null != approved.

If a Human Gate decision reference is present, the option does not inherit more
authority than that exact decision grants.

---

## 21. Deterministic Identity

Decision option identity MUST be deterministic over the attributable option
state.

Equivalent option state MUST produce the same option identity.

Materially changed option state MUST produce a different option identity.

No random identifiers.

No hidden defaults.

No timestamp participates in identity unless it is an attributable material
input.

---

## 22. Authority Boundary

Decision option != decision authority.

Decision option != Human Gate approval.

Decision option != execution.

Decision option != publication authority.

Decision option != canonical promotion.

Authority remains NONE.

Human Gate remains ACTIVE.

---

## 23. No Compression Out

A decision option MUST NOT compress away independently relevant:

- evidence lineage;
- MC disposition;
- required conditions;
- inadmissibility reasons;
- uncertainty;
- evidence boundary;
- evidence ceiling;
- Room identity;
- coordinate;
- Raven binding;
- Human Gate state;
- provenance.

Short option text may reference those structures.

Reference != erasure.

---

## 24. Failure Conditions

R5-G MUST reject:

- missing Room identity;
- missing PMC intake lineage;
- missing PMC run;
- missing CCR;
- missing MC evaluation;
- missing Raven representation;
- missing evidence boundary;
- missing evidence ceiling;
- missing coordinate;
- AVAILABLE option not backed by MC ADMISSIBLE;
- CONDITIONAL option not backed by MC CONDITIONAL;
- CONDITIONAL option without conditions;
- UNAVAILABLE option not backed by MC INADMISSIBLE;
- MC-inadmissible option presented as AVAILABLE;
- silent evidence expansion;
- silent claim-ceiling promotion;
- unknown erased into certainty;
- option treated as Human Gate approval;
- option treated as execution;
- material option change retaining old identity;
- loss of lineage;
- loss of provenance.

Fail closed.

Do not manufacture a preferred decision.

---

## 25. R5-G Lock

Decision option != decision.

Decision option != authority.

Decision option != approval.

Decision option != execution.

Decision options are downstream analytical / reporting artifacts.

They do not become a new truth-producing pipeline stage.

Option lineage MUST NOT begin at Raven alone.

Decision option lineage is end-to-end lineage.

An option does not create a new Room.

Alternative course != alternate Room.

Decision option generation != access expansion.

Possible action != permission to invent supporting evidence.

Decision utility != higher claim ceiling.

An option MUST NOT be presented as available when its MC disposition is
INADMISSIBLE.

Admissible option != approved option.

Presentation ordering != decision ranking.

Option description != directive.

AVAILABLE != approved.

CONDITIONAL != approved.

UNAVAILABLE != nonexistent.

BLOCKED != false analysis.

First option != recommended option.

Last option != rejected option.

No hidden default winner.

Recommendation != decision.

Recommendation != approval.

Recommendation != execution.

Approval of one option MUST NOT silently approve another option.

Changed option != previously approved option.

Decision option does not own Cartography.

Coordinate reference != Cartography ownership.

Actionability != certainty.

A conditional option without conditions is invalid.

Condition != decoration.

Unavailable != deleted.

Unavailable != recommended.

Null != denied.

Null != approved.

Decision option != decision authority.

Decision option != Human Gate approval.

Decision option != execution.

Decision option != publication authority.

Decision option != canonical promotion.

Authority remains NONE.

Human Gate remains ACTIVE.

Reference != erasure.

Fail closed.

Do not manufacture a preferred decision.

R5-H owns Report / Rendering Contract.
