# Zervan v40 Candidate — Wave 0 Tranche 3 Receipt

Receipt State: LOCAL VERIFICATION COMPLETE

Candidate State: CANDIDATE ONLY

Authority: NONE

Human Gate: ACTIVE

Canonical Promotion: NOT REQUESTED

External Runtime: DISABLED

System Population: DISALLOWED

## Specification Checkpoint

- Specification: `candidate/v40/specifications/tranche3_scar_replay_continuity_specification.md`
- Specification commit: `0bfc3f19abdce996aa2e46a970bab8437cf0797a`
- Tranche-2 implementation commit: `2d75db540cd330f79e27a3baeb9ba7e4d04f30f1`
- Implementation branch: `candidate/v40-wave0`

The Tranche 3 specification was reviewed and committed before implementation. The seven implementation units were then completed sequentially without changing the specification.

## Implemented Artifacts

- `candidate/v40/contracts/scar.schema.json`
- `candidate/v40/contracts/replay_receipt.schema.json`
- `candidate/v40/runtime/continuity.py`
- `candidate/v40/runtime/control_plane.py`
- `candidate/v40/tools/validate_continuity.py`
- `tests/test_v40_candidate_continuity.py`
- `Makefile`
- `candidate/v40/receipts/wave0_tranche3_receipt.md`

## Implemented Units

1. Scar schema:
   - closed Draft 2020-12 record;
   - fixed Authority `NONE` and Human Gate `ACTIVE`;
   - explicit evidence boundary, analytical state, and continuation objects;
   - immutable null Scar continuation reference;
   - strict identifier, class, time, uniqueness, and SHA-512 fields.
2. Replay receipt schema:
   - closed preparation and decision receipts;
   - no `ACTIVE`, `RUNNING`, or `RESUMED` status;
   - state-dependent Human Gate metadata;
   - authorization requires `AUTHORIZED_NEW_CONTRACT_REQUIRED` and a continuation reference;
   - denial cannot carry a continuation reference;
   - new contract identifiers remain null.
3. Immutable Scar ledger writer:
   - complete transition-ledger validation before publication;
   - terminal-witness resolution and binding checks;
   - canonical JSON and SHA-512 integrity;
   - same-filesystem atomic, no-overwrite publication;
   - file and directory synchronization;
   - duplicate, tamper, overwrite, and partial-publication rejection.
4. Terminal-event-to-Scar reconciliation:
   - `COMPLETE`;
   - `MISSING_SCAR`;
   - `ORPHAN_SCAR`;
   - `DUPLICATE_SCAR`;
   - `BINDING_MISMATCH`;
   - `INTEGRITY_FAILURE`; and
   - `UNREADABLE`.
   - Replay binding uses the SHA-512 digest of the complete sorted Scar set without inventing a mutable Scar chain.
5. Structured repeating-thirds runtime control:
   - recognizes only `REPEATING_ONE_THIRD` and `REPEATING_TWO_THIRDS` structured markers;
   - treats detection as successful self-observation, not confidence;
   - preserves contradiction, evidence-exhaustion, recursive-failure, and unknown classification;
   - invokes the existing Audit interrupt and terminal stop path;
   - ordinary decimals, fractions, prose, quotations, and confidence objects do not trigger.
6. Minimum Replay preparation:
   - requires complete Scar reconciliation;
   - restores only explicitly supplied typed references;
   - records unavailable context instead of reconstructing it from conversation memory;
   - blocks drifted, unavailable, or invalid canonical state;
   - produces only `PREPARED`, `BLOCKED`, or `HUMAN_GATE_REVIEW` receipts;
   - cannot reopen or execute the source contract.
7. Human Gate Replay decision:
   - accepts only explicit human-owned decision metadata;
   - rejects runtime-generated approval;
   - appends a new immutable SHA-512-chained receipt;
   - permits only one decision per preparation receipt;
   - denial produces `DENIED`;
   - approval produces `AUTHORIZED_NEW_CONTRACT_REQUIRED` and a continuation reference;
   - approval creates no contract, contract instance, route execution, or active runtime.

## Acceptance Fixtures

All 38 specified Tranche 3 fixtures pass:

- 01–16: Scar creation, immutability, binding, integrity, persistence, unknown evidence, and explicit missing evidence;
- 17–22: structured repeating-thirds termination, false-positive rejection, successful self-observation, and unknown-condition preservation;
- 23–29: Replay reconciliation gate, integrity failure, canonical drift, unavailable context, terminality, non-execution, and pending Human Gate;
- 30–36: runtime-approval rejection, immutable denial and approval, continuation-only authorization, overwrite and chain failure, and temporal separation;
- 37–38: clean-tree validation and disabled external runtime/system population.

Total v40 candidate regression tests: 109.

Additional schema fixtures validate closed objects, authority preservation, state-dependent receipt constraints, malformed hashes and times, duplicate references, and Human Gate ownership.

## Verification Evidence

The following commands passed:

```text
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_v40_candidate_*.py' -v
PYTHONDONTWRITEBYTECODE=1 make validate-v40-candidate
PYTHONDONTWRITEBYTECODE=1 python call/verify_local_call.py
PYTHONDONTWRITEBYTECODE=1 python tools/validate_zervan_5_6_bridge.py --root .
```

Observed results:

- 109 v40 candidate tests passed;
- failure inventory validator passed with 40 findings;
- Operational Contract validator passed against canonical commit `b9460bf2955246ff3b1f61ed0b398496d7ad49c1`;
- Tranche 2 control-plane validator passed with no persistent output;
- Tranche 3 continuity validator passed through terminal witness, immutable Scar, and Human-Gated Replay with no persistent output;
- v39.0 local call package verification passed;
- 5.6 bridge validation passed, including 29 JSON files and 23 Python files;
- `git diff --check` passed; and
- no `__pycache__` directories or persistent validation artifacts were created.

## Claim Boundary

This receipt establishes local candidate implementation and verification only.

It does not promote v40, mutate canonical v39, close P0-040 or dependent findings, push Git, open a PR, merge a branch, activate an external runtime, populate a system, or authorize production execution.

Replay re-establishes explicit context. It does not reopen a stopped or completed source contract. Human approval produces only a continuation reference and requires a separately created, validated, reviewed, and activated Operational Contract.

## Required Continuation

The next architectural dependency is the reporting-production boundary control identified by the Tranche 2 receipt and preserved by the Tranche 3 specification. That work requires a separately reviewed specification and checkpoint before implementation.
