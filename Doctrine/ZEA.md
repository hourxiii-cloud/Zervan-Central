# ZEA — Zervan Execution Architecture

ZEA defines the **architectural constitution** of Zervan: boundaries, contracts, and lawful flows.

ZEA answers: **“What is allowed to connect to what, and under which rules?”**

---

## Scope (What ZEA governs)

- Layer boundaries:
  - DoctrineOps (Truth & Control Plane)
  - Observers (perception, no mutation)
  - Engines (authoritative state changers)
  - Modules (interpret/report/actuate within contracts)
- Interface contracts (inputs/outputs, required metadata)
- “No bypass” rules (anything that touches canon must pass gates)
- Canonical directory semantics (what belongs where)

---

## Non-Negotiables

- No component may bypass DoctrineOps.
- Observers may not mutate state.
- Engines are the only lawful state changers.
- All mutation must be permissioned and traceable (PMC).
- All recursion must be governed and bounded (Oraborus).

---

## Artifacts (Eventually)

- Contract schemas (JSON/YAML as needed)
- Interface definitions
- Data-flow diagrams
- Gate definitions (Gate 0 → Gate N)

---

## What does NOT live here

- Equations / collapse math (→ ZEE)
- Change approval mechanics (→ PMC)
- Recursion termination logic (→ Oraborus)
