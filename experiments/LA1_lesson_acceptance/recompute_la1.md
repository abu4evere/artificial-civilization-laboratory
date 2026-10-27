# LA1 — Independent recompute (GPT and Gemini, fresh chats, raw cells only, no analysis script)

**Input:** `la1_cells.csv`, built from the 32 output JSONs. It has 2,563 rows, one per world × cell, with every raw
counter. GPT received it as a zip; Gemini received the CSV. Both files were checked as attached before sending.

**The prompt (the same text to both):** the definitions of the gates and counters, and the tasks:
- (1) per-era gate shares;
- (2) T1–T4, P and their Δ ln from era 0 to era 2, and the most negative term;
- (3) a world-bootstrap interval for Δ ln P.

No analysis numbers were given.

Chats:
- GPT: https://chatgpt.com/c/6ae0522e-0964-83e9-bd72-358034bf8344
- Gemini: https://gemini.google.com/app/24f3dead6015dc96

## GPT (27 October 2026; numbers read from its reply)
Computed with Python. It checked 32 worlds and 959 selected rows, and found that both gate-count identities hold
exactly in every selected row.

| | era 0 | era 1 | era 2 |
|---|---|---|---|
| G1 / offered | 0.0413 | 0.0311 | 0.0329 |
| G3 / offered | 0.7409 | 0.7528 | 0.7660 |
| G4 / offered | 0.1942 | 0.1949 | 0.1765 |
| taken / offered | 0.0236 | 0.0212 | 0.0247 |

| term | era 0 | era 2 | Δ ln |
|---|---|---|---|
| T1 | 0.9587 | 0.9671 | +0.0088 |
| T2 | 1.0000 | 1.0000 | 0 |
| T3 | 0.2272 | 0.2087 | −0.0848 |
| T4 | 0.1082 | 0.1231 | +0.1293 |
| P | 0.0236 | 0.0248 | +0.0533 |

- **The most negative term is T3.**
- **"Is P lower in Era 2? No."**
- Δ ln P bootstrap 95%: **[−0.0397, +0.1574]** (20,000 replicates).

**Against the analysis:** every number matches to the reported precision. The analysis's interval is [−0.0376, 0.155]
from 10,000 replicates, the same within bootstrap noise.

## Gemini (27 October 2026; numbers read from its reply)
Computed with Python (pandas, NumPy).

| | era 0 | era 1 | era 2 |
|---|---|---|---|
| G1 / offered | 0.0413 | 0.0311 | 0.0329 |
| G3 / offered | 0.7409 | 0.7528 | 0.7660 |
| G4 / offered | 0.1942 | 0.1949 | 0.1765 |
| taken / offered | 0.0236 | 0.0212 | 0.0247 |

**The terms, with Gemini's sums:**
- **Era 0:** T1 = 165,086 / 172,203 = 0.9587; T3 = 37,505.4878 / 165,086 = 0.2272; T4 = 4,056.9264 / 37,505.4878 =
  0.1082; P = 0.0236.
- **Era 2:** T1 = 199,313 / 206,088 = 0.9671; T3 = 41,601.4115 / 199,313 = 0.2087; T4 = 5,121.1075 / 41,601.4115 =
  0.1231; P = 0.0248.
- **Δ ln:** T1 +0.0088; T2 0; T3 −0.0848; T4 +0.1293; P +0.0533.

- **The most negative term is T3.**
- P is "higher in Era 2".
- Δ ln P bootstrap 95%: **[−0.0396, 0.1571]** (10,000 replicates).

**Against the analysis:** every number matches.

## Verdict
**The analysis, GPT and Gemini agree on every key number:**
- the gate shares in all three eras;
- T1–T4;
- P 0.0236 → 0.0248, Δ ln +0.053;
- the bootstrap intervals all include zero;
- T3 is the only term that falls.

The frozen premise (a fall after year 50) does not hold per lesson, as the findings state. **The findings are final.**
