# N8 — Evidence: P1 (seek the people you know) and P2 (leave when there is no one); and power

**Written:** October 2026. Questions, anchor criteria and the power method: `questions.md` (committed before any search
or computation). **No code in ACL, no experiment, no choice.** "Abstract read" = abstract read in full (OpenAlex or
PubMed); "full text read" = text extracted and read; "record only" = bibliographic record and search snippets.

## Sources

- **Apicella, C. L., Marlowe, F. W., Fowler, J. H. and Christakis, N. A. (2012).** Social networks and cooperation in
  hunter-gatherers. *Nature* 481: 497–501 ([doi](https://doi.org/10.1038/nature10736); **abstract read**, via PubMed).
  Hadza networks show "geographic decay" (ties more likely between people living nearer), reciprocity, and ties with both
  kin and non-kin, spanning camps. (That Hadza named whom they would like to live with after the current camp ended,
  about six or seven people each, is **record only**, from a snippet.)
- **Aureli, F. et al. (2008).** Fission-fusion dynamics: new research frameworks. *Current Anthropology* 49(4) (**full
  text read**, key passages). In fission-fusion species "individuals must remember the members of their own group for
  longer periods because they are not exposed to them continuously"; but how individuals "keep track of one another
  without maintaining spatial cohesion is a critical next step" for research.
- **Hill, K. R. et al. (2014)** (carried from N5; **summary read**): adults interact with more than 300 same-sex adults
  in a lifetime, across bands.
- **Kramer, K. L., Schacht, R. and Bell, A. V. (2017)** (carried from N5; **abstract read**): in small groups the adult
  sex ratio fluctuates by chance; "dispersal outside of the group is an important behavioural means to mediate locally
  constrained mating options"; in a model, the globally rarer sex disperses. (That most Pumé, 86% of men and 76% of
  women, marry within their natal village, and that women marry at about 15 and men at about 18, is **record only**,
  from snippets.)
- **Hill, K. R. et al. (2011)** (carried from N5; **abstract read**): across 32 foraging societies, either sex may
  disperse at marriage or remain.

## Answers

1. **Do foragers know where known people are?** Their networks span camps and fade with distance (Apicella 2012); they
   meet hundreds of others in a lifetime (Hill 2014); fission-fusion species remember absent group members (Aureli 2008).
   **No source read shows that people keep track of where acquaintances are and travel to them**; Aureli et al. name
   exactly this as an open question.
2. **Travelling to known others to find partners:** not shown in the sources read.
3. **A general capacity?** Remembering absent group members: yes (Aureli 2008). Remembering *where* they are: not
   established in what was read.
4. **Leaving when partners are scarce:** yes: dispersal outside the group is how small groups meet locally constrained
   mating options (Kramer 2017), and either sex may disperse at marriage (Hill 2011). Most people still marry within
   their group (Pumé, record only): dispersal is the response to scarcity, not the rule.
5. **How long people wait before leaving:** no source read gives a figure.
6. **Nature or culture:** remembering others and leaving when no partner is available are plausibly species-typical;
   arranged marriages, marriage rules and who is expected to move are culture.

## Against the anchor criteria (written before the search)

| | criterion | verdict |
|---|---|---|
| **P1** | foragers keep track of where known people are and travel to them, as a general pattern; remembering where others are is a general capacity | **not anchored**: knowing many people across camps is supported, but tracking *where* they are and walking to them is not shown, and the best source read names it as unresolved. **P1 is held**, not designed, until such evidence is found |
| **P2** | the unpartnered leave their group when partners are scarce; timing anchored only if a source gives one | **anchored in its behaviour** (Kramer 2017; Hill 2011); **no timing anchor**. By the criterion, P2 may be designed only in a form whose timing does not depend on a chosen number |

**A timing-free form of P2 (for the creator; nothing chosen):** ACL already has a trigger that needs no new number: a
single adult with no eligible partner within sight (the code's existing condition for exploring). Today that adult
takes a random step. In P2, the step would go **outward, away from the places they have known** (their remembered
places), instead of in a random direction. Only the direction changes; when it happens is the code's own rule.

## Power (`power_n8.py`, `power.md`)

From the control (22 of 64 extinct) and the sham (18 of 64 worlds changed fate by chance; HB1's and MC1's shams
identical), the model gives:

| worlds | F2's full effect | half of it | a third of it |
|---|---|---|---|
| 64 | 0.93 | 0.32 | 0.15 |
| 128 | 1.00 | 0.63 | 0.31 |
| 192 | 1.00 | 0.83 | 0.46 |
| 256 | 1.00 | 0.92 | 0.60 |

Check: with no effect, the test signals "fewer extinctions" in 1.5% of simulated 64-world experiments (≤ 2.5%).

**Consequences:** a realistic mechanism with half of F2's effect needs **about 192–256 worlds** to be detected reliably;
64 worlds detect only effects near F2's. **MC1's "no detectable effect" at 64 worlds cannot rule out a benefit up to
about half of F2's size**, and HB1's harm, which was detected, was large. Any next experiment should be sized from this
table before it is frozen.
