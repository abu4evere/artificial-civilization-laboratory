# IMPLEMENTATION STATUS

Maps every World Bible law to what the current code actually does.
This document reflects the real code, not the design intent.

Statuses used:

- **IMPLEMENTED** — the law is present and behaves as written.
- **PARTIAL** — some aspects exist, some do not.
- **NOT_IMPLEMENTED** — no mechanism exists.
- **ASPIRATIONAL** — a design goal with no mechanism (later experiments).
- **DETECTED_ONLY** — the historian *observes* it, but there is no causal mechanic.

Code modules: `config.py`, `world.py`, `geo.py`, `fauna.py`, `weather.py`,
`person.py`, `mind.py`, `thought.py`, `inquiry.py`, `information.py`, `marks.py`,
`actions.py`, `matter.py`, `biology.py`, `social.py`, `knowhow.py`,
`historian.py`, `decision.py`, `experiment.py`, `mindview.py`, `viewer.py`.

Last checked against the code: 2026-10-03.

**World Bible v8.1 (2026-10-03).** The creator's v8.1 draft gives each law its own number for the first time
(v7 grouped Laws 29–43 in ranges), so Laws 35–43 below are numbered differently from v8.1 (v8.1: 35 Reputation,
36 Norms, 37 Institutions, 38 Diversity, 39 Civilization, 40 Cultural Detection, 41 Cultural Impact,
42 Open-Endedness, 43 Final Principle of Culture). The current per-law status, in v8.1 numbering and in the
creator's notation (Implemented / Partial / Future mechanism / Example only), is `bible/law_status_v81.py`,
and it is printed under every law in
`bible/THE_ARTIFICIAL_CIVILIZATION_World_Bible_v8_1_EXPANDED_DRAFT_with_status.docx`
(built by `bible/build_v81_status.py`). Where the two differ, `law_status_v81.py` is newer. Under v8.1's wording:
Law 97 counts as Partial (hunting together catches more than hunting alone), and Laws 33 and 53 count as Partial
(skills are tracked and differ). The tables below will be redone in v8.1 numbering after E5.

---

## Chapter 1 — The Universal Laws (Reality)

| Law | Status | Module | Evidence / Notes |
|---|---|---|---|
| 1 Time exists | IMPLEMENTED | `config.py` | 1 tick = 1 week; 52 weeks = 1 year; default 15 real min = 1 day |
| 2 Time irreversible | IMPLEMENTED | `world.py` | events permanent; memory fades but history (chronicle) persists |
| 3 Space exists | IMPLEMENTED | `world.py` | tiles, toroidal distance; moving goes tile by tile and water stops anyone without something that floats; travel costs energy and carries risk |
| 4 Objects have state | IMPLEMENTED | `matter.py`, `world.py` | materials/items carry properties; tiles carry piles/fire/stash |
| 5 Energy is limited | IMPLEMENTED | `actions.py` | every action has `COST`; rest recovers |
| 6 World produces resources | IMPLEMENTED | `world.py`, `geo.py` | plants/wood/stone/flint/fiber regrow by biome |
| 7 Resources scarce | IMPLEMENTED | `config.py`, `geo.py` | caps, regrow rates, oceans, islands |
| 8 Nature changes | IMPLEMENTED | `world.py`, `weather.py` | seasons, wet and dry years, weekly rain, droughts, storms, floods, hard winters, place-based temperature, lightning, rot; disease does not spread between people |
| 9 Food chains exist | IMPLEMENTED | `fauna.py` | rabbit→deer→bison grazed by wolf/bear; fish; animal attacks |
| 10 Environment indifferent | IMPLEMENTED | — | no "main character", no protection logic |
| 11 Every agent an individual | IMPLEMENTED | `person.py` | name/genes/history; two agents never identical |
| 12 Limited knowledge | IMPLEMENTED | `person.py` | all knowledge local to the agent |
| 13 Perception imperfect | PARTIAL | `mind.py`, `information.py`, `marks.py` | radius-limited sight; traces of what others did can be seen; memories are misremembered when retold; marks can mislead; **no deliberate deception** |
| 14 Needs | PARTIAL | `biology.py`, `weather.py`, `thought.py` | hunger ✓ thirst ✓ cold/shelter ✓ health ✓ social/loneliness ✓ reproduction ✓ curiosity ✓ safety (fear of people and animals) ✓; **sleep ✗** (only a rest action), **autonomy ✗** |
| 15 Drives | PARTIAL | `person.py` | 8 temperament traits map to drives; status/reputation ✗ |

---

## Chapter 2 — Emergence, Culture, Knowledge, Civilization

| Law | Status | Module | Evidence / Notes |
|---|---|---|---|
| 21 Emergence | IMPLEMENTED | — | no scripted civ; everything from rules + agents |
| 22 Shared meaning | PARTIAL | `marks.py`, `historian.py` | marks start meaningless; each person links shapes with what they notice around them, counted only when a shape predicts a thing better than its usual presence; the historian reports a symbol when 3+ people share the link for 2 years. **Speech is still our English rendering, not their language** |
| 23 Symbol evolution | PARTIAL | `marks.py`, `historian.py` | copied shapes change by slips; what a shape goes with can drift and the historian records it; marks only |
| 24 False beliefs | IMPLEMENTED | `knowhow.py` | superstitions form; beliefs can be wrong |
| 25 Rumors | PARTIAL | `information.py` | stories spread unverified and change in the retelling (wrong actor, place, size); **no deliberate lying** |
| 26 Myths & legends | IMPLEMENTED | `information.py`, `historian.py` | stories outlive events, drift, and are acted on (grudges against the wrong person); the historian writes down false versions 3+ living people share |
| 27 Cultural inheritance | PARTIAL | `knowhow.py`, `social.py` | teaching + stories + habits; no symbols/traditions |
| 28 Goal generation | PARTIAL | `inquiry.py`, `thought.py` | surprises become puzzles that pull people back to a particular thing they found; the kinds of pull are still a fixed list |
| 29 Invention | IMPLEMENTED | `matter.py`, `actions.py` | play/make → property-based configurations |
| 30 Reusable behaviors/scripts | PARTIAL | `biology.py` | habits (Q-table) are reusable behaviors; not "scripts" |
| 31 Technology | IMPLEMENTED | `matter.py` | problem→experiment→discovery→adoption chain |
| 32 Surplus | PARTIAL | `actions.py` | food stashes exist; no surplus→specialization |
| 33 Specialization | NOT_IMPLEMENTED | — | skills vary, no specialization mechanic |
| 34 Trade | PARTIAL | `social.py`, `historian.py` | exchange partnerships (give/return); no market/currency |
| 35 Trade emerges | PARTIAL | (same) | |
| 36 Reputation | PARTIAL | `information.py` | track records of whose word held, and reputation passed on by word; reputations for generosity or violence exist only as each person's own feelings |
| 37 Norms | NOT_IMPLEMENTED | — | no norm enforcement (only grudge/revenge) |
| 38 Institutions | NOT_IMPLEMENTED | — | |
| 39 Diversity | PARTIAL | `world.py` | islands/histories diverge; no anti-convergence rule |
| 40 Civilization | PARTIAL | — | accumulation/teaching ✓; institutions/norms ✗ |
| 41 Culture detection | PARTIAL | `historian.py` | detects bands/settlements/practices; not "culture" |
| 42 Culture changes behavior | PARTIAL | `knowhow.py` | beliefs change behavior (farming/storing); no full culture |
| 43 Open-endedness | IMPLEMENTED | — | seeded, deterministic, no predefined future |

---

## Chapter 3 — The Laws of Knowledge

| Law | Status | Module | Evidence / Notes |
|---|---|---|---|
| 44 Not innate | IMPLEMENTED | `person.py` | only instincts/temperament at birth |
| 45 Personal & local | IMPLEMENTED | `person.py` | recipes/beliefs/memories per-agent |
| 46 Knowledge has cost | IMPLEMENTED | `actions.py`, `config.py` | actions cost energy; learning has a rate |
| 47 Sources | IMPLEMENTED | `knowhow.py`, `information.py` | experience, experiment (play, puzzles), communication, inheritance (habits), inference, and observation of what others left behind (traces) |
| 48 Forms | PARTIAL | — | procedural ✓ declarative ✓ causal ✓ social ✓ symbolic (marks) partial; normative ✗ |
| 49 Can be wrong | IMPLEMENTED | `knowhow.py` | beliefs are interpretations, not truth |
| 50 Fragile | IMPLEMENTED | `knowhow.py`, `social.py` | `check_lost`, memory fade, death of last knower |
| 51 Imperfect transmission | IMPLEMENTED | `information.py`, `knowhow.py` | stories drift with fading memory and grudges; methods come across with a step wrong (less with demonstration and skill); beliefs slip a season or a thing; watching errs more than being shown |
| 52 Externalized | PARTIAL | `marks.py` | marks are durable and can come to mean what is done in a place; reading one gives a claim or an idea for a technique; single marks only |
| 53 Specialization | NOT_IMPLEMENTED | — | |
| 54 Meta-knowledge | PARTIAL | `information.py` | people keep track of whose word holds and pass it on; nothing about who knows which techniques |
| 55 Knowledge & power | NOT_IMPLEMENTED | — | no power system |
| 56 Verification & trust | IMPLEMENTED | `information.py`, `knowhow.py` | told claims are tested by experience and by checking reported places; each listener keeps a track record per source, which comes to outweigh goodwill |
| 57 Accumulation | PARTIAL | `knowhow.py` | accumulates via teaching; short horizon in E0 |
| 58 Knowledge frontier | IMPLEMENTED | `mind.py` | `can_make` requires existing parts |
| 59 Detection | PARTIAL | `historian.py` | `know_spread` metric |
| 60 Final law | IMPLEMENTED | — | philosophy honored by architecture |

---

## Chapter 4 — Discovery and Science

| Law | Status | Module | Evidence / Notes |
|---|---|---|---|
| 61 Belief ≠ knowledge | IMPLEMENTED | `person.py`, `knowhow.py` | claims heard are kept apart (`heard`) from what was tested (`beliefs`); hearsay steers but fades if never tested |
| 62 Reality is arbiter | IMPLEMENTED | `matter.py`, `world.py` | physics is consistent |
| 63 Curiosity opens | IMPLEMENTED | `inquiry.py` | a big gap between expectation and outcome becomes a puzzle; curiosity scales its pull, hunger crowds it out |
| 64 Experimentation | IMPLEMENTED | `inquiry.py`, `information.py`, `mind.py`, `actions.py` | puzzles pull people to try things again and to vary them; a claim they accept becomes something to check |
| 65 Testing/compare | PARTIAL | `inquiry.py` | repeated tests settle or renew a puzzle; no comparison of conditions (no controls) |
| 66 Falsification | IMPLEMENTED | `knowhow.py`, `information.py` | a contradicting outcome moves a judgement twice as fast; a refuted claim lowers trust more than a confirmed one raises it |
| 67 Models improved | PARTIAL | `knowhow.py` | `itemval`/`beliefs` update from outcomes |
| 68 Hidden regularities | IMPLEMENTED | `matter.py` | physics discoverable, never revealed |
| 69 Individual/collective | PARTIAL | `information.py` | individual testing; reputations pooled by word; no group experiments |
| 70 Social error correction | PARTIAL | `information.py` | witnesses reject wrong versions; sources who turn out wrong lose credibility with everyone they told, and by word of mouth |
| 71 Superstition competitor | IMPLEMENTED | `knowhow.py` | false causal stories can institutionalize as beliefs |
| 72 Accumulates under pressure | PARTIAL | `biology.py` | habits reinforce what works |
| 73 Discovery cascade | IMPLEMENTED | `mind.py` | `can_make` dependency chains |
| 74 External records | PARTIAL | `marks.py`, `historian.py` | a mark can teach a technique nobody alive knows (the historian records it); no records of observations over time |
| 75 Detection | IMPLEMENTED | `historian.py` | counts puzzles, tests, verified and refuted claims; notes the first person to test the same thing three times |
| 76 Final law | IMPLEMENTED | — | philosophy honored |

---

## Chapter 5 — The Laws of Information

| Law | Status | Module | Evidence / Notes |
|---|---|---|---|
| 77 Information ≠ knowledge | IMPLEMENTED | `information.py` | the speaker builds a telling (a message); only the listener's functions change the listener |
| 78 Information cost | PARTIAL | `actions.py` | talking takes the week's action and energy; nothing more |
| 79 Channels | PARTIAL | `information.py`, `marks.py` | speech, demonstration, watching, traces, and marks read as claims |
| 80 Fidelity imperfect | IMPLEMENTED | `information.py`, `historian.py` | every retelling can change a story; the historian measures wrong versions by number of tellings |
| 81 External storage | PARTIAL | `marks.py` | marks persist, wear away and can be destroyed; they hold links to things and practices, not texts |
| 82 Asymmetry | PARTIAL | `person.py` | local knowledge only |
| 83 Control | NOT_IMPLEMENTED | — | |
| 84 Trust separate | IMPLEMENTED | `information.py` | acceptance weighs goodwill, the source's track record, visible evidence, fit with own experience, emotion, attention and how many said it |
| 85 Enables scale | NOT_IMPLEMENTED | — | |
| 86 Contested history | PARTIAL | `information.py`, `historian.py` | rival versions of the same event coexist; listeners keep the better-trusted one; no records |
| 87 Information as resource | NOT_IMPLEMENTED | — | |
| 88 Bandwidth/latency/noise | NOT_IMPLEMENTED | `config.py` | only implicit (reach/perception radius) |
| 89 Detection | PARTIAL | `historian.py` | story drift, myths and shared symbols are measured |
| 90 Final law | ASPIRATIONAL | — | later experiment |

---

## The Influence Layer (91–92)

| Law | Status | Module | Evidence / Notes |
|---|---|---|---|
| 91 Beliefs not written directly | IMPLEMENTED | `information.py`, `knowhow.py` | speakers only build messages; listeners accept, doubt or reject from their own state; accepted claims stay hearsay until tested |
| 92 Influence equation | IMPLEMENTED | `information.py` | trust ✓ demonstrated success: track records and visible health ✓ attention ✓ social proof ✓ emotion ✓ evidence partial; additive, not a literal product |

---

## Chapter 6 — The Laws of Power

| Law | Status | Module | Evidence / Notes |
|---|---|---|---|
| 93 Power relational | DETECTED_ONLY | `historian.py` | detects leaders; no power mechanic |
| 94 Forms of power | NOT_IMPLEMENTED | — | |
| 95 Attention scarce | PARTIAL | `thought.py` | attention system exists; no power consequence |
| 96 Influence → authority | NOT_IMPLEMENTED | — | |
| 97 Coordination is power | NOT_IMPLEMENTED | — | |
| 98 Authority legitimate | NOT_IMPLEMENTED | — | |
| 99 Maintenance | NOT_IMPLEMENTED | — | |
| 100 Institutions | NOT_IMPLEMENTED | — | |
| 101 Power concentrates | NOT_IMPLEMENTED | — | |
| 102 Power contested | NOT_IMPLEMENTED | — | |
| 103 Collapse possible | PARTIAL | `world.py` | population/skills can die out |
| 104 Final law | ASPIRATIONAL | — | later experiment |

---

## Chapter 7 — Creation & Invention (the strongest implemented chapter)

| Law | Status | Module | Evidence / Notes |
|---|---|---|---|
| 105 Properties not recipes | IMPLEMENTED | `matter.py` | no named recipes anywhere; edge/reach/hard/contain/warm/float |
| 106 Primitive actions only | IMPLEMENTED | `actions.py` | 17 primitive actions; no "build house" |
| 107 Materials by properties | IMPLEMENTED | `matter.py` | `RAW` table of numeric properties |
| 108 World resolves outcomes | IMPLEMENTED | `matter.py` | strike/bind compute new state from properties |
| 109 Usefulness discovered | IMPLEMENTED | `knowhow.py` | `judge_item`/`itemval` from felt ease |
| 110 Remember & repeat | IMPLEMENTED | `knowhow.py` | recipes remembered, remade |
| 111 Taught & copied | IMPLEMENTED | `knowhow.py` | `teach`/`watch` |
| 112 Open-ended improvement | PARTIAL | `matter.py` | new sigs via play; no explicit "improve a recipe" step |
| 113 Changes possibility space | IMPLEMENTED | `mind.py` | `can_make` requires earlier parts |
| 114 Can be lost | IMPLEMENTED | `knowhow.py` | `check_lost` |
| 115 Externalization of technique | PARTIAL | `marks.py` | a mark linked with a kind of stone being struck can lead a reader to try striking it; nothing longer than one step is recorded |
| 116 Problem + opportunity driven | IMPLEMENTED | `mind.py`, `actions.py` | needs (problem) + play/curiosity (opportunity) |
| 117 Detection | IMPLEMENTED | `historian.py` | `classify` names things by properties only |
| 118 Final law (physical core) | IMPLEMENTED | `matter.py` | bottom-up assembly |
| 119 Not limited to objects | PARTIAL | `marks.py` | marks and their shared links; no norms or rituals |
| 120 Complex from earlier | IMPLEMENTED | `mind.py` | dependency chains via `can_make` |

---

## Summary counts

Counted from the tables above (115 rows):

- **IMPLEMENTED:** 56
- **PARTIAL:** 39
- **NOT_IMPLEMENTED:** 17
- **ASPIRATIONAL:** 2 (Laws 90, 104)
- **DETECTED_ONLY:** 1 (Law 93)

The fully built layers are **Reality (Ch. 1, mostly)**, **Creation (Ch. 7)**
and the **Influence layer (91-92)**. Knowledge (Ch. 3) and Discovery (Ch. 4)
are largely built. Culture (Ch. 2) and Information (Ch. 5) are partly built.
Power (Ch. 6) is deliberately left unbuilt: it must emerge from the layers
below, or not at all.

---

## Known Bible ↔ code discrepancies (for the next Bible revision)

1. **Year length.** The code uses **52 weeks = 364 days**; the Bible says "365
   simulated days."
2. **Initial population.** The 20 founders are **distributed across four
   islands** (one band each), not one contiguous landmass.
3. **Chapter 7 is not merely theoretical.** It is currently the *strongest
   implemented* chapter and should eventually be described as
   implemented/stable rather than "LOCKED."
4. **Rule 14 (needs).** Thirst now exists. There is still no **sleep** (only a
   "rest" energy action) and no autonomy need.
5. **Rule 13 (perception).** Perception is radius-limited and memories are
   misremembered, but nobody deliberately deceives.
6. **Weekly decisions.** Decisions are weekly (accepted by the creator). Water
   in sight that can be walked to counts as reachable every day, at an energy
   cost, rather than being walked to day by day.
7. **Speech.** The words in speech bubbles are our English rendering of what
   really passed between people. They have no language; only marks can gain
   meaning so far.
8. **Resolved by v8.1:** the year length (v8.1 Law 1: 52 weeks of 7 days, weekly decisions) and Rule 14's
   gaps (v8.1 marks autonomy as not modelled and sleep as partly modelled). Law 16's "persistence" was the
   engine's "diligence"; fixed in the status edition at the creator's request.
9. **Open from v8.1:** "runtime core state should remain deterministic and discrete where practical; floats …
   must not silently alter core decisions." The core is deterministic but uses floats throughout. Awaiting
   the creator's reading.

---

## Feature ledger

Every feature, the laws it implements, and the laws it violates or only partly
honours. Newest first.

### 2026-10-03 — Reputation, testing, records, floating (after E1's investigations)

**1. Reputation from tested accuracy** (`information.record`, `credence`, `tested`, `share_reputation`; `person.records`)
- Implements: 36 (for whose word holds), 54 (partly), 56, 70 (partly), 84, 92 (the "demonstrated
  success" lever now rests on each listener's own track record of a source).
- Partly violates: how fast a record outweighs goodwill (n / (n + 3)), and word of mouth counting as half
  an observation, are numbers we chose. Reputation covers only whose word holds, not generosity or violence.

**2. More testing** (`information._wonder`, `tell_place`, `hear_place`, `check_places`; `knowhow.look_at_traces`; traces in `world.py`)
- Implements: 47 (observation of what others left behind), 64 (a claim taken on becomes something to
  check), 65 (more repeated observations), 59 (tests are counted).
- Partly violates: the new kinds of claim (where water is, where animals were seen) are a list we chose.
  So are the checking distance (2 tiles), how long a sighting is worth checking (12 weeks), and which
  activities leave traces and how fast they fade (turned earth, flakes, ash, bones), which is physics we
  wrote.

**3. External records** (`marks.read`; traces as things a mark can mean)
- Implements: 22 and 23 (marks can now mean what was done in a place), 52, 74 (partly), 79, 81, 114 (a
  lost technique can be recovered from a mark), 115 (partly).
- Partly violates: a mark can be read for only four kinds of claim (water here, animals hunted here, seed
  sown in a season, a kind of stone struck). "Strike it with the hardest stone in hand" is our rule for
  turning a mark into a technique. Marks are never combined, so this is proto-writing, not writing.

**4. Floating as an affordance, and water as a barrier** (`world.walk`, `actions._over_water`, far shores in `mind.py` and `thought.py`)
- Implements: Rule 3 (movement crosses space tile by tile; this fixes the 3-tile jump over water that E1
  found), 28 (partly: a far shore becomes something to want), 63 (curiosity about land out of reach),
  109 (a raft's worth comes from reaching land it made reachable), 111 (people who see someone come
  ashore can copy the raft).
- Partly violates: the pull of a seen shore, the 12 weeks a voyage holds its heading, and washing a
  person ashore "half drowned" if their raft is gone are rules we wrote.

### 2026-10-02 — Information, surprise, marks, water and weather

**1. The listener decides** (`information.py`: `credence`, `hear_story`, `hear_how`, `hear_belief`)
- Implements: 56, 61, 84, 91, 92 (all six levers in some form). Removes a
  telepathy breach: before, the teller looked into the listener's memories and
  know-how to choose something new to say. Now the teller says what matters to
  them and cannot see what the listener knows.
- Partly violates: 92, because the levers are added with weights we chose,
  not discovered. 13, because nobody lies.

**2. Imperfect transmission** (`information.py`: `_recall`, `_suspect`, `_recipe_as_shown`, `_belief_as_told`; `knowhow.watch`)
- Implements: 25, 26, 51, 80, 112 (a mistaken copy can work better), 23 (for marks).
- Partly violates: the kinds of error are a fixed list we wrote: wrong actor
  (biased toward people the teller dislikes), place shift, exaggeration,
  material swap and season slip. Real distortion is more varied.

**3. Hearsay and testing** (`person.heard`, `information.tested`, `knowhow.judge_item`, `knowhow._credit`)
- Implements: 49, 56, 61, 66, 67, 70 (partly), and the influence chain
  "accurate predictions → trust".
- Partly violates: the asymmetry between contradiction and confirmation (twice
  the update; −0.10 vs +0.06 trust) is our claim about human nature, not
  something they learn.

**4. Surprise → investigation** (`inquiry.py`; puzzles in `thought.py`, `mind.py`, `actions._play`)
- Implements: 28 (partly), 63, 64, 65 (partly), 66, 116 (opportunity-driven
  invention), 73 (a found effect pulls toward the next try).
- Partly violates: the surprise threshold and the pull weights are fixed
  numbers. Expectations exist for only three things: what made things do, how
  set-down things turn out, and what striking does. Other surprises, such as a
  hunt going unusually well, do not become puzzles.

**5. Marks** (`marks.py`; drawn by the viewer; detected by the historian)
- Implements: 22 (for marks), 23, 52 (partly), 79, 81 (partly), 119 (partly).
- Partly violates: the list of things a mark can be linked with is fixed by
  us (food set down, growing food, fire, water, shelter, grave, six animals,
  people). The "associative hand" (drawing shapes already linked with what is
  here) is a built-in bias. Marking only happens while fiddling with things
  (no separate act), with a chance we set (0.2).

**6. Water and thirst** (`weather.drink`, `person.springs`, water-seeking in `mind.py`)
- Implements: Rule 3 (walking to water costs energy), Rule 6 (water as a
  resource), Rule 7, Rule 12 (water is known only once seen), Rule 14 (thirst),
  62 (drinking the sea has consequences, and nobody is told).
- Partly violates: the weekly abstraction (water in sight counts as reachable
  daily). Thirst's pull being stronger than hunger's is our human-nature claim.
  Founders start near water if their island has any, which is an initial
  condition we chose.

**7. Weather** (`weather.py`: wet and dry years, weekly rain, storms, floods, hard winters, place-based cold)
- Implements: Rules 7, 8, 10. Storms and floods are remembered and retold
  like other events.
- Partly violates: one rain roll per week for the whole map (deserts
  excepted), not regional weather. Disease still does not spread.

**8. Livable islands** (`geo.py`: more rivers; every island of 12+ tiles gets a stream or pond)
- Implements: Rule 6.
- Partly violates: guaranteeing water on every sizeable island is our choice
  of world. It is physics, not history, but it does rule out a dry-island
  extinction.

**9. Animals that fight back, and learned fear** (`actions.resolve_hunts`, `social.react` for "mauled", hunting choices in `mind.py`)
- Implements: Rule 9, Rule 13 (fear learned from experience and stories),
  Chapter 1's "emotions are derived from events + memory + personality".
- Partly violates: none known.

**10. Mind view and their clock** (`mindview.py`, `viewer.html`)
- Implements: observer mode. It only reads: what is on their mind, the choices
  weighed, puzzles, hearsay, marks and feelings, put into words for us.
- Partly violates: Law 22 for speech. Thought and speech text are our English
  rendering of real state, not their words.

**11. Historian checks against the truth** (`historian.py`: truth, myths, story drift, symbols, testing)
- Implements: 26 (detection), 41, 59, 75, 89 (partly). It never changes the
  world (tested).
