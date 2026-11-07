# EG1 results (from output)

Worlds: 32 (seeds 24701-24732); fingerprints: ['7334081948f01355da4c618b411157a7f05adbed502f7b41f1f9ba5cbea1262c']; extinct: 0
Hook check over all logged person-weeks (40327088): mismatches 0 ({'weeks': 40327088, 'forage_mismatch': 0, 'hunt_mismatch': 0, 'energy_mismatch': 0}) -> OK

## Primary
P = blocked-by-energy-alone starving person-weeks / all starving person-weeks = 37276 / 593814 = 0.0628  [95% 0.0540, 0.0713]
**Reading: a minor contributor**

## Secondaries
1. Starving person-weeks split (a offered and chosen, b offered not chosen, c blocked by energy alone, d no food feasible):
   a: 0.8794 [0.8676, 0.8912]
   b: 0.0578 [0.0525, 0.0644]
   c: 0.0628 [0.0540, 0.0713]
   d: 0.0001 [0.0000, 0.0001]
2. By age band and sex, starving weeks: weeks; a, b, c, d shares
   6-11 F: 858 weeks; a 0.988, b 0.008, c 0.000, d 0.003
   6-11 M: 969 weeks; a 0.988, b 0.008, c 0.003, d 0.001
   12-15 F: 22856 weeks; a 0.887, b 0.063, c 0.050, d 0.000
   12-15 M: 23472 weeks; a 0.889, b 0.062, c 0.049, d 0.000
   16-29 F: 101367 weeks; a 0.869, b 0.055, c 0.076, d 0.000
   16-29 M: 96570 weeks; a 0.881, b 0.063, c 0.056, d 0.000
   30-49 F: 106476 weeks; a 0.834, b 0.047, c 0.119, d 0.000
   30-49 M: 115378 weeks; a 0.884, b 0.062, c 0.054, d 0.000
   50+ F: 48003 weeks; a 0.917, b 0.060, c 0.022, d 0.000
   50+ M: 77865 weeks; a 0.917, b 0.060, c 0.023, d 0.000
3. Non-starving person-weeks blocked by energy alone: 0.0065 [0.0057, 0.0073] of 21398700 weeks
4. Blocked starving weeks where a tile looked at had food and was affordable (the best-tile quirk): 0.4289 [0.4201, 0.4367]; where even one's own tile (25) was unaffordable: 0.5458
4. Blocked non-starving weeks where a tile looked at had food and was affordable (the best-tile quirk): 0.9255 [0.9222, 0.9287]; where even one's own tile (25) was unaffordable: 0.0023
5. Chosen in blocked starving weeks (37276): rest 0.655, put 0.171, join 0.088, talk 0.029, care 0.025, gather 0.012, take 0.006, steal 0.006, give 0.004, play 0.002, make 0.001, court 0.001
6. Runs of consecutive blocked starving weeks: 27980 runs; mean length 1.335; share of 2+ weeks 0.2767; longest 7
7. Starvation deaths at 6+: 1519; with a blocked starving week in their last 4 decisions: 532 = 0.3502 [0.3024, 0.3959] (with any logged decision in that span: 1516); all deaths at 6+ by cause: {'old age': 4669, 'thirst': 1094, 'starvation': 1519, 'illness': 1867, 'childbirth': 101, 'killed': 1}
8. Rest weeks of the grown (16+, all weeks): 143879; food blocked by energy alone 0.3283; food offered and rest chosen 0.6716; no food feasible 0.0001
9. Mean energy at decision, starving weeks: 77.52 (593814 weeks)
9. Mean energy at decision, non-starving weeks: 86.38 (21398700 weeks)
