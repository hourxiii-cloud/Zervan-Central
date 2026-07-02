# HYDRATION_SURFACE — Visibility Declaration (Transport Only)

Version: 1.0
Mode: VISIBILITY ONLY (Data Hydration)
Default: FAIL-CLOSED
Repo Transport: https://github.com/hourxiii-cloud/zervan-core
No Discovery: TRUE (no repo crawl permitted)

Purpose:
Declare the complete hydration surface for constrained runtimes.
Hydration makes artifacts VISIBLE as data. Hydration does NOT grant authority.
Authority binding is performed only by explicit post-hydration policy selection.

-------------------------------------------------------------------------------
A. Hydration Invariants (Non-Bypassable)
-------------------------------------------------------------------------------

1) Hydration ≠ Authority
   - All hydrated artifacts are loaded as data blobs.
   - No artifact gains authority unless explicitly bound by an authority profile.

2) No Implicit Discovery
   - Only the URIs enumerated in this document may be fetched.
   - Directory listings, repo crawling, recursive link following are prohibited.

3) Fail-Closed
   - If any REQUIRED artifact is missing/unreadable (HTTP != 200) → HARD HALT.

4) Deterministic Identity
   - Each hydrated artifact MUST be recorded with:
     - uri
     - sha512(bytes)
     - byte_length
     - retrieved_at (UTC)
   - If a pinned hash is provided, mismatch → HARD HALT.

-------------------------------------------------------------------------------
B. Authority Binding (Post-Hydration)
-------------------------------------------------------------------------------

Hydration loads visibility surfaces only.

After hydration, runtime must select exactly one binding profile:

- BINDING_PROFILE: NONE
  - No doctrine authority; exploration permitted; promotion DISALLOWED.
  - Conflicts are reported; resolution is NOT performed.

- BINDING_PROFILE: CANONICAL
  - Apply doctrine only as enumerated by DoctrineOps/DOCTRINE_MANIFEST.md.
  - Conflicts resolve exclusively by DoctrineOps/AUTHORITY_RESOLUTION.md under Cathedral.
  - PMC and MC gates are enforceable; promotion MAY be allowed if MC certifies.

If binding profile cannot be selected or certified → NO OUTPUT.

-------------------------------------------------------------------------------
C. Core Control-Plane Artifacts (REQUIRED)
-------------------------------------------------------------------------------

1) DoctrineOps/AUTHORITY_RESOLUTION.md
   - uri: https://raw.githubusercontent.com/hourxiii-cloud/zervan-core/main/DoctrineOps/AUTHORITY_RESOLUTION.md

2) DoctrineOps/DOCTRINE_MANIFEST.md
   - uri: https://raw.githubusercontent.com/hourxiii-cloud/zervan-core/main/DoctrineOps/DOCTRINE_MANIFEST.md

3) INVENTORY.md
   - uri: https://raw.githubusercontent.com/hourxiii-cloud/zervan-core/main/INVENTORY.md

-------------------------------------------------------------------------------
D. Initialization Surfaces (REQUIRED — Behavior Only, Not Doctrine Truth)
-------------------------------------------------------------------------------

1) Accelerator/LLM_INIT.md
   - uri: https://raw.githubusercontent.com/hourxiii-cloud/zervan-core/main/Accelerator/LLM_INIT.md

2) Accelerator/LLM_DELTA.md
   - uri: https://raw.githubusercontent.com/hourxiii-cloud/zervan-core/main/Accelerator/LLM_DELTA.md

3) Accelerator/CONTEXT_PACK.md
   - uri: https://raw.githubusercontent.com/hourxiii-cloud/zervan-core/main/Accelerator/CONTEXT_PACK.md

4) Accelerator/LLM_INTAKE_GATE.md
   - uri: https://raw.githubusercontent.com/hourxiii-cloud/zervan-core/main/Accelerator/LLM_INTAKE_GATE.md

-------------------------------------------------------------------------------
E. Domain Surfaces (OPTIONAL — Loaded As Data)
-------------------------------------------------------------------------------

This section enumerates additional packages that may be hydrated as data.
None are authoritative unless bound by CANONICAL profile and manifest order.

E1) Crypto / PKI / ECC (OPTIONAL)
- schema/envelopes/manifest.schema.json
- schema/envelopes/proof.schema.json
- (no crypto_policy files are loaded by path; policy must be injected at runtime)

E2) Runtime / Module Contracts (OPTIONAL)
- retriever/retriever_contract.md
- doctrine/PMC.md
- doctrine/PMC_ARENA.md
- (additional modules must be enumerated explicitly here; no crawl)

-------------------------------------------------------------------------------
F. Crypto Verification Rule (Option 2 — Policy Injection)
-------------------------------------------------------------------------------

When cryptographic verification is active:
- Runtime MUST accept crypto_policy as an injected policy object.
- Runtime MUST NOT load crypto policy by filesystem path or repository path.
- Verification MUST be fail-closed if policy is absent or invalid.

Policy binding requirements (enforced when enabled):
- manifest.crypto.policy_id MUST match crypto_policy.policy.id
- Canonicalization + signature requirements MUST be derived from crypto_policy
  (no hardcoded versions/scopes)

-------------------------------------------------------------------------------
G. Hydration Output Artifact (REQUIRED)
-------------------------------------------------------------------------------

Hydration MUST emit a hydration receipt (data artifact), containing:
- hydration_surface_version
- binding_profile_selected (NONE | CANONICAL)
- artifact list:
  - uri
  - sha512
  - byte_length
  - retrieved_at
  - required (true/false)
  - pinned_sha512 (optional)
- failures (if any)
- overall_status (PASS | HARD_HALT)

Receipt is not doctrine truth; it is visibility evidence.

---

H. 5.6 Bridge Hydration Binding

Bridge review must document repository binding instead of silently rewriting repository identity.

Package transport reference in this artifact family may point to `https://github.com/hourxiii-cloud/zervan-core`.
Current v39 initialization may be grounded from `https://github.com/hourxiii-cloud/Zervan-Core-v39`.

This mismatch is a transition-binding issue, not an authority grant. Hydration remains visibility-only. No discovery, external runtime activation, system population, or authority promotion is permitted.

Observer and sub-observer visibility remains explicit-enumeration only.

Primary observer surfaces may include:
- observers/README.md
- observers/Eagle/README.MD
- observers/Mole/README.md
- observers/Duck/README.md
- observers/Wildflower/README.md
- observers/Mockingbird/README.md
- observers/Platypus/README.md
- observers/owl_hoot/README.md

Controlled sub-observer surfaces may include:
- observers/Osprey/README.md
- observers/Osprey/osprey_contract.md
- observers/AnimalKingdom/README.md
- observers/AnimalKingdom/animalkingdom_subobserver_contract.md
- observers/Armadillo/README.md
- observers/Armadillo/armadillo_contract.md

Owl_Hoot remains a primary observer even when a bounded sub-observer mode is invoked for narrow pressure.
