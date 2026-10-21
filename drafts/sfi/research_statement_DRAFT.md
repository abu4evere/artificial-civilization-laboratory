# SFI UCR research statement — DRAFT (the creator edits and submits; one page)

SFI asks for one page with three research ideas, each showing a clear question, a plausible path, and why the path fits
the question (UCR "Applying" page, read 21 October 2026). Draft below, about 480 words; numbers from ACL's findings
files. Edit freely: it must sound like you.

---

**Research statement — Abdurashid Khudoyberdiev**

For the past several months I have been building the Artificial Civilization Laboratory (ACL), an agent-based model of
hunter-gatherers in which nature is programmed and culture is not: agents have bodies, needs, kinship and materials to
work with, but no list of inventions, no reward for inventing, and no language model. I run it as controlled
experiments, with predictions frozen before each run and hundreds of simulated worlds compared side by side. Three
questions from that work are ones I would like to pursue.

**1. Why doesn't knowledge accumulate?** In ACL, agents invent useful things early, but only about one in ten useful
inventions is ever learned by anyone except its inventor; many are forgotten within a season because memory is limited.
I want to understand how cumulative culture depends on two things together: how much individuals can hold, and how many
learners they meet. *Approach:* vary memory capacity and group connectivity in a simple transmission model (and in
ACL), and measure the longest chain of inventions built on inventions that survives. *Why it fits:* theory and data
(e.g. Henrich's Tasmania argument; Kline and Boyd on population size and tool complexity in Oceania) link population
to cultural complexity, but the role of individual memory is less explored; a model where both can be varied
separately can show whether they trade off or compound.

**2. Why doesn't more contact help people find partners?** When I split the same 80 founders into smaller bands, couples
across lineages rose from about 6% to 54%, yet the share of time women spent without a partner did not change. I want
to know whether the limit is meeting, eligibility (age, kinship) or demography. *Approach:* build the contact network
from simulation runs and ask, for each unpartnered person, whether any eligible partner was reachable, and through
which links; compare network properties with published hunter-gatherer contact data (e.g. Hill et al. on inter-band
interaction). *Why it fits:* treating partner finding as reachability on a changing network separates "too few
encounters" from "no eligible partner exists", which averages cannot.

**3. How can we tell whether culture emerged or was built in?** Many artificial-society models, especially those using
language models, show agents forming norms and institutions, but it is hard to tell discovery from recall. I would like
to develop simple measures of emergence for agent societies: whether a shared practice outlives the individuals who
started it, whether it spreads beyond kin, and whether it carries information that no single agent's programming
contains. *Approach:* define the measures, test them on cases where the answer is known (practices deliberately
programmed in versus ones that arose), then apply them to ACL. *Why it fits:* a measure is only trustworthy if it
correctly separates known cases first, and ACL's exact replay allows the same world to be run with and without a
practice built in.

Code and all experiment records: github.com/abu4evere/artificial-civilization-laboratory
