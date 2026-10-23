# BD2 — Bodies with realistic rot: does the bodies effect hold when the dead rot as fast as real ones? (DRAFT for the creator; nothing built or run)

**Why.** BD1 found that when bodies stay, fewer worlds die out (146 vs 189 of 512) and population is 19% higher, and
an exploratory breakdown put the gain on disgust at rot. The creator adopted bodies into nature (v4, "Go with
bodies"). But in v4 a body rots at the rate ACL uses for stored food (4% a week), so it takes about two years to
become bones; the living meet rotting bodies about 11 weeks per person-year. Real bodies go to bones in weeks to
months in warm weather and far slower in cold. The assistant recommended checking this before adoption; the creator
chose to adopt first. BD2 is that check, now on v4.

## The candidate (one setting, `body_rot`, default 0 = nature v4 exactly)

- **A body's flesh rots by the weather:** weekly loss = a rate that rises with warmth (fast in summer heat, very slow
  in frost) instead of v4's flat 4%. The exact curve is an assumption anchored to forensic decomposition research
  (rate rises with temperature; GPT also pointed to moisture and exposure), set before data and never tuned.
- **Rotten** when a share of the flesh is gone (as v4); the body's food (what the dead carried) keeps v4's rate.
- Everything else as v4 (disgust, sight, eating by choice, tools for kin).

## Design (to be fixed with the creator and GPT)

C (v4) against R (v4 + realistic rot); 512 new paired seeds; zero checks; safety (survival, population); described:
weeks to bones by season, foul person-weeks, meals from bodies; **and the key reading:** does v4's gain over v3 hold?
(Compare with BD1's C on its seeds, labelled, or add a v3 arm: the creator chooses.)

## Decisions for the creator

1. Run BD2 now, or after digging and things on the ground.
2. Add a v3 arm (so the question "is the bodies gain real with realistic rot?" is answered inside one study).
