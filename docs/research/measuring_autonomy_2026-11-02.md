# Measuring autonomy: published measures, and how they map onto ACL (2 November 2026)

**Why:** the creator's second goal (30 October): "define and measure autonomy early". The internal design note
(`docs/design_note_apprenticeship_autonomy_2026-10-30.md`, Part 2) lists GPT's five signs, with hooks in the code.
This note adds published measures that could ground them. **A source suggests; only a frozen study decides.**

**Labels:** what was read is stated for each source. None was read in full text.

## Sources
1. **Seth 2010**, "Measuring autonomy and emergence via Granger causality", *Artificial Life* 16(2):179–196, doi
   10.1162/artl.2010.16.2.16204.
   - **Read:** the abstract (Europe PMC).
   - **What it says:** **G-autonomy** measures how far a variable's own past helps predict its future, compared with
     predictions from the past of external (environmental) variables. It was tested on agent-based models of
     predation, where evolution raised autonomy.
2. **Bertschinger, Olbrich, Ay & Jost 2008**, "Autonomy: an information theoretic perspective", *BioSystems*
   91:331–345, doi 10.1016/j.biosystems.2007.05.018.
   - **Read:** the abstract (Europe PMC, through the fetch tool's summary, with quoted parts).
   - **What it says:** autonomy is measured as the information between a system's consecutive states, given the
     environment's history. A "causal" variant handles systems and environments that act on each other. Synergy stays
     hard to attribute.
3. **Barandiaran, Di Paolo & Rohde 2009**, "Defining Agency: Individuality, Normativity, Asymmetry, and
   Spatio-temporality in Action", *Adaptive Behavior* 17:367–386, doi 10.1177/1059712309343819.
   - **Read:** the abstract (Crossref record, in part).
   - **What it says:** agency needs three conditions:
     1. individuality that the system defines itself;
     2. being an active source of activity in its environment;
     3. norms (its own success conditions).
     The authors define agency as an "autonomous organization that adaptively regulates its coupling with its
     environment".
4. **Salge, Glackin & Polani 2013**, "Empowerment – an Introduction", arXiv 1310.1863.
   - **Read:** the abstract (arXiv).
   - **What it says:** **empowerment** is the channel capacity between an agent's actions and its later sensor states:
     how much the agent can affect what it will perceive. It is a task-independent measure of control. (The original
     paper, Klyubin, Polani & Nehaniv 2005, was not read.)
5. **Oudeyer & Kaplan 2007**, "What is Intrinsic Motivation? A Typology of Computational Approaches", *Frontiers in
   Neurorobotics* 1, doi 10.3389/neuro.12.006.2007.
   - **Read:** the abstract (Europe PMC).
   - **What it says:** a formal typology of computational intrinsic motivation. (The split into knowledge-based and
     competence-based kinds is the assistant's background from this paper's typology, **not read here**.)
6. **Colas, Karch, Sigaud & Oudeyer 2022**, "Autotelic Agents with Intrinsically Motivated Goal-Conditioned
   Reinforcement Learning: a Short Survey", *JAIR* (arXiv 2012.09830).
   - **Read:** the abstract (arXiv).
   - **What it says:** **autotelic** agents learn to "represent, generate, select and solve their own problems."

## How they map onto ACL (the assistant's reading; for the council)
The sources measure **three different things**. Keeping them apart avoids calling habit "autonomy".

| level | what it asks | source | in ACL today |
|---|---|---|---|
| **A. Self-driven behaviour** | Does a person's own past predict their next choices beyond the situation they are in? | Seth; Bertschinger et al. | Measurable read-only. The `q` table and attention's inertia carry personal history, while `decide` never reads the last action. **Caution:** strong habits would score as "autonomous", so A alone is not Bob's autonomy. |
| **B. Self-chosen goals** | Does a person represent, choose and pursue a goal they set themselves? | Colas et al.; Barandiaran et al. (norms) | The design note's five signs. Today "focus" is attention with inertia, not an intention: it has no stored goal and no success condition (design note 2.2). |
| **C. Power over the world** | How much can a person's actions change what they will later perceive? | empowerment (Salge et al.) | Measurable only by trying other actions in copies of a world: costly. It would show whether culture (tools, know-how) **raises** people's control over generations. That is a measure of "cumulative" capacity, not of choosing goals. |

**Suggestions for the council** (not proposals for a nature change):
- **An early read-only autonomy audit could report A beside B:**
  - A as a G-autonomy-style ratio: how much better a person's next-action distribution is predicted from the situation
    *plus* their own past choices than from the situation alone, cross-validated;
  - B as the design note's signs.
  - A without B would read as "habit-driven, not goal-driven". Writing that down in advance would stop it being
    mistaken for progress.
- **Empowerment (C)** suits a later question: does accumulated culture raise what people *can* do? It would need
  frozen counterfactual runs in copies, and is costly on the cloud.
- **The autotelic criteria** mark the honest gap. ACL's people cannot yet **represent or generate** a goal. They can
  only be pulled by needs, curiosity (count-based novelty) and puzzles (surprise). Closing that gap without scripting
  is the open problem nearest to Bob.

## Sources
- [Seth 2010 (Europe PMC)](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE%3A%22Measuring%20autonomy%20and%20emergence%20via%20Granger%20causality%22&format=json&resultType=core)
- [Bertschinger et al. 2008 (Europe PMC)](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE%3A%22Autonomy%3A%20an%20information%20theoretic%20perspective%22&format=json&resultType=core)
- [Barandiaran et al. 2009 (Crossref)](https://api.crossref.org/works?query.bibliographic=Barandiaran+Di+Paolo+Rohde+Defining+agency+individuality+normativity+asymmetry+spatio-temporality+action)
- [Salge, Glackin & Polani 2013 (arXiv)](https://arxiv.org/abs/1310.1863)
- [Oudeyer & Kaplan 2007 (Europe PMC)](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE%3A%22What%20is%20intrinsic%20motivation%3F%20A%20typology%20of%20computational%20approaches%22&format=json&resultType=core)
- [Colas et al. 2022 (arXiv)](https://arxiv.org/abs/2012.09830)
