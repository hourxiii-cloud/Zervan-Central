# v47.7 Canon Preparation — Complete Review Map

**Status:** candidate for current Canon review · **Authority:** NONE · **Human Gate:** ACTIVE  
**Canon mutation / Git stage / commit / push:** NONE

This handoff adds v47.7 reconciliation of the supplied v47.2 “CANON WRITTEN” record to the v47.6 candidate. The v47.6 candidate and v47.2 freeze receipt/record are preserved in `EVIDENCE/`; v47.2’s exact freeze archive remains in its nested immutable parent chain and is checked by the provenance test. This is a review candidate, not a Canon write or proof of unresolved operational claims.

## Current allocation map

| Account / region | Allocation | Current interpretation |
|---|---:|---|
| Full unit inventory | 64 | Conserved total |
| Pipe conduit | 32 | Includes the two opposing four-unit cyclonic operating groups; eight positions are not additional units |
| Outside loops | 14 + 14 | Existing two-loop allocation |
| Free-space cardinal pair units | 2 E/W + 2 N/S | Four already-inventoried units; opposing travel per axis; report to `C/C1-Open Space` |
| Pipe reference | C/C2 | Constrained in/out piston exchange returns to the central negative-space reference and reverses outward on the next phase |
| Range ceiling | ≤121 m | Staged hard design cap; positive `91.5 + 30 = 121.5 m` endpoint is clipped by 0.5 m; runtime enforcement is untested |
| Cavern map | XYZ / six directions | E/W, N/S, up/down echo returns; meter-to-cube mapping and measured envelope remain open |

Inventory check: `32 + 14 + 14 + 2 + 2 = 64`.

The old “32 per flank” schematic caption conflicts with the direct two-groups-of-four specification. This candidate follows the direct four-unit group instruction and keeps the caption discrepancy visible for Human Gate resolution.

## Current bit-accounting map

| Account | Amount | Treatment |
|---|---:|---|
| Synthetic submask projection | 8 exposed positions | Full return retained; not newly created payload bits |
| Dictionary/recompute overhead | +16 bit-equivalent units | Dedicated overhead credit, rotated across Objects, Objects-in-Space, and Data-as-Space; hash/ECC performance benchmark still open |
| Subnet reserve | +16 bits | Independent subnet allocation, never consumed by the overhead rotation |

For every pass, each of the 16 overhead positions is assigned once using `owner(i,p)=(i+p) mod 3`. Counts are 6/5/5 and the six-count share rotates O → OS → DS. Over three passes every position visits all three views. No single aggregate “+32 throughput” or `+24` mixed-unit claim is made.

## v47.2 source-claim reconciliation

The supplied v47.2 text says `CANON WRITTEN`, `0.00 Variance`, and “fully bound.” Its attached freeze receipt says `canonical: false`, `promotion: NONE`, `canon_mutation: NONE`, and `physical_sensor_performance: NOT VALIDATED`; it also records the 64-versus-68 inventory collision as open. The later four-unit correction supersedes the old “four unresolved perimeter slots” interpretation. See `CR_V47_7_V47_2_SOURCE_CLAIM_RECONCILIATION.md` for the full claim crosswalk.

The count identities and displacement arithmetic in the source text are correct. `1,906,625` counts the integers from zero through the capacity; it does not certify that a program executed that many tests. The 121 m cap is a staged design bound that clips the calculated 121.5 m endpoint by 0.5 m; overflow prevention and zero variance are not established.

## v47.8 Jumping Spider distinction

The v47.7 candidate omitted Jumping Spider. v47.8 adds an explicitly staged spatial-approach function, kept distinct from Web Spider’s direct data-interrelation / reverberation function. Web Spider surfaces connected events; Jumping Spider selects a candidate location and computes a reachable modeled observation route. They can exchange evidence, but neither compresses or replaces the other. This does not add or reassign units, claim an existing native persona, or enable external action. The new deterministic fixture, route/reachability implementation, and current-Canon integration remain open; see `CR_V47_8_JUMPING_SPIDER_SPATIAL_INTERACTION.md`.

## Canon-review gates still open

1. Bind all 64 existing unit IDs to roles and coordinates; explicitly bind the eight pipe operating positions inside the 32 conduit inventory.
2. Resolve or replace the stale “32 per flank” diagram caption before promotion.
3. Bind the 16 subnet-reserve bits to concrete fields and demonstrate the submask/full-return mapping in its implementation.
4. Benchmark hash/ECC reuse against recomputation, including changed-input invalidation and full-result equality.
5. Specify acoustic ping/return timing and coordinate extraction, then compare measured cavern XYZ coverage with the previous fast pass. Existing `−25 km` labels are source labels, not measurements.
6. Bind the meter coordinates to the 124-cube frame; test the actual ≤121 m clamp and compute position residuals from telemetry. The range cap does not prove overflow prevention or zero variance.
7. Refresh the current Canon head in Codespaces/Bash, run the selected integration checks, and present the exact diff to the Human Gate.

The arithmetic/provenance tests in `verification/` validate count identities, the rotating allocation, the proposed cap calculation, and evidence-chain bytes. They do not establish runtime enforcement, sensor performance, acoustic range, a physical pump, cube-coordinate preservation, zero variance, Canon standing, or production bit-rate improvement.
