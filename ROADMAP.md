# ACL roadmap: the pathway

Read this first when the project feels lost. It says where ACL is, what comes next, and how each next step is decided.
It is updated after every experiment, like the book.

**Last updated:** after P2's pilot (October 2026).

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
| 0. The world | Is there a world worth living in? | **reopened (October 2026):** a third of control worlds die out of failed pairing (F1); N5 evidence on how real foragers find partners |
| 1. Culture appears | Does anything cultural emerge unscripted? | **done** (E1–E5: traditions, trust, stories) |
| 2. Why it stops | Where does the chain from possible to practised break? | **mostly done** (E6–E12) |
| 3. Transmission | Can a useful practice pass between adults? | **paused until stage 0 is settled;** was in progress: a habit passes, a plan does not; now: why food does not last through winter |
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

**N3 evidence review done** (`experiments/N3_lean_season/evidence.md`; no code): strong support for L1 (temperate plants
are dormant in winter; zero growth is the realistic value) and L6 (lean seasons vary with climate); partial for L2 (short
seasons leave foragers plant-poor, but no rate is given, and real foragers turn to meat: ACL's hunting is almost nil);
animals only for L3. Real people meet lean seasons by meat, body reserves, moving and storing, so any harder-winter
experiment must count a non-storage answer as a finding. Storage in human foragers goes with predictability, richness and
clumped, owned resources. **N3 in the book (Chapter 48). L1 pre-registration drafted** (`experiments/L1_no_winter_growth/preregistration_draft.md`,
not frozen): one setting changed (winter plant regrowth 0.15 → 0, no code change), control and L1 on seeds 601–616, a
survival pilot on 701–704 read for survival only, and a frozen test of the immediate-return hypothesis (removing winter
growth alone will not create substantial delayed-return behaviour).

**L1 frozen (`L1-frozen`); survival pilot triggered the stop rule:** 2 of 4 pilot worlds died out (702, 704), so the
experiment did not run. A post-pilot survival-only diagnostic (recorded before it ran: the unchanged world on the same
seeds) found both explanations partly true: seed 702 dies in the unchanged world too (fragile), seed 704 dies only under
L1, and every surviving L1 world ends smaller (31 against 44; 32 against 94). Removing winter growth materially harms
survival and population: winter growth is an important stabiliser of ACL's world. **The creator chose: redesign the pilot
with same-seed controls** (recorded in the book, Chapter 49). **Draft written**
(`experiments/L1_no_winter_growth/pilot2_and_amendment_draft.md`): a new pilot on seeds 711–718, both arms, survival and
population only, stopping on excess extinction against the control; and Amendment 1 to the frozen design for the
population confound (population beside every measure, verdict on paired surviving worlds). **Signed off and frozen (`L1-pilot2-frozen`).**

**L1 done** (`experiments/L1_no_winter_growth/results.md`): the redesigned pilot passed (C lost 3 of 8, L 1 of 8). The
main run was valid; **outcome A**: the manipulation check failed, because L1 worlds ended far smaller (final median 6
against 30) and so had as much winter food per person (design flaw admitted: measured per person, not per tile). 0 of 3
delayed-return criteria on six paired seeds; by the frozen rule the null says nothing about lean seasons. Post-hoc
observation: a steady leaner winter was absorbed by density, not by behaviour, as the human evidence suggests. A lean
season people cannot adjust to by numbers (unpredictable bad winters, L5) would be a different test.

**New hypothesis, created by L1 (the creator):** **H-L5:** *delayed-return behaviour is primarily an adaptation to
uncertainty rather than to average scarcity.* Sharpened from P1 (to be checked against the literature): storage should
answer bad years that strike everyone at once (correlated risk) more than misfortune that strikes some (idiosyncratic
risk, which sharing covers). **N4 candidates written** (`experiments/N4_uncertain_winters/candidates.md`): U0 keep, U1
wider swings, U2 rare severe winters, U3 runs of bad years, U4 patchy bad years, U5 unpredictable timing, U6 (harsher
and more variable: not a test of H-L5). L1's lessons bind all of them: mean-preserving, per-tile manipulation check,
same-seed controls, population beside every measure.

**Overnight (the creator asleep):** **N4 evidence review done** (`experiments/N4_uncertain_winters/evidence.md`): the
sharpening holds (sharing insures idiosyncratic, not aggregate risk: Ravallion and Chaudhuri 1997, Townsend 1994,
Hoogeveen 2001), but uncertainty can also favour sharing and moving (Lewis et al. 2014); real grassland production varies
~37% a year (Shi et al. 2014). **V1 done** (`experiments/V1_bad_years/findings.md`): ACL's food varies ~7–8% a year; bad
winters kill (~7× starvation in the poorest quarter) but do not teach storage (more sowing, a few more planners, no more
household stock, fewer stashing); poor years cluster (0.73). **U design drafted** (`experiments/N4_uncertain_winters/preregistration_draft.md`,
not frozen): control vs wider world-wide years (W, settings only) vs wider patchy years (P, new code), width calibrated to
real variability by measuring land only. **Signed off** (grassland target, quarters for regions).

**U, October 2026: stopped at the pilot** (`experiments/N4_uncertain_winters/pilot_stop.md`). Calibration (land only):
even the widest weather (0 to 1.9) moves autumn food per tile only ~11% a year against ~37% in grassland; the widest was
used by the frozen rule and the shortfall recorded before freezing (`U-frozen`). Pilot at that width: worlds died out
C 4, W 7, P 6 of 8; all three arms alive in 0 of 8: **hard stop**, main run not done, no behaviour measured. In ACL's
present world no weather setting gives realistic food variability, and the closest one kills. Also exposed: half of
control worlds die out within 120 years, which limits every paired design. **The design returns to the creator**
(options in `pilot_stop.md`: stop U; a narrower width by a new advance rule; make the land itself vary; first address
baseline fragility).

**The creator chose option 4: F1, baseline fragility** (`experiments/F1_baseline_fragility/findings.md`; read-only,
40 saved control worlds, confirmed on 24 new). Control worlds die out at **34%** (22 of 64), not from hunger, food or
neglect: **births stop 40–65 years before extinction and the people age out.** Women of childbearing age have no partner;
pairing happens mostly among the founders; in small worlds a partner is almost never within sight, because people court
only within 4 tiles on a 40 × 40 world. Worlds that lose more children early are smaller by year 20 and do not recover.
They can be identified decades ahead (population at year 20; at year 30, population below the 20 founders and at most
three fertile women). **This is a gap in stage 0 (the world), not in culture:** every stage 3–5 result has been read on
worlds a third of which were ageing out. Rules 12 to 19 were added during F1. **Next: the creator decides** whether to
reopen stage 0; any change to how people find partners must be anchored to real evidence (rule 17) and checked for
feasibility first (rule 12).

**Stage 0 reopened by the creator (October 2026).** Stage 3 is paused until the world can sustain its people.
**N5 evidence done** (`experiments/N5_mate_search/evidence.md`): real foragers find spouses in networks of hundreds
(mating pool ~500, Pearce 2014; minimum viable population ~75–150 even when any partner can be found, White 2017; more
with space, Wobst 1974), by looking outside the local group (Kramer et al. 2017), through fluid camps (Hill et al. 2011;
Dyble et al. 2015), aggregations, and mostly kin-arranged marriage (67–85%, Walker et al. 2011). Random movement fails at
low density (Pearce). ACL: the whole world is 20 founders, below every estimate; search is random within sight; ACL has
no physical scale. Most real means are culture and may not be written; memory of people known, travel and dispersal are
nature. **Next (assistant's view; the creator decides):** a read-only feasibility check (rule 12): would 20 founders
persist even with perfect search? Then size before search.

**F2 done** (`experiments/F2_perfect_search/findings.md`; signed off and frozen; a diagnostic copy with perfect partner
finding on F1's 64 seeds): **7 of 64 died out against 22, frozen verdict "both"**. Search is most of the problem
(17 of 22 saved; populations grow, median 67 against 28 at year 120); size is real at the margin (in the 7 that still
die, no eligible partner existed anywhere: tiny worlds run out of non-kin of the right age). Two new limits appear once
people pair: couples drift apart (out of reach in 46% of women's weeks; corrected by C1: per couple 58% in the control
and 65% under F2, so couples were already apart about half the time), and larger peoples meet the food limit
(starvation half of all deaths). **Next: the creator decides** among size (M1), anchored search or dispersal (M2/M3),
and couples' proximity; any choice anchored (rule 17) and checked for feasibility (rule 12).

**C1 done, the creator's choice** (`experiments/C1_couples_apart/findings.md`; read-only, confirmed on a holdout):
ACL's couples are apart about half their weeks in the unchanged world. Two in five apart weeks sit at exactly 3 tiles,
in a gap between two separately written thresholds (conception within 2; the pull toward a partner only beyond 3).
Partners forage independently and foraging makes most splits; beyond reach the pull is present but outbid by food; a
third of reunions are chance. Nothing in nature keeps a couple together while they forage. C1 also corrected F2's
"20% → 46%" (per couple 58% → 65%). **Next: the creator decides**; candidates (the threshold gap, a shared camp, the
pull's strength) each need evidence first (rule 17).

**N6 evidence done, the creator's choice** (`experiments/N6_living_together/evidence.md`): real foragers return to a
central place each night; spouses often forage apart by day but share a camp; separation lowers fertility. At ACL's
weekly step a real couple would be together almost every week, so ACL's "apart half the weeks" has no counterpart; the
gap is the absence of a shared home base. Candidates: align the thresholds (L1), a shared home base (L2, best
anchored), a pair bond at any distance (L3); division of labour and residence rules are culture and may not be written.
**Next (assistant's view; the creator decides):** a read-only feasibility check (rule 12) of how far apart partners'
personal homes lie today, then a design for sign-off.

**H1 done** (`experiments/H1_partner_homes/findings.md`; read-only, rule 12): partners' homes lie within conception
distance only about half the time; about 30% are 4 or more tiles apart; homes change in about 18% of adult-weeks.
Frozen rule: **mixed**. Aligning the thresholds (L1) alone would leave much of the separation; a shared home base (L2)
is what the evidence points to. **Next: the creator decides** (L1, L2, or L1 then L2 as separate experiments).

**The creator chose L1 then L2, as T1 then HB1, then F3 comparing them.** **T1 done** (`experiments/T1_threshold_align/
findings.md`; signed off and frozen): the manipulation check failed (apart weeks at 3 tiles did not fall), so its outcome
is not read. Diagnosis: the added pull was among the top options but food outbid it, as C1 found beyond 3 tiles. The
missing piece is a shared place that foraging returns to, not a pull toward a partner's position. Also learned: a slight
change flipped the fate of 19 of 64 worlds (sign test p = 0.36 on 22 → 27), so differences of a few worlds are noise.
**Next: HB1 (a shared home base)**, designed from N6's evidence, with a sham arm to measure the noise, for sign-off.

**HB1 done** (`experiments/HB1_home_base/findings.md`; signed off and frozen, with a sham arm): couples were together
almost every week (apart 57.8% → 0.1%) and had more children, but **extinction rose (33 of 64 vs 22; p = 0.043; sham
p = 0.815)**. Exploratory: food near fixed homes ran short, adults and teens starved, widowhood rose and pairing slowed;
crowding illness was not the driver. HB1 gave couples a central place without the residential mobility real central
places have (Garg et al. 2021: foragers forage near home or move home to new areas). **Next: the creator decides**:
HB2 (a home that moves with the food), or first measure food around homes read-only.

**The creator chose to measure first. HF1 done** (`experiments/HF1_home_food/findings.md`; read-only, signed off,
holdout on new seeds): **not confirmed**. The land around HB1's homes was only about 3% less full than the control's
(0.970 / 0.976); HB1's extra starvation repeats on new seeds but local depletion did not cause it. By the frozen design,
**HB2 is not designed until the cause is found.** Leads for the next read-only check: hunting fell under HB1; HB1's
couples had more children, and carers feed dependants first.

**HF2 done** (`experiments/HF2_household_food/findings.md`; read-only, signed off, holdout on new seeds): **neither**
frozen lead. Not mouths (HB1's carers had only 8–12% more dependants, and the extra hunger falls on every kind of adult);
not meat (meat is about 0.02% of ACL's food). A lead written before the holdout and repeated in it: **under HB1, people
gave each other about two fifths less food**, about three quarters of the drop in what adults took in. Consistent, not
formally confirmed. **Next: the creator decides**; proposed HF3, a pre-registered read-only test of why gifts fell and
whether losing them predicts starving. HB2 still waits.

**HF3 done** (`experiments/HF3_gifts/findings.md`; read-only, signed off, holdout on new seeds): **not supported**.
Gifts fell, but starving adults under HB1 had someone with food to spare within reach as often as in the control;
meetings did not fall; surplus and choice both fell a little, channel not identified. **After HF1–HF3, HB1's hunger is
real and repeats, but no single cause tested explains it** (not depletion, children, meat or gifts). Remaining
hypothesis, not a finding: many small shifts pushing adults over the starvation line. **Next: the creator decides**:
HF4, a read-only hunger ledger testing that hypothesis, or close the HB1 question and return to keeping couples
together with a different design.

**HF4 done, and the HB1 question closed** (`experiments/HF4_hunger_ledger/findings.md`): by the frozen rule, **small
shifts explain the hunger**: under HB1 the food adults hold when they eat fell about 6–7% across the whole
distribution (no tail of a few badly-off people). Caveat recorded before the holdout: the shift accounts for about half
of the *extra* starvation. A shared home, as HB1 built it, made people hungrier through a broad, modest fall in food
held, not one failure; HB2 is not designed. **Next (the creator's decision at sign-off): return to keeping couples
together with a different, evidence-anchored design** that does not tie each week's foraging to a fixed home.

**N7 done** (`experiments/N7_couple_designs/candidates.md`, `evidence.md`): candidates K0–K4; evidence that foragers
return to a central place each day and move it as local returns fall. **K2, a camp that goes where the couple goes,
is anchored; K1 is dropped** (no evidence turns a day's range into ACL tiles, and its threshold would act on births).
Feasibility already in the record: couples are beyond reach in 28–29% of couple-weeks (C1). **Next: the creator
decides whether to design K2** (with a sham arm, a paired test and HF4's ledger from the start).

**MC1 done** (`experiments/MC1_moving_camp/findings.md`; K2, signed off and frozen): couples apart 57.8% → 17.0%,
births +12%, **no extra hunger** (food held at eating unchanged), but **no detectable effect on extinction** (26 vs 22
of 64; p = 0.503; sham p = 0.815). The first change in this series that is anchored, achieves its aim and does no
harm. **The thread ends here: pair stability limited births, not survival.** F2's lever, finding partners, remains.
**Next: the creator decides**: realistic, anchored mate search (N5's M2/M3); whether MC1 joins ACL's nature; size
(M1) for the smallest worlds.

**N8 done** (`experiments/N8_partner_finding/`): candidates P0–P5; evidence: **P1 (walk to where you last saw a known
single) not anchored** (knowing many people across camps is supported, tracking where they are is not); **P2 (leave
when there is no one) anchored in behaviour**, with no timing anchor, so only a timing-free form: outward instead of
random steps when no eligible partner is in sight. **Power:** detecting half of F2's effect needs about 192–256 worlds;
64 detect only large effects (so MC1's null cannot rule out a modest benefit). **Next: the creator decides** whether
to design P2 (outward dispersal) at that size.

**MC1-L done** (`experiments/MC1L_moving_camp_large/findings.md`; MC1 re-tested at 256 new seeds, frozen): control
87 of 256 died out (34%); couples apart 57% → 16%, births +15%; **extinction 93 vs 87** (p = 0.532; sham p = 0.248);
effect −0.023, 95% interval [−0.086, +0.039], below half of F2's effect (0.116). **Frozen rule: MC1 is genuinely
weak.** Pair stability limits births, not survival: now a confident null. The sham's noise matched the power model.
**Next: the creator decides** whether to design P2 (outward dispersal) at 256 worlds.

**P2 stopped at its pilot** (`experiments/P2_outward_search/pilot_stop.md`; signed off and frozen: outward instead
of random steps for seekers with no eligible partner in sight, direction only). Seekers have no one in sight in 95%
of their weeks, but the search wins against food, water and home so seldom that the outward step was taken in
**3.9% of trigger weeks** (frozen gate 5%). Main run not started. **The question is now how much people search, not
where;** only evidence may set that. **Next: the creator decides** (evidence on time spent seeking others; a
direction-only variant; or N8's other candidates).

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

**Added October 2026, signed off by the creator during F1 (before F1's holdout finished).** Each was paid for by a real
failure, stop, confound or correction:

12. **Feasibility before design.** Before designing an experiment around a world setting or target condition, perform a
    read-only feasibility check to verify that the world can actually produce that condition. If the condition cannot be
    produced, the design must be revised before sign-off. *(U: ACL could not reach grassland-level variability.)*
13. **Manipulation checks protect the scientific target.** Manipulation checks must be anchored to the scientific target
    being tested, not to the magnitude achieved by the manipulation itself. A manipulation that falls short of its target
    does not redefine success. *(U's check became detached from the grassland target.)*
14. **Baseline survival is reported first.** Any experiment whose interpretation depends on surviving worlds must begin
    by reporting the control survival rate and the expected number of paired worlds available for comparison. *(L1, U
    and F1 were all affected by extinction and shrinking populations.)*
15. **Discovery and confirmation are separate.** Patterns found through exploratory analysis are hypotheses until they
    are tested on fresh, unseen worlds. Findings discovered on one set of seeds must be confirmed on a holdout before
    being treated as established. *(D1 and F1.)*
16. **Every reported number must be traceable.** Every quantitative claim in a report must be reproducible from a script
    committed to the repository. Claims must not extend beyond the population, worlds, or conditions actually measured.
    *(F1's "in any world" overstatement; an earlier claim of work not done.)*
17. **Nature is anchored, not tuned.** Changes to nature must be anchored to external evidence about the real world.
    Values are chosen from evidence and fixed before running experiments. Nature may not be tuned toward a desired
    outcome. *(The temptation F1 opens: widening mate search until worlds survive.)*
18. **Population accompanies interpretation.** Population must be reported alongside any behavioral measure when
    population differences could influence interpretation. Where possible, verdicts are based on worlds surviving in
    all relevant arms. *(L1's Amendment 1, made a rule.)*
19. **Corrections are appended, not rewritten.** Errors are corrected openly through dated amendments. Earlier
    conclusions remain visible and are not silently rewritten. *(Long practice, made a rule.)*

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
