#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  Matrix Publisher Panel"
echo "============================================"
echo ""

# Prefer social-auto-upload venv Python (has patchright)
PYTHON="python3"
if [ -f "../social-auto-upload/.venv/bin/python3" ]; then
    PYTHON="../social-auto-upload/.venv/bin/python3"
    echo "[INFO] Using SAU venv Python"
fi

# Check social-auto-upload
if [ ! -f "../social-auto-upload/sau_cli.py" ]; then
    echo "[WARN] social-auto-upload not found at ../social-auto-upload/"
    echo "       Login and upload features will not work."
    echo "       Set SAU_ROOT env var to its path if it's elsewhere."
    echo ""
fi

# Install httpx into current environment if missing (patchright is in SAU venv)
if ! $PYTHON -c "import httpx" 2>/dev/null; then
    echo "[INFO] Installing httpx..."
    $PYTHON -m pip install httpx --quiet
fi

echo "[INFO] Starting server on http://127.0.0.1:8787"
echo "[INFO] Press Ctrl+C to stop."
echo ""

exec $PYTHON server.py
