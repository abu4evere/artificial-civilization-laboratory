# Inheriting what parents learned: published simulation work bearing on BN1 (2 November 2026)

**Why:** BN1 asks whether a newborn should start with half its parents' learned habit values (v11) or with none.
Computer studies have compared "Lamarckian" inheritance (learned changes passed on), "Darwinian" (not passed on) and
"Baldwinian" (not passed on, but learning steers selection). **Written while BN1 runs, before its data.** A source
suggests; only BN1 decides.

**Labels:** what was read is stated for each source. Nothing here was read in full text.

## Sources
1. **Sasaki & Tokoro 1999**, "Evolving Learnable Neural Networks Under Changing Environments with Various Rates of
   Inheritance of Acquired Characters: Comparison of Darwinian and Lamarckian Evolution", *Artificial Life* 5:203–223,
   doi 10.1162/106454699568746.
   - **Read:** the abstract, through the Crossref record, in part.
   - **What it says:** neural networks learn to tell food from poison within a life, and evolve across generations.
     "Populations with lower rates of heritability not only show more stable behavior against environmental changes,
     but also maintain greater adaptability" to changing environments.
   - **The companion papers** (Sasaki & Tokoro 2000, *Knowledge and Information Systems* 2:201–222, and an LNCS chapter
     in 1999, pp. 34–41) were seen as **records only**.
2. **Thomsen & Rasmussen 2023**, "Dynamics of Darwinian versus Baldwinian versus Lamarckian evolution", arXiv
   2305.00491.
   - **Read:** the abstract (arXiv).
   - **What it says:** in agent-based simulations, constant and changing, the advantage of the Lamarckian and Baldwinian
     strategies falls as their learning and replication costs rise. In most cases the Baldwinian performs between the
     other two. The authors stress "the superiority of the Lamarckian strategy in most cases with low learning cost".
3. **Benito, Lutzeyer & Doerr 2026**, "A Fresh Look at Lamarckian Evolution and the Baldwin Effect", arXiv 2605.28703.
   - **Read:** the abstract (arXiv).
   - **What it says:** on optimization benchmarks, Baldwinian and Lamarckian evolution both beat Darwinian.
4. **Hinton & Nowlan 1987**, "How Learning Can Guide Evolution", *Complex Systems* 1:495–502.
   - **Read:** the abstract (the author's page).
   - **What it says:** learning can greatly speed evolution even when nothing learned is passed to the genotype (the
     Baldwin effect).
5. **Ackley & Littman 1994**, "A case for Lamarckian evolution", in *Artificial Life III*, pp. 3–10.
   - **Read:** the record only. Not read; nothing is claimed from it.

## What this suggests for ACL (inspiration and caution, not evidence about ACL)
- **The literature does not agree.** Inheriting learned content tends to help in **stable** settings, or when
  learning is costly. It tends to hurt stability and adaptability in **changing** settings.
  - ACL's world changes: seasons, a random growing factor each year (0.65–1.25), moves, and other people.
  - So, from these sources, z (born at 0) need not be worse than v11, and could be steadier. That is in line with
    BN1's frozen prior ("z not worse"), but it does not test it.
- **The analogy is partial:**
  1. In these models, inheritance writes into the **genotype**, under **selection** across generations. In ACL, the
     habit table is not a gene and nothing selects on it. Birth inheritance in ACL is more like an extra **vertical
     cultural channel** at birth, on top of upbringing and talk.
  2. BN1 measures **early-life calibration** (how close young people's values are to what actually follows). It does
     not measure fitness or long-run adaptation.
- **A later question for the council, not a proposal:** if BN1 reads "z not worse", a follow-up could ask whether
  values passed at birth make a population **slower to adjust after a change** (Sasaki & Tokoro's prediction).
  - An example: compare how a hard year's lessons persist in v11 and z.
  - It would be a frozen read-only study of BN1's outputs first, if the data allow.

## Sources
- [Sasaki & Tokoro 1999, *Artificial Life* (Crossref record)](https://api.crossref.org/works?query.bibliographic=Adaptation+under+Changing+Environments+with+Various+Rates+of+Inheritance+of+Acquired+Characters)
- [Thomsen & Rasmussen 2023 (arXiv)](https://arxiv.org/abs/2305.00491)
- [Benito, Lutzeyer & Doerr 2026 (arXiv)](https://arxiv.org/abs/2605.28703)
- [Hinton & Nowlan 1987 (author's page)](https://www.cs.toronto.edu/~hinton/absps/evolution.htm)
