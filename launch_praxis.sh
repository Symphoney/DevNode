#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export DISPLAY=:0
export XAUTHORITY="${XAUTHORITY:-/home/pi/.Xauthority}"
export PRAXIS_SIGIL="${PRAXIS_SIGIL:-spider}"

cd "$SCRIPT_DIR"
exec /usr/bin/python3 praxis_gui.py
