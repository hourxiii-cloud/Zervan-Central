# CANON INTEGRATION NOTES

Target baseline: vTemporal.42.5.2
Requested destination: main
Human intent: canon update alongside the current v42.5.2 canonical line.

This package does not itself claim canonical promotion. It carries the qualified Clean Room CR and clean-freeze receipt for Human-controlled integration.

Recommended repository placement:
- change_requests/CR_CLEAN_ROOM_TERMINAL_IDENTITY_REFERENCE_WITHOUT_RETURN.md
- canonical/clean_room/CLEAN_ROOM_IRREVERSIBLE_IDENTITY_DEQUALIFICATION.md
- verification/clean_room/CLEAN_FREEZE_RECEIPT.md

Required integration preservation:
- vTemporal.42.5.2 identity remains unchanged unless Human separately authorizes version change.
- Authority NONE.
- Human Gate ACTIVE.
- No Compression Out ACTIVE.
- Existing canonical RETRIEVABLE ≠ SELF-RETURNING remains intact.
- Existing Box / superposition CR remains intact.
- Inverse-Box mechanism remains unresolved and must not be silently implemented during canon integration.
- Canon promotion requires an explicit promotion receipt / repository state establishing Canonical TRUE for the integrated object.
