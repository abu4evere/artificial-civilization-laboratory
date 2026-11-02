# IQ1 — Islamic Sources and Emergent Cognition: first report (1 November 2026)

**Status:** literature review, conceptual analysis and proposals only. Nothing in nature has changed. No experiment has
been run. Any law that comes out of this needs a frozen study, and adoption needs **the creator's explicit approval**
(the creator, 1 November 2026, for IQ1).

**The creator's charge** (their words): "Our purpose is not to prove a conclusion we already decided upon. Our purpose
is to seek understanding." So this report keeps four things apart, and labels them:
- **[S] Source:** what the Qur'an or hadith text says, verified.
- **[I] Interpretation:** what classical scholars said, as read.
- **[C] Computational reading:** the assistant's proposal, a speculation.
- **[H] Hypothesis:** testable in ACL.

A simulation result cannot prove or disprove a religious teaching. Consciousness and the *ruh* cannot be inferred from
behaviour.

## How the sources were checked (what was read)
- **Qur'an:** Arabic text and two translations for every verse cited: Saheeh International (SI) and M.A.S. Abdel
  Haleem (AH). They were read from quran.com and its data service (api.quran.com) on 1 November 2026. Where the two
  differ in a way that matters, both are given.
- **Word frequency:** the Quranic Arabic Corpus (corpus.quran.com), the root ʿ-q-l.
- **Hadith:** the English text and grading from sunnah.com; the grading is given when the site shows one (al-Albani).
- **Tafsir:** Ibn Kathir (abridged English), on quran.com, for 30:30, 16:78, 75:2 and 12:53. Only those passages
  were read.
- **Secondary:** the Wikipedia article "Fitra", for the range of scholarly positions. It cites Hoover (EI3), Chittick
  and al-Samarqandi; **those works themselves were not read.**
- **Not used:** one reference tried (Sahih Muslim 2658a on sunnah.com) returned a different hadith, so it is not
  cited. The fitrah hadith is cited from al-Bukhari only.

## A and B. Ten principles, with sources and context

### 1. Born knowing nothing, given faculties that grow
- **[S]** Q 16:78.
  - SI: "And Allāh has extracted you from the wombs of your mothers not knowing a thing, and He made for you hearing
    and vision and hearts [i.e., intellect] that perhaps you would be grateful."
  - AH: "…knowing nothing, and gave you hearing and sight and minds…"
- **[I]** Ibn Kathir: He gives "hearing to recognize voices, sight to see visible things and hearts — meaning reason".
  He adds: "These abilities and senses develop gradually in man. The more he grows, the more his hearing, vision and
  reason increase, until they reach their peak." He also records a **disagreement on the seat of reason**: "according
  to the correct view, is the heart, although it was also said that its seat is the brain."
- **[C]** A mind is born with **faculties** (ways to perceive and learn), not with **learned content**. Its knowledge
  comes after birth, through those faculties. The faculties themselves mature gradually.
- **ACL compared:**
  - ACL's newborn **inherits learned content.** Its habit values start at half its parents' mean (`acl/biology.py`
    line 553). That is a learned value passed at birth.
  - Earth's biology agrees with 16:78 here: learned values are not inherited genetically.
  - **So this principle points at a law in ACL that is unrealistic by both standards.** UV1 and UV3 found that this
    halved inheritance is part of why habit values sit below what life returns, and why they climb so slowly across
    generations.

### 2. Fitrah: an innate disposition, shaped by those who raise the child
- **[S]** Q 30:30.
  - SI: "[Adhere to] the fiṭrah of Allāh upon which He has created [all] people. No change should there be in the
    creation of Allāh."
  - AH: "This is the natural disposition God instilled in mankind — there is no altering God's creation."
- **[S]** Sahih al-Bukhari 1385 (Abu Huraira): "Every child is born with a true faith of Islam (i.e. to worship none
  but Allah Alone) and his parents convert him to Judaism or Christianity or Magianism, as an animal delivers a perfect
  baby animal. Do you find it mutilated?"
- **[I]** Ibn Kathir: people are created "to recognize Him and know His Tawhid".
  - On "no change in Allah's creation" he gives **two readings**: an instruction (do not divert people from their
    fitrah), or a statement that all are created alike with the same sound fitrah.
  - Several early authorities (Ibn ʿAbbas, Mujahid, ʿIkrimah, Qatadah and others) took it to mean "the religion of
    Allah".
- **[I, secondary]** The range of later positions (Wikipedia, citing EI3 and others; not read first-hand):
  - fitrah *is* Islam (the Muʿtazila; some traditions);
  - the pre-revelation religion of Adam;
  - purity plus an innate **capacity to choose or reject** guidance (al-Samarqandi);
  - an innate capacity to understand reality that the environment **obscures** (Chittick).
- **[C]** The part ACL can take, without theology, is the **structure**: an innate disposition that the **people who
  raise the child shape**. The hadith names the parents.
- **ACL compared:** ACL has innate dispositions (genes such as kindness and curiosity) and upbringing (a child's
  habits are pulled 8% a week toward one carer's). The **content** of fitrah, recognition of God, is doctrine. It is
  not something ACL can or should model.

### 3. ʿAql as an activity: reasoning about signs
- **[S]** Verified in the Quranic Arabic Corpus: the root ʿ-q-l "occurs 49 times in the Quran as the form I verb"
  ("to understand, to reason"). **The noun ʿaql does not occur.** Reason appears as something one does.
- **[S]** Q 2:164 (signs in the heavens and earth, night and day, ships, rain, winds) "are signs for a people who use
  reason" (SI).
- **[S]** Q 3:190–191: "signs for those of understanding — who … give thought to the creation of the heavens and the
  earth" (SI).
- **[S]** Q 88:17. SI has "Then do they not look at the camels — how they are created?", but AH has "Do the
  disbelievers not see how rain clouds are formed". **The two translations differ on the word *al-ibil*.**
- **[C]** Reasoning is **inference from regularities in the world**, an active use of perception, not reward alone.
- **ACL compared:** ACL has a module where people make claims, check them against outcomes and trust sources that
  hold up (`acl/information.py`: `verified` and `refuted`). Most of what people do is still driven by instinct and
  habit. In v11, instincts carry 78% of the variance in option scores (ES2).

### 4. Taught by the pen, through names and speech; knowledge outlives the knower
- **[S]** Q 96:4–5: "Who taught by the pen — Taught man that which he knew not" (SI).
- **[S]** Q 2:31: "And He taught Adam the names — all of them" (SI); AH: "all the names [of things]".
- **[S]** Q 55:4: "[And] taught him eloquence" (SI); AH: "and taught him to communicate".
- **[S]** Sahih Muslim 1631: "When a man dies, his acts come to an end, but three, recurring charity, or knowledge (by
  which people) benefit, or a pious child, who prays for him."
- **[C]** Knowledge travels through **names, speech and durable marks**, and it can **outlive its holder**.
- **ACL compared:**
  - ACL people learn recipes by making them, by being taught, by watching (copying), and by **reading marks**
    (`remember_recipe` with "taught", "copied" and "read").
  - HA1 found that objects do not carry knowledge: 0.1% of receivers who could not make a thing later made it.
  - AW1 found that being taught doubles crafting skill, but watching passes little.
  - **No study has yet asked how much know-how dies with its holders, and how much marks save.**

### 5. The receivers of knowledge, and passing it on
- **[S]** Sahih al-Bukhari 79 (Abu Musa): knowledge and guidance are "like abundant rain falling on the earth".
  - **Fertile soil** that absorbed it and "brought forth vegetation".
  - **Hard ground** that "held the rain water" so that people "utilized it".
  - **Barren land** that "could neither hold the water nor bring forth vegetation".
  - In the English on sunnah.com, the explanation names the first (one who "learns and then teaches others") and the
    last (one who "does not care for it"). The middle kind is described in the parable but not separately explained.
- **[S]** Sahih al-Bukhari 3461: "Convey (my teachings) to the people even if it were a single sentence…"
- **[C]** Receivers differ: some use what they learn and teach it; some **store** it for others; some neither. Passing
  on is a duty even for small pieces.
- **ACL compared:** ACL's receivers are alike, apart from a curiosity gene in watching. No study has measured who
  becomes a **teacher** of what they learned.

### 6. Nafs: impulse and self-review
- **[S]** Q 12:53: "Indeed, the soul is a persistent enjoiner of evil, except those upon which my Lord has mercy" (SI).
  **[I]** The speaker is disputed. Ibn Kathir prefers the wife of al-ʿAziz, citing al-Mawardi and Ibn Taymiyya; he
  notes that al-Tabari presented only the reading that Yusuf speaks.
- **[S]** Q 75:2: "the reproaching soul" (SI); AH: "the self-reproaching soul". **[I]** Ibn Kathir reports three early
  readings:
  - al-Hasan al-Basri: the believer asks "What did I intend by my statement…";
  - Saʿid ibn Jubayr: "He criticizes himself in good and bad";
  - Mujahid: "He is sorry for what he missed (of good deeds) and he blames himself for it."
- **[S]** Q 89:27–28: "O reassured soul" (SI); AH: "soul at peace".
- **[S]** Q 91:7–10: the soul "inspired [with discernment of] its wickedness and its righteousness. He has succeeded
  who purifies it, and he has failed who instills it [with corruption]" (SI).
- **[C, labelled speculation]** Two levels: impulses, and a **reviewing self** that judges one's own past choices,
  including what one missed. Reading the three named states as a stage model is a later scholarly tradition. **It was
  not verified here and is not relied on.**
- **ACL compared:** ACL has impulses (instinct terms) and one-step habit learning from one's own reward. It has no
  review of one's choices against what one missed.
- **The council warns** (GPT, Gemini): moral self-reckoning is **not** a learning algorithm. The computational version
  is independently motivated, and the source only inspires it.

### 7. Ikhtiyar: guided, yet choosing; change from within
- **[S]** Q 76:3: "Indeed, We guided him to the way, be he grateful or be he ungrateful" (SI).
- **[S]** Q 13:11: "Indeed, Allāh will not change the condition of a people until they change what is in themselves"
  (SI). AH adds "[for the worse]", **a translator's interpretation** in brackets.
- **[C]** Choice is real within given conditions, and collective change follows inner (individual) change.
- **ACL compared:** ACL's mission is autonomy: minds that choose their own goals. UV3 found the whole population's
  values climbing together, a slow collective change built from individual learning. **The link to 13:11 is thematic
  only.**

### 8. Stages: from childhood to discernment to maturity
- **[S]** Q 40:67: "then He brings you out as a child; then [He develops you] that you reach your [time of] maturity,
  then [further] that you become elders" (SI).
- **[S]** Q 24:59: "And when the children among you reach puberty…" (SI).
- **[S]** Sunan Abi Dawud 495: "Command your children to pray when they become seven years old, and beat them for it
  (prayer) when they become ten years old; and arrange their beds (to sleep) separately." Graded **hasan sahih**
  (al-Albani), as shown on sunnah.com.
- **[S]** Sunan Abi Dawud 4403: "There are three (persons) whose actions are not recorded: a sleeper till he awakes, a
  boy till he reaches puberty, and a lunatic till he comes to reason." Graded **sahih** (al-Albani), as shown.
- **[I]** Ibn Kathir on 16:78: faculties "develop gradually".
- **[C]** Development is **staged and graded**, not one line. **The council's caution (GPT), accepted:** the two
  hadith concern **religious instruction and accountability**, not practical or technical skill. They show a staged
  view of responsibility; they say nothing about when children can make tools. The graded-ability idea rests on 16:78
  and on forager ethnography (`docs/research/children_ages_making_2026-10-31.md`: a gradient, no age line).
- **ACL compared:** in ACL nobody under 12 can choose to make (a single line), though children forage at reduced
  rates.

### 9. Knowing one another, consultation, cooperation
- **[S]** Q 49:13: "…and made you peoples and tribes that you may know one another. Indeed, the most noble of you in
  the sight of Allāh is the most righteous of you" (SI). AH: "so that you should recognize one another".
- **[S]** Q 42:38: "whose affair is [determined by] consultation among themselves" (SI).
- **[S]** Q 5:2: "cooperate in righteousness and piety, but do not cooperate in sin and aggression" (SI).
- **[C]** Contact and mutual recognition between groups, and shared decision-making.
- **ACL compared:** ACL has families and cooperation (food sharing mostly to kin: G1, P1). It has no study of
  contact between groups. **The council's caution (GPT, Gemini), accepted:** 49:13 concerns mutual recognition and
  moral equality, not the spread of know-how. A contact hypothesis would be a secular idea, only loosely inspired by
  it.

### 10. Ruh, and the limits of knowledge
- **[S]** Q 17:85: "And they ask you, [O Muḥammad], about the soul. Say, 'The soul is of the affair [i.e., concern] of
  my Lord. And you [i.e., mankind] have not been given of knowledge except a little.'" (SI). AH: "the Spirit … part of
  my Lord's domain".
- **[S]** Q 17:36: "And do not pursue that of which you have no knowledge. Indeed, the hearing, the sight and the
  heart — about all those [one] will be questioned" (SI).
- **[C]** A boundary. ACL can model behaviour, learning and transmission. It **cannot** model the *ruh*, and it cannot
  claim a mind has one, or is conscious, from what it does.
- 17:36 also states a rule ACL already follows: do not claim what you do not know. Every number in ACL comes from a
  script, with labels for what was read.

## C. ACL gaps these principles help to see
1. **Newborns inherit learned content** (half the parents' habit values), against 16:78 and biology. This ties
   directly to UV1–UV3's findings.
2. **A single age line for making (12)**, against graded faculties (16:78, Ibn Kathir) and forager evidence.
3. **Know-how's survival is unmeasured:** how much dies with its holders, and how much teaching, copying and marks save
   (96:4; Muslim 1631). This follows HA1, where objects carried no knowledge.
4. **No self-review of choices**, judging past choices against what one missed (75:2, as inspiration only). Choices
   are instinct-dominated.
5. **Value transmission is one carer only**, while the fitrah hadith names both parents and forager children learn
   from many after about age 6 (Hewlett et al. 2011, read).
6. **Contact between groups is unstudied** (49:13, loosely).

## D. Five testable hypotheses
Each has an alternative explanation and a way to tell them apart. **All would be frozen studies in copies; none
changes live nature.**

**H1 — Born without learned content** (from principle 1).
- **Law in a copy:** newborns start with no learned habit values (0), and acquire them only through their own learning
  and upbringing.
- **Arms:** v11 (inherited half-values); zero start; and a **sham**: random starting values drawn to match the
  inherited values' distribution (GPT), so the level and spread are the same but the content is not the parents'.
- **Prediction:** if inherited *content* matters, the zero and sham arms differ from v11 in the same direction. If
  only the *level* matters, the sham behaves like v11.
- **Alternative:** any change of start shifts calibration mechanically. The sham separates this.
- **Measures:** calibration (as in UV1), cumulative know-how (recipes per adult) and survival, kept separate (GPT).
- **Guard:** child survival.
- **Council:** Gemini warned that a noisy sham may simply do worse. That is a result, not a flaw: it would show that
  the content carries information.

**H2 — Graded abilities in childhood** (from principles 1 and 8; source link **weak** for the hadith, per GPT).
- **Law in a copy:** children's chance of successfully making a known thing rises gradually with age (or skill), not
  at a single line at 12.
- **Arms:** v11 (line at 12); graded; a **step** at the same mean age; with the **total childhood making
  opportunity equalized** across arms (GPT, Gemini).
- **Alternative:** more making time alone. The equalized step arm separates timing from amount.
- **Measures:** adults' known recipes, making per adult-year.
- **Guard:** child deaths.

**H3 — Know-how that outlives its holders** (from principles 4 and 5; the strongest connection, per GPT).
- **Step 1, read-only on v11:**
  - For each recipe, how often does its last living knower die with it, and how often is it held by someone else
    (taught, copied, read from marks) before that?
  - Separate know-how that **survives physically** (marks) from know-how that is **read and used** (GPT).
- **Step 2, only if step 1 shows marks matter or could:** vary how long marks last, with teaching held fixed. Include a
  sham (marks that last but cannot be read), and test against weaker oral copying, to avoid a ceiling (Gemini).
- **Alternative:** population size and teaching alone set the loss rate.

**H4 — Self-review against what one missed** (principle 6, as **inspiration only**; GPT and Gemini: overreach).
- **Law in a copy:** after a week, a person also updates the value of an option they did not choose, **only from an
  outcome they could see** (a neighbour's result from that action). Otherwise it would give them privileged
  information (GPT).
- **Arms:** v11; self-review; imitation (E13R's kind); sham.
- **Alternative:** plain imitation. The separate imitation arm distinguishes them.

**H5 — Contact between groups** (principle 9, loosely inspired, a secular idea).
- **Read-only first:** how recipes spread between families or bands.
- **Then:** vary contact with population fixed, measuring disease, conflict, mating and resources as mediators (GPT).
- **Alternative:** population size.

## E. Three priorities (scientific value, feasibility, relevance to autonomous, cumulative minds)
1. **H3, step 1: a read-only audit of know-how loss at death.**
   - It needs no change to nature, and it follows directly from HA1 (objects carry no knowledge).
   - It asks Bob's core question: does knowledge outlive the knower?
   - GPT's first choice (94%); Gemini third (75%).
2. **H1: born without learned content** (a test in a copy).
   - Both 16:78 and biology point at the same unrealistic law, and UV1–UV3 already show its effects.
   - High value; feasible with ES2-style machinery.
   - GPT 88%, Gemini 85% (its first choice).
   - **Adoption only with the creator's approval.**
3. **H2: graded abilities in childhood.**
   - The creator's own question about the age-12 line.
   - It rests on 16:78 and ethnography, not on the hadith.
   - Gemini 80%; GPT ranked H5 above it.

## F. Critical assessment
- **Promising:**
  - **16:78 (born knowing nothing; faculties grow).** This is the clearest case where a source points at something
    concrete in ACL: a law (inherited learned values) that is also unrealistic biologically. **This is the strongest
    finding of this first pass.**
  - **96:4 and Muslim 1631 (knowledge by the pen, knowledge that outlives the knower).** These turn attention to the
    **media** of knowledge (speech, teaching, marks), which is exactly where HA1 left us.
  - **Ibn Kathir on the gradual growth of faculties** supports a graded view of development, agreeing with
    ethnography.
- **Mostly secular ideas, relabelled:**
  - H4 (counterfactual learning) and H5 (contact) are standard ideas in learning science and cultural evolution.
  - The Islamic sources add emphasis, not a new mechanism. Both models said so, and I agree.
  - H2's mechanism is developmental psychology; only 16:78 and Ibn Kathir's "gradually" support it from the sources.
- **Too speculative:**
  - Mapping the three named states of the *nafs* onto a stage model of mind.
  - Mapping fitrah's content (recognition of God) onto any parameter.
  - Reading 13:11 as a law of cultural change.
- **Cannot meaningfully be modelled:**
  - the *ruh* (17:85 itself says "you have not been given of knowledge except a little");
  - divine guidance (*hidaya*, 76:3);
  - faith, worship, moral rightness as content: modelling them would script culture, which ACL forbids;
  - consciousness, which behaviour cannot establish.
- **Risks, and how they were handled:**
  - **Choosing verses that fit:** disagreements were recorded (12:53's speaker; the seat of reason; the readings of
    30:30; the translations of 88:17), and so was where the link is weak.
  - **The models' agreement is not proof:** their critiques were used to find overreach, not to confirm.
  - **Translation:** only two translations were compared; nuances of the Arabic beyond these were not examined.
- **The overall honest answer:** the sources did not hand ACL new mechanisms that science lacks. But they did three
  useful things.
  - They pointed at one concrete unrealistic law (16:78).
  - They sharpened the question of knowledge media (96:4; Muslim 1631).
  - They supported a graded view of development.

  That is worth pursuing, with the labels kept.

## Council record (opinions, not sign-off)
- **GPT** (fresh chat `6ae7f84b`):
  - "none should be presented as scientifically derived from Islamic scripture";
  - H1 moderate overreach ("does not establish that learned dispositions cannot be inherited");
  - H2 and H4 significant overreach; H3 moderate, "the strongest conceptual connection"; H5 moderate.
  - Ranking: H3 94%, H1 88%, H5 83%. "Run H3's read-only mortality and knowledge-loss audit first."
- **Gemini** (fresh chat `7bad229d125ec614`):
  - H4 and H5 overreach and "relabel" standard algorithms; H2 relabels developmental psychology, and H3 stigmergy and
    external memory, "both, however, maintain clean textual alignment".
  - Ranking: H1 85%, H2 80%, H3 75%.
- **Where they differ:**
  - **H2:** Gemini sees clean alignment; GPT sees significant overreach. The council sides with GPT on the hadith,
    and keeps H2 on 16:78 and the ethnography.
  - **H1's sham:** Gemini prefers a neutral baseline; GPT wants a matched random draw. The council keeps GPT's
    matched sham as the test of content, plus the zero arm itself as the neutral baseline.

## Addendum (1 November 2026, evening): what is innate, for H1
**Spelke, E. S. & Kinzler, K. D. (2007).** "Core knowledge." *Developmental Science* 10(1): 89–96 (PubMed 17181705).
**Read: the abstract only.**
- "Human cognition is founded, in part, on four systems for representing objects, actions, number, and space. It may
  be based, as well, on a fifth system for representing social partners."
- "Each system has deep roots in human phylogeny and ontogeny."

**Bearing on H1** (the assistant's synthesis; [C], not a finding):
- Developmental science does not say newborns are blank: they come with structured **systems for representing** the
  world. Q 16:78's "knowing nothing" sits beside the "hearing, sight and minds" given at birth, and Ibn Kathir reads
  those as faculties.
- So the two can be read together: what is innate is **structure and faculties**, not **learned content**, such as how
  much a given action is worth in a given situation.
- H1 keeps everything innate in ACL: genes, instincts, the way situations are perceived. It removes only the inherited
  learned habit values. That makes H1 a cleaner test of "content versus structure", and it stays consistent with this
  literature.
