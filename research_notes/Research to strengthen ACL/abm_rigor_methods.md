# Research methods for scientific rigour in agent-based models (social / cultural / archaeological), for ACL

Scope note. Written 2026-10-11 to inform the Artificial Civilization Laboratory (ACL), a hunter-gatherer ABM that already uses: frozen pre-registered predictions, discovery/holdout seeds, sham arms, paired sign tests, power analysis, read-only observers verified by state hashes, and openly appended corrections.

Verification method. Every DOI below was resolved against the Crossref API (authors, year, title, venue, volume, pages checked) on 2026-10-11; abstracts were pulled from OpenAlex / Europe PMC; some full texts were read via the publisher page. Each source carries one label:
- **full text read**: the article page was fetched and its body summarised (via a fetch tool that summarises; not a line-by-line human read).
- **abstract read**: only the abstract was read.
- **record only**: the bibliographic record was verified in Crossref, but content claims about it come from prior knowledge and were NOT re-checked this session. Treat those claims as lower confidence.

Year conventions. Several papers appeared online a year before their volume. Both years are given where they differ (e.g., "online 2013, vol. 2014").

---

## 1. Pattern-oriented modelling (POM): validating an ABM against multiple empirical patterns at once

### Takeaway
POM tests a model against several weak, independent patterns at different scales and levels together, rather than against one strong pattern. Since 2020 the ODD protocol builds this in through a "Purpose and patterns" element. ACL's frozen predictions are close to POM in spirit, but they appear to be predictions about the simulation's own behaviour, not a pre-declared set of *empirical* hunter-gatherer patterns that the model must reproduce together.

### Cited Findings
- Grimm, Revilla, Berger, Jeltsch, Mooij, Railsback et al. (2005). "Pattern-Oriented Modeling of Agent-Based Complex Systems: Lessons from Ecology." *Science* 310:987–991. DOI 10.1126/science.1116681. **record only**. Known content: patterns observed at several scales and hierarchical levels act as filters. They are used to (a) choose model structure, (b) compare alternative submodels ("theories") of agent behaviour in a strong-inference way, and (c) narrow parameter ranges (inverse modelling). — [Crossref/DOI](https://doi.org/10.1126/science.1116681)
- Grimm & Railsback (2012). "Pattern-oriented modelling: a 'multi-scope' for predictive systems ecology." *Phil. Trans. R. Soc. B* 367:298–310. DOI 10.1098/rstb.2011.0180. **record only**. — [DOI](https://doi.org/10.1098/rstb.2011.0180)
- Gallagher, Chudzinska, Larsen-Gray, Pollock, Sells et al. (2021). "From theory to practice in pattern-oriented modelling: identifying and using empirical patterns in predictive models." *Biological Reviews* 96:1868–1888. DOI 10.1111/brv.12729. **abstract read**. Finding: ABM production has risen quickly, but "the explicit use of POM has not increased." The review gives guidance on where in the hierarchy to find patterns, which kinds of pattern are useful, "how should simulations and observations be compared", and when in the modelling cycle to use patterns. — [DOI](https://doi.org/10.1111/brv.12729)
- Railsback & Grimm (2019). *Agent-Based and Individual-Based Modeling: A Practical Introduction*, 2nd ed., Princeton University Press. DOI 10.2307/jj.28274141. **record only**. A textbook with chapters on POM, model calibration and theory development using patterns. — [DOI](https://doi.org/10.2307/jj.28274141)
- Grimm et al. (2020) ODD update made the first element "Purpose and patterns". The patterns are "observations, at the individual or system level, that are believed to be driven by the same processes, variables, etc. that are important for the model's purpose" (**full text read**, see §2). — [JASSS 23(2) 7](https://www.jasss.org/23/2/7.html)
- Edmonds et al. (2019) give "Reproduce multiple patterns simultaneously to filter unrealistic parameters" as a mitigation for *explanation*-purpose models (**full text read**, see §6). — [JASSS 22(3) 6](https://www.jasss.org/22/3/6.html)
- Archaeological example of multi-pattern testing: Carrignon, Brughmans & Romanowska (2020), *PLOS ONE* 15:e0240414, DOI 10.1371/journal.pone.0240414 (**full text read**). They scored three competing cultural-transmission hypotheses jointly against two patterns: "Pattern A" (ware distribution through time) and "Pattern B" (site diversity). — [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0240414)
- Hunter-gatherer ABM with ethnographic grounding: Janssen & Hill (2014). "Benefits of Grouping and Cooperative Hunting Among Ache Hunter–Gatherers: Insights from an Agent-Based Foraging Model." *Human Ecology* 42:823–835. DOI 10.1007/s10745-014-9693-1. **record only**. The model draws on Ache foraging data. Also Janssen & Hill (2016), an agent-based model of resource distribution and hunter-gatherer foraging strategies, in *Computational Social Sciences* (Springer) pp. 159–174, DOI 10.1007/978-3-319-31481-5_3. **record only**. — [DOI](https://doi.org/10.1007/s10745-014-9693-1)

### Inferences
- ACL has: frozen predictions and a discovery/holdout split. These are the machinery POM needs.
- ACL lacks (probably; confirm against ROADMAP): a frozen, pre-declared **empirical pattern set** drawn from ethnography and archaeology. Examples: camp-size distributions (the often-cited ~25-person band and its variance), mobility frequency and distance, food-sharing networks, age-specific mortality and fertility curves, kin composition of residential groups, and the tails of the forager return-rate distribution. Each would carry a pre-stated acceptance band.
- Suggestion: add a POM table to the pre-registration. Columns: pattern, source dataset, level (individual / band / region), metric, acceptance criterion. Require the model to pass **jointly**. Hold some patterns back as "holdout patterns", the empirical analogue of holdout seeds: never inspect them during calibration and test them once at the end. Use the patterns to adjudicate *alternative submodels*, for example sharing rule A versus B, the way Grimm et al. 2005 and Carrignon et al. 2020 do, rather than only checking one model.

### Gaps
- I did not find a published hunter-gatherer ABM that runs a full, explicit POM multi-pattern validation with holdout patterns. That does not show none exists; search coverage was limited.
- The precise empirical values (e.g., band-size statistics) were outside scope and are not sourced here.

---

## 2. ODD protocol (2006, 2010, 2020), ODD+D, TRACE, and documentation standards

### Takeaway
ODD (Overview, Design concepts, Details) is the de facto description standard. The 2020 second update adds "Purpose and patterns" and optional "Rationale" subsections, and endorses short "Summary ODDs". TRACE is the companion standard for documenting the *evidence* behind a model: development, testing and analysis. ACL's hash-verified observers and appended corrections are TRACE-like practices but are not yet structured as a TRACE document.

### Cited Findings
- Grimm, Berger, Bastiansen, Eliassen, Ginot, Giske et al. (2006). "A standard protocol for describing individual-based and agent-based models." *Ecological Modelling* 198:115–126. DOI 10.1016/j.ecolmodel.2006.04.023. **record only**. — [DOI](https://doi.org/10.1016/j.ecolmodel.2006.04.023)
- Grimm, Berger, DeAngelis, Polhill, Giske, Railsback et al. (2010). "The ODD protocol: A review and first update." *Ecological Modelling* 221:2760–2768. DOI 10.1016/j.ecolmodel.2010.08.019. **record only**. — [DOI](https://doi.org/10.1016/j.ecolmodel.2010.08.019)
- Grimm, Railsback, Vincenot, Berger, Gallagher, DeAngelis et al. (2020). "The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism." *JASSS* 23(2) 7. DOI 10.18564/jasss.4259. **full text read**. Points found:
  - It keeps the 7 elements, but element 1 becomes "Purpose and patterns".
  - Each element gets an optional "Rationale" subsection, because "describing the rationale for an ABM's design in ODD has substantial benefits."
  - It gives guidance for "Summary ODDs" in a paper's main text.
  - "The proportion of papers using ODD has grown significantly only in the life sciences."
  - It proposes ODD as a "lingua franca for simulation modelling", and suggests governance and maintenance structures.
  — [JASSS](https://www.jasss.org/23/2/7.html)
- Müller, Bohn, Dreßler, Groeneveld, Klassert et al. (2013). "Describing human decisions in agent-based models – ODD + D, an extension of the ODD protocol." *Environmental Modelling & Software* 48:37–48. DOI 10.1016/j.envsoft.2013.06.003. **record only**. ODD+D adds a "Decision" section (theoretical and empirical basis of decisions, learning, individual sensing and prediction, social interaction). This fits ACL, whose agents make social and cultural decisions. — [DOI](https://doi.org/10.1016/j.envsoft.2013.06.003)
- Grimm, Augusiak, Focks, Frank, Gabsi, Johnston et al. (2014). "Towards better modelling and decision support: Documenting model development, testing, and analysis using TRACE." *Ecological Modelling* 280:129–139. DOI 10.1016/j.ecolmodel.2014.01.018. **record only**. Known content: TRACE = "TRAnsparent and Comprehensive model Evaludation". Its standard sections are problem formulation, model description, data evaluation, conceptual model evaluation, implementation verification, model output verification, model analysis, and model output corroboration. — [DOI](https://doi.org/10.1016/j.ecolmodel.2014.01.018)
- Ayllón, Railsback, Gallagher, Augusiak, Baveco et al. (2021). "Keeping modelling notebooks with TRACE: Good for you and good for environmental research and management support." *Environmental Modelling & Software* 136:104932. DOI 10.1016/j.envsoft.2020.104932. **record only**. It argues for a running TRACE-structured notebook kept during development, not written afterwards. — [DOI](https://doi.org/10.1016/j.envsoft.2020.104932)
- Lemmen & Sommer (2024). "Good modelling software practices." *Ecological Modelling* 498:110890. DOI 10.1016/j.ecolmodel.2024.110890. **abstract read**. It argues good practices (tractable development workflow, collaborative governance, continuous integration and deployment, licensing, software paper, archiving) should be adopted "early on", not "as an add-on … at a later stage". Its highlights begin "You must publish your model software". — [DOI](https://doi.org/10.1016/j.ecolmodel.2024.110890)

### Inferences
- ACL has: corrections appended openly (an audit trail), and observer hash verification (implementation verification).
- ACL may lack: (a) an ODD (or ODD+D) document with "Purpose and patterns" and Rationale subsections; (b) a TRACE-structured evidence file mapping each of ACL's existing practices onto the TRACE sections.
- Suggestion: produce `ODD+D.md` per the 2020 template, with a Rationale for every behavioural rule citing its ethnographic basis. Restructure the ROADMAP/experiment log into the 8 TRACE sections and keep it live, as a modelling notebook in the Ayllón et al. 2021 sense. Reviewers in JASSS, Ecological Modelling and archaeology outlets recognise both.

### Gaps
- I did not verify the exact current TRACE template version or any post-2021 TRACE revision.

---

## 3. Verification, validation, calibration: ABC, sensitivity analysis (Sobol), equifinality, overfitting; archaeology critiques

### Takeaway
Current best practice treats calibration as likelihood-free inference: ABC, often preceded by history matching or emulators, with explicit posterior uncertainty, cross-validation and coverage checks. It treats sensitivity analysis as *global*, exploring the whole input space. Equifinality (many parameter sets or mechanisms fit the same data) is expected and should be quantified through ABC model selection and posterior breadth, not denied. Archaeology has used ABC and ABMs together since about 2014.

### Cited Findings
**Inference and calibration**
- Hartig, Calabrese, Reineking, Wiegand & Huth (2011). "Statistical inference for stochastic simulation models – theory and application." *Ecology Letters* 14:816–827. DOI 10.1111/j.1461-0248.2011.01640.x. **record only**. A standard review of likelihood approximation and ABC for stochastic simulation models. — [DOI](https://doi.org/10.1111/j.1461-0248.2011.01640.x)
- van der Vaart, Beaumont, Johnston & Sibly (2015). "Calibration and evaluation of individual-based models using Approximate Bayesian Computation." *Ecological Modelling* 312:182–190. DOI 10.1016/j.ecolmodel.2015.05.020. **abstract read**. Findings:
  - Rejection-ABC on a 14-parameter IBM narrowed 7 parameters. Of the 7 it did not narrow, 3 were correlated with other parameters and 4 were "not estimable given the data available".
  - Accuracy was checked by "cross-validation and coverage".
  - ABC model selection compared the full model against a simplified one.
  — [DOI](https://doi.org/10.1016/j.ecolmodel.2015.05.020)
- McCulloch, Ge, Ward, Heppenstall, Polhill et al. (2022). "Calibrating Agent-Based Models Using Uncertainty Quantification Methods." *JASSS* 25(2) 1. DOI 10.18564/jasss.4791. **abstract read**. A framework combining History Matching with ABC, demonstrated on Sugarscape, a bird-movement model and the RISC farmer-decision model. — [JASSS PDF](https://www.jasss.org/25/2/1/1.pdf)
- Thiele, Kurth & Grimm (2014). "Facilitating Parameter Estimation and Sensitivity Analysis of Agent-Based Models: A Cookbook Using NetLogo and R." *JASSS* 17(3) 11. DOI 10.18564/jasss.2503. **record only** (issue number from memory). — [DOI](https://doi.org/10.18564/jasss.2503)
- Fagiolo, Moneta & Windrum (2007). "A Critical Guide to Empirical Validation of Agent-Based Models in Economics: Methodologies, Procedures, and Open Problems." *Computational Economics* 30:195–226. DOI 10.1007/s10614-007-9104-4. **record only**. — [DOI](https://doi.org/10.1007/s10614-007-9104-4)

**Sensitivity analysis**
- Saltelli, Aleksankina, Becker, Fennell, Ferretti, Holst et al. (2019). "Why so many published sensitivity analyses are false." *Environmental Modelling & Software* 114:29–39. DOI 10.1016/j.envsoft.2019.01.012. **abstract read**. Finding: 42% of highly cited papers reviewed "fail the elementary requirement to properly explore the space of the input factors". Many analyses move "along one-dimensional corridors" (one-at-a-time). — [DOI](https://doi.org/10.1016/j.envsoft.2019.01.012)
- ten Broeke, van Voorn & Ligtenberg (2016). "Which Sensitivity Analysis Method Should I Use for My Agent-Based Model?" *JASSS* 19(1) 5. DOI 10.18564/jasss.2857. **record only**. Compares OFAT, regression-based and variance-based (Sobol) methods on an ABM. — [DOI](https://doi.org/10.18564/jasss.2857)
- Lee, Filatova, Ligmann-Zielinska, Hassani-Mahmooei, Stonedahl, Lorscheid et al. (2015). "The Complexities of Agent-Based Modeling Output Analysis." *JASSS* 18(4) 4. DOI 10.18564/jasss.2897. **full text read**. Findings:
  - OAT with 10 inputs covers only about 0.25% of parameter space.
  - Variance-based SA "does not assume linearity" but needs about M(k+1) runs with M > 1000.
  - It also covers elementary-effects screening, standardised regression coefficients and meta-modelling.
  — [JASSS](https://www.jasss.org/18/4/4.html)
- Ligmann-Zielinska, Kramer, Spence Cheruvelil & Soranno (2014). "Using Uncertainty and Sensitivity Analyses in Socioecological Agent-Based Models to Improve Their Analytical Performance and Policy Relevance." *PLoS ONE* 9:e109779. DOI 10.1371/journal.pone.0109779. **record only**. — [DOI](https://doi.org/10.1371/journal.pone.0109779)

**Equifinality**
- Beven (2006). "A manifesto for the equifinality thesis." *Journal of Hydrology* 320:18–36. DOI 10.1016/j.jhydrol.2005.07.007. **record only**. The source of the idea that many acceptable model and parameter sets fit the data (GLUE tradition). — [DOI](https://doi.org/10.1016/j.jhydrol.2005.07.007)
- Edmonds et al. (2019) list "Multiple explanations might fit the same data" as a key risk for explanation models (**full text read**). — [JASSS](https://www.jasss.org/22/3/6.html)

**Archaeology and anthropology**
- Lake (2014). "Trends in Archaeological Simulation." *Journal of Archaeological Method and Theory* 21:258–287 (online 2013). DOI 10.1007/s10816-013-9188-1. **abstract read**. Finding: the post-2000 growth is "largely characterized by mature application in areas where it fits naturally into existing inferential frameworks (e.g., certain strands of evolutionary archaeology) but … explicitly 'sociological' simulation remains a challenge." — [DOI](https://doi.org/10.1007/s10816-013-9188-1)
- Romanowska, Wren & Crabtree (2021). *Agent-Based Modeling for Archaeology: Simulating the Complexity of Societies*. SFI Press. DOI 10.37911/9781947864382. **record only**. Reviewed in *American Antiquity* 87:846–847 (Cegielski 2022, DOI 10.1017/aaq.2022.27) and *European Journal of Archaeology* 25:547–549 (Vander Linden 2022, DOI 10.1017/eaa.2022.33). Note: Crossref lists only Romanowska as author on the book DOI record; the reviews give all three authors. — [DOI](https://doi.org/10.37911/9781947864382)
- Romanowska, Crabtree, Harris & Davies (2019). "Agent-Based Modeling for Archaeologists: Part 1 of 3." *Advances in Archaeological Practice* 7:178–184. DOI 10.1017/aap.2019.6. **record only**. Part 3 exists as a preprint, "Outreach in Archaeology with Agent-Based Modeling: Part 3 of 3" (Crabtree, Harris, Davies, Romanowska 2019, SocArXiv DOI 10.31235/osf.io/9uw6j). — [DOI](https://doi.org/10.1017/aap.2019.6)
- Romanowska (2015). "So You Think You Can Model? A Guide to Building and Evaluating Archaeological Simulation Models of Dispersals." *Human Biology* 87:169. DOI 10.13110/humanbiology.87.3.0169. **record only**. — [DOI](https://doi.org/10.13110/humanbiology.87.3.0169)
- Cegielski & Rogers (2016). "Rethinking the role of Agent-Based Modeling in archaeology." *Journal of Anthropological Archaeology* 41:283–298. DOI 10.1016/j.jaa.2016.01.009. **record only** (no abstract retrieved). — [DOI](https://doi.org/10.1016/j.jaa.2016.01.009)
- Crema, Edinborough, Kerig & Shennan (2014). "An Approximate Bayesian Computation approach for inferring patterns of cultural evolutionary change." *Journal of Archaeological Science* 50:160–170. DOI 10.1016/j.jas.2014.07.014. **record only**. — [DOI](https://doi.org/10.1016/j.jas.2014.07.014)
- Carrignon, Brughmans & Romanowska (2020). *PLOS ONE* 15:e0240414. **full text read**. Methods and findings:
  - Used ABC-PMC to compare 3 transmission hypotheses by Bayes factor: independent learning was "1.96 times more likely than Unbiased Learning" and about 23.5 times more likely than success-biased learning.
  - Data were normalised to proportions because only 178 of about 500 estimated settlements were observed.
  - Used 50 ten-year bins and 206,902–1,267,560 simulation runs across 13 epsilon thresholds.
  - Caveat: archaeological data's "high dimensionality" and "low resolution" made summary-statistic design hard.
  — [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0240414)
- Kandler & Crema (2019). "Analysing Cultural Frequency Data: Neutral Theory and Beyond." In *Handbook of Evolutionary Research in Archaeology*, pp. 83–108. DOI 10.1007/978-3-030-11117-5_5. **record only**. — [DOI](https://doi.org/10.1007/978-3-030-11117-5_5)
- Wren & Burke (2019). "Habitat suitability and the genetic structure of human populations during the Last Glacial Maximum (LGM) in Western Europe." *PLOS ONE* 14:e0217996. DOI 10.1371/journal.pone.0217996. **record only**. An example of a forager-population ABM confronted with an independent data type (genetic structure). — [DOI](https://doi.org/10.1371/journal.pone.0217996)

**Replication across implementations**
- Donkin, Dennis, Ustalakov, Warren & Clare (2017). "Replicating complex agent based models, a formidable task." *Environmental Modelling & Software* 92:142–151. DOI 10.1016/j.envsoft.2017.01.020. **abstract read**. When the same model was re-implemented in NetLogo and Repast, "the findings differed not only in magnitude but the trends … resulting in different conclusions." — [DOI](https://doi.org/10.1016/j.envsoft.2017.01.020)

### Inferences
- ACL has: holdout seeds, which guard against over-fitting to *stochastic noise*. They do not guard against over-fitting to *empirical data* or against structural equifinality.
- ACL lacks (likely):
  - global SA, such as Morris screening followed by Sobol indices on the key outputs;
  - formal calibration against empirical data with posterior uncertainty;
  - a model-selection step between rival mechanisms;
  - an independent re-implementation of core rules (docking).
- Suggestions:
  1. Run Morris screening, then Sobol on the outputs named in the frozen predictions. Pre-register the input ranges, and report which predictions are robust across the plausible parameter space versus true only at the default parameter values.
  2. If ACL claims any empirical match, use ABC (rejection or SMC/PMC), as in van der Vaart et al. 2015 and Carrignon et al. 2020. Report posterior coverage and cross-validation, and flag non-identifiable parameters as non-identifiable.
  3. Treat rival behavioural submodels as competing hypotheses and compare them with ABC model selection or POM filtering. This turns equifinality into a reported result.
  4. Use a "docking" check. Re-implement one critical submodule (e.g., sharing or reproduction) independently, in a different language or by a different person, and compare output distributions. Donkin et al. 2017 show that implementation choices alone can flip conclusions.

### Gaps
- I did not retrieve full text for Romanowska et al. 2021 (book) or Cegielski & Rogers 2016, so their specific critiques are not summarised here.
- Premo's work on equifinality in archaeological ABM was searched for but not verified in Crossref. It is not cited.
- No specific source on Sobol applied to hunter-gatherer ABMs was found.

---

## 4. Pre-registration and open science in simulation and computational modelling; reproducibility, containers, seeds, CoMSES

### Takeaway
Pre-registration of *simulation studies* has a 2019–2024 literature, mostly from statistics and psychology: ADEMP, ADEMP-PreReg, and questionable research practices (QRPs) in simulation studies. Pre-registering ABM experiments themselves is rare; I found no ABM-specific pre-registration standard. Code availability for ABMs has historically been poor (about 10% in 1990–2014). CoMSES Net now offers peer-reviewed model archiving with DOIs under FAIR4RS. By pre-registering, ACL already goes further than most ABM practice; its remaining gaps are environment capture (containers), independent archiving with a DOI, and a standard template.

### Cited Findings
- Pawel, Kook & Reeve (2024; online 2023). "Pitfalls and potentials in simulation studies: Questionable research practices in comparative simulation studies." *Biometrical Journal* 66. DOI 10.1002/bimj.202200091. **abstract read**. They invented a method with "no expected performance gain", benchmarked it in a *preregistered* simulation study, and showed "how easy it is to make the method appear superior" using QRPs. Recommendations include "preregistering simulation protocols, incentivizing neutral simulation studies, and code and data sharing." — [DOI](https://doi.org/10.1002/bimj.202200091)
- Siepe, Bartoš, Morris, Boulesteix, Heck (2024). "Simulation studies for methodological research in psychology: A standardized template for planning, preregistration, and reporting." *Psychological Methods*. DOI 10.1037/met0000695 (preprint 10.31234/osf.io/ufgy6, 2023). **abstract read**. Findings:
  - 31.2% (100/321) of articles reviewed report a simulation study.
  - Many lack "justifications for the number of simulation repetitions, Monte Carlo uncertainty estimates, or code."
  - The paper provides **ADEMP-PreReg** and formulae for the number of repetitions needed to hit a target Monte Carlo SE.
  — [DOI](https://doi.org/10.1037/met0000695); [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7616844/)
- Morris, White & Crowther (2019). "Using simulation studies to evaluate statistical methods." *Statistics in Medicine* 38:2074–2102. DOI 10.1002/sim.8086. **record only**. The source of ADEMP (Aims, Data-generating mechanisms, Estimands, Methods, Performance measures). — [DOI](https://doi.org/10.1002/sim.8086)
- Crüwell & Evans (2021). "Preregistration in diverse contexts: a preregistration template for the application of cognitive models." *Royal Society Open Science* 8. DOI 10.1098/rsos.210155. **abstract read**. It notes that pre-registration templates were "designed for purely experimental work" and builds a template for computational-model applications, discussing modelling-specific "researcher degrees of freedom". — [DOI](https://doi.org/10.1098/rsos.210155)
- Janssen (2017). "The Practice of Archiving Model Code of Agent-Based Models." *JASSS* 20(1) 2. DOI 10.18564/jasss.3317. **full text read** (page summary). Findings:
  - 2,367 ABM articles from 1990–2014 were reviewed; about 10% made code available.
  - Sharing was under 10% until 2012, rising to about 15% by 2014.
  - Rates were similar for publicly funded work, with "big differences among journals".
  — [JASSS](https://www.jasss.org/20/1/2.html)
- Barton, Lee, Janssen, van der Leeuw, Tucker, Porter, Greenberg, Swantek, Frank, Chen, Jagers (2022). "How to make models more useful." *PNAS* 119(35) e2202112119. DOI 10.1073/pnas.2202112119. **record only**. The author list was verified via Europe PMC; the abstract and full text were not retrievable (HTTP 403). Known content: argues for FAIR model sharing and reuse via repositories such as CoMSES. — [DOI](https://doi.org/10.1073/pnas.2202112119)
- CoMSES Net Computational Model Library (web pages, read via search snippets; 2026). Authors can request peer review. A model that passes gets a peer-reviewed badge and a DOI. Review uses a checklist aligned with the "FAIR Principles for Research Software (FAIR4RS)", and includes "Ease of Execution" (are dependencies documented?). — [CoMSES](https://www.comses.net/); [reviews](https://miracle.comses.net/reviews/)
- Sandve, Nekrutenko, Taylor & Hovig (2013). "Ten Simple Rules for Reproducible Computational Research." *PLoS Comput Biol* 9:e1003285. DOI 10.1371/journal.pcbi.1003285. **record only**. The rules include recording random seeds and archiving exact program versions. — [DOI](https://doi.org/10.1371/journal.pcbi.1003285)
- Boettiger (2015). "An introduction to Docker for reproducible research." *ACM SIGOPS Operating Systems Review* 49:71–79. DOI 10.1145/2723872.2723882. **record only**. — [DOI](https://doi.org/10.1145/2723872.2723882)
- Lemmen & Sommer (2024) (see §2, **abstract read**): continuous integration and deployment, archiving, and a software paper. — [DOI](https://doi.org/10.1016/j.ecolmodel.2024.110890)

### Inferences
- ACL has: frozen pre-registered predictions and discovery/holdout seeds, which matches Pawel et al.'s main recommendation. It also has openly appended corrections, the equivalent of transparent deviation reporting.
- ACL may lack:
  - **a timestamped third-party registry** (OSF Registries, or a Zenodo DOI per frozen prediction file). A file in ACL's own repository is less credible than an external timestamp. The user's memory notes say the Zenodo upload is deferred to 60% progress. A lightweight alternative is to timestamp each *pre-registration* file now (OSF, or a public git commit hash posted externally) without releasing the full package.
  - **an environment capture**: a Dockerfile, a pinned lockfile, and the exact RNG library and version. Seed-identical runs can diverge across library versions, which hash-verified observers would detect but not prevent.
  - **an ADEMP-style framing** of each experiment, plus an explicit Monte Carlo SE for each reported estimate.
- Suggestions:
  - Adapt ADEMP-PreReg (Siepe et al. 2024) as ACL's pre-registration template: Aims → hypotheses; Data-generating mechanism → model config and seeds; Estimands → outcome metrics; Methods → paired sign test etc.; Performance → acceptance criteria. Also borrow the "researcher degrees of freedom" list from Crüwell & Evans 2021.
  - Add a Dockerfile, and record the state hashes of a reference run in CI so that any environment drift fails loudly.
  - Plan a CoMSES submission with peer-review badge in addition to Zenodo.

### Gaps
- I found no published standard or template specifically for pre-registering *agent-based* model experiments (2019–2026). The JASSS search returned nothing relevant. This is a genuine gap that ACL could publish into, but absence of evidence is not certain.
- No quantitative post-2017 update to Janssen's code-availability rate was verified.

---

## 5. Statistical analysis of stochastic simulations: replicates, power, effect sizes over p-values, common random numbers, multiple testing

### Takeaway
With simulations, p-values can be driven arbitrarily small simply by adding replicates, and the null of "no difference" is known to be false. The consensus is to report effect sizes with uncertainty (Monte Carlo SE or intervals), justify the replicate count by precision or power, and use paired or common-random-number designs to reduce variance. ACL's paired sign tests plus power analysis are defensible, *provided* effect sizes and a practical-significance threshold are pre-registered alongside them.

### Cited Findings
- White, Rassweiler, Samhouri, Stier & White (2014; online 2013). "Ecologists should not use statistical significance tests to interpret simulation model results." *Oikos* 123:385–388. DOI 10.1111/j.1600-0706.2013.01073.x. **abstract read**. **Citation correction:** the brief's title "Ecological models and the pitfalls of p-values" does not match the Crossref record; the verified title is the one given here. Key claims:
  - "p-values are determined by statistical power (i.e. replication), which can be arbitrarily high in a simulation context".
  - "the null hypothesis of no difference … is known a priori to be false".
  - Modellers should "focus on evaluating the magnitude of differences".
  — [DOI](https://doi.org/10.1111/j.1600-0706.2013.01073.x)
- Lee et al. (2015) (**full text read**):
  - Number of replicates: the Lorscheid coefficient-of-variation method, with the caution that it "favors those μ sufficiently larger than 0"; and a windowed-variance stability alternative.
  - Large samples expose "extremely small and contextually inconsequential differences".
  - Recommends effect sizes (Cohen's d), stricter thresholds, Bayesian approaches, and variance reduction by control variates.
  - Wilcoxon tests are more conservative for skewed outputs.
  — [JASSS](https://www.jasss.org/18/4/4.html)
- Lorscheid, Heine & Meyer (2012; online 2011). "Opening the 'black box' of simulations: increased transparency and effective communication through the systematic design of experiments." *Computational and Mathematical Organization Theory* 18:22–62. DOI 10.1007/s10588-011-9097-3. **record only**. A design-of-experiments (DOE) framework for ABMs, and the source of the coefficient-of-variation method. — [DOI](https://doi.org/10.1007/s10588-011-9097-3)
- Secchi & Seri (2017; online 2016). "Controlling for false negatives in agent-based models: a review of power analysis in organizational research." *CMOT* 23:94–121. DOI 10.1007/s10588-016-9218-0. **abstract read**. Findings: "most studies are underpowered, with some being overpowered". Gives two formulas for the number of runs and recommends power of at least 0.95 at α = 0.01. — [DOI](https://doi.org/10.1007/s10588-016-9218-0)
- Seri & Secchi (2017). "How Many Times Should One Run a Computational Simulation?" In *Simulating Social Complexity* (2nd ed.), Understanding Complex Systems series, pp. 229–251. DOI 10.1007/978-3-319-66948-9_11. **record only**. — [DOI](https://doi.org/10.1007/978-3-319-66948-9_11)
- Siepe et al. (2024) give formulae for the number of repetitions needed to reach a target Monte Carlo SE (**abstract read**). — [DOI](https://doi.org/10.1037/met0000695)
- Common random numbers (CRN): standard in the simulation-output-analysis literature (e.g., Kleijnen's "Design and Analysis of Simulation Experiments"; a tutorial version is on SSRN, DOI 10.2139/ssrn.2941492, 2017, **record only**). I did not retrieve a peer-reviewed ABM-specific CRN source this session. — [SSRN record](https://doi.org/10.2139/ssrn.2941492)

### Inferences
- ACL has: paired designs (sign tests on paired seeds are effectively CRN, provided the arms consume random numbers in a synchronised way), power analysis, and sham arms (an empirical null).
- ACL may lack:
  - pre-registered *smallest effect size of interest* (SESOI);
  - reporting of effect sizes with intervals alongside sign-test p-values;
  - an explicit multiple-testing policy across the set of frozen predictions;
  - a check that CRN synchronisation actually holds.
- Suggestions:
  1. For each frozen prediction, pre-register the direction, the SESOI, and a primary effect-size metric. Examples: median paired difference with a bootstrap CI, or the proportion of seeds in which arm A beats arm B with a Wilson interval. Treat the sign-test p-value as secondary (White et al. 2014).
  2. Declare a family-wise or FDR correction across all predictions (e.g., Holm or Benjamini–Hochberg), or else declare each prediction a separate confirmatory family with a stated rationale.
  3. Verify CRN by using separate RNG streams per stochastic process, so that one intervention does not desynchronise every later draw. Report the paired-difference variance reduction relative to an unpaired design, using the sham arm.
  4. Use the sham arms to estimate the empirical false-positive rate of the whole pipeline, and report it. This is a strong credibility signal that few ABMs provide.
  5. Report Monte Carlo SE for each headline number (Siepe et al. 2024).

### Gaps
- I found no source specifically evaluating sign tests on paired ABM seeds. The suggestion is an inference from general principles.
- I did not verify a peer-reviewed ABM paper on CRN implementation.

---

## 6. Validating "emergence" claims and avoiding circularity (reading out what was built in)

### Takeaway
The generative tradition ("if you didn't grow it, you didn't explain it") yields *how-possibly* (sufficient, not necessary) explanations. A macro-pattern that follows directly from a coded rule is not emergent. The main defences are:
- a clear statement of the modelling purpose;
- rival mechanisms, so the pattern does not appear under every assumption;
- ablation or knock-out experiments;
- sensitivity analysis showing the pattern is not brittle;
- testing against patterns that were *not* used to build or calibrate the model.

ACL's sham arms and holdout seeds address statistical circularity. Conceptual circularity needs separate controls.

### Cited Findings
- Epstein (1999). "Agent-based computational models and generative social science." *Complexity* 4(5):41–60. DOI 10.1002/(SICI)1099-0526(199905/06)4:5<41::AID-CPLX9>3.0.CO;2-F. **record only**. The origin of the generative-sufficiency criterion. Reprinted as Ch. 1 of *Generative Social Science* (Princeton, 2006/2012; chapter DOI 10.1515/9781400842872.4). — [DOI](https://doi.org/10.1002/(SICI)1099-0526(199905/06)4:5%3C41::AID-CPLX9%3E3.0.CO;2-F)
- Grüne-Yanoff (2009; online 2008). "The explanatory potential of artificial societies." *Synthese* 169:539–555. DOI 10.1007/s11229-008-9429-0. **record only**. Argues that generative ABMs mostly give potential (how-possibly) explanations. — [DOI](https://doi.org/10.1007/s11229-008-9429-0)
- A 2025 review in *Artificial Intelligence Review* (Springer, "Validation is the central challenge for generative social simulation: a critical review of LLMs in agent-based modeling", DOI 10.1007/s10462-025-11412-6). **search snippet only**; authors and full record not verified. It states that ABMs "can provide sufficient explanations, not necessary ones, as the same macro-phenomenon can be explained by several different micro-level mechanisms", and criticises behavioural rules "simply assumed by the modeler." — [Springer](https://link.springer.com/article/10.1007/s10462-025-11412-6)
- Edmonds, Le Page, Bithell, Chattoe-Brown, Grimm, Meyer et al. (2019). "Different Modelling Purposes." *JASSS* 22(3) 6. DOI 10.18564/jasss.3993. **full text read**. Findings:
  - Defines 7 purposes: prediction, explanation, description, theoretical exposition, illustration, analogy, social learning.
  - Lists confusions, e.g. "Theoretical exposition → Explanation" and "Description → Explanation". For the explanation purpose: "Hidden assumptions in code could undermine validity".
  - Advice: use sensitivity analysis and code experiments, and reproduce multiple patterns.
  - "A confused, conflated or unclear modelling purpose leads to a model that is hard to check … a recipe for bad science."
  - It also points to Galán et al. on detecting errors and artefacts.
  — [JASSS](https://www.jasss.org/22/3/6.html)
- Galán et al. (2017). "Checking Simulations: Detecting and Avoiding Errors and Artefacts." In *Simulating Social Complexity* (2nd ed.), Understanding Complex Systems. DOI 10.1007/978-3-319-66948-9_7 (1st-ed. version: 10.1007/978-3-540-93813-2_6). **record only**; Crossref did not return the author list in my query, and attribution to Galán et al. is via Edmonds et al. 2019. Known content: distinguishes *errors* (the code does not match the modeller's intent) from *artefacts* (outcomes caused by accessory assumptions the modeller considers irrelevant, e.g. scheduling order or space topology). — [DOI](https://doi.org/10.1007/978-3-319-66948-9_7)
- Graebner (2018). "How to Relate Models to Reality? An Epistemological Framework for the Validation and Verification of Computational Models." *JASSS* 21(3) 8. DOI 10.18564/jasss.3772. **abstract read**. Finding: the "meta-theoretical strategies of how the models should be related to reality often remain implicit". It offers an epistemological framework linking interpretation to verification and validation. — [DOI](https://doi.org/10.18564/jasss.3772)
- O'Sullivan & Haklay (2000). "Agent-Based Models and Individualism: Is the World Agent-Based?" *Environment and Planning A* 32:1409–1425. DOI 10.1068/a32140. **record only**. A classic critique of the methodological individualism built into ABMs. — [DOI](https://doi.org/10.1068/a32140)
- Zurell, Berger, Cabral, Jeltsch, Meynard et al. (2010). "The virtual ecologist approach: simulating data and observers." *Oikos* 119:622–635. DOI 10.1111/j.1600-0706.2009.18284.x. **record only**. Simulates the *observation/sampling process* on top of the model, so that the comparison with real data is like-for-like. — [DOI](https://doi.org/10.1111/j.1600-0706.2009.18284.x)

### Inferences
- ACL has:
  - sham arms (an intervention that should do nothing);
  - holdout seeds (against fishing in noise);
  - read-only observers verified by state hashes, which prove that measurement does not perturb the simulation. This is a strong and unusual verification control.
- ACL may lack:
  1. **A circularity audit.** For each claimed emergent outcome, a written trace stating which coded rules could produce it directly, and why the outcome is not a restatement of them.
  2. **Ablation / knock-out arms.** Remove or randomise the hypothesised causal mechanism; the "emergent" pattern should disappear. Also add a "null-mechanism" arm in which the pattern should not arise. Sham arms test the inverse case (no effect where none is expected) but do not by themselves show that the mechanism is necessary.
  3. **Artefact checks** (Galán et al.): rerun key results under alternative scheduling (random versus fixed activation order), alternative space or topology, and different time-step granularity.
  4. **An explicit purpose statement** in Edmonds et al. 2019 terms. If ACL is "theoretical exposition", it should not make empirical explanatory claims. If it is "explanation", it needs empirical patterns (§1) and rival mechanisms (§3).
  5. **Virtual-archaeologist observers** (Zurell et al. 2010). The read-only observers could additionally emulate how ethnographers or archaeologists *would* sample the simulated society (partial site recovery, time-averaging, small ethnographic samples). Comparisons with real data would then be like-for-like. Carrignon et al. 2020 had to normalise for 178 of about 500 sites being recovered; a virtual-observer layer would make such corrections explicit.
- Suggestion: add a pre-registered "emergence claim card" for each claimed emergent phenomenon, containing:
  - the rules that could trivially produce it;
  - an ablation arm;
  - a schedule/topology artefact test;
  - a pattern the model was not tuned on.

### Gaps
- I found no dedicated methods paper giving a formal "circularity test" for social simulations. The guidance above is assembled from Edmonds et al. 2019, Galán et al., Grüne-Yanoff 2009 and the generative-explanation literature.
- The 2025 *AI Review* paper's authorship was not verified, so cite it cautiously or verify before use.

---

### Additional verified context sources (record only, for a report writer's background)
- Schulze, Müller, Groeneveld & Grimm (2017). "Agent-Based Modelling of Social-Ecological Systems: Achievements, Challenges, and a Way Forward." *JASSS* 20(2) 8. DOI 10.18564/jasss.3423. — [DOI](https://doi.org/10.18564/jasss.3423)
- An, Grimm, Sullivan, Turner II, Malleson et al. (2021). "Challenges, tasks, and opportunities in modeling agent-based complex systems." *Ecological Modelling* 457:109685. DOI 10.1016/j.ecolmodel.2021.109685. Note: there is a corrigendum, 10.1016/j.ecolmodel.2022.110064. — [DOI](https://doi.org/10.1016/j.ecolmodel.2021.109685)
- Heppenstall, Crooks, Malleson, Manley, Ge et al. (2021; online 2020). "Future Developments in Geographical Agent-Based Models: Challenges and Opportunities." *Geographical Analysis* 53:76–91. DOI 10.1111/gean.12267. — [DOI](https://doi.org/10.1111/gean.12267)
- Calder, Craig, Culley, de Cani, Donnelly, Douglas et al. (2018). "Computational modelling for decision-making: where, why, what, who and how." *Royal Society Open Science* 5:172096. DOI 10.1098/rsos.172096. — [DOI](https://doi.org/10.1098/rsos.172096)

### Citation corrections and cautions found during verification
- The White et al. Oikos paper's real title is "Ecologists should not use statistical significance tests to interpret simulation model results", not "Ecological models and the pitfalls of p-values".
- Lake's "Trends in Archaeological Simulation" is JAMT vol. 21 (2014), online 2013.
- The Romanowska, Wren & Crabtree book's Crossref DOI record lists only Romanowska. Cite all three authors per the book and its reviews.
- JASSS issue/article numbers for Thiele et al. 2014 (17(3) 11), ten Broeke et al. 2016 (19(1) 5), Graebner 2018 (21(3) 8) and Schulze et al. 2017 (20(2) 8) are from memory. The DOIs are verified; re-check the issue numbers before final citation.
