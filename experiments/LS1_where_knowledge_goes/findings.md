# LS1 — Where does knowledge go? Findings (recomputed independently; final)

Frozen as `LS1-frozen` (Revision 1, operational note 1); run on GitHub Actions (run 40260721191). 96 worlds on nature
v7: LP (primary, 64 worlds, seeds 18001–18064, 80 founders on an 80×80 map) and D80 (secondary, described, 32 worlds,
seeds 18101–18132), 1,000 years. Every number comes from `analyse_ls1.py` (written before data); full tables are in
`results.md`. Validity: zero checks pass; all 96 worlds present under one fingerprint (`code_v7`); the ledger, kind
counts and holdings match in every world (every mismatch count is 0).

**Check against M1 (M1's rules, LP, 51 worlds alive at year 1,000):** A4 late / early 0.061 [0.050, 0.072] (M1 on v6:
0.054 [0.046, 0.063]); B-retained late 0, as in M1. The erosion is the same on v7.

**Population (LP):** 104 people at the start, 129 in years 50–100, 77–83 in years 300–700, 102 in years 900–1,000.
51 of 64 worlds lived to year 1,000 (13 ended between years 156 and 872). Every bin is read over the worlds alive at
its start.

## The answer

**Knowledge does not leak from living minds. It goes with the dead, and it is not replaced, because people who could
make things and weigh making stop choosing to make.**

### Q1 — Where copies and kinds are lost (LP, after year 100)
- **The dominant copy-loss channel is death:** 0.979 [0.978, 0.981] of 661,439 losses; push-out by the 12-recipe limit
  0.021; forgetting as useless 0.
- **The dominant kind-extinction channel is death** (the last holder died): 0.979 [0.977, 0.981] of 71,152
  extinctions.
- **Net flow:** positive up to year 100 (+505 to +3 per 1,000 person-years), negative in every century from 100 to 900
  (−42 at worst, then shrinking towards 0), and +0.0 in years 900–1,000. By the frozen rule it **never** turns negative
  and stays negative: after year 100 the stock shrinks, then levels off at a low value.
- Inflow by invention falls from 269 per 1,000 person-years (years 5–10) to 0.1 (years 900–1,000). After year 300
  nearly all inflow is rediscovery and teaching.
- D80: the same, death 0.983 [0.977, 0.987]; net flow negative from years 20–50.

### Q2 — Origin, transmission, persistence (LP, useful kinds)
| origin, era | kinds | ever held by 2+ | held 25 years after the maker's death | held 2+ generations after |
|---|---|---|---|---|
| founder, years 0–100 | 5,616 | 0.73 | 0.55 | 0.69 |
| world-born, years 0–100 | 37,337 | 0.30 | 0.14 | 0.25 |
| world-born, years 100–1,000 | 13,203 | 0.12 | 0.03 | 0.08 |

Founders' know-how is shared and kept far more often than what the world's own people invent, and what is invented
later is kept least. In years 0–100, 0.73 [0.72, 0.74] of the useful know-how held was founders' (descriptive).

### Q3 — The making funnel (LP, adults)
From years 0–10 to years 100–200, making per adult person-week fell (Δ ln −1.93). The exact decomposition:
- **feasible** (can make something now): Δ ln **+0.77** [0.75, 0.79]. It *rose*: 0.23–0.55 → 0.80.
- **weighed given feasible:** Δ ln **+0.33** [0.31, 0.35]. It *rose*: 0.49–0.63 → 0.81.
- **chosen given weighed:** Δ ln **−3.03** [−3.10, −2.97], share of the decline **1.57** [1.54, 1.61].

**The gate carrying the largest share: chosen given weighed.** People could make, and making was among their options,
but they chose it about 1 time in 800 (0.0012) in years 100–200, against 1 in 40 (0.027) in years 0–5. The fall is
steepest between years 10–20 (0.0195) and 50–100 (0.0026). When making was weighed and not chosen, forage won 0.68 of
the time, then gathering 0.09, putting things down 0.07, rest 0.06. D80: the same gate, share 1.65 [1.58, 1.73].

### Q4 — The fall in tools' food, exactly (LP, 51 worlds alive at year 1,000)
A4 = s × g × k fell by Δ ln −2.79 (decades 2–4 to 95–99):
- **s, the share of forage acts with a tool: 0.318 → 0.021, share of the fall 0.97** (Δ ln −2.71 [−2.92, −2.51]);
- g, food per tool act: 21.2 → 21.1, share 0.00;
- k, the tool's part of that food: 0.132 → 0.123, share 0.02.

Tools still work as well when used. **Almost nobody has one.** In decades 2–4, 0.98 of tools used were made by their
holder; only 0.05 were made in the first 20 years. A person who lost their last forage tool had one again within a
year 0.59 of the time in years 0–5, 0.37 in years 20–50, 0.14 in years 100–200 and 0.07 after year 400.

### Q5 — Does each generation take up what it inherits? (LP, world-born, by birth cohort)
- **Inheritance rate** (of the useful recipes a child's carers held while it was a child, the share it acquired by 30):
  **0.41** [0.405, 0.415] for people born in years 0–50; **0.32** for 50–100; **0.29** for 100–150; then steady at
  **0.26–0.29** in every later cohort. It falls, then holds; it never rises.
- How it was inherited: early, mostly by making it oneself (own making 0.65, taught 0.24); late, about half taught
  (taught 0.54, own making 0.46).
- Useful recipes acquired by 30: 14.5 (born years 0–50) → 7.3 (150–200) → 2.1 (950–1,000).
- Of recipes got from others, the share later made: 0.10 (born 0–50), then 0.02–0.03.
- Useful kinds invented by world-born people: 45,610; held by someone of a later generation: 0.19.
- D80: the same pattern, lower (0.40 → 0.19–0.25).

## Described (associations, not causes)
- **Crafting skill at 16** falls by cohort: 0.45 (born years 0–50) → 0.18 (100–200) → 0.04 (900–1,000), with practice
  weeks per person 39 → 12 → 2.5.
- **The habit value for "make" at 16 rises** by cohort (0.005 → 0.030) and is the same as the carer's and the talk
  partners' to three decimals. The habit for making does not fall; making still loses to foraging.
- **Teaching:** lessons offered per person-year rise to 3.95 in years 10–20, then fall to 0.46; the share taken is low
  throughout (0.03–0.13); of lessons taken, the share later made falls from 0.34 to 0.04.

## Against the prior
1. Net flow negative within 0–50 and staying negative: **wrong for LP** (negative only after year 100, levelling at 0);
   right for D80 (20–50).
2. Copy loss by death or push-out, kind extinction mostly death: **right** (death, 0.98 for both).
3. Founder kinds transmitted more than world-born: **right**. Persistence over 2+ generations under 10% for both:
   **wrong** (founder 0.69, early world-born 0.25; only late world-born 0.08).
4. "Weighed given feasible" carries the largest share: **wrong.** Feasible and weighed both rose; **chosen given
   weighed** carries it all.
5. A4's fall carried by s: **right** (0.97).
6. Inheritance under 20% from the first cohort and not rising: **wrong on the level** (0.41, then 0.26–0.29); right
   that it does not rise.
7. Making stops being weighed first: **wrong.** It stops being chosen.

## What follows (frozen branches that apply)
- **Q3's largest share is "chosen"** (Q5's rate falls to about a quarter and holds): each generation does not use what
  it could make. Next: an evidence review of how forager children come to make and use tools (apprenticeship,
  necessity, worth), before any change to nature.
- **Kind extinction is mostly death:** knowledge is not passed on before its holder dies. Next: transmission (CA1's
  bottleneck).
- **Q4's fall is carried by s:** tools are not remade or replaced. The tool lifecycle is the leak.
- Copy loss is not push-out (0.02): memory is not the leak.
- **Timing:** the choice to make collapses first (years 10–100), together with replacement (from years 20–50); skill
  and practice fall by cohort after it.

**Read with care:** Q1's shares say *when* copies and kinds are lost (when their holder dies), not that death causes
the loss: what is lost at death is what was never passed on. Q3 places the fall at the choice; it does not show why
the choice changes.

## Independent recompute (26 October 2026)
GPT, in a fresh chat, from the raw files only, without the analysis script (`recompute_ls1.md`). Every key number
agrees: Q1's death shares (LP 0.9795 copies, 0.9790 kinds), Q3's decomposition and largest gate (LP chosen share
1.5734), Q4's split (s 0.9736) and Q5's inheritance rates (0.4098, 0.3152, 0.2900; pooled from year 100 0.2775). One
difference, D80's Q3 (+0.939 / +0.324 / −3.221 against +0.936 / +0.327 / −3.206), comes from which worlds were pooled in
years 0–10 (all 32 against the 30 alive at year 100); run GPT's way, the raw data give its numbers exactly. **Final.**
