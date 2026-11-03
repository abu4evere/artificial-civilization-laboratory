# Routines and goals across weeks: the "options" framework (2 November 2026)

**Why:** the action audit (`docs/action_audit_2026-11-02.md`, step 5) and DeepSeek's first reply both name the lack of
goals or routines held across weeks as a barrier to Bob's autonomy. In v11, every week is a fresh one-step choice
among 19 actions. **A source suggests; only a frozen study decides.**

## Source
**Sutton, Precup & Singh 1999,** "Between MDPs and semi-MDPs: A framework for temporal abstraction in reinforcement
learning", *Artificial Intelligence* 112:181–211.
- **Read:** the abstract and section 2 (the definition of an option), as text taken from the PDF (34 pages, a copy
  hosted at swarthmore.edu). The rest was not read.
- **What it says:**
  - An **option** generalises a primitive action to "closed-loop policies for taking action over a period of time".
  - It has three parts: a **policy** π (how to act while it runs), a **termination condition** β (the chance of
    stopping in each state), and an **initiation set** I (the states where it can start).
  - "options may be used interchangeably with primitive actions in planning methods such as dynamic programming and in
    learning methods such as Q-learning."
  - The paper also shows three things: plans made with options can be **interrupted** during execution to do better;
    **intra-option** learning learns about an option from fragments of its execution; and **subgoals** can improve the
    options themselves.

## What it suggests for ACL (the assistant's reading; for a future council round)
- **A general law, not a script:** let a person **keep a sequence of their own actions** that went well (for example,
  gather this, then make that) as a routine. It carries:
  - **I:** the situations where it started;
  - **π:** the steps as they were done;
  - **β:** stopping when a step cannot be done or the end is reached.
- **Each routine is learned and valued like any action:** it is offered beside the 19 actions, and its value is learned
  by the same TD rule over its whole duration (the semi-MDP form).
- **Nothing names what the routines are.** Every routine comes from the person's own history, so different people grow
  different routines. That is the creator's "all people act different and think different".
- **Interruption** (the paper's result 1) fits ACL's needs-driven world: hunger or a threat can break a routine. AM1's
  M5 (resuming after a need) is the matching measure.
- **Its place in the order:** after AM1 has validated measures on v11 and v12, so that a routine law can be judged by
  them (M3, M5, M6b), not by more activity.
- **A risk to test for:** routines could lock people into old habits, the opposite of cumulative invention. A frozen test
  needs a guard on new kinds and on SC1's uptake.
