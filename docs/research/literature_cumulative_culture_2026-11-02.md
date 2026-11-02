# Literature: cumulative culture, transmission and agency, beside ACL (2 November 2026)

**The sources the creator supplied** (1 November 2026): six papers to find, and six files in Downloads. Read
alongside ACL's latest results: KL1 (know-how loss), HA1 (handing), UV1–UV3 (habit values), and IQ1.

- **The files** were read locally (text in gitignored `books_local/`).
- **The papers** were read from PubMed abstracts, from the publisher's abstract page (Cambridge Core for Henrich
  2004), or from the open-access full text (JASSS for ODD).
- **Labels:** what was read is stated for each source. **[C]** marks the assistant's synthesis. Short quotes only.

## Problems with three of the files (please note)
- **"The Evolution of Agency" (Tomasello) is not the book.**
  - The PDF is an advert for a "free ebook" site, followed by hundreds of pages of random words in several
    languages. There is no Tomasello text in it.
  - Its links should not be followed; such sites can carry malware.
  - **Nothing from Tomasello is used here.** The real book is published by MIT Press.
- **"The Secret of Our Success PDF"** is a **third-party summary by "Bookey"**, not Henrich's book. What it says is
  labelled as the summary's, not Henrich's own words.
- **The Mesoudi file** (*Cultural Evolution*, 2011) holds only 10 pages: the contents and part of the index. **No
  argument from it is used.**
- **Sutton & Barto** is a **2014–15 draft** of the 2nd edition. It lacks the sections on Expected Sarsa and
  maximization bias that the published edition has, so those were not read here.

## The six papers
1. **Henrich (2004), "Demography and Cultural Evolution… The Tasmanian Case"**, *American Antiquity* 69:197–214.
   - **Read:** the abstract on Cambridge Core. The author's PDF refused an automated fetch, so the full text was not
     read.
   - Over about 8,000 years Tasmanian societies lost skills and technologies (bone tools, cold-weather clothing,
     nets, fishing spears and others).
   - His formal model of social learning and inference finds that a sudden fall in **effective population size**, "the
     size of the interacting pool of social learners", can keep simple skills stable or improving while complex
     skills deteriorate and disappear.
2. **Vaesen et al. (2016), "Population size does not explain past changes in cultural complexity"**, *PNAS*
   (PubMed 27044082).
   - **Read:** the PubMed abstract. This paper was **added as counter-evidence**; the creator did not supply it.
   - Co-authors and page numbers are left out where only "et al." was seen.
   - It argues that Henrich's and Powell et al.'s models "only support a relationship between demography and culture
     in implausible conditions", and that their predictions conflict with the archaeological and ethnographic record.
   - **The population-size account is contested.**
3. **Dean et al. (2012), "Identification of the social and cognitive processes underlying human cumulative
   culture"**, *Science* (PubMed 22383851).
   - **Read:** the PubMed abstract.
   - Groups of capuchins, chimpanzees and children faced a three-stage puzzle box. Only the children reached the
     higher stages.
   - Their success went with "teaching through verbal instruction, imitation, and prosociality", observed only in the
     children.
4. **Tennie et al. (2009), "Ratcheting up the ratchet"**, *Phil. Trans. R. Soc. B* (PubMed 19620111).
   - **Read:** the PubMed abstract.
   - Chimpanzee traditions stay within a "zone of latent solutions" that individuals could find themselves, through
     mostly **product**-oriented copying.
   - Human culture **accumulates** (the "ratchet effect") because social learning is **process**-oriented, and because
     cooperation brings **active teaching**, conformity and sanctions.
5. **Derex & Boyd (2016), "Partial connectivity increases cultural accumulation within groups"**, *PNAS* (PubMed
   26929364).
   - **Read:** the PubMed abstract.
   - In a computer-based experiment with groups of the same size, **fully** connected groups lost diversity: everyone
     learned from the successful.
   - **Partially** connected groups kept more diverse solutions, and reached complex solutions that fully connected
     groups never produced.
6. **Kirby et al. (2008), "Cumulative cultural evolution in the laboratory"**, *PNAS* (PubMed 18667697).
   - **Read:** the PubMed abstract.
   - Artificial languages passed down chains of learners became **easier to learn and more structured** over
     generations, "without any intentional design" by the learners.
   - The first experimental support for "the appearance of design without a designer".
7. **Grimm et al. (2020), "The ODD Protocol for Describing Agent-Based and Other Simulation Models"**, *JASSS* 23(2) 7.
   - **Read:** the open-access paper's headings and its description of the elements.
   - **ODD's seven elements:** (1) purpose and patterns; (2) entities, state variables and scales; (3) process
     overview and scheduling; (4) design concepts; (5) initialization; (6) input data; (7) submodels.
   - **Its aim** is a description from which a reader could re-implement the model.

## The books and précis
- **Epstein & Axtell (1996), *Growing Artificial Societies*** (Sugarscape).
  - **Read:** the introduction's framework.
  - Artificial societies are laboratories in which to "grow" social structures from **agents, an environment and
    rules**, bottom up. The aim is to find local mechanisms *sufficient* to generate the large-scale patterns.
  - **[C]** ACL is in this lineage, with learning minds, culture and knowledge added. Their method carries a caution
    ACL should keep: **sufficient is not necessary.** A rule that grows a pattern shows a way it can arise, not that it
    did.
- **Heyes (2019), "Précis of *Cognitive Gadgets*"** (accepted *BBS* manuscript).
  - **Read:** the abstract.
  - Distinctively human mechanisms (imitation, mindreading, language) are "cognitive gadgets", shaped by **cultural**,
    not genetic, evolution.
  - They are built in development by general-purpose learning from social information, and spread "because the
    holders had more students, not just more babies".
  - She rejects innate modules. **That disagrees with Spelke & Kinzler's "core knowledge"** (IQ1 report, addendum);
    both were read at the abstract level.
- **Henrich, *The Secret of Our Success*** (via the Bookey summary only).
  - **"Collective brains":** group size and connections preserve complex know-how.
  - **The Polar Inuit:** an 1820s epidemic cost them skills, which they re-learned on meeting another group in 1862.
  - **"On the origin of faith":** this chapter concerns **trust in inherited practices** whose reasons no individual
    can see (for example, the many steps of processing manioc to remove cyanide). It is not about religion as such.
- **Sutton & Barto, 2nd ed. (draft):** §2.5 on optimistic initial values. Its content matches the 1st edition already
  in `docs/research/initial_values_and_longer_view_2026-11-01.md`.

## What this means for ACL ([C] unless stated)
1. **KL1 fits the cumulative-culture literature's central question, with a caution.**
   - KL1 found that know-how held by one person (61% of kinds) dies with them, which is 90% of all loss.
   - Henrich's Tasmanian model and Henrich's "collective brain" (as summarised) predict such losses when few people
     hold a skill.
   - **But Vaesen et al. dispute** that population size alone explains such losses.
   - **ACL can test this instead of arguing it:** vary the number of people who hold or learn a skill, with
     everything else fixed.
2. **Partial connectivity can beat full connectivity** (Derex & Boyd). This sharpens the old contact idea (IQ1, H5).
   The prediction is **not** "more contact is better". It is that **partly separated groups keep more diverse know-how
   and reach more complex solutions.** The Polar Inuit relearning (summary) is an example of rare contact restoring
   lost skills. ACL's people live in scattered groups, but no study has measured how knowledge flows between them.
3. **Teaching is what ratchets** (Tennie; Dean). This matches ACL:
   - AW1: being taught doubled crafting skill, while watching passed little;
   - KL1: teaching passes know-how on, and copying by watching almost never happens (10 gains).
   - Tennie's distinction, **process versus product copying**, maps onto ACL's teaching (the recipe) versus handing
     (the object; HA1: objects carry no know-how).
4. **Design without a designer** (Kirby). This is ACL's founding claim, "culture written by nobody", shown in a
   laboratory.
   - ACL's marks link shapes to meanings in people's minds.
   - **A read-only question:** do mark-meanings become more structured and more shared across generations, as Kirby's
     languages did?
5. **Should ACL hard-code its learning tools?** (Heyes)
   - ACL writes teaching, watching and reading marks as laws.
   - Heyes argues such tools are themselves cultural products of general learning.
   - That would push "nature programmed, culture written by nobody" one level deeper: let the *ways of learning*
     emerge too.
   - It is a **long-term question for the council**, and a large change. It is not a proposal.
6. **Three views on tradition**, for IQ1:
   - Henrich (summary): trusting inherited practices can carry knowledge no individual could work out.
   - Deutsch: static traditions block growth.
   - The Qur'an (2:170, 43:22–23) reproaches following forefathers who "understood nothing".
   - **[C]** These are not simply opposed. Inherited practice can carry real knowledge, and blind following can also
     preserve error. The difference may be whether the inheritance stays open to understanding and checking (Q
     67:3–4, "Look again"). **This is interpretation, not a finding.**
7. **Document ACL in ODD** (Grimm et al.). ACL has never been described in a standard form. An ODD description of
   nature v11 would let outside researchers check, compare and re-implement it. **That is a safe, concrete next step,
   with no change to nature.**

## Model libraries (first look only)
- **CoMSES** (comses.net), a search for "cumulative culture", lists models close to ACL's questions, among them:
  - "Cumulative knowledges learning in networks" (Barbet & Rouchier, published 2026);
  - "Hunter Gatherer Survival" (Barceló & Del Castillo, 2018);
  - "GRASP world" (Hofstede, 2019).
  - **Only their listings were read.** A side-by-side comparison with ACL is a later task.
- **The NetLogo Models Library** was **not browsed yet.**

## Next steps proposed (for the council; no change to nature)
1. **An ODD description of nature v11:** documentation only, starting now.
2. **H1, born without learned content:** a test in a copy. Q 16:78, core knowledge, Deutsch's anti-Lamarckism and
   UV1–UV3 all point to it. Adoption is the creator's decision.
3. **A read-only follow-up to KL1:**
   - is lost know-how valuable or minor;
   - how knowledge flows between groups;
   - whether partly separated groups keep more kinds (Derex & Boyd's prediction, tested in ACL's own worlds).
