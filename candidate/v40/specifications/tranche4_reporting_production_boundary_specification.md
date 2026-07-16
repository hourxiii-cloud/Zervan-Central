# Zervan v40 Candidate - Wave 1 / Sequential Tranche 4 Reporting-Production Boundary Specification

Specification State: PRE-IMPLEMENTATION / REVIEW COMPLETE

Implementation State: NOT STARTED

Version Target: vTemporal.40.0-candidate

Operating Mode: DISCUSSION / TECH / NONE / NON-DOCTRINAL / STABLE

Candidate Posture: CONTROLLED / LOCAL SPECIFICATION / READ-ONLY BASELINE

Authority: NONE

Human Gate: ACTIVE

Canonical Promotion: NOT AUTHORIZED

External Runtime: DISABLED

System Population: DISALLOWED

Publication: DISALLOWED UNTIL HUMAN GATE

## 1. Decision

This specification defines the typed Evidence -> Analysis -> Reporting boundary and the production gates required to prevent analytical loss during artifact creation.

The controlling rule is:

> Reporting may translate, organize, summarize, visualize, sequence, and adapt analytical material for a defined audience. Reporting may not mutate analytical claims, lineage, evidence relationships, scope, risk inheritance, attribution, limitations, or uncertainty.

Reporting is not limited to literal serialization. It is controlled projection.

Production is not successful because files exist. Production is successful only when the requested understanding is carried into substantive, standalone, integrity-bound artifacts and passes the declared Human Gate boundary.

No reporting implementation may begin until this specification is reviewed and committed separately.

## 2. Git-First Baseline and Contract Precondition

This specification is anchored to current public Git state observed at drafting time:

- canonical repository: `https://github.com/hourxiii-cloud/Zervan-Core-v39.git`;
- canonical branch: `main`;
- canonical main commit: `d07023f028833f3ed1b61eebbd3298ed61c28d72`;
- candidate branch: `candidate/v40-wave0`;
- candidate implementation parent: `f8227ada793c2ef8dae778ce7bdd6d1bda488bb4`;
- prior canonical baseline recorded by the Wave 0 contract: `b9460bf2955246ff3b1f61ed0b398496d7ad49c1`.

The old Wave 0 Operational Contract remains immutable. It is not silently rebound from `b9460bf...` to `d07023f...`.

Before implementation begins:

1. fetch current `origin/main` and `origin/candidate/v40-wave0`;
2. verify the main and candidate heads against this specification;
3. if either head changed, stop and record an explicit specification revalidation;
4. create a new reporting-production Operational Contract instance;
5. bind that contract to the exact current canonical main commit and candidate parent;
6. preserve Authority `NONE`, Human Gate `ACTIVE`, external runtime `DISABLED`, and system population `DISALLOWED`; and
7. commit the contract checkpoint before reporting runtime code.

Canonical advancement is not an implementation detail. It is a transition requiring evidence.

At specification review, the existing candidate validator and activation fixtures fail closed because the historical Wave 0 contract remains bound to `b9460bf...` while `origin/main` is `d07023f...`. That failure is correct canonical-drift evidence, not permission to edit the historical contract or weaken the validator.

The Wave 1 contract checkpoint must therefore separate active and historical validation:

- active Wave 1 fixtures validate against the new exact current binding;
- historical Wave 0 fixtures verify the immutability and recorded binding of the old contract rather than asserting that it remains the active current-main contract;
- runtime fixtures that require activation use the new active contract instance; and
- canonical-drift fixtures continue to prove that an active contract fails closed when its bound head changes.

## 3. Architectural Placement

The required dependency chain is:

Canonical Resolver
-> Operational Contract
-> Runtime Conformance / Internal Audit
-> Evidence Records
-> Analysis Records
-> Analytical Inventory Freeze
-> Report Projection
-> Artifact Reconciliation
-> REVIEW_READY
-> Human Gate

Scar and Replay surround the chain. They do not replace it.

The chain is a claim-preservation boundary, not a fixed orchestration topology. Functions may communicate multidirectionally, but claims cross into Reporting only through the declared projection contract.

Stable seats and boundaries remain:

- Beagle validates source and evidence objects;
- Retriever produces or revises analysis;
- Raven produces report projections and human-facing surfaces;
- Audit validates lineage, mutation boundaries, and gate evidence;
- Governance preserves claim ceiling and Human Gate posture;
- Reporting Adaptation changes package shape, not evidence or verdict;
- Human Gate alone authorizes promotion or external representation.

This specification does not canonize Analysis as a Persona. Analysis remains the ANALYTICAL layer plus selected Processors until a later ADR decides otherwise.

## 4. Scope

This tranche specifies:

1. typed immutable evidence records;
2. typed immutable analysis and claim records;
3. explicit uncertainty, contradiction, limitation, attribution, and risk-inheritance fields;
4. an analytical inventory freeze;
5. a reporting requirement inventory;
6. a report projection contract;
7. allowed and forbidden audience transformations;
8. report-element-to-claim lineage;
9. production states and transitions;
10. conversation-to-artifact reconciliation through explicit records;
11. escalation-lineage ordering where route-required;
12. no-placeholder and substantive-content gates;
13. evidence-carriage and standalone-review gates;
14. scope and report-inflation controls;
15. package manifest, hashing, archive reopen, and verification;
16. Human Gate promotion and return behavior;
17. Audit interrupt, Scar, and Replay integration;
18. adversarial and end-to-end acceptance fixtures; and
19. regression and commit discipline.

## 5. Explicit Exclusions

This tranche does not:

- create new analytical findings from raw evidence;
- reconstruct missing analysis from conversation memory;
- define the complete inquiry-envelope architecture;
- decide whether Analysis becomes a Persona;
- change the functional seats of Beagle, Retriever, Raven, Observers, Signal Ecology, Personas, or Processors;
- treat Framework Mapping as compliance;
- treat Reporting Adaptation as verdict;
- authorize publication, certification, legal findings, HR action, disciplinary action, or production execution;
- send reports to external recipients;
- populate external systems;
- merge or promote v40;
- mutate canonical v39;
- close P0 findings automatically; or
- fabricate the missing insider-threat source package or analytical corpus.

## 6. Definitions

### 6.1 Evidence record

An immutable record describing an observed, supplied, measured, or explicitly derived evidence object and its provenance boundary.

Evidence is not analysis, verdict, authority, or factual truth merely because it is recorded or hashed.

### 6.2 Analysis record

An immutable analytical object containing claims, evidence relationships, methods, uncertainty, contradiction, limitation, attribution, risk inheritance, and temporal boundaries.

### 6.3 Claim

A bounded analytical assertion with structured semantic fields and explicit support state.

### 6.4 Analytical inventory

The complete route-bounded set of material findings, counts, identities, methods, limitations, evidence objects, uncertainties, contradictions, classifications, mappings, ordering requirements, and requested artifacts that reporting must preserve.

### 6.5 Analytical inventory freeze

An immutable digest-bound snapshot of the analytical inventory accepted as the source boundary for one reporting operation.

Freeze means the source set is fixed for the projection. It does not mean the analysis is universally true or permanently final.

### 6.6 Reporting requirement

An explicit item derived from the user request, active Operational Contract, route, established analytical record, or Human Gate decision that the production operation must satisfy.

### 6.7 Report projection

A declared mapping from immutable analytical objects into audience-specific report elements under an allowed transformation set.

### 6.8 Presentation-only context

Material used for navigation, layout, definitions, disclaimers, or audience guidance that does not assert a new analytical claim.

Presentation-only context must be labeled as such and cannot satisfy a required analytical item.

### 6.9 Artifact reconciliation

The process of proving that every required inventory item and reporting requirement resolves to a substantive report element and artifact, and that every analytical report element resolves back to immutable analysis and evidence.

### 6.10 Review ready

A local, standalone, reopened, hash-verified package that satisfies its production contract and is eligible for Human Gate review.

Review ready is not promoted, published, approved, certified, compliant, or authoritative.

### 6.11 Promotion

An explicit Human Gate designation that a verified package may move into the exact authorized next state.

Promotion does not imply external delivery unless the decision explicitly authorizes the target, action, and scope.

## 7. Typed Boundary Objects

### 7.1 Evidence record minimum fields

Every evidence record must include:

- `evidence_version`;
- `evidence_id`;
- `evidence_class`;
- `source_ref`;
- `source_object_ref`;
- `source_sha512` or an explicit unavailable state;
- `object_ref`;
- `value_ref` or `content_ref`;
- `scope`;
- `observation_time_utc` or `null` when unknown;
- `source_time_utc` or `null` when unknown;
- `acquired_at_utc`;
- `reliability_state`;
- `limitations`;
- `provenance_refs`;
- `authority_state`: `NONE`;
- `human_gate_state`: `ACTIVE`; and
- `evidence_sha512`.

Allowed `evidence_class` values are:

- `SOURCE_ASSERTION`;
- `OBSERVATION`;
- `MEASUREMENT`;
- `DERIVED_MEASUREMENT`;
- `DOCUMENT`;
- `DATASET_OBJECT`;
- `WORKBOOK_OBJECT`;
- `TRANSITION_WITNESS`;
- `SCAR`;
- `REPLAY_RECEIPT`; and
- `OTHER_DECLARED`.

Unknown provenance remains unknown. It is not rewritten as absent, reliable, or verified.

### 7.2 Claim semantic object

Every material claim must contain a structured semantic object sufficient to detect mutation of:

- subject or actor;
- predicate or relationship;
- object or value reference;
- polarity;
- quantitative magnitude and unit where applicable;
- population and denominator where applicable;
- scope;
- temporal boundary;
- classification or risk category;
- ordering or inheritance relationship; and
- claim ceiling.

Free-form claim text may accompany the semantic object. The text does not replace the structured fields.

### 7.3 Analysis record minimum fields

Every analysis record must include:

- `analysis_version`;
- `analysis_id`;
- `inquiry_ref`;
- `route_ref`;
- `contract_ref`;
- `method_refs`;
- `claim_objects`;
- `finding_refs`;
- `count_refs`;
- `identity_refs`;
- `evidence_refs`;
- `uncertainty_objects`;
- `contradiction_refs`;
- `limitation_objects`;
- `eliminated_world_refs`;
- `surviving_world_refs`;
- `risk_inheritance_edges`;
- `classification_refs`;
- `framework_mapping_refs`;
- `attribution`;
- `analysis_time_utc`;
- `provenance_refs`;
- `authority_state`: `NONE`;
- `claim_ceiling`;
- `status`; and
- `analysis_sha512`.

Claim support states are:

- `SUPPORTED`;
- `PARTIALLY_SUPPORTED`;
- `CONTRADICTED`;
- `UNRESOLVED`;
- `RETRACTED`; and
- `UNKNOWN`.

Reporting must preserve the exact support state.

### 7.4 Uncertainty object

An uncertainty object must distinguish:

- missing evidence;
- unreliable evidence;
- contradictory evidence;
- bounded statistical uncertainty;
- scope uncertainty;
- temporal uncertainty;
- classification uncertainty;
- mapping uncertainty;
- unresolved analytical state; and
- unknown cause.

Reporting cannot convert uncertainty into confidence, certainty, omission, or reassurance.

### 7.5 Attribution object

Every material conclusion must identify its actual origin:

- `USER_ESTABLISHED`;
- `SOURCE_ASSERTED`;
- `EVIDENCE_OBSERVED`;
- `SYSTEM_DERIVED`;
- `HUMAN_VALIDATED`;
- `HUMAN_DECIDED`; or
- `UNKNOWN`.

User-established engineering conclusions cannot be relabeled as assistant discoveries.

## 8. Analytical Inventory Freeze Contract

Before reporting begins, the production route must create an immutable analytical inventory freeze.

The freeze must enumerate every material:

- finding;
- count and denominator;
- identity or ranked entity;
- method;
- limitation;
- evidence object;
- uncertainty;
- contradiction;
- classification;
- possible framework mapping;
- risk-inheritance edge;
- ordering requirement;
- requested artifact;
- required appendix or evidence file;
- user-owned completion criterion; and
- known unavailable item.

The freeze must include:

- `freeze_version`;
- `freeze_id`;
- canonical and candidate Git bindings;
- Operational Contract reference;
- reporting request reference;
- route reference;
- ordered inventory items;
- source analysis record identifiers and hashes;
- requirement inventory identifier and hash;
- known exclusions;
- unresolved ambiguities;
- created time;
- Authority `NONE`;
- Human Gate `ACTIVE`;
- `previous_freeze_ref` when versioned; and
- `freeze_sha512`.

The freeze digest is calculated over canonical JSON excluding only its own digest field.

Once frozen:

- an analysis object is never edited in place;
- a correction creates a new analysis object and new freeze version;
- every prior projection becomes bound to its original freeze;
- a changed freeze invalidates dependent reconciliation and review-ready receipts; and
- reporting cannot silently add an analytical claim.

## 9. Reporting Requirement Inventory

Every production operation must create a closed requirement inventory before artifact writing.

Each requirement must include:

- `requirement_id`;
- `requirement_class`;
- `source_class`;
- `source_ref`;
- `required`;
- `description`;
- `completion_test`;
- `ordering_constraint` where applicable;
- `artifact_role`;
- `claim_or_inventory_refs`;
- `status`; and
- `exclusion_reason` when explicitly excluded.

Allowed source classes are:

- `USER_EXPLICIT`;
- `OPERATIONAL_CONTRACT`;
- `ROUTE_REQUIRED`;
- `ANALYTICAL_ESTABLISHED`;
- `GOVERNANCE_REQUIRED`; and
- `HUMAN_GATE_DECISION`.

Conversation-to-artifact reconciliation does not authorize hidden conversation memory.

Relevant conversational content must first become an explicit requirement or analytical record. If a material conversational assertion cannot be resolved to an explicit record, it is unavailable context and blocks completion until the user clarifies or supplies the record.

Commentary, planning, filenames, and acknowledgements do not satisfy production requirements.

## 10. Report Projection Contract

Every report projection must include:

- `projection_version`;
- `projection_id`;
- `request_ref`;
- `contract_ref`;
- `route_ref`;
- `freeze_ref` and `freeze_sha512`;
- `audience_profile`;
- `reporting_lane`;
- `allowed_transformations`;
- `forbidden_transformations`;
- `required_requirement_refs`;
- `required_inventory_refs`;
- `report_elements`;
- `omission_records`;
- `presentation_only_elements`;
- `claim_ceiling`;
- `authority_state`: `NONE`;
- `human_gate_state`: `ACTIVE`;
- `projection_status`;
- `created_at_utc`;
- `previous_projection_ref` where revised; and
- `projection_sha512`.

### 10.1 Allowed transformations

Declared transformations may include:

- `TRANSLATE_LANGUAGE`;
- `ORGANIZE`;
- `SUMMARIZE`;
- `VISUALIZE`;
- `SEQUENCE`;
- `FORMAT`;
- `AUDIENCE_ADAPT`;
- `DECLARED_FILTER`;
- `DECLARED_AGGREGATION`; and
- `ACCESSIBILITY_ADAPT`.

Every transformation must identify its source analytical objects, output report elements, and transformation parameters.

### 10.2 Forbidden transformations

Reporting must reject any transformation that changes or conceals:

- claim subject, actor, object, predicate, or polarity;
- quantitative value, denominator, unit, or aggregation boundary;
- scope or time;
- evidence relationships;
- source or transformation lineage;
- support state;
- uncertainty type or magnitude;
- contradiction;
- limitation;
- attribution;
- risk category;
- risk-inheritance edge;
- classification boundary;
- framework-mapping boundary;
- claim ceiling;
- ordering required by the route; or
- user-owned completion criteria.

Reporting also must reject:

- invented facts;
- invented citations;
- invented evidence identifiers;
- invented missing analysis;
- silent omission of required material;
- conversion of candidate mapping into compliance;
- conversion of preparation into authorization;
- conversion of triage into verdict;
- conversion of Review Ready into Promoted; and
- conversion of presentation-only context into an analytical claim.

### 10.3 Semantic equivalence boundary

Machine validation may prove that structured fields, references, and hashes remained unchanged. It cannot by itself prove that every natural-language paraphrase preserved meaning.

Therefore:

- every analytical report element carries the source claim semantic digest;
- structured invariants are compared automatically;
- a human-readable claim map is produced;
- natural-language equivalence remains a Human Gate review obligation; and
- the system cannot self-certify semantic equivalence.

## 11. Report Elements

Every report element must be typed as one of:

- `CLAIM_PROJECTION`;
- `FINDING`;
- `COUNT`;
- `TABLE`;
- `VISUALIZATION`;
- `METHOD`;
- `LIMITATION`;
- `UNCERTAINTY`;
- `CONTRADICTION`;
- `EVIDENCE_INDEX`;
- `IDENTITY_ASSESSMENT`;
- `CLASSIFICATION_SURFACE`;
- `FRAMEWORK_MAPPING_SURFACE`;
- `RECOMMENDATION`;
- `PRESENTATION_ONLY`; or
- `NAVIGATION`.

Analytical elements must include:

- stable element identifier;
- source analysis and claim references;
- source semantic digests;
- evidence references;
- transformation reference;
- rendered artifact path;
- stable section, table, figure, or anchor reference;
- uncertainty and limitation references;
- content status;
- element digest; and
- human-review status.

Presentation-only elements must include a reason and cannot carry analytical completion credit.

Visualizations must additionally bind:

- source data or count references;
- series and category definitions;
- axes and units;
- filters and aggregations;
- suppressed or unavailable values;
- caption claim references; and
- accessible description.

## 12. Multidirectional Callback Without Mutation

Reporting may expose:

- missing source context;
- analytical ambiguity;
- unsupported visualization;
- missing denominator;
- broken lineage;
- audience mismatch;
- route-required omission; or
- claim-ceiling pressure.

Raven may call back to Retriever, Beagle, Audit, Governance, or the active route.

The callback does not edit the frozen analysis.

If analysis changes:

1. create a new immutable analysis record;
2. record the transition and reason;
3. produce a new inventory freeze;
4. invalidate dependent projections and completeness receipts;
5. create a new projection version; and
6. reconcile again.

Dynamic communication is permitted. Meaning drift is not.

## 13. Production State Machine

Machine states are:

- `DISCOVERY`;
- `ANALYSIS_COMPLETE`;
- `REPORTING`;
- `RECONCILIATION`;
- `REVIEW_READY`;
- `HUMAN_GATE_REVIEW`;
- `PROMOTED`;
- `RETURNED`;
- `STOPPED`.

### 13.1 Allowed transitions

- `DISCOVERY -> ANALYSIS_COMPLETE` only after a valid analytical inventory freeze;
- `ANALYSIS_COMPLETE -> REPORTING` only after a valid projection contract;
- `REPORTING -> REPORTING` for recorded artifact production events inside the locked route;
- `REPORTING -> RECONCILIATION` only when every required artifact is declared produced;
- `RECONCILIATION -> REPORTING` for bounded, recorded, non-integrity defects;
- `RECONCILIATION -> REVIEW_READY` only when every mandatory gate passes;
- `REVIEW_READY -> HUMAN_GATE_REVIEW` only on an explicit promotion request;
- `HUMAN_GATE_REVIEW -> PROMOTED` only on an explicit human approval receipt;
- `HUMAN_GATE_REVIEW -> RETURNED` only on an explicit human return or denial receipt; and
- any nonterminal state -> `STOPPED` on Audit interrupt, integrity failure, route drift, claim mutation, or unrecoverable production failure.

### 13.2 Terminal states

`PROMOTED`, `RETURNED`, and `STOPPED` are terminal for the active production contract instance.

They cannot reenter reporting.

A returned package requires a new or explicitly authorized repair contract. A stopped package requires Scar and later Replay. A promoted package requires a separately authorized external action when actual delivery or publication is requested.

### 13.3 Reconciliation return boundary

The same contract may return from `RECONCILIATION` to `REPORTING` only when:

- the route remains unchanged;
- the freeze remains unchanged;
- the projection remains valid;
- the defect is an artifact omission, formatting defect, broken local anchor, or other bounded production defect;
- no claim, evidence, uncertainty, or lineage mutation occurred; and
- the return is recorded as a transition.

Repeated non-progressing returns trigger `LOGIC_FREEZE`, Audit stop, Scar, and later Replay.

## 14. Production Failure Classes

Production events must distinguish:

- `CANONICAL_BINDING_FAILURE`;
- `CONTRACT_NONCONFORMANCE`;
- `ANALYTICAL_FREEZE_FAILURE`;
- `REPORT_MUTATION`;
- `LINEAGE_BREAK`;
- `REQUIREMENT_OMISSION`;
- `INVENTORY_OMISSION`;
- `PLACEHOLDER_SUBSTITUTION`;
- `EVIDENCE_CARRIAGE_FAILURE`;
- `ESCALATION_ORDER_FAILURE`;
- `SCOPE_INFLATION`;
- `STANDALONE_REVIEW_FAILURE`;
- `PACKAGE_INTEGRITY_FAILURE`;
- `COMPLETION_MISMATCH`;
- `CLAIM_CEILING_VIOLATION`;
- `HUMAN_GATE_REQUIRED`;
- `HUMAN_GATE_DENIED`;
- `LOGIC_FREEZE`; and
- `UNKNOWN_PRODUCTION_FAILURE`.

These are `production_failure_class` values. They do not silently expand the Tranche 2 stop-class enum. An Audit stop may retain `AUDIT_INTERRUPT` while the production event preserves the specific failure class.

## 15. Mandatory Gates

### 15.1 Analytical Inventory Freeze Gate

Reject reporting when:

- required inventory categories are absent;
- source analysis objects are mutable, unreadable, or hash-invalid;
- the freeze omits known material items;
- unresolved ambiguity is silently resolved;
- the Git or contract binding disagrees; or
- the freeze was changed without a new version.

### 15.2 Projection Gate

Reject reporting when:

- the audience or lane is undeclared;
- transformations are undeclared;
- analytical elements lack immutable source references;
- semantic digests disagree;
- a forbidden transformation is requested; or
- presentation-only material is used as analytical support.

### 15.3 Conversation-to-Artifact Reconciliation Gate

Map every required requirement and inventory item to:

requirement
-> analytical object where applicable
-> report element
-> artifact path and anchor
-> artifact digest

An omission is a defect. It is not future work.

The gate must also reject report elements that have no source requirement, analytical object, or declared presentation-only role.

### 15.4 Escalation-Lineage Gate

Where the active route requires the insider-threat hierarchy, the report must preserve:

Anomaly
-> Threat
-> Hidden Threat
-> Insider Threat
-> Offending IDs

Each higher category must reference the inherited evidence and claims of the prior category. Offending IDs remain last.

This ordering is route-specific. It is not imposed on unrelated report types.

### 15.5 No-Placeholder Gate

A required artifact or section cannot be satisfied by:

- a heading without substantive report elements;
- a filename;
- a table of contents entry;
- a future-work list;
- a `Remaining Work` section standing in for requested analysis;
- a template prompt;
- `TBD`, `TODO`, or equivalent unresolved production markers;
- a summary that omits the required analytical body; or
- commentary describing what could be produced.

Placeholder detection cannot rely only on banned words or file size. It must reconcile typed substantive report elements against the required inventory.

### 15.6 Evidence-Carriage Gate

Every cited:

- claim;
- count and denominator;
- graph or visualization;
- ranked identity;
- transition edge;
- classification;
- possible framework mapping;
- method;
- limitation; and
- recommendation

must resolve to a reviewable evidence or analysis artifact through the manifest.

No external reviewer may be required to read the conversation to reconstruct the evidence chain.

### 15.7 Scope and Report-Inflation Gate

Completeness does not require copying the complete analytical corpus into every report.

The projection must contain:

- every required item;
- every dependency needed to understand those items;
- required evidence and limitation surfaces; and
- only additional material with an explicit audience or route justification.

Unnecessary corpus import is a defect when it obscures the requested report, destroys audience fit, or creates unsupported scope.

### 15.8 Standalone Review Gate

A package is standalone only when a reviewer can determine without conversation access:

- what was requested;
- what source boundary was used;
- what analysis was frozen;
- what claims are made;
- what evidence supports them;
- what remains uncertain or unavailable;
- what transformations produced the report;
- what files comprise the package;
- how integrity is verified;
- what the claim ceiling is; and
- what Human Gate state applies.

### 15.9 Package Reopen Gate

After final package assembly:

1. close the writer;
2. reopen the exact final container;
3. reject absolute paths, traversal paths, duplicate normalized paths, and undeclared links;
4. enumerate every file;
5. compare the inventory to the manifest;
6. recalculate per-file SHA-512 digests;
7. verify declared SHA-256 digests where interoperability requires them;
8. verify the package digest;
9. parse or open every required reviewable artifact using its declared verifier;
10. rerun completeness and lineage reconciliation against reopened content; and
11. write an immutable reopen receipt.

The unopened original directory is not sufficient evidence for the final archive.

### 15.10 Claim Ceiling and Mapping Gate

The package must preserve:

- analysis is not authority;
- classification is not proof;
- framework mapping is not compliance;
- Reporting Adaptation is not verdict;
- Review Ready is not Promoted;
- Promoted is not externally delivered unless separately authorized; and
- hash, manifest, receipt, Replay, and Scar are not truth by themselves.

### 15.11 Human Gate Promotion Gate

Only a human decision may move `HUMAN_GATE_REVIEW` to `PROMOTED` or `RETURNED`.

Approval must contain:

- preparation or review-ready receipt reference;
- package manifest and digest;
- exact authorized next state;
- authorized scope;
- authorized target or audience when external movement is included;
- decision reference;
- decision owner `HUMAN`;
- decision time; and
- limitations or conditions.

The runtime cannot synthesize approval from tone, silence, prior approval, report quality, or completion status.

## 16. Substantive Content Contract

Substantiveness is established by reconciled typed content, not word count.

A required report artifact is substantive when:

- it contains the required report-element classes;
- every element resolves to the frozen inventory or a declared presentation-only role;
- required claims and evidence relationships are present;
- uncertainty and limitations are carried;
- required tables or visualizations contain bound data references;
- route-specific ordering is preserved;
- the artifact hash is recorded; and
- a standalone reviewer can interpret its role.

A short artifact may be substantive. A long artifact may be empty.

## 17. Artifact and Manifest Contract

The production manifest must include:

- `manifest_version`;
- `package_id`;
- `package_form`: `DIRECTORY`, `ZIP`, or `SINGLE_ARTIFACT`;
- canonical Git binding;
- candidate Git binding;
- Operational Contract reference;
- request and route references;
- freeze and projection references and hashes;
- production state;
- ordered artifact inventory;
- required and optional designation;
- file role and media type;
- file size;
- SHA-512 digest;
- optional SHA-256 digest where declared;
- report-element references;
- requirement and analytical inventory coverage;
- verifier and parse result;
- standalone-review state;
- reopen receipt reference;
- Human Gate state;
- claim ceiling;
- created time; and
- manifest SHA-512 digest.

The manifest binds identity and continuity. It does not prove factual truth.

## 18. Completion Contract

User-owned completion criteria remain controlling.

The production controller may not declare `REVIEW_READY` merely because:

- tests passed;
- files exist;
- hashes match;
- a ZIP opens;
- the assistant believes the report is sufficient; or
- the package appears professional.

Every user-owned completion criterion must resolve to explicit reconciliation evidence.

Missing criteria cause `COMPLETION_MISMATCH` or a bounded return to `REPORTING`; they are not converted into a future-work appendix.

## 19. Integrity and Temporal Rules

### 19.1 Integrity

- Typed records use canonical JSON.
- Immutable record digests use SHA-512 excluding only the record's own digest field.
- Production transitions and gate receipts are append-only and SHA-512 chained.
- Package files carry SHA-512; SHA-256 is added only where declared for interoperability.
- Archive and directory manifests are deterministic.
- Changed objects are rehashed; unchanged source objects are not redundantly rehashed without a declared reason.
- Optional encryption is route- and material-dependent and never substitutes for provenance, Scar, Replay, or Human Gate.

### 19.2 Temporal separation

The system must preserve distinct:

- source time;
- evidence observation time;
- acquisition time;
- analysis time;
- inventory-freeze time;
- projection time;
- artifact creation time;
- reconciliation time;
- archive time;
- reopen verification time;
- Human Gate request time; and
- Human Gate decision time.

Unknown time remains `null` with a reason. It is not copied from a nearby event.

## 20. Audit, Scar, and Replay Integration

Audit is callable at every production transition.

Audit must interrupt on:

- canonical or contract drift;
- claim mutation;
- lineage break;
- evidence-carriage failure;
- claim-ceiling violation;
- integrity failure;
- repeated non-progress;
- Human Gate bypass;
- false completion; or
- unknown conditions that cannot be safely bounded.

A stopped production operation must:

1. enter terminal `STOPPED`;
2. write a production transition witness;
3. invoke the Tranche 2 Audit stop path;
4. require an immutable Scar;
5. preserve the freeze, projection, manifest, defect inventory, and last verified state;
6. prohibit in-place resume; and
7. use Tranche 3 Replay only to prepare context for a separately authorized new contract.

Replay cannot mutate or reopen the stopped production contract.

## 21. Required Candidate Artifacts

Implementation is expected to add:

- `candidate/v40/contracts/wave1_reporting_production.operational_contract.json`;
- `candidate/v40/contracts/evidence_record.schema.json`;
- `candidate/v40/contracts/analysis_record.schema.json`;
- `candidate/v40/contracts/analytical_inventory_freeze.schema.json`;
- `candidate/v40/contracts/reporting_requirement_inventory.schema.json`;
- `candidate/v40/contracts/report_projection.schema.json`;
- `candidate/v40/contracts/production_state.schema.json`;
- `candidate/v40/contracts/production_event.schema.json`;
- `candidate/v40/contracts/artifact_completeness.schema.json`;
- `candidate/v40/contracts/production_manifest.schema.json`;
- `candidate/v40/runtime/reporting_production.py`;
- `candidate/v40/tools/validate_reporting_production.py`;
- `tests/test_v40_candidate_reporting_production.py`;
- `candidate/v40/receipts/wave1_reporting_production_receipt.md`; and
- a sealed acceptance-fixture directory declared by manifest.

Existing Tranche 1, 2, and 3 records remain immutable. Compatibility changes require explicit schema versioning and regression evidence.

## 22. Insider-Threat End-to-End Acceptance Fixture

The rejected insider-threat reporting route is the required real-world acceptance fixture for operational validation.

It must exercise:

- canonical source and package hashes;
- JSON schema and field definitions;
- analytical procedure;
- execution-signature catalog;
- row-to-signature map;
- identity-to-signature map;
- signature-to-identity map;
- transition-edge list;
- GraphML graph;
- operational shells and interlocks;
- anomaly census;
- threat census;
- hidden-threat census;
- insider-threat candidate table;
- identity ranking;
- full offending-ID assessments at the end;
- calculation rules;
- limitations and evidence gaps;
- core report series;
- README;
- per-file manifest and hashes;
- ZIP reopen verification; and
- Human Gate review.

The required risk order is:

Anomaly
-> Threat
-> Hidden Threat
-> Insider Threat
-> Offending IDs

Each category inherits and references the evidence of the prior category.

### 22.1 Current source boundary

The real insider-threat source dataset and completed analytical corpus are not present in the current repository state.

This specification does not fabricate them.

Therefore:

- implementation may use sealed normative and adversarial fixtures to verify control mechanics;
- the tranche may reach `CONTROL_IMPLEMENTED` after those fixtures pass;
- the tranche may not claim `OPERATIONALLY_VALIDATED`, `REVIEW_READY`, or promoted Wave 1 status until the real rejected operation is loaded, hashed, frozen, produced, reopened, and reviewed; and
- absence of the source package must be recorded as a promotion blocker, not hidden as remaining work.

Passing a shallow synthetic report is insufficient for final operational validation.

## 23. Acceptance Fixtures

Implementation must include at least these fixtures:

1. Current Git binding passes only at the declared canonical and candidate commits.
2. The old Wave 0 Operational Contract cannot be silently rebound or reused as the Wave 1 contract.
3. Canonical or candidate drift stops before report production.
4. A valid evidence record validates and preserves Authority `NONE`.
5. Evidence with unknown provenance remains unknown.
6. Evidence mutation after hashing is rejected.
7. A valid analysis record resolves every claim to evidence or explicit unsupported state.
8. A claim without attribution is rejected.
9. A claim without uncertainty state is rejected.
10. A contradicted or unresolved claim cannot be projected as supported.
11. A risk-inheritance edge cannot be dropped from a dependent higher-risk claim.
12. A valid analytical inventory freeze is immutable and digest-valid.
13. An inventory freeze omitting a known material count, identity, method, limitation, or evidence object is rejected.
14. A changed analysis record requires a new freeze version and invalidates the old projection.
15. A valid requirement inventory preserves user, contract, route, analytical, and governance sources separately.
16. Commentary or a filename cannot satisfy a required production item.
17. A valid projection may translate language without changing structured claim semantics.
18. A valid projection may reorganize or sequence elements while preserving route-required order.
19. A valid visualization preserves source data, units, filters, aggregation, and caption lineage.
20. A projection that changes claim polarity is rejected.
21. A projection that changes actor, scope, time, magnitude, denominator, unit, or risk category is rejected.
22. A projection that removes evidence, uncertainty, contradiction, limitation, or attribution is rejected.
23. A presentation-only element cannot satisfy an analytical requirement.
24. A framework mapping cannot be reported as compliance.
25. A candidate classification cannot be reported as proof or verdict.
26. Reporting callback may request re-analysis but cannot mutate the frozen analysis.
27. A revised analysis creates a new freeze and projection rather than overwriting prior records.
28. The production state machine rejects undeclared transitions.
29. `PROMOTED`, `RETURNED`, and `STOPPED` reject reentry.
30. A bounded artifact defect may return `RECONCILIATION -> REPORTING` without changing route or freeze.
31. A claim or integrity defect cannot use the bounded return path and instead invokes Audit stop.
32. Repeated non-progressing reconciliation returns trigger Logic Freeze, Scar, and later Replay.
33. Every required requirement and inventory item maps to a substantive report element and artifact anchor.
34. Every analytical report element resolves back to a frozen claim and evidence path.
35. A heading-only or filename-only artifact fails the no-placeholder gate.
36. A future-work or `Remaining Work` artifact cannot substitute for requested analysis.
37. Placeholder detection does not reject a substantive limitations section merely because it discusses future evidence needs.
38. Every count, graph, ranked identity, method, limitation, and recommendation passes evidence carriage.
39. The insider-threat fixture preserves Anomaly -> Threat -> Hidden Threat -> Insider Threat -> Offending IDs, with offending IDs last.
40. A concise audience projection passes when it includes every required item and justified dependency.
41. An inflated report containing unnecessary corpus without projection justification is rejected.
42. A package that requires conversation memory fails standalone review.
43. A package with complete explicit context passes standalone review.
44. Missing required files, undeclared extra files, duplicate normalized paths, traversal paths, or links fail package reopen.
45. File, manifest, or archive hash tampering fails closed.
46. Reopened contents are reconciled again rather than trusting the pre-archive directory.
47. `REVIEW_READY` requires exact user-owned completion evidence.
48. Runtime-generated Human Gate approval is rejected.
49. Human return creates terminal `RETURNED`; human approval creates terminal `PROMOTED` but no external delivery unless explicitly authorized.
50. A stopped production operation creates a Scar and Replay can only propose a new contract.
51. The sealed normative fixture leaves the repository tree clean and activates no external runtime.
52. The absent real insider-threat corpus is reported as a promotion blocker and is never fabricated.

## 24. Implementation Units and Commit Discipline

After this specification is reviewed and committed separately, implementation proceeds in this order:

1. re-anchor Git and create the new Wave 1 Operational Contract checkpoint;
2. re-seat active runtime fixtures on the new contract while preserving historical Wave 0 contract immutability checks;
3. add and test evidence and analysis record schemas;
4. add and test claim semantics, uncertainty, limitation, attribution, and risk-inheritance validation;
5. add and test analytical inventory freeze and requirement inventory schemas;
6. add and test report projection and report-element schemas;
7. implement and test projection mutation detection;
8. add and test production state and production event schemas;
9. implement and test the production state controller and Audit interrupt integration;
10. add and test artifact completeness, manifest, substantive-content, and reconciliation gates;
11. implement and test standalone review and package reopen verification;
12. implement and test Human Gate promotion and return receipts;
13. implement sealed normative and adversarial fixtures;
14. run all 52 fixtures and every Tranche 1, 2, and 3 regression;
15. run v39 and 5.6 canonical validation;
16. write the Wave 1 reporting-production receipt;
17. review the complete implementation diff; and
18. commit implementation separately from this specification and the Operational Contract checkpoint.

No architectural improvisation is permitted inside the code phase.

If a required schema, state, transition, transformation, failure class, or gate is missing from this specification, stop and amend the specification in a separately reviewed checkpoint before dependent code.

## 25. Regression Requirements

The implementation is not complete unless:

- all 52 fixtures pass;
- every prior v40 candidate test still passes;
- all candidate validators pass;
- v39 local-call verification passes against the declared canonical state;
- the 5.6 bridge validator passes;
- default validation creates no bytecode, package, result, deployment, or system-population artifact;
- validation never reaches an external runtime;
- prior Operational Contracts, transitions, Scars, Replay receipts, and receipts remain unchanged;
- every schema is closed and fail-closed;
- every digest is independently recalculated during validation;
- every terminal state rejects reentry; and
- the final implementation diff contains no placeholder-only production artifact.

## 26. Definition of Done

This control tranche reaches `CONTROL_IMPLEMENTED` only when:

- the new Wave 1 contract is current and immutable;
- typed Evidence, Analysis, Freeze, Requirement, Projection, Production, Completeness, and Manifest objects exist;
- report adaptation preserves structured analytical meaning;
- natural-language semantic equivalence is exposed for Human Gate review rather than self-certified;
- every required item reconciles to substantive standalone artifacts;
- placeholder and commentary substitution fail closed;
- evidence carriage and route-specific escalation lineage are enforced;
- report inflation is bounded by the declared projection;
- packages are reopened and verified after final assembly;
- Human Gate is non-bypassable;
- Audit, Scar, and Replay integration is complete;
- all regression requirements pass;
- a substantive receipt records the evidence;
- the implementation is committed separately; and
- no publication, external delivery, system population, merge, or canonical promotion occurs.

Wave 1 reaches `OPERATIONALLY_VALIDATED` only after the real insider-threat acceptance fixture also passes.

## 27. Failure Mapping

This tranche primarily addresses:

- `P0-007` Reporting Mutation;
- `P0-008` Analysis / Reporting Collapse;
- `P0-009` Artifact Substitution;
- `P0-010` Provenance Contamination;
- `P0-023` Commentary Substitution;
- `P0-024` Production Failure;
- `P0-025` Evidence Serialization Failure;
- `P0-026` Report Inflation;
- `P0-029` Professional Representation Risk;
- `P0-030` User Time Destruction;
- `P0-035` Unsupported Optimism;
- `P0-039` Execution Ownership Confusion; and
- `P0-040` Contract Enforcement Failure.

This tranche supplies control evidence for those findings. It does not close them automatically.

## 28. Claim Boundary

This specification authorizes no implementation, publication, deployment, merge, promotion, external delivery, system population, compliance claim, legal finding, HR action, or production execution by itself.

It is a candidate engineering boundary under Authority `NONE` and Human Gate `ACTIVE`.

Reporting transfers understanding.

Reporting may change the shape of understanding for an audience.

Reporting may not change what the evidence and analysis mean.

Production carries the complete requested understanding into artifacts.

Production may not substitute structure, commentary, optimism, or future work for the requested result.

Human Gate controls promotion.
