# PL1 — How much do ACL's children play, against forager children? (frozen plan)

**Read-only on nature v8. No change to nature.** Chosen in debate round 26 (`docs/debate_after_ic2_lr1_2026-10-28.md`)
as the safe step while the curiosity law waits for the creator: both models judged their own curiosity designs to hide
a strength scale; this audit looks for an evidence anchor first. GPT 90%, Gemini 95%.

**Why.** EX1 (final) showed that habit inflation is not caused by copying; the core is practice starvation: values rise
only with use, so whatever is done early wins, and making is rarely practised (HL1: 258 times fewer updates than
foraging). ACL already has an instinct for play (`mind.py`: score (0.04 + 0.3 × curiosity × (1 − hunger)), × 1.6 for
children, offered only when a person holds a material or an item), and play raises crafting skill (`actions._play`).
**Human anchor:** in 12 forager societies (Lew-Levy et al. 2022, *Scientific Reports*; 690 children aged 3–18; 85,597
observations), play is **9–58% of time at ages 3–6**, then declines with age; among Hadza and BaYaka (Lew-Levy et al.
2020, *Child Development*) it is 24.2% at ages 3–18.

## Design (32 worlds, seeds 20101–20132; LP: 80 founders, 80×80; 200 years; `code_v8` = live nature; one arm)

**The observer only reads.** Wrappers call the original unchanged:
- `thought.steer`: the options a person weighed this week (is `play` among them: **available**);
- `actions.perform`: the option chosen (**chosen**);
- `actions._gain_skill`: each gain in crafting skill, attributed to what the person was doing that week (`p.doing`:
  play, make, or other).

Age bands (completed years): **1–2, 3–6, 7–12, 13–18** (children under 1 are infants and do not choose).

## Questions (per age band; person-weeks; world bootstrap, 10,000 replicates)
- **Q1 (primary): play share** = weeks play was chosen ÷ weeks a choice was made.
- **Q2: availability vs choice** (GPT and Gemini): the share of weeks play was available; the share chosen when
  available. Among weeks without play, the share where play was **unavailable** (held nothing) vs **available but not
  chosen**.
- **Q3: where crafting skill comes from**: crafting skill gained in play, in making, otherwise; by band.
- **Q4: survivors (GPT):** Q1 again for children who lived through the whole band (alive at its upper age), so deaths
  do not distort the age trend.

## Frozen readings (descriptive; the human range is context, not an equivalence test: GPT)
- **Ages 3–6 against the human range:** "below" if the 95% upper bound of the play share is under 0.09; "within" if
  the interval lies inside 0.09–0.58; "above" if the lower bound is over 0.58; else "overlaps".
- **Decline with age:** whether the point shares fall from 3–6 to 7–12 to 13–18.
- **The bottleneck at ages 3–6:** "availability" if most weeks without play had no play available; otherwise
  "choice".
- **Caveat (both models):** ACL's people choose one action per week; human data are shares of daytime observations.
  The comparison is approximate. A share below the human range is a warning worth investigating, not proof that a
  curiosity law is needed.

## The assistant's prior
1. ACL children aged 3–6 play **below** the human range (well under 9% of weeks).
2. The bottleneck is **choice** more than availability (children often hold something).
3. Play declines with age.
4. Most of children's crafting skill comes from play, not making.

## Validity (hard stops)
- **Zero checks:** the observer and wrappers are read-only (state and random numbers identical with and without them,
  at 20 and 60 years, seeds 501 and 601); reload exact; wrapper counts match the law: chosen `play` weeks = the play
  handler's calls; chosen options = decisions made.
- All 32 worlds present under one fingerprint (`code_v8`).
- An independent recompute by GPT and Gemini (fresh chats, raw per-world counts) of Q1 and Q2 at ages 3–6.

## Sign-off (29 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). GPT 90%, Gemini 95%; the assistant's
estimate is 80%. Read-only: no change to nature. Logged in `docs/autonomous_decisions.md`.
