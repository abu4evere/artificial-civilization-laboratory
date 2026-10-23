# LT1 — Teach what the learner lacks: if teachers stop offering what the learner visibly has, are more lessons taken? (Revision 1 after GPT's review; SIGNED OFF 23 October 2026; frozen as `LT1-frozen` before any data)

**Why (the creator: "go with gpt decision", 23 October 2026; `gpt_review_next.md`).**
- LU1: only 6.4% of lessons about useful inventions are taken. 34% of the failed ones teach something the learner
  already has. The teacher offers one of their own three most-valued recipes, chosen without regard to the learner.
- GR2: memory is not the bottleneck; the lesson is.

A **Law 126 study**: one candidate change to nature, tested against v3.

## The candidate (one setting, default = nature v3)

| setting | v3 | candidate | the change |
|---|---|---|---|
| `teach_what_lacks` (T) | 0 | **1** | Before choosing what to show, the teacher sets aside recipes they **can tell** the learner already has: the learner **carries** one of that kind, or the learner **said so** in an earlier lesson from this teacher (a lesson that ended "already known"). The teacher then chooses among the rest by v3's rule (top three by value, one at random). If nothing is left, v3's choice stands. Acceptance, teaching frequency and values do not change. |

**What the teacher remembers:** for each learner, the kinds that learner said they already knew, at most 40 in all
(the oldest goes first). Saved with the world only when held, so v3's worlds are unchanged.

**Why not GPT's exact wording** (the teacher checks the learner's recipes): in ACL nobody reads another's mind. This
version uses only what a teacher could see or be told, so it may catch fewer of the "already known" lessons.

## Design

- **Code:** `code_lt1` = `code_v3` + `teach_what_lacks` (default 0 = v3 exactly) + LU1's read-only lesson logging.
- **Arms:** C (v3) and T. **Seeds: 512 new, 11001–11512** (recommended; GPT suggested 256 to start, but GR1 showed
  256 can give a pass by chance); 20 founders, 120 years; 1,024 worlds on GitHub.
- **Zero checks (hard stops):** setting 0 equals `code_v3` (seeds 11 and 501 at 5 years, 501 and 601 at 20); T acts;
  observers and logging change nothing; reload is exact.
- **Manipulation check (hard stop):** the share of useful lessons ending "already known" falls in T (paired
  Wilcoxon, p < 0.05).
- **Primary (learning), after GPT's review:** each world's **useful recipes learned per person-year**: distinct
  (learner, kind) acquisitions by lesson of kinds that are useful at the end, divided by the world's person-years;
  T − C paired; Wilcoxon; mean difference with a 95% bootstrap interval (10,000, random.Random(2026)).
  **"Changes learning meaningfully"** if p < 0.05 **and** the mean rise is at least **10% of C's mean**;
  "no meaningful effect" if the interval lies inside ±10% of C's mean; otherwise "not shown".
- **Secondary:** the share of lessons about useful inventions that are taken (the draft's primary; GPT showed it can
  rise only because fewer wasted lessons are counted).
- **Safety (as GR2):**
  - passing on (CA1's link 3): T − C, its interval's lower bound above −0.02 ("not worse");
  - time-averaged population: lower bound of T / C − 1 above −0.05 ("safe"), upper bound below −0.05 ("harmful"),
    otherwise "inconclusive";
  - survival: sign test, bootstrap, yardstick ±0.117.
- **Described:** every LU1 outcome share; useful lessons offered and taken per person-year (a big change in
  lessons offered would mean more teaching, not better matching: GPT's caution); repeat acquisitions; the share of taken lessons later made; passing on
  (link 3) as a number; population at years 60 and 120.

## The adoption rule (fixed now, before any data)

`teach_what_lacks` is **adopted into nature (v4)** only if all hold:
1. The manipulation check passes.
2. Learning reads "changes learning meaningfully" with T higher.
3. Passing on is not worse, population is safe, and survival is not worse.

If 1 and 2 hold but a safety reading is inconclusive, it **stays experimental**. Otherwise it is not adopted.

## The assistant's prior

- The manipulation check passes, but the "already known" share falls only from about 34% to about 25%, because a
  teacher sees only what is carried or what they were told.
- **Learning rises a little, but below the 10% bar:** useful recipes learned per person-year up about 5%; the take
  rate from about 6.4% to about 7%. "not_open" is untouched. So most likely **not adopted**.
- **Passing on barely moves** (as GR2: more lessons offered did not mean more learned). Safety: no effect.

## Before freezing (the research rule)

GPT chose the candidate and reviewed this draft (`gpt_review_next.md`). It accepted the perceivable definition, and
asked for a per-person-year primary, a numeric "meaningful" bar and the offered-lessons diagnostic; all are in above.

## Decisions for the creator

1. The candidate as described (the "carries it, or said so" version).
2. Seeds: **512 new** (recommended), or GPT's 256.
3. The adoption rule and the prior, as written.

## Sign-off (23 October 2026)

The creator: "Appove all". So: the candidate as described, 512 new seeds (11001–11512), the 10% bar, the adoption
rule and the prior, as written.

## Operational note (23 October 2026, while building, before any data; rule 19)

How the plan is put into code (`v3_to_lt1.diff`). Nothing else changes.
- **Setting aside:** in `show_how`, after v3 lists the teacher's valued recipes and beliefs, recipes the learner
  carries (an item of that kind) or told this teacher they knew are removed; beliefs are untouched. If nothing is
  left, v3's list stands. Then v3's choice (top three by value, one at random).
- **"Told":** when a lesson ends "already known", the teacher remembers [learner, the kind they meant to show]
  (`told_known`, at most 40, the oldest dropped; no duplicates). Saved with the world only when held.
- **Measures:** "learned" = a lesson ending "taken" whose recipe is a useful kind at the end; distinct (learner,
  kind) pairs per person-year (living person-weeks / 52); repeats counted separately. Lessons logged as in LU1.

