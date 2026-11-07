# Council round 70: HK1's design (who holds the kill) (6 November 2026, from 18:38)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round70_question_2026-11-06.md` (the same paragraph to all three).
- **The chats:** GPT, the main chat (the reply came on "Instant" thinking; the input box was cleared before
  inserting); Gemini, chat 87f468c684ee5839; DeepSeek, chat 2552dbba.
- **Recorded from the replies read in the chats.** DeepSeek's reply was read from screenshots, because the page
  blocked reading its text by script.

## Round 1
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| 1. who lands the kill | own skill × tool, weighted; freeze the formula and handle zero weights | own skill × tool ("an even draw ignores physical competence") | own skill × tool, normalised in the party, **drawn from a dedicated stream so the sham repeats the draw**; report who lands it by skill rank as the manipulation check |
| 2. meat past carry room | **keep the live rule (deleted) and measure it** as a critical diagnostic; a stash would confound ownership with storage; if much meat disappears, HK1 tests ownership plus destruction | **set it down as a stash**; one holder "guarantees massive overflow", and deleting it is an unphysical tax | **keep the live rule and report the loss**, now "first-order, not rounding". If a guard is raised, check first whether it is mechanical (meat deleted); if it is, the stash is the next study, not a rejection of HK |
| 3. the hunt's expectation | **keep the even-split one**: a change would be a second intervention; the mismatch is informative | **change it** to my landing chance × take; otherwise people are "deluded by obsolete code" | **keep it** in the main arms (equal to the true value when skills are equal; the skill range is narrow); HK+E as a described arm at most |
| 4. decision rule | the manipulation check plus the safety guards, with no outcome required. **Keep killing as a harm guard**; a new threshold would need independent justification, not "violence is expected". Report killings also as a share of deaths. Removing the limit and failing safety are separate conclusions | the manipulation check plus no harm. **Drop killing as a strict guard**: CI1's limit is "artificially peaceful" against the 4–28% evidence. Describe it, and flag it only above 28% of deaths | the manipulation check plus no harm, with no outcome ("requiring one is tuning"). Make the check concrete: party kills happen, and the logs show the drawn lander gets the meat. ("Inequality above the sham" is trivially true.) **Keep the killing guard and describe killings against the forager range**: "different purposes; both" |
| 5. measures to add | meat deleted, total and per hunt; hunger and starvation of hunters against non-hunters; successful thefts; chains of who got meat from whom; participation and party size; injuries and deaths among holders, failed hunters and others; inequality only over party kills of 2 or more; whether the weights predict the lander | rot at kill-site stashes; starvation inequality; the unsuccessful hunters' next action | meat lost to carry room; the holder's food against the others' after a kill; party size and composition (do the unskilled drop out?); returns per hunter-week by skill; gift recipients' kinship and past giving; theft aimed at holders; the same person landing again and again; total meat; trust and respect toward sharers. Solo hunts are unchanged, so the whole effect is in party hunts |
| 6. base nature | **wait for CI1-C** and use whatever is live at the freeze | wait (v15) | wait; freeze the plan with base = the nature live at the freeze. On v14, results would need confirming on v15 anyway |
| 7. estimate | **94%** valid and informative. The biggest worry is carry-room deletion | **95%** | **about 80%**. The risk is power: party kills may be too few. Count them in a smoke run before freezing |

## Checked (the assistant as council)
1. **Gemini's "massive overflow" is checked by measurement, not by argument.**
   - The largest single take is 55 meat. Carry room is 100 × the carry tool − food and seeds held.
   - A read-only measurement on three v14 worlds (seeds 9911–9913, 100 years each) records, at every successful hunt,
     the meat taken and each member's free room. From these come the loss under the even split, and the expected loss
     if one member drawn by own skill × tool held it all.
   - The script is `experiments/HK1_who_holds_the_kill/explore_overflow.py`.
   - **Result (18:59; read-only, exploratory):** successful hunts were 33, 39 and 33 per world over 100 years,
     with 336.5, 439.5 and 439.5 meat.
   - Meat lost at the carry limit was **0.0** in every world, under the even split and under a single holder.
     The smallest free carry room at any kill was 69.8, and the largest take was 55.
   - **Gemini's "massive overflow" does not happen in v14.** Keeping the live carry rule costs nothing.
2. **DeepSeek's power worry is worse than feared. There were no party successes at all: 0 of 105 kills in 300
   world-years.** Every kill was by a lone hunter, so the forced equal split never applied.
   - HK1 as designed would change nothing in v14, because it changes only party kills.
   - A second read-only count of every hunt attempt by party size (`explore_parties.py`, seeds 9911 and 9914)
     shows whether parties form and fail, or never form.

## Part 2 (sent about 19:1x; question in `docs/debate_round70b_question_2026-11-06.txt`; recorded 19:20)
The measured facts went to all three: no party kills, 1 pair in 713 hunt attempts, about one hunt per grown person
every 12-23 years, no meat lost at the carry limit, and no way to hunt together on purpose. DeepSeek's chat page froze
twice, so the question was re-sent in a reloaded tab of the same chat. Its reply was read from screenshots.

| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| 1. HK1 | **shelve** (99%); keep the design for later | **shelve**: a guaranteed null | **shelve, with a written revival condition**: party kills reach a countable base (at least 50 in the smoke worlds) |
| 2. order | **HR1**, then **acting together on purpose** (a general ability to join another's ongoing task, with visible intentions, coordination costs and freedom to refuse; not "hunt together"), then HK1 again; theft and taking may be studied on their own | **HR1 first**: cooperation and conflict both need a valuable, contested resource to exist | **HR1, then joint action, then the non-hunting hand limits**; an attack-gate study (winning moves no goods) could run alongside as a cheap read-only study |
| 3. calibration and "no tuning" | yes, with conditions: audit why F7 is unused; define what one ACL hunt is; convert units; freeze parameters from outside evidence before seeing outcomes; never tune the decision pulls afterwards to force hunting | yes: it corrects physics to evidence. **First it said adopt F7's table; after a fact check it revised:** "HR1 must discard the F7 table entirely", and build rates from the evidence after a frozen unit conversion | yes, under four conditions: the target is an external, pre-registered evidence quantity; one setting per arm; the unit conversion is frozen first ("that conversion is where tuning can hide"); and **F7's table is a calibration choice, not a fault** |
| 4. estimate | 96% that a read-only HR1 measurement and calibration is valid and informative; about 70% that an evidence-calibrated change makes hunting realistic without harm | 95% | about 78%; a calibrated hunt may still be rarely chosen (an informative null) |

### Checked (the assistant)
- **Gemini's first claim (F7's table is "empirically accurate") did not match the records.** The table's provenance
  is unknown (round 54), and the Hadza per-encounter rates read for HR1 are 7.3% for small game and under 5.3% for
  large. Gemini was told, and it revised.
- **DeepSeek named "CO2's built-in pull".** CO2 exists in the index (what makes the other options beat making, v9).
  Its relevance to hunting was not checked here.

### What survived
1. **HK1 is shelved,** with DeepSeek's revival condition. It was never frozen.
2. **Next on the laws road: HR1.** It calibrates hunting to forager evidence:
   - define one ACL hunt;
   - freeze the conversion of units (day, week, encounter) first;
   - drop F7's unused table and derive any per-species rate from the evidence;
   - one setting per arm;
   - harm guards as in CI1;
   - hunting participation and returns described against the evidence, never tuned afterwards.
3. **Then a general ability to act together on purpose,** then HK1's revival check, then the attack and taking gates.
