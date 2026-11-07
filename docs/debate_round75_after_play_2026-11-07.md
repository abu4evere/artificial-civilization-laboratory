# Council round 75: what play mode showed, and what to test first (7 November 2026)

The question and the follow-up: `docs/debate_round75_question_2026-11-07.md`. Source: `experiments/PLAY1_inside_acl/journal.md`
(the creator's one-off play-mode exception; not a study, not data). GPT (main chat), Gemini and DeepSeek got the same
text. **Each answer is that model's opinion, not sign-off.** Claude was the council: each claim was checked against the
v15 code, and the facts were sent back to all three in a follow-up.

## First answers

**GPT's opinion, not sign-off.**
- Verdict: "Investigate the energy gate first. Fix the theft-target bug independently. Do not treat the play session as
  experimental evidence."
- Classification:
  - the energy gate is calibration or a possible structural fault;
  - one parent cannot feed a family: calibration;
  - no way to seek a partner or ask for help: missing general abilities;
  - theft from children: a fault (verify the intended rule);
  - no revenge: potentially fine;
  - choosing the lesson or the item: missing agency;
  - pots: a missing material affordance;
  - food dominance: diagnostic.
- First study: **EG1**, a frozen read-only audit of energy-blocked forage and hunt options on v15. It would cover:
  - energy before and after acts;
  - starving weeks where only energy stood between a person and food;
  - age and sex;
  - available, offered, chosen and completed.
- "Do not lower costs or increase recovery yet."
- Estimates: 97% valid; 75% that energy is a substantial contributor.

**Gemini's opinion, not sign-off.**
- Faults: theft from children (5) and pots (8), to be fixed at once in code.
- Missing laws: seeking a person (3), asking for help (4), and choosing what to give or teach (7).
- Calibration: energy (1) and family margin (2).
- Fine as they are: no revenge (6) and thin margins (9).
- First: merge energy and margins into HR1.
- The weekly gate is "an artifact of the time step, not a reasonable model of empirical fatigue".
- Estimate: 95%.

**DeepSeek's opinion, not sign-off.**
- Faults:
  - theft from children (5), as a fault fix with a harm check (FF4);
  - seeking a partner (3) partly: if `join` cannot target a specific person, that is a targeting fault.
- Missing laws: asking (4), choosing what (7) and keeping food in containers (8); no revenge (6) is a weaker law gap.
- Calibration: energy (1), family margin (2) and thin margins (9).
- First: **EN1**, a read-only audit of inactive weeks (energy-gated vs chosen rest), with FF4 in parallel.
- "The energy gate is a defensible fatigue model, but the granularity is what binds": forage is a whole week's act.
  Don't fix it by tuning energy alone.
- Estimates: EN1 about 88%; FF4 about 92%.

## What the code says (Claude's checks, v15 = live)

**(a) Theft from children is not a plain fault.**
- The steal rule dates from the first commit (`87a46dcc`). Its comment reads "Steal: hunger, without kindness or love
  to hold you back" (`mind.py`).
- The `st != "child"` check gates the **actor**, as `attack` and `flee` also do.
- Victims are filtered only by these conditions:
  - they hold over 4 food;
  - they are not kin (kin < 0.5);
  - they are not the partner.
- The thief's kindness, affection and fear of the victim lower the score.
- No record says children were meant to be off-limits. A ban would write a moral norm into nature.
- ACL's fault rule ("a rule that does not do what its own comment or plan says") does not apply.

**(b) Pots: the play journal's limit 12 was overstated.**
- `carry_capacity` = `carry_limit` (100) × (1 + contain), so a pot of contain 60 lets one carry 160.
- Loose food rots 4% a week (`spoil_rate`), a quarter as fast near smoke (`smoke_keep`).
- A pot does not slow rot, so storage is not what binds a lone parent; production is.
- A correction was appended to the journal.

**(c) Energy.**
- The cap is 100.
- Recovery is 25 a week × (1 − 0.5 × deficit), so 12.5 when wholly short (`biology.py`). A rest week adds 40
  (`actions._rest`).
- Forage costs 25 + 4 a tile. Walks to far water cost more (`weather.py`).
- So foraging on one's own tile every week is break-even when fed.
- Found while checking, a quirk: `decide` picks the **single best** forage tile ignoring energy, and `add` then drops
  forage entirely if that tile is unaffordable. A tired person can thus lose the forage option even when a nearer tile
  with food was affordable. Is it a fault? Not by its comment (none). EG1 should measure it.
- Gemini's "a starving person is locked out while they starve to death" is overstated: one rest week from 0 gives
  12.5 + 40 = 52.5, enough to forage. The lock is a delay of about a week, not a trap. Whether that week kills is for
  EG1 to measure.

## After the facts (follow-up answers)

**GPT's opinion, not sign-off.**
- (a) "Revised verdict: Leave unchanged. My earlier fault classification was incorrect."
- (b) Correction accepted: "No demonstrated missing storage law".
- (c) It keeps EG1, but narrows its hypothesis: "the interaction of travel, starvation, and energy-gated food
  acquisition, not routine foraging".
- Primary outcome: starving person-weeks with feasible food acquisition blocked solely by energy, ÷ all starving
  person-weeks. Feasibility is judged by the existing action rules, energy aside.
- Secondaries: age-sex breakdowns, travel costs, energy trajectories.
- Confidence: 96% that EG1 is valid and informative. About 60% that energy-only blocking explains a substantial share of
  starving weeks (down from 75%).

**Gemini's opinion, not sign-off.**
- It agrees (a) is not a fault: "enforcing a 'do not rob children' shield would artificially write a moral norm into
  the physics engine".
- It revises (b): "storage is working as intended".
- It still wants the energy audit first. Its primary is "starvation-locked weeks": the share of weeks where an agent is
  starving and the forage option is dropped only because energy is too low.

**DeepSeek's opinion, not sign-off.**
- (a) "Agree — not a fault … Drop FF4."
- (b) "point 8 was overstated, withdrawn". Food preservation (rot slowed by a pot) is a possible later law, not urgent.
- (c) "still EN1 first — with a narrower primary": the share of starving adult-weeks in which forage and hunt were both
  energy-blocked, by age band and sex.
- Secondaries:
  - the same share in non-starving weeks;
  - the inactive-week split (energy-gated vs chosen rest).
- Estimate: about 87%.

## What survived
- All three withdrew the theft fault and the pot point once shown the code.
- All three still put the **energy audit first**, read-only, with no cost or recovery change before it.
- They converge on one primary: **among starving person-weeks, the share in which getting food (forage, and hunt for the
  grown) was feasible but blocked by energy alone.**
- Kept as secondaries:
  - DeepSeek's non-starving weeks and inactive-week split;
  - GPT's age-sex and travel;
  - the best-tile quirk found here.
- Seeking a specific person and asking for help stay on the list of missing general abilities (law candidates), not
  faults. `join` does pull toward loved ones by last-seen place (NV2); play saw her own mind find her partner.
- **Decision (the assistant, under the creator's standing permissions, "you can keep going do not rely on me"):** freeze
  EG1 as a read-only audit on v15. The estimate that it is valid and informative is 90%.
