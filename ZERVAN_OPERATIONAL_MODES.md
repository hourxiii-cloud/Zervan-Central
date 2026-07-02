zervan-core

Doctrine-first, engine-gated, observer-driven architecture

Zervan is a doctrinal, epistemic, and architectural system designed to enforce
stability, traceability, and admissibility across analysis, interpretation,
and controlled change.

This repository exists to store and organize the artifacts that Zervan
operates over. Authority is defined elsewhere.

⸻

Authority & Canonical Truth

⚠️ Important:
This repository is not self-authoritative.

Canonical authority for Zervan is defined exclusively by DoctrineOps, governed
by Cathedral, and resolved through explicit doctrine manifests.

Specifically:
	•	Authority is defined by:
	•	DoctrineOps/DOCTRINE_MANIFEST.md
	•	Additional DoctrineOps manifests explicitly enumerated therein
	•	This repository provides:
	•	Doctrine files referenced by DoctrineOps
	•	Contracts, schemas, and tests bound by doctrine
	•	Implementation artifacts subject to doctrinal validation
	•	This repository does NOT:
	•	Define authority by location
	•	Override doctrine via implementation
	•	Grant canonical status by existence alone

If an implementation or document in this repository contradicts doctrine,
the implementation is wrong.

⸻

Repository Identity & INIT Binding (Zero Trust)

This repository is location-addressable but not location-authoritative.

For purposes of initialization (INIT), reproducibility, and zero-trust execution:
	•	Canonical identity of this repository is bound by:
	•	Repository URL (informational only)
	•	Exact Git commit SHA (authoritative)
	•	Optional tree hash or manifest hash (content integrity)
	•	INIT statements MUST NOT rely on:
	•	Branch names
	•	Tags
	•	Repository location alone
	•	Local clones or forks

An INIT binding MAY take the form:

zervan_core:
  repo_url: https://github.com/<org>/zervan-core
  commit_sha: <40-hex>
  doctrine_manifest_hash: <sha512>   # optional but recommended
  
The canonical INIT fingerprint is the hash of the canonicalized INIT payload,
not the repository URL.

This ensures:
	•	deterministic recomputability
	•	ephemerality safety
	•	zero-trust execution
	•	drift prevention

⸻

Role of This Repository

This repository serves as the canonical storage location for:
	•	Zervan doctrine files (as referenced by DoctrineOps)
	•	Architectural contracts and schemas
	•	Engine, module, and observer implementations
	•	Tests, diagnostics, and tooling

“Canonical” in this context means:

Referenced, versioned, and validated by DoctrineOps — not self-authorizing.

No local clone, fork, export, mirror, or copy supersedes doctrine-defined authority.

⸻

Doctrine First (Precedence Model)

Zervan operates under a strict precedence model:
	1.	Cathedral — root governance and admissibility
	2.	DoctrineOps manifests — authority resolution and load order
	3.	Doctrine files — executable truth
	4.	Architecture & contracts — binding structure
	5.	Implementations & tests — subject to validation

Any deviation from this order is invalid.

⸻

Final Clarification

This repository is:
	•	Content-addressable
	•	Doctrine-governed
	•	INIT-bindable
	•	Zero-trust compatible

It is not:
	•	an authority source
	•	a trust anchor
	•	a governance substitute

Zervan trusts process and proof, not repositories.

---

5.6 Bridge Mode Clarification

5.6 bridge review is a controlled compatibility/deployment-path review.

It does not authorize external runtime, system population, authority promotion, doctrine replacement, or capability compression.

The full Zervan spine remains:

```text
INIT → SIGNAL / Signal Ecology → DELTA → K9 / Pups → FAMILY / Teams →
TRAVERSAL → VERIFICATION → ANALYTICAL → CREATIVE → GOVERNANCE
```

Primary modules produce evidence. Primary observers perceive evidence and context. Controlled sub-observers pressure evidence. Raven reports what survives. Audit records what fails.
