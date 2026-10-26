# MK1 — Independent recompute (27 October 2026)

**Who:** GPT and Gemini, each in a fresh chat with no earlier context (the creator's rule of 27 October: both models).
**What they saw:** the raw output of all 32 worlds (cells and tools; nothing recomputed or summarised), a field
dictionary and the frozen definitions. **Not** the analysis script, `results.md` or the findings.
- GPT got `mk1_raw.zip`.
- Gemini could not open a zip, so it got the same rows, unzipped, as two CSV files. Its first attempt computed other
  ratios (arithmetically right; checked). The tasks were restated, and it then computed them.

Both used their own Python and 10,000 whole-world bootstrap replicates.

| measure | analysis | GPT | Gemini | match |
|---|---|---|---|---|
| worlds; mismatch dicts empty | 32; yes | 32; yes | 32; yes | yes |
| R1 chosen / offered, early → late (raw) | 0.0232 → 0.0012 | 0.023215 → 0.001186 | 0.023215 → 0.001186 | yes |
| R1 late / early | 0.051 | 0.05108 [0.0465, 0.0561] | 0.05108 [0.0466, 0.0558] | yes |
| R2 kept states | 24 | 24 | 24 | yes |
| matched rate, early → late | 0.0232 → 0.0020 | 0.023215 → 0.001989 | 0.023215 → 0.001989 | yes |
| mean v, early → late | 0.144 → 0.144 | 0.143778 → 0.143844 | 0.143778 → 0.143844 | yes |
| mean U_other, early → late | 1.296 → 1.937 | 1.295803 → 1.936550 | 1.295803 → 1.936550 | yes |
| Δ mean log-odds | −3.120 [−3.19, −3.05] | −3.119983 [−3.196, −3.048] | −3.119983 [−3.195, −3.048] | yes |
| −Δ U_other / 0.2 (share) | −3.204 [−3.28, −3.13] (1.03) | −3.203736 [−3.280, −3.133] (102.7%) | −3.203736 [−3.280, −3.132] (102.7%) | yes |
| worth term (v + diligence + hunger + covariance) | −0.001 − 0.010 + 0.006 + 0.002 = −0.003 | −0.003520 | −0.003520 | yes |
| habit; thought | +0.134; −0.046 | +0.133646; −0.046373 | +0.133646; −0.046373 | yes |
| largest part | the other options | U_other | −U_other | yes |
| R3 owed by 52 weeks, tools made in years 0–5 | 29.4 | 29.354 | 29.354 | yes |
| R3 owed by 52 weeks, tools made in years 100–200 | 44.4 (adults and teens) | 45.591 (adults) | 45.591 (adults) | explained |

**The one difference is explained.** The request said "adults only" for R3, while the analysis's Q4 table counts every
deliberate maker, teens included. Adults only, the raw data give 45.591 for years 100–200 (10,590 tools; checked by
script); all makers give 44.444 (12,091). The reading is the same either way.

**GPT's caution (adopted):** the data show that the other options' soft maximum carries the decline. They do not say
which competing action causes it.

**Verdict:** every key number agrees across the analysis, GPT and Gemini. The findings are final.
