# Council: An agent-based simulation of small hunter-gatherer bands (no language models; agents learn a table of 544 habit values b

Asked 2026-10-14 15:19. **Ideas only; not decisions.** Claude sorts these against ACL's rules before anything is used.

## The question

An agent-based simulation of small hunter-gatherer bands (no language models; agents learn a table of 544 habit values by reinforcement, 32 situations by 17 actions) has a founding rule: nature is programmed, culture must emerge unscripted. When two agents talk, the listener's whole habit table moves a few percent toward the speaker's if the listener respects the speaker or the speaker seems happier. A measurement just found: (1) habits change about one adult choice in seven; (2) of the adult habit term, about 57 percent comes from this copying in talk, 37 percent from the person's own experience, 6 percent from caregivers, nothing from inheritance at birth; (3) everyone ends up alike: a child's habits correlate 0.96 with their parents' but 0.92 with an unrelated adult's; (4) only about 9 percent of an adult's habits trace back to experience two or more generations earlier; (5) swapping one person's whole habit table with another's barely changes their behaviour, because everyone's tables are so similar. Questions: (a) Is whole-table copying in conversation a defensible model of human social learning, or a shortcut that homogenises the population and erases variation that cumulative culture needs? What does research on conformity, payoff-biased and prestige-biased copying, and copying specific behaviours versus general dispositions say? (b) What would be the smallest honest change, testable against a control, and what would it predict for the five measurements above? Say what you are unsure about.

## nvidia: moonshotai/kimi-k3

## (a) Assessment

Whole-table copying is **not a defensible model of ordinary human social learning**. It is best treated as an implementation shortcut—and the measurements strongly suggest it is doing the cultural work by force.

Humans do not acquire another person’s complete policy from a conversation. Social learning is generally:

- **Selective:** particular practices, interpretations, or responses are copied.
- **Model-biased:** learners prefer prestigious, successful, older, similar, or locally common models.
- **Payoff-sensitive:** apparent success matters, but people also test outcomes themselves.
- **State-dependent:** what is copied depends on the learner’s current problem, uncertainty, and prior habits.
- **Partially inferential:** observers may infer goals or norms from behaviour, rather than directly moving every disposition.

Research on **conformist transmission** does support attraction toward common behaviour, sometimes disproportionately. Prestige- and payoff-biased transmission can also spread traits rapidly. But these mechanisms usually operate over identifiable alternatives, not by averaging entire behavioural architectures. Moreover, conformity experiments show substantial individual resistance, context dependence, and selective use of social information under uncertainty. Even strong conformity does not imply that all 544 habit values move together.

The present measurements are warning signs:

1. **57% social versus 37% individual learning** is not inherently impossible, but the mechanism makes it suspicious.
2. **Child–parent correlation 0.96 versus unrelated-adult 0.92** leaves almost no family-specific transmission.
3. **Only 9% two-generation persistence** indicates rapid replacement rather than cumulative retention.
4. **Whole-table swaps having little behavioural effect** means individual learned variation has become behaviourally irrelevant.
5. Everyone being alike is exactly what whole-table averaging should produce, especially when respect and happiness are themselves broadly shared or correlated.

That does not mean the result is useless. It demonstrates that repeated model-biased averaging can create norms. But it has not shown that human-like selective social learning generates those norms. It also risks erasing the standing variation on which cumulative culture depends: failed variants, local specialisations, minority practices, and recombinable differences.

### Relevant empirical expectations

- **Conformity:** people often shift toward majority behaviour, especially under uncertainty or social risk; they do not uniformly copy majorities.
- **Payoff bias:** demonstrably successful practices are favoured, although perceived rather than actual payoffs can dominate.
- **Prestige bias:** learners disproportionately attend to skilled, respected, or self-similar models; prestige effects are domain-specific.
- **Behaviour-specific copying:** children and adults copy actions and strategies, sometimes even causally irrelevant actions (“overimitation”), but this remains tied to observed sequences and contexts.
- **Disposition transmission:** broad temperament and values are not normally overwritten by brief exposure to another person’s complete disposition profile.

I am unsure how much “conversation” represents in the simulation. If it is intended as years of immersion rather than a discrete talk, whole-table movement is still too direct, but the effective amount of copying might be less unrealistic than it first appears.

## (b) Smallest honest change

Replace whole-table movement with **situation- and behaviour-specific copying**:

> When a listener receives a report or observes an action in situation \(s\), update only the listener’s value for the reported action in \(s\), or a small neighbourhood around that action/situation.

For example:

\[
H_L(s,a) \leftarrow H_L(s,a)
+ \eta \, P(\text{model}) \, U_L(s)\,
[H_S(s,a)-H_L(s,a)]
\]

where:

- \(P(\text{model})\) combines prestige, respect, perceived success, similarity, and possibly local frequency;
- \(U_L(s)\) increases when the listener is uncertain or inexperienced;
- only the communicated \((s,a)\) entry is updated, with optional weak spillover to very similar situations;
- no entry changes merely because the speaker possesses it.

A second small addition, if computationally possible, is **copy-the-observed-action**, not the speaker’s valuation: the listener receives a candidate behaviour and then reinforcement learning evaluates its consequences. That separates “what people try because of others” from “what they retain because it works.”

### Control comparison

Run matched populations under:

1. **Current whole-table copying**;
2. **Cell-specific copying**, with total social-learning opportunity matched as closely as possible;
3. Ideally, a **no-social-learning control** and perhaps a **random-cell copying control** to distinguish selective transmission from merely reducing the copying rate.

Use identical ecology, reinforcement rates, initial variation, population size, mortality, and network structure.

## Predicted effects on the five measurements

### 1. Habit change per adult choice

Whole-table copying should produce more total habit movement because every conversation changes hundreds of entries. Cell-specific copying should reduce raw value turnover.

However, the reported “one adult choice in seven” may not fall proportionally, because only relevant entries change and exploration can still alter choices. The key prediction is therefore not just less movement, but movement concentrated in recently discussed or observed situation–action pairs.

**Falsification:** if whole-table and cell-specific versions produce the same distribution of behavioural change while cell-specific copying leaves no detectable update locality, the implementation may not actually be selective.

### 2. Sources of adult habit variation

The 57% copying contribution should fall, and the 37% own-experience contribution should rise. Social learning should mainly supply candidates; experience should decide retention.

A plausible directional prediction is:

- copying contribution: down;
- experience contribution: up;
- caregiver contribution: up during childhood if caregivers are disproportionately encountered in relevant situations;
- birth inheritance: unchanged, unless temperament or learning parameters are genetically varied.

I would not specify exact replacement percentages; they depend on encounter rates and how attribution is calculated.

### 3. Population similarity

The extreme convergence should weaken. In particular:

- child–parent correlation should remain high because of shared caregivers and ecology;
- child–unrelated-adult correlation should fall more than child–parent correlation;
- between-band differences should become possible if interaction networks are not fully mixed.

A defensible expectation is therefore a **larger family- or band-specific component**, not necessarily low overall similarity. Shared ecology may still make many habits converge because the same actions genuinely work.

**Falsification:** if selective copying still yields correlations around 0.9 between children and arbitrary adults and no stable subgroup structure, homogenisation may be driven mainly by a common reinforcement landscape rather than by the copying rule.

### 4. Persistence across generations

The 9% persistence should increase if successful innovations are retained by reinforcement and transmitted as specific practices. Prestige or success bias can preserve good variants, while conformity can preserve common ones.

But persistence will not automatically increase. If every generation re-solves the same problem through individual learning, old variants may still disappear. Persistent cumulative culture requires mechanisms such as durable skill advantages, teaching, complementary practices, or environmental traces.

A useful diagnostic is whether a seeded advantageous practice survives longer under selective copying than under whole-table averaging.

### 5. Whole-table swap test

Under selective learning, swapping two adults’ full tables should matter more, especially if individuals occupy different roles or learning histories. Yet the effect may remain modest if the shared ecology quickly retrains them.

A stronger test is to swap **only entries for a particular domain**—foraging, danger response, food sharing, childcare, and so on. Behaviour should change mainly in that domain. Global swaps are too blunt to diagnose whether culture is encoded as differentiated knowledge.

## Additional tests that would discriminate the mechanisms

- **Variant-seeding test:** introduce two equally effective practices in different subgroups. Selective conformity should allow local traditions; whole-table averaging should collapse them rapidly.
- **Prestige manipulation:** make one model successful in foraging but poor at danger avoidance. Human-like prestige effects should be partly domain-specific, not transfer the model’s entire table.
- **Payoff test:** pair a prestigious but unsuccessful practice with an unprestigious successful one. Track adoption and retention separately.
- **Uncertainty test:** social copying should be strongest among inexperienced or uncertain agents, not a fixed influence on all entries.
- **Network test:** restrict whom agents encounter. Selective copying should produce lineage, family, or band structure; whole-table copying should erase it.
- **Innovation test:** measure whether novel actions arise, persist, and are refined. Homogenisation without retained innovations is not cumulative culture.

## Bottom line

The current rule is a useful **norm-generation shortcut**, but not an adequate model of human cultural transmission. The smallest honest repair is to transmit specific situation–action information and let reinforcement determine whether it survives. The central prediction is less instant homogenisation, more family/band structure, greater long-term persistence of successful variants, and behaviour that becomes sensitive to differences between individuals’ learned tables.

The main uncertainty is whether homogenisation comes primarily from the copying operator or from all agents facing an almost identical reinforcement environment. The model-specific, no-learning, and common-ecology controls are needed to separate those explanations.

## nvidia: google/gemma-4-31b-it

**(a) Analysis of the current model**

The current "whole-table copying" mechanism is an indefensible shortcut. It functions as a **global averaging filter** rather than social learning.

*   **The Problem:** By shifting the entire table, you aren't copying a *skill* or a *belief*; you are copying a *personality*. This creates a "regression to the mean" effect that erases the niche specializations and trial-and-error variations necessary for cumulative culture.
*   **Research Context:**
    *   **Conformity/Prestige Bias:** Humans don't copy "everything" from a prestige figure; they copy *specific* behaviors that yield high payoffs or are associated with the prestige.
    *   **Specific vs. General:** Social learning is typically **modular**. I copy a master weaver's technique for baskets, but I do not adopt their temperament toward strangers or their sleep habits.
    *   **The Result:** Your 0.92 correlation between unrelated adults confirms the simulation has collapsed into a single, homogeneous "blob." Cumulative culture requires "ratcheting," which needs stable variations to be selected; your model dissolves those variations faster than they can be tested.

**(b) Proposed Change and Predictions**

**The Change: "Situational Copying"**
Instead of moving the whole table, only move the value for the **specific situation** currently being discussed or enacted. 
*   *Mechanism:* When two agents interact in Situation $X$, only the habit value for $X$ (across all 17 actions) moves toward the speaker's. The other 31 situations remain untouched.

**Test against Control:**
Run the simulation with the original "Whole Table" rule vs. the "Situational" rule.

**Predicted Impact on Measurements:**
1.  **Habit change frequency:** Likely *decrease* (from 1/7 to lower), as only the active situation is updated per interaction.
2.  **Sources of habits:** The % from "copying in talk" will drop significantly; the % from "own experience" will rise, as agents must learn non-discussed situations themselves.
3.  **Correlation:** The correlation between unrelated adults will drop sharply (e.g., 0.92 $\rightarrow$ 0.40), while the correlation with parents/mentors will remain higher due to shared environments.
4.  **Generational Trace:** The % tracing back two+ generations will *increase*. Specific successful habits (e.g., "how to hunt deer") will persist as stable "cultural memes" rather than being diluted by a global average.
5.  **Table Swapping:** Swapping tables will now significantly change behavior, as agents will have distinct "expertise" profiles.

**What I am unsure about:**
I am unsure if the "respect/happiness" trigger is sufficient to prevent the population from still homogenizing over very long timescales. If everyone eventually talks about every situation, you may still reach a consensus. You may eventually need a "forgetting" mechanism or a "cost of learning" to maintain diversity.

