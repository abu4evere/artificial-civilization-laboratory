# Neural-network brains for ACL: what is known (8 November 2026)

**Why:** the creator, 8 November 2026: "I think our current structure is more predetermined we should go back to
neural network cuz i think bob's brain will emerge from neural network", and "before starting learn more about neural
network learn everything available then come up to me".

**How it was read:**
- Four reading agents worked from open pages (arXiv HTML and abstracts). PDFs they could not parse were saved, and the
  assistant extracted their text locally.
- Each source is labelled with what was read. **[summary]** marks a point that came only from a reading tool's summary,
  not verbatim text. It is not relied on.
- **A source suggests; only a frozen study decides.**

## 1. Evolved neural brains inside a world

### Polyworld (Yaeger 1994) — **full text read** (extracted locally)
Yaeger L (1994). Computational genetics, physiology, metabolism, neural systems, learning, vision, and behavior or
PolyWorld: Life in a new context. *Artificial Life III*.

The closest earlier world to what the creator describes.
- **What it is:** "biologically motivated genetics, simple simulated physiologies and metabolisms, Hebbian learning in
  arbitrary neural network architectures, a visual perceptive mechanism". All behaviour goes through the brain:
  eating, mating, fighting, moving, turning, field of view, and body light.
- **Brains:**
  - **Genes set the brain's wiring**: the number and size of neuron groups, the excitatory and inhibitory neurons, the
    connection densities, and the learning rate for each pair of groups.
  - **Hebbian learning changes the connections during life.** "Organisms expend energy with each action, including
    neural activity."
- **Scale:** "over 300 organisms, with up to approximately 200 neurons each", about 13 seconds per time-step on 1994
  hardware; 500 generations took about a week.
- **What emerged:** recurring "species" with their own strategies:
  - "frenetic joggers" (run straight ahead, always wanting to eat and mate);
  - "indolent cannibals" (stay near kin; mates readily available);
  - "dervishes";
  - small swarms, "suggestive of simple 'flocking' behaviors";
  - a "following" strategy.

  "The resulting survival strategies, both individual and group, are purely emergent".
- **An important caveat for ACL:** until a population could sustain itself, Polyworld ran "a sort of 'on-line Genetic
  Algorithm (GA)' mode … with an ad hoc fitness function". When numbers fell below a minimum, the system created new
  organisms, some from the fittest so far. Only after a "Successful Behavior Strategy" emerged was "there … no fitness
  function except survival".
- **Its stated future direction:** a developmental ("ontogenetic") process to build the brain from genes.

### Yaeger, Griffith & Sporns 2008 — **saved, not yet read** (title page only)
On "passive and driven trends in the evolution of complexity" in Polyworld. Yaeger's own summary page (read) reports:
- evidence of increasing neural complexity over evolution;
- selection for "small-world" network structure.

### NEAT (Stanley & Miikkulainen 2002) — **abstract only**
Evolves both the weights and the wiring, starting "from minimal structure" and growing. Speciation protects new
structure. Each part was shown necessary.

### Stanley, Clune, Lehman & Miikkulainen 2019 (*Nature Machine Intelligence*) — **abstract only** (paywalled)
Neuroevolution can evolve architectures "and even the algorithms for learning themselves", with "extreme exploration
and massive parallelization".

## 2. Evolution shapes how the brain learns

### Hinton & Nowlan 1987 — **full text read** (extracted locally)
"How learning can guide evolution", *Complex Systems* 1: 495–502.
- **The setup:** a "good net" exists only if 20 connections are all right, "a needle in a haystack". Genes fix some
  switches and leave others to learning. There are 1,000 organisms, each with 1,000 learning trials a life.
- **The result:** with learning, evolution finds the good net. "The same problem was never solved by an evolutionary
  search without learning."
- **Why:** learning builds "a large zone of increased fitness around the good net". There is little pressure to fix the
  last few switches in the genes, because learning finds them. **Nothing learned is inherited.** (This is the Baldwin
  effect.)

### Najarro & Risi 2020 — **read by an agent: verbatim to §5, the rest a summary**
"Meta-learning through Hebbian plasticity in random networks", arXiv 2007.02686.
- **What evolves:** **only a learning rule per connection**, never the weights. Every life starts from random weights.
  The weights change by Δw = η(A·oᵢoⱼ + B·oᵢ + C·oⱼ + D). There is no reward during life.
- **Results:**
  - car racing: 872 ± 11 against 711 ± 16 for fixed weights;
  - a four-legged robot with a leg damaged in a way never seen in training: 452 ± 95 against 68 ± 56;
  - the weights settle within 30–80 steps of a life.
- **Costs:** about 456,640 evolved numbers for the car task. Population 200–500. The learning rules need more search.
  Fixed weights did better on the bodies they were trained on.

### Miconi, Clune & Stanley 2018 — **read by an agent: verbatim to §4.5**
"Differentiable plasticity", arXiv 1804.02464.
- **The mechanism:** each connection has a fixed part and a plastic part (a Hebbian trace that starts at zero each life
  and decays). How plastic each connection is gets learned between lives.
- **Results:** on a memory task, the plastic network learned "250 times faster than the LSTM". A non-plastic recurrent
  network never learned it.

### Soltoggio, Stanley & Risi 2018 (review of evolved plastic networks) — **read by an agent: verbatim about the first 22%**
- Evolution acts as "a meta-learning process"; the brains are "evolved not to learn specific tasks, but to synthesize
  recipes to learn a large variety of general skills".
- **The costs it names:**
  - "the high computational cost required to simulate even simple models of lifelong learning and evolution";
  - deceptive objectives;
  - catastrophic forgetting (the "plasticity-stability dilemma").

## 3. Why small networks learn slowly, and what helps

### Pritzel et al. 2017, Neural Episodic Control — **read by an agent: full main text**
Episodic memory with fast value updates, read out from the 50 nearest stored situations.
- Median human-normalised score on 57 Atari games, against prioritised replay:

  | frames | episodic memory | prioritised replay |
  |---|---|---|
  | 1M | 16.7% | −2.4% |
  | 10M | 54.6% | 22.4% |
  | 40M | 83.3% | 89.0% (replay overtakes) |

- **Why gradient learning is slow:** "Low learning rates mean that experience can only be incorporated into a neural
  network slowly."

### Ha & Schmidhuber 2018, World Models — **read by an agent: verbatim to §4.5**
- **The design:** a large network learns to predict the world without reward; a tiny controller (867–1,088 numbers) is
  evolved on top of it.
- **Why:** "The RL algorithm is often bottlenecked by the credit assignment problem". A small controller keeps the
  search small.
- **A risk:** the controller can "find an adversarial policy that can fool our dynamics model".

### Pathak et al. 2017, curiosity — **read by an agent: verbatim to §4.1**
- **The idea:** reward for failing to predict the result of one's own action, in a learned feature space that ignores
  what one cannot affect.
- **Result:** in the hardest maze start, plain learning never succeeded; with curiosity, a perfect score in 66% of runs.
- **A caution:** "the agent can fall into an artificial curiosity trap".

### Botvinick et al. 2019, "Reinforcement learning, fast and slow" — **not read** (blocked)

## 4. Neural agents that learn from each other

### Ndousse, Eck, Levine & Jaques 2021 — **read by an agent: verbatim to §4.2, the rest a summary**
"Emergent social learning via multi-agent reinforcement learning", arXiv 2010.00581.
- **The finding:** "vanilla model-free RL agents do not use social learning".
- **What social learning needed:**
  - an extra task: **predicting the next state** of the world;
  - **experts present**;
  - **costly exploration**: "with no exploration penalty agents do not learn to rely on social learning".
- With these, the learners "wait and observe while the expert explores", then follow. Most seeds outdid the experts.
  Mixing solo and social experience gave agents that did better alone. Plain learners stalled after one goal.
- **Scale [summary]:** about 375 million steps per run, about 30 hours.

### Bhoopchand et al. 2023 (*Nature Communications*) — **read by an agent: the PMC copy verbatim to the middle of the ablations**
"Learning few-shot imitation as cultural transmission".
- **The ingredients** (each removed in turn): memory (an LSTM), an expert present, the expert dropping out, attention
  to others (predicting the co-player's position), and an automatic curriculum. Without the expert, memory or
  attention to others, transmission fell to zero.
  - "Having an expert at hand is futile if the agent cannot recognise and pay attention to it."
- **The phases:** explore, follow, remember, then become independent and improve:
  - "Our agent stands on the shoulders of giants, and then riffs to climb yet higher."
- **Weights are trained over very many episodes** (about 100 hours before social learning appeared).

### Baker et al. 2019, emergent tool use (hide and seek) — **read by an agent: verbatim to §7**
- **Six stages of strategy emerged** (forts, ramps, box surfing and their defences), though "there are no direct
  incentives for agents to interact with objects".
- **The cost:** 132 million episodes (31.7 billion frames) to stage 4. Smaller batches "never converged".
- **A condition:** "fairly robust as long as we randomize the environment".

### Suarez et al. 2019, Neural MMO — **read by an agent: the main text verbatim**
- **Many agents competing for scarce food** drove exploration and niche formation: "Agents learn to explore only
  because the presence of other agents provides a natural incentive for doing so."
- Populations trained in larger groups beat the others. The study's own caution: "multiagent competition is a
  curriculum magnifier, not a curriculum in and of itself".

## What this suggests for ACL (the assistant's reading; for the creator; nothing decided)
1. **A network learning from scratch within one life is too slow.** That is what PB1 found, and the literature agrees:
   - "experience can only be incorporated into a neural network slowly";
   - every neural-agent success above used millions to billions of steps, or evolution across many generations.
   
   An ACL person makes roughly 1,500–3,000 weekly decisions in a life (a rough estimate: 30–60 years × 52).
2. **Evolution is the answer real life used, and ACL already has it** (genes, birth and death):
   - Polyworld evolved its brains' wiring and learning rates;
   - Hinton & Nowlan show that learning plus evolution solves what evolution alone never did;
   - Najarro & Risi evolve only the *learning rules* and start every life with random weights.
   
   **The catch:** a 200-year ACL world has only about 8–10 generations (a rough estimate at 20–25 years each), far too few for brains to evolve. A neural
   brain would need **deep time**: many generations in the same physics, selected only by survival and children.
   - Polyworld needed a scaffold (system-created organisms with an ad hoc fitness) until populations sustained
     themselves.
   - ACL should avoid any hand-made fitness: survival and birth only, perhaps across many worlds.
3. **Fast learning inside a life comes from memory, not from slow weight change:**
   - episodic memory (NEC: 54.6% against prioritised replay's 22.4% at 10 million frames);
   - Hebbian plasticity (Miconi: 250 times faster than an LSTM on a memory task);
   - ACL's PB1b and PB2 agree.
4. **Learning from others does not come free.** It needed:
   - memory;
   - experts present;
   - attention to others (predicting them or the world);
   - exploration that is costly alone.
   
   ACL has costly exploration and experts. Its people would need to *see* others' actions and results and predict
   them.
5. **Keep the brain small, and the senses and drives built in.** The literature's working designs:
   - World Models: a big learned world model and a tiny evolved controller;
   - Najarro & Risi: random weights with evolved learning rules.

   "Program the body, not the decisions" fits: hunger, cold, pain and loneliness as feelings (rewards), and a small
   network deciding.
6. **Compute is the main practical limit.** Polyworld needed about a week for 500 generations of 300 organisms in 1994.
   ACL's Python worlds would need the cloud, small networks and careful design.

## Not read
- Botvinick et al. 2019 (blocked).
- Stanley et al. 2019's full text (paywalled).
- NEAT's full text: saved but not extracted; the abstract only so far.
- Yaeger et al. 2008's full text: saved, title page only.
