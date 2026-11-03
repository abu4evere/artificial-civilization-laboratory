# Council round 57: PB0's design (3 November 2026)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/pb0_design_draft_2026-11-03.md` and its four open questions. Each model was also asked for an
  estimate that a frozen version would be valid and decisive.
- **The chats:** GPT, the main chat; Gemini `87f468c684ee5839`; DeepSeek `2552dbba-…`.
- **Recorded from the replies read in the chats.**

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| estimate | none given; "if resources permit only one replay per option, label PB0 exploratory rather than decisive" | 85% | about 80% after the control is fixed; about 55% as drafted |
| 1. horizon | keep H = 1 and 4; add H = 26 on a smaller frozen sample, secondary. A four-week replay with habits after week 1 is not a planner. | 1–4 weeks is not enough; add H = 26 on a smaller, stratified sample | add H = 13 and 26 on about 80 decisions a world, described only; a forced multi-week plan (goal-holding) is a separate study |
| 2. outcome | r primary, since PB0 asks whether prediction could improve the current decision system; food, health and survival reported as checks; no composite | food, health and survival primary: r weighs scripted mood | r primary (the learner's real objective); report reward and mood apart, and flag gains that come from mood |
| 3. K | K = 6 plus the chosen option for the main sample; **all** options on a smaller sample, reporting how often the full-menu winner lies outside the top six; tell the top-scored option apart from the softmax pick | K = 6 is enough (softmax at 0.2 concentrates the choice) | K = 6 biases S downward; evaluate all eligible options (up to 19), or report top-6 as a lower bound with a tail sample |
| 4. go/no-go | **reject S against shuffled.** High disagreement is not evidence, and taking the best of noisy outcomes creates a winner's curse. Instead: several replays per option with common random numbers; **pick the oracle's winner on one set of streams and test it against the baseline on independent held-out streams**; world bootstrap; GO = held-out gain with its 95% interval above 0, plus a pre-set minimum (for example ≥ 5% of mean absolute return); S descriptive | G must exceed 1.5–2 × the noise SD | **the shuffled control is inverted:** with outcomes permuted, the oracle picks almost at random, so the shuffled S ≈ 1 − 1/K ≈ 0.86; the real S can never beat it by 10 points, and the rule would say NO-GO mechanically. Fix: G primary against a permutation null; S as a regret share (gain above one noise SD) |

## Checked (the assistant as council)
- **DeepSeek's catch is right.** With K + 1 options and outcomes permuted at random, the oracle's pick matches the
  top-scored option about 1/(K + 1) of the time, so the shuffled S is about 0.86. The drafted rule could never say GO.
  It was the assistant's error.
- **GPT's winner's-curse point is right as well.** Choosing the best of 7 noisy outcomes and measuring its gain on the
  same streams overstates the gain, even when all options are equal. Selecting on one set of streams and testing on
  held-out streams removes that bias. It also answers DeepSeek's concern more cleanly than a permutation null.
- **Outcome:** two of three say r primary. Gemini's point (r includes scripted mood) is met by reporting the reward
  and mood parts apart, and food, health and survival as checks (DeepSeek, GPT).
- **K:** a smaller all-options sample settles whether the top-6 truncation matters (GPT, DeepSeek).

## The revised design (to be frozen as PB0's plan)
1. **Replays:** for each sampled decision, each option is replayed R = 4 times. Each replay index has its own
   common-random stream, shared across options.
2. **Selection and test:**
   - the oracle picks its winner on streams 1–2;
   - its gain over the top-scored option is measured on streams 3–4 (held out).
3. **Primary: the held-out gain G** in r at H = 4, with a world bootstrap.
   - **GO** if its 95% interval is wholly above 0 **and** G ≥ 5% of the mean absolute r over 4 weeks.
4. **Described:**
   - S as a regret share (held-out gain above one noise SD);
   - H = 1;
   - H = 13 and 26 on a small sample;
   - r split into reward and mood;
   - food, health and alive at H;
   - all options on a small sample;
   - by decision kind.
5. **Labelled exploratory** if the cost forces R below 4.
