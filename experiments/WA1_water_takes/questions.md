# WA1 — Water takes things: what is lost at sea, and what comes back? (DRAFT for the creator and GPT; nothing built or run)

**Why (the creator, 23 October 2026):** "objects may go deep inside water ... make these things possible for their
nature". Third in the agreed order (bodies, digging, water). GPT's ideas (`../BD1_bodies_stay/gpt_ideas.md`): an
object in water floats, sinks or stays near the surface by its existing float value; drift only if water already
moves; floating things may be recovered, sunk things are harder to recover; never destroy lost things outright.

## What v3 does now

People cross water on things that float (rafts). In v3, **nothing is ever lost in water**: a person at sea keeps
everything they carry; if their float breaks they are put ashore half drowned (−10 health), still holding all their
things. Things worn out by use simply vanish, wherever the person is.

## The candidate (one setting, `water_takes`, default 0 = nature v3 exactly)

1. **Losing things at sea:** a person whose float breaks at sea (v3's half-drowned case) loses what they cannot keep
   hold of while swimming: each carried thing is lost with a chance (an assumption, for example a half), except what is
   worn.
2. **Floating or sinking:** a lost thing with a float value at or above v3's raft threshold (0.65) **floats**; below,
   it **sinks**.
3. **Floating things drift ashore:** a floating thing comes to rest on the nearest shore of that water after some
   weeks, where anyone can find it on the ground (needs a way to pick things up: the same gap as BD1's tools).
4. **Sunk things stay** on that water tile, out of reach in this version (ACL has no diving), recorded as lost there.
5. **A body lost at sea** (someone who drowns, if drowning ever kills; in v3 it only hurts) follows the same rule:
   bodies float.

## Questions before freezing

- Is the "break at sea" moment the only honest way things enter water, or should a person also be able to drop or
  throw things in (the "put" action on a water edge)?
- How does anyone pick up a thing found on a shore? ACL has no picking-up of tools (BD1 has the same gap). Without
  it, drifted things are lost too, and the study only measures what water takes.
- Wait for BD1 and DG1: a shared "things on the ground" mechanic would serve bodies' tools, pits and drifted things.

## Recommendation (the assistant's)

Build **"things on the ground"** first (a thing can lie on a tile, be seen, and be picked up by anyone, by a v3
action such as "take"). It is the missing piece behind BD1's tools, DG1's hidden stores and WA1's drifted things, and
it is physics, not culture. Then WA1 is small.
