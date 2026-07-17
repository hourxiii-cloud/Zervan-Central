# ZERVAN — EQUATIONS WIRE MAP (PASS 1 + PASS 2)
Version: 1.0  
Mode: CONTROLLED  
Posture: READ-ONLY  
Discovery: DISABLED  
Mutation: DISALLOWED  
Invention: DISALLOWED  
Authority Inference: DISALLOWED  
Fail-Closed: ENABLED  

Observer State (Pass 2): UNHYDRATED • NON-CANONICAL (context only)

---

## 0) Legend

### Node Types
- **Eq#** = deterministic equation / function (pure, parameterized)
- **A#** = artifact (file output)
- **H(x)** = SHA-512 hash of bytes of x
- **→** produces
- **↤** consumes
- **[GATE]** = fail-closed boundary

### Control-plane vs Data-plane
- **Control-plane artifacts**: declarations, manifests, parameter records (readable, minimal)
- **Data-plane evidence**: raw bytes / chunks (never emitted as content; only referenced by identity hash)

### Identity authority
- **Beagle** is authoritative for evidence identity hashing (dataset/chunk bytes).
- **LeafcutterAnt** is authoritative only for admission decisions (bounds + routing).

---

# PASS 1 — ANALYSIS + FIRST COLLAPSE (Canonicalizable → Canonical Commitment Record)

## A) Admission Pre-Gate (Project_LeafcutterAnt) — BEFORE Beagle

### Eq0.1 — Bound Measurement
**Eq0.1:** `bounds = measure(file_handle | manifest_handle)`  
Outputs (minimum):
- `byte_size`
- optional: `row_count` (only if parseable without inference)

### Eq0.2 — Chunk Decision
**Eq0.2:** `decision = decide_chunk(bounds.byte_size, thresholds)`  
Outputs:
- `chunking_required ∈ {true,false}`
- if true: `engine_ref`, `profile_ref`, `target_chunk_bytes`

### A0 — admission_declaration.json (control-plane)
Contains (minimum):
- `filename`
- `byte_size`
- `row_count?`
- `chunking_required`
- `threshold_used`
- `engine_ref?`
- `profile_ref?`
- `target_chunk_bytes?`
- `declared_by`
- `timestamp`
- mode/posture flags (optional but recommended)

### Eq0.3 — Admission Declaration Hash
**Eq0.3:** `A0_hash = H( canonical_json(A0) )`  
- This binds the *decision*, not the evidence bytes.

### A0h — admission_declaration.sha512
- contains `A0_hash`

### [GATE] Admission Fail-Closed
Hard halt if any of the following:
- missing `byte_size`
- contradictory declaration fields
- chunking decision cannot be evaluated against thresholds
- malformed declaration

---

## B) Evidence Identity (Beagle) — Authoritative Identity Sealing

### Eq1.1 — Evidence Identity Hash (authoritative)
Unchunked:
- **Eq1.1a:** `dataset_hash = H(raw_bytes(dataset))`

Chunked:
- **Eq1.1b:** for each chunk `c`: `chunk_hash[c] = H(raw_bytes(c))`

### Eq1.2 — Chunked Dataset Root Hash (authoritative)
**Eq1.2:**  
`root_hash = H( concat( order_index || chunk_id || chunk_hash[chunk_id] ) in canonical order )`

### A1 — dataset_identity.json
Minimum fields:
- `evidence_type`: {unchunked|chunked}
- `dataset_hash` OR `root_hash`
- if chunked: `chunk_hash_list_ref`
- `engine_ref/profile_ref` (if chunked)
- linkage: `A0_hash` (admission declaration hash)
- mode/posture flags

### A2 — chunk_hashes.sha512list (chunked only)
- ordered list: `order_index, chunk_id, chunk_hash`

### Eq1.3 — Schema Snapshot (verification artifact)
**Eq1.3:** `schema = snapshot_schema(dataset)`  
Outputs (deterministic):
- columns, dtypes
- null counts
- basic cardinality summaries where appropriate  
If not parseable: emit NOT_APPLICABLE reason.

### A3 — schema_snapshot.json

### Eq1.4 — Dataset Fingerprint (deterministic summary)
**Eq1.4:** `fp = fingerprint(dataset; params)`  
Outputs (deterministic, documented params):
- row/column counts
- descriptive stats (bounded set)
- missingness summary  
(Do not introduce interpretation.)

### A4 — dataset_fingerprint.json

### [GATE] Identity Fail-Closed
Hard halt if:
- cannot compute authoritative evidence identity hash (dataset_hash/root_hash)
- required identity artifacts missing or contradictory

---

## C) PASS 1 Analysis Helix — Deterministic Metrics (Derived Evidence)

> Only deterministic computations are allowed. Every parameter must be recorded.

### Eq2.0 — Transform / Feature Derivation
**Eq2.0:** `X = transform(data; params)`  
- deterministic preprocessing / vectorization

### Eq2.A — Anomaly Score
**Eq2.A:** `s_anom(i) = f_anomaly(X_i; params)`  
Outputs:
- anomaly score per line item (or per event)

### Eq2.T — Threat Score
**Eq2.T:** `s_threat(i) = f_threat(X_i; params)`  
Outputs:
- threat score per line item (or per event)

### Eq2.N — Neighborhood / DM-KNN Smoothing (if used)
**Eq2.N1:** `N_k(i) = kNN(X_i; k, metric)`  
**Eq2.N2:** `s_smooth(i) = aggregate( s_threat(j) for j in N_k(i); weights )`  
**Eq2.N3:** `neighbor_ratio_threat(i) = |{j∈N_k(i): label(j)=threat}| / k`

### Eq2.H — Hidden Threat Candidate Rule (example form)
**Eq2.H:**  
`hidden(i) = (label(i)=benign) ∧ (s_smooth(i) ≥ τ) ∧ (neighbor_ratio_threat(i) ≥ ρ)`  
- Note: exact predicate depends on run parameters; must be recorded.

### Eq2.I — Insider Threat Applicability Gate
**Eq2.I:** `insider_applicable = has_identity_and_cadence_substrate(data)`  
If false:
- Insider Threat output MUST be `NOT_APPLICABLE` with reason.

### Derived Artifacts (typical)
- **A5** `scores_anomaly.(csv|jsonl)`
- **A6** `scores_threat.(csv|jsonl)`
- **A7** `hidden_candidates.(csv|jsonl)`
- **A8** `neighborhood_stats.json` (if Eq2.N used)
- **A9** `model_params.json` (all params, versions, seeds if any)

### [GATE] Determinism Contract
Hard halt if:
- parameters are missing
- nondeterministic behavior is introduced without explicit control
- derived artifacts cannot be linked to dataset identity hash

---

## D) PASS 1 Governance Helix — PMC → CCR → MC

### Eq3.PMC — World Utility Scoring & Selection
Define worlds (minimum):
- Conservative
- Balanced
- Aggressive
(+ optional additional worlds as configured)

**Eq3.PMC:**  
`U(world) = w1*FN_cost + w2*FP_cost + w3*audit_risk + w4*ops_load`  
PMC must:
- select exactly **one** world `W*`
- reject all others with explicit reasons

### A10 — PMC1_world_record.json
Must include:
- worlds evaluated
- criteria, weights (or qualitative rubric)
- selected world
- explicit rejections

### Eq3.CCR — Canonical Commitment Record Construction (Collapse #1)
**Eq3.CCR:** `commit = collapse(metrics, W*; TopN=25, stable_ties=true)`  
Outputs:
- severity-prioritized risk statements (pre-observables)
- Top N line items per category (default 25)
- explicit NOT_APPLICABLE determinations
- explicit rejection list of inadmissible claims

### A11 — CCR1_canonical_commitment_record.json

### Eq3.MC — Meta Collapse Response-Admissibility Gate

MC consumes only the PMC output, the CCR candidate, explicit uncertainty, and governance constraints.

MC marks each response/output class as `ADMISSIBLE`, `CONDITIONAL`, or `INADMISSIBLE`.

MC may not alter PMC truth, generate CCR contents, or authorize execution.


---

## E) PASS 1 Freeze Boundary — Integrity-Gated (MANDATORY)

### Eq4.1 — Artifact Hashing
For each emitted artifact `Ai`:
- **Eq4.1:** `Hi = H(bytes(Ai))`

### Eq4.2 — Manifest Root Hash
**Eq4.2:** `M1 = H( concat( Ai_name || Hi ) in canonical order )`

### A12 — PASS1_manifest.json
Must include:
- dataset identity linkage (`dataset_hash` or `root_hash`)
- admission declaration hash (`A0_hash`)
- list of artifacts + their SHA-512 hashes
- generation timestamp
- mode/posture flags
- declaration: `DERIVED EVIDENCE — NON-DOCTRINAL`

### A12h — PASS1_manifest.sha512
- contains `H(bytes(A12))`

### [GATE] PASS 1 Completion
PASS 1 is FAILED unless:
- A12 exists and validates
- every referenced artifact hash matches recomputation
Validation failure → HARD HALT (PASS 2 FORBIDDEN)

---

# PASS 2 — OBSERVABLE CONTEXT + SECOND COLLAPSE (Refinement → Final Canonical Commitments)

## F) PASS 2 Preconditions (Hard)

### EqP.1 — Freeze Manifest Verification
**EqP.1:**  
`freeze_verified = verify_manifest(PASS1_manifest.json, PASS1_manifest.sha512, artifacts[])`

### [GATE] PASS 2 Authorization
If `freeze_verified=false` → HARD HALT  
If `freeze_verified=true` → PASS 2 authorized (requires explicit human approval, satisfied here)

---

## G) Observables Invocation (UNHYDRATED • NON-CANONICAL)

### EqF.0 — Observer Output Envelope
**EqF.0:**  
`Ok = { observer_id, version, inputs_declared, claims[], confidence[], limits[], timestamp, NON_CANONICAL:true, STATE:"UNHYDRATED" }`

Observers MAY:
- emit interpretive context about Pass 1 artifacts

Observers MAY NOT:
- gate, approve, promote, assert authority, introduce new evidence

### Owl_Hoot (temporal/cadence) — if substrate exists
**EqF.OH.1:** `silence_windows = detect_silence(events; params)`  
**EqF.OH.2:** `s_time(i) = f(cadence_features(i); params)`  
If no cadence substrate: emit `NOT_APPLICABLE`.

### Duck (contextual narrative)
**EqF.D.1:** `narrative = explain(PASS1_commitments, TopN; constraints)`  
No new facts. Interpretation only.

### WildFlower (theme bloom)
**EqF.WF.1:** `themes = bloom(top_candidates; params)`  
Interpretive grouping only.

### Mole (subsurface pathways)
**EqF.M.1:** `routes = infer_routes(neighbor_graphs; params)`  
Interpretive connectivity only.

---

## H) PASS 2 Governance Helix — PMC (Observer-Informed World Selection)

### EqG.PMC.1 — World Utility with Observer Terms
Let:
- `S` = Pass 1 frozen score surfaces
- `C` = operational constraints
- `O` = observer emissions (non-canonical)

**EqG.PMC.1:**  
`U2(world) = base_U(world; S, C) + ΔU(world; O)`  

Constraints:
- `ΔU` is bounded and must be explicitly justified
- Observers cannot introduce new line items; they may only reweight interpretation of existing frozen items or reinforce NOT_APPLICABLE outcomes.

### EqG.PMC.2 — Explicit Influence Statement
PMC must state:
- where Observables changed interpretation
- where Observables were ignored due to insufficient substrate

### A13 — PMC2_world_record.json

---

## I) PASS 2 Collapse — CCR Construction + MC Admissibility

### EqH.CCR.1 — Final Severity Score
Let:
- `sev_base(i)` from Pass 1 deterministic scoring
- `W2*` selected world from PMC2
- `adj(i)` = bounded adjustment recorded in PMC2 (not raw observer text)

**EqH.CCR.1:**  
`sev_final(i) = f(sev_base(i), W2*, adj(i))`

### EqH.CCR.2 — Deterministic Top-N Selection
**EqH.CCR.2:**  
`TopN(category) = stable_rank(items; key=sev_final, N=25, deterministic_ties=true)`

### Outputs (required order)
1. Hidden Threat Risk Report (highest priority)
2. Threat Risk Report
3. Anomaly Risk Report
4. Insider Threat Risk Report (or NOT APPLICABLE with reason)

### Artifacts (typical)
- **A14** `CCR2_canonical_commitment_record.json`
- **A15** `PASS2_HiddenThreat_Top25.csv`
- **A16** `PASS2_Threat_Top25.csv`
- **A17** `PASS2_Anomaly_Top25.csv`
- **A18** `PASS2_InsiderThreat_Top25.csv` OR `NOT_APPLICABLE.json`

---

## J) PASS 2 Final Integrity & Report Binding

### EqI.1 — Report Hashing
For each report `Rk`:
- **EqI.1:** `H(Rk) = H(bytes(Rk))`

### EqI.2 — Pass 2 Manifest Root
**EqI.2:** `M2 = H( concat( artifact_name || hash ) in canonical order )`

### A19 — PASS2_final_manifest.json
Must include:
- dataset identity linkage (`dataset_hash` or `root_hash`)
- PASS1 manifest hash linkage
- list of PASS2 artifacts + their hashes
- observer state: UNHYDRATED
- mode/posture flags

### A19h — PASS2_final_manifest.sha512 (recommended)

### Integrity Header (mandatory in every final report)
Include:
- Dataset identity hash (Beagle authoritative)
- Report SHA-512
- Canonicalization identifiers (dataset + report)
- Generation timestamp
- Mode/posture flags
- Observer state: UNHYDRATED
- PASS1 manifest hash (or manifest hash list)
- PASS2 manifest hash

---

# Architectural Invariant (Pass 2)

**Observers influence PMC → PMC constrains CCR construction → MC gates response admissibility → Raven produces permitted reports.**  
Observers never directly alter PMC truth, CCR contents, or MC admissibility decisions.

---

# Mermaid Wire Map — PASS 1 (Admission → Beagle → Analysis → PMC → CCR → MC → Freeze)

```mermaid
flowchart TD

A0[admission_declaration.json] --> A0h[admission_declaration.sha512]
A0h -->|A0_hash| B[Beagle Identity Sealing]

B --> A1[dataset_identity.json]
B --> A3[schema_snapshot.json]
B --> A4[dataset_fingerprint.json]
B --> A2[chunk_hashes.sha512list (if chunked)]

A1 --> ANALYSIS[Deterministic Analysis Helix]
A3 --> ANALYSIS
A4 --> ANALYSIS
A2 --> ANALYSIS

ANALYSIS --> A5[scores_anomaly]
ANALYSIS --> A6[scores_threat]
ANALYSIS --> A7[hidden_candidates]
ANALYSIS --> A9[model_params]

A5 --> PMC1
A6 --> PMC1
A7 --> PMC1
A9 --> PMC1

PMC1[PMC #1] --> A10[PMC1_world_record.json]
A10 --> CCR1[CCR #1]
CCR1 --> A11[CCR1_canonical_commitment_record.json]
A11 --> MC1[MC #1 Response Admissibility]

A1 --> FREEZE
A3 --> FREEZE
A4 --> FREEZE
A2 --> FREEZE
A5 --> FREEZE
A6 --> FREEZE
A7 --> FREEZE
A9 --> FREEZE
A10 --> FREEZE
A11 --> FREEZE

FREEZE[PASS 1 Freeze + Manifest Hashing] --> A12[PASS1_manifest.json]
A12 --> A12h[PASS1_manifest.sha512]
