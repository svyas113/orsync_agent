#!/usr/bin/env bash
set -euo pipefail
cd "/Users/srushtivaidya/Desktop/Orsync Dev"
export PYTHONPATH="/Users/srushtivaidya/Desktop/Orsync Dev${PYTHONPATH:+:$PYTHONPATH}"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

echo "==> Checking numpy..."
.venv/bin/python -c "import numpy; print('numpy', numpy.__version__)"

echo "==> Training orsync_visitor (this can take several minutes)..."
.venv/bin/fastworkflow train \
  "./Or Sync Agent/orsync_visitor" \
  "./Or Sync Agent/orsync_visitor/fastworkflow.env" \
  "./Or Sync Agent/orsync_visitor/fastworkflow.passwords.env"

echo "==> Starting API on http://localhost:8003 ..."
exec .venv/bin/python -m fastapi_fastworkflow \
  --workflow_path "./Or Sync Agent/orsync_visitor" \
  --env_file_path "./Or Sync Agent/orsync_visitor/fastworkflow.env" \
  --passwords_file_path "./Or Sync Agent/orsync_visitor/fastworkflow.passwords.env" \
  --startup_action "./Or Sync Agent/orsync_visitor/startup_action.json" \
  --host 0.0.0.0 \
  --port 8003
