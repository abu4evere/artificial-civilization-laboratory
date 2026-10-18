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
   - **Meat worth hunting:** the value of a kill, against a week of foraging, is far below real forager returns; this
     needs its own evidence review (return rates per hour for large game against plant foods: optimal-foraging studies
     of the Hadza, Ache, Hiwi), before any number is touched.
4. **What this does not show:** that changing the diet would let culture accumulate. That would be a frozen experiment,
   with this note as its evidence.
