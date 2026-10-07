# HF1 — Food around HB1's homes: discovery (seeds 501–516; holdout not yet run)

Questions and decision rule frozen as `HF1-questions`. Corrected observer (see `correction_stale_cap.md`; the stale-cap
run is archived and not used). Valid: observer read-only in both arms, all 32 replays reproduce HB1's and F1's saved
populations, code unchanged. Full table: `results_discovery.md`.

| measure | H (home base) | C (control) | H ÷ C |
|---|---|---|---|
| **fullness within 3 tiles of home** (rule) | 0.774 | 0.798 | **0.970** |
| fullness on the ring 4–6 tiles out | 0.946 | 0.911 | 1.039 |
| fullness within 3 tiles, winter | 0.588 | 0.635 | 0.926 |
| **food per adult forage action** (rule) | 18.93 | 19.61 | **0.966** |
| food per forage action within 3 tiles of home | 17.71 | 19.15 | 0.925 |
| share of adult forage actions within 3 tiles of home | 0.531 | 0.404 | 1.316 |
| people per land tile within 3 tiles of home | 0.256 | 0.217 | 1.180 |
| hunts per person-year | 0.048 | 0.080 | 0.597 |

**Discovery alone, against the frozen rule:** fullness near home H ÷ C = 0.970 (confirmation needs ≤ 0.80; "not
confirmed" needs ≥ 0.90 in both sets); food per forage action lower in H. **On discovery, the reading leans to "not
confirmed"**; the rule is applied only when the holdout is in.

**Noted for later, not read now** (descriptive; outside the rule): hunting fell by about two fifths in H; adults who
starved under H had, in their last 8 weeks, less food around them than all adults in the same weeks (0.712 against
0.732), while in C the starving had more around them than all adults (0.822 against 0.799). These are leads for the
holdout and for whatever follows, not findings.

Next, frozen order: holdout seeds 1301–1316 (`run_hf1.py holdout`), then `analyse_hf1.py both` and the frozen rule.
