# IC1 — independent recompute

**Who:** GPT and Gemini, each in a fresh chat with no earlier context, working from raw per-world counts only, without
the analysis script. Files: `recompute/ic1_worlds.csv` and `recompute/ic1_pair_hist.csv` (to GPT), and the same data in
one file `recompute/ic1_one_file.csv` (to Gemini, which handles one small file best). All three files were built from
the 32 output JSONs by a short script, not by `analyse_ic1.py`.

**The assistant's own check, in the open:** while building the pair file, the assistant first read the wrong column
(water sources instead of shared talks) and got 0.719 for the repeated-pairs share. The cause was found in the
assistant's script, not the analysis. The file was rebuilt from the right column before anything was sent.

## GPT (fresh chat https://chatgpt.com/c/6ae1a474-6654-83ea-91ac-5a367a73512f, 28 October 2026)

Recorded from its reply:

| measure | analysis | GPT | match |
|---|---|---|---|
| (1) first-option share | 0.000 [0.000, 0.000] | 0.0000 [0.0000, 0.0001] | yes |
| (2) held share | 0.886 [0.855, 0.908] | 0.8857 [0.8546, 0.9078] | yes |
| held: number checked | 262,774 | 262,774 | yes |
| (3) accepted share | 0.201 | 0.2014 | yes |
| (4) adult talks both seeing water, per adult-year | 4.04 [3.78, 4.28] | 4.0390 [3.7782, 4.2820] | yes |
| (5) moments in pairs with ≥ 5 | 0.870 [0.859, 0.881] | 0.8697 [0.8592, 0.8807] | yes |
| pairs / with ≥ 5 | 986,994 / 513,853 | 986,994 / 513,853 | yes |
| B1 | not raised | not raised | yes |
| B2 | raised | raised | yes |

## Gemini (fresh chat https://gemini.google.com/app/34598c6808e22bfb, 28 October 2026)

Recorded from its reply, after it finished:

| measure | analysis | Gemini | match |
|---|---|---|---|
| (1) first-option share | 0.000 [0.000, 0.000] | 0.0000 [0.0000, 0.0001] | yes |
| (2) held share | 0.886 [0.855, 0.908] | 0.8857 [0.8544, 0.9080] | yes |
| held: number checked | 262,774 | 262,774 | yes |
| (3) accepted share | 0.201 | 0.2014 | yes |
| (4) per adult-year | 4.04 [3.78, 4.28] | 4.0390 [3.7707, 4.2719] | yes |
| (5) moments in pairs with ≥ 5 | 0.870 [0.859, 0.881] | 0.8697 [0.8595, 0.8807] | yes |
| pairs / with ≥ 5 | 986,994 / 513,853 | 986,994 / 513,853 | yes |
| B1 | not raised | not raised | yes |
| B2 | raised | raised | yes |

Interval ends differ in the third decimal at most, as expected from different bootstrap draws.

**Verdict:** every key number agrees across the analysis, GPT and Gemini. The findings are final.
