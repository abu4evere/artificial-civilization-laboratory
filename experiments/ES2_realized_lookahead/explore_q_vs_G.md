# ES2 — exploratory: habit value against realized return, by action (NOT frozen; decides nothing)

Reads ES2's raw output (`output/`, 32 seeds per arm), habit updates started in years 100-200. q = the habit value when the update started; G = the return that followed (VC1's measure). Actions with at least 10,000 closed updates in both arms.

| situation | action | v11 n | v11 q | v11 G | v11 abs(q-G) | r n | r q | r G | r abs(q-G) | rise |
|---|---|---|---|---|---|---|---|---|---|---|
| all other situations | care | 36,621 | +0.409 | +0.855 | 0.464 | 93,738 | +0.303 | +0.859 | 0.558 | +0.094 |
| all other situations | court | 16,343 | +0.074 | +0.748 | 0.674 | 38,394 | +0.073 | +0.703 | 0.631 | -0.043 |
| all other situations | explore | 21,287 | +0.058 | +0.521 | 0.464 | 64,803 | +0.055 | +0.530 | 0.475 | +0.011 |
| all other situations | forage | 5,997,495 | +1.143 | +0.726 | 0.445 | 6,317,515 | +0.548 | +0.728 | 0.222 | -0.223 |
| all other situations | gather | 4,378,862 | +0.873 | +0.482 | 0.423 | 4,953,092 | +0.358 | +0.486 | 0.161 | -0.263 |
| all other situations | give | 1,874,515 | +1.334 | +0.913 | 0.456 | 1,968,599 | +0.826 | +0.896 | 0.200 | -0.256 |
| all other situations | join | 1,158,056 | +0.770 | +0.603 | 0.259 | 1,311,371 | +0.361 | +0.590 | 0.247 | -0.012 |
| all other situations | make | 21,838 | +0.081 | +0.591 | 0.510 | 74,262 | +0.083 | +0.592 | 0.509 | -0.001 |
| all other situations | play | 45,431 | +0.072 | +0.619 | 0.548 | 143,553 | +0.069 | +0.631 | 0.562 | +0.015 |
| all other situations | put | 2,046,832 | +0.749 | +0.443 | 0.348 | 2,491,066 | +0.325 | +0.452 | 0.153 | -0.195 |
| all other situations | rest | 130,101 | +0.250 | +0.634 | 0.393 | 282,271 | +0.177 | +0.635 | 0.459 | +0.066 |
| all other situations | talk | 2,805,841 | +1.057 | +0.787 | 0.345 | 2,910,911 | +0.545 | +0.788 | 0.266 | -0.079 |
| crisis, with company | forage | 3,110,514 | +1.188 | +0.793 | 0.413 | 3,924,843 | +0.635 | +0.797 | 0.203 | -0.210 |
| crisis, with company | gather | 120,573 | +0.139 | +0.430 | 0.312 | 202,935 | +0.037 | +0.420 | 0.387 | +0.074 |
| crisis, with company | give | 34,529 | +0.264 | +0.510 | 0.273 | 82,760 | +0.216 | +0.432 | 0.237 | -0.037 |
| crisis, with company | join | 44,069 | +0.233 | +0.535 | 0.350 | 70,368 | +0.090 | +0.543 | 0.468 | +0.118 |
| crisis, with company | play | 78,879 | +0.051 | +0.422 | 0.373 | 183,377 | +0.011 | +0.392 | 0.383 | +0.010 |
| crisis, with company | put | 44,782 | +0.180 | +0.446 | 0.304 | 76,909 | +0.073 | +0.466 | 0.406 | +0.101 |
| crisis, with company | rest | 810,432 | +0.377 | +0.484 | 0.212 | 1,021,329 | +0.108 | +0.476 | 0.372 | +0.161 |
| crisis, with company | talk | 1,088,964 | +0.372 | +0.620 | 0.262 | 1,351,388 | +0.094 | +0.587 | 0.493 | +0.231 |

- **All updates:** v11 mean q +0.967, mean G +0.664; r mean q +0.456, mean G +0.656.
- **Rows where q is below G:** v11 13 of 20; r 20 of 20.

## Reading (the assistant's; a hypothesis for the council, not a finding)
- **Under r, rest is not a special case.** The realized return G hardly moves between the arms in any row. What changes is q: under r it sits below G for every action listed, so the whole habit system under-values.
  - Under v11 the max look-ahead's inflation lifted the common actions above G and partly hid this.
  - In the crisis rows, talk worsens even more than rest. The frozen per-action guard pooled each action over all situations, so talk's rise there was diluted by its other situations.
- **A candidate cause, from the code** (not tested): habits start low and learn slowly.
  - A newborn's habits start at half the parents' mean (`child.q = 0.25 * (mother.q + father.q)`, `acl/biology.py` line 553).
  - They then move 5% of the way per update (`learning_rate` 0.05).
  - Without the max's upward push, a value built from the next choice's (still low) value may climb slowly within one life.
- **What would test it, read-only:** calibration split by age, or by how many times the person had already updated that habit. It would need a new frozen diagnostic study, debated with GPT and Gemini first.

