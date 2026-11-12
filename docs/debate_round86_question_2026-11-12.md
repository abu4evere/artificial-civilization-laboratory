# Council round 86: what should ACL's neural brain get next? (question, 12 November 2026)

ACL is an agent-based simulation of hunter-gatherers. Its people have a neural brain: a small feed-forward network
that adds its score to hand-written instinct scores (weighted by an inherited gene g), and learns by actor-critic
from a weekly feeling number. The world (nature v17) is frozen until 7 December; only the brain may change. The aim
is a people that lives without the old hand-written brain, and later more autonomous minds.

## What the last studies found
- **NB2:** without the old brain's thresholds, most worlds died out: violence (the world paid +0.1 per attack),
  starvation, early death.
- **NB3 (feelings):** an inborn reluctance to harm ended the killing; learned feelings (guilt, empathy, love of one's
  child, approval, curiosity) did not. Extinct worlds 5 of 16 (old minds 4), population 0.49 of the old minds'.
  Still "not viable" by the frozen rule.
- **NB3-A (autopsy):** the feeling people starve the same ways as the old minds, 2.4 times as often. They forage and
  eat as well per adult, but have **44% more births per adult**, and give **half as much** outside the household. A
  demographic trap.
- **The garden (NB2, NB3):** the network alone (instinct weight g = 0) dies within a year.
- **Mind Lab's W1b** (a small grid-world detour test): a flat network of this kind could not even learn to walk to
  food it could see, by actor-critic or by imitating a planner. **W1c** (done): a small convolutional network learns
  to navigate (0.73 on simple layouts by imitation in 30,000 episodes; 0.95 in empty rooms from reward alone in
  100,000), but still takes the short way round a barrier only about a third of the time. An egocentric view without
  convolution barely helps. The convolution is the missing part for navigation; looking ahead needs more.

## The question
Which one or two changes should come next for ACL's people, tested as a frozen study against the old minds?
- (a) a feeling that weighs the household's food against another child (before courting or having a child);
- (b) a reason to share beyond the household (reciprocity, remembered gifts);
- (c) a learning signal that counts children's survival rather than births;
- (d) spatial structure in the network (an egocentric map of food and kin, convolution), so it can find food itself;
- (e) something else.

Please answer concisely:
1. Your choice and why.
2. The biggest risk.
3. How to test it (the arms).
4. Your probability that it makes the network-led people viable by the NB3 rule (extinct at most the old minds' + 3,
   population ratio upper bound ≥ 0.80).
