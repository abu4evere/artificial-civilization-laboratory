# G1 — Who receives the food? Questions (written before any data)

**Read-only. No new mechanic, no rule touched.** The creator's question after S1, which found that storage loses mostly
to giving food away (39% of the times stashing was offered and lost). S1 showed that food is given; G1 asks to whom.

**Worlds:** E13R's control (Arm A, A2-full), seeds 501–516, 120 years, replayed with a probe that reads every gift (the
world's own `give` events) and classifies it from the world's state at that moment. The probe must not touch the world
(state hash, 20 years) and every replay must equal the saved E13R run.

## From the code, before any data

- A gift is offered to anyone within reach when the giver holds more than two weeks' food beyond what their dependents
  need. Its pull: the recipient's hunger × (kindness, affection, kinship, partnership), plus the wish to pay back food
  received. A gift moves at most two weeks of the recipient's need.
- Giving rewards the giver at once (0.1 + 0.2 × kindness + 0.2 × kinship); being paid back strengthens the giver's habit
  of giving. Stashing earns no immediate reward.
- A carer feeding their own young dependents is separate (automatic, every week) and is not a gift. Every gift goes to
  someone else.

## The questions

1. **To whom?** Food given, by the recipient's tie to the giver, in this order: partner; the giver's own child (by
   age: infant or child, teen, adult); parent; sibling; other kin; friend (affection 0.3 or more before the gift);
   acquaintance (some familiarity); stranger (none).
2. **To which ages?** By the recipient's stage: infant, child, teen, adult, elder; and whether a child recipient is in
   someone else's care.
3. **To the hungry?** The recipient's food just before the gift, in weeks of their own need.
4. **To the high-status?** The recipient's standing: the respect all living people hold for them, as a percentile among
   living adults.
5. **To the same few?** How concentrated giving is: the share of all food received by the top 10% of recipients; the
   share of each giver's yearly giving that goes to their single main recipient; and how much is repayment.
6. **When?** All of the above by season, especially autumn (when storing would matter) and winter.

## Reading rule

Descriptive; nothing scored. G1 changes nothing in any world.
