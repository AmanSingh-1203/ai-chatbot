#!/usr/bin/env bash
# Run the visual game (Linux / macOS)
PY="python3"
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
fi
$PY start_game.py
