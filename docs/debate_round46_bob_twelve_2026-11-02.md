# Debate round 46: the creator's twelve capacities for Bob (2 November 2026)

**Why:** the creator sent (Telegram, 2 November 02:21) twelve capacities that "may create Bob". The Telegram session
read them against v11 (`docs/research/bob_twelve_capacities_2026-11-02.md`) but could not ask the models. This round
asks them.
- **Who:** GPT in a fresh chat (`6ae8506b`) and Gemini in a fresh chat (`c422a1f1fa63affe`; it answered as "Flash").
- **What was sent:** the same text to both, saved as `research/local/round46_bob12.txt`.
- **Each answer is an opinion, not a sign-off.** Only the creator decides.

## The question (summary)
(a) Which of the twelve must be minimal laws, which should emerge, and which are results of others? (b) One honest
read-only measure for each. (c) What is missing, or should be merged? (d) Which ONE to work on next as a frozen study
that adds a condition, not an outcome, with an estimate (%).

## Gemini (opinion, not sign-off)
- **(a) Its three groups:**
  - **laws:** perception (1), memory with retrieval (2), motivation and emotion (11);
  - **should emerge:** causal understanding (4), planning (5), invention (6), goals (7), communication (9), culture (10);
  - **results of others:** learning with transfer (3), self-model (8), identity (12).
- **(b) A measure for each.** For example:
  - perception: how fast choices shift after an unannounced change in the world;
  - memory: how often the memories recalled match the present situation, beyond chance;
  - invention: working combinations that were neither given nor copied;
  - communication: the information signals carry about states others cannot see;
  - culture: how long complex recipes survive in a population across deaths;
  - identity: how far identical twins' action profiles diverge.
- **(c) Merges and gaps:**
  - merge learning with memory and causal understanding;
  - merge self-model with identity;
  - missing: **mental rollout before acting**, and a rule for which variables enter the situation (instead of a fixed
    32-cell grid).
- **(d) Its pick:** **prospective mental simulation** (the condition for planning), at **85%**.
  - **The mechanism:** when surprise or conflict is high, sample k steps ahead through memories and associations, and
    add a prospective weight to the choice.

## GPT (opinion, not sign-off; it thought for 3 minutes 24 seconds)
- **Its principle:** "ACL should program the conditions that make thinking possible, not the thinking itself."
- **(a) L = a minimal law, E = should emerge, R = a result of others:**

  | capacity | GPT's label |
  |---|---|
  | perception (1) | L |
  | memory (2) | L for storage and retrieval, E for effective use |
  | learning (3) | L for plasticity, E for transfer |
  | causal understanding (4) | E |
  | planning (5) | E |
  | invention (6) | E, needing an open-ended action law |
  | goals (7) | E, needing a way to keep commitments |
  | self-model (8) | E, needing access to one's own history |
  | communication (9) | L for channels, E for symbols |
  | social cognition and culture (10) | E for social cognition, R for cumulative culture |
  | motivation and emotion (11) | L for basic drives, E for regulation |
  | identity (12) | R |

- **(b) Behavioural measures, for example:**
  - **memory:** does an old, relevant experience improve a decision long after, compared with matched unfamiliar
    situations?
  - **causal understanding:** when a material's effect changes apart from its usual context, does the person follow
    the real cause?
  - **planning:** a cost paid now for a future need, beyond what rewards and seasonal habits explain;
  - **communication:** can one person tell another something about an absent thing, so that the other acts
    successfully without seeing it?
  - **culture:** improvements that pass through several people, outlive their inventors, and go beyond what any one
    person found.

  GPT's caution: "These are behavioral indicators, not proof of internal cognition". Where v11 lacks the behaviour,
  the honest result is "not identifiable".
- **(c) Missing or to merge:**
  - missing: **working memory and attentional control**, and **compositional action and physical affordances**;
  - separate social cognition (a person's) from cumulative culture (a population's);
  - identity is not a module to build.
- **(d) Its pick:** **capacity 6, open-ended action composition.** A study "AC1":
  - **the condition:** let people combine general physical operations on materials and objects within reach;
  - **arms:** v11 / AC1 / a sham;
  - **the primary:** new, unspecified combinations that have checkable effects **and are reused by choice**.
  - **Estimate: 75%** that the study would be valid and informative, "not ... that intelligence emerges". The main risk:
    v11's physics may not be general enough to judge new combinations "without quietly scripting their results".

## Checked against the code and the records (the assistant, as council)
- **Memory "retrieval when relevant" does not exist in v11.**
  - Memories enter choices only by strength and feeling: the most salient painful memory, grief, the latest salient
    memory in talk, and gossip by salience (`thought.py` 116–132, `information.py` 148, `mind.py` 443).
  - Nothing recalls a memory because it matches the present situation.
  - So Gemini's memory measure has nothing to measure yet. Capacity 2 is weaker than the 2 November note's "given store,
    learned content" suggests: the store is given; **relevant retrieval is missing.**
- **Gemini's goal measure echoes a written law.** Its "preemptive homeostatic index" (acting before a deficit) would
  re-measure `anticipation_weight`, the law that a season of shortage is felt a season early.
- **Gemini's reason for its pick conflicts with the records:**
  - **It says habit undervaluation "creates the primary bottleneck where 90% of know-how dies with its holder".** KL1
    found know-how is lost because **lone holders die**; it measured no link to habit values.
  - **It says undervaluation comes from collapsed multi-step credit.** UV2 tested a version of this ("propagation" from
    unpractised choices ahead) and found it was **not** the cause.
  - **Its claim that a rise in culture would "prove" undervaluation was the barrier is too strong.** A rollout law
    changes many things at once.
- **What survives:** planning by mental rollout is a real gap (ODD v11 §9), and a fair candidate. But it is a large
  change to how people choose. It would need a frozen nature-change test in a copy, the creator's approval, and a
  design that does not tune toward an outcome.
- **GPT's pick misses one fact.** v11's making is **already compositional over things**:
  - fiddling strikes, binds (nesting made things), shapes, heats and fills;
  - each result is described only by its physical properties, with no recipe list.

  What v11 lacks is **new kinds of action**: a sequence that becomes one act, or a new verb. GPT was told this and asked
  which it means.

## Second round (each model given the facts and the other's main argument)
**Gemini (opinion, not sign-off):**
- **It accepts all three checks:**
  1. **memory:** relevant retrieval "is indeed a missing minimal law rather than an existing mechanism";
  2. **its goal measure:** it echoed `anticipation_weight`. It offers instead "Drive-Unrelated Task Persistence": how
     long a multi-step routine continues after the need that started it is back in the safe zone;
  3. **its pick:** mental rollout "targets the wrong bottleneck for cultural preservation" (KL1, UV2).
- **Its estimate drops from 85% to 40%.**
- **On GPT's pick (open-ended action composition):** "a trap for ACL's current architecture". Without a way to filter
  and value new action kinds, an open action space over 32 coarse situations and TD at rate 0.05 would make habit
  learning "collapse under the curse of dimensionality".
- **It agrees with GPT** on separating social cognition (a person's conditions) from cumulative culture (a population
  outcome).
- **The council's note:** "useless if the agent has no structural way to evaluate their utility before trying them" is
  too strong. ACL's people try untried things and learn from the result (the curiosity pull, play). The cost Gemini
  names is real, though: every new action kind dilutes learning over a fixed table.

**GPT (opinion, not sign-off), given the composition facts and Gemini's first pick:**
- "The code correction changes my recommendation. I underestimated v11's existing creativity."
- **AC1, narrowed:** **temporal composition**, turning an experienced action sequence into a reusable unit. Each part
  still costs its normal time and resources, gets no novelty reward, and can fail. **Its estimate falls to 60%.**
- **It now favours capacity 5 (prospective reasoning), as "PL1", in a weaker form than Gemini's:**
  - **the condition:** a **fallible** internal simulation built only from each person's own remembered transitions,
    with no oracle for the world's rules;
  - **kept for a separate study:** choosing which variables enter the situation;
  - **the primary:** completing naturally available multi-step sequences that need a costly first step and pay off
    later, especially ones the person has not completed before;
  - **its estimate: 72%.** Not Gemini's 85%: coarse situations, limited memory and the known habit miscalibration make
    imagined futures unreliable.
- **The models crossed over.** GPT moved toward planning (72%) at the moment Gemini moved away from it (40%). Neither
  had seen the other's revision. Both were then given it, with one last question (below).

## Last question: a read-only scorecard first, or a nature change?
- **The question to both:** given the creator's order (knowledge that survives death first; define and measure
  autonomy early), should the next step be a read-only scorecard of the twelve capacities in today's worlds, before
  any nature change?
- **GPT (opinion):** "Yes. I now favor a read-only baseline scorecard before any nature change." **90%**, "provided
  unobservable capacities are explicitly marked not measurable, rather than scored zero".
  - It calls this **SC1**, a cognitive baseline of v11, with "No combined intelligence score, no nature changes".
  - "PL1 should no longer come first. Its possible benefits are too indirect for the creator's immediate priority."
  - After SC1: "select the smallest missing condition that addresses the observed bottleneck in knowledge transmission
    or retention."
- **Gemini (opinion):** "Yes, the read-only scorecard should come first". **90%**.
  - Its first nature-change test after that: **cue-driven transmission**. A holder's relevant know-how would be called
    up by what the other person is doing or handling, instead of by global salience. This targets KL1's
    lone-holder loss.

## Outcome (the assistant, as council; the creator decides)
- **Both models agree:**
  - **next:** a read-only scorecard, SC1. It needs no nature change, so it is allowed under the 40% rule;
  - **after it:** the smallest missing condition aimed at keeping know-how alive.
- **Checked against the code:** teaching in v11 (`information.show_how`) offers one of the teacher's three most valued
  things **at random**, whatever the learner is doing. So "teaching what is relevant to the listener" is a real gap,
  and a fair candidate condition later.
- **What survived the debate:**
  - **Relevant memory retrieval is missing:** both models accepted the code check.
  - **Working memory is missing:** GPT raised it and Gemini agreed.
  - **Social cognition (a person's) and cumulative culture (a population's) are separate.**
  - **Object composition already exists.**
  - **The council's view of the estimates:** planning (PL1, 72% from GPT, 40% from Gemini) and action composition (60%
    from GPT; Gemini calls it a trap) stay later candidates, not next steps.
- **SC1 still needs:** its own frozen plan, with measures chosen so they do not echo written formulas (both models
  gave candidates above), and "not measurable in v11" where the behaviour cannot occur.
