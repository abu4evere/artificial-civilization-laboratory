# ACL nature v11 described with the ODD protocol (2 November 2026)

**What this is.** A description of ACL's nature as it stands, in the standard form for agent-based models (ODD:
Overview, Design concepts, Details; Grimm et al. 2006, 2010, 2020). It lets others understand, judge and rebuild the
model. **Documentation only: nothing in the simulation changes.**

**Source.** The live package `acl/` at nature v11 (live since 31 October 2026; frozen copy
`experiments/NV11_nature_v11/code_v11`). Every number below was read from the code. The file and function are named
where it helps. The first draft, `docs/ODD.md` (21 October, nature v2), is kept as that version's record.

---

## 1. Purpose and patterns

**Purpose.** The creator's mission (24 October 2026): "a world with **minimum laws** and a period that produce an
**autonomous and cognitive mind**."
- Only nature is written: bodies, needs, materials, land, seasons, kinship and feelings. Culture is written by nobody.
- The model tests whether minds that **build on what they and others learned** (cumulative) and **choose their own
  goals** (autonomy) can arise. Where they do not, it locates what stops them.
- There are no named inventions, no recipe chains, no rewards for cultural outcomes, and no language models inside the
  people.

**Patterns that keep nature honest.** These are references, not targets to tune to:
- **Ageing and death:** anchored to the !Kung (AG1, adopted as v10).
- **Births:** twins and the sex ratio at birth (TW1, v7).
- **Childhood:** at what ages children make things (`docs/research/children_ages_making_2026-10-31.md`).
- **Value passing among foragers:** Hewlett et al. 2011 (`docs/research/value_transmission_2026-11-01.md`).

Each study's frozen plan names the evidence it compares against.

## 2. Entities, state variables and scales

**World** (`world.py`, `geo.py`).
- **The grid:** default 40 × 40 tiles; studies use 80 × 80 with 80 founders (`LP`). Coordinates wrap, and the land
  sinks into sea toward the edges, so it is continent and islands with sea all round.
- **Each tile's fixed qualities:** biome, height, temperature, cost to cross, fertility, rock, forest, wildness, and
  whether it has flint.
- **Each tile's stocks:** wild plant food, seed in the ground and crops, wood, stone, flint, fibre, clay (only on banks
  by rivers and lakes), char, fire, and traces of what people did there.
- **What the world as a whole holds:**
  - groups of animals by species (`fauna.py`);
  - the bodies of the dead;
  - made things lying on the ground;
  - dug pits;
  - marks on surfaces (`marks.py`);
  - the year's growing factor (0.65–1.25);
  - the sky: the year's wetness and winter, the week's rain, storms and floods (`weather.py`).
- **The knowledge register** (`world.knowledge`): every kind of thing anyone has made, with who made it first and
  whether anyone alive still knows how.

**Person** (`person.py`).
- **Identity and family:** sex, birth week, generation, mother, father, partner, children, wards, carer.
- **Body:** health, energy, thirst, illness, pregnancy.
- **Holdings:**
  - food and seeds, up to 100 together;
  - eight raw materials, up to 20 together;
  - up to 3 made things.
- **Temperament:** eight inherited traits, each 0–1: curiosity, diligence, sociability, kindness, temper, anxiety, care,
  boldness.
- **Skills:** foraging, hunting, crafting.
- **Feelings:** mood, fear, anger, grief, loneliness, wellbeing.
- **Ties to each other person** (not symmetric): affection, trust, familiarity, grudge, respect, and the balance of
  food given.
- **Memories:** at most 60. Each memory fades, and records whether it was lived or told, and by whom.
- **Habit table `q`:**
  - one learned value per **situation × action**: 32 × 19 = 608 values, each kept within −1.5 to 1.5;
  - a count of how often each was tried (`tried`).
- **What they have worked out:**
  - recipes, at most 12, each with the value of that kind of thing (`itemval`);
  - beliefs about what to leave where;
  - how good life has been at each place;
  - expectations;
  - hearsay (`heard`);
  - puzzles;
  - what is on their mind (`thoughts`, `focus`).

**Situation** (`mind.context_index`): food on hand (4 levels) × anyone within reach (2) × season (4).
- **Food levels:** below half a week's need or health below 40; under 2 weeks; under 6 weeks; 6 weeks or more.

**The 19 actions:** rest, forage, hunt, gather, put, take, make, play, explore, give, care, talk, court, steal, attack,
flee, join, heat, fill.

**Things** (`matter.py`).
- **Eight materials:** stone, flint, bone, wood, fibre, hide, clay, char.
- **Ten properties**, each 0–100: edge, reach, hard, contain, warm, float, tight, plastic, fuel, flex.
- **Made things are described only by their properties and how they were made. No thing has a name.**

**Scales.**
- **Time:** one step is **one week**. A year is 52 weeks, in four seasons of 13 weeks. The world starts in spring.
- **Life stages:**

  | stage | age |
  |---|---|
  | infant | under 1 |
  | child | 1 to 11 |
  | teen | 12 to 15 |
  | adult | 16 to 49 |
  | elder | 50 and over |

- **Space:** a person can travel and still act within **3 tiles** a week, and sees **4 tiles**.

## 3. Process overview and scheduling (`World.step`, in this order)

1. **The land and the animals:**
   - the land grows and decays (`_grow_land`);
   - the week's weather is set;
   - animals move, eat and breed (`fauna.step`).
2. **Decisions:** everyone aged **one year or more**, in an order shuffled from the world's random stream, chooses an
   action (`mind.decide`) and does it at once (`actions.perform`). Later movers see earlier movers' effects.
3. **Hunts** are settled together.
4. **Children under 12** move to their carer's tile.
5. **The body phase** (`biology.body_phase`):
   1. Loose food rots: slower near smoke, and slower if it has been in a fire. Seeds keep.
   2. Carers feed their dependents first. How much they give up is set by their `care` trait.
   3. Eating: food that has been in a fire goes 15% further. Hunger costs health.
   4. Drinking; then cold, softened by shelter, fire and worn things.
   5. Orphans under 6 with no carer suffer from neglect.
   6. Illness; then death, either when health reaches 0 or by the age-based (Gompertz) risk.
   7. Births and conceptions.
   8. Orphans under 12 find a carer. At 12, children fend for themselves.
   9. Feelings and wellbeing; the value of the place; **habit learning** (age 1 and over).
   10. **Every 4 weeks:** children are pulled toward their carer's habits (upbringing), and memories fade.
   11. **Every 13 weeks:** ties are upkept; old placements are dropped; recipes that proved useless are forgotten; and
       the register marks any kind of thing that no one alive knows how to make as lost.
6. **The ground:**
   - bodies rot;
   - made things on the ground are picked up by whoever stands there with room;
   - pits slowly fill in.
7. **Anyone left on water** with nothing that floats is put ashore, half drowned (−10 health).
8. **Record:** the week's events are hashed into the event chain, the week advances, and observers read the world.

## 4. Design concepts

**Basic principles.**
- **Laws, not history:** write conditions, never outcomes.
- **Nature changes one law at a time.** Each change is a frozen study first. Each adopted version stays in its own frozen
  copy, so it can be undone (table in §8).

**Emergence.** None of these is written as an outcome:
- tools and techniques;
- sharing and paying back;
- storage, shelters and sowing;
- what marks mean;
- bands and their splits;
- who teaches whom.

**Adaptation: how a choice is made** (`mind.decide`). Each possible action (and its target) gets a score, made of:
- an **instinct-like pull**, set by the body, feelings, temperament, kin and what is in sight;
- the **curiosity pull** (v9): 0.3 × curiosity × (1 − hunger) ÷ (1 + times this action was tried in this situation);
- **minus a cost** for heading where no water is in sight;
- **plus 0.6 × the learned value** `q`[situation, action].

Attention then steers the scores toward what is on the person's mind (`thought.steer`). The choice is drawn at random,
weighted by a **softmax at temperature 0.2**.

**Objectives.** No one has a goal given from outside.
- **The weekly learning signal** is the action's reward plus 2 × the week's change in mood (`biology._learn`).
- **Mood** follows wellbeing:
  `wellbeing = 0.3 fed + 0.2 health + 0.2 (1 − loneliness) + 0.15 family's health + 0.15 warmth − 0.5 grief − 0.25 fear − 0.15 anger`,
  with mood moving a quarter of the way to wellbeing each week.
- **Action rewards** (`actions.py`):

  | action | reward |
  |---|---|
  | **forage** | 0.3 × min(1, got ÷ need) × (0.3 + 0.7 × hunger) |
  | **hunt** | 0.3 × min(1, got ÷ need) on success; −0.05 on failure |
  | **take** someone else's food | 0.3 × min(1, taken ÷ need) |
  | **take** back one's own | +0.1 |
  | **rest** | +0.05 |
  | **gather** | +0.02 |
  | **heat food** | +0.02 |
  | **explore** | +0.03 × curiosity |
  | **join** | +0.03 |
  | **flee** | +0.05 |
  | **make** (a known thing, made) | +0.1 |
  | **play** that makes something | +0.05 |
  | **play** that leaves a mark | +0.03 × curiosity |
  | **play** with nothing to fiddle with | −0.01 |
  | **give** food | 0.1 + 0.2 × kindness + 0.2 × kinship |
  | **care** | 0.1 + 0.3 × care × kinship |
  | **talk** | 0.1 + 0.1 × sociability; **+0.1 more if the listener took something new from a lesson** |
  | **court**: pairing | +0.5 |
  | **court**: with one's partner | +0.2 |
  | **court**: otherwise | +0.03 |
  | **steal** | 0.3 × min(1, amount ÷ need), −0.2 if noticed |
  | **attack** | +0.3 × temper − 0.2 × kindness, or +0.1 (by outcome, `actions._attack`) |

- **Honest note:**
  - No reward names any invention or cultural result.
  - Small fixed rewards do exist for the **act** of making (+0.1), for play that makes something (+0.05), and for a
    lesson the listener takes (+0.1). The 21 October draft said there was "no reward" for inventing or teaching. That
    did not match the code then either (the +0.1 for a lesson taken is in v2 too). The correction is appended to that
    draft.

**Learning.**
- **Habits:** `q += 0.05 × (r + 0.8 × max q[next situation] − q)`, kept within ±1.5. When a gift is paid back, the
  first giver's give-habit gets +0.025.
- **Habits pass between people in three ways:**
  1. **At birth:** a newborn's values start at 0.25 × (mother's + father's), using the mother's twice if the father is
     dead or absent. That is half the parents' mean (`_born`). Study BN1 is testing a copy without this (§9).
  2. **Upbringing:** every 4 weeks, a child under 12 on the same tile as their carer moves 8% of the way toward the
     carer's whole table (`_upbringing`).
  3. **Talk:** the listener moves toward the speaker's whole table at 0.05 × (0.5 + curiosity) × (0.5 + respect). This
     happens only if their respect for the speaker is at least 0.2, or the speaker's mood is more than 0.1 above theirs
     (`_imitate`).
- **Know-how (recipes)** comes in five ways:
  1. **Made** while fiddling (play): striking, binding, shaping wet clay, holding in a fire, filling.
  2. **Taught** in talk, to listeners aged 4 or more. The teacher shows one of their three most valued things (value
     above 0.15).
  3. **Copied** by watching someone do well with a thing. The chance is 0.04 × (0.5 + curiosity). In 15% of cases the
     copy goes through the error step twice (seen, not explained).
  4. **Read** from marks: only the striking kind.
  5. **Heated:** a dry clay thing or lump carried by a hot fire (heat 6 or more) sets by itself, and the carrier
     remembers how (`biology._passive_heat`).
- **Showing is imperfect** (`information._recipe_as_shown`):
  - the error chance is 0.3 − 0.15 × the teacher's crafting − 0.1 × the learner's crafting, a further −0.1 if the
    teacher has the things in hand, and never below 0.04;
  - an error changes one step: the wrong form, stone, part or binding.
- **Holding and losing know-how:**
  - at most 12 recipes; the least valued is dropped (`knowhow.MAX_RECIPES`);
  - a recipe valued below −0.15 is forgotten;
  - know-how dies with its holder;
  - a kind of thing is **lost** when no one alive knows it, and is marked alive again if someone re-learns it.
- **What things are worth:** a thing's value rises when using it beats what the person expected, and falls when it
  does not.
- **Beliefs about what to leave where:** linked to what followed at that spot, at rate 0.25 (`association_rate`).
- **Puzzles:** surprises become puzzles that draw the curious back to test again (`inquiry.py`).

**Prediction.**
- A season in which a person went short is felt a season early, in the pull to get food (`anticipation_weight` 1.0).
- The habit values are themselves learned expectations of what follows.

**Sensing.**
- **People:** those within reach; the 12 nearest count.
- **Food, water and animals:** within sight. Fresh water within 2 tiles is drunk from daily.
- **Marks** are seen where a person stops. Traces and placements nearby are seen from age 6.
- **Hearsay:** what is heard stays hearsay until the person's own experience tests it (`information.py`).

**Interaction.**
- **Talk:** gossip, reputation, places, lessons, and habit imitation.
- **Giving:** food, or since v11 a made thing handed over, when it helps the receiver more than it costs the giver.
- **Care:** for the sick and for kin.
- **Pairing:** courting and pairing.
- **Harm:** stealing, fighting and fleeing.
- **Joint work:** hunting together (success chance grows with the number of hunters^1.5).
- **Family:** feeding dependents, and upbringing.

**Stochasticity.**
- Every random draw comes from one stream seeded by the world's seed (`world.rng`), so any world replays exactly.
- A "sham" setting (`sham_draw`) adds one extra draw in week one, to measure how far chance alone moves a world.

**Collectives.** Bands are not programmed.
- **How founders start:** in up to 4 groups (founders ÷ 4, at most 4), each on its own island where there are enough
  islands, with starting ties (affection 0.3, trust 0.3, familiarity 0.5).
- **After that:** groups are only measured, from who lives near whom.

**Observation.**
- Observers read the world after each week.
- **For each study, zero checks show that the observers change nothing**: the world's state hash and the random
  stream's state are unchanged, with the observer and without it.
- Code fingerprints tie every result to the exact nature it ran on.

## 5. Initialization (`World.__init__`, `_make_land`, `_make_founders`)

**Land.**
- The land is raised from seeded noise.
- Stocks start at 0.6 of their caps: plants at 0.6 × 64 × fertility, wood, stone, fibre and flint likewise, and clay
  on banks.
- Animals are placed (`fauna.populate`).

**Founders:**

| setting | value |
|---|---|
| number | default 20; 80 in studies |
| sexes | half and half |
| ages | 16–28 years, drawn by the week |
| temperament traits | each drawn between 0.1 and 0.9 |
| skills | each 0.2–0.4 |
| food | 21 (three weeks) |
| health, energy | 100 |
| mood | 0.5 |
| loneliness | 0.3 |

**Habit values all 0, no recipes, no beliefs.** Founders start near fertile ground with fresh water.

## 6. Input data

None. Everything grows from the seed.

## 7. Submodels (key numbers, all from `acl/config.py` unless named)

**Bodies** (`biology.py`).
- **Food needed a week:**

  | infant | child | teen | adult | elder |
  |---|---|---|---|---|
  | 2 | 4 | 6 | 7 | 6 |

- **Hunger:** starvation costs 14 × the share of need not met; a fed week restores 1.5.
- **Thirst** costs up to 20 a week.
- **Cold** costs 1.2 in a hard-winter week fully exposed, more in harsher cold, doubled for infants and elders.
- **Illness:**
  - starts with chance 0.003 a week, raised by hunger, frailty and crowding, and lowered by fire;
  - costs 3.5 a week;
  - ends with chance 0.15 a week, +0.25 if cared for, +0.1 if fed.
- **Death by age** (Gompertz; v10): weekly risk = 1.5e-5 × 0.0072 ÷ 0.0249 × e^(0.0866 × age in years), so the
  risk doubles about every 8 years.

**Births** (`biology.py`).
- **Fertility:** from 16 to 45.
- **Conception:** chance 0.04 a week for a couple within 2 tiles, doubled when courting. None while the mother is
  starving, below 50 health, or nursing (78 weeks, while her youngest lives).
- **Pregnancy:** 39 weeks. The mother dies in childbirth with chance 0.01.
- **The newborn:**
  - a boy with chance 105 ÷ 205; identical twins 0.004; fraternal twins 0.010;
  - each trait is the parents' midpoint plus a random drift (Gaussian, spread 0.08), kept within 0.02–0.98;
  - starting health 70.

**Land** (`world._grow_land`).
- **Wild plants:** at most 64 per tile and regrowth 14 a week, both at fertility 1, scaled by season (1.3, 1.0, 0.5,
  0.15 for spring to winter) and by the year's factor.
- **Winter:** 3% of plant food rots each winter week.
- **Seed in plant harvests**, by season: 0, 12%, 35%, 5%.
- **Buried seed:** 8% sprouts each spring and summer week, giving 5 food per unit. Outside the growing season, 3% a week
  is eaten.

**Fire** (`world.py`, `actions.py`).
- **Lightning:** chance 0.03 a summer or autumn week.
- **Flint struck hard** sparks 30% of the time.
- **Fuel:** a fire burns 1 fuel a week; one unit of wood adds 1.5.
- **Warmth:** a fire keeps off 60% of cold.

**Work** (`mind.py`, `actions.py`).
- **Foraging:** (12 + 14 × skill) × a stage factor (child 0.4, teen 0.8, adult 1.0, elder 0.7) × the best tool's
  factor.
- **Hunting:** success chance min(0.92, 0.10 × hunters^1.5 × (0.5 + skill) × tool); prey 25 + 12 per hunter; injury
  chance 0.03.
- **Gathering:** 3 + 4 × skill.
- **Skill** grows by 0.012 with use.

**Ages at which actions open** (`mind.decide`):
- **from 1:** deciding at all, and talking;
- **from 3:** gathering and play;
- **from 6:** foraging and taking;
- **from 12:** hunting, making, putting down, heating, filling, exploring out of curiosity or hunger, caring, stealing and attacking;
- **from 16:** courting (adults, to 49).

**Things** (`matter.py`).
- **The ways of making:**
  - **strike:** a brittle thing struck with a harder one can flake to an edge;
  - **bind:** joined with something flexible, reach adds up, and edge and hardness carry over;
  - **shape:** soft, wet clay pressed into hollow, long or point;
  - **heat:** dries, burns away, or sets hard what was shaped.
- **Use:** what a thing is good for comes only from its properties (`matter.factor`).

**Marks** (`marks.py`).
- **Making a mark:** three strokes, made while fiddling.
- **How long a mark lasts:** on the ground, weeks; on wood, years; on rock, generations.
- **Meaning:** a mark means nothing in the code. People link shapes with what is around them, beyond what is there
  anyway.

| submodel | module |
|---|---|
| land, plants, seasons, materials, fire | `world.py`, `geo.py`, `matter.py`, `weather.py` |
| animals and hunting | `fauna.py`, `actions.py` |
| attention, choice | `thought.py`, `mind.py`, `decision.py` |
| actions | `actions.py` |
| body, ageing, death, birth, habit learning, upbringing | `biology.py` |
| memories, gossip, telling, hearsay | `social.py`, `information.py` |
| recipes, item values, what to leave where, loss | `knowhow.py` |
| surprise and puzzles | `inquiry.py` |
| marks | `marks.py` |
| measurement | `measure.py`, `report.py`, each study's observers |

## 8. How nature got here (each change a frozen study first; the earlier nature kept in a frozen copy)

| version | change | from |
|---|---|---|
| v2 | the live package moves to nature v2 | the creator, 16 October 2026 |
| v3 | a failed lesson shows the needed part first (`parts_first`) | LM1 |
| v4 | the dead leave bodies (`bodies_stay`) | BD1 |
| v5 | the ground can be dug; food in a pit keeps longer (`digging`) | DG1 |
| v6 | bodies rot by warmth (`body_rot`) | BD2 |
| v7 | twins; 105 boys to 100 girls (`twins`, `sex_ratio_birth`) | TW1 |
| v8 | made things fall to the ground instead of vanishing (`ground_items`) | OP1 |
| v9 | the curiosity pull (`curiosity_pull`) | CU1 |
| v10 | ageing anchored to the !Kung | AG1 |
| v11 | a made thing can be handed to someone (`hand_items`) | HD1, HD1C |

## 9. Known gaps (from the studies; each would be a frozen study first, never a quiet change)

- **Learned values are passed at birth** (§4, Learning), which Earth's biology does not do. BN1 is testing a copy
  without it (`experiments/BN1_born_without_learned_content/`).
- **Making starts at 12**, while forager children make things earlier, by a gradient
  (`docs/research/children_ages_making_2026-10-31.md`).
- **Most know-how lives in one head** and dies with it; marks rarely revive it (KL1).
- **Handing things is rare and carries no know-how** (HA1).
- **The ways of learning from others** (teaching, watching, reading) **are written as laws.** In people they may be
  partly learned (Heyes 2019; `docs/research/mechanisms_cumulative_culture_2026-11-02.md`).
- **People choose among 19 given actions. They cannot make new kinds of option.** This is the gap closest to autonomy,
  and still open.
