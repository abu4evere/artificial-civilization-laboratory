# Council: The same simulated hunter-gatherer world: winter is when people starve, autumn offers enough food to store, but nobody s

Asked 2026-10-14 03:37. **Ideas only; not decisions.** the assistant sorts these against ACL's rules before anything is used.

## The question

The same simulated hunter-gatherer world: winter is when people starve, autumn offers enough food to store, but nobody stores food or sows seeds, because food left somewhere can be taken or shared by others, and the learned value of storing is weak because its reward comes months later. Without scripting storage, what does the evidence on delayed-return versus immediate-return foragers (Woodburn and later work), food sharing norms, demand sharing, ownership and storage, and the evolution of planning say about the conditions under which storage appears? Give the three conditions best supported by evidence, how each could be represented as programmed nature rather than scripted culture, and how each could be tested against a control. Say what you are unsure about.

## nvidia: moonshotai/kimi-k3

# Three conditions under which storage should emerge

## 1. Defensibility: stored food must be excludable, not just ownable in principle

**Evidence.** Woodburn's core contrast is that immediate-return foragers (Hadza, Mbuti, !Kung) share meat and gathered food nearly on demand, while delayed-return societies (Northwest Coast, Calusa, Australian groups with storage) invest in assets — stores, nets, weirs — that are *individually or kin-group defensible*. Testart and later work (e.g., on storage and inequality) show storage correlates with the ability to exclude others, often via sedentism, kin-based defense, or concealment. Demand sharing (Peterson) suppresses accumulation precisely when refusal is socially impossible.

**As programmed nature (not scripted culture):**
- Make *theft/demand cost* a function of physical facts: containers that are heavy, buried, or in a defended shelter raise the effort/risk of taking; agents have a natural aversion to conflict-cost when caught.
- Give agents kin-preference in tolerance (evidence: sharing is preferentially tolerated toward kin — Hamilton's rule is nature, not culture).
- Nothing says "store food." It says: taking from a sealed cache near its owner's sleeping site is costly and risky.

**Test vs. control.** Control: identical world, but caches are universally accessible at zero cost (no defensibility gradient). Prediction: storage emerges only in the defensibility condition, and emerges first among high-kin-density clusters. Falsified if storage appears equally in both arms.

## 2. A planning/anticipation drive: interoceptive memory of past starvation

**Evidence.** The evolution-of-planning literature (e.g., Suddendorf & Corballis on episodic foresight; comparative work on caching in corvids and apes) suggests future-directed behavior rests on the capacity to simulate a future need state *as if* it were present. Humans who have experienced hunger show stronger hoarding/loss-aversion — scarcity experience recalibrates valuation (documented in human behavioral studies of scarcity, e.g., Mullainathan & Shafir, and famine-cohort effects). Storage never appears in populations that have never experienced a lean season severe enough to be remembered.

**As programmed nature:**
- Give agents episodic memory of past drive states and a mechanism whereby *anticipated* future hunger (triggered by seasonal cues — temperature drop, day length) partially activates the current hunger drive. This is a drive-simulation mechanism, not a rule saying "put food in a cave."
- The discount rate for delayed reward should itself be plastic: sharpened by starvation experience. That's a learning-rate parameter grounded in evidence, not a storage script.

**Test vs. control.** Control: agents with flat temporal discounting and no drive-anticipation (same foraging skill, same environment). Prediction: only the anticipation condition produces autumn caching, and within it, agents that have survived ≥1 winter store more than naive agents. Also test a lesion arm: remove the memory-of-hunger mechanism after storage has emerged — does the practice decay? (Evidence check: real traditions of storage persist culturally even after lean periods, so full decay would suggest the model under-weights social transmission.)

## 3. Tolerated-return asymmetry: sharing norms that exempt future shares

**Evidence.** Across foragers, what is shared is not random: large, unpredictable, high-variance packages (big game) are shared widely — this is risk-pooling (Winterhalder's risk-reduction model, Gurven's tolerated-theft vs. reciprocity analyses). Small, predictable, storable items are often *not* subject to demand sharing and can be monopolized. Storage appears where the item type falls outside the sharing norm's scope. Crucially this is not "a rule to store" — it's variation in which resources trigger sharing pressure.

**As programmed nature:**
- Program sharing propensity as a function of package size and acquisition variance (high-variance windfalls trigger strong demand-sharing impulses in others; low-variance accumulated items trigger weaker impulses). This is a tuned social-emotional response (envy/fairness response to windfalls), grounded in the ethnographic pattern.
- Do not program "don't demand from caches." Let the weaker demand response to small accumulated packages make caching viable.

**Test vs. control.** Control: uniform demand-sharing pressure regardless of package type. Prediction: storage emerges only when demand pressure scales with windfall-ness; in the control, any cache is immediately drained, and agents learn caching is worthless (matching your current null result). Manipulate package-size thresholds and check whether the emergence boundary tracks the ethnographic pattern (big game shared, stored plant food not).

---

# What I'm unsure about

- **Whether defensibility alone suffices.** Testart's correlation between storage and sedentism/inequality may be confounded: sedentism may lower transport cost of stores rather than raise defensibility. A cleaner test would independently vary sedentism and cache-defense cost — I haven't specified that interaction and it could flip condition 1's mechanism.
- **Whether drive-anticipation is enough without social transmission.** Real storage is also a *tradition*; my mechanism 2 might produce one-off caching that never stabilizes. If agents in the model cache but don't teach/observe-copy caching, the population-level pattern may be fragile. I'm unsure whether that's a failure of the nature or a correct prediction about how rare storage is without cumulative culture.
- **The demand-sharing function's shape.** The ethnography supports a qualitative windfall/staple distinction, but the quantitative threshold is basically unmeasured. Any parameterization I choose is underdetermined by evidence; the honest test is to sweep the parameter and report which range produces the ethnographic distribution — and flag that as calibration, not prediction.

## nvidia: google/gemma-4-31b-it

Based on the evidence from Woodburn’s distinction between immediate-return (IR) and delayed-return (DR) systems, and the cognitive requirements for planning, here are the three conditions best supported by evidence for the emergence of storage.

### 1. High Environmental Variance (Predictable Seasonality)
**The Evidence:** DR systems emerge not just from scarcity, but from *predictable* pulses of abundance followed by predictable deficits. In IR systems (like the Ju/'hoansi), mobility is the primary strategy to avoid starvation; storage only emerges when the cost of mobility exceeds the cost of guarding a fixed site.
**Programmed Nature:** Implement a "Metabolic Threshold." Instead of a generic hunger drive, give agents a caloric floor below which cognitive function/movement speed drops sharply. If the "winter" dip is deep enough to immobilize agents, the utility of "food in place" outweighs the risk of loss.
**Test:** Compare a world with a steady, low-food year (Control) against a world with a massive autumn glut and a lethal winter (Test). Storage should only emerge in the latter.

### 2. Social Stability and "Territoriality" (Reduced Demand Sharing)
**The Evidence:** Woodburn notes that IR societies have powerful norms of "demand sharing" that act as a social leveler, effectively making storage impossible because any surplus is immediately redistributed. Storage requires a shift toward "ownership" or restricted access—often tied to a specific kinship group or a defended location.
**Programmed Nature:** Program "Kinship-Weighted Trust." Agents should have a higher threshold for sharing with non-kin than with kin. If the "cost" of sharing (loss of calories) is weighed against the "benefit" (social bond), and the kinship bond is programmed as a primary drive, agents will naturally hoard within a small circle.
**Test:** Compare a population where all agents have equal sharing weights (Control) against a population with strong kin-clustering (Test). Storage should emerge only in the kin-clustered group.

### 3. Prospective Memory and Temporal Discounting
**The Evidence:** The "planning fallacy" in simulations often stems from too high a discount rate. Humans evolved the capacity for "episodic future thinking." Storage requires the agent to value a future state (not starving in January) more than the immediate reward (eating everything in October).
**Programmed Nature:** Implement "State-Dependent Value." Instead of a linear decay of reward over time, make the "value" of food a function of the agent's current *and* projected internal state. If the agent "remembers" the starvation state from the previous winter (via a simple memory buffer), the value of food during the autumn glut should be modified by the memory of the winter deficit.
**Test:** Compare agents with a "zero-memory" Markovian state (Control) against agents with a 12-month memory buffer of their own caloric lows (Test).

***

**What I am unsure about:**
I am unsure if "ownership" can truly emerge without some form of territoriality programmed into the nature of the agent. If agents are perfectly mobile and have no innate preference for a "home" coordinate, they may never find a "place" to store food that they feel is "theirs," regardless of kinship or memory. I suspect a "nesting" or "home-base" drive may be a necessary latent variable.

