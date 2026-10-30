# Debate round 34: the apprenticeship law, after LS2 (30 October 2026)

**GPT's and Gemini's opinions, not sign-off. Only the creator decides.** The same text went to the main ChatGPT chat
and the ACL Gemini chat. Facts given: LS2's final numbers; the code facts from the read-only scout
(`docs/design_note_apprenticeship_autonomy_2026-10-30.md`); the research notes (`docs/research/skill_learning_sources_2026-10-30.md`):
Morgan et al. 2015 (teaching, and especially language, improved stone-tool transmission; imitation and emulation did
not) and Lew-Levy et al. 2017 (forager children learn by play, observation and participation; adults teach complex
tool making in adolescence). Two candidate laws, each reusing nature's existing chance and skill step: **W**, watching
someone make a thing gives an onlooker one practice step; **T**, being shown a recipe in talk also gives the learner
one practice step.

## Answers
| question | GPT | Gemini |
|---|---|---|
| Which law | **W and T as separate arms** (v9, W, T, sham); slightly favours T (closer to the teaching evidence); W could reach children who rarely get lessons | W, T **and WT combined** as separate arms, plus sham (are they additive?) |
| Primary | **making**: making events per adult person-year (years 100–999); supported only if the paired 95% interval of (arm − v9) is above 0 and outside the sham's interval; demographic flags pre-registered; skill a secondary mechanism check | **making**: make choices per adult-year in years 100–200, up ≥ 2.0× (or +0.05) **and** world-born adults' skill up ≥ +0.03, no flags |
| Risk: skill up, making flat | likely, because the choice bottleneck remains; informative, but not enough to adopt for cumulative learning | "high"; proposes that each watched or taught practice step also triggers a TD (habit) update for q(s, make) |
| Size | 32 paired seeds × 1,000 years, after AG1 | 32 paired seeds × 200 years, without waiting for AG1 |
| Estimate | 90% informative; **40%** a meaningful rise in making | 90% |

## Council: checked
- **Both put making first.** That follows LS2: the leak is at the choice, so a law that raises only skill does not
  answer the question. Agreed.
- **Making does not read skill directly.** In `mind.py` the pull to make comes from the thing's worth, the person's
  diligence and hunger; crafting skill enters only through better strikes, faster gathering and fewer copying errors.
  So a skill-only law can raise making only indirectly. GPT's 40% is plausible; a "no" would itself say technique is
  not the bottleneck.
- **Gemini's TD coupling is a second mechanism** and would need a reward value for a step nobody took (the scout found
  that the only precedent, `_follow`, is off by default). Rejected for this study; noted for later.
- **Gemini's thresholds (2.0×, +0.05, +0.03) are invented.** ACL's rule shape is CU1's: the interval above 0 and beyond
  the sham's band.
- **WT (combined):** one change at a time; if W and T each work, a combined arm can follow.
- **Size:** CU1's pattern fits: 200 years first (32 paired seeds, 128 worlds, fits the cloud), then a 1,000-year check
  (like LC1) only if supported. A 1,000-year four-arm run on 32 seeds would overrun GitHub's job limit.
- Gemini's "1 in 800" is LS1's v7 figure; under v9 (LS2) chosen given weighed was about 1 in 560 in years 100–200.

## Proposed (a draft for the creator's sign-off): AW1, `experiments/AW1_watch_and_teach/questions.md`
Arms v9, W, T, sham; 32 paired seeds; 200 years; primary making per adult-year in years 100–200 (CU1's measure); rule
as CU1's; skill and inheritance as secondaries. GPT 90% informative (40% that making rises meaningfully); Gemini 90%;
the assistant 75% informative.
