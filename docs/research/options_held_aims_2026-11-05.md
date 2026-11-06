# Research note: held aims as "options" in learning agents (5 November 2026)

**Why now:** council round 66 points to a possible intention law for remaking (a held aim toward a state one's own
experience valued), if RF1 shows that pursuit, not inability, is where remaking fails. Is there a standard, general
form for an aim held across many steps in an agent that learns from reward?

## Source
**Sutton, R. S., Precup, D., & Singh, S. (1999). Between MDPs and semi-MDPs: A framework for temporal abstraction in
reinforcement learning. *Artificial Intelligence*, 112(1–2), 181–211.**
- **Read: the abstract and opening pages** (the authors' PDF at incompleteideas.net, 31 pages, text extracted with
  pypdf on 5 November 2026). The rest of the paper was not read.

## What it says (paraphrased)
- It extends "an action" to include **options**: closed-loop ways of acting over a stretch of time. The examples are
  picking up an object, going to lunch, and travelling to a distant city.
- Options can be used in place of single actions inside the usual learning methods (Q-learning) and planning methods.
- Three results bear on ACL:
  1. **Interruption:** an option can be cut short during execution when something better appears, and this does
     better than following it to the end.
  2. **Intra-option learning:** an agent can learn about an option from fragments of its execution.
  3. **Subgoals:** subgoals can be used to improve the options themselves.

## How it bears on ACL (a suggestion only; a frozen study decides)
- A held aim in an ACL person could take this general form, with nothing named:
  - **when it starts:** a valued thing is gone and its recipe is known;
  - **what it does:** a pull toward the missing inputs and parts;
  - **when it ends:** the inputs are in hand, or the value falls.
- **Interruption is the key point for ACL's trade-off.** LH1 and HE1 showed that whatever releases making raises
  starvation. An aim that yields when hunger or danger rises (the paper's interruption) is the general way to pursue a
  sequence without starving.
- **Caution:**
  - the paper's options are designed by the modeller or learned with machinery ACL does not have;
  - an ACL law must stay general (any valued state, no recipe named) and small;
  - RF1 must first show that pursuit, not inability, is the bottleneck.

**Label:** a source suggests; only a frozen study decides.
