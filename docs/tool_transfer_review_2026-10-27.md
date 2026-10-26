# Can a tool pass from one living person to another? A read-only code review (27 October 2026)

**Written in sleep mode, for the creator. Nothing is frozen or changed.** It answers LS1's second frozen branch ("the
tool lifecycle is the leak": 0.98 of tools used were made by their holder; replacement within a year fell 0.59 → 0.07)
and the evidence review's main contrast (forager children hold tools made or given by others,
`docs/evidence_review_children_tools_2026-10-26.md`).

## What the code allows (nature v7, `code_v7`)

| how a made thing can change hands | where | condition |
|---|---|---|
| **Giving to a living person** | `actions._give` | **Not possible.** "Give" moves food only (food and seeds). No action hands over a made thing. |
| Inheritance at death | `biology` (death) | Goes to the partner if at the same place, otherwise to a child aged 12+ at the same place. Otherwise the things stay with the body. |
| From the body (v4 on) | `biology` (bodies) | Only the dead person's partner, or a child aged 12+, on the body's tile. |
| Stealing | `actions` | Food only. |

**How a thing leaves a person's hands:**
- **Wear:** forage and other uses take away uses; warm clothing wears in the cold. At 0 uses the thing is gone.
- **The carry limit:** `item_limit` = 3 made things. A new one pushes out the least valued.
- **Death:** passed on as above, or left on the body.

**So in ACL a child can hold a tool someone else made only by inheriting it when a parent dies, and only if the child
is at least 12 and in the right place.** "Tools almost never pass between people" (LS1: 0.013 of tools used were made
by someone else) is not people choosing not to give. **The world has no way to give.**

## Why this matters
- The forager evidence points the other way. Children receive tools, often well made, before they can make them
  (opportunity scaffolding; Lew-Levy et al. 2020, 2022; Hewlett & Roulette 2016, to be checked). That is how they
  feel a tool's worth before they can make a good one.
- In ACL the only way to know a tool's worth is to make one yourself. With low skill, that means a weak tool, a weak
  felt worth, and less making (the low-skill-trap hypothesis MK1 is testing).
- Being able to give is a **capacity, not an outcome**: it says nothing about which tools, to whom, or when. Whether
  anyone uses it would be up to them, like giving food.

## What a study could look like (for the creator to weigh; not proposed until MK1 reads)
- **A read-only lifecycle audit first** (cheap, no change to nature): how each tool ends (worn out, pushed out by the
  carry limit, its holder's death) and, at death, whether it was inherited, left on the body, or taken from it.
  Also how often children near a tool-holding carer hold no tool. This shows how much a giving capacity could matter.
- **Then, if the creator wants, a nature candidate:** "give" may also hand over a made thing, by the same rules as food
  giving (the giver's motive, relationship, kinship; the receiver's need and carry limit), with no rule about what to
  give. Frozen, with a control, a sham and zero checks; the primary test is whether children who receive tools later
  *choose* to make, not population.
- Wait for MK1. If MK1 shows "opportunity cost" dominates (making simply pays less than foraging), giving may not help.
  If it shows the low-skill trap or a delayed-benefit failure, giving is a direct, evidence-backed candidate.

## Debate round 2 (27 October 2026): GPT and Gemini, Claude as council (opinions, not sign-off)

| claim | who | council check | result |
|---|---|---|---|
| Giving things is a legitimate minimal law (a missing capacity, not an outcome), if it uses the same social evaluation as food giving, with no bonus for children or novices | GPT ("Yes. Strongly."), Gemini | Agreed by all three | **Stands** |
| A received tool would go unused if the recipient's learned worth is 0 | Gemini | `matter.best_item` uses the tool with the highest physical factor; worth does not gate use | **Wrong; withdrawn** |
| If opportunity cost dominates, adjust nature's parameters (tool multipliers, depletion) | Gemini | Breaks ACL's no-tuning rule | **Withdrawn** |
| "Adults below 7 food a week" | Gemini | In nothing sent; Gemini: "an ungrounded hallucination" | **Withdrawn** |
| Giving brings the giver nothing back, so making-for-others cannot arise | Gemini | `_give` records a balance the receiver owes; a paying-back motive; the giver's habit is reinforced when paid back; the giver gets reward, affection, trust and respect | **Wrong; withdrawn** (Gemini: specialisation "possible in principle") |
| Even if opportunity cost dominates, giving may help (one maker's effort serves several users) | GPT | Consistent with the code's reciprocity | **Stands as a possibility** |
| **Handout skill trap:** children who receive tools may never practise, and become unskilled adults when the tools wear out. Or the opposite: using a good tool raises its worth and the wish to make one | Gemini (risk); GPT (both directions) | Untested | **Open: measure it** (age at first receipt; practice before and after; what happens when the gift wears out) |
| Food-giving motives may not fit durable things: they may make tool gifts almost impossible, or strip people of tools | GPT, Gemini | The food-giving utility uses the giver's surplus food and the receiver's hunger, which make no sense for a tool | **Stands: the motive needs designing before any candidate** |
| Possession is not knowledge: never pass a recipe with a tool | GPT, Gemini | Agreed | **Stands** |
| Primary outcome: whether the new pathway is used and what follows, compared across arms, not recipients against non-recipients (selection) | GPT, Gemini | Agreed | **Stands** (replaces "children who receive tools later make") |
| The carry limit **deletes** the displaced item (it is not dropped): a structural loss route of its own | Claude (found), GPT, Gemini | `_keep` and inheritance pop items | **Stands; to be measured in the audit** |
| Audit now or wait for MK1? | GPT: audit now (read-only; a different question). Gemini: first wait, then agreed the audit can run now | Running any new study needs the creator's sign-off; sleep mode cannot start it | **Draft only; for the creator** |

**What the audit would measure** (draft):
- how every forage tool ends: worn out, deleted at the carry limit, or its holder's death (then inherited, left on the
  body, or taken);
- how often children near a carer holding a tool hold none;
- how often a carry-limit deletion removes a tool better than one kept.

GPT's question for the study: "Does access to someone else's invention help an individual acquire the capability to
reproduce it, or does it make that capability unnecessary until the tool disappears?"

## Debate round 3 (27 October 2026): the creator's question (opinions, not sign-off)

**The creator:** "If they cannot pass the things themselves, it is unwise to expect them to pass the knowledge."

| claim | who | council check | result |
|---|---|---|---|
| The creator is right: object access matters for knowledge to matter, because people learn a thing's worth by using it before they can make it | GPT ("mostly yes"), Gemini ("right") | Fits the code: a held tool is used automatically, so receiving one teaches its worth by use | **Stands** |
| ...but it is not a strict prerequisite: a learner can watch and reproduce; naive crows make tools without demonstration | GPT | Gemini accepted it | **Stands** |
| Evidence that access to artefacts helps: Aka caregivers give infants knives and digging sticks; chimpanzee mothers transfer termite-fishing probes to offspring, who then use tools and feed more (Musgrave et al. 2016); young crows handle parents' tools; young capuchins practise around shared anvils and stones | GPT, Gemini | Sources to check before use | **Stands, to check** |
| "Active teaching is virtually non-existent in animals" | Gemini | GPT cited the chimpanzee probe transfers, counted as teaching by their authors | **Withdrawn** |
| Foragers carry "3 to 6 core items" | Gemini | No source; GPT found no universal number, only flexible toolkits and caches | **Withdrawn** |
| The leak is the deletion, not the number 3 | GPT, Gemini | True: `_keep` deletes the least valued thing | **Stands** |
| Replace deletion with dropping on the tile | Gemini | **Tiles cannot hold made things in v7** (only materials); a made thing exists only in someone's hands or with a body. So dropping needs a new law (persistence, decay, visibility, who may pick it up). Gemini accepted this; GPT warned against an unlimited communal store | **Not a small fix; a separate candidate** |
| What matters is **access to artefacts** (gifts, borrowing, abandoned tools, shared places), not gifting alone | GPT; Gemini agreed | — | **Stands** |
| **Prediction:** allowing tool transfer will improve tool use more reliably than it improves the passing of making knowledge. Material and knowledge transmission may be separate bottlenecks | GPT; Gemini agreed | — | **On record** |
| Order: finish MK1 and the read-only lifecycle audit, then giving things and what happens to discarded things (two separate candidates, not combined), and teaching last. Don't raise lesson uptake directly (that would be tuning); don't just raise the carry number | GPT, Gemini (same order) | Consistent with ACL's rules | **The council's recommendation, for the creator** |
