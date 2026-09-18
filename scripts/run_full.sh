#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)/src"
DATA_DIR="${DATA_DIR:-$(cat data/dataset_dir.txt)}"
SCOPE="${SCOPE:-shop}"
N_NEG="${N_NEG:-999}"
SEEDS="${SEEDS:-20260918 20260919 20260920}"
python -m kuailive_agent.prepare --data-dir "$DATA_DIR" --out-dir "data/prepared/$SCOPE" --scope "$SCOPE"
for seed in $SEEDS; do
  python -m kuailive_agent.evaluate --prepared-dir "data/prepared/$SCOPE" --out-dir "results/$SCOPE" --n-neg "$N_NEG" --seed "$seed"
done
python -m kuailive_agent.aggregate --results-dir "results/$SCOPE"
