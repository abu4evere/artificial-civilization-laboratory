# Debate round 18 (28 October 2026, sleep mode): after IC1, what should the first signal law be about? (opinions, not sign-off)

**The same text to GPT (main chat) and Gemini (ACL session); Claude as council.** IC1 (final): telling where water is
does no real work (11 of 240,709 accepted places new; 0.997 told while the listener already saw water; never a thirst
target), but moments of shared attention at water are common (0.989 of talks; 4.04 per adult-year; 0.870 in repeated
pairs; about 11 water tiles and 4.7 animal groups in view). **Code fact (checked):** `mind._nearest_spring` uses told
water only when a person knows no water of their own, which almost never happens. The creator's rule stands: no map, no
coordinates, no built-in meanings.

**Claude's view put to both:** a "water here" signal would rarely tell anyone anything, and replacing a channel nobody
uses cannot show usefulness. An alternative: tokens become **names for particular places**, learned only when two
people are together there; hearing a token later calls up the listener's own memory of that place (no coordinates
sent; the listener must have been there).

Questions: (1) is water still the right first referent? (2) are learned place names fair under the no-map rule? (3) how
to test usefulness without tuning water? (4) the next step, with an estimated chance.

## Answers
- **GPT:**
  1. "Don't make water-location communication the first language law. IC1 shows abundant opportunities to learn
     signals, but almost no need to use them." Water is good for studying shared meaning, poor for testing usefulness.
     Audit game and danger next; "don't assume either is better without evidence."
  2. **Place names are fair, with a condition:** a token may call up a place the listener personally experienced. "That's
     not a hidden map, provided no coordinates, location identity, or meaning are transferred invisibly."
  3. Rare situations may be studied, reporting both conditional success (does it help when information is truly
     missing?) and how often such situations occur. "Don't change water availability to manufacture demand."
  4. **A short read-only referent-opportunity audit** comparing water, game and danger: shared attention, repeated
     encounters, private knowledge, and moments where a signal could change a listener's decision. Then freeze one
     signal law "based on those measurements, not on which referent seems most likely to produce language." **90%.**
- **Gemini:**
  1. **Pivot to game.** Water has near-zero information asymmetry; game moves, is out of sight, and pays when reported.
  2. **Place names are fair**, "provided no coordinates cross the wire": a token resolving to the listener's own
     memory is ordinary episodic memory.
  3. Changing water to force demand is "textbook nature-tuning". Test usefulness in natural stress (dry seasons) or on
     game, where asymmetry occurs naturally.
  4. **A read-only game information-asymmetry audit** on v8: how often a listener lacks game knowledge while a nearby
     peer sees a herd; clutter and repeated pairs for animal sightings. **90%.**

## Council (checked against the code)
- **Agreed by all three:** water is not the right referent for showing usefulness; learned place names are fair under
  the no-map rule if only the listener's own memory is called up; no tuning of water.
- **Checked: game has real use today, unlike water.** A told game place enters the listener's options twice
  (`mind.py`): as a tile worth a look when within reach, and, when hunger > 0.3, as a reason to walk 1–3 reaches to it.
  So the audit can measure decision change for game, which it could not for water.
- **Checked: danger exists but has no channel.** Wolves and bears maul people (`fauna.py`, `mauled` events); nothing is
  said about them in talk. So danger can be audited for opportunity (who saw it, who did not, who was later hurt) but
  not for current use.
- **GPT's three-referent audit is adopted over Gemini's game-only one:** it costs little more and avoids assuming game
  wins.
- **Corrected (again):** Gemini calls the runs "deterministic replays". They are new worlds with a read-only observer;
  the zero checks show the observer changes nothing.

**Next:** draft IC2, the referent-opportunity audit (read-only on v8), review it with both, then freeze in sleep mode
if the estimate is 40% or more. Any signal law itself stays the creator's decision.

# Debate round 19 (28 October 2026, sleep mode): the IC2 draft

**The same text to both.** The draft IC2 (read-only referent-opportunity audit; water, game, danger).
- **GPT: yes, 85%.** Fix the gap definitions (the listener must truly lack the information; the water gap needs a
  particular place; a wolf the listener cannot see matters only if it can reach them). Danger relevance by a frozen
  physical rule, not by a later mauling. Check that 3 reaches is today's behaviour. Keep the ranking descriptive and
  report how many gaps are actionable. Distinguish choosing a destination from reaching it.
- **Gemini: yes, 95%.** Add sighting age bands (0–4, 5–8, 9–12 weeks) and danger near misses (within 2 tiles within
  2 weeks).
- **Council:** all points adopted except one met another way (groups are not remembered by identity, so "knows that
  group" is checked at the spot level). 3 reaches checked in `mind.py`. **Corrected:** Gemini again offered to draft a
  game-signal pre-registration; that is premature until IC2 is read, and the law is the creator's.
