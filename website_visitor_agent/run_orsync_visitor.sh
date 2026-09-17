#!/usr/bin/env bash
# Run Or-sync website visitor agent (FastAPI) for embedding on orsync.co.in
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKFLOW_DIR="$SCRIPT_DIR/orsync_visitor"

cd "$REPO_ROOT"

if [[ -x .venv/bin/python ]]; then
  PYTHON=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
else
  echo "No Python found. Create a venv in Orsync Dev and install requirements.txt" >&2
  exit 1
fi

PASSWORDS_FILE="${PASSWORDS_FILE:-$WORKFLOW_DIR/fastworkflow.passwords.env}"
if [[ ! -f "$PASSWORDS_FILE" ]]; then
  echo "Missing $PASSWORDS_FILE" >&2
  echo "Copy orsync_visitor/fastworkflow.passwords.env.example → fastworkflow.passwords.env and add keys." >&2
  exit 1
fi

export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PORT="${PORT:-8003}"

# Prefer the scrubbing server wrapper (strips discontinued product names from JSON replies)
exec "$PYTHON" "$SCRIPT_DIR/serve_orsync_visitor.py"
