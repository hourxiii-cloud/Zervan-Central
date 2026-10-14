# AZIMUTH ↔ OSPREY reciprocal bridge — STAGED CANDIDATE

**Base repository:** hourxiii-cloud/Zervan-Central  
**Pinned base commit:** `61c65bbee55d538fb7c737f8b979fbbb7d24c014`  
**Baseline:** vTemporal.48.1.3  
**Authority:** NONE | **Human Gate:** ACTIVE | **No Compression Out:** ACTIVE

## Purpose

Executable, pure-Python, dependency-free bounded reciprocal *contract* for Azimuth analytical coordinates and Osprey contextual returns. This package does not alter existing canonical artifacts or observer contracts. It does not invoke an Osprey runtime, fetch external data, locate people, or claim integration validation.

## How it works

1. Supply a question, a six-dimensional coordinate map, object/Room/operation identity, permitted scope, and evidence references.
2. Osprey (external to this package) may evaluate only permitted context and return an attributable bounded result.
3. `qualify(request, [return1, return2, ...])` validates every return against the originating request, preserves distinct round receipts, and stops repeated identical returns.
4. A human may inspect the results and authorize another round; no loop grants authority, expands evidence, or promotes canonical state.

**Critical distinction:** This is a validated message-boundary implementation, *not yet* an integrated bidirectional runtime. Connecting a real Osprey invocation to the request/return adapter is subsequent staged integration work.

## Install through Codespaces

Upload ZIP to repository root, then:

```bash
unzip -o AZIMUTH_OSPREY_RECIPROCAL_STAGE.zip -d .
python -m unittest discover -s stage/azimuth_osprey/tests -t stage/azimuth_osprey -v
```

Only files under `stage/azimuth_osprey/` are installed. No canonical file is overwritten. Inspect `stage/azimuth_osprey/RECEIPT.json` and `stage/azimuth_osprey/MANIFEST_SHA256.txt` before a human-controlled commit. Do not promote on test success alone.

## Missing qualification

- Real Osprey invocation and Azimuth return-to-next-request adapter
- End-to-end integration tests against the actual repository runtime
- Security, concurrency, throughput, and performance validation
- Human Gate review for any later promotion
