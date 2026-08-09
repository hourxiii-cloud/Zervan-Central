# AC-RTIOT-01 — Collision Boundary

Status: CONTROLLED ACTIVATION PATCH
Version: vTemporal.41.0
Activation Branch: ac/v41-activation
Authority: NONE
Human Gate: ACTIVE

## Purpose

The Collision Boundary separates exact measurable-body contradiction from
ordinary supervised scoring.

Identical measurable bodies carrying conflicting reviewed labels are collision
evidence.

Collision != anomaly.
Collision != model error.
Collision != malicious.
Collision != benign.

## Population Dispositions

Every admitted row receives exactly one collision-boundary disposition:

- CLEAN
- COLLISION
- UNRESOLVED_CONTEXT

CLEAN means the canonical measurable body does not participate in a cross-label
exact-body collision.

COLLISION means the same canonical measurable body occurs with more than one
distinct reviewed label.

UNRESOLVED_CONTEXT means the collision disposition cannot be established
defensibly from the declared measurable identity surface.

UNRESOLVED_CONTEXT != CLEAN.

Unknown remains unknown.

## Measurable-Body Identity

Measurable-body identity SHALL:

- exclude the reviewed target label;
- exclude row index as semantic evidence;
- declare the measurable feature surface explicitly;
- use deterministic field ordering;
- preserve explicit null values;
- use deterministic canonical JSON;
- use SHA-512 identity.

Canonical form:

sha512:<128 lowercase hexadecimal characters>

Hash != truth.

## Collision Group

Rows with the same measurable-body identity are grouped before supervised
train/test splitting.

If a group contains more than one distinct reviewed label, every member is
COLLISION.

Each collision group preserves:

- collision_group_id;
- measurable_body_sha512;
- member_count;
- distinct_labels;
- member references;
- feature identity surface;
- provenance where available.

Collision-group identity SHALL NOT depend on input row order.

## Pre-Split Invariant

Required analytical route:

source
->
measurable-body identity
->
collision analysis
->
population disposition
->
eligible CLEAN supervised population

COLLISION and UNRESOLVED_CONTEXT remain preserved evidence populations.

They SHALL NOT silently enter ordinary supervised scoring denominators.

## Reconciliation

The following counts SHALL be independently visible:

- total_source_rows;
- clean_rows;
- collision_rows;
- unresolved_context_rows;
- collision_groups.

Required invariant:

total_source_rows =
clean_rows +
collision_rows +
unresolved_context_rows

## Evidence Boundary

A collision establishes that the current measurable body cannot uniquely
support all attached reviewed labels.

It does not establish which macro-context label is true.

It does not reconstruct missing native context.

It does not establish actor intent, compromise, command-and-control, or
maliciousness.

## Fail Closed

The boundary SHALL reject or preserve UNRESOLVED_CONTEXT when:

- the measurable feature surface is empty;
- the target label is included in measurable-body identity;
- canonicalization is nondeterministic;
- required measurable fields cannot be resolved;
- reconciliation fails;
- collision identity depends on row order;
- a cross-label exact-body collision is classified CLEAN;
- a collision row enters an ordinary supervised denominator.

## Authority Boundary

Authority remains NONE.

Human Gate remains ACTIVE.

External Runtime remains DISABLED.

External Action remains DISABLED.

System Population remains DISALLOWED.

Collision analysis creates no authority.
