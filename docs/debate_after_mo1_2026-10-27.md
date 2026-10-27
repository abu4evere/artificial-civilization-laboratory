# Debate round 11 (27 October 2026, sleep mode): after MO1, which first? (opinions, not sign-off)

**The same question to GPT (main chat) and Gemini (ACL session); Claude as council.**

**The candidates:**
- **(B)** a read-only value-calibration audit;
- **(C)** an Expected SARSA nature study;
- **(E)** a read-only exploration audit.

## Answers
- **GPT: (B), 75%.** "MO1 must remain not supported; its improved retention does not justify changing the frozen 0.90
  threshold or adopting v8."
  - **A correction to the design:** "max-bootstrap TD estimates a different target from the returns agents actually
    experience under their current behavior. Therefore, disagreement with realized returns alone does not prove
    miscalibration." Compare under the behaviour policy and the max target separately, stratified, and report poor
    coverage for making.
  - Order: B, E, C.
  - Its prediction: "reasonably consistent values for frequently performed actions but weakly supported estimates for
    making".
- **Gemini: (B), 95%.** Running (C) first "violates the diagnostic-first protocol". (E) quantifies the softmax's tail
  suppression "without identifying whether the q-inputs feeding into that softmax are fundamentally distorted".

## Council
Both choose (B). GPT's correction is adopted:
- the realised return G and the max gap (0.8 × (max q[s′] − q[s′, a_next])) are measured separately;
- make's coverage is reported beside every make number.

**The assistant's estimate is 65%,** lower than both models': realised returns depend on what else people do afterwards,
so the reading may be less decisive than they expect.
