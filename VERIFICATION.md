# Verification log

## 2026-10-17 — release hash check and expected outputs

`sha256sum -c MANIFEST.sha256` run inside this directory: **100 files, 100 OK, exit 0**.
One trap found and fixed while setting this up: the manifest was written with CRLF line
endings, which makes every line fail on Windows bash and on Linux. It is now LF; if you
regenerate it on Windows, write it with `newline="
"`.

Expected outputs of `reproduce.sh` (checked on 2026-10-17):

| artifact | expected |
| --- | --- |
| `data/numbers.json` | sha256 `c983362bd6f9bbf1faa5a2cd1849b8158029e8072d0a731bab3f7689e4851288` |
| `data/numbers.md` | sha256 `0929f32e15ce9ebd2765253a06e19da3fbb9e64beca46b0fe531ba72d85b87d7` |
| `data/appendix-b-per-game.md` | 19 screen arms plus 5 calibration runs; ft09 counts 3 of 6 guards and 2 of 13 non-guards |
| `data/appendix-c-registry.md` | 15 registry rows |
| `figures/` | `fig1-variation`, `fig2-duration`, `fig3-tokens`, `fig4-pergame`, each PNG and SVG, plus `cover.png` |

Number-to-artifact traceability, for the tables in the paper:

| paper number | produced by | read from |
| --- | --- | --- |
| Table 1 means, levels, actions | `tools/build_numbers.py` | `runs/*/out/phase_b_safe_*/<arm>_p0/metrics.json` |
| Table 2 durations, caps, tokens | `tools/build_numbers.py` | `runs/calib_a4|a5/output/.../request-events.jsonl`, `serve.log` |
| Table 3 and 3a local deltas, submission scores | `tools/build_numbers.py` | `metrics.json`, competition submission list |
| Table 4 evidence rows | hand-entered, each row cites its run directory | `metrics.json` |
| Appendix B per-game tables | `tools/build_appendix_b.py` | all `metrics.json` above |
| Appendix C registry | `tools/build_appendix_c.py` | run directories and kernel metadata |
| Figures 1 to 4 | `tools/make_figures.py` | `metrics.json`, `serve.log` |
| Section 4 spreads, Section 6 guard paragraphs | hand-computed from the same `metrics.json`, cross-checked against Appendix B | `metrics.json` |

Commands actually run on 2026-10-17, in this directory:

```bash
python tools/build_numbers.py
python tools/build_appendix_b.py
python tools/build_appendix_c.py
python tools/make_figures.py
sha256sum -c MANIFEST.sha256
```

## 2026-10-15 — number recomputation audit


`tools/build_numbers.py` reads the run artifacts and writes `data/numbers.json` and
`data/numbers.md`. Two consecutive runs produced byte-identical outputs:

| item | sha256 |
| --- | --- |
| `data/numbers.json` | `c983362bd6f9bbf1faa5a2cd1849b8158029e8072d0a731bab3f7689e4851288` |
| `data/numbers.md` | `0929f32e15ce9ebd2765253a06e19da3fbb9e64beca46b0fe531ba72d85b87d7` |

The same session regenerated `data/appendix-b-per-game.md` (per-game tables for all
19 screen arms plus the five calibration runs; the ft09 guard/non-guard counts come out
as 3 of 6 and 2 of 13), `data/appendix-c-registry.md`, and the four figures in
`figures/`. `MANIFEST.sha256` in the release root lists the hash of every file in this
release.

One definition worth recording, because the first implementation of `build_numbers.py`
got it wrong: "requests terminated at the cap" must key off the run's own cap (a4 at
119 s, a5 at 239 s), not a fixed threshold. The first version used a median heuristic
that mislabelled a5's "requests above 120 s" count (135) as its cap terminations; the
correct a5 figure is 38 requests (2.6% of 1,453). Both numbers appear in Table 2, in
separate rows.

## 2026-10-14 — the harness patch applies to the published bundle

| item | value |
| --- | --- |
| bundle | `dfranzen/taaf-kaggle-source-bundle-copy` (Kaggle dataset, downloaded 2026-10-14) |
| bundle size / sha256 | 449765 bytes / `cd687f4bc10b2128ea9895024cd2e990b24a1070607a071901cccd1638606187` |
| patch size / sha256 | 498780 bytes / `80aef535ee80970622127f3ee1917e1b127db22ebe07ece40fc8558a63b4484d` |

Commands (run inside the bundle's `src/` directory):

```bash
git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm base
git apply --include='ARC3-Inference/*' -v ../patch/harness-changes.patch
```

Result: `Applied patch ... cleanly.` on all 16 touched files, exit code 0,
`10 files changed, 7136 insertions(+), 197 deletions(-)` plus 6 new files.
The same command is what the notebooks run at boot, so this is the same code path
the live entry executed.

One trap worth recording: `git apply` reports `corrupt patch` if the patch file does
not end with a newline. Our stored copy ends with one; if you re-extract the patch from
a notebook cell with a naive line split, re-add it.
