# Council round 85: NB3-A, the feeding autopsy (11 November 2026)

**Question:** `experiments/NB3A_feeding_autopsy/questions.md` (the draft), attached as a file, with four questions.
- **Gemini** was busy with NB3's recompute in its only working tab, so it was not asked. **DeepSeek's** page does not
  take input. Both are to be asked later, as opinion only.

## GPT (chat 6af4f4cf, Thinking medium), labelled as GPT
- **Verdict:** "Approve with minor revisions before freezing. This is the right next study."
- **Q1, the patterns:** mostly right. Add a sixth, **"has food but does not eat"**.
  - Kin having surplus does not show that the starving person could get it (availability vs access).
  - "Cannot find" measures failed attempts, not inability to find.
- **Q2, the comparison:** c stays primary, and fH should be included as the mechanistic comparison. n2 should not be in
  the primary: its own failures complicate things.
- **Q3, the window:** 8 weeks for the frozen classifications, plus a 24-week sensitivity window.
- **Biggest risk:** "mistaking symptoms of starvation for causes". A dying person may stop foraging because it is
  already weak. The time order must be kept.
- **Changes:**
  1. add "has food but does not eat";
  2. record the ability to act: unable, no food act offered, or able but chose otherwise;
  3. **compare against matched survivors** (the same world, age group and week);
  4. track food received per child (recipient level), not only totals;
  5. report each pattern as deaths per 1,000 living-years, f against c, not only as shares;
  6. keep the fingerprint rule and report how many worlds remain.
- **Probabilities that each pattern leads:** child not fed 60%; not shared 55%; does not try 45%; cannot find 25%;
  hard times 15%.
- **Its leading hypothesis:** the people can get food, but the brain does not prioritise sharing and care. Its largest
  uncertainty is whether food production itself has fallen.
- **Its principle:** "Don't just ask what starving agents did before dying. Ask what the surviving agents did
  differently under comparable conditions."

## Taken into the plan (the assistant)
All six changes. In detail:
- **The early window:** "does not try" and "cannot find" are judged on weeks 8 to 3 before death, leaving out the last
  2 weeks, when weakness may be the cause.
- **"Leads" now also needs** the pattern to be at least 1.5 times as common in f's starved as in **f's matched
  survivors**.

**Reworked before freezing** (the assistant, after reading `code_nb3/acl/biology.py`):
- eating is automatic each week, and caregivers feed their dependents first, in full when they can;
- so GPT's "has food but does not eat" cannot happen by construction, and is kept as a code check;
- "child not fed" became two patterns, **"caregiver short"** and **"no caregiver"**.
