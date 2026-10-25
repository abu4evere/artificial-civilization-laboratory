# GPT's view of the TW1 result (25 October 2026). GPT's opinion, not sign-off.

Asked by the assistant at the creator's request: (a) cut v7 = v6 + twins + 105:100 + nursing fix, or (b) keep v6?

**GPT votes (a), on one condition: an integrity audit of maternal deaths and the sex ratio must pass first.**
- Do not keep v6 because v7 has a few more extinctions or fewer adult women. Nature must be justified on its own,
  not by whether it helps worlds survive.
- The manipulation checks show the intended biology was implemented.
- Twins dying more with no special rule is closer to ACL's philosophy than adding an invented twin-death chance. Check
  that it comes from shared food, not from birth order or a bug.
- Three checks before cutting v7:
  1. The adult sex ratio (men already outnumber women in C): sex-specific deaths by age and cause; make sure the
     ratios use properly followed cohorts.
  2. The 31 of 329 twin mothers who died within a year (about 9.4%): compare with singleton mothers; make sure one
     delivery does not trigger two childbirth risks.
  3. Extinction 83 vs 97: report it, and use paired (discordant) counts. It is not an adoption gate, and arm T changes
     two settings at once.
- No new 512-world experiment is needed. A focused read-only audit, delivery tests and the existing parity checks are
  enough.

## What the assistant could check from the saved data and code (post hoc, described only)

- **Ratios use followed cohorts:** yes. A person counts at age a only if they were born in the world and seen alive at
  age a (`summarise` in run_tw1.py). Younger people do not lower either sex.
- **One childbirth risk per delivery:** yes. Shown by the code (one draw after both twins are born) and by zero-check
  unit test 13.
- **Extinction, paired by seed:** both died 48; only C died 35; only T died 49. Exact McNemar p = 0.16, so the
  difference is not clear.
- **Why women die younger, from the code (v6, unchanged):** only women carry costs. Pregnancy adds 1.5 to weekly food
  need. The mother is the infant's carer and feeds dependants from her own food. Childbirth carries a death risk. The
  saved deaths have no sex, so the assistant could not split deaths by sex and cause. That needs a small read-only
  logging pass (the creator decides; RH1, in M1's worlds, may show part of it for women).
- **Twin mothers against singleton mothers:** not in the saved data; it needs the same logging pass.
