# ACL resources

The project's reading list, chosen by the creator. Every citation below was checked against arXiv or Crossref. Each entry
says why it matters for ACL and which experiments it speaks to. **Read first** marks what bears on the current work.

Using a source never means copying a behaviour into ACL. Sources may suggest what to *measure* and which *capacities* a
person could plausibly have; the founding rule still holds: nature is programmed, culture is written by nobody.

## Reading plan

The creator's order, with the assistant's suggested changes applied. Full citations for each item are in the sections
below.

**Phase 1 — Understand culture**
1. Mesoudi (2011), *Cultural Evolution*: the readable overview; read first. Then Mesoudi (2011), acquisition costs.
2. Boyd & Richerson (1985), *Culture and the Evolutionary Process*: the formal foundation; easier after Mesoudi.
3. Henrich & Gil-White (2001), prestige; then Henrich (2004), Tasmania.
4. Tomasello (1999), *The Cultural Origins of Human Cognition*: the ratchet effect.
5. Kendal et al. (2018), social learning strategies.

**Phase 2 — Understand artificial societies**
6. Sugarscape (Epstein & Axtell, 1996)
7. The social protocell hypothesis (Andersson & Czárán, 2023)
8. Iterated learning (Kirby, Cornish & Smith, 2008)

**Phase 2.5 — Artificial agents that learn culture** (closest to ACL's current work; can be read first)
9. Ndousse et al. (2021), emergent social learning
10. Cook et al. (2024), cultural accumulation across generations
11. Dalmaijer (2022), cumulative culture in artificial navigators
12. Bhoopchand et al. (2023), imitation as cultural transmission
13. Jaques et al. (2019), social influence as intrinsic motivation

**Phase 3 — Understand modern AI worlds**
14. Crafter (Hafner, 2021): read before Craftax, which is built on it.
15. Craftax and Multi-Agent Craftax (2024, 2025)
16. Neural MMO (2021): mainly a benchmark; skim.
17. Melting Pot (2021): mainly a benchmark; skim.

**Phase 4 — Understand open-ended intelligence**
18. Avida (Ofria & Wilke, 2004): how to run artificial-life experiments rigorously.
19. POET (Wang et al., 2019)
20. Hughes et al. (2024), open-endedness
21. JaxLife (Lu et al., 2024)
22. Werld

---

## 1. Social learning and cumulative culture in artificial agents

**Read first — Ndousse, K., Eck, D., Levine, S. and Jaques, N. (2021).** Emergent Social Learning via Multi-agent
Reinforcement Learning. ICML 2021. [arXiv:2010.00581](https://arxiv.org/abs/2010.00581)
- Ordinary learning agents beside experts mostly did *not* learn from them; social learning appeared only after changes
  to the environment and an added learning signal.
- **For ACL:** the same finding as E12 (planners seen, not copied), in another setting. Their analysis of *why* agents
  ignore experts is the starting point for anything after E13R.

**Read first — Cook, J., Lu, C., Hughes, E., Leibo, J. Z. and Foerster, J. (2024).** Artificial Generational
Intelligence: Cultural Accumulation in Reinforcement Learning. [arXiv:2406.00392](https://arxiv.org/abs/2406.00392)
- Knowledge accumulated across generations when social learning was balanced with independent learning.
- **For ACL:** the untested question after E13R, whether a practice outlasts the people who first learned it.

**Read first — Dalmaijer, E. S. (2022).** Cumulative culture spontaneously emerges in artificial navigators who are social
and memory-guided. [arXiv:2206.06281](https://arxiv.org/abs/2206.06281)
- Minimal agents (goal direction, staying near others, imprecise route memory) produced cumulative improvement across
  generations; removing social proximity or memory weakened it.
- **For ACL:** cumulative culture without sophisticated copying. Relevant to the memory ceiling (E7.6) and to whether
  following others (E13) is already enough of a channel.

**Jaques, N., Lazaridou, A., Hughes, E., Gulcehre, C. and others (2019).** Social Influence as Intrinsic Motivation for
Multi-Agent Deep Reinforcement Learning. ICML 2019. [arXiv:1810.08647](https://arxiv.org/abs/1810.08647)
- Agents rewarded for influencing others' actions coordinated and communicated better.
- **For ACL:** a caution as much as an idea. Rewarding influence is a built-in drive; if ever considered, it must be
  judged against the founding rule.

**Bhoopchand, A., Brownfield, B., Collister, A. and others (2023).** Learning few-shot imitation as cultural
transmission. Nature Communications. [doi:10.1038/s41467-023-42875-2](https://doi.org/10.1038/s41467-023-42875-2)
- Agents learned, in real time, to follow an expert through new worlds and keep the skill after the expert left.
- **For ACL:** what high-fidelity imitation looks like when it works, a comparison point for E13's weak copying.

## 2. Human cultural evolution

**Read first — Henrich, J. and Gil-White, F. J. (2001).** The evolution of prestige: freely conferred deference as a
mechanism for enhancing the benefits of cultural transmission. Evolution and Human Behavior 22(3).
[doi:10.1016/s1090-5138(00)00071-4](https://doi.org/10.1016/s1090-5138(00)00071-4)
- People learn preferentially from those who visibly succeed; prestige grows from that.
- **For ACL:** the theory behind E13's model choice (success, not accumulated respect).

**Kendal, R. L., Boogert, N. J., Rendell, L. and others (2018).** Social Learning Strategies: Bridge-Building between
Fields. Trends in Cognitive Sciences. [doi:10.1016/j.tics.2018.04.003](https://doi.org/10.1016/j.tics.2018.04.003)
- A map of who-to-copy and when-to-copy strategies (success, prestige, majority, uncertainty).
- **For ACL:** the candidate list for model-selection rules after E13R.

**Henrich, J. (2004).** Demography and Cultural Evolution: How Adaptive Cultural Processes Can Produce Maladaptive
Losses. The Tasmanian Case. American Antiquity 69(2). [doi:10.2307/4128416](https://doi.org/10.2307/4128416)
- (Listed by the creator as "the demographic requirements of cultural accumulation, the Tasmanian effect model".)
  A model in which small, isolated populations lose skills because too few learners copy the best well enough.
- **For ACL:** E4 (isolation), E7.6 (skill collapsing across generations), and the open question of 100 against 30.

**Boyd, R. and Richerson, P. J. (1985).** Culture and the Evolutionary Process. University of Chicago Press.
- The founding formal treatment of cultural transmission: biased learning, conformity, and why culture can adapt faster
  than genes.
- **For ACL:** the vocabulary for describing what E9 to E13 tested.

**Mesoudi, A. (2011).** Cultural Evolution: How Darwinian Theory Can Explain Human Culture and Synthesize the Social
Sciences. University of Chicago Press. [doi:10.7208/chicago/9780226520452.001.0001](https://doi.org/10.7208/chicago/9780226520452.001.0001)
- A readable overview of the field and its methods, including simulation and laboratory experiments.

**Mesoudi, A. (2011).** Variable Cultural Acquisition Costs Constrain Cumulative Cultural Evolution. PLoS ONE.
[doi:10.1371/journal.pone.0018239](https://doi.org/10.1371/journal.pone.0018239)
- As culture grows, learning it takes longer, which caps how much can accumulate.
- **For ACL:** close to the memory ceiling (E7.6) and the degenerative loop.

**Tomasello, M. (1999).** The Cultural Origins of Human Cognition. Harvard University Press.
[doi:10.4159/9780674044371](https://doi.org/10.4159/9780674044371)
- The ratchet effect: cumulative culture needs faithful transmission so that improvements are not lost before the next
  one is added.
- **For ACL:** why tools that build on tools have not appeared since E6.

**Read first — Woodburn, J. (1982).** Egalitarian societies. *Man* 17(3).
[doi:10.2307/2801707](https://doi.org/10.2307/2801707)
- Immediate-return societies (food eaten soon after it is got, shared widely, little stored) against delayed-return
  societies (stores and lasting obligations). Not yet read in full; as described in the literature citing it.
- **For ACL:** the interpretation that ACL may have converged on an immediate-return mode of life (N1, N2).

**Peterson, N. (1993).** Demand sharing: reciprocity and the pressure for generosity among foragers. *American
Anthropologist* 95(4). [doi:10.1525/aa.1993.95.4.02a00050](https://doi.org/10.1525/aa.1993.95.4.02a00050)
- Much forager sharing is by demand. **For ACL:** ACL people cannot ask, so sharing on demand is absent (N2).

**Schnegg, M. (2015).** Reciprocity on demand. *Human Nature* 26(3).
[doi:10.1007/s12110-015-9236-5](https://doi.org/10.1007/s12110-015-9236-5)
- Under a demand-sharing norm, real food networks are highly reciprocal. **For ACL:** matches G1 (53% repayment).

**Kelly, R. L. (2013).** *The Lifeways of Hunter-Gatherers.* Cambridge University Press.
[doi:10.1017/cbo9781139176132](https://doi.org/10.1017/cbo9781139176132)
- The diversity of hunter-gatherers; a warning against using any of them as "human nature stripped to its core".

**Bowles, S. and Choi, J.-K. (2018).** The Neolithic agricultural revolution and the origins of private property.
*Journal of Political Economy* 127(5). [doi:10.1086/701789](https://doi.org/10.1086/701789)
- Possession-based property among sedentary foragers as the condition for farming. **For ACL:** stashes are owned but
  undefended (N2).

**Marean, C. W. (2016).** The transition to foraging for dense and predictable resources and its impact on the
evolution of modern humans. *Phil. Trans. R. Soc. B.* [doi:10.1098/rstb.2015.0239](https://doi.org/10.1098/rstb.2015.0239)
- Dense, predictable resources make land worth defending. **For ACL:** does its world offer any (N2)?

**Wengrow, D. and Graeber, D. (2015).** Farewell to the 'childhood of man': ritual, seasonality, and the origins of
inequality. *Journal of the Royal Anthropological Institute* 21(3).
[doi:10.1111/1467-9655.12247](https://doi.org/10.1111/1467-9655.12247)
- Hunter-gatherers alternating between social modes in seasonal environments.

**Kirby, S., Cornish, H. and Smith, K. (2008).** Cumulative cultural evolution in the laboratory: An experimental
approach to the origins of structure in human language. PNAS 105(31).
[doi:10.1073/pnas.0707835105](https://doi.org/10.1073/pnas.0707835105)
- Iterated learning: passing a language through chains of learners makes it more structured and easier to learn,
  with no one designing it.
- **For ACL:** transmission itself shapes what survives. Relevant to stories (E11) and any future signalling.

**Andersson, C. and Czárán, T. (2023).** The transition from animal to human culture: simulating the social protocell
hypothesis. Philosophical Transactions of the Royal Society B 378(1872).
[doi:10.1098/rstb.2021.0416](https://doi.org/10.1098/rstb.2021.0416)
- Names the "startup problem" of cumulative culture, and proposes that it began not with faithful copying of know-how
  but with group-level lifestyles: an inheritance channel that emerges from ordinary group behaviour.
- **For ACL:** a direct alternative to the individual-copying route ACL has tested. If E13R's channel proves too weak,
  this suggests looking at what groups, not individuals, carry.

## 3. Artificial worlds and open-endedness

**Lu, C., Beukman, M., Matthews, M. and Foerster, J. (2024).** JaxLife: An Open-Ended Agentic Simulator.
[arXiv:2409.00853](https://arxiv.org/abs/2409.00853) · [code](https://github.com/luchris429/JaxLife)
- Large evolving populations on the GPU; reports communication, agriculture and tool use.
- **For ACL:** scale, and how to run many more people per world.

**Werld.** [github.com/nocodemf/werld](https://github.com/nocodemf/werld)
- Evolving NEAT brains, no reward function, an energy cost for every neuron, connection and signal.
- **For ACL:** the ideas that complexity should cost energy and that senses could be discovered.

**Epstein, J. M. and Axtell, R. (1996).** Growing Artificial Societies: Social Science from the Bottom Up. MIT Press.
[doi:10.7551/mitpress/3374.001.0001](https://doi.org/10.7551/mitpress/3374.001.0001)
- Sugarscape: social patterns from simple agents. Its behaviours were written by its designers, which ACL forbids.

**Ofria, C. and Wilke, C. O. (2004).** Avida: A Software Platform for Research in Computational Evolutionary Biology.
Artificial Life 10(2). [doi:10.1162/106454604773563612](https://doi.org/10.1162/106454604773563612)
- Digital evolution with careful experimental controls; a model for how to run artificial-life science rigorously.

**Wang, R., Lehman, J., Clune, J. and Stanley, K. O. (2019).** Paired Open-Ended Trailblazer (POET).
[arXiv:1901.01753](https://arxiv.org/abs/1901.01753)
- Environments and solutions that grow more complex together.
- **For ACL:** open-endedness as a co-evolving world, not just smarter agents.

**Hughes, E., Dennis, M., Parker-Holder, J., Behbahani, F. and others (2024).** Open-Endedness is Essential for
Artificial Superhuman Intelligence. [arXiv:2406.04268](https://arxiv.org/abs/2406.04268)
- A working definition of open-endedness (novel and learnable to an observer).
- **For ACL:** useful framing if ACL is ever written up as a paper.

## 4. Environments and benchmarks

**Leibo, J. Z., Duéñez-Guzmán, E., Vezhnevets, A. S., Agapiou, J. P. and others (2021).** Scalable Evaluation of
Multi-Agent Reinforcement Learning with Melting Pot. ICML 2021. [arXiv:2107.06857](https://arxiv.org/abs/2107.06857)
- A suite of social dilemmas for testing agents with others.

**Hafner, D. (2021).** Benchmarking the Spectrum of Agent Capabilities (Crafter).
[arXiv:2109.06780](https://arxiv.org/abs/2109.06780)
- An open-world survival game with resources and crafting.

**Matthews, M., Beukman, M., Ellis, B., Samvelyan, M. and others (2024).** Craftax: A Lightning-Fast Benchmark for
Open-Ended Reinforcement Learning. [arXiv:2402.16801](https://arxiv.org/abs/2402.16801) · **Al Omari, B., Matthews, M.,
Rutherford, A., Foerster, J. N. and others (2025).** Multi-Agent Craftax. [arXiv:2511.04904](https://arxiv.org/abs/2511.04904)
- Crafter-like worlds rewritten in JAX to run very fast on the GPU.
- **For ACL:** the clearest example of how a crafting-and-survival world can be made orders of magnitude faster.

**Suarez, J., Du, Y., Zhu, C., Mordatch, I. and others (2021).** The Neural MMO Platform for Massively Multiagent
Research. [arXiv:2110.07594](https://arxiv.org/abs/2110.07594)
- A large persistent world of many agents with resources, survival and competition.
