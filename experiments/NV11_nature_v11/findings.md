# NV11 — Nature v11: people can hand a made thing to one another (adopted 31 October 2026)

**Adopted by the assistant under the creator's safe-path rule** (`CLAUDE.md`, 31 October 2026), every step met:
1. **a frozen study supporting the change:** HD1, final;
2. **an independent blind recompute** by GPT and Gemini: matched (`experiments/HD1_handing/recompute_hd1.md`);
3. **a confirmatory run on new seeds:** HD1-C, final, confirmed and recomputed
   (`experiments/HD1C_handing_confirm/findings.md`);
4. **both models consulted on adoption:** GPT 92%, Gemini 88%; the assistant's estimate 85%
   (`docs/gpt_view_adopt_v11_2026-10-31.md`);
5. **`code_v11`** with zero checks (`zero.txt`);
6. **reference hashes** regenerated, and the tests passing;
7. **a tag `nature-v11`,** a line in `docs/autonomous_decisions.md`, and a Telegram message.

The creator, on Telegram (31 October, 13:31): "I think that law is fine cuz it works in real life we give things to
other people and get from other people."

## What changed
- **The law (`hand_items` = 1):** the existing `give` action is generalized. A person may hand one made thing they hold
  to someone within reach who has room (fewer than 3 items), instead of food.
  - **The item handed** is the one with the highest net use: the receiver's gain over their own best for any use, minus
    the giver's loss.
  - **It is chosen** with give's own social weights times that net use.
  - Food giving still needs surplus and hunger; **handing needs neither.**
  - Same action, habit entry and cost. No reward, no relation change, objects conserved.
- **Four files:** `config.py` (the setting), `mind.py` (`hand_pick` and the option), `actions.py` (`_hand`) and
  `world.py` (a weekly transient note). See `v10_to_v11.diff` (116 lines).

## Checks
- **Zero checks** (`zero.txt`): all pass.
  - v11's code with `hand_items` 0 = `code_v10` (4 runs);
  - v11 = HD1's arm h (2 seeds);
  - the live package's defaults = v11;
  - the law acts;
  - reload is exact.
- **Tests:** 66 pass. The live reference hashes were regenerated (= v11); v11's set was added; v10's is kept.

## What it does (HD1 and HD1-C, 64 paired worlds)
- **Tools' share of adults' foraged food rises by about a third:** +0.36 and +0.25 points.
- **A tool is in hand in more forage weeks:** 11% → 16% and 10% → 14%.
- **Handings:** about 0.2 per adult-year.
- **No harm flag** in either run.

## Known limits (both models)
- **Small, not a breakthrough** (GPT): handing fixes access, not the choice to make. Most of TR1's 20% headroom stays
  unused.
- **Watch in the first study on v11:**
  - why handing stays rare;
  - who receives tools (children against working adults);
  - whether tools pool within close kin (Gemini);
  - whether they pile up in low-use hands.

## For studies
New studies use `code_v11`; v10 findings stay v10's. v10 stays in `experiments/NV10_nature_v10/code_v10`, so the
change can always be undone.
