# ZERVAN PKI / ECC DOCTRINE

**Version:** 1.0.0  
**Status:** ACTIVE  
**Authority:** Zervan Doctrine Layer  
**Applies To:** All Zervan repositories, environments, operators, and evaluators  
**Supersedes:** Ad-hoc key handling, implicit trust, undocumented identity flow

---

## 1. Purpose

This doctrine defines the cryptographic identity model used by Zervan systems.

Its purpose is to ensure that:

- Identity is provable
- Authorization is scoped
- Integrity is verifiable
- Trust is never implicit
- Code is not the source of truth

Cryptography exists to preserve truth under motion, not to decorate systems.

---

## 2. Core Principle

**Identity must remain stable while everything else changes.**

All PKI / ECC behavior in Zervan is evaluated against this principle.

Any mechanism that obscures identity is rejected, regardless of convenience.

---

## 3. Cryptographic Foundation

### 3.1 Authorized Algorithm

Zervan exclusively authorizes:

- **ECC / ED25519**

Rationale:
- Deterministic behavior
- Compact, auditable keys
- Modern security margin
- Explicit identity binding

RSA and hybrid fallback mechanisms are not authorized for Zervan identity.

---

## 4. Identity Domain Separation

Zervan enforces strict separation of identity domains.  
No domain may impersonate or collapse into another.

| Domain | Description | Example |
|------|------------|--------|
| Operator Identity | Human or service actor | GitHub Account |
| Transport Identity | Secure channel | SSH |
| Authorization Surface | Access control | GitHub permissions |
| Content Identity | State of truth | Repository fingerprint |
| System Identity | Logical evaluator | Zervan PMC |

Violation of domain separation constitutes a doctrine breach.

---

## 5. Cryptographic Envelope

A **cryptographic envelope** is the complete chain of identity preservation from operator intent to content state.

An envelope is considered **closed** when all of the following are true:

1. Operator authenticates via ECC key
2. Transport verifies identity without fallback
3. Authorization grants explicitly scoped access
4. Content is retrieved without mutation
5. Repository fingerprint remains stable

If any step fails, the envelope is open and invalid.

---

## 6. Fingerprints and Non-Equivalence

Zervan recognizes multiple fingerprints, each representing a different truth.

They must never be compared for equality.

| Fingerprint Type | Represents |
|-----------------|------------|
| SSH key fingerprint | Public key material |
| GitHub key fingerprint | Authorized identity |
| Repository fingerprint (SHA256) | Content truth state |
| PMC seal fingerprint | Admitted evidence |

Treating one fingerprint as another is a category error, not a cryptographic failure.

---

## 7. Authorization Rules

### 7.1 Allowed

- ECC authentication via SSH
- Authorization via GitHub account keys or deploy keys
- Read/write access strictly scoped
- Multiple keys per operator
- Key rotation without content mutation

### 7.2 Forbidden

- Committing private keys
- Sharing keys across identity domains
- Relying on implicit SSH agent state
- Mixing transport identity with content identity
- Accepting fallback authentication silently

---

## 8. Key Lifecycle Doctrine

### 8.1 Creation

- Keys are generated locally
- Private material never leaves origin
- Public material is explicitly registered

### 8.2 Registration

- GitHub Account Keys → operator authorization
- Deploy Keys → repository-scoped authorization

### 8.3 Rotation

Key rotation is routine, not exceptional.

Rotation must not:
- Change repository fingerprints
- Invalidate prior PMC seals
- Rewrite historical truth

---

## 9. Zervan PMC Integration

Zervan does not trust cryptography blindly.

Cryptographic success is necessary but insufficient.

The PMC evaluates:
- Repository integrity
- Fingerprint stability
- Admission conditions
- Evidence continuity

Only after PMC admission does cryptographic identity become operational truth.

---

## 10. Smoke Testing as Cryptographic Validation

Smoke tests validate cryptographic envelope closure, not functionality.

A valid smoke test confirms:
- Identity continuity
- Authorization correctness
- Content immutability
- Deterministic evaluation

Smoke logs are evidence artifacts, not build artifacts, and are not committed by default.

---

## 11. Failure Classification

| Symptom | Interpretation |
|------|---------------|
| Permission denied | Authorization failure |
| Key mismatch | Identity scope error |
| Hash mismatch | Domain confusion |
| Repository fingerprint change | Content mutation |
| PMC rejection | Truth invalidation |

Not all failures are cryptographic. Most failures are conceptual.

---

## 12. Doctrine over Code

Code implements doctrine. Doctrine never chases code.

If behavior is not defined in doctrine, it does not exist, regardless of implementation.

This document is the highest authority for PKI / ECC behavior in Zervan.

---

## 13. Final Assertion

Zervan systems do not trust keys.  
They trust preserved truth.

Cryptography is a tool.  
Doctrine is the system.

---

**ZERVAN PKI / ECC DOCTRINE — SEALED**
