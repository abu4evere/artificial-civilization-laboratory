# Related Work (DRAFT for the creator's review)

Not yet in the README or the book. Citations marked [verify] must be checked against the original before publishing.

---

## Short version (for the README)

ACL belongs to a long line of artificial worlds, and differs from most of them in two ways.

**What changes.** In most open-ended simulations, behaviour improves through genetic evolution: agents with better
networks leave more offspring. In ACL, nothing is inherited but the body. What a person knows, they learned in their own
lifetime, from experience, from watching, or from stories, and it dies with them unless someone else learns it. ACL
asks whether *culture* can accumulate, not whether *genes* can.

**How claims are made.** Every ACL experiment freezes its predictions before any code, compares against a control on the
same worlds, checks that measurement never touches the world, and tests for leaks: ways the experimenter's knowledge
could have been scripted in. Failures are published as failures.

| project | what changes | human knowledge built in | method |
|---|---|---|---|
| JaxLife | genes (evolved networks), at GPU scale | no | paper, evolutionary runs |
| Werld | genes (evolving NEAT brains) | no | observed runs |
| SimWorld | nothing; agents are language models | yes | benchmarks for agents |
| Generative-agent towns | nothing; agents are language models | yes | demonstrations |
| Sugarscape | rules written by the designers | in the rules | exploratory models |
| **ACL** | **culture, learned within lifetimes** | **no** | **pre-registered experiments** |

---

## Long version (for the book, Part VII or an appendix)

### Worlds where life evolves

The oldest relatives of ACL are artificial-life systems in which digital organisms reproduce and mutate: Tierra and
Avida [verify] showed that evolution in a computer can produce real novelty. Two recent projects carry this toward
societies.

**JaxLife** (Lu et al., "JaxLife: An Open-Ended Agentic Simulator", 2024 [verify]) runs very large populations of
agents with recurrent neural networks on the GPU. Agents can program robots capable, in principle, of any computation,
and reshape the terrain; the authors report mass terraforming and coordination between agents and robots. Its scale is
far beyond ACL's. But its agents pass their network weights to their offspring with small mutations: what accumulates is
inherited, as in biology.

**Werld** (nocodemf, open source) starts thirty agents with small NEAT networks on a small-world graph, with no reward
function and an energy cost for every neuron, connection and signal, so that complexity must pay for itself. Senses can
be discovered by evolution, and agents evolve broadcast signals. Its author reports populations growing from 30 to
thousands through repeated famines. Its two best ideas, that complexity has a metabolic cost and that hidden senses can be
discovered, are worth ACL's attention. Its results are observations of single runs, without controls.

ACL differs from both in what it allows to accumulate. Its people have fixed, human-like capacities; everything they come
to know about their world must be learned in a lifetime and passed on socially, or lost. This is the harder problem, and
the one that matters for civilization: human culture grew far faster than human genes changed.

### Worlds run by minds that already know

**SimWorld** (SimWorld-AI; NeurIPS 2025 [verify]) builds realistic cities in Unreal Engine 5 for testing language-model
agents in navigation, planning and cooperation. Generative agents in a small town (Park et al., 2023 [verify]) and
language-model "civilizations" in Minecraft (Project Sid, 2024 [verify]) show agents forming routines, relationships and
roles quickly.

These are valuable for building and testing agents, and they cannot answer ACL's question. A language model trained on
human writing already knows what a village, a trade or a law is. When such agents build one, there is no way to tell
whether civilization emerged or was remembered. ACL's rule, nature is programmed and culture is written by nobody,
exists to keep that door closed: its people have human capacities and no human knowledge.

### Worlds with written rules

**Sugarscape** (Epstein and Axtell, *Growing Artificial Societies*, 1996 [verify]) grew trade, migration, inequality and
conflict from simple agents on a grid, and showed how much social pattern can come from little. But its behaviours,
trading included, were rules its designers wrote. ACL forbids writing any behaviour it hopes to see; its people must
find it, or not.

### What the study of human culture predicts

The closest relatives of ACL's recent experiments are not simulations but theories of cultural evolution. Researchers
such as Boyd and Richerson, and Henrich [verify], argue that humans owe their success to cumulative culture: learning
from others, especially from the successful and the prestigious, so that knowledge outgrows any one mind.

ACL arrived at the same idea from the other side. E12 found that people noticed and respected the planners and did not
copy them; E13 gave them a way to learn from those who visibly do well, which is what that literature calls
success-biased or prestige-biased learning (Henrich and Gil-White, 2001 [verify]). E13 also found something that
literature predicts: in ACL, models chosen by visible success (food in hand) were the planners most of the time, while
models chosen by accumulated respect almost never were. ACL did not start from this theory, and should say plainly
where it rediscovers it.

### Where ACL stands

ACL is small and slow beside JaxLife, and less realistic than SimWorld. What it offers instead is method: frozen
predictions, controls on identical worlds, read-only measurement, leak tests, replication, and published failures. Most
open-ended simulations can say what happened. ACL tries to say what caused it.
