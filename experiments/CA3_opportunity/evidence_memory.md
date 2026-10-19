# Human memory for techniques: evidence notes (after CA3; notes only, nothing concluded)

Written 19 October 2026 on GPT's review under the creator's delegation ("Evidence review: human memory for techniques —
APPROVED ... Keep it as a draft"). GPT's standards, kept: small-scale societies first; field observation kept apart from
laboratory work and models; sample sizes and limits recorded; "Do not treat human memory as a fixed number of recipe
slots. Our 12-recipe limit is an ACL implementation choice, not an established fact about human cognition"; and "Don't
infer that ACL's memory limit is the sole cause just because 99% of these inventions were displaced from memory." The
question GPT put first: **what makes useful knowledge persist in a population even when individuals forget it?**

Read-level labels as in `evidence_teaching.md`: **full text** or **abstract/record**.

## What ACL does now (read from the code; fact, not evidence)

Each person holds at most 12 recipes. A new recipe starts valued at 0; when the 13th arrives, the least-valued is
dropped, ties broken by name, so composite names (beginning with a bracket) go first. Useless recipes (value below
−0.15) are forgotten each season. Nothing else decays: a recipe held is held perfectly, and skill (a separate number)
grows only by practice. CA3: 99% of useful inventions lost before any lesson were dropped by the 12-limit within a
season.

## Sources

### 1. Arthur, W., Bennett, W., Stanush, P. L. and McNelly, T. L. (1998). Factors that influence skill decay and retention: a quantitative review and analysis. *Human Performance* 11(1): 57–101. Abstract/record. Laboratory and training studies.
- **Claim / evidence:** meta-analysis of 189 data points from 53 articles. Skill is lost with non-use, from almost
  nothing immediately after training (d ≈ −0.01) to a large loss after more than a year (d ≈ −1.4). Physical, natural
  and speed-based tasks decay less than cognitive, artificial and accuracy-based ones.
- **Limits:** mostly Western training and laboratory settings; skill performance, not knowing that a technique exists.
- **ACL relevance (hypothesis):** forgetting in people is gradual and depends on use and kind of task; ACL has no
  gradual forgetting of recipes at all, only a hard limit and a drop. Memory and skill are separate in ACL, as in this
  literature (knowing how versus doing well).

### 2. Collard, M., Kemery, M. and Banks, S. (2005). Causes of toolkit variation among hunter-gatherers: a test of four competing hypotheses. *Canadian Journal of Archaeology*. Abstract/record. Ethnographic data, 20 societies.
- **Claim / evidence:** toolkit diversity and complexity (counts of tools and of "technounits", Oswalt's measure of
  parts) are best predicted by the risk of resource failure, not by population size, mobility or kind of food.
- **Limits:** 20 populations; toolkit counts, not individual memory.
- **ACL relevance (hypothesis):** how many techniques a people keeps tracks what its environment demands (FX1, FX2):
  a world-side condition. No figure for how many techniques one person can hold was found here.

### 3. Salali, G. D., Chaudhary, N., Thompson, J. et al. (2016). Knowledge-sharing networks in hunter-gatherers and the evolution of cumulative culture. *Current Biology* 26. Abstract/record (and the authors' press summary). Field study, BaYaka (Congo).
- **Claim / evidence:** uses of 33 plants recorded from 219 people in four camps. Medicinal knowledge was shared
  mainly between spouses and relatives; foraging and social knowledge more widely among campmates, related or not.
  Pair bonds, ties between families, marrying out and moving between camps link unrelated families and spread
  knowledge.
- **Limits:** knowledge of plant uses (declarative), not crafts; one people.
- **ACL relevance (hypothesis), GPT's first question:** knowledge persists in a population when it is **held by many
  people, spread through many kinds of ties**; no one person needs to hold it all. In ACL, CA3 found 80% of inventions
  that never spread were held by one child for a season.

### 4. Reyes-García, V. and colleagues (2003–2007), Tsimane' (Bolivian Amazon). Abstract/record. Field studies.
- **Claim / evidence:** ethnobotanical knowledge is widely shared among Tsimane' adults and relates to parents'
  (vertical) and, even more, older generations' (oblique) knowledge; children learn much in peer groups away from
  adults; mothers' plant knowledge is associated with better child health (PNAS 2007: 330 children aged 2–10).
- **Limits:** horticulturalist-foragers; declarative knowledge; association, not cause.
- **ACL relevance (hypothesis):** knowledge comes from many directions (parents, elders, peers); ACL's teaching is one
  told recipe per talk, from whoever talks.

### 5. Strimling, P., Enquist, M. and Eriksson, K. (2009). Repeated learning makes cultural evolution unique. *PNAS* 106(33): 13870–13874. Abstract/record. Model.
- **Claim:** because people can learn (and drop) cultural traits many times in a life, cultural traits can spread fast
  and also vanish fast; repeated exposure matters to what persists.
- **Limits:** model; abstract only.
- **ACL relevance (hypothesis):** in ACL a dropped recipe returns only if someone teaches or rediscovers it; repeated
  exposure to the same technique (seeing it made, hearing it again) has no effect on keeping it.

### 6. From `evidence_teaching.md` (already noted there)
- **Lew-Levy et al. (2017), full text:** children meet techniques repeatedly over years (toy tools, play, sub-tasks,
  apprenticeship); mastery of complex skills takes decades.
- **Morgan et al. (2015), full text:** reverse engineering from finished pieces recovers little of a technique;
  teaching recovers more but still decays along chains.
- **Caldwell et al. (2017/18), full text:** for simple techniques, the finished product alone is enough to reconstruct
  them; for complex ones it is not.

## Across the sources, by GPT's four questions (notes, not conclusions)

- **Capacity.** No source gave a number of distinct techniques one person can hold, and none treats memory as a fixed
  set of slots. People's toolkits vary with what their environment demands (2). **Gap:** a measured count of crafts an
  individual forager knows was not found in this pass.
- **Retention.** Forgetting is gradual and depends on use and kind of task (1); knowing that something exists and
  being able to do it are separate (1, 6). ACL: perfect memory up to 12, then a sudden drop of the least-valued.
- **Reconstruction.** Simple techniques can be rebuilt from finished things; complex ones mostly cannot without
  teaching (6: Caldwell, Morgan).
- **Social persistence.** Knowledge lasts in a people when many hold it through many ties (3, 4), and learners meet it
  repeatedly (5, 6). The individual's memory is not where a people's knowledge mainly lives.

## For the proposal (GPT's design sketch; to be weighed by the creator; nothing adopted)

- **Hypothesis A (memory):** inventions vanish because inventors lose them before passing them on. In ACL that loss is
  produced by a rule (a hard 12-limit, new things valued at zero, composites dropped first by name order) that no
  source supports in that form. GPT: "The memory intervention should first address the composite-name tie-break."
- **Hypothesis B (prerequisites):** composites cannot be followed by learners who lack the parts (CA3: 1 talk in 12);
  living learners meet parts first.
- **Hypothesis C:** both, and fixing one alone may not be enough.
