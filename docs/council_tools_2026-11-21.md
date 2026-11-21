# Council: useful materials, tools, compute and people (21 November 2026): GPT's and Gemini's opinions, not sign-off

The creator asked: "ask council for advice of useful materials and things we can use".
- **The question:** `council_tools_prompt_2026-11-21.txt` (the same text to both).
- **GPT:** https://chatgpt.com/c/6b021ff1-c330-83e9-8af1-4bb4e2448e14
- **Gemini:** https://gemini.google.com/app/227adb21dd7e96bc
Both answers were read in full. The specific claims were checked against the sources (below).

## Where they agree
- **Read first:**
  - Sutton and Barto, *Reinforcement Learning: An Introduction* (free online): planning, Dyna, models;
  - Stanley and Lehman (novelty search; *Why Greatness Cannot Be Planned*; POET);
  - Schmidhuber (curiosity as learning progress);
  - work on cultural transmission (GPT: Tomasello's cultural ratchet; Gemini: Bhoopchand et al., DeepMind, "Learning
    few-shot imitation as cultural transmission", *Nature Communications*).
- **Borrow tests, not frameworks:**
  - MiniGrid: FourRooms for detours, Memory tasks, dynamic obstacles;
  - Crafter: survival with an achievement ladder;
  - Melting Pot: social dilemmas, with fixed background populations as controls.
  Neither recommends moving to these frameworks; both say to port their tasks into our worlds.
- **Funding and compute come through a BMCC faculty mentor:**
  - the BMCC Foundation Fund for Undergraduate Research;
  - CRSP (the CUNY Research Scholars Program);
  - NSF REU summer programs;
  - (Gemini) CSTEP and NSF ACCESS with a faculty lead.
- **Where to show the work:** the artificial-life community (ISAL, the ALIFE conference); workshop papers; a short
  two-page brief with one result and one failure, not a pitch about a conscious mind.
- **Don't scale up yet.** No transformers, no PyTorch rebuild, no GPUs; diagnose planning against memory first.

## Where they differ, and what checking found
- **GPT:**
  - five controlled navigation tests (full map; perfect memory; learned memory; map changes; new layouts), with BFS
    and greedy baselines;
  - prioritized sweeping (Moore and Atkeson 1993) and Dyna before world models;
  - tools: pytest, Ruff, uv, joblib, MLflow later, OSF for preregistrations;
  - named Dr. Odaelys Pollard (BMCC Director of Research).
- **Gemini:**
  - the **successor representation** (Dayan; Gershman, Momennejad, Daw) as the best upgrade for detours: it separates
    the map's layout from where rewards are;
  - score the Bob Profile with a **geometric mean** (as Crafter does), so a zero in one ability cannot hide;
  - Animal-AI and PsychLab detour tasks from comparative cognition;
  - tools: **Numba** (10–100×), Hydra or OmegaConf, **rliable** (statistics for few seeds), Aim (local dashboards);
  - researchers: Brenden Lake (NYU), Lisa Soros, Anya Vostinar, Ken Stanley.
- **Checked (web, 21 Nov):**
  - **BMCC Foundation Fund:** $1,500 for one semester, 100 hours, faculty-mentored, 30 students a year (bmcc.cuny.edu).
    GPT was right; Gemini's $1,000 was wrong.
  - **Dr. Odaelys Pollard** is BMCC's Director of Research (Fiterman Hall F-1230F); Ayat Agha coordinates CRSP and the
    Foundation Fund (bmcc.cuny.edu, Student Research Opportunities).
  - **Oracle Always Free A1** was cut from 4 OCPU / 24 GB to 2 OCPU / 12 GB on 15 June 2026 (InfoQ, July 2026;
    Oracle's documentation). GPT was right, Gemini out of date, and so was the assistant's earlier advice. The
    project's paid E3 machine is not affected.
  - **Numba:** the assistant's own test on MoveVIN agrees with Gemini's claim. The planning loop was 21× faster for a
    single step (2.64 → 0.125 ms) and about 10× for a batch; the backward pass up to 140×; the results match
    (`D:\mindlab\workbench\W3p\explore\numba_mv.py`, run in a separate environment).

## The assistant's shortlist (the creator decides)
1. **The creator:** contact BMCC's Office of Research (Dr. Pollard) about a faculty mentor. One mentor opens:
   - the Foundation Fund (Spring 2027);
   - CRSP;
   - NSF ACCESS;
   - CUNY HPCC.
2. **The assistant:**
   - a Numba version of the new brain for the next studies;
   - a detour test suite from MiniGrid FourRooms and the animal detour task (with GPT's five controls);
   - the successor representation and prioritized sweeping as candidate brain parts after W3p;
   - rliable-style statistics beside the bootstrap;
   - a geometric-mean line in the Bob Profile beside the sum (the creator's floor rule already does this job).
3. **Later:** a two-page brief for the ALIFE community and BMCC's research symposium, once W3p has a clean result.
