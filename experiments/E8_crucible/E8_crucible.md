# E8: The Crucible · Pre-Registered Design & Predictions (FROZEN)

**Question:** *Can naturalistic apprenticeship (guided practice), decoupling deliberate making from inventory suppression, protecting composite recipe memory, or expanding demographic scale arrest the multi-generational collapse of expertise and unlock cumulative cultural evolution (CCE)?*

**Written:** 2026-10-05, before any E8 code is written and before any run. Not to be edited after results.

---

## 1. Context & The Diagnostic Chain (E5 $\to$ E6 $\to$ E6.5 $\to$ E6.6 $\to$ E7 $\to$ E7.5 $\to$ E7.6 $\to$ E7.7)

The trajectory of the Artificial Civilization Laboratory has systematically eliminated superficial explanations and converged upon the deep mechanics of cultural accumulation:

- **E5 (Millennium):** Discovered the 11-year novelty plateau: all tool kinds appeared in the first decade; 990 years of zero new tool kinds followed.
- **E6 (Novelty & Physics):** Continuous material properties and active commands (`heat`, `fill`, `shape`) failed to break the plateau (LFA $\le 28$ in 7 of 8 worlds). Deep branches remained untouched.
- **E6.5 (The Autopsy):** Identified the **Interaction Bottleneck**: Reibik (Seed 304) held a watertight vessel at fresh water for 102 weeks and never once filled it due to the spatio-temporal utility disconnect.
- **E6.6 (Reward Horizon):** Eliminated temporal credit assignment as a culprit: agents learn from delayed outcomes up to a year later via the "by thing" channel (47% remade $>1$ year later).
- **E7 (Passive Affordances):** Passive fluid dynamics and radiant heat fired clay 647 times, but 78% of agents who learned the recipe never made ceramics deliberately. Water carrying remained zero. The plateau persisted (LFA $\le 54$ in 7 of 8 worlds).
- **E7.5 (Autopsy 301):** Dissected the sole late novelty in Seed 301 (Year 115). It was not an invention: it was a *duller* flint flake struck by unskilled descendants (skill 0.14 vs. founder 0.82). The novelty metric had mistaken cultural degradation for innovation.
- **E7.6 (Expertise Retention Audit):** Proved that the worlds do not plateau—they suffer a **multi-generational collapse of expertise**:
  1. *Crafting skill collapsed 10- to 20-fold:* Founder skill (0.73–0.98 best, 0.33–0.50 mean) dropped to 0.05–0.11 best and 0.01–0.03 mean by Year 1000.
  2. *Recipes thinned 4- to 8-fold:* Peak recipe diversity (85–173) plummeted to 15–32.
  3. *Deliberate making collapsed 40- to 60-fold:* From 2.1–3.1 makes per person-decade down to 0.03–0.05. Play making dropped 50-fold.
  4. *Watertight vessels never existed:* 2 made across 16 millenniums; 0 held at any checkpoint.
  5. *Demographics remained untested:* Populations only varied between 36 and 54 in long-lived worlds ($\rho = -0.05$). The population hypothesis was left unexamined.
- **E7.7 (Exposure & Reproduction Audit):** Revealed the structural asymmetries of transmission:
  1. *Teaching works, watching fails:* 1,782 recipes spread by teaching; 233 by reading marks. Watching happened 1,770 times and produced **7 copies** (all boats), because observation was hardcoded only for raft landings and hunts.
  2. *Affordance without motivation:* 272 people knew how to fire clay; 78% never made one.
  3. *The Composite Penalty:* Finite recipe memory (`MAX_RECIPES = 12`) evicted intermediate components with 0 immediate utility, resulting in a **5-fold higher loss rate** for composite inventions (21% forgotten on making vs. 4% for simple items).

---

## 2. Core Philosophy & Anti-Lamarckian Constraints

E8 maintains unconditional fidelity to the core tenets of ACL:

| Principle | Meaning in E8 |
|---|---|
| **Nature vs. Culture** | Nature is programmed; culture is written by nobody. Physical state changes belong to nature. |
| **No Teleology** | No agent possesses goals, tech trees, or pre-programmed awareness of unmade tools. |
| **Properties, Not Recipes** | All affordances arise strictly from continuous property tensors (sharpness, hardness, tightness). |
| **Law 44 (Skill Is Embodied)** | Skill resides in neuromuscular coordination; it cannot be transferred like a file. |
| **Law 46 (No Telepathy)** | No agent can read another's internal cognitive state or directly inherit motor skill. |
| **No Pretrained Models** | No LLM reasoning or human cultural priors. |
| **The Anti-Lamarckian Rule** | **Direct skill inheritance (e.g. $\text{skill}_{\text{learner}} \leftarrow 0.5 \times \text{skill}_{\text{teacher}}$) is strictly forbidden.** Such an intervention would constitute a superhuman shortcut, rendering the experiment incapable of distinguishing genuine cultural transmission from an artificial cheat. |

### Naturalistic Apprenticeship vs. Lamarckian Shortcuts
In human evolutionary anthropology (Henrich 2004, Tomasello 1999, Lave & Wenger 1991), apprenticeship does not bypass physical practice. A novice does not magically download motor coordination. Instead, apprenticeship is **socially scaffolded practice**:
1. Observation creates cognitive salience and perceptual attunement to technique.
2. Demonstrations provide a model that accelerates the learner's own trial-and-error.
3. Guided practice yields faster learning per physical act without ever granting free skill points.

---

## 3. The Four Suspects & The Degenerative Loop

The E7.6 and E7.7 audits established the **Degenerative Making-and-Skill Loop**:
$$\begin{matrix}
\text{Durable tools held} & \longrightarrow & \text{\texttt{\_holding} lock suppresses making} \\
\uparrow & & \downarrow \\
\text{Low utility } \to \text{ low value} & & \text{No deliberate practice} \\
\uparrow & & \downarrow \\
\text{Novices make dull tools} & \longleftarrow & \text{Crafting skill decays to zero}
\end{matrix}$$

E8 tests four orthogonal interventions aimed at dismantling this loop:

1. **Suspect 1 (Deliberate-Making Scarcity):** Tools last 20–50 weeks, and `mind.py` strictly forbids crafting an item if one is already held (`_holding`). Agents only make when empty-handed. Once a basic tool exists, making drops to 0.05 per decade.
2. **Suspect 2 (Procedural Transmission Failure):** Declarative recipes spread via teaching (1,782 transfers), but procedural motor skill cannot pass between agents. Each newborn starts at 0.0 skill, knaps with blunt hands, and produces low-utility items.
3. **Suspect 3 (Composite Memory Bias):** Multi-step technologies require intermediate components (cores, blades, handles, frames). Because intermediate parts have no independent utility ($v = 0$), `MAX_RECIPES = 12` prunes them immediately, imposing a 21% eviction tax on composite inventions.
4. **Suspect 4 (Demographic Scale):** Henrich’s Tasmanian model posits that cumulative culture requires a critical population threshold $N > N_{\text{crit}}$ to prevent stochastic loss of rare high-skill practitioners. Prior experiments were trapped in $N \in [36, 54]$.

---

## 4. Architectural Modifications by Arm

### 4.1 Arm 1: Making Freedom & Maintenance Decoupling (`mind.py`)
Relaxes the rigid `_holding(p, sig)` suppression in `mind.py`:
1. **Preventive Replacement:** If a held tool's wear exceeds 0.35 (`matter.wear`), the agent does not treat it as satisfied and is permitted to craft a replacement.
2. **Kin Provisioning:** If an agent's partner or dependent lacks a valuable tool ($v > 0.15$), the agent evaluates crafting it for them.
3. **Curious Practice:** When focused or when curiosity exceeds hunger ($g[\text{"curiosity"}] > 0.5$ and $\text{hunger} < 0.4$), the agent may craft to refine skill, scoring practice utility as:
   $$u_{\text{practice}} = 0.08 \times g[\text{"diligence"}] \times (1.0 - p.\text{skills}[\text{"crafting"}])$$

### 4.2 Arm 2: Naturalistic Apprenticeship & Guided Practice (`actions.py`, `knowhow.py`)
1. **Universal Craft Observation:** Fixes the E7.7 blindspot. When an agent crafts (`_craft` or `_make`), any observer within distance $\le 1$ with age $\ge 6$ years calls `knowhow.watch(world, observer, crafter, sig, felt)`.
2. **Scaffolded Practice Multiplier:** When an agent physically executes a craft action (`_craft`), if they learned the recipe from a master (or a master with higher skill is within perception distance), their practice efficiency is amplified:
   $$\text{multiplier} = 1.0 + 1.5 \times \frac{\max(0, \text{master\_skill} - \text{my\_skill})}{\max(0.1, \text{master\_skill})}$$
   $$\Delta \text{skill} = \text{cfg.skill\_gain} \times \text{multiplier} \times (1.0 - \text{my\_skill})$$
   *Crucial Anti-Cheat Guarantee:* If no crafting action is taken, skill gain is exactly zero. Novices must still knap flint and bind materials with their own hands.

### 4.3 Arm 3: Composite Component Memory Protection (`knowhow.py`)
1. **Sub-Recipe Dependency Tracking:** When `len(p.recipes) > MAX_RECIPES`, candidate eviction is evaluated.
2. **Component Shielding:** If recipe $A$ is listed as a component (`parts`) of another recipe $B \in p.\text{recipes}$ and $p.\text{itemval}[B] > 0.0$, recipe $A$ cannot be evicted unless $B$ is evicted first. Intermediate steps are recognized by the cognitive architecture as structural dependencies.

### 4.4 Arm 4: Demographic Scale Test ($N_0 = 80$)
1. Map and founder configuration expanded to 4 distinct island bands of 20 founders each ($N_0 = 80$, total map scaled proportionally to maintain constant resource density).
2. Codebase identical to Arm 0 (baseline control). Tests whether population scale alone sustains expertise.

### 4.5 Arm 5: The Crucible (Synergistic Triad)
Combines Arms 1, 2, and 3 simultaneously on standard population ($N_0 = 20$).

### 4.6 Arm 6: The Full Synthesis
Combines the Synergistic Triad (Arm 5) with Demographic Scale (Arm 4: $N_0 = 80$).

---

## 5. Experimental Design & Factorial Matrix

| Arm | Description | Making Freedom | Natural Apprenticeship | Memory Protection | Demographic Scale | Code Base |
|---|---|:---:|:---:|:---:|:---:|---|
| **Arm 0** | Control Baseline | ❌ | ❌ | ❌ | $N_0 = 20$ | E7 verified |
| **Arm 1** | Making Freedom | ✅ | ❌ | ❌ | $N_0 = 20$ | Arm 1 branch |
| **Arm 2** | Scaffolded Apprenticeship | ❌ | ✅ | ❌ | $N_0 = 20$ | Arm 2 branch |
| **Arm 3** | Composite Memory | ❌ | ❌ | ✅ | $N_0 = 20$ | Arm 3 branch |
| **Arm 4** | Demographic Scale | ❌ | ❌ | ❌ | $N_0 = 80$ | E7 baseline ($N_0=80$) |
| **Arm 5** | The Crucible Triad | ✅ | ✅ | ✅ | $N_0 = 20$ | Crucible branch |
| **Arm 6** | Full Synthesis | ✅ | ✅ | ✅ | $N_0 = 80$ | Crucible ($N_0=80$) |

---

## 6. Run Specifications & Compute Budget

- **Seeds:** 301, 302, 303, 304 (Identical map topography and founder genetics).
- **Duration:** **120 years** (6,240 ticks) per run, with full demographic and cultural census sampled every 10 years.
- **Rationale for 120 Years:**
  - E7.6 showed that the collapse occurs almost entirely between Years 20 and 100 (skill drops from 0.85 to 0.38; deliberate making drops from 3.1 to 0.6).
  - 120 years covers 4 full generational transitions.
  - Runtime: ~90–120 seconds per run on a single CPU core.
  - Total computational cost: 7 arms $\times$ 4 seeds = 28 runs $\approx$ 42 minutes CPU time.

---

## 7. Measures & Metrics (Fixed in Advance)

1. **Peak and Mean Crafting Skill at Year 100 ($S_{\text{max}}^{100}, S_{\mu}^{100}$):**
   - Best living crafter's skill and mean skill across all living adults at Year 100.
2. **Deliberate Making Rate ($M_{\text{delib}}$):**
   - Deliberate makes per person-decade during the mature epoch (Years 50–100).
3. **Living Recipe Pool at Year 100 ($R_{\text{unique}}^{100}$):**
   - Total number of unique recipes held by at least one living person.
4. **Composite Technology Proportion ($C_{\text{ratio}}^{100}$):**
   - Percentage of living unique recipes that are multi-part composite inventions.
5. **Watertight Vessels & Carried Water ($V_{\text{water}}, W_{\text{drinks}}$):**
   - Count of watertight vessels crafted; count of carried-water drinking events.
6. **Latest First Appearance of Lasting Novelty (LFA):**
   - First year of appearance of any novelty that persists $\ge 50$ years.

---

## 8. Decision Rules & Diagnostic Disambiguation

Evaluated on worlds surviving to Year 100:

- **CCE BREAKTHROUGH:**
  1. Best crafting skill at Year 100 satisfies $S_{\text{max}}^{100} \ge 0.70$ in $\ge 3$ of 4 seeds, AND
  2. Deliberate making rate satisfies $M_{\text{delib}} \ge 2.0$ per person-decade in Years 50–100, AND
  3. LFA $\ge 80$ in $\ge 2$ seeds.
- **ISOLATED MECHANISM IDENTIFIED:**
  - If a single-mechanism arm (Arm 1, 2, 3, or 4) achieves $\ge 85\%$ of the performance of Arm 5/6 across all three breakthrough metrics, that mechanism is declared the primary bottleneck.
- **SYNERGISTIC TRIAD CONFIRMED:**
  - If Arms 1, 2, 3, and 4 each fail individually ($S_{\text{max}}^{100} < 0.50$ or $M_{\text{delib}} < 1.0$), but Arm 5 or 6 achieves CCE Breakthrough, cumulative culture is proven to require the coupled cognitive-social triad.
- **DEGENERATIVE COLLAPSE PERSISTS:**
  - If all arms exhibit $S_{\text{max}}^{100} \le 0.40$ and $M_{\text{delib}} \le 0.80$ by Year 100, the bottleneck lies beyond making, transmission, and demographics (e.g. innovation economics / problems worth solving).

---

## 9. Frozen Predictions

1. **Skill Retention in Arm 2 (Apprenticeship):**
   In Arm 2, guided practice will prevent inter-generational skill collapse: best crafting skill at Year 100 will exceed 0.60 in all surviving seeds (vs. $\le 0.40$ in Control).
2. **Deliberate Making in Arm 1 (Making Freedom):**
   In Arm 1, deliberate making in Years 50–100 will exceed 2.0 per person-decade (a 3-fold increase over Control), but skill will still decay below 0.50 if novices lack scaffolded guidance.
3. **Composite Technology in Arm 3 (Memory Protection):**
   In Arm 3, composite recipe retention at Year 100 will exceed 25% of unique recipes (vs. $<12\%$ in Control), but overall making rates will remain depressed without Arm 1.
4. **Demographic Scale in Arm 4 ($N_0 = 80$):**
   In Arm 4, larger population alone will *not* arrest the skill collapse: best crafting skill at Year 100 will remain $<0.45$, confirming that scale without transmission fidelity cannot sustain expertise.
5. **Synergy in Arm 5 (The Crucible):**
   Arm 5 will produce a statistically significant super-additive synergy:
   $$S_{\mu}^{100}(\text{Arm 5}) > S_{\mu}^{100}(\text{Arm 1}) + S_{\mu}^{100}(\text{Arm 2}) - S_{\mu}^{100}(\text{Arm 0})$$
   Deliberate making, skill retention, and recipe diversity will all be simultaneously preserved.
6. **Watertight Vessels:**
   In Arm 5 and Arm 6, at least one world will craft $\ge 2$ watertight vessels and sustain them in use beyond Year 50.

---

## 10. Kill Criteria (Run Invalidation)

An arm or run is strictly invalid and must be aborted and re-examined if:
1. Any simulation run raises an unhandled exception or crashes.
2. The probe changes the world state (verified via SHA-256 state hash matching between instrumented and uninstrumented 20-year runs).
3. Any form of Lamarckian skill transfer or telepathic state assignment occurs.
4. Any simulation code file changes during the active execution of an arm.
