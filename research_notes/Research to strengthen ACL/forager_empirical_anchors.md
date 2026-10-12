# Empirical anchors from real hunter-gatherers for ACL's "nature": mobility, visiting, mate search, seasonality, storage, sharing

Compiled 2026-10-11 for the Artificial Civilization Laboratory (ACL). Every source carries a reading label:
- **full text read**: I retrieved and searched the full article text (Europe PMC full-text XML, PMC or the publisher PDF). The numbers were taken from that text.
- **abstract read**: only the abstract was seen. Numbers come from the abstract alone.
- **record only**: only a bibliographic record or a search-engine snippet was seen. Treat any number as unverified.

Bibliographic data (authors, year, venue, volume, pages, DOI) were checked against Europe PMC records unless a note says otherwise. Where a DOI could not be resolved, the note says so.

ACL framing used below:
- **"Nature" parameter**: something measured that ACL can hard-code, such as a distance, a rate or a cost.
- **"Emergence test"**: a measured pattern that ACL should reproduce without scripting it, used as a validation target rather than an input.

---

## 1. Mobility and search: Lévy walks, GPS day ranges, residential moves, visiting between camps

### Takeaway
Measured forager movement has a clear structure:
- Adults walk about 8–14 km/day. Men range about 4× more land than women.
- Camps move every ~5–60 days, depending on the ecology.
- Residential bands of one ethnolinguistic population sit roughly 10–35 km apart.
- Foraging paths have heavy-tailed step lengths in about half of bouts. Whether that is a true "Lévy strategy" or an artefact of intermittent, encounter-conditional search is contested.

ACL's fixed 3-tile random step contradicts all of these facts. It should be replaced by goal- and memory-driven daily forays from a camp, plus separate, rarer residential moves and visits.

### Cited Findings

**Lévy walks and their critiques**
- Hadza (Tanzania) foragers performed Lévy walks in "nearly one-half of all foraging bouts". These occurred when searching for many food types, from animal prey to tubers. Raichlen DA, Wood BM, Gordon AD, Mabulla AZP, Marlowe FW, Pontzer H (2014) *PNAS* 111(2):728–733, doi:10.1073/pnas.1318616111. **Abstract read.** The publisher's page returned 403, so the fitted exponent (μ) and the bout counts were not verified here. — [Europe PMC record](https://europepmc.org/article/MED/24367098); [DOI](https://doi.org/10.1073/pnas.1318616111)
- Wood et al. (2021) note that Raichlen et al. analysed step lengths in "a much smaller sample of GPS tracks from four camps". The Lévy result therefore rests on a modest sample. — [Wood et al. 2021, PMC8060163](https://europepmc.org/article/PMC/PMC8060163)
- Rural non-foragers show the same signature. About 50% of search patterns among Me'Phaa (Mexico), Cariri (Brazil) and Amazonian farmers gathering firewood, fruit and nuts resemble Lévy walks, with exponents close to 1.7. The rest are closer to bi-phasic walks. The authors attribute the pattern to "frequent excursions and meanderings from pre-existing trails". Reynolds A, Ceccon E, Baldauf C, Karina Medeiros T, Miramontes O (2018) *PLoS ONE* 13:e0199099, doi:10.1371/journal.pone.0199099. **Abstract read.** — [DOI](https://doi.org/10.1371/journal.pone.0199099)
- Theoretical critique: when foragers have some information about prey distribution, adaptive "encounter-conditional" heuristics (area-restricted search) outperform Lévy flights. Ross C, Pacheco-Cobos L, Winterhalder B (2018) *J Theor Biol* 455:357–369, doi:10.1016/j.jtbi.2018.07.031. **Abstract read.** — [DOI](https://doi.org/10.1016/j.jtbi.2018.07.031)
- Evolutionary model in which the move-length distribution was not constrained in advance:
  - Searchers consistently evolved "intermittent search", meaning frequent local walks plus infrequent long moves, which outcompeted Lévy walks.
  - Interaction with resources can make intermittent search look like a Lévy walk.
  - Campeau W, Simons AM, Stevens B (2024) *Am Nat* 203:513–527, doi:10.1086/729220. **Abstract read.** — [DOI](https://doi.org/10.1086/729220)
- Virtual foraging experiment (200 players): efficient foragers produced Lévy-like alternation between locomotion and perception or planning. Under a home-range constraint, trajectories were less diffusive because players spent more time scanning. Garg K, Kello CT (2021) *Sci Rep* 11:5242, doi:10.1038/s41598-021-84542-w. **Abstract read.** — [DOI](https://doi.org/10.1038/s41598-021-84542-w)
- Brown CT, Liebovitch LS, Glendon R (2007), "Lévy flights in Dobe Ju/'hoansi foraging patterns", *Human Ecology* 35:129–138. This paper is usually cited as finding Lévy-like distributions in Ju/'hoansi *residential* (camp-to-camp) moves. **Record only.** It was not found in Europe PMC, and I could not verify the DOI (believed to be 10.1007/s10745-006-9083-4) or its numbers.

**GPS day ranges (the strongest quantitative anchor)**

Source for all of this subsection unless stated: Wood BM, Harris JA, Raichlen DA, Pontzer H, Sayre K, Sancilio A, Berbesque C, Crittenden AN, Mabulla A, McElreath R, Cashdan E, Jones JH (2021), "Gendered movement ecology and landscape use in Hadza hunter-gatherers", *Nature Human Behaviour* 5:436–446, doi:10.1038/s41562-020-01002-7. **Full text read.** — [PMC8060163](https://europepmc.org/article/PMC/PMC8060163)

- **Sample:** 2,078 person-days of GPS movement (23,872 person-hours), from 15 camps, recorded between 2005 and 2018. Devices recorded about 11.5 h/day on average. The authors estimate that 90–100% of calories in the study camps came from wild foods.
- **Adult day ranges:**
  - Women walked 7.6 km/day (10,888 steps). Men walked 12.9 km/day (18,476 steps).
  - At ages 30–45, the model estimates ~14 km/day for men and ~8 km/day for women.
  - Men's travel peaks near age 32 (~15 km/day).
  - Women show an early peak at 17–20 years (~9 km/day), then a plateau of ~7 km/day through age 60.
- **Children:** at age 15, boys averaged 12 km/day and girls 9 km/day.
- **Effect of young children on women's travel:** having young children made no credible difference to women's daily travel distance. At age 30 the difference was −0.84 km (95% CI −3.21 to 1.55).
- **Land explored:**
  - Women covered in 15 days about the same area that men covered in 5 days (~0.47–0.53 km²).
  - Averaged across camps, the land visited by males was 3.9× the female-visited area. The ratio of minimum convex polygon areas was ~4:1.
- **Path sinuosity:** outbound paths were more sinuous than inbound ones. Model estimates:
  - Outbound: men 1.55, women 1.44.
  - Inbound: men 1.50, women 1.38.
  - Routes back to camp are more direct, which implies navigation by memory.
- **Being alone:** at 2 km from camp, women had a 0.77 probability of being within 5 m of a campmate, against 0.07 for men. At 12 km the probabilities were 0.99 for women and 0.06 for men.
- **Purpose of trips:** the authors' conservative estimate is that more than 95% of forays out of camp were to search for and harvest food, water and firewood.

Follow-up analysis of the same GPS sample: Wood BM, Raichlen DA, Pontzer H, Harris JA, Sayre MK, Paolo B, Anyawire M, Mabulla AZP, et al. (2024), "Beyond the here and now: hunter-gatherer socio-spatial complexity and the evolution of language", *Phil Trans R Soc B*, doi:10.1098/rstb.2022.0521. **Full text read.** — [PMC11449209](https://europepmc.org/article/PMC/PMC11449209)
- The sample covers 179 participants (87 female, 92 male), aged 2–84.
- Adults aged 18–50 averaged an 11 km day range.
- 25% of time was spent within 24 m of the day's starting point (usually the hearth) and 50% within 88 m.
- 17% of time was spent more than 2.1 km away. The maximum distance from the start was 12.8 km.
- Co-resident Hadza dyads shared a median of only 0.04 of the landscape each visited per day. Olive baboon dyads shared 0.35.
- A small subset of camp members may "leave on short visits to neighbouring camps". This is qualitative; no rate is given.

Cross-cultural day-travel distances come from ethnographic accounts: !Kung 16 km, Siriono 13–16 km (up to 40), Yukaghir 11–56 km, Mbuti 5 km average daily movement during hunting, and others. Many are anecdotal. Source: Brill G, Dyble M (2025), "The fitness costs and benefits of hunter-gatherer locomotor engagement", *Evolutionary Human Sciences*, doi:10.1017/ehs.2025.10025. **Full text read.** — [PMC12645331](https://europepmc.org/article/PMC/PMC12645331)

**Residential moves (camp shifts)**
- Days between camp moves, cited from Lewis et al.'s Table 1 (which compiles ethnographic data): Ache 6.3, Punan 8.1, Hiwi 9.1. Their demand-sharing model survives when moves fall between 5 and 30 days apart, a range that includes 11 of the 12 demand-sharing groups in that table. Lewis HM, Vinicius L, Strods J, Mace R, Migliano AB (2014), "High mobility explains demand sharing and enforced cooperation in egalitarian hunter-gatherers", *Nature Communications* 5:5789, doi:10.1038/ncomms6789. **Full text read**, but the per-society values are secondary compilations. — [PMC4284614](https://europepmc.org/article/PMC/PMC4284614)
- A search-engine summary of Kelly (2013) gave move intervals of Ache 5–10 days, Hadza 10–15 days and !Kung 63.4 days. Kelly RL (2013), *The Lifeways of Hunter-Gatherers: The Foraging Spectrum*, Cambridge University Press, ISBN 978-1-107-02487-8. **Record only; unverified.** Kelly's Table 4-1 should be checked directly before use. — [Kelly 2013 (archive.org PDF)](https://dn710205.ca.archive.org/0/items/robert-l.-kelly-the-lifeways-of-hunter-gatherers-the-foraging-spectrum-cambridge/Robert%20L.%20Kelly%20-%20The%20Lifeways%20of%20Hunter-Gatherers_%20The%20Foraging%20Spectrum-Cambridge%20University%20Press%20(2013).pdf)
- Annual and per-move distances. Source: Hamilton MJ, Lobo J, Rupley E, Youn H, West GB (2016), "The ecological and evolutionary energetics of hunter-gatherer residential mobility", *Evolutionary Anthropology* 25:124–132, doi:10.1002/evan.21485. **Full text read.** — [PMC5094510](https://europepmc.org/article/PMC/PMC5094510)
  - Hunter-gatherer annual migration distance is about 158 km/yr in Binford's dataset and 174 km/yr in Kelly's.
  - Average distance per move falls with temperature and rises in drier places (regression ⟨D⟩ ∝ P^−0.27, plus a temperature term).
  - Distance per move scales with density as ⟨D⟩ ∝ (N/A)^−1/4 and is effectively independent of population size.
  - The eight groups with the most moves per year are all tropical.
  - Coastal foragers with abundant, predictable resources can become effectively sedentary.
- Batek (Malaysian rainforest), 93 days across 11 residential camps: the time spent at each camp fit the marginal value theorem. Groups left when their perceived returns declined, after "protracted … deliberation and argument". Venkataraman VV, Kraft TS, Dominy NJ, Endicott KM (2017) *PNAS* 114:3097–3102, doi:10.1073/pnas.1617542114. **Abstract read.** — [DOI](https://doi.org/10.1073/pnas.1617542114)
- Area used per person scales sublinearly with population size (exponent < 1), "because social networks of material and information exchange introduce an economy of scale". Hamilton MJ, Milne BT, Walker RS, Brown JH (2007) *PNAS* 104:4765–4769, doi:10.1073/pnas.0611197104. **Abstract read.** A 2026 paper by Hamilton & Walker reports the exponent for small-scale societies as often 0.6–0.85. — [DOI](https://doi.org/10.1073/pnas.0611197104)

**Visiting and interaction between bands (per person, per year)**

Source for the Ache and Hadza figures: Hill KR, Wood BM, Baggio J, Hurtado AM, Boyd RT (2014), "Hunter-gatherer inter-band interaction rates: implications for cumulative culture", *PLoS ONE* 9:e102806, doi:10.1371/journal.pone.0102806. **Full text read.** — [PMC4105570](https://europepmc.org/article/PMC/PMC4105570)

- **Ache (Paraguay):**
  - About 560 Northern Ache lived in 18–20 bands across a core range of ~5,270 km² (maximum ~14,630 km²).
  - Bands were usually 10–30 km apart, occasionally up to 150 km.
- **Eastern Hadza:**
  - About 950 people lived in 49 named bands in 2012.
  - Bands were 0.2–80 km apart, with a mean of about 35 km.
- **Interaction rates between random same-sex adult pairs living in different bands:**
  - Common activities (conversing, sleeping in the same camp, sharing food, watching someone make a tool): about 0.20–0.30 per pair per year among the Ache, 2–5 times lower among the Hadza.
  - Medium-frequency activities: 0.10–0.12 per year among the Ache.
  - Rare activities (hunting together, gifts, lending a tool, caring for the sick): 0.02–0.08 per pair per year in both groups.
  - The headline range across activities is 5–29% per year.
- **Kinship among random pairs:** 5–10% were close kin (r ≥ 0.125) and 15–20% were affines.
- **Ritual ties:**
  - Ritual relationships covered about 20% of Ache pairs and 16% of Hadza pairs.
  - Among the Hadza, a shared epeme ritual raised interaction rates for all 13 interaction types.
- **Lifetime exposure:** men are estimated to observe over 300 men making tools in a lifetime, against about 20 for a male chimpanzee.

Agta proximity-sensor networks, recorded over about one month. Migliano AB, Battiston F, Viguier S, Page AE, Dyble M, et al. (2020), "Hunter-gatherer multilevel sociality accelerates cumulative cultural evolution", *Science Advances* 6:eaax5913, doi:10.1126/sciadv.aax5913. **Full text read.** — [PMC7048420](https://europepmc.org/article/PMC/PMC7048420)
- Forest group: 59% of possible within-camp pairs and 28% of between-camp pairs were observed interacting.
- Coastal group: 85% of within-camp pairs and 56% of between-camp pairs.
- Within-camp pairs made up 38% (forest) and 56% (coastal) of unweighted interacting pairs, so many observed ties cross camps.
- There were no sex biases in interacting pairs.

Hadza social networks show geographic decay, transitivity and assortment on cooperation. Apicella CL, Marlowe FW, Fowler JH, Christakis NA (2012) *Nature* 481:497–501, doi:10.1038/nature10736. **Abstract read.** — [DOI](https://doi.org/10.1038/nature10736)

Martu (Australia) foraging groups differ in composition from residential groups. Both are dominated by unrelated people, and membership is fluid. Bird DW, Bird RB, Codding BF, Zeanah DW (2019) *J Hum Evol* 131:96–108, doi:10.1016/j.jhevol.2019.03.005. **Abstract read.** — [DOI](https://doi.org/10.1016/j.jhevol.2019.03.005)

### Inferences
- **Daily movement (nature parameter).** Replace fixed 3-tile random steps with daily central-place forays from a camp:
  - Round trips of about 8 km/day for adult women and about 13 km/day for adult men (Hadza).
  - The return leg should be straighter than the outbound leg (sinuosity ~1.4–1.55 outbound, ~1.4–1.5 inbound). This implies agents carry a memory of camp location.
  - Search steps can come from a mixture distribution: many short local moves plus occasional long relocations, i.e. intermittent search. Any Lévy-like statistics should then emerge rather than being imposed (Campeau 2024; Ross 2018).
  - Per tile, ACL needs a scale: if 1 tile = X km, then 3 tiles/day = 3X km. ACL should state its tile scale and check it against 8–13 km/day.
- **Camp moves (nature parameter).** Model residential moves as separate events: about every 5–30 days for tropical foragers and up to ~60 days for !Kung-like settings (the latter unverified). Driving them by marginal-value depletion (Venkataraman 2017) is better than a fixed timer. That way the move interval *emerges* from depletion, and the 5–30 day range becomes an **emergence test**.
- **Metapopulation layout.** ACL's "groups hardly mix" problem conflicts with Hill et al. (2014). Real adults in different bands have about 0.05–0.3 annual probability of meeting for common activities.
  - A concrete **emergence test**: in ACL, measure the per-pair, per-year probability that two random adults from different bands are co-located. Compare it with Ache (0.2–0.3) and Hadza (about 0.05–0.15) values.
  - Realistic layout: bands of ~25–40 people spaced 10–35 km apart inside a 5,000–15,000 km² range, with hundreds of people per ethnolinguistic unit.
- **Founder count (direct implication).** A founding population of 20 is roughly one band. Real forager "tribes" are about 500–1,000 people in 18–50 bands (Ache 560 in 18–20 bands; Hadza about 950 in 49 bands). Founding with ≥ several bands is the evidence-based choice. A single band of 20 would not be a viable mating pool in reality either (see section 2).

### Gaps
- No verified per-person count of *visits* to other camps per year. Hill et al. give per-pair interaction probabilities, not visit counts. Ju/'hoansi visiting data (Lee; Wiessner's hxaro) were not retrieved.
- Raichlen et al.'s μ exponent and bout numbers, Brown et al. (2007) and Kelly's residential-mobility table were not verified. They need checking against the full texts.
- Binford's (2001) raw residential-move counts (available in Binford's dataset and D-PLACE) were not extracted here.

---

## 2. Mate search and marriage networks

### Takeaway
In real foragers, finding a spouse routinely requires leaving one's band:
- Bands contain only about 20–30 adults, and band adult sex ratios swing widely year to year.
- Either sex may disperse, and most co-residents are unrelated.
- Marriage is usually arranged or brokered by kin through brideservice or bride-price networks that span bands.

ACL's "single adults rarely meet eligible partners" therefore reproduces a real constraint. Real foragers solve it with cross-band ties, visiting, rituals and kin brokerage, not with random encounters.

### Cited Findings

**Band composition (32 societies)**

Source: Hill KR, Walker RS, Božičević M, Eder J, Headland T, Hewlett B, Hurtado AM, Marlowe F, Wiessner P, Wood B (2011), "Co-residence patterns in hunter-gatherer societies show unique human social structure", *Science* 331:1286–1289, doi:10.1126/science.1199071. **Abstract read.** — [DOI](https://doi.org/10.1126/science.1199071)
- 32 present-day foraging societies, 5,067 individuals.
- Mean experienced band size: 28.2 adults.
- Either sex may disperse or stay in its natal group.
- Adult brothers and sisters often co-reside.
- Most individuals in residential groups are genetically unrelated.

**Why relatedness within camps is low (Agta, BaYaka)**

Dyble M, Salali GD, Chaudhary N, Page A, Smith D, Thompson J, Vinicius L, Mace R, Migliano AB (2015), "Sex equality can explain the unique social structure of hunter-gatherer bands", *Science* 348:796–798, doi:10.1126/science.aaa5139. **Abstract read.** — [DOI](https://doi.org/10.1126/science.aaa5139)
- The paper uses an agent-based model calibrated on Agta and Mbendjele BaYaka co-residence.
- Even if everyone tries to live with as many kin as possible, within-camp relatedness falls when men and women have equal say in choosing camp members.

**Partner scarcity in a small population (Savannah Pumé, Venezuela)**

Kramer KL, Schacht R, Bell A (2017), "Adult sex ratios and partner scarcity among hunter-gatherers: implications for dispersal patterns and the evolution of human sociality", *Phil Trans R Soc B* 372:20160316, doi:10.1098/rstb.2016.0316. **Full text read** (extracted via a fetch tool; figures should be spot-checked). — [PMC5540858](https://pmc.ncbi.nlm.nih.gov/articles/PMC5540858/)
- **Data:** 25 years of demographic records.
- **Group size:** mean 58 ± 16.4 across 18 censuses (1983–2007). The two study bands averaged only about 10–12 adult men and 10–12 adult women each.
- **Adult sex ratio (ASR):** fluctuated widely year to year, from 0.67 to 0.43 (proportion male). The pooled average was 0.52 ± 0.03.
- **What drives ASR swings:** the sex ratio at maturity had about 13× the effect of mortality and 3× the effect of migration.
- **Age at marriage:** women 15.1 ± 2.5 years (first birth 16.0 ± 2.5); men 18.0 ± 4.3 years.
- **Relocation to marry:** 15% of first marriages and 37% of subsequent marriages involved relocating.
- **Polygyny:** 20% of women and 11% of men were in a polygynous union at some point in life.
- **Authors' conclusion:** in small populations, "looking outside of one's local group is necessary to find a mate". Their model predicts that the globally rarer sex disperses.

**Marriage practices across foragers**

Walker RS, Hill KR, Flinn MV, Ellsworth RM (2011), "Evolutionary history of hunter-gatherer marriage practices", *PLoS ONE* 6:e19066, doi:10.1371/journal.pone.0019066. **Full text read.** — [PMC3083418](https://europepmc.org/article/PMC/PMC3083418)
- Arranged marriage is found in 85% of hunter-gatherer societies in Apostolou's sample.
- Exchange of goods or labour between the spouses' families (brideservice or bride-price) occurs in 80%.
- 78% of societies have low polygyny (under 20% of men polygynous).
- Courtship marriage occurs in 3 of 8 African hunter-gatherer societies.
- Arranged marriage is *not* related to Binford's environmental variables, such as latitude, temperature, mobility or population density.
- The authors infer "regulated exchange of mates" through alliances spanning multiple residential communities.

**Distance to a spouse's natal group**

MacDonald DH, Hewlett BS (1999), "Reproductive interests and forager mobility", *Current Anthropology* 40(4):501–523/524, doi:10.1086/200047. **Record only.** — [Journal record](https://www.journals.uchicago.edu/doi/abs/10.1086/200047)
- Reports quantitative mating-distance data across foragers and farmers.
- Mating distance correlates with population density.
- Males travel farther than females over a lifetime; among the Aka, age and sex affect distances travelled.
- I could not retrieve the actual kilometre values.

**Related works not retrieved**
- Hackman J, Kramer KL (2023), "Kin networks and opportunities for reproductive cooperation and conflict among hunter-gatherers", *Phil Trans R Soc B*, doi:10.1098/rstb.2021.0434. **Record only.** — [PMC9703223](https://europepmc.org/article/PMC/PMC9703223)
- Marlowe FW (2004), "Marital residence among foragers", *Current Anthropology* 45:277–284. **Record only.** It was not found in Europe PMC; I believe the DOI is 10.1086/382256 but did not verify it.

### Inferences
- **Mate-search mechanism (structural nature parameter).** Eligible partners should be sought through the *metapopulation*, not only within one's band. Plausible evidence-based mechanisms:
  - Visits to bands where kin or affines live (Hill 2014: kinship and affinity raise interaction rates).
  - Kin-brokered matching: 85% of foragers arrange marriages, and 80% involve exchange between the families.
  - Relocation to marry (15% of Pumé first marriages).
  - These can be implemented as *capabilities*, such as "parents and siblings know unmarried people in other bands" or "visit a kinsperson's band". The marriage-alliance norms themselves can then emerge.
- **Emergence tests:**
  - Adult band size of about 20–30 (Hill 2011: 28.2).
  - Low within-band relatedness, with most co-residents unrelated (Hill 2011; Dyble 2015).
  - Annual swings in band adult sex ratio of about ±0.1–0.15 around 0.5 for bands of about 20 adults (Kramer 2017).
  - Age at first marriage of about 15 for women and about 18 for men in a high-fertility forager population (Pumé; other populations differ).
- **ACL's extinction problem (about a third of worlds) is expected for isolated single bands.** Pumé bands of about 11 men and 10 women are viable only *because* people disperse outside them. With 20 founders and little mixing, ACL is effectively simulating a single isolated band. The evidence supports founding several bands that share a language and kin ties, rather than making mate search easier inside a band.

### Gaps
- Kilometre distances to a spouse's natal group (MacDonald & Hewlett 1999; Ju/'hoansi, Aka) were not retrieved.
- No verified cross-cultural *percentage* of marriages that cross band boundaries; the Pumé 15%/37% figures cover relocation only.
- Ages at first marriage for Hadza, Ju/'hoansi and Ache were not verified in this pass.

---

## 3. Seasonality, lean seasons and famine

### Takeaway
Hard numbers on how seasonal forager environments are, at the scale of an individual population, were the weakest part of this search. The robust comparative findings are three:
- Mobility (distance per move) scales with temperature and rainfall (Hamilton 2016).
- Storage dependence rises sharply below a cold-climate threshold (Binford's ET ≈ 15.25 °C; see section 4).
- Controlling for habitat quality, hunter-gatherers had *less* famine than agriculturalists (Berbesque 2014).

### Cited Findings
- **Famine frequency (cross-cultural database):** "if we control for habitat quality, hunter-gatherers actually had significantly less … famine than other subsistence modes". Berbesque JC, Marlowe FW, Shaw P, Thompson P (2014), "Hunter-gatherers have less famine than agriculturalists", *Biology Letters* 10:20130853, doi:10.1098/rsbl.2013.0853. **Abstract read.** The famine-frequency coding categories and effect sizes were not retrieved. — [DOI](https://doi.org/10.1098/rsbl.2013.0853)
- **Resource stress and sharing:** in 96 Standard Cross-Cultural Sample (SCCS) societies, resource stress predicts more food and labour sharing beyond the household. Religious beliefs do not mediate this. Skoggard I, Ember CR, Pitek E, Jackson JC, Carolus C (2020) *Human Nature* 31:249–271, doi:10.1007/s12110-020-09371-8. **Abstract read.** — [DOI](https://doi.org/10.1007/s12110-020-09371-8)
- **Climate and mobility:** in Binford's data, average distance per move depends on temperature (r² = 0.36) and on precipitation residuals (r² = 0.24). Tropical groups move most often. Hamilton et al. (2016). **Full text read.** — [PMC5094510](https://europepmc.org/article/PMC/PMC5094510)
- **Daily hunting success:** about 28% for Hadza, 27% for !Kung and 10–30% for Efe. In Lewis et al.'s model, enforced sharing protects individuals from food shortage on about 2 of every 3 days. These figures are cited in Lewis et al. (2014) from primary ethnographies. **Full text read; the values are secondary.** — [PMC4284614](https://europepmc.org/article/PMC/PMC4284614)
- **Hadza large-game returns:** over 256 days (2,076 hunter-days, 1985–89), Hadza took 71 large animals, about 10,115 kg live weight. That is just under 5 kg per hunter-day, or about 0.7 kg live weight per consumer-day. Hawkes K, O'Connell JF, Blurton Jones NG (2001), "Hadza meat sharing", *Evolution and Human Behavior* 22:113–142. **Full text read** (PDF). The DOI was not verified; I believe it is 10.1016/S1090-5138(00)00066-0. — [PDF](https://in-africa.org/wp-content/uploads/2012/12/Hawkes-et-al-2011-EHB-Hadza-meat-sharing.pdf)
- **Synchrony and extinction risk:** across 227 indigenous Amazonian populations (1,580 census estimates), population volatility declines with size as N^−1/4, not the N^−1/2 expected if individuals were independent. Synchronised shocks (rainfall, prey, epidemics) therefore raise extinction risk for small populations above what classical viability analysis predicts. Hamilton MJ, Walker R (2026), "Demographic synchrony increases volatility and extinction risk in human populations", *Cambridge Prisms: Extinction*, doi:10.1017/ext.2026.10013. **Full text read.** — [PMC13430546](https://europepmc.org/article/PMC/PMC13430546)

### Inferences
- **Seasonal amplitude (nature parameter).** ACL can tie its seasonal amplitude to real climate rather than tuning it. One option is a climate-derived index such as Binford's effective temperature (ET), computed from warmest- and coldest-month temperatures (see section 4), assigned per world.
  - Worlds with ET < 15.25 should have a genuine lean season, in which fresh food falls to near zero for months.
  - Tropical worlds should have mild seasons but high day-to-day variance in hunting success (only about 25–30% of hunter-days succeed).
  - This links to ACL problem (3): tools matter little because the environment is too forgiving. The evidence suggests the harshness should come from *stochastic daily failure* (about 70% of days without game) and, in cold worlds, from a *long zero-production season*, not from global scarcity.
- **Emergence test:** in a working ACL, sharing should rise with resource stress (Skoggard 2020), and residential moves should become rarer in more productive or wetter worlds (Hamilton 2016).
- **Calibration warning:** Hamilton & Walker (2026) suggest that some die-off of small, synchronised populations is *realistic*. ACL should not treat every extinction as a bug. It should compare extinction rates for populations of 20 versus about 500, given correlated shocks.

### Gaps
- No verified quantitative coefficient of variation of food availability for named foragers. Ju/'hoansi and Hadza seasonal body-weight changes were not retrieved, and neither were Jenike (2001) or Hurtado & Hill (1990, Hiwi).
- Berbesque et al.'s famine frequency coding (SCCS variables) was not retrieved, so no "famines per generation" number is available.
- No 2020–2026 cross-cultural paper with an explicit numeric seasonality index for foragers was located in this pass.

---

## 4. Storage and delayed return

### Takeaway
In the classic literature, large-scale food storage among foragers is tied to:
- strongly seasonal but abundant resources,
- cold climates (Binford's ET < ~15.25 °C), and
- techniques for mass harvest and preservation (Testart 1982).

Storage also goes with sedentism, higher density and inequality. Mobile, immediate-return, demand-sharing foragers mostly do *not* store food, and demand sharing breaks down when such groups become sedentary. The evidence here is largely qualitative and typological, with Binford's ET threshold the main number.

### Cited Findings
- **Testart's four conditions.** Testart A (1982), "The significance of food storage among hunter-gatherers: residence patterns, population densities, and social inequalities", *Current Anthropology* 23(5):523–537. **Record only.** The full-text PDF failed with a certificate error, and the DOI (believed to be 10.1086/202894) was not found in Europe PMC. — [Author-hosted PDF (TLS error)](http://www.alaintestart.com/UK/documents/storage.pdf)
  - Large-scale storage of a staple happens where four conditions meet: abundant resources, seasonal resources, efficient techniques for getting food, and techniques for storing it.
  - Testart links storage to sedentism, higher population density and social inequality.
  - These statements are from secondary summaries in the search results, not from the paper itself.
- **Binford's storage threshold.** Binford's threshold is ET = 15.25 °C, with ET = (18W − 10C)/((W − C) + 8), where W and C are the mean temperatures of the warmest and coldest months. Below the threshold, foragers depend on procuring a large surplus during the growing season to get through the winter. Binford LR (2001), *Constructing Frames of Reference*, University of California Press; also Binford LR (1980), "Willow smoke and dogs' tails", *American Antiquity* 45:4–20. **Record only.** These came from search snippets of secondary works and were not verified in the primary texts. — [Search result (ResearchGate, Binford-database analyses)](https://www.researchgate.net/publication/257578033_Exploring_Adaptive_Variation_among_Hunter-gatherers_with_Binford%27s_Frames_of_Reference)
- **Demand sharing depends on mobility.** Source: Lewis et al. (2014). **Full text read.** — [PMC4284614](https://europepmc.org/article/PMC/PMC4284614)
  - In their agent-based model, demand-sharing populations with free riders survive only when families can move between camps.
  - Sedentary demand sharers accumulate free riders and go extinct.
  - The authors note that "ethnographic studies have shown that demand sharing does break apart when hunter-gatherer populations are forced to settle".
  - The model allows storage only as body fat, capped at 30 days' survival. It cites food storage as "not observed in simple hunter-gatherers".
- **Sharing changes with sedentism (Ache).** Source: Gurven M, Hill K, Kaplan H (2002), "From forest to reservation: transitions in food-sharing behavior among the Ache of Paraguay", *Journal of Anthropological Research* 58(1):93–120. **Full text read** (PDF). — [PDF](https://gurven.anth.ucsb.edu/sites/secure.lsit.ucsb.edu.anth.d7_gurven/files/sitefiles/papers/gurvenetal2002JAR.pdf)
  - On forest treks, nuclear families gave away 80% of what they acquired, and only 3.4% of family pairs never transferred food.
  - On the agricultural reservation, 33% of family pairs had no transfers, and an item was shared with about 9% of families (41% in the forest).
  - For non-meat packages larger than about 2,000 kcal, 70–90% was given away. Families kept about 1,500–2,000 kcal regardless of package size, even for packages of 20,000 kcal: "greater production does not mean greater consumption".
  - Kaplan et al. (2000) also note that reservation Ache "withhold even large game, sharing mainly with preferred partners".
- **Sharing practices vs ecology (22 societies).** Across 22 small-scale societies in the Americas and Siberia, presence or absence of 14 basic sharing practices showed no significant relationship to environmental variables, except dependence on animal husbandry and status distribution. Pairwise dissimilarity in sharing showed none at all. Ahedo V, Caro J, Bortolini E, Zurro D, Madella M, Galán JM (2019) *PLoS ONE* 14:e0216302, doi:10.1371/journal.pone.0216302. **Full text read.** — [PMC6541262](https://europepmc.org/article/PMC/PMC6541262)

### Inferences
- **ACL's failure "storage and sowing fail because benefits get shared away" matches real ethnography.**
  - Real Ache foragers gave away about 70–90% of large packages. Families kept about 1,500–2,000 kcal no matter how much they produced (Gurven 2002).
  - Under demand sharing, the producer's returns on surplus are largely removed. Real foragers storing at scale did so under different *conditions*: sedentism, seasonal gluts, cold winters (Testart; Binford), and then property norms.
  - So ACL should **not** script "this is mine" norms. It should create the conditions in which they become adaptive: worlds with ET < 15.25 and long zero-production seasons, mass-harvestable seasonal gluts, and preservation technology. Then test whether ownership and restricted sharing *emerge*.
- **Emergence test (from Gurven 2002):** when ACL agents become more sedentary or rely on cultivation, the share of family pairs with no transfers should rise (from about 3% to about 33% in the Ache case). The share of the band an item reaches should fall (from about 41% to about 9%).
- **Nature parameter:** forager body-fat reserves of roughly 30 days' maintenance. This is Lewis et al.'s model assumption, based on hunger-strike data, not forager field data.

### Gaps
- Testart's and Binford's quantitative tables were not verified. Binford's QSTOR (quantity stored) variable exists in his database and in D-PLACE but was not extracted.
- No quantitative cross-cultural study of "this is mine" norms or property among foragers was retrieved. Woodburn (1982, "Egalitarian societies", *Man* 17:431–451) and Peterson (1993, "Demand sharing", *American Anthropologist* 95:860–874) are the classic qualitative sources (**record only**; from my own knowledge, not retrieved here).

---

## 5. Food sharing: who gives to whom, how much is shared, risk reduction

### Takeaway
Sharing in mobile foragers is extensive and quantified:
- Ache forest families give away about 80% of what they acquire.
- A Hadza hunter's own household takes only about 5–10% of a large carcass.
- Sharing is explained jointly by reciprocity, kinship and tolerated scrounging, each with similar effect sizes (r ≈ 0.2–0.48 for reciprocity).
- Sharing is structured in levels: household, a cluster of 3–4 households, then the camp.

### Cited Findings
- **Hadza meat shares.** Hawkes, O'Connell & Blurton Jones (2001). **Full text read.** — [PDF](https://in-africa.org/wp-content/uploads/2012/12/Hawkes-et-al-2011-EHB-Hadza-meat-sharing.pdf)
  - From 113 household shares weighed from 20 large kills, the successful hunter's household took about 5% of meat from prey under 180 kg and about 10% from prey over 180 kg. Each other man's household took about 5%.
  - Share size stayed about constant (mean 3.14 kg) across carcasses of 40–160 kg.
- **Ache, forest vs reservation.** Gurven, Hill & Kaplan (2002). **Full text read.** — [PDF](https://gurven.anth.ucsb.edu/sites/secure.lsit.ucsb.edu.anth.d7_gurven/files/sitefiles/papers/gurvenetal2002JAR.pdf)
  - Forest families gave away 80% of their acquisitions. An item reached on average 2.6 other families, about 41% of the band.
  - Meat made up about 78% of calories on forest treks in the 1980s.
  - Each additional consumer per producer in the donor family reduced the share given away by about 4–15%, depending on the model.
  - Each extra trip member raised the share given away by about 1%.
- **Reciprocity vs kinship vs scrounging.** Meta-analysis of 32 independent study populations of humans and other primates: reciprocity had an effect size of r = 0.20–0.48, depending on the measure, similar to the effects of kinship and tolerated scrounging. Jaeggi AV, Gurven M (2013) *Proc R Soc B* 280:20131615, doi:10.1098/rspb.2013.1615. **Abstract read.** — [DOI](https://doi.org/10.1098/rspb.2013.1615)
- **Synthesis of why humans share.** Humans in a risky foraging niche use sharing to buffer risk and to recruit mates and allies, with co-evolving norms of production and sharing. Jaeggi AV, Gurven M (2013), "Natural cooperators: food sharing in humans and other primates", *Evolutionary Anthropology* 22:186–195, doi:10.1002/evan.21364. **Abstract read.** — [DOI](https://doi.org/10.1002/evan.21364)
- **Life-history consequences of sharing.** Kaplan H, Hill K, Lancaster J, Hurtado AM (2000), "A theory of human life history evolution: diet, intelligence, and longevity", *Evolutionary Anthropology* 9(4):156–185. **Full text read** (PDF). — [PDF](https://www.unm.edu/~jlancas/KaplanHillLancasterHurtado_2000_LHEvolution.pdf)
  - By age 15, forager children had consumed over 25% of their expected lifetime energy but acquired less than 5% of their lifetime production.
  - Those who share a greater share of their production are provisioned by more people when sick or injured.
  - Meat is transferred most between non-kin, followed by extracted products, then fruits.
- **Multilevel sharing structure.** In Agta and Mbendjele BaYaka sharing networks, sharing clusters of 3–4 households sit within camps. These levels are linked to provisioning between the sexes, kin provisioning and risk-reduction reciprocity. Dyble M, Thompson J, Smith D, Salali GD, Chaudhary N, Page AE, Vinicius L, Mace R, Migliano AB (2016) *Current Biology* 26:2017–2021, doi:10.1016/j.cub.2016.05.064. **Abstract read.** — [DOI](https://doi.org/10.1016/j.cub.2016.05.064)
- **Model of sharing networks.** A normative model reproduces empirical properties of food-sharing networks: kin-based households in clusters with few links between clusters. The modularity minimises starvation risk. Large, unpredictable items (meat, honey) are most widely shared. Plana F, Pérez J, Abeliuk A (2023) *PLoS ONE* 18:e0272733, doi:10.1371/journal.pone.0272733. **Full text read** (model, not field data). — [PMC10171659](https://europepmc.org/article/PMC/PMC10171659)
- **Demand-sharing model outputs.** Lewis et al. (2014) **full text read.** — [PMC4284614](https://europepmc.org/article/PMC/PMC4284614)
  - In their model, free riders persist at about 10% of mobile demand-sharing populations.
  - Simulated life expectancy at age 50 was 9.1 years for sharers versus 3.3 for loners. The observed Agta figure is 10.8.

### Inferences
- **Nature parameters:**
  - Large, unpredictable packages (game, honey) arrive as rare, large windfalls: Hadza large-game success about 28% of hunter-days, carcasses around 140 kg.
  - Plant foods arrive as small, frequent packages.
  - Package size and predictability should be properties of the *resource*, coded in nature. How widely each is shared should *emerge*.
- **Emergence tests:**
  - Mobile ACL bands should converge on giving away about 70–90% of large packages, with the acquirer keeping about 5–10%.
  - About 80% of a family's acquisition should flow out; nearly all family pairs (about 97%) should exchange food at least once.
  - Sharing should cluster into groups of about 3–4 households.
  - When agents settle or farm, sharing breadth should collapse toward reservation-Ache values.
  - Free riders should persist at about 10% of mobile populations.
- **Sowing and storage experiments.** A real mechanism that limits sharing-away is *mobility plus relocation to escape free riders* (Lewis 2014), together with the shift toward preferred partners under sedentism (Gurven 2002). ACL could test whether letting producers choose co-residents, or leave, rescues the payoff of storage.

### Gaps
- The primary source for Ache sharing, Kaplan H, Hill K (1985), "Food sharing among Ache foragers: tests of explanatory hypotheses", *Current Anthropology* 26:223–246, was not read. A search snippet said individuals gave away 87% of honey; that figure is unverified.
- Gurven M (2004), "To give and to give not", *Behavioral and Brain Sciences* 27:543–583, which compiles the percentage of consumed food produced by others across foragers, was **not retrieved** (Europe PMC did not find doi:10.1017/S0140525X04000123). It is the key source for a cross-cultural "fraction of diet shared" number.
- Winterhalder B (1986), "Diet choice, risk, and food sharing in a stochastic environment", *J Anthropol Archaeol* 5:369–392 (record only, from my own knowledge): the classic risk-pooling model. Its quantitative result (most variance reduction is achieved with a small number of sharers) was mentioned secondarily in Ahedo et al. (2019) but not verified.
