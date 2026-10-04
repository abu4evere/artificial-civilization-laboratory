# Design: the rules of this world

The simulation has two kinds of rules.

- **Nature** is written by us: what bodies need, how land, materials and fire
  behave, what people feel, and how they remember and learn.
- **Culture** is written by nobody. Tools, dwellings, fire-making, sowing,
  food stores, who shares with whom, who leads, how feuds start and end, and
  which stories survive all come out of people living under nature's rules.

No list of inventions exists anywhere the people's minds can reach. Only the
historian has names, and it uses them only to describe what happened. Nobody
is told that flint makes a blade, that hides keep you warm, or that seeds grow. If they find out,
it is because they tried something and noticed what happened.

Every number below lives in [`acl/config.py`](acl/config.py).

## Time

- 1 tick = 1 week. 52 weeks = 1 year. Four seasons of 13 weeks, starting in spring.
- Life stages: infant (< 1 year), child (< 12), teen (< 16), adult (< 50), elder.

## Land

- 40 × 40 tiles of islands in a sea (see `geo.py`). The map wraps. Each band
  of founders starts on its own island, near fresh water if the island has
  any, and cannot reach the others without something that floats.
- Kinds of land: deep sea, sea, lake, beach, plains, forest, woods, hills,
  mountain, snow, desert, tundra and river. Each has its own fertility, wood,
  stone, animals and cost to cross. Nobody can walk on sea or lake water;
  rivers can be waded. The north and high ground are colder.
- Rivers run downhill from wet high ground. Every island big enough to live on
  has at least one stream or spring-fed pond.
- Plants grow back fast in spring and barely at all in winter, and some rot over
  winter. Each year has random growing conditions, and a dry year grows less.

## Animals (`fauna.py`)

- Rabbits, deer, bison, wolves, bears and fish live in groups. Each species
  has one fixed set of instincts, the same for every animal of that kind: eat,
  run from what hunts you, hunt what you can catch, breed in the warm seasons,
  survive the winter. That makes a food chain: plants feed grazers, grazers
  feed wolves, bears and people, and fish feed bears and people.
- Starving wolves may go for a lone person, but never near fire or two adults.
  Bears attack when surprised. Bison and deer can hurt hunters.
- Being hurt by an animal, seeing it, or being told of it teaches fear of that
  kind of animal. Fear then holds people back from hunting where those animals
  are.

## Water and weather (`weather.py`; Rules 8, 10, 14)

- Every year is wetter or drier and its winter milder or harder. Every week it
  rains or not. Storms cross part of the land in summer and autumn: they put
  out fires, tear at heaps, spoil uncovered food, wash away ground marks, and
  hurt and frighten whoever is caught outside. In a wet spring the rivers may
  flood once: crops, seed and stores on the banks are washed away, and silt
  makes the ground more fertile.
- Cold depends on the place, the season and the year, not only on winter.
- Bodies need fresh water. Water in sight (within 4 tiles) is walked to every
  day, at an energy cost beyond 2 tiles; something that holds water saves some
  of the walking. After rain there are pools for a week (less in desert).
  Otherwise a week without water costs 20 health.
- Sea water is salty. Nobody knows that. Whoever drinks it gets no relief, may
  fall ill, and expects less of it next time.
- None of this aims at anyone.
- **Seeds.** Part of every plant harvest is seed, mostly in autumn. Seeds are
  edible and keep far longer than other food. Seed left on open ground sprouts
  in spring and summer and grows up to five times its weight in food, depending
  on how fertile the ground is. Outside the growing season, animals dig some of
  it up.
- **Fire.** Lightning sometimes starts fires on wooded land in summer and
  autumn. A fire burns one unit of fuel a week and goes out when the fuel runs
  out; wood set on a burning fire feeds it. Flint struck against something hard
  throws sparks, which can catch on dry fiber or wood lying on the ground.
- On the tile where a fire burns:
  - It keeps off 60% of the winter cold.
  - Food eaten there goes 15% further, because it is cooked.
  - Illness is less likely.
  - Loose food rots at a quarter of the usual speed, because of the smoke.

## Materials and things

Six raw materials have five physical properties each:

| | edge | reach | hard | contain | warm |
|---|---|---|---|---|---|
| stone | .10 | .10 | .80 | 0 | 0 |
| flint | .25 | .10 | .70 | 0 | 0 |
| bone | .20 | .30 | .50 | 0 | 0 |
| wood | .05 | .60 | .35 | 0 | 0 |
| fiber | 0 | .10 | 0 | .25 | .15 |
| hide | 0 | .10 | 0 | .30 | .45 |

Stone, flint, wood and fiber are picked up from the land. Hide and bone come
from animals people hunt.

Two physical acts change materials:

- **Striking** one material with another. Brittle things struck with something
  at least as hard flake to an edge. Flint flakes sharpest, then bone, then stone.
- **Tying** two things together with fiber or hide:
  - Reach adds up.
  - The sharpest edge and the hardest body carry over.
  - Flexible things joined to flexible things hold and wrap better, though
    each extra layer adds less.

What a thing does follows only from its properties:

| Use | Helped by |
|---|---|
| foraging | edge, and the ability to hold things |
| hunting | edge × reach, and hardness × reach |
| cutting wood | edge × hardness |
| fighting | edge × reach, and hardness × reach |
| carrying more food | containing |
| winter cold | warmth, when worn |

Things wear out with use. Each person can carry 3 made things, 20 units of
material and 100 units of food (more with something that holds).

## Things left on the ground

Anything can be put down on a tile:

- **Seed** goes into the ground, unless the tile is covered, in which case it
  stays dry with the food.
- **Food** stays where it was left, marked as whose it is. It rots, but more
  slowly under cover or near a fire.
- **Wood** goes onto a fire if one is burning. Otherwise it joins the heap
  there, like any other material.
- **A heap** shelters people from the wind according to its shape:
  - Long and heavy things make walls (wood, stone, bone).
  - Flat flexible things make a roof (hides, fiber).
  - Its warmth is walls × roof, so it needs both.
  - It has room for 2 to 10 people. The people who put the most into it get
    the places first, then everyone else in a fixed order.
  - Fiber and hide rot slowly, and wood more slowly still.

Anyone can take food from anywhere. If the person who left it is nearby, they
probably notice. That counts as theft and is remembered and resented like any
other.

## Bodies

- Food needed per week: infants 2, children 4, teens 6, adults 7, elders 6,
  pregnancy +1.5. People eat loose food first, then seeds.
- Missing a week's food costs up to 14 health. A fed week restores 1.5.
- A hard-winter week fully exposed costs 1.2 health (more in the far north),
  doubled for infants and elders. Heaps, fires and anything warm being worn
  each keep some of it off.
- A week without water costs 20 health (see Water and weather).
- Illness strikes at random, more often for the hungry, the very young, the old
  and the crowded. Being cared for speeds recovery.
- Ageing: the weekly death risk doubles about every 8 years.
- Every action costs energy; rest and food restore it.

## Reproduction and inheritance

- Couples whose camps are within 2 tiles of each other can conceive (women
  aged 16–45, healthy, not starving, not still nursing). Pregnancy lasts
  39 weeks, and 1% of births kill the mother.
- A child's **temperament** is the average of the parents' plus random drift.
  The traits are curiosity, diligence, sociability, kindness, temper, anxiety,
  care and boldness. This is the only biological inheritance.
- A child's **habits** start as a softened copy of the parents' and keep moving
  toward whoever raises them.
- **Know-how, beliefs and memories are not inherited.** Children have to be
  taught, shown and told.
- When someone dies, a partner or grown child on the same tile inherits what
  they carried. Otherwise it is left on the ground where they died.
- Orphans go to the other parent, then grown siblings, then grandparents. If
  none of them can take the child, a kind adult nearby may.

## Feelings (built in)

| Feeling | Rises when | Fades |
|---|---|---|
| Happiness (mood) | fed, healthy, warm, not lonely, family doing well | moves toward that each week |
| Loneliness | a week without contact | contact clears it |
| Anger | being hurt, or a loved one being hurt | fast; slower for hot-tempered people |
| Fear | violence nearby, a threatening person | fast; slower for anxious people |
| Grief | a loved one dies | slow (half-life about a year) |
| Grudge (toward one person) | they harmed you or someone you love | very slow; slower for hot-tempered people |

Parents feel built-in love for a newborn, scaled by their **care** trait, and
feed their young before themselves as far as that trait takes them.

## The actions (everything a body can do)

| Action | What it does |
|---|---|
| rest | recovers energy and a little health |
| forage | takes plant food (and seed) from a tile |
| hunt | goes after animals; several hunters together succeed far more often, and share meat, hides and bones |
| gather | picks up stone, flint, wood or fiber |
| play | strikes or ties together whatever is in hand, just to see; children do it most |
| make | does again something that was made before |
| put | sets food, seed or a material down here |
| take | picks up food left here |
| explore | travels somewhere new |
| give | hands food to someone |
| care | looks after someone sick, hurt or very young |
| talk | company; each tells the other a story as they now remember it, and the teller may show a skill or pass on a belief. The listener decides what to take (see Information) |
| court | woos someone or keeps a bond warm |
| steal | takes food from someone |
| attack | fights someone, and can kill |
| flee | runs from someone feared |
| join | heads toward family, friends, home, a possible partner, water they know of, or a fire they can see when it is cold |

## How a person decides

```
score = instinct(option, body, feelings, temperament, situation)
      + 0.6 × habit[situation][action]
      + what they have learned the option is worth
```

- **Instinct** is human nature:
  - hunger pulls toward food, fatigue toward rest, cold toward fire;
  - loneliness pulls toward company, love toward caring and giving;
  - a grudge plus temper plus boldness pulls toward attack, fear toward flight;
  - curiosity pulls toward picking up and fiddling with things, especially
    things never handled before;
  - the urge to find a partner pulls toward courting.
- **Habit** is a learned table with 32 situations: food on hand (4 levels) ×
  alone or with others × season. It learns from how each action turned out,
  looking a few weeks ahead (temporal-difference learning).
- **Learned worth** is what the next section describes.

The choice is a softmax draw, so two people with the same temperament still
live different lives.

## What people work out for themselves

- **What things are worth.** When someone uses a thing, they feel how much
  easier it made the job, and come to value that kind of thing accordingly.
  Valued things get made again.
- **How to make things.** Whatever someone makes, they remember how. If the
  thing proves useless, they forget.
- **What to leave where, and when.** People remember what they set down and
  where, and what they saw others set down. They link it to what happens there
  afterwards, separately for each season:
  - a spot that now stands out from the land around it more than it did
    (seasons affect every tile alike, so they cancel out);
  - a winter week there that was warmer than they have come to expect;
  - food left there that kept better than food carried around.

  This is how burying seed in spring, heaping wood and hides in autumn, or
  striking flint at home in winter can come to seem worth doing. It is also
  how superstitions form: a stone left where the harvest happened to be good
  gets some of the credit.
- **Places.** People remember how good life has been at each place, and are
  drawn back to the best one. That is the only "home" there is.

All of this passes on by talking, teaching (parents most), watching someone
use a thing, and seeing someone put something down. All of it dies with the
person unless passed on. When nobody alive knows how to make a kind of thing
any more, it is lost until someone works it out again.

## Memory

- Each person holds up to 60 memories of things seen, done, suffered or told,
  each with a salience and a strength that fades. A brother's murder is
  remembered for life; a minor gift is forgotten within a year.
- Talking passes on a story that matters to the teller. The teller cannot
  know what the listener already knows. The story is retold from memory, so
  it can change (see Information). Retelling keeps a story alive.

## Attention (`thought.py`)

- Each week many things pull at a person's mind: hunger, thirst, cold,
  tiredness, illness, grief, a memory that will not let go, a grudge, a fear,
  dread of an animal, love, missing someone, worry for a child, curiosity, the
  wish to make something again, a puzzle, the wish for a partner, loneliness.
  Each pull's strength comes from their body, feelings, history and temperament.
- The strongest wins their attention, and that makes related choices more
  attractive. Whatever held them last week holds a little harder: diligence
  keeps a task, anxiety keeps a worry.
- Three weeks on the same goal is **focus**: skills grow faster and they feel
  steadier. Three weeks on the same pain is **overthinking**: they work worse,
  feel worse, and the painful memory stays sharp. Nobody is told to be focused
  or anxious; those are only our names for what happens.

## Information: telling and believing (`information.py`; Laws 51, 77, 80, 91)

- **Telling is never exact.** A story is retold from memory: a faded memory
  gets filled in (the wrong person blamed, most likely someone the teller
  already dislikes), the place shifts, and it grows worse in the telling. A way
  of making something can come across with a step wrong; showing it with the
  things in hand, and skill on both sides, make that less likely. A belief can
  slip a season or a thing. Working something out by watching goes wrong more
  often than being shown.
- **The listener decides.** Nothing a speaker does writes into a listener's
  mind. The listener weighs trust and respect for the speaker, how the speaker
  visibly is (healthy, fed, holding the thing they describe), whether it fits
  what they saw themselves, how many others said the same, how much attention
  they have to spare (overthinking leaves less), and their fear (stories of
  harm are believed more by the frightened). Children believe grown-ups more.
  A witness rejects a wrong version and trusts the teller less. Of two heard
  versions, the more believed source wins.
- **Heard is not known** (Law 61). What a listener accepts stays hearsay until
  their own experience tests it. It still steers them meanwhile, which is how
  practices and superstitions spread. When it is tested, the listener's trust
  in whoever told them rises if it held and falls further if it did not
  (Law 66). Untested hearsay slowly stops seeming true.

## Surprise and testing (`inquiry.py`; Laws 63-66)

- People expect things: what a thing they made will do, how a spot where they
  left something will turn out, what striking one stone on another does. When
  the world answers very differently, the gap becomes a **puzzle**.
- A puzzle pulls at their attention (curious people more, hungry people less)
  and draws them back to the same thing: make it again, leave the same thing in
  the same season, gather what trying again needs, and fiddle with similar
  things. Each try is a test. A test that comes out as expected settles the
  puzzle; another surprise keeps it alive. A result that contradicts what they
  expected moves their judgement twice as much as one that confirms it.
- Sparks and fire are surprises too: the first sparks from struck flint, and the
  first time they catch, become puzzles about striking those two things.

## Marks (`marks.py`; Laws 22, 23)

- While fiddling with something hard, a person may scratch three strokes into
  rock, wood or bare ground, as deep as the tool and the surface allow. Ground
  marks wash out in weeks, wood marks in years, rock marks last generations.
- A mark means nothing. Hands draw something new, or copy a shape they have
  seen (with slips, so shapes change over generations), pulled toward shapes
  they already link with what is here and on their mind.
- People link each shape they see with whatever is around it: food set down,
  fire, water, a shelter, a grave, animals, the person they saw make it. They
  also keep a sense of how often each of those is around wherever they stop. A
  shape only tells them something when it goes with a thing more often than
  that thing is around anyway. Then meeting the shape where the thing is absent
  makes them half expect it (a warning, a place to look for water, a good spot).
- The historian calls a shape a shared symbol only when it has been made in
  more than one place and at least three living people have taken it to go
  with the same thing for two years running. It may never happen.

## Revenge

1. A harms B. Witnesses within 4 tiles may see it.
2. Everyone who loves B (partner, family or friend), on seeing or hearing of it,
   gains a grudge against A. The grudge is scaled by love and temper. They also
   grow angry, and grieve if B died.
3. Grudge, temper and boldness, set against kindness, fear and liking, make
   attacking A attractive. Acting on it satisfies the grudge.
4. A's family then holds a grudge back. When revenge answers revenge, the
   historian calls it a feud.

## The historian (read-only)

It reads each week's events and looks at the whole world once a year:

- **Inventions, judged only by properties:**
  - blade: edge ≥ .55;
  - spear: edge ≥ .5 and reach ≥ .6;
  - club: hard ≥ .6 and reach ≥ .55;
  - carrier: contain ≥ .6;
  - wrap: warm ≥ .6.

  It also records lost skills and rediscoveries.
- **Firsts:**
  - fire made by people;
  - a kept fire;
  - a dwelling (a heap keeping out ≥ 20% of the cold);
  - a harvest from seed left in the ground, at first by accident;
  - food left four or more weeks and fetched back;
  - farming: seed buried on purpose by someone who has come to believe in it;
  - keeping stores: food set aside on purpose for the same reason;
  - a theft from a store.
- **Social patterns:**
  - bands, recorded once they last two years, and their leaders;
  - exchange partnerships between unrelated people;
  - revenge and feuds;
  - settlements (a dwelling with four or more people around it);
  - famines;
  - which killings the living still remember.
- **Era summaries** every 25 years.

A test checks that running with or without the historian gives an identical world.

## What the historian checks against the truth

- It keeps what really happened for every remembered harm, death and attack,
  and each year counts how many stories people hold, how many are wrong, and
  how far they travelled. When three or more living people share a false
  version, it writes the myth down next to what really happened.
- It counts claims that turned out right or wrong, puzzles, and tests, and
  notes the first person to test the same thing three times.

## Determinism

- One seeded `random.Random` owned by the world. Its state is saved in every snapshot.
- IDs come from counters. People act in a seeded shuffled order each week.
- No iteration over sets.
- Snapshots keep dictionary order, because the order people consider their
  recipes and beliefs in is part of the state.
- The state hash and an event hash chain must match:
  - between two runs with the same seed;
  - between a straight run and one resumed from a snapshot.
