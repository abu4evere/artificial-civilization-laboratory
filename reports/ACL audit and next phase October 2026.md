# ACL — audit and next phase (12 October 2026)

Answer to the creator's plan "Scientific Improvement and Biological Learning Research". Everything below was read
from the repository or run on 12 October 2026. **Observed** = read in code or measured; **interpretation**,
**hypothesis** and **proposal** are labelled as such. Branch: `audit-2026-10` (nothing in it touches a frozen run).

---

## 1. Current ACL state (what the code does)

**The brain** (`acl/mind.py`, `acl/biology.py`, `acl/thought.py`, `acl/util.py`; observed):

- Each week every person aged 1 or more builds a list of options. Each option's score is **instinct** (hand-written
  formulas of needs, feelings and temperament) **+ 0.6 × a learned habit value** for (situation, action).
- **Situations: 32** = food held (4 bands: under half a week or health under 40; under 2 weeks; under 6; more) × anyone
  within reach (2) × season (4).
- **Actions: 17**, not 19: rest, forage, hunt, gather, put, take, make, play, explore, give, care, talk, court, steal,
  attack, flee, join. So the habit table is **32 × 17 = 544 values**, not 608. The figures 19 and 608 were wrong on the
  viewer's brain screen, in the brain-scan tool and in ID1's frozen questions; all three are corrected (section 3).
- **Learning:** only the habit for last week's (situation, chosen action) is updated, by a temporal-difference rule
  (rate 0.05, discount 0.8, clipped to ±1.5). The reward is the week's reward plus twice the change in mood. A repaid
  gift also nudges the giver's give-habit.
- **Inheritance of habits:** at birth, a quarter of the sum of the parents' habits; under 12, habits move 8% a week
  toward the carer's while together. Otherwise **unused habits never change or fade**.
- **Choice:** a thought on the mind adds a bonus (`thought.steer`); then a softmax at temperature 0.2. The top score
  does not always win.
- **Internal states** (observed): energy, health, food held, thirst, sickness, starving, fatigue (attention); feelings
  mood, fear, anger, grief, loneliness, wellbeing; eight inborn traits: curiosity, diligence, sociability, kindness,
  temper, anxiety, care, boldness. These enter the **instinct** formulas directly; only food held enters the situation.
- **Other learned or remembered things** (observed): episodic memories that fade by salience; place values (decay 0.5%
  a week); expectations updated by prediction error (`p.expect`: dryness, fire, items); trust that fades for people
  never seen again; recipes forgotten if useless; hearsay about game; social learning by watching (4% chance a week,
  scaled by curiosity) and teaching.
- **Perception** 4 tiles, **reach** 3 tiles a week.

**Bands** (`world._make_founders`, observed): `n_groups = max(1, min(4, founders // 4))`, each on its own island, or
far apart on the largest if islands are too few. 20 founders → 4 bands of 5; 80 → 4 bands of 20. The cap of 4 is
this one line.

**A breach found this week** (ST1, observed): a raft used at sea for foraging, gathering, hunting or fighting can wear
out after the walk, leaving its owner on open water for a week. 22 of 1,291,054 person-weeks (40 worlds × 30 years);
equal in every arm of every study. Nature not changed. `experiments/ST1_stranded_at_sea/finding.md`.

## 2. Existing experiments (status and protected baselines)

| study | status (observed 12 Oct, 02:46) |
|---|---|
| **WS1** world size | running, detached: **831 of 1,280** (c 63, l 256, lp 256, p 256, s 0). About 4 hours left. Untouched. |
| **AA1** artifact audit | frozen (`AA1-frozen`); its discovery run starts by itself when WS1 ends (waiter running). |
| **MB1a** cross-band contact | frozen (`MB1a-frozen`); after AA1. |
| **ID1** memory and identity | frozen (`ID1-frozen`); after MB1a. |
| F1, MC1, MC1-L, GF1, P2, E-series, HF-series … | finished; frozen and done tags kept (`F1-done`, `MC1L-done`, …). |

Frozen code copies the studies run on: `experiments/E13R_replication/code_e13r` (control), `experiments/P2_outward_search/code_p2`
(WS1), `experiments/AA1_artifact_audit/code_aa1`. None was edited.

## 3. Changes completed

On `master` (made before this plan arrived, at the creator's request "start with hypothesis tests and github
actions"; not on a separate branch):

- `tests/test_properties.py`: Hypothesis property tests.
- `tests/test_reference_replays.py` and `tests/reference_hashes.json`: a replay check.
- `.github/workflows/tests.yml`: CI.
- `pyproject.toml`: Hypothesis as a test-only extra.
- `experiments/ST1_stranded_at_sea/`: `check.py`, `finding.md`, `output/check.json`.
- An ST1 row in `experiments/INDEX.md`.

On branch **`audit-2026-10`** (this plan):

- `acl/viewer.html`, `tools/mind_views/brain_template.html`, `tools/mind_views/brain_scan.py`: labels corrected, 19 → 17
  actions and 608 → 544 habits. The drawing already took the actions from the code; only fixed text was wrong.
- `experiments/ID1_memory_identity/questions.md`: correction appended (17 actions, 544 habits; design unchanged).
- `experiments/MB1_multi_band/questions.md`: correction appended on what the Hill et al. benchmark measures (section 6).
- `experiments/BL0_habit_use/questions.md`: a **draft** (not frozen) for the recommended next study.
- This report.

Hypothesis is imported only by `tests/`, never by `acl/`.

## 4. Tests

- **Before this work: 47 tests**, as reported. **Now: 55.** The new ones are:
  - 3 property tests;
  - 2 replay tests;
  - 3 from ST1: a known-breach test marked as an expected failure, a pinned world 803 marked as a strict expected
    failure, and the world 601 child case, which passes.
- **Local runs:** 52 of 52 passed before ST1, on this machine and on a fresh clone. After the ST1 change, the property
  file passed under the seed that had found the breach: 4 passed, 1 expected failure, 1 tolerated pass.
- **CI:** the first two GitHub runs **failed**. That was correct: GitHub's random worlds found the ST1 breach. The run
  for `08b084d` has not been checked from here (no `gh`, and the Chrome extension was not connected). **The creator
  should look at the Actions tab.**
- **Invariants actually tested,** each checked against the code:
  - nothing carried or on a tile is negative;
  - energy stays in 0–100 and health stays at or below its age limit;
  - birth is not after now;
  - everyone is on the map;
  - on water only if afloat, or a child with an afloat carer on the same tile (stranding is tracked separately);
  - partners are mutual, alive and not kin;
  - the dead are out of the living list.
- **Plan invariants not tested, and why:**
  - "Ages never decrease": age is computed from birth, so it cannot.
  - "Reproduction and death preserve population and resource accounting": the code has no conservation law to test.
    Food is created by growth and lost by decay. Adding one would be inventing a rule.

## 5. Reproducibility

- **What a hash covers** (`World.state_hash`, observed): SHA-256 of the whole saved world:
  - config and tick;
  - the **random generator's internal state**;
  - every tile and every person: all of `Person.__slots__` is saved (checked: none missing);
  - animals, knowledge, weather, sky and graves;
  - a **chain hash of every week's events since week 0**.
- **Not covered:** caches rebuilt on load (occupancy, the island map, the week's plans).
- **Reference hashes** (`tests/reference_hashes.json`) for ACL's live code and the frozen control copy, seeds 11 and
  501 at 5 years: all four matched locally, and on a fresh clone.
- **Limits:**
  - They were made on Windows with Python 3.14.7, so CI runs on Windows.
  - They cover 5 years of two seeds, not every arm's settings: `code_p2` and `code_aa1` are not yet pinned (proposal:
    add them).
  - The test never regenerates a hash. That is a separate `--update` command, to be used only with an explained commit.

## 6. Cross-band findings

**Not measured yet.** Stage A (MB1a) is frozen to run after AA1. It needs **replays**, because saved runs hold
populations, not weekly positions. Running them now would compete with WS1 for the computer, which the plan forbids. So
there are no rates to report, and none are estimated.

**Benchmark, verified in full text** (Hill et al. 2014, PLoS ONE 9(7): e102806, PMC4105570):

- **Who:** random same-sex adult pairs from the whole population, not only different bands. Ache: 351 interviews about
  adults alive 1965–70. Hadza: 850 interviews in 22 bands.
- **How:** yes/no recall ("did target ever…"), converted to a yearly probability by a model in which elapsed time is the
  main predictor.
- **Rates:** "about 0.20 to 0.30 per annum" for the Ache, for conversing, sleeping in the same camp, sharing food and
  watching tool-making. The Hadza were generally 2–5 times lower. Rare activities ran 0.02–0.08.

**Limitations:**

- ACL's "within sight" (4 tiles) is neither conversation nor sharing a camp. It is at most an upper bound on contact.
- MB1a's frozen text called the benchmark "between-band"; that is inexact. A correction is appended.
- The thresholds (0.05 and 0.005) stay frozen, labelled as operational cut-offs, not biological boundaries.
- Stage A will also report the same-sex-pair rate as a description. **This was added in the correction; it is the
  creator's call whether to keep it.**

**Stage B:** not designed further. It waits for Stage A, as frozen.

## 7. Biological learning research

**Sources.** All were checked against their PubMed records on 12 October 2026. For each, the **abstract** was read, not
the full text. Each is labelled with what it supports.

| function | fly finding (source) | what ACL has (observed) | gap |
|---|---|---|---|
| Associative learning | Mushroom body: ~2,000 Kenyon cells; 21 output-neuron types in 15 compartments; 20 dopamine-neuron types, each to 1–2 compartments. "A logic for associative learning" (Aso et al. 2014, eLife, [10.7554/eLife.04577](https://doi.org/10.7554/eLife.04577)). Pairing an odour with dopamine depresses that odour's output synapse, only in the right time order (Hige et al. 2015, Neuron, [10.1016/j.neuron.2015.11.003](https://doi.org/10.1016/j.neuron.2015.11.003)); order can also reverse it, through two receptors (Handler et al. 2019, Cell, [10.1016/j.cell.2019.05.040](https://doi.org/10.1016/j.cell.2019.05.040)). | Value of an **action in a situation** (544 cells), learned by temporal difference. | ACL learns about actions, not cues. No stimulus-specific value of a place, person or object in the habit system (some in `places`, `expect`, `rel`). |
| Generalisation | Overlap between sparse odour codes sets how far learning generalises (Hige et al. 2015). | 32 separate situations; learning in one never spreads to a neighbour. | **No generalisation.** Hypothesis: most of the 544 cells are rarely visited. BL0 Q1 measures this. |
| Internal state gates memory | Hunger, via neuropeptide F on six dopamine neurons, switches on expression of food memory; satiety blocks it (Krashes et al. 2009, Cell, [10.1016/j.cell.2009.08.035](https://doi.org/10.1016/j.cell.2009.08.035)). Dopamine neurons encode context and internal state, rerouting one odour to different outputs (Cohn et al. 2015, Cell, [10.1016/j.cell.2015.11.019](https://doi.org/10.1016/j.cell.2015.11.019)). | Partly: food held is one axis of the situation, so food habits are kept per hunger band. The learned weight (0.6) is the same for every need and state. | No gating by thirst, fear, fatigue or loneliness. |
| Prediction and its errors | In the larva, dopamine neurons compare feedback from aversive and appetitive systems, "integrated predictions" (Eschbach et al. 2020, Nat Neurosci, [10.1038/s41593-020-0607-9](https://doi.org/10.1038/s41593-020-0607-9)). | A temporal-difference error, plus expectation updates by error (`p.expect`). | Rough match. |
| Forgetting | Forgetting is active and dopamine-regulated (Berry, Guhle & Davis 2024, review, Mol Psychiatry, [10.1038/s41380-024-02521-9](https://doi.org/10.1038/s41380-024-02521-9)). One dopamine neuron causes transient forgetting (Sabandal et al. 2021, Nature, [10.1038/s41586-020-03154-y](https://doi.org/10.1038/s41586-020-03154-y)). Extinction is a **new opposing memory**, not erasure (Felsenberg et al. 2018, Cell, [10.1016/j.cell.2018.08.021](https://doi.org/10.1016/j.cell.2018.08.021)). | Memories, places and trust fade. **Habits never fade.** | No habit forgetting or extinction. |
| Navigation | Head direction held by a ring-attractor-like network, combining landmarks and self-motion, persisting in darkness (Seelig & Jayaraman 2015, Nature, [10.1038/nature14446](https://doi.org/10.1038/nature14446)). Central complex connectome: motifs for vector navigation and state-dependent action selection (Hulse et al. 2021, eLife, [10.7554/eLife.66039](https://doi.org/10.7554/eLife.66039)). | Steps toward targets in sight or remembered (places, springs, hearsay). No heading. Some targets known without sight (AA1's A5, A6c, A6d). | No path integration. AA1 measures the shortcuts first. |
| Whole-brain structure | 139,255 neurons and about 5 × 10⁷ synapses of an adult female fly (Dorkenwald et al. 2024, Nature, [10.1038/s41586-024-07558-y](https://doi.org/10.1038/s41586-024-07558-y)). A connectivity-only model predicted feeding and grooming sensorimotor responses (Shiu et al. 2024, Nature, [10.1038/s41586-024-07763-9](https://doi.org/10.1038/s41586-024-07763-9)). Human cortex: 1 mm³, about 57,000 cells and 150 million synapses, 1.4 PB (Shapson-Coe et al. 2024, Science, [10.1126/science.adk4858](https://doi.org/10.1126/science.adk4858)). | n/a | Related work only. Nothing to copy: a connectome gives wiring, not the learning rules or values ACL needs. Nothing downloaded. |

**Candidate mechanisms** (proposals; **not implemented**; each a change to nature, needing its own freeze):

- **M1 — habits that fade or are extinguished.**
  - Evidence: Berry et al. 2024; Felsenberg et al. 2018; Sabandal et al. 2021.
  - Change: unused habit values decay slowly toward the inherited value. Or, the extinction variant: a separate
    opposing value is learned when an expected reward fails to come.
  - Competing hypothesis: stale habits do no harm, because the situations recur and are relearned.
  - Control and sham: current code, plus a sham with one extra random draw.
  - Prediction (held loosely): fewer choices driven by outdated habits after the world changes.
  - Measures: staleness (BL0 Q4), habit influence, survival, population.
  - Cost: about 1 multiply per value per week, which is small.
  - Confounders: decay rate is a free parameter that would need anchoring. It also interacts with inheritance.
- **M2 — need-gated habit use.**
  - Evidence: Krashes et al. 2009; Cohn et al. 2015.
  - Change: the learned weight for an action scales with how relevant the current need is (hunger for foraging,
    loneliness for talking).
  - Competing hypothesis: food band in the situation already gates enough.
  - Confounders: the scaling functions are free design choices, so this risks tuning toward an answer. Evidence would
    be needed for the form.
- **M3 — generalisation between neighbouring situations.**
  - Evidence: Hige et al. 2015.
  - Change: a learning update spills a fraction to the same action in adjacent food bands or seasons.
  - Competing hypothesis: the situations are already visited often enough.
  - Measure first: BL0 Q1 (how many cells are ever learned).

**More neurons are not more intelligence:** none of these adds neurons. Each is one rule, testable against the current
brain.

## 8. Not implemented (needs approval)

- Any change to ACL's nature: the ST1 fix (a float that breaks at sea puts its owner ashore half-drowned) and M1–M3.
- BL0 (draft; thresholds for sign-off).
- MB1a Stage A runs (after AA1, as frozen) and Stage B (after Stage A).
- Profiling with cProfile (after WS1 and AA1, so it does not compete with them).
- Pinning reference hashes for `code_p2` and `code_aa1`.
- Merging branch `audit-2026-10` into `master`.

## 9. Recommended next experiment

**BL0, after the agreed queue (WS1 → AA1 → MB1a → ID1).** It is read-only and asks whether learned habits change what
people do at all, and how many of the 544 are ever learned. Every brain mechanism above depends on its answer, and it
needs no change to nature. If the creator wants the brain question sooner, BL0 can run before ID1. It is a replay of
F1's worlds, and it can't start before WS1 and AA1 free the computer.
