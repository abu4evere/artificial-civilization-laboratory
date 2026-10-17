# SA1-F Part B — Evidence for sight (`perception`) and range (`reach`), as ratios

**Written:** 16 October 2026, under `SA1F-frozen` (Part B: read-only; rule 17; "use comparable ratios", the creator).
No code in ACL changed, no setting chosen. "Full text read" = text extracted and the relevant passages read;
"record only" = reported in another source. Numbers from Binford's data come from `evidence_ratios.py`; ACL's from
`acl_ratios.py` (`acl_ratios.json`). One note for both settings, because the same obstacle (a tile has no measured size,
N10) blocks both, and the same ratios answer both.

## What the two settings do in ACL (from the code, `code_e13r`)

- **`perception` = 4 tiles:** whom and what a person can see (people, food, water, prey), and so who counts as a possible
  partner; a 9 × 9 square (Chebyshev distance), 81 tiles of the world's 1,600.
- **`reach` = 3 tiles:** the furthest a person can move in a week and still act, and the radius of "near" (children cared
  for, one's own store, company).
- ACL's time step is **a week**, and a person may move every week. Foragers live in camps that move every few weeks and
  forage out from them every day. So "4 tiles" cannot be compared with any distance in metres, and the comparison has to
  be made in things both worlds have: **how far the base moves relative to the area searched**, and **how many people one
  is in touch with**.

## Sources

- **Binford, L. R. (2001).** *Constructing Frames of Reference.* University of California Press. Data: the LRB table, 339
  societies, as published with the R package `binford` (B. Marwick;
  [data-raw/LRB.csv](https://github.com/benmarwick/binford/tree/master/data-raw)); **data read** (the table itself;
  variables `grppat`, `nomov`, `dismov` in miles, `group1`, `group2`, per the package codebook, Binford 2001:117).
- **Grove, M., Hall, H., Timbrell, L., Benton, A. and French, J. C. (2023).** Moving far or moving often? A neglected axis
  of variation in hunter-gatherer mobility. *Journal of Archaeological Science: Reports* 52: 104266
  ([open access](https://livrepository.liverpool.ac.uk/3176567/1/Grove%20et%20al.%202023%20JASR.pdf)); **full text
  read** (methods, sections 2.1–2.2). The filter used here (whole group moves camp, `grppat` = 1; `nomov` > 0) gives their
  175 groups exactly. Reports Binford's (1982) "complete radius leapfrog": a camp that relocates moves at least the
  **diameter** of the foraging radius it has depleted (Binford 1982, *The archaeology of place*, J. Anthropol. Archaeol. 1:
  5–31: **record only**, as reported by Grove et al.).
- **Wood, B. M., Harris, J. A., Raichlen, D. A., Pontzer, H. et al. (2021).** Gendered movement ecology and landscape use
  in Hadza hunter-gatherers. *Nature Human Behaviour* 5: 436–446 ([doi](https://doi.org/10.1038/s41562-020-01002-7);
  [open text](https://escholarship.org/content/qt32n5s66t/qt32n5s66t_noSplash_fc0b0c23dbddd31d5741a37068aef164.pdf));
  **full text read** (results, Fig. 7). GPS, 179 people, 2,078 person-days: adults walked **7.6 km a day (women) and 12.9
  km (men)**; foraging trips went **beyond 10 km from camp** (the paper defines "far from camp" as beyond 10 km and models it out to 12 km; it gives no single foraging radius); median distance to the nearest person while foraging **3.2 m
  (women and girls) and 63.3 m (men and boys)**.
- **Pontzer, H., Raichlen, D. A., Wood, B. M. et al. (2012).** Hunter-gatherer energetics and human obesity. *PLoS ONE*
  7(7): e40503 ([doi](https://doi.org/10.1371/journal.pone.0040503)); **record only** (figures as reported in a search summary of the article; not read): Hadza walked
  **5.8 ± 1.7 km a day (women), 11.4 ± 2.1 (men)** (GPS, 11 days).

## Forager numbers (Binford 2001; 175 fully mobile societies; `evidence_ratios.py`)

| measure | median (middle half) |
|---|---|
| camp moves per year | 12 (7–14) |
| weeks between camp moves | 4.3 (3.7–7.4) |
| km per move | 28 (18–40) |
| km of camp movement per week, averaged over the year | 6.0 (2.6–10.1) |
| smallest cooperating group (dispersed camp), people | 16 (11–18.5) |
| aggregated camp, people | 36.5 (30–50) |

## The ratios

ACL's side: `acl_ratios.py` (control code; 16 of F1's seeds, 501–516; 60 years; adults and elders, every week; 778,945
person-weeks; the observer leaves the world unchanged, checked by state hash). Forager side: the table above, and the
Hadza GPS study.

| | ACL (default: sight 4, reach 3) | foragers | ratio, ACL ÷ foragers |
|---|---|---|---|
| **how often the place one sleeps changes** | **59% of weeks** (stays put in 41%; moves the full 3 tiles in 27%) | camp moves every 4.3 weeks (middle half 3.7–7.4): **about 23% of weeks** (14–27%) | **about 2.5 ×** as often |
| **people in direct contact in a week** | **9 others within sight** (median; middle half 4–15); 7 within reach | the camp one lives in: dispersed camps of **16** (11–18.5), so **15 others**; 36.5 when camps gather | **about 0.6 ×** (9 against 15) |
| **how far a move goes, against the area searched** | a week's move, when there is one, averages 2.2 tiles: **0.56 of sight**, 0.74 of reach | a camp move goes at least the **diameter** of the foraged-out area (Binford's leapfrog, record only): **2 or more foraging radii** | not comparable (below) |

**What can be compared, and what cannot.**
1. **How often people change place: comparable, and ACL's people move about two and a half times as often** as forager
   camps. This is a behaviour, not a setting: the rule lets people move every week, and they do so in more than half of
   weeks. A real difference, measured both sides, without any tile size. It is what the council asked about (16 October).
2. **How many people one is in touch with: comparable as a count, and ACL's people see fewer** (a median of 9 against a
   camp's 15). Two cautions: ACL's whole world holds only 20–60 people, so the count is capped by the population as much
   as by sight; and a forager in camp is in touch with campmates every evening, which ACL, with a weekly step, has no
   equivalent for. This is the one anchor for sight that needs no tile size: **"people in direct contact in a week" is
   about the size of a forager camp**.
3. **How far a move goes: not comparable.** It would need to know which ACL quantity plays the part of a forager's daily
   foraging radius. Sight (4) is the area a person knows first-hand, but ACL people forage only the tile they end the week
   on, so there is no foraging radius to set against a camp move. Range (`reach`) stays **unanchored**; this note records
   why, as N10 recorded for the tile.

## Reading (for the creator; nothing adopted)

1. **Sight (`perception`)** can be anchored only indirectly, as a count of people in contact: at today's value ACL's
   people see about 60% of the people a forager camp holds. SA1 found that more sight keeps worlds alive. Matching the
   camp count would mean raising sight, but how far depends on population as much as on sight, so it would have to be
   measured, not computed, and it is a change to nature under Law 126 (the creator's decision; nothing adopted). It must
   not be chosen to make worlds survive.
2. **Range (`reach`)** cannot be anchored with what exists: the comparison needs a foraging radius, which ACL does not
   have. It stays unanchored, with every finding's caveat (SA1).
3. **How often people move** is the clearest finding here, and it was not one of the two settings: ACL's people change
   place about **2.5 times as often** as forager camps move. It gives the council's proposed residence-time study (people
   move only every few weeks, the same distance a month) a measured basis on both sides, and Binford's data as its
   evidence. It would be a new study, frozen first; nothing is started.
4. All of this assumes ACL's week is a week. If the creator ever anchors time differently, every ratio here changes.
