# N8 — Evidence review for P1 (seek the people you know) and P2 (leave when there is no one), and a power calculation

**Chosen by the creator (October 2026).** Questions written before any search or calculation. **No code in ACL, no
experiment, no choice.** Sources marked "abstract read", "summary read", "full text read" or "record only".

## Evidence questions

**P1 (seek the people you know):**
1. Do foragers know **where** the people they know are (other camps, kin, acquaintances), and how do they keep track as
   camps move?
2. Do people **travel to known others** to find or court partners (visiting), and how often?
3. Is remembering where conspecifics are a general capacity (primates, humans), i.e. nature, not culture?

**P2 (leave when there is no one):**
4. When partners are locally scarce, do the unpartnered **leave their group**? At what age, how far, and who (the rarer
   sex, either sex)?
5. Is there any evidence on **how long** people wait before leaving, that could anchor "some weeks" without tuning?

**Both:** 6. Nature or culture: which parts are plausibly species-typical (spatial memory of others; dispersal under
scarcity), which cultural (arranged visits, marriage rules)?

## What would count as an anchor (written before any search)

- **P1** is anchored if sources read show that foragers keep track of where known people are and travel to them, as a
  general pattern, and that remembering where others are is a general capacity.
- **P2** is anchored if sources read show that the unpartnered leave their group when partners are scarce; its timing
  parameter is anchored only if a source gives one; otherwise P2 must be designed with a timing that does not depend on
  a chosen number, or be held.

## Power calculation (method fixed before computing)

Data: the control (F1's 64 replays) and the sham arm (HB1's and MC1's shams: the same code and seeds) already run.
Model: each world i has an extinction probability q_i, drawn from a Beta distribution whose mean is the control's
extinction share and whose spread is set so that two independent histories of the same world disagree as often as the
sham disagrees with the control. A treatment multiplies every q_i by (1 − e). For e equal to F2's effect, half of it,
and a third of it, and for 64, 128, 192 and 256 worlds, simulate 20,000 experiments and report the power: the share in
which the exact two-sided sign test on discordant worlds gives p < 0.05 with fewer extinctions in the treatment.
Script: `power_n8.py`.
