# Zervan Operator Contract

## Definition
An operator is a deterministic, side-effect-bounded computation unit invoked by the generated conductor.

Operators are persistent code.
Their invocation is ephemeral.

## Identity
Each operator is identified by a stable string ID referenced in Run Plan IR:
- Example: normalize.cert_event
- Example: model.random_forest

## Inputs
- Operators MAY receive:
  - Structured parameters from IR
  - Explicit upstream outputs
- Operators MUST NOT:
  - Access filesystem outside allowed temp scope
  - Access network
  - Access cryptographic keys

## Outputs
- Operators MUST return structured, serializable outputs
- Outputs MUST be hashable and bindable
- Outputs MUST NOT persist themselves

## Determinism
- Deterministic operators MUST be deterministic given identical inputs
- Stochastic operators MUST accept an explicit seed

## Security
- Operators MUST NOT:
  - Perform dynamic imports
  - Execute shell commands
  - Load plugins dynamically
  - Modify global state

## Failure
- Operators MUST fail fast
- Errors MUST be structured and surfaced to diagnostics

## Trust Boundary
- Operators are trusted code
- Operator execution context is untrusted
