# CR-AZIMUTH-001 / REVISION 2 — OBJECT/STATE ARCHITECTURE

## 0. Control and standing
- Name: AZIMUTH — Object/State Analytical Territory and Addressing
- Record: CR-AZIMUTH-001, revision 2 (supersedes revision 1 proposal, does not overwrite its frozen artifact)
- Reference baseline: Zervan vTemporal.48.1.3 (not modified)
- Stage: CR CANDIDATE, REVISED / SPECIFICATION FREEZE
- Canonical authority: NONE; Human Gate: ACTIVE; No Compression Out: ACTIVE
- GitHub changes: NONE; runtime qualification: NOT PERFORMED; physical qualification: NOT PERFORMED
- Producer: ChatGPT drafting from user-directed OBJECT/STATE correction; human authorization for canonical promotion: NOT GIVEN

## 1. Material correction and rationale
REV1 described a typed six-coordinate representation A(o)=(I,R,S,T,X,V), with the identity/state distinction preserved but object/state not established as the governing ontology. REV2 makes OBJECT/STATE primary. A coordinate is a projection of an object state; an address is a resolver reference; neither creates the object. The revision does not assert that six arbitrary spatial points establish a unique coordinate, or that all six typed dimensions are independent Euclidean axes.

## 2. Object, state, provenance, and coordinate
Let O_i be an object with persistent identifier oid_i and declared continuity policy C_i. Let s_{i,k} be its immutable recorded state at revision k. Let p_{i,k} be provenance supporting the state. Let F be a declared reference frame and E a canonical encoding specification.

State record: s_{i,k}=(R_{i,k},S_{i,k},T_{i,k},X_{i,k},V_{i,k}), with I_i=(oid_i,C_i) as the identity anchor.

AZIMUTH analytical coordinate: A_F(O_i,s_{i,k})=(I_i,R_{i,k},S_{i,k},T_{i,k},X_{i,k},V_{i,k}). The six labels are typed analytical dimensions; some components may be graphs, sets, intervals, structured histories, or unresolved/null values rather than scalars. V is a report of verification standing, not a truth oracle.

Persistent object reference: oid_i (scoped by namespace and issuer). State reference: (oid_i,k) or an equivalent immutable state identifier. Address: addr_E(oid_i,k,F) is a resolvable representation under declared encoding E, namespace, and version. No uniqueness, collision resistance, or deterministic serialization is claimed until qualified. Provenance is linked to object and state records and is not silently collapsed into the six-tuple.

## 3. Object lifecycle and continuity
- CREATE: issue an object identity and initial state with provenance; duplicate issuance must be detectable under a declared namespace policy.
- OBSERVE: add an observation as evidence; distinguish observation from interpretation.
- TRANSITION: append a new state to the same object only if continuity policy is satisfied; preserve earlier state and receipt.
- DERIVE: create a new object identity with explicit parent/source lineage when an operation changes object identity or semantic type.
- FORK: competing hypotheses or alternative interpretations become separately referable state branches or derived objects; no silent merge.
- MERGE/RECONCILE: require explicit policy, provenance, and receipt; contradictions remain visible until resolved.
- RETIRE: record standing change without erasing prior object or state history.
- REJECT/QUARANTINE: preserve suspect inputs with disallowed standing; do not promote them by re-encoding.

Identity continuity is governed by declared rules, not by visual similarity, equal coordinates, or a model's assertion. A transformation may preserve identity, generate a derivative, or remain unresolved; each outcome must be explicit.

## 4. Six analytical dimensions
I / IDENTITY: persistent namespace-qualified identity, continuity contract, issuer and alias resolution.
R / RELATIONSHIP: typed graph edges, endpoint references, direction, cardinality, context and provenance; relations may change by state.
S / SPACE: declared reference frame and spatial/relational location, including negative space and unknown coverage; no inferred physical metric.
T / TIME: observation time, event time, processing time, validity interval, clock source, timezone and uncertainty as applicable; do not assume clocks are interchangeable.
X / TRANSFORMATION: operation identity, inputs, outputs, parameters, declared invariants, reversibility status, and lineage; operations are not automatically invertible.
V / VERIFICATION: claims, tests, evidence receipts, confidence/uncertainty, scope, conflicts, and standing; a PASS is scoped to its actual test.

## 5. Addressing and subnetting
Partition function P maps object/state references or qualified relationship regions to analysis work units, not to independent truth claims. Partition membership is versioned, reversible where declared, and auditable. Replicated states preserve a common origin and must not be counted as independent observations. Reassembly reconciles references, versions, ordering, lineage and duplicates; disagreements are recorded rather than erased. An object may belong to multiple analytical subnets without acquiring multiple originating identities. Coordinates describe qualified state; addresses resolve qualified records; partition labels route work.

## 6. Analytical and ML/AI contract
Models consume explicitly scoped object/state snapshots, not unqualified merged replicas. Feature records link to source object IDs, state revisions, observation times, transformations, and missingness. Labels carry origin and temporal validity. Train/validation/test splitting must account for shared object lineage, temporal leakage and replicated observations. Inference results are new claims/evidence or derived objects with model version, inputs, outputs and evaluation scope, not automatic changes to source truth. Competing models can produce competing interpretations without overwriting source states. Unobserved territory remains unknown, not negative evidence unless a qualified measurement supports that interpretation.

## 7. Integration boundaries (proposed, not admitted)
- PIPE: proposed inventory, transport and transformation interface; its 64-unit inventory and any '65' designation require independent contract verification; no invented allocation is admitted here.
- C/C2: proposed axial/reference-frame and negative-space mapping; definitions and interface are pending qualification.
- CAVERN: proposed analytical staging, transformation, comparison and assembly territory; implementation unqualified.
- SKYFALL: inherited canonical logical specification at vTemporal.48.1.3. Its three 248-identity channel snapshots are replicas, not 744 unique identities. SKYFALL logical PASS does not validate AZIMUTH runtime or its integration.
No interface in this section is declared implemented or canonically admitted.

## 8. Invariants and failure semantics
INV-01: object identity and state version are separately resolvable.
INV-02: historical state records are immutable; correction appends a new record with linkage.
INV-03: identity-preserving transformations satisfy declared continuity rules; derivative operations issue new identity.
INV-04: all replicated evidence retains common source lineage; duplicate counting is detectable.
INV-05: unknown/null/unobserved/contradictory are distinct conditions.
INV-06: verification claims are scoped, attributable and independently challengeable.
INV-07: clock/reference-frame conversions preserve original representations and record method and uncertainty.
INV-08: reversible operations have defined inverses and receipts; irreversible operations are marked as such.
INV-09: address collisions, ambiguous aliasing, orphaned relations and missing receipts fail closed or remain explicitly unresolved.
INV-10: subnet movement cannot silently alter source object identity or fabricate evidence.

## 9. CR qualification plan and acceptance criteria
T01 Object/state distinction: create two revisions of one object; stable oid, distinct immutable state refs, recover both. Fail if state replaces identity.
T02 Identity/derivation: identity-preserving transformation retains oid; derivation creates new oid and parent lineage. Fail if policy ambiguous.
T03 Address determinism: under specified E/F, equivalent snapshots serialize equivalently; version changes are visible. Fail if canonical encoding undefined.
T04 Collision/alias: deliberate collisions and aliases detected and resolved or quarantined without conflating objects.
T05 Relational graph: edge edits and missing endpoints retain provenance; no silent orphan/merge.
T06 Temporal: event/observation/processing times and out-of-order data remain distinct and reconstructable.
T07 Transformation: invertible operation round-trips exactly within declared domain; irreversible operation does not claim round-trip.
T08 Replication/subnet: duplicate states across work units retain one originating evidence identity; reassembly conserves object/state accounting.
T09 Verification: missing, false, contradictory or tampered receipt never silently receives qualified PASS.
T10 ML leakage: lineage-aware splitting blocks replicated and derived leakage across evaluation partitions; demonstrate with labeled fixtures.
T11 Unknown/negative space: absent observations remain unknown, not false; conflict branches survive.
T12 Adversarial/recovery: dropped states, mutated identifiers, broken clocks, stale addresses and divergent replicas produce detectable failures.

Every test requires: dataset/fixture ID and bytes when available; declared assumptions; expected/observed output; failure record; reproducible command; hash receipt; reviewer decision. No numerical performance, ROC/AUROC, latency, throughput, collision rate, or physical metrics are claimed without executed evidence. CR exit requires passing scoped tests, resolved material blockers, independent review, and explicit Human Gate decision.

## 10. Risks and unresolved surface
- Ontology: what qualifies as one object; identity issuer; continuity and derivation policy.
- Reference-frame mathematics: dimensional independence, metrics, embeddings, topology and transformations.
- Canonical encoding: schema, namespaces, state versioning, hash/address collision handling.
- Concurrency: simultaneous updates, causal ordering, forks, merges and distributed consistency.
- Graph scale: relationship storage, cardinality, missing endpoints and traversal semantics.
- Verification: threat model, receipt trust, evidence quality and tamper resistance.
- Privacy/security: access control, data minimization, retention and cross-subnet disclosure.
- ML: data leakage, model/version lineage, evaluation protocols, concept drift and bias.
- Integration: Pipe/C/C2/Cavern contracts; SKYFALL interface; no runtime demonstration.
- Performance: complexity, storage cost, throughput, latency, scaling and failure recovery.

## 11. Revision lineage and freeze boundary
REV1 remains a frozen historical artifact: AZIMUTH_CR001_FULL_FREEZE.md, original six-dimension concept. REV2 explicitly supersedes its object-addressing-first framing with OBJECT/STATE-first ontology, preserves all six dimension labels and all prior nonclaims, and adds lifecycle, addressing separation, subnet semantics, ML contract, invariants and qualification tests. No retroactive mutation of REV1. No changes to vTemporal.48.1.3 canon, registries, admissions, or GitHub main.

## 12. Qualification conclusion
Result: QUALIFIED AS A REVISED CR-STAGE CONCEPTUAL SPECIFICATION. The revision resolves the architectural ambiguity between object, state, coordinate and address at the specification level. It does not establish formal correctness, uniqueness, implemented behavior, or runtime performance. Material unresolved issues remain listed in section 10. Standing: CR-STAGED, CLEAN FULL SPECIFICATION FREEZE; AUTHORITY NONE; HUMAN GATE ACTIVE; NO COMPRESSION OUT ACTIVE.
