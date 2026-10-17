# Appendix C. Experiment registry

Every experiment started over the competition, its state, and why it did or did not enter the analysis. Kernel slugs point at the pushed notebooks in the release.

| id | kernel | purpose | design | state | disposition |
|---|---|---|---|---|---|
| E4 | `-` | Serving-stack throughput probe | archived notebook and module only | code archived, no retained run artifacts | informed the calibration-run design; not an analysis input |
| a1 | `zgyyyl/arc3-calib-a` | First calibration probe, 25 games, single arm | single execution | all 25 game records cancelled with zero actions | excluded: no usable play records |
| a2 | `zgyyyl/arc3-calib-a2` | Calibration follow-up, 25 games, single arm | single execution | complete (2026-10-12), mean 14.72 | latency context; Appendix B |
| a3 | `zgyyyl/arc3-calib-a3` | Calibration run, 25 games, stock 120-second analyzer timeout | single execution | complete (2026-10-12), mean 27.40 | member of the timeout pair (a3 vs a5), Table 2 |
| a4 | `zgyyyl/arc3-calib-a4` | Calibration run, 25 games, widened per-game ceiling and session count | single execution | complete (2026-10-12), mean 25.36 | latency anatomy pair (a4 vs a5); queue-delay statistics |
| a5 | `zgyyyl/arc3-calib-a5` | Calibration run, 25 games, doubled analyzer timeout 240 seconds | single execution | complete (2026-10-12), mean 24.20 | member of the timeout pair and the latency pair |
| E5 | `zgyyyl/arc3-e5-behavior` | Behavior screen: baseline vs no-op guard | bracketed screen, batch aborted | two of the planned arms completed; batch stopped by a watcher failure | both completed arms enter Table 1, Table 4 and the ft09 count; the lost arms were re-run as E5b |
| E5b | `zgyyyl/arc3-e5b-behavior` | Behavior screen re-run: six arms including inventory, memory slim, drain and a repeat baseline | fully bracketed screen, six arms | complete (2026-10-13) | main screen for the guard, inventory, memory-slim and drain readings, Tables 1-4 |
| E6 | `zgyyyl/arc3-e6-combo` | Second behavior screen: baseline, guard, drain, combo, repeat baseline | fully bracketed screen, five arms | complete (2026-10-14); the first kernel build failed before running and was rebuilt | second controlled guard reading and the drain/combo candidates, Tables 1-4 |
| E6-b1 | `zgyyyl/arc3-e6-combo` | E6 kernel, first build: failed before any run (serialization error in one arm's configuration) | build only | failed at build stage; no records produced | rebuilt as E6; the failed build contributes nothing to the analysis |
| E7-b1 | `zgyyyl/arc3-e7-repeat-matrix` | E7 kernel, first build: failed budget validation before any run | build only | failed at build stage; no records produced | rebuilt as E7; the failed build contributes nothing to the analysis |
| E7 | `zgyyyl/arc3-e7-repeat-matrix` | Alternating repeat matrix: three baseline and three guard arms interleaved | A-B-A-B-A-B, six arms, ten games each | complete (2026-10-15); the first kernel build failed budget validation and was rebuilt | same-configuration spread for both arms of a pair, Section 4 and the guard paragraphs |
| S-noop | `zgyyyl/arc-agi-3-daniel-m2-baseline` | Submission build: baseline plus no-op guard only | local build of the competition kernel | built and locally verified | not submitted; superseded by the three-switch guard build |
| S-guard | `zgyyyl/arc-agi-3-daniel-m2-baseline` | Submission build: three guard switches on | local build of the competition kernel | submitted twice: 57147727 (2026-10-13) and 57174905 (2026-10-14) | the linked submission of this paper, Table 3a |
| S-drain | `zgyyyl/arc-agi-3-daniel-m2-baseline` | Submission build: guard build plus history turn drain at 60 turns | local build of the competition kernel | built and locally verified; local deltas +5.19 (E6) and +2.00 (end-control view) | not submitted: daily submission limit and an unresolved reading |
| S-combo | `zgyyyl/arc-agi-3-daniel-m2-baseline` | Submission build: guards plus drain combined | local build of the competition kernel | built and locally verified | not submitted: weak local reading |
| N1 | `-` | Overnight orchestration script (downloads, pushes, watchers) | infrastructure, not an experiment | log retained | not an analysis input |

The two failed builds above never produced records: the failure happened before the batch started, so neither screen contains partial arms from them.
