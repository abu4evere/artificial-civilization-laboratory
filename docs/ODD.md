# ACL described with the ODD protocol (draft, 21 October 2026)

The ODD protocol (Overview, Design concepts, Details; Grimm et al. 2006, 2010, 2020) is the standard way agent-based
models are described, so others can understand, judge and rebuild them. This is ACL's first ODD description, written
from the live package `acl/` (nature v2 as its defaults). Every value named here lives in `acl/config.py`; where a
point is approximate it says so. It describes the model, not any one study: each study's frozen plan names the
settings it changes.

---

## 1. Purpose and patterns

**Purpose.** To test whether cumulative culture and, eventually, civilization can emerge in a population of agents
given *nature only* (bodies, needs, materials, seasons, kinship and feelings), with no list of inventions, no reward
for cultural behaviour, and no pre-trained knowledge (no language models); and, where it does not emerge, to locate
exactly what stops it.

**Patterns used to judge the model** (pattern-oriented modelling): forager demography (mortality by age, fertility
spacing), small-population fragility, the share of the diet by means of getting food, the rarity and loss of
inventions, and inter-band contact rates. Comparisons with real foragers are made in each study's evidence notes and
labelled as such.

## 2. Entities, state variables and scales

- **World:** a torus of tiles, by default **40 × 40**, made of islands and water. Each tile holds wild plant food,
  seed, crops, raw materials (stone, wood, fibre, clay, flint, char), fire, fresh or salt water, and animals.
- **Person:** id, name, sex, birth tick, parents, partner, wards and caregiver; health, energy, food and seed carried,
  items and materials carried; **temperament** (eight inherited traits: curiosity, diligence, sociability, kindness,
  temper, anxiety, care, boldness, each 0–1); skills; **relationships** to others (affection, familiarity, trust,
  respect); **memories** of events and places; **beliefs**; **recipes** (at most 12); and a **habit table** (Q-values,
  32 contexts × 19 actions).
- **Scales:** one step is **one week**; 52 weeks a year, four seasons of 13 weeks. Studies usually run 120 years.
  A person can act within **reach = 3** tiles a week and see **perception = 4** tiles.

## 3. Process overview and scheduling

Each week (`World.step`), in this order:
1. The land grows and decays (plants by season and the year's weather; materials; fires), the week's weather is set,
   and animals move.
2. Every person older than one year, **in a random order**, decides and acts: each scores every available action
   (rest, forage, hunt, gather, put, take, make, play, explore, give, care, talk, court, steal, attack, flee, join,
   heat, fill) and picks one at random, weighted by score (softmax, temperature 0.2). Actions take effect at once.
3. Hunts are resolved; infants and children move with their caregivers.
4. **Body phase:** eating, thirst, cold, illness, healing, ageing, death (Gompertz mortality), conception, birth,
   and learning from the week's reward.
5. Observers (instruments) read the world. They are checked, for every study, to change nothing in it.

## 4. Design concepts

- **Basic principles.** "Nature, not history": only physical and biological rules are written; anything cultural must
  arise from them. Changes to nature need a written case and evidence about the real world.
- **Emergence.** Tools, techniques, sharing, storage, sowing, marks and their transmission are not programmed as
  outcomes; materials have properties, and combinations are discovered.
- **Adaptation.** Choices combine instinct-like scores with learned values: `learned_weight` (0.6) sets how much
  experience counts.
- **Objectives.** Agents have no global goal; each week's reward comes from the body (food, warmth, health) and
  feelings (company, care).
- **Learning.** A per-person habit table updated by temporal-difference learning (learning rate 0.05, discount 0.8); people also imitate those they respect or who seem to do well; recipes are learned by trying, by being
  taught in conversation, and in a few cases by watching.
- **Prediction.** A weak anticipation of next season's shortage (`anticipation_weight`).
- **Sensing.** Only what is within perception: people, food, water, animals, fire; plus memories of places and people.
- **Interaction.** Talking (gossip, teaching, telling places), giving, caring, courting and pairing, stealing,
  fighting, hunting together.
- **Stochasticity.** Every random draw comes from one seeded stream, so any world can be replayed exactly; a "sham"
  extra draw is used to measure how far chance alone moves a world.
- **Collectives.** Bands are not programmed; groups are measured from who lives near whom.
- **Observation.** Per study: read-only observers and, when needed, logging copies of the code that write to a
  record nothing in the world reads; each is shown to leave the world's final state hash unchanged.

## 5. Initialization

By default **20 founders**, aged 16 and over, each with three weeks of food (`founder_food` 21), split into up to
four bands placed on separate islands; founders' temperaments are drawn between 0.1 and 0.9. Founders start with
ties within their band and know nothing else: no recipes, no beliefs.

## 6. Input data

None. The world is generated from the seed; no external data drive it.

## 7. Submodels (where each lives)

| submodel | module |
|---|---|
| land, plants, seasons, materials, fire | `world.py`, `matter.py`, `weather.py` |
| animals and hunting | `fauna.py`, `actions.py` |
| choice of action | `mind.py`, `decision.py`, `thought.py` |
| actions | `actions.py` |
| body, ageing, death, birth, learning | `biology.py` |
| relationships, gossip | `social.py`, `information.py` |
| recipes, teaching, memory limit | `knowhow.py` |
| marks on surfaces | `marks.py` |
| measurement | `measure.py`, `report.py`, each study's observers |

---

**Still to do before this is final:** exact reward terms and learning rate values; the full list of conditions for
each action; the pattern targets with their sources. Each will be filled in from the code, not from memory.
