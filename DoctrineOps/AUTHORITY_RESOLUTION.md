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

9. R1-A — Canonical Implementation Resolution

Canonical implementation resolution and doctrinal authority are separate concerns.

The active canonical implementation baseline is resolved from the repository's
canonical branch, `main`, at a specific commit.

Git `main` may:
    • identify the active canonical implementation set
    • bind implementation state to a concrete commit
    • distribute and preserve canonical artifacts
    • provide repository evidence for version and implementation resolution

Git `main` may not:
    • create doctrinal truth by repository placement alone
    • elevate a lower authority-class artifact
    • override Cathedral, DoctrineOps, or Doctrine
    • resolve doctrinal contradiction merely because a file is committed

A development, candidate, recovery, or feature branch is non-canonical until
promotion is explicitly authorized and completed.

Canonical implementation resolution therefore answers:

    Which implementation state is active?

Authority resolution answers:

    Which artifact governs when assertions conflict?

These questions MUST NOT be collapsed into one another.

⸻

10. Runtime Authority

Runtime authority is a separate axis from artifact and doctrinal authority.

Unless a valid governing state explicitly resolves otherwise:

    Runtime Authority: NONE

Runtime Authority: NONE means that an analytical runtime, engine, model,
observer, module, capability, or conversation possesses no independent authority
to authorize external action, canonical mutation, publication, certification,
or downstream execution.

Runtime Authority: NONE does not demote or nullify the authority class of
Cathedral, DoctrineOps, Doctrine, Interfaces, Contracts, or other canonical
artifacts.

Artifact authority governs what is controlling truth within Zervan.

Runtime authority governs what the executing runtime itself is permitted to do.

The two MUST NOT be conflated.

⸻

11. Human Gate

Human Gate is the controlled authorization boundary for governed transitions.

Unless a valid governing state explicitly resolves otherwise:

    Human Gate: ACTIVE

Human Gate may approve or reject, when otherwise admissible:

    • canonical mutation
    • candidate promotion
    • publication
    • authorized downstream execution
    • other explicitly Human-Gated transitions

Human Gate does not:

    • manufacture truth
    • override Cathedral or DoctrineOps
    • convert an inadmissible state into an admissible state
    • erase provenance or unresolved contradiction
    • replace PMC, MC, Audit, Registry, Governance, or other bounded functions
    • itself constitute execution of an approved action

A Human Gate decision MUST remain attributable as governance state.

Approval and execution remain distinct events.

⸻

12. Mutation Authority

Technical ability to modify a file, branch, repository, system, or artifact
does not constitute authority to perform that mutation.

Canonical mutation requires all of the following:

    • an explicitly identified canonical target
    • an admissible proposed change
    • preserved provenance
    • satisfied required validation
    • explicit mutation authorization
    • Human Gate approval where required
    • a recorded resulting state

Candidate and development surfaces may be modified within their authorized
scope without becoming canonical.

Mutation of a candidate does not constitute promotion.

Mutation of a repository does not create doctrinal authority.

Write capability is capability only.

⸻

13. Promotion Authority

Promotion is a governed state transition from non-canonical candidate state to
canonical implementation state.

Promotion requires, at minimum:

    • explicit candidate identity
    • explicit canonical target
    • provenance for the proposed change
    • required validation evidence
    • known conflicts and unresolved conditions surfaced
    • applicable completeness or acceptance conditions satisfied
    • Human Gate approval
    • actual canonical repository mutation
    • a verifiable resulting canonical state

The following do not constitute promotion:

    • candidate existence
    • branch creation
    • successful file write
    • commit creation
    • push capability
    • pull-request creation
    • test availability without test execution
    • model confidence
    • human intent that has not crossed the required gate
    • naming an artifact "canonical"

No system may report promotion as complete before the required transition
evidence exists.

⸻

14. Default and Resolved State Precedence

A default is an entry state or fallback state only.

A default governs only while the relevant state is genuinely undefined.

When a valid governing source explicitly resolves that state, the resolved
state supersedes the default for its authorized scope and duration.

Therefore:

    DEFAULT < VALID RESOLVED STATE

A runtime MUST NOT remain at, revert to, or reassert a default merely because
the default is easier, more familiar, or globally available.

A resolved state remains controlling until:

    • its defined scope ends
    • it is explicitly superseded
    • it is revoked
    • its validity condition fails
    • a higher-authority governing state lawfully replaces it

When the resolved state ceases to apply and no replacement exists, the
appropriate default may again govern.

Defaults may never be used to erase provenance, bypass a Human Gate, defeat an
active contract, or silently reset established state.

⸻

15. R1-A Separation Invariant

The following are independent control dimensions and MUST remain separately
resolvable:

    • canonical implementation resolution
    • artifact / doctrinal authority
    • runtime authority
    • Human Gate state
    • mutation authorization
    • promotion authorization
    • default state
    • currently resolved state

No outer capability may redefine, merge, or locally override these dimensions.

No Room identity, branch semantics, merge semantics, state-root semantics,
authorized-view semantics, or capability-local behavior is defined by R1-A.

Those surfaces remain downstream and unresolved until their prerequisite
contracts are established.

⸻

16. Canonical Statement

Truth is not where it is stored.
Truth is where authority is resolved.

Implementation is not authority.
Capability is not authorization.
Approval is not execution.
A default is not authority over a resolved state.

— End of Document —
