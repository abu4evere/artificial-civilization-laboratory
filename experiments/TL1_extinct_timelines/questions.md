# TL1 — Extinct-world timelines: did reproduction cease before demographic collapse? (SIGNED OFF 21 October 2026; frozen as `TL1-frozen` before any analysis)

**Why.** TP1 (`../TP1_tipping_point/findings.md`) showed that extinction risk falls along a smooth slope with fertile
women rather than dropping at a sharp threshold above zero. F1 (`../F1_baseline_fragility/findings.md`) found on 64 worlds
that births stopped 40–65 years before extinction, with unpartnered women reaching 100% in the final decades. GPT's review
of TP1 (`../TP1_tipping_point/gpt_review_tp1.md`) recommended an explicit, read-only reconstruction of extinct worlds'
timelines across the large saved sample:
1. Did births stop decades before the last person died (reproductive cessation before mortality collapse)?
2. When births stopped, were eligible reproductive pairs still present in the world, or was the pool empty?
3. Is a multi-year gap with zero births an absorbing state (a point of no return), or do worlds ever recover?
4. What killed the last inhabitants (old age vs starvation/thirst)?

**Read-only:** no new runs; reads existing saved control worlds from RT1b, FX2, and FX3.

---

## 1. Worlds and Data (Decision 1)

Control worlds saved under nature v2 (the same 768 control worlds analyzed in TP1):
- **Discovery:** RT1b's C (`output_rt1b`, seeds 5701–5956; 91 extinct) and FX2's C (`output`, seeds 6001–6256; 96 extinct): 512 worlds (187 extinct, 325 surviving).
- **Holdout:** FX3's C (`output`, seeds 7301–7556): 256 worlds (80 extinct, 176 surviving), read only after discovery results are written and committed.

All world files record exact annual demographic snapshots (`years`), birth events (`births` with year and mother's age),
and death events (`deaths` with year, age, stage, and cause).

---

## 2. Questions and Measures (fixed in advance)

### Q1. The Reproductive Gap ($\Delta T$)
- In each extinct world, let $T_{\text{last\_birth}}$ be the year of the final recorded birth, and $T_{\text{extinct}}$ be the
  year of the final death.
- **Measure:** $\Delta T = T_{\text{extinct}} - T_{\text{last\_birth}}$ (in years).
- **Frozen reading:**
  - **Ageing out:** median $\Delta T \ge 30$ years, and $\Delta T \ge 20$ in $\ge 80\%$ of extinct worlds (births ceased
    decades before extinction).
  - **Acute collapse:** median $\Delta T < 10$ years, or $\Delta T < 10$ in $\ge 50\%$ of extinct worlds (mortality
    event directly closes the world).
  - **Mixed:** neither condition met.

### Q2. Were Eligible Pairs Present When Births Stopped?
- Evaluated at the exact snapshot year of the last birth: $t = T_{\text{last\_birth}}$.
- Count only extinct worlds where at least one single fertile woman was alive at that snapshot (`women_single > 0`).
- **Measure:** The share of single fertile women who had an eligible (living, unrelated) man available in the world:
  $$\text{eligible\_share} = \frac{\text{women\_single} - \text{women\_single\_no\_mate}}{\text{women\_single}}$$
  reported per world and averaged across qualifying worlds, alongside the number of qualifying worlds.
  The distribution across worlds is reported as a description only.
- **Frozen reading:**
  - If mean $\text{eligible\_share} \ge 0.50$, confirmed as **"failure to pair"** (eligible partners existed but did not court/form couples).
  - If mean $\text{eligible\_share} < 0.20$, confirmed as **"empty mate pool"** (demographic exhaustion of eligible men).
  - Anything in between is confirmed as **"mixed"**.

### Q3. The Point of No Return: Does a Birth Hiatus Recover?
- One row per world (no overlapping episodes). For each world (both extinct and surviving) that ever has at least one
  fertile woman alive (`women > 0`), find its **first episode** of $K$ consecutive years with zero births ($K \in \{5, 10, 15\}$).
- For worlds experiencing a first $K$-year hiatus, report two distinct recovery measures:
  1. **Subsequent birth:** share of worlds that ever record another birth after the hiatus ($n / N$).
  2. **Survival:** share of worlds that survive to year 120 ($n / N$).
- **Frozen reading:** If for $K = 10$, the survival rate is $< 5\%$, a 10-year birth hiatus is classified as an
  **"empirical point of no return"** (an absorbing state in practice). If $\ge 20\%$, classified as **"recoverable"**;
  otherwise **"rarely recovered"**.

### Q4. Causes of Final Deaths
- For all deaths occurring in the final 10 years before extinction:
  - Cause breakdown using exact saved cause names: `illness`, `starvation`, `old age`, `thirst`, `neglect`, `childbirth`, `killed`, `cold`
    (with death counts beside every share).
- **Frozen reading:** If old age accounts for $\ge 40\%$ of deaths in the final decade, the demographic collapse is
  confirmed as **"natural attrition following reproductive failure"**. Otherwise **"not confirmed"**.

---

## 3. Statistical Rules and Holdout Confirmation

- All discovery findings are committed before holdout files are touched.
- World counts ($n / N$) and population counts are reported beside every percentage.
- A discovery conclusion **stands** on the holdout if the holdout point estimate falls within $\pm 10$ percentage points
  (or $\pm 5$ years for medians) of the discovery estimate, and satisfies the same qualitative reading rule.

---

## 4. Assistant's Prior (written before looking at data; held loosely)

1. $\Delta T$ will have a median $\ge 40$ years, with $\ge 85\%$ of extinct worlds having $\Delta T \ge 25$ years (ageing out).
2. At $T_{\text{last\_birth}}$, among extinct worlds with single fertile women, mean $\text{eligible\_share} \ge 0.60$.
3. For $K = 10$, subsequent birth will be $< 10\%$ and survival $< 5\%$ (point of no return).
4. Old age will be the plurality cause of death ($\ge 45\%$) in the final decade.

---

## 5. Decisions for the Creator

1. **Scope:** 512 discovery worlds (187 extinct), 256 holdout worlds (80 extinct) from RT1b, FX2, and FX3.
2. **Measures:** The four questions, exact year $T_{\text{last\_birth}}$ mate measure, first-hiatus rule, and three-way outcome classes.
3. **Priors:** Frozen as written.

---

## Sign-off (21 October 2026)

The creator: "approve all recommendations, freeze it". All recommended options and the prior stand as written.
