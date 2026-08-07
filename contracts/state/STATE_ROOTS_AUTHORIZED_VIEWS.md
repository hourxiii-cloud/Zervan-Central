# R1-E — State Roots, Authorized Views, and State Pointer

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R1-E
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R1-E defines canonical state identity, authorized-view identity, and the
mutable pointer selecting current state.

R1-E consumes:

- R1-A authority and mutation rules;
- R1-B version identity;
- R1-C SHA-512 identity and provenance;
- R1-D immutable manifest architecture.

R1-E does not redefine those contracts.

R1-E does not resolve branch or merge semantics.

---

## 1. Required Separation

The following are independent:

- accepted definition;
- canonical object state;
- authorized representation of canonical state;
- execution state.

Definition is not state.

State is not projection.

Projection is not execution.

No outer capability may collapse these dimensions.

---

## 2. Canonical State Record

A Canonical State Record describes one accepted state of an analytical object
under one selected manifest definition.

It contains:

- manifest reference;
- monotonic state sequence;
- canonical state payload;
- provenance route;
- state creation time;
- canonical state root.

The state payload may evolve while the manifest definition remains unchanged.

A state change does not automatically create a Revision Manifest.

A definition change does not silently rewrite historical state.

---

## 3. State Root

A State Root is the SHA-512 identity of a deterministic state preimage.

The State Root preimage consists of exactly:

- active manifest reference;
- state sequence;
- canonical state payload.

Canonical serialization for R1-E root calculation is UTF-8 JSON with:

- keys sorted;
- no insignificant whitespace;
- deterministic separators;
- Unicode preserved.

Canonical form:

`sha512:<128 lowercase hexadecimal characters>`

The State Root identifies state under a declared definition.

It is not automatically:

- Room identity;
- object identity;
- Genesis identity;
- Revision identity;
- authority;
- truth.

State root != object identity.

Hash != truth.

---

## 4. Historical State

Accepted State Records are immutable historical evidence.

A new state does not overwrite an older state record.

Historical state must remain addressable by State Root.

Replay may later resolve a historical State Root, but replay behavior remains
downstream.

---

## 5. Authorized View

An Authorized View is a controlled projection of one canonical State Root.

It MUST identify:

- source State Root;
- authorization reference;
- view scope;
- projection payload;
- restrictions or redactions;
- view creation time;
- Authorized View Root.

An Authorized View does not create a new canonical object.

An Authorized View does not mutate canonical state.

Multiple Authorized Views may resolve against the same State Root.

Different visibility does not imply different reality.

---

## 6. Authorized View Root

An Authorized View Root is the SHA-512 identity of a deterministic projection
preimage.

The Authorized View Root preimage consists of exactly:

- source State Root;
- authorization reference;
- view scope;
- projection payload;
- restrictions.

Canonical serialization follows the same deterministic JSON rules as State
Root generation.

Authorized View Root identifies a projection.

It is not:

- canonical State Root;
- object identity;
- Room identity;
- independent analytical reality.

Authorized View Root != State Root.

Projection != canonical state.

---

## 7. Shared Invariants Across Views

Authorized Views over the same State Root MUST preserve the invariants needed
to resolve them back to the same canonical state.

At minimum:

- source State Root;
- active manifest reference resolvable through that state;
- existence of restricted material when known;
- provenance continuity;
- authorization reference;
- projection restrictions.

A view may differ in:

- visible fields;
- visible relationships;
- permitted operations;
- representation;
- bounded evidence exposure.

A view MUST NOT falsify hidden content as nonexistent merely because access is
restricted.

Restricted remains existent.

---

## 8. State Pointer

The State Pointer is the mutable locator selecting current canonical state.

It identifies:

- active manifest reference;
- active State Root;
- current state sequence;
- prior State Root;
- update time;
- mutation reason;
- authorization reference;
- provenance route.

The State Pointer does not contain the complete canonical state payload.

It does not rewrite historical State Records.

It does not replace the R1-D Manifest Pointer.

Manifest Pointer selects current accepted definition.

State Pointer selects current accepted state under that definition.

---

## 9. State Pointer Mutation

State Pointer movement is canonical mutation governed by R1-A.

Technical write capability is insufficient.

Pointer movement MUST preserve:

- prior State Root;
- new State Root;
- mutation reason;
- mutation time;
- authorization reference;
- provenance route.

Approval and execution remain separate.

---

## 10. Definition / State Coordination

Every State Record MUST resolve to one accepted manifest reference.

If the selected manifest changes, later state must explicitly identify the new
manifest reference.

R1-E does not decide when a definition change is required.

That remains governed by R1-D and later object/revision semantics.

No state payload may silently mutate its governing definition.

---

## 11. Representation Boundary

Bounded Zones, Bounded Spaces, perspectives, renderings, and later
representation transforms may consume Authorized Views.

They may not redefine:

- State Root;
- canonical state;
- manifest definition;
- provenance;
- authorization evidence.

Representation changes what is exposed or emphasized.

Representation does not clone canonical state.

---

## 12. Execution-State Boundary

Execution state remains distinct from canonical object state.

A capability being:

- requested;
- authorized;
- entered;
- active;
- running;
- completed;
- failed

does not by itself alter canonical State Root.

Only an admissible state mutation may create a new canonical State Record.

Execution != state mutation.

---

## 13. Unknown / Restricted / Unavailable

Canonical state and Authorized Views MUST preserve the R1-C distinctions among:

- known and available;
- known but restricted;
- known but unavailable;
- unresolved;
- absent.

Projection may hide payload.

Projection may not erase known existence.

---

## 14. Branch / Merge Boundary

R1-E does not define branch identity.

R1-E does not define merge identity.

A historical State Root is not automatically a branch.

Two Authorized Views are not branches.

Two different State Roots are not automatically distinct objects.

R1-F owns revision / branch / merge semantics.

---

## 15. R1-E Lock

Manifest identifies accepted definition.

State Root identifies canonical state under that definition.

Authorized View Root identifies a controlled projection of canonical state.

State Pointer selects current canonical state.

Manifest Pointer and State Pointer remain separate.

Historical state is immutable.

Views do not mutate canonical state.

Different visibility does not create different reality.

State does not equal execution.

State Root does not equal object identity.

Authorized View Root does not equal State Root.

R1-F remains blocked.
