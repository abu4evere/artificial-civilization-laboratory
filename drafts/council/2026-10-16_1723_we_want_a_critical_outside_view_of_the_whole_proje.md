# Council: We want a critical outside view of the whole project so far, and three concrete next steps.

THE PROJECT. A world of sma

Asked 2026-10-16 17:23. **Ideas only; not decisions.** the assistant sorts these against ACL's rules before anything is used.

## The question

We want a critical outside view of the whole project so far, and three concrete next steps.

THE PROJECT. A world of small islands on a 40 by 40 grid. Twenty founders, no tools, no knowledge. People have programmed bodies (hunger, thirst, cold, illness, ageing, pregnancy), drives and temperament, and learn habits by simple reinforcement learning (a table of 32 situations by 17 actions). Materials have physical properties; anything tied, struck, shaped or heated becomes a new object whose uses are never named in the rules. People talk (gossip, stories, where water is, how to make things), give gifts, store food, mark things, pair up, raise children. A historian outside the world names things after the fact and never changes anything. Runs are exactly replayable. Every study is frozen in writing before it runs (predictions, thresholds, a sham arm that changes nothing but one random draw), uses fresh seeds, and wrong predictions are kept on record.

WHAT WE FOUND (October 2026):
1. Culture appears and then freezes. Over 1,000 simulated years, every kind of tool ever made first appeared within the first 11 years; nothing new for 990 years. Inventions are lost when their only holders die (one child fired the only clay pot in a thousand years and starved 14 weeks later). A vessel was invented and used 104 times as a carrier but never filled with water by its maker, who lived beside water and was rarely thirsty; the thirsty people never saw it. Tools add little to food (a few percent), so the world gives little reason to keep or improve them. Watching others led to copying only 7 times in 1,770 observations.
2. Worlds die out, mostly because people cannot find partners. About a third of 20-founder worlds die within 120 years. Giving people perfect partner search removes about half of that. Bands rarely meet: between-lineage meeting is about 0.05 per adult pair-year in today's world, and almost zero in a larger world with 80 founders, even though that larger world survives best because its bands are big enough on their own.
3. Sensitivity: survival depends strongly on unanchored numbers, above all how far people can see (halve it: 49 of 64 worlds die; double it: 8 die; normal: 22). A tile has no measured size, so sight cannot be anchored in metres. Forager data (Binford's 175 fully mobile societies) give: camps move every 4.3 weeks, about 28 km each move; dispersed camps of about 16 people, aggregated about 37. In our world, people move every week, up to 3 tiles, and see 4.
4. Habits: learned habits steer about one adult choice in seven. More than half of an adult's habit table was copied wholesale from others in conversation; own experience 37%. Copying only the habits for the speaker's current situation makes habits mostly one's own (65%) with no change in survival. Everyone's habits end up very alike, and most of that sameness remains even with no copying at all (we suspect the shared environment, unproven).
5. Identity: swapping one part of a person (memories, habits, relationships, skills, temperament) on a copy of the world never changes them beyond chance; swapping everything except temperament does.
6. We just fixed four unintended shortcuts (people walking toward absent loved ones they could not know the location of; a hidden land bridge at diagonal corners of water; people left standing on open water when a raft broke; a record-keeping flaw). 256 new worlds: no change in survival (94 vs 97 died out).

QUESTIONS (answer each briefly and concretely; say what test would show you right or wrong; say when unsure):
A. What is the single biggest threat to the validity of what we have concluded so far, that we may not be seeing?
B. Cumulative culture freezes. Without adding any rule that names an invention or rewards progress, which conditions in the world (not in the minds) would most plausibly let knowledge accumulate, and what is the cheapest experiment to test one?
C. Our time step is a week, and people relocate every week, while real foragers move camp every month or so and forage out daily. Is that a problem for partner finding and for meeting other bands? How would you test whether it drives our extinction results?
D. What should we stop doing, or do less of?
E. If you could run only three more studies, which, in what order, and why?

## nvidia: nvidia/nemotron-3-super-120b-a12b

**A. Single biggest threat to validity**  
*Threat:* The model’s world is temporally uniform – resources renew at the same rate every week and there are no stochastic shocks (droughts, floods, disease outbreaks). Real hunter‑gatherer groups experience periodic resource booms and busts that create strong pressures to innovate, store, and share knowledge. If such variability is missing, the observed “culture freezes after the first decade” may be an artefact of a benign, constant environment rather than a genuine property of the emergence process.  

*Test:* Add a simple seasonal cycle (e.g., resource abundance high for 2 weeks, low for 2 weeks, repeating every 8 weeks) or occasional random resource shocks (e.g., 5 % chance each week that a tile’s yield drops to zero). Run a matched set of worlds with the same seed distribution and compare: (i) the timing and number of novel tool inventions, (ii) the persistence of those inventions over centuries, and (iii) survival rates. If inventions continue to appear beyond the first 11 years or survival improves markedly, the original conclusion is threatened; if nothing changes, the threat is less likely.  
*Uncertainty:* I am unsure how large the seasonal amplitude must be to produce a detectable effect; a pilot with a modest 20 % swing is a safe first step.

---

**B. Conditions that could let knowledge accumulate (no explicit reward rule)**  
*Plausible conditions:*  
1. **Durable, shareable artifacts** – objects that persist after the maker’s death and can be used by anyone who finds them.  
2. **Centralized storage or caching sites** – a location where tools are deposited and later retrieved, creating a “public good” that reduces the chance that an invention dies with its holder.  
3. **Overlapping generations with low turnover** – longer adult lifespans or slower ageing increase the window for transmission.  

*Cheapest experiment:* Introduce a single, immutable “storage pit” tile that any agent can deposit an object on (no cost) and later retrieve it from (no cost). The pit persists forever and is visible to all agents (sight range unchanged). Run otherwise identical worlds and measure: (a) the proportion of inventions that survive > 50 years after their origin, (b) the average number of uses per invention, and (c) any gradual improvement in efficiency (e.g., reduced hunger per use) across generations. If storage yields a clear rise in long‑term survival or incremental improvement, the condition is sufficient; if not, durability alone may be insufficient.  
*Uncertainty:* I am unsure whether mere visibility of the pit is enough or whether agents need a bias to deposit/retrieve (e.g., a habit that favors storing surplus). The test will reveal whether the simple affordance drives accumulation.

---

**C. Weekly time step vs. real‑world camp movement**  
*Problem:* Moving camp every week (≈ 1 tile per week) makes individuals change location far more often than real foragers (≈ once per month). This can (i) break nascent pair‑bonds before they solidify, reducing effective partner‑finding, and (ii) increase the chance that bands never encounter each other because each group’s trajectory is constantly reshuffled. Both mechanisms could exaggerate the extinction risk we see.  

*Test:* Create a variant where the decision to move is made only every *n* weeks (e.g., n = 2 or 4) while keeping the same weekly movement capacity (so when a move occurs the agent can still travel up to 3 tiles). Keep all other parameters identical. Compare three outcomes across many seeds: (1) proportion of worlds that go extinct within 120 years, (2) average inter‑band meeting rate (lineage‑pair encounters per adult‑pair‑year), and (3) average age at first reproduction. If lowering the movement frequency raises meeting rates and reduces extinction, the weekly step is driving the result; if there is no change, the step is less critical.  
*Uncertainty:* I am unsure whether the effect is linear in *n* or whether a threshold (e.g., moving only once per month) is needed; the two‑week and four‑week tests will bracket the likely range.

---

**D. What to stop doing (or do less of)**  
*Stop:* Treating the habit‑copying statistic (“learned habits steer about one adult choice in seven”) as direct evidence of cultural transmission without checking for alternative sources of similarity (e.g., convergent individual learning driven by identical environmental cues).  
*Do less of:* Adding ad‑hoc patches to fix individual simulation bugs (the four shortcuts) without a systematic regression‑test suite. Each patch risks introducing hidden dependencies that make it hard to tell whether a change in outcome is due to the intended fix or to an unintended side‑effect.  
*Alternative:* Implement a lightweight unit‑test harness that runs a set of “canonical” scenarios (e.g., a single agent with known hunger, a known water source, a known tool) and asserts expected behavior after each code change. This will catch regressions early and reduce the need for furtive patches.

---

**E. Three more studies – order and rationale**  

| Order | Study | Why it matters | Core manipulation | Primary read‑out |
|------|-------|----------------|-------------------|-----------------|
| **1** | **Movement‑frequency test** (see C) | Directly addresses the extinction driver we are most uncertain about; cheapest to implement (just change a decision timer). | Agents decide to move only every *n* weeks (n = 2,4) while retaining weekly movement capacity. | Extinction rate, inter‑band meeting rate, age at first reproduction. |
| **2** | **Durable shared storage** (see B) | Tests whether giving inventions a public, long‑lived medium can break the “freeze” and let cumulative culture emerge without any reward rule. | Add a permanent, visible storage pit where any agent can deposit/retrieve objects at zero cost. | Survival of inventions > 50 yr, number of uses per invention, any gradual efficiency gain across generations. |
| **3** | **Seasonal/resource‑shock regime** (see A) | Examines whether environmental variability — a known catalyst for innovation in real foragers — can sustain invention beyond the early burst and affect survival. | Impose a bi‑weekly high/low resource cycle or random weekly yield shocks (5 % chance of zero yield). | Timing/number of novel tools, persistence of tools over centuries, long‑term survival probability. |

*Rationale for order:*  
1. **Movement** is the simplest tweak and directly challenges the extinction explanation; clearing this up tells us whether we need to look elsewhere for survival drivers.  
2. **Storage** builds on the first outcome: if movement is not the main issue, we then test the most plausible structural lever for cultural accumulation.  
3. **Seasonality** is the most computationally expensive (adds time‑varying fields) and is best run after we have clarified the other two factors, ensuring any observed effect is not confounded by movement or storage artifacts.

---  

**Summary of concrete next steps**  
1. Run the movement‑frequency variants (n = 2, 4) and compare extinction/meeting metrics.  
2. Add a permanent storage pit and measure invention longevity and use efficiency.  
3. Introduce a simple seasonal cycle or random resource shocks and track invention dynamics over long horizons.  

Each step includes a clear, falsifiable prediction and a minimal implementation effort, letting us quickly see whether the current conclusions hold or need revision.

## nvidia: openai/gpt-oss-20b

**A.  The single biggest threat to the validity of our conclusions**

> **Unanchored perceptuo‑temporal scales** – the model treats sight, movement, and time as pure, unitless parameters that have no real‑world calibration.  Because the grid is 40×40, one tile can mean a few metres or a few kilometres, a week can mean a day or a month, and “seeing 4 tiles” can mean a 20 m view or a 20 km view.  This means that the *relative* importance of tools, partner‑search, and social learning can be arbitrarily high or low, and we may be seeing artefacts of the chosen scale rather than genuine phenomena.

**Test that would confirm or disprove this**  
Create a calibration experiment:  
1. Pick a realistic forager baseline (e.g., Binford’s 28 km/month camp‑move, 4 km/day foraging).  
2. Translate these into grid units by assigning a fixed physical size to a tile (e.g., 1 km per tile) and a fixed time step (e.g., 1 day per step).  
3. Run a set of worlds with these calibrated parameters and compare survival, tool‑use, and partner‑finding rates to the uncalibrated runs.  
If the patterns (e.g., cultural freeze, high extinction) shift substantially, the unanchored scales are a major threat; if they remain essentially the same, the threat is smaller.

**When I’m unsure** – if the calibration produces wildly different results but still shows cultural freeze, we’ll need to examine which underlying rules (e.g., learning table size, habit copy rate) are still the real culprits.

--------------------------------------------------------------------

**B.  Conditions that would plausibly let cumulative culture grow **(no rule‑level “reward” or “invention” added)**

| Condition | Why it matters | Cheapest experiment |
|----------|---------------|----------------------|
| **Tool durability → repeated use** | If a tool lasts many steps, there is a tangible incentive to keep it. | Add a “durability” attribute that decrements each use but never reaches zero for one simple tool (e.g., a stone stick that can be used 10 times). Run 10 worlds; count how many worlds keep the tool on the table for > 5 steps and whether subsequent generations adopt it. |
| **Environmental hazard that requires a tool** | A direct fitness payoff (e.g., a fire that burns edible plants, a shallow water crossing) creates an immediate need for a tool. | Add a “fire” event that destroys edible plants in a 2‑tile radius unless a “fire‑proof” tool (a stone shield) is used by at least one adult. Run 10 worlds; measure if the tool is ever created, used, and retained. |
| **Social learning pressure** | If learning a tool confers a *social* benefit (e.g., better gossip score, higher chance of being chosen as a partner), use can spread. | Modify the habit‑copy rule: when an adult sees a tool in use, add +0.5 to the “social value” of the action that produced the tool, making it more likely to be copied. Run 10 worlds; track tool persistence and overall survival. |
| **Population density / group size** | Smaller groups have more “noise” in learning; larger groups can reinforce a behaviour. | Increase founder count to 40 (double the current max) while keeping all other parameters constant. Run 10 worlds; compare tool‑use persistence and extinction rates. |
| **Tool‑dependent resource access** | If a tool unlocks a resource that is otherwise inaccessible, it becomes useful. | Add a “stone axe” that can chop a “wood” tile into “wooden planks”, which can be used to build a simple shelter that reduces cold damage. Run 10 worlds; see if the axe is invented and kept. |

**Test to show the idea right or wrong** – If the cheap experiment (e.g., durability) leads to > 50 % of worlds retaining a tool for > 5 steps and those worlds have higher survival, the condition is a plausible driver of cumulative culture. If not, the condition is likely insufficient.

--------------------------------------------------------------------

**C.  Does the weekly time step distort partner‑finding and band‑meeting?**

> **Yes, it probably inflates partner‑search difficulty and reduces inter‑band encounters** because people move every week while in reality most foragers move a camp once a month. The effect is two‑fold:  
> * (1) The “search radius” in terms of real distance is much smaller per unit time, so partners are harder to locate.  
> * (2) Bands are effectively “frozen” in a local neighbourhood for several simulated weeks, preventing them from spreading out enough to meet others.

**Test**  
1. **Create a “slow‑move” variant**: keep the same 40×40 grid but change the movement rule so people relocate only every 4 simulated steps (≈ month).  
2. **Create a “fast‑move” variant**: keep the weekly move but double the sight range to 8 tiles.  
3. Run 10 worlds for each variant, measuring (a) partner‑finding success rate, (b) inter‑band meeting rate, (c) extinction rate.

If the slow‑move variant shows significantly higher partner‑finding and lower extinction, the weekly time step is a true problem. If the fast‑move variant with doubled sight improves outcomes, it suggests that sight distance (not time step) is the main driver.

--------------------------------------------------------------------

**D.  What to stop doing / do less of**

| Current practice | Why it may be harming validity | Suggested change |
|------------------|------------------------------|------------------|
| **Swapping entire copies of people to test “identity”** | It introduces massive, non‑natural perturbations that may mask subtle social dynamics. | Stop large‑scale swapping; instead, use targeted swaps (e.g., only habits or only memories) and in a controlled, small set of worlds. |
| **High frequency of gossip** | Gossip is the *only* social learning channel, which over‑weights it relative to observation or imitation. | Reduce gossip frequency or give it a smaller learning weight; introduce observation‑based learning (e.g., a “watch” action that copies the observed action with probability). |
| **Small grid (40×40) with no scaling** | It forces a high density of individuals, increasing competition and reducing realistic movement patterns. | Expand the grid or add “empty” territory, or at least run a subset of experiments on a larger grid. |
| **One‑size‑fits‑all “habit table” (32×17)** | It limits behavioural richness and may artificially homogenise actions. | Increase the number of situations or allow dynamic expansion of the table as new contexts arise. |
| **No feedback loop for tool durability** | Tools disappear immediately, preventing any cumulative advantage. | Implement durability and a simple repair mechanic (e.g., an “repair” habit that can restore a tool’s durability at a cost). |

--------------------------------------------------------------------

**E.  Three more studies to run (in order)**

1. **Introduce environmental hazard that creates a *direct* tool benefit**  
   *Why*: It tests whether a clear fitness payoff can seed cumulative culture without scripting a reward.  
   *Method*: Add a “fire” that burns edible plants in a radius unless a “fire‑proof” tool is used. Run 10 worlds, track tool invention, use, and persistence.  
   *What we learn*: Whether a single, immediate benefit is enough to seed and maintain tool use.

2. **Calibrate sight, movement, and time to real forager data**  
   *Why*: Removes the biggest threat identified in A and checks whether the observed cultural freeze is a scale artefact.  
   *Method*: Translate Binford’s camp‑move and foraging rates into tile and step units; run 10 worlds; compare survival and culture metrics.  
   *What we learn*: Whether the current model’s time/movement frequencies are plausibly responsible for partner‑finding failures and cultural stagnation.

3. **Experiment with tool durability and repair**  
   *Why*: Durable tools create a persistent incentive to keep them; repair adds a maintenance loop that can support cumulative culture.  
   *Method*: Give each tool a durability counter that decrements on use; add a “repair” habit that can restore durability for a small cost (e.g., consuming food). Run 10 worlds; measure tool longevity, adoption rates, and survival.  
   *What we learn*: Whether the ability to maintain tools promotes cultural accumulation and reduces extinction.

These three studies together will test the core mechanisms we suspect (environmental pressure, realistic scale, tool persistence) and either confirm that our earlier conclusions were artefacts or reveal the missing ingredients needed for cumulative culture to emerge in a fully unscripted agent‑based world.

