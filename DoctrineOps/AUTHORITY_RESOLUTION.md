AUTHORITY_RESOLUTION — Canonical Authority & Precedence

Status: CANONICAL • NON-OPTIONAL • GOVERNANCE-CRITICAL
Classification: DoctrineOps
Applies to: All Zervan executions, interpretations, accelerators, engines, modules, observers, demonstrations, tests, and exploratory analysis

⸻

0. Purpose

This document defines the exclusive authority model for Zervan.

It answers one question only:

When multiple artifacts appear to assert truth, which one governs?

Any system state that violates this resolution is inadmissible under Cathedral.

⸻

1. Canonical Authority Classes

All Zervan artifacts belong to exactly one authority class.

Authority classes are totally ordered.
No artifact may exist outside this ordering.

Authority Classes (Highest → Lowest)

1. Cathedral

Root governance doctrine. Final arbitrator.

⸻

2. DoctrineOps

Canonical manifests, inventories, and authority wiring that define:
	•	what doctrine exists
	•	how doctrine is loaded
	•	which governance-critical surfaces must exist
	•	how conflicts are resolved
	•	what absence halts execution

⸻

3. Doctrine

Executable epistemic law, including:
	•	ZEA
	•	ZEE
	•	ZSD
	•	PMC
	•	MC
	•	ORABORUS
	•	PMC_ARENA
	•	Domain doctrine only when activated by DoctrineOps

Doctrine does not self-authorize.

⸻

4. Interfaces & Contracts

Canonical boundaries between doctrine layers and execution surfaces, including:
	•	PMC ↔ MC interface contracts
	•	Intake gate contracts and admissibility interfaces
	•	Engine, module, and observer contracts
	•	Normalizer contracts (when invoked)
	•	Envelope schemas governing signed scopes
(manifest, run_plan IR, proof, diagnostics references)
	•	Verifier interface boundaries
	•	Hydration specification and hydration packet contract

Interfaces & Contracts:
	•	define lawful data flow and boundary semantics
	•	are non-bypassable when required by DoctrineOps
	•	do not define doctrine truth
	•	do not override Doctrine, DoctrineOps, or Cathedral

⸻

5. Initialization Artifacts

Bootstrapping and constraint declarations, including:
	•	LLM_INIT
	•	CONTEXT_PACK
	•	LLM_DELTA
	•	LLM_INTAKE_GATE

Initialization artifacts are authoritative only for:
	•	execution mode
	•	mutation permissions
	•	admissibility constraints
	•	initialization load posture

Initialization artifacts are not authoritative for:
	•	doctrine content
	•	equations or operational physics
	•	architectural truth
	•	governance logic

⸻

6. Guardrails / Policy

Binding operational constraints that limit what may execute, not what is true.

Includes:
	•	Zervan Guardrails
	•	Artifact-class operator eligibility constraints
	•	Crypto policy (algorithms, keys, signing rules)
	•	Canonicalization enforcement gates
	•	Domain separation constraints

Guardrails / Policy:
	•	may abort execution (fail closed)
	•	may force rejection under MC
	•	may never assert doctrine truth
	•	may never override Doctrine, DoctrineOps, or Cathedral

⸻

7. Repositories & Storage Locations

Organizational containers only:
	•	GitHub
	•	local clones
	•	archives
	•	buckets

Never authoritative.

⸻

2. Precedence Rule (Non-Negotiable)

When two artifacts conflict:

The artifact in the higher authority class ALWAYS dominates.

There are:
	•	no exceptions
	•	no local overrides
	•	no contextual reinterpretations

Lower-class artifacts must yield or be invalidated.

⸻

3. Repository Demotion Rule

Repositories:
	•	may contain canonical artifacts
	•	may version canonical artifacts
	•	may distribute canonical artifacts

Repositories may not:
	•	assert authority
	•	define canon
	•	override doctrine
	•	resolve contradictions

Any document claiming “this repository is authoritative” is non-canonical unless explicitly scoped by DoctrineOps.

⸻

4. Initialization Artifact Scope

Initialization artifacts are canonical only for:
	•	execution mode
	•	mutation permissions
	•	admissibility constraints
	•	initialization load posture

They are not authoritative for:
	•	doctrine content
	•	equations
	•	architectural truth
	•	governance logic

If an initialization artifact conflicts with:
	•	Cathedral, or
	•	DoctrineOps manifests

→ Initialization is invalid and execution must halt.

⸻

4.1 Hydration Scope (Execution Projection)

Hydration artifacts define the lawful projection of Zervan execution into constrained runtimes
(including LLM evaluation sessions) without expanding authority.

Hydration artifacts are classified as Interfaces & Contracts.

Rules:
	•	Hydration is REQUIRED outside the native control plane
	•	Only hydrated artifacts may be visible at runtime
	•	Hydration artifacts are non-authoritative and ephemeral
	•	Hydration may not redefine doctrine, authority, precedence, or eligibility
	•	Hydration may not be used to infer or crawl a repository

If hydration is required and missing → execution must halt.

⸻

5. DoctrineOps Supremacy Rule

DoctrineOps artifacts:
	•	define which doctrine exists
	•	define doctrine load order
	•	define doctrine completeness requirements
	•	define required governance surfaces

If a doctrine file:
	•	is not listed in a DoctrineOps manifest, or
	•	is listed but missing

→ Execution must halt.

DoctrineOps governs doctrine existence.
Doctrine does not self-authorize.

⸻

6. No Implicit Authority Rule

Authority must be explicitly declared and located.

The following confer zero authority:
	•	file names
	•	directory placement
	•	human intent
	•	model memory
	•	prior runs
	•	confidence
	•	popularity
	•	“it worked last time”

If authority is not resolved by this document and DoctrineOps manifests, it does not exist.

⸻

7. Mode Invariance

This authority model applies identically to:
	•	humans
	•	engines
	•	LLMs
	•	accelerators
	•	demonstrations
	•	tests
	•	exploratory analysis

There is:
	•	no demo exception
	•	no “thinking out loud” exception

⸻

8. Cathedral Enforcement Clause

Any contradiction across authority classes triggers:
	•	immediate inadmissibility
	•	execution halt
	•	no output production

Silent contradiction is forbidden.
Ambiguity without declaration is forbidden.

⸻

9. Canonical Statement

Truth is not where it is stored.
Truth is where authority is resolved.

— End of Document —
