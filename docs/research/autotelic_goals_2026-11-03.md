# Minds that make their own goals: "autotelic" agents (3 November 2026; for the brain road)

**Why:**
- The brain road's missing piece is goal formation: goals built, not only selected (rounds 55–56).
- The creator, 3 November: "Making something again isn't necessarily making it again on purpose."

**A source suggests; only a frozen study decides.**

## Source
**Colas, Karch, Sigaud & Oudeyer 2022,** "Autotelic Agents with Intrinsically Motivated Goal-Conditioned Reinforcement
Learning: A Short Survey", *Journal of Artificial Intelligence Research* 74, doi 10.1613/jair.1.13554 (arXiv 2012.09830).
- **Read:** the abstract in full, and the full text in part. The key sections were searched and read in the arXiv
  PDF: the definition of goals, learning progress, sample efficiency, and the socio-cultural challenge. It is 41
  pages; not every section was read.

## What it says (in brief, paraphrased)
- **Autotelic agents** are learning agents that "learn to represent, generate, select and solve their own problems"
  (the abstract). The authors argue that open-ended skill repertoires need such agents.
- **What a goal is**, in the psychological sense they adopt:
  - a mental representation of a future state that the organism commits to approach or avoid;
  - so goal-directed behaviour is proactive, not reactive, and the commitment shapes behaviour directly.
- **How such agents choose goals:**
  - many methods estimate **learning progress** (how fast competence on a kind of goal is changing) in different
    regions of the goal space;
  - they then favour goals where the absolute progress is high;
  - this aims at what more practice can still improve, setting aside the impossible and the already mastered.
- **Results they cite** in developmental robotics: sample-efficient learning of motor skills, including nested tool
  use by real robots (Forestier et al. 2017). That paper was not read here.
- **A challenge they name:** deep reinforcement learning rarely uses socio-cultural environments. When it does, it
  usually models them as direct teaching, which removes the agent's autonomy.

## What it suggests for ACL (the assistant's reading)
1. **A general goal law exists in the literature that names no goal.**
   - Goals are represented as **states** (properties the person could bring about).
   - The person favours goals where their own competence is **changing fastest**.
   - That is not a target written by us. It is a drive toward what one is getting better at, close to the creator's
     "deciding what matters".
2. **The definition fits the creator's point on purpose.** A goal is a represented future state the person
   **commits** to. So tests of intent should look for the commitment (preparation, persistence, return after an
   interruption), as the brain design's five tests do.
3. **Learning progress also gives metacognition** almost for free. Tracking where one is improving, and where one is
   not, is a form of "knowing what you don't know" (capability 7 in the brain design).
4. **A warning for ACL's teaching:** in ACL, teaching is automatic (`knowhow.teach`). The survey's point supports
   making teaching and learning from others something the person *does*, not something done to them. That is already
   in the action audit.
5. **For PB0 and after:** if PB0 says NO-GO for foresight alone, a goal memory driven by learning progress is a strong
   candidate for the first brain part.

## Second source (4 November 2026)
**Forestier, Portelas, Mollard & Oudeyer,** "Intrinsically Motivated Goal Exploration Processes with Automatic
Curriculum Learning", *JMLR* 2022 (arXiv 1708.02190, first submitted August 2017).
- **Read:** the abstract only (the arXiv page).
- **What it says:**
  - IMGEP is a framework for learning from **self-generated goals**, chosen by intrinsic rewards that follow the
    agent's own learning progress;
  - a variant with object-centred modules was shown on a humanoid robot;
  - the robot discovered skills including **nested tool use**, as stepping stones, with no external task given. The
    designers did not specify the goals or the tools.
- **For ACL:** this is direct evidence that tool use can emerge from a general goal-choosing law (learning progress)
  without naming tools. It fits the brain design's rule (goals as states, never named things). The full text should be
  read before any frozen brain study cites its details.

## Not read (to find next)
- The full text of Forestier et al. (JMLR 2022): the goal-space modules and how the tool stages appeared.
- Baranes & Oudeyer 2013 (active learning of skills by learning progress).
- Elliot & Fryer 2008 (the goal construct in psychology).
