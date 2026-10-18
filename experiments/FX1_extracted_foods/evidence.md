# FX1 — Evidence review: food that has to be opened, dug or hunted (read-only; nothing adopted)

**Why:** the council (16 October 2026, Gemma 4) proposed "a food that only opens with force" to answer E8.2's finding
that tools add only a few percent to food (`drafts/council/synthesis_2026-10-16.md`). Under Law 126 a change to nature
needs evidence about real people first. Written in sleep mode (18 October 2026, the creator's standing instruction:
useful work that needs no decision). **No code in ACL changed; no setting chosen.** "Full text read" = text extracted and
the relevant passages read; "record only" = reported in a search result or another source.

## Sources

- **Kaplan, H., Gurven, M. and Winking, J. (2009).** An evolutionary theory of human life span: embodied capital and the
  human adaptive complex. In *Handbook of Theories of Aging* (2nd ed.), ch. 3
  ([PDF](https://gurven.anth.ucsb.edu/sites/secure.lsit.ucsb.edu.anth.d7_gurven/files/sitefiles/papers/kaplanetal_ch3.pdf));
  **full text read** (the diet section), summarising **Kaplan, Hill, Lancaster and Hurtado (2000)**, *Evolutionary
  Anthropology* 9: 156–185 (record only). Ten foraging societies with measured caloric production: **vertebrate meat
  about 60%** of calories (30–80%, equally weighted mean); **extracted resources about 32%** ("roots, nuts, seeds, most
  invertebrate products, and difficult-to-extract plant parts"; "nonmobile resources that are embedded in a protective
  context such as underground or in hard shells or bearing toxins that must be removed before they can be consumed");
  **collected resources about 8%** (fruits, leaves, "simply gathered and consumed"). Chimpanzees: collected 95%,
  extracted 3%, hunted about 2%. Extraction skill rises slowly with age: Hiwi root-digging rates peak at 35–45; Hambukushu
  nut-cracking peaks about 35; 10-year-olds extract at 10–15% of adult rates.
- **Hill, K., Kaplan, H., Hawkes, K. and Hurtado, A. M. (1987).** Foraging decisions among Aché hunter-gatherers: new data
  and implications for optimal foraging models. *Ethology and Sociobiology* 8: 1–36
  ([PDF](https://content.csbs.utah.edu/~hawkes/Hill_al87ForagingAcheOFT.pdf)); **full text read** (results, Tables 1–2).
  Overall foraging returns, search included: **men 1,339 calories per hour** (mostly hunting), **women 1,221** (mostly
  plant foods). After encounter (Table 2): deer 15,398 cal/hr, collared peccary 6,120, paca 4,705; honey 8,666–22,411;
  palm fiber starch 2,246–3,219; fruits 2,549–10,078. A peccary hunt averages 316 man-minutes and 29,040 calories.
- **Koster, J., McElreath, R., Hill, K. et al. (2020).** The life history of human foraging: cross-cultural and individual
  variation. *Science Advances* 6: eaax9070 ([doi](https://doi.org/10.1126/sciadv.aax9070)); **record only** (search
  summary of the abstract): hunting records from 40 locations; average age of **peak productivity 30–35**.

## ACL, measured (`acl_diet.py`; nature v2; seeds 501–516; 60 years; read-only, checked by state hash)

| food source | ACL | foragers (Kaplan et al.) | chimpanzees |
|---|---|---|---|
| wild plants, picked and eaten (collected) | **98.9%** | 8% | 95% |
| crops (ACL's only food that takes work before eating) | 1.1% | (extracted 32%) | (3%) |
| meat (hunted, fish included) | **0.02%** | 60% | 2% |

- Hunts: 1,659 in 16 worlds × 60 years, **138 successful (8%)**; meat per success about **10.5 food units**, against about
  **20 units** from an average week of foraging (E8.2's measure in SA1-F's control worlds). A successful hunt is worth
  half a week of picking plants.
- Shares are of ACL's food units (what its bodies eat), not calories; the comparison is of shares.
- **Returns to hunting against foraging, per unit of time** (a ratio, so no tile or calorie scale is needed): an ACL
  week spent hunting yields on average 8% × 10.5 ≈ **0.9 food units**, a week spent foraging about **20**: hunting returns
  **about 4%** of foraging. Among the Aché, hunting (men's returns, 1,339 cal/hr) and gathering (women's, 1,221) pay
  **about the same (×1.1)**. ACL's hunting is about 20–25 times less rewarding, relative to plants, than real hunting.
  (ACL's figure is per hunt, not divided among the party, so it overstates each hunter's return.)

## Reading (for the creator; nothing adopted)

1. **ACL's people eat like no human foragers, and more like chimpanzees than chimpanzees do.** Almost all their food is
   simply picked up. In real forager diets, 92% of calories come from food that must be hunted, dug, cracked or
   detoxified, the foods that take years of skill and, often, tools.
2. **This is a measured, evidence-anchored version of the "generous earth" diagnosis** (E8.2: tools add a few percent).
   It suggests why tools, skill and teaching barely matter in ACL: the world almost never asks for them.
3. **Two kinds of candidate condition** (each a change to nature under Law 126, for the creator; none to be tuned toward
   any outcome):
   - **Embedded plant food:** some plant food is protected (underground, in hard shells), so that it yields far more
     when dug or struck with something hard, by the physics of properties ACL already has. Anchor: extracted foods are
     about a third of forager calories.
   - **Meat worth hunting:** in ACL, hunting returns about 4% of what foraging does; among the Aché, the two pay about
     the same (Hill et al. 1987, above). The anchor is a ratio of returns per unit of time. Before any number is touched,
     the evidence should be widened beyond one people (Hadza and Hiwi return rates), and the cause found in ACL's code:
     the chance of success, the meat per kill, or the cost of a hunt.
4. **What this does not show:** that changing the diet would let culture accumulate. That would be a frozen experiment,
   with this note as its evidence.

## Where ACL's low hunting returns come from (read from the code, 18 October 2026; nothing changed)

`acl/mind.py` (`hunt_chance`), `acl/actions.py` (`resolve_hunts`), `acl/fauna.py` (`SPECIES`, `take_prey`):

1. **The chance of success** is `hunt_base_chance` (0.10) × party size^1.5 × (0.5 + hunting skill) × tool, capped at 0.92.
   A lone hunter of middling skill (0.3) with no tool: 0.10 × 1 × 0.8 = **8%**, as measured. `hunt_base_chance` is an
   unanchored setting.
2. **No prey on the tile, no chance:** the chance is 0 unless an animal of a prey species stands on the hunter's tile
   that week, and the week is spent either way. Many of the 1,521 failed hunts may be of this kind (not counted
   separately by `acl_diet.py`).
3. **Small game dominates:** a success takes one deer (22 units of meat) or bison (55), but small game in bundles worth
   about 10 (rabbits, 3 each; fish, 1.5 each); in the measured worlds fish and rabbit gave 85% of all meat.
4. **Meat beyond what a hunter can carry is lost:** each hunter keeps `min(share, carrying room)`. A large kill cannot
   feed a camp unless it is carried and given away the same way any food is.

Each is a candidate place for a Law 126 review, not a fix: the evidence above is about what real hunting returns, not
about which ACL rule should change. Any change would be one rule at a time, frozen, with this note as its evidence.
