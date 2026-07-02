# crypto/policies — Zervan Crypto Policies

This directory contains **canonical cryptographic policy artifacts** that govern
hashing, signing, verification, and byte-level canonicalization for Zervan envelopes.

These files are **control-plane constraints**:
- they do **not** define doctrine truth
- they **do** constrain what signatures/hashes are valid
- they **must** be enforced by verifiers (e.g., `runtime/zervan_verify.py`)

---

## Primary Policy

### `crypto_policy.yaml`
**Purpose:** Pin allowed algorithms, key constraints, signature requirements, hashing rules,
canonicalization binding, and verifier enforcement gates for Zervan envelopes.

Key policy anchors (as currently defined):
- Policy identity: `policy.id: zervan://crypto/policy/1`
- Version: `policy.version: 1.0.0`
- Canonicalization binding: `canonicalization.envelope.version: zervan://crypto/canonicalization/envelope/1`
- Signed-scope float rule: `canonicalization.envelope.forbid_signed_scope_floats: true`
- Hashing algorithm: `SHA-512` for canonical hashes and CAS IDs
- Signature preimage: sign **raw 64-byte SHA-512 digest bytes** (not hex text)
- Allowed signature algorithms:
  - `RSA-PSS-SHA512` (min 3072, MGF1-SHA512, salt_length=hash)
  - `ECDSA-SHA512` (curves: `secp256r1`, `secp384r1`)
- Envelope enforcement (examples):
  - `manifest` requires signature scope `full_envelope` and signature set `manifest_minimum`
  - `proof` uses the same canonicalization version; verifier signature may be optional until enforced

---

## Relationship to Envelope Canonicalization

Canonicalization defines **what exact bytes are signed**.

`crypto_policy.yaml` binds:
- which canonicalization version must be used for envelope types
- which envelope types must be signed (and by what roles)
- how the signature preimage is formed (SHA-512 digest bytes)

Verifiers MUST reject envelopes that violate policy gates, including:
- canonicalization version mismatch
- signed hash mismatch vs recomputed canonical hash
- invalid signatures or missing required roles
- CAS references that do not hash to declared IDs (when artifacts are available)

---

## How Policies Are Referenced (Recommended)

Policies SHOULD be referenced by **hash** in signed scopes to prevent silent substitution.

Recommended pattern:
- compute `policy_ref = sha512:<hex128>` over the policy file bytes (exact bytes)
- include `policy_ref` in the envelope’s signed scope (or full envelope if required)
- verifier checks that:
  - the referenced `policy_ref` matches the policy bytes used during verification
  - the envelope’s declared canonicalization version matches policy expectations

(If policy references are not yet present in schemas, add as a forward-compatible field
in signed scopes and have verifiers enforce when available.)

---

## Update & Governance Rules

1. **Fail closed:** Unknown algorithms, unknown roles, or unmet required signature sets MUST fail verification.
2. **No silent drift:** Any policy update must be explicit and reviewable.
3. **Version bump:** Changes to allowed algorithms, key constraints, signing scope rules, or verification gates MUST bump `policy.version`.
4. **Verifier alignment:** `runtime/zervan_verify.py` (or equivalent) MUST be updated (if necessary) to enforce the updated policy gates.
5. **Reproducibility:** Canonicalization + hashing rules must remain deterministic across machines.

---

## Operational Notes

- Policies constrain **verification** and **signature validity**; they do not grant authority by themselves.
- Private key material is never stored here.
- Certificates may be allowed per policy (`keys.certs.allow_x509: true`); chain references should be hash-addressed.

---

## Quick Checks (Suggested)

- Verify policy file hash:
  - `sha512sum crypto/policies/crypto_policy.yaml`
- Run verifier in strict mode (if present):
  - `make verify` (or `python runtime/zervan_verify.py --strict`)

If verification does not consume this policy, then the policy is **not enforced**—it is documentation only.'
