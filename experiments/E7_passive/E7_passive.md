# E7: Passive Affordances and the First Step · Pre-Registered Design & Predictions (FROZEN)

**Question:** *Does passive environmental physics mend the interaction bottleneck and allow the world to sustain novelty beyond its first century?*

**Written:** 2026-10-03, before any E7 code is written and before any run. Not to be edited after results.

---

## 1. Context & The Diagnostic Chain (E5 $\to$ E6 $\to$ E6.5 $\to$ E6.6)

- **E5 (Millennium):** Discovered the open-ended evolution plateau: all tool kinds appeared within 11 years; 990 years followed with zero new kinds.
- **E6 (Novelty & Physics):** Added continuous properties (mass, heat, wetness, tightness, plasticity) and active actions (`heat`, `fill`, `shape`). **Verdict: BOTTLENECK REMAINS.** LFA $\le 28$ in 7 of 8 worlds. Deep branch stayed shut: 0 food cooked, 0 water carried, 1 lump of raw clay fired once.
- **E6.5 (The Autopsy):** Isolated the exact broken link in the 6-link discovery chain:
  $$\text{Opportunity} \xrightarrow{\quad\mathbf{BROKEN}\quad} \text{Interaction} \to \text{Transformation} \to \text{Observation} \to \text{Reuse} \to \text{Tradition}$$
  - **Seed 304:** Reibik made a watertight vessel (year 12), used it 104 times as a carrier, and taught it to 7 people over 60 years. Transmission worked. But Reibik stood at water holding the vessel for **102 weeks and never once filled it**.
  - **Seed 302:** A 4-year-old child (Beimak) fired clay in play, but starved 14 weeks later before it could matter.
  - **The Diagnosis:** The bottleneck is **Interaction**, driven by the **Spatio-Temporal Utility Disconnect**. At a river, thirst is zero. Choosing to fill a vessel requires abstract foresight of future drought. Agents are too rational to take an unrewarded first step for a distant payoff.
- **E6.6 (Reward Horizon):** Proved that the "reward horizon" is **not the bottleneck**. The existing "by thing" learning channel has an infinite delay horizon as long as the object is held (47% remade even when first used > 1 year later). If an item *is* filled and later drunk from, credit assignment works effortlessly.

**The E7 Hypothesis (H1):**
> *Civilization stalls because the world creates too few accidental encounters with transformative affordances. If nature executes the first physical transformation passively (fluid displacement and radiant heat), agents encounter the affordance at the point of need without requiring teleological foresight.*

---

## 2. Core Philosophy & Boundaries

Every piece of E7 must strictly pass the foundational principles:

| Principle | Meaning in E7 |
|---|---|
| **Nature vs. Culture** | Nature is programmed; culture is written by nobody. Physical state changes belong to nature. |
| **P1 (No named products)** | No `pot`, `bucket`, `well`, `cistern`, `kiln`, `cooking` in code paths. |
| **P2 (One rule, many consequences)** | Rain fills any open watertight hollow thing; heat radiates from any fire to any adjacent matter. |
| **P3 (Outputs are states)** | Water in a container is a held substance; fired clay is a state with high hardness/tightness and zero wetness. |
| **P4 (Consequences are physical)** | Water is drunk when thirsty; tight vessels prevent leakage; heat dissipates. |
| **P6 (Agents learn everything)** | No new instincts, no Q-table nudges, no hardcoded desire to collect water. |
| **P7 (Responses before pressures)** | No new hazards or death mechanisms added. |

### The "Zero Agent-Side Changes" Rule
**`acl/mind.py`, `acl/person.py`, `acl/thought.py`, and `acl/actions.py` remain 100% frozen.**
- No new primitive actions (`no fill()`, `no heat()`).
- No modifications to the 32 Q-table contexts.
- No changes to attention weights, curiosity mechanics, or memory pruning.
- All additions live strictly within the world's physical and environmental tick (`world.py`, `weather.py`, `matter.py`).

---

## 3. Exact World-Side Physical Changes

### 3.1 Passive Fluid Dynamics (Rain Catchment & Submersion)
Fluid mechanics are physical laws, not deliberate choices.

1. **Rain Catchment:**
   * During any rainy week, any open item with `tightness >= 50` and `contain >= 40` (whether carried by an agent in the open or lying on an uncovered tile) accumulates water proportional to rainfall, up to the container's volume.
   * Items inside a covered heap (`pile_shape` cover $> 0.5$) do not catch rain.
2. **Submersion / Wading:**
   * When an agent carrying an open item with `tightness >= 50` and `contain >= 40` steps onto or wades through a `river` or `lake` tile, the item fills with water to capacity by fluid displacement.
3. **Passive Consumption & Credit Assignment (Existing Machinery):**
   * When an agent away from a spring experiences thirst ($> 0$), if they are carrying an item containing water, they automatically drink from it.
   * Drinking from the held item calls `_judge_use(world, p, idx, "water")`.
   * Through the existing "by thing" channel (proven in E6.6), the container immediately gains high `itemval`. Once valued, it is remade, preserved, and taught.

### 3.2 Passive Thermodynamic Radiation (Hearth Desiccation & Baking)
Thermal energy radiates into space; it does not wait for a `heat` command.

1. **Hearth Radiation:**
   * Any material or item resting on a tile where `tile.fire > 0`, or carried by an agent standing on that tile during the end-of-week tick, absorbs heat and loses moisture.
2. **Ceramic Phase Transition:**
   * If a plastic material (clay) or shaped clay item reaches `wetness == 0` while exposed to `heat >= 6`, its lasting properties transform:
     * `hardness` increases (scales with fire intensity).
     * `tightness` increases (enabling water containment).
     * `plasticity` permanently drops to 0 (cannot be reshaped).
3. **Food Preservation:**
   * Loose food or meat on a tile with fire absorbs smoke/heat, reducing its weekly spoil rate by 75% (`smoke_keep`).

---

## 4. Law Accounting (World Bible v8.1)

| Law | Status in E7 | How it is strengthened |
|---|---|---|
| **Law 4 (Objects Have State)** | Strengthened | Containers hold volume; clay transitions between plastic and ceramic states. |
| **Law 8 (Nature Changes)** | Strengthened | Rain fills hollow vessels; fires radiate ambient heat to adjacent matter. |
| **Law 14 (Needs: Thirst & Hunger)** | Strengthened | Carried water satisfies thirst far from springs, altering territorial range. |
| **Law 105 (Properties, Not Recipes)** | Strictly preserved | Watertightness and heat thresholds derive entirely from continuous numeric properties. |
| **Law 109 (Usefulness Is Discovered)** | Strictly preserved | Agents discover the utility of water containers only after drinking from a passively filled vessel. |
| **Law 123 (Doing Leaves Traces)** | Strengthened | Ceramic shards and charred remains persist in hearth ashes. |
| **Law 124 (Uses Must Be Experienced)** | Core driver | The environment delivers the physical experience so Law 124 can trigger value formation. |

---

## 5. Experimental Design

- **Baseline Arm:** Verified E6 codebase (`experiments/E6_novelty/code_e6/`), seeds 301–308, 1,000 years, run with the novelty recorder.
- **E7 Arm:** E6 codebase + Passive Fluid Dynamics + Passive Thermal Radiation. Same seeds 301–308 (identical maps and founder genetics), 1,000 years, same recorder.
- **Comparability:** Paired seed-by-seed comparison across all 8 worlds.

---

## 6. Definitions & Metrics (Fixed in Advance)

Identical to E6 definitions to maintain longitudinal validity:
* **Kind of thing:** Lasting properties grouped in 5 discrete bands.
* **Behaviour:** Tuple of `(action, kind_used, kind_acted_on/target)`.
* **Lasting Novelty:** A new kind or behaviour made or done again $\ge 50$ years after first appearance.
* **LFA (Latest First Appearance):** The year of the latest *lasting* novelty in a world.
* **New Tradition:** A technique, belief, or mark held by 3+ people in every 10-year sample for 100+ years.
* **New Consequence:**
  1. Water carried $\ge 5$ tiles from any spring or river.
  2. A ceramic object outliving its creator.
  3. Food eaten past its natural unpreserved rot threshold.

### New Diagnostic Metric: First Encounter Count (FEC)
To isolate physical opportunity generation from cultural uptake, the recorder explicitly tallies every passive affordance event per world:
* `FEC_water`: Number of times an open watertight container gains water passively (via rain or wading).
* `FEC_ceramic`: Number of times dry plastic clay hardens into ceramic passively on an active fire tile.
* `FEC_preserved`: Number of times food on a fire tile has its rot delayed by ambient smoke/heat.

---

## 7. Decision Rule & Diagnostic Failure Modes (Fixed in Advance)

Only worlds living 300+ years count toward thresholds (reported otherwise):

- **BREAKTHROUGH:**
  1. E7’s LFA is year 150 or later in at least half of the counted worlds, AND
  2. E7’s LFA is later than E6’s in at least 6 of the 8 seed pairs, AND
  3. At least 3 counted worlds exhibit water carried $\ge 5$ tiles.
- **BOTTLENECK REMAINS:** E7’s LFA is year 50 or earlier in at least half of the counted worlds, or water is never carried in any world.
- **PARTIAL:** Novelty extends (LFA 50–150) or water carrying occurs without sustaining multi-century novelty.

### Diagnostic Disambiguation (Failure A vs. Failure B)
If the result is *BOTTLENECK REMAINS* or *PARTIAL*, the FEC metric isolates the root cause:
* **Failure Mode A (Physical Starvation):** `FEC_water == 0` or `FEC_ceramic == 0`.  
  *Diagnosis:* The passive physics parameters were too conservative; the world failed to generate affordances. (Resolution: recalibrate physical thresholds).
* **Failure Mode B (Cultural / Cognitive Detachment):** `FEC_water >= 50` and/or `FEC_ceramic >= 20`, but no lasting traditions form and LFA $\le 50$.  
  *Diagnosis:* The environment provided abundant affordances, but agents failed to convert encountered affordances into cumulative culture. (Resolution: investigate the cultural accumulation, memory, and social transmission rules).

---

## 8. Frozen Predictions

### Primary Hypotheses (E7 Arm)
1. **The Reibik Test (Seed 304):** In Seed 304, passive rain catchment or stream wading will fill a watertight vessel within the first 50 years. At least one agent will consume carried water $\ge 3$ tiles from fresh water, establishing a lasting water-carrying tradition.
2. **Passive Ceramics (Seed 302 & others):** Fired clay items will form passively on hearth tiles without requiring an active `play(heat)` action from a child. At least one ceramic item will survive for $>50$ years and outlive its maker.
3. **First Encounter Generation (FEC):**
   * `FEC_water >= 10` in at least 6 of the 8 worlds (Failure Mode A eliminated for water).
   * `FEC_ceramic >= 5` in at least 4 of the 8 worlds (Failure Mode A eliminated for heat).
4. **Novelty Extension (LFA):** E7’s LFA will exceed year 100 in at least **4 of the 8 worlds** (compared to 0 of 8 in E6).
5. **Seed Pairs:** E7 will achieve a later LFA than E6 in at least **6 of the 8 seed pairs**.
6. **Demographic Safety (P7):** E7 will produce no increase in extinction rate (at least 4 of 8 worlds survive to year 1000, identical to or better than E6).
7. **Traditions:** At least 3 surviving worlds will produce a new tradition that originated after year 100.

---

## 9. Kill Criteria (The Experiment Is Invalid If...)

- Any simulation crashes or errors during execution.
- The recorder changes the world state (state hash differs with and without recorder over 20 years).
- Code changes occur during the execution of the 8 seeds.
- Fewer than 6 worlds complete in either arm.
- The baseline arm does not replicate E6’s population and LFA metrics.
