# Zervan Compiler

## Role
The compiler translates a validated Run Plan IR into an ephemeral executable conductor.

## Inputs (Required)
- manifest.schema.json (validated)
- run_plan.ir.schema.json (validated)
- crypto_policy.yaml

## Outputs
- generated_pipeline.py (ephemeral)
- diagnostics.json (sealed)
- outputs/* (sealed)

## Forbidden Behaviors
- No network access
- No persistence outside build directory
- No reading keys from repo
- No dynamic imports outside allowed operators

## Ephemerality
- Build directory MUST be wiped post-run
- Generated code MUST NOT survive beyond TTL

## Determinism
- Deterministic runs MUST reproduce identical IR
- Stochastic runs MUST record seed

## Trust Model
- Compiler is trusted code
- Generated code is untrusted and disposable
