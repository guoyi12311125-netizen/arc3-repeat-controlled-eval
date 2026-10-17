# What one submission a day taught us about measuring our own ARC-AGI-3 agent

**Subtitle:** Repeat-controlled evaluation and request-level accounting on a single Kaggle GPU

The short version: we did not find a big score gain. What we found is that our local measurements were less trustworthy than we assumed, and that fixing the measurement changed which of our own changes we were allowed to keep.

## What we ran

The agent is Daniel Franzen's milestone-2 solution on top of the Duck harness from Tufa Labs, running Qwen3.8-Flash-Next through SGLang on one Kaggle GPU with ten parallel sessions. We made small changes to that code and tested them in screens: batches of arms on a frozen set of ten public games, 2000 seconds per game, one pass each. A screen is one kernel, four to five hours, inside the nine hour limit.

The competition gives one scored submission a day. We used six between October 6 and October 14. Four of them were the same code: 29.28, 24.38, 29.41, 29.60. That spread of 5.22 points is larger than anything we were trying to measure.

## The screens disagreed with themselves

The two fully bracketed screens, E5b and E6, put a baseline arm, one or more candidates, and an identical repeat of the baseline at the end. Two arms, same configuration, hours apart, same server. A third session, E7, interleaved three baselines with three guard arms instead.

In one screen the baselines came out 14.90 and 18.22. In the next, 11.52 and 14.71. Same code, same games, differences of 3.33 and 3.20 points. Then we ran an alternating matrix, A-B-A-B-A-B, three baselines and three guard arms interleaved in one session. Those three baselines landed at 12.71, 13.53 and 12.30, a spread of 1.23.

So the same-configuration difference was 3.33 in one session, 3.20 in another, 1.23 in a third. It is not a constant you can subtract. An earlier draft of our paper quoted a single noise floor of 3.33 points. That number did not survive the third session, and anyone quoting one for this benchmark is guessing.

## The candidate moved more than the baseline

The alternating matrix gave us something we did not expect. The three baseline arms were tight, 1.23 points. The three guard arms in the same session scored 15.43, 18.66 and 12.43, a spread of 6.23, sample standard deviation 3.12 against 0.63 for the baselines. The three paired differences were +2.72, +5.13 and +0.13.

That matters more than the guard result itself. If the candidate is noisier than the control, a bracketing baseline tells you how much the world wobbles, not how much the candidate wobbles. We do not know why the guard arms vary that much. It could be a real mechanism that only fires in some runs, or sampling amplified by longer trajectories. Three pairs cannot separate those explanations.

## Where the GPU time went

We logged every request. In a 25-game calibration run, 225 requests ended at the 120 second client timeout. That is 15 percent of requests and about 7.5 hours of request duration, 37.5 percent of the run's 19.98 hour total. Request duration is not GPU time; the share says that a third of the client's own request time went to requests it cut off.

Two run pairs sit behind those numbers and they are not the same pair. The 225 to 38 change comes from a4 and a5, which also differ in per-game ceiling and session count, so it is a latency comparison. Total reported errors across the 25 games were 210 in a3 and 53 in a5, a pair that differs in the timeout plus three budget companions. The score did not improve: 24.20 against 27.40, one run each. The configurations differed in their error profiles, while the score effect remained unresolved.

## What the guards did

The guards watch the board state outside the play area. If an action leaves it bit-identical, they refuse to repeat that action in that state, with a one-slot escape so the model can re-issue it immediately if it meant to. Across six guard runs in four sessions, the local gain over each run's control arm ranged from +0.13 to +9.12. One of two fully bracketed comparisons passed our screening rule, and two of three alternating ones did.

On ft09, the game that gave the cleanest story early on, guards reached 100 points in 3 of their 6 runs, against 2 of 13 non-guard arms. But the three E7 guard runs scored 45.27, 47.62 and 47.62, so the early three-for-three story does not hold.

On the leaderboard the guard build scored 29.89 and 30.21 against the older build's four samples averaging 28.17. That looks like +1.9 points. It is two submissions against four, unpaired, and the guard build's own two samples differ by 0.32. We call it descriptive and do not claim an effect.

Daniel Franzen, whose writeup our entry builds on, says he tried repeated-state guards and a death ledger and left them out for lack of clear benefit. Two independent attempts, one of them by the milestone winner, and neither of us can confirm the thing works.

## The protocol we would use again

Five rules, none of them clever:

- Freeze the game set and the budgets before the first arm starts.
- Put a baseline on both sides of every candidate.
- Write the decision rule down before you look, including what "unresolved" means. Ours: if the candidate's margin over the end control is smaller than the session's own baseline gap, the result is unresolved rather than a win.
- Report the same-configuration gap of every session next to every effect you claim.
- Make every number in the writeup recomputable from stored artifacts. We wrote a script that regenerates all of ours from the run logs.

One addition, from the E7 session: if you can afford six arms, spend three of them on the candidate. Candidate variability can be the larger term, and a protocol that only measures the baseline will make candidates look cleaner than they are.

## What the rules changed for us

We replayed our own record under three reading rules. The naive read kept ten of eleven candidate readings. The bracketing rule, which also requires the margin over the end control, dropped six of the nine positive readings it could screen; one negative reading never entered. Three survived, and all three are guard readings. The same data supported a keep decision under one rule and an unresolved decision under another, and we could not tell which rule was active until we wrote it down.

## What we would do with more compute

Not more switches. The lever with published evidence on this benchmark is memory, in the sense of a searchable interaction log, which is what the PRO-LONG paper describes. Every screen cost four to five hours of a nine hour GPU day, so we could afford four of them and that was that.

## Files

- Submission: 57174905, the guard build, 30.21
- Notebook: the guard build notebook, version 3
- Code, logs, harness patch and analysis scripts: the public project link
- Full paper with appendices: the PDF on the public project link
