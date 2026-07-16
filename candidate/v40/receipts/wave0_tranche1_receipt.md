# Zervan v40 Candidate — Wave 0 Tranche 1 Receipt

Receipt State: LOCAL VERIFICATION COMPLETE

Candidate State: CANDIDATE ONLY

Authority: NONE

Human Gate: ACTIVE

Canonical Promotion: NOT REQUESTED

External Runtime: DISABLED

System Population: DISALLOWED

## Canonical Binding

- Repository: `https://github.com/hourxiii-cloud/Zervan-Core-v39.git`
- Canonical branch: `main`
- Canonical commit: `b9460bf2955246ff3b1f61ed0b398496d7ad49c1`
- Local implementation branch: `candidate/v40-wave0`
- Operational Contract: `OC-V40.WAVE0.TRANCHE1`

The contract binds the initiation statement, v39 canonical body, and 5.6 canonical definitions by path and SHA-256. The contract validator resolves `origin/main` and re-hashes each bound artifact before passing.

## Implemented Controls

1. Frozen P0 registry taxonomy:
   - `P0` identifies the single parent failure operation.
   - `Critical`, `High`, and `Medium` identify individual finding severity.
   - `P0-001` through `P0-040` remain stable and ordered.
   - `P0-040 — Contract Enforcement Failure` remains the parent finding.
2. Candidate schema and registry for all 40 findings, including implementation wave, primary control, acceptance evidence, and closure state.
3. Candidate Operational Contract schema and first active contract instance.
4. Candidate runtime-state and transition-event schemas.
5. Current-Git canonical binding validation by repository, branch, commit, path, and SHA-256.
6. v39 local verifier repair:
   - accepts plain or inline-code Markdown formatting;
   - tolerates a terminal period;
   - requires a complete semantic boundary line;
   - rejects wrong values and negated context.
7. 5.6 bridge validator repair:
   - output emission is opt-in;
   - default validation creates no result artifact;
   - Python syntax validation uses in-memory compilation and creates no bytecode cache.
8. Make targets for candidate validation and regression testing.

## Verification Results

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 make test-v40-candidate
PYTHONDONTWRITEBYTECODE=1 make validate-v40-candidate
PYTHONDONTWRITEBYTECODE=1 python call/verify_local_call.py
PYTHONDONTWRITEBYTECODE=1 python tools/validate_zervan_5_6_bridge.py --root .
```

Observed results:

- Candidate regression tests: PASS — 11 tests.
- Failure inventory: PASS — 40 findings; Critical 17, High 16, Medium 7.
- Operational Contract: PASS — current `origin/main` commit and three canonical artifact hashes verified.
- v39 local call verifier: PASS.
- 5.6 bridge validation: PASS.
- Default 5.6 validation changed no tracked or untracked repository state.
- Python cache artifacts after the verified run: none.

## Files Added

- `candidate/v40/README.md`
- `candidate/v40/governance/failure_inventory.schema.json`
- `candidate/v40/governance/failure_inventory.json`
- `candidate/v40/contracts/operational_contract.schema.json`
- `candidate/v40/contracts/runtime_state.schema.json`
- `candidate/v40/contracts/transition_event.schema.json`
- `candidate/v40/contracts/wave0_tranche1.operational_contract.json`
- `candidate/v40/tools/validate_failure_inventory.py`
- `candidate/v40/tools/validate_operational_contract.py`
- `candidate/v40/receipts/wave0_tranche1_receipt.md`
- `tests/test_v40_candidate_controls.py`

## Existing Files Repaired

- `call/verify_local_call.py`
- `tools/validate_zervan_5_6_bridge.py`
- `ZERVAN_5_6_VALIDATION_PROCESS.md`
- `Makefile`

## Claim Boundary

This receipt proves only that the listed candidate controls and local repairs passed the listed local checks against the bound Git state.

It does not prove that Wave 0 is complete. It does not close P0-040 or any dependent finding. It does not promote v40. It does not authorize external execution, system population, publication, or production use.

## Required Continuation

Next dependency: implement the runtime conformance monitor, transition writer, Audit interrupt behavior, route lock, and Human Gate stop state against the candidate schemas. Then add adversarial fixtures for route substitution, completion override, invariant drift, and canonical mismatch.
