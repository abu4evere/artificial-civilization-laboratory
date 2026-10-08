% The World That Nobody Wrote
%% How we tried to build a civilization instead of simulating one
%% Living edition 9 · written after E11, the first test of cultural memory · October 2026

# A Note Before Reading

This is the story of the Artificial Civilization Laboratory, ACL: how it was built, what it was for, what went wrong, and what its worlds did that nobody expected.

It is not the manual and it is not the rule book. The rules live in the World Bible, the design in DESIGN.md, and the code in the repository. This book keeps what none of those keep: why each decision was made, what was believed at the time, and how those beliefs changed.

A few rules govern the writing. They are the same rules that govern the experiments.

- Every number comes from an experiment record in the repository: a frozen prediction file, a results file, an investigation, an autopsy or a replay. Where a sentence is an interpretation rather than a measurement, it says so.
- Every name is a person who lived in a seeded world, and every event in their stories is in the record.
- Failures are kept. A prediction that was wrong is printed as wrong, next to the reasoning that produced it.
- Nothing is claimed before the evidence exists. Where an experiment is still running, the book says so and stops.
- The history is not tidied. Ideas that seemed obvious at the time and look naive now stay as they were.

The record begins later than the project. By the time the first experiment in the repository ran, the World Bible was already at version 7.1. The thinking of versions 1 to 6 survives only in what version 7 kept.

ACL has been built by one creator working with AI assistants. The assistants wrote much of the code and many of the reports. Some predictions in the record are signed by the creator and some by an assistant, and at least once their guesses were scored against each other. That collaboration is part of the history and is not hidden here.

From the next edition, the book will carry **Creator's Notes**: short passages in the creator's own voice about why a decision mattered, and an opening chapter on why the project exists. Those can only come from the creator, so this edition leaves room for them rather than imagining them. Everything here is written from the record.

// ============================================================================================
// CHAPTER 0 — WHY THIS PROJECT EXISTS. TO BE WRITTEN FROM THE CREATOR'S OWN ANSWERS.
// Lines starting with // are notes for whoever edits this file. The build script skips them.
// When this chapter exists, add it here as:  ## Chapter 0 — Why This Project Exists
// Questions it should answer, in the creator's words:
//   - What was JARVIS, and how did building it lead to bigger questions?
//   - When did emergence become the thing you cared about? Was there a moment?
//   - What did you try or play before ACL that felt unsatisfying, and why?
//   - Where did "culture is written by nobody" come from? Who said it first, and when?
//   - Why build a world instead of another AI product?
//   - What do you hope a reader, or Bob, takes from all this?
// ============================================================================================

# Part I — The Dream

## Chapter 1 — The Question

The project did not begin with code. It began with a doubt.

Every civilization simulator seemed to produce civilization. Yet when they were looked at closely, the answers were already inside the machine. Governments existed because someone programmed governments. Markets existed because someone programmed markets. Technology trees existed because someone had decided, in advance, what came before what.

The question that would not go away was this: if civilization were removed entirely from the design, would it ever come back on its own?

That question changed the goal. The goal was no longer to simulate a civilization. It was to find out whether one could appear without being written.

There was a second question underneath the first, and for a long time it went by a name: Bob. Bob was not a character. Bob was a question about individuals. If a person were born inside a simulated world, learned from experience, made friends, kept memories, developed fears and habits, would that person be someone? Would they still be themselves if their experience were carried somewhere else, into another body, into our world?

Bob never appears in an experiment. But Bob explains a choice that runs through the whole design. Every person in ACL is a particular individual with a particular history, never a number in a population model. If the second question is ever to mean anything, the first has to be answered with people.

// CREATOR'S NOTE (to be written): Who is Bob to you? When did the question first occur to you?

## Chapter 2 — What Is Wrong With Civilization Simulators

Most civilization simulations are not badly made. Many are beautiful. They fail at a different job: they cannot tell us anything we did not already put in.

A technology tree is a list of answers. When a simulated people discovers bronze after copper, nothing has been discovered. The designer discovered it, long before, and wrote it down. A happiness meter that rises with temples is not religion. A trade screen is not trade. A government chosen from a menu is not politics.

These systems are honest games, and they never claimed to be experiments.

The problem has a simple shape. If the outcome is written into the rules, the outcome cannot be evidence for anything.

There is a quieter version of the same problem, and it worried the project more. Even simulations that avoid technology trees often reward the right answer directly. Agents are paid for inventing, paid for trading, paid for cooperating. The behaviour appears, and it looks like emergence. But the reward was the recipe. The designer has moved the answer from the rules into the reward, where it is harder to see.

So ACL set itself a harder test:

- Nothing the people think with may contain a list of inventions.
- Nothing may reward an invention for being an invention.
- Nothing may tell anyone what is useful.

If civilization appears under those conditions, it means something. If it does not appear, that means something too.

## Chapter 3 — Four Kinds of Worlds

It helped to name what ACL was not.

A **game** is built to be played. Its rules exist to make choices interesting for a player. Whether its history is plausible does not matter, and should not.

An **agent simulation** has autonomous agents following rules, and studies what they do together: flocking birds, traffic, epidemics. Agent simulations are often excellent science. But they usually study one phenomenon, with that phenomenon's ingredients put in on purpose.

A **civilization simulation** models the large structures of history: states, economies, wars, technologies. The structures are the units of the model. People, if they exist at all, are parts of the structures.

An **artificial civilization**, the thing ACL is trying to make, is different from all three. It has no player. It studies no single phenomenon. It has no large structures in its rules at all. It has individual people, a physical world, and time. Any structure larger than a person has to be built by people, out of what they do, or it does not exist.

That last kind may not be possible. Finding out is part of the point.

## Chapter 4 — What Would Count as Success

The word that kept coming back was **open-ended**.

A world is open-ended if it keeps producing things that are genuinely new: new kinds of objects, new behaviours, new traditions, new possibilities, and not only new arrangements of a fixed list. Life on Earth is open-ended in this sense. Human culture is, so far. Almost no simulation is. Most settle, after a while, into a steady state where nothing new appears.

From the beginning the project tried to say in advance what would count as success and what would count as failure, so that it could not later redefine one as the other.

Success, at its most modest, would be culture of any kind appearing without being scripted: practices passed from person to person, symbols that come to mean something, knowledge that outlives the person who found it. At its most ambitious, success would be a world where novelty does not stop, where year five hundred contains things year fifty could not have contained.

Failure could take three forms, and each was named:

- **Nothing happens.** People survive or die and never accumulate anything.
- **Something happens, but it was scripted.** The result is real but the experiment is void, because the answer was put in.
- **Something happens, then stops.** Culture appears, settles, and freezes.

By October 2026 ACL had clearly avoided the first failure, fought hard to avoid the second, and walked straight into the third. Most of this book is about the third.

# Part II — The Philosophy

The principles below were not handed down at the start. Most were written after something went wrong. For each, this part records why it exists, what it prevents, and what was considered and rejected instead.

## Chapter 5 — Nature Is Programmed; Culture Is Written by Nobody

This is the founding rule. Every other principle is a way of keeping it.

The creator writes the physics, the bodies and the feelings: what hunger is, how winter works, how flint breaks, what grief does to a person. The creator does not write tools, fire-making, dwellings, sowing, trade, leaders, feuds or myths. Those must come from people living under nature's rules. The World Bible puts it in one sentence: the creator writes the laws of the universe, not the history.

**What it prevents.** The most common failure of the field: getting out exactly what was put in.

**What was rejected.** The obvious alternative was a small technology tree, a few steps, just to get things started. It was rejected because there is no safe size for a script. If the first step is written, every later step stands on it.

**What it costs.** The rule is brutal in practice. ACL's people start with nothing and may never get anywhere. It means long stretches of watching a world do very little. And it means the line between nature and culture has to be argued case by case. Is fear of wolves nature or culture? ACL's answer: the capacity to fear is nature. Fear of wolves in particular is learned, from being hurt, from seeing someone hurt, or from being told.

// CREATOR'S NOTE (to be written): Why does this rule matter so much to you? What would it mean to you if ACL only worked because the answers were put in?

## Chapter 6 — No Teleology

Teleology is explanation by purpose: things happen because they are heading somewhere. A simulation is teleological when its rules assume a destination, such as progress, complexity or civilization, and push toward it.

ACL's people have no purpose built in beyond staying alive and the pulls of their own feelings. Nothing in them wants to invent, advance or build. No rule rewards a world for becoming more complex.

**What it prevents.** Mistaking a designed drift for a discovery. If worlds are nudged toward complexity, complexity proves nothing.

**What was rejected.** Rewards for novelty itself, rewards for invention, and fitness scores over whole worlds. A curiosity drive does exist: a pull toward the untried that comes from temperament. It is not a reward for being inventive.

**An example.** When people in E1 made blades in the first year, nobody had wanted a blade. Someone struck flint with flint, often while playing, and was left with a sharp edge. The edge helped them forage. Whether a blade appears in a world depends on whether that accident happens and whether the help is felt.

## Chapter 7 — No Special Inventions

If the code treats some inventions as special, with their own rules or events or names, then those inventions were chosen in advance. ACL tries to make every made thing an ordinary consequence of the same physics.

**What it prevents.** A hidden tree. A rule for "spear" is a branch of a tree even if no tree is drawn.

**How it is enforced.** First, the people's code contains no names of inventions. A test reads the source and fails if words like pot, kiln or cooking appear where people think. That test has already caught the project's own authors: during the E7 audit an event was given a banned word as its name, the test failed, and the name was changed. Second, names exist only in the historian, which watches from outside and calls a thing a raft or a blade by its properties, after the fact. Another test checks that the historian never changes anything a person does.

**What was rejected.** Named recipes, recipe books, and tables of combinations with known results.

## Chapter 8 — The Indifferent World

The world has no main character and protects no one (Law 10). Rain falls where it falls. Storms put out the fires of the careful and the careless alike. A band of five on a small island with no partner for anyone dies out, and nothing steps in.

**What it prevents.** A world tuned to make the story come out well. A world that saves the last survivors, or sends rain when a people is dying of thirst, is a world with an author.

**What it costs.** Extinction. Two of E1's eight worlds died. Three of E5's did. In E4, under the E2 code, nine of twenty-four worlds were gone by year 200. These losses are not bugs. They are what an indifferent world does. The project's discipline is to report them and ask why, not to prevent them.

## Chapter 9 — Properties, Not Recipes

In ACL, materials are bundles of physical properties: how sharp, how long, how hard, how well they hold, how warm, how well they float, how tight, how soft. Two physical acts change them: striking one against another, and tying two together. What a made thing does follows only from its properties. Edge and reach help hunting. Holding helps carry food. Warmth helps in winter, when worn. This is Law 105.

**What it prevents.** The designer deciding what can be made. Nobody listed the raft. The raft exists because wood floats a little, tying two floating things together adds half the smaller one's float, and enough float lets a person stand on water. The first person to tie two sticks together made a raft whether anyone meant it or not.

**What it costs, as learned later.** Properties do not guarantee depth. With six materials and two acts, the space of things that can be made runs out fast. E1 counted 54 possible one-step actions on raw materials; 14 of them already made a named kind. This became one of the suspects in the freeze.

## Chapter 10 — Uses Must Be Discovered

An object is useful because someone experiences a consequence that matters to them, not because the creator knows its human meaning (Law 109). After E1 a stronger version was added: uses must be experienced (Law 124). It is not enough that a use exists. Someone has to live through it.

**What it prevents.** Declaring value. If the code says rafts are valuable, rafts will be carried, and nothing has been learned about whether a people would come to value them.

**The story that wrote the law.** In E1, rafts were invented in the first few years and almost never used, because nothing ever let anyone feel what floating was for. The fix was not to reward rafts. It was to make crossing water a felt event, the moment it happened, visible to the person and to anyone watching. That story is told in full in Part VI.

## Chapter 11 — Conditions, Not Outcomes

This is the working form of the founding rule, and the question asked before any new system is added (method rule M7): does this create a condition that people can use, or does it quietly script the social result?

Rather than asking how to create trade, ask what conditions make exchange useful. Rather than asking how to create government, ask what pressures make coordination valuable. Rather than asking how to make people fill vessels with water, ask what in the world could ever show them that a vessel holds water.

**What it prevents.** Intervening on the wrong side of the line. When something does not emerge, the temptation is always to add it. This principle says: add the condition, never the outcome, and if the condition is not enough, find out why before adding anything else.

## Chapter 12 — Known Compromises

A book that claims principles should also list where they are not kept. These are the places, known in October 2026, where the code falls short of its own philosophy.

- **Speech is English.** The conversations a visitor sees in the viewer are an English rendering of what really passed between people. The people have no language of their own yet. The marks they scratch are the only symbols that are truly theirs.
- **A floating instinct.** A person carrying something that floats well enough will set out across the water toward land they have seen, or sometimes at random. That knowledge, that a floating thing is a way across the sea, is supplied rather than learned. It was found in a code review in October 2026 and has not yet been removed.
- **A fixed list of pulls.** The kinds of things that can pull at a person's mind (hunger, worry, a puzzle, grief, cold and so on) are a fixed list. Goals can attach to particular things a person has found, but the kinds of goal cannot grow.
- **A memory that discards composite inventions.** Each person can remember at most twelve recipes. A new one beyond that pushes out the least valued, and a brand-new invention is valued at nothing, so a full memory often loses a thing the moment it is made. Ties are broken by the recipe's name, and the names of composite things (things tied from other things) begin with a bracket, which sorts first. So among equally valued recipes, the composite one is always dropped. Nobody designed this as nature. It is a detail of tie-breaking, found in October 2026 while building the E7.7 probe, and it falls hardest on exactly the inventions a cumulative chain is made of.
- **Watching is narrow.** People can work out a recipe by watching someone in only two situations: seeing them land on new shore with a raft, and hunting beside them. A carrier, a warm wrap, a blade used for foraging or a piece of fired clay can be inherited, carried and lived beside for a lifetime without anyone learning how it was made.
- **Fixed situations for habits.** Habits are learned for a fixed set of situations. The people cannot invent new situations to have habits about.

A history that records its principles but not its compromises is a kind of advertisement.

# Part III — The Great Mistakes

This part tells the experiments in order. Each had its predictions written down and frozen before it ran. The scorecards are reproduced as they were, including the many predictions that were wrong.

## Chapter 13 — E0: A Mind Before Civilization

The first experiment in the record was small and careful. Ten founders in two bands of five. Five hundred simulated days. Seed 42.

It asked a modest question: does the agent architecture produce behaviour that cannot be explained as simple scripted reactions?

The frozen predictions guessed that survival would dominate everything early; that people would predict the results of foraging and resting well and of social acts badly, because they had no model of each other; that fertile land would draw them; that friendships would feed themselves; that the two bands would never meet; and that invention would be rare or absent in the first fifty days.

The repository keeps E0's predictions and the script that ran it. It does not keep a scored report. That is the first gap in the record, and it is left as a gap rather than filled in from memory.

What E0 left behind was a habit. Every later experiment began the same way, with predictions frozen in a file of their own before anything ran. E0 also built a single door through which every decision passes and is recorded, so that the mind could one day be replaced without rewriting the world.

## Chapter 14 — E1: The First Long Histories

E1 was the first time the worlds were left to run long enough to have a history.

Eight worlds, seeds 101 to 108, up to two hundred years each. Twenty founders per world in four bands of five, each band on its own island. Nineteen predictions, frozen.

The worlds came alive almost at once. In seed 104, Ruleidon went back to the place where they had left something, for the third time, to see if it would happen again: the first deliberate test of anything in that world, in year 0. In year 4, Tairo struck flint where dry things lay, and they caught: the first fire made by people. In year 14, Roukarail attacked Kaileir: the world's first violence. That one would echo for nearly two centuries.

When the scores came in, ten predictions were confirmed, eight were wrong and one was unclear. The confirmed ones were the large ones. Six of eight worlds lived. All eight formed shared symbols, 763 in all, scratched marks that came to mean water, shelter or a grave, and 261 of them reached people born after they formed. Myths, false stories told by several living people, appeared about twice per world per century. Every world invented every named kind of thing by year 100. In every surviving world, someone struck fire after puzzling over sparks.

The wrong predictions were the interesting ones. Stories went wrong far more often than expected: in one world, three quarters of the stories people held about past events were wrong. And trust had nothing to do with truth. The correlation between how often a person was right and how much others trusted them was −0.066. People trusted whoever fed them.

There was a mistake in E1's own report, too. It said about five claims were tested per world-year. That counted a claim once for every person who had passed it on. Counted properly, it was about two. The correction was printed in the next experiment's results.

And then there was the raft, invented in year 0 in almost every world and almost never used. That is its own story, in Part VI.

What changed afterwards: four changes, made together. Reputation earned by tested accuracy rather than goodwill. Many more chances to check what one is told. Traces and marks as records that can teach. And floating made into something felt, with the small jump across narrow water removed.

## Chapter 15 — E2: The Four Changes, and the Price

The four changes worked, and they cost lives. It took two more experiments to understand how.

The predictions were written on 2 October 2026, from short spot checks, before any full run. A kill criterion was added before any results were read: the changes would be declared failed if testing stayed rare, if reputation did not track accuracy, if nobody crossed open water, if nobody ever learned anything from a mark, or if the population at year 100 fell below half of E1's.

Every intended effect appeared. Tested claims rose from about two per world-year to thirty-three. Reputation began to track truth: the correlation between a person's accuracy and other people's records of them reached 0.59. People crossed open water in every world. Techniques were taken up from marks in every world that lived, and in three worlds a skill that nobody alive knew was recovered from a mark someone had left.

But the mean population at year 100 fell from 46.6 to 28.1. The kill criterion's limit was 23.3. E2 came within five people of failing its own test. Five of its ten predictions were wrong.

The causes of death had not changed shares. Births had fallen by a third. Nobody could say why.

Nothing new was built. The next two experiments were spent finding out what had happened.

## Chapter 16 — E3: Chasing the Missing Births

E3 changed nothing in any world. It replayed the first century of all sixteen worlds from E1 and E2, confirmed that each replay matched the saved experiment exactly, and then followed the chain from a woman of child-bearing age to a birth, step by step.

Before the analysis, the competing explanations were written down with odds. The creator put 60% on island separation: with the jump gone, fewer people could reach a mate. The assistant put 35% on time and attention: people busier with the new things to check. Smaller odds went to health thresholds and to infants starving in their mothers' care.

Almost every explanation failed. The pooled birth rate per fertile woman barely moved, from 0.146 in E1 to 0.144 in E2. People's choices barely moved: fertile adults foraged in 44.4% of their weeks before and 44.1% after. Infants went hungry in 5.9% of their weeks before and 6.2% after.

One world showed the creator's explanation perfectly. In seed 105 under E2, almost nobody had a possible mate on their own island. The share of women with a partner fell from 44% to 21%. Births fell from 80 per century to 22. The world dwindled away. But in the pooled numbers that one world was hidden, and the extra infant deaths sat in just a few worlds: seed 107 alone had 20 of E2's 53 starved infants.

The honest conclusion was the uncomfortable one. Eight worlds were not enough to tell a real effect from bad luck.

## Chapter 17 — E4: Twenty-Four Worlds

E4 was built to settle it. Twenty-four worlds, sixteen of them new, each run under both the E1 code and the E2 code. The decision rule was frozen in advance: E2 would count as truly lowering population only if it was lower in at least 17 of the 24.

It was lower in 18. The mean gap at year 100 was 18.4 people, with a 95% interval from 9.8 to 27.2. The effect was real. Infant starvation, the explanation E3 had leaned toward, was noise: 68.8 against 67.6 per thousand infant-years.

The cause was the creator's first guess, but it worked differently from how anyone had pictured it. Every world starts with four bands of five. Under the E1 code, 70% of bands ever had a child with another band. Under E2, 39%. And a band of five that never mixes almost always dies, under either code. Within a few generations everyone on the island is related, and no one is left to pair with. Only 17% of bands that never mixed still had a living descendant at year 100. E2 had not made isolation deadlier. It had made isolation far more common: 59 bands never met another band, against 29 before.

It cost more than people. Under E2, the number of techniques tried fell 28%, and the median life of a technique fell 39%. Fewer people keep fewer things alive.

Two of E4's six predictions were confirmed, three were wrong and one could not be tested as written. The untestable one had first been measured wrongly, and the correction is printed in the results.

What changed afterwards: the four changes stayed. Their gains held in every world that lived. But the project had learned that walls of water are death sentences for small peoples, and that any change to physics can reach all the way into who is born.

## Chapter 18 — E5: The Millennium, and the Freeze

E5 was the experiment everyone had been waiting for. Eight new worlds, seeds 301 to 308, every feature frozen, one thousand years each.

The predictions were cautious. At least three worlds would die out. Surviving worlds would rarely keep two populated islands. There would be no distinct peoples. Some tradition would outlive its founders by centuries.

Six of seven came true. Three worlds died: two within fifty-five years, from starvation, thirst and neglected children, and one slowly after 419 years, mostly from illness. Five reached year 1000 alive, with 36 to 86 people each. Populations held flat for nine centuries, at 30 to 90 people, births matching deaths.

In almost every world, one people remained, and usually not a mixed one. In four worlds, everyone alive at year 100 descended from a single founding band of five. The other three bands had left no one. The usual path was not merging. It was one band outliving the rest.

Some things lasted the whole thousand years. The simplest carrier, fibre tied to fibre, was held in five worlds from year 10 to year 1000. A replay of the final century showed that about three in four people who came to hold it had been taught by someone. The rest found it again on their own, because it is the easiest thing in the world to make.

But the frozen predictions had not asked the question that mattered most, and the results answered it anyway.

Every kind of tool any world ever had, whether carrier, boat, club, blade, spear or warm wrapping, first appeared within the first eleven years. After that, for 990 years, nothing new appeared. Not one new kind of thing.

Worse, the worlds slowly forgot. The number of techniques known at once peaked between 95 and 156, around year 50 to 100, and fell to between 11 and 19 by year 1000. Much of what was lost was the clutter of play. But not all of it. Spears were lost in every long-lived world, between years 141 and 487, and never came back. Warm wrappings were lost in all of them.

A world at year one thousand looked much like the same world at year thirty, and sometimes poorer.

It was not a bug. The experiment had worked exactly as designed. That made it impossible to dismiss. These worlds had history. What they did not have was open-ended history.

// CREATOR'S NOTE (to be written): What did the E5 freeze feel like? What did you think it meant for the project at the time? Did you consider stopping, or changing direction entirely?

What changed afterwards was the question itself. The project had been asking whether culture could emerge. It clearly could. Now it asked: why does novelty stop?

## Chapter 19 — E6: Richer Matter

The first answer was the obvious one. Perhaps the world was too poor. Perhaps there was simply not enough to discover.

E6 gave matter more to it. Continuous properties: mass, heat, wetness, tightness, softness. Clay, soft and wet, by rivers and lakes. Three new acts: holding something in a fire, filling something, and pressing soft stuff into a shape. Two arms, the old code and the new, eight seeds, a thousand years each.

The hope was written into the frozen predictions: in at least half the long-lived worlds, the latest lasting novelty would appear in year 300 or later.

It did not happen. In every E6 world that lived three centuries, the latest lasting novelty appeared by year 66. Across all eight worlds, 578 lasting novelties appeared in the first century and not one after it. The verdict, applied by the frozen rule, was two words: **bottleneck remains**. Four of six predictions were wrong.

The people did take up the new physics, but only the shallow end of it. They shaped clay constantly: 36 to 61 shaped kinds per world, points and hollows bound into larger things. And then they stopped. In all eight worlds, over up to a thousand years each, exactly one thing was ever changed by being held in a fire. Nobody ever filled a vessel. No water and no fire was ever carried anywhere.

E6 worlds were also harsher, and nobody ever found out why. Four of eight died out, against three under the old code. Seed 306 lived a thousand years under the old code and 124 under the new.

There was one small thing that E6 had and the old code did not. In two of the four surviving E6 worlds, new traditions began after year 100 and lasted a century or more. In seed 304, a belief about leaving fibre at places in summer and autumn began around year 340 and lasted to the end of the millennium. No world under the old code had any tradition that began after year 100. They used old mechanics, not the new physics, and two worlds against none is suggestive at most. It is recorded because it may matter later.

What changed afterwards: the project stopped asking what possibilities were missing and started asking why possibilities stayed undiscovered. It stopped running new worlds and started dissecting old ones.

## Chapter 20 — E6.5 and E6.6: The Autopsies

Two investigations followed, and neither changed a single world. E6.5 replayed two E6 worlds from their first week with probes that recorded every decision and every option a person had weighed. E6.6 measured how far back in time people can learn from a consequence.

E6.5 found where the chain of discovery broke, and gave the place a name: interaction, the first try. E6.6 tested the most likely alternative explanation, that people simply could not learn from delayed rewards, and found it was wrong.

Their stories are in Parts IV, V and VI. E7 was designed directly from them.

## Chapter 21 — E7: The Experiment That Almost Died Before It Began

E7 asks the question the autopsies left behind. If nature performs the first step itself, will people pick up the rest?

Rain fills any open watertight thing. Wading into a river or lake fills it. A fire hot enough hardens dry clay carried beside it. The people's minds were not touched at all: their decision, body, thought and action code stayed byte for byte the same as E6. Seven predictions, a decision rule and two named failure modes were frozen on 3 October 2026, before any E7 code was written.

On 4 October, before any world ran, the code was audited line by line against its own pre-registration. Six problems were found.

One would have ended the experiment on its own. When clay hardened by a fire, its recipe was stored under the wrong field name, and the next time that person made a decision, the world crashed. Every test passed, because none of them let a world keep running after a firing. The first piece of passively fired clay in any world would have stopped the run and set off E7's own kill criterion.

The other five were quieter. Each would have meant testing something other than what was registered. Rivers never filled anything, because in this world rivers can be waded and do not count as water. Everyone standing by a fire had all their food treated as cooked, which the design never said. The fire's real heat was ignored. Plain lumps of clay never fired, only shaped ones. And a lightly covered heap kept the rain out when the design said it needed to be more than half covered.

All six were fixed, recorded in a separate note, and frozen under a tag before the first world ran. The pre-registration itself was not touched. Two parts of the design turned out to have nothing to act on: in this world nothing can be set down on a tile, so nothing on a tile can catch rain, and each person's food is one pooled amount with no age, so "food eaten past its natural rot" cannot be measured.

All sixteen worlds then ran a thousand years each, and every validity check held: no crash, no change of code during the runs, a recorder that changed nothing, and a baseline that reproduced E6 exactly.

Half of the idea worked. Fires hardened clay in front of people 647 times, against none under the old code. People kept what the fire made. Twenty-five fired objects outlived the people who first carried them, and six were still being carried more than fifty years later.

The other half never had a chance. In eight worlds over up to a thousand years, rain or a river filled a vessel three times, and nobody ever drank carried water. The world cannot fill vessels nobody makes.

And novelty did not continue. Across the eight worlds, 628 lasting new things appeared in the first century and one after it. The frozen rule gave the same two words as E6: **bottleneck remains**. Three of seven predictions were confirmed.

Two things were not predicted and are recorded as leads, not findings. E7 worlds lived longer: seed 306 reached year 465 instead of 124. And eleven new traditions began after year 100.

The single late novelty, in seed 301 in year 115, looked for a while like a world that had almost found something. The next chapter tells what it really was.

An experiment can be lost before it starts, quietly, inside a single field name. And a hopeful result can turn out to be something else entirely, which is why the next step was another autopsy.

## Chapter 22 — E7.5: The Year-115 Flake

Seed 301 was the only world in any experiment whose latest lasting novelty came after its first century. Before building anything on that, it was taken apart.

The world was replayed under the E7 code to year 135, and the replay matched the saved run at every ten-year mark. The probe found that the novelty was not new. It was a flint flake: flint struck with flint or with stone. The flake had been known since year 2, made in play in year 4, taught at least twenty-four times and read from marks on rock many more. What happened in year 115 was narrower. For the first time, three people deliberately made a flake of middling sharpness within ten years.

Two facts explained it. Deliberate making had become rare: the whole world made anything from a recipe zero to three times a year. And a flake's sharpness depends on the skill of the person striking it. The three makers were unskilled, at 0.14 to 0.29, where the founder who first made the flake had reached 0.82. Their flakes came out duller, and the novelty measure, which sorts things by how sharp they are, counted a duller flake as a new kind of thing.

Fired clay played no part in it.

So E7's one late novelty was most likely a sign of skill being lost, not of discovery. E7's real effect on late novelty was none. And the novelty measure had a weakness nobody had seen: it could count a decline as something new. Every late novelty in future experiments is to be checked for this before it is reported.

## Chapter 23 — E7.6 and E7.7: Counting What Is Kept

The autopsy left a suspicion: perhaps the worlds were not frozen at all, but slowly forgetting. Two read-only audits were designed to find out, each with predictions frozen and tagged before it ran. Neither changes a line of how the worlds behave.

E7.6 replays all sixteen E7 worlds and records, every twenty-five years, the skill of the best crafter, the top ten and everyone alive; how many recipes the living still hold; how often people make things deliberately and in play; and whether watertight vessels exist at all. It then sets all of it against population, to see whether larger worlds keep more.

E7.7 asks a sharper question, put by the creator: when someone carries, inherits or lives beside a useful thing, how often do they go on to learn to make it, and how often do they actually make one?

Building the probes turned up three facts in the code that change how the question is asked. They are facts about the rules, not results:

- Crafting skill grows only by practice. Founders start at 0.2 to 0.4, everyone born later at nothing. Skill is never taught, never inherited, and it dies with the person.
- Watching teaches only in two situations, a raft landing and a shared hunt. Everything else must be taught, read from a mark, or found again in play.
- Each person remembers at most twelve recipes, and when memory is full, composite inventions are the ones it drops first.

Both audits finished on 5 October 2026. Every validity check held: sixteen of sixteen replays in E7.6 and eight of eight in E7.7 reproduced their saved runs exactly, proving the probes had only watched.

What they found overturned the project's model of what was happening.

The worlds were not frozen on a plateau. They were slowly unlearning.

**The collapse of skill.** Founders began with crafting skills between 0.2 and 0.4. By year 25, the best living crafter in surviving worlds reached 0.73 to 0.98, and the average across everyone alive was 0.33 to 0.50. After that, expertise fell in every single world, under both the E6 and the E7 code. By year 100, the best crafter was down to 0.34 to 0.61 (average 0.14 to 0.21). By year 300, the best was 0.14 to 0.33 (average 0.04 to 0.09). By year 1000, the best crafter alive had a skill of only 0.05 to 0.11, and the average across the population was 0.01 to 0.03. A tenfold collapse. The people who made the late flakes and points were novices compared with the founders who had first made them.

**The thinning of recipes.** In the early decades, when founders and their children were exploring and teaching, the number of unique recipes held by living people peaked between 85 and 173 per world. By year 500, that pool had shrunk to between 15 and 32: a four- to eight-fold loss. Most of what had once been known was forgotten.

**People stop making things.** The most striking number in E7.6 was not skill, but the act itself. In the first twenty years, people made things deliberately from a recipe about two to three times per person per decade. By year 500, that rate had collapsed to 0.02 to 0.07. By year 1000, it was 0.03 to 0.05: a forty- to sixty-fold drop. Making things in play fell fifty-fold, from about eleven per person per decade in childhood to 0.15 to 0.26. By the later centuries, people almost never made anything at all.

**Watertight vessels never existed.** Across all sixteen millennium runs, a watertight vessel was made exactly twice—both by Reibik in seed 304 under the baseline code. In E7, across eight thousand world-years, not one watertight vessel was ever made. In not a single ten-year sample was anyone in any world carrying one. E7's passive rain and wading catchment had nothing to work with.

**Population is still open.** Among worlds that survived past year 300, average population showed no correlation with the skill of the best crafter at year 500 (Spearman rho = -0.05). But those worlds only varied in mean size between 36 and 54 people. That is the size of one small band versus one slightly larger band. The demographic hypothesis was never tested under real variance.

E7.7 traced why knowledge failed to become action:

**Teaching works, but watching almost fails.** Over the first three centuries of eight E7 worlds, 1,782 recipes spread by being taught, and 233 by reading marks carved on stone. In contrast, watching someone make or use an object happened 1,770 times and produced exactly seven copies—and all seven were boats, because watching had only been coded for boat landings and shared hunts. For blades, spears, clubs, carriers, and wraps, watching produced zero copies.

**Fired clay: knowing without doing.** Fired clay proved that having an affordance and knowing the recipe does not produce a tradition. 1,120 people carried or lived beside fired clay. 244 learned how to make it (96 taught, 176 fire-hardened). Yet of the 272 people who knew the recipe, 213 (78%) never once made it deliberately. Knowing how was not enough when the object solved no urgent problem.

**The composite memory penalty.** When people made things in play, simple things were kept in memory 96% of the time (3,984 kept, 162 forgotten). Composite things, which require intermediate parts, were forgotten upon making 21% of the time (7,982 kept, 2,160 forgotten): a five-fold penalty. Because memory holds only twelve recipes and drops the least valued, intermediate components with zero immediate utility are purged before they can ever be combined.

Scorecards: E7.6 confirmed three of six predictions (1, 3, 4 confirmed; 2, 5, 6 wrong as scored). E7.7 confirmed one of six (4 confirmed; 1, 3, 5, 6 wrong; 2 unscorable as nobody inherited first). The audits proved that the problem was not a plateau. It was a degenerative collapse.

## Chapter 24 — E8: The Crucible, Reviewed

The first plan for E8 came from a different AI assistant working on the same repository, and it was ambitious: seven arms, run together, to test every remaining suspect at once. Freeing people to make things they already held. Letting skill grow faster when practising beside someone better. Protecting composite recipes from the memory ceiling. Starting worlds with eighty people instead of twenty. And every combination of them.

Its central idea was sound, and it was put well. Skill must never be copied into a learner's head, because that would be a cheat: a person in ACL can only become skilled by doing. A good teacher can make each act of practice count for more, but the learner still has to strike the stone.

Before any code was written, the plan was checked against the code and the records, the same way every plan is. The check found five problems.

- One success criterion could never be met. It asked for a lasting novelty first appearing after year 80, in runs only 120 years long, when a novelty counts as lasting only if it is still alive fifty years later.
- One arm changed two things at once, so its result could never be explained.
- One arm promised identical maps while also making the map four times larger.
- Two descriptions of the code were inaccurate, and the time the runs would take was underestimated several times over.

None of this was hidden or rewritten. The frozen plan stayed exactly as it was, and a dated amendment was written beside it, before any code existed, saying what was wrong and what replaced it.

The amendment also changed the order of work. Instead of running all seven arms, it ran one first: the arm whose answer every other arm depended on. If people could be freed to practise, the rest might matter. If they could not, the rest would be built on sand.

## Chapter 25 — E8 Arm 1: Freeing the Hands

The hypothesis was simple. People stop making things because the rules stop them: a person holding a tool will not make another while it is in good shape. Remove that, and they would practise, keep their skill, and perhaps hold on to more of what their parents knew.

The creator chose the exact rule from three candidates before any code was written. A held thing that has proved its worth may be made again, at half the pull it would otherwise have. Everything the old rule allowed stayed exactly as it was; the new rule only added practice. Six predictions were frozen with it, and the first was a manipulation check: if making did not at least triple, nothing else would be read into the result.

Freeing more making did not, in itself, count as success. In this world skill rises only by making, so more making must mean more skill. What would count was what practice did to everything else: whether skill survived the founders, whether more recipes were kept, whether traditions held, and whether anyone starved for it.

The run was clean. And making did not triple. In the two worlds that lived to year 120, people made things less often per person, not more. Decade by decade, the new rule added a little making early, while the founders still valued their tools, and then making collapsed at the same pace as without it. Two of the four worlds died out; with only four worlds, and every change to the code giving every world a different history, that could not be laid at the rule's door.

All six predictions were wrong, and the last five were not interpreted, as the frozen rules required. The honest statement is narrow: there was no evidence that freeing the hands helped. It does not prove that it could never help.

The holding rule had looked like the obvious culprit. It was not what was stopping people.

## Chapter 26 — E8.1 and E8.2: Why Nobody Makes Anything

The new rule only let people practise things they valued. So the next question was whether they valued anything at all. Two read-only autopsies followed, each with its predictions frozen first.

**E8.1 asked how people valued what they held, generation by generation, and what they chose instead of making.** Every fourth week of 120 years, in four worlds, every adult was examined.

The founders were the surprise. In the weeks they could have made something, having both the knowledge and the materials, they weighed making only one week in nine, and chose it one week in a hundred. Whatever they chose instead scored seven to nine times higher than making could have. Making was never competitive, even for the generation that made most.

Then it fell further. By the third generation, adults held about one made thing for every five people, half of what they held was worth nothing to them, and making was weighed in fewer than one week in a hundred and fifty. What won instead was everyday life: foraging, talking, being with others, giving food.

One number did not fall. The best worth among the recipes people knew stayed about the same in every generation. They knew how. They had the materials in nearly nine weeks of ten. They simply never had a reason.

**E8.2 asked whether that reason existed in the world.** Not what people thought their tools were worth, but what the tools actually did.

In this world, a week of foraging brings an adult about nineteen units of food, against a need of seven. The best tool adds a fifth to a harvest that was never short. Across four worlds and more than five million units of food foraged, tools accounted for at most two per cent of it. Most made things never repaid, through foraging, the food it had cost to make them. Hunting, where a tool helps most, took less than one adult-week in a thousand.

The measurement has limits, and they are recorded with it: it counts only food from foraging, and rafts, wraps and clubs do other things too. But the main finding does not depend on those limits. The people who ignored making were not being foolish. Their world gave them almost no reason to make anything.

## Chapter 27 — E8.3: Winter

One fact refused to fit. If food was so plentiful, why was starvation the largest single cause of death in ACL's long-lived worlds? The creator saw that the two facts pulled against each other, and that resolving the contradiction was worth more than any new experiment.

The answer was the oldest one in the world. Every one of the 195 people who starved in four worlds over 120 years was followed back through their last two months.

Seventy-one per cent died in winter, and eighty-eight per cent in winter or the first weeks of spring, when the plants had not yet come back. In winter, one person-week in nine was spent starving; in summer, one in a hundred. Food is plentiful three seasons out of four, and the average hides the fourth.

Infants starved at seven times their share of the population. Of the eighty-one children and infants who starved, eighty still had a living carer. The carers were hungry too.

Eight weeks before they died, in late autumn, the typical person who starved had no food on hand at all. Most had no stored food anywhere within reach. Not one of the 195 was carrying anything that holds food.

The arithmetic of this world says that need not be. Loose food loses a twenty-fifth of itself each week, so food laid by in autumn keeps more than half of itself through a thirteen-week winter. Seeds, which are food too, barely rot at all. Food kept by a fire or under a covered heap rots more slowly still. Getting through a winter takes about a hundred and fifty units laid by in autumn. A person can carry a hundred with bare hands, and twice that with a carrier.

So storage was possible, and it was exactly what carriers and heaps were for. But nobody ever filled even their bare hands. The one thing a carrier is really for, holding a winter's food, was never lived through, and so, as with the raft long before, it was never valued.

It was the raft again. The tool existed. Its use existed. Nobody ever felt it.

## Chapter 28 — E8.4: Autumn

Winter left one question, and the creator put it in a single sentence: did the people fail to survive winter because they could not prepare, or because they did not?

The two answers lead to different projects. If autumn gave too little to spare, winter was a fact of the world's ecology, and the next experiment would change the world. If autumn gave plenty and nobody kept any, the problem was in the people, in something they lacked that every farming people has.

Every adult, in every autumn, in four worlds over 120 years, was measured: 11,832 autumns in all. Five predictions were frozen first. All five were confirmed.

Autumn gave plenty. A week of autumn foraging brought nearly twenty food. An adult who foraged every autumn week could have laid by about 160 beyond what autumn itself required, more than the 150 a winter takes once rot is counted. Ninety-eight autumns in a hundred offered at least a hundred to spare.

Almost none of it was kept. Adults foraged in fewer than half their autumn weeks, because the pull to forage grows with hunger, and in autumn they were not hungry. The other weeks went to talk, to giving food to others, to being with people. No one, in nearly twelve thousand autumns, ever held eighty food at once; the typical most was twenty-seven. When winter came, the typical adult had nothing in hand, a few seeds, and thirteen food in all. Not one entered winter with what a winter takes.

So the world allowed it, and the people did not do it. The bottleneck for ACL's largest killer was not ecology. It was that nothing in the people looked ahead to a hunger that had not happened yet.

The creator saw at once why that mattered more than any earlier finding. Civilization is largely the doing of expensive things now, because of problems that have not happened yet. Granaries, fields, roads, bridges and reservoirs are all of that kind. The people of ACL feel today's hunger, and not next season's.

## Chapter 29 — E9: Feeling Winter in Autumn

For the first time, the evidence pointed at one specific thing the people lacked. Not knowledge, not tools, not more people, but a capacity: to feel, before it comes, a hardship they have lived through before.

The creator was careful about how such a thing could be built. It must not say "store food". It must not mention carriers or heaps. It must not fire because it is autumn. It must not tell anyone that winter comes. It could only take what a person had lived through and let it reach a little ahead.

The mind already did something like it for thirst. People who have been thirsty carry an expectation of thirst, learned from their own experience, and it makes dry places weigh on them. And people already thought one season ahead about materials. So the design gave hunger the same treatment: each person learns, season by season, how often they have actually gone short of food, and the season they have gone short in is felt one season early, in the pull to get food and nowhere else. Not in stealing, not in giving, not in play.

A pilot, before any code, caught a trap. Learned from how little food a person holds, the expectation was not seasonal at all, because everyone holds only a few weeks of food all year; it would simply have made everyone hungrier. Learned instead from the weeks a person actually went short, it was seasonal, and faint. Rather than turn the dial until something happened, two strengths were fixed in advance, each with a reason: the thirst mechanism's own, and the strongest a season-ahead feeling can be without exceeding the real thing.

There was one more safeguard, and the creator insisted it be absolute. If anyone who had never gone short in a winter changed what they did in autumn, the experiment would be declared failed, whatever else it showed.

The safeguard held. The mechanism touched no one who had nothing to anticipate.

And the experiment failed its central test. Adults who had gone short the winter before foraged in autumn barely more than before. The typical person still walked into winter with about twelve food. Winter deaths did not fall.

But something happened that had never happened in ACL. In the strongest arm, in about one autumn in a hundred, a person filled their hands: eighty food or more, against none ever in the control worlds. Every one of them had gone short the winter before. They foraged in three autumn weeks of four, and walked into winter with a median of seventy-four food, six times what everyone else carried.

For the people it moved, the capacity did exactly what the hypothesis said. It moved too few of them.

## Chapter 30 — E9.1: A Faint Lesson

The obvious explanation was that the lesson reached too few people. It was wrong.

Nearly every adult, ninety-nine in a hundred, had learned to expect going short in winter, and the mechanism touched nearly every autumn. The problem was not reach. It was strength. The expectation was learned as an average: the share of a winter's weeks spent short. For most people that share was small, so what it added to the pull to forage was a tenth of a unit of hunger, too little to outweigh a week's ordinary business. Only those whose lesson was strong, people who had spent half their winter weeks short, were moved to lay food by.

A second fact surfaced, and it complicated the story. For any one adult, any one winter rarely kills: six in a thousand. Winter is when starvation comes, but much of its toll falls on infants and children, through the people who feed them. A store may matter more for a carer's children than for the carer.

People do not seem to remember a hard season as an average. They remember its worst. A lesson learned from the worst week rather than the share of bad weeks would be stronger without being any less grounded in experience. Whether to build that is a decision for the creator, and it would be a new experiment, not a change to this one.

## Chapter 31 — E9.2: Whose Life a Store Saves

If winter so rarely kills any one adult, whom does it kill? The answer had been in the record since E8.3: infants, at seven times their share. And infants eat what their carers have.

So every child, in every winter, in eight worlds, was followed from the first week of winter to the first week of spring, beside the food their carer held when the winter began. Thirteen thousand child-winters.

When a carer began winter with less than twenty food, about one child in ninety starved before spring. When the carer held between twenty and fifty, one in five hundred. A few weeks' more food in a carer's hands made a child's winter five times safer. Among the rare carers who held fifty or more, no child starved at all, though there were too few of them for that alone to mean much.

Without anticipation, those well-stocked carers were almost non-existent: two child-winters in a thousand. With it, nine times as many, still under two in a hundred.

This was the missing piece of the winter story. The reward for laying food by is real and large. It simply does not fall on the person who does the work. An adult who forages through autumn mostly saves a child, not themselves, and a lesson learned only from one's own hunger will rarely teach it. In a world where nothing reaches from a child's death back to what their carer did in autumn, the most valuable habit a people could have is the one their experience is least able to teach them.

## Chapter 32 — E10: A Child Lost to Winter

If one's own hunger teaches too faintly, perhaps grief would not. The creator chose to test the strongest lesson a carer could learn from: a child of theirs dying of hunger in a season. And beside it, a weaker one that could reach far more people: seeing someone die of hunger.

The design followed what the mind already did. A death in winter left the carer a full-strength lesson for winter, fading at the same rate grief fades in the code. Those within sight of a starvation death, a median of ten adults, were left a lesser lesson. How much lesser had no precedent anywhere in the code, so the creator refused to guess one number and set two: a quarter of a parent's lesson, and a half, so that the experiment would show what the value does rather than rest on it. As before, the lesson was felt a season early and only in the pull to get food, and anyone who had neither lost a child nor seen a death had to behave exactly as in the control. They did.

The bereaved did forage more the next autumn, in about six weeks of ten rather than five. Witnesses barely changed. And in no arm did anyone walk into winter with more food than before: about twelve, as always. The share of carers holding enough to protect their children moved by barely a point.

Then the deaths, read last, as the creator had insisted. In one arm, a third fewer children starved in winter than in the control. In another, a fifth more. Nothing upstream had changed to explain either: the carers held the same food. These were four diverging worlds doing what diverging worlds do; in two of them, one world nearly died out. Read first, the arm with fewer child deaths would have looked like the breakthrough the project had been waiting for. Read in order, it was noise.

With E9, E10 closed a road. A lesson from one's own hunger, from losing a child and from witnessing a death, felt ahead at full strength, left the world's preparation for winter where it was.

## Chapter 33 — E9.3: The First Planners

Before moving on, the creator asked for one more look backward: at the hundred and twelve autumns in E9 when someone, for the first time in the history of ACL, filled their hands before winter. "They're the first naturally occurring winter planners in the entire history of ACL," the creator said. "That's a treasure trove."

There was nothing special about them. Their care for others, their diligence, their anxiety, their curiosity, their kindness: all the same as everyone else's. They were a little younger, a generation further down, and a little more often caring for children. What set them apart was only the lesson. They had gone short in a winter hard enough that the memory of it was more than twice as strong as most people's.

They laid by nearly seventy food. Through the winter they gave almost a third of it away, ate the rest, left almost none in heaps, and came out of winter with about five. Not one child in their care starved.

And then they stopped. Of the hundred and thirteen autumns in which someone planned for winter, only one was followed by a second.

## Chapter 34 — E11: Stories of a Hard Season

If a lesson dies when its suffering stops, it needs something that outlasts suffering. The creator asked whether the channel that had carried "Kaileir killed Ludol" for a hundred and eighty years could carry a lesson about winter too.

The channel was already there, and it was enormous. A pilot found that almost every death from hunger became a story: tens of thousands of tellings in four worlds, each death heard by a median of twenty-six people and still told decades later. But a death was remembered by who died and where, never by what of, or when. All that telling taught nothing about winter.

So the change was the smallest the creator could ask for. A story of a death would carry two things it had always dropped: that it was hunger, and in which season. Nothing about storing, nothing about tools, nothing about what to do. "Stories carry experiences, never instructions," the creator insisted; the existing machinery would decide what anyone did with them. How strongly a story should teach had no precedent, so, as in E10, it was tested at two strengths. And the new code, with stories switched off, reproduced the previous experiment exactly, so that what stories added could be measured against what was there before.

Forty thousand times, someone heard and believed a story of a hunger death, with its season. And each time, they were moved a very little. People who had heard such a story foraged in autumn about four per cent more than before. The number of people who filled their hands before winter rose from none to fifty-three over four worlds and a hundred and twenty years; the share of carers with enough food for their children rose by four points. Each of these rose in step with how strongly stories were allowed to teach, so the effect was real. It was faint. Two of the fifty-three planners planned again the next year.

The arithmetic explains why. A story teaches as strongly as it is believed and as clearly as it is remembered, and both are usually well short of whole. E9.4 had found that almost nobody prepares until their lesson reaches about four tenths. A told lesson almost never gets there, however often it is told.

## Chapter 35 — E12: Seen, Respected, and Not Copied

The creator would not let the next step be another mechanism. The planners had shown that preparation was possible in ACL; the question was what had happened around them. "The planners are the closest thing ACL has produced to proto-civilization so far," the creator said. "That's where I'd dig next."

There were three possible answers. Nobody noticed them. People noticed and did not copy them. Or people already copy the successful, and something else had stopped it. The code answered the third before any world ran: ACL's people can copy a way of making something by watching, and only when they see someone land on new shore or share a hunt; and children slowly take on the habits of whoever raises them. A planner's preparation lived in neither. It came from what they expected of winter, and nothing carried that from one person to another.

So the autopsy asked about everything else. The planners were not hidden. More adults were within sight of them through autumn than of most people, and each had more than eighteen neighbours. Through the winter they fed others, three times as much food to three times as many people. Respect and trust toward them rose faster than toward anyone else who had gone short.

And nothing around them changed. Their neighbours foraged the next autumn exactly as everyone else's neighbours did, and planned exactly as rarely. The children they fed and raised grew up to plan no more often than anyone's children.

It was the second answer. People saw them, were fed by them, thought better of them, and did not do what they did. The bridge between one family that fills its store and a people that fills its stores was missing, and for the first time it was clear exactly where.

## Chapter 36 — E13: Following Those Who Do Well

E12 had found the gap exactly: the planners were seen, and nothing let anyone follow them. E13 built the smallest bridge the creator would allow. "Copy observable behaviour, not expectations." An adult who saw someone better fed than themselves forage that week would learn from it as if they had foraged themselves, from the food they saw the other person get, valued by their own hunger. Nothing about winter passed between them, and nothing about why. A pilot had shown that the planners were usually the best-fed person in sight and almost never the most respected, so models were chosen by visible success, not by standing. A third arm allowed only models whose children were all alive.

The headline was frozen as the question E9.4 had left: would a planner, now surrounded by people learning from them and from others like them, plan again the next autumn? At least one planner-autumn in ten had to be followed by another.

The worlds did something no earlier mechanism had done. Planner-autumns rose more than fourfold, from 112 to 462. Twenty-nine of them were followed by planning the next year, against one in the control: 6.3% against 0.9%, short of the one in ten that was needed. Adults' habits for foraging in autumn while already stocked were higher in all four worlds. Carers entering winter with enough for their children rose by eight points. Neighbours of planners foraged only 7% more, short of the 10% predicted, and children did not die any less often in winter. The stricter arm did far less, and one of its worlds died out.

None of it can be claimed. E13 had a safeguard against scripting: people who never once saw a better-fed neighbour forage had to behave as they did in the control, so that any change could be traced to watching and not to some leak in the code. Over a hundred and twenty years, almost everyone sees that at least once. The group was empty in two arms, and three people strong in the third. A test with nobody in it cannot find a leak and cannot rule one out, and the frozen analysis counted it as a failure. The assistant had designed that test and noted the group would be small; it did not foresee that it would be empty. By the rule written before the run, E13 is declared failed.

The verdict stands as written. What it left was the clearest signal the project had produced, and no right to it: a replication, frozen before any run, with a safeguard that can actually be measured.

## Chapter 37 — E13R: What Spreads Is a Habit, Not a Plan

E13 had left the project holding its strongest lead and no right to it. E13R was built to settle it, on sixteen new worlds, with two changes the creator signed off before any code: a safeguard that could not come out empty, and a second question. If copying worked, what was being copied?

The safeguard was made physical. A sham arm ran the copying step to the very point of learning and then wrote nothing; its worlds had to end identical, byte for byte, to the control's. An instrumented run checked every single copying step and allowed only one change: the watcher's own habit for foraging. And the run was ordered so that a failure would stop everything before any outcome existed to look at. "Failure of either L1 or L2 terminates E13R before any outcome analysis is read," the creator wrote into the design. Neither failed. In all sixteen worlds the sham equalled the control exactly, and 6,894 checked updates touched nothing but the watcher's habit. The question E13 could not answer had an answer: the copying works only through the person who watches.

Then the outcomes, in the order frozen before them. The headline failed. Planners in the copying worlds planned again the next autumn 5.6 per cent of the time, against 4.3 in the control; the frozen bar was three times the control. On these new worlds the control repeated far more often than on E13's four, and much of E13's sevenfold contrast turned out to have come from an unusually low control.

But the links that E13 had found held again. Habits for foraging while stocked were higher in fourteen worlds of sixteen; there were nearly three times as many planner-autumns; eight points more carers went into winter with enough for their children. And two things did not move, again: the neighbours of planners foraged no more than anyone else's, and children did not starve less. Pooled, they starved more often in the copying worlds, although the worlds split nine to seven, and the difference came from a few large ones.

The second question had the clearest answer of all. One arm let people learn only from neighbours holding less than a planner's store; the other, only from those holding more. The first reproduced everything the full copying did, to within a few per cent. The second reproduced nothing, though it had a hundred and thirty-six times fewer chances to teach, so it could not show that planners teach less, only that the effect did not need them. Ninety-eight per cent of all copying in the full arm had come from ordinary, moderately fed neighbours. Both the creator and the assistant had bet on this before the run.

So what passed from adult to adult was real, and it was not what the project had hoped. It was a habit: forage while you still have some food, learned from whoever around you is doing a little better. That habit left more people well stocked at the end of autumn. It did not teach anyone to prepare for winter, it did not spread from the planners to the people beside them, and it did not save children. For the first time in ACL, behaviour moved between adults; what moved was a way of foraging, not a plan.

## Chapter 38 — The Autopsy of E13R: More Food, No More Winter

E13R had left a puzzle the creator would not build past. Eight points more carers went into winter with enough for their children, and their children did not starve less. E9.2 had shown that a stocked carer protects a child five-fold. Either that protection had stopped working in the copying worlds, or something else was happening. "Autopsy first," the creator said, before any next mechanism.

The replays answered the first half cleanly. Protection had not stopped working. In both kinds of world, a child whose carer held twenty to fifty at the start of winter was five to ten times safer than one whose carer held under five. But at every level of a carer's food, children in the copying worlds starved more often, between one and a half and two times as often. More children had stocked carers, which should have saved lives; the higher risk at every level outweighed it.

The children who starved were mostly infants, under a year old, and they died late, in the eleventh week of a thirteen-week winter. Most had a carer who was still alive and had nothing left. In the copying worlds, more of those carers had already died, and they had more children depending on them. And the stocked carers there gave more away: more than half of them fed someone outside their own family during the winter, against two in five in the control.

The second half of the autopsy asked whether the copied habit was preparation at all. It was not. People in the copying worlds foraged a little more in every season alike, spring as much as autumn. They did go into winter with more: the share of adults holding twenty or more rose in all sixteen worlds of sixteen. By the end of winter the advantage was gone.

The reading the record allows is narrow. The worlds split on deaths, nine to seven for children and eight to five for adults, so the autopsy does not claim that copying did harm. It claims that copying did not help winter. What the copied habit gave was more food going in; what nothing gave was a way to make it last until spring. For thirteen experiments the project had asked how to get people to gather for winter. The autopsy suggested that gathering had never been the whole problem.

## Chapter 39 — W1: The Winter Ledger

After the autopsy, the creator changed course. The road written before E13R's result said to test whether the copied habit would last. The autopsy had shown that the habit was not preparation and did not help winter, and the creator would not spend the next experiment making it last. "Change the branch," the creator said, "investigate why food doesn't last." The change was written into the roadmap as what it was: a decision made after a result, with its reason beside it.

Some of the answer was in the rules before any world ran. An adult eats seven a week, and winter is thirteen weeks long. A person can carry a hundred. Carried as seed, which barely rots, a full load would just see one adult through. A carer with two children needs nearly two hundred, twice what anyone can carry. A family's winter could only ever be kept on the ground, in a stash.

To see the rest, the code was copied and taught to count, without changing anything: every unit of food that rotted, was eaten, was fed to a child, was given, stolen, stashed or taken back. Its worlds were checked to be byte for byte the worlds of E13R.

The ledger overturned the question. Food did not fail to last; almost none was held to last. Food held at the start of winter covered a seventh of what was eaten through it. The rest was gathered week by week, in the snow, and it very nearly sufficed: over all the winters, people ate ninety-six per cent of what they needed. The median family went into winter with a ninth of what it would need. Rot took little. Most of what people held was already seed, which keeps. And the stash, the one thing that could have held a family's winter, was almost never used: in sixteen worlds over a hundred and twenty years, barely six thousand units of food were put away in autumn.

In every season people gathered about what they ate, a little more in spring and less in winter. The surplus that E8.4 had found waiting on the land in autumn stayed on the land. About half of all adults went short at some point every winter, and those who began it with a store went short too, only later.

So the problem the project had been circling since E8 was not keeping food. It was that nobody gathered more than the present asked for, and nobody put anything away. The next question was already plain: the means to hold a winter existed in the world, and why did no one use it?

## Chapter 40 — S1: Three Gates

W1 changed how the creator saw the whole sequence of experiments. "W1 feels bigger than E13R," the creator wrote. "E13R proved that behaviour can spread between adults. W1 suggests the transmitted behaviour was never the missing ingredient." The creator suspected the reward structure itself: that it only valued solving present hunger, never building a reserve. And the creator set a limit: "I don't want new mechanics yet. I want the decision process mapped first." Five questions followed. How often is stashing considered? What beats it? What value does it get, against foraging? Do the people who stash learn that it worked? And if they learn it, why does it not spread?

The rules answered part of it before any data. Putting food away was offered only to someone holding more than two weeks' food for themselves and those they fed. The single chance each week to set something down was shared between food and every other thing a person carried. Setting food down brought no reward that week, so habit could not learn to value it. And the belief that stashing works was tested only when an owner came back for their stash, judged by how much it had kept against food carried loose, never by whether it had carried anyone through a winter.

Then a copy of the code was taught to record every option every adult weighed, and every choice, in all sixteen worlds; and checked, again, to change nothing. The decisions showed three gates, one after another.

Most of the time stashing was not on offer at all. Only one adult-week in eight held food above the line, and in autumn, when it would have mattered, fewer than three in a hundred. When the line was crossed, more than a quarter of the time the one chance to set something down went to stone or wood instead. And when stashing was offered, it nearly always lost. Its chance of being chosen averaged one in twenty. What beat it was rarely foraging. It was giving food to others, talking, joining people nearby: being present for others outscored keeping something for later.

The few who did stash mostly learned that it paid, in the only terms they could judge: the food had kept better than it would have in hand. In five hundred and forty-eight returns to a stash across sixteen worlds and a hundred and twenty years, belief rose two times in three. And the belief spread: most adults held one, and it was told seven thousand times. But a belief could not open the gates. One caveat stayed attached to all of it: seed set down in the open is sown, not stored, so the belief about leaving food or seed somewhere was shared with sowing, and the record could not tell the two apart.

The creator's suspicion was half right. Stashing was worth less than foraging to habit, by a factor of four. But the strongest rival to a store for winter was not this week's hunger. It was this week's neighbours.

## Chapter 41 — G1: Where the Food Goes

S1 had found that a store for winter lost, most often, to a gift. The creator wanted to know where the gifts went before anything else was touched. "Not a new experiment. Not a new mechanic. A read-only question: who receives the food?" Children, parents, friends, strangers, the powerful, or the same few people again and again. "If food is mostly being redistributed inside social networks, that's a huge finding." And a warning to go with it: ACL had been strongest when it found something strange, mapped it completely, and only then changed the code.

Every gift in the worlds was already written down, giver, receiver and amount. The replays only had to look at each one as it happened and ask who the two people were to each other. The first attempt failed for a small reason: when someone received food and died later that same week, the measuring code could not find them among the living, and stopped. It was fixed and every world was replayed again.

The answer was family. Nearly three quarters of all food given went to kin, and the largest share of all, a third, went to brothers and sisters. In every one of the sixteen worlds, siblings received at least a fifth of everything given. Parents, grown children, and young children in the other parent's care came next. Friends received a tenth, people one merely knew a sixth, and strangers almost nothing.

It went to the hungry. Nearly two thirds of all food given went to people holding less than half a week's food, and in winter more than two thirds. Hardly any went to people who already had plenty. The respected received a little more than the rest, but only a little. And more than half of everything given was a gift being repaid.

So the food that might have become a store for winter did not vanish. It moved inside families, to whoever was hungriest that week, and came back later as a debt repaid. In ACL a family's surplus was kept, if it was kept anywhere, in its members' stomachs and in what they owed one another. That was why a stash and a gift competed for the same food, and why the gift so often won: it fed someone now, it pleased the giver now, and it was often returned. Whether that sharing helped the worlds through their winters, or only spread the same shortage more evenly, was the next thing the record did not yet say.

## Chapter 42 — P1: A Pool With Almost Nothing in It

By now the creator could tell the story in five lines. Behaviour could pass between adults. Winter was survived hand to mouth. A store lost, most often, to a gift. And the gifts went to family, to the hungry, and came back as debts repaid. "So the emerging picture is not selfish individuals failing to cooperate," the creator wrote. "It's cooperative families repeatedly solving short-term hunger while failing to create long-term surplus." One question had to come before anything was designed: "Does the family network function as effective risk pooling, or is it only spreading scarcity?"

Without switching sharing off, no replay could say what winter would have been without it. What the record could show were the marks each answer would leave. If families pooled risk, a hungry person with well-fed kin would fare better than one without; people would seldom starve while their kin held plenty; and giving would not leave the giver hungry. If sharing only spread scarcity, none of that would hold. A first test of the measuring code caught a flaw before any world was replayed: a person fed in a week has eaten, and is no longer hungry by its end, so help had to be looked for in the weeks after hunger, not during it. The change was written down before the data.

The marks of pooling were there. A person who began winter with almost nothing and whose family also had almost nothing starved to death about one time in thirty. With the same almost nothing of their own, but a family holding two weeks or more for each of its members, it was about one time in eight hundred. People seldom starved while a close relative nearby held plenty: in fewer than one death in six. Giving did not leave the giver hungry. And the few who were helped in a hungry week died half as often in the weeks that followed.

But the pool held almost nothing. Families entered winter with a ninth of what they would need. Only one hungry week in ten was followed by a gift. When people died, it was mostly because everyone around them was nearly empty too; the median of all that their close kin held, together, was less than two weeks of one adult's food. And the worlds that shared the most did not winter better.

The record could not separate a family's sharing from the land a family shared, since kin live near one another and good years come to them together; and the worlds that shared more also differed in copying. But the shape was clear enough to change the question. The family network did pool risk. It insured a family against one member's bad week, and could not insure it against a winter that emptied everyone. The bottleneck was not how food was shared. It was how much there was to share when winter came, and the one way to make that larger, the store, was the very thing that sharing outcompeted.

## Chapter 43 — U1: Two Weeks

After P1 the creator held the code back again. "I would not change code yet." There was one large question left, and it was an old one: E8.4 had found, before any of the experiments on anticipation, loss, stories or copying, that autumn left a surplus on the land and nobody took it. S1 had shown that stashing was rarely even possible, because only one adult-week in eight held enough food for it. "That means the problem starts upstream," the creator wrote. Was the food there at all? Were people spending autumn on other things? Were they hitting the limit of what they could carry, or wandering too far, or simply stopping once they were no longer hungry? And how much could they have gathered if they had kept on?

The first test of the measuring code made a familiar kind of mistake. It measured what people held after the week's work, so a person who had just foraged looked rich, and the hungry seemed never to forage. It was changed to measure what they held when they chose, before any data was read.

The food was there. Within reach of the adults of each world lay nearly three hundred units of plant food for each of them at the start of autumn, and nearly as much at its end. Each adult gathered about a hundred over the whole season. People did not spend autumn differently from any other season: they foraged in about four weeks of ten, as in spring, summer and winter, and spent much of the rest talking, joining others and giving. They almost never came near the limit of what they could carry. They did not wander far, and the land near them was not stripped.

They stopped when they were fed. With less than a week's food in hand, people foraged in more than four autumn weeks of five. With two to four weeks' food, in one week of seventeen. The code said why, in a single line written long before: hunger was one minus the weeks of food in hand divided by two. At two weeks of food, a person in ACL felt no hunger at all, and the pull to gather fell to almost nothing. And two weeks of food was exactly the line above which a stash became possible. People stopped gathering at the very point where storing could have begun.

The surplus E8.4 had found was real, and up to eighty more units per adult per autumn could have been gathered. It stayed on the land. The search that began with the question of why nobody prepared for winter had come back, by way of transmission, ledgers, decisions, gifts and families, to the simplest thing in a person's nature: when they stop feeling hungry.

**Note added after the evidence review (Chapter 45), at the creator's request.** This chapter read the two-week stop as the end of a search, as if U1 had found a flaw in nature. That reading was too strong. U1 identified a candidate bottleneck. The evidence review then raised another interpretation: people in ACL may resemble an immediate-return society, in which people with full human foresight eat what they get, share it, and store little, rather than a broken one. The question therefore shifted from "what should satiety be?" to "under what conditions do delayed-return societies emerge?" The design document N2 sets out that question.

## Chapter 44 — N1: What Should a Satisfied Person Feel?

U1 had ended at a single line of code, and that line was not culture. It was nature: how a person in ACL feels hunger. Changing it would be changing what kind of creature lived in the worlds, and the creator would not let that happen by instinct. "Write the candidates document. No implementation. No experiments. Just list every plausible interpretation of what should a satisfied person feel." Each was to be judged against the founding rule: is this nature, is this culture, is this scripting, is this a human capacity? "Only after that should anyone touch code."

The first thing the document had to admit was that the line in question had never been chosen from human evidence. Hunger that ends at exactly two weeks of food in hand was written when ACL's people were first given bodies, to make the early worlds work. And it mixed two different things: the hunger a body feels after a day without food, and the worry a person feels about whether there will be food next month. Nobody's stomach hungers with three weeks of food in the store.

Thirteen readings were written down. Some were changes to the feeling: hunger that ends later; two separate drives, one for the body and one for security; a satisfaction that fades smoothly with each extra week of food and never quite reaches nothing; a worry learned only by those who have lived through shortage; carers who feel further ahead. Some changed something else and were listed so that they would not be mistaken for answers: the cost of gathering, the line at which a stash becomes possible. One changed the body itself, so that food eaten in plenty is kept as a reserve and burned in want. And one left the feeling alone and lengthened the mind instead, so that a person could connect what they did in autumn with what happened to them in winter.

Each was given a fifth test, the one ACL had learned to care about most: would it change people who had never gone short? A change that pointed everyone toward storing, whatever they had lived, would be the answer written in.

Two were rejected outright. An inborn sense that winter is coming would write in exactly the behaviour ACL exists to see emerge; and the idea that holding food brings respect is culture, not nature, and must be left to appear. Four stood out, each for a different reason: the smooth satisfaction, as the smallest change; the worry learned from experience, as the only change to the feeling that leaves untouched anyone who has never been hungry; the body's own reserve, as the most plainly natural, with the warning that it might relieve the very pressure that makes storing worth inventing; and the longer mind, not as a satiety at all, but as the strongest other way to read what U1 had found.

No number would be tuned to produce storage. Whatever was chosen would be frozen, piloted and leak-tested like everything since E9, and every claim in the document about what humans feel would be checked against sources before anything was frozen. The choice was left to the creator.

## Chapter 45 — The People Who Do Not Store

The candidates were on paper and the creator still would not choose. "Do not choose an implementation. First, verify the human evidence behind the leading candidates." Four had stood out: a satisfaction that fades smoothly, a worry learned from lived shortage, a longer mind, and the body as a store. The creator wrote down what they expected before any evidence was read: the smooth satisfaction would be the safest, the longer mind the most interesting, the learned worry the cleanest to test, and the body the most realistic. And a second question was to follow: which of them changes the least while still answering U1?

Every claim about human beings was checked against its source. The body held up best. Human fat exists to buffer shortage, and humans are unusually fat for the environment they evolved in, which is tied to the uncertainty of their food. In a rural community in West Africa, women weighed three to four kilograms less at the end of the rainy season than in the dry season, every year: a store kept in the body, filled and drained with the seasons. The longer mind held up as a capacity: humans can see and plan for particular futures, and there is no convincing evidence that other animals can. But people discount the future steeply and inconsistently, and the ability to wait differs from one person to the next. The learned worry was real but pointed both ways: hard times leave lasting marks on how cautious people are, and yet scarcity can also narrow a person's attention to what is pressing now, at the expense of later. And the smooth satisfaction rested on a general truth, that the pull of food depends on the state of the body and that each extra unit of anything is worth less than the last, rather than on anything known about how people value food held for the future. The creator's four expectations all survived.

One source changed the question. Among hunter-gatherers, the anthropologist James Woodburn had described two kinds of society. In immediate-return societies, food is eaten soon after it is got and shared widely, and little is stored. In delayed-return societies there are stores, and lasting obligations around them. The people of the first kind have the same bodies, the same appetites and the same foresight as anyone. They do not store because of how their life together is arranged.

That was a description of ACL. W1 had found winter lived from week to week, G1 food shared inside families with whoever was hungry, P1 a pool with almost nothing in it. It was possible that the people of ACL were not missing a piece of their nature at all, and that what was missing was the kind of thing that cannot be written into nature: a different way of living together. The first candidate, to change nothing, was no longer only a baseline.

The second document measured each candidate against the code. The general feeling of hunger shaped twenty-six different pulls in a person's choices; changing it would change nearly everything a person did. E9 had left a narrower channel, a hunger used only for the pull to gather and hunt and for the thought of being hungry, three places in all. The smooth satisfaction, confined to that channel, was a single expression with one new number, leaving every social choice untouched and the old worlds reproducible; it answered U1 directly. The learned worry was nearly as small and the only one that left alone anyone who had never gone hungry, but likely to reach only a few. The body and the longer mind changed far more, and the longer mind worked on habit, while the stop at two weeks lay in instinct.

So the smallest change that answered U1 was the safest one, as the creator had guessed. It came with a warning written beside it: its one number was the danger, since a number tuned until storage appears is the answer written in. And it came with the question the evidence had raised, which no number could answer: whether to change nature at all.

## Chapter 46 — D1: A World Without a Lean Season

Woodburn had turned the question around, and the creator turned it once more before anything could be changed in a person. "Before discussing satiety changes, I want to know whether delayed-return behaviour is even adaptive in ACL's world." If food lay everywhere, thinly, all year, then living from week to week might simply be the right way to live there, and changing the people would be solving the wrong problem. Two questions were to be answered from the worlds as they were: whether ACL's food was dense, predictable and storable enough to make a store worth having; and whether sowing, which the people already did, worked as a delayed return they could discover. And a rule came with them: "If either answer is no, then changing agent psychology may be premature."

The world answered first. Food was predictable: a patch of land rich in one autumn was rich in the next, and a world's whole harvest varied little from year to year. It could be stored, as seed, which kept for many months. But it was not dense. The richest tenth of the land held about a quarter of all the food, spread over the rest in a thin, even cover. And winter took very little away. In the middle of winter the land still held seven-eighths of the food it held in the middle of autumn for each person living on it. The lean season that, among human foragers, makes a store worth the trouble barely existed. In this world a person could gather what they needed week by week, all year round, and most did.

Sowing answered second, and more strangely. It was already a real investment. Seed put in the ground grew more than twice its weight in food, weeks or months later; dozens of people in every world sowed, and most of them sowed again the next year. But it had no owner. Of the crop that grew where someone had sown, the sower ate a quarter, their close family another quarter, and other people the rest. When sowers came back to look at the place, their sense of whether sowing paid more often fell than rose, in every season, for reasons the record could not show. They kept sowing anyway. And all the sowing in all the worlds fed less than one mouthful in sixty.

By the rule the creator had written down before the data, one answer was largely no and the other was yes, but. The world as it had been built gave its people little reason to store, and the one delayed return they had discovered fed other people and taught them that it did not work. Changing their psychology would have been premature. Whatever made a people begin to keep things for later, it was not yet in this world.

**Correction (added after D2, Chapter 47).** This chapter says that sowers' sense of whether sowing paid "more often fell than rose". That measure was confounded: every belief fades a little each season, and D1 counted a belief lower a year later as a lesson of failure. D2 separated the sources and found the opposite: what sowers lived through raised their belief in sowing more often than it lowered it. The reading that sowers learn sowing fails is withdrawn; the rest of the chapter stands.

## Chapter 47 — D2: The Crop That Feeds Someone Else

D1 had left one strange result that the creator would not step past. Sowing paid, and the people who sowed seemed to learn that it did not. If that were true, ACL already held its own explanation for why nobody invested in the future: the world taught the lesson wrong. "Before evidence review, I want to settle whether sowing's negative learning is already explaining the absence of delayed-return behaviour," the creator wrote. If it was, the answer was already in ACL's world. If it was not, a harder lean season would become the leading path.

Two things were found before any data. The first was arithmetic. Sowing grew more than twice its seed, but the sower and their close family harvested only about half of what grew, which meant the sower's own family got back roughly what it had put in. The second was a mistake in D1. Every belief in ACL fades a little every season, about an eighth over a year, whether or not anything happens. D1 had counted a sower's belief as having fallen if it was lower a year later, and so had counted forgetting as failure.

A copy of the code was taught to write down, without changing anything, every placement of seed and every change to anyone's belief about sowing, with where it came from and what the spot held at the time. The record reversed D1. Setting forgetting aside, what sowers lived through raised their belief in sowing more often than it lowered it, and by more each time. Their looks at the places they had sown mostly told them the truth: where crop had grown and nobody else had taken it, three looks in four said sowing paid. The bad lessons came when the spot had fallen, its crop eaten or not yet grown. A few sowers had chosen spots that were already rich and saw them fade back to ordinary; most had sown where food was thin. D1's chapter carries a correction.

The return was the problem. Of everything that grew where a person had sown, the sower and their close family harvested about as much as they had sown; other people harvested more. The median sowing gave its sower's family back a quarter of its seed. Autumn sowing, two thirds of all sowing, cost the family more than it returned. Sowing fed the community and not the sower.

So sowing explained part of the absence of delayed return, and not all of it. People believed in it and kept doing it, but nothing they sowed was theirs, and an investment that pays everyone but the investor is a gift by another name. It also stayed very small, held back, perhaps, by the same narrow choices that kept people from putting food away. And in a world whose winter barely bit, even a sower who kept every grain would have had little need of it. The harder lean season remained a leading path, now beside a question the project had not yet asked: what it would take for anything to belong to anyone.

## Chapter 48 — N3: What a Winter Is

By the end of D2 the story had changed under the project's feet twice in a few days. U1 had found that people stop gathering at two weeks of food. D1 had found a world with almost no lean season, and had seemed to find that sowers learn sowing fails. D2 had shown that second finding to be forgetting counted as failure: sowers learned that sowing worked, and simply did not get its harvest. What was left was a coherent hypothesis. Storage was absent not because people failed to learn, and not because sowing was bad, but because the world stayed productive through winter, and a life lived week by week fitted it. The creator wanted that hypothesis tested against a leaner world, and wanted the reasons for every step kept in order first, so that anyone reading later would see the original reading, the correction, and why the lean season became the leading path.

The candidates came before any evidence. The code showed why ACL's winter was mild: plants went on growing in winter at a seventh of their spring rate, and that growth roughly cancelled the winter's dieback, so the land stayed nearly full. It also showed a subtlety: a week of gathering took the lesser of a person's rate and what lay on their patch of ground, so a winter would only bite if patches fell below about twenty, whatever was left on the land as a whole. Nine readings of a harder winter were written down: no growth in winter at all; plant food dying back much faster; food left in place but out of reach under snow; an autumn pulse of seed; more variable years; leaner winters only where it was colder; people needing more food in the cold; and crops that alone survived the winter. The last was rejected at once, because it built the answer into the world. Changing the world was nature in ACL's terms, so the danger was no longer scripting people but tuning the world until storage paid.

The evidence then sorted them. Temperate plants go dormant in winter and wait for spring warmth to grow again, so a winter with no growth was not a dial but the realistic value. Lean seasons vary with climate, so a world whose colder places had real winters and whose warmer places did not was the realistic shape. A winter in which plant food simply vanished was half supported: foragers in short growing seasons do lack plant food, but no source gave a rate. And snow that hides food was shown in animals, not in people.

The evidence also widened the question in two ways. Human foragers meet short growing seasons mostly by eating meat, and also by losing weight, by moving, and by storing; storing is only one answer among several, and ACL's people could hunt almost not at all. And foragers who store, rank and own tend to live by resources that are predictable, rich, clumped and held: ACL's food was predictable and rich, but thin and nobody's.

So the first test of the lean-season hypothesis would be the smallest one the evidence supported: take winter growth to nothing and change nothing else. It might do almost nothing, by the arithmetic of the forager's week, and that would be a finding. It might bring storage, or sharing, or something else entirely. The design would have to say, before any world ran, what would count against the idea that ACL's people live the life their world rewards.

## Chapter 49 — L1: The Stop Rule Holds

The first test of a leaner world was the smallest the evidence allowed. One setting would change: wild plants would no longer grow in winter at all, as temperate plants do not. No rule would change, no person, no line of code. Before anything ran, the creator froze what would count against the idea that ACL's people live the life their world rewards: if removing winter growth produced substantial delayed return, at least two of three demanding measures of it, the idea would take a serious hit. The creator added a sentence to guard against reading too much into the opposite: "Failure to create delayed-return behaviour is not evidence that lean seasons are irrelevant. It is evidence only that removing winter growth alone is insufficient under ACL's current world structure." And a rule went with it: a null would be read only if winter had in fact grown leaner.

A survival pilot came first, on four worlds of its own, read for nothing but whether their people lived. Its rule was simple: if two of the four died out, the experiment would not run. Two did. The experiment did not run.

Only afterwards did a weakness in the pilot show itself. It had changed the winter in four worlds and watched them, but had not watched the same four worlds without the change. Some worlds in ACL die out anyway: two of sixteen had done so in E13R's control, with nothing altered. The two that died had both begun small. The pilot could not say whether it was the winter that killed them. The creator asked for one check before any decision, limited to the same question: the unchanged world, on the same four seeds, read only for survival. The check, and what each answer would mean, were written down before it ran.

Both answers turned out to be partly true. One of the two worlds died in the unchanged world as well; it had been fragile from the start. The other lived in the unchanged world, small, and died only without winter growth. And in every world that survived, the people of the leaner winter were fewer at the end, a third fewer in one, two thirds fewer in another. The strongest effect was not extinction but shrinkage. Winter growth, which D1 had found left the land almost as full in winter as in autumn, turned out to be one of the things that kept ACL's peoples alive and growing.

Nobody quietly resumed the experiment. The frozen design stood, untouched; the pilot's stop was obeyed; the weakness was named; the check was limited and declared. The finding about winter growth was real, but it did not answer the question the path from N2 had been built to reach, whether a real lean season brings delayed return. The creator chose to redesign the pilot so that each world would be watched both ways, rather than retire the idea or call the shrinkage the end of it. And the shrinkage left a warning for any experiment that followed: worlds with fewer people share less, have fewer people to learn from and fewer to sow, so any comparison of how people meet a leaner winter would have to set population beside every other measure.

## Chapter 50 — L1: Fewer People, the Same Winter

The redesigned pilot watched eight new worlds both ways, with and without winter growth. Its rules, written before it ran, asked only whether the leaner winter killed more worlds than those same worlds lost anyway, and whether enough pairs survived to compare. Three of the eight unchanged worlds died out, and one of the eight leaner ones. The extinctions of the first pilot had been mostly the fragility of particular worlds, not the winter. Five pairs survived, the minimum the creator had set. The pilot passed, and the experiment ran as it had been frozen, with the creator's amendment: population beside every measure, and a verdict taken only from worlds where both arms lived.

The answer came in the order fixed in advance, and the first step decided the rest. The manipulation check asked whether winter had in fact grown leaner. It had not, for the people living through it. Food on the land for each person in midwinter was higher in the leaner worlds than in the ordinary ones, and a week of gathering in winter brought in the same. On the delayed-return test itself, nothing moved: on the six pairs of worlds where both kinds survived, the people of the leaner winter held the same share of their winter's need, stashed almost the same, and foraged in autumn as they did in summer. None of the three measures came close. By the rule written before the run, this null said nothing about lean seasons at all. The setting had not made one.

The reason was in the populations, and it exposed a flaw in the design. The leaner worlds ended with far fewer people, a median of six against thirty. The manipulation check had measured food on the land for each person, and with fewer persons, each had as much as before. The design should have measured the land itself as well. The very confound the creator's amendment had guarded against in the outcomes had struck the check that came before them. The flaw was written into the record beside the result.

What the worlds had done was not a finding the experiment was built to test, and it was recorded as an observation, not a result. A winter with no growth had been answered not by storing, nor by sharing more, nor by any new way of life, but by numbers. The worlds came to hold fewer people, until each of those who remained had a winter as plentiful as before. It was what the human evidence had said: that the lean season sets how many people a land can carry. A steady, predictable lean season, in ACL as among real foragers, could be met by density. A lean season that people could not adjust to by their numbers, one that came unpredictably, would be a different test.

## Chapter 51 — Uncertainty: The Night's Work

L1 had not failed in the way anyone expected. A leaner winter had not pushed ACL's people to prepare; it had left fewer of them, each as well fed as before. "The world absorbed the shock through population density instead of behaviour," the creator wrote, and drew the consequence: a permanently harsher world can be answered by fewer people, but a family stores because this winter might be worse than the average, not because every winter is. A new hypothesis was written down before any work on it began. Delayed-return behaviour is primarily an adaptation to uncertainty, not to average scarcity. Then the creator went to sleep, with an instruction: build, verify, document, keep the audit trail clean, and leave findings to read in the morning.

The candidates came first: wider swings in the growing year with the same average; rare severe winters; runs of bad years; bad years that strike some regions and not others; winters that come early or last long; and a harsher and more variable world, set aside because a lower average is answered by density, as L1 had shown. Three lessons from L1 bound them all. Keep the average and change only the spread. Measure the land itself, not only food per person. Watch every world both ways from the start.

The evidence sharpened the hypothesis. Economists studying village insurance had shown, almost by definition, that sharing within a group can insure each household against its own bad luck but not against a shock that strikes the whole group: under full sharing, each household's fortune still moves with the village's. Villages in southern India insured their members' own misfortunes well, and were vulnerable to poor rains that came to everyone. Households elsewhere held buffer stocks as well as sharing. ACL's own P1 had found the same shape. So storage was the candidate answer to bad years that strike everyone, and sharing the answer to bad years that strike some. The evidence also warned the other way: in a model of mobile foragers, it was families that shared and moved between camps who survived unpredictable environments, not those who stayed put. And it gave a number. Real grassland production varies from year to year by about a third. ACL's world, by D1's measure, varied by about a fourteenth.

Then the existing worlds were asked what their own bad years did. They do kill: winters with the least food on the land brought about seven times the starvation of the richest. After a bad winter people sowed more, and a few more held large stores in autumn; but households held no more against the next winter, and fewer of them put food away. Poor years ran on into one another, because the land and the people on it carried each year into the next. At the uncertainty ACL had, bad winters did not teach storage.

By morning a design was drafted and waiting, frozen nowhere: the unchanged world beside two worlds made as variable as a real grassland, one in which the bad years struck everyone together and one in which they struck different regions at different times. The hypothesis would predict storage in the first, and sharing and moving in the second. The width of the swings would be found by measuring the land, not by watching the people, and nothing would run until the creator had signed.

## Chapter 52 — U: The Land That Would Not Vary

The creator signed the design in one line: a grassland target, quarters for regions, sign off. Three kinds of world would run side by side from the same seeds: the world as it was; a world whose growing years swung wider, all together; and a world whose years swung just as wide, but separately in each quarter of the map. If H-L5 was right, the first kind of uncertainty would teach storage and the second would teach sharing and moving.

The quarters needed code, and the code was checked before it was trusted: with the regions switched off it reproduced the old world exactly, and its own random numbers took nothing from the world's. One claim in the design was found false by these checks and corrected in the open: the wider world shared only its first year's draw with the control, not every year's, because once the land grew differently the people did differently and the world's dice fell differently.

Then the width. It was to be set by measuring the land, never the people: the weather's range widened step by step until the food on the land varied by about a third from year to year, as a real grassland's does. It never got there. At the present width the food varied by about seven parts in a hundred. Weather allowed to run from nothing at all to nearly double moved it only to eleven. The plants grew back toward their limits, and most of the weather's swing was smoothed away before autumn came. The rule written in advance said what to do: take the widest, and say plainly how far short it fell. That was written down, and the design was frozen.

The pilot came next, eight worlds in each arm, counting only who lived. The control lost four of its eight worlds within the hundred and twenty years, as ACL's worlds often do. The world-wide arm lost seven, three of them in the first decade or two: a single year in which almost nothing grew anywhere was enough. The patchy arm lost six, more slowly; a bad quarter left three others. Not one seed kept all three arms alive. Both stop rules fired. The main worlds were never run, and nothing was learned about storage or sharing.

What was learned was about the land. In ACL as it stood, no weather gave the people a grassland's uncertainty, and the weather that came closest killed them. The plants smoothed the good years and could not smooth the worst. The hypothesis was untouched, neither supported nor refuted; the world could not yet ask the question. The design went back to the creator, with the choices laid out and none of them taken.

## Chapter 53 — F1: The Worlds That Grew Old

When U stopped, the creator did not reach for another storage hypothesis. Half the control worlds in its pilot had died, and the creator's view was that understanding that mattered more than any experiment built on top of it. No fixes, no tuning, no code changes: first find the mechanism.

The first finding was a smaller number. Across all forty control worlds already run with the same code, twelve had died, not half; across the twenty-four new worlds that later checked the work, ten. A third, then, not a half. Every one of the forty old worlds was replayed with a silent observer, and every replay reproduced its recorded populations exactly.

The worlds did not starve. People in dying worlds went hungry no more often than people in living ones; their land held as much food or more; their small children always had someone caring for them. What the dying worlds had in common was quieter. Their last child was born forty to sixty-five years before their last death. For decades nobody was born, and the people who were left grew old together, until old age and illness took them one by one. Women of childbearing age lived on in those worlds, sometimes for thirty years, and in every one of those years they had no partner.

The reason was in nature, not in culture. The founders paired in their first decade. After that, pairing nearly stopped in every world, dying or living. A person looking for a partner courts only someone within sight, four tiles away, or walks toward someone a little further, or else wanders a few steps at random, on a world of sixteen hundred tiles. In a small, scattered people, a single woman almost never had an eligible man in sight, though one was usually alive somewhere. Large worlds kept enough people near one another for chance to do the rest. Small ones did not, and what made a world small was often its first years: worlds that died had lost more of their children early, and by their twentieth year they were already smaller. By that year the worlds that would die could be told from the ones that would live, by their size alone, decades before the end.

Part of what was first written had to be corrected before the new worlds were run: the claim that single women saw no partner "in any world" was true only of small ones. The correction was added beside the claim, and the test written for it was left as it was and reported as failed.

The project had spent many experiments asking why its people did not prepare for winter. F1 found that a third of its worlds had been ageing out the whole time, not for want of food but for want of meeting. It was a gap in the world itself, and the question of how real people find partners across a landscape now stood in front of every other.

## Chapter 54 — Stage Zero, Reopened

Stage zero had been closed for a long time. Its question, whether there was a world worth living in, had seemed answered by physics, seasons, bodies and minds that worked. F1 reopened it. A third of the worlds were ageing out for want of meeting, and the creator moved the project back to its foundation and asked how real people find partners.

The answer, gathered from the literature without touching the code, was that real foragers never do it the way ACL's people did. Nobody finds a spouse among a handful of people by bumping into them. A forager's social universe runs to hundreds of adults met in a lifetime; the network within which spouses are found is counted in hundreds; a people that can always find any eligible partner still needs something like seventy-five to a hundred and fifty members to be safe from the accidents of births and deaths, and more when the people are spread over land. Spouses come from outside the local group: in small groups the balance of men and women swings by chance from year to year, and people move outward to meet it. Camps are fluid, joined and left many times a year. Bands gather at good places in good seasons, and marriages are brokered there. Above all, most marriages are arranged by parents and kin, with service or exchange between families binding groups together across the land. And a model of foragers who simply wander, as ACL's people do, found that wandering alone stops bringing groups together once people are spread thinly enough.

Against that, ACL's whole world held twenty founders, fewer than any estimate of a people that can last, and its people looked for partners only within sight. The review drew a line the project had drawn from the start. Arranged marriage, bride service, gatherings and their rituals are culture; ACL could not write them, only watch whether its people ever found them. What belonged to nature was smaller: the wish to find a partner, the memory of people met and where they lived, the legs to go there, and the number of people the world began with. ACL had no scale either: a tile had never been given a size, so no distance from the ethnographies could be carried over.

Nothing was changed. The review ended with a question for the creator, and a test to run before any change: would twenty founders last even if every one of them could find any eligible partner at once?

## Chapter 55 — F2: If Everyone Could Find Everyone

F1 had found the symptom, and the evidence on real foragers had offered two explanations that F1 could not tell apart. Perhaps ACL's people simply could not find the partners who were there. Or perhaps twenty founders were too few, and no way of searching could save them. The creator's view was that the cleanest question was also the cheapest: give every person perfect knowledge of every eligible partner in the world, and see who still dies.

It could not be done by watching. A copy of the code was made with one switch, never meant as nature: once a week, every unpartnered woman was paired at once with an eligible man from anywhere in the world, by the code's own rules about kin and age, and he came to her. With the switch off, the copy reproduced the old world exactly. With it on, it was run on the same sixty-four worlds F1 had studied, each to be compared with itself. The thresholds were frozen first: five deaths or fewer would mean the problem was search; seventeen or more, size; anything between, both.

Seven worlds died. Twenty-two had died before. Perfect finding saved seventeen of them, and populations that had held still for a century grew instead. The verdict, by the frozen rule, was both, one world above the line that would have called it search alone. The count was reported as it fell.

The seven that still died told the rest. In every year that a woman of childbearing age was single in those worlds, there was no man anywhere who was not her kin and close to her age. The pool was not hidden; it was empty. These worlds had been tiny from their first decade, and lost half as many children again as the worlds that lived. Perfect finding put off their end by seven to forty years, and could not prevent it.

Two more things came into view once people could pair. Couples brought together did not stay together: in the ordinary course of foraging they drifted apart, and nearly half of women's weeks were spent with a partner out of reach. And the larger peoples that perfect finding allowed met the limit of their food: starvation became half of all deaths. The old question of winter, set aside while the worlds were dying, was waiting for them as soon as they lived.

None of it was a mechanism to adopt. Real foragers widen their mating networks through culture, and ACL could not write culture. What F2 showed was that ACL lacked something that made a wider network reachable, and at the margin, enough people to begin with.

*Correction, added in October 2026 during C1:* the figures above for couples out of reach were shares of all women's weeks, including women with no partner. Counted per couple, partners were already out of reach about three weeks in five in the unchanged worlds, and only a little more under perfect finding. Couples had not begun to drift apart because of F2; they had always been apart about half the time, and F2 only made it visible by giving most women a partner.

## Chapter 56 — C1: Apart Half the Time

F2 had left a loose thread: once people could pair, their partners were so often out of reach. The creator chose to follow it before changing anything, and to follow it only by watching.

Sixteen worlds were replayed for their first forty years with an observer that read every couple, every week, and changed nothing. The questions were frozen first: how far apart couples were, which of them moved away and while doing what, whether the pull back to a partner was there when it was needed, and how couples came together again. Before any world ran, reading the code had already turned up something odd. A child could be conceived only when partners were within two tiles of each other. But a person felt drawn back toward a partner only when the partner was more than three tiles away. At exactly three, a couple could neither have a child nor feel any reason to close the gap.

The worlds said the same thing, and then a little more. Couples were apart in about half of all their weeks. Two in five of those weeks were spent at exactly three tiles, in the gap. Most separations began with foraging: each partner went to whatever nearby patch looked best, and nothing in either of them weighed being near the other. When a partner had wandered further, the wish to go back was there, among their top choices three weeks in four, and lost to food five times in six. Love was not the problem; affection between partners was high. Hunger simply outbid it. A third of the time couples found each other again by accident, two foragers landing on neighbouring ground. Sixteen new worlds, run only after all of this was written down with thresholds to meet, repeated every part of it.

The study also corrected the one before it. F2 had said couples drifted apart once perfect finding brought them together, from a fifth of women's weeks to nearly half. Those figures had counted women without partners too. Counted per couple, ACL's partners had always been apart about half the time; F2 had only given enough women partners for it to show. The correction was added beside the earlier words, which were left as they were.

Nothing was changed. The two thresholds had been written separately, long before anyone asked whether they agreed, and whether they should was a question about nature: about what living together means for real people who forage apart by day. That would have to be answered from evidence, not from how many children the change produced.

## Chapter 57 — Where a Couple Sleeps

C1 had found that ACL's couples spent half their weeks apart, and the creator would not change anything until the evidence said what living together means for real people who live by foraging.

The answer was simpler than the question. Foragers do not spend their days side by side. Often husband and wife go out separately, after different foods, and share what they bring back; among the Aka they sometimes hunt together with nets, and even then are within sight of each other only about half the time. But at the end of the day they come back to the same place. A camp is the centre of a forager's life: people forage out from it and return to it, and the camp itself moves every few weeks to fresh ground. And when spouses are kept apart, by migration or by work, fewer children are born, in proportion to how long and how completely they are apart.

ACL counts time in weeks. Measured that way, a real couple would be together almost every week, because whatever they did by day they slept in the same camp. ACL's couples had no camp. Each person had a place they remembered as best, but partners did not share it, and nothing brought them back to it together. Half their weeks apart had no counterpart in any people the review could find. The gap was not a want of affection; it was the want of a shared place to come home to.

The review drew the line again between nature and culture. The pair bond, and the habit of coming back to a home base, belong to the species; the division of work between men and women, and the rules about who moves where at marriage, are culture, and ACL could not write them. Three possible changes were laid out, none chosen: make the two thresholds agree, give partners a shared home to forage out from and return to, or let the pull toward a partner be felt at any distance. The best anchored was the shared home. The first step would be to look, without changing anything, at how far apart partners' homes already lay.

## Chapter 58 — Two Homes

Before deciding how to give couples a shared place, the creator wanted to know what ACL's people already had. Each person did have a home of a kind: the place where life had felt best, remembered and slowly forgotten. Partners had never been asked to share it. The question was simple and read-only: how far apart were the homes of people who were partners?

A rule was written first. If partners' homes lay close enough for a child to be conceived in at least two weeks in three, the smallest change would do: make the two distances in the code agree. If they lay that close in one week in three or fewer, a shared home would be needed. Anything between would be called mixed, and left to the creator.

It came out mixed, almost exactly in the middle. In about half of all the weeks a couple was together as partners, their two homes lay close; in the other half, apart, and in a third of all weeks four tiles or more. When couples were apart, two times in five each partner was near home, and the homes were what lay apart. And the homes would not hold still: a person's home changed in nearly one week in five, every five or six weeks on average, because a home in ACL was only the place that had felt best lately. By coincidence, that is about how often a Hadza camp is said to move. The coincidence was noted, and not used.

What the check showed was that fixing the gap between the two distances would not be enough by itself. ACL's partners did not have one home with a gap in the middle; they had two, which agreed half the time and drifted. The evidence pointed to a shared home. Whether to change the small thing first, the large thing, or one and then the other, each measured on its own, was the creator's decision.

## Chapter 59 — T1: A Pull That Lost to Food

The creator chose to test the small thing first. Couples three tiles apart could not conceive and felt no pull to close the gap; T1 changed only that, so that a partner more than two tiles away became someone to be drawn toward. Everything else stayed as it was: how strong the pull was, how it weighed against hunger, how people foraged. The outcome bands were frozen, and so was a check that the change had done its job: the weeks couples spent at exactly three tiles had to fall by at least half.

They did not fall at all. Couples spent as many of their apart weeks at three tiles as before, and only slightly fewer weeks apart overall. Under the frozen rule, when a manipulation does not do what it was meant to, its outcome is not read. Twenty-seven worlds died instead of twenty-two, and the number was written down and left alone.

Replaying a few of the worlds showed why. At three tiles the new pull was there, among each partner's leading choices four weeks in five. It was chosen one week in five. Half the time people went to forage instead, and the couples who had drifted back together that week were drawn apart again by the next week's foraging. T1 had supplied a pull where there had been none, and food had outbid it, exactly as C1 had found further out. The gap in the code was real; it was not what kept couples apart.

The run taught something else, about the worlds themselves. A change that barely moved anyone's behaviour still altered the fate of nineteen of the sixty-four worlds, seven saved and twelve lost, because any change, however slight, sends each world's chances down a different road from the first week. A difference of five worlds in sixty-four could not be told from chance. Every experiment from then on would need to measure that noise before claiming to see past it.

What was missing, the evidence and now this failure agreed, was not a pull toward wherever a partner happened to be. It was a place that foraging returned to.

## Chapter 60 — HB1: A Home That Did Not Move

The evidence had said that real couples share a camp, and the creator designed the test with care. Each couple would have a home, chosen from the places both of them remembered as best. Each week, wherever they had gone to forage or to see someone, partners within a day's walk would come back to it. Nothing would say who moved to whom, or who gathered what. And this time, after T1, the noise would be measured: a third set of worlds, identical to the control except for a single extra roll of the dice in the first week, would show how many worlds change their fate by chance alone.

The change did exactly what it was meant to. Couples who had been apart more than half their weeks were now apart almost never. Women with partners conceived more often. In the first decade, more children were born.

Then the worlds began to die. Thirty-three of the sixty-four died out, against twenty-two in the control; paired world against world, eighteen were lost and seven saved, and the test said this was not chance. The worlds with one extra roll of the dice lost twenty-four, which was what chance looked like.

It was not the crowding that had been feared: illness took a smaller share of the dead. It was hunger. Families tied to one place each week ate the land around it, and a home in ACL was only the place that had felt best, which changed slowly as memories faded; it did not move when the food around it ran out. Adults starved, about three quarters more of them in the first forty years; teenagers, too old to follow a parent and too young to forage well, died almost three times as often. Women were widowed, pairing slowed, and populations that had held steady shrank.

Read against the evidence, the failure was exact. Real foragers return to a camp each night, and they also move the camp when the land around it is spent. HB1 had given ACL's couples a centre without the movement that real centres have. A home that does not follow the food, the worlds said, is worse than no home at all.

*Correction, added in October 2026 after HF1:* the land around HB1's homes was later measured directly, and it was not bare: about three per cent emptier than in the control. The explanation in this chapter, that families ate the land around homes that did not move, was not confirmed. The hunger was real; its cause was not the one told here.

## Chapter 61 — HF1: The Land Was Not Empty

HB1 had left an explanation that fitted too well: families tied to one place had eaten the land around it. The creator would not build the obvious remedy, a home that moves with the food, on an explanation that had only been inferred from deaths. The food on the land would be measured first, around every couple's home, in worlds with a shared home and the same worlds without, and on sixteen new worlds besides. A rule was fixed in advance: depletion confirmed if the land near shared homes held four fifths or less of the food it held in the control; not confirmed if it held nine tenths or more.

The first run turned up a fault, not in the worlds but in the measuring. The observer had worked out each tile's capacity in the first week and kept it, but floods enrich the land over the years, and the capacity grows with them; the old figure made tiles look fuller than full. The fault was corrected, the run repeated, and the mistake written down beside the numbers that had already been seen, before the new worlds were touched.

Then the answer came, the same on both sets of worlds. The land around shared homes was about three per cent emptier than around the same couples' homes in the control. A short walk further out it was, if anything, fuller. The people of HB1 were starving, again, on the new worlds as on the old, about three quarters more adults than in the control; but not because the land around them was bare.

The prediction had been that depletion would be confirmed. It was not, and the remedy that depended on it was set aside. Two leads were written down for the next look: the people of HB1 hunted less, and they had more children, in a world where parents feed their children first. Whatever was making them hungry, it was not the land.

## Chapter 62 — HF2: Fewer Gifts

The land had not been bare, so the hunger had to be looked for somewhere else. Two places had been written down: perhaps the couples who shared a home had too many children to feed, in a world where parents feed their children first; perhaps they hunted less and lost their meat. The creator had a rule fixed before anything ran, and sixteen new worlds set aside to check it.

Neither held. The couples with a shared home had a few more children each, about one in ten more, and the hunger did not fall mainly on parents: it fell on everyone, on parents, on couples without children, on people living alone. Meat turned out to be almost nothing in ACL, two hundredths of one per cent of what people ate; whatever happened to hunting could not starve anyone. The prediction had been that the children would explain it. For the second time running, the prediction was wrong, and it was written down as wrong.

Something else showed in the accounts. In worlds with a shared home, people gave each other about two fifths less food. The land gave them almost as much as before; what they lost was what had passed from hand to hand, and it was most of what they lost. The pattern was noticed in the first sixteen worlds, written down before the new ones were run, and the new ones showed it again, almost to the decimal. Because no threshold had been set for it in advance, it was called consistent, not confirmed.

Years earlier the project had found that food in ACL is kept in other people's stomachs and debts: what protects the hungry is what their families and neighbours give them. A shared home ended every couple's week in the same place. Perhaps it ended, too, the meetings by which food found its way to those who needed it. That was the next thing to find out.

## Chapter 63 — HF3: Help Within Reach

The accounts had shown that people with a shared home gave each other less food. HF3 asked the obvious next questions, with a rule set before anything ran and sixteen more new worlds to check it on. Did the lost gifts explain the hunger? And if gifts fell, why: because people met fewer of the hungry, because fewer of them had food to spare, or because, with food to spare and someone hungry beside them, they chose to give less often?

Gifts fell again, by two fifths, in the old worlds and the new. But when an adult was starving, someone with food to spare was within reach just as often as in the worlds without a shared home: about two weeks in five, in both. Help was no further away. It came less often, and when it came it protected less: people who had been given food lately starved more often than the same people did without a shared home. Meetings had not fallen, which was the prediction, wrong for the third time in a row. What fell, a little each, were the number of people holding a surplus and how often they used it to give; and which fell more changed from one set of worlds to the other.

So the third check closed like the first two. The land had not been emptied; there were not too many children; meat was nothing; and the gifts, though fewer, were not what starved people. The hunger was real, measured four times on four sets of worlds, and no single cause the project had thought to test explained it.

What the checks had in common was a set of small shifts: a little less food coming in, a fifth fewer people with food to spare, two fifths fewer gifts, poorer foraging near home. In ACL an adult counts as starving when they fall more than a twentieth short of what they need, and many sit close to that line. Small shifts, each too small alone, could tip many of them over. That was the one explanation the data still allowed, and it was written down as a hypothesis, not a finding. Whether to test it, or to leave the question and find another way to keep couples together, was the creator's to decide.

# Part IV — The Great Debates

Some of the most important turns in ACL's thinking came from arguments, not experiments: two serious positions, held before the evidence, and settled, or not settled, by what the worlds did. This part records them as they appear in the record. Where the record shows who held which view, it says so. Where it does not, the positions are described without names.

## Chapter 64 — Isolation or Distraction?

**The question.** Why did E2's population fall?

**The positions.** The creator believed the four changes had cut people off: with the narrow jump gone, fewer people could reach a mate, and that one physical change decided who was born. The assistant thought the cause was more likely in how people spent their time: with more claims to check and more to watch, they gave less time to finding mates and feeding children. Both wrote their odds down before looking: 60% on isolation from the creator, 35% on time and attention from the assistant.

**What the evidence said, the first time.** E3 found neither clearly. Choices did not change. Birth rates per woman did not change. One world showed isolation exactly, but the pooled numbers hid it, and the analysis leaned instead toward infant deaths in a few worlds.

**What the evidence said, the second time.** E4 ran three times as many worlds and settled it. Isolation, confirmed over 24 worlds. The infant-death explanation did not replicate. The assistant's explanation was not supported at either stage.

**What changed.** Two things. A respect for the simplest physical explanation, and a rule of thumb that survives in every later experiment: eight worlds can mislead; when they disagree with intuition, run more before believing either.

## Chapter 65 — Richer Matter or Richer Discovery?

**The question.** After the E5 freeze: why does novelty stop?

**The positions.** One view held that the world was too poor. Six materials and two acts can only make so much; give matter more properties and more ways to change, and history will have more to find. The other view held that possibilities were already lying unused, and that the problem was the path from a possibility to a practice.

**What the evidence said.** E6 tested the first view directly, and it failed. More properties, clay, heat and filling were all added. People used the shallow end and never reached the deep one. The second view had no experiment yet, only a suspicion. E6.5 turned the suspicion into a measurement.

**What changed.** The project's model of the problem. Richness of the world is necessary but not enough. What matters is whether anything leads a person from what is possible to what is done.

## Chapter 66 — Opportunity or Interaction?

**The question.** After E6: where exactly does the chain of discovery break?

**The positions.** E6.5 wrote down four possibilities before running. One: people never meet the opportunity. Two: they meet it and ignore it. Three: they act on it and the result is transformed, but nobody cares. Four: someone discovers it, but the knowledge dies with them.

The fourth was the intuitive favourite. Knowledge loss had been everywhere in E1, with 3,828 techniques lost against 789 rediscovered.

**What the evidence said.** For water, opportunity was plentiful: a person holding a watertight vessel stood at fresh water for 102 weeks. For heat, opportunity was rare, because fires are rare and brief. But for both, the step was never chosen. Possibility two was true for both. Knowledge loss, the favourite, was not the general problem: the one water vessel was taught to seven people and outlived its maker by decades.

**What changed.** The name of the problem. It became the interaction bottleneck.

## Chapter 67 — The Reward Horizon

**The question.** If people never fill a vessel because the payoff comes weeks later and far away, is the real problem that they cannot learn from delayed rewards at all?

**The position.** It was a reasonable suspicion. The habit system, which learns which kinds of action go well in which situations, forgets fast. A reward five weeks after an act counts a third as much; one twenty weeks later counts almost nothing. If that were the only way to learn, delayed payoffs would be invisible.

**What the evidence said.** E6.6 found two other channels that learn over much longer delays. Beliefs about leaving things at places learn from outcomes up to a year later. And the worth of a made thing learns with no limit at all, as long as the thing is still held: things first used more than a year after they were made were made again more often, 47%, than things used at once, 16%. If a vessel had ever been filled and later drunk from, the lesson would have reached its owner.

**What changed.** The suspicion was dropped. The problem is not learning from delay. It is the first step, which no delay can teach because it never happens.

## Chapter 68 — Fix the World or Fix the People?

**The question.** Once the interaction bottleneck was named, which side should be mended?

**The positions.** One option was to change the people: let them handle what they hold with what is around them more often, beyond play. That attacks the bottleneck where it lives, in the decision. The other option was to change the world: let nature do the first step itself, the way crossing water once showed the raft its worth. Rain falls into an open hollow thing. A fire hardens the clay beside it.

The record says plainly where the creator stood: the creator preferred, for now, not to change the people. E7's design made that a hard rule. The people's code is frozen.

**The argument for it.** Changing the world keeps the experiment clean. If people's minds are changed and novelty returns, nobody can tell whether the change found something real or put the answer in. Changing the world only offers conditions; whether anyone takes them up is still up to the people.

**The argument against it.** If the bottleneck is truly in the decision, mending the world may only move it. A people that never tries anything unrewarded might drink from a vessel that rain filled and still never think to fill one.

**What the evidence says.** E7 answered half of it. For heat, the world produced hundreds of first encounters, and people kept the results but built nothing on them. That is close to what the frozen rules called Failure B: the bottleneck lies, at least partly, beyond the world. For water, the world produced almost no encounters, because the vessels it was meant to fill almost never exist. Neither failure mode's definition was met exactly, and the debate is narrower than before, not closed.

// CREATOR'S NOTE (to be written): Why did you prefer to leave the people unchanged? Is that a principle, or a choice for now?

## Chapter 69 — Topology or Multipliers?

**The question.** Are all inventions alike, or do some matter differently?

**The positions.** The ordinary view treats invention as improvement: better tools, more output, a steadily richer life. The view that grew inside ACL held that most inventions are multipliers, making something a little better, while a rare few change the map of what is possible at all: a raft that reaches land never reachable before, a vessel that makes dry land livable.

**What the evidence says.** It is suggestive, not decisive. Every map-changing invention in the record, the raft and the watertight vessel, stalled until its use could be felt. Everything else people made was a multiplier, and in E5 the whole list of kinds was complete in eleven years and never grew. That pattern fits the topology view. It does not prove it.

**What changed.** The project began to ask of every new piece of physics: does this add a multiplier, or does it add a new connection to the map?

## Chapter 70 — Physics or Cognition?

**The question.** Under all the others: is the freeze a property of the world, or of the minds in it?

**The positions.** Everything from E6 to E7 has tried the world side first, partly from principle and partly because the world side is easier to change cleanly. The record also shows a decision made in advance about fire: before E6, the creator decided not to touch how fire works, so that whatever fire did would be what the world did on its own. But the autopsy's own last line points the other way: people try new things almost only in play, and adults play in about one week in a hundred.

**What the evidence says.** Not yet enough, but it has moved. E7 showed that richer encounters with the world do not, on their own, start a chain. And the code facts found while building E7.6 and E7.7 point to the minds and the society: skill that cannot be taught, watching that teaches almost nothing, and a memory that discards composite inventions. This debate is still open, and it may be the one that decides the project.

**Added in edition 6.** E8.1 and E8.2 moved it again, toward the world. People in ACL know how to make things and have the materials, but making is almost never worth more to them than eating and company, and measurement of what tools actually do shows why: they add almost nothing to how much anyone eats. That is a fact about the world's economy before it is a fact about anyone's mind.

## Chapter 71 — Population or Transmission?

**The question.** If the worlds are losing what they know, is it because there are too few people, or because what one person knows cannot pass to another?

**The positions.** The creator ranked population first. The worlds hold twenty to ninety people, the size of one village. When a single master dies, a fifth of a world's expertise can go with them, and there is no other village to learn from. The assistant pointed to transmission: in today's code a skill cannot be passed on at all, however many people there are.

**What reframed it.** The two are not rivals. In the standard model of cultural loss from human evolution studies, a skill survives when the number of learners, multiplied by how faithfully they copy the best, outweighs what is lost when people die. A large population that copies badly still loses its skills. A small population that copies perfectly still loses them when its few experts die. The useful question is not which one, but what each contributes.

**What was proposed.** One experiment with four arms: today's worlds; worlds four times larger; worlds where people slowly gain skill by watching someone better than themselves; and both together. The pattern of which arms stop the decline would answer the question. If none of them do, both suspects fall, and a third rises: that ACL's inventions give no reason to build on them, because fired clay, so far, solves nothing.

**What the evidence said.** E7.6 and E7.7 answered half of the question, and reframed the rest.

Transmission of recipes is not the break. 1,782 recipes spread by teaching. People readily tell each other what they know. What fails to transmit is skill: in the design, crafting skill cannot be taught, cannot be inherited, and cannot be caught by watching. It can only be built by making.

And people stopped making. Deliberate making collapsed forty-fold over a thousand years. Without making, skill decayed by a factor of ten. With decayed skill, made tools became dull and low-valued. With low value and an inventory check that suppresses making what one already holds, people had even less reason to make them. The worlds did not freeze because people forgot recipes; they decayed because nobody's hands were practiced.

Population was not refuted. The long-lived worlds only varied between 36 and 54 people on average, far too narrow a range to test whether a population of one hundred or two hundred could sustain what fifty lose. That question remains alive for E8.

**Correction, added in edition 6.** The paragraph above names "an inventory check that suppresses making what one already holds" as part of why people stopped making. E8 Arm 1 removed that check, and making collapsed just the same. E8.1 then found that making was never competitive with daily life, even for the founders, and E8.2 found why: in this world, tools add almost nothing to how much anyone eats. The paragraph is left as it was written, because it is what the project believed at the time.

## Chapter 72 — Irrational People or an Unrewarding World?

**The question.** When the people of ACL stopped making things, were they failing to see what tools could do for them, or were they right that tools did little?

**The positions.** If tools were powerful and people ignored them, the problem was in their minds: how they value things, plan ahead, or learn from others. If tools were weak, the people were behaving sensibly, and the problem was in the world: nothing they could make solved a problem that mattered. The creator put the question in exactly those terms, and asked for the payoff to be measured directly rather than inferred from what people chose.

**What the evidence says.** E8.2 measured it. Tools added at most two per cent of the food people foraged, in a world where a week of foraging already brought nearly three times what an adult needs. The world side of the argument has the evidence, for now.

**Added after E8.3.** The winter autopsy sharpened the answer. Tools add little food in three seasons of plenty, and in the fourth season, when people die, no one has laid anything by, though the world would let them. The reward for storing is real; it is simply never experienced.

**Added after E8.4.** And the autumn autopsy turned the debate around a second time. Autumn offers enough to see a person through winter, nearly every year, and no one lays it by. Tools pay little because the one use that would pay, holding a winter's food, is never attempted, and it is never attempted because nothing in the people looks ahead. The world is not the whole answer after all. The missing piece is in the mind, but it is a capacity, not a piece of knowledge.

**What it does not settle.** It does not say what to change. Turning up how strongly worth pulls on people's choices would make them craft more, but it would be putting the answer in. The honest change is to the world: whether there are problems that tools would actually solve. Lean seasons where carrying and storing matter. Prey that cannot be caught without a spear. Water too far away to walk to. In other words, it brings back the question that fired clay raised in E6: a thing must solve something before anyone will build on it.

# Part V — The Discoveries

These are ideas the project did not have when it began. Each came from evidence and is stated as strongly as the evidence allows, and no more.

## Chapter 73 — Civilization Is a Chain

The autopsies produced the framework that now organises almost all of ACL's thinking. For a discovery to become part of a culture, it has to pass through six links:

**Opportunity → Interaction → Transformation → Observation → Reuse → Tradition.**

- **Opportunity:** the right things are in the right place at the right time.
- **Interaction:** someone actually does something with them.
- **Transformation:** the world changes something as a result.
- **Observation:** someone notices a consequence that matters to them.
- **Reuse:** they do it again.
- **Tradition:** others learn it, and it outlives them.

A discovery must survive every link. The record shows breaks at every one. Many transformations happened with no one noticing a consequence. Many things noticed were never done again. Many reused techniques died with their only holder. The longest-lived thing in ACL, the fibre carrier held for a thousand years, is the one whose chain is shortest and strongest: easy to stumble on, useful at once, easy to teach, and easy to find again if lost.

Seen this way, civilization looks less like a single event and more like a fragile chain, made over and over, in which every link must hold.

## Chapter 74 — Topology Changes History

Most inventions are multipliers. A sharper blade cuts a little faster. A better carrier carries a little more. Life gets easier, but it does not change shape.

Some inventions change the map. A raft reaches land that could never be reached before. A vessel lets people live where there is no water. These add new connections to the graph of the possible, and every later history runs on the new graph.

The phrase inside the project became: **topology changes history**.

The evidence is still mostly the shape of what did not happen. Once the raft's use could be felt, islands connected: open-water crossings went from almost none in E1 to between 7 and 167 per world in E2. The watertight vessel could have changed the map and never did, because it was never filled. Everything else ACL's people made was a multiplier, and the list of kinds was complete in eleven years. The working idea is that open-ended history needs a steady supply of map-changing inventions, and that a world whose physics offers only multipliers will freeze. It is a hypothesis, not a result.

## Chapter 75 — Why Delayed Utility Is Hard

Many of the most important inventions in human history pay off later and somewhere else. Stored grain feeds you in winter. Carried water saves you in the desert. A sown field feeds you next year.

ACL's people can learn from delays. E6.6 showed it. What they cannot do is begin. A delayed payoff gives nothing to pull on at the moment the first act would have to be chosen. People learn delayed consequences well; they almost never take a first step that pays nothing now.

There is a cost hidden in one of the long-delay channels, and it belongs here. Beliefs about leaving things at places credit everything left at a spot in the past year, whether or not it caused what followed. They learn long delays, but without discrimination. Superstition is built into them on purpose (Law 71).

## Chapter 76 — Why Transmission Alone Is Not Enough

The water vessel in seed 304 was taught by its maker to three people, and passed on to four more, and survived sixty years. Transmission worked.

What was transmitted was a carrier. The vessel's one world-changing property, that it could hold water, was never seen by anyone, so it was never part of what anyone taught. A tradition can only carry what someone has observed.

Transmission multiplies observation. It cannot create it.

## Chapter 77 — Why Opportunity Alone Is Not Enough

E6 was built on the belief that richer opportunities would make richer history. The autopsy counted the opportunities, and the count ended that belief. A watertight vessel at fresh water, 102 weeks, never filled. Raw food at a fire, dozens of adult-weeks in two worlds, never once held in the flame.

An opportunity nobody acts on is invisible. A world can be full of possibilities and still have no history.

## Chapter 78 — Isolation Kills Small Peoples

This was found while looking for something else. A band of five alone on an island almost always dies out. Within a few generations everyone is related, and nobody is left to pair with. Only 17% of bands that never mixed had a living line at year 100.

Every barrier in the physics, a wider channel or a removed jump, is therefore also a decision about who will have descendants. In most of E5's long-lived worlds, everyone alive descended from a single band of five.

## Chapter 79 — Belief Is Not Practice

Several findings warn against treating what people believe, what they do, and what is true as one thing.

- Sowing beliefs outlived sowing. People went on believing in a practice they no longer did, because its payoff to the sower was weak.
- Trust followed food before it followed truth. Only after E2 made claims checkable and records personal did reputation begin to track accuracy.
- Stories outlived their events and drifted. A killing was remembered for 180 years and blamed on the wrong person, and people acted on the wrong name.
- Knowing how to make a thing is not using it. In E1, between 10 and 44 people per world knew how to make something that floats, and between 0 and 3 carried one.

A world where people always believe what is true, always do what they believe, and always value what is useful would be simpler to build and would teach nothing.

## Chapter 80 — The Degenerative Loop

Until E7.6, the project assumed that ACL's worlds reached a plateau: that novelty stopped after year twenty, but that what had been discovered remained part of life.

The audits showed that the plateau was an illusion. The worlds were steadily running down.

To explain the forty-fold collapse of making and the ten-fold collapse of skill, the project formed a working hypothesis. It is an interpretation, not yet an experiment, and E8 is designed to test it.

The hypothesis names a closed feedback loop:

- When an adult holds a tool, the decision rules skip remaking it unless something extra pulls on them, such as an active inquiry or a seasonal belief about a place.
- Adults play only rarely, in about one week in a hundred, when curiosity briefly outweighs hunger and fatigue.
- Because adults rarely play and seldom remake what they already hold, they get few opportunities to practice making.
- As the skilled founders die, later generations make things with less practiced hands.
- Less practiced hands produce duller, less effective tools.
- Less effective tools yield lower utility in foraging, hunting, and cutting.
- By Law 124, experienced utility is what creates subjective value. Lower utility produces lower value.
- Lower value gives even less reason to remake the tool when it eventually wears out.
- With even less making, the next generation practices even less, and skill continues to decay.

If this loop is real, it means culture in ACL did not stall because possibilities were missing. It stalled because what was once known was not practiced enough to survive.

**Added in edition 6.** E8 tested the first link of this loop by freeing people to remake what they held, and found no evidence that it mattered. E8.1 and E8.2 found the loop's real starting point earlier and outside the mind: making was never competitive, because tools add almost nothing to how much anyone eats. The loop of falling skill is real; what starts it is the world's economy.

## Chapter 81 — The Memory Ceiling on Composites

In E7.7, simple things made in play were kept in memory 96% of the time (3,984 kept, 162 forgotten). Composite things were forgotten at the moment they were made 21% of the time (7,982 kept, 2,160 forgotten): a five-fold penalty.

The cause was not in the nature of people or of discovery. It was an accident of code.

Each person remembers at most twelve recipes. When someone discovers a thirteenth, the memory rules prune the recipe with the lowest subjective value. A brand-new recipe starts with value zero, because it has not yet been used.

When several recipes share the lowest value, Python breaks the tie alphabetically by the recipe's signature. Simple tool signatures begin with letters, such as `flint/flint` or `stone/wood`. Composite signatures begin with parentheses, such as `(stone/stone+wood)#fiber`. In ASCII order, the opening parenthesis sorts before any letter.

So when a crafter whose memory is already full invents a composite tool in play, the brand-new invention is tied for lowest value at zero, sorts first alphabetically, and is immediately deleted in the very next line of code. The person tied two things together, held the result, and instantly forgot how they had done it.

This is an accident of tie-breaking, not nature. It belongs to the book's Known Compromises, and E8 is designed to remove it.

## Chapter 82 — A World That Does Not Need Tools

This is stated as narrowly as the evidence allows: in ACL as it is now, measured over 120 years in four worlds, tools barely matter to how people live.

Foraging, the work adults do most, brings in nearly three times what a person needs, and the best tool adds about a fifth to it. The person's own foraging skill matters far more than anything they could make. Hunting, where tools help most, is almost never done. Most made things never repay the food spent making them.

If this holds, much of what the earlier chapters describe follows from it. Skill decays because nobody practises. Nobody practises because making is never worth more than daily life. Teaching recipes does not help, because knowing how was never what was missing. And a thing that solves nothing, like fired clay, is learned and then left alone.

It also suggests why the first decades looked so different. The founders made things in play, out of curiosity, and were rewarded with puzzles and surprises, not with food. When the surprises ran out, so did the making.

None of this has yet been tested by changing the world. It is a measured description of the world as it is, and the starting point for the next experiment.

The creator put it this way, and E8.3 added its last sentence: the surprising discovery was not that the people failed to invent civilization. It was that, in the world they were given, technology had almost nothing to offer them. Food was usually plentiful, water was near, and simple foraging met most needs. When hunger came, in winter, as it did every year, no one had laid anything by.

## Chapter 83 — A Lesson That Undoes Itself

This began as an interpretation of E9.3. At the creator's insistence it was then tested before anything was built on it (E9.4, below), and the test confirmed it.

The planners stored food because they had gone short. Having stored, they did not go short. And the lesson they acted on was learned from going short: in a winter without it, the memory moves toward nothing. So the next autumn there is nothing left to anticipate, nobody lays anything by, and the shortage that taught them comes back. A lesson learned only from suffering is erased by its own success.

If that is right, it explains why no lesson tried in E9 or E10 changed how a people meets winter, however strong it was made. Each person's lesson lasts only as long as their suffering does.

Human societies seem to have answered this with things that outlast experience. A story about a winter no one alive remembers. A custom of filling the store whether or not anyone is hungry. A granary that stays full because emptying it is forbidden. A rule. All of them keep the lesson when the suffering that taught it is gone. ACL's people have stories, but no story of hunger reaches them as a reason to act; they have heaps, but nothing keeps food in them.

That may be the next question. Not how a person learns to prepare, but how a people keeps a lesson that its own success would erase.

**The test (E9.4).** Every adult in four worlds was followed from one autumn to the next. Those who prepared went short far less: six in ten of them had a winter with no hungry week at all, against about three in ten of those who had gone short and did not prepare. After a winter like that, their lesson fell to a quarter of its strength; among those who did not prepare and went short again, it held. And preparing turned out to be a threshold. Almost no one prepared with a lesson weaker than about four tenths; a quarter of those at five tenths or more did. A planner's well-fed winter left their lesson at about an eighth, far below the line. They would not prepare again until hunger built it back up. How far the lesson falls is set by the rule the mind learns by. That it falls at all is because the preparation worked.

**Provisional conclusion, in the creator's words (October 2026).** ACL individuals can learn from winter, but the lesson is not self-sustaining. Successful preparation removes the experience that created the lesson, causing the lesson to fade. No tested individual-learning mechanism has yet produced stable, population-level winter preparation.

What this does and does not rule out should be said precisely. Tested and failed: freeing people to remake what they hold (E8 Arm 1); anticipating a season one has gone short in (E9); the lesson of a lost child, and of a witnessed death (E10). Never tested, only set aside because people almost never chose to make anything: protecting composite recipes from the memory ceiling, apprenticeship, and larger populations. They were moved down the queue, not refuted, and may matter again if a people ever begins to prepare.

The creator also marked the limit of the conclusion itself: it shows that individual learning from experience is not enough. It does not show that stories, or any other form of shared memory, are what is missing. That is the next hypothesis, not a finding.

## Chapter 84 — Reach or Strength

Three experiments, read together, show a pattern. It is stated as a pattern in what was tried, not as a law.

A lesson from one's own hunger (E9), or from losing one's own child (E10), is strong enough to make some people prepare, but it reaches only the few who suffered it, and it fades as soon as preparing works. A lesson from seeing someone starve (E10) or hearing that someone did (E11) reaches far more people, and outlasts any one person's suffering, but it is too faint to carry anyone over the threshold at which people prepare.

In no form tried has a lesson been both widespread and strong. The people who would prepare are not the people who hear; the people who hear are not moved enough to prepare.

Human societies seem to bridge this in ways ACL's people do not have yet: a lesson that grows stronger the more people hold it, a practice copied from those who prepare rather than a warning heard from those who suffered, a custom kept because it is the custom. Which of these, if any, a world like ACL could grow without being told is the question the next experiments will have to ask.

# Part VI — Lives

These are stories from real worlds, told as closely to the record as possible. Every person here lived in a seeded world, and every event is in a replay, a chronicle or an autopsy. Where the record is silent, so is the story.

## Chapter 85 — The Raft

The islands were meant to keep peoples apart. Each founding band started on its own island, and without something that floats, nobody could cross.

So the first question anyone asked of E1 was: when will they invent the raft?

The answer was almost embarrassing. Immediately.

A raft in this world is two pieces of wood tied together. Raw wood floats 0.5. Tie two floating things and you add half the smaller one's float, so two sticks make 0.75, and 0.65 is enough to carry a person. Wood is the commonest thing near any camp. In every E1 world, someone tied two sticks together within the first three years, often within weeks, usually while playing. They had made a boat. Nobody knew.

And then nobody used it.

Of 5,682 crossings between islands in E1, 92% were made with nothing that floats at all. They were made over channels three tiles wide or less, a gap the movement rules had quietly let people jump. Across open water there were three crossings in 1,462 world-years.

Between 10 and 44 people per world knew how to make something that floats. Between 0 and 3 carried one. When the investigation looked for the reason, it found three. Nothing in the world ever judged a thing by how well it floats. People carry their three most valued things, and a raft was valued at about 0.1, as a slightly awkward club. And the rare person who did set out to sea holding one chose a random far shore, and the target changed every week.

The raft was invented and forgotten at the same moment.

E2 changed the world, not the people. The jump was removed: water now blocked walking. Far shores could be seen from the coast. Crossing to new land became the thing that gave a raft its worth, felt the moment it happened, and visible to anyone watching from the shore. A sea trip kept its heading.

Open-water crossings rose from almost none to between 7 and 167 per world.

There was a price, and it took two experiments to see. Removing the jump also stranded many small bands on their islands, and stranded bands die. The change that let rafts matter made the world harsher for anyone who never built one.

The raft story wrote Law 124: uses must be experienced. An invention does not matter when it is made. It matters when someone lives through its use.

## Chapter 86 — Beimak

Beimak was born in seed 302 in the eighth year of the world, to Thikor and Reloulour, both founders. There were older siblings, Baiyugos, born in the world's first years, and Keikenem, and a younger one, Thadim, who in year 13 was not yet three.

The record describes Beimak's temperament in numbers, as it describes everyone's: curious, more than most (0.59); not diligent (0.21); not very sociable (0.16); quick-tempered and anxious, both a little over the middle.

In year 13, Beimak was playing at a fire. The fire was not especially hot; it burned at heat 5. Beimak held a dry lump of clay in it.

The clay set. It came out hard, 65, and tight, 50. It was the first fired clay in the world, and as it turned out, the only fired clay that world would ever make in a thousand years.

Beimak remembered having made it. The record keeps that much: the recipe was learned, as a thing once made. It was valued at nothing. No puzzle formed about it. Beimak never used it, never made it again, and never showed it to anyone.

The probes that replayed this world record what Beimak weighed in the weeks that followed, every fourth week. Two weeks after the firing: rest, gathering stone, playing, or talking with Baiyugos. Beimak talked. Two weeks after that: rest, gathering stone, or playing. Beimak gathered stone.

Nine weeks after the firing, Beimak's mother, Thikor, starved to death.

The next sample of Beimak's choices comes the week after. The options have narrowed to resting, at 0.72, or talking to one of the brothers and sisters, all well below. Beimak rested.

Three weeks after Thikor, Thadim, the youngest, died of thirst, not yet three years old.

Two weeks after that, in the world's 700th week, Beimak starved to death, four years old. In the last sample of Beimak's choices, rest stood at 0.78, with nothing else close.

In five weeks the family had lost a mother and two children. Reloulour, the father, lived on for decades.

Two weeks after that, the world recorded that nobody alive knew how clay could be made hard in a fire. The knowledge had lasted sixteen weeks.

That is the whole history of pottery in seed 302: one child, one lump, sixteen weeks.

**Why it mattered.** Beimak's lump proved that the physics worked: heat did exactly what it was meant to do. It showed how rare the chance was: across the first century of that world, adults stood at a fire holding a dry, fireable shaped piece of clay in only three weeks. And it showed something harder to see in the tables. In ACL, the people most likely to try something new are the ones who play, and the ones who play are children, who are also the ones most likely to die.

## Chapter 87 — Reibik

Reibik was one of the founders of seed 304, already about twenty-six when the world began. Reibik was very sociable (0.83), calm (temper 0.13), not especially bold (0.13) and not especially curious (0.35). Reibik had a partner, Vothi, and over the world's first fourteen years six children: Riyaishin, Mathis, Baigi, Noshe, Shabai and Houhaineil.

In year 12, about thirty-eight years old, Reibik was playing with materials and bound a piece of hide to a piece of bone with fibre. The thing that came out held 53, and its tightness was 60. It could have carried about five weeks of water.

It was the only watertight thing ever made in E6, in any world.

Reibik liked it. The replay keeps every use. Reibik used it as a carrier the very next week, and again, and again. Its worth to Reibik rose with almost every use, slowly: 0.03, 0.06, 0.08, 0.12, 0.15. By the end Reibik had used it 104 times and valued it at about 0.28, more than most things people carried. In year 14 Reibik made a second one.

Reibik taught it. In year 15, Reibik showed Riyaishin. In year 16, Shabai, who was about five, and then Baigi. The children carried the recipe on after their parent. Later, Noshe was the one who taught it: to a ten-year-old named Yaitik in year 36, to Yaitik's child Monos in year 65, and to a half-sibling, Shoutheiveil, in year 70. By then the recipe had changed in the telling. The later learners believed it was tied with hide, not fibre.

The replay recorded something else.

For 102 weeks, Reibik stood within reach of fresh water, holding a vessel that could hold water.

In none of those weeks was filling it among the four things Reibik weighed most. Reibik foraged in 38 of them. Gave food away in 22. Talked in 21. Went to be with people in 20. In the replay's sample of Reibik's very last weeks, every option weighed was a conversation with one of the children.

Why? Filling something with water pulls on a person only as something untried, and that pull grows with how much thirst they have known. Reibik had lived beside water. Reibik had known almost no thirst. The pull was about 0.04. Ordinary choices pull between 0.3 and 1.

The person holding the vessel was never thirsty. The thirsty people had no vessel.

Reibik died of illness in year 17, about forty-four years old. Nobody ever held one of the vessels again. The recipe lived on in Reibik's children and their learners for another fifty-five years. In the world's 3,743rd week, Baigi, Reibik's child, starved to death. The next week, the world recorded that the knowledge was gone.

**Why it mattered.** What spread through seed 304 for sixty years was a carrier. The thing that could have made dry land livable was in people's hands the whole time, and nobody ever saw what it was. Reibik is the clearest single case of the interaction bottleneck, and the reason E7 exists.

// CREATOR'S NOTE (to be written): What was it like to read Reibik's 102 weeks for the first time? What did you realise in that moment about the bottleneck?

## Chapter 88 — The Autopsy

The autopsy deserves its own chapter for how it was done, not only for what it found.

After E6 it would have been easy to guess at the problem and add a fix. The project did something slower. It replayed seeds 302 and 304 from their first week with probes that only read. For every decision it recorded whether there had been an opportunity, whether the step was among the person's top four options, and what they chose. Every time anything was held in a fire was logged. The one rare thing in each world, Beimak's clay and Reibik's vessel, was followed through its whole life.

Before a single number was trusted, the replays were checked against the saved worlds. Both matched exactly at year 100. The probes had changed nothing.

Then each link of the chain was scored, separately for heat and for water. Opportunity: rare for heat, plentiful for water. Interaction: never chosen on purpose for either; the one fired lump came from a child's play. Transformation: worked every time it happened. Observation: weak; the clay was never used, and the vessel was seen only as a carrier. Reuse: none for the clay; plenty for the vessel, as a carrier. Tradition: the clay was lost in sixteen weeks; the vessel was taught to seven people over sixty years, as a carrier.

The autopsy ended with options, not a decision. Mend the chain from the world's side, or from the people's side. It recorded that the creator preferred not to change the people, and left the choice to the creator.

Every fix proposed before the autopsy would have targeted the wrong link.

## Chapter 89 — Two Peoples Who Never Met

In E5, the frozen prediction said there would be no distinct peoples. Seed 301 proved it wrong.

Two islands, 15 to 53 people each, lay side by side for 990 years. In a thousand years not one person on either island formed a relationship of any kind with anyone on the other. They never met.

One island descended entirely from a single founding band of five. The other descended from two bands that had merged before year 100. Their temperaments drifted apart early, to a gap that then held steady for nine centuries, while the traits that differed kept changing. At first the islands differed most in diligence. Centuries later they differed most in anxiety and in care for others.

Their cultures diverged in ways nobody designed. One island held beliefs about practice, about leaving fibre, stone and wood at certain places in certain seasons: the old building practice first seen in E1. The other island held none of these, in any sample, for a thousand years. The other island bound things with hide and worked bone; the first did neither. Their marks shared nothing. Each island had made its own shapes for rabbits, for graves and for water. About half their techniques overlapped.

They were two peoples, with two histories, across a stretch of sea, and neither ever knew the other existed.

**Why it mattered.** It showed that distinct cultures can form and hold for a millennium without being written. It also showed the limit of that result. The prediction about rival identities scored "confirmed", but only because the two peoples never met. Rivalry needs contact. It was not tested, and it was not refuted.

## Chapter 90 — The Killing of Ludol

Seed 104, E1. In year 14, a person named Roukarail attacked a person named Kaileir. It was the first violence anyone in that world had done. The same year was a hungry one; three people starved after a poor growing season.

Six years later, in year 20, Ludol attacked Kaileir. Kaileir fought back and killed Ludol.

The historian, which only watches, wrote down what followed: revenge answered revenge, and a feud began between Kaileir's kin and Ludol's kin.

Then the story began to travel. It went the only way anything goes in ACL: parents telling children by the fire, neighbours passing on news, each person telling it as they remembered it. By year 31, three people said it was Rukeimei who had killed Ludol. By year 100, sixteen living people believed it was Naikoubo. By year 200, fifty-one people believed it was Midigain.

None of them had been there. And the memory itself held. One hundred and eighty years after the killing, 62 people across five generations remembered that Ludol had been killed. It was the longest-lived memory in all of E1. They had simply lost who did it.

**Why it mattered.** It was the first clear evidence that ACL's people could carry history beyond living memory, which is the beginning of what a culture is. And in the same breath it showed that what a people carries is not the same as what happened. A people's past is something they make out of retellings. ACL does not correct them, and should not.

## Chapter 91 — Mouthir and the Duller Flake

Seed 301, under the E7 code. Daiyei was born in the world's first year. At four, playing, Daiyei struck flint against flint and was left with a sharp flake. Over a long life Daiyei's crafting skill rose to 0.82, the hand of a practised maker. Daiyei died of old age in year 62.

The flake did not die with Daiyei. It was taught at least twenty-four times, by several teachers, and it was read from marks on rock by people who had never met the one who made them.

Mouthir was born in year 96, four generations down. Mouthir was caring (0.78) and fairly bold (0.58), and had almost no practice at making anything: a crafting skill of 0.15. In year 115, at about eighteen, Mouthir took flint and struck a flake from a remembered recipe. In the next few years Vetibin, forty-four and curious, did the same, and so did Sosei, a child of eight. Their skills were 0.29 and 0.14. Their flakes came out duller than Daiyei's had been.

The measure that watches for new things saw three people making a kind of flake nobody had deliberately made before, and recorded the first lasting novelty after year 100 in the history of ACL. It was the same flake, made worse.

Mouthir starved in year 130.

**Why it mattered.** It was the most hopeful number E7 produced, and it turned out to be a measure of loss. It is in this book because the project almost believed it.

# Part VII — The Science of Open-Endedness

The method was not designed at the start. It grew out of mistakes, and by version 8 of the World Bible it had been written down as nine rules, M1 to M9. This part explains why each part of it exists.

## Chapter 92 — Why Predictions Are Frozen

Before every experiment, the predictions are written down and frozen. Afterwards each is scored: confirmed, wrong, or unclear. Nothing is edited once the results are in.

The reason is human. After an experiment, every result looks expected. Without a frozen record, the project would remember having predicted whatever happened. The long lists of wrong predictions in Part III are the proof that the rule works; they would not exist without it.

Freezing also forces precision. "Rafts will matter" cannot be scored. "Every surviving world will have at least 20 open-water crossings in 200 years" can. Three surviving E2 worlds had fewer than 20, and the record says so.

With the predictions comes a kill criterion: a result, stated in advance, that would show the idea failed. E2 came within five people of its own. A mechanism survives by evidence, not by enthusiasm.

## Chapter 93 — Why Autopsies Come Before Interventions

When something does not emerge, the temptation is to add it, or to add whatever seems to be missing. ACL has learned to replay the world and find the broken link first.

The cost of skipping that step is in the record. E6 was an intervention made before an autopsy. It assumed the world lacked possibilities, added many, and found that possibilities were not the missing link. E3 was a careful investigation that still leaned on the wrong explanation, because eight worlds were too few, and E4 had to correct it.

An autopsy is cheap compared with an experiment built on the wrong diagnosis.

## Chapter 94 — Why Experiments Need Controls and Many Worlds

One seed shows one history. Histories in ACL diverge from the first week, and a single world can do almost anything. Seed 105 under E2 dwindled away because almost nobody had a mate on their island. Seed 107 alone held 20 of E2's 53 starved infants. Neither says what the E2 code does in general.

So every comparison runs the same seeds under both codes, and a difference has to hold across many worlds. When eight were not enough, E4 ran twenty-four, with a threshold fixed in advance and an interval around the gap. Any change to the code changes the random history of every world, so only patterns across worlds can be trusted.

## Chapter 95 — Why Failures Are Worth More Than Assumptions

Almost everything ACL knows that it did not know at the start came from a failure.

- The unused raft wrote Law 124.
- E2's population drop revealed that isolation kills small peoples.
- The E5 freeze reframed the whole project around open-endedness.
- E6's failure moved the question from possibilities to interaction.
- The E7 audit, a failure caught before it happened, put code-against-specification checks into the method.

An assumption that is never tested teaches nothing. A failure that is honestly recorded teaches something every time it is reread.

## Chapter 96 — Why Measurement Must Not Touch the World

Observers, the historian and every experiment's recorder must never change the world they watch (M4). This is checked, not assumed. Before an experiment's runs, a world is run for twenty years with the recorder and without it, and the two final states must be identical, down to a fingerprint of every value.

A recorder that so much as drew a random number would change the history it was recording. A historian that nudged one decision would make every "first" it wrote down a little less real.

The same principle is why the code is frozen during experiments (M3). In E7, each run records a fingerprint of its code at the start and at the end, and a run whose fingerprint changed is thrown out.

## Chapter 97 — Why the Experimenter Is the Most Likely Cheater

Every time a problem appears in ACL, the easiest solution is to put the answer straight into the simulation. Add a reward for filling vessels. Give people a little knowledge about fire. Let the historian's names leak into the people's minds.

Each shortcut would make the worlds look better and the experiment worthless.

The project's defence is to assume that cheating, when it happens, will come from inside, from the people who most want the experiment to succeed. Hence the banned-word test on the source, the test that the historian changes nothing, the frozen predictions, the kill criteria and the published wrong answers. Hence too the list of known compromises in Part II, including a floating instinct that the project wrote itself and found later.

The challenge was never making civilization happen. It was learning whether it would happen without help.

## Chapter 98 — Rules Bought by Failures

For most of its life ACL ran on eleven rules, set down early: nature programmed and culture written by nobody, predictions frozen before code, pilots first, measurement that never touches the world, failures published as failures, and the creator's signature on every design. In October 2026, in the middle of an investigation into why a third of the control worlds died out, eight more were added. None of them changed what the project was looking for. Each was paid for by something that had gone wrong.

U had been designed around a target the world could not reach: a grassland's year-to-year swing in food, which ACL's land smoothed away whatever the weather did. So the twelfth rule: before designing around a condition, check, read-only, that the world can produce it. U's manipulation check had then been set against what the calibration managed rather than what the science needed, and so it passed when it should have warned. The thirteenth: a manipulation that falls short does not redefine success. L1, U and the fragility study had all been shaken by worlds that shrank or died, so the fourteenth asks every design that reads surviving worlds to say first how many it can expect. D1's confounded reading, and patterns that looked like findings in the fragility study before fresh worlds had been asked, gave the fifteenth: what is found by looking is a hypothesis until it holds on worlds nobody has seen. The sixteenth came from the assistant's own mistakes, a claim widened past its data and, earlier, work reported that had not been done: every number must come from a script in the repository, and no claim may reach beyond what was measured.

The seventeenth looks forward. The fragility study pointed at nature itself, at how far a person can look for a partner, and the easy next step would be to widen that reach until the worlds survived. That would be tuning the world toward the answer, the oldest temptation in the project wearing new clothes. So: nature is anchored to evidence about the real world, fixed before the run, and never tuned toward an outcome. The last two only wrote down what was already done: population beside every measure, verdicts on worlds alive in every arm; and corrections appended, dated and visible, never rewritten.

The creator's view was that good method grows this way. Rules invented in advance guard against imagined errors. These guard against errors that happened.

## Chapter 99 — Relatives and Ancestors

ACL was not built from a reading list. Most of what it found, it found by running worlds and looking. But it is not alone, and several of its discoveries were known, in other forms, long before it began. This chapter places it among its relatives, and says plainly where it rediscovered what others knew. Sources are listed in Appendix C.

**Worlds where life evolves.** The oldest relatives are artificial-life systems in which digital organisms reproduce and mutate, such as Tierra and Avida, which showed that evolution in a computer can produce real novelty. Two recent projects carry this toward societies. JaxLife runs very large populations of agents with deep neural networks on graphics processors, in a world with terrain, weather and robots the agents can program; its authors aim at agents that accumulate open-ended culture and technologies across generations, and report rudimentary communication, agriculture and tool use. Werld, an open-source project, starts thirty agents with small evolving brains on a graph, with no reward of any kind and an energy cost for every neuron, connection and signal, so that complexity must pay for itself.

Both aim where ACL aims. Both get there mainly by evolution: agents whose networks work better leave more offspring, and pass those networks on. In ACL nothing is inherited but the body. Whatever a person comes to know, they learned in their own lifetime and must pass on by being watched, by raising children, or by telling, or it is lost. Human culture grew far faster than human genes changed, which is why ACL chose the harder road. Its price is scale: JaxLife's worlds dwarf ACL's, and the question of what a hundred connected people achieve against thirty is still open here. Two of Werld's ideas, that complexity should cost energy and that hidden senses could be discovered, are recorded for later.

**Worlds run by minds that already know.** SimWorld builds realistic cities for testing agents driven by language models. Generative agents in a small town, and Project Sid's many-agent societies in Minecraft, show such agents forming routines, relationships, roles, rules, and even religions. These are valuable for building and testing agents. They cannot answer ACL's question. A language model trained on human writing already knows what a village, a trade and a law are, and when its agents build one, no one can tell whether civilization emerged or was remembered. This is the trap named in Chapter 102, and the reason for ACL's founding rule.

**Worlds with written rules.** Sugarscape grew trade, migration, inequality and conflict from simple agents on a grid, and showed how much social pattern can come from very little. But its behaviours, trade included, were rules its designers wrote. ACL forbids writing any behaviour it hopes to see.

**Learning agents that learn from each other.** The nearest scientific relatives are not worlds but experiments with learning agents. In 2021, Ndousse and colleagues found that ordinary reinforcement-learning agents placed beside experts mostly did not learn from them; the agents needed a changed environment and an added learning signal before social learning appeared. That is E12's finding in another setting: the planners were seen, and nobody followed. In 2024, Cook and colleagues found that knowledge accumulated across generations of agents when learning from others was balanced with learning alone.

**What the study of human culture already knew.** Researchers of cultural evolution have argued for decades that humans owe their success to cumulative culture: learning from others so that knowledge outgrows any one mind. ACL kept arriving at their ideas from the other side.

- **Small, isolated peoples lose skills.** Henrich's account of Tasmania, cut off by rising seas, argues that a small population can lose techniques because too few people learn them well; studies of Oceanic island tools and of laboratory groups found more complex culture in larger populations. ACL's E4 found isolation behind its missing births, and E7.6 found skill collapsing across generations, in populations of a few dozen.
- **Learning from the successful.** Henrich and Gil-White argued that people learn preferentially from those who visibly do well, and that prestige grows from this. E13 built this kind of learning, chosen by visible success, because a pilot found that the planners were usually the best fed in sight and almost never the most respected.
- **Storing food is not universal among foragers.** Binford distinguished foragers, who move to food, from collectors, who store it, and tied storage to seasonal environments; Testart linked storage to settled life, denser populations and inequality. ACL's people met a seasonal world and, for twelve experiments, did not store.

None of this makes ACL's findings less its own. Its people were never told any of it. But a serious reader will know this work, and the book should say where ACL rediscovered it rather than let the rediscovery look like invention.

**Where ACL stands.** ACL is small and slow beside JaxLife, and plain beside SimWorld. What it offers instead is method: frozen predictions, controls on identical worlds, measurement that never touches the world, leak tests, replication, and failures published as failures. Most open-ended simulations can say what happened. ACL tries to say what caused it.

# Part VIII — The Future

## Chapter 100 — The Road Ahead

In October 2026, in the middle of E13R, the creator said the project felt as if it might lose its way. So the way was written down: nine stages from a world worth living in to a society, where the project stood among them, and how each next step would be decided.

![The ACL roadmap, redrawn after E13R. Teal: done. Coral: now and, beside it, the branch E13R took. Grey: ahead. The three outcomes of E13R were fixed before its result.](../docs/roadmap.png)

The first three stages were behind it. The world existed; culture had appeared in it unscripted; and twelve experiments had mapped where the chain from a possible practice to a kept one broke. The fourth stage, whether a useful practice can pass from one adult to another, was the one in progress, and E13R would decide it.

The most important part of the map is the fork beside that stage. What would follow E13R was written before E13R had a result: a failed safeguard would mean fixing the code and running again, a failure to replicate would mean another route to transmission, and a replication would mean moving on to the next question, whether a practice survives when nobody is left to copy it. Writing the branches first is the same discipline as freezing predictions. It keeps the path from bending to fit whatever comes out.

The roadmap is kept in the repository beside the code, and redrawn after every experiment. The chapters of this book are how the project got here; the roadmap is where it means to go next, and it is allowed to be wrong.

## Chapter 101 — Open Questions

This chapter records questions. It does not answer them.

About civilization:

- Can institutions emerge: rules that outlive the people who follow them?
- Can trade emerge, beyond the give-and-return partnerships already seen?
- Can property emerge, as more than who left food where?
- Can religion emerge?
- Can language emerge, beyond marks that come to go with things?
- Can states emerge?
- Can cities emerge?
- Can technological acceleration emerge, where each invention makes the next more likely?

About ACL's own findings:

- Why does novelty stop? The shallowness of the physics, the smallness of the populations, the absence of any pull toward the unrewarded, or something not yet suspected?
- Will the world performing the first step be enough? E7 suggests not on its own: fire made hundreds of encounters and nothing built on them.
- Are the worlds frozen, or slowly forgetting? Answered by E7.6: they are forgetting. Best skill falls from ~0.9 to ~0.08, deliberate making falls forty-fold, and recipes thin four- to eight-fold.
- When people live with useful things, how often do they learn to make them? Answered by E7.7: many learn the recipe, but few ever make one. 78% of people who knew how to make fired clay never made it deliberately.
- Can the degenerative loop be broken without Lamarckian telepathy? E8 Arm 1 found no evidence that freeing people to practise breaks it on its own.
- Would people make, keep and build on tools if tools solved real problems: lean seasons, prey that needs a spear, water too far to walk to? E8.2 suggests this is the question to test next.
- Why does no one lay food by for winter? E8.4 answered half of it: autumn gives enough to spare, nearly every year, and no one keeps it. What is missing is looking ahead.
- Can people come to anticipate a hunger they have lived through before, without being told that winter comes? E9 built the capacity faithfully and found it faint: it moved the few with a strong lesson, and they stored food, but not enough people to change the world.
- Is a hard season remembered by its average or by its worst? E9.1 suggests the answer decides whether anticipation can matter in ACL.
- Does a carer's store protect their children through winter? E9.2: yes, five-fold. The reward for storing falls on the children, which is why one's own hunger so rarely teaches it.
- Would losing a child to winter teach what one's own hunger cannot? E10: it moves the bereaved a little, and changes nothing about how a people meets winter.
- How does a people keep a lesson that its own success erases? E9.3 and E9.4 show every lesson learned only from suffering fades when the suffering stops.
- Can stories carry a lesson about winter? E11: they carry it to almost everyone, decades long, and too faintly to change what anyone does.
- Can a lesson be both widespread and strong without being told what to do?
- Would a people prepare if they could copy what a visible, respected neighbour does? E12 shows the neighbours were watching; nothing let them follow. E13 let them learn from the visibly well fed, and the signs were the strongest yet, but its own safeguard could not be measured. E13R measured it and answered part of the question: copying passes a foraging habit between adults, from anyone better fed, but not winter preparation, and its autopsy found that more food going into winter did not last to its end. Can anything pass a plan, or make food last? W1 sharpened it: almost no food is held to last, and the stash, the only way a family could hold a winter, is almost never used. Why does no one put food away? S1 mapped the decision: stashing is rarely on offer, often displaced, and usually outscored, mostly by giving. What would open those gates without writing the answer in? G1 found where the given food goes: inside families, above all to siblings, to whoever is hungriest, half of it repaid. Does that sharing carry a people through winter, or only spread the same shortage? P1: it pools risk, but the pool is almost empty when winter comes. What would make a family's pool deeper, without writing the answer in? U1 found where the surplus is lost: people stop gathering at two weeks of food, when their hunger reaches zero, exactly where storing could begin. What should a satisfied person feel? N1 set out thirteen answers and rejected two; the human evidence then showed whole societies of people who, with full foresight, store little because they live by sharing. Is what ACL lacks a capacity, or a way of living together? Under what conditions do delayed-return societies emerge, and does ACL's world contain them? D1: largely not. Food is predictable and keeps as seed, but it is thin and winter is barely lean; sowing pays but feeds others. What would a world that rewards keeping look like, and would it still be ACL's world? D2: sowers learn that sowing works, but its crop is not theirs; what would it take for anything to belong to anyone? N3: real winters stop growth, and people meet them with meat, weight, movement and stores; does ACL's way of life survive a winter with no growth? L1's pilot: fewer of its people survive it, and those who do are fewer; winter growth stabilises ACL's world. Would a real lean season, with the population confound handled, bring delayed return? L1: a steady leaner winter is answered by fewer people, not by storing; would a lean season people cannot adjust to by their numbers be different? H-L5: delayed return answers uncertainty, not average scarcity; and storage, if anything, answers bad years that strike everyone at once, while sharing answers bad years that strike some. ACL's years vary a fifth as much as a real grassland's.
- Can scaffolded apprenticeship allow procedural skill to survive across generations?
- Does removing the composite memory penalty allow multi-stage tools to accumulate?
- What does a connected population of one hundred people achieve compared with thirty?
- Can identity be measured? If a person were copied into another world, the share of their choices that still match the original, measured against how much the original changes over the same years and how much a stranger matches by chance, would turn the oldest question in this book into a number.
- Why were E6's worlds harsher? Four of eight died out, and the cause was never found.
- Would larger, connected populations hold on to more of what they find?
- Can rival identities form when distinct peoples finally meet?
- Is the interaction bottleneck in the world, or in the people?
- And the oldest question, from before the record began: is anyone in there? Can a person born in ACL be someone?

## Chapter 102 — The Minimum Conditions

An idea took shape in October 2026, in conversation rather than in an experiment, and it is recorded here as an idea.

For a while the project seemed impossible, because Earth is impossibly rich, and no simulation will ever have its physics. The answer was that it may not need to. Aeroplanes do not copy birds. They found the principle that makes flight possible, lift, and built that.

ACL may not need Earth. It may need only the minimum conditions that make cumulative culture possible: some world in which things can be combined into things that make other things, problems worth solving, enough people that knowledge outlives any one of them, and minds that can pass on what they learn. If ACL ever shows that a short list like that is enough, civilization would turn out to be a consequence of conditions, not a miracle of one planet.

There is a trap on the way, and it was named at the same time. Better minds are allowed; minds that already know are not. A newborn has human capacities and no human knowledge. A language model trained on human writing has the knowledge. Put it in a world and it may rebuild pottery quickly, but no one could ever tell whether civilization emerged or was remembered.

## Chapter 103 — How This Book Is Kept

This is a living book, meant to be updated after every major experiment, in the same spirit it was written.

After each experiment:

- Add a chapter to Part III: what was hoped, what was predicted, what happened, what surprised, what changed. Copy the scorecard honestly.
- If an argument shaped the experiment, add it to Part IV, with what each side believed before the evidence.
- If a new idea came out of it, add it to Part V, stated no more strongly than the evidence allows.
- If a world produced a life worth telling, add it to Part VI, from the replay and the chronicle, not from imagination.
- If the method changed, say why in Part VII.
- Move questions out of Part VIII only when evidence has answered them, and name the experiment that did.
- Never edit an earlier chapter to make the project look wiser than it was. If a chapter turns out to be wrong, leave it, and add a correction saying when and how it was found to be wrong.

The code shows what ACL is. This book is meant to show how ACL became what it is.

# Appendix A — Timeline

Dates are as recorded in the repository. World Bible versions 1 to 6 are not preserved in the record.

- **Before the record.** The founding question; Bob; the rule that nature is programmed and culture written by nobody; World Bible versions up to 7.1.
- **E0.** A mind before civilization. Ten founders, 500 days. Frozen predictions begin.
- **E1.** The first long histories. Culture appears; the raft is invented and not used; trust follows food; Kaileir kills Ludol.
- **2 October 2026 — E2.** The four changes. Testing, reputation, records and floating work; population falls by 40%.
- **E3.** The missing births. Inconclusive.
- **E4.** Twenty-four worlds. The effect is real; the cause is isolation.
- **E5.** The millennium. Thousand-year traditions; two peoples who never met; the freeze.
- **3 October 2026 — World Bible 8.1.** Laws 121 to 125 written from the first runs; the method set down as M1 to M9.
- **E6.** Richer matter. Bottleneck remains.
- **E6.5, E6.6.** The autopsies. Beimak and Reibik; the interaction bottleneck; delayed learning shown to work.
- **3 October 2026 — E7 designed and frozen.**
- **4 October 2026 — E7 audited, fixed and launched.** Six problems fixed before any world ran.
- **4 October 2026 — E7 results.** Valid. Fire hardens clay hundreds of times; water almost never; bottleneck remains.
- **4 October 2026 — E7.5.** The year-115 novelty is a duller flint flake, made by unskilled people.
- **4 October 2026 — E7.6 and E7.7 frozen and launched.** The memory ceiling and the narrowness of watching found in the code.
- **5 October 2026 — E7.6 and E7.7 results.** Valid. Crafting skill collapses tenfold; deliberate making collapses fortyfold; recipes thin out 4- to 8-fold; watertight vessels never exist; watching produces only 7 copies in 1,770 observations; composite inventions face a 5x memory eviction penalty.
- **5 October 2026 — E8 (The Crucible) designed and frozen.** Testing four orthogonal arms against the degenerative loop: making freedom, scaffolded apprenticeship, composite memory protection, and demographic scale.
- **5 October 2026 — E8 amendment 1.** Review finds an impossible criterion, a confounded arm and a self-contradiction; one arm is to run first.
- **5 October 2026 — E8 Arm 1.** Freeing people to remake what they hold does not free making. No evidence it helps.
- **5 October 2026 — E8.1.** Making was never competitive, even for the founders; by the third generation it is weighed less than one week in a hundred and fifty.
- **5 October 2026 — E8.2.** Tools add at most 2% of food foraged. The world gives almost no reason to make anything.
- **5 October 2026 — E8.3.** 88% of starvation deaths come in winter or early spring; the dead had laid nothing by; not one carried a container.
- **5 October 2026 — E8.4.** Autumn offers a median surplus of 163 beyond its own needs; the median adult enters winter with 13. The world allows preparation; nobody prepares.
- **5 October 2026 — E9.** Anticipation built from experience, at two pre-stated strengths. Leak test passed; central test failed; for the first time, people fill their hands before winter.
- **5–6 October 2026 — E9.1.** The lesson reaches nearly everyone, faintly; only the few who learned it strongly store food.
- **6 October 2026 — E9.2.** A carer's food at the start of winter cuts their children's risk of starving five-fold.
- **6 October 2026 — E10.** The lesson of a lost child and of a witnessed death, at two witness strengths. Leak test passed; the bereaved forage a little more; no one enters winter with more food.
- **6 October 2026 — E9.3.** The first winter planners: ordinary people with a hard lesson; their stores shared and used up; one in 113 plans again.
- **6 October 2026 — E9.4.** The self-erasing lesson measured: preparing is a threshold behaviour, and a successful winter drops the lesson below it.
- **6 October 2026 — E11.** Stories of hunger deaths carry cause and season to forty thousand hearers, and move each of them very little.
- **6 October 2026 — E12.** The planners were visible, generous and respected, and nobody around them changed: no one in ACL can copy what a neighbour does.
- **6 October 2026 — E13.** People learn from the foraging of the visibly well fed. Planners fourfold, repeat planning 6.3% against 0.9%; declared failed by its own rule, because its leak test had no one in it to measure.
- **October 2026 — E13R.** Sixteen new worlds, a sham arm and an instrumented check: the copying acts only through the watcher's habit. Headline failed (5.6% against 4.3%); planners 2.9×, carers +8.3 points; neighbours unchanged, children not saved. Copying passes a foraging habit, learned from anyone better fed, not a plan.
- **October 2026 — E13R autopsy.** Stocked carers still protect children five- to tenfold, but at every level of a carer's food, children in the copying worlds starved more. The copied habit is year-round, not autumn; people go into winter with more food and end it with none. Copying did not help winter.
- **October 2026 — W1, the winter ledger.** The creator changes the roadmap's branch after the autopsy. Winter is lived hand to mouth: gathering in winter covers 102% of winter eating, stock at its start 14%. The median family holds a ninth of its winter; stashes are almost unused. Not keeping food: nobody puts any away.
- **October 2026 — S1.** The decision to stash, mapped. Three gates: rarely eligible (13% of adult-weeks, 2.7% in autumn), often displaced by materials, usually outscored, mostly by giving (39%) and other social actions; foraging wins only 4%. Stashers learn it kept food better than carrying it; the belief spreads; belief is not what is missing.
- **October 2026 — G1.** Who receives the food. 72% of gifts go to family, a third to siblings (in every world); 63% to people with under half a week of food; half is repayment; strangers receive almost nothing. A family's surplus is kept in its members' stomachs and debts, not in a store.
- **October 2026 — P1.** Risk pooling or spreading scarcity. Family food protects the poorest strongly (winter starvation 25 times lower with a well-stocked family); people rarely starve amid plenty; giving does not leave givers hungry. But help follows only one hungry week in ten, families hold a ninth of their winter, and more sharing brings no better winters. A pool with almost nothing in it.
- **October 2026 — U1.** E8.4 revisited. The food is on the land and barely touched; autumn is foraged like any season; the carrying limit is never reached. People stop when fed: foraging falls from 86% of autumn weeks with under half a week of food to 6% with two to four weeks. In the code, hunger reaches zero at two weeks, exactly where stashing becomes possible.
- **October 2026 — N1.** No code, no experiment: thirteen readings of what a satisfied person should feel, judged for nature, culture, scripting, human capacity and leak. A seasonal instinct and food-as-standing rejected; smooth satiety, insecurity learned from experience, the body as a store, and a longer mind stand out. The creator chooses.
- **October 2026 — N1, the evidence.** The human evidence behind four candidates checked against its sources: strong for the body as a store, strong for foresight as a capacity but weak for its use, mixed for learned worry, general for smooth satisfaction. Woodburn's immediate-return societies store little despite full foresight. The least change that answers U1 is smooth satisfaction confined to the pull to gather; changing nothing stays on the table.
- **October 2026 — N2 and D1.** The question reframed (ACL may live as an immediate-return society, not a broken one), then tested on the world itself. Food is predictable and storable as seed but thin, and winter leaves the land seven-eighths as full as autumn. Sowing already returns more than twice its seed, yet half its crop feeds others and sowers mostly come away believing it failed. By the creator's rule, changing people's psychology is premature.
- **October 2026 — D2.** Why sowers seemed to learn failure. They do not: D1's measure counted forgetting as failure (corrected). Sowers learn that sowing works, but the return is not theirs: the sower's family gets back about what it sowed, others harvest more, and autumn sowing is a loss to the family. Sowing explains part of the absence of delayed return; the lean season and property remain open.
- **October 2026 — N3.** Nine readings of a harder lean season, then the evidence: temperate plants are dormant in winter, so zero winter growth is the realistic value; lean seasons vary with climate; foragers meet them with meat, weight loss, movement and storage. The first test chosen: winter growth set to zero, nothing else changed.
- **October 2026 — L1 frozen, and stopped.** The survival pilot's rule was triggered (two of four worlds died out) and the experiment did not run. A declared, survival-only check of the same seeds without the change found one world fragile anyway, one killed by the leaner winter, and every surviving leaner world much smaller. The creator chose to redesign the pilot with same-seed controls.
- **October 2026 — L1 run.** The redesigned pilot passed (the unchanged worlds died out more often than the leaner ones). The experiment ran as frozen: its manipulation check failed, because the leaner worlds ended with far fewer people and so as much winter food each (a design flaw, admitted: food was measured per person, not per tile). By the frozen rule, a null that says nothing about lean seasons. Observed: a steady lean season is absorbed by density, not by storing.
- **October 2026 — H-L5, N4 and V1 (overnight).** The creator's hypothesis that delayed return answers uncertainty, not average scarcity. Candidates for unpredictable winters; evidence that sharing insures only what is not common to the whole group, and that real grassland production varies about a third from year to year against ACL's fourteenth; and a read-only study of ACL's own bad years: deadly, but not teaching storage. A design comparing world-wide with patchy bad years drafted for sign-off.
- **October 2026 — U stopped at the pilot.** Signed off for a grassland target. ACL's land smoothed even the widest weather to about 11% variation in food a year (grassland about 37%); at that width the pilot lost 7 and 6 of 8 worlds against the control's 4, with no seed keeping all three arms alive. Hard stop; no behaviour measured; the design returns to the creator.
- **October 2026 — Rules 12 to 19.** During the fragility study (F1), eight rules added to the eleven, each paid for by a failure: feasibility before design; manipulation checks anchored to the target; baseline survival first; discovery confirmed on a holdout; every number traceable; nature anchored, not tuned; population beside every measure; corrections appended, not rewritten.
- **October 2026 — F1, baseline fragility.** A third of control worlds die out (22 of 64), not from hunger: births stop forty to sixty-five years before the end and the people age out. After the founders people rarely pair, because in a small, scattered people a partner is almost never within sight. Dying worlds can be told apart by their size at year twenty. Read-only; confirmed on 24 new worlds.
- **October 2026 — Stage 0 reopened; N5.** The creator reopens the world's foundation. Evidence: real foragers find spouses in networks of hundreds, outside the local group, mostly through kin; a viable people needs some 75 to 150 members even with perfect search. ACL's whole world held twenty, searching within sight. Nothing changed; a feasibility question set for the creator.
- **October 2026 — F2.** Perfect partner finding, as a diagnostic on the same 64 worlds: 7 died out against 22, verdict "both". Search was most of the problem; the worlds that still died had no eligible partner left anywhere. Once people paired, couples drifted apart and larger peoples met the limit of their food.
- **October 2026 — C1.** Why couples drift apart, read-only and confirmed on new worlds: they are apart about half their weeks; two in five of those weeks sit in a gap between two thresholds written separately in the code; foraging splits them and food outbids the pull back. F2's figure on couples apart corrected.
- **October 2026 — N6.** How real forager couples live together: apart by day, often, but in the same camp at night. At ACL's weekly step a real couple would be together almost every week; ACL's couples share no home. Candidates set out for the creator; none chosen.
- **October 2026 — H1.** How far apart partners' homes lie, read-only: close in only half of couple-weeks, and changing every five or six weeks. Mixed by the frozen rule; a shared home, not only aligned thresholds, is what the evidence points to.
- **October 2026 — T1.** The pull toward a partner moved to where conception stops. The manipulation check failed: the pull was there and food outbid it; the outcome was not read. A slight change flipped the fate of 19 of 64 worlds: differences of a few worlds are noise.
- **October 2026 — HB1.** A shared home base, with a sham arm. Couples were together almost every week and had more children, but extinction rose (33 of 64 against 22; the sham, 24): families ate the land around homes that did not move with the food. (Not confirmed by HF1; see below.)
- **October 2026 — HF1.** The land around HB1's homes measured directly: only about 3% emptier than in the control, on old and new worlds alike. Depletion not confirmed; HB1's hunger has another cause, and the moving home waits.
- **October 2026 — HF2.** The household accounts of HB1's hunger: not too many children, not meat. People gave each other about two fifths less food, seen in the first worlds and again in new ones; consistent, not yet confirmed.
- **October 2026 — HF3.** The lost gifts did not explain HB1's hunger: help was within reach as often as before, and came less often. After three read-only checks, the hunger is real and unexplained by any single cause tested.

# Appendix B — Words Used in This Book

- **Seed:** the number that fixes a world's random history. The same seed and code always give the same world.
- **Tick:** one week of the people's time. Fifty-two make a year.
- **Band:** one of the founding groups of five, each starting on its own island.
- **Kind:** a made thing's lasting properties, each grouped into one of five bands, so near-identical things count as one kind.
- **Novelty:** a kind or behaviour new to the world, made or done by three or more people within ten years of first appearing.
- **Lasting novelty:** a novelty still being made or done fifty or more years after it first appeared.
- **LFA, latest first appearance:** the first year of the latest lasting novelty in a world. A world that keeps producing new things has a late LFA.
- **Tradition:** a technique, belief or mark held by three or more people in every ten-year sample over a long stretch.
- **FEC, first encounter count:** in E7, how often the world itself performs a transformation in front of someone, such as rain filling a vessel or a fire hardening clay.
- **Historian:** the read-only observer that names firsts after they happen. It never influences anyone.
- **Autopsy:** a read-only replay of a finished world, with probes, to find where a chain of discovery broke.
- **Replay:** running a saved world again from its seed, to watch it more closely. A replay is trusted only if it reproduces the saved world exactly.

# Appendix C — Sources

Artificial worlds and agents:

- Lu, C., Beukman, M., Matthews, M. and Foerster, J. (2024). JaxLife: An Open-Ended Agentic Simulator. arXiv:2409.00853. Code: github.com/luchris429/JaxLife.
- Werld: agentic life simulation from inception. Open-source project, github.com/nocodemf/werld.
- Ren, J., Zhuang, Y., Ye, X., Mao, L. and others (2025). SimWorld: An Open-ended Realistic Simulator for Autonomous Agents in Physical and Social Worlds. arXiv:2512.01078.
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R. and others (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv:2304.03442.
- Altera.AL and others (2024). Project Sid: Many-agent simulations toward AI civilization. arXiv:2411.00114.
- Epstein, J. M. and Axtell, R. (1996). Growing Artificial Societies: Social Science from the Bottom Up. MIT Press.
- Ofria, C. and Wilke, C. O. (2004). Avida: A Software Platform for Research in Computational Evolutionary Biology. Artificial Life 10(2).

Learning agents that learn from each other:

- Ndousse, K., Eck, D., Levine, S. and Jaques, N. (2021). Emergent Social Learning via Multi-agent Reinforcement Learning. ICML 2021; arXiv:2010.00581.
- Cook, J., Lu, C., Hughes, E., Leibo, J. Z. and Foerster, J. (2024). Artificial Generational Intelligence: Cultural Accumulation in Reinforcement Learning. arXiv:2406.00392.

Human cultural evolution:

- Henrich, J. and Gil-White, F. J. (2001). The evolution of prestige: freely conferred deference as a mechanism for enhancing the benefits of cultural transmission. Evolution and Human Behavior 22(3).
- Henrich, J. (2004). Demography and Cultural Evolution: How Adaptive Cultural Processes Can Produce Maladaptive Losses. The Tasmanian Case. American Antiquity 69(2).
- Kline, M. A. and Boyd, R. (2010). Population size predicts technological complexity in Oceania. Proceedings of the Royal Society B 277.
- Derex, M., Beugin, M.-P., Godelle, B. and Raymond, M. (2013). Experimental evidence for the influence of group size on cultural complexity. Nature 503.
- Binford, L. R. (1980). Willow Smoke and Dogs' Tails: Hunter-Gatherer Settlement Systems and Archaeological Site Formation. American Antiquity 45(1).
- Testart, A. (1982). The Significance of Food Storage Among Hunter-Gatherers: Residence Patterns, Population Densities, and Social Inequalities. Current Anthropology 23(5).
- Woodburn, J. (1982). Egalitarian societies. Man 17. doi:10.2307/2801707.

Hunger, foresight and the body (checked for N1; abstracts via PubMed where marked):

- Cabanac, M. (1971). Physiological role of pleasure. Science 173(4002): 1103–1107. doi:10.1126/science.173.4002.1103 (PubMed).
- Layard, R., Mayraz, G. and Nickell, S. (2008). The marginal utility of income. Journal of Public Economics. doi:10.1016/j.jpubeco.2008.01.007.
- Malmendier, U. and Nagel, S. (2011). Depression babies: do macroeconomic experiences affect risk taking? Quarterly Journal of Economics 126(1). doi:10.1093/qje/qjq004.
- Nettle, D., Andrews, C. and Bateson, M. (2016). Food insecurity as a driver of obesity in humans: the insurance hypothesis. Behavioral and Brain Sciences 40: e105. doi:10.1017/S0140525X16000947 (PubMed).
- Shah, A. K., Mullainathan, S. and Shafir, E. (2012). Some consequences of having too little. Science 338(6107): 682–685. doi:10.1126/science.1222426 (PubMed).
- Suddendorf, T. and Corballis, M. C. (2007). The evolution of foresight: what is mental time travel, and is it unique to humans? Behavioral and Brain Sciences 30(3): 299–313. doi:10.1017/S0140525X07001975 (PubMed).
- Frederick, S., Loewenstein, G. and O'Donoghue, T. (2002). Time discounting and time preference: a critical review. Journal of Economic Literature 40(2): 351. doi:10.1257/jel.40.2.351.
- Mischel, W., Shoda, Y. and Rodriguez, M. L. (1989). Delay of gratification in children. Science. doi:10.1126/science.2658056.
- Wells, J. C. K. (2006). The evolution of human fatness and susceptibility to obesity: an ethological approach. Biological Reviews 81(2): 183–205. doi:10.1017/S1464793105006974 (PubMed).
- Simondon, K. B. and others (2004). Season of birth is not associated with risk of early adult death in rural Senegal. International Journal of Epidemiology 33(1): 130–136. doi:10.1093/ije/dyg279 (PubMed).
