# Tools that could help the whole project (research notes, 21 November 2026)

The creator, 21 Nov: "if there are other things that is helpful for our whole project we should get it so do research about other things".
What was read is labelled: **search results** means summaries from a web search, not the full pages. A tool suggests;
only a test on our own code decides.

## 1. Speed: Numba (free; the biggest lever)
- **Read:** search results (pythonspeed.com, apxml.com, analyticsinsight.net, and a population-based RL paper,
  arXiv 2206.08888).
- **What:** a compiler for Python loops over NumPy arrays. It helps most where loops run on small arrays, which is
  exactly our brains: 15 × 15 maps, 30 planning rounds per step, where NumPy's own overhead dominates. Sources report
  10–200× on such loops (to be measured, not assumed).
- **For us:** every W3 run takes 10–40 hours. A 5–10× faster brain would turn a 3-day study into an overnight one.
- **Caution:**
  - the numbers change in their last digits, so it is for **new** studies only (never mid-study);
  - determinism must be re-checked;
  - it must be installed in a **separate Python environment**, because installing it can change the NumPy version that
    the running, frozen studies use.
- **Next step:** a prototype of MoveVIN's planning loop in Numba, in a separate environment, measured against the
  current code (speed and agreement).

## 2. Big free compute through one professor (CUNY HPCC and NSF ACCESS)
- **Read:** search results (the ACCESS allocations policy page, allocations.access-ci.org; university guides).
- **CUNY HPCC:** CUNY's shared supercomputer centre (College of Staten Island) serves all CUNY colleges, BMCC included;
  students usually need a faculty sponsor.
- **NSF ACCESS:** national supercomputers, free for US research. Undergraduates cannot lead a request but can be users
  under a faculty or other eligible lead. Search results also mention streamlined paths for community colleges. The
  smallest tier ("Explore") is meant to be quick to get.
- **For us:** one BMCC professor who agrees to sponsor could unlock both: hundreds of cores, far more than our three
  machines.

## 3. Automatic off-site backups: rclone to Google Drive (free)
- **Read:** general knowledge (rclone is a widely used open-source sync tool); not researched further yet.
- **What:** a nightly copy of `D:\acl` and `D:\mindlab` history (git bundles) and key results to the creator's Google
  Drive, so no single machine or service can lose the work (the GitHub ban showed why).
- **Needs:** the creator authorises Drive access once, in their own browser.

## 4. Research papers: Zotero (free)
- **What:** collects papers (PDFs, citations) with one click from the browser, and links into Obsidian.
- **For us:** the "keep researching" rule produces many sources. Zotero keeps them findable, and the book's references
  follow from it.

## 5. Obsidian add-ons (now that Obsidian is set up)
- **Dataview:** live tables built from notes, for example every study with its status and main result.
- **Excalidraw:** hand-drawn diagrams inside notes (brain designs, world maps).
- **A 3D graph** ("Nebula", the creator's find): the vault as a star map.
- Install only through Obsidian's own Community Plugins browser.

## Not recommended
- GitHub Actions or Codespaces for running studies: against GitHub's terms, the reason Mind Lab was disabled.
- A second free account anywhere to get more compute: against the terms of GitHub and Oracle (one free account per
  person).
