# VA1: is a new invention valued before it is lost? (results)

Frozen as `VA1-frozen`. run_va1.py, analyse_va1.py (written before data). Read-only on v13; kinds first made in years 130–165, followed 5 years.

## Validity

- Zero checks (All: PASS, same `code_v13` fingerprint): **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint, `code_v13`'s: **yes**

**Valid.**

## Primary 1: used before lost

Share of kinds used by their inventor at least once before the recipe was gone: **0.824 [0.788, 0.858]** (kinds 1,194).

**Reading: not shown (most kinds are used before loss, or the interval reaches 0.5).**

## Primary 2: counterfactual survival of the 12-recipe cap at invention

| first value | survives the cap | 95% | kinds |
|---|---|---|---|
| actual (value 0; held at the first week's end) | 0.871 | [0.835, 0.905] | 1,194 |
| v_first (the first use's felt value; used kinds) | 0.998 | [0.995, 1.000] | 1,141 |
| v_sim (similar known kinds' values) | 1.000 | [1.000, 1.000] | 1,188 |

Amendment 1: the v_sim row is close to 1 by construction (a mean of the person's values is almost always above their lowest) and carries no reading.

## Primary 3: does experience with similar things predict a new kind's usefulness?

Correlation of v_sim with the first use's felt value: **0.297 [0.245, 0.350]** (kinds used and with a v_sim: 1,135).
Amendment 1: the plain mean value's correlation with the first felt value: 0.267. "Similar experience is informative" requires v_sim's interval wholly above 0.2 and v_sim's correlation above the plain mean's.

**Reading: similar experience is informative.**

**What follows (decided before data): the next target is opportunity or intention (getting the inputs again).**

## Described

- Kinds 1,194; ever used by the inventor within 5 years 1,141 (0.956).
- Stage shares (LD1's funnel): 0: 0.129, 1: 0.869, 2: 0.001, 3: 0.001, 4: 0.001, 5: 0.000
- Weeks to first use (median): 0; weeks to loss (median): 0 (of 193 lost)
- First uses with felt > 0.05: 903 of 1,141; v_first clears the 0.05 offer threshold: 903; v_sim clears it: 533 of 1,188
- Cap full at invention: 155 of 1,194

## Population

- Worlds 32; extinct 1

