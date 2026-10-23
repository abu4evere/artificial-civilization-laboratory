# BD1 exploratory breakdown (after BD1's results; NOT frozen; labelled exploratory)

Planned and run after seeing BD1's survival result, to look for its cause. `explore/code_bd1x` = `code_bd1` + three
switches that each turn one part of `bodies_stay` off. BD1's first 64 seeds (12001–12064), paired with BD1's own C and
B worlds on the same seeds. Run on this PC (`explore/run_x.py`).

| arm | what is off | died out (of 64) | time-averaged population | foul weeks | seen | meals from bodies |
|---|---|---|---|---|---|---|
| C (v3) | no bodies | 21 | 25.12 | 0 | 0 | 0 |
| B | nothing | **12** | **31.55** | 2,677,152 | 27,865 | 972 |
| B without disgust at rot | foul | **26** | 26.81 | 0 | 22,344 | 714 |
| B without knowing by sight | seen | 14 | 28.21 | 2,219,344 | 0 | 862 |
| B without meat (a body leaves no food; quickly bones) | meat, and so rot | 20 | 26.77 | 54,080 | 164 | 0 |

Reading (exploratory, 64 seeds, no test): the survival gain goes with **disgust at rot**. Without it, as many worlds
die as without bodies at all; without the sight of bodies, most of the gain remains; without meat (which also removes
the rot), the gain is gone.
