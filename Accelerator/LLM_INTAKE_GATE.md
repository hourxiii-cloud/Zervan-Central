ZERVAN — LLM INTAKE GATE (Dataset Admission)

Version: 1.1.0
Status: CANONICAL • NON-OPTIONAL
Authority Class: Governance / Admission Control
Mode: READ-ONLY ADMISSION (No mutation, no inference)

⸻

0. Purpose

This document defines the only approved workflow for admitting external datasets
into Zervan through an LLM-mediated interface.

The Intake Gate exists to:
	•	Establish dataset identity
	•	Enforce integrity and determinism prerequisites
	•	Classify artifact type and evidence class
	•	Bind datasets to contracts, guardrails, and engines
	•	Prevent implicit ingestion or authority inference

The Intake Gate is not analysis.
The Intake Gate is not PMC.
The Intake Gate is not MC.

It is admission only.

⸻

1. Intake Boundary (Hard)

1.1 Allowed Inputs

Accepted:
	•	User uploads dataset directly into the LLM session
	•	Single file or archive (e.g., ZIP)

Rejected:
	•	Local filesystem references
	•	URLs as substitutes for upload
	•	Repository crawling
	•	“Assume you already have my data”
	•	Implicit or inferred datasets

If the dataset is not uploaded in-session:

→ REJECT

⸻

2. Intake Receipt (Mandatory, Deterministic)

For every dataset presented, the system MUST emit an Intake Receipt.

2.1 Required Receipt Fields

The Intake Receipt MUST include:

Identity
	•	Original filename(s)
	•	File size (bytes)
	•	Cryptographic hashes:
	•	SHA-512 (REQUIRED)
	•	SHA-256 (OPTIONAL, if policy allows)

Format & Shape
	•	Detected format (CSV / JSON / Parquet / ZIP / other)
	•	Compression/container type (if any)

Structural Summary
	•	Row count (when applicable)
	•	Column count (when applicable)
	•	Schema snapshot:
	•	Column names
	•	Inferred data types

Quality Indicators
	•	Missingness summary (top offenders)
	•	Obvious structural anomalies (best-effort)

Risk Scan (Best-Effort, Non-Authoritative)
	•	Obvious credential/secrets patterns
	•	Obvious PII indicators

If any element cannot be computed:
	•	It MUST be explicitly marked UNAVAILABLE
	•	No inference or substitution is allowed

⸻

3. Artifact Classification (Required)

The Intake Gate MUST explicitly classify:
	•	Artifact Class
	•	Dataset / Archive / Signal / Other
	•	Evidence Class
	•	PRIMARY (original uploaded bytes)
	•	DERIVED (only if explicitly generated later)
	•	Intended Consumers
	•	Engines / Modules potentially eligible (non-binding)

Misclassification or ambiguity:

→ REJECT

⸻

4. Chunking & CAS Preconditions

4.1 When Chunking Is Required

Chunking MUST be invoked (and declared at intake) when:
	•	Dataset size exceeds practical in-memory analysis bounds
	•	Partial, distributed, or replayable analysis is expected
	•	CAS-addressed sub-artifacts will be produced
	•	Deterministic recomposition is required

If chunking is required but not declared:

→ REJECT

⸻

4.2 Required Chunking Profile

When chunking is invoked, the Intake Gate MUST declare:
	•	Chunking Method ID
	•	zervan://chunking/fastcdc/1 (Baseline Profile A)
	•	Confirmation that:
	•	Determinism contract applies
	•	Profile parameters are immutable

Missing required chunking profile artifacts:

→ REJECT

⸻

4.3 CAS ↔ Chunking Binding

If chunking or CAS will be used, the Intake Gate MUST verify the existence of:
	•	/CAS_CHUNK_MANIFEST.md

This manifest governs:
	•	Chunk identity binding
	•	Recomposition requirements
	•	Non-authority of storage

Missing binding manifest when required:

→ REJECT

⸻

5. Admission Decision (Contracts-First)

The Intake Gate MUST emit exactly one decision:
	•	ADMIT
	•	ADMIT-WITH-RESTRICTIONS
	•	REJECT

5.1 Decision Requirements

The decision MUST:
	•	Cite violated or satisfied contracts
	•	Reference guardrails when applicable
	•	Declare any imposed restrictions (column exclusions, mode limits, etc.)

No hedging.
No “probably safe.”
No implied continuation.

⸻

6. Execution Mode Declaration (Non-Inferential)

If a label column exists and is explicitly identifiable:
	•	Supervised paths MAY be declared admissible

If no label column exists:
	•	Unsupervised / anomaly paths ONLY

Rules:
	•	No label invention
	•	No semantic guessing
	•	No column meaning inference

⸻

7. MC Boundary (Hard Separation)

The Intake Gate MUST NOT:
	•	Invoke Meta Collapse (MC)
	•	Classify response types
	•	Frame escalation, action, or governance outcomes
	•	Assess “what should be done”

MC occurs only after PMC, never before.

Any attempt to drag MC upstream:

→ CATEGORY ERROR → REJECT

This preserves the separation:

admission → truth → permission → action

⸻

8. Beagle Binding (Gate 0)

Successful intake results in a Beagle Admission Request, including:
	•	Intake Receipt
	•	Admission Decision
	•	Declared chunking/CAS requirements
	•	Artifact classification

Beagle performs:
	•	Integrity verification
	•	Determinism enforcement
	•	Hash validation
	•	Final admission or rejection

If Beagle rejects:

→ EXECUTION HALTS

⸻

9. Output Proof (Dry-Run Artifact)

For each intake, the system MUST emit a non-executable proof artifact:

/tests/dry_run_00X_<dataset_name>.md

It MUST record:
	•	Intake Receipt
	•	Admission Decision
	•	Declared execution path(s)
	•	Required contracts/modules
	•	Explicit rejections (if any)

This artifact is diagnostic only and non-authoritative.

⸻

10. Final Constraint

No dataset may proceed to analysis unless:
	•	Intake Receipt is complete
	•	Admission Decision is explicit
	•	Chunking/CAS prerequisites are satisfied (when required)
	•	Beagle admission succeeds

If certainty cannot be established:

→ FAIL CLOSED

⸻

End of Document
