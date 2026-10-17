# Repeat-controlled evaluation for ARC-AGI-3: artifacts and code

Artifacts for the paper "Before Tuning the Harness: Repeat-Controlled Evaluation and
Request-Level Accounting for ARC-AGI-3" (Paper Prize track, ARC Prize 2026).

Linked competition submission: **57174905** (public score 30.21), a re-submission of the
guard build described in the paper.

- GitHub: https://github.com/guoyi12311125-netizen/arc3-repeat-controlled-eval

All six competition submissions of this project, in order (see paper Table 3a):

| date (UTC) | submission | build | public score |
|---|---|---|---|
| 2026-10-06 | 56882441 | base build, every switch off | 29.28 |
| 2026-10-10 | 57037255 | identical code | 24.38 |
| 2026-10-11 | 57061252 | identical code | 29.41 |
| 2026-10-12 | 57100038 | identical code | 29.60 |
| 2026-10-13 | 57147727 | base build plus the three guard switches | 29.89 |
| 2026-10-14 | 57174905 | byte-identical to 57147727 | 30.21 |

## What is here

| path | contents |
|---|---|
| `kernels/` | every Kaggle notebook we pushed, one per experiment |
| `tools/` | analysis and build scripts; `build_numbers.py` regenerates every number in the paper |
| `data/` | `numbers.json` (all paper numbers), `numbers.md`, Appendix B (per-game tables), Appendix C (experiment registry) |
| `figures/` | the four paper figures (PNG and SVG) |
| `patch/` | our harness changes as a diff against the public source bundle |
| `logs/` | curated request and queue logs from three runs |
| `paper/` | the manuscript (Markdown, 24-page PDF, DOCX) and the Kaggle writeup draft |
| `MODEL_PROVENANCE.md` | checkpoint, quantization, serving build, license terms |
| `SUBMISSION_MAPPING.md` | which kernel version produced submission 57174905, with its switches |
| `reproduce.sh` | regenerates numbers, appendices and figures, then checks the manifest |
| `requirements.txt` | analysis-side dependency pins |
| `VERIFICATION.md` | verification record: patch application, number recomputation, hashes |

## Environment

The experiment notebooks run offline on the Kaggle image: the source bundle, the model
checkpoint and the SGLang wheels all come from competition input datasets, so no network
access is needed at run time. The analysis scripts need only Python 3.12 with the pins in
`requirements.txt`.

## Reproduce the numbers

```
python tools/build_numbers.py        # writes data/numbers.json and data/numbers.md
python tools/build_appendix_b.py     # per-game tables (needs the run artifacts)
python tools/build_appendix_c.py     # experiment registry
python tools/make_figures.py         # figures/
```

`build_numbers.py` reads the run artifacts directly (downloaded kernel outputs). The
run directories it expects are listed in `tools/build_numbers.py`; each is the output of
one notebook in `kernels/`.

## Apply the harness patch

See `VERIFICATION.md` for the exact commands and hashes. In short: copy the upstream
`src/` tree, `git init`, then
`git apply --include='ARC3-Inference/*' patch/harness-changes.patch`.

## Experiment matrix

See `data/appendix-c-registry.md` for every experiment, its state, and why it entered
or left the analysis. The paper's Table 3a lists the six competition submissions behind
the leaderboard rows.

## License

MIT-0 for our code; third-party components as described in `THIRD_PARTY_NOTICES.md`.
