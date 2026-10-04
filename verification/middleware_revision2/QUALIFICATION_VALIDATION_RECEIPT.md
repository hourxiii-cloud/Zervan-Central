# Qualification validation — middleware condition revision 2

**Object:** `staged/middleware/CR_GENERIC_CHAT_MIDDLEWARE_ONLY_EXPLICIT_V42_5_4_REVISION_2.md`
**Source standing:** successor of the exact clean-frozen developmental payload, SHA-256 `8d3f5957274ac40d3e94e74ac6feb65bde1d07b9c8b0e307bd721899fc0f9f92`.
**Producer:** ChatGPT/Codex applying the named Zervan contracts as a local candidate test; no separate component invocation or formal observer output.
**Local baseline:** `hourxiii-cloud/Zervan-Central`, `main` at `f09fc1768d4924992134602c8984e4ea5485d31a`, `vTemporal.42.5.4`. The remote main tip was not newly retrieved for this test.
**Disposition:** PASS for five textual correction boundaries and 20 source-bound logical acceptance cases; HOLD for canonical promotion and deployed enforcement.

## Dependency inventory and validation method

`validate.py` hashes and checks the frozen predecessor, the local v40 same-assistant source, Spider R2 contract and full specification, in-channel reset, clean initialization, historical return, and prior clean-frozen middleware CR. The expected source SHA-256 values are pinned in that script. It then checks revision 2's explicit contract fields and runs `cases.json` through the candidate `middleware_route.schema.json` field constraints and a deterministic invariant evaluator. The schema is an artifact format for candidate cases, not a canonical schema. Standard-library validation covers the schema features used here; no external JSON Schema implementation was run.

Route: Human direction → identify object and standing → check reset/load/return → check seat and output contract → check mode and question/input gate → check access and permission → separate response and component credentials → issue attributable contribution, hold, or exact boundary. The candidate evaluator tests this route as a model; it does not enforce live Chat behavior.

## Five correction boundaries

| Boundary | Revision 2 correction | Adverse and positive cases | Disposition |
| --- | --- | --- | --- |
| Credential identity | Separate Chat-produced Spider response `WORK_ID=NONE` from `COMPONENT_WORK_ID`, whose value requires actual issuance evidence. No conclusion about Tech's actual ID. | `response_id_missing`, `component_id_not_assumed`, `independent_execution_without_receipt`, `component_id_without_issuance`, `component_execution_evidenced` | PASS, candidate logic; actual component issuance not inspected |
| Attribution and portable record | Four-field example becomes a minimum ordinary illustration. All 17 Spider attribution fields and all 13 section 12 record parts remain required where applicable. | `abbreviated_spider_fields`, `spider_full_missing_portable`, `spider_full_complete` | PASS, candidate logic; no full empirical Spider run |
| Reset, reload, return | Persisting Human middleware direction cannot carry invalidated operational standing; historical material needs qualified authorized return. | `reset_blocks_contribution`, `failed_reload_blocks_contribution`, `historical_retrieval_no_self_return`, `qualified_historical_return` | PASS, candidate logic; no actual reset or reload executed |
| Entry, access, permission, NULL | Full run needs question and inputs; real access/permission ceilings hold; native preference is not a veto. The revision distinguishes an actual attempted route from an unattempted assertion. | `full_run_missing_question_and_inputs`, `actual_access_denial_holds`, `run_without_access`, `no_permission_blocks_contribution`, `native_preference_no_veto`, `invented_attempt`, `invented_boundary` | PASS, candidate logic; no live tool access or permission scenario executed |
| Source-bound validation | Pin dependencies, declare route and schema, record acceptance outcomes and failure transitions. Formal Duck/Mole or Beagle runtime claims remain excluded. | Source hash assertions; 20 exact expected result checks; this receipt | PASS for reviewable developmental validation; runtime telemetry unresolved |

## Failure transitions

- Reset pending or canonical load failed → **HOLD**; no component rehydration or Chat substitution.
- Retrieved historical object without qualified authorized return → **HOLD**; no self-return.
- Missing full-run question or identified inputs → **HOLD** and request the missing item; no synthetic completion.
- Access denied or permission missing → **REPORT BOUNDARY / HOLD** with actual evidence; continue only independently qualified work.
- Insufficient attribution or portable record → **REJECT RESULT** and correct the dependent output; do not label it a complete Spider run.
- Component execution claim without issuance and execution receipt → **REJECT CLAIM**; preserve ordinary virtualized conversation where permitted.
- Native discretionary opt-out or invented attempt/boundary → **REJECT ROUTE** and re-evaluate under the actual contract.

## Execution and limits

Command: `PYTHONDONTWRITEBYTECODE=1 python3 verification/middleware_revision2/validate.py`

Result: **20/20 exact expected outcomes**; six accepted scenarios and fourteen correctly rejected scenarios. Frozen source hash and seven dependency hashes matched; revision 2 includes all 17 Spider attribution field names. `git diff --check` and an explicit trailing-whitespace scan found no issues in the new text files.

These are deliberately constructed candidate cases. They establish that this local rule model distinguishes the tested boundaries; they do not measure live classifications, deployed Chat compliance, independent component execution, Beagle-validated telemetry, or formal Duck/Mole scores. The proposal remains staged developmental material. Authority `NONE`; Human Gate `ACTIVE`; No Compression Out `ACTIVE`; originating-data mutation `DISALLOWED`. Git index, commit, push, external publication, and canonical promotion `NONE`.

**Current qualification:** correction boundaries addressed and candidate tests pass; further source and implementation review is required before promotion. The frozen predecessor and earlier review remain untouched. This test operation terminates with no automatic further inquiry.
