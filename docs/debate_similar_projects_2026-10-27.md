# Debate round 6 (27 October 2026): projects like ACL to learn from (opinions, not sign-off)

**The creator:** "is there other same type of projects that we can learn something from them … ask gpt and gemini too".
Claude gave a first list (Henrich 2004, Derex et al. 2013, Bhoopchand et al. 2023, Sugarscape, Artificial Anasazi,
Tierra and Avida, Polyworld and Creatures, OpenAI hide-and-seek, XLand, LLM-agent worlds). The same question went to
GPT and Gemini, with Claude as the council. **Sources are as given by the models; to be checked before use.**

## GPT
**Top three:**
- Bhoopchand et al. 2023 (*Nature Communications*, "Learning few-shot imitation as cultural transmission"): separate
  exposure, attention, imitation, retention and independent performance after the demonstrator leaves;
- Derex, Beugin, Godelle & Raymond 2013 (*Nature*, group size and cultural complexity);
- Sugarscape (Epstein & Axtell 1996) and Artificial Anasazi (Axtell, Epstein, Dean et al. 2002): validate simulated
  histories against independent observations, and tell a matched trajectory apart from a correct mechanism.

**Also:**
- Muthukrishna et al. 2014: who learns from whom matters as much as headcount;
- Kirby, Cornish & Smith 2008 (*PNAS*): transmission chains;
- Tierra/Avida (Ray about 1990–92; Ofria & Wilke 2004): lineage tracking and novelty measures, not to be equated with
  social learning;
- Polyworld and Creatures: for Bob's eventual mind;
- Baker et al. 2019 (hide-and-seek);
- XLand 2021 (held-out worlds, for a cross-nature Bob test);
- Generative Agents and Project Sid: borrow their logging and evaluation, never their pretrained knowledge;
- Caldwell & Millen 2008: a review of lab cumulative-culture experiments.

**Corrections to Claude:**
- **Population size is not a magic threshold.** Henrich's Tasmania case is disputed, and "there is no established rule
  that 80–130 individuals are too few". Distinguish the census population from the **effective cultural population**
  (who can actually exchange useful information). Derex & Boyd 2016: partially connected groups sometimes accumulated
  more. "I wouldn't increase founder counts to rescue culture."
- DeepMind's agents show imitation, not cumulative civilisation. The test ACL needs is "A invents → B learns → B
  improves → C learns the improvement".

**Lessons to act on:**
- measure the whole path from exposure to independent use;
- study effective connectivity: more people may just add more competing social options (MK1);
- demand inheritance **plus improvement**.

**Read-only tests:**
1. **an effective cultural network audit:** for each useful kind, how many non-knowers meet a living knower;
2. an opportunity-to-acquisition funnel;
3. a three-generation ratchet ledger.

GPT would pick the first.

**On Bob:** "A civilization capable of cumulative culture does not automatically produce an individually general
cognitive mind." ACL needs evidence of both individual cognition and collective accumulation.

## Gemini
**Added:**
- Bedau et al. 1998 (evolutionary activity statistics);
- Boyd & Richerson 1985 and Mesoudi 2011 (transmission biases);
- Laland, Odling-Smee & Feldman 2000 (niche construction: lasting artefacts change what the next generation is born
  into, so persistence and inheritance of things are niche construction).

**First lessons:** observational transmission (C1), physical niche construction (A2), and formal activity metrics.

**Read-only tests:** a Bedau activity audit on LS1, and a demographic threshold audit.

## Council checks
| claim | who | check | result |
|---|---|---|---|
| Social transmission of crafting between living people is 0% | Gemini | Recipes pass by teaching in talk; in LS1 about a quarter (early) to a half (late) of inherited recipes came by teaching. Zero is only for things and for watching making | **Withdrawn** |
| ACL's habit copying is unbiased | Gemini | `_imitate` copies only from a model the learner respects (≥ 0.2) or who seems better off (mood + 0.1), at a rate scaled by respect: already prestige- and success-biased | **Withdrawn** |
| 80–130 people may be too few (Claude's first list) | Claude | GPT: no established threshold; the Tasmanian case is disputed; effective connectivity matters more | **Claude's claim softened** |
| First read-only test: the Bedau audit | Gemini | Gemini adopted GPT's effective-network audit and funnel instead | **Revised** |

## Agreed
- **First read-only step:** an effective cultural network audit (who could have learned each useful kind from a living
  knower, and how far along the path from exposure to use each got).
- Treat material transmission (things) and knowledge transmission as separate.
- Require inheritance plus improvement (A→B→C) before calling anything cumulative.
- Import no other project's architecture into nature.
