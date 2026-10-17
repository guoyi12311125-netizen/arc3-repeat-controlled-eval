# -*- coding: utf-8 -*-
"""Assemble the public release folder from live sources. Deterministic, rerunnable."""
import shutil, hashlib, sys
from pathlib import Path

PAPER = Path(__file__).resolve().parent.parent          # arc3-paper
RUNS = PAPER.parent / "arc3-eng" / "runs"
REL = PAPER / "release"
OLD = PAPER / "open-source"

KERNELS = [
    ("calib_a",   "arc3-calib-a.ipynb"),
    ("calib_a2",  "arc3-calib-a2.ipynb"),
    ("calib_a3",  "arc3-calib-a3.ipynb"),
    ("calib_a4",  "arc3-calib-a4.ipynb"),
    ("calib_a5",  "arc3-calib-a5.ipynb"),
    ("e5_behavior", "arc3-e5-behavior.ipynb"),
    ("e5b",       "arc3-e5b-behavior.ipynb"),
    ("e6",        "arc3-e6-combo.ipynb"),
    ("e7",        "arc3-e7-repeat-matrix.ipynb"),
    ("submission-guards",  "arc3-submission-guards.ipynb"),
    ("submission-drain60", "arc3-submission-drain60.ipynb"),
    ("submission-combo",   "arc3-submission-combo.ipynb"),
    ("submission-noop",    "arc3-submission-noop.ipynb"),
]
TOOLS = ["build_appendix_b.py", "build_appendix_c.py", "splice_appendices.py", "make_figures.py"]
OLD_TOOLS = ["analyze_e5b.py", "build_e5.py", "build_e5b.py", "build_e6.py",
             "build_submission_noop.py", "build_submission_variant.py", "fetch_kernel_output.py"]

LICENSE = """MIT No Attribution

Copyright 2026 Guoyi Zhang

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

THIRD_PARTY = """# Third-party notices

Our own notebooks, analysis scripts, figures and the harness patch (our changes) are
released under MIT-0; see LICENSE. **Third-party code and models are not relicensed by
this release.** They keep the terms their authors set, and the patch below contains only
our changes as a diff against those files.

## Redistributed here
- `kernels/*.ipynb` and `tools/*.py`: our own artifacts. The notebooks contain no
  third-party source; at run time they fetch the upstream bundle from a Kaggle input
  dataset and apply `patch/harness-changes.patch` to their own copy, offline.
- `patch/harness-changes.patch`: a diff of our modifications against the ARC-AGI-3
  harness files as published in the public Kaggle dataset `dfranzen/taaf-kaggle-source-bundle-copy`
  (a copy of the competition source bundle, itself built on the Duck harness). The patch
  contains only our additions and changes. Upstream files remain under the terms their
  authors set on Kaggle; apply the patch to your own copy of the upstream bundle.

## Referenced, not redistributed
- The ARC-AGI-3 competition source bundle and the Duck harness: via the Kaggle
  distribution by dfranzen and the ARC Prize competition pages.
- Model checkpoint: `intel-qwen3.8-flash-next-w4a16-autoround`, served from the Kaggle
  input path `dfranzen/intel-qwen3.8-flash-next-w4a16-autoround/transformers/default/1`;
  license terms as published on Kaggle Models. Weights are not redistributed. Details in
  `MODEL_PROVENANCE.md`.
- Serving stack: SGLang `Pennyroyal v2.5.3` wheels from the Kaggle dataset `pennyroyal-v253`,
  plus their transitive dependencies (PyTorch and CUDA libraries as pinned by that image).
  Not redistributed here.
- Analysis dependencies: matplotlib, numpy, pypdf; pins in `requirements.txt`. Installed
  from their own distributions under their own licenses.
- ARC-AGI-3 game environments and tasks: ARC Prize Foundation.

Corrections from upstream authors are welcome.
"""

README = """# Repeat-controlled evaluation for ARC-AGI-3: artifacts and code

Artifacts for the paper "Before Tuning the Harness: Repeat-Controlled Evaluation and
Request-Level Accounting for ARC-AGI-3" (Paper Prize track, ARC Prize 2026).

Linked competition submission: **57174905** (public score 30.21), a re-submission of the
guard build described in the paper.

- GitHub: https://github.com/guoyi12311125-netizen/arc3-repeat-controlled-eval
- Kaggle dataset mirror: https://www.kaggle.com/datasets/zgyyyl/arc3-paper-release

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
"""

def sha256(p: Path):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if REL.exists():
        shutil.rmtree(REL)
    for d in ("kernels", "tools", "data", "figures", "patch", "logs", "paper"):
        (REL / d).mkdir(parents=True, exist_ok=True)

    # kernels
    missing = []
    for run, name in KERNELS:
        src = RUNS / run / "kernel" / "notebook.ipynb"
        if run.startswith("submission"):
            src = RUNS / run / "kernel" / "arc-agi-3-daniel-m2-baseline.ipynb"
        if src.exists():
            shutil.copy2(src, REL / "kernels" / name)
        else:
            missing.append(str(src))
    # tools
    for t in TOOLS:
        shutil.copy2(PAPER / "tools" / t, REL / "tools" / t)
    for t in OLD_TOOLS:
        s = OLD / "tools" / t
        if s.exists():
            shutil.copy2(s, REL / "tools" / t)
    shutil.copy2(PAPER / "build_numbers.py", REL / "tools" / "build_numbers.py")
    shutil.copy2(PAPER / "tools" / "make_cover.py", REL / "tools" / "make_cover.py")
    shutil.copy2(PAPER / "tools" / "assemble_release.py", REL / "tools" / "assemble_release.py")
    # data
    for f in ("numbers.json", "numbers.md", "appendix-b-per-game.md", "appendix-c-registry.md"):
        shutil.copy2(PAPER / "data" / f, REL / "data" / f)
    # figures
    for f in sorted((PAPER / "figures").glob("fig[1-4]-*")):
        shutil.copy2(f, REL / "figures" / f.name)
    # patch + logs + paper
    shutil.copy2(OLD / "patch" / "harness-changes.patch", REL / "patch" / "harness-changes.patch")
    if (OLD / "logs").exists():
        shutil.copytree(OLD / "logs", REL / "logs", dirs_exist_ok=True)
    for f in ("DRAFT-v6-20261017.md",):
        shutil.copy2(PAPER / f, REL / "paper" / f)
    d = PAPER / "for-gpt" / "ARC-AGI-3-paper-draft-v6.docx"
    if d.exists():
        shutil.copy2(d, REL / "paper" / d.name)
    pdf = PAPER / "paper-v6.pdf"
    if pdf.exists():
        shutil.copy2(pdf, REL / "paper" / pdf.name)
    w = PAPER / "writeup" / "KAGGLE-WRITEUP-v1.md"
    if w.exists():
        shutil.copy2(w, REL / "paper" / w.name)
    cov = PAPER / "figures" / "cover.png"
    if cov.exists():
        shutil.copy2(cov, REL / "figures" / "cover.png")

    # fixed documents
    (REL / "README.md").write_text(README, encoding="utf-8")
    (REL / ".gitattributes").write_text(
        "* text=auto\n*.sh text eol=lf\nMANIFEST.sha256 text eol=lf\n*.py text eol=lf\n*.md text eol=lf\n*.ipynb text eol=lf\n",
        encoding="utf-8", newline="\n")
    (REL / ".gitignore").write_text("__pycache__/\n*.pyc\n.DS_Store\n", encoding="utf-8", newline="\n")
    dataset_meta = {
        "title": "ARC-AGI-3 repeat-controlled evaluation artifacts",
        "id": "zgyyyl/arc3-paper-release",
        "licenses": [{"name": "MIT"}],
        "subtitle": "Paper artifacts for the ARC Prize 2026 paper track (submission 57174905)",
        "description": (
            "Code, run logs, analysis scripts, per-game tables and the manuscript for the paper "
            "'Before Tuning the Harness: Repeat-Controlled Evaluation and Request-Level Accounting for ARC-AGI-3'. "
            "Our code is MIT-0; third-party components keep their own terms, itemised in THIRD_PARTY_NOTICES.md. "
            "The linked competition submission is 57174905 (public score 30.21). "
            "Mirror of https://github.com/guoyi12311125-netizen/arc3-repeat-controlled-eval."
        ),
    }
    import json as _json
    (REL / "dataset-metadata.json").write_text(_json.dumps(dataset_meta, indent=2, ensure_ascii=False), encoding="utf-8")
    (REL / "LICENSE").write_text(LICENSE, encoding="utf-8")
    (REL / "THIRD_PARTY_NOTICES.md").write_text(THIRD_PARTY, encoding="utf-8")
    shutil.copy2(OLD / "VERIFICATION.md", REL / "VERIFICATION.md")
    for f in ("requirements.txt", "MODEL_PROVENANCE.md", "SUBMISSION_MAPPING.md", "reproduce.sh"):
        src = OLD / f
        if src.exists():
            shutil.copy2(src, REL / f)
        else:
            print("缺失:", src)

    # manifest
    lines = []
    for p in sorted(REL.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.sha256":
            lines.append(f"{sha256(p)}  {p.relative_to(REL).as_posix()}")
    with open(REL / "MANIFEST.sha256", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    n_files = len(lines)
    total = sum(p.stat().st_size for p in REL.rglob("*") if p.is_file())
    print(f"release/ 组装完成: {n_files} 文件, {total/1024/1024:.1f} MB")
    if missing:
        print("缺失源文件:", missing)

if __name__ == "__main__":
    main()
