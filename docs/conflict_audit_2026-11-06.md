# Why ACL looks so peaceful: a read-only audit of the conflict rules (6 November 2026)

Asked by the creator on Telegram, 17:30: "for me their life looks too peaceful ... i am feeling like you giving
restrictions for some of their actions and behaviors". Read-only; nothing in nature changed.

## What the records say
LH1 (`experiments/LH1_fair_lookahead/findings.md`, v13, 32 worlds, years 100-200): deaths by killing 2, by starvation
2,029, by thirst 1,076, by illness 1,931. Killing 0.0045 per 1,000 living-years. Stealing 0.144 per 1,000 acts.
People die of hunger quietly far more than they fight.

## Where the doorways to conflict are narrow (acl/mind.py, acl/actions.py, nature v14)
1. Attack needs a grudge first (`mind.py:487`, grudge > 0.15). A grudge comes only from harm already done (theft,
   attack, killing of someone loved: `actions.py:825,861`, `social.py:63-67`). So the first harm can only be a theft.
   Hunger, rivalry, a contested animal, a mate or a place never lead to a fight directly.
2. Stealing has a fixed cost subtracted (`mind.py:483`, `u -= 0.25 + 0.4*fear`), needs hunger > 0.3, the other holding
   more than 4 food, and no kin; it takes only food, never tools or made things.
3. No contest over a shared hunt: people hunting the same place become one party and split the meat evenly.
4. No rivalry in courting, no defending a place or a stash before it is taken, no threat or display short of a blow.
5. Each fight is one on one; there are no sides (no "war", "coalition", "faction" in the code; checked 6 Nov).
6. LH1 arm m (a longer look-ahead) raised killing from 2 to 116 deaths: the short look-ahead also holds conflict down.

## Reading (the assistant's, not a finding)
These gates were written by hand when nature was built. They are outcome-shaped (violence only as revenge), which the
creator's rules warn against. A general law would let any act that takes or keeps a scarce thing (food, meat, items,
a mate, a place) be weighed by the same need/temper/strength terms, with retaliation following from the physics.
Real forager violence rates: not checked in this audit (to research, with sources, before any study).

## Next step proposed
Council (GPT, Gemini, DeepSeek) on one general law, then a frozen test in a copy with a sham, as with every rule change.
Not started; waits for CI1-C to finish.
