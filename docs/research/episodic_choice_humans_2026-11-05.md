# Do people choose by recalling single past episodes? (research note, 5 November 2026)

Written while PB2's zero checks ran. In PB2, a person's choice uses **r-hat**: the mean of the matching lived cell,
or else the 8 most similar weeks of their own memory. That is an episodic rule, not a running average like the habit
table q. Is there human evidence that people choose this way? A source suggests; only a frozen study decides.

## Bornstein, Khaw, Shohamy & Daw (2017)
"Reminders of past choices bias decisions for reward in humans". *Nature Communications* 8, 15958.
DOI [10.1038/ncomms15958](https://doi.org/10.1038/ncomms15958); PMC5490260; PMID 28653668. **Read: full text** (main
text and methods, from PubMed Central through the PubMed tool), not the supplementary material.

**What they did:**
1. **Experiment 1** re-analysed a four-armed bandit task: 20 people, 300 choices, with payoffs that drift. Two models
   were set up alike except for one feature:
   - the standard incremental learner (a running average, like ACL's habit table);
   - a "sampler" that values each option by recalling **one** past outcome of it, more often a recent one.
2. **Experiment 2:** 30 people were recruited and 21 analysed. They made 130 choices between two machines, each
   choice tagged by a unique photograph. 32 memory probes showed an old photograph, about 39 choices back, as a
   reminder of that one episode.

**What they found** (as reported by the authors):
- The sampler fit the choices better than the running average for **all 20** people in experiment 1 (mean log Bayes
  factor about 8.9), and for 19 of 21 in experiment 2.
- After a reminder, the next choice leaned toward what the reminded episode taught. The size was about that of a
  reward received 2–3 choices earlier.
- The authors' view: episodic sampling lets people generalise to new situations from partly similar past experience,
  at the moment of choice.
- **Their open question** is which memories get sampled. They used recency; in structured worlds, similarity on other
  features may matter.
- They expect episodic and incremental (running-average) systems to **coexist**, with their weight shifting by the
  situation.

## What it means for ACL (suggestions, not decisions)
1. **PB2's steering has a human anchor.** Valuing an option from one's own similar past weeks, at the moment of
   choice, is a general ability people show. It is not a researcher's invention.
2. **A recorded difference (before PB2's data):** PB2's memory picks by **similarity** of the situation and gives an
   old week the same weight as a new one. The paper's sampler picks by **recency**. In a world with seasons and aging,
   old weeks may mislead. A recency term is a candidate for a later frozen study, not a change now.
3. **A hybrid:** the authors expect both systems to work together. PB2 replaces q with r-hat wherever r-hat exists
   (council round 61 rejected adding both, since that counts twice with an arbitrary mix). If P fails, a principled
   hybrid is one candidate, for example trusting r-hat more where one's own memory is dense.
4. **The validity check in arm c** (does r-hat predict r better than q?) is the right first gate. The paper shows
   episodic values can fit behaviour better, not that they predict outcomes better in every world.
