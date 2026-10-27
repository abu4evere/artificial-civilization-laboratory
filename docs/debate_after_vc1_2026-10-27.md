# Debate round 12 (27 October 2026, sleep mode): after VC1, which first? (opinions, not sign-off)

**The same question to GPT (main chat) and Gemini (ACL session); Claude as council.**

**The candidates:**
- **(C)** Expected SARSA (a nature change);
- **(F)** a copying-rule change (a nature change);
- **(G)** a read-only calibration ledger;
- **(E)** a read-only exploration audit.

## Answers
- **GPT: (G), 80%.** "Neither intervention is sufficiently targeted yet."
  - HL1's 0.41 copying share "measures habit growth, not calibration error".
  - Record each update's route and its effect on the gap between predicted and experienced returns.
  - **Caveat:** "distinguish exact accounting of value changes from causal attribution: copying alters later choices
    and TD updates".
  - Order: G, E, then F or C by G's results. "Do not change Nature yet."
  - Its prediction: "copying amplifies common-action overvaluation while sparse experience sustains making's
    underestimation".
- **Gemini: (G), 95%.** Intervening before knowing the route "violates the diagnostic-first protocol".

## Council
- **Both choose (G).** GPT's caveat is written into CL1 (the split is accounting, not causal).
- **Gemini again called the method "deterministic replays".** It is a read-only observer on 32 new worlds, with zero
  checks proving it changes nothing (already corrected in round 9).
