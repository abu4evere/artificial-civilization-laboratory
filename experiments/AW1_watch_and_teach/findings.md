# AW1 — Learning a craft from others: does watching, or being shown, pass technique and bring making back? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `AW1-frozen` (operational note 1); **signed off by the creator** ("yea go ahead with AW1 run it after AG1").
A nature-change study: `code_aw1` = `code_v9` + one setting, `skill_pass` (`v9_to_aw1.diff`). Run on GitHub Actions (run
41111670960, `skip_zero=local`). 128 worlds: v (v9), w (watching), t (being shown), x (sham), on the same 32 paired
seeds (20601–20632). LP (80 founders, 80 × 80), 200 years. Every number comes from `analyse_aw1.py`, written before
data; full tables are in `results.md`.

**Validity:** zero checks pass; all 128 worlds present under one fingerprint (`code_aw1`); each arm passed only its own
kind of step (v and the sham none).

**Population beside it:** mean living in years 100–200: v 113.2, w 114.3, t 108.9, sham 122.3. Died out by year 200:
v 1, w 0, t 0, sham 3.

## The answer

**No. Neither law brings making back.** Being shown (T) passes a great deal of technique: world-born adults' crafting
skill nearly doubles. But people do not make things more often than the sham's chance drift. Watching (W) passes
almost nothing at nature's existing chance of noticing.

### Primary — making events per adult-year, years 100–200
| arm | making per adult-year | − v [95%] |
|---|---|---|
| v (v9) | 0.0763 | |
| w (watching) | 0.0754 | −0.0009 [−0.0085, +0.0066] |
| t (being shown) | 0.0832 | +0.0069 [−0.0007, +0.0146] |
| x (sham) | 0.0798 | +0.0035 [−0.0026, +0.0095] |

**The frozen rule:** an arm supports if the lower bound of (arm − v) is above 0 and above the sham's upper bound
(+0.0095). **w: not supported** (lower bound −0.0085). **t: not supported** (lower bound −0.0007). **Flags: none**:
extinct 0 against v's 1 in both; population w ÷ v 1.010, t ÷ v 0.962.

### Secondaries (described; years 100–200)
| measure | v | w − v [95%] | t − v [95%] | sham − v [95%] |
|---|---|---|---|---|
| world-born adults' (20–40) crafting skill | 0.262 | +0.010 [−0.005, +0.025] | **+0.224 [+0.191, +0.258]** | +0.013 [−0.000, +0.028] |
| children's (6–11) crafting skill | 0.181 | +0.003 [−0.007, +0.014] | **+0.074 [+0.060, +0.089]** | +0.010 [−0.000, +0.019] |
| teens' (12–15) making per teen-year | 0.073 | −0.005 [−0.014, +0.004] | +0.005 [−0.004, +0.013] | +0.001 [−0.007, +0.007] |
| made things held per adult | 1.05 | −0.05 [−0.16, +0.07] | +0.00 [−0.10, +0.12] | +0.09 [−0.02, +0.20] |
| practice steps passed per living person-year | 0 | 0.029 | **1.07** | 0 |

Over the whole run, the law passed 31,105 steps in w and 908,582 in t (summed over 32 worlds).

## Against the prior (the assistant's, frozen)
1. "Both arms raise skill, T more than W": **half right.** T raises skill strongly; W's rise is not clear (its interval
   includes 0). Watching at nature's noticing chance passes about 0.03 steps per person-year, too few to matter.
2. "Making rises little": **right.** Skill nearly doubles in t, and making does not follow.
3. "No flags": **right.**

GPT gave 40% that making would rise meaningfully. It did not.

## What it means
- **Technique is not the bottleneck. The choice is.** This is the frozen branch "skill rises, making does not". LS2
  located the leak at the choice to make; AW1 now shows that a large, real gain in skill does not move that choice. In
  the code, the pull to make reads the thing's worth, diligence and hunger, not skill (`mind.py`).
- **Being shown works as a channel; watching barely does.** It agrees with Morgan et al. 2015 (abstract): teaching
  passed stone-tool skill, imitation did not. But in ACL a skilled person still rarely chooses to make.
- **Next, as frozen:** a read-only look at why the choice falls. What makes foraging win (LS2: 0.67 of the time when
  making was weighed)? Is it the worth people expect from made things, or how often those things help? No change to
  nature until that is understood.
- **Adoption:** neither law is supported, so neither is proposed for adoption.

## Independent recompute
Pending: GPT and Gemini, fresh chats, from raw per-world sums (`recompute/aw1_one_file.csv`). Recorded only from their
actual replies.

## Independent recompute (30 October 2026)
GPT and Gemini, each in a fresh chat, worked from raw per-world sums only, without the analysis script
(`recompute_aw1.md`). **All three agree:** making per adult-year v 0.0763, w 0.0754, t 0.0832, sham 0.0798; w − v
−0.0009 and t − v +0.0069, both **not supported**; no flags; being shown raises world-born adults' skill by +0.2238.

**Final.**
