# TU1 — how tool use is learned, and whether it spreads: findings

Frozen as `TU1-frozen` before any code or data. Read-only: FX3's S25 and B50 worlds (seeds 7301–7556, 512 worlds) were
replayed exactly with an observer on GitHub's machines (`cloud-run`, run 39657856506). Tables: `results.md`, from
`analyse_tu1.py`. Described, no tests. Tool use, tool possession and survival are kept apart.

## Validity

- The zero check passed on this PC: the observer changes nothing.
- All 512 worlds are present.
- Every replay equals FX3's saved world (512 of 512).
- There is one code fingerprint (`code_fx2`).

**Valid.**

## The frozen reading

**Q1: how people come to their first tool use.**

| arm | first users | after being told | inherited the item | own discovery |
|---|---|---|---|---|
| S25 | 11,784 | 1.6% | 0.1% | 98.3% |
| B50 | 14,879 | 1.2% | 0.1% | 98.7% |

**The main route is own discovery, the same in both arms, so it stands.** A person holding a hard thing while foraging
embedded food feels it help. Being told comes first in under 2% of cases. **The prior was right.**

**Q2, spread (described).** At a person's first use, someone within sight had used a tool on embedded food in the 13
weeks before in 78% of cases (S25) and 78% (B50); in about two-thirds of those, that person was kin. By year 10,
about 91–92% of adults (median over worlds) had used a tool. By year 20 it was 100%, and it stayed there.

These numbers **do not show spread from person to person.** Almost everyone becomes a user within a decade or two, by
their own discovery. So a user nearby, usually kin, since people forage near kin, is close to certain whether or not
anyone learns from anyone. There is no baseline here that would separate copying from everyone finding it alone.

**Q3, lasting (described).** Once started, use lasts. The median user used a tool in 136–138 weeks, and their first
and last use were 954–1,020 weeks apart (about 18–20 years).

## What it means for ACL

Tool use in these worlds is **universal but not cultural.** Each person rediscovers it, and it is seldom passed on.
That fits the earlier picture: in CA1, CA3 and LM1, information passes on weakly. It also fits FX3: tool use rose
without changing survival. Real foragers' tool skill grows from access and self-directed play, alongside watching and
later teaching (`evidence_tools.md`). ACL has the self-directed part. The routes that would make tool use a tradition
rather than a rediscovery are rare (being told) or missing (handing tools over, children playing with them). TU1
proposes no change. Any such route would be a Law 126 question, and the custom of giving tools to children would be
culture, which must not be written in.
