# NB3: independent blind recompute (11 November 2026)

- **Input:** `recompute/nb3_worlds.csv` (112 worlds) and `recompute/nb3_genes.csv` (arm f), built by
  `recompute/build_nb3_counts.py`. The builder and `recompute/prompt.txt` were committed before the data. The garden
  file is empty: phase 2 is still running.
- **GPT** (Thinking, medium), chat `6af4b445`: the files were attached and it ran code. It matches every point value
  and the reading:
  - extinct worlds c 4, n2 12, f0 11, fH 7, f 5, f−E 10, f−H 12;
  - population f/c 0.4893 [0.3245, 0.6726] (analysis [0.3251, 0.6705]: a different random draw);
  - survival f 0.7813, f − n2 −0.0310 [−0.0612, −0.0043], f − fH −0.0331, f − c −0.0936;
  - the g and gene means are the same;
  - reading: **f not viable.**
- **Gemini** (chat `a2054078`, the instructions and both tables in one attached text file): pending.
