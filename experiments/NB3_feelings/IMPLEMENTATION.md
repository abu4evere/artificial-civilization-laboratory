# NB3: implementation readings (written before any data)

How `patch_nb3.py`, `brain_nb3.py` and the runners read the points `questions.md` (NB3-frozen) leaves open.

## The code
- `code_nb3` = `code_nb2` + `brain_nb3.py` + switches (`patch_nb3.py`). With `nb3` 0 every new line is skipped, so
  arm n2 run on code_nb3 equals NB2's full arm on code_nb2 (a zero check).
- **When the feelings act:** once a week, in the learning step (`brain_nb.learn`). The week's feeling sum is added to r
  just before NB2's actor-critic learns from it. Nothing forbids any act; only H changes a score directly.
- **Founders** take the start values (E 0.5, G 0.5, L 1.0, A 0.5, C 0.5, H 1.0). **A child** takes them from the same
  parent its network genome came from (NB2's `s`), each plus a normal draw (sd 0.08), kept in 0–2. The draws use the
  same NumPy generator as the genome, after it.

## Each feeling
- **No joy in attacking** (`nb3_no_attack_joy`): the +0.1 per attack and the kill bonus (0.3 temper − 0.2 kindness) are
  not paid. Nothing else in `_attack` changes.
- **Defence:** p attacking q is defence if q attacked p in the last 4 weeks. Each person keeps a list of who attacked
  them and when (older than 4 weeks is pruned). Whether it was defence is read just before the attack changes
  anything.
- **Guilt** (G): an attack one starts, not in defence, +0.3; a kill +1.0 more, ×2 if kin (kinship > 0); a theft that is
  noticed (the victim's relation is bumped), +0.15. Each week r −= G × guilt, then guilt × 0.9.
- **Empathy** (E): over everyone in reach (not oneself), weights 1 for kin or partner, 0.5 for affection > 0.3, else
  0.2. Distress = mean of hunger (0 when holding twice one's need, 1 when holding nothing) and 1 − health/100. The rise is
  this week's distress minus the other's snapshot from the end of last week (each person takes a snapshot at their own
  learning step; old minds have none, so their rise is 0). r −= E × weighted mean of (rise + 0.25 × distress), the
  level term from the scale audit.
- **Love** (L): only when one has living children under 12. "Well" = the share of one's own children under 6 who hold
  at least half their need, have health ≥ 50 and have their caregiver on their tile. Concern = mean distress of one's
  own children under 12. r += L × (well − 0.5 × concern), plus 0.1 L in a week one chose care or give for one's own child.
- **Approval and shame** (A): every relation update by others this week that changes affection or grudge is summed
  (affection − grudge rises) for the person it is about, filed under the world now stepping. r += A × that sum.
  Kept in checkpoints.
- **Curiosity** (C): r += C × 0.1 / (1 + times this action was done in this situation before), never for attack or
  steal. The count is per person, per "situation:action".
- **The inborn reluctance** (H): each attack or steal option's score − H (not scaled by g), except an attack in defence.

## Arms (switches on top of NB2's full brain)
c: v17. n2: NB2 full. f0: nb3 + no attack joy. fH: f0 + H. f: f0 + E, G, L, A, C, H. fmE: f without E. fmH: f without
H. Seeds 25801–25816, 600 years, the long-run workflow with checkpoints.

## Observers
As NB2's, plus the yearly mean of each feeling gene (read-only), and each genome sample also keeps that person's
feeling genes for the garden.
- **The network's share of decisions:** H's penalty is counted with the instincts ("hand"), not the network. Before
  this fix, the smoke runs showed the penalty inflating the network's column in the arms with H.
- **Added to the analysis** (frozen secondaries, descriptive): causes of death by arm, and adults' acts by arm (hunt,
  attack, steal, give, care, take, make; years 100–600).
- These changes were all made before any data. The zero checks were stopped twice and run again after the last one.

## The garden
- `run_nb3_garden.py`: genomes of generations 1 and 18 from each f world, with their feeling genes, as all the
  founders of a fresh world (seeds 25901–25916), all feeling switches on, g held at 0, learning off: arms g1Z, g18Z
  (the frozen "generation 1 against 18"). 60 years.
- **Note:** with learning off, the feelings cannot change choices through r; only H (as inherited) and the inherited
  network act. That is what the frozen garden asks: whether the inherited brain alone, shaped by the feelings over
  generations, can live.
- **Measured:** founders alive after one year (the frozen question "does a feeling brain alone live a year?"), NB2's
  founder-weeks, births, and survival to 16 of children born by year 44.

## Analysis
`analyse_nb3.py` is built from NB2's frozen analysis by `make_analyse_nb3.py` (arms, primary rule, seed 20261113, gene
table). The recompute files come from `recompute/build_nb3_counts.py`; the prompt is `recompute/prompt.txt`.
