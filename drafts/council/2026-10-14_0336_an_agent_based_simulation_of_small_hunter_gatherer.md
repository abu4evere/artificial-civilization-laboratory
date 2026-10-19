# Council: An agent-based simulation of small hunter-gatherer bands (no language models; agents learn habits by reinforcement, have

Asked 2026-10-14 03:36. **Ideas only; not decisions.** the assistant sorts these against ACL's rules before anything is used.

## The question

An agent-based simulation of small hunter-gatherer bands (no language models; agents learn habits by reinforcement, have drives, memories, kinship, gifts, can make simple tools from recipes, teach and copy by watching) has a founding rule: nature is programmed, culture must emerge unscripted. Observed problem: new practices and tools appear early, then freeze; skills degrade as they pass between generations; people see others succeed but rarely copy them; tools barely matter because the environment is forgiving; worlds of about 20 to 40 people in separate bands rarely meet. From the research on cumulative cultural evolution (population size and connectivity, transmission fidelity, payoff-biased copying, ratchet effects, environmental demand for technology), what are the three most likely causes of the freeze, and for each, a measurable diagnostic that could be run read-only on existing simulated worlds before changing anything? Be concrete and say what you are unsure about.

## nvidia: moonshotai/kimi-k3

Three most likely causes, in order of my confidence:

**1. Population size and connectivity are below the threshold for cumulative culture.**

The strongest replicated finding in this literature (Derex & Boyd; Henrich's Tasmanian model; Muthukrishna & Henrich 2016 on "cultural brain" size) is that ~20–40 people in isolated bands is far too small and too disconnected to sustain complex skills, let alone build on them. Effective cultural population size is what matters, and your bands are effectively isolated, so each world is really several populations of ~8–15 learners. Skill loss across generations is exactly the predicted signature (the "Tasmanian effect").

*Diagnostic (read-only):* Compute effective cultural population size per world: for each skill, count how many distinct demonstrators each learner was actually exposed to over its lifetime, and count inter-band contact events (any co-presence within observation range). Correlate these with per-skill fidelity trajectories. If median demonstrators-per-learner is low (say <3) and inter-band contact is near zero, cause 1 is confirmed structurally. You can also replay existing logs as a "many-bands-connected" counterfactual offline — pool the interaction graph across bands and measure what a learner *could* have seen — but that only bounds the problem; the behavioral bottleneck (cause 2) may still bind. I'm unsure whether 20–40 with occasional contact might be enough for *simple* recipes; the literature mostly concerns complex multi-step technology.

**2. Copying is not payoff-biased enough, or observation doesn't transmit the causal steps (low fidelity, no ratchet).**

"People see others succeed but rarely copy them" plus intergenerational degradation suggests two separable failures: (a) the decision to copy isn't conditioned on observed payoff differences, and (b) even when copying occurs, what's transmitted is the outcome, not the procedure — so each generation re-learns a degraded version (no ratchet: nothing prevents backsliding to the individually-learnable baseline). Reinforcement-driven habits will regress toward what individual learning alone supports unless transmission loss is smaller than individual improvement.

*Diagnostic:* From logs, (a) build a regression: does an agent's probability of adopting an observed behavior increase with the demonstrator's observed payoff relative to the observer's own recent payoff? A flat or weak slope confirms non-payoff-biased copying. (b) Measure transmission fidelity directly: for each teaching/watching event, compare demonstrator's action sequence and success rate to the observer's subsequent attempt; track a skill's mean performance across a transmission chain. If performance decays monotonically down chains and never exceeds the best solo learner's level, there's no ratchet. These are distinguishable: strong payoff-bias + decaying fidelity = transmission problem; flat payoff-bias + stable fidelity = motivation problem. I'm unsure whether your "watching" channel even exposes enough of the action sequence for high fidelity to be possible — that should be checked first, since it caps everything downstream.

**3. The environment doesn't make technology pay, so there's no gradient for culture to climb.**

In a forgiving environment, the payoff difference between tool-users and non-users is small, so (i) payoff-biased copying has nothing to detect, (ii) individual reinforcement doesn't strongly maintain skills, and (iii) small transmission losses aren't selected against. This interacts with cause 2: copying mechanisms can't outperform the noise floor if the signal (payoff difference) is tiny.

*Diagnostic:* Compute, per tool/recipe, the realized payoff advantage: calories/time (or whatever the drive-relevant currency is) for practitioners vs. matched non-practitioners doing the same task in the same patches. Also compute the variance of that advantage. If the mean advantage is small relative to payoff noise, selection on culture is weak by construction. A second read-only check: look at whether skill retention correlates across worlds with local resource scarcity in the logs — if harsher worlds keep skills longer, environmental demand is a live lever. I'm unsure how much of the freeze this explains independently versus merely amplifying causes 1–2; the diagnostics above should be run jointly (e.g., does payoff-bias slope rise where payoff advantages are larger?), because the three causes likely interact rather than acting alone.

## nvidia: google/gemma-4-31b-it

As an adviser to the ACL project, here are the three most likely causes for the cultural freeze, based on cumulative cultural evolution (CCE) theory.

### 1. Insufficient Transmission Fidelity (The "Copying Gap")
The agents are likely failing to capture the precise sequence of actions required for complex tools. If the "copying by watching" mechanism is too noisy or lacks a corrective feedback loop, the "ratchet" slips. Skills degrade because the cost of rediscovering the "correct" habit via reinforcement is higher than the benefit of the imperfectly copied habit.

*   **Diagnostic:** Calculate the **Action-Sequence Correlation** between a master (the innovator) and a learner. Compare the sequence of inputs for a tool-making recipe in Generation $N$ versus Generation $N+1$. If the correlation drops significantly despite the learner "successfully" completing the task, the fidelity is too low to support complexity.

### 2. Lack of Payoff-Biased Copying (The "Indifference Problem")
The agents see others succeed but do not copy. This suggests they are copying based on *frequency* (conformity) or *proximity* rather than *performance*. If an agent doesn't explicitly value the "payoff" (e.g., more calories, less effort) of another's tool, they have no drive to overwrite their own existing habits.

*   **Diagnostic:** Run a **Payoff-Copying Correlation** analysis. For every instance where Agent A observes Agent B using a tool, correlate the *difference in resource acquisition rate* (B minus A) with the *probability that A adopts B's habit*. If the correlation is near zero, the agents are "blind" to the success of others.

### 3. Low Selective Pressure (The "Forgiving Environment")
CCE requires "environmental demand" to prune inefficient habits and reward innovation. If the environment is too forgiving, the fitness delta between a "primitive" agent and a "technologically advanced" agent is negligible. Without a survival or drive-based penalty for inefficiency, there is no pressure to maintain expensive high-fidelity skills.

*   **Diagnostic:** Measure the **Resource Buffer Variance**. Compare the "Drive Satisfaction" levels of agents using tools versus those not using tools. If the variance is low (i.e., both groups stay comfortably above the starvation/failure threshold), the environment is not exerting enough selective pressure to drive the ratchet effect.

***

**What I am unsure about:**
I am unsure if the "freeze" is caused by the **population size/connectivity** (the 20–40 person bands). While CCE generally requires larger populations to avoid stochastic loss of traits, the fact that skills are *degrading* rather than simply *vanishing* suggests a transmission/incentive failure rather than a demographic one. I suspect the "separate bands" issue is a secondary problem that prevents the spread of a "best" practice, but not the primary cause of the initial freeze.

