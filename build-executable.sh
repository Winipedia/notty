#!/usr/bin/env bash
set -euo pipefail

uv \
  run \
  pyinstaller \
  --onefile \
  --name=notty-"${OSTYPE}" \
  --icon=src/notty/rig/resources/icon.png \
  --collect-data=notty.rig.resources \
  src/notty/main.py
