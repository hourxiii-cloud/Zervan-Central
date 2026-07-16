# Zervan 5.6 Bridge — Validation Process

Status: REPRODUCIBLE VALIDATION PROCESS  
Authority: NONE  
External Runtime: DISABLED  
System Population: DISALLOWED

This file documents the validation mechanism referenced by `ZERVAN_5_6_TRANSITION_NOTE.md`.

## Validation Command

Run a read-only validation from the package root:

```bash
python tools/validate_zervan_5_6_bridge.py --root .
```

To explicitly emit a validation receipt:

```bash
python tools/validate_zervan_5_6_bridge.py --root . --emit ZERVAN_5_6_VALIDATION_RESULTS.json
```

## Validation Script

Package-local script:

```text
tools/validate_zervan_5_6_bridge.py
```

The script is read-only by default. It does not create validation files or Python bytecode caches unless receipt emission is explicitly requested. It does not activate external runtime, perform collection, populate systems, or promote authority.

## Validation Output

Optional generated artifact when `--emit` is supplied:

```text
ZERVAN_5_6_VALIDATION_RESULTS.json
```

## Checks Performed

The script validates:

- Required bridge artifacts exist.
- Required observer and sub-observer paths exist.
- JSON files parse successfully.
- Python files compile successfully.
- Canonical definition invariants are present in `ZERVAN_5_6_CANONICAL_DEFINITIONS.md`.
- Bridge and transition documents reference the canonical definitions file.
- Owl_Hoot primary observer language is present.
- The Unkindness Raven reporting-brand language is present.
- The modified-file record states that no files were deleted.

## Current Result

The current generated validation artifact reports:

```text
status: PASS
```

See `ZERVAN_5_6_VALIDATION_RESULTS.json` for the full check list.
