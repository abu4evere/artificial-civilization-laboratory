# AW1 — Learning a craft from others: results

Frozen as `AW1-frozen`. run_aw1.py, analyse_aw1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (128 of 128): **yes**
- One fingerprint (`code_aw1`): **yes**
- Each arm passed only its own kind of step (v and x none): **yes**

**Valid.**

Paired seeds: 32; years 100–200. Extinct by year 200: v 1, w 0, t 0, x 3. Mean living in the window: v 113.2, w 114.3, t 108.9, x 122.3.

## Primary — making events per adult-year, years 100–200

| arm | making per adult-year | − v [95%] |
|---|---|---|
| v (v9) | 0.0763 | |
| w (watching) | 0.0754 | -0.0009 [-0.0085, +0.0066] |
| t (being shown) | 0.0832 | +0.0069 [-0.0007, +0.0146] |
| x (sham) | 0.0798 | +0.0035 [-0.0026, +0.0095] |

## The frozen rule

- **w:** lower bound -0.0085 above 0 and above the sham's upper bound +0.0095: **not supported**. Flags: extinct 0 vs v 1 (no flag); population w ÷ v = 1.010 (no flag).
- **t:** lower bound -0.0007 above 0 and above the sham's upper bound +0.0095: **not supported**. Flags: extinct 0 vs v 1 (no flag); population t ÷ v = 0.962 (no flag).

## Secondaries (described; years 100–200)

| measure | v | w − v [95%] | t − v [95%] | x − v [95%] |
|---|---|---|---|---|
| world-born adults' (20–40) crafting skill | 0.2616 | +0.0098 [-0.0048, +0.0248] | +0.2238 [+0.1911, +0.2579] | +0.0133 [-0.0003, +0.0276] |
| children's (6–11) crafting skill | 0.1811 | +0.0034 [-0.0069, +0.0138] | +0.0744 [+0.0602, +0.0893] | +0.0097 [-0.0000, +0.0193] |
| teens' (12–15) making per teen-year | 0.0729 | -0.0045 [-0.0135, +0.0042] | +0.0045 [-0.0040, +0.0131] | +0.0005 [-0.0072, +0.0073] |
| made things held per adult | 1.0533 | -0.0455 [-0.1611, +0.0718] | +0.0019 [-0.0988, +0.1182] | +0.0877 [-0.0188, +0.2028] |
| steps passed by watching, per living person-year | 0.0000 | +0.0293 [+0.0253, +0.0331] | +0.0000 [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] |
| steps passed by being shown, per living person-year | 0.0000 | +0.0000 [+0.0000, +0.0000] | +1.0677 [+0.8514, +1.3146] | +0.0000 [+0.0000, +0.0000] |

Whole-run steps passed (sum over worlds): v: watched 0, shown 0; w: watched 31105, shown 0; t: watched 0, shown 908582; x: watched 0, shown 0.
