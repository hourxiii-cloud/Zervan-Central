# Zervan 5.6 Deployment Bridge — Transition Control

Status: TRANSITION CONTROL  
Authority: NONE  
Human Gate: ACTIVE  
Mode: DISCUSSION / TECH / NONE / NON-DOCTRINAL / STABLE  
Posture: CONTROLLED / READ-ONLY unless explicitly authorized for patch work  
External Runtime: DISABLED  
System Population: DISALLOWED

This bridge is the current planned deployment path for adapting the uploaded v39 package against the 5.6 architecture decisions. It is not a rewrite, not a compression exercise, not a source-of-truth promotion, and not an execution authorization.

## Canonical Definitions

Canonical 5.6 bridge definitions are centralized in:

```text
ZERVAN_5_6_CANONICAL_DEFINITIONS.md
```

This bridge document intentionally does not restate the full spine, observer registry, sub-observer registry, Owl_Hoot boundary, or Raven / The Unkindness role definitions. Those definitions live in the canonical definitions file to reduce drift risk between the bridge, transition note, modified-file record, and future maintenance updates.

## Bridge Control Scope

This document controls the transition process:

```text
Bridge + v39 package → affected inventory confirmed → branch/worktree plan →
patch only affected files → validate against bridge → produce modified-file record →
produce transition note → promote only after clean validation.
```

The canonical definitions file controls the architecture definitions.

## Non-Compression Rule

The non-compression rule is defined canonically in `ZERVAN_5_6_CANONICAL_DEFINITIONS.md` and applies to this bridge. In operational terms:

```text
No named function, observer, module, persona lens, or routing capability may be
compressed out of existence.
```

## Modification Priority

1. Full spine / load-order preservation
2. Evidence-engine boundary clarification
3. Observer registry / observer boundary preservation
4. ANALYTICAL / observer-lens preservation
5. Sub-observer reseating
6. Raven / The Unkindness reporting branding
7. Manifest / hydration / validation alignment
8. Documentation / demo cleanup

## Branch Family Plan

The uploaded zip has no `.git` metadata, so these names are planned branch/worktree families only:

- bridge/v39-5.6-transition-control
- bridge/v39-5.6-spine-loadorder
- bridge/v39-5.6-evidence-engine-boundary
- bridge/v39-5.6-observer-registry-boundary
- bridge/v39-5.6-analytical-lens-preservation
- bridge/v39-5.6-sub-observer-reseat
- bridge/v39-5.6-raven-unkindness
- bridge/v39-5.6-manifest-hydration-validation
- bridge/v39-5.6-docs-demo-cleanup

## Validation Mechanism

Reproducible validation is performed with:

```bash
python tools/validate_zervan_5_6_bridge.py --root . --emit ZERVAN_5_6_VALIDATION_RESULTS.json
```

The validation script checks JSON parseability, Python syntax compilation, required bridge artifacts, expected observer/sub-observer paths, and the canonical invariants named in `ZERVAN_5_6_CANONICAL_DEFINITIONS.md`.

## Promotion Rule

Promotion requires explicit human gate approval, review of `ZERVAN_5_6_MODIFIED_FILE_RECORD.md`, review of `ZERVAN_5_6_TRANSITION_NOTE.md`, and a current passing validation result from `tools/validate_zervan_5_6_bridge.py`.

No silent replacement. No jink. No compression out.
