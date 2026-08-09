#!/usr/bin/env bash
# One-command launcher (macOS / Linux). Thin wrapper over launch.py so there is
# only one implementation to maintain. All arguments are passed straight through.
#
#   ./scripts/launch.sh            # build if needed, serve, open browser
#   ./scripts/launch.sh --dev      # Vite dev server for UI work
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "error: python3 not found on PATH" >&2
  exit 1
fi

exec "$PYTHON" "$REPO_ROOT/scripts/launch.py" "$@"
