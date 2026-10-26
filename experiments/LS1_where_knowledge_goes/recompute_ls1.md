# LS1 — Independent recompute (26 October 2026)

**Who:** GPT, in a fresh chat (https://chatgpt.com/c/6adf2061-371c-83ea-97f1-6205719cbfb4), with no earlier context.
**What it saw:** the raw output of all 96 worlds (`output/*_seed_*.json`, reduced to the fields arm, seed, final_tick,
bins, decades, people and mismatch; nothing recomputed or summarised), a field dictionary, and the frozen definitions
of the four measures. **Not** the analysis script, `results.md` or the findings. It wrote its own Python and ran
10,000 whole-world bootstrap replicates.

## Results side by side

| measure | analysis (`analyse_ls1.py`) | GPT's recompute | match |
|---|---|---|---|
| mismatch dicts empty; worlds | yes; 64 LP + 32 D80 | yes; 64 + 32 (51 LP to year 1,000) | yes |
| Q1 LP copy loss by death, after year 100 | 0.979 [0.978, 0.981] | 0.9795 [0.9777, 0.9811] | yes |
| Q1 LP kind extinction by death | 0.979 [0.977, 0.981] | 0.9790 [0.9771, 0.9808] | yes |
| Q1 D80 copy loss / extinction by death | 0.983 / 0.983 | 0.9826 / 0.9831 | yes |
| Q3 LP Δ ln feasible / weighed / chosen | +0.773 / +0.333 / −3.034 | +0.7729 / +0.3327 / −3.0338 | yes |
| Q3 LP share of "chosen given weighed" | 1.57 [1.54, 1.61] | 1.5734 [1.5430, 1.6068] | yes |
| Q3 largest gate, LP and D80 | chosen given weighed | C, chosen given weighed | yes |
| Q3 D80 Δ ln feasible / weighed / chosen | +0.936 / +0.327 / −3.206 | +0.9389 / +0.3237 / −3.2213 | explained below |
| Q4 worlds; s early → late | 51; 0.318 → 0.021 | 51; 0.3178 → 0.0211 | yes |
| Q4 share of the fall carried by s | 0.97 | 0.9736 [0.9596, 0.9878] | yes |
| Q4 g, k shares | 0.00, 0.02 | 0.0023, 0.0241 | yes |
| Q4 Δ ln A4 | −2.786 | −2.7859 | yes |
| Q5 inheritance, born years 0–50 | 0.410 [0.405, 0.415] | 0.4098 [0.4048, 0.4150] | yes |
| Q5 born 50–100 / 100–150 | 0.315 / 0.290 | 0.3152 / 0.2900 | yes |
| Q5 pooled, born year 100 on | 181,634 / 654,555 = 0.2775 (checked separately) | 181,634 / 654,555 = 0.2775 [0.2682, 0.2863] | yes, exactly |

**The one difference, D80's Q3, is explained.** The analysis reads the decline over the worlds alive at the start of
years 100–200 (30 of 32 D80 worlds: one ended at year 85, one at year 100), using the same worlds for the early and the
late period. The request to GPT did not say this, and GPT pooled the early period over all 32 worlds. Run GPT's way, the
raw data give GPT's numbers exactly (+0.9389, +0.3237, −3.2213; checked by script). LP is unaffected, since all 64 LP
worlds were alive then. The conclusion (chosen given weighed carries the decline) is the same either way.

**GPT's cautions (adopted in the findings):**
- The Q1 shares are event channels. They show *when* copies and kinds are lost (at death), not that death is the cause
  of the loss.
- The Q3 decomposition places the fall at the choice, given that making was weighed. It does not show why that choice
  changes.

**Verdict:** every key number agrees, and the one difference has a known cause. The findings are final.
