#!/usr/bin/env bash
# Regenerate every number, appendix table and figure in the paper from the run artifacts.
# Layout expected: <parent>/arc3-eng/runs holds the downloaded kernel outputs, one
# directory per experiment (see data/appendix-c-registry.md for the mapping).
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d "../arc3-eng/runs" ]; then
  echo "Missing ../arc3-eng/runs. Put the downloaded kernel outputs there first." >&2
  echo "The scripts' RUNS constant points at that directory; edit it if yours differs." >&2
  exit 1
fi

python tools/build_numbers.py        # data/numbers.json, data/numbers.md
python tools/build_appendix_b.py     # data/appendix-b-per-game.md
python tools/build_appendix_c.py     # data/appendix-c-registry.md
python tools/make_figures.py         # figures/fig1..4 .png/.svg

sha256sum -c MANIFEST.sha256
