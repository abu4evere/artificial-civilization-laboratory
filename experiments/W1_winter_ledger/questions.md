# W1 — Why does food not last through winter? Questions (written before any data)

**Read-only investigation**, chosen by the creator after the E13R autopsy changed the roadmap branch: people go into
winter with more food when they copy the well fed (16 of 16 worlds), and end it with none. What ACL's people lack may
not be getting food but keeping it. W1 asks where winter food goes.

**Worlds:** E13R's Arm A (control, A2-full) and Arm B (copying), seeds 501–516, 120 years, replayed.

**Method:** an instrumented copy of the E13R code that only counts food where it moves inside the body phase (rotting
on people, feeding dependents, eating, rotting in stashes). Everything else (gathering, hunting, stashing, taking,
giving, stealing, inheriting) is read from the world's own events. The instrumented code must reproduce the original
exactly: same state hash after 20 years in both arms, and every replay's population equal to the saved E13R run.

## Q1. The arithmetic ceiling (from the rules alone, no simulation)

An adult eats 7 a week; winter is 13 weeks; loose food rots 4% a week (a quarter as fast near smoke or once fired;
slower under cover in a stash); seeds rot 0.5% a week; one person carries at most 100 food and seed.
- How many weeks does a full load last one adult as loose food, as fired food, as seeds?
- How many weeks for a carer with typical dependents?
- Can any household carry a winter, or must it stash, keep gathering, or both?

## Q2. The winter ledger

For each world and winter, where does food go? **In:** gathered in winter (foraging, hunting), taken from stashes,
inherited. **Out:** eaten, rotted on people, rotted in stashes, given away, stolen, put into stashes, sown, lost at
death. What share of winter eating is covered by food held at the start of winter, and what share by gathering during
winter?

## Q3. Households

For carers with dependents at the start of winter: household stock (carer, dependents and the carer's own stashes)
against the household's winter need. What share of households could cover winter from stock? How does stock compare
with what the household could carry?

## Q4. Rot and seeds

What share of food held at the start of winter rots before it is eaten, on people and in stashes? How much of what
people hold at the start of winter is seed, which keeps?

## Q5. Stashes

How much food is stashed in autumn, how much is in stashes at the start of winter, how much is taken back in winter by
its owner and by others, and how much rots there?

## Q6. Who runs out, and when

For adults and carers: the week of winter they first go short, against the food they held at its start.

## Reading rule

Descriptive; nothing scored. Arm B is reported beside Arm A for contrast, with seed agreement for every pooled
difference. W1 changes nothing in any world.
