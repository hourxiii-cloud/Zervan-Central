# Admission Layer Clarification — Canonical Placement

## Authority Surface

`Admission/` is a **unified authority surface** within `zervan-core`.

All logic that decides **whether evidence may enter the Zervan pipeline** belongs **only** under this layer.

No admission logic may live:
- at the repository root
- under `Chunking/`
- under `Beagle/`
- under `Accelerator/`
- or inside any analysis or governance component

---

## Module Placement

**Project_LeafcutterAnt** is a **bounded module** within the Admission layer.

Correct placement:
