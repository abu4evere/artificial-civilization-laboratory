# Computational and agent-based models of cumulative cultural evolution: population size, connectivity, migration and demography (notes for ACL)

Compiled 2026-10-11. Scope: models, lab experiments and ethnographic tests of when culture accumulates or is lost, written to inform the Artificial Civilization Laboratory (ACL).

**How the sources were checked.** Every DOI below was resolved against Crossref (authors, year, venue, volume and pages matched) or Europe PMC/OpenAlex during this session. Each source has a label for how much of it was read:
- **[FT]**: the open full text was downloaded from Europe PMC and the relevant passages were read. These were extracted by keyword, so I did not read every word.
- **[ABS]**: the abstract was read.
- **[REC]**: the bibliographic record was verified but the content was not read in this session. Any claim about it comes from memory and is marked as unverified.
- **[PRE]**: a preprint that has not been peer-reviewed.

Specific numbers that I remember but could not confirm in this session are listed under Gaps, not as findings.

ACL facts used throughout (from the brief):
- Worlds start with 20 founders and hold 20–40 people in a single band.
- Novelty appears and then freezes for centuries.
- Skills degrade down the generations ("a duller flake").
- 78% of co-resident adults are still together after two years.
- About a third of worlds die out because people cannot find partners.

---

## 1. What do the main models say about population size and cultural complexity, and what conditions make culture accumulate or collapse?

### Takeaway
In the classic "treadmill" models (Henrich 2004; Powell et al. 2009; Kobayashi & Aoki 2012), imperfect copying pulls every skill backwards. A population can only outrun that loss if it has enough skilled models to select from and occasionally improve on. Below a critical effective population size, complex skills decay, and that threshold rises with skill difficulty. However, the result depends heavily on the model's assumptions: very selective copying of the single best model, a wide spread of skill outcomes, how "complexity" is defined, and whether you count census size or the size of the interacting pool. The later literature largely reframes the variable as *effective* or *connected* population size, not head-count.

### Cited Findings
- **Henrich 2004 [ABS].** Ethnohistoric and archaeological evidence suggests Tasmania lost bone tools, cold-weather clothing, hafted tools, nets, fishing spears, barbed spears, spear-throwers and boomerangs over about 8,000 years. In the model, a sudden fall in *effective population size*, defined as "the size of the interacting pool of social learners", keeps simple skills stable or improving while complex skills decay, some to disappearance. — [Henrich 2004, *American Antiquity* 69:197–214, doi:10.2307/4128416](https://doi.org/10.2307/4128416)
- **Structure of Henrich's model (Vaesen 2012 [FT]).**
  - Learners copy the single most skilled individual.
  - Each copy is drawn from a Gumbel distribution: a mean loss α (how hard the skill is) plus a spread β.
  - The expected gain from picking the best of N models grows roughly with ln N. This defines a critical N below which the skill declines.
  - Vaesen finds that Henrich's model "largely withstands" robustness tests.
  - Powell et al.'s model, which adds the assumption that mentors are chosen in proportion to skill, does *not* survive weaker selectivity (random copying or conformity). Vaesen therefore "warrants a fair amount of skepticism" towards Powell et al.'s explanation of the Upper Palaeolithic.
  - Whether real skills follow a Gumbel, Logistic or Normal distribution is "an open empirical question". The extreme spread the Gumbel assumes is less intuitive among adult tutors than across the whole population.
  - [Vaesen 2012, *PLoS ONE* 7:e40989, doi:10.1371/journal.pone.0040989](https://doi.org/10.1371/journal.pone.0040989)
- **Powell, Shennan & Thomas 2009 [ABS].** Demography is "a major determinant in the maintenance of cultural complexity". Regional subpopulation density and/or migration produce spatial structure in skill accumulation. Genetic estimates suggest early Upper Palaeolithic European densities were similar to those in sub-Saharan Africa when modern behaviour first appeared. — [Powell et al. 2009, *Science* 324:1298–1301, doi:10.1126/science.1170165](https://doi.org/10.1126/science.1170165)
- **Kobayashi & Aoki 2012 [ABS].**
  - They reformulate Henrich rigorously and add an overlapping-generations (Moran) version. For large populations it predicts a much larger effect of population size than the discrete-generation model.
  - When each newborn copies the best of only a *limited number of acquaintances*, small relative to N, a change in innovation rate matters more than a proportional change in population size.
  - [Kobayashi & Aoki 2012, *Theor. Popul. Biol.* 82:38–47, doi:10.1016/j.tpb.2012.04.001](https://doi.org/10.1016/j.tpb.2012.04.001)
- **Kobayashi, Ohtsuki & Wakano 2016 [ABS].** In a gene–culture coevolution model where the time split between social and individual learning can evolve, "social connectedness has a larger impact on the equilibrium level of culture than population size especially when connectedness is weak and population size is large". — [Kobayashi et al. 2016, *Theor. Popul. Biol.* 111:87–95, doi:10.1016/j.tpb.2016.07.001](https://doi.org/10.1016/j.tpb.2016.07.001)
- **Mesoudi 2011 [ABS].** If acquisition cost rises with accumulated complexity, cultural complexity reaches an *upper limit above which no further innovation can occur*. The paper also tests unbiased, directly biased and indirectly biased transmission, population size, and innovations that themselves lower acquisition costs. — [Mesoudi 2011, *PLoS ONE* 6:e18239, doi:10.1371/journal.pone.0018239](https://doi.org/10.1371/journal.pone.0018239)
- **Kolodny, Creanza & Feldman 2015 [ABS].** Innovation is built from interdependent processes running at different rates ("lucky leaps", toolkit refinements and combinations). This produces *both* exponential growth and *punctuated* patterns: long stasis broken by sudden gains or losses of many traits. Splitting a population into groups with different repertoires raises susceptibility to loss, and environmental change can rapidly remove traits that are no longer useful. The authors propose an "effective cultural population size". — [Kolodny et al. 2015, *PNAS* 112:E6762, doi:10.1073/pnas.1520492112](https://doi.org/10.1073/pnas.1520492112)
- **Fogarty & Creanza 2017 [ABS].** Adding cultural niche construction (innovations that change the environment for other traits) helps explain why a population-size and toolkit association appears in only some datasets. Niche construction may be stronger in food producers than in foragers. — [Fogarty & Creanza 2017, *Phil. Trans. R. Soc. B* 372:20160428, doi:10.1098/rstb.2016.0428](https://doi.org/10.1098/rstb.2016.0428)
- **Fogarty, Creanza & Feldman 2019 [ABS].** A combined demographic and cultural framework with age-structured "learning life histories" (learning from parents, peers or unrelated elders at different ages) changes cultural outcomes. It helps explain domain-specific patterns and rare demographic events. — [Fogarty et al. 2019, *PLoS Comput. Biol.* 15:e1006821, doi:10.1371/journal.pcbi.1006821](https://doi.org/10.1371/journal.pcbi.1006821)
- **Querbes, Vaesen & Houkes 2014 [ABS].** Demographic effects depend on how complexity is defined. Under Herbert Simon's definition, demography plays "a much more limited role" in sustaining cumulative culture. — [Querbes et al. 2014, *PLoS ONE* 9:e102543, doi:10.1371/journal.pone.0102543](https://doi.org/10.1371/journal.pone.0102543)
- **Andersson & Törnberg 2016 [ABS].** Combining a population-size model with an imitation-fidelity model shows that "group size is found to be important for small but not for larger groups", which improves agreement with data. — [Andersson & Törnberg 2016, *American Antiquity* 81:576–590, doi:10.7183/0002-7316.81.3.576](https://doi.org/10.7183/0002-7316.81.3.576)
- **Andersson & Read 2016 [ABS].** A critical review of the "treadmill model". It argues the model has become entrenched despite critiques and should be integrated with other explanations of cultural complexity. — [Andersson & Read 2016, *Current Anthropology* 57:261–286, doi:10.1086/686317](https://doi.org/10.1086/686317)
- **Premo 2016 [ABS].** Natural and cultural selection weaken the link between census size, cultural diversity and mean skill. Effective population size can differ between traits transmitted by different mechanisms *within the same population*. — [Premo 2016, *American Antiquity* 81:605–622, doi:10.7183/0002-7316.81.4.605](https://doi.org/10.7183/0002-7316.81.4.605)
- **Aoki 2018 [ABS].** Much of the confusion comes from a "mismatch between the theoretical variable and the empirical observable".
  - With the appropriate variable, models predict a positive size–toolkit association under many transmission modes: random oblique, vertical, best-of-K, conformist, anticonformist, success-biased and one-to-many.
  - This holds *only if* population size has been constant and toolkit size has reached equilibrium.
  - Changing population size can erase the correlation.
  - [Aoki 2018, *Phil. Trans. R. Soc. B* 373:20170061, doi:10.1098/rstb.2017.0061](https://doi.org/10.1098/rstb.2017.0061)
- **Shennan 2001 [REC]** is the earlier demography-and-innovation model; its content was not re-read here. — [Shennan 2001, *Cambridge Archaeol. J.* 11:5–16, doi:10.1017/S0959774301000014](https://doi.org/10.1017/S0959774301000014)
- **Enquist, Ghirlanda & Eriksson 2011 [REC]** and **Kolodny, Creanza & Feldman 2016 [REC]** ("game-changing innovations" that alter the parameters of cultural evolution) are related models; records verified only. — [Enquist et al. 2011, doi:10.1098/rstb.2010.0132](https://doi.org/10.1098/rstb.2010.0132); [Kolodny et al. 2016, *PLoS Comput. Biol.* 12:e1005302, doi:10.1371/journal.pcbi.1005302](https://doi.org/10.1371/journal.pcbi.1005302)

### Inferences
- **What ACL's band size means in these models.** A single band of 20–40 people, where each learner effectively copies only a few kin, is exactly the regime the treadmill models predict will lose complex skills. Kobayashi & Aoki's "limited acquaintances" result makes the same point. The "duller flake" pattern is therefore an expected outcome of ACL's demography plus imperfect copying, not necessarily a bug. What matters is whether the *size of ACL's effective learning pool* (not its head-count) is below the critical value for each skill.
- **Why novelty may freeze.** Three mechanisms in the literature could produce ACL's appear-then-freeze pattern:
  - a ceiling set by acquisition costs (Mesoudi 2011);
  - punctuated equilibria (Kolodny et al. 2015);
  - small-N equilibria (Henrich).
  These are not mutually exclusive, and they leave different signatures:
  - A cost ceiling shows learning time per skill rising with complexity.
  - Punctuated dynamics show stasis broken by multi-trait jumps.
  - A treadmill equilibrium shows a stationary mean skill, where each generation's best-of-models gain just cancels the copy loss.
- **Suggestion for ACL: estimate Henrich's parameters from the simulation.** Do not hard-code them. For each skill:
  - Log every learner's resulting proficiency against the proficiency of the model(s) they actually observed.
  - The distribution of (learner − model) gives an empirical α (mean loss) and β (spread).
  - Plug these, with the measured number of models each learner actually watches, into Henrich's threshold to predict whether the skill should grow or decay. Compare that prediction to what ACL actually does.
  - This turns the "duller flake" into a testable quantity.
- **Suggestion for ACL: track effective population size per skill (Premo 2016; Aoki 2018).** Count the people who actually practise or demonstrate each skill and the number of distinct models each learner sampled. Do not use band size. Different ACL skills (gift conventions, marks, flaking) may have very different effective sizes.

### Gaps
- I did not re-read Henrich 2004's full text in this session, so I give no exact critical-N values from the paper.
- Powell et al.'s density and migration thresholds were not verified (abstract only).
- Kolodny, Creanza & Feldman 2016 and Enquist et al. 2011 were not read here.

---

## 2. Lab-experimental and ethnographic evidence that larger or more connected groups keep more complex culture, and the disputes

### Takeaway
The evidence is genuinely mixed:
- **Supporting larger groups:** Derex et al. 2013, Kempe & Mesoudi 2014 and Muthukrishna et al. 2014 (lab); Kline & Boyd 2010 and Collard et al. 2013 (ethnographic).
- **Finding no benefit or the reverse:** Caldwell & Millen 2010 and Fay et al. 2019 (lab); earlier hunter-gatherer toolkit studies.

The PNAS 2016 exchange between Vaesen et al. and Henrich et al. left the core dispute unresolved. One side holds that census population size does not explain the archaeological record. The other holds that the models were never about census size but about the size of the interacting, socially connected learning pool. A recurring mechanism in the "no benefit" results is that learners cannot exploit many models: working memory and selectivity limits.

### Cited Findings
- **Kline & Boyd 2010 [ABS].** Among Oceanic island societies at around the time of early European contact, smaller populations had less complicated marine foraging technology. The paper contrasts this with two earlier quantitative tests on continental data that found no support, where contact rates were not available. — [Kline & Boyd 2010, *Proc. R. Soc. B* 277:2559–2564, doi:10.1098/rspb.2010.0452](https://doi.org/10.1098/rspb.2010.0452)
- **Collard, Ruttle, Buchanan & O'Brien 2013 [ABS].** In 40 non-industrial farming and pastoralist groups, toolkit richness and complexity rose significantly with population size, independently of risk of resource failure. — [Collard et al. 2013, *PLoS ONE* 8:e72628, doi:10.1371/journal.pone.0072628](https://doi.org/10.1371/journal.pone.0072628)
  - Related records, not read here [REC]: [Collard, Buchanan, Ruttle & O'Brien 2011, *Biological Theory* 6:251–259, doi:10.1007/s13752-012-0034-6](https://doi.org/10.1007/s13752-012-0034-6) (toolkits of hunter-gatherers versus food producers); [Buchanan, O'Brien & Collard 2016, *Archaeol. Anthropol. Sci.* 8:625–634, doi:10.1007/s12520-015-0245-4](https://doi.org/10.1007/s12520-015-0245-4) (prehistoric Texas test of the population-size and risk hypotheses).
- **Vaesen, Collard, Cosgrove & Roebroeks 2016 [ABS].** The Henrich and Powell models "only support a relationship between demography and culture in implausible conditions". Their predictions also conflict with archaeological and ethnographic evidence. — [Vaesen et al. 2016, *PNAS* 113:E2241–E2247, doi:10.1073/pnas.1520288113](https://doi.org/10.1073/pnas.1520288113)
- **Henrich, Boyd, Derex, Kline, Mesoudi, Muthukrishna, Powell, Shennan & Thomas 2016 [REC]** replied ("Understanding cumulative cultural evolution"). Vaesen et al. answered with "Reply to Henrich et al.: The Tasmanian effect and other red herrings" [REC].
  - From memory, not re-read: the reply argues the models concern the size and interconnectedness of the social learning network, not census size. Treat this characterisation as unverified.
  - [Henrich et al. 2016, *PNAS* 113:E6724, doi:10.1073/pnas.1610005113](https://doi.org/10.1073/pnas.1610005113); [Vaesen et al. 2016 reply, *PNAS* 113, doi:10.1073/pnas.1613074113](https://doi.org/10.1073/pnas.1613074113)
- **Aoki 2018 [ABS].** Statistical analyses of ethnographic *hunter-gatherers* show *no* correlation between population size and toolkit size. Aoki attributes this to measuring the wrong variable and to non-equilibrium populations. — [Aoki 2018, doi:10.1098/rstb.2017.0061](https://doi.org/10.1098/rstb.2017.0061)
- **Derex, Beugin, Godelle & Raymond 2013 [ABS].** In a dual-task computer game, a simple and a complex task, "players in larger groups maintained higher cultural complexity". With larger groups, knowledge "is less deteriorated", improvements are more frequent and trait diversity is maintained more often. — [Derex et al. 2013, *Nature* 503:389–391, doi:10.1038/nature12774](https://doi.org/10.1038/nature12774)
- **Muthukrishna, Shulman, Vasilescu & Henrich 2014 [ABS].**
  - *Experiment 1 (image editing, 10 lab generations):* learners who could observe five models improved; those with one model showed no improvement.
  - *Experiment 2 (knot-tying):* starting from trained experts, one-model chains *lost skills faster* than five-model chains.
  - In both, every five-model participant in the final generation outperformed the one-model participants.
  - [Muthukrishna et al. 2014, *Proc. R. Soc. B* 281:20132511, doi:10.1098/rspb.2013.2511](https://doi.org/10.1098/rspb.2013.2511)
- **Kempe & Mesoudi 2014 [REC + secondary snippet].** Per a search-result summary, not the paper: transmission chains with one versus three models over four generations on a jigsaw task; viewing three earlier attempts produced accumulation. Unverified in detail. — [Kempe & Mesoudi 2014, *Evol. Hum. Behav.* 35:285–290, doi:10.1016/j.evolhumbehav.2014.02.009](https://doi.org/10.1016/j.evolhumbehav.2014.02.009)
- **Caldwell & Millen 2010 [ABS].** In paper-aeroplane chains with varying cohort size, "Contrary to expectations, there was no advantage for larger cohort sizes." — [Caldwell & Millen 2010, *Learning & Behavior* 38:310–318, doi:10.3758/LB.38.3.310](https://doi.org/10.3758/LB.38.3.310)
- **Fay, De Kleine, Walker & Caldwell 2019 [FT].**
  - n = 543; paper aeroplanes; conditions with 1, 2 or 4 models, plus an individual-learning condition.
  - Larger populations had more variation and better planes available, but there was an *inverse* relationship between population size and cumulative improvement. Only the 1-Model condition improved over generations (by 1.21 m from generation 1 to 8), and the individual-learning condition improved comparably (1.38 m).
  - An exploratory analysis suggests the extra variation "may have overwhelmed their working memory". Working memory holds about four chunks, and each plane involves at least three (artefact, performance, construction method).
  - [Fay et al. 2019, *PNAS* 116:6726–6731, doi:10.1073/pnas.1811413116](https://doi.org/10.1073/pnas.1811413116)
- **Wilks, Atkinson & Caldwell 2022 [ABS].** Children aged 5–10 could not fully combine information from two models when it was spatially or temporally displaced. This suggests combining multiple models is cognitively demanding. — [Wilks et al. 2022, *Culture and Evolution* 19:2–21, doi:10.1556/2055.2021.00005](https://doi.org/10.1556/2055.2021.00005)
- **Thompson, van Opheusden, Sumers & Griffiths 2022 [ABS].**
  - N = 3,450 participants; 12 generations; 20 populations; a sorting-algorithm task.
  - Complex algorithms persisted when participants could *choose whom to learn from*.
  - Without that choice they "frequently became extinct", and populations converged on highly transmissible, lower-performance algorithms.
  - [Thompson et al. 2022, *Science* 376:95–98, doi:10.1126/science.abn0915](https://doi.org/10.1126/science.abn0915)
- **Ethnographic data on band fluidity.**
  - **Hill et al. 2014 [FT].**
    - Ache and Hadza: 20 Ache bands and 42 Hadza bands; 1,201 same-sex adult dyads interviewed.
    - Randomly chosen adults had 5–29% annual probabilities of cultural or cooperative interaction across bands.
    - Hadza and Ache men are estimated to observe more than 300 men making tools in a lifetime, versus about 20 males for chimpanzees.
    - Ache band composition "was stable over periods of months but not years".
    - [Hill et al. 2014, *PLoS ONE* 9:e102806, doi:10.1371/journal.pone.0102806](https://doi.org/10.1371/journal.pone.0102806)
  - **Hill et al. 2011 [REC]** is a co-residence study across 32 foraging societies. The detail that most co-residents are not close kin is from memory and was not verified here. — [Hill et al. 2011, *Science* 331:1286–1289, doi:10.1126/science.1199071](https://doi.org/10.1126/science.1199071)
  - **Bird, Bird, Codding & Zeanah 2019 [ABS].** Residential and foraging groups are small, but "there is little evidence that these groups are drawn from small communities nested within small-scale societies". Membership is fluid and supports large-scale networks dominated by non-relatives. The data are from Martu in Western Australia. — [Bird et al. 2019, *J. Hum. Evol.* 131:96–108, doi:10.1016/j.jhevol.2019.03.005](https://doi.org/10.1016/j.jhevol.2019.03.005)

### Inferences
- **The disputes are about what "size" means.** Census size, the effective pool of models, and the number of models a learner can actually attend to give different answers. Fay et al. 2019 and Thompson et al. 2022 together suggest the benefit of more models depends on learners being able to *select* well among them.
- **ACL's band stability is far from the ethnographic baseline.** 78% of co-resident adults still together after two years contrasts with the Ache ("stable over months but not years") and with Bird et al.'s fluid membership. Real foragers sit in a band-of-bands network in which a lifetime exposes a man to hundreds of toolmakers (Hill et al. 2014). An ACL person sees at most around 40.
- **Suggestion for ACL: build a "models-per-learner" ledger.** Over a lifetime, record:
  - how many distinct individuals each agent observed performing each skill;
  - how many it actually copied from, meaning Q-value updates sourced from social observation.
  Compare with Hill et al.'s order of magnitude (around 300 toolmakers in a lifetime).
- **Suggestion for ACL: run Muthukrishna-style experiments inside a world.** Use seeded A/B runs in which learners can observe 1 versus 5 models (via a social-exposure radius or visiting), all else equal. Measure skill loss over generations. This is an in-silico replication that does not script outcomes.
- **Suggestion for ACL: test the Fay-style failure mode.** If ACL learners cannot rank models by success, more exposure may not help. Log whether learners' choice of model correlates with the model's actual payoff.

### Gaps
- I did not read the full Henrich et al. 2016 reply or the Vaesen et al. reply. I give no claims about their exact arguments beyond titles.
- I did not verify Kline & Boyd's sample of societies and contact coding, Derex et al. 2013's exact group sizes, or Kempe & Mesoudi's exact design. I recall Derex et al. 2013 using groups of 2–16, but this was not checked.
- Collard, Kemery & Banks (2005) on hunter-gatherer toolkits was not located or verified.

---

## 3. Partial connectivity and migration between subgroups: when does it help (recombination) and when does it hurt?

### Takeaway
There is a robust, repeatedly modelled trade-off:
- **Full connectivity** spreads and preserves the best trait. But it collapses diversity through success-biased copying, so there are fewer distinct lineages available to recombine.
- **Heavy fragmentation** generates diversity but cannot hold onto complex traits.
- **Intermediate fragmentation or modular (multilevel) structure** maximises accumulation in several models and one experiment (Derex & Boyd 2016; Derex, Perreault & Boyd 2018; Migliano et al. 2020).

This benefit depends on the transmission mechanism and on population size. Modular networks also make high-value products more likely to go extinct (Cantor et al. 2021), and under unbiased copying network effects are weak (Leite et al. 2026). Migration between otherwise isolated populations can trigger bursts of combinatorial innovation (Creanza et al. 2017). Population turnover can help better variants invade (Chimento et al. 2021).

### Cited Findings
- **Derex & Boyd 2016 [ABS].** In an experiment on a complex fitness landscape, success-biased learning "drastically reduces cultural diversity within fully connected groups". Partially connected groups of the same size produced more diverse solutions and "complex solutions that are never produced in fully connected groups". — [Derex & Boyd 2016, *PNAS* 113:2982–2987, doi:10.1073/pnas.1518798113](https://doi.org/10.1073/pnas.1518798113)
- **Derex, Perreault & Boyd 2018 [ABS].** In an agent-based model, for a given population size there is an *intermediate* level of fragmentation that maximises the rate of cumulative cultural evolution. Fully connected populations maintain complex traits but generate too little variation. Highly fragmented ones produce variety but cannot maintain complexity. — [Derex et al. 2018, *Phil. Trans. R. Soc. B* 373:20170062, doi:10.1098/rstb.2017.0062](https://doi.org/10.1098/rstb.2017.0062)
- **Migliano et al. 2020 [FT].**
  - *Field data.* Agta networks were mapped with wireless sensors: a forest group (7 camps, 53 adults) and a coastal group (3 camps, 37 adults). In the forest, 59% of possible intra-camp dyads were observed versus 28% of inter-camp dyads. Households were mostly close kin, while links between households and between camps were mostly non-kin.
  - *Simulation.* Agents combine virtual medicinal plants along two lineages (A, B). The top-level innovation requires a "crossover" between lineages.
  - *Time to crossover.* In real multicamp networks it took 177.3 rounds (SD 250.5) for the forest group and 516.7 (SD 506.2) for the coastal group. In size-matched fully connected networks it took 509.5 and 698.7 rounds. When innovations were passed only to close kin, it fell to 60.7 (forest) and 99 (coastal) rounds.
  - *Mechanism.* Full connectivity spreads one lineage fast "at the expense of discoveries in the other lineage". Coexisting lineages enable recombination.
  - As innovations became more complex, the share contributed by non-kin dyads rose from 29% to 41% (forest) and from 31% to 48% (coastal).
  - [Migliano et al. 2020, *Science Advances* 6:eaax5913, doi:10.1126/sciadv.aax5913](https://doi.org/10.1126/sciadv.aax5913)
- **Migliano et al. 2017 [REC]** characterised Agta and BaYaka networks; not read here. — [Migliano et al. 2017, *Nat. Hum. Behav.* 1:0043, doi:10.1038/s41562-016-0043](https://doi.org/10.1038/s41562-016-0043)
- **Cantor et al. 2021 [FT].**
  - *Design.* Six architectures (random, small-world, lattice, modular, modular lattice, multilevel) at N = 64, 144 and 324, with degree standardised.
  - "Partially connected networks consistently outperform fully connected networks" in time to recombination. That time was optimised at *intermediate* connection density, and the optimum varied with population size.
  - Modular and multilevel structures promote recombination but "hinder spread and make products more likely to go extinct".
  - Under one-to-many diffusion, multilevel and modular networks did better in small, well-connected and in large, sparse populations. They did *worse* than lattice, small-world or random networks in small, sparse and in large, dense ones.
  - "Transmission mechanisms are therefore critical."
  - [Cantor et al. 2021, *Proc. R. Soc. B* 288:20203107, doi:10.1098/rspb.2020.3107](https://doi.org/10.1098/rspb.2020.3107)
- **Creanza, Kolodny & Feldman 2017 [FT].**
  - Migrants carrying core technologies can produce three outcomes: transient bursts in complexity, a higher steady state, or a positive feedback loop of accelerating accumulation.
  - Loss per trait is scaled as P_SpontLoss/N.
  - In an illustrative run, one population of N = 50 holds roughly 40,000 tools at steady state. The same population split into two disconnected groups of 25 holds roughly 8,000.
  - Even very rare migration (P_migrate = 0.000025 per step) after isolation can trigger change.
  - [Creanza et al. 2017, *J. R. Soc. Interface* 14:20170171, doi:10.1098/rsif.2017.0171](https://doi.org/10.1098/rsif.2017.0171)
- **Premo & Kuhn 2010 [ABS].** In a spatially explicit agent-based model, frequent *local extinctions* of subpopulations within a persistent metapopulation strongly reduce diversity, differentiation and the rate of cumulative change. In some cases this mimics the signature of conformist transmission. — [Premo & Kuhn 2010, *PLoS ONE* 5:e15582, doi:10.1371/journal.pone.0015582](https://doi.org/10.1371/journal.pone.0015582)
- **Smolla & Akçay 2019 [FT].**
  - Networks form by inheriting parents' links (p_n) or by random linking (p_r).
  - Dense networks give higher proficiency but fewer traits; rare traits are filtered out and lost. Sparse networks give larger repertoires but lower proficiency.
  - Selecting for specialists evolves dense networks; selecting for generalists evolves sparse ones.
  - Random linking (p_r) matters more than inherited links because it shortens path length.
  - [Smolla & Akçay 2019, *Science Advances* 5:eaaw0609, doi:10.1126/sciadv.aaw0609](https://doi.org/10.1126/sciadv.aaw0609)
- **Chimento, Alarcón-Nieto & Aplin 2021 [ABS].** In 18 captive great-tit populations, gradual replacement with naive immigrants "greatly increased the probability" that a more efficient behaviour displaced an established inefficient one. Turnover acted on *adoption*, not innovation: immigrants disproportionately sampled the novel efficient behaviour. — [Chimento et al. 2021, *Current Biology* 31:2477, doi:10.1016/j.cub.2021.03.057](https://doi.org/10.1016/j.cub.2021.03.057)
- **Gunasekaram et al. 2024 [ABS].** Chimpanzee population networks were built from genetic markers of recent (female) migration and from shared cultural traits. "Limited levels of group connectivity favored the emergence of a few instances of cumulative culture". The authors propose that greater between-group mobility in *Homo* drove dependence on cultural exchange. — [Gunasekaram et al. 2024, *Science* 386:920–925, doi:10.1126/science.adk3381](https://doi.org/10.1126/science.adk3381)
- **Padilla-Iglesias et al. 2022 [ABS].** Central African hunter-gatherers "stem from a deep history of partially connected populations". This allowed relatively large effective population sizes alongside local differentiation. — [Padilla-Iglesias et al. 2022, *PNAS* 119:e2113936119, doi:10.1073/pnas.2113936119](https://doi.org/10.1073/pnas.2113936119)
- **Schimmelpfennig, Razek, Schnell & Muthukrishna 2022 [ABS].** Sociality, fidelity and trait diversity can each both increase and harm innovation, through challenges of coordination, conformity and communication. This is the "paradox of diversity". — [Schimmelpfennig et al. 2022, *Phil. Trans. R. Soc. B* 377:20200316, doi:10.1098/rstb.2020.0316](https://doi.org/10.1098/rstb.2020.0316)

### Inferences
- **ACL has no between-group level at all.** It has one band, almost no turnover (78% together after two years) and no immigrants. In model terms this is a single small module with no source of foreign lineages to recombine. It has neither the maintenance benefit of size nor the diversity benefit of fragmentation. Creanza et al. 2017's illustration shows that isolation alone cuts steady-state repertoire several-fold.
- **Suggestion for ACL: a multi-band world as a structural treatment.** Nothing should be scripted culturally. Seed several bands (for example 4–8 bands of 20–40) on a shared landscape. Let visiting, marriage and seasonal aggregation arise from drives (food, partners, kin). Then measure:
  - **Inter-band contact rate** per adult-pair per year, compared with Hill et al.'s 5–29%.
  - **Lineage diversity**: the number of distinct variants per skill across bands, and time to first cross-band recombination, following Migliano and Cantor.
  - Whether accumulation peaks at intermediate contact rates (Derex, Perreault & Boyd 2018). Vary the cost or attractiveness of travel, not the outcome.
- **Suggestion for ACL: a turnover test (Chimento 2021).** When an immigrant joins a band, do better variants spread faster afterwards? Log adoption events by newcomers versus residents.
- **Caution for ACL.** Cantor et al. and Leite et al. (Section 5) show that the advantage of structure is conditional on the transmission rule. ACL should report which learning rule its agents effectively follow (random, success-biased or kin-only) before interpreting any connectivity effect.

### Gaps
- Grove 2016 ("Population density, mobility, and cultural transmission", *J. Archaeol. Sci.* 74:75–84, [doi:10.1016/j.jas.2016.09.002](https://doi.org/10.1016/j.jas.2016.09.002)) [REC] is directly relevant to mobility and transmission but was not read.
- The Mesoudi migration and acculturation model (PLOS ONE 2018, between-group variation) was located only as a bioRxiv preprint and a correction record (doi:10.1101/234807; correction doi:10.1371/journal.pone.0216316). I did not resolve the original article's DOI. It is not cited as a finding.
- Lab experiments on migration between *experimental* subgroups (beyond Derex & Boyd 2016) were not searched systematically.

---

## 4. Transmission fidelity and degradation: models of loss under imperfect copying, and how many models or teachers keep a skill from degrading

### Takeaway
Fidelity and the number of models interact; neither alone is enough (Kempe, Lycett & Mesoudi 2014; Andersson & Törnberg 2016). Small gains in fidelity can switch a population from traditions to ratcheting (Lewis & Laland 2012). Empirically, five models versus one slowed skill loss from experts in a knot-tying chain (Muthukrishna et al. 2014). But more models only help if learners can select or integrate (Fay et al. 2019; Wilks et al. 2022; Thompson et al. 2022). No paper gives a universal "number of teachers needed". The threshold depends on the copying-error distribution of the specific skill (Henrich 2004; Vaesen 2012).

### Cited Findings
- **Lewis & Laland 2012 [ABS].** Small increases in transmission fidelity can produce cumulative culture. Modification and combination have less influence, and novel invention "appears unimportant" to ratcheting. Progress depends more on combination than on invention or modification. — [Lewis & Laland 2012, *Phil. Trans. R. Soc. B* 367:2171–2180, doi:10.1098/rstb.2012.0119](https://doi.org/10.1098/rstb.2012.0119)
- **Kempe, Lycett & Mesoudi 2014 [ABS].** Social learning accuracy and the *number of cultural demonstrators* jointly determine the maximum trait complexity a population can maintain. Combining the models produces two regimes: "a few, simple traits" (non-human-like) or "many, complex traits" (human-like). — [Kempe et al. 2014, *J. Theor. Biol.* 359:29–36, doi:10.1016/j.jtbi.2014.05.046](https://doi.org/10.1016/j.jtbi.2014.05.046)
- **Andersson & Törnberg 2016 [ABS].** When population size and fidelity models are combined, group size matters for small groups but not for larger ones. — [doi:10.7183/0002-7316.81.3.576](https://doi.org/10.7183/0002-7316.81.3.576)
- **Muthukrishna et al. 2014 [ABS].** Starting from trained experts, one-model chains lost knot-tying skill faster than five-model chains. — [doi:10.1098/rspb.2013.2511](https://doi.org/10.1098/rspb.2013.2511)
- **Derex et al. 2013 [ABS].** In larger groups, cultural knowledge "is less deteriorated". — [doi:10.1038/nature12774](https://doi.org/10.1038/nature12774)
- **Copying error as a source of drift.**
  - **Eerkens & Lipo 2005 [REC]** model copying error. The widely cited estimate of a perceptual error of about 3% (a Weber fraction) for size attributes comes from my memory and was *not* verified here. — [Eerkens & Lipo 2005, *J. Anthropol. Archaeol.* 24:316–334, doi:10.1016/j.jaa.2005.08.001](https://doi.org/10.1016/j.jaa.2005.08.001)
  - **Kempe, Lycett & Mesoudi 2012 [REC]** experimentally tested the accumulated-copying-error model for Acheulean handaxe size. — [*PLoS ONE* 7:e48333, doi:10.1371/journal.pone.0048333](https://doi.org/10.1371/journal.pone.0048333)
- **Thompson et al. 2022 [ABS].** Selective social learning (choosing whom to copy) preserved rare complex algorithms. Without it, populations drifted to "highly transmissible lower-performance algorithms", a fidelity-driven simplification. — [doi:10.1126/science.abn0915](https://doi.org/10.1126/science.abn0915)
- **Derex, Bonnefon, Boyd & Mesoudi 2019 [ABS].** A physical artefact was optimised across generations without explicit causal understanding. Transmitting causal theories did not speed improvement and constrained exploration. — [Derex et al. 2019, *Nat. Hum. Behav.* 3:446–452, doi:10.1038/s41562-019-0567-9](https://doi.org/10.1038/s41562-019-0567-9)
- **Fay et al. 2019 [FT].** Individual trial-and-error produced improvement comparable to single-model social learning (1.38 m versus 1.21 m over 8 generations). — [doi:10.1073/pnas.1811413116](https://doi.org/10.1073/pnas.1811413116)
- **Mesoudi 2011 [ABS].** Acquisition cost that rises with complexity produces a ceiling on complexity. — [doi:10.1371/journal.pone.0018239](https://doi.org/10.1371/journal.pone.0018239)
- **Muthukrishna & Henrich 2016 [ABS].** Innovation rates depend on sociality, transmission fidelity and cultural variance, and these shape each other. — [Muthukrishna & Henrich 2016, *Phil. Trans. R. Soc. B* 371:20150192, doi:10.1098/rstb.2015.0192](https://doi.org/10.1098/rstb.2015.0192)
- **Morgan et al. 2015 [REC]** is experimental evidence that teaching and language improve the transmission of stone-tool-making (Oldowan-style flaking). It is directly relevant to the ACL "flake" skill but was not read here. — [Morgan et al. 2015, *Nat. Commun.* 6:6029, doi:10.1038/ncomms7029](https://doi.org/10.1038/ncomms7029)

### Inferences
- **The "duller flake" in model terms.** It is Henrich's α > 0: systematic loss per copy. In a 20–40 band with kin-limited observation, the "best-of-K" gain is small because K is small. The remedies in the literature are more models, higher fidelity (teaching or practice), or selection of better models. Each could *emerge* in ACL, for example from gifts or apprenticeship driven by drives, rather than being hard-coded.
- **Suggestion for ACL: build the fidelity curve empirically.** For each skill, plot transmitted proficiency against the number of distinct models observed (K = 1, 2, 3…) and against time spent practising beside a model. This gives a per-skill "minimum K to hold the skill" estimate that ACL can report and track over versions.
- **Suggestion for ACL: separate social from individual learning.** Q-learning means agents also learn on their own. Fay et al. 2019 suggests individual trial-and-error can rival single-model copying. ACL should log the share of each skill's proficiency attributable to social versus individual updates. If the social share is near zero, there is nothing to accumulate culturally.
- **Suggestion for ACL: test for model selection.** Is the person a learner watches correlated with that person's skill (a success or prestige bias), or random or kin-only? Thompson et al. 2022 implies this is pivotal for keeping complex variants.

### Gaps
- I found no source giving a general numeric "teachers needed" threshold independent of the skill's error distribution, and I believe none exists.
- Morgan et al. 2015 and Eerkens & Lipo 2005 were not read; numbers from them are not reported.

---

## 5. Recent (2020–2026) computational work on cumulative culture (multilevel and network models, "cultural ratchet" conditions), and what ACL could measure or test

### Takeaway
Since 2020 the field has moved from "bigger is better" to "structure × transmission rule × cognition":
- Multilevel hunter-gatherer networks accelerate recombination (Migliano 2020). This is conditional on network type, size and transmission mechanism (Cantor 2021), and on learning bias (Leite et al. 2026 preprint).
- Selective social learning preserves complex solutions (Thompson 2022).
- Semantic or structured knowledge guides innovation (Yaman et al. 2026).
- Population connectivity explains even chimpanzee proto-cumulative culture (Gunasekaram 2024).
- Demographic viability work shows a single 20–40 band is near or below sustainable size.

For ACL, the main lesson is to measure effective learning pools, lineage diversity, inter-group contact and demographic viability, and to add an emergent between-band level. It should not script culture.

### Cited Findings
- **Derex & Mesoudi 2020 [ABS].** A review that synthesises how both population size and *structure* shape the pool of information available for innovation. It also asks whether human social networks themselves partly result from selection for reliance on cumulative culture. — [Derex & Mesoudi 2020, *Trends Cogn. Sci.* 24:654–667, doi:10.1016/j.tics.2020.04.005](https://doi.org/10.1016/j.tics.2020.04.005)
- **Migliano et al. 2020 [FT]** and **Cantor et al. 2021 [FT]**: see Section 3.
- **Leite, Reia, Mesoudi & Campos 2026 [PRE, ABS, bioRxiv, not peer-reviewed].** Mesoudi's 2011-style model is extended to random, scale-free, small-world and Mason–Watts networks under three biases: unbiased, indirect (copy successful individuals) and direct (copy successful traits).
  - Unbiased transmission: network effects are weak except at very low connectivity.
  - Indirect bias: complexity increases with connectivity.
  - Direct bias: optimal at *intermediate* connectivity, a diffusion–diversity trade-off.
  - Topology matters modestly once average degree is fixed.
  - "No single social structure universally promotes cumulative cultural evolution."
  - [Leite et al. 2026, bioRxiv, doi:10.64898/2026.04.15.718734](https://doi.org/10.64898/2026.04.15.718734)
- **Yaman, Tian & Lindström 2026 [ABS].** An agent-based model plus an experiment (N = 1,243) show that semantic knowledge directs exploration, enhances innovation, interacts synergistically with social learning and accelerates cumulative change. Participants without semantic knowledge performed no better than chance even with social learning. — [Yaman et al. 2026, *PNAS*, doi:10.1073/pnas.2530750123](https://doi.org/10.1073/pnas.2530750123)
- **Thompson et al. 2022 [ABS]**: selective social learning preserves complex algorithms (Section 4).
- **Gunasekaram et al. 2024 [ABS]**: limited connectivity favoured the few cases of chimpanzee cumulative culture (Section 3).
- **Garg, Padilla-Iglesias, Restrepo Ochoa & Knight 2021 [ABS].** In an agent-based model of central-place foraging, intermediate environmental heterogeneity and mobility increased global and local network efficiency and the rate of contagion-based information transmission. Central-place mobility further improved transmission in larger populations. — [Garg et al. 2021, *R. Soc. Open Sci.* 8:211324, doi:10.1098/rsos.211324](https://doi.org/10.1098/rsos.211324)
- **Romano, Lozano & Fernández-López de Pablo 2020 [ABS].** Proposes a multilevel network framework linking hunter-gatherer social structure to cumulative culture, with predictions from local- and global-level network metrics. — [Romano et al. 2020, *Biological Reviews* 95:1020, doi:10.1111/brv.12599](https://doi.org/10.1111/brv.12599)
- **Deffner & McElreath 2020 [ABS].** Adding endogenous age structure and population regulation reverses intuitions. Social learning is favoured more in "fast" life histories; long lifespans favour individual learning. The authors call for frameworks with strategic learning and cumulative culture. — [Deffner & McElreath 2020, *Phil. Trans. R. Soc. B* 375:20190492, doi:10.1098/rstb.2019.0492](https://doi.org/10.1098/rstb.2019.0492)
- **Schimmelpfennig et al. 2022 [ABS]**: the "paradox of diversity" and "cultural evolvability" (Section 3).
- **Demographic viability (relevant to ACL extinctions).**
  - **White 2017 [FT via page summary; check before quoting].** A non-spatial agent-based model gives "a stable population size of about 150 persons" as demographically viable against stochastic mortality, fertility and sex-ratio fluctuations. Less restrictive marriage rules improve the viability of small populations. Per the page summary, populations under about 40 were not viable over 400 years in the model, and 40–50 were viable only under the most permissive rules. These small-N figures came through an automated summary and should be confirmed against the paper. — [White 2017, *JASSS* 20(4):9, doi:10.18564/jasss.3393](https://doi.org/10.18564/jasss.3393)
  - **Wobst 1974 [ABS, numbers not verified].** Classic Monte Carlo simulation of the minimal size of Palaeolithic mating networks. — [Wobst 1974, *American Antiquity* 39:147–178, doi:10.2307/279579](https://doi.org/10.2307/279579)
- **Premo & Kuhn 2010 [ABS].** Local extinctions within a metapopulation suppress cumulative change (Section 3).
- **Mesoudi & Thornton 2018 [REC]** give definitional criteria for cumulative cultural evolution. These are useful for deciding what counts as a "ratchet" in ACL; not re-read here. — [Mesoudi & Thornton 2018, *Proc. R. Soc. B* 285:20180712, doi:10.1098/rspb.2018.0712](https://doi.org/10.1098/rspb.2018.0712)

#### Source register (what was read)
- **Full text, key passages read [FT]:**
  - Migliano 2020
  - Cantor 2021
  - Fay 2019
  - Creanza 2017
  - Hill 2014
  - Vaesen 2012
  - Smolla & Akçay 2019
  - White 2017 (via an automated page summary)
- **Abstract read [ABS]:**
  - Henrich 2004; Powell 2009; Kline & Boyd 2010
  - Derex 2013; Derex & Boyd 2016; Derex, Perreault & Boyd 2018; Derex & Mesoudi 2020; Derex 2019
  - Vaesen 2016; Collard 2013; Aoki 2018; Premo 2016; Premo & Kuhn 2010
  - Mesoudi 2011; Kobayashi & Aoki 2012; Kobayashi et al. 2016
  - Fogarty 2019; Fogarty & Creanza 2017; Kolodny 2015
  - Caldwell & Millen 2010; Muthukrishna 2014; Muthukrishna & Henrich 2016; Schimmelpfennig 2022
  - Lewis & Laland 2012; Kempe, Lycett & Mesoudi 2014; Querbes 2014; Andersson & Törnberg 2016; Andersson & Read 2016
  - Thompson 2022; Wilks 2022; Chimento 2021; Gunasekaram 2024; Padilla-Iglesias 2022; Garg 2021
  - Deffner & McElreath 2020; Romano 2020; Bird 2019; Yaman 2026; Wobst 1974
- **Preprint abstract read [PRE]:** Leite et al. 2026.
- **Record only [REC]:**
  - Henrich et al. 2016 reply; Vaesen et al. 2016 reply
  - Kempe & Mesoudi 2014 (plus a secondary snippet)
  - Migliano 2017; Hill 2011; Shennan 2001; Enquist 2011; Kolodny 2016
  - Eerkens & Lipo 2005; Kempe, Lycett & Mesoudi 2012; Morgan 2015; Mesoudi & Thornton 2018
  - Grove 2016; Collard 2011; Buchanan 2016
  - Read 2006 ("Tasmanian knowledge and skill", *American Antiquity* 71:164–184, [doi:10.2307/40035327](https://doi.org/10.2307/40035327)), a critique of the Tasmanian loss interpretation.

### Inferences
These are concrete, honest measurements and tests for ACL: measure, don't hard-code.

1. **Effective learning pool per skill.** Log, per agent and per skill, the distinct models observed and the models actually copied. Report the distribution, not band size. This is the variable the models actually use (Henrich; Aoki 2018; Premo 2016).
2. **Empirical copy-loss parameters.** Fit α and β per skill from learner-versus-model proficiency. Predict Henrich's critical pool size and check whether ACL skills that decay are those predicted to decay. This distinguishes the "duller flake" being a demographic consequence from it being an implementation artefact, for example Q-values not transferring.
3. **Diagnose the freeze.** Classify centuries of stasis as one of:
   - a treadmill equilibrium (stable mean skill, loss equal to gain);
   - a cost ceiling (learning time rising with complexity, Mesoudi 2011);
   - an innovation shortage (no new variants generated);
   - punctuated stasis awaiting a "lucky leap" (Kolodny 2015).
   Each predicts different logs.
4. **Lineage diversity and recombination.** Tag every variant with its origin, recording who and which band. Measure the number of coexisting lineages per skill and whether any innovation combines variants from different households or bands (Migliano 2020's crossover metric).
5. **Mixing and inter-band contact.** Report annual contact probability between random adult pairs across groups (Hill 2014: 5–29%) and co-residence turnover. ACL's 78% two-year persistence suggests far less fluidity than the Ache or Martu (Hill 2014; Bird 2019).
6. **Structural treatment, not a cultural script.** Run multi-band worlds and let fission, fusion, visiting and marriage arise from drives (partner seeking, food, kin). Then test whether accumulation peaks at intermediate contact (Derex et al. 2018; Cantor 2021; Leite 2026).
7. **Demographic viability as a confound.** Check whether the worlds that die out are below White 2017's viable range, and whether marriage rules are restrictive (incest avoidance, kin exclusion). Culture-loss results should be reported conditional on surviving worlds, and the size of the marriage pool should be logged. The third of worlds that die out is consistent with an isolated band of 20–40 being below viable size. A metapopulation is the realistic fix, not a tuning hack.
8. **In-silico replications.** One versus five accessible models (Muthukrishna 2014); turnover with immigrants (Chimento 2021); selection versus no selection of models (Thompson 2022). Each is an A/B on seeded worlds with outcome metrics fixed in advance, so results cannot be cherry-picked.

### Gaps
- I did not find any published agent-based model that combines Q-learning individual agents with seasons, kinship, storage and emergent cumulative culture in a way directly comparable to ACL. This search was not exhaustive.
- I did not read most 2023–2026 work beyond abstracts, and there may be relevant JASSS or *Evolutionary Human Sciences* papers I did not find in the limited number of searches.
- Leite et al. 2026 is unreviewed.
- The White 2017 small-N figures need confirming from the paper itself.
