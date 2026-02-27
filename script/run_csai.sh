#!/usr/bin/env bash
# run_evaluations.sh
# ────────────────────────────────────────────────────────────
# Hard‑coded list of report *prefixes* to process.
# For each prefix the pipeline runs:
#   1) make_verfication_report.py   → creates <prefix>_n.verify.md
#   2) make_report_score.py         → produces output_eval/<prefix>/summary.json
# After all prefixes are processed a single call to make_tableandchart.py
# builds combined radar PNGs + the Excel workbook.
# --------------------------------------------------------------------
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt


# ✏️  EDIT PREFIXES AS NEEDED
PREFIXES=(
  gpt5.2_fast
)

# --------------------------------------------------------------------
# Configurable options
ROOT="data/csai"          # where 1/,2/,3/… live
OUT="output/csai"            # destination for make_report_score outputs
EVAL_MODEL="gpt-5.2"           # model for make_report_score.py claude-sonnet-4-20250514 ,o3,o4-mini, gpt-5
SAMPLES="1-10"                      # numeric folders 1..SAMPLES
# --------------------------------------------------------------------
set -euo pipefail

if (( ${#PREFIXES[@]} == 0 )); then
  echo "❌  PREFIXES array is empty. Edit run_evaluations.sh first." >&2
  exit 1
fi

echo "▶️  Running pipeline for prefixes: ${PREFIXES[*]}"

for P in "${PREFIXES[@]}"; do

  echo -e "\n=== [$P] 1️⃣ run_information_verification.py ==="
  python run_information_verification.py \
    --root "$ROOT" \
    --prefix  "$P" \
    --samples "$SAMPLES" \
    --output_root "$OUT" || { echo "verification failed for $P"; exit 1; }
  
  echo -e "\n=== [$P] 2️⃣ run_report_evaluation.py ==="
  python run_report_evaluation.py \
    --root "$ROOT" \
    --prefix     "$P" \
    --eval_model "$EVAL_MODEL" \
    --samples    "$SAMPLES" \
    --output_dir "$OUT" || { echo "scoring failed for $P"; exit 1; }
  
  echo -e "\n=== [$P] 3️⃣ run_score_integration.py ==="
  python run_score_integration.py \
  --prefix     "$P" \
  --samples    "$SAMPLES" \
  --output_dir "$OUT" || { echo "integration failed for $P"; exit 1; }
done

