# D2 — Why do sowers learn failure? Questions (written before any data)

**Read-only. No new mechanic.** The creator's first priority after D1: "Before evidence review, I want to settle whether
sowing's negative learning is already explaining the absence of delayed-return behaviour. If sowing fails because
returns aren't captured, that's a world-level explanation already present in ACL. If sowing is not the explanation,
then N3 becomes the leading path."

## Two things found before any data

1. **Capture, from D1's own numbers.** Sowing returns 2.36 food per unit of seed; the sower and close kin harvest 48%
   of the crop. So the sower's family gets back roughly 1.1 per unit of seed, against the unit of seed given up. For the
   sower's own family, sowing about breaks even. (A rough estimate: it pools D1's harvest shares, which count only
   harvests of one unit or more.)
2. **D1's learning measure was confounded with forgetting.** Every 13 weeks every belief fades by 2% (`prune_placements`),
   about 8% a year. D1 counted a sower's belief as "fell" if it was lower a year after sowing, which includes plain
   fading with no negative lesson at all. D1's "fell in 58%" mixes negative learning with forgetting. D2 separates them;
   D1's write-up will carry a correction once D2 shows how much forgetting accounts for.

## How sowers learn, read from the code

- A sower, and anyone within one tile who sees it (half the time), records a placement: the key (`seeds@season`), the
  spot, and how much the spot stood out then (`contrast` = the spot's plant food and crop against the mean of its eight
  neighbours, plus 5).
- Whenever a person aged six or more arrives on a spot where they left (or saw) something, four or more weeks after they
  last looked, they compare how much it stands out now with how it stood out at placement; a difference of 0.1 or more
  moves their belief by `0.25 × difference`. They may look again and again within the year.
- People also record a placement when they come upon turned earth where someone sowed (`look_at_traces`).
- Other surprises at a spot (taking back a stash, finding it gone) also credit placements made there in the past year.
- Placements are forgotten after a year.

## Method

An instrumented copy of the E13R code that only records: every placement of seed (with the spot's and its neighbours'
food at that moment), every change to a belief about sowing and its source (looking at a spot, another surprise at a
spot, or fading), with what the spot held then and now. It must leave the world byte-identical (state hash, 20 years),
and every replay must equal the saved E13R run. Worlds: E13R's control (Arm A), seeds 501–516.

## The questions

1. **Capture.** For each sowing, the crop that grew on that spot in the following year, and how much of it the sower,
   the sower's close kin, and others harvested. Per unit of seed sown, what did the sower's family get back? In what share
   of sowings did they get back more than the seed?
2. **Where does a sower's change of belief come from?** Over the year after sowing, the change in the sower's belief
   about sowing in that season, split by source: their looks at the spot they sowed; looks at other spots (their own
   other sowings, or spots they saw sown); other surprises; and fading. Which dominates?
3. **What do the looks see?** For each look at a spot one sowed: weeks since sowing; whether the change in standing-out
   came from the spot (its plants or crop fell or rose) or from its neighbours; whether crop was there, not yet grown, or
   grown and harvested in between (and by whom).
4. **Are the lessons right?** Is a look's credit positive when crop actually grew on the spot since sowing, and negative
   when it did not?
5. **Where are spots sown?** How much a spot stood out when it was sown (a spot chosen while rich will tend to stand out
   less later, whatever was sown).

## Reading rule

Descriptive; nothing scored. D2 changes nothing in any world. Its answer decides the creator's next step: if captured
returns or the learning signal explain why sowing stays small, the explanation is already in ACL's world; if not, N3
(a harder lean season) leads.
