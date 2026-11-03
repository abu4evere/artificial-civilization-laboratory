# Debate round 50: AF1, opening what made things can do (2 November 2026)

**Why:** the creator asked to stop restricting what inventions can do ("we should give them all possibilities"),
after the audits `docs/affordance_audit_2026-11-02.md` and `docs/action_audit_2026-11-02.md`. The creator approved
step 1 ("go ahead").

**What was asked:** `research/local/round50_af1.txt`, a five-arm test in a copy:
- **v11**;
- **S, "make by what it does":** a recipe's part or binder may be replaced by anything held whose 10 properties are each
  within D = 10;
- **K, "containers contain":** the best container's factor multiplies the made-thing and material limits, as it
  already does for food;
- **S+K;**
- **a sham.**
- **Who:** GPT (chat `6ae9421b`) and Gemini (chat `d5ecc8b87be7ae89`).
- **Each answer is an opinion, not a sign-off.**

## First answers
- **GPT, 85%:**
  - "AF1 is a sound next experiment, but the primary measure needs one important safeguard."
  - Freeze D = 10, with 5 and 20 as sensitivity checks.
  - Keep all five arms (a 2 × 2 design plus a sham).
  - Containers count toward their own limit, with no recursive multiplying.
  - Leave storage and shelter for a separate study.
  - **Its main risk is measurement:** two things invented apart could look alike, so a functional measure could report
    remaking where no knowledge survived. And "the same D = 10 tolerance appears in both the intervention and the
    outcome", which could favour S by definition. It asks for a lineage measure, and that one make not count for
    several inventions.
- **Gemini, 90%:**
  - The design is valid, D = 10 is sensible, keep the arms, and leave the third rule for later.
  - **Its risks:** "property drift" (substituted parts becoming the next template), and coincidental matches with
    forgotten things.

## The change, and second answers
- **The change (the assistant):** the lineage measure becomes primary. An invention counts as made again when **its
  own remembered recipe** is chosen by a "make" action, by anyone who knows it, with any parts the arm allows.
  - The functional measure is secondary: one make counts for at most one kind, the nearest; D = 5, 10 and 20 are
    checked.
  - Substitution never rewrites the remembered recipe, so the template cannot drift.
- **GPT, 85% → 93%:** "Making recipe-lineage remaking the primary outcome is the right decision." Its safeguards:
  1. track recipe identity apart from product identity;
  2. count only deliberate recipe choices;
  3. report how many eligible inventions remain known to someone during the five years, to tell knowledge loss from
     inability to remake.
- **Gemini, 90% → 95%:** "The changes are exactly right." The one-to-one mapping and the locked template remove
  multi-counting and drift.

## Outcome
Freeze AF1 with:
- the five arms;
- D = 10 for rule S;
- the lineage primary (GPT's rule: intervals above 0 against both v11 and the sham, and at least 1 percentage point);
- the functional secondary at D = 5, 10, 20;
- recipe availability reported;
- guards on population and extinctions;
- the third rule (storage and shelter) left for a later study.

Both chat tabs were closed afterwards.
