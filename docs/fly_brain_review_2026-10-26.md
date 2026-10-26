# ACL's learning against the fly's mushroom body: a read-only review (26 October 2026)

Step 2 of GPT's order, which the creator chose ("lets go with gpt's way"; `gpt_view_fly_brain_2026-10-26.md`):
1. finish LS1;
2. **review ACL's learning code against fly-brain principles, read-only** (this file);
3. design the smallest change, with a causal hypothesis;
4. build it on an isolated copy, with zero checks;
5. freeze only with the creator;
6. accept either result.

**Nothing here changes nature or proposes a study.** A design waits for LS1's answer about where knowledge leaks.

## 1. How ACL's people learn today (from the v7 code)

| system | where | what it learns | how |
|---|---|---|---|
| **Habits** | `person.q`, `biology._learn` | how good each action is in a situation | One table: 32 situations (food on hand: 4 bands × alone or with someone × 4 seasons) × each action. Temporal-difference learning from the week's reward and mood change, learning rate 0.05, next week counted at 0.8. **One timescale.** |
| **Copied habits** | talk; `biology._upbringing` | others' habits | Talk copies whole habit tables (BL0: about 57% of an adult's habit term is copied in talk). A child moves 8% a week toward its carer's. |
| **Worth of things** | `knowhow.judge_item` (`itemval`) | how useful a made thing felt | Error-driven, rate 0.15 (0.3 when proved wrong). No time limit while the thing is held (Part One). Drives whether making is weighed at all. |
| **Beliefs about places** | `knowhow.associate`, `_credit` | what leaving something somewhere does | Credits outcomes up to a year back, by place. |
| **Expectations and surprise** | `knowhow.expectation`, `inquiry` | what usually happens | Surprise feeds a curiosity pull ("try it again and see"). |
| **Recipe memory** | `knowhow.remember_recipe` | how to make things | 12 flat slots; the least valued is pushed out. |
| **Trust and credence** | `information` | whom to believe | Per person, from experience of what they said. |

## 2. What the mushroom body does (summary of the literature, to be read in full before any design)

The fruit fly's mushroom body is its main centre for learning which situations predict good or bad outcomes.
- **Sparse, expanded coding:** about 2,000 "Kenyon cells", each sampling a few inputs, with only a small fraction
  active at once. Different situations get different, barely overlapping codes, so learning about one disturbs others
  little.
- **Three-factor learning:** a connection to an output neuron changes only when a Kenyon cell is active *and* a
  dopamine neuron signals good or bad at the same time. Value is learned for the specific situation that was present.
- **Compartments with different speeds:** separate dopamine and output pairs learn and forget at different rates,
  giving short-, middle- and long-lasting memories of the same event in parallel.
- **Approach and avoid outputs** that are weighed against each other. Extinction is often a new, opposing memory added
  beside the old one, not the old one erased, so an old lesson can return.
- **State-dependent use:** hunger and other internal states change which memories steer behaviour.

Sources to read (titles from the assistant's knowledge; to be checked before use):
- Aso et al. 2014, *eLife*, "The neuronal architecture of the mushroom body provides a logic for associative learning".
- Aso & Rubin 2016, *eLife*, on dopamine neurons writing and updating memories with cell-type-specific rules.
- Felsenberg et al. 2018, *Cell*, on parallel opposing memories in extinction.
- Modi, Shuai & Turner 2020, *Annual Review of Neuroscience*, "The Drosophila mushroom body: from architecture to
  algorithm in a learning circuit".

## 3. Where ACL differs (candidate gaps, not conclusions)

1. **Situations are coarse.** All learning about actions is filed under 32 broad situations. Making something with
   flint in hand, beside a fire, while hungry and while not, all share one cell. A person cannot learn "making this
   helps when that", only "making is good or bad when I have little food in summer with company". A sparse, specific
   code is the most striking difference.
2. **One timescale.** Habits learn and forget at one rate. Nothing keeps a fast trace of a recent surprise beside a
   slow, stable memory of what usually works.
3. **Overwriting, not adding.** A value that drops is simply lowered. A good thing tried at a bad moment can lose its
   value for good.
4. **Others' habits outweigh one's own** (BL0: copied about 57%, own experience about 37%). In the fly, learning is
   one's own. In people, social learning is real, but copying whole tables may wash out what an individual learned.
5. **Memory for how to make things is one flat list.** The fly keeps memories of different kinds and durations. Part
   One and the memory studies found the 12-slot list loses new things first (CA3), but keeping by use made people
   know less (MR1). The structure of memory, not its size, may be what matters.

## 4. How this meets LS1 (the decision waits for its results)

- **If LS1 shows making is feasible and weighed but not chosen** (as its smoke test hints), the gap to look at is how
  the *worth* of making is learned: gaps 1 and 2 above. A specific, multi-timescale value for making in its situation
  is a candidate.
- **If LS1 shows knowledge is lost mostly when holders die before passing it on,** the leak is transmission, not
  individual learning, and a fly-inspired learner would not be the fix.
- **If LS1 shows generations rarely take up what their carers knew,** the question becomes how children learn, and
  gap 4 (copying versus own experience) matters most.

## 5. The rules any design must keep (GPT's and the project's)

- Give a **capacity to learn**, never knowledge: no recipes, no tasks, no named inventions.
- A **matched-capacity control:** the same extra memory and computation without the mechanism, so a gain is not just
  "more brain".
- The **primary test is learning:** does earlier experience improve later choices in related, new situations, and
  does the advantage vanish when the mechanism is disabled? Not population.
- Report the **costs**: interference, false associations, worse choices in some places.
- Frozen with the creator first, zero checks, and an independent recompute before findings are final.
