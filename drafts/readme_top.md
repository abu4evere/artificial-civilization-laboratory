# Artificial Civilization Laboratory

**Twenty people wake up on a set of islands knowing nothing. No tools, no fire, no language, no rules. Nobody writes
their history. What do they build?**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![Dependencies: none](https://img.shields.io/badge/dependencies-none-brightgreen)](pyproject.toml)
[![tests](https://github.com/abu4evere/simulated-world/actions/workflows/tests.yml/badge.svg)](https://github.com/abu4evere/simulated-world/actions/workflows/tests.yml)
[![Book: The World That Nobody Wrote](https://img.shields.io/badge/book-The%20World%20That%20Nobody%20Wrote-8a5a44)](https://github.com/abu4evere/simulated-world/releases/tag/book-part-one)

![A live ACL world: 33 people in five bands on a set of islands, with population, ages and group stability](docs/img/viewer.png)

ACL is a simulated world of hunter-gatherers where **nature is programmed and culture is not**. People have bodies,
hunger, cold, fear, love, grief, curiosity and memory. Stone can be struck, wood floats, seeds grow. That is all. No
list of inventions, no reward for being clever, no script. Whatever they come to make, believe or pass on, they find for
themselves, or it never exists.

Then I measure what happens, with the rigour of a lab: every experiment's predictions are written down and locked
before it runs, every world replays bit for bit, and every wrong guess stays in the record.

## What happened in their worlds

- **They invented a raft in their first weeks, and never used it.** Nothing ever showed them what floating was for.
- **One person made the only water vessel in their world, and carried it beside fresh water for two years without
  once filling it.** The thirsty people never had one.
- **A killing was remembered for 180 years, across five generations, and blamed on the wrong person.**
- **Two peoples lived side by side for a thousand years and never met.** Each grew its own marks, crafts and beliefs.
- **Food flows to family:** 72% of gifts go to relatives, and a third of all gifts to brothers and sisters. Nobody wrote that.
- **And culture keeps stalling.** Nine in ten useful inventions are never passed on, and 99% of those are forgotten
  within a season, pushed out of memory before anyone could learn them. Finding out why is what this project does.

| question | answer | record |
|---|---|---|
| Why do a third of small worlds die out? | Not hunger: **people can't find partners.** With perfect partner-finding, 17 of 22 doomed worlds survive. | [F1](experiments/F1_baseline_fragility/findings.md), [F2](experiments/F2_perfect_search/findings.md) |
| Does more land help, or more people? | **People.** 80 founders instead of 20: extinction falls from 2 worlds in 5 to under 1 in 100. | [WS1](experiments/WS1_world_size/findings.md) |
| What decides whether a small world survives? | **How far people can see.** Halve sight: 49 of 64 worlds die; double it: 8. | [SA1](experiments/SA1_sensitivity/findings.md) |
| Where does cumulative culture break? | **At the first hand-over.** About 1 useful invention in 10 is ever learned by anyone else. | [CA1](experiments/CA1_chain_audit/findings.md), [CA2](experiments/CA2_teaching_gates/findings.md), [CA3](experiments/CA3_opportunity/findings.md) |

All 76 studies, with their predictions and results: [`experiments/INDEX.md`](experiments/INDEX.md).

## Read the story

**[*The World That Nobody Wrote, Part One*](https://github.com/abu4evere/simulated-world/releases/tag/book-part-one)**
(free PDF): how the worlds were built, what their people did, and every mistake along the way.

## Run a world yourself

```bash
git clone https://github.com/abu4evere/simulated-world.git
cd simulated-world
python -m acl watch
```

Pure Python, no dependencies. A world opens in your browser: click anyone to follow them and see what is on their mind.

## How it stays honest

- **Predictions first.** Each experiment's plan and guesses are committed and git-tagged before any code or data.
- **Controls and replication.** Changes are compared on identical worlds, with "sham" worlds to show what chance alone
  does, and findings are re-checked on worlds nobody has looked at.
- **Measurement never touches the world.** Every observer is proven read-only: the world ends identical with and without it.
- **No hidden answers.** A test fails if invention names appear in the code people think with.
- **Failures are kept.** Wrong predictions are printed as wrong; corrections are added beside the original, never over it.
- **Check one end to end:** [LK1](experiments/LK1_location_knowledge/): frozen plan
  ([`questions.md`](experiments/LK1_location_knowledge/questions.md), tag `LK1-frozen`) → runner → raw outputs →
  [`results.md`](experiments/LK1_location_knowledge/results.md) → [`findings.md`](experiments/LK1_location_knowledge/findings.md).
