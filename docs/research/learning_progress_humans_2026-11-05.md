# Do people choose what to practise by learning progress? (research note, 5 November 2026)

Written while PB2's zero checks ran. PB2's goal arm (G) chooses a goal by **learning progress** (LP): how much the
memory's prediction error on an output fell over the last 26 weeks compared with the 26 before. Is there human
evidence for such a rule? A source suggests; only a frozen study decides.

## Ten, Kaushik, Oudeyer & Gottlieb (2021)
"Humans monitor learning progress in curiosity-driven exploration". *Nature Communications* 12, 5972.
DOI [10.1038/s41467-021-26196-w](https://doi.org/10.1038/s41467-021-26196-w); PMC8514490; PMID 34645800
(volume and page checked in PubMed's record). **Read: full text** (from
PubMed Central, through the PubMed tool), apart from the supplementary material.

**What they did:**
- 382 online participants. 4 activities: guess the food a "monster" likes.
  - Three activities could be learned, at three levels of difficulty.
  - The fourth was **random and could not be learned**.
- 15 forced trials on each activity, then 250 free trials, choosing freely among the 4.
- Two groups:
  - one told to maximise learning, with a test at the end (196 people);
  - one told only to play freely (186 people).
- Percent correct (PC) and its change over time (LP, in 15-trial windows) were used to model each choice.

**What they found** (as reported by the authors):
- Models with an **LP component fit the choices best**.
- **PC and LP were not correlated, and both shaped the choices:**
  - competence (a high error rate) drew people toward hard, unfamiliar activities;
  - LP **steered people away from the unlearnable activity**.
- Without being told to learn, about 65% of the free-play group still mastered more than one activity, and about 30%
  mastered all three. This is spontaneous self-challenge.
- The group told to learn spent more time on the random activity (about 37%). An outside goal made some people "labour
  in vain" on what could not be learned.
- The best learning went with **intermediate** self-challenge (an inverted U).
- The authors' own limit: the activities were simple and quickly mastered. In a world full of hard or unlearnable tasks,
  they expect LP to matter more.

## What it means for ACL (suggestions, not decisions)
1. **PB2's G is built on the same idea as this human evidence.** G's LP is the drop in the memory's prediction error
   over recent windows. That is the same shape as "the change in percent correct", on the person's own experience. It
   is an anchor that the rule is general and human-like, not a researcher's invention.
2. **What G leaves out:** the paper finds that **competence** (error level) also drives choice, independently of LP.
   PB2's goal uses LP only.
   - This is a known difference, recorded here **before PB2's data**. It is not a change to the frozen plan.
   - If G − P is null, an LP + competence goal is one candidate for a later study, in its own frozen plan.
3. **"Unlearnable" outputs exist in ACL:** food from a hunt is very noisy, and affection depends on others. In PB2, LP
   should rarely pick outputs whose errors do not fall. G's goal table (adoptions by output) can be compared with that
   expectation. This is description only.
4. **External goals can mislead:** the paper's warning, that an imposed goal pulls people toward what cannot be learned,
   supports ACL's rule that the creator never writes Bob's goals.
