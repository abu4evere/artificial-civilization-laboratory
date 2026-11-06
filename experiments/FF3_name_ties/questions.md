# FF3: Memory ties settled by name, a fault fix in nature v13 (frozen plan)

**A fault-fix check in a copy, not a new law** (the third round, after FF1 and FF2).
- **The copy:** `code_ff3` = `code_v13` + one setting, `fix_name_ties`. With 0 it is v13 exactly.
- **The authority:** the creator, 2 November 2026: "I give you permission to edit world rules. Take a look and check
  all rules. If you find something fix it or add any new rules. From now on keep working without me".
- **The sources:**
  - VA1's appended note (`experiments/VA1_value_at_invention/findings.md`): 129 of 130 tied new kinds were lost by
    name order;
  - the design draft and the exploratory tie count, `docs/ff3_design_draft_2026-11-05.md`;
  - council rounds 66 (`docs/debate_round66_after_lh1_2026-11-05.md`) and 67
    (`docs/debate_round67_after_rf1_2026-11-06.md`). All three models call it a fault and put FF3 first. GPT's split
    is adopted: the fault fix is a name-free draw; "the longest-unused is forgotten" is a separate law, for later.

## The fault (the code does not do what its own rule says)
When one of four memories is full, it drops `min(memory, key=(value, key text))`. The written rule is "the least
valued is dropped" (`docs/ODD_v11.md`). On a tie in value, **the key's text decides**, which is no part of that rule.

| memory | place | the key that decides a tie | exploratory share of evictions decided by the tie (one world) |
|---|---|---|---|
| recipes (12) | `knowhow.remember_recipe` | the kind's name; more nested kinds sort first | 64% |
| known marks | `marks._link` | the shape | 34% |
| records of sources | `information._note` | the person's id; older people sort first | 15% |
| puzzles | `inquiry.notice` | "m:" or "f:" + the kind's name | 9% |

Known places never tie (0 of 171,922 in that world) and are left as they are. Items already break ties by the order
held, not by name.

## The fix (setting `fix_name_ties`)
- With 1, when the minimum value is shared, the item dropped is **drawn uniformly among the tied ones**.
- The draw comes from **a stream of its own**: `random.Random(s)`, where `s` is an integer made only from:
  - the world's seed;
  - the week;
  - the person's number;
  - the memory's number (1 to 4);
  - the memory's size.

  It never touches the world's generator, so no other random draw in the world moves because of the fix itself.
- The tied items are put in a fixed order before the draw. Each tied item is equally likely, whatever its name and
  whenever it was learned.
- **Unchanged:** which items are at the minimum, the memories' sizes, and everything else.

## Arms (32 paired seeds 23901–23932; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
| arm | setting | |
|---|---|---|
| **v13** (c) | `fix_name_ties` 0 | = `code_v13` (shown by the zero checks) |
| **f** | `fix_name_ties` 1 | the candidate nature v14 |
| **sham** (x) | 0, with `sham_draw` 1 | |

## Decision (frozen): a check for harm only (FF1's and FF2's rule)
- **Guards** (f against v13):
  - **population:** living-weeks in years 100–200, f ÷ v13 below 0.90 with the upper bound of its 95% interval below
    1;
  - **extinctions:** 3 or more worlds beyond v13's.
- **Intervals:** a paired world bootstrap, 10,000 replicates, NumPy seed 20261121. The same drawn seeds are used for
  every arm.
- **Reading:**
  - **"No harm"** if neither guard is raised. f is then adopted as **nature v14**. A fault fix restores what the rule
    says; it is not a new law, so there is no confirmatory run (as FF1 and FF2).
  - **"Harm: investigate"** if a guard is raised. The cause is found and appended first. The fault is not simply kept.
- **Flag for investigation** (not a stop): if, for f against v13, any described measure below has a ratio outside
  [0.8, 1.25] with its 95% interval wholly outside 1, a read-only explanation is written before adoption. Adoption then
  goes ahead unless the explanation finds harm.
- **The sham:** sham − v13 is shown beside every contrast, for scale.

## Described (not decisive), per arm and as f and sham against v13
- **The fix at work** (a log the code writes at each eviction; read by nothing in the world), per memory:
  - evictions;
  - evictions with a tie;
  - and, for recipes, how often the newest recipe was the one dropped.
- **Kept at birth:** among recipes that enter a full memory, the share kept to the week's end.
- **Kinds:** world-new kinds; remade kinds (made again by their inventor within 5 years, AF1's lineage rule, as in
  VA1); makes per adult-year.
- **Population:** living-weeks and adult-weeks.

## Validity (hard stops)
- **Zero checks:**
  - `code_ff3` with 0 = `code_v13` (state and random numbers, 20 and 60 years);
  - the observer and the log are read-only (the same state with and without them; c and f);
  - the sham acts;
  - the fix acts where its log shows a tie (the state then differs from v13's). If no tie is logged in these runs,
    "not triggered" is reported; that is not a failure;
  - reload is exact (arm f, saved at year 10, continues exactly to year 15);
  - **unit checks:**
    - in an f world (30 years), every eviction drops an item whose value equals the memory's minimum;
    - the draw leaves the world's generator untouched (its state is the same before and after each draw, checked at
      every eviction in that world);
    - over 30,000 draws for a synthetic three-way tie (one plain kind, one nested, one strike recipe), each item is
      drawn between 0.31 and 0.356 of the time;
    - the same `s` gives the same pick whatever the order the items are given in.
- **All 3 × 32 worlds** are present under one `code_ff3` fingerprint.
- **A smoke run** before the cloud.
- **A blind recompute** by GPT, Gemini and DeepSeek, from per-world counts, of:
  - the population ratio f ÷ v13 and its interval;
  - the extinction difference;
  - the reading.

## Adoption (if "no harm")
1. `code_v14` = `code_v13` with `fix_name_ties` defaulting to 1.
2. **Zero checks:** v14 with 0 = `code_v13`; v14 = FF3's arm f.
3. Reference hashes regenerated; the tests pass.
4. Tag `nature-v14`, a line in `docs/autonomous_decisions.md`, and a Telegram to the creator.

## The assistant's prior
1. **No guard raised** (about 90%).
2. **Recipes:** the newest kind is kept at birth much more often, because it no longer loses every tie.
3. World-new kinds and makes change a little, likely flagged and explained. Remaking stays near 0: RF1 found that
   pursuit fails, and that most inventors are children.

## Sign-off (6 November 2026)
The assistant, under the creator's 2 November permission to edit world rules, and sleep-mode autonomy (the creator's
last message: "keep working"). Council rounds 66 and 67: all three models call it a fault and
put FF3 first (GPT 97%, Gemini 95%, DeepSeek about 90%). The assistant 88%. Frozen as `FF3-frozen` before any code or
data.
