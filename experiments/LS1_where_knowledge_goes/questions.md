# LS1 — Where does knowledge go? A study of loss over a thousand years (DRAFT, Revision 1, 25 October 2026; not frozen; waiting for the creator)

**Why.** M1 (`../M1_millennium_v6/findings.md`, final, independently recomputed) found that over 1,000 years nothing
builds. Every surviving world erodes:
- food owed to tools falls 95%;
- crafting skill falls to a tenth;
- unique recipes fall to an eighth;
- deliberate making falls 96%;
- no new kind made after year 100 lasted.

M1's frozen rule for this result: "a study of loss (where retention breaks, with CA1–CA3's methods), not a longer run".
The creator chose this study first (25 October 2026). It is read-only and changes nothing.

**Known, and not known.** Earlier studies on older natures found:
- making was never competitive, even for founders (E8.1);
- tools seemed worth little (E8.2);
- most inventions are pushed out of a 12-recipe memory within a season (CA3);
- one in ten is ever passed on (CA1).

No study has followed **the flow over centuries**: what enters and leaves the stock of know-how, skill and tools, by
which channel and when, and **whether each generation reproduces what it inherits** or only uses up what it was
given. That last question matters most for the mission: a cumulative mind needs a process by which people acquire,
use, pass on and sometimes improve what earlier people found.

**From the code (v7).**
- Founders start with skills of 0.2–0.4; every child starts at 0.
- Skill grows only by practice and never decays, so a falling population skill means less practice, cohort
  replacement or selective death, not forgetting.
- A person holds at most 12 recipes; the least valued are pushed out, and useless ones are forgotten.
- Habits move toward a carer's (upbringing) and toward what others say (talk).
- **A forage act owes food to a tool by an exact identity.** With `got` the food gained and `f` the tool's forage
  factor, it owes got × (1 − 1/f) when f > 1, and nothing otherwise. So A4 = (share of acts with f > 1) × (food per
  tool act) × (the tool's share of that food), exactly.

## Design

- **Read-only: live nature v7 plus a logging observer.** It changes nothing; zero checks prove it.
- **Primary: LP**, M1's setting: 80 founders on 80 × 80, 1,000 years, 64 new seeds (18001–18064).
- **Secondary, described:** D80 (80 founders on 40 × 40), 32 new seeds (18101–18132), to see whether a mechanism is
  peculiar to LP.
- No arm changes nature. A world where founders start with no skill would answer a different question; it may follow
  if these results call for it.
- M1's A4 and B-retained are recomputed by M1's rules first, as a check that the erosion is the same on v7.

**Time bins:** years 0–5, 5–10, 10–20, 20–50, 50–100, then each century to 1,000. A collapse in years 5–20 must not
hide inside a century.

**Survivorship and population:**
- Every bin is read over the worlds alive at its start. Worlds that die out are reported with the year and treated as
  ended, never as holding zero knowledge.
- Population, adults, age structure, cohort sizes and density are reported by decade.
- Rates are per capita and per exposure (per person-year, per held recipe-year) beside raw counts.
- **If fewer than 20 LP worlds are alive at year 1,000, late readings are marked "thin"; no reading is drawn from a
  bin with fewer than 10 alive worlds.**

## Logged (read-only observer)

**A. The ledger of holdings.** Every change to any person's recipes, with its route:
- **gained:** invented, taught, watched, other;
- **lost:** pushed out by the 12-recipe limit, forgotten as useless, or the holder died.

Founders' starting holdings are the opening stock. Re-acquiring a held recipe changes nothing.

For every kind (recipe signature):
- first maker (founder or world-born) and generation;
- every holder (ids, generations, ages);
- when it vanished (no living holder) and the last channel.

**B. Teaching.** Every teaching opportunity and lesson:
- teacher and learner (ages, cohorts, relation: parent, carer, other kin, other);
- the recipe;
- whether taken;
- whether the learner later made it or passed it on.

**C. The making funnel.** For each person-week:
- **feasible:** knows a recipe and holds or can reach its materials;
- **weighed:** making was among the options scored;
- **chosen;**
- when weighed and not chosen: what won, and the score gap.

Logged by bin, age band (children 6–15 apart, as play-making) and cohort. Practice weeks and crafting skill at 16
and 30.

**D. Tools.** Each forage act: the tool's factor, food got, and origin (made by the holder, given, taken from a body,
or held since the founding decades). Tool lifecycles: made, transferred, worn out.

**Replacement:** the holder makes or receives a forage tool with f > 1 within 52 weeks after their last one wore out.

**E. Habits (described).** Each person's habit value for making at 16 and 30, beside their carer's and their talk
partners'.

## Primary questions (each by time bin, intervals from a world bootstrap that keeps whole worlds)

**Q1, the ledger: copy loss and kind extinction, separately.**
- By bin: person-recipe inflow by route and outflow by channel, per capita and per held recipe-year.
- **The dominant copy-loss channel** after year 100.
- **The dominant kind-extinction channel** (the last holder's loss) after year 100.
- The bin in which net flow first turns negative and stays negative.

**Q2, origin, transmission, persistence** (three measures, no single verdict). For useful kinds (forage or any
factor > 1), by origin (founder or world-born) and era of first making:
- **transmission:** the share ever held by two or more people;
- **persistence:** the share still held 25 years after the maker's death, and the share ever held by someone two or
  more generations after the maker;
- **descriptive:** the founder share of useful know-how held in years 0–100.

**Q3, the making funnel.** Rates by bin:
- feasible per adult person-week;
- weighed given feasible;
- chosen given weighed;
- and the unconditional chosen rate.

**The decline decomposition, frozen.** From years 0–10 to years 100–200 (and to each later bin, described):
Δ ln(chosen) = Δ ln(feasible) + Δ ln(weighed | feasible) + Δ ln(chosen | weighed), from pooled counts. The share of the
decline carried by each term is reported with its interval. **The gate carrying the largest share** is named. If a term
falls to zero, that gate is named and marked "fell to zero".

**Q4, the fall in A4, exactly.** A4 = s × g × k, where:
- s = the share of adult forage acts with f > 1;
- g = the food per such act;
- k = the share of that food owed to the tool.

Δ ln A4 from decades 2–4 to decades 95–99 is split into the three terms, with intervals. Also:
- the share of tools held in decades 2–4 made by their holder, against held since the founding decades;
- the replacement rate by bin.

**Q5, does each generation replace what it inherits?** Per birth cohort (50-year bands):
- **The inheritance rate:** of the useful recipes held by a child's carers while the child was 0–16, the share the
  child ever acquired (by 30), by route and by relation.
- Useful recipes acquired by 16 and by 30, by route.
- **Use:** the share of acquired recipes the person ever made.
- **Onward:** the share they passed to someone younger.
- **Survival:** the share outliving them by 25 years.
- **New knowledge:** world-born inventions entering a later generation.

## Validity (hard stops)

- **Zero checks:**
  - the observer is read-only: state and random numbers identical with and without it, at 20 and at 100 years, LP and
    D80;
  - reload is exact.
- **The ledger balances in every world:**
  - holdings at the end of every decade = start + inflow − outflow, exactly;
  - over the whole run;
  - **the kind count rebuilt from holdings equals the observer's kind record** at every decade boundary;
  - **the observer's holdings equal every living person's actual recipes** at every century boundary.
  Every mismatch count must be 0.
- All worlds are present, under one fingerprint (`code_v7`).
- **An independent recompute** of the Q1 dominant channels, Q3's decomposition, Q4's split and Q5's inheritance rate,
  from the raw files, before the findings are final (CLAUDE.md).

## What would follow (stated now; not exclusive, several can apply)

- **Q5's inheritance rate is low and Q3's largest share is "weighed" or "chosen":** each generation does not take up or
  use what its carers knew. Next: an evidence review of how forager children come to make and use tools
  (apprenticeship, necessity, worth), before any change to nature.
- **Copy loss is mostly push-out:** memory is a leak. Next: revisit memory, mindful of MR1 (keeping by use cut
  transmission).
- **Kind extinction is mostly death:** knowledge is not passed on before the holder dies. Next: transmission (CA1's
  bottleneck).
- **Q4's fall is carried by s:** tools are not remade or replaced. The tool lifecycle is the leak.
- Whatever leads, the timing (which bin first) is reported, since an early failure may cause later ones.

## The assistant's prior (separate predictions)

1. Net flow turns negative within years 0–50 and stays negative.
2. The dominant copy-loss channel after year 100 is death or push-out. The assistant cannot rank them: if acquisition
   collapses, death may lead. Kind extinction after year 100 is mostly death of the last holder.
3. Useful founder-origin kinds are transmitted more often than world-born ones; persistence across two or more
   generations is rare (under 10%) for both.
4. In the decomposition, "weighed given feasible" carries the largest share of the fall in making.
5. A4's fall is carried mainly by s, the share of forage acts with a tool.
6. The inheritance rate is low (under 20%) from the first cohort on, and does not rise.
7. Several bottlenecks act in sequence: early, making stops being weighed; then skill and tools fall; then fewer
   chances to learn.

## Revision 1 (25 October 2026, before any code or data)

After GPT's review (`gpt_review_ls1.md`):
- copy loss and kind extinction are separate;
- Q2 is origin, transmission and persistence, with no endowment verdict;
- Q3 uses conditional rates and an exact log decomposition instead of a "first gate" rule;
- Q4 uses the exact A4 identity from the code;
- **Q5, intergenerational replacement, is added;**
- teaching, childhood making, population, age, density and survivorship rules are added;
- a few-survivors rule is added;
- the ledger checks are strengthened (kind count, state reconstruction);
- D80 is added as a small secondary setting;
- the prior is restated as separate predictions;
- the "what follows" branches are not exclusive;
- no zero-skill-founder arm (a later question).
