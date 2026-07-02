# ZERVAN — RUNBOOK: MINIMAL PASS 1
Version: 1.0.0  
Mode: CONTROLLED  
Posture: READ-ONLY  
Discovery: DISABLED  
Mutation: DISALLOWED  
Invention: DISALLOWED  
Authority Inference: DISALLOWED  
Fail-Closed: ENABLED  

Scope: **PASS 1 ONLY**  
Observers: **NOT USED**  
Chunking: **NOT USED**  

---

## Purpose

This runbook defines the **minimal executable path** for Zervan.

It validates that a small dataset can pass cleanly through:

**Admission → Beagle → Pass 1 Analysis → PMC #1 → MC #1 → Freeze**

This is the **Alpha “hello world”** for Zervan.

No scale.  
No chunking.  
No Observables.  
No Pass 2.

---

## Preconditions (Required)

- A **single small dataset** (e.g., CSV)
- Dataset byte size **below chunking threshold**
- Local access to the dataset
- Ability to compute SHA-512
- All Admission artifacts present in repo

---

## Inputs

### Evidence
- `sample_small_dataset.csv`
  - byte size < threshold in `thresholds.json`

### Admission Configuration
- `Admission/LeafcutterAnt/admission_declaration.schema.json`
- `Admission/LeafcutterAnt/thresholds.json`
- `Admission/LeafcutterAnt/decision_tree.md`

---

## Step 1 — Admission (LeafcutterAnt)

### Action
Produce an Admission Declaration using LeafcutterAnt.

- Measure `byte_size`
- Evaluate threshold rule
- Determine `chunking_required=false`

### Artifact Produced
- `admission_declaration.json`
- `admission_declaration.sha512`

### Validation
- Declaration validates against schema
- `chunking_required=false`
- No `chunking` object present

### Halt Conditions
- Missing byte size
- Schema validation failure
- Threshold cannot be evaluated

---

## Step 2 — Identity Sealing (Beagle)

### Action
Hand off admitted evidence to Beagle.

Beagle MUST:
- Compute authoritative dataset SHA-512
- Produce identity and fingerprint artifacts
- Bind identity to Admission Declaration hash

### Artifacts Produced
- `dataset_identity.json`
- `dataset_identity.sha512`
- `schema_snapshot.json`
- `dataset_fingerprint.json`

### Validation
- Dataset SHA-512 computed successfully
- Identity artifacts reference `admission_declaration.sha512`
- No chunk hashes present

### Halt Conditions
- Hash computation failure
- Missing identity artifacts
- Admission declaration contradiction

---

## Step 3 — Pass 1 Analysis Helix

### Action
Run deterministic Pass 1 analysis.

- Apply deterministic transforms
- Compute anomaly/threat metrics as configured
- No Observables invoked
- No contextual interpretation

### Artifacts Produced
- `scores_anomaly.csv` (or equivalent)
- `scores_threat.csv`
- `model_params.json`

### Validation
- All parameters recorded
- Deterministic outputs reproducible
- Artifacts reference dataset identity hash

### Halt Conditions
- Missing parameters
- Non-deterministic behavior
- Artifact/data mismatch

---

## Step 4 — Pass 1 Governance Helix (PMC #1 → MC #1)

### PMC #1
- Evaluate worlds (Conservative / Balanced / Aggressive)
- Select exactly one world
- Reject others explicitly

### MC #1
- Produce minimal commitments
- Generate Top N (default 25 or fewer if dataset smaller)
- Record explicit NOT APPLICABLE determinations if any

### Artifacts Produced
- `PMC1_world_record.json`
- `MC1_commitment_record.json`

### Validation
- Exactly one world selected
- Rejections explicitly documented
- No observer influence

---

## Step 5 — Pass 1 Freeze Boundary

### Action
Freeze all Pass 1 artifacts.

### Artifacts Produced
- `PASS1_manifest.json`
- `PASS1_manifest.sha512`

Manifest MUST include:
- dataset identity hash
- admission declaration hash
- list of all Pass 1 artifacts + their hashes
- generation timestamp
- mode/posture flags
- declaration: `DERIVED EVIDENCE — NON-DOCTRINAL`

### Validation
- All listed artifact hashes recompute correctly
- Manifest hash validates
- No missing artifacts

### Halt Conditions
- Any hash mismatch
- Missing artifact
- Manifest validation failure

---

## Success Criteria (PASS 1 COMPLETE)

PASS 1 is considered **successful** if:

- Admission completed without chunking
- Beagle identity sealing succeeded
- Deterministic analysis artifacts produced
- PMC #1 and MC #1 artifacts exist
- PASS1 manifest validates fully

At this point:
- **Pass 2 is not executed**
- **Observers are not invoked**
- **No conclusions are finalized**

---

## Explicit Non-Goals

This runbook does NOT:
- Test chunking
- Test streaming
- Invoke Observables
- Execute Pass 2
- Optimize performance
- Process large datasets

Those occur in later runbooks.

---

## Canonical Assertion

> **If this runbook succeeds, Zervan is operationally viable.  
All further capability builds on this path.**

---

## Status

- Runbook Type: **Alpha**
- Scope: **Minimal Pass 1**
- Authority: **None beyond derived evidence**
- Safe to repeat
- Safe to audit

END
