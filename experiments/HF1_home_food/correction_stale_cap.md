# HF1 — Correction: the first discovery run measured fullness against a stale cap (rule 19)

**Found:** October 2026, after the first discovery run and its analysis were read, **before any holdout data**.

**What was wrong.** The frozen definition of fullness is plants ÷ the code's cap (`plant_cap × fertility`). The observer
computed each tile's cap once, in the first week, and reused it. But floods raise a tile's fertility (by 0.03 a flood, up
to 1.0; `weather.py`), and with it the cap, so the observer divided by a stale, too-low cap and reported fullness above 1.
Separately, food carried by a person who dies with no heir nearby is dropped on the tile and added to its plants
(`biology.py`), which can also take a tile above its cap; that is part of the frozen definition (plants ÷ cap) and is
kept.

**What was seen.** The stale-cap run was analysed and read: fullness within 3 tiles of home, H ÷ C = 0.998; food per
adult forage action, H ÷ C = 0.966. Those numbers are not valid measures of the frozen quantity and are not used. The run
is kept for audit in `output_stale_cap/`.

**The fix** follows from the frozen definition, not from any result: the observer now reads each tile's cap live, every
week. It was re-verified read-only in both arms (seeds 501 and 1301, 20 years). Discovery is re-run with the corrected
observer; the holdout has not been run.

**What could this have influenced?** The decision rule and its thresholds were frozen before any data and are
unchanged. The only change is to make the measurement match the definition.
