# Third-party notices

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
