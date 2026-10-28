# IC2 — Where is there a real information gap: water, game or danger? (frozen plan)

**Read-only on nature v8. No change to nature.** Chosen in debate round 18 (`docs/debate_after_ic1_2026-10-28.md`):
GPT's referent-opportunity audit (water, game, danger), which covers Gemini's game-only audit. Chosen in sleep mode
(`docs/autonomous_decisions.md`, 28 October 2026).

**Why.** IC1 showed that people often attend to the same water together, but that water information is almost never
needed: listeners nearly always see or know water already, and told water is used only by someone who knows none.
A signal law can only show usefulness where **one person knows something another lacks and needs**. Before any signal
law (the creator's decision; no map, no coordinates, no built-in meanings), this audit measures, for each of three
referents that exist in v8, how often:
1. two people attend to the same instance together (where a signal could be learned);
2. one knows of an instance the other neither sees nor knows (an information gap);
3. the gap is decision-relevant: the other is in a state where today's mind would act on it.

## Design (32 worlds, seeds 19801–19832; LP: 80 founders, 80×80; 200 years; `code_v8` = live nature; one arm)

**The observer only reads.** Wrappers call the original unchanged and note the state at that moment:
- the talk action (`actions.HANDLERS["talk"]`): the start of each talk, with both people's state;
- `information.hear_place`: each game or water place accepted;
- `actions.perform`: each chosen option, to see whether its destination is a told game place;
- `fauna._go_for_people`: which animal group mauled whom (by comparing health before and after; draws nothing).

**Definitions (fixed now).** "Sees" = within `perception` (4 tiles; the law's own square). Adult = 16 or older.
- **Game:** prey groups other than fish, with animals in them (as `_look_for_water` remembers them). A person
  **knows** a game spot if it is among their own sightings no older than 12 weeks, or among the game places they were
  told.
- **Water:** fresh-water tiles (as IC1). A person knows water if they see fresh water or have any spring of their own.
- **Danger:** wolf and bear groups with animals in them. Nobody remembers or tells them today; a person knows of one
  only by seeing it.

For each talk, both directions are looked at (each person as the one who knows, the other as the one who lacks).

## Questions

- **Q1. Shared attention, per referent:** talks in which both people see the same instance (the same fresh tile; the
  same game group; the same danger group). Per adult-year (both adults), the share in pairs with at least 5 such
  moments, and clutter (how many instances of that referent both see).
- **Q2. Information gaps, per referent** (per adult-year, adult listeners):
  - **game gap:** one has their own game sighting no older than 12 weeks, and the other neither sees any game group
    nor knows that spot;
  - **water gap:** one has a spring of their own that the other does not have, and the other sees no fresh water
    (GPT: the gap must contain a particular place to pass on);
  - **danger gap:** one sees a danger group that the other does not see.
- **Q3. Decision-relevant gaps** (the primary), per adult-year:
  - **game:** a game gap where the listener's hunger is above 0.3 and the spot is within 3 reaches (today's mind
    walks to a told game place under exactly these conditions);
  - **water:** a water gap where the listener has no spring of their own (today's mind uses told water only then);
  - **danger:** a danger gap where the group is within 3 reaches of the listener (the same walking range as game; a
    frozen physical rule for "could plausibly threaten", as GPT advised; a later mauling is an outcome, not the test).
  - Beside each count, the **share of that referent's gaps that are decision-relevant** (GPT).
- **Q4. Today's game channel** (described; it is the channel a game-signal law would replace):
  - accepted game places per 1,000 person-years, and the share later chosen as a destination by that listener, overall
    and for spots the listener could not see at the telling. "Chosen" mirrors the mind's two uses exactly: an option
    whose target is the told spot (within one reach), or a `join` whose target is the step toward it
    (`world.step_toward_land`, 1–3 reaches). Another reason can pick the same tile, so this is an upper bound;
  - **chosen against reached** (GPT): whether, after the move, the person stands on the spot, and whether they then see
    a game group;
  - the share of all chosen options that go to a told game place;
  - **the age of the sighting** in game gaps and game tellings: 0–4, 5–8, 9–12 weeks (Gemini: old spots may be cold).
- **Q5. Danger outcomes** (described): maulings per 1,000 person-years; the share of maulings in which the victim, in
  the 4 weeks before, was the listener in a danger gap about the same group; and **near misses** (Gemini): the share of
  decision-relevant danger gaps after which the listener comes within 2 tiles of that group within 2 weeks.

## Frozen ranking and branches (descriptive, for the creator's signal-law decision; none changes nature)

- **The rule is a screen, not a law of language** (GPT): counts and shares are reported in full for every referent.
- **A referent is workable** if its shared-attention moments are ≥ 1 per adult-year with ≥ 25% in repeated pairs (IC1's
  B2 rule), **and** its decision-relevant gaps are ≥ 1 per adult-year.
- **The proposed first referent** is the workable referent with the most decision-relevant gaps per adult-year.
- **If none is workable:** ACL today has no referent where a learned signal could both be grounded and be useful; the
  next question is the creator's (which law change would create a real need, judged against human evidence, not
  tuned).
- **If game is proposed:** a game-signal study must carry a flag on hunting and food, because today's game telling
  (Q4) does real work and would be replaced.

## The assistant's prior
1. Game gaps are common and decision-relevant (several per adult-year); game is workable and proposed.
2. Water's decision-relevant gaps are near 0 (IC1).
3. Danger gaps are rare and almost never followed by a mauling from the same group (danger not workable).
4. Today's told game places are used: more than 5% of accepted game places later become a destination.

## Validity (hard stops)
- **Zero checks:**
  - the observer and wrappers are read-only: state and random numbers identical with and without them, at 20 and 60
    years (seeds 501 and 601);
  - reload is exact;
  - the wrappers' counts match the law's own events: talks = `talk` events; accepted game places = `learn` events with
    a `g:` spot; maulings seen by the wrapper = `mauled` events.
- All 32 worlds are present under one fingerprint (`code_v8`).
- An independent recompute by GPT and Gemini (fresh chats, raw per-world counts) of the Q1 and Q3 numbers before the
  findings are final.

## Review (debate round 19, `docs/debate_after_ic1_2026-10-28.md`)
- **GPT: yes, 85%.** Adopted: the water gap needs a particular spring the other lacks; danger relevance by a frozen
  physical rule (within 3 reaches), with maulings as an outcome; checked that 3 reaches is today's behaviour (it is:
  `mind.py` walks to a told game place 1–3 reaches away when hunger > 0.3); report shares of actionable gaps; chosen
  against reached. Its point that a game gap should exclude a listener who knows that group by another route is met at
  the spot level (the listener neither sees any game group nor knows that spot); groups are not remembered by identity.
- **Gemini: yes, 95%.** Adopted: sighting age bands; near misses for danger.

## Sign-off (28 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). GPT estimates 85% and Gemini 95%; the
assistant's estimate is 75% (the decision-relevance rules are new and the `perform` attribution is an upper bound).
Logged in `docs/autonomous_decisions.md`. Read-only: no change to nature. Any signal law stays the creator's decision.

## Operational note 1 (28 October 2026, after freezing, before any data)

How the code (`run_ic2.py`, `analyse_ic2.py`) reads the text where it left a choice, found in two 20-year smoke worlds
(seeds 9950 and 9951; not data). Nothing in the plan, its thresholds or its rules was changed after the smoke worlds.
1. **A talk** is noted by wrapping the talk action, which runs only once the two people are within 1 tile of each
   other (as IC1). So both people see almost the same square, and a danger group one sees and the other does not is
   rare by construction. This is part of the answer, not a fault: it says when talk could carry danger.
2. **The listener's hunger** is computed as the mind computes it before choosing (`hunger_of` with dependants' need),
   at the start of the talk.
3. **A game gap** counts once per talk direction, however many spots qualify. Its age band is that of the freshest
   qualifying sighting. Decision-relevant if any qualifying spot is within 3 reaches and hunger > 0.3.
4. **A danger gap** records, for each group the listener does not see, the last week of such a gap (for Q5's maulings);
   decision-relevant gaps (group within 3 reaches) are followed for near misses for 2 weeks, checked once a week at the
   end of the week.
5. **"Chosen as a destination"** (Q4) is checked before the move, on the person's place at the moment of choosing;
   "reached" means standing on the option's target tile after the move; "sees game" means a game group within
   perception after the move. Every chosen option counts in the denominator.
6. **Pairs** (Q1's repeated-pair share) count all ages, as in IC1; shared moments per adult-year count talks between
   two adults.
7. **Maulings** are seen by wrapping `fauna._go_for_people` and comparing the health of the people within 1 tile before
   and after; the count must equal the `mauled` events.
8. The zero checks passed locally (`zero_local.log`): identical state and random numbers with and without the observer
   at 20 and 60 years; reload exact; wrapper counts equal the law's events; fingerprint fedbb8d4.

## Operational amendment 1 (28 October 2026, after the first cloud run, before any outcome was read)

**What happened.** The first cloud run (40653330784, 32 worlds) failed a hard stop: in 15 worlds the maulings the
observer counted were fewer than the law's `mauled` events. Nothing beyond the validity block was read: `results.md`
for that run says only "NOT VALID: no reading is drawn" (kept as `results_run1_invalid.md`; the outputs are kept
locally as `output_run1_invalid/`, not deleted). The per-world listing used to find the cause showed only the mauling,
talk and accepted-game counts, which are validity counts.

**Why.** v8 has **two** routes to a mauling: a hungry wolf or bear going for people (`fauna._go_for_people`, the one
the plan named) and a bear **surprised** by someone foraging or hunting on its tile (`fauna.surprised`). The observer
wrapped only the first. The local zero checks passed because no surprised-bear mauling happened in those two worlds
(seed 501: 1 mauling; seed 601: 2; both by the first route). The hard stop worked as intended.

**The amendment.** The observer also wraps `fauna.surprised` in the same read-only way (health before and after; it
draws nothing). For such a mauling the possible groups are the bear groups on that tile, and Q5's "same group" check
counts a prior danger gap about any of them. Maulings are also counted by route (hungry / surprised). Nothing else
changes: same seeds, same definitions, same thresholds. The zero checks are re-run, and the 32 worlds are run again on
GitHub. The seeds stay the same because no outcome was read; the worlds are new worlds with a read-only observer, so
the same seeds give the same worlds.

**Decided by** the assistant, under the creator's sleep-mode autonomy (a technical fix of a read-only observer; no
change to nature or to any reading rule).

**Check of the amendment (before the re-run):** the zero checks pass again (`zero_local.log`). They cannot exercise the
new route (no surprised-bear mauling happens in seeds 501 and 601), so the amended observer was also run on seed 19806
(one of the 15 failing worlds) for 200 years: maulings counted 3 = `mauled` events 3 (all by surprised bears), no
mismatch. Only these validity counts were looked at.
