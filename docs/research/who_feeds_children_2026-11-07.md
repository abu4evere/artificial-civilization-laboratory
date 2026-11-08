# Who feeds the children in small-scale societies, for law B ("both parents feed") (7 November 2026)

**Why:** DF1 found that in ACL the mother feeds her children by rule (`biology.py`: `child.caregiver = mother.id`).
The father feeds them only by gift: about one twentieth of what mothers feed
(`experiments/DF1_dependents_feeding/findings.md`). Council round 78 queued law B, "both parents feed". It has two
candidate forms:
- **second-feeder** (GPT, Gemini): the mother first, then the father if present and holding food;
- **shared pool** (DeepSeek): any present adult carer with food.

These sources are anchors. A source suggests; only a frozen study decides.

## Hooper, Gurven, Winking & Kaplan 2015 — **full text read** (Introduction, Methods, Results verbatim; Discussion only as a machine summary)
Hooper PL, Gurven M, Winking J, Kaplan HS (2015). Inclusive fitness and differential productivity across the life
course determine intergenerational transfers in a small-scale human society. *Proc. R. Soc. B* 282: 20142808
(PMC4345452, CC BY). Read through a web-fetch agent.

**Who they studied:** Tsimane' (Bolivia), **forager-horticulturalists, not pure foragers**. 1,254 people in 8
communities, about 14 months each, 2005–2010. All figures are net calories per day.

**Within the family:**
- **Fathers to their children:** mean 1,107, peak 1,737 in their 30s.
- **Mothers to their children:** mean 177, peak 1,042 in their 30s. This **excludes breastfeeding** (Fig. 2 caption).
- **Husbands to wives:** mean 273 (p < 0.001).
- **Children receive** net food until about age 10 at the peak:
  - daughters: mean 437, peak 701;
  - sons: mean 393, peak 792.
- **Grandparents to grandchildren:**
  - grandmothers: mean 117, peak 176 in their 40s;
  - grandfathers: mean 223, peak 337 in their 60s.
- When a parent is absent, grandchildren under 12 get more: about 90 more without the mother, 60 more without the
  father.
- **The analysis assumes food is pooled within the nuclear family** ("regular pooling of food within nuclear families").
  Each parent's transfer is modelled to all their children together. Nothing read says a parent feeds only certain
  children.
- The paper gives **no share** of a child's food by provider.

**Between families:** food flows toward need, along kinship.
- Net transfers from older to younger families "increase with the number of unproductive mouths in the younger
  household, but decrease with those in the older household". "Energy flows to the demographically needier of the two
  families."
- Need without relatedness was not significant (p > 0.12).
- Table 2, net calories per day by relationship:
  - parent to adult child: 150.3;
  - sibling to sibling: 113.4;
  - other kin: 47.3 (not significant);
  - non-kin: 49.0.

## Wood & Marlowe 2013 — **abstract and endnotes only** (full text paywalled)
Wood BM, Marlowe FW (2013). Household and kin provisioning by Hadza men. *Human Nature* 24: 280–317.

Hadza (Tanzania), foragers, data from 2005–2009:
- Men brought food to camp on 28% of days if single, 31% if married without children at home, and **42% if married
  with children at home**.
- Men "channeled the foods they produced to their wives, children, and their consanguineal and affinal kin". Large
  game was shared "in ways that significantly advantaged producers' households". The best hunters gave their families
  3–4 times the food of median or poor hunters.
- Nothing seen on men giving more while the wife is nursing. The earlier note's mention of this
  (`mothers_energy_2026-11-07.md`, Marlowe) stays **record only**.

## Hawkes, O'Connell & Blurton Jones 2014 — **abstract only** (the open PDF could not be read as text)
*Human Nature* 25: 596–619, a reply to Wood & Marlowe.

The other side of the debate:
- In their 1980s data, men targeted big game though rarely successful, and "most of the meat went to others, at
  significant opportunity cost to their own families".
- They argue that this brings collective benefits, and that status competition is a likely explanation.
- **No numbers were seen.**

## What this suggests for ACL (not a decision)
- **ACL is reversed against the Tsimane' anchor.**
  - In ACL, mothers feed by rule. Fathers' gifts are about 1/20 of that, and the father becomes caregiver only after
    the mother's death (0.157 of dependent-weeks).
  - Among the Tsimane', fathers' net transfers to children (mean 1,107 calories a day) are about 6 times mothers'
    (177). This leaves out breastfeeding, which ACL also does not model.
- **Pooling within the nuclear family** is the modelling assumption of the one full-text source. This sits closer to
  a shared family pool than to a strict mother-first order. Two cautions:
  - it is an analytic assumption, not a measured rule;
  - the Tsimane' grow crops.
- **Food flows to need along kinship** between families. ACL's gift rule already weighs the receiver's hunger, kin,
  affection and partner (`mind.py`, the give motive). So ACL's between-family part is already roughly of this shape.
  - *Correction (7 November, before commit of any study):* first written as "`care × kin` and `q_trouble`". Those
    weigh the separate care action, not gifts.
- **For the council (round 79):**
  - Does law B in either form fit these anchors?
  - Should the father's share depend on presence and food in hand (GPT's "do not teleport food"), as these
    data imply? Men brought food to camp, so they were present.
  - **Not to be tuned:** no target share of fathers' feeding may be set from these numbers. The law changes who may
    feed; the shares must emerge.

## Not read
- Wood & Marlowe 2013's full text (paywalled), including any data on provisioning during lactation.
- Hawkes et al. 2014's numbers, and the further reply (*Hum Nat* 25: 620–630).
- Kramer 2010, *Annu. Rev. Anthropol.* 39: 417–436 (cooperative breeding; record only, from a search result).
