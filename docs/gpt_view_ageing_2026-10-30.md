# Debate round 33: ageing, should ACL people live longer? (30 October 2026)

**GPT's and Gemini's opinions, not sign-off.** The creator's idea: "humans used to live longer before and i think we
should do same with acl", then "we are not gonna make grow their ages unrealisticly but slightly", then "just discuss
with gpt and gemini and solve this aging problem" (a delegation). The same text went to the main ChatGPT chat and the
ACL Gemini chat, then one debate round (33b).

## Facts put to both
- Evidence: no human is verified past 122; foragers' life expectancy at birth was about 21–37, mostly from child deaths,
  but adults often lived into their 60s–70s (Gurven & Kaplan 2007; SA1 evidence note).
- ACL's ageing: weekly death risk `1.5e-5 × exp(0.0866 × age)`; the rate (doubling every 8.0 years) matches the forager
  average (8.1), but the scale is 5.3 times the forager average a3 = 1.47 × 10⁻⁴ a year (SA1 note), as if every person
  were 19 years older. Maximum health also falls 1.5 a year after 50 (floor 30); elders' illness chance is doubled.
- **Measured today** (`docs/research/acl_lifespan_v9_2026-10-30.md`, 6 throwaway v9 worlds, a cohort of 1,314 followed
  to death): life expectancy at birth 33.4; adults die at mean 42.0; 11% of adult deaths at 60+, 1% at 70+; death rates
  0.032 (ages 30–45), 0.081 (45–60), 0.219 (60–70) against the forager total of about 0.018 at 40 and 0.039 at 60.
- LS2: 98% of knowledge copies and kinds are lost at death.
- Two anchored options for `mortality_base` (the rate unchanged): **A**, the forager average (1.47 × 10⁻⁴ ÷ 52 ≈
  2.83 × 10⁻⁶ a week); **B**, a smaller step matched to the !Kung at age 40 (1.5 × 10⁻⁵ × 0.0072 ÷ 0.0249 ≈
  4.34 × 10⁻⁶ a week).

## Round 33: first answers
| question | GPT | Gemini |
|---|---|---|
| A or B | **B**: a conservative first correction anchored to an observed population; disagrees that humans used to live longer (life expectancy at birth was low; surviving adults reached their 60s–70s) | **A**: B "picks the harshest outlier ... cherry-picking"; the cross-cultural mean is the honest anchor |
| other ageing routes | leave unchanged; test separately later | leave both alone (they reflect real senescence) |
| primary | **calibration**: adult mortality closer to the reference across several age bands, not only age 40; no major harm; knowledge reported, **not required** | **knowledge**: inheritance up by ≥ 0.10 and late skill up by ≥ 0.02, with no collapse flags |
| years, seeds | 1,000 years, 32 paired seeds, 200-year checkpoints | 1,000 years, 32 paired seeds |
| risks | more food demand, crowding, competition; fewer chances for the young; ageing-only predictions are not whole-world survival; other ageing routes may still cut lives short | elders drag on food in hard seasons; overshoot of carrying capacity; flags at more extinctions than v9 or late population below 0.85× or above 1.8× v9 |
| estimate | 85% | 90% |
| adoption | should rest on physical plausibility and demographic safety, **not** on whether it helps Bob | (knowledge-based rule) |

## Council: checked
- **GPT's principle is ACL's rule.** Adopting an anchored value because it helps knowledge would be tuning towards an
  outcome. Knowledge stays a described secondary; Gemini's thresholds (+0.10, +0.02) are invented numbers.
- **Gemini is right about B.** B was the assistant's own construction (one group matched at one age, with ACL's rate),
  so it is a weaker anchor than the average. Gemini's "kills 89% of adults before 60" matches the measurement (11% of
  adult deaths at 60+).
- **Proposal put to both (33b):** run both A and B, with v9 and the sham, on 20 paired seeds × 1,000 years (4 worlds per
  cloud job, so no job reaches the time limit). Primary: a calibration distance over three age bands against the
  forager reference `h(x) = 0.013 + 1.47e-4 × exp(0.086 x)` (it reproduces the SA1 note's 0.018 at 40 and 0.039 at 60).

## Round 33b
- **GPT: accept, with three changes** (90%): (1) run both A and B; Gemini is right that B's single-age anchor is weaker;
  (2) calibrate with age-specific deaths divided by age-specific person-years at risk, freeze the reference and the band
  weights, report paired uncertainty; (3) treat 20 seeds as exploratory: three more extinct worlds is a safety warning,
  not strong evidence; **require a larger confirmatory run before adopting either arm**. Choose by calibration, not by
  which arm produces more skill.
- **Gemini: accept** (running both "cleanly resolves the debate"). One refinement: the reference is a total hazard, so
  ACL's rates must be all-cause (ageing plus starvation, thirst and illness), so A is not over-penalised.

## Decided (the assistant, under the creator's delegation and sleep-mode autonomy; estimate 80%)
AG1, a frozen four-arm calibration study (`experiments/AG1_ageing_anchor/questions.md`), with all three changes and the
refinement adopted: all-cause, age-specific rates per person-year at risk; reference and equal band weights frozen;
paired world bootstrap; exploratory on 20 seeds; adoption needs a confirmatory run and the creator's decision.
