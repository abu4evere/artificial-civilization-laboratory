# P1 — Does the family network pool risk, or only spread scarcity? Questions (written before any data)

**Read-only. No new mechanic, no rule touched.** The creator's question after G1, which found that given food goes
mostly to family (72%), to the hungry (63%), and half as repayment: "Does the family network function as effective risk
pooling, or is it only spreading scarcity?"

**What read-only can and cannot settle.** Without switching sharing off, nothing here can show what winter would be
like without it. What the record can show are the signatures that tell the two apart:

- **Pooling:** a person's winter fate depends on their family's food, not only their own; hungry people receive food;
  people rarely starve while their close kin hold plenty; giving does not push the giver into hunger.
- **Spreading scarcity:** fate depends on the family's total food alone, whoever holds it; the starving have kin who
  are just as empty; giving pushes givers short; sharing moves who goes short, not how many.

**Worlds:** E13R's Arm A (control) and Arm B (copying, which gives 40% more food away in winter: a natural difference
in how much is shared), seeds 501–516, replayed with a read-only probe (state hash, 20 years; every replay equal to the
saved E13R run).

**Family:** a person's close kin who are alive: kinship 0.5 or more (parents, children, siblings, grandparents and
grandchildren) and their partner.

## The questions

1. **Does family food protect, beyond one's own?** At the start of winter, every person's own food (in weeks of their
   need) and their family's food per head (in weeks of the family's need). Going short during winter and starving to
   death in winter, by own band × family band. Pooling: within the same own band, more family food means a better
   winter.
2. **Do people starve amid plenty?** For every winter starvation death: what the dead person's close kin held at that
   moment (in total, and whether any one of them within sight held two weeks or more of their own need), and whether
   the dead had received any gift in the four weeks before.
3. **Does help reach the hungry in time?** For adults going short in a winter week: how often they receive a gift that
   week; and, by their food band, how often they die within four weeks, with and without a gift.
   *(Amended before any data, after a smoke test: someone fed in a week has eaten and is no longer short by its end,
   so "a gift that week" is always zero. Help is looked for in the two weeks after a short week instead.)*
4. **What does giving cost the giver?** For adults in winter weeks, by food band: how often they go short within the
   next four weeks, in weeks they gave food away and weeks they did not.
5. **More sharing, better winters?** All of the above in Arm B against Arm A.

## Reading rule

Descriptive; nothing scored; associations, not causes. P1 changes nothing in any world.
