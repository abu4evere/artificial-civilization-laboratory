# Debate round 41 (1 November 2026, sleep mode): after UV1, what keeps the floor? (opinions, not sign-off)

**The same text to GPT (fresh chat `6ae78ac5`) and Gemini (fresh chat `e54b7e1f240ad7a4`); Claude as council.** Three
steps. The facts given are from `experiments/UV1_undervaluation_by_experience/findings.md` and the code.

**The options:**
- **A:** read-only. Does the floor vanish when the next choices are well practised? This tests **propagation**: a
  practised habit's target uses the values of the next choices, which may still be start-lagged.
- **B:** read-only. Does G vary with finer state within situations (state aliasing)?
- **C:** read-only. Children: the carer's pull against their own learning.
- **D:** the queued handing audit.

## Step 1: which first?
- **GPT: A, 88%** ("95% valid read-only design, 80% diagnostic ability, 99% preservation of ACL's rules").
  - Weight by the real choice probabilities.
  - Condition on k, age, situation and year.
  - "Do not interpret a smaller bias among experienced next options as proof of propagation; experience may correlate
    with better circumstances."
- **Gemini: A, 95%.**
  - **Council: two claims were wrong.**
    - It said A uses "existing UV1 replay data". UV1's output does not hold the next options or their experience, so
      a new replay is needed.
    - It called A "a definitive diagnostic". It is observational (GPT's point).

## Step 2: the one-step design (U = the next decision's choice-probability mass on unpractised options)
- **Corrections sent to Gemini**, with GPT's weighting adopted.
- **GPT: accept, 93%.** "Propagation" would mean "evidence consistent with propagation, not causal proof".
- **Gemini: accept, 96%.**

## Step 3: a flaw the council found in its own design, and the fix
- **The flaw:**
  - At a steady state, B_t ≈ 0.8 × the choice-weighted bias of the next options.
  - Practised next options carry the floor themselves, sustained by *their* next options.
  - So B(U < 0.1) ≈ 0.8 × F, still below −0.05. The rule would say "not propagation" even if propagation were the
    whole cause.
- **The fix:** discounted exposure over the same future that G uses, D_t = Σ_j 0.8^j U_(t+1+j), accumulated in the
  observer exactly as G is.
- **GPT: "Your objection is correct"; accept with one change, 91%.**
  - Match the discount clock to G's: per habit update, the same closing.
  - "Normalize using the actual accumulated discount weights rather than a fixed 0.2 if the trajectory terminates
    early". **Adopted:** Dn = D / W, with W = the summed weights actually accrued.
- **Gemini: accept, 98%.** "Your objection is entirely correct." It called the result "a clean, unconfounded test".
  **Council: that overstates it.** It remains observational (GPT).

## What survived checking
- **UV2:** a read-only replay of ES2's r arm on its 32 seeds.
- **Primary:** the signed bias for practised habits (k ≥ 80, ages 16–44, not death-closed) when the discounted future
  exposure to unpractised options is low (Dn < 0.1).
- **Reading:** "propagation", "not propagation" or "mixed", by a frozen rule, with a coverage guard.
- **Secondary:** the dose-response by Dn bins, the one-step U, year quarters (cause 3) and age.
- **Estimates:** GPT 91%, Gemini 98%; **the assistant 75%** (the new exposure bookkeeping is the main risk; the zero
  checks and a replay match against ES2 guard it).
