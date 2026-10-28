# PD1 — Independent recompute (GPT and Gemini, fresh chats, raw files only, no analysis script)

**Input:** two files built from the 192 output JSONs:
- `pd1_counts.csv`: one row per world;
- `pd1_census.csv`: world-years.

GPT received both in a zip; Gemini received the two CSVs. The attachments were checked before sending.

**The prompt (the same text to both):**
1. the accounting check;
2. the living at the end per arm, and the o − c and x − c gaps with a paired bootstrap;
3. births and each cause's deaths, o − c;
4. population in years 100–199;
5. tools in hand at attacks.

No analysis numbers were given.

Chats:
- GPT: https://chatgpt.com/c/6ae15cba-b0e8-83ea-aaa1-b650f8954d23
- Gemini: https://gemini.google.com/app/b880022f7eaa214a

## GPT (27 October 2026; numbers read from its reply)
Computed with Python; 20,000 replicates.
- **Accounting:** 192 of 192 worlds pass.
- **Living at year 200:** c 7,323, o 7,101, x 6,995.
  - o − c **−222 [−903, +497]**;
  - x − c **−328 [−1,042, +352]**;
  - both include 0.
- **o − c in deaths and births:**
  - births −909;
  - deaths: hunger +128, thirst −39, cold +1, illness −568, childbirth −5, violence +8, animals +1, other −213; total −687.
  - Check: −909 − (−687) = −222.
- **Population, years 100–199:** c 129.849, o 127.876, x 124.242; o ÷ c **0.985.**
- **Tool share at attacks:** c 0.400, o 0.593, x 0.387. Kills per attack: c 0.036, o 0.044, x 0.043.

**Against the analysis:** every number matches. The analysis lists each cause as its contribution to the gap
(−Δdeaths); GPT lists Δdeaths. They are the same numbers with opposite signs, as stated in the findings.

## Gemini
Pending. Nothing is recorded until its reply is read.
