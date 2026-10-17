# Submission mapping

The paper links one competition submission. This file records what produced it.

## Linked submission

| field | value |
| --- | --- |
| submission id | **57174905** |
| date (UTC) | 2026-10-14 |
| public score | **30.21** |
| kernel | `zgyyyl/arc-agi-3-daniel-m2-baseline` |
| kernel version | 3 (the guard build) |
| notebook in this release | `kernels/arc3-submission-guards.ipynb` |
| effective switches | `ARC3_NOOP_REPEAT_GUARD=1`, `ARC3_DEATH_LEDGER=1`, `ARC3_DEATH_REPEAT_GUARD=1`; every other switch off |
| code identity | byte-identical to submission 57147727 below; the sha256 of `kernels/arc3-submission-guards.ipynb` is recorded in `MANIFEST.sha256` |
| source fingerprint | the notebook's sha256 is the commit identity for this release; the release is not a git checkout, so no git hash exists |

## All six submissions of this project

| date (UTC) | submission | build | public score |
| --- | --- | --- | --- |
| 2026-10-06 | 56882441 | base build, every switch off | 29.28 |
| 2026-10-10 | 57037255 | identical code | 24.38 |
| 2026-10-11 | 57061252 | identical code | 29.41 |
| 2026-10-12 | 57100038 | identical code | 29.60 |
| 2026-10-13 | 57147727 | base build plus the three guard switches (kernel version 3) | 29.89 |
| 2026-10-14 | 57174905 | byte-identical to 57147727, resubmitted for a second sample | 30.21 |

The four "identical code" rows are the same notebook, executed four times on four days.
Their spread (24.38 to 29.60) is the leaderboard variation reported in Section 4 of the
paper and is the reason the guard build was submitted twice.

## Reproducing the linked score

The competition reruns the submission kernel on its own infrastructure; nothing in this
release can be re-scored locally. What can be reproduced is the local evidence behind the
paper (see `reproduce.sh`) and the patch application (see `VERIFICATION.md`).
