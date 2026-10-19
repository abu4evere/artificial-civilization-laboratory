# Council: An agent-based simulation of hunter-gatherers (no language models; agents are simple learners with drives, emotions, mem

Asked 2026-10-13 01:09. **Ideas only; not decisions.** the assistant sorts these against ACL's rules before anything is used.

## The question

An agent-based simulation of hunter-gatherers (no language models; agents are simple learners with drives, emotions, memories and habits learned by reinforcement) has a founding rule: nature is programmed, but culture must emerge and be written by nobody. Today, when two agents 'talk', the simulation directly copies structured knowledge from one mind to the other (gossip about a person, how reliable someone is, where water or game was seen, a remembered event that can be distorted as memory fades, craft know-how, and a pull toward the speaker's habits). The listener weighs it by trust. No signal is produced: meaning arrives already understood, like telepathy with noise. Separately, agents can make visual marks that start meaningless and gain meaning only by learned association. The creator feels this talk looks like a programmed machine: real people talk for many purposes (jokes, screams, warnings, play, comfort, lies) and invent words. Questions: (1) Is direct knowledge copying a defensible simplification for studying emergent culture, or does it undermine the claim that culture is unscripted? (2) What does the research on emergent communication (signalling games, naming games, iterated learning, vocal alarm calls in primates, emergent communication in multi-agent reinforcement learning) say about how a learned signal system could replace it, and at what cost? (3) What would be the smallest honest step, testable against a control, rather than a full redesign? Be concrete and say what you are unsure about.

## ollama: qwen2.5:3b

### (1) Is direct knowledge copying a defensible simplification for studying emergent culture, or does it undermine the claim that culture is unscripted?

**Evidence:**
- **Direct Knowledge Copying:** In the simulation, agents directly copy structured knowledge from one mind to another, including gossip, reliability assessments, and memories. This can be tested by observing the emergence of diverse, adaptive, and context-specific knowledge in a culture. If knowledge is emergent and not directly copied, we should see agents developing their own unique forms of knowledge and not just replicating what they've seen.
- **Unscripted Culture:** If direct copying is not the only way culture can emerge, then it doesn’t undermine the claim of unscripted, emergent culture. An alternative explanation could be that agents learn from direct knowledge copying, but also engage in other forms of interaction (e.g., social interactions, problem-solving, and innovation) that contribute to the emergence of cultural knowledge.

**When I am unsure:**
- **Alternative Models:** I am unsure if other models explaining the emergence of culture, like social learning, imitation, and innovation, can fully substitute direct knowledge copying. The exact role of direct knowledge in a culture’s emergence remains unclear. Also, I am unsure about the extent to which direct knowledge copying can be seen as a simplification that doesn't capture the complexity of cultural evolution.

### (2) What does the research on emergent communication (signalling games, naming games, iterated learning, vocal alarm calls in primates, emergent communication in multi-agent reinforcement learning) say about how a learned signal system could replace it, and at what cost?

**Evidence and Analysis:**
- **Emergent Communication:** Research on emergent communication in multi-agent systems, signalling games, naming games, and vocal alarm calls in primates suggests that signals can evolve in a non-programmed way. For example, vocal alarms start as noise and become meaningful through learned associations. The research shows that meaningful signals can emerge even without direct programming, but they are often context-dependent and may not cover all information.
- **Costs:** The cost of emergent communication might include a loss of precision and the necessity for agents to learn new signals frequently. While signals in signalling games often evolve to communicate complex information, they might be less reliable or less precise compared to signals that are directly programmed. The agents in the simulation might also have to relearn signals frequently, which could be resource-intensive.

**When I am unsure:**
- **Complexity and Precision:** I am unsure how the precision and complexity of signals in a simulated environment compare to those in real human communication. Real humans often need to communicate complex ideas and emotions, which might be harder for emergent systems without direct programming. Also, I am unsure about how the cost of learning and relearning signals could be compared to the benefits of emergent systems.

### (3) What would be the smallest honest step, testable against a control, rather than a full redesign, rather than a full redesign?

**Testable Step:**
- **Reduced Direct Knowledge Copying:** The smallest honest step would be to reduce the frequency or scope of direct knowledge copying in the simulation. For instance, agents could still copy structured knowledge, but not all aspects. For example, they could only copy a random subset of knowledge items, or they could copy only a subset of knowledge items related to survival (e.g., water locations, game sightings) and not all aspects of gossip or reliability assessments.
- **Implementation:** Implement this change and observe the outcomes. If the reduced copying does not substantially alter the cultural development, then it is a valid testable step. If it does alter cultural development significantly, it suggests that direct knowledge copying plays a crucial role.

**When I am unsure:**
- **Impact on Cultural Development:** I am unsure how much the reduction of direct knowledge copying would impact the cultural development. It may not be clear if the reduction would be enough to show that direct knowledge copying is not essential to the emergence of culture, or if it would still be enough to show that culture can emerge without direct copying.
- **Complexity of Cultural Formation:** I am unsure about the complexity of cultural formation. It is unclear how much the reduction of direct copying would affect the emergence of diverse and adaptive cultural practices. The test may not reveal the full extent of the role of direct copying in cultural emergence, but it could provide some insights.

## nvidia: moonshotai/kimi-k3

# Adviser's note

## (1) Is direct knowledge copying defensible?

It is defensible as a *content* channel but indefensible as a model of *communication*, and under the founding rule the distinction matters. The rule is "nature programmed, culture unscripted." Direct copying doesn't script any cultural *content* — no one wrote the gossip, the water locations, the reputations. On that reading it's a legitimate simplification, like abstracting digestion into an energy number.

But it smuggles in three things that are arguably nature-claims without evidence, and one that forecloses the phenomenon:

1. **A shared semantics for free.** Agents parse "X is unreliable" using the sender's own representational scheme. Real humans must negotiate reference; miscommunication, ambiguity, and repair are not noise on the channel, they are engines of cultural divergence (drift between groups, slang, euphemism). Telepathy-with-noise guarantees mutual intelligibility and therefore guarantees a kind of cultural coherence that should be an *outcome*, not an assumption.
2. **No cost, no signal choice.** Real utterances cost time, attention, and social exposure, and speakers *choose* what to say. Copying removes strategic communication — lying as a signal act, withholding, bragging — and replaces it with a fidelity parameter. Deception becomes "corrupt the payload," not "choose to emit a misleading signal," which is a different selective game.
3. **No performative functions.** Jokes, screams, comfort, play are not knowledge transfer; they act on drives and relationships directly. A copy-channel can never produce them, so "talk for many purposes" is ruled out by architecture, not shown to be absent.

Verdict: fine for studying *what spreads*; it undermines the claim if the project wants to study *how shared meaning exists at all*. The honest framing: you've programmed a language instinct with a universal grammar and zero acquisition. That's a strong nature-claim that needs flagging, not a neutral wire.

## (2) What the emergent-communication literature says

- **Signalling games (Lewis; Skyrms).** Conventions for meaning arise from reinforcement alone when there is common interest and a cheap signal channel. Cost: you need many iterated interactions before anything stabilises, and with asymmetric interests you get partial or deceptive signalling — which for you is a feature, not a bug.
- **Naming games (Steels, Baronchelli et al.).** Populations converge on shared vocabularies through local pair interactions with no central semantics, and the convergence dynamics (invention → spread → alignment) are themselves measurable cultural phenomena. Cost: agents need an invention mechanism (random symbol generation) and a cross-situational learning rule; vocabulary convergence takes thousands of episodes in small populations.
- **Iterated learning (Kirby, Smith, Brighton).** Transmission bottlenecks turn holistic, fragile codes into compositional, learnable ones. This is directly relevant: your agents already have memory decay and distortion — that *is* a bottleneck. Cost: you need transmission across "generations" or many successive learners to see structure emerge.
- **Primate alarm calls (vervets: Seyfarth & Cheney).** Functionally referential signals exist with minimal learning of production but learned *comprehension*. This licenses a hybrid: a small innate repertoire of affect-tagged calls (alarm, affiliation, distress) as *nature* (evidence-based), with learned association doing the rest.
- **Emergent communication in MARL (Lazaridou, Foerster, Mordatch, etc.).** Agents reliably invent protocols when a signal is the only way to solve a cooperative task — but the sobering finding is that the protocols are often non-compositional, unstable, and collapse when the incentive changes. Meaning in these systems is grounded only in the task reward. Cost: compute (orders of magnitude more than lookup), and a real risk that nothing interpretable emerges on your timescale.

Consensus cost summary: you trade guaranteed information transfer for (a) large interaction counts, (b) a grounding problem — signals only mean what the reward structure makes them mean, and (c) no guarantee of emergence within simulation time.

## (3) Smallest honest step

Don't replace the copy-channel. **Insert a signal layer in front of it and let the copy-channel remain as a hidden "meaning space" the signals must point into.**

Concrete proposal:

1. Give each agent a small set of producible signals (start with your existing visual marks, or vocal tokens — same mechanism). A "talk" act now emits a *signal*, not content.
2. The listener retrieves whatever association it has learned for that signal (from co-occurrence: signal + shared perceptual context at emission time). If it has no association, nothing transfers.
3. Ground truth for learning comes from joint attention to the same event (both agents see the water; one emits a token; listener associates token→water-schema). This is the evidence-based part: word learning via cross-situational co-occurrence and joint attention is well documented in infants (Tomasello; Smith & Yu).
4. Keep trust as a weight on association-updating, not on content.

**Control comparison:** run paired populations — (A) direct copy as now, (B) signal-mediated as above — identical ecology and seed schedule. Measure: information actually transferred per interaction, spread and accuracy of resource knowledge, between-group divergence of "vocabularies," and whether deceptive or non-informative signal uses (comfort, play) appear at all.

**Predictions that would vindicate it:** (B) converges on shared token→meaning mappings within a feasible number of episodes; group dialects differentiate; transfer is noisier early but approaches (A) for high-frequency, jointly observable content while failing for abstract content (reliability gossip) — which is itself a finding about what needs language-like structure.

**What would falsify/kill it:** no stable mapping emerges in realistic episode counts, or mappings emerge but carry so little that fitness-relevant coordination collapses — meaning the copy-channel was load-bearing and the project must either accept the abstraction openly or invest in the full redesign.

## What I'm unsure about

- Whether joint-attention co-occurrence is enough to ground *social* content (reputation, reliability). I suspect not — there's no shared percept to anchor "X cheated me" for a third party. You may get place/thing words easily and social vocabulary never. I don't know a clean minimal fix that stays honest.
- Whether reinforcement alone will produce the *expressive* functions (comfort, play) without an intrinsic social reward for affecting another's drive state. If agents get no payoff from calming a conspecific, screams and jokes won't emerge regardless of channel design. That may be the deeper gap, and it's a nature-question (is social affect contagious in the model?) rather than a channel-question.
- Timescale. Naming-game convergence results come from clean, dense interaction regimes; in a sparse foraging simulation with realistic contact rates, emergence may be far slower than published numbers suggest.

## nvidia: google/gemma-4-31b-it

As an independent adviser, here are my assessments:

### 1. Is direct knowledge copying defensible?
**Assessment:** No. It is a critical flaw if the goal is "unscripted culture."
Direct copying assumes a **pre-existing shared ontology**. For knowledge to be copied, both agents must already agree on what a "person," "water," "reliability," and "craft" are. By scripting the *categories* of knowledge, the project has scripted the *structure* of the culture. You aren't simulating the emergence of culture; you are simulating the distribution of a pre-defined database.

*   **Evidence/Test:** If you introduce a new environmental feature (e.g., a new type of berry), does the "copying" mechanism automatically handle it, or do you have to write a new "knowledge category" in the code? If the latter, the culture is scripted.

### 2. Lessons from Emergent Communication
Research (e.g., Steels’ Naming Games, MARL signaling) suggests that meaning emerges from the **coordination of signals to achieve a goal**.

*   **The Process:** Agents produce a random signal $\to$ the listener guesses the intent $\to$ if the goal is achieved (e.g., both find the water), the signal is reinforced.
*   **The Cost:** 
    *   **Computational:** Huge increase in "noise" and failure rates initially. 
    *   **Temporal:** Culture takes much longer to stabilize. Agents will spend thousands of cycles "babbling" before a stable lexicon forms.
    *   **Complexity:** You must move from *copying data* to *associating signals with states*.

### 3. The Smallest Honest Step
Instead of a full redesign, implement **"Signal-Gated Access."**

**The Proposal:** 
Keep the "telepathy" mechanism for now, but wrap it in a **learned trigger**. An agent cannot "copy" knowledge unless the speaker produces a specific signal (a "word") that the listener has learned to associate with that category of knowledge.

*   **Concrete Implementation:**
    1.  Define 5-10 "slots" for signals (e.g., sound A, B, C).
    2.  When Agent 1 wants to share "Water Location," they emit Signal A.
    3.  Agent 2 initially ignores Signal A. However, if Agent 2 happens to find water shortly after hearing Signal A, they form a reinforcement link: `Signal A $\to$ Water Knowledge`.
    4.  Now, when Agent 1 emits Signal A, the "copying" mechanism is triggered.

**The Test (vs. Control):**
*   **Control Group:** Current "telepathy" (automatic copying).
*   **Experimental Group:** Signal-Gated Access.
*   **Metric:** Measure the **rate of knowledge spread**. In the control, knowledge spreads instantly. In the experiment, knowledge should spread in "clusters" based on who has successfully coordinated their signals. If the experimental group develops distinct "dialects" (different signals for the same knowledge) across different tribes, you have proven emergent culture.

**What I am unsure about:**
I am unsure if your current reinforcement learning architecture can handle the *temporal delay* between hearing a signal and receiving the reward (finding the water). If the reward is too delayed, the agents may never associate the signal with the knowledge, and the system will collapse into silence.

