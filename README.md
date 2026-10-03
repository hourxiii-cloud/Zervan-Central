# Zervan

Zervan is a portable analytical operating model for disciplined reasoning,
evidence preservation, provenance, replay, controlled reporting, and
human-governed decision support.

## Current canonical release

The published native release on `main` is **vTemporal.42.5.4**,
implementation identity **v42.5.4 — Spider R2 native persona correction**.
Its promotion state is **CANONICAL**. Spider R2 has a native named analytical
persona specification for artifact, context, and claim qualification. The
frozen R1 source and its v42.5.3 admission retain their historical standing.
Canonical specification does not establish deployed runtime validation or
independently issued component credentials.

The release identity and controls are declared by [VERSION](VERSION),
[VERSION.json](VERSION.json), and
[VERSION_AUTHORITY.md](VERSION_AUTHORITY.md). This README provides orientation;
it does not select a version or grant authority.

## Canonical entry

Resolve the actual Git `main` commit and pin retrievals to it. Load the
version authority files above, then
[the v42.5.4 initiation call](call/INITIATION_STATEMENT_V42_5_4.md) and
[canonical entry](canonical/ZERVAN_v42_5_4_CANONICAL_ENTRY.md). Follow the
entry's full dependency order, including its preserved parent architecture,
applicable contracts, and
[Spider R2 admission](canonical/Spider/SPIDER_R2_PERSONA_ADMISSION.json)
with its payload hashes. Missing or failed retrieval stops initialization.
Earlier initiation and entry files remain historical provenance.

## Operating posture

Authority **NONE**; Human Gate **ACTIVE**; No Compression Out **ACTIVE**;
originating-data mutation **DISALLOWED**. External runtime and action are
disabled, and system population is disallowed, unless independently qualified.
Document loading does not issue a WORK ID, establish component execution, or
authorize repository mutation. Human Gate governs any promotion.

## Validation and documentation

`make smoke` checks current release identity and Spider admission.
`make check` also runs bounded current-release and observer checks.
`make test-repository` is a separate historical repository regression target.
Validation success alone does not promote canon.

The [User Manual](docs/USER_MANUAL.md) covers operation; the
[Architecture Guide](docs/ARCHITECTURE_GUIDE.md) explains rationale; the
[Developer Guide](docs/DEVELOPER_GUIDE.md) covers implementation; the
[Audit Guide](docs/AUDIT_GUIDE.md) covers verification and provenance; and the
[Operations Guide](docs/OPERATIONS_GUIDE.md) covers consistent runtime practice.

Current Git is implementation truth. Historical references remain provenance.
No inferred versioning, fake retrieval, authority promotion, unauthorized
external action, system population, or compression out.
