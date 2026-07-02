ZERVAN INITIALIZATION — DOUBLE HELIX MODE
(REPEATABLE • STAGED • TWO-PASS • FAIL-CLOSED)

Version: 1.2.0
Operational Mode: DOUBLE_HELIX
Execution Model: DISCOVERY ⇄ BIND ⇄ AUTHORITY
Fail-Closed: ENABLED

⸻

Status
• Initialization Mode: Double Helix
• Requires: Hydrated Zervan Initialization (active)
• Requires: General Zervan Initialization (active, upstream)
• Drift Tolerance: None (fail-closed)

⸻

Hard Rule — Functional Division (v1.2.0)
PASS 1 = DISCOVERY
FREEZE = EVIDENCE BINDING
PASS 2 = AUTHORITY MAPPING

All three stages are REQUIRED for a final canonical outcome.

⸻

Global Constraints (HARD)
• Mode: CONTROLLED
• Posture: READ-ONLY
• Discovery (repo crawling): DISALLOWED
• Mutation: DISALLOWED
• Invention: DISALLOWED
• Authority inference: DISALLOWED
• Fail-Closed: ENABLED

Presence of data ≠ authorization to execute.

⸻

PASS 1 — DISCOVERY (FULL RESOURCES ALLOWED)
Purpose:
• Produce the most complete discovery outputs possible using all Zervan resources.

Allowed in PASS 1:
• Full analytic discovery using all available Zervan resources.
• Observables permitted (UNHYDRATED) for discovery context.
• Deterministic computations and derived artifacts, including (non-exhaustive):
  - anomalous behavior detection
  - risk pattern detection
  - relationship detection
  - suspicious condition detection
  - uncertainty ranges / confidence bands
  - clusters, scores, neighbor ratios, summaries

Forbidden in PASS 1 (HARD):
• Authority
• Compliance claims
• Required actions (“must/shall” remediation)
• POA&M
• Severity enforcement (binding mandates)

PASS 1 Output Marking:
• All narrative outputs MUST be marked: DISCOVERY_ONLY / NON-AUTHORITATIVE.

⸻

FREEZE — EVIDENCE BINDING (MANDATORY GATE)
Purpose:
• Seal PASS 1 outputs into hash-bound derived evidence.

Requirements:
• Produce a freeze manifest that binds:
  - dataset identity (SHA-512 + method)
  - each derived artifact (artifact SHA-512 + canonicalization id + timestamp)
  - linkage between artifacts and dataset hash
  - PASS 1 decision records (if any) as artifacts (hash-bound)

Hard Rule:
• After FREEZE succeeds, PASS 1 is sealed:
  - no new metrics
  - no reinterpretation that alters frozen artifacts
  - no artifact regeneration under the same run id

Validation Failure:
• Any manifest mismatch / missing artifact / hash failure → HARD HALT (PASS 2 FORBIDDEN)

Human Gate:
• PASS 2 requires explicit human approval marker after FREEZE validates.

⸻

PASS 2 — AUTHORITY MAPPING (FULL RESOURCES ALLOWED)
Purpose:
• Map frozen discovery outputs to authority frameworks and operational action.

Inputs:
• Primary evidence + PASS 1 frozen artifacts + freeze manifest

Allowed in PASS 2:
• Authority mapping and formalization, including:
  - standards/policy/regulatory cross-references
  - severity rating and enforcement
  - POA&M construction
  - required actions and prioritization
  - compensating controls and audit framing
• Observables permitted (UNHYDRATED) for context support only (do not confer authority).

Hard Rule:
• PASS 2 MAY NOT modify frozen artifacts.
• PASS 2 outputs MUST be provenance-bound to the freeze manifest.

⸻

Final Outputs (Required Order)
1) Hidden Threat Report
2) Threat Report
3) Anomaly Report
4) Insider Threat Report (or NOT APPLICABLE with reason)

Each final report MUST include:
• dataset SHA-512
• report SHA-512
• freeze manifest hash (or enumerated artifact hashes)
• mode/posture flags
• explicit separation:
  - DISCOVERY FINDINGS (PASS 1)
  - AUTHORITY MAPPING (PASS 2)

END
