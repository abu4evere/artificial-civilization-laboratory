# SP1: where does the spreading of new kinds stop? (frozen plan)

**A read-only study on nature v15.** The creator asked whether missing language is why knowledge does not spread
(Telegram, 6 November 2026, 23:28). The code check that night showed that a lesson already passes a recipe from mind
to mind with no words (`information.show_how`, `hear_how`; `knowhow.watch`). Yet council round 71 recorded **0
non-inventor makes in about 11,500 new kinds** (`docs/debate_round71_adoption_v15_2026-11-06.md`). SP1 follows every
new kind through each step of spreading, to find the step where it stops. **SP1 decides no law.** It points at
the step a later frozen study could test.

Earlier studies LS1 and LS2 (nature v7 and v9) asked where knowledge goes, but did not follow each new kind step
by step on today's nature.

## Design
- **Code:** `code_v15` (fingerprint 3d46cd2c…), unchanged. One arm, no sham. LP (80 founders, 80 × 80).
- **Seeds 24401–24432** (32 new seeds, used by no study). 200 years.
- **The kinds followed:** every new entry in the world's record of known kinds (`world.knowledge`) that first appears
  in **years 100–190**. Each is followed to year 200, so every kind has at least 10 years. Its **origin** is recorded:
  made (an invention by making or play), heated, or born from a copying error (taught, copied, read).
  **The main counts use invented kinds** (origin made or heated). Copy-error kinds are reported apart.
- **The inventor** is the person recorded as `first_by`.

## The observer (read-only)
It wraps, never changes, `information.show_how`, `information.hear_how` and `knowhow.can_follow`. It reads the week's
events, the decision log and people's state at each week's end. Every check it makes is a pure function of state,
with no random draws.

For each followed kind K:
1. **Teaching chances:** the times someone who knows K is the teacher in a lesson (`show_how`), split by inventor and
   others.
2. **Offered:** K is among the teacher's offers. These are the top 3 valued things with value > 0.15, recomputed by the
   code's own rule before the call.
3. **Shown:** K is the lesson picked (`hear_how` with meant = K, not a part lesson).
4. **The lesson's outcome**, read in `hear_how`:
   - the learner already knew it;
   - distrust: the learner tried it and found it bad;
   - declined: the trust × openness draw failed;
   - missing part: `can_follow` failed, and a part lesson may follow;
   - taken as meant;
   - taken with a copying error.
5. **Learned:** someone other than the inventor gains K (a `learn` event with thing = K), by route: taught, copied
   (watching), read, heated. A non-inventor who holds K with no `learn` event got it on their own ("own").
6. **Knower-weeks** of non-inventors who hold K: weeks with K's value > 0.05; weeks with the parts in hand
   (`mind.can_make`); weeks with "make K" among the top 4 options considered; weeks they chose to make K. The same is
   kept for the inventor, for comparison.
7. **Made by someone else:** a `make` event of K by someone other than the inventor, by route of how they got it.
8. **Lost:** the week no one alive knows K any more.

## The funnel (each kind counted once per stage)
- A. born (invented, years 100–190)
- B. offered at least once
- C. shown at least once
- D. learned by a non-inventor, through a lesson (D-taught) or by any route (D-any)
- E. a non-inventor who learned it had the parts in hand in some week
- F. made by a non-inventor who learned it

## Primary outcome
The conditional pass rate at each step: B|A, C|B, D-taught|C, E|D-any, F|E. Each is computed from pooled counts,
with a world bootstrap 95% interval (10,000 draws of 32 seeds). **The step where spreading stops** is the step with the
lowest conditional rate. If its interval overlaps the next lowest, both are named.

## Secondary
- The lesson outcome shares (item 4), for K shown.
- Where E fails: value > 0.05 weeks and can_make weeks, per knower-week.
- Copying by watching (D-copied | A) as a side route.
- Teaching chances that reach the inventor: the share of K whose inventor ever teaches while knowing K. The share
  whose inventor's value for K ever passes 0.15.
- How long K lives (to loss, or censored at year 200).
- All with populations: kinds, worlds, lessons, knower-weeks.

## Zero checks (hard stops)
1. **Read-only:** world and random-stream hashes with and without the observer (20 and 60 years).
2. **Offer replica:** in every top-level `hear_how`, the meant thing is in the observer's recomputed offers (0
   misses allowed).
3. **Event check:** every lesson the observer counts as taken matches one `learn` event (how = taught) in the same
   week, for the same learner and thing.
4. **Reload is exact.**
5. **All 32 worlds** are present under one fingerprint.

## A blind recompute
GPT, Gemini and DeepSeek, from a per-world count file built by a script written before data. They recompute the funnel
counts, the conditional rates and their intervals.

## Prior (the assistant, before data)
- **Offered (B|A) is the lowest step**, about 60%. A new kind rarely reaches a teacher's top 3 above 0.15.
- Next most likely: E|D (learners never get the parts), about 25%.
- About 15% for the other steps.
- F (made by a non-inventor who learned it) is near 0.

## Sign-off (7 November 2026)
The creator, by Telegram, confirmed by the listener's code (00:26): "Draft and freeze a read-only study on v15 that
follows each new kind through being shown, being learned, having the parts, and being made by someone else, to find
where spreading stops, then run it on the cloud." The design was not put to the council before the freeze. GPT, Gemini
and DeepSeek do the blind recompute. Frozen as `SP1-frozen` before any code or data.
