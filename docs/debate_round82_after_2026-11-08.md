# Council round 82: the neural brain's design (8 November 2026)

The question and the follow-up: `docs/debate_round82_question_2026-11-08.md`. Each answer is that model's opinion, not
sign-off.

**GPT's opinion, not sign-off** (fresh chat https://chatgpt.com/c/6af0b162-a710-83e9-9295-debce0712776):
- (a) Start B, with u as a temporary scaffold. "never reward genomes for reducing that coefficient. Let survival and
  reproduction decide". Run A as a separate arm.
- (b) Targets stay rule-based.
- (c) REINFORCE with a baseline, dw = eta (r − b) grad log pi. Episodic memory in NB2.
- (d) 1,000 years.
- (e) Separate the questions: does it survive, does it learn, does it evolve? The strongest test: "Freeze genomes from
  generations 1, 20, and 40. Put them into identical fresh environments with learning enabled and disabled."
- (f) "Hidden intelligence in the scaffolding". Learning instability. Averaging parents' weights "can destroy useful
  neural configurations".
- (g) 85% valid; 50% viable without permanent dependence on u; 25% measurable improvement across generations.
  "A brain is not autonomous merely because its decisions come from neural weights."

**Gemini's opinion, not sign-off** (ACL chat):
- (a) B: "pure random weights (A) will result in a 100% mortality rate in generation 1". It proposed making the
  u-reliance gene "metabolically costly".
- (b) Targets stay rule-based.
- (c) Three-factor Hebbian; no episodic memory yet.
- (d) 1,000 years "a bare minimum"; 3,000+ for "definitive evolutionary divergence".
- (e) A lifespan slope from generation 10 to 40, with g decreasing.
- (f) A local optimum where the network never beats u: "the illusion of an emergent brain".
- (g) 80%.

**DeepSeek's opinion, not sign-off** (ACL chat):
- (a) B, with the u-gene as a co-primary readout. A's restart "is artificial selection no ACL law contains".
- (b) Targets stay rule-based.
- (c) Three-factor Hebbian, plus an evolution-only arm (learning rate 0); memory in NB2.
- (d) 1,000 years; check stationarity and cost.
- (e) Primary: the within-world trend across generations of survival to 16 per birth and adult lifespan. Readouts:
  u-gene, the network–u correlation, entropy, genetic variance.
- (f) A decorative network; scale mismatch; neutral drift.
- (g) About 70% with B.

## The follow-up and the replies
The follow-up proposed:
1. no cost on g;
2. REINFORCE with a baseline, plus the evolution-only arm;
3. a child inherits one parent's whole genome;
4. GPT's common garden plus DeepSeek's trend as primaries;
5. 16 seeds × 1,000 years, with v17 / n / e.

The replies:
- **GPT:** "No objection, provided the common-garden comparison uses matched conditions and learning-on versus
  learning-off controls".
- **Gemini:** accepts (1), "making the g gene metabolically costly violates the strict 'no outcome pushing' rule"; (3);
  and (5). On (2) it began drawing a diagram and raised no objection.
- **DeepSeek:** "No objection to (1)–(4) … REINFORCE-with-baseline is the correct three-factor rule." It flagged that
  16 seeds leave the guards underpowered:
  - make the within-world trend primary;
  - keep the guards descriptive until powered.
  - **Taken.**

## Decision
NB1 is frozen with the resolved design (`experiments/NB1_neural_brain/questions.md`).
