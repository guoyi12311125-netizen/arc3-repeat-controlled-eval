# Paper numbers, re-extracted from run artifacts

## E5_screen
| arm | games | mean | levels | actions | errors | source |
|---|---|---|---|---|---|---|
| baseline | 10 | 12.9077 | 17/73 | 552 | 68 | `e5_behavior\out\phase_b_safe_1791857607678366179\baseline_p0\metrics.json` |
| noop_guard | 10 | 22.0431 | 24/73 | 658 | 62 | `e5_behavior\out\phase_b_safe_1791857607678366179\noop_guard_p0\metrics.json` |

## E5b_screen
| arm | games | mean | levels | actions | errors | source |
|---|---|---|---|---|---|---|
| baseline | 10 | 14.8954 | 21/73 | 635 | 71 | `e5b\out\phase_b_safe_1791871401644733360\baseline_p0\metrics.json` |
| baseline_rep | 10 | 18.2211 | 20/73 | 655 | 68 | `e5b\out\phase_b_safe_1791871401644733360\baseline_rep_p0\metrics.json` |
| drain60 | 10 | 20.9142 | 22/73 | 546 | 63 | `e5b\out\phase_b_safe_1791871401644733360\drain60_p0\metrics.json` |
| inventory | 10 | 13.5945 | 20/73 | 649 | 73 | `e5b\out\phase_b_safe_1791871401644733360\inventory_p0\metrics.json` |
| memory_slim | 10 | 15.563 | 21/73 | 635 | 65 | `e5b\out\phase_b_safe_1791871401644733360\memory_slim_p0\metrics.json` |
| noop_guard | 10 | 20.4334 | 23/73 | 652 | 62 | `e5b\out\phase_b_safe_1791871401644733360\noop_guard_p0\metrics.json` |

## E6_combo
| arm | games | mean | levels | actions | errors | source |
|---|---|---|---|---|---|---|
| baseline | 10 | 11.5152 | 17/73 | 631 | 67 | `e6\out\phase_b_safe_1791952567840217146\baseline_p0\metrics.json` |
| baseline_rep | 10 | 14.7121 | 20/73 | 625 | 72 | `e6\out\phase_b_safe_1791952567840217146\baseline_rep_p0\metrics.json` |
| combo | 10 | 15.6146 | 20/73 | 708 | 60 | `e6\out\phase_b_safe_1791952567840217146\combo_p0\metrics.json` |
| drain60 | 10 | 16.7093 | 22/73 | 569 | 66 | `e6\out\phase_b_safe_1791952567840217146\drain60_p0\metrics.json` |
| noop_guard | 10 | 20.421 | 21/73 | 650 | 70 | `e6\out\phase_b_safe_1791952567840217146\noop_guard_p0\metrics.json` |

## E7_matrix
| arm | games | mean | levels | actions | errors | source |
|---|---|---|---|---|---|---|
| base_1 | 10 | 12.7115 | 20/73 | 617 | 67 | `e7\out\phase_b_safe_1791969354283162683\base_1_p0\metrics.json` |
| base_2 | 10 | 13.5286 | 20/73 | 656 | 65 | `e7\out\phase_b_safe_1791969354283162683\base_2_p0\metrics.json` |
| base_3 | 10 | 12.3006 | 17/73 | 664 | 78 | `e7\out\phase_b_safe_1791969354283162683\base_3_p0\metrics.json` |
| guard_1 | 10 | 15.431 | 22/73 | 597 | 64 | `e7\out\phase_b_safe_1791969354283162683\guard_1_p0\metrics.json` |
| guard_2 | 10 | 18.658 | 22/73 | 639 | 66 | `e7\out\phase_b_safe_1791969354283162683\guard_2_p0\metrics.json` |
| guard_3 | 10 | 12.426 | 17/73 | 652 | 71 | `e7\out\phase_b_safe_1791969354283162683\guard_3_p0\metrics.json` |

## a2_25games_2900s_guard1GiB
- games: 25
- mean: 14.7248
- levels: 37
- levels_total: 183
- actions: 1334
- errors: 29
- nonzero: 11
- source: calib_a2\output\phase_b_safe_1791750955488883931\baseline_p0\metrics.json

## a3_25games_2900s_memfrac092
- games: 25
- mean: 27.397
- levels: 75
- levels_total: 183
- actions: 3245
- errors: 210
- nonzero: 24
- source: calib_a3\output\phase_b_safe_1791769819918702902\baseline_p0\metrics.json

## a5_25games_2900s_timeout240
- games: 25
- mean: 24.1988
- levels: 69
- levels_total: 183
- actions: 3094
- errors: 53
- nonzero: 23
- source: calib_a5\output\phase_b_safe_1791807741414334601\baseline_p0\metrics.json

## requests_a4_timeout120
- requests: 1500
- median_s: 34.0
- p90_s: 120.1
- max_s: 120.2
- hit_client_timeout: 225
- hit_client_timeout_pct: 15.0
- over_120s: 225
- over_120s_pct: 15.0
- timeout_request_hours: 7.51
- total_request_hours: 19.98
- wallclock_hours_if_10_ways: 2.0
- source: calib_a4\output\phase_b_safe_1791796870944110556\baseline_p0\request-events.jsonl

## outputlen_a4_timeout120
- requests: 1496
- median_tokens: 1255.0
- p90_tokens: 4265
- max_tokens: 9423
- over_3000_pct: 21.93
- source: calib_a4\output\serve.log

## requests_a5_timeout240
- requests: 1453
- median_s: 28.3
- p90_s: 114.5
- max_s: 240.1
- hit_client_timeout: 38
- hit_client_timeout_pct: 2.62
- over_120s: 135
- over_120s_pct: 9.29
- timeout_request_hours: 2.53
- total_request_hours: 19.16
- wallclock_hours_if_10_ways: 1.92
- source: calib_a5\output\phase_b_safe_1791807741414334601\baseline_p0\request-events.jsonl

## outputlen_a5_timeout240
- requests: 1454
- median_tokens: 1303.0
- p90_tokens: 5099
- max_tokens: 12290
- over_3000_pct: 21.8
- source: calib_a5\output\serve.log

## submissions
- {'ref': 56882441, 'date': '2026-10-06', 'score': 29.28, 'build': 'M2 baseline first push'}
- {'ref': 57037255, 'date': '2026-10-10', 'score': 24.38, 'build': 'identical code rerun'}
- {'ref': 57061252, 'date': '2026-10-11', 'score': 29.41, 'build': 'identical code rerun'}
- {'ref': 57100038, 'date': '2026-10-12', 'score': 29.6, 'build': 'identical code rerun'}
- {'ref': 57147727, 'date': '2026-10-13', 'score': 29.89, 'build': 'guard build (3 env keys changed)'}
