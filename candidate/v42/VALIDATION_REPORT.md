# Candidate v42 Validation Report

## Identity

- Baseline: `vTemporal.41.0`
- Baseline commit: `ae898ab803061823b36fb825e0664e3d8d255409`
- Candidate branch: `candidate/v42-governed-development`
- Authority: NONE
- Human Gate: ACTIVE
- Canonical: FALSE

## Candidate validation

Commands:

```text
make validate-v42-candidate
make test-v42-candidate
```

Result:

- generated-artifact drift check: PASS
- positive aggregate fixture: PASS
- hostile negative fixture rejection: PASS
- candidate unit/integration tests: 26 passed, 0 failed, 0 errors
- Python compilation: PASS
- Git whitespace validation: PASS

Covered failures include false trigger, Harmony scheduling, force escalation,
AnimalKingdom contract mismatch, carrier self-admission, external action, in-run mission
expansion, contamination laundering, false object restoration, truth promotion,
standing delegation, carrier substitution, evidence-ceiling increase, object identity
divergence, invented mission, lossy closure, and removal fail-closed behavior.

## Canonical-suite comparison

The complete existing repository suite was run independently on canonical `main` and
on the candidate branch.

Canonical `main` result at the baseline commit:

- 1,803 tests
- 30 failures
- 23 errors

Candidate branch result before any canonical-file mutation:

- 1,803 existing tests
- 32 failures
- 23 errors

The two additional failures are branch-name assertions that require the active branch
to be exactly `main`. They are expected on any candidate branch. The remaining failures
and errors reproduce on unmodified canonical `main`; they include stale pre-promotion
expectations, a deleted or unavailable `origin/candidate/v41-complete` reference, and
v40 contracts bound to an older canonical commit.

Disposition:

`NO NEW FUNCTIONAL CANONICAL REGRESSION DETECTED`  
`BASELINE SUITE NOT CLEAN`  
`BASELINE FAILURES PRESERVED / NOT REPAIRED BY v42`

Candidate v42 does not claim that the existing canonical suite is green.

## Promotion boundary

This report establishes candidate implementation evidence only. It does not authorize
canonical promotion, alter `VERSION`, or rewrite canonical v41 failures.

