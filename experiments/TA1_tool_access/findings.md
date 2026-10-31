# TA1 — Why do tools not reach hands? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `TA1-frozen` (operational note 1). Signed off by the assistant under sleep-mode autonomy (read-only; GPT
95%/90%, Gemini 95%/94%; debate rounds 35–36). Run on GitHub Actions (run 41213975492, `skip_zero=local`). 32 worlds
on nature v10 (seeds 21101–21132), LP (80 founders, 80 × 80), 200 years. Every number comes from `analyse_ta1.py`,
written before data; full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v10`);
- every forage tool's entry and exit is accounted for, and no worn tool stays in hand (mismatches 0).

**Population beside it:** no world died out. Mean living population 141.7; 105.8 adults per world-year in years
100–200. There were 7,026,833 adult forage weeks in years 100–200, of which 6,310,506 (89.8%) were bare-handed.

## The answer

**Both an access gap and a choice gap.** When adults forage bare-handed, a tool is usually near and could often be
made on the spot. Hardly anyone lacks the knowledge.

### Q1 — Why is a forager bare-handed? (primary; shares of bare-handed adult forage weeks)
- **(a) a forage tool is in someone's hands within 3 tiles: 81.9%** [80.2%, 83.4%].
  - (a′) with room to receive it: 68.0% [64.9%, 70.9%].
- **(b) the forager knows a helpful kind and could make it now: 72.6%** [71.2%, 73.9%].
  - (c) knows one but lacks materials: 26.8%;
  - (d) knows none: **0.5%**.
- **Hands:**
  - full with other things (e): 16.1%;
  - empty: 47.9%;
  - holding 1–3 other things: 52.1%.
- **The frozen reading: "both"** ((a) ≥ 0.50 and (b) ≥ 0.50). GPT: a classification, not causal proof.

### Q2–Q5 (described)
- **Q5:** in the (a′) weeks, the nearest holder's actual tool would add **9.9%** to those forages' food (TR1's
  arithmetic, with the carry room and plants).
- **Q2, who holds forage tools:**
  - children 0–11 in **39.2%** of their weeks;
  - teens 13.7%;
  - adults about 10.5–11.1%.
  - **Adult holders forage in only 36.7% of their holding weeks.**
- **Q3 and Q4, how tools move:**
  - **Into hands:** 86.9% are newly made (or changed from another item); 11.3% picked up from the ground; 1.1% passed
    on at death; 0.7% from a body.
  - **Out of hands:** **55.6% are used up as parts or changed**; 37.1% wear out; 4.1% are dropped; 2.1% go with a
    body.
  - A forage tool stays in one hand **58.6 weeks** on average.
  - **54.5% of forage-tool makes are by people who already hold one.**

## Against the prior (the assistant's, frozen)
1. "Neither: (a) and (b) below 0.50": **wrong.** Both are high (0.82 and 0.73).
2. "Hands holding other things in more than 30% of bare-handed weeks": **right** (52.1%).
3. "Most forage tools leave by wear": **wrong.** Most are used up as parts or changed (55.6%).

## What it means
- **Knowing is not the problem:** 99.5% of bare-handed foragers know a helpful kind. **Two things stand between
  knowledge and use:**
  1. **Access.** A tool is near in 82% of bare-handed weeks, but no one can hand it over. Its holder forages with it in
     only about a third of their weeks, and tools pile up in children's hands. The nearest tool would add about 10% to
     those forages.
  2. **Choice.** In 73% of bare-handed weeks the forager could make a tool now and does not. This matches CO2 and IW1:
     making loses to food at the choice, and tools help only modestly.
- **Tools are also turned into other things** (56% of exits): a tool's material often goes into bigger made things.
- **What follows, by the frozen branch "both":**
  - **(1) Handing a made thing to someone (B),** drafted with both models' guards (round 35):
    - objects conserved;
    - room in the receiver's hands;
    - the existing choice machinery;
    - no rewards or kin preference written in;
    - opportunities recorded apart from transfers.
    It is a nature-change test in a copy, allowed in sleep mode as a frozen study; **adopting it would follow the safe
    path in `CLAUDE.md`.**
  - **(2) The choice to make:** the creator's open learning-rule item and the worth of tools.
  - Both models are to be asked which first.
- **No change to nature** follows from this study by itself.

## Independent recompute (31 October 2026)
GPT and Gemini, each in a fresh chat, worked from per-world counts of the raw output only, without the analysis
script (`recompute_ta1.md`). **All three agree:** A 0.819 [0.802, 0.834]; B 0.726 [0.712, 0.739]; F 0.680; reading
"both".

**Final.**
