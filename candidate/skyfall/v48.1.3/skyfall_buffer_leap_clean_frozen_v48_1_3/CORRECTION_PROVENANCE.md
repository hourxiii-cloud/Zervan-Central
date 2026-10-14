# v48.1.3 Correction Provenance — No Compression Out

## Input pressure preserved

The input proposed a `118/3` tri-channel leap and asserted:

- a three-meter spatial offset;
- a three-meter network transit reserve;
- a 110-meter deployment radius;
- `39.333333 clicks` per channel;
- equal `1/3, 1/3, 1/3` behavior;
- skipped verification latency;
- automatic rehydration;
- physical or network security conclusions.

## Material corrections

| Input representation | Corrected representation |
|---|---|
| Three-meter initiating offset | `r_min`, tightest admissible circle; numeric value unresolved |
| Three-meter transit reserve | Rejected; channel count does not create distance reserve |
| 110-meter deployment radius | Rejected |
| `39.333333 clicks` | `118/3 = 39 1/3 miles` |
| Three equal identity partitions | Rejected because `248 mod 3 = 2` |
| Three analytical channels | Three full replicated 248-identity snapshots |
| Two anchors are stationary under off-diagonal mixing | Two non-selected lanes explicitly hold the verified snapshot |
| Verification time zeroed | Gate 1, Gate 2, and reconciliation remain explicit timing terms |
| Gate 2 catches all drift | Gate 2 catches only modeled exact-state deviations |
| Automatic rehydration | Explicit verified reconciliation |
| Physical range/performance | Not validated |
| v48.1.2 `118-mile total span` | Rejected; 118 miles is the step-distance basis |
| v48.1.2 `39 1/3-mile per-channel span` | Rejected; `39 1/3 miles` is the selected-channel distance per step |
| Channels as spatial partitions | Rejected; channels coordinate replicated state |

## Preserved idea

One analytical lane may advance from an already verified checkpoint while two
other lanes retain the full admitted reference. The advancing result cannot be
committed until it exactly matches the deterministic transform independently
derived from the anchored state.

## Standing

```text
OBJECT: SKYFALL — VERIFIED THREE-LANE BUFFER LEAP CANDIDATE
VERSION: vTemporal.48.1.3
STANDING: POST-FREEZE CANDIDATE
AUTHORITY: NONE
HUMAN GATE: ACTIVE
NO COMPRESSION OUT: ACTIVE
```

This block records the input standing before qualification. It is provenance,
not a final freeze. v48.1.2 is preserved as a rejected material-error record
and is not a valid promotion source.
