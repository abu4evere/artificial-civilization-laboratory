# Council round 79: law B, "both parents feed": which form, and how to test it (7 November 2026)

The question: `docs/debate_round79_question_2026-11-07.md`. GPT (main chat; it answered in its "Instant" mode),
Gemini (ACL chat bcb733d3360cc674) and DeepSeek (ACL chat 2552dbba) got the same text. **Each answer is that model's
opinion, not sign-off.**

## Answers

**GPT's opinion, not sign-off.** "Test B1 first, with safeguards against interpreting reduced maternal burden as
improved child welfare."
- (a) **B1 (second feeder)**, with the father on the same tile. "Preserve the existing caregiver, ownership, and
  food-consumption rules." No shared inventories, no automatic kin redistribution. Its caveat: "B1 is the smallest code
  intervention, not necessarily the most general or ethnographically representative household law. It retains the
  mother-first asymmetry."
- (b) Yes, the father's own care gene, with exactly the same formula. Prevent double feeding when the father is
  already the caregiver.
- (c) Two co-primaries:
  - dependent child-weeks with unmet food need, per 1,000;
  - feeding-caused adult short weeks, pooled across grown carers, per 1,000 grown person-weeks.

  The women − men gap should be a secondary: "optimizing the gap could reward equalizing hardship rather than reducing
  it." Child survival to 16 is a secondary; making by women 30–49 is exploratory. Guards: CI1's eight, plus male
  starvation mortality; watch female starvation too. Risk: "B1 may do almost nothing if fathers rarely have food
  available on the child's tile." Record eligibility, food available, offers, feeds and shortages.
- (d) Test now on v16, in parallel with VW1, with separate seeds and a sham. Test the interaction on combined code
  before combining.
- (e) 97% valid and informative; 75% that it raises fathers' feeding; 55% that it reduces child shortfalls without a
  guard raised.

**Gemini's opinion, not sign-off.**
- (a) **B3 (any present grown kin carer with food)** "is the truest minimal general law. It relies on universal
  biological kin selection rather than hardcoding the human construct of a 'nuclear family' or an arbitrary sequence".
  The feeder must be on the same tile.
- (b) Yes, the feeder's own care gene. A different threshold for fathers would be outcome-tuning.
- (c) Co-primary 1: the women − men gap is valid "as long as you are merely observing it rather than writing rules to
  force it to zero". Co-primary 2: child survival to 16. Making by women is "too noisy for a primary metric". Guards:
  CI1's eight plus men's starvation.
- (d) **Wait** for VW1 and test on whatever is live: "Testing Law B in parallel on an older branch will yield
  confounded data, violating your 'one change, frozen test' methodology."
- (e) 95%.

**DeepSeek's opinion, not sign-off.**
- (a) **B2 (shared family pool)**, same tile. "B1 keeps 'mother first, father as fallback' — that writes a role
  priority (culture) into nature." B3 is "the correct later broadening … not the first step". It also says "the give
  action already requires proximity".
- (b) Yes, the father's own care gene, symmetric with the mother's.
- (c) "The gap is not the right co-primary — it is outcome-tuning." Its proposals:
  - primary: dependents' food-shortfall weeks;
  - co-primary: child survival to 16;
  - manipulation check (not gating): the father's food reaching his children rises;
  - descriptive only: the gap, and women 30–49 making.

  Guards: CI1's eight plus men's starvation.
- (d) In parallel on v16; "if VW1 becomes v17, B's confirmatory runs on v17."
- (e) About 76%. Its risk: "if fathers are usually 5–7 tiles away, B2 is inert". Count co-located father–child weeks
  read-only first.

## Checked against the code (Claude)
- **Same tile:** children are moved to their caregiver's tile each week (`world.py`, before the body phase). A father
  can only be counted on the child's tile if he is on the mother's tile.
- **DeepSeek's "give already requires proximity": true.** The giver walks toward the receiver, and the give is done only
  if they end within 1 tile (`actions.py`: `distance(...) > 1: return`).
- **Gemini's "confounded" claim:**
  - a test of B on v16 against v16 changes one thing, so it is not confounded;
  - what it cannot show is B together with VW. GPT and DeepSeek cover that with a test on the combined or live code
    before any adoption.
- **The shared risk** (GPT, DeepSeek): how often is the father on the child's tile with food to spare? A side look (not
  data) is running on two v16 worlds, exploration seeds 26901–26902
  (`experiments/BF1_both_feed/explore/colocation.py`).
