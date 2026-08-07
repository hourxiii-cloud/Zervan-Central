# R2-C — Terrain and Territory

Status: CONTROLLED CANDIDATE CONTRACT
Ring: R2-C
Version: vTemporal.41.0
Promotion State: CANDIDATE

---

## 0. Purpose

R2-C defines Terrain and Territory as separate Operational Geography
primitives attached to one established Canonical Room Object.

R2-C consumes:

- complete Ring 1;
- R2-A Canonical Room Object identity and singularity;
- R2-B Origin Establishment and Object Binding.

R2-C does not redefine them.

R2-C does not yet define:

- Bounded Zone;
- Bounded Space;
- Perspective / Representation Transform;
- Orientation;
- Cartography;
- Stick;
- Passageway;
- Occupation;
- capability movement.

---

## 1. Operational Geography Boundary

An established Canonical Room Object may contain informational structure that
can be encountered and navigated.

R2-C separates:

Terrain
    = what is encountered.

Territory
    = what is navigably reachable.

Terrain != Territory.

Neither primitive creates another Room Object.

---

## 2. Terrain

Terrain is the observed informational surface and structure encountered through
a declared representation of the Canonical Room Object.

Terrain may include:

- source structure;
- fields;
- records;
- relationships;
- density;
- absence;
- fractures;
- signal concentrations;
- boundaries;
- gradients;
- discontinuities;
- reachable surfaces;
- unreachable surfaces;
- stable regions;
- uncertainty frontiers;
- deformation regions.

Terrain records what is encountered.

Terrain is not a conclusion.

---

## 3. Terrain Is Object-Bound

Every Terrain Record MUST carry or resolve the canonical `object_id`.

Terrain identity is local geography identity.

Terrain identity is not object identity.

Different Terrain may be exposed through different representations while
remaining attached to the same Canonical Room Object.

Terrain difference != object difference.

---

## 4. Representation Sensitivity

Terrain is representation-sensitive.

A shift in evidence access, perspective, discipline, scale, time boundary, or
other later-declared representation dimension may expose different Terrain.

That change does not establish another object.

R2-C records only the representation reference associated with observed
Terrain.

R2-C does not yet define representation semantics.

Those belong to later Ring 2 contracts.

---

## 5. Terrain Evidence Status

Terrain observations MUST preserve whether a feature is:

- OBSERVED;
- RESTRICTED;
- UNAVAILABLE;
- UNRESOLVED.

Restricted or unavailable Terrain MUST NOT silently become nonexistent.

Unknown remains unknown.

Absence may itself be observed Terrain when supported by evidence.

---

## 6. Terrain Record

A Terrain Record captures an attributable description of informational
structure encountered against one Canonical Room Object.

It MUST preserve:

- Terrain Record identity;
- canonical object identity;
- declared representation reference;
- observation/evidence reference;
- observed features;
- accessibility state;
- provenance route;
- observation time.

The Terrain Record does not own analytical truth.

It records encountered structure.

---

## 7. Territory

Territory is the navigable analytical geography reachable from the Canonical
Room Object and its validated relationships.

Territory describes where later operations may legitimately move or establish
contact.

Territory is derived from demonstrated reachability.

Territory is not merely all imaginable adjacent information.

Possible != reachable.

---

## 8. Territory Boundary

Territory may include references to:

- reachable Terrain;
- validated relationships;
- reachable analytical surfaces;
- bounded reachable neighboring structures.

Territory MUST NOT silently include:

- unvalidated relationships;
- imagined adjacency;
- inaccessible surfaces merely because they are known to exist;
- another object merely because a relationship exists.

Relationship != identity collapse.

Reachability != ownership.

---

## 9. Reachability

A candidate surface or relationship may have one of the following R2-C
reachability states:

- REACHABLE;
- UNREACHABLE;
- UNRESOLVED.

Only REACHABLE material belongs to active Territory.

UNREACHABLE remains known but outside current navigable Territory.

UNRESOLVED remains unresolved.

UNRESOLVED MUST NOT silently become REACHABLE.

---

## 10. Validated Relationship Requirement

Territory expansion requires a validated relationship or other admissible
reachability basis.

A relationship reference alone does not prove reachability.

R2-C therefore distinguishes:

- relationship existence;
- relationship validation;
- operational reachability.

Existence != validation.

Validation != reachability.

---

## 11. Territory Record

A Territory Record MUST preserve:

- Territory Record identity;
- canonical `object_id`;
- reachable Terrain references;
- validated relationship references;
- reachable surface references;
- unresolved reachability references;
- excluded/unreachable references;
- provenance route;
- derivation time.

Territory identity is geography identity.

Territory identity is not object identity.

---

## 12. Terrain / Territory Relationship

Terrain may exist outside active Territory.

Known Terrain can be unreachable.

Unknown Terrain may later become observable.

Territory may change as validated relationships and reachability change.

A Territory change does not by itself create another Room Object.

Terrain change != object change.

Territory change != object change.

---

## 13. State Boundary

Terrain and Territory describe analytical geography.

They do not replace R1-E canonical State Root semantics.

If a geography change is accepted as canonical state change, R1-E governs
State Root creation.

R2-C does not create an alternate state system.

Geography != State Root.

---

## 14. Distinct-Object Boundary

Encountering another informational structure does not automatically establish a
new Room Object.

If evidence indicates that reachable geography crosses into a genuinely
distinct analytical object, R1-F distinct-object semantics apply.

R2-C MUST NOT manufacture a new `object_id`.

Passage between genuinely distinct objects remains deferred.

---

## 15. Terrain Record Identity

Terrain Record identity is deterministic SHA-512 over exactly:

- canonical `object_id`;
- representation reference;
- observation reference;
- observed features;
- accessibility state;
- observation time.

Terrain Record identity identifies the observation of Terrain.

It does not identify the Canonical Room Object.

---

## 16. Territory Record Identity

Territory Record identity is deterministic SHA-512 over exactly:

- canonical `object_id`;
- reachable Terrain references;
- validated relationship references;
- reachable surface references;
- unresolved reachability references;
- excluded/unreachable references;
- derivation time.

Territory Record identity identifies one resolved geography record.

It does not identify the Canonical Room Object.

---

## 17. No Premature Cartography

R2-C defines the geography that later Cartography will map.

R2-C does not define the map.

Terrain != Cartography.

Territory != Cartography.

Cartography remains downstream.

---

## 18. No Premature Zone or Space

Terrain may reference the declared representation under which it was
encountered.

R2-C does not define Bounded Zone or Bounded Space contracts.

A representation reference is opaque at R2-C.

Zone semantics remain R2-D.

Space semantics remain R2-E.

---

## 19. No Premature Occupation

The source architecture later permits capabilities to occupy and move through
Territory.

R2-C defines the geography only.

It does not authorize or record occupant presence.

Territory != Occupation.

Reachable != occupied.

---

## 20. R2-C Lock

Terrain is encountered informational structure.

Terrain is representation-sensitive and object-bound.

Terrain is not a conclusion.

Territory is navigable analytical geography reachable from the Room Object and
validated relationships.

Terrain != Territory.

Possible != reachable.

Known != reachable.

Relationship existence != relationship validation.

Relationship validation != operational reachability.

Only REACHABLE material belongs to active Territory.

Terrain identity is not object identity.

Territory identity is not object identity.

Terrain change does not replace object identity.

Territory change does not replace object identity.

No Zone semantics yet.

No Space semantics yet.

No Transform semantics yet.

No Orientation yet.

No Cartography yet.

No Occupation yet.
