# IW1 — How does the worth of made things form? Findings (not final until GPT and Gemini recompute)

Frozen as `IW1-frozen` (operational note 1). Signed off by the assistant under sleep-mode autonomy (read-only; GPT 75%,
Gemini 85%; debate round 33). Run on GitHub Actions (run 41180403699, `skip_zero=local`). 32 worlds on nature v9
(seeds 20901–20932), LP (80 founders, 80 × 80), 200 years. Every number comes from `analyse_iw1.py`, written before
data; full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v9`);
- every worth update and every offered make's score replays exactly (mismatches 0).

**Population beside it:** no world died out. Mean living population 119.9; 81.0 adults per world-year in years
100–200. 17,094 makes by adults in years 100–200; 8,784,929 adult weeks with making offered but not chosen; 10,189,353
uses of made things in all.

## The answer

**People know what made things are worth. The things are simply worth modestly.** The frozen reading is **"mixed"**:
- worth is learned, so it is not "unlearned";
- but the help is above the 0.10 bar for "honest low".

### Q1 — Calibration at the make (primary)
- **Under-valuation against everyone's uses of the kind: +0.004 [+0.002, +0.006].** At the moment they make a thing,
  people's worth for it is within a few thousandths of what that kind really gives.
- **The kinds made help by 0.163 [0.160, 0.166] per use:** a job made about 16% easier.
- **Against the maker's own later uses:** +0.009 [+0.008, +0.011] (599 makes had no later use).
- **By how the maker first got the kind:**
  - made or invented themselves: +0.000;
  - taught: +0.023;
  - read from marks: −0.024.

### Q2 — Experience
- **88.5% of makes come after 6 or more uses** of that kind.
- **Only 11.5% [10.1%, 13.2%] rest on fewer than 6.** So worth has had time to be learned (the frozen bar for
  "unlearned" was more than half).

### Q3–Q8 (described)
- **Q3, the zero start is real but short-lived.** A kind someone invents starts at worth 0 against a help of about
  0.13. Worth reaches the help after about 10 uses, and by then most uses have happened (5.3 million of 5.8 million).
  Taught kinds start nearer (0.08 against 0.18).
- **Q4, help is modest everywhere.**
  - Tool use: 36% of uses help by 0.1 or less, and 14% by more than 0.3.
  - Floats help most (58% above 0.3).
  - 62% of all uses help by more than 0.1.
- **Q5, the memory limit pushes out kinds before they are ever used.** 135,262 person-kinds left through the 12-recipe
  limit without ever being used by that person (PG0 found the same on v7). Only 771 helpful ones left that way. At
  death, 77,365 helpful kinds go with the dead.
- **Q6, people do not make the most helpful kinds.** The rank correlation of how often a kind is made with how much
  it helps is **−0.091** on average (all 32 worlds between −0.137 and −0.039).
- **Q7, offered but not chosen** (GPT): the same picture. Under-valuation +0.015 [+0.013, +0.017]; mean help 0.152;
  81% of these weeks after 6+ uses.
- **Q8:** when making is offered, its worth comes from the thing's own worth 81% of the time, and from its worth as a
  part 18%. Belief and surprise hardly count.

## Against the prior (the assistant's, frozen)
1. "Mixed, leaning unlearned": **"mixed" right, "leaning unlearned" wrong.** Worth is well learned.
2. "Mean felt help per tool use is modest (0.1 to 0.3)": **right** (0.163).
3. "Invented kinds are the most under-valued at the make": **wrong** (+0.000; taught kinds slightly more, +0.023).

**Gemini's concern** (the zero start makes self-made kinds "dead on arrival") is real in the first uses but gone by the
time people make things. **GPT's caution** (six uses is a diagnostic bin) is borne out: most makes are far past it.

## What it means
- **The learning of worth is not the bottleneck.** People value made things about right.
- **Made things help modestly** (about 16% easier), while food and gathering pull hard every week (CO2). So making
  loses at the choice **because, in today's world, a made thing is worth little against food.** That is the creator's
  third goal, "a world where knowing matters", now with numbers: **tools give too little to do**.
- **Two smaller leaks:**
  - the 12-recipe memory throws out many kinds before their first use;
  - people do not make the kinds that help most (−0.09).
- **What follows, by the frozen branch for "mixed":** report both. For the creator and the next debate: whether
  "knowing matters" should be studied as a world question first, by measuring where tools could matter more (which
  tasks, which seasons), before any law makes anything harder or more rewarding. Per the creator's order, measure
  first.
- **No change to nature** follows from this study by itself. It ran on v9; nature v10 (ageing) changes how long people
  live, not how made things help.

## Independent recompute
Pending: GPT and Gemini, each in a fresh chat, from `recompute/iw1_one_file.csv` (per-world sums from the raw output).
Recorded only from their actual replies.
