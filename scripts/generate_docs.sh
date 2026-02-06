#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install "pdoc==15.0.4"

export PYTHONPATH="$(pwd)/.pdoc_stubs:${PYTHONPATH:-}"
rm -rf dhxdocs
pdoc dhxpyt -o dhxdocs
