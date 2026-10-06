# Zenodo deposit: fields to paste (prepared October 2026; the creator uploads)

Two records. **Access for both: Restricted** (metadata and DOI public; files released only to people the creator
approves), matching LICENSE (all rights reserved). Everything below is stated as findings inside ACL, not claims about
real human history. F2 is filled in; only the upload date in [square brackets] is left for the creator.

---

## Record 1 (new upload): the book

**Resource type:** Publication → Book
**Title:** The World That Nobody Wrote
**Additional title (subtitle):** How we tried to build a civilization instead of simulating one
**Creator:** Khudoyberdiev, Abdurashid
**Publication date:** [date of upload]
**Version:** v1 (96 chapters, October 2026)
**Language:** English
**Access:** Restricted. **Licence:** none granted (all rights reserved; if the form requires a choice, select the
closest "all rights reserved / not open" option, and keep the sentence at the end of the description).
**Keywords:** artificial life; cultural evolution; agent-based simulation; emergence; hunter-gatherers; demography;
pre-registration; research methods
**File:** `The_World_That_Nobody_Wrote_v1.pdf`
**Related works:** *documents* → the software record "Artificial Civilization Laboratory (ACL)" (its concept DOI)

**Description:**

> *The World That Nobody Wrote* is the living history of the Artificial Civilization Laboratory (ACL), a computer
> world built on one rule: nature is programmed, culture is written by nobody. ACL's people have bodies, needs,
> seasons, families and minds, but no scripted customs, plans or institutions; whatever culture appears must arise
> unaided.
>
> The book records how the project came to be what it is: its founding questions and philosophy; the debates that
> shaped each design; and, experiment by experiment, what was predicted, what happened and what was learned,
> including the failures, stops and corrections. Every experiment was pre-registered and frozen before it ran,
> controlled with the same random seeds, and read in a fixed order; negative results and corrections are kept, not
> rewritten. It covers over forty studies, from the first traditions and stories, through the long search for why
> ACL's people do not prepare for winter, to the discovery that a third of ACL's worlds die out not from hunger but
> because, in a small and scattered people, partners are rarely found , and a test showing that perfect partner finding saves most of
> them, while the smallest still run out of partners.
>
> The findings are findings inside ACL. They show what happens in this simulated world under the stated rules; they
> are not claims about how human history happened, though the book compares them with the evidence on real foragers
> where it can.
>
> The book is kept as a living document and will be updated in new versions as the work continues.
>
> Copyright © 2026 Abdurashid Khudoyberdiev. All rights reserved. No licence is granted to copy, adapt or reuse this
> work. Access to the file is by request.

---

## Record 2 (new version of the existing software record, v1.0 → v1.2)

Use **"New version"** on the existing record (not a new upload), so the concept DOI stays the same.

**Resource type:** Software
**Title:** Artificial Civilization Laboratory (ACL)
**Version:** v1.2
**Access:** Restricted (as v1.0). **Licence:** as v1.0 (all rights reserved).
**Files:** a snapshot of the repository at the release commit (`git archive` of the tagged commit, see below)
**Related works:** *is documented by* → the book record (Record 1)

**Description:**

> The Artificial Civilization Laboratory (ACL) is a simulation that asks whether culture, and eventually
> civilization, can emerge in a world where nature is programmed and culture is written by nobody. People have
> bodies, needs, seasons, kin and learning minds; no custom, plan or institution is scripted.
>
> The archive contains the simulation's source code; every experiment's question or pre-registration (frozen and
> tagged before code or data), its code, analysis scripts, outputs and results; the experiment index; the roadmap;
> the project's rule book; and the source of the book *The World That Nobody Wrote*. Methods throughout: predictions
> frozen before any run; same-seed controls; read-only measurement verified by state hashes; replays checked against
> saved runs; pilots with hard stops; discovery and holdout sets for exploratory work; corrections appended, not
> rewritten.
>
> **Selected findings inside ACL (not claims about real human history):**
> - Traditions, trust and stories emerge unscripted; making and tools do not accumulate (E1–E8).
> - People could learn to expect winter, but preparing erased the hunger that taught it; copying the well fed passed
>   a foraging habit between adults, not a plan (E9–E13R).
> - Winter is lived hand to mouth; food is kept in family members' stomachs and debts, not stores; the world rewards
>   immediate return (W1–D2).
> - At ACL's present level of uncertainty, bad years kill but do not teach storage; even the widest weather varies
>   food only about a third as much as a real grassland's, and that weather was lethal (V1, U).
> - A third of control worlds (22 of 64) die out, not from hunger but because births stop decades before the end:
>   after the founders, partners are rarely found in a small, scattered people (F1, confirmed on a holdout).
> - Given perfect partner finding (a diagnostic, not a realistic mechanism), 7 of 64 die instead of 22: search is
>   most of the problem; the smallest worlds run out of eligible partners altogether (F2).
> - Couples are apart about half their weeks: partners forage independently, a gap between two code thresholds
>   leaves couples at 3 tiles neither able to conceive nor drawn together, and food outbids the pull back (C1,
>   confirmed on a holdout).
>
> **Changes since v1.0:** baseline-fragility study F1 (discovery and holdout); evidence review N5 on how real
> foragers find partners; stage 0 reopened; diagnostic experiment F2 (search mostly, size at the margin); read-only study C1 on why couples drift apart,
> with an open correction to F2's figure on couples apart; rules 12–19 added to the rule book;
> uncertainty experiment U (stopped at its pilot, recorded).
>
> Copyright © 2026 Abdurashid Khudoyberdiev. All rights reserved. No licence is granted to copy or reuse this work.

**The snapshot (made after C1; v1.1, made after F2, was superseded before upload):**

    git tag v1.2
    git archive --format=zip --prefix=acl-v1.2/ -o release/acl-v1.2.zip v1.2

Upload `release/acl-v1.2.zip`.

---

## Before uploading

- Check Zenodo → account menu → GitHub: if `simulated-world` is switched on, every GitHub release publishes a new
  Zenodo version automatically. Leave it on only if that is wanted.
- Rebuild the PDF after F2's chapter is in: `python book/build_book.py` then `python book/make_pdf.py`.
- Fill the placeholders: chapter count, F2's result, the upload date.
