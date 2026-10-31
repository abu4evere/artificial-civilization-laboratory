# Research note: how much foragers make, and how children come to tools (31 October 2026)

**For the open question** (CO2, AW1): making loses the choice at any moment to the built-in pull of food and gathering,
and declines over time through habit. The queued read-only study asks how the worth of made things (`itemval`) forms.
These sources suggest; only a frozen study decides.

## What was read (labels per CLAUDE.md)

1. **Lee, R. B. (1979, 1984), !Kung work time.** **Secondary only:** the Wikipedia article "Original affluent society"
   and an Adam Smith Institute blog post that quotes Lee's 1984 book. Lee's own tables were **not** read.
   - Lee's first estimate (12–19 hours a week) left out food processing, **tool making** and housework.
   - With them included: about **40–44 hours a week**; Wikipedia gives 44.5 for men and 40.1 for women.
   - **The tool-making share itself was not found** in what was read. It needs Lee (1979), *The !Kung San: Men, Women
     and Work in a Foraging Society*, ch. 9 (archive.org record `kungsanmenwomenw0000leer`; record only, not opened).
   - **Bearing on ACL:** among real foragers, making and repairing tools is a regular, counted part of the work week,
     not a rare event. ACL's making collapses at the choice (LS2, CO2). A measured share of time on manufacture would be
     an anchor (Law 126 style), not a target. **Not yet found.**
2. **Lew-Levy, S., Andersen, M. M., Lavi, N., Riede, F. (2022).** "Hunter-gatherer children's object play and tool use:
   an ethnohistorical analysis." *Frontiers in Psychology* 13:824983. PMC9132165.
   - **Read:** the abstract, the methods (coding categories) and the start of the results; **not** every table.
   - 434 observations of children's toys and tools from **54 hunter-gatherer societies** (eHRAF).
   - **Most objects are used in play.** Children readily **make their own toys**. Most objects are built from several
     materials. Most are full-sized or **miniature versions of adult tools**.
   - **Bearing on ACL:**
     - PL1 found ACL's young children play in 6.8% of weeks, below real forager children, and that play is where nearly
       all of a child's crafting skill comes from;
     - here, making itself is part of children's play. Whether ACL children can *make* during play (not only handle
       things) is a question to check in the code before any proposal.

## Candidate next readings (not yet read)
- Lee (1979), ch. 9 "Men, women and work": the hours on manufacture.
- Salali et al. (2019), *Sci Rep* 9:11080 (PMC6668464): BaYaka children's time budgets and social learning, from
  infancy to adolescence.
- Lew-Levy et al. (2017), *Hum Nat* 28:367 (PMC5662667): how forager children learn subsistence skills. Adults teach
  complex tool making directly only in adolescence.

## Checked in the code after reading (31 October 2026, live nature v9)
- **In ACL, "make"** (making again a thing whose recipe is known) **is offered only to people aged 12 or more.**
  - `acl/mind.py`, the make option sits under `if grown:`, where `grown` means teen, adult or elder;
  - `acl/config.py`: `CHILD_END` = 12 years.
- **Children from 3 to 12 can only "play"** (`actions._play`): striking, tying, wetting and shaping what they hold.
  Play builds crafting skill and can turn up new kinds. Toddlers (under 3) cannot gather.
- **Against Lew-Levy et al. (2022):** forager children "readily manufacture their own toys", mostly miniature or
  full-sized versions of adult tools, that is, making known things. ACL's children cannot make a known thing until 12.
- **This is a possible gap, not a proposal.** Letting children make would be a nature change (Law 126):
  - it needs the creator's decision;
  - evidence first: at what ages forager children make which things;
  - a frozen study.
  It bears on the creator's first goal (knowledge that survives death), since practice in childhood is where PL1 found
  crafting skill comes from.
