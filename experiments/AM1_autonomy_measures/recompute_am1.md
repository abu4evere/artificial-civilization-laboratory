# AM1: independent blind recompute (3 November 2026)

- **Input:** `recompute/am1_counts.csv` (160 rows). Per arm and world: the chain counts behind M3 and M5, the living
  weeks and extinction. It was built by `recompute/build_am1_counts.py`, written before data.
- **The exact text sent:** `recompute/prompt.txt`, written and committed before the data existed. The CSV was attached
  as a file.
- **Who** (each a fresh chat; none saw the analysis script or any earlier result):
  - GPT, chat `6ae998a7`: Python, 10,000 draws;
  - Gemini 3.1 Pro (High), chat `be3f18612734932e`: it ran code;
  - DeepSeek, chat `2e5c76a3`: no code tool. It worked by hand; its reasoning hit its length limit once and the
    assistant pressed "Continue".
- **Recorded only from their actual replies.**

| quantity | analyse_am1.py | GPT | Gemini | DeepSeek |
|---|---|---|---|---|
| M3: v11 / no habits / more chance / sham | 0.0036 / 0.0293 / 0.0077 / 0.0035 | the same | the same | the same |
| M5: v11 / no habits / more chance / sham | 0.0038 / 0.0318 / 0.0083 / 0.0035 | the same | the same | the same |
| M3, v11 − no habits | −0.0257 [−0.0277, −0.0238] | −0.0257 [−0.0277, −0.0238] | −0.0257 [−0.0277, −0.0238] | −0.025725 [−0.026071, −0.025379] |
| M3, v11 − more chance | −0.0041 [−0.0047, −0.0034] | −0.0041 [−0.0047, −0.0034] | −0.0041 [−0.0047, −0.0034] | −0.004077 [−0.004190, −0.003964] |
| M5, v11 − no habits | −0.0280 [−0.0302, −0.0259] | −0.0280 [−0.0302, −0.0259] | −0.0280 [−0.0301, −0.0259] | −0.028020 [−0.028393, −0.027646] |
| M5, v11 − more chance | −0.0045 [−0.0053, −0.0037] | −0.0045 [−0.0052, −0.0037] | −0.0045 [−0.0052, −0.0037] | −0.004505 [−0.004642, −0.004367] |
| readings | M3 not validated; M5 not validated | the same | the same | the same |
| sanity (arm a, made) | 0 | 0 | 0 | 0 |
| living weeks (v11, no habits, fewer acts, more chance, sham) | 22,182,887; 16,576,852; 21,807,441; 21,213,665; 22,385,275 | the same | the same | the same (a, c, h, t; sham not reported) |

The analysis's arm − v11 entries in `results.md` are the same numbers with the sign reversed (v11 − arm here, as the
prompt asked).

- **On arm a (fewer acts),** where nobody can make, the measures are 0 ÷ 0:
  - GPT: "mathematically undefined… Reporting either measure as 0 would be incorrect";
  - the analysis prints "nan";
  - Gemini and DeepSeek wrote 0.0000, DeepSeek "by the zero-opportunity convention".

  Nothing depends on it: arm a enters only the sanity count.
- **GPT's note:** "This is stronger evidence than merely failing to detect a positive difference: the measured
  contrasts point in the opposite direction."
- **GPT and Gemini match the analysis** on every point value, interval (within 0.0001), reading and the sanity count.
- **DeepSeek matches** every point value, reading and the sanity count. **Its intervals are far too narrow,** about a
  fifth of the bootstrap's width: its hand approximation understates the spread between worlds. No reading depends on
  it, since all four intervals lie far below 0 either way. The fault is in that approximation, not in the data.

M1 comes from the per-world held-out error sums of the ridge models (as in SC1). It was not part of this prompt.

**All three agree: M3 not validated, M5 not validated, the sanity count 0. AM1 is final.** All three tabs were closed.
