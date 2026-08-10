# AC-10 — Evidence-Ceiling Semantic Enforcement

Status: CONTROLLED CANDIDATE CONTRACT
Activation Control: AC-10
Version: vTemporal.41.0
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

AC-10 defines semantic enforcement of the evidence ceiling.

An evidence-ceiling field is not sufficient evidence that a claim obeys the
ceiling.

A claim is admissible only when the meaning of the claim remains within the
strongest claim justified by attributable evidence under the governing
evidence ceiling.

Metadata agreement is necessary but insufficient.

Evidence ceiling constrains claim meaning.

---

## 1. Governing Invariant

For every material analytical or rendered claim:

semantic claim strength
<=
maximum justified claim under attributable evidence.

The comparison MUST account for more than an evidence-ceiling reference.

It MUST account for applicable:

- assertion strength;
- support state;
- causal posture;
- uncertainty;
- surviving alternatives;
- temporal attribution;
- evidence provenance;
- integrity/truth distinction;
- historical versus current evidence state.

A structurally valid claim that semantically exceeds its evidence is invalid.

---

## 2. Semantic Claim State

AC-10 requires material claims to expose sufficient structured semantics for
deterministic admissibility evaluation.

At minimum a semantic claim state MUST preserve:

- claim identifier;
- subject;
- predicate;
- object or value;
- polarity;
- assertion strength;
- support state;
- causal posture;
- uncertainty state;
- surviving alternatives where material;
- temporal scope;
- evidence references;
- evidence-boundary reference;
- evidence-ceiling reference;
- provenance references;
- source analytical-state reference.

Free-form prose MAY accompany the structured claim.

Free-form prose MUST NOT replace the structured semantic state.

---

## 3. Assertion Strength

Assertion strength MUST be explicit and ordered.

Native AC-10 recognizes the following ordered strength classes:

1. `OBSERVATION`
2. `POSSIBLE`
3. `PLAUSIBLE`
4. `PROBABLE`
5. `ESTABLISHED`

A downstream claim MUST NOT increase assertion strength without a separately
attributable evidentiary state supporting the stronger class.

Presentation preference does not justify promotion.

Confidence wording does not override the evidence ceiling.

---

## 4. Support State

Support state remains independent from assertion strength.

AC-10 preserves support states including:

- `SUPPORTED`;
- `PARTIALLY_SUPPORTED`;
- `CONTRADICTED`;
- `UNRESOLVED`;
- `RETRACTED`;
- `UNKNOWN`.

Reporting MUST NOT convert:

- PARTIALLY_SUPPORTED -> SUPPORTED;
- CONTRADICTED -> SUPPORTED;
- UNRESOLVED -> SUPPORTED;
- UNKNOWN -> SUPPORTED

without a separately attributable analytical transition supported by evidence.

Support-state preservation alone does not authorize stronger prose.

---

## 5. Causal Posture

Causal posture MUST be explicit where a claim expresses or implies
relationship strength.

AC-10 recognizes:

- `NONE`;
- `ASSOCIATION`;
- `CORRELATION`;
- `CONTRIBUTORY`;
- `CAUSAL`.

A claim bounded to association or correlation MUST NOT be rendered as causal.

Correlation != causation.

Temporal ordering != causation.

High confidence != causation.

Cryptographic integrity != causation.

---

## 6. Uncertainty Preservation

Material uncertainty is part of claim meaning.

A downstream transformation MUST preserve applicable:

- unresolved alternatives;
- contradictory evidence;
- missing evidence;
- reliability limitations;
- scope uncertainty;
- temporal uncertainty;
- classification uncertainty;
- mapping uncertainty;
- statistical uncertainty;
- unknown cause.

Deleting material uncertainty is semantic strengthening.

Moving uncertainty into metadata while rendering an unconditional claim is
semantic strengthening.

Summary != uncertainty erasure.

---

## 7. Collapse Boundary

Collapse may narrow supported possibilities.

Collapse MUST preserve surviving uncertainty and surviving alternatives.

A Collapse operation MUST NOT silently transform:

- unresolved -> resolved;
- possible -> established;
- correlated -> causal;
- bounded evidence -> proof

unless attributable evidence supports that transition.

Removed alternatives MUST remain historically attributable.

Surviving uncertainty MUST remain semantically active downstream.

Collapse != certainty manufacture.

---

## 8. Raven Boundary

Raven may adapt representation.

Raven MUST NOT strengthen analytical meaning.

Raven MUST preserve applicable:

- assertion strength;
- support state;
- causal posture;
- uncertainty;
- surviving alternatives;
- evidence boundary;
- evidence ceiling;
- temporal scope;
- provenance.

Linguistic strengthening without analytical-state change is invalid.

Examples of prohibited unsupported strengthening include:

- possible -> probable;
- probable -> established;
- association -> causation;
- correlation -> causation;
- indication -> proof;
- unresolved -> resolved;
- material uncertainty -> omission.

Readable != stronger.

Executive language != stronger evidence.

---

## 9. Rendering Boundary

Rendering may change:

- format;
- layout;
- density;
- section order;
- typography;
- audience adaptation;
- visualization.

Rendering MUST NOT increase semantic claim strength.

A renderer MUST NOT produce an unconditional surface while the attributable
claim remains conditional, uncertain, contradicted, or bounded.

Visual emphasis MUST NOT imply unsupported rank, certainty, causality, or
authority.

Rendering != analytical promotion.

---

## 10. Evidence Ceiling

The evidence ceiling defines the maximum semantically admissible claim state
under the governed evidence.

A claim validator MUST evaluate the structured claim against the ceiling.

It MUST NOT merely verify that:

claim.evidence_ceiling_reference
==
expected_evidence_ceiling_reference.

Correct ceiling metadata + excessive semantic claim = FAIL.

The evidence ceiling MUST constrain all downstream representations of the claim.

---

## 11. Temporal Evidence Boundary

Historical analytical state remains historical analytical state.

Later evidence MUST NOT retroactively strengthen a historical conclusion.

Replay MUST preserve:

- evidence available then;
- evidence used then;
- historical evidence ceiling;
- historical assertion strength;
- historical causal posture;
- historical uncertainty;
- historical surviving alternatives.

Later evidence MAY support a new current analytical claim.

It MUST NOT rewrite the historical claim as though the later evidence existed
then.

Current support != historical support.

Replay != retrospective promotion.

---

## 12. Integrity / Truth Boundary

Cryptographic validity does not establish semantic truth.

AC-10 preserves:

Hash != truth.

Signature != correctness.

Integrity != semantic correctness.

Provenance != endorsement.

A valid:

- hash;
- signature;
- content identity;
- provenance chain;
- replay identity;
- deterministic serialization

MUST NOT independently increase assertion strength, support state, causal
posture, or evidence ceiling.

Integrity evidence proves integrity within its declared boundary.

It does not manufacture factual support.

---

## 13. Cross-Stage Semantic Monotonicity

The native analytical pipeline remains:

Evidence
->
PMC
->
CCR
->
MC
->
Raven
->
Human Gate

AC-10 requires semantic claim state to remain attributable across the complete
composition.

No downstream stage may produce a semantically stronger claim than its
attributable upstream analytical state unless a separately governed analytical
operation admits new evidence and produces a new attributable claim state.

CCR commitment != semantic strengthening.

MC admissibility != semantic strengthening.

Raven representation != semantic strengthening.

Human Gate approval != semantic strengthening.

Approval governs movement.

Approval does not manufacture evidence.

---

## 14. Semantic Admissibility

AC-10 defines:

- `ADMISSIBLE`;
- `BLOCKED`.

`ADMISSIBLE` means the complete structured semantic claim remains within the
governing evidence ceiling and preserves material uncertainty, temporal state,
causal posture, support state, and provenance.

`BLOCKED` means semantic admissibility cannot be established or the claim
exceeds the governing evidence.

ADMISSIBLE != true.

ADMISSIBLE != authorized.

BLOCKED != false.

BLOCKED means the requested claim form is not defensible under the attributable
evidence state.

---

## 15. Fail-Closed Conditions

AC-10 MUST fail closed when:

- structured semantic claim state is missing for a material claim;
- assertion strength exceeds the evidence ceiling;
- support state is strengthened without attributable evidence;
- causal posture exceeds evidentiary support;
- material uncertainty is removed;
- surviving alternatives are erased;
- Collapse silently changes surviving uncertainty;
- Raven strengthens wording without analytical-state change;
- rendering implies stronger certainty than source state;
- later evidence is rebound into historical support;
- historical evidence ceiling is raised retroactively;
- cryptographic integrity is treated as factual truth;
- provenance is treated as endorsement;
- evidence boundary is broadened;
- evidence ceiling is raised without attributable evidence;
- semantic comparison cannot be determined.

Unknown semantic admissibility = BLOCKED.

No optimistic default.

---

## 16. Deterministic Validation

AC-10 semantic enforcement MUST be deterministic over structured semantic
state.

The validator MUST NOT depend on unrestricted interpretation of arbitrary prose
as its primary enforcement mechanism.

Prose MAY be checked for consistency with structured semantic state.

Structured semantics remain the enforcement surface.

Equivalent structured claim + equivalent evidence state + equivalent ceiling
MUST produce the same admissibility disposition.

No hidden heuristic promotion.

No random semantic classification.

---

## 17. Required Adversarial Validation

AC-10 validation MUST include at minimum:

1. correct ceiling metadata with excessive assertion strength -> BLOCKED;
2. possible claim rendered as established -> BLOCKED;
3. correlation rendered as causation -> BLOCKED;
4. partially supported claim rendered as supported -> BLOCKED;
5. material uncertainty removed by Raven -> BLOCKED;
6. surviving Collapse alternative removed downstream -> BLOCKED;
7. later evidence strengthening historical claim -> BLOCKED;
8. later evidence producing a new current claim while historical claim remains
   unchanged -> ADMISSIBLE;
9. valid hash with unsupported factual assertion -> BLOCKED;
10. valid signature with unsupported factual assertion -> BLOCKED;
11. preserved semantic state across PMC -> CCR -> MC -> Raven -> ADMISSIBLE;
12. Human Gate approval without stronger evidence does not raise claim strength;
13. unknown semantic comparison -> BLOCKED;
14. equivalent structured state produces deterministic disposition.

Tests MUST evaluate meaning-bearing structured fields.

Metadata-only equality tests are insufficient evidence of AC-10.

---

## 18. Authority Boundary

AC-10 validates semantic admissibility.

AC-10 does not establish factual truth.

AC-10 does not authorize publication.

AC-10 does not authorize execution.

AC-10 does not create compliance, legal, certification, or disciplinary
authority.

Semantic admissibility != authority.

Authority remains NONE.

Human Gate remains ACTIVE.

---

## 19. AC-10 Lock

Evidence ceiling constrains claim meaning.

Metadata agreement is necessary but insufficient.

Correct ceiling metadata + semantic overclaim = FAIL.

Structured semantics are the enforcement surface.

Free-form prose does not replace structured semantic state.

Assertion strength MUST NOT increase without attributable evidence.

Correlation != causation.

High confidence != causation.

Material uncertainty is part of claim meaning.

Deleting material uncertainty is semantic strengthening.

Collapse != certainty manufacture.

Raven MUST NOT strengthen analytical meaning.

Rendering != analytical promotion.

Later evidence MUST NOT retroactively strengthen historical conclusions.

Replay != retrospective promotion.

Hash != truth.

Signature != correctness.

Integrity != semantic correctness.

Provenance != endorsement.

CCR commitment != semantic strengthening.

MC admissibility != semantic strengthening.

Human Gate approval != semantic strengthening.

Unknown semantic admissibility = BLOCKED.

No optimistic default.

Semantic admissibility != truth.

Semantic admissibility != authority.

Authority remains NONE.

Human Gate remains ACTIVE.
