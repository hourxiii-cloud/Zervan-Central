# Change Request v47.4 — 64 Unit Pipe and Cavern Echo Mapping

**Canon stage:** `STAGED_ADDITIVE_PATCH_FOR_CURRENT_CANON_REVIEW`
**Standing:** developmental patch for the pending v47.3 one-push review candidate
**Canon:** FALSE · **Promotion:** NONE · **Authority:** NONE · **Human Gate:** ACTIVE
**Mutation lock:** ACTIVE · **Repository write / push:** NONE
**Patch parent:** `Zervan_v47_3_One_Push_Review_Handoff_Candidate.zip`
**Parent SHA-256:** `c5757a3da3cc7f7d3905e1c1cad2a6270b6e3b200d79ccc84981bb3ec88562f8`

## Change

Clarify the non-sight mapping across the pipe-to-cavern transition. The same 64 inventoried units provide the echo-location mapping; this update adds no units and does not change the existing inventory partition.

- **Constricted pipe:** ping/return mapping follows the axial in/out path. C/C2 is the known negative-space reference. The piston drives the exchange; C/C2 is not described as a central pump. The opposing four-unit swarms flank the piston and shape the counter-rotating in/out motion already recorded in v47.3.
- **Cavern:** the return map opens into volumetric XYZ coverage. It retains the in/out relation and adds up/down returns, extending the same non-sight mapping vertically through the cavern.
- **Inventory:** all 64 units remain conserved. The four N/S/E/W free-space units remain part of the existing inventory and report to C/C1-Open Space. No 65th unit or added sensor is implied.

## Qualification boundary

This is a geometry and function clarification for staging. It does not supply sensor IDs, coordinates, timing, waveform, acoustic range, accuracy, or a measured XYZ envelope. It does not update the prior axial span figures or establish reach beyond a previous fast pass. The earlier `−25 km` label remains a source label, not measurement evidence. Frozen v47.2 evidence and the v47.3 swarm correction remain preserved as parent evidence.

## Canon-stage disposition

Append this CR to the pending v47.3 review package as an additive staging delta. Before promotion, bind the 64 unit IDs and operating roles to the map, define the echo timing/coordinate procedure, compare the resulting XYZ envelope with the prior pass, and run the read-only package checks in Codespaces/Bash against current Canon. Human Gate review remains required. No Canon or repository state is changed by this patch.
