# AF1: Open what made things can do — findings

**A nature-change test in a copy (`code_af1` = `code_v11` + `similar_parts` + `containers_carry`). Live nature stays
v11.**
- Frozen as `AF1-frozen`.
- Signed off with the creator's approval of step 1 (GPT 93%, Gemini 95%, the assistant 55%; debate round 50).
- Its origin: the creator's "we should not script that but we should create the best possibilities to be created".

**The run:**
- GitHub Actions run 41573896983 (2 h 17 min).
- The zero checks ran locally (`zero_local.log`: All: PASS). They show:
  - `code_af1` at 0 = v11;
  - the observer is read-only;
  - reload is exact;
  - S makes a recipe exactly as v11 whenever the exact inputs are held (279,043 checks).
- 160 worlds: five arms × 32 paired seeds (22301–22332). LP, 200 years; years 100–200 counted.
- Every number comes from `analyse_af1.py`, written before data. Full tables are in `results.md`.

**Validity:** zero checks pass; all 160 worlds are present under one `code_af1` fingerprint.

## The answer
**Neither rule lets inventions be made again. S, K and S+K are all inconclusive. No guard was raised.**

| arm | R (late kinds remade within 5 years) | kinds | remade |
|---|---|---|---|
| v11 | 0.0003 | 3,414 | 1 |
| S, make by what it does | 0.0006 | 3,437 | 2 |
| K, containers contain | 0.0000 | 3,150 | 0 |
| S+K | 0.0000 | 3,194 | 0 |
| sham | 0.0000 | 3,346 | 0 |

- **The contrasts:** every one lies within ±0.0014. S − v11 is +0.0003 [−0.0007, +0.0012]; S − sham is +0.0006
  [+0.0000, +0.0014]. No arm comes near the frozen minimum of 0.01.
- **The guards:** none raised.
  - population ÷ v11: S 0.981 [0.868, 1.102]; K 0.966 [0.847, 1.093]; S+K 0.974 [0.858, 1.094];
  - extinctions beyond v11's: S −1, K 0, S+K −1.

**The assistant's prior:**
1. K inconclusive: **right**.
2. S positive: **wrong**.
3. S+K positive: **wrong**.
4. No guard: **right**.

## What the secondary numbers show (described, not decisive)
| arm | stand-in makes per adult-year | made things held per adult (limit 3, or more under K) | materials per adult (limit 20) | makes per adult-year | late kinds still known 5 years on |
|---|---|---|---|---|---|
| v11 | 0 | 0.93 | 11.8 | 0.072 | 0.806 |
| S | 0.0013 | 0.92 | 11.9 | 0.075 | 0.793 |
| K | 0 | 0.90 | 12.7 | 0.068 | 0.834 |
| S+K | 0.0012 | 0.95 | 12.7 | 0.067 | 0.829 |

**The assistant's reading** (it decides nothing; for the council):
1. **Carrying was not the bottleneck.** Adults hold **under one made thing on average**, far below the limit of 3, and
   about 12 of 20 units of material. Raising the limits (K) changed almost nothing. So UP1's "cannot make" does not
   come from full hands: people do not keep parts at all.
2. **Stand-ins were possible but rare** (about one make in 60 under S). People seldom hold a made thing close enough
   in all ten properties.
3. **The knowledge survives but is not used.** About 80% of late kinds are still known by someone alive five years
   later, in every arm. Remaking fails at the choice, not at memory or loss.
4. **Making itself is rare.** About 0.07 makes per adult-year: an adult makes something about once in 14 years. Most
   new kinds come from play. TR1 (31 October) found tools add about 1% of the food foraged. In this world, a made
   thing seldom pays for the week spent making it. That points to the open objective "a world where knowing matters".
   Better tools may need to matter more, by physics, before people choose to make and remake them. That would be a
   question about nature, never a reward written in.

## Next (for the council, round 53)
- **Not adopted:** neither rule changes live nature.
- **The rules review continues:** FX1 is running; MT1, FT1 and FX2 are drafted.
- **A new question raised by AF1:** why is making so rare when about 80% of new kinds are still known? It would be
  answered by a read-only look at the value side: the worth people learn for made things against what the things
  really add (IW1 and TR1's measures, on v11). This should come before more openings.

## Blind recompute (`recompute_af1.md`)
- **GPT** (chat `6ae97939`) and **Gemini 3.1 Pro** (chat `6f881f4f9bb44719`) recomputed with code from the per-world
  counts, blind, with the prompt written before data. Both **match every point value, reading and guard**. Their
  interval ends differ by at most 0.004.
- **DeepSeek** (chat `0edb4e50`, the first recompute by the third council member) had no code tool. Working by hand,
  it **matches every point value, reading and guard**, and gave approximate intervals.
- **AF1 is final.**
