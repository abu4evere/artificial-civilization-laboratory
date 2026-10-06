# ACL roadmap: the pathway

Read this first when the project feels lost. It says where ACL is, what comes next, and how each next step is decided.
It is updated after every experiment, like the book.

**Last updated:** after E13R (October 2026).

![The ACL roadmap: stages 0 to 2 done, stage 3 (transmission) now, with E13R's three outcomes fixed in advance; stages 4 to 8 ahead](docs/roadmap.png)

*The picture is drawn by [`docs/make_roadmap.py`](docs/make_roadmap.py) (also as [SVG](docs/roadmap.svg)). After each
experiment, edit its stage list and run `python docs/make_roadmap.py`; the book uses the same picture.*

---

## The goal, in one line

Civilization emerging in a world where **nature is programmed and culture is written by nobody**: people who keep,
pass on and build on what they learn, until their practices outgrow any one life.

## Where we are

| stage | question | status |
|---|---|---|
| 0. The world | Is there a world worth living in? | **done** (physics, seasons, bodies, minds) |
| 1. Culture appears | Does anything cultural emerge unscripted? | **done** (E1–E5: traditions, trust, stories) |
| 2. Why it stops | Where does the chain from possible to practised break? | **mostly done** (E6–E12) |
| 3. Transmission | Can a useful practice pass between adults? | **in progress:** a habit passes, a plan does not; now: why food does not last through winter |
| 4. Persistence | Does it last when nobody is there to copy? | next |
| 5. A people's practice | Does it become a tradition of the whole people? | later |
| 6. Scale | What do larger, connected populations keep? | later |
| 7. Accumulation | Do practices and tools build on each other? | later |
| 8. Society | Specialisation, trade, rules made by the people | far |

### What stage 2 found (the chain, in one paragraph)

Winter kills, and autumn offers enough to prepare (E8). People could learn to expect winter, but faintly, and those who
did prepared (E9). A carer's store protects their children five-fold (E9.2). But preparing removes the hunger that taught
it, so planners stop (E9.3, E9.4). Loss and witnessing barely move people (E10). Stories reach everyone, too faintly
(E11). Planners were seen and respected, and not copied, because no adult could copy another (E12). Copying the visibly
successful gave the strongest lead yet, but its safeguard could not be measured (E13). E13R measured it: the copying acts
only through the watcher's own habit, and what passes between adults is a general habit of foraging while moderately
stocked, learned from anyone better fed, not winter preparation. Children were not saved.

---

## Stage 3, now: E13R and what follows it

These branches were fixed before E13R's result, so the path could not bend to fit what came out.

**E13R result: B replicates (R2, R3, R4 held), N carries it.** The headline (repeat planning) failed, neighbours did not
change and children were not saved. **Branch taken: "B replicates, N carries it".** Before stage 4, the assistant
recommends a read-only autopsy: why better-stocked carers did not protect their children, and whether the spread habit is
linked to preparation at all. **Autopsy done** (`experiments/E13R_replication/autopsy/findings.md`): stocked carers
still protect children, but at every food level children in the copying worlds starved more; the copied habit is
year-round, not autumn; people enter winter with more food (16 of 16 worlds) and end it with none. Copying did not help
winter. What is missing is not getting food but making it last until spring.

**Branch changed by the creator (after the autopsy):** instead of stage 4 (testing whether the copied habit persists),
stay in stage 3 and **investigate why food does not last through winter**. Reason: the habit E13R found is not
preparation and did not help winter, so making it persist would not move the project; the autopsy points to keeping
food, not getting it. Recorded openly, as a change made after the result and why.

**W1 (winter ledger) done** (`experiments/W1_winter_ledger/findings.md`): food does not fail to last; almost none is
held. Winter is lived hand to mouth (winter gathering covers 102% of winter eating; stock at the start, 14%). The median
family holds 11% of its winter need; rot is minor; stashes, the only way a family can hold a winter, are almost unused.
People gather about what they eat in every season.

**S1 (stashing decisions) done** (`experiments/S1_stash_decisions/findings.md`): stashing fails three gates in a row:
rarely eligible (food above two weeks' household need in 13% of adult-weeks, 2.7% in autumn), often displaced (a
material takes the one put option in 28% of eligible weeks), usually outscored (5.4% of offers; beaten by giving 39%,
talking 23%, joining 17%, foraging only 4%). Stashers learn it kept food better than carrying it, never that it saved a
winter; the belief spreads. The creator's hypothesis (reward values only present hunger) is partly supported: put earns
no immediate reward and its habit is a quarter of foraging's, but the strongest rival is social.

**G1 (who receives the food) done** (`experiments/G1_who_receives/findings.md`): 72% of gifts go to family, a third
to siblings (16 of 16 worlds); 63% to people with under half a week of food; 53% is repayment; strangers 1.4%. A
family's surplus is held in its members' stomachs and debts, not in a store.

**P1 (risk pooling) done** (`experiments/P1_risk_pooling/findings.md`): the family network pools risk (family food cuts
the poorest members' winter starvation 25-fold; deaths rarely amid plenty; giving does not leave givers short) but pools
almost nothing (help follows ~10% of hungry weeks; families hold a ninth of their winter; more sharing, no better
winters). The bottleneck is not distribution but how much there is to distribute when winter comes.

**U1 (upstream surplus) done** (`experiments/U1_upstream_surplus/findings.md`): the food is on the land and barely
touched; autumn is foraged like any season; no carrying limit, little moving. People stop when fed: foraging falls from
86% of autumn weeks (under half a week of food) to 6% (two to four weeks). In the code, hunger is 1 − weeks ÷ 2, zero at
two weeks, exactly the line where stashing becomes possible. **The chain from E8 to U1 now runs to one line of nature:
when a person stops feeling hungry.**

**N1 candidates written** (`experiments/N1_satiety/candidates.md`, no code, no experiment): thirteen readings of "what
should a satisfied person feel?", each judged for nature, culture, scripting risk, human capacity and leak. C6 (seasonal
instinct) and C9 (food brings standing) rejected; C3 (smooth satiety), C4 (insecurity learned from experience), C11 (the
body as a store) and C8 (a longer mind, not satiety) stand out.

**N1 evidence and least-change documents written** (`experiments/N1_satiety/evidence.md`, `least_change.md`; no code,
no choice): human evidence verified against PubMed and Crossref. Strong for C11 (body reserves), strong capacity but
weak use for C8, moderate and mixed for C4, moderate and general for C3. The least change that addresses U1 directly is
C3 scoped to `food_hunger` (one expression, three uses, one number, zero check possible). Caution: human
immediate-return societies store little despite full foresight, so C0 (no change to nature) stays on the table.

**Reframed (the creator, after N1's evidence):** U1 identified a candidate bottleneck, not a proven flaw. ACL may have
converged on an **immediate-return** mode of life (Woodburn 1982), a normal and stable human pattern, rather than a
broken one. The question shifts from "what should satiety be?" to **"under what conditions do delayed-return societies
emerge, and does ACL's world contain them?"** **N2 design document written** (`experiments/N2_immediate_delayed/design.md`):
ACL already shows immediate consumption, little storage, reciprocal kin sharing and no binding commitments; it lacks
sharing on demand, possession of stores and any capacity to ask or promise; whether its world offers dense, predictable,
storable resources is unmeasured. The N1 candidates stay, as hypotheses to weigh against this one.

**D1 (is delayed return adaptive in ACL's world?) done** (`experiments/D1_delayed_return_world/findings.md`).
Part A, largely no: food is predictable (tile r 0.90) and storable as seed, but not dense (the richest 10% of land holds
24%), and winter is barely lean (land food per person 504 against 582 in autumn); the world favours immediate-return
living. Part B, yes but: sowing returns 2.36 food per seed and is repeated (77% sow again), but 52% of its crop is
eaten by non-kin, sowers' belief falls more often than it rises, and it is 1.6% of food. **By the creator's rule,
changing people's psychology is premature.**

**D2 (why sowers learn failure) done** (`experiments/D2_sowing_learning/findings.md`): they don't. D1's measure was
confounded with belief fading (corrected in D1 and the book); setting fading aside, experience raises sowers' belief in
55% of sowings and lowers it in 30%. But returns are not captured: the sower's family gets back 1.08 per unit of seed
(autumn sowing 0.84, a loss); others harvest more. Sowing explains part of the absence of delayed return (no
possession), not all of it (it stays small, likely held by S1's gates; and winter is barely lean). **Priority as set by
the creator: N3 evidence review next, then an L1 pilot if the evidence supports it, then L6.**

**Rule for property (the creator, after D2):** possession is a dangerous lever. "Storage didn't emerge → add ownership
→ storage emerges" would write the answer in. If property is studied, the same order as everything since E13R applies:
read-only first, map it completely, then candidates, then evidence, then the least change, then an experiment.

**N3 candidates written** (`experiments/N3_lean_season/candidates.md`, no code, no choice): nine readings of a harder
lean season, judged for realism, tuning risk, targeting, effect from the rules, viability and continuity. Why winter is
mild now: winter regrowth roughly cancels dieback, and a forage week only bites when a tile falls below about 20. L1 (no
growth in winter) is the cleanest but may change little by arithmetic; L6 (colder places, leaner winters) the most
realistic; L2 and L3 bite but turn on dials; L8 (crop survives winter) rejected; L7 is about people, not the world.
**Awaiting the creator.**

| E13R result | what it means | next step |
|---|---|---|
| **L1 or L2 fails** (hard stop) | the copying code does something beyond the watcher's habit | fix the code; rerun E13R. No outcomes read. |
| **B does not replicate** (R2 or R3 fails) | E13's lead was specific to its four worlds | go back to stage 3 with reading Phase 2.5: a different learning signal (Ndousse), group-level transmission (social protocell), or children learning from successful adults |
| **B replicates, N carries it** ← **taken, then changed** (see above) | what spreads is a general "forage while things are good" habit | stage 4, testing the general habit |
| **B replicates, P carries it** | planners pass on a preparation practice | stage 4, testing the planners' practice |
| **B replicates, both or mixed** | no single source | stage 4; the source question stays open in the book |

## Stage 4: persistence (the next big question)

**Question:** once people have learned from others, does the practice survive when the models are gone?

Both Ndousse (2021) and Cook (2024) found that learners can become dependent on whoever they copy. A practice that
vanishes with its models is not culture.

Candidate designs, to be chosen after E13R, not before:
- **Switch copying off** halfway through a run. Does preparation stay above the control?
- **Generations:** do the children of people who learned by copying prepare more than other children, with copying off?
- **Remove the models:** do neighbours of planners keep preparing after the planners die?

**Done when:** a practice learned socially stays measurably above the control for at least a generation without copying.

## Stage 5: a people's practice

**Question:** does preparation become a tradition, held by many people across decades, the way ACL already measures
traditions (three or more people in every ten-year sample)?

**Done when:** preparing for winter meets ACL's own definition of a tradition, and children's winter deaths fall because of
it (read last, only if the links before it hold).

## Stage 6: scale

**Question:** do larger, connected populations keep more? Henrich (2004), Kline & Boyd (2010) and Derex (2013) all say
population size and connection decide how much culture survives, and ACL's E4 found isolation in small peoples.

Likely needs faster worlds (see JaxLife and Craftax for how). **Done when:** 100 connected people against 30 has been
tested under the same method.

## Stage 7: accumulation

**Question:** with transmission working, do tools and practices finally build on each other? This returns to the problem
ACL hit in E6 to E8: the memory ceiling, the degenerative loop, and tools that pay too little. Tomasello's ratchet and
Mesoudi's acquisition costs are the theory to read first.

**Done when:** something is made that depends on something else that was learned from someone else.

## Stage 8: society

Specialisation, trade, leaders and rules made by the people themselves (README, "Not yet"). Not planned in detail;
each earlier stage will change what this one looks like.

---

## Rules that never change

These hold at every stage, whatever the results:

1. **Nature is programmed, culture is written by nobody.** Never write a behaviour you hope to see.
2. **Copying carries behaviour, never instructions or expectations.** Stories carry experiences, never instructions.
3. **Freeze predictions before any code**, tag the commit, and never edit them after the results.
4. **Pilots first**, read-only, before choosing a design.
5. **Leak tests are hard fails**, and every test states its minimum sample. An empty test counts as failed.
6. **Measurement never touches the world** (probe read-only, checked by state hash).
7. **New code with the mechanism off must reproduce the old world exactly.**
8. **Read in the fixed order:** validity, then causal links, then deaths last.
9. **Cap every conclusion** at what the evidence shows.
10. **Failures are published as failures.** Never change a verdict after seeing it.
11. **The creator signs off every design** before it is frozen.

## The cycle for every experiment

1. Name the question, from this roadmap.
2. Autopsy or pilot (read-only).
3. Candidates document; the creator chooses.
4. Pre-registration; the creator signs off; freeze and tag.
5. Code, tests, zero check.
6. Write the analysis script before any outcome exists.
7. Run, with the safeguards first.
8. Report in the fixed order.
9. Update the record: `results.md`, `experiments/INDEX.md`, the book chapter and timeline, this roadmap.
10. Commit and push.

## How not to lose track

- **One question at a time.** No new mechanism starts until the current experiment is resolved and recorded.
- **Every idea goes in the parking lot below**, not into the current experiment.
- **When in doubt, open this file**, then `experiments/INDEX.md`, then the latest `results.md`.
- **Update this file after every experiment:** move the "now" line, and record which branch was taken and why.

## Reading alongside the stages

| stage | read (see [RESOURCES.md](RESOURCES.md)) |
|---|---|
| 3. Transmission (now) | Phase 2.5: Ndousse, Cook, Dalmaijer; Henrich & Gil-White; Kendal |
| 4. Persistence | Cook; Ndousse (dependence); Bhoopchand |
| 5. A people's practice | Boyd & Richerson; Mesoudi; social protocell |
| 6. Scale | Henrich 2004; Kline & Boyd; Derex; Craftax, JaxLife |
| 7. Accumulation | Tomasello; Mesoudi (acquisition costs); Kirby (iterated learning) |
| 8. Society | Sugarscape (as a contrast); Melting Pot; Neural MMO |

## Parking lot (ideas held, not scheduled)

- Energy cost for complexity, and senses that can be discovered (from Werld).
- Faster worlds on the GPU (Craftax, JaxLife).
- Measuring identity: copy a person into another world and see how much of them persists (Part VIII, open questions).
- Why E6's worlds were harsher (never found).
- Rival identities when separate peoples meet.
- **A language barrier.** Today "talk" passes stories, reputations, places and know-how perfectly between any two people,
  even strangers from peoples that never met: in effect, telepathy across groups. Stories and teaching could get through
  only partly between people who share little (for example, limited by familiarity or by shared marks). Matters before
  any study of separate peoples meeting.
- **Wariness of strangers, as nature?** A stranger now starts at zero on every feeling, with no caution toward the
  unfamiliar. Whether a mild inborn caution belongs in ACL's nature is an open question: writing it in risks scripting
  group conflict, so it needs the creator's sign-off and a careful design.
- Writing ACL up as a paper (Hughes et al. for framing).
