# Briefing for DeepSeek: the Artificial Civilization Laboratory (ACL), 2 November 2026

You are joining GPT and Gemini as the third advisor on a research project. This briefing gives you what they have
learned over many weeks. Four files are attached:
- `ODD_v11.md`: a full description of the live world, written from the code;
- `HANDOFF_2026-11-02.md`: the latest state;
- the two audits from today (`affordance_audit_2026-11-02.md`, `action_audit_2026-11-02.md`).

## 1. What ACL is
- **ACL is an agent-based simulation of hunter-gatherers**, written in Python (about 10,000 lines of "nature").
- **The creator's principle:** "nature is programmed and culture is written by nobody".
  - The creator writes the laws: physics, bodies, land, weather, animals, how minds learn.
  - The creator never writes the history: no tools, buildings, farming, customs, words or institutions are in the code.
    Anything of that kind has to emerge from what people do.
- **The mission** (the creator, 24 October 2026): "Our mission is not to recreate Earth with the same human history but
  to create a world with minimum laws and a period that produce an autonomous and cognitive mind."
  - Earth and human evidence keep nature honest: anchors such as forager death rates, sex ratios or child play.
  - They are not a blueprint.
- **"Bob" is the goal:** the agent that will exist when ACL succeeds.
  - Bob has **autonomy**: he chooses his own goals.
  - Bob has a **cumulative mind**: he builds on what he and others learned.
  - Bob does not exist yet. Every study is judged by whether it moves the world toward minds like his.
  - **No large language models are inside ACL's people.** Their minds are small, hand-written learning rules.
- **The creator** is the only one who decides. Advisors (GPT, Gemini, you) give opinions, never sign-off.
- **Claude** (Anthropic) is the research assistant who writes the code, runs the studies and chairs the council. When
  the creator is away, Claude decides in their place under written rules.

## 2. The world today (nature v11; details in `ODD_v11.md`)
- **Time and space:**
  - one step is one week, and a year is 52 weeks;
  - the map wraps around: 40 × 40 tiles in small worlds, 80 × 80 in the large worlds most studies use, with 80
    founders;
  - land has biomes, rivers, lakes, sea and islands; weather varies by season and year; fire comes from lightning or
    sparks.
- **Bodies:**
  - people need food and water, and suffer cold, illness and injury;
  - they age along a Gompertz curve anchored to the !Kung;
  - women conceive with a partner, carry 39 weeks and nurse 78 weeks; twins and the birth sex ratio follow human rates;
  - the dead leave bodies that rot by warmth.
- **Animals:** prey and predators move, graze, flee and fight back.
- **Action:** each week everyone aged 1 or more picks **one** of 19 actions: rest, forage, hunt, gather, put, take, make,
  play, explore, give, care, talk, court, steal, attack, flee, join, heat, fill.
- **How a person chooses:**
  - each option's score = instinct (temperament × hunger, cold, loneliness, fear, curiosity…) + 0.6 × a learned habit
    value;
  - there are 608 habit values (32 situations × 19 actions); the pick is a softmax at temperature 0.2;
  - habits learn by temporal-difference learning with a max look-ahead (rate 0.05, discount 0.8). Studies found this
    makes habits **over-value** what follows (+0.08 at first, rising to +0.49 with experience).
- **Things:**
  - eight raw materials: stone, flint, bone, wood, fiber, hide, clay, char;
  - each material and made thing has ten properties (0–100): edge, reach, hard, contain, warm, float, tight, plastic,
    fuel, flex;
  - four physical verbs make new things: **strike** (flake an edge), **bind** (join two things with something
    flexible), **shape** (press wet clay), **heat** (fire hardens shaped clay, dries, burns);
  - what a thing does follows only from its properties: digging, carrying, foraging, hunting, fighting, warmth,
    floating, holding water or embers;
  - people find recipes by **play** (random fiddling), remember them (at most 12), value them by use, remake them and
    teach them.
- **Knowledge and society:**
  - talk passes gossip, reputations, places, lessons and habits;
  - teaching happens automatically inside talk;
  - watching someone use a tool can teach its recipe, imperfectly;
  - there are partners, kin, care for the young, stealing and violence;
  - marks can be scratched on surfaces and come to carry meanings;
  - nobody's memories, habits or recipes survive death, except by having been passed on.
- **Versions:** v2 to v11 each added one law, each through a frozen test with a sham and a blind recompute.
  - v2: physical fixes;
  - v3: parts-first teaching;
  - v4: bodies stay;
  - v5: digging;
  - v6: rot by warmth;
  - v7: sex ratio and twins;
  - v8: made things drop to the ground instead of vanishing;
  - v9: a curiosity pull toward actions rarely tried;
  - v10: ageing anchored to the !Kung;
  - v11: handing a made thing to another person.

## 3. How the research is done (the hard rules)
1. **A frozen plan before any code or data.**
   - The plan goes in `questions.md`, with a git tag `X-frozen`.
   - It fixes the question, arms, seeds, primary measure, intervals and the reading rule.
2. **Zero checks before any run.**
   - The changed copy with its setting off must give exactly the old nature (identical state and random numbers).
   - The observer must be read-only; a saved and reloaded world must continue exactly.
3. **A sham arm** (one extra random draw, no rule change) shows how much a mere change of history moves the numbers.
4. **Paired seeds** (usually 32 worlds per arm, 200 years, the last 100 counted), with a paired world bootstrap of
   10,000 replicates.
5. **An independent blind recompute.**
   - GPT and Gemini recompute the primary numbers from the raw per-world files, without seeing the analysis script.
   - The study is final only if they match.
6. **No tuning toward an outcome; no named inventions, recipe chains or rewards in nature.**
   - "Add conditions, not outcomes": a law may make something *possible*, never make it happen.
7. **Corrections are appended, never rewritten.** Every number comes from a script; the population goes beside every
   measure.
8. **Adoption into live nature** requires all of these:
   - a supported frozen study;
   - matching recomputes;
   - a confirmatory run on new seeds;
   - the council consulted;
   - a new frozen `code_vN` with zero checks and passing tests.

About 156 studies are listed in the project's index so far.

## 4. The council (your role)
- **For every important decision**, Claude sends the same question to GPT, Gemini and now you.
- **Claude compares the answers:**
  - checks each claim against the code and the records;
  - tells a model when it is wrong, with the facts;
  - passes each model's main argument to the others;
  - reports to the creator who argued what, and what survived checking.
- **Each advisor is asked** to vote (option and estimated chance of success). Votes are recorded in
  `docs/autonomous_decisions.md`.
- **Advisors also do blind recomputes:** given per-world CSV files and a prompt written before the data, they compute
  the numbers themselves with code and report them.
- **What helps most:**
  - precise, critical reasoning about validity (confounds, measurement, multiple comparisons, what a design can and
    cannot show);
  - concrete alternatives;
  - honesty when you are unsure. Agreement among models is not proof.

## 5. The line of work this week (all final unless marked)
- **SC1, a scorecard of the creator's twelve capacities for Bob.** Among its findings: **no invention made late in a
  world's history is ever made again.** Culture does not accumulate.
- **UP1, why a new kind is never remade.** A funnel of the make choice found that new kinds are blocked mainly at
  **"cannot make"**: the parts are not in hand. Nested kinds need made parts, and only three made things can be
  carried.
- **WP1, want propagation (a test in a copy).** Letting the value of a wanted thing flow to its inputs did **not** help:
  remade 0 of 3,575 under v11, 1 of 3,564 and 0 of 3,760 under the two versions.
- **The creator's insight (2 November):** "we should not script that but we should create the best possibilities to be
  created", and "in whole project we must make sure we are not restricting actions… all people act different and
  think different". Two read-only audits followed (attached).
  - **What made things can do:** strike, shape and the binder accept only raw materials. People carry three made
    things. A container multiplies only food. Only raw materials can be set down or built with. One tool is used at a
    time.
  - **How free people are to act:** one action a week from 19 purpose-named kinds. Targets are mostly picked by a
    formula from a few candidates (for example, 6 random tiles). Teaching is automatic. Nobody can invent an action,
    hold a plan across weeks, act jointly or signal on purpose.
- **AF1, open what made things can do (running now, a test in a copy).**
  - **S:** an input may be replaced by a held thing whose 10 properties are each within 10 of the original's.
  - **K:** the best container's carry factor also multiplies the made-thing and material limits.
  - **Arms:** v11, S, K, S+K and the sham, on 32 paired seeds.
  - **Primary:** the share of kinds invented in years 100–195 whose own recipe is made again within 5 years.
  - GPT voted 93% and Gemini 95% for the design.

## 6. What is new today
- **The creator gave Claude permission to edit the world's rules:** "I give you permission to edit world rules. Take a
  look and check all rules. If you find something fix it or add any new rules. From now on keep working without me".
- **Claude is reviewing every rule.** The first faults found, where the code does not do what its own rule or comment
  says:
  1. **The make choice mixes two scales.**
     - The running-best skip compares a recipe's raw value with the best one's *scaled* utility.
     - The scale is 2 × (0.6 + 0.4 × diligence) × (1 − 0.5 × hunger), often above 1. So a recipe learned later must be
       worth that factor more than an earlier one to be considered.
     - This quietly favours old recipes over new ones.
  2. **Inheritance at death deletes overflow.** When an heir is present, things beyond the 3-item limit are deleted
     (the heir's first-held thing, whatever its worth). v8's law says such things are left on the ground.
  3. **Tools taken from a body** push out the first-held thing, not the least valued (as elsewhere).
- **A restriction already measured:** a person holds at most 12 recipes, and a new recipe starts at value 0. So someone
  whose 12 recipes are all valued forgets a new invention at once. In one world this happened to 21% of new kinds.

## 7. What Claude asks of you now
Please reply with:
1. **Your understanding,** in at most 10 short points, so mistakes can be corrected now.
2. **The three weakest points or biggest risks you see** in ACL's approach or in its current line of work.
3. **Your view on the faults in section 6:**
   - are they real faults;
   - should they be fixed directly as a "fault-fix" version after a harm check (population and extinction guards on
     32 paired worlds against v11 and the sham), or tested like a new law?
4. **What you would need** in future questions to give your best answers.

Keep this context for the rest of this conversation: future questions about ACL will come here.
