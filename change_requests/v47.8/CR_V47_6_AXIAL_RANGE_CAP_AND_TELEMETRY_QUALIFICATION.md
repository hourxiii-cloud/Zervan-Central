# Change Request v47.6 — Axial Range Ceiling and Telemetry Qualification

**Standing:** additive staging correction to the v47.5 one-push review candidate  
**Authority:** NONE · **Canon:** FALSE · **Promotion:** NONE · **Human Gate:** ACTIVE  
**Mutation lock:** ACTIVE · **Canon/repository write:** NONE · **Push:** NOT PERFORMED

## Corrected limit

Record the proposed maximum range as a hard design cap of **121 m** (`range ≤ 121 m`). The prior positive displacement calculation is:

\[
S_0 + \Delta x = 91.5\text{ m} + 30.0\text{ m}=121.5\text{ m}.
\]

Applying the proposed cap gives:

\[
S_{\text{allowed}}=\min(121.5\text{ m},121.0\text{ m})=121.0\text{ m},
\qquad
\text{clipped excess}=0.5\text{ m}.
\]

For the negative displacement, `91.5 m − 30.0 m = 61.5 m`, which is within that cap. The 121 m value is therefore an explicit staged ceiling that clips the computed positive endpoint by 0.5 m; it is not the unmodified result of `91.5 + 30`.

## What this does and does not establish

- The cap is a design boundary to enforce in telemetry and swarm-coordinate validation. This arithmetic does not demonstrate that runtime code enforces it or that any observed swarm previously crossed it.
- The earlier description of a **critical buffer overflow being prevented** is withdrawn as an established result. No buffer size, address calculation, overflow trace, or runtime boundary test was provided. Treat overflow prevention as an unverified risk hypothesis until such evidence exists.
- A 124-unit cube has `124³ = 1,906,624` cells. This is a count. No unit conversion or mapping from meters to cube coordinates/cell indices is specified, so the 121 m cap cannot yet be said to preserve that cube boundary or prevent grid escape.
- “Zero variance achieved,” “zero bleed,” and “integrity verified” are not supported by this calculation. Retain zero variance only as a target until coordinate telemetry is supplied and the residual is computed over a defined interval.
- The 121 m cap may shorten the prior 121.5 m positive endpoint. Any effect on the claimed cavern coverage must be measured against the prior pass; do not infer coverage from the cap alone.

## Test and integration requirement

`verification/verify_range_cap.py` checks the stated decimal arithmetic and cap clipping. It is not a hardware or runtime bounds test. Before promotion, bind the meter coordinates to the 124-cube frame, define inclusive boundary and rounding semantics, test the actual telemetry clamp at and above 121 m, test the piston/swarm trajectory against those coordinates, and calculate variance from measured position samples. Preserve Human Gate and current-Canon Codespaces/Bash review requirements.
