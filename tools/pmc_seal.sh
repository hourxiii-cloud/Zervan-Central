#!/usr/bin/env bash
set -euo pipefail

# PMC SEAL — writes the repo fingerprint into ./pmc_seal/repo_fingerprint.sha256
# This becomes the baseline for PMC admission checks.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SEAL_DIR="${SEAL_DIR:-pmc_seal}"
mkdir -p "$SEAL_DIR"

OUT="${SEAL_DIR}/repo_fingerprint.sha256"

FP="$(
  find Accelerator Doctrine tests -type f -print0 \
    | sort -z \
    | xargs -0 sha256sum \
    | sha256sum \
    | awk '{print $1}'
)"

echo -n "$FP" > "$OUT"
echo "SEALED: $OUT"
echo "FP: $FP"
