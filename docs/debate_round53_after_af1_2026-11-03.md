# Council round 53: after AF1, what next? (3 November 2026, about 01:10 New York)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round53_question_2026-11-03.md`, with the same file to all three.
- **The chats:** GPT, the main chat; Gemini 3.1 Pro, `d5ecc8b87be7ae89`; DeepSeek, `2552dbba-6c74-4cc4-b613-2228b137c47f`.

## First answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| ranking | **A**, D, C, B, E | **A**, C, B, D, E | **A**, C, D, B, E |
| first choice's estimate | 91% (for methodological validity, "not a 91% probability that it increases remaking") | 95% | about 78% |
| setting first | let a read-only funnel decide: base chance if failed rolls dominate, prey availability if empty tiles do | base success chance | prey availability and encounter ("a lost week with no prey is a structural failure, not a tuning knob") |
| target | the hunting/foraging return ratio (the Aché's about 1.1 as "a population-specific reference, not a universal hunter-gatherer target"); animal share secondary | the return ratio; the animal share is "an outcome of agent choices and local ecology" | the return ratio, with a range; the animal share described only (Cordain's basis is debated) |
| what is wrong in the reading | causation not established; "raising success probability alone could make unarmed hunting profitable, reducing rather than increasing demand for weapons" | "empirically flawless" | foraging (too easy without tools) and hunting (too unrewarding) are different failures; demand may not be enough (CO2: making loses on the built-in pull); FX2 and FX3 starved worlds, so safety comes first |

**Checked against the records:**
- DeepSeek's points on CO2 and on FX2/FX3 match the INDEX entries.
- GPT's point about bare-handed hunting is right about the code: the tool factor multiplies the base chance (`mind.hunt_chance`). Raising the base raises bare-handed and armed hunts in the same proportion, so the **absolute** gain from a weapon grows, but bare-handed hunting also becomes worthwhile.

## The merged plan (sent to all three)
- **Step 1, HN1: a read-only funnel on v11** (32 new seeds, frozen first). For every hunt it records:
  - whether prey stood on the tile;
  - the success roll;
  - meat kept against meat lost to carrying;
  - armed or bare-handed;
  - each hunter-week's food against matched forage-weeks, giving v11's return ratio with an interval.
- **Step 2, HR1: a calibration study,** frozen after HN1, with the rule written now:
  - **the setting:** if hunts with no prey on the tile are more than half of failed hunts, the one setting calibrated is
    prey encounter (density); otherwise the base chance;
  - **the arms:** levels chosen only to bring the return ratio toward the Aché's (a range of 0.5–1.5, as a
    population-specific reference);
  - **the primary:** calibration distance;
  - **guards first:** population and extinctions;
  - **reported separately:** armed and bare-handed returns;
  - **described only:** remaking and tool use;
  - **confirmation:** on new hold-out seeds.

## Final answers
- **GPT: 95%.** "Yes, I support the merged HN1 → HR1 plan". Its remaining caution: match forage-weeks "on opportunity
  and environmental conditions, not just person and season", and avoid reading the Aché range as universal realism.
- **Gemini: 98%.** "I fully support this merged plan". It holds that the armed/bare-handed split "neutralizes the risk of
  accidentally rewarding tool-less hunting".
- **DeepSeek: about 78%.** "Support: yes". Its caveat: report the armed/bare-handed ratio as "guard-adjacent" and "flag
  any material narrowing before adoption".

## Decision
- **The assistant's estimate:** 80% for HN1 (read-only); 60% for HR1.
- **HN1 is frozen next.** GPT's amendment is adopted: forage-weeks are matched on the tile's plant stock as well as on
  person and season. So is DeepSeek's: the armed/bare-handed ratio becomes a flagged description in HR1.
