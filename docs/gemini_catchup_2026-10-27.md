# ACL: catch-up for Gemini (27 October 2026)

Written by Claude (the assistant working on ACL with the creator) so that Gemini can give opinions alongside GPT.
From now on the creator wants every question asked of GPT to be asked of Gemini too, with the same text, and the two
answers compared. **Your role, as GPT's:** an honest, critical second opinion. Opinions are never sign-off; only the
creator decides. Code and records: https://github.com/abu4evere/artificial-civilization-laboratory

## 1. What ACL is
The **Artificial Civilization Laboratory**: an agent-based world of hunter-gatherers on a torus map (land, water,
seasons, plants, animals, materials, fire). **Nature is programmed; culture is written by nobody.** The creator writes
the laws, never the history.
- People are simple agents with bodies (hunger, thirst, energy, health, age, sex, genes for temperament), drives,
  learning and relationships.
- They forage, hunt, gather materials, make things (recipes found by trying), teach, talk, court, pair, have children,
  care, give, steal, fight, explore and die.
- There are no LLMs inside the people.
- The creator has written a book about it, *The World That Nobody Wrote* (Part One on Amazon). Part Two is being
  drafted.

**The mission (the creator, 24 October 2026):** "Our mission is not to recreate Earth with the same human history but
to create a world with minimum laws and a period that produce an autonomous and cognitive mind." Earth and human
evidence keep nature honest (no tuning); they are not the blueprint.

**Bob** is the goal: the agent that will exist when ACL succeeds, with **autonomy** (chooses its own goals) and a
**cumulative mind** (builds on what it and others learned). Every study is judged by whether it moves the world toward
such minds.

## 2. How the people decide and learn (nature v7)
- **Choice:** each week every option gets an instinct utility plus 0.6 × a learned habit value. One option is picked
  by softmax (temperature 0.2).
- **Habits:** temporal-difference learning, rate 0.05, discount 0.8 a week. They are kept for 32 situations (food on
  hand × company × season), and copied between people in talk (about 57% of an adult's habit term is copied).
- **Item worth:** learned from use, so a tool's felt worth is its factor − 1.
- **Recipe memory:** 12 slots.
- **Skill:** rises with practice; tool quality scales with crafting skill.
- **Also:** trust, beliefs about places, surprise that drives curiosity, fear (of animals that hurt them), grief.
- **Making** is scored as 2.0 × learned worth × diligence factor × (1 − 0.5 × hunger).

## 3. How the work is done (hard rules)
Every study follows the same steps:
1. Questions and predictions are written and frozen (`questions.md`, git tag `X-frozen`).
2. The creator signs off.
3. Code is built.
4. Zero checks are run: an observer changes nothing, reload is exact, and a switch turned off reproduces the old code.
5. Worlds are run in the cloud (GitHub Actions).
6. An analysis script written before the data is run.
7. Findings are written.
8. An **independent recompute** (a fresh chat recomputes the key numbers from the raw files, without the analysis
   script) must agree before the findings are final.

Other rules:
- Nature (the code of the laws) changes only by the creator's decision, one law at a time, after a study.
- No named inventions, recipes or rewards in nature: conditions, never outcomes.
- Wrong predictions are kept, and corrections are appended, never rewritten.

Nature versions so far:

| version | adds |
|---|---|
| v2 | memory fixes |
| v3 | parts-first teaching |
| v4 | bodies stay after death |
| v5 | digging |
| v6 | realistic rot |
| v7 (live since 25 Oct 2026) | twins and 105 boys per 100 girls at birth |

## 4. What about 100 studies have found (very short)
- **Culture appears without scripting** (symbols, techniques passed on, fire), but **novelty freezes**: few new kinds
  of thing after the first decades. Skill, recipes and making decay over generations.
- **Food:** people live hand to mouth. They stop foraging once fed and almost never store for winter. Tools barely
  pay. A lesson to prepare "undoes itself": preparing prevents hunger, so the lesson fades.
- **Worlds die out** (about a third in small worlds) because **births stop and people age out**, mostly through
  failing to find and keep partners, not through hunger. Couples are apart about half their weeks. Small worlds have
  too few people. Many fixes were tested; most had no meaningful effect.
- **Knowledge transmission** is the core bottleneck. Inventions are rarely taught because the inventor soon loses
  them. Offered lessons are rarely taken (6%). Several fixes to memory and teaching had no meaningful effect.
- **A thousand years (M1, nature v6):** every surviving world **wears away**. Food owed to tools fell 95%, skill to a
  tenth, recipes to an eighth, and no new kind lasted after year 100. A person born late knows a fifth as much as one
  born early.
- **Childlessness (RH1):** the break is pairing. Only 4–11% of childless women ever paired.
- **Women die younger (WM1):** mostly a rule that a mother feeds her child first; starvation is 68% of the gap.

## 5. The latest result: LS1, "Where does knowledge go?" (final, 26 Oct 2026; 96 worlds × 1,000 years)
- **Q1:** after year 100, **98% of lost knowledge is lost when the holder dies**; only 2% through the 12-slot memory
  pushing it out. Knowledge isn't forgotten; it is never passed on.
- **Q2:** the founders' knowledge was shared and kept; what the world's own people invented after year 100 almost
  never outlived its maker (3%).
- **Q3 (the surprise):** from years 0–10 to 100–200, more people **could** make things (feasible rose) and more
  **weighed** making, but they **chose** it far less: about 1 time in 800 when weighed, against 1 in 40 at the start.
  The choice carries the whole decline. Foraging wins 68% of the time.
- **Q4:** food from tools fell because almost nobody holds one (97% of the fall); tools work as well when used. 98%
  of tools are made by their user, and tools almost never pass between people. Replacing a lost tool within a year fell
  from 59% to 7%.
- **Q5:** children take up 41%, then about 27%, of their carers' useful recipes, and that never rises.

**Evidence contrast:** forager children get real and child-sized tools early, often made or given by others ("opportunity
scaffolding", Lew-Levy et al. 2020/2022; Hewlett & Roulette 2016). They learn by a mix of watching, play and teaching,
and adults subsidise their unproductive early practice (Kaplan et al. 2000). In ACL a child only ever holds a tool it
made itself.

## 6. Now: MK1, "Why is making not chosen?" (frozen 27 Oct 2026; read-only; 32 worlds × 200 years; about to run)
An observer replays each decision exactly and splits making's score into worth, diligence, hunger, habit and thought,
against all other options (the full softmax). Three hypotheses, which can all hold:
1. **Low-skill trap:** low skill → poor tools → low learned worth → making loses → no practice.
2. **Opportunity cost:** foraging simply pays more, even for the skilled.
3. **Delayed-benefit failure:** tools pay over a year, but the learner doesn't see it.

Also logged: the offer gate (why making is not even offered), matched early-against-late comparisons, and a
descriptive benefit-cost estimate for tools made.

## 7. Other threads
- **Fly brain:** the FlyWire connectome. GPT's advice, which the creator chose: borrow learning principles (the
  mushroom body's sparse coding, several timescales, opposing memories), not the whole connectome, and only if MK1
  and the follow-ups show a missing general learning mechanism.
- **Other natures:** later, one deep law changed at a time, frozen, never tuned, to test which laws are truly needed.
  Also an idea of moving an agent between natures as a test of a general mind (cross-nature transfer).
- **Minds:** ACL's people have no concept of death; they fear specific animals. GPT's view: emergent fear of death is
  not a headline Bob marker. What matters is a self-model, prospective reasoning, and learning to invest effort for
  benefits that come later.

## 8. What would help
When asked, give your own view: where Claude or GPT may be wrong, what is missing, and what you would do. Be concise and
critical.
