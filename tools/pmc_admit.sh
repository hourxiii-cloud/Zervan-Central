#!/usr/bin/env bash
set -euo pipefail

# PMC ADMIT — "availability-bounded truth under an evidence envelope"
#
# Requires:
#   - A sealed repo fingerprint file (default: ./pmc_seal/repo_fingerprint.sha256)
# Optional:
#   - A dataset path to admit (hashes it and writes admission record)
#
# Usage:
#   ./tools/pmc_admit.sh
#   ./tools/pmc_admit.sh --dataset path/to/file.csv

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SEAL_DIR="${SEAL_DIR:-pmc_seal}"
LOG_DIR="${LOG_DIR:-pmc_logs}"
SEALED_FP_FILE="${SEALED_FP_FILE:-${SEAL_DIR}/repo_fingerprint.sha256}"

mkdir -p "$SEAL_DIR" "$LOG_DIR"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

DATASET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset)
      DATASET="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1"
      exit 2
      ;;
  esac
done

if [[ ! -f "$SEALED_FP_FILE" ]]; then
  echo "ERROR: Missing sealed fingerprint: $SEALED_FP_FILE"
  echo "Run: ./tools/pmc_seal.sh  (we'll create it in Step A)"
  exit 1
fi

SEALED_FP="$(tr -d '\n' < "$SEALED_FP_FILE")"

# Compute current fingerprint using the same algorithm as smoke
CUR_FP="$(
  find Accelerator Doctrine tests -type f -print0 \
    | sort -z \
    | xargs -0 sha256sum \
    | sha256sum \
    | awk '{print $1}'
)"

ADMIT_ID="$(date -u +"%Y%m%dT%H%M%SZ")_$(git rev-parse --short HEAD 2>/dev/null || echo "nogit")"
OUT="${LOG_DIR}/pmc_admit_${ADMIT_ID}.txt"

{
  echo "PMC ADMIT RECORD"
  echo "UTC: $(ts)"
  echo "REPO: $(git remote get-url origin 2>/dev/null || echo 'no-origin')"
  echo "HEAD: $(git rev-parse HEAD 2>/dev/null || echo 'nogit')"
  echo "BRANCH: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'nogit')"
  echo
  echo "SEALED_FP_FILE: ${SEALED_FP_FILE}"
  echo "SEALED_FP: ${SEALED_FP}"
  echo "CURRENT_FP: ${CUR_FP}"
  echo
} > "$OUT"

if [[ "$CUR_FP" != "$SEALED_FP" ]]; then
  {
    echo "RESULT: REJECT"
    echo "REASON: repo fingerprint mismatch"
  } >> "$OUT"
  echo "REJECT: repo fingerprint mismatch"
  echo "See: $OUT"
  exit 3
fi

# Optional dataset hashing
if [[ -n "$DATASET" ]]; then
  if [[ ! -f "$DATASET" ]]; then
    {
      echo "RESULT: REJECT"
      echo "REASON: dataset not found: $DATASET"
    } >> "$OUT"
    echo "REJECT: dataset not found: $DATASET"
    echo "See: $OUT"
    exit 4
  fi

  DS_SHA="$(sha256sum "$DATASET" | awk '{print $1}')"
  DS_BYTES="$(wc -c < "$DATASET" | tr -d ' ')"

  {
    echo "DATASET_PATH: $DATASET"
    echo "DATASET_SHA256: $DS_SHA"
    echo "DATASET_BYTES: $DS_BYTES"
  } >> "$OUT"
fi

{
  echo "RESULT: ADMIT"
  echo "CONDITION: Availability-bounded truth under this evidence envelope (repo fingerprint match)."
} >> "$OUT"

echo "ADMIT: OK"
echo "Record: $OUT"
