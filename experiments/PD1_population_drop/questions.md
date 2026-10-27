# PD1 — Why does population fall when made things persist? (frozen plan)

**Read-only. No change to nature.** The worlds are run on OP1's code (`code_op1`), arms as OP1, with a read-only
observer. Chosen in sleep mode (`docs/autonomous_decisions.md`, 27 October 2026). Both GPT (75%) and Gemini (95%)
agreed; GPT put it first (debate round 15, `docs/debate_after_op1_2026-10-27.md`).

**OP1 (final):** the law (made things drop instead of vanishing, and are picked up) was supported but flagged.
- Mean population in years 100–200 was o ÷ c 0.845, 95% [0.755, 0.938].
- The sham alone was 0.898 [0.806, 1.014].

**Before any decision on adopting the law, the cause of the fall must be understood** (GPT and Gemini). GPT's caution:
the sham alone moves population by about 10%. One extra random draw sends each world down a different path, so 32
worlds cannot separate a 15% effect from chance. **So PD1 uses 64 paired seeds, and compares o with both c and x.**

## Arms (64 paired seeds, 19401–19464; LP; 200 years; run on GitHub; code `code_op1`)

| arm | setting |
|---|---|
| **c** | v7 (`ground_items` 0) |
| **o** | `ground_items` 1 |
| **x** | sham (`sham_draw` 1) |

## Logged (read-only: weekly events and a wrapper on `actions._attack` that reads before calling the original)

- **Every death:** the cause as the code records it, grouped as:
  - hunger (starvation, neglect);
  - thirst;
  - cold;
  - illness;
  - childbirth;
  - violence (killed);
  - animals (wolves, a bear);
  - other.

  With the age band of the dead: child under 12, teen, adult 16–49, elder 50+.
- **Every birth.**
- **Every attack:**
  - the attacker's best fighting-tool factor at that moment (`best_item(p, "fight")`, read without drawing);
  - whether the attacked was killed;
  - whether the attacker died.
- **A yearly census:** living people by age band.

## Questions (primary: years 0–200; population and exposure beside every measure; 95% paired world bootstrap, 10,000 replicates)

**Q1 (primary). The exact split of the population gap.**
- Every world starts with the same 80 founders. So the living population at year 200 equals 80 + births − deaths.
- The difference o − c in final population splits exactly into:
  - the births difference;
  - minus each cause's deaths difference.
- This is pooled over paired worlds, with worlds that died out counted at 0.

**Named:** the component carrying the largest share of the gap. The same split for x − c is shown beside it, as the
yardstick.

**Q2. Rates.** Deaths per 1,000 person-years by cause and age band, and births per 1,000 woman-years aged 16–45. For
o − c and x − c: is o's difference outside the sham's band?

**Q3. Fighting.**
- Attacks and killings per 1,000 adult-years.
- The share of attacks made with a fighting tool in hand (factor > 1), and the kill rate with and without one.
- Deaths of attackers.

All o against c and x.

## What would follow (stated now)
- **Violence carries the gap,** and attacks with tools in hand rise: more tools in hand make fights deadlier. A
  candidate for the creator: whether OP1 is still wanted, or whether fighting's laws need looking at first.
- **Births carry the gap:** fewer children (perhaps through time spent, or mothers' health). Described.
- **Hunger, cold or illness carry it:** tools change how people spend their weeks. Described.
- **o's differences are inside the sham's band:** the OP1 flag was chance. OP1 can be reconsidered with this evidence,
  which is the creator's decision.

## The assistant's prior
1. Violence carries the largest share of the gap.
2. Attacks with a fighting tool in hand are more common in o, and their kill rate is higher.
3. Births change little.

**On record from the debate:** Gemini expects weapon access to turn disputes lethal. GPT warns that a cause of death
"explaining most of the death-count difference is not necessarily the underlying mechanism".

## Validity (hard stops)
- **Zero checks:**
  - `code_op1` with the setting 0 equals `code_v7` (as OP1);
  - the observer is read-only in arms o and c (state and random numbers identical with and without it);
  - reload is exact in arm o.
- **Accounting:** in every world, 80 + births − deaths = the living population at the end (a mismatch counter that
  must be 0).
- All 192 worlds are present under one fingerprint.
- An independent recompute by GPT and Gemini (fresh chats, raw files) of Q1's split and the largest component before
  the findings are final. A recompute is recorded only from numbers read from the reply.

## Sign-off (27 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). Both models agreed (GPT 75%, Gemini
95%); the assistant's estimate is 75%, above the 40% threshold. Logged in `docs/autonomous_decisions.md`. Frozen as
`PD1-frozen` before any code or data.
