# Council round 60: how should the shadow brain learn? (4 November 2026, about 21:40; corrected from an estimated "22:30")

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round60_question_2026-11-04.md`, with the episodic-memory research note.
- **The chats:** GPT, the main chat; Gemini `87f468c684ee5839`; DeepSeek `2552dbba-…`.
- **Recorded from the replies read in the chats.**

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| ranking | **A** (episodic), D (fix observation, needed regardless), B, C | **A** (92% to beat the table on unfamiliar cases), D, C, B | **A + D together** (about 72%; D about 65% as a companion), C about 55%, B about 50% |
| the gate | add a familiar-case safety rule: unfamiliar cases with an interval wholly above 0, **and non-inferiority on familiar cases** within a prespecified margin | "match the table on familiar cases and beat it on unfamiliar ones" | the same: familiar cases skill ≥ **−0.02** and unfamiliar cases with an interval above 0; A must not lose badly on food and materials |
| similarity and k | **k = 8**; compare only memories of the **same action**; weighted Euclidean distance on fixed physical ranges; feature groups get **equal total weight**; inverse-distance with a small stabiliser; **for exact familiar (situation, action) cases use the table mean**; a distance-to-nearest diagnostic | **k = 5** (larger k blurs distinct cases); Euclidean on inputs standardised with fixed spreads; **never learn the similarity online**; inverse distance, so an exact match dominates | **k = 15**, with 5 and 40 described only; held-thing properties and the action weighted more; leave out age band, sex and distance moved; inverse distance with a floor; outcomes stored standardised |
| observation | weight each observed week by 1 ÷ (visible examples that week), so a crowded week cannot swamp one's own; visible outputs only; failures kept | full weight 1.0: a memory stores events, so the batching flaw vanishes | 1 ÷ (number of weeks an entry summarises), one per observed week; plus a 0.5 arm (PB1's best), fixed in advance |
| a caution | a nearest-neighbour learner does **not** automatically equal the table on familiar cases; it needs explicit exact-key averaging | — | — |

## Checked and merged (the assistant as council)
1. **All three choose A (episodic memory), with D's principle built in.** Observation enters as memory entries, so
   no step size exists to blow up.
2. **The gate changes, and all three agree:**
   - **unfamiliar cases:** skill against the table with the interval wholly above 0;
   - **familiar cases:** non-inferior, with skill ≥ −0.02, the margin set now (DeepSeek's number, GPT's principle).
3. **Exact familiar cases use the table mean** (GPT's point, and it is right).
   - Nearest neighbours do not reduce to the table.
   - So the episodic predictor = the table's own mean when the (situation, action) pair has been lived, and the
     neighbours' weighted mean otherwise.
   - This makes it non-inferior on familiar cases by construction, except where observed entries are added. The gate
     then tests what matters: borrowing from neighbours.
   - **Caveat:** that makes the familiar half of the gate partly true by design. It still matters for the variant
     with observation, where observed entries enter the familiar cells too.
4. **k: the three disagree (5, 8, 15).** Frozen choice: **k = 8** (the middle; GPT's), with k = 5 and k = 15 described
   only, never chosen on.
5. **Similarity:**
   - **only memories of the same action** (GPT);
   - weighted Euclidean distance on the PB1 inputs, each scaled by a fixed physical range (the inputs are already
     0–1);
   - feature groups (body, setting, tile, held things, target) get **equal total weight** (GPT);
   - age band, sex and recent actions are left out of the distance (DeepSeek);
   - inverse-distance weights with a stabiliser of 0.05;
   - nothing is learned online (Gemini).
6. **Observation variants:**
   - **E-obs:** observed weeks at weight 1 ÷ (visible observed weeks that week), GPT's and DeepSeek's principle;
   - **E-obs-0.5:** a fixed 0.5 each (PB1's best), described.
7. **Kept from PB1:** the cases, outputs, visibility masks, worlds design and per-output reporting. **The table and
   L-obs-0.5 are rerun beside it** as references.
