# WM1: independent recompute (25 October 2026)

**Who:** GPT, in a fresh ChatGPT chat (https://chatgpt.com/c/6ade9307-2384-83ea-8580-e582d29f1650) with no ACL history.
**Given:** the 1,152 raw output files (five zips) and a description of the fields and the frozen definitions. **Not
given:** `analyse_wm1.py`, `results.md` or any of our numbers. GPT wrote and ran its own Python (saved in that chat).

| number | `analyse_wm1.py` | GPT's recompute | match |
|---|---|---|---|
| files; fingerprints | 1,152; one per code | 1,152; one per code; before = after | yes |
| C20 women / men std rate | 41.2 / 32.5 | 41.182 / 32.532 | yes |
| C20 G [95%]; R | 8.6 [5.85, 11.37]; 1.27 | 8.650 [5.848, 11.366]; 1.266 | yes |
| D80 G; R | 13.6 [11.30, 16.05]; 1.39 | 13.586 [11.303, 16.048]; 1.388 | yes |
| G by arm: P, B, K, PB, PK, BK, PBK | 9.09, 9.78, 3.87, 9.30, 2.85, 3.41, 2.14 | 9.093, 9.782, 3.874, 9.296, 2.850, 3.415, 2.143 | yes |
| main effect P | −0.58 [−2.38, 1.23] | −0.585 [−2.383, 1.228] | yes |
| main effect B | 0.04 [−1.10, 1.21] | +0.042 [−1.104, 1.215] | yes |
| main effect K | −6.13 [−8.19, −4.11] | −6.135 [−8.186, −4.106] | yes |
| G(PBK) / G(C20) | 0.25 [0.00, 0.55] | 0.248 [0.004, 0.550] | yes |

**About the identical intervals:**
- The point estimates are independent arithmetic.
- The intervals also agree to the third decimal because GPT chose the same bootstrap generator seed as
  `analyse_wm1.py`. Both used today's date, 20261025, with numpy's default generator. This is a coincidence of
  convention, not a shared script.

**GPT's notes:**
- 438 single world × sex × band cells have no person-weeks, but no pooled band was empty.
- C20 adult cells hold 93 childbirth deaths, against 1,494 starvation and 2,766 illness deaths.
- B alone raises G a little (9.78 against 8.65); this may be an indirect population effect.
- These are model results, not evidence about real populations.

**The recompute agrees on every number. WM1's findings stand as final.**
