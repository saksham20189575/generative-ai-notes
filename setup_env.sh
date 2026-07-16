#!/usr/bin/env bash
# Create/refresh the project venv and install Coding-Examples dependencies.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if command -v python3.12 >/dev/null 2>&1; then
  PYTHON=python3.12
elif command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
else
  echo "Python 3.12+ is required (python3.12 preferred)." >&2
  exit 1
fi

VERSION="$("$PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
MAJOR="${VERSION%%.*}"
MINOR="${VERSION#*.}"
if (( MAJOR < 3 || (MAJOR == 3 && MINOR < 10) || (MAJOR == 3 && MINOR >= 14) )); then
  echo "Warning: detected Python $VERSION. Use Python 3.10–3.12 for best compatibility." >&2
fi

if [[ ! -d venv ]]; then
  echo "Creating venv with $PYTHON ($VERSION)..."
  "$PYTHON" -m venv venv
else
  echo "Using existing ./venv"
fi

# shellcheck disable=SC1091
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo
echo "Environment ready. Activate with:"
echo "  source venv/bin/activate"
echo
echo "Run an example (from its folder), e.g.:"
echo "  cd Coding-Examples/langChain_rag && python main.py"
echo
echo "Put GROQ_API_KEY in a .env file in the example folder (or the repo root)."
