# Zervan 5.6 Bridge — Validation Process

Status: REVIEW-RESPONSE VALIDATION PROCESS  
Authority: NONE  
Human Gate: ACTIVE  
External Runtime: DISABLED  
System Population: DISALLOWED

This file documents the reproducible validation mechanism for the Zervan 5.6 bridge package. It exists to make the transition note's validation claims traceable and repeatable by future maintainers.

## Validation Command

The package-local validation command is:

```bash
python tools/validate_zervan_5_6_bridge.py --root . --emit ZERVAN_5_6_VALIDATION_RESULTS.json
```

## Validation Scope

The validator is read-only. It does not mutate source files, hydrate external runtime, populate systems, contact external services, or promote authority.

The validator checks:

1. Required bridge artifacts exist.
2. JSON files parse successfully.
3. Python files parse successfully with `ast.parse`.
4. The canonical definitions file exists and includes required invariants.
5. The full Zervan spine is present in the canonical definitions.
6. The evidence-engine boundary is present.
7. Owl_Hoot remains a primary observer.
8. Owl_Hoot bounded sub-observer mode is documented without demotion.
9. Osprey, AnimalKingdom, and Armadillo are seated as controlled sub-observers.
10. The Unkindness is defined as Raven reporting brand / output voice only.
11. No deleted-file condition is recorded in the modified-file record.
12. No external runtime activation, system population, or authority promotion is declared.

## Required Artifacts

The validation process expects these files at repository/package root:

```text
ZERVAN_5_6_CANONICAL_DEFINITIONS.md
ZERVAN_5_6_DEPLOYMENT_BRIDGE.md
ZERVAN_5_6_TRANSITION_NOTE.md
ZERVAN_5_6_MODIFIED_FILE_RECORD.md
ZERVAN_5_6_VALIDATION_PROCESS.md
```

Optional but recommended:

```text
ZERVAN_5_6_VALIDATION_RESULTS.json
ZERVAN_5_6_CODE_REVIEW_RESPONSE.md
```

## Output Artifact

The validator emits:

```text
ZERVAN_5_6_VALIDATION_RESULTS.json
```

The output should include:

```json
{
  "status": "PASS",
  "authority": "NONE",
  "external_runtime": "DISABLED",
  "system_population": "DISALLOWED",
  "checks": []
}
```

Each check should include:

```json
{
  "name": "check_name",
  "status": "PASS",
  "detail": "Human-readable explanation."
}
```

If any validation check fails, the top-level status must be `FAIL`.

## Minimal Validator Reference

The package-local validator may be implemented as `tools/validate_zervan_5_6_bridge.py`.

Required behavior:

- Accept `--root` for package root.
- Accept `--emit` for validation result output path.
- Walk the package root for `.json` files and parse them.
- Walk the package root for `.py` files and parse them with Python `ast`.
- Read canonical Markdown artifacts and assert required invariant strings.
- Emit machine-readable JSON.
- Exit non-zero on failure.
- Perform no mutation except writing the requested validation-results artifact.

## Validation Invariants

The validation command must confirm:

- Full spine remains visible.
- Beagle / Retriever / Raven / Audit remain evidence-engine modules inside the full spine, not the whole skeleton.
- TECH / AUDIT / HYBRID / CREATIVE remain preserved as lenses or unit postures.
- Owl_Hoot remains a primary observer.
- Owl_Hoot optional sub-observer mode is bounded and does not demote it.
- Osprey, AnimalKingdom, and Armadillo are controlled sub-observers only.
- The Unkindness is Raven reporting brand only.
- No source-of-truth lane is silently added.
- No external runtime is activated.
- No system population occurs.
- No capability is compressed out.
