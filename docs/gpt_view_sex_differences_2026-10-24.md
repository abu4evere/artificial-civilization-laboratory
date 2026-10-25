# GPT's view: should men and women differ in body in ACL? (24 October 2026)

**Source: GPT (ChatGPT, the creator's account, main ACL chat), asked by the assistant at the creator's request. GPT's
opinion and its reading of sources, in summary; figures and sources not yet checked by the assistant; not sign-off.**

**The question.** In ACL sex matters only for courting (opposite sex), partner search and pregnancy, plus two
leftovers (a father's love for a newborn is 0.8 of a mother's; the newborn's carer is the mother). Otherwise men and
women are identical. Body differences would be nature (Law 126); a division of labour is culture and must only emerge.

## GPT's answers

- **Evidence (averages with overlap):** men ~7–8% taller, ~15–16% heavier, ~36% more lean mass; women's upper-body
  strength ~50–60% of men's, lower-body ~60–70% (Nuzzo 2023; Lassek & Gaulin 2022). Throwing speed differs (~10% in one
  elite handball sample) but hunting success depends far more on tracking, patience, technique, cooperation. Aerobic
  capacity: women ~80–85% of similarly trained men's, by body mass. Energy: needs follow lean mass (Pontzer et al.
  2021); pregnancy ~+340–450 kcal/day in later trimesters, lactation ~+330–400 kcal/day (CDC). Mortality: a female
  survival advantage is common but varies (Raute: life expectancy at 15, women 28.2 vs men 20.8 years; Gurven & Kaplan
  2007); not a universal male death penalty. Fertility: gradual decline with age is what ACL's fixed 16–45 misses.
  Forager labour: women's hunting disputed (Anderson et al. 2023: 79% of 63 societies; Venkataraman et al. 2024:
  coding problems; divisions are widespread but flexible). Childcare constraints and ecology shape who does what.
- **Nature vs scripting by proxy:** a rule "strength sets force, for everyone" is physics; "men and women have
  overlapping strength distributions" is a legitimate body model; "men get +30% hunting success" is scripting. A
  division of labour that comes only from bodies is an **ecological** result, not yet **culture**; it becomes culture
  only when techniques are learned from others, task choices are coordinated by relationships, and the pattern outlives
  the people who began it (and differs between worlds with similar bodies).
- **What to add, in tiers:** (1) audit reproductive energy costs (pregnancy, milk, infant feeding) and fix only a real
  gap, without double counting; (2) individual body size and strength from overlapping distributions, only where ACL's
  actions have a coherent physical use for force (carrying, digging, striking, fighting); (3) defer mortality, injury,
  aerobic capacity and reproductive ageing.
- **Never add:** task preferences by sex; sex-based bonuses for hunting, crafting, intelligence, bravery or teaching;
  tools or skills by sex; roles for children by sex; rescue bonuses tied to sex ratio; sex-specific mortality without a
  mechanism; calling any labour difference "culture" automatically; tuning to match one ethnography.
- **The two leftovers:** a fixed 20% lower father's love is a hard psychological claim to justify; "carer = mother"
  mixes nursing with all childcare. Audit both.
- **With hunting at ~0.02% of food, strength would barely matter for hunting now.**
- **Honest test (concept, not frozen):** first measure today's v6 by sex (choices per opportunity, output per effort,
  care, age and reproductive state). Then separate arms: C (v6), L (lactation cost), S (strength variation), LS, and a
  sex-neutral strength control. Primary outcome: task choice per opportunity, by sex. Ask: if strength were equal but
  reproduction costs differed, would labour differences emerge?
- **For Bob:** whether bodies and lives produce different individual capabilities and histories, not behaviour by
  assigned sex.

## The assistant's notes (checked in the code)

- **Infant feeding already costs the carer:** each week a carer hands food to dependants from their own food
  (`acl/biology.py` body phase); an infant needs 2 a week. So the mother already pays her infant's food, a rough stand-in
  for milk; a separate lactation cost would partly double count. Pregnancy adds +1.5 a week (`acl/person.py` `need`).
- These are for later, after BD3, M1 and the twins plan. Nothing drafted.
