# AC-RTIOT-02 — Evidence-Ceiling Enforcement

Status: CONTROLLED ACTIVATION PATCH
Version: vTemporal.41.0
Activation Branch: ac/v41-activation
Authority: NONE
Human Gate: ACTIVE

## Purpose

Evidence-Ceiling Enforcement prevents an analytical claim from becoming
stronger than the evidence surface that supports it.

Model confidence does not raise the evidence ceiling.

Collision state does not resolve missing context.

Repeated prediction does not create stronger evidence.

Evidence ceiling != confidence score.

Confidence does not override claim ceiling.

## Evidence Scope

Native AC-RTIOT-02 recognizes:

- ROW_LOCAL
- GROUP_LOCAL
- EVENT_CONTEXT
- NATIVE_CONTEXT

ROW_LOCAL means the claim is supported only by the measurable content of one
row.

GROUP_LOCAL means the claim is supported by a bounded relationship among
multiple attributable rows or collision-group members.

EVENT_CONTEXT means the claim requires attributable event/session/window
context beyond isolated row bodies.

NATIVE_CONTEXT means the claim requires native source context such as packet,
log, host, identity, process, temporal, session, or equivalent source evidence.

A narrower evidence scope MUST NOT silently satisfy a broader evidence scope.

## Claim State

Every evaluated claim receives exactly one disposition:

- ADMISSIBLE
- CONDITIONAL
- INADMISSIBLE
- UNRESOLVED

ADMISSIBLE means the available evidence scope and evidence ceiling support the
declared claim without promotion.

CONDITIONAL means the claim may become admissible only if explicitly identified
additional evidence or conditions are satisfied.

INADMISSIBLE means the claim exceeds the current evidence ceiling or contradicts
the governed evidence state.

UNRESOLVED means the system cannot defensibly determine admissibility from the
available evidence.

UNRESOLVED != ADMISSIBLE.

CONDITIONAL != ADMISSIBLE.

## Observation / Inference / Unknown

Every material analytical assertion MUST preserve one epistemic class:

- OBSERVED
- INFERRED
- UNKNOWN

OBSERVED means directly supported by the admitted evidence surface.

INFERRED means derived from admitted evidence without being directly observed.

UNKNOWN means the available evidence cannot establish the assertion.

INFERRED MUST NOT silently become OBSERVED.

UNKNOWN MUST NOT silently become INFERRED.

UNKNOWN MUST NOT silently become OBSERVED.

## Collision Boundary Integration

AC-RTIOT-01 population dispositions remain:

- CLEAN
- COLLISION
- UNRESOLVED_CONTEXT

A COLLISION row establishes an exact measurable-body contradiction across
reviewed labels.

COLLISION does not establish which conflicting macro-context label is true.

COLLISION MUST NOT be used to promote a ROW_LOCAL observation into an
EVENT_CONTEXT claim.

UNRESOLVED_CONTEXT MUST NOT be used as affirmative evidence.

Collision != event attribution.

Collision != attack attribution.

Collision != command-and-control evidence.

## Confidence Boundary

Confidence is analytical metadata.

Confidence MUST NOT:

- raise evidence scope;
- raise evidence ceiling;
- change UNKNOWN to INFERRED;
- change INFERRED to OBSERVED;
- change CONDITIONAL to ADMISSIBLE;
- change INADMISSIBLE to ADMISSIBLE;
- resolve COLLISION;
- resolve UNRESOLVED_CONTEXT;
- manufacture native context.

High confidence in an unsupported claim remains unsupported.

Confident wrong != stronger evidence.

## Required Evidence

A claim requiring broader evidence than currently available MUST preserve the
missing evidence requirement explicitly.

Required evidence may include:

- timestamps;
- source or destination identity;
- device identity;
- host identity;
- user/session identity;
- capture/session identity;
- attack/event window;
- source shard or source file;
- original PCAP linkage;
- sequence ordering;
- host/network role;
- authentication evidence;
- process lineage;
- native packet/log reconstruction;
- upstream/downstream flow context;
- other explicitly declared native context.

Missing evidence != negative evidence.

Missing evidence != permission to infer.

## Claim Promotion

A claim may move to a broader evidence scope only through a separately
attributable evaluation using newly admitted evidence.

Promotion requires:

- prior claim reference;
- prior evidence scope;
- requested evidence scope;
- new evidence references;
- evidence-boundary compatibility;
- evidence-ceiling compatibility;
- provenance;
- resulting disposition.

Claim promotion MUST NOT occur merely because:

- confidence increased;
- a model repeated the prediction;
- multiple identical rows exist;
- the reviewed label is stronger;
- a report prefers stronger language;
- a Human Gate decision exists.

Human approval does not manufacture evidence.

## Fail Closed

Evidence-Ceiling Enforcement SHALL reject or preserve non-admissible state when:

- required evidence scope exceeds available evidence scope;
- evidence ceiling is absent;
- evidence boundary is absent;
- provenance is absent;
- an UNKNOWN assertion is promoted;
- an INFERRED assertion is rendered OBSERVED;
- confidence is used as evidence authority;
- COLLISION is treated as event attribution;
- UNRESOLVED_CONTEXT is treated as affirmative evidence;
- missing native context is reconstructed or guessed;
- claim promotion lacks new attributable evidence;
- a broader claim is produced from a narrower evidence surface.

## RT-IoT2022 Boundary

For the established collision population:

ROW_LOCAL evidence supports observation of protocol instruction residue.

The row-local evidence does not independently establish the complete
macro-event represented by the reviewed label.

The established residue lanes include:

- UDP DNS/mDNS 5353;
- UDP DHCP 68 -> 67;
- ICMP reachability/control-compatible residue.

The current row-feature evidence does not independently establish:

- command-and-control;
- actor intent;
- live compromise;
- binary execution;
- process lineage;
- exact relationship between each residue row and its macro-event label.

Those claims require broader attributable evidence.

## Authority Boundary

Authority remains NONE.

Human Gate remains ACTIVE.

External Runtime remains DISABLED.

External Action remains DISABLED.

System Population remains DISALLOWED.

Evidence evaluation creates no authority.

Human Gate approval does not raise the evidence ceiling.
