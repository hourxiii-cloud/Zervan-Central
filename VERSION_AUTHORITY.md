# VERSION_AUTHORITY — Native v41 Version Identity and Promotion

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R1-B — Version Identity & Promotion
Version Identity: vTemporal.41.0
Implementation Identity: v41 Complete
Promotion State: CANDIDATE
Canonical: FALSE
Canonical Branch: `main`
Development Branch: `candidate/v41-complete`
Authority: NONE
Human Gate: ACTIVE

---

## 0. Purpose

This contract defines how native v41 version identity is declared, resolved,
validated, and promoted without conflating version identity with authority,
repository location, or promotion state.

R1-B consumes the authority and canonical-resolution rules established by
`DoctrineOps/AUTHORITY_RESOLUTION.md`.

R1-B does not redefine R1-A.

---

## 1. Single Version Identity

Native v41 has one implementation version identity:

`vTemporal.41.0`

The human-readable declaration is:

`/VERSION`

The machine-readable declaration is:

`/VERSION.json`

These two declarations MUST agree exactly.

`VERSION_AUTHORITY.md` defines their interpretation and resolution.

No README, branch name, directory name, historical artifact, bridge artifact,
candidate document, manifest, conversation state, or implementation detail may
independently redefine the active version.

One active version.
One authority path.
No inferred versioning.

---

## 2. Implementation Identity and Promotion State Are Separate

Version identity answers:

> Which native implementation is this?

Promotion state answers:

> Has this implementation crossed the governed boundary into canonical `main`?

These are independent dimensions.

The current native implementation identity is:

`vTemporal.41.0`

Its current promotion state is:

`CANDIDATE`

Promotion MUST NOT manufacture a new version identifier merely because the same
validated implementation moves from candidate state to canonical state.

Therefore:

`vTemporal.41.0 CANDIDATE`

and, after valid Human-Gated promotion:

`vTemporal.41.0 CANONICAL`

refer to the same version identity at different governed promotion states.

A substantive implementation change requiring a new version is a separate
versioning decision and MUST NOT be inferred from promotion alone.

---

## 3. Candidate State

While development occurs on:

`candidate/v41-complete`

the native v41 implementation is:

- Version: `vTemporal.41.0`
- Implementation Identity: `v41 Complete`
- Promotion State: `CANDIDATE`
- Canonical: `FALSE`

Candidate strength, completeness, test success, branch existence, commit
existence, or technical write capability does not independently make the
candidate canonical.

The canonical implementation remains whatever is validly resolved from `main`
until promotion completes.

---

## 4. Canonical State

The canonical implementation surface is `main`.

Native v41 becomes canonical only after the promotion requirements established
by R1-A and the applicable v41 validation contracts are satisfied.

Promotion requires, at minimum:

1. candidate identity is explicit;
2. intended canonical target is explicit;
3. source disposition and provenance are preserved;
4. required stability, regression, completeness, and lossless-collapse
   validation succeeds;
5. unresolved conflicts and evidence ceilings are surfaced;
6. required promotion evidence exists;
7. Human Gate explicitly approves promotion;
8. canonical repository mutation actually occurs;
9. the resulting state on `main` is independently resolvable and verifiable.

Only after those conditions are satisfied may `/VERSION.json` on promoted
`main` declare:

`promotion_state = CANONICAL`

and:

`canonical = true`

Promotion is not complete merely because a merge, push, commit, or file write
is technically possible.

---

## 5. No Mixed-Version Identity

An active repository state MUST NOT simultaneously claim incompatible current
version identities.

Historical versions MAY remain for provenance.

Candidate bridge versions MAY remain as historical development evidence.

Neither historical nor bridge identifiers may impersonate the active native
version.

In particular:

- v39 references are historical when preserved;
- v40 references are baseline/history when preserved;
- v41.1.x references identify candidate/recovery/bridge development history;
- `vTemporal.41.0` identifies the native v41 implementation.

Historical presence is not active authority.

---

## 6. Historical-Reference Inventory

`/VERSION_REFERENCES.json` is the repository-wide inventory of detected v39,
v40, v41, and vTemporal version references.

Its purpose is to prevent old version residue from silently becoming active
version authority.

The inventory records:

- file path;
- detected version token;
- line;
- classification.

The inventory is evidence and control metadata.

It does not create authority and does not replace `/VERSION` or
`/VERSION.json`.

Any repository change adding, deleting, or changing a version reference MUST
cause version-reference validation to be rerun.

---

## 7. Active Version Surfaces

The only native version declaration surfaces are:

1. `/VERSION`
2. `/VERSION.json`
3. `/VERSION_AUTHORITY.md`

README owns orientation, not version authority.

Historical canonical loads, archived initiation statements, transition
documents, bridge documents, manifests, receipts, and prior-version materials
may retain version identifiers for provenance but may not supersede these
active version surfaces.

---

## 8. Validation

`tools/validate_version_identity.py` MUST fail when:

- `/VERSION` is absent;
- `/VERSION.json` is absent;
- the two active version declarations disagree;
- the declared version is empty or inferred;
- candidate/canonical state is internally contradictory;
- the authority contract is missing;
- the historical-reference inventory is missing;
- repository version references differ from the recorded inventory;
- active control surfaces assert a competing version identity.

A silent version disagreement is invalid.

---

## 9. Promotion Receipt Boundary

R1-B defines that a Promotion Receipt is required.

R1-B does not create that receipt.

A Promotion Receipt may be produced only after the required native v41
implementation, disposition, validation, completeness, and lossless-collapse
work has actually occurred.

Receipt existence without satisfied evidence does not authorize promotion.

---

## 10. Downstream Boundary

R1-B defines version identity and promotion interpretation only.

It does NOT define:

- Room identity;
- object identity;
- provenance primitives;
- Genesis or Revision Manifests;
- state roots;
- authorized-view roots;
- active object pointers;
- revision semantics;
- branch semantics;
- merge semantics.

Those remain downstream Ring 1 dependencies.

---

## 11. R1-B Lock

Version identity is singular.
Promotion state is explicit.
Version identity and promotion state are not the same thing.
Historical references remain provenance, not current authority.
No version is inferred.
No mixed-version identity is admissible.
Human Gate remains required for canonical promotion.
