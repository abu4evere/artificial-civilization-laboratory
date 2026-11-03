# Council round 52: measuring autonomy before redesigning action (2 November 2026, about 22:30 New York)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/autonomy_measures_draft_2026-11-02.md` (attached), with the same text to all three.
- **The chats:** GPT, the main chat; Gemini 3.1 Pro, `d5ecc8b87be7ae89`; DeepSeek, `2552dbba-6c74-4cc4-b613-2228b137c47f`.

## First answers (summarised; key sentences quoted)
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| M1–M5 | "a sound initial diagnostic battery, but not yet a measure of genuine autonomy"; each has a confound (M1: resources, location or habits; M3: immediate opportunity; M5: recurring needs) | "highly sophisticated" | "a sound first set and correctly separated by level" |
| what is missing | **M6, adaptive transfer:** a sequence used successfully where its original cues are absent. Defines new capability as "an agent-generated, executable action or operator not already represented in the available action grammar" | **M6, cross-domain composition:** an action applied to a category of target never targeted before | **M6, decomposition:** whether a new act is new in steps or new only in arrangement |
| "more chance" as a control | "not a valid less-autonomous control by itself": a stochasticity control. Do not require every measure to exceed every control; freeze positive and negative controls; report failures rather than discard | "an essential control"; it shows the measures capture "structured intentionality, not just stochastic drift" | fair only as a one-sided detector: it should lower M1, M3 and M5, but may raise M2 and M4 |
| when to run | start on v11 now; repeat the same scorecard on v12; never use v11–v12 differences to redefine success | **wait for v12**: FX1 changes recipe choice and item retention | start on v11 now; repeat on v12 |
| estimate | 88% | 93% | about 90% |

## The merged design (sent to all three)
1. **Timing:**
   - freeze the measure definitions now;
   - run them on v11 now. Validating the measures against the controls is about the measures, not the baseline, and
     it debugs the observer while FX1 runs;
   - run the identical frozen battery on v12 as the baseline for any redesign;
   - never use v11–v12 differences to redefine success.
2. **Directional validation, frozen per measure:**
   - **no learned habits** is expected to lower M1, M3 and M5;
   - **fewer acts** is a sanity check only (M3 must be 0 there);
   - **more chance** is a stochasticity control, expected to lower M1, M3 and M5 and allowed to raise M2 and M4;
   - a measure that fails its frozen prediction is reported as **not validated**. It is not used to judge a redesign
     until it passes later.
3. **Opportunity-matched baselines for M3 and M5:** weeks in which the same inputs were reachable but not gathered.
4. **M6:**
   - **M6a, decomposition:** whether a new act is new in steps or only in arrangement. Cross-domain composition is its
     strongest case.
   - **M6b, transfer:** an established sequence used where its original cues are absent.
   - New kinds of act stay at 0 by construction in v11.

## Final answers
- **GPT: 94%.** "Yes, I support the merged design". Its remaining concern is that the controls keep comparable
  opportunities, and that M6 truly tells flexible composition from familiar sequences.
- **Gemini: 97%.** "I fully support this merged design". It says the plan "resolves the timing conflict without
  contaminating future redesigns".
- **DeepSeek: about 92%.** "Support: yes". The identical v11→v12 re-run "removes my main remaining baseline risk".

## Next
A frozen plan, `experiments/AM1_autonomy_measures/questions.md`, is to be written in the merged form. It runs
read-only on v11 now and identically on v12 later.
