# Research note: from whom do forager children learn, and when? (1 November 2026)

**For the open question:** UV1 found that ACL's children are the most under-valued habit learners, and UV3 asks
whether values climb across generations. In ACL, a child's habit values come from:
- **its parents at birth:** half their mean (`acl/biology.py` line 553);
- **its one carer through childhood:** an 8% pull each week (`_upbringing`, under 12).

**Is that how forager children come by what they value?** A source suggests; only a frozen study decides.

## What was read (labels per CLAUDE.md)
**Hewlett, B. S., Fouts, H. N., Boyette, A. H. & Hewlett, B. L. (2011).** "Social learning among Congo Basin
hunter–gatherers." *Philosophical Transactions of the Royal Society B* 366: 1168–1178 (doi 10.1098/rstb.2010.0373;
PubMed 21357239; PMC3049106). **Read: the abstract only** (on PubMed). The full text (PMC) was not read.
- Aka and Bofi foragers of Central Africa; behavioural observations and interviews.
- "Hunter-gatherer social learning occurred early, was relatively rapid, **primarily vertical under age 5 and oblique
  and horizontal between the ages of 6 and 12**."
- Teaching existed "as early as 12 months of age", but was "relatively infrequent by comparison to other processes of
  social learning such as observation and imitation".
- It notes that the earlier literature suggested hunter-gatherer learning is "primarily vertical (parent-to-child)".
  This study qualifies that.

**Seen but not read:** Gallois et al. (2018, *Human Nature*), on Baka children. Its machine-written summary on Semantic
Scholar says horizontal transmission "appears to be the most common" in middle childhood. That is a tool's summary,
not the paper, so it is **not stated here as a finding**.

## Bearing on ACL (suggestions only; not proposals)
- **ACL's value transmission is vertical through all of childhood:** the parents at birth, then one carer to age 12.
  In the Aka and Bofi, learning turns oblique and horizontal (other adults, other children) from about age 6.
- **This may matter for UV1's finding.** Children's values are pulled toward one adult's values, in situations that
  adult rarely updates. In forager children's real lives, those values would come from many people, including other
  children who live in the same situations.
- **Any change here would be a nature change** (how children's habits are pulled, and by whom). It would need a frozen
  study, debated first, with no target outcome. The full text should be read first: who children learn *what* from, by
  age.

## Addendum (1 November 2026, evening): the full text, section 4(a)
**Read now (PMC3049106):** section 4(a), "Modes of transmission: from whom do hunter–gatherer children learn?", with
Table 2. Sections 1–3, 4(b) and 5 were not read.
- **Parents stay the largest single source.**
  - Foragers "say that parents as a category provide more cultural transmission than any other similar category".
  - Boyette asked 39 Aka children aged 5–18 who taught them to share food. They named mothers 60% of the time,
    fathers 27%, other kin 20% and non-family 3% (more than one could be named).
  - Often the same-sex parent was named: girls named mothers 84% of the time, and boys named fathers 65%.
- **Others matter early.** From 3–4 years of age, children "were interacting with others just as frequently as
  parents" (Table 2). In infancy, others were more likely than parents to play with the child.
- **Middle and late childhood:** "children spend most of the day in multi-aged child groups" and "frequently observed
  and imitated/emulated other children's behaviour". Step-parent households add oblique learning: 42.4% of 11–15 year
  olds do not live with both biological parents.
- **Public against private knowledge:** among the Baka (Hattori, as cited), plants used for food or material culture
  showed 80–95% agreement between informants, but medicinal plants only 25–30%. The authors suggest that public
  knowledge is shaped by more than parents.
- "The roles of 'others' … are poorly understood and probably underestimated."

**Revised bearing (a suggestion only):**
- ACL's vertical pull (both parents at birth, one carer through childhood) is close to what foragers say about
  **parents**.
- What it lacks:
  - the other children of the same age group;
  - the other adults from about age 3–4;
  - perhaps the "public" domains, such as foraging and making, where many people's ways are seen.
- **A law to test would add, not replace.** Children would also be pulled, more weakly, toward the people they spend
  their days with. It would be frozen and debated first, with no target outcome.

## Correction (2 November 2026): how learned values pass between people
Two statements here were wrong, and they also went into other records and into questions put to GPT and Gemini.
1. **The carer pull runs every 4 weeks, not every week.**
   - `acl/biology.py` calls `_upbringing` when `tick % 4 == 0`: 8% about 13 times a year.
   - About a third (0.92^13 ≈ 0.34) of a newborn's starting difference is still there at age one, when habit learning
     begins. It is nearly gone by twelve if the carer stays near.
   - Per week, the pull is about 2%; a child's own learning step is 5% on the habit being updated, while the pull moves
     every entry. So "the pull is stronger than the child's own learning" does not hold as stated.
2. **Values do not pass only from parents and one carer.**
   - In every conversation, the listener also moves part of the way toward the speaker's **whole** habit table, if
     they respect the speaker or the speaker seems happier (`acl/actions.py`, `_imitate`; rate 0.05 × (0.5 +
     curiosity) × (0.5 + respect)).
   - So learning values from other adults and from peers (oblique and horizontal) **already exists in ACL**, at any
     age.
3. **What this changes here:** the bearing above ("ACL's value transmission is vertical through all of
   childhood") is wrong. ACL already has oblique and horizontal value transmission through talk. Whether children
   should learn values from the people they spend their days with is therefore partly answered by the existing law;
   the open question becomes how strong each channel is.
