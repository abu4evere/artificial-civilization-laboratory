# ES2 — exploratory: where rest's calibration worsens (NOT frozen; decides nothing)

Reads ES2's raw output (`output/`, 32 seeds per arm). Rest's habit updates started in years 100-200, by the situation they were made in (food level x company; seasons pooled).

| food | company | v11 n | v11 mean abs(q-G) | v11 bias | r n | r mean abs(q-G) | r bias | rise |
|---|---|---|---|---|---|---|---|---|
| weak/<0.5 wk | no | 1,692 | 0.432 | -0.423 | 1,666 | 0.436 | -0.426 | +0.003 |
| weak/<0.5 wk | yes | 810,432 | 0.212 | -0.107 | 1,021,329 | 0.372 | -0.368 | +0.161 |
| <2 wk | no | 2,675 | 0.516 | -0.515 | 2,654 | 0.503 | -0.502 | -0.013 |
| <2 wk | yes | 58,925 | 0.458 | -0.456 | 133,574 | 0.513 | -0.512 | +0.055 |
| <6 wk | no | 4,262 | 0.416 | -0.415 | 4,141 | 0.405 | -0.405 | -0.010 |
| <6 wk | yes | 59,267 | 0.314 | -0.295 | 136,832 | 0.408 | -0.406 | +0.094 |
| 6+ wk | no | 201 | 0.275 | -0.273 | 208 | 0.274 | -0.274 | -0.001 |
| 6+ wk | yes | 3,079 | 0.524 | -0.524 | 3,196 | 0.495 | -0.495 | -0.029 |

All rest updates: v11 0.2367 over 940,533; r 0.3912 over 1,303,600 (the frozen guard's numbers: 0.237 -> 0.391).

**Reading (exploratory; a hypothesis for the next debate, not a finding):**
- **Nearly all of rest's rise is in one situation:** weak or under half a week of food, **with company**. That cell
  holds about 80% of rest updates in both arms. There, rest's error rises 0.212 → 0.372, and its bias moves −0.107 →
  −0.368.
- **In every other situation** the change is small (−0.03 to +0.09).
- **A possible mechanism:** under the max, rest in a crisis borrowed the inflated best value of the next week. Under the
  realized look-ahead, the next week's values (now honest or slightly low for the common actions) carry less, so resting
  in a crisis is marked down below what follows it.
- **Whether that is a flaw in the rule or a truer picture of resting while starving** is a question for a frozen,
  read-only study. ES2's reading (not supported) stands.
