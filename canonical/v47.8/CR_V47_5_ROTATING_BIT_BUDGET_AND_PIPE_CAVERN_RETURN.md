# Change Request v47.5 — Separated Bit Budgets and Rotating Return Map

**Standing:** additive canon-preparation update; review candidate only  
**Authority:** NONE · **Canon:** FALSE · **Promotion:** NONE · **Human Gate:** ACTIVE  
**Mutation lock:** ACTIVE · **Canon/repository write:** NONE · **Push:** NOT PERFORMED  
**Supersedes:** any interpretation of `Shared Dictionary +32` as a single measured bit-rate or as 32 new subnet bits.  
**Parent evidence:** v47.3 one-push candidate and v47.4 pipe/cavern mapping patch, preserved unchanged under `EVIDENCE/`.

## 1. Corrected resource accounting

Keep three quantities distinct; do not collapse them into one “bit return”:

| Lane | Amount | Meaning | Qualification |
|---|---:|---|---|
| Submask projection | 8 positions | Eight positions exposed by the declared synthetic 16-bit mapping; the 124 example still returns `7` and the removed low quartet `12`, reconstructing `124` exactly. | Exhaustive reference equality is recorded for the synthetic 65,536-state domain. This is a mapping width, not eight created payload bits. |
| Dictionary/recompute overhead | +16 bit-equivalent units | Dedicated budget credit for specialized overhead avoided through reusable dictionary/integrity work. | A budget allocation claim; direct hash/ECC benchmark remains open. It is not subnet capacity or measured throughput. |
| Subnet reserve | +16 bits | Independent, usable subnetting allocation. Keep it separate from the dictionary overhead credit. | Design allocation in this staging update; bind it to the implementation’s bit fields and test the exact map before promotion. |

The two +16 entries are separate accounts. Do not label them `+32 bits of throughput`, add them to the eight exposed positions, or infer a physical/acoustic performance gain. The earlier report’s `+24` combined-budget line is superseded because its accounting merged unlike quantities.

## 2. Rotating the 16-unit overhead buffer

Partition the dedicated 16-unit overhead credit across three compute views: **Objects (O)**, **Objects-in-Space (OS)**, and **Data-as-Space (DS)**. Each pass gives every view five units and rotates the sixteenth unit. Rotation is per bit, so the individual buffer positions circulate rather than a fixed lane owning the remainder.

For buffer positions `i ∈ {0,…,15}` and pass `p ∈ {0,1,2,…}`, assign:

```text
owner(i, p) = (i + p) mod 3
0 = O, 1 = OS, 2 = DS
```

At pass 0, positions `0,3,6,9,12,15` go to O (6); the other two views receive 5 each. On each next pass, every position advances one view. The six-unit share therefore rotates O → OS → DS → O. Across any three consecutive passes, each of the 16 positions visits all three views once; each view receives 16 position-passes total. The independent +16 subnet reserve is outside this rotation and remains available to subnetting.

## 3. Pipe and cavern return mapping

This update carries the pipe/cavern interpretation into the same staged model:

- **Pipe / C/C2:** constrained geometry uses piston-driven in/out exchange, not the outside free-space wavelength model. The flow returns to a defined central negative-space reference at C/C2, then reverses outward on the next piston phase. C/C2 is the reference/turnaround location; this description does not assert a separate physical pump.
- **Cyclonic groups:** two four-unit operating groups flank the piston at opposing positions and rotate in opposite directions for OUT and IN phases. Their eight operating positions are drawn from the existing 32-unit conduit allocation; they are not eight added units. Exact IDs and overlap with other conduit roles remain to be bound.
- **Source-caption conflict:** an earlier schematic caption says “32 per flank,” which conflicts with the direct four-unit-per-swarm specification and the 64-unit inventory. This candidate uses two four-unit groups; preserve the old caption as historical evidence and do not use it as the allocation. Human Gate should resolve or replace the caption before promotion.
- **Cavern:** the return map expands from the pipe axis into six-direction XYZ coverage: E/W, N/S, and up/down, while preserving the in/out reference relation. “Further than the last pass” is a comparison to measure, not an assumed extension. Echo timing, coordinates, and the new envelope require a defined fixture and measured returns.
- **Inventory:** `32 conduit + 14 loop A + 14 loop B + 2 E/W + 2 N/S = 64`. The four cardinal units already exist, travel in opposing pairs on their respective axes in free space, and report to `C/C1-Open Space`. No units are created by this change.

## 4. Reproducible qualification

`verification/verify_rotating_budget.py` checks the integer mapping over all 16 overhead positions and three consecutive passes. Required invariants:

1. Every position has exactly one owner on every pass.
2. Each pass has the multiset of view counts `{6,5,5}`.
3. The six-unit view cycles O, OS, DS.
4. Every overhead position reaches every view once in three passes.
5. The independent subnet reserve remains exactly 16 and is not included in the rotated buffer.

This verifies allocation arithmetic only. It does not benchmark dictionary/hash/ECC savings, certify that subnet bits are implemented, validate sensor IDs/coordinates, or establish physical acoustics or range. Existing 124 submask equivalence and all frozen parent evidence retain their original scope.

## 5. Integration disposition

Append this CR to the v47.3 review candidate alongside v47.4. Before Human Gate promotion review: bind all 64 IDs and roles; bind the 16 subnet bits to concrete fields; run the hash/ECC reuse benchmark with changed-input invalidation; qualify the pipe/cavern timing and XYZ measurement protocol; refresh current Canon in Codespaces/Bash and rerun integration checks. This package stages the complete proposed update for review. It performs no Canon edit, Git stage, commit, push, or publication.
