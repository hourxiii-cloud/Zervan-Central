Zervan v39.0 Data Provenance Control Layer

Package ID: LCALL-2026.06.17-001
Canonical Configuration: vTemporal.39.0
Control Layer: ZERVAN-v39.DATA-PROVENANCE.1
Authority State: NONE
Human Gate: ACTIVE
External Runtime: DISABLED
System Population: DISALLOWED

⸻

Purpose

The Data Provenance Control Layer preserves where work starts, how it moves, what changed, what stayed the same, and which branch or package state is active.

It binds:

* Origin Dataset Boundary,
* Static Manifest,
* Transition Manifest,
* Secondary Manifest Control,
* Helix branch continuity,
* no-change / no-reach,
* no-unnecessary-rehash,
* Replay Scar where material,
* Human Gate where authority is implicated.

This layer is provenance control.

It is not truth.
It is not authority.
It is not deployment.
It is not compliance certification.
It is not legal finding.

⸻

Core Law

This started here.

Every branch points back.
Every movement records why.
Every changed object gets bounded validation.
Every unchanged object avoids redundant rehash.
No change, no reach.
Changed state, write the row.
Human Gate controls authority.

⸻

Origin Boundary

An origin boundary declares where a dataset, workbook, artifact, package, evidence object, report family, or analysis branch begins.

Origin boundary is provenance root.

Origin boundary is not factual truth.

Required origin record fields:

{
  "origin_id": "<origin-id>",
  "origin_line": "This started here.",
  "source_object": "<path-or-object-name>",
  "source_type": "<dataset | workbook | package | report | artifact | evidence_object | other>",
  "first_seen_utc": "<timestamp>",
  "sha256": "<pending-or-value>",
  "sha512": "<pending-or-value>",
  "authority_state": "NONE",
  "human_gate": "ACTIVE",
  "claim_ceiling": "provenance_root_only"
}

⸻

Static Manifest

Static Manifest answers:

* what files are inside the package,
* what roles the files serve,
* what package inventory exists,
* what source paths are declared,
* what hash status is known.

Static Manifest is inventory.

Static Manifest is not truth.
Static Manifest is not correctness.
Static Manifest is not authority.

Current static manifest:

manifests/v39_0_manifest.json

⸻

Transition Manifest

Transition Manifest answers:

* what changed,
* why it changed,
* what stayed the same,
* which prior state was used,
* which new state was created,
* whether claim ceiling changed,
* whether authority state changed,
* whether Human Gate was required,
* whether evidence changed or only report/package surface changed,
* whether rollback exists,
* whether Replay Scar is required.

Transition Manifest is movement history.

Transition Manifest is not truth.
Transition Manifest is not correctness.
Transition Manifest is not authority.

Current transition manifest:

manifests/v39_0_transition_manifest.json

⸻

Secondary Manifest Control

Secondary Manifest Control binds static inventory to transition movement and Helix branch continuity.

It preserves manifest relationships and prevents branch overwrite.

Secondary Manifest Control is not truth.
Secondary Manifest Control is not authority.
Secondary Manifest Control is not approval.

Current secondary manifest control:

manifests/v39_0_secondary_manifest_control.json

⸻

Helix Continuity

Helix 1 = intake and analysis.
Helix 2 = preserved analysis package state.
Helix 3 = prepared movement state.

Each new operating group returns to Helix 1.

Prior Helix 1, Helix 2, and Helix 3 branches remain intact.

Helix 3 prepares movement.
Helix 3 does not execute movement.
Helix continuity is not approval.
Human Gate controls authority-bearing movement.

⸻

No-Change / No-Reach

If no state transition occurred and local state is complete:

read state → confirm stable → no external reach → no rehash → move

No change means:

* no package hash change,
* no object hash change,
* no manifest hash change,
* no receipt pointer change,
* no claim ceiling change,
* no authority state change,
* no operating-group branch change,
* no handoff-state change,
* no promotion request,
* no audit validation requirement,
* no failure / rollback / repair trigger.

Do not pull object storage just to re-prove existence.

Do not rehash stable packages just to re-consume the operator.

⸻

No-Unnecessary-Rehash

Rehash only changed objects, changed packages, changed manifests, changed rendered reports, changed envelopes, changed receipts, changed branch packages, changed payloads, or changed transition artifacts.

Do not rehash unchanged source package, unchanged Helix 2 package, unchanged Helix 3 payload, unchanged workbook, unchanged static manifest, unchanged evidence graph, or unchanged legal / compliance / security report.

Hash validates identity and continuity.

Hash is not truth.

⸻

Local Simulation Boundary

The local provenance simulator may record local-only transition rows.

Current simulator:

scripts/local_provenance_simulator.py

Local simulation may:

* record first origin,
* compare local file hash,
* return NO_CHANGE_NO_REACH,
* record local changed-state transition.

Local simulation may not:

* reach S3,
* reach DynamoDB,
* reach Jira,
* deploy infrastructure,
* promote authority,
* populate systems.

⸻

Required Movement Record

When state changes, record:

{
  "transition_id": "<transition-id>",
  "timestamp_utc": "<timestamp>",
  "origin_id": "<origin-id>",
  "source_path": "<path>",
  "status": "<ORIGIN_RECORDED | LOCAL_CHANGE_RECORDED | NO_CHANGE_NO_REACH>",
  "reason": "<why movement occurred>",
  "prior_sha512": "<prior-or-null>",
  "new_sha512": "<new-or-null>",
  "external_reach": false,
  "system_population": false,
  "authority_state": "NONE",
  "human_gate": "ACTIVE"
}

⸻

Failure Classes

Provenance failures include:

* Origin Boundary Missing,
* Static Manifest Treated as Movement Ledger,
* Transition Manifest Missing,
* Secondary Manifest Control Missing,
* Unnecessary Rehash / Rehydration,
* Branch Overwrite,
* Pointer Drift,
* Evidence Boundary Collapse,
* Authority Leak,
* Prepared Movement Treated as Execution,
* Changed State Without Row,
* No-Change State Re-Consumed.

⸻

Repair Line

A package mismatch is not automatically corruption.
A changed hash may be a missing transition.
A missing transition is provenance debt.
Origin must be declared.
Movement must be recorded.
No change, no reach.
Changed state, write the row.

⸻

Truth Boundary

Origin Boundary is not factual truth.
Receipt is not truth.
Hash is not truth.
Manifest is not truth.
Transition Manifest is not truth.
Secondary Manifest Control is not truth.
Classification is not proof.
Framework mapping is not compliance.
Reporting adaptation is not verdict.
Prepared movement is not execution.
Helix continuity is not approval.
Human analysis validates output.
Human authorization permits authority-bearing action.

⸻

Final Control Line

This started here.

Every branch points back.
Every movement records why.
Every changed object gets bounded validation.
Every unchanged object avoids redundant rehash.
No change, no reach.
No unnecessary rehash.
Human Gate controls authority.
Stop.
