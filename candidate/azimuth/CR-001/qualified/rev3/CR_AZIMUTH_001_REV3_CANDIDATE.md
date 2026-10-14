# CR-AZIMUTH-001 — REVISION 3 DEVELOPMENTAL CANDIDATE

## Control
Baseline: REV2 CLEAN FULL FROZEN (preserved verbatim in this package). Zervan baseline vTemporal.48.1.3. Status: CR DEVELOPMENTAL CANDIDATE; NOT FROZEN; NOT CANONICAL. Authority NONE. Human Gate: approved for analysis only. No Compression Out ACTIVE. Producer: ChatGPT. No repository writes, runtime execution, or canonical promotion.

## Material finding: first-class relational object
An established relationship may be modeled as an independently addressable OBJECT/STATE, not only an edge attribute of a participant. Let O_A and O_B be endpoint objects, and O_R a distinct relationship object with its own identity, immutable state revisions, provenance, and continuity policy.

O_A <--endpoint-A-- O_R --endpoint-B--> O_B

A_F(O_R,s_R,k)=(I_R,R_R,k,S_R,k,T_R,k,X_R,k,V_R,k)

The six typed dimensions remain unchanged; no seventh dimension is introduced. Relationship objects can reference other relationship objects, subject to declared graph constraints and cycle handling.

## Required distinction
Historical relationship existence is not evidence of present activity, contact, mutual intention, current physical location, or continuing obligations. A relational object can be historically established while its present operational state is UNKNOWN, INACTIVE, DISPUTED, or OBSERVED_ACTIVE; each state requires evidence and temporal scope. Relational objects are analytical records, not surveillance access or inferred private facts.

## Candidate state schema
- relation_oid: namespace-qualified persistent identity
- relation_type: typed semantics and scope
- endpoints: role-labeled object references; allow n-ary relations by policy
- validity: claimed effective interval, observation time, recorded time; explicit uncertainty
- activity_standing: OBSERVED_ACTIVE | OBSERVED_INACTIVE | HISTORICAL | UNKNOWN | DISPUTED (not an exhaustive ontology)
- evidence_refs: observations, records, receipts, conflicts
- state_revision: immutable identifier; prior state links
- transformation_lineage: state changes, derivations, corrections
- verification_standing: scoped assessment, not automatic truth
- privacy/access: declared authorization and disclosure boundary

## Invariants proposed for addition
RINV-01: relationship identity independent of endpoint identity.
RINV-02: endpoint state changes do not silently mutate relationship state.
RINV-03: historical existence and current activity are separately represented.
RINV-04: absent observation does not imply active or inactive status.
RINV-05: every relational claim retains source, time scope, and challenge path.
RINV-06: missing endpoint, conflicting evidence, and temporal overlap remain visible.
RINV-07: relation-of-relation traversal is bounded and cycle-safe.
RINV-08: disclosure of relational coordinates respects privacy and authorization.

## Qualification tests to design and execute
RT01 Create two endpoints and one relation object; verify three identities.
RT02 Change endpoint state; verify relation unchanged absent explicit event.
RT03 Mark relationship HISTORICAL, then current activity UNKNOWN; no invented current contact.
RT04 Contradictory evidence yields DISPUTED, not silent overwrite.
RT05 Verify n-ary roles and relation-to-relation cycles without infinite traversal.
RT06 Duplicate relation observations across subnets retain shared provenance and are not counted as independent evidence.
RT07 Test event-time versus observation-time corrections and immutable revisions.
RT08 Verify unauthorized disclosure requests fail closed.

## Integration hypothesis
AZIMUTH can index relationship objects; Cavern may compare their states; Pipe may transport their qualified representations; SKYFALL may replicate logical snapshots without multiplying originating evidence. These are integration hypotheses, NOT validated implementation claims.

## Open questions
Relationship identity issuance and continuity; whether to distinguish relationship and event objects; graph cardinality; temporal overlap semantics; address encoding; privacy/access policy; relation lifecycle and deletion/retention; performance at scale; test fixtures and execution.

## Standing and receipt
Conceptual consistency review: PASS for CR development. Test execution: NOT PERFORMED. Repository promotion: NOT PERFORMED. REV2 remains unchanged and frozen. REV3 is a candidate pending human review and qualification; do not call it a clean/full freeze without a separate gate decision.
