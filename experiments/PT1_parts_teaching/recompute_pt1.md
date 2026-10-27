# PT1 — Independent recompute (GPT and Gemini, fresh chats, raw files only, no analysis script)

**Input:** two files built from the 32 output JSONs:
- `pt1_cells.csv`: 1,316 rows (world × cell), every raw counter;
- `pt1_chains.csv`: 59,990 world-born useful chains with their step weeks.

GPT received both in a zip; Gemini received the two CSVs. The attachments were checked before sending.

**The prompt (the same text to both):** the cell and chain definitions, and the tasks:
- (1) class shares and a bootstrap interval for the reach share;
- (2) the reachable funnel and the lowest conditional step;
- (3) the memory shares.

No analysis numbers were given.

Chats:
- GPT: https://chatgpt.com/c/6ae065af-bc88-83e9-8dec-482818ec6bd9
- Gemini: https://gemini.google.com/app/055d65c828e91942

## GPT (27 October 2026; numbers read from its reply)
Computed with Python (pandas, NumPy). It checked 32 worlds, 1,316 cell rows and 59,990 chain rows.

- **(1)** 95,580 failures:
  - none 9,332 (0.098);
  - wrong 4,249 (0.044);
  - deep 55,381 (0.579);
  - **reach 26,618 (0.278)**, 95% [0.266, 0.290] (10,000 replicates).
- **(2)** 19,472 reachable chains:

  | step | count | conditional |
  |---|---|---|
  | pt | 6,092 | 0.313 |
  | pk | 3,900 | 0.640 |
  | pm | 436 | 0.112 |
  | ah | 346 | 0.794 |
  | wt | 215 | 0.621 |
  | wm | 12 | 0.056 |

  **Lowest: wm (whole made)**, with pm second.
- **(3)** Whole overflows, 41,808:
  - new lesson evicted 29,851 (**0.714**);
  - replay survives 40,004 (**0.957**).

**Against the analysis:** every number matches.

## Gemini (27 October 2026; numbers read from its reply)
The first attempt returned an error ("I seem to be encountering an error"). Asked to retry, Gemini computed with
Python (pandas, NumPy):
- **(1)** 95,580 failures:
  - none 9,332 (0.098);
  - wrong 4,249 (0.044);
  - deep 55,381 (0.579);
  - **reach 26,618 (0.278)**, 95% [0.266, 0.291] (exact [0.2655, 0.2906]; 10,000 replicates).
- **(2)** 19,472 reachable chains:
  - pt 6,092 (0.313);
  - pk 3,900 (0.640);
  - pm 436 (0.112);
  - ah 346 (0.794);
  - wt 215 (0.621);
  - wm 12 (0.056).

  **Lowest: wm (whole made).**
- **(3)** Of 41,808 whole overflows:
  - evict_new 29,851 (**0.714**);
  - replay survives 40,004 (**0.957**).

**Against the analysis:** every number matches. The upper bootstrap bound differs in the third decimal (0.291
against 0.290), which is bootstrap noise.

## Verdict
**The analysis, GPT and Gemini agree on every key number.** The findings are final.
