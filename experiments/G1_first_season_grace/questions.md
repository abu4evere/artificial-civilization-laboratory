# G1 — A first season of grace: if new inventions cannot be pushed out at once, are more of them taught? (Revision 1 after GPT's review; SIGNED OFF 22 October 2026; frozen as `G1-frozen` before any data)

**Why (the creator chose option (a) after MR1, 22 October 2026).**
- CA3: 99% of inventions lost before any lesson were pushed out of their inventor's memory by the 12-recipe limit
  within a season. A new recipe starts valued at 0, so it is the first to go when a 13th arrives.
- MR1: replacing the limit with "forgotten after 2 years unused" kept new inventions through their first season
  (held at 13 weeks: 55% → 100%), but people then held far fewer things (8.8 → 2.3), and **fewer were passed on
  (−3.3 points)**. v3's memory is too short at the start and long afterwards: whatever survives the first season is
  kept for life.

G1 changes only the start. It is a **Law 126 study**: one candidate change to nature, tested like LX1 and MR1.
Nothing is adopted by G1 itself.

## The candidate (one setting, default = nature v3)

| setting | v3 | candidate | the change |
|---|---|---|---|
| `first_season_grace` (G) | 0 | **1** | When a 13th recipe arrives, a recipe **first held less than 13 weeks ago** (learned or invented) cannot be the one dropped; the lowest-valued older recipe goes instead (v3's tie rule). If all are under 13 weeks old, v3's rule applies unchanged. Nothing else changes: the 12 limit, forgetting the useless, lifelong keeping. |

**Why 13 weeks:** one season, the span in which CA3 found the losses. It is a stand-in, chosen before data and never
retuned. **It is exploratory, not measured** in ACL's units.

**The cost it may carry:** protecting new things means an older recipe is dropped instead, possibly a useful one.
This is measured (below), not assumed away.

## Design (the assistant's recommendation; decisions marked)

- **Code:** `code_g1` = `code_v3` + `first_season_grace` (default 0 = v3 exactly). "First held" is stored per person
  (saved only when held, so v3's worlds are unchanged).
- **Arms:** C (v3) and G. **Seeds: 256 new, 9501–9756**; 20 founders, 120 years; 512 worlds on GitHub.
- **Zero checks (hard stops):** setting 0 equals `code_v3` (seeds 11 and 501 at 5 years, 501 and 601 at 20 years);
  G acts; observers change nothing; reload is exact.
- **Manipulation check (hard stop):** in G, the share of new useful inventions still held by their inventor 13 weeks
  later rises against C (paired Wilcoxon, p < 0.05).
- **Primary (transmission):** CA1's link 3, the share of useful inventions ever learned by someone else, G against C,
  paired. Wilcoxon, mean difference with a 95% bootstrap interval. Readings as MR1: "changes transmission",
  "no meaningful effect" (interval inside ±0.02), "not shown".
- **Survival check (as LX1):** extinction, G against C, paired sign test, bootstrap, yardstick ±0.117.
- **Described:** as MR1 (recipes held per person; weeks an invention stays with its inventor; built on by a learner;
  longest chain; children's inventions passed on), plus, after GPT's review:
  - **the displacement cost:** drops where grace protected a new recipe and an older one went instead; how many of
    those older ones were valued above 0.15 (teachable), and how many were useful kinds;
  - **the fallback:** drops where every held recipe was under 13 weeks old, so v3's rule dropped a new one;
  - **the transmission pathway** for useful inventions: held at 13 weeks → ever used again by the inventor → ever
    valued above 0.15 by the inventor → ever offered in a lesson → ever learned by someone else. This tells failure at
    the memory stage from failure at the teaching stage.

## The adoption rule (fixed now, before any data)

G may be **proposed for adoption into nature (v4)** only if all of these hold:
1. The manipulation check passes.
2. Transmission reads "changes transmission" with G higher.
3. Survival is not worse ("no meaningful effect", or fewer worlds dying out).
4. The creator accepts the evidence.

## The assistant's prior (to be frozen at sign-off)

- The manipulation check passes: new inventions are held through their first season.
- **Transmission rises a little (about 1–2 points on about 11%).** A protected invention still has to be used and
  valued above 0.15 before anyone is taught it, and most are not used in their first season.
- More teachable recipes are dropped than in C, but few.
- Survival: no meaningful effect.

## Before freezing (the research rule)

GPT was asked (22 October 2026; `gpt_review_g1.md`, labelled as GPT). It supports running G1 as designed and
asked for the displacement, fallback and pathway measures, now added above as described measures. It changes no
test. It named **V1, a small positive starting value (below 0.15)**, as the next candidate if G1 fails, and advised
against combining the two.

## Decisions for the creator

1. The candidate: **first-season grace, 13 weeks** (recommended), as described.
2. Seeds: **256 new (9501–9756)** (recommended), or 512.
3. The adoption rule and the prior, as written.

## Sign-off (22 October 2026)

The creator: "approve all and run it on github". So:
- the candidate, first-season grace, 13 weeks;
- 256 new seeds (9501–9756), two arms, 512 worlds on GitHub;
- the adoption rule and the prior, as written.

## Operational note (22 October 2026, while building, before any data; rule 19)

How the plan is put into code (`v3_to_g1.diff`). Nothing else changes.
- **"First held"** is kept per person (`recipe_got`, the week a recipe was first held), only while under 13 weeks
  and only with grace on; saved with the world only when held, so v3's worlds are unchanged. A recipe counts as new
  when it enters memory by any route (made, taught, copied, read, heated).
- **The drop:** when a 13th recipe arrives, v3 picks the lowest-valued (ties by name). With grace, the same rule
  picks among recipes not first held in the last 13 weeks; if there are none, v3's pick stands ("fallback").
- **Logging** (`world.g1log`, not saved; read by nothing in the world): each full-memory drop (week, person, recipe,
  its value, and whether it was v3's pick, a displaced older one, the same as v3's, or a fallback), and each lesson
  offered (week, teacher, recipe). Observers and logging change nothing (zero checks).
- **The pathway** counts, for each useful invention, five steps separately (not nested): held at 13 weeks; made again
  by the inventor (a "make" event); valued above 0.15 by the inventor while holding it; offered in any lesson;
  learned by someone else (CA1's link 3).

