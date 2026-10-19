# RT1 — Residence time: findings

Frozen as `RT1-frozen`, Amendment 1 `RT1-amend1` (both before any data). Table: `results.md`, from `analyse_rt1.py`.
Run: `run_rt1.py` (768 worlds; nature v2 + `residence_weeks`). Described checks: `thirst_check.py` and its logs.

## Validity

Zero checks PASS (off = `code_v2`; observers read-only; R4 acts; a saved and reloaded R4 world continues exactly); all 768
worlds present; one fingerprint. **Manipulation check passed:** R4's adults changed the tile they slept on in **20.5%** of
weeks (needed 15–35%; forager camps about 23%; C 55.0%), and travelled **0.80** of C's distance a month (needed
0.75–1.25). Sham quiet (94 vs 93; p = 1). **Valid.**

## The frozen reading: residence time changes survival

| arm | died out (of 256) | saved / lost | p | effect (C − arm) | 95% interval |
|---|---|---|---|---|---|
| C (today's rule) | 93 | | | | |
| **R4** | **164** | 22 / 93 | 1.4 × 10⁻¹¹ | **−0.277** | [−0.352, −0.203] |
| sham | 94 | 41 / 42 | 1 | −0.004 | [−0.074, +0.062] |

**Frozen rule: "residence time changes survival"**, and in the harmful direction: about 28 more worlds in every hundred
die out.

## Described (population first, rule 18)

| arm | median population, year 60 / 119 | births per woman-year | blocked for want of a partner | between-lineage meeting | adult starvation deaths, years 0–39 |
|---|---|---|---|---|---|
| C | 22 / 22 | 0.128 | 0.548 | 0.184 | 1,974 |
| R4 | 7 / 0 | 0.127 | 0.540 | **0.242** | 1,968 |

Births, partner finding and starvation are unchanged; bands even meet **more** under R4. **Deaths by cause, years 0–39:**
thirst **2,864 in R4 against 1,740 in C** (adults 2,128 against 1,240; children 661 against 400); every other cause the
same or lower.

## Why: the base rule, not staying put (described, not a frozen reading)

In ACL a person goes short of water only if no reachable fresh water is within sight of where they **started or ended**
the week (`weather.drink`). R4 sends people back to their base at the end of the week. So someone who walks to water
and is brought home ends the week at a dry base, and the walk to water counts for nothing. Real camps are pitched near
water; R4's bases are wherever a person happened to stop in a move week.

**Checked** (`thirst_check.py`; read-only replays, seeds 5001–5008, 30 years): of adult-weeks spent short of water, the
person had chosen a destination with water in sight in **52% under R4** (401 of 770) against **0.9% under C** (6 of 667).
Most of R4's thirst is people who went to water and were sent back.

So RT1 shows that **this way of keeping a base** kills worlds, through water, not that moving camp less often does. It
cannot say what forager-like residence would do. That would need the week's trip to water to count, as a daily trip
from camp does.

## The assistant's prior, against the result

| prior (frozen) | result |
|---|---|
| no meaningful effect on survival | **wrong**: R4 changes survival, strongly, for the worse |
| fewer between-band meetings | **wrong**: more (0.24 against 0.18) |
| fewer starvation deaths than HB1 | **right in kind**: starvation unchanged; the deaths came from thirst |

## What it decides (the creator decides)

Nothing in nature changes. A second, separately frozen study (RT1b) could fix the flaw the run exposed: for example, a
person drinks from water within sight of anywhere they went that week (the trip out and back counts, as a forager's daily
walk to water does), or a base can only be set within reach of water. Either is a design choice under Law 126. Also
noted: HB1's unexplained hunger (couples returned to a fixed home) may share a mechanism; its causes of death could be
read the same way (a read-only check).

## Note (18 October 2026, appended; rule 19): the HB1 lead above does not hold

The line above suggested HB1's unexplained hunger "may share a mechanism" with RT1's. HB1's own record already answers
it, with no new run: in years 0–39, HB1's home-base arm had **fewer** adult thirst deaths than its control (**249 against
326**; `../HB1_home_base/explore.md`, "Deaths by stage and cause"), while starvation rose (714 against 412). HB1 returned
couples to a home they had *chosen* as the place that felt best, not to wherever they stopped, and its extra deaths were
hunger, not thirst. So RT1's water mechanism does not explain HB1. The HB1 question was also closed by the creator after
HF4 (`../HF4_hunger_ledger/findings.md`). Checked from saved tables only; GPT (under the creator's
delegation) had approved a read-only check, which this makes unnecessary.
