% The World That Nobody Wrote
%% A research history of the Artificial Civilization Laboratory
%% Living edition 2 · written after E6.6, while E7 was running · October 2026

# A Note Before Reading

This book is the intellectual history of the Artificial Civilization Laboratory, ACL. It is not the manual and it is not the rule book. The rules live in the World Bible. The design lives in DESIGN.md. The code lives in the repository. This book tries to keep what none of those keep: why each decision was made, what was believed at the time, what turned out to be wrong, and what the worlds did that nobody expected.

It is written for someone who finds ACL later and wants to know how it became what it is.

A few rules govern the writing, and they are the same rules that govern the experiments.

- Every number in this book comes from an experiment record in the repository: a frozen prediction file, a results file, an investigation, or an autopsy. Where a claim is an interpretation rather than a measurement, it says so.
- Failures are kept. A prediction that was wrong is recorded as wrong, next to the reasoning that produced it.
- Nothing is claimed before the evidence exists. Where an experiment is still running, the book says that and stops.
- The history is not tidied. Some ideas that seemed obvious at the time look naive now. They stay as they were.

The record has a beginning that is later than the project's. By the time the first experiment in the repository ran, the World Bible was already at version 7.1. The ideas of versions 1 to 6 survive only in what version 7 kept. This book begins where the evidence begins, and says so when it reaches further back.

One more fact belongs at the front. ACL has been built by one creator working with AI assistants. The assistants wrote much of the code and many of the reports. Some predictions in the record are signed by the creator and some by an assistant, and in at least one experiment their guesses were scored against each other. That collaboration is part of the history and is not hidden here.

# Part I — The Dream

## Chapter 1 — The Question

The project did not begin with code. It began with a doubt.

Every civilization simulator seemed to produce civilization. Yet when they were looked at closely, the answers were already inside the machine. Governments existed because someone programmed governments. Markets existed because someone programmed markets. Technology trees existed because someone decided what came before what.

The question that would not go away was this: if civilization were removed entirely from the design, would it ever come back on its own?

That question changed the goal. The goal was no longer to simulate a civilization. It was to find out whether one could appear without being written.

There was a second question underneath the first, and for a long time it was carried around under a name: Bob. Bob was not a character. Bob was a question about individuals. If a person were born inside a simulated world, learned from experience, formed friendships, kept memories, developed fears and habits, would that person be someone? Would they still be themselves if their experience were carried somewhere else?

Bob never appears in an experiment. But Bob explains a choice that runs through the whole design: every person in ACL is a particular individual with a particular history, never a statistic in a population model. If the second question is ever to mean anything, the first has to be answered with people, not with averages.

## Chapter 2 — What Is Wrong With Civilization Simulators

Most civilization simulations are not badly made. Many are beautiful. They fail at a different job: they cannot tell us anything we did not already put in.

A technology tree is a list of answers. When a simulated people discovers bronze after copper, nothing has been discovered. The designer discovered it, long before, and wrote it down. A happiness meter that rises with temples is not religion. A trade screen is not trade. A government chosen from a menu is not politics.

These systems are honest games. They are not experiments, and they never claimed to be.

The problem has a simple shape. If the outcome is written into the rules, the outcome cannot be evidence for anything.

There is a second, quieter version of the same problem, and it was the one that worried the project more. Even simulations that avoid technology trees often reward the right answer directly. Agents are paid for inventing, paid for trading, paid for cooperating. The behaviour appears, and it looks like emergence. But the reward was the recipe. The designer has moved the answer from the rules into the reward, where it is harder to see.

So ACL set itself a harder test:

- Nothing the people think with may contain a list of inventions.
- Nothing may reward an invention for being an invention.
- Nothing may tell anyone what is useful.

If civilization appears under those conditions, it means something. If it does not, that means something too.

## Chapter 3 — Four Kinds of Worlds

It helped to name what ACL was not.

A **game** is built to be played. Its rules exist to make choices interesting for a player. Whether its history is plausible does not matter, and should not.

An **agent simulation** has autonomous agents following rules, and studies what they do together. Flocking birds, traffic, epidemics. Agent simulations are often excellent science. But they usually study one phenomenon, with the phenomenon's ingredients put in on purpose.

A **civilization simulation** models the large structures of history: states, economies, wars, technologies. The structures are the units of the model. People, if they exist, are parts of the structures.

An **artificial civilization**, the thing ACL is trying to make, is different from all three. It has no player. It has no single phenomenon under study. It has no large structures in its rules at all. It has individual people, a physical world, and time. Any structure larger than a person has to be built by people, out of what they do, or it does not exist.

That last kind may not be possible. Part of the point of ACL is to find out.

## Chapter 4 — Open-Endedness, Success and Failure

The word that kept coming back was **open-ended**.

A world is open-ended if it keeps producing things that are genuinely new: new kinds of objects, new behaviours, new traditions, new possibilities, and not only new combinations of a fixed list. Life on Earth is open-ended in this sense. Human culture is, at least so far. Almost no simulation is. Most settle, after a while, into a steady state where nothing new appears.

From the beginning the project tried to say in advance what would count as success and what would count as failure, so that it could not later redefine one as the other.

Success, at its most modest, would be culture of any kind appearing without being scripted: practices passed from person to person, symbols that come to mean something, knowledge that outlives its discoverer. At its most ambitious, success would be a world where novelty does not stop: where year five hundred contains things year fifty could not have contained.

Failure could take several forms, and each was named:

- **Nothing happens.** People survive or die and never accumulate anything.
- **Something happens, but it was scripted.** The result is real but the experiment is void, because the answer was put in.
- **Something happens, then stops.** Culture appears, settles, and freezes.

By October 2026 ACL had clearly avoided the first failure, worked hard to avoid the second, and run straight into the third. Most of this book is about the third.

# Part II — The Philosophy

The principles below were not handed down at the start. Most were written after something went wrong. For each, this part records why it exists, what it prevents, and what was considered and rejected instead.

## Chapter 5 — Nature Is Programmed; Culture Is Written by Nobody

**Why it exists.** This is the founding rule, and every other principle is a way of keeping it. The creator writes the physics, the bodies and the feelings: what hunger is, how winter works, how flint breaks, what grief does. The creator does not write tools, fire-making, dwellings, sowing, trade, leaders, feuds or myths. Those must come from people living under nature's rules.

The World Bible puts it in one sentence: the creator writes the laws of the universe, not the history.

**What it prevents.** It prevents the most common failure of the field: getting out exactly what was put in.

**What was rejected.** The obvious alternative was a light technology tree, just a few steps, to get things started. It was rejected because there is no safe size for a script. If the first step is written, every later step stands on it.

**What it costs.** The rule is brutal in practice. It means the people of ACL start with nothing and may never get anywhere. It means long stretches of watching a world do very little. And it means the line between nature and culture has to be argued case by case. Is fear of wolves nature or culture? ACL's answer: the capacity to fear is nature; fear of wolves in particular is learned, from being hurt, from seeing someone hurt, or from being told.

## Chapter 6 — No Teleology

**Why it exists.** Teleology is explanation by purpose: things happen because they are heading somewhere. A simulation is teleological when its rules assume a destination, such as progress, complexity or civilization, and push toward it.

ACL's people have no purpose built in beyond staying alive and the pulls of their own feelings. Nothing in them wants to invent, advance, or build. No rule rewards a world for becoming more complex.

**What it prevents.** It prevents mistaking a designed drift for a discovery. If worlds are nudged toward complexity, complexity proves nothing.

**What was rejected.** Rewards for novelty itself, rewards for invention, and fitness functions over whole worlds were all considered and set aside. A curiosity drive exists, but it is a pull toward the untried that comes from temperament, not a reward for being inventive.

**An example.** When the people of E1 made blades within the first year, nobody had wanted a blade. A person struck flint with flint, often while playing, and was left with a sharp edge. The edge helped them forage. Whether a blade appears in a world at all depends on whether that accident happens and whether the help is felt.

## Chapter 7 — No Special Inventions

**Why it exists.** If the code treats some inventions as special, with their own rules, events or names, then those inventions have been chosen in advance. ACL tries to make every made thing an ordinary consequence of the same physics.

**What it prevents.** It prevents a hidden tree. A rule for "spear" is a branch of a tree, even if no tree is drawn.

**How it is enforced.** Two ways. First, the people's code contains no names of inventions at all. A test reads the source and fails if words like pot, kiln, cooking or boiling appear where people think. That test has already caught the project's own authors: during the E7 audit an event was named with a banned word, the test failed, and the name was changed. Second, names exist only in the historian, which watches from outside and calls a thing a raft or a blade by its properties after the fact. A separate test checks that the historian never changes anything a person does.

**What was rejected.** Named recipes, recipe books, and lists of combinations with known outputs.

## Chapter 8 — The Indifferent World

**Why it exists.** The world has no main character and protects no one (Law 10). Rain falls where it falls. Storms put out the fires of the careful and the careless alike. A band of five on a small island with no partner for anyone dies out, and nothing intervenes.

**What it prevents.** It prevents a world tuned to make the story come out well. A world that saves the last survivors, or sends rain when a people is dying of thirst, is a world with an author.

**What it costs.** Extinction. Two of E1's eight worlds died out. Three of E5's did. In E4, under the E2 code, nine of twenty-four worlds were gone by year 200. These losses are not bugs. They are what an indifferent world does. The project's discipline is to report them and to ask why they happened, not to prevent them.

## Chapter 9 — Properties, Not Recipes

**Why it exists.** In ACL, materials are bundles of physical properties: how sharp, how long, how hard, how well they hold things, how warm, how well they float, how tight, how soft. Two physical acts change materials: striking one against another, and tying two together. What a made thing does follows only from its properties. A thing with edge and reach helps hunting. A thing that contains helps carry food. A thing that is warm helps in winter, when worn.

This is Law 105: properties, not recipes.

**What it prevents.** It prevents the designer from deciding what can be made. Nobody listed the raft. The raft exists because wood floats a little, tying two floating things together adds half the smaller one's float, and a certain float lets a person stand on water. The first person to tie two sticks together made a raft whether anyone meant it or not.

**The cost, discovered later.** Properties do not guarantee depth. With six materials and two acts, the space of things that can be made runs out fast. E1 found 54 possible one-step actions on raw materials, 14 of which already made a named kind. This became one of the suspects in the freeze described in Part III.

## Chapter 10 — Uses Must Be Discovered

**Why it exists.** An object is useful because someone experiences a consequence that matters to them, not because the creator knows its human meaning (Law 109). And after E1, a stronger version was added: uses must be experienced (Law 124). It is not enough that a use exists. Someone has to live through it.

**What it prevents.** It prevents declaring value. If the code says rafts are valuable, rafts will be carried, and nothing has been learned about whether a people would come to value them.

**The example that wrote the law.** In E1, rafts were invented in the first few years and almost never used, because nothing ever let anyone feel what floating was for. The fix in E2 was not to reward rafts. It was to make crossing water a felt event, the moment it happened, visible to the person and to anyone watching. Law 124 was written from that story, which is told in full in Part V.

## Chapter 11 — Conditions, Not Outcomes

**Why it exists.** This is the working form of the founding rule, and the question the creator method asks before any new system is added (M7): does this create a condition that people can use, or does it quietly script the social result?

Rather than asking how to create trade, ask what conditions make exchange useful. Rather than asking how to create government, ask what pressures make coordination valuable. Rather than asking how to make people fill vessels with water, ask what in the world could ever show them that a vessel holds water.

**What it prevents.** It keeps interventions on the world side of the line. When something does not emerge, the temptation is always to add it. This principle says: add the condition, never the outcome, and if the condition is not enough, find out why before adding anything else.

**An example from E7.** When the autopsies found that nobody ever filled a vessel, the project had two choices: change the people so they try such things, or change the world so it sometimes does the first step itself. It chose the world. Rain falls into an open watertight thing. A fire hardens clay beside it. These are physics, not scripts. Whether anyone then makes use of them is still up to the people.

## Chapter 12 — Known Compromises

A book that claims principles should also list where they are not yet kept. These are the places, known in October 2026, where the code falls short of its own philosophy.

- **Speech is English.** The conversations a visitor sees in the viewer are an English rendering of what really passed between people: news, a skill taught, a thanks, an accusation. The people have no language of their own yet. The marks they scratch are the only symbols that are truly theirs.
- **A floating instinct.** A person carrying something that floats well enough will set out across the water toward land they have seen, or sometimes at random. That knowledge, that a floating thing is a way across the sea, is supplied rather than learned. It was found in a review of the code in October 2026 and has not yet been removed.
- **A fixed list of pulls.** The kinds of things that can pull at a person's mind (hunger, worry, a puzzle, grief, cold and so on) are a fixed list. Goals can attach to particular things a person has found, but the kinds of goal cannot grow.
- **Fixed situations for habits.** Habits are learned for a fixed set of situations. The people cannot invent new situations to have habits about.

None of these is hidden in the code, and all are recorded in the implementation status documents. They are listed here because a history that only records its principles, and not its compromises, is a kind of advertisement.

# Part III — The Great Mistakes

This part is chronological. For each experiment it records the hypothesis, what was expected, what happened, what surprised the project, and what changed afterwards. Every experiment had its predictions written and frozen before it ran. The scorecards are reproduced honestly, including the many predictions that were wrong.

## Chapter 13 — E0: Mind Before Civilization

**Context.** E0 was the first experiment kept in the record. World Bible 7.1, world version 0.1, agent version 0.1. Ten founders in two bands of five, 500 simulated days, seed 42.

**Hypothesis.** The governing question was modest: does the agent architecture produce behaviour that cannot be explained as simple scripted reactions?

**What was expected.** The frozen predictions expected survival to dominate early action; prediction error to be small for foraging and resting and large for social acts, because people had no model of each other; fertile land to attract people; successful actions to become more common; friendships to reinforce themselves; the two bands not to meet; and invention to be rare or absent in the first fifty days.

**What the record keeps.** The repository preserves E0's frozen predictions and the script that ran it. A scored report was not kept alongside them. This is the first small gap in the record, and it is noted here rather than filled in from memory.

**What changed afterwards.** E0 established the habit that every later experiment kept: predictions first, frozen, in a file of their own. It also established a single decision interface, through which every choice passes and is recorded, written so that the mind could one day be replaced without rewriting the world.

## Chapter 14 — E1: Long Histories

**Context.** Eight worlds, seeds 101 to 108, up to 200 years each. Twenty founders per world in four bands of five, each band on its own island. Features frozen for the whole experiment.

**Hypothesis.** With bodies, feelings, memory, learning and physics in place, culture of some kind would appear and persist across generations.

**What was expected.** Nineteen frozen predictions. They covered survival, symbols, false stories, invention, the life of techniques, trust and puzzles.

**What happened.** Ten predictions were confirmed, eight were wrong and one was unclear.

The confirmed ones were the big ones. Two of eight worlds died out and six held or grew. All eight worlds had a shared symbol at some point; 763 shared symbols formed in all, mostly meaning water, shelter or a grave, and 261 of them reached people born after they formed. Myths, false stories shared by several living people, appeared about twice per world per century. Every world invented all six named kinds of thing by year 100. In every surviving world, a technique still known at the end was held by people two or more generations after its inventor. In every surviving world, fire was struck after someone had puzzled over sparks.

The historian also recorded things nobody predicted. A building practice, heaping materials against the cold, persisted for about 190 years in seven of eight worlds and produced real dwellings. A killing in year 20 was still remembered 180 years later by 62 people across five generations, though later generations often blamed the wrong person.

The wrong predictions were wrong in instructive ways. Symbols lasted less than expected. Wrong versions of stories were far more common than expected; in one world, three quarters of the stories people held about events were wrong. Trust was weak and spread thin. And trust had nothing to do with truth: the correlation between how often a person was right and how much others trusted them was −0.066. Trust followed food. People trusted those who fed them.

**What surprised the project.** Two things. First, how much culture appeared from so little. Second, the raft: invented in year zero in almost every world, and almost never used. That story is told in Part V.

**A mistake in the report itself.** E1's report said that about five claims were tested per world-year. That counted a claim once for every person who had passed it on. Counted properly, once per test, it was about two. The correction was published in E2's results, not quietly fixed.

**What changed afterwards.** Four changes, made together and tested in E2: reputation earned by tested accuracy rather than goodwill; many more chances to test what one is told; traces and marks as records that can teach; and floating as an experienced affordance, with the three-tile jump across water removed.

## Chapter 15 — E2: The Four Changes

**Context.** The same eight seeds as E1, 200 years each, after the four changes. The predictions were written on 2 October 2026 from short spot checks, before any full run.

**Hypothesis.** Making reality checkable, letting credibility be earned, letting records teach, and making floating felt would each produce its intended effect, without breaking the world.

**What was expected.** Ten predictions, and a kill criterion added before any results were read: the changes would be declared failed if testing stayed rare, reputation did not track accuracy, nobody crossed open water, nobody learned anything from a mark, or the population at year 100 fell below half of E1's.

**What happened.** The changes did what they were meant to do. Tested claims rose from about two per world-year to 33. Reputation came to track truth: the correlation between a person's accuracy and others' records of them reached 0.59. Open water was crossed in every world. Techniques were taken up from marks in every world that lived, and in three worlds a skill that nobody alive knew was recovered from a mark.

But five of ten predictions were wrong. The biggest was the population. Mean population at year 100 fell from 46.6 to 28.1. The kill criterion's limit was half of E1's, 23.3. E2 came within five people of failing its own test.

**What surprised the project.** Births fell by a third, and the causes of death did not change. Something about the four changes was costing lives, and nobody could say what.

**What changed afterwards.** Nothing was built. The next two experiments were spent finding out what had happened.

## Chapter 16 — E3: Chasing the Missing Births

**Context.** No world was changed. E3 replayed the first century of every E1 and E2 world, confirmed that each replay matched its saved experiment exactly, and followed the chain from fertile woman to birth step by step.

**Hypothesis.** There were several, and they were written down with probabilities before any analysis. The creator put 60% on island separation: with the jump gone, fewer people could reach a mate. Other explanations covered time and attention spent elsewhere, health thresholds, and infants starving in their mothers' care. One of them was the assistant's.

**What happened.** The pooled birth rate per fertile woman hardly moved: 0.146 in E1, 0.144 in E2. People's choices hardly moved either: fertile adults foraged 44.4% of their weeks in E1 and 44.1% in E2. Infants went hungry in 5.9% of infant-weeks in E1 and 6.2% in E2. Almost every predicted mechanism was not supported.

One world showed island separation exactly. In seed 105, almost nobody had a possible mate on their own island. Partnered women fell from 44% to 21%, births from 80 to 22 per century, and the world dwindled away. The excess infant deaths were concentrated in a few worlds; seed 107 alone had 20 of E2's 53 starved infants.

**What surprised the project.** That the honest answer was "we cannot tell". Eight worlds were not enough to separate a real effect from bad luck.

**What changed afterwards.** E4, a replication large enough to decide.

## Chapter 17 — E4: Replication

**Context.** Twenty-four worlds, sixteen of them new, each run under both the E1 code and the E2 code. Both codes were kept and verified. The decision rule was frozen in advance: E2 would count as a real effect on population only if it was lower in at least 17 of 24 worlds.

**What happened.** E2 was lower in 18 of 24. The mean gap at year 100 was 18.4 people, with a 95% interval from 9.8 to 27.2. The effect was real. Infant starvation, the explanation E3 had leaned toward, was noise: 68.8 against 67.6 per thousand infant-years.

The cause turned out to be island separation after all, but not in the way first imagined. Every world starts with four bands of five. Under the E1 code, 70% of bands ever had children with another band; under E2, 39%. A band of five that never mixes almost always dies out, under either code: everyone on its island ends up related, and nobody is left to pair with. Only 17% of never-mixed bands still had a living line at year 100. E2 did not make isolation deadlier. It made isolation far more common: 59 bands never met another band, against 29 under E1.

**What surprised the project.** That the creator's first guess had been right, and that it took two experiments to show it. And that the cost reached beyond population: techniques tried fell 28% and their median life 39%. Fewer people keep fewer things alive.

**The scorecard.** Of six predictions, two were confirmed, three were wrong and one was untestable as stated. The untestable one had been measured wrongly at first, between any two islands rather than between the islands where bands started, and the correction is printed in the results.

**What changed afterwards.** The four changes were kept. Their gains held in every world that lived. But the project now knew that walls of water are deadly to small peoples, and that every change to physics can reach into demography.

## Chapter 18 — E5: The Millennium

**Context.** Eight new worlds, seeds 301 to 308, current code, every feature frozen, one thousand years each.

**Hypothesis and expectations.** The predictions were cautious and mostly about long-term structure: at least three worlds would die out; surviving worlds would rarely keep two populated islands; there would be no distinct peoples; a long tradition would outlive its founders.

**What happened.** Most predictions were confirmed. Three worlds died out: two within 55 years, from starvation, thirst and neglected children, and one slowly after 419 years, mostly from illness. Five reached year 1000 alive, with 36 to 86 people each. Populations held flat for nine centuries, at 30 to 90 people, with births matching deaths.

In almost every world, one people remained. And it was usually not a mixed people. In four worlds, everyone alive at year 100 descended from a single founding band of five; the other three bands left no descendants. The usual path was not merging but one band outliving the rest.

Some traditions lasted the whole millennium. The simplest carrier, fibre tied to fibre, was held in five worlds for all thousand years. A replay of the last century showed that about three in four people who came to hold it had been taught it; the rest found it again themselves.

**What surprised the project.** The freeze. Every kind of tool any world ever had, whether carrier, boat, club, blade, spear or warm wrapping, first appeared within the first eleven years. Then nothing new appeared for 990 years. Knowledge peaked around year 50 to 100 and then thinned: the number of techniques known at once fell from a peak of 95 to 156 to between 11 and 19 by year 1000. Most of what was lost was the clutter of play, forgotten; but not all of it. Spears were lost in every long-lived world, between years 141 and 487, and never came back. Warm wrappings were lost in all of them.

The world at year one thousand looked much like the world at year thirty, and sometimes poorer.

This was not a bug. The experiment worked exactly as designed. That made it harder to dismiss. The worlds had history. What they lacked was open-ended history.

**One prediction was wrong in an interesting way.** It said there would be no distinct peoples. Seed 301 kept two, side by side, for the whole millennium. Their story is told in Part V.

**What changed afterwards.** The central question of the project changed. It was no longer whether culture could emerge. It clearly could. The question became: why does novelty stop?

## Chapter 19 — E6: Richer Matter

**Context.** Two arms: the E5 code as a baseline, and the E6 code with new physics. Seeds 301 to 308, one thousand years each.

**Hypothesis.** Perhaps the world was too poor. If matter had more properties and more could be done with it, history might keep finding new things. E6 added continuous properties (mass, heat, wetness, tightness, softness), clay by rivers and lakes, and three new acts: holding something in a fire, filling something, and pressing soft stuff into a shape.

**What was expected.** That novelty would continue for centuries: in at least half the long-lived worlds, the latest lasting novelty would appear in year 300 or later.

**What happened.** It did not. In every E6 world that lived 300 years, the latest lasting novelty appeared by year 66. Across all eight worlds, 578 lasting novelties appeared in the first century and none after. The verdict, applied by the frozen rule, was: **bottleneck remains**. Four of six predictions were wrong.

People did take up the new physics, but only the shallow end of it. They shaped clay heavily: 36 to 61 shaped kinds per world. They never fired a shaped thing. In all eight worlds over up to a thousand years, exactly one thing was ever changed by being held in a fire. Nobody ever filled a vessel. No water and no fire were ever carried anywhere.

E6 worlds were also harsher, and the cause was never established. Four of eight died out, against three in the baseline. Seed 306 lived 1000 years under the baseline code and 124 under E6.

**What surprised the project.** That richer possibilities changed almost nothing. And one small thing it had not looked for: in two of the four surviving E6 worlds, traditions began after year 100 and lasted 100 to 670 years. No baseline world had any. They used the old mechanics, placing things and making marks, not the new physics. Two worlds against none is suggestive at most.

**What changed afterwards.** The project stopped asking what possibilities were missing and started asking why possibilities stayed undiscovered. It stopped running new worlds and started dissecting old ones.

## Chapter 20 — E6.5 and E6.6: The Autopsies

**Context.** Two read-only investigations. E6.5 replayed two E6 worlds from week one with probes that recorded every decision and every option weighed. E6.6 measured how far back in time people can learn from a consequence.

**What happened.** E6.5 found the single broken link in two chains of discovery, and named it: interaction, the first try. E6.6 showed that the obvious alternative explanation was wrong: people learn from delayed consequences well, as long as the consequence comes back through a thing they still hold or a place where they left something. Both are told in detail in Parts IV and V.

**What changed afterwards.** E7 was designed directly from these two findings.

## Chapter 21 — E7: The Experiment That Almost Died Before It Began

**Context.** E7 asks the question the autopsies left behind. If nature performs the first transformation itself, will people take up the rest? Rain fills any open watertight thing. Wading into a river or lake fills it. A fire hot enough hardens dry clay carried beside it. The people's minds were not touched: their decision, body, thought and action code stayed byte for byte the same as E6. Seven predictions, a decision rule and named failure modes were frozen on 3 October 2026, before any E7 code was written.

**What went wrong before the first run.** On 4 October, before any world ran, the E7 code was audited line by line against its own pre-registration. Six problems were found.

One of them would have ended the experiment on its own. When clay hardened by a fire, the new recipe was stored under the wrong field name, and the next time that person made a decision, the world crashed. All the tests passed, because none of them let the world keep running after a firing. The first piece of passively fired clay in any world would have stopped the run and triggered E7's own kill criterion.

The others were quieter, and each would have meant testing something other than what was registered. Rivers never filled anything, because in this world rivers can be waded and do not count as water tiles. Everyone standing by a fire had all their food treated as cooked for free, which the design never said. The fire's real heat was ignored. Plain lumps of clay were never fired, only shaped ones. And a heap with a light cover kept the rain out when the design said it needed more than half.

All six were fixed, recorded in a separate note, and frozen under a tag before the first world ran. The pre-registration itself was not edited.

Two parts of the design turned out to have nothing to act on. In this world, made things are only ever carried; nothing can be set down on a tile, so nothing on a tile can catch rain. And each person's food is one pooled amount with no age, so "food eaten past its natural rot" cannot be measured.

**Status at the time of writing.** Sixteen worlds are running, eight with the passive physics and eight under the E6 code, a thousand years each. The answer is not in, and this book does not guess it.

**The lesson so far.** An experiment can be lost before it starts, quietly, inside a single field name. Auditing code against its pre-registration belongs in the method, not after the results.

# Part IV — The Discoveries

These are the ideas the project did not have when it started. Each came from evidence, and each is stated as strongly as the evidence allows and no more.

## Chapter 22 — Civilization Is a Chain

The autopsies produced a framework that now organises almost all of the project's thinking. For a discovery to become part of a culture, it has to pass through six links:

**Opportunity → Interaction → Transformation → Observation → Reuse → Tradition.**

- **Opportunity:** the right things are in the right place at the right time. Someone holds dry clay at a fire. Someone stands at a river holding a vessel.
- **Interaction:** someone actually does something with them.
- **Transformation:** the world changes something as a result. The clay hardens. The vessel fills.
- **Observation:** someone notices a consequence that matters to them.
- **Reuse:** they do it again.
- **Tradition:** others learn it, and it outlives them.

A discovery must survive every link. The records show breaks at every one. Many transformations happened with no one observing a consequence. Many observations were never reused. Many reused techniques died with their only holder. The longest-lived things in ACL, such as the fibre carrier held for a thousand years, are the ones whose chain is short and strong: easy to stumble on, useful at once, easy to teach, and easy to find again if lost.

Seen this way, civilization looks less like a single event and more like a fragile chain, made again and again, in which each link must hold.

## Chapter 23 — The Topology Principle

Most inventions are multipliers. A sharper blade cuts a little faster. A better carrier carries a little more. They make life easier. They do not change what life can be.

Some inventions change the map. A raft reaches land that could never be reached before. A container lets people live where there is no water. A bridge joins two regions. These do not improve a quantity. They add new connections to the graph of the possible, and every later history runs on the new graph.

The phrase used inside the project was: **topology changes history**.

The evidence for it is still mostly negative, and that should be said plainly. The raft changed the map, and once its use was felt, islands began to connect: from almost no open-water crossings in E1 to between 7 and 167 per world in E2. The watertight vessel could have changed the map, by making dry land livable, and in E6 it never did, because it was never filled. Everything else ACL's people made was a multiplier, and in E5 the whole list of kinds was complete within eleven years and never grew again.

The working hypothesis is that open-ended history needs a steady supply of map-changing inventions, and that a world whose physics offers only multipliers will freeze. It is a hypothesis, not a result.

## Chapter 24 — Why Delayed Utility Is Difficult

Many of the most important inventions in human history pay off later and somewhere else. Stored grain feeds you in winter. Carried water saves you in the desert. A sown field feeds you next year.

E6.6 measured how far back ACL's people can learn, and found three channels.

- **By place:** beliefs about what happens when something is left somewhere. These learn from outcomes up to a year later, the whole length of a person's memory for what they left where. Beliefs moved by outcomes 27 to 52 weeks later changed behaviour as much as those moved 5 to 12 weeks later.
- **By thing:** the worth of a made thing. While the thing is still held, there is no limit. Things first used more than a year after they were made were made again more often, 47%, than things used at once, 16%.
- **Habits:** the weekly learning of what kind of action goes well in a situation. These forget fast: a reward five weeks later counts a third as much, and one twenty weeks later almost nothing.

So delayed utility is not, in itself, the problem. If a vessel had ever been filled and later drunk from, far from a spring, the thing channel would have carried that lesson back to its maker.

The difficulty is the step before. A delayed payoff gives nothing to pull on at the moment the act would have to be chosen. People learn delayed consequences well. They almost never take a first step that pays nothing now.

There is a cost hidden in the place channel too, and it should be recorded. It credits everything left at a spot in the past year, whether or not it caused the outcome. It learns long delays, but without discrimination. Superstition is built into it on purpose (Law 71).

## Chapter 25 — Why Transmission Alone Is Not Enough

Before the autopsies, a natural guess was that knowledge was being lost: people found things, then died before teaching them. The records show that this happens. In E1 there were 3,828 losses of a technique against 789 rediscoveries.

But the autopsy of seed 304 showed something more interesting. The only watertight vessel in E6 was taught by its maker to three people. The recipe passed on, slightly garbled, to four more, and lasted sixty years after it was invented. Transmission worked.

What was transmitted was a carrier. The vessel's one world-changing property, that it could hold water, was never seen by anyone, so it was never part of what was taught. A tradition can only carry what someone has observed.

Transmission is a multiplier on observation. It cannot create the observation.

## Chapter 26 — Why Opportunities Alone Are Not Enough

E6 was built on the idea that richer opportunities would produce richer history. The autopsy counted the opportunities, and the numbers ended that idea.

In seed 304, a person holding a watertight vessel stood at fresh water for 102 adult-weeks. In none of them was filling it among the top four options considered. Across the first century of two worlds, people stood at fires with raw food they could have heated for dozens of adult-weeks, and never once did it.

Opportunity was not the missing link for water. For heat, it was rare, because fires are rare and brief. But even when the opportunity was there, nothing happened.

An opportunity that nobody acts on is invisible. A world can be full of possibilities and still have no history.

## Chapter 27 — Isolation Kills Small Peoples

This was not looked for. It was found while chasing a population drop.

A band of five people alone on an island almost always dies out. Within a few generations everyone is related, and nobody is left to pair with. In E4, only 17% of bands that never mixed with another band still had a living line at year 100. Of the bands that did mix, 82% did under the E1 code.

This changed how the project thinks about walls. Every barrier in the physics, such as a wider channel or a removed jump, is also a demographic decision. Small changes to movement rules decided which founding bands would have descendants at all. In most of E5's long-lived worlds, everyone alive descended from a single band of five.

## Chapter 28 — Belief Is Not Practice

Several findings, gathered across E1 and E2, warn against treating a person's beliefs, behaviour and circumstances as one thing.

- Sowing beliefs persisted after sowing itself faded, because the payoff to the sower was weak. People went on believing in a practice they no longer did.
- In E1, trust followed food, not truth. People trusted those who fed them, and how often a person was right had nothing to do with how much they were believed. Only after E2 made claims checkable and records personal did reputation begin to track accuracy.
- Stories outlived their events and drifted. A killing was remembered for 180 years and was often blamed on the wrong person. A grudge against the wrong person is still a grudge, and people acted on it.
- Knowing how to make a thing is not using it. In E1, between 10 and 44 people per world knew how to make something that floats. Between 0 and 3 carried one.

The lesson for the design is that these must stay separate variables. A world where people always believe what is true, always do what they believe, and always value what is useful would be simpler to build and would teach nothing.

# Part V — Case Studies

These are stories from real worlds. Every name is a person who lived in a seeded world, and every event is in the record.

## Chapter 29 — The Raft Story

The islands were meant to keep peoples apart. Each founding band started on its own island, and without something that floats, nobody could cross.

So the first question about E1 was simple: when do they invent the raft?

The answer was embarrassing. Almost immediately.

A raft in this world is two pieces of wood tied together. Raw wood floats 0.5. Tying two floating things adds half the smaller one's float, so two sticks make 0.75, and 0.65 is enough to carry a person. Wood is the commonest material near any camp. In every E1 world someone tied two sticks together within the first three years, often within weeks.

And then nobody used it.

Of 5,682 crossings between islands in E1, 92% were made with nothing that floats at all, over channels three tiles wide or less, a gap the movement rules had quietly allowed people to jump. Over open water there were three crossings in 1,462 world-years.

Between 10 and 44 people per world knew how to make something that floats. Between 0 and 3 carried one. The investigation found the reasons. Nothing in the world ever judged a thing by how well it floats. People carry their three most valued things, and a raft was valued at about 0.1, as a slightly awkward club. And when someone holding one did go to sea, they chose a random far shore, and the target changed every week.

The raft was invented and forgotten at the same time.

E2 changed the world, not the people. The jump was removed: water now blocked walking. Far shores could be seen. Crossing to new land became the thing that gave a raft its worth, the moment it happened, and anyone watching could see it. A sea trip kept its heading.

Open-water crossings rose from almost none to between 7 and 167 per world.

There was a cost, found only later. Removing the jump also isolated many small bands, and isolation killed them. The same change that let rafts matter made the world harsher for those who never built one. Part III tells how long it took to see that.

**Why it mattered.** The raft story wrote Law 124: uses must be experienced. An invention does not matter when it is made. It matters when its use is lived through. It also set the pattern every later intervention tried to follow: change the world so the consequence can be felt, never reward the invention.

## Chapter 30 — The Pottery Mystery

E6 gave the world clay: soft wet earth by rivers and lakes, things that could be pressed into shapes, heat that dries, burns and hardens, and tightness, the property that decides whether a hollow thing holds water.

Everything needed for pottery was there. Nothing was named pottery. No line of code said pot, kiln or cooking, and a test made sure of it.

The people took to clay at once. They shaped it heavily, pressing it into points and hollows and binding the shapes into larger things. Between 36 and 61 shaped kinds appeared per world.

Then they did nothing else with it.

In eight worlds, over up to a thousand years each, one thing was ever held in a fire and changed by it: a raw lump of clay, once, in seed 302. No shaped thing was ever fired. No food was ever held in a fire by three or more people in any decade. Nobody filled anything with water.

The physics worked. Every test passed. The possibility was real, and it stayed shut.

**Why it mattered.** The mystery could have been explained in several ways: too little opportunity, no reason to try, no notice taken, no one to teach. Each explanation called for a different intervention, and the project had already learned not to intervene on a guess. So instead of changing the world again, it performed an autopsy.

## Chapter 31 — Beimak and the Fired Clay

The only fired clay in E6 was made by a child.

Beimak was four years old, in seed 302: curious, and not very diligent. In year 13, playing at a fire of heat 5, Beimak held a dry lump of clay in it. The clay set: hardness 65, tightness 50.

Beimak remembered having made it. The recipe was kept, as a thing once made. No puzzle formed about it. Beimak never used it and never made it again, and never taught it to anyone.

Fourteen weeks later, Beimak starved to death, aged four. Nobody else knew how it had been done. Two weeks after that the knowledge was gone from the world.

That was the whole history of pottery in E6: one child, one lump, sixteen weeks.

**Why it mattered.** Beimak's lump showed that the transformation link worked. Heat did what the physics said. It also showed how rare the opportunity was: across the first century of that world, adults stood at a fire holding a dry, fireable shaped clay thing in only three weeks. And it showed that the people most likely to try something new are the ones who play, and in ACL that means children, who are also the most likely to die.

## Chapter 32 — Reibik and the Forgotten Container

Reibik was a founder in seed 304, about 38 years old, very sociable and not especially curious. In year 12, playing with materials, Reibik bound hide to bone with fibre and made something unusual. It held 53 and its tightness was 60. It could carry about five weeks of water.

It was the only watertight thing ever made in E6.

And Reibik valued it. Reibik used it 104 times as a carrier, and its worth rose with each use. Reibik made it again in year 14 and carried it for years, and taught it to three people in years 15 and 16. The recipe passed on, slightly garbled, to four more people over fifty years, and lasted until year 72, long after its maker.

Every link of transmission worked.

But the probe showed something else. Reibik stood at fresh water, holding a vessel that could hold water, for 102 adult-weeks. In none of those weeks was filling it among the four things Reibik considered most. Reibik foraged in 38 of them, gave food away in 22, talked in 21 and went to see people in 20.

Why? Filling something with water pulls on a person only as something untried, and that pull grows with how much thirst they have known. Someone who lives by a river has known almost none. The pull was about 0.04. Ordinary choices pull between 0.3 and 1.

The person holding the vessel was never thirsty. The thirsty people had no vessel.

**Why it mattered.** What spread through seed 304 for sixty years was a carrier. The thing that could have made dry land livable was in people's hands the whole time, and nobody ever saw what it was. Reibik is the clearest single case of the interaction bottleneck, and the reason E7 exists.

## Chapter 33 — The E6.5 Autopsy

The autopsy deserves a chapter of its own for its method, not only its findings.

After E6, it would have been easy to guess at the problem and add a fix. The project did something slower. It replayed two worlds, 302 and 304, from their first week, with probes that only read. Every decision was recorded: was there an opportunity, was the step among the person's top four options, what did they choose. Every time anything was held in a fire was recorded. The one rare thing in each world was followed through its whole life.

Before trusting a single number, the replays were checked against the saved worlds. Both matched exactly at year 100. The probes had changed nothing.

Then each link of the chain was scored, separately for heat and for water.

- **Opportunity:** very rare for heat, two or three adult-weeks per century at a fire with something fireable; plentiful for water, 102 weeks.
- **Interaction:** never chosen on purpose for either. The one fired lump came from a child's random play.
- **Transformation:** worked whenever it happened.
- **Observation:** weak. The fired clay was never used. The vessel was valued only as a carrier.
- **Reuse:** none for the clay; plenty for the vessel, as a carrier.
- **Tradition:** the clay lost in sixteen weeks; the vessel taught to seven people over sixty years, as a carrier.

The autopsy ended with options, not a decision: mend the chain from the world side, by letting the world show the property by itself, or from the people's side, by having them try things in context more often. It recorded that the creator preferred not to change the people. The choice was left to the creator.

**Why it mattered.** It replaced a guess with a measurement. Every fix proposed before the autopsy would have targeted the wrong link.

## Chapter 34 — The Interaction Bottleneck

Put the autopsy and the reward-horizon study side by side, and the problem has a precise shape.

Opportunity was not the main problem for water: Reibik met it 102 times. Transformation worked whenever it happened. Transmission was good enough to carry a recipe for sixty years. Learning from delay worked: had the vessel ever been filled and later drunk from far from water, the lesson would have reached back to its owner through the thing they held.

It never started, because the vessel was never filled once.

The broken link was interaction: the very first try.

People in ACL try new things almost only in play, and adults play in about one week in a hundred. An act with no reward now, whose payoff comes later and somewhere else, has nothing to pull on. In a sense the people are too sensible. They do what has worked before.

There were two ways to mend it. Change the people, so they handle what they hold with what is around them more often. Or change the world, so it performs the first step itself, the way crossing water once showed the raft its worth.

The project chose the world, for now, because it keeps the people unchanged and so keeps the experiment clean. It did so knowing that it may be the wrong side to mend from, and E7 was designed to tell the difference: if the world produces many first encounters and nobody takes them up, the bottleneck is in the people after all.

## Chapter 35 — Two Peoples Who Never Met

In E5 the frozen prediction said there would be no distinct peoples. Seed 301 proved it wrong.

Two islands, 15 to 53 people each, lay side by side for 990 years. In a thousand years not one person on either island formed a relationship with anyone on the other. They never met.

One island descended entirely from a single founding band of five. The other descended from two bands that merged before year 100. Their temperaments drifted apart early, to a steady gap, while which traits differed kept changing over the centuries.

Their cultures differed in ways nobody designed. One island held practice beliefs, leaving fibre, stone and wood at places in particular seasons, the building practice first seen in E1. The other held none, in every sample for a thousand years. The other bound things with hide and worked bone; the first did not. Their marks shared nothing: each made its own shapes for rabbits, graves and water. About half their techniques overlapped.

**Why it mattered.** It showed that distinct cultures can form and hold without being written. It also showed the limit of that result. The prediction about rival identity scored "confirmed", but only because the two peoples never met. Rival identity needs contact. It was not tested, and it was not refuted.

## Chapter 36 — The Killing Remembered for 180 Years

In one of E1's worlds, someone was killed in year 20.

One hundred and eighty years later, 62 people across five generations still remembered it. None of them had been alive when it happened. It had reached them the only way anything reaches anyone in ACL: parents telling children by the fire, neighbours passing on news, stories retold and slightly changed each time.

By then, the later generations often blamed the wrong person.

**Why it mattered.** It was the first clear evidence that ACL's people could carry history beyond living memory, which is the beginning of what a culture is. And it showed, in the same breath, that what is carried is not the same as what happened. A people's past is something they make out of retellings. ACL does not correct them, and should not.

# Part VI — The Science of Open-Endedness

The method was not designed at the start. It grew out of mistakes, and by version 8 of the World Bible it had been written down as nine rules (M1 to M9). This part explains why each one exists.

## Chapter 37 — Why Predictions Are Frozen

Before every experiment, the predictions are written down and frozen. Afterwards each is scored: confirmed, wrong, or unclear. Nothing is edited after the results are in.

The reason is human, not technical. After an experiment, every result looks expected. Without a frozen record, the project would remember having predicted whatever happened. The scorecards in Part III, with their long lists of wrong predictions, are the evidence that the rule works. They would not exist if it did not.

Frozen predictions also force precision. "Rafts will matter" cannot be scored. "Every surviving world will have at least 20 open-water crossings in 200 years" can. Three surviving E2 worlds had fewer than 20. That prediction was wrong, and the record says so.

With the predictions comes a kill criterion: a result stated in advance that would show the idea failed. E2 came within five people of its own. A mechanism survives by evidence, not by enthusiasm.

## Chapter 38 — Why Autopsies Come Before Interventions

When something does not emerge, the temptation is to add it, or to add what is guessed to be missing. ACL has learned to replay the world and find the broken link first.

The cost of skipping this step is visible in the record. E6 was an intervention made before an autopsy: it assumed the world lacked possibilities, added many, and found that possibilities were not the missing link. E3 was a careful investigation that still landed on the wrong explanation, because eight worlds were too few, and E4 had to correct it.

An autopsy is cheap compared to an experiment built on the wrong diagnosis.

## Chapter 39 — Why Experiments Need Controls and Many Worlds

One seed shows one history. Histories in ACL diverge from the first week, and a single world can do almost anything. Seed 105 under E2 dwindled away because almost nobody had a mate on their own island. Seed 107 alone held 20 of E2's 53 starved infants. Neither tells us what the E2 code does in general.

So every comparison runs the same seeds under both codes, and every claim about a difference has to hold across many worlds. When eight were not enough to decide, E4 ran twenty-four, with a decision threshold fixed in advance and a bootstrap interval around the gap.

Controls also protect against a subtler error. Any change to the code changes the random history of every world, so a single seed run under two codes is not a matched pair in any simple sense. Only patterns across worlds can be trusted.

## Chapter 40 — Why Failures Are Worth More Than Assumptions

Almost everything ACL knows that it did not know at the start came from a failure.

- The raft not being used wrote Law 124.
- The population drop in E2 revealed that isolation kills small peoples.
- The freeze in E5 reframed the whole project around open-endedness.
- E6's failure moved the question from possibilities to interaction.
- The E7 audit, a failure caught before it happened, put code-against-specification checks into the method.

An assumption that is never tested teaches nothing. A failure that is honestly recorded teaches something every time it is reread.

## Chapter 41 — Why Measurement Must Not Touch the World

Observers, the historian, the surprise logs and every experiment's recorder must never change the world they watch (M4). This is checked, not assumed. Before an experiment's runs, the world is run for twenty years with the recorder and without it, and the two final states must be identical, down to a hash of every value.

This matters more than it seems. A recorder that so much as draws a random number would change the history it is recording. A historian that nudged one decision would make every "first" it wrote down a little less real.

The same principle is why the people's own code is frozen during experiments (M3). If the world changes while it is being measured, no cause can be read from the result. In E7, each run records a fingerprint of its code at the start and at the end, and a run whose fingerprint changed is thrown out.

## Chapter 42 — Why the Experimenter Is the Most Likely Cheater

Every time a problem appears in ACL, the easiest solution is to put the answer directly into the simulation. Add a reward for filling vessels. Give people a little knowledge about fire. Let the historian's names leak into the people's minds.

Each shortcut would make the worlds look better and the experiment worthless.

The project's defence is to assume that the cheating, when it happens, will come from inside: from the people who want the experiment to succeed. Hence the banned-word test on the source, the test that the historian changes nothing, the frozen predictions, the kill criteria, and the published wrong answers. Hence too the list of known compromises in Part II, including one, a floating instinct, that was written by the project itself and found later.

The challenge was never making civilization happen. It was learning whether it would happen without help.

# Part VII — The Future

## Chapter 43 — Open Questions

This chapter records questions. It does not answer them. Each is open because no experiment has yet addressed it, or because the experiments so far have not been able to decide.

About civilization:

- Can institutions emerge: rules that outlive the people who follow them?
- Can trade emerge, beyond the gift-and-return partnerships already seen?
- Can property emerge, as something more than who left food where?
- Can religion emerge?
- Can language emerge, beyond marks that come to go with things?
- Can states emerge?
- Can cities emerge?
- Can technological acceleration emerge, where each invention makes the next more likely?

About the project's own findings:

- Why does novelty stop? Is it the shallowness of the physics, the smallness of the populations, the lack of any drive to try the unrewarded, or something not yet suspected?
- Will the world performing the first step be enough? E7 is running.
- Why were E6's worlds harsher? Four of eight died out, and the cause was never found.
- Would larger, connected populations hold on to more of what they find? Small peoples lose skills; the records show spears and warm wrappings lost and never regained.
- Can rival identities form when distinct peoples finally meet?
- Is the interaction bottleneck in the world or in the people?
- And the oldest question, from before the record began: is anyone in there? Can an individual born in ACL be someone?

## Chapter 44 — How This Book Is Kept

This is a living book. It is meant to be updated after every major experiment, by whoever runs it, in the same spirit it was written.

After each experiment:

- Add a chapter to Part III with the context, hypothesis, expectations, what happened, what surprised the project and what changed afterwards. Copy the scorecard honestly.
- If the experiment produced a new insight, add it to Part IV, stated no more strongly than the evidence allows.
- If a world produced a story worth telling, add it to Part V.
- If the method changed, record why in Part VI.
- Move questions out of Part VII only when they have been answered by evidence, and record the experiment that answered them.
- Never edit an earlier chapter to make the project look wiser than it was. If a chapter turns out to be wrong, leave it, and add a correction that says when and how it was found to be wrong.

The code shows what ACL is. This book is meant to explain how ACL became what it is.

# Appendix A — Timeline

Dates are as recorded in the repository. Earlier history, World Bible versions 1 to 6, is not preserved in the record.

- **Before the record.** The founding question; the rule that nature is programmed and culture written by nobody; World Bible versions up to 7.1.
- **E0.** Mind before civilization. Ten founders, 500 days. The habit of frozen predictions begins.
- **E1.** Long histories. Eight worlds, 200 years. Culture appears; the raft is invented and not used; trust follows food.
- **2 October 2026 — E2.** The four changes. Testing, reputation, records and floating work; population falls by 40%.
- **E3.** The missing births investigated. Inconclusive.
- **E4.** Replication over 24 worlds. Population effect real; cause is isolation of founding bands.
- **E5.** The millennium. Long traditions; one people per world; the freeze.
- **3 October 2026 — World Bible 8.1.** Laws 121 to 125 written from the first runs; the creator method set down as M1 to M9.
- **E6.** Richer matter. Bottleneck remains.
- **E6.5, E6.6.** The autopsies. The interaction bottleneck named; delayed learning shown to work.
- **3 October 2026 — E7 designed and frozen.**
- **4 October 2026 — E7 audited, fixed and launched.** Running at the time of writing.

# Appendix B — Words Used in This Book

- **Seed:** the number that fixes a world's random history. The same seed and code always give the same world.
- **Tick:** one week of the people's time. 52 weeks make a year.
- **Band:** one of the founding groups of five, each starting on its own island.
- **Kind:** a made thing's lasting properties, each grouped into one of five bands, so that near-identical things count as one kind.
- **Novelty:** a kind or a behaviour new to the world, made or done by three or more people within ten years of first appearing.
- **Lasting novelty:** a novelty still being made or done fifty or more years after it first appeared.
- **LFA, latest first appearance:** the first year of the latest lasting novelty in a world. A world that keeps producing new things has a late LFA.
- **Tradition:** a technique, belief or mark held by three or more people in every ten-year sample for a long stretch.
- **FEC, first encounter count:** in E7, how often the world itself performs a transformation in front of someone, such as rain filling a vessel or a fire hardening clay.
- **Historian:** the read-only observer that names firsts after they happen. It never influences anyone.
- **Autopsy:** a read-only replay of a finished world, with probes, to find where a chain of discovery broke.
