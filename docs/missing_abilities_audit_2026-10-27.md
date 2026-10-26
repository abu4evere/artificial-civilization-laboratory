# Missing abilities: a read-only audit of nature v7 (27 October 2026)

**Asked by the creator:** "can you check whole code if there are other such places where we missed some features like
that. Cuz these features might be main problem." Written in sleep mode. **Nothing is changed or proposed for freezing.**
Each item is a candidate for the creator, to be weighed with GPT's and Gemini's views and the evidence. Any change to
nature would be one law at a time, frozen, with a control, a sham and zero checks.

**Method:** Claude read every action handler (`actions.py`), the decision (`mind.py`), teaching and watching
(`information.py`, `knowhow.py`), childhood, feeding, death and bodies (`biology.py`) and things (`matter.py`) in
`code_v7`. It looked for one-sided rules: something that exists for food but not for things, or that one route allows
and another doesn't. One measurement was taken in a 30-year smoke world (seed 9957, not study data).

## A. Made things

| # | what is missing or one-sided | where | why it may matter |
|---|---|---|---|
| A1 | **A living person cannot give a made thing** to anyone. "Give" moves food and seeds only. | `actions._give` | No child holds a tool someone else made (LS1: 1.3% of tools used). Children cannot learn a tool's worth by using a good one. |
| A2 | **Made things cannot be put down, left or stored anywhere.** Tiles hold only food stashes and materials. A made thing exists only in a hand or with a body. | `actions._put`, `world` tiles | No caches, no tools left at a camp, nothing found later by others (cf. capuchin anvils, crows using parents' tools). |
| A3 | **Made things cannot be taken or stolen** from the living. "Steal" and "take" move food only. | `actions._steal`, `_take` | Things never circulate, even by force. |
| A4 | **Hands hold 3 made things; a fourth deletes the least valued, and on a tie the newest.** A new kind made in play has worth 0, so with full hands it is often deleted the same week, never used and never valued. **Measured:** 447 of 2,977 things made in play (15%) were gone by the end of their week, 439 of them new kinds with worth 0. | `actions._keep` | Worth is learned only by use. A new invention deleted at once can never prove itself, which may feed the "novelty freeze" seen since E5. |
| A5 | **Inheritance only on the spot:** a partner, or a child aged 12+, on the same tile. Otherwise the things stay with the body, where only those same people can take them. | `biology.die`, `bodies_week` | Most tools at death are probably lost (TF1 will measure). |

## B. Materials

| # | what | where | why it may matter |
|---|---|---|---|
| B1 | **Materials put on a pile can never be picked up again** by anyone. Gathering reads only the land's own materials; piles only give warmth or burn. | `actions._gather`, `world.material` | Piles work as building but not as stores. Nobody can lay in flint for later, or share it. (Possibly intended; to check with the creator.) |
| B2 | Materials cannot be given. | `actions._give` | As A1, for the raw stuff of making. |

## C. Learning from others

| # | what | where | why it may matter |
|---|---|---|---|
| C1 | **Watching** (working out a recipe by seeing it used) happens in only two situations: hunting together, and seeing someone come ashore on something that floats. **Nobody learns by watching someone make something, or forage with a tool.** | `knowhow.watch`, called only from `_hunt` and `_over_water` | LS1: the "copied" route was 1.1 → 0.0 per 1,000 person-years after year 20. Observation, the main route for forager children and for other primates, is almost shut. |
| C2 | **Teaching is only a side effect of talk.** Nobody can choose to show or teach; in each talk the teacher offers one of their top three valued things (worth > 0.15). | `actions._talk`, `information.show_how` | Teaching cannot be aimed (at a child, a skill, a moment of making). Lessons come without the thing in hand unless the teacher happens to hold the materials. |
| C3 | **Making is always solitary:** no making together, helping, or apprenticeship. Hunting is the only joint work. | `actions._make`, `_play` | No route where a novice practises beside a skilled maker. |
| C4 | Habit learning copies whole habit tables in talk (TC1, BL0: about 57% of habits copied). | `actions._imitate` | Known; may wash out individual learning (fly-brain gap 4). |

## D. Childhood

| # | what | where | why it may matter |
|---|---|---|---|
| D1 | **Care, and being fed by a carer, ends at 12.** At 12 children "fend for themselves". Forager children are net consumers well into their teens (Kaplan et al. 2000, to check), which pays for a long, unproductive time of learning. | `biology` (caregiver cleared at `CHILD_END` = 12 years) | ACL's teens must feed themselves from 12, so foraging wins and practice at making has no subsidy. This fits LS1 (skill at 16 falling by cohort) and MK1's question. |
| D2 | Children under 12 cannot make deliberately, only play (deliberate making starts at the teen stage, 12). | `mind.decide` (`grown`) | Probably fine; play is their making. Noted for completeness. |

## E. Valuing

| # | what | where | why it may matter |
|---|---|---|---|
| E1 | A thing's worth is learned **only from one's own use** (or a little from watching a hunt). Being told helps credence, not felt worth. | `knowhow.judge_item` | With A1–A4 and C1, someone who never holds a good tool never learns what it is worth. |
| E2 | Making's score counts one use's gain, not what owning the tool gives over time (debate round 1). | `mind.decide` | Being tested in MK1 ("delayed-benefit failure"). |

## How these connect

LS1's chain was: people don't choose to make → they don't practise → tools vanish → the young never see or hold good
tools → they don't take up the knowledge → it dies with its holder. Several links in that chain are **closed by nature**,
not chosen by the people:
- seeing tools made (C1);
- holding a tool someone else made (A1, A2);
- keeping a new thing long enough to learn its worth (A4);
- a subsidised youth in which to practise (D1).

**Most likely to matter, in the assistant's view (to be debated):**
1. C1, watching making;
2. D1, care ending at 12;
3. A1 and A2, handing over and leaving things;
4. A4, new things deleted at once.

None of these would name a tool or an outcome. Each is a condition that real people (and other tool users) live
with.

## For TF1 (frozen, not yet run)

A4 shows that TF1's weekly census cannot see things made and deleted within the same week. Operational note 2 (before
any data) adds a count of them from the week's events.

## Debate round 4 (27 October 2026): GPT and Gemini on this audit, Claude as council (opinions, not sign-off)

**Rankings:**
- **GPT:** A4 (new things deleted at once) → C1 (watching making and tool use) → A2, A1, B1 (things lying in the world,
  handing over, materials), each tested separately → vicarious worth → D1 (care) → E2 and salvage.
- **Gemini (after revision):** the same order. A4 and A2 first, then C1, then A1, then B1 and B2.
- **Claude's first ranking** put C1 first and D1 second. Both models put **A4 first**, because it can destroy an
  invention before its maker can learn its worth. The council accepts that A4 should be investigated first, with the
  caveat GPT raised: check whether those things could have been used before they were deleted.

| claim | who | council check | result |
|---|---|---|---|
| A4 (and B1) are engine bugs to patch outside the nature process | Gemini | The carry limit and eviction are nature (`acl/`, `code_v7`). GPT: a bug is code breaking its own rule; a design limit is code faithfully doing an unrealistic thing, and that needs the nature process | **Withdrawn** |
| Test A1 + A2 + B1 together as one law of matter | Gemini | ACL changes one law at a time. GPT: shared engineering underneath is fine, but each behind its own switch that reproduces v7 when off, each tested alone, and a combined arm only later | **Withdrawn** |
| E2 as worth = expected uses × felt gain | Gemini | Inserts foresight the agent never learned; GPT: "foresight rather than the capacity to develop foresight" | **Withdrawn** (a cognitive question for after MK1) |
| Extending care past 12 smuggles the outcome | Gemini | The 12 cut-off is itself a hardcoded age | **Withdrawn**. GPT: don't just move it to 16 or 18; a candidate might let care follow real dependency, hunger and means, in its own study |
| **Vicarious worth:** seeing someone do better with a tool should be able to teach its worth before holding or making one | Gemini (added); GPT: "high priority" | The code: watching sets worth only in joint hunts | **Stands, as a gap**. Observation, learning how to make, and learning worth are three separate capacities, to test separately |
| **Salvage:** worn tools cannot be broken back into materials | Gemini | True in the code | **Stands; low priority** |
| Abandoned tools as cues that draw people | Gemini | Depends on A2; no curiosity should be hard-coded toward them | **Stands, conditional** |
| **Skill grows only by completing a making or by play,** not by helping or partial practice | GPT (asked), council (code) | True: `_gain_skill("crafting")` is called only in `_craft` and `_play` | **A gap to note** (fits C3) |
| A3, A5, C2, C3 are defensible simplifications for now; C4 (whole-table habit copying) deserves its own audit | GPT | — | **Noted** |

**Agreed by all three:** every one of these is an ability or condition, never an outcome. Each is tested alone,
frozen, with a switch that reproduces v7 when off. "The mission is not to make invention spread by changing numbers
until it does. It's to ensure the world permits ordinary physical interactions, and then discover what its
inhabitants actually do with them." (GPT)
