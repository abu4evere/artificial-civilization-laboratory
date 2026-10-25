# TW1: independent recompute (25 October 2026)

**Who:** GPT, in a fresh ChatGPT chat (https://chatgpt.com/c/6ade4051-7bb0-83e9-82c5-49f1fbf52052) with no ACL
history, so it had not seen the TW1 results. **Given:** the 512 raw output files (zip) and a description of the JSON
fields and of the frozen check definitions. **Not given:** `analyse_tw1.py`, `results.md` or any of our numbers. GPT
wrote and ran its own Python (SciPy `binomtest`).

| number | `analyse_tw1.py` / findings | GPT's recompute | match |
|---|---|---|---|
| files present | 512 | 512 (256 pairs; no name/arm/seed mismatches) | yes |
| distinct fingerprints | 1 | 1 (`179f67e1…7eedb`; 0 before/after mismatches) | yes |
| arm T deliveries | 23,652 | 23,652 | yes |
| twin deliveries, p vs 0.014 | 337, p 0.74 | 337 (248 fraternal + 89 identical), p 0.739794 | yes |
| identical deliveries, p vs 0.004 | 89, p 0.606 | 89, p 0.606397 | yes |
| boys / independent draws, p vs 105/205 | 12,346 / 23,900, p 0.176, 106.9 per 100 girls | 12,346 / 23,900, p 0.176283, 106.855 | yes |
| twin deliveries in arm C | 0 | 0 | yes |
| extinctions C / T | 83 / 97 | 83 / 97 | yes |
| paired: both / only C / only T, McNemar p | 48 / 35 / 49, p 0.156 | 48 / 35 / 49 (124 both survived), p 0.155656 | yes |

GPT found nothing odd in the data: no malformed deliveries, no unexpected kinds, no missing seeds or mislabelled files;
23,900 draws = 23,652 deliveries + 248 extra fraternal draws, as expected. It agrees the extinction difference is
inconclusive.

**The recompute agrees on every number. TW1's findings stand as final.**
