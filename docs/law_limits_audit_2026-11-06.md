# Which laws of ACL limit people by hand? A read-only audit of nature v14 (6 November 2026)

Asked by the creator on Telegram, 17:38: "Double check all laws of world again and filter all with other ai modules
make sure we are not limiting like this cuz laws are beginning of world and the rest build above them".
Follows `docs/conflict_audit_2026-11-06.md`, `docs/action_audit_2026-11-02.md`, `docs/affordance_audit_2026-11-02.md`.
Read-only: nothing in nature changed. Code read in this session: `acl/mind.py` (decide, lines 123-576),
`acl/actions.py` (hunt, give, hand, care, talk, imitate, court, steal, attack, flee, join), `acl/biology.py`
(conception 189, death 593), `acl/config.py`.

## The test used
A law is fine if it is physics, body or a general ability (what can be done, and what it costs).
A law is a **hand limit** if it decides *who may want what*: an option is never offered unless a written condition
holds, or the result is fixed instead of following from the situation. Hand limits shape history by hand.

Note on how choice works: `decide` adds options with a score and picks by chance (softmax). An option with a low or
negative score can still be chosen. An option that is **not added** can never be chosen. So the hard limits are the
`if` gates before `add(...)`.

## Hand limits found (social and conflict)
1. **Attack only after a grudge** (`mind.py:487`, grudge > 0.15). A grudge comes only from harm already done. No
   attack from hunger, rivalry, a contested kill, a mate, a place, or fear (no first strike).
2. **Stealing gated** (`mind.py:480-484`): victim holds > 4 food, thief hunger > 0.3, not kin (< 0.5), not partner, not
   a child; fixed penalty `-0.25 - 0.4*fear`. Only food, always half (`actions.py:816`). Tools, materials, made things
   cannot be taken from a person.
3. **Taking another's stash only when hunger > 0.4** (`mind.py:347`), only from the first 4 tiles looked at.
4. **Shared hunt = forced equal split** (`actions.py:179`): everyone on a tile who hunts is one party; meat split
   evenly; hide and bone by coin. Nobody can keep a kill, claim a bigger share, or drive another off.
5. **Pairing is for life** (`biology.py:593`: a pair ends only when one dies). No leaving, no second partner, no
   rivalry for a mate; courting only between two unpaired adults, opposite sex, not kin, at most 15 years apart
   (`mind.py:469-477`); acceptance = a fixed threshold 0.55 then a 60% coin (`actions.py:797`). Children come only
   from partners (`biology.py:189`).
6. **Revenge after theft is automatic** (`actions.py:829-832`): the victim's counter-attack is rolled by formula, not
   chosen by the victim in their own decision.
7. **Care only for kin, partner or affection > 0.3** (`mind.py:452`); never for a stranger.
8. **Flee only from someone distrusted (trust < -0.4) and nearly as strong** (`mind.py:492`); not from a stranger, an
   angry person or a crowd.
9. **No group act except hunting on one tile.** No sides, no defending a place or another person, no joining a fight
   (conflict audit, 6 Nov).
10. **No territory or ownership of places**; nobody can guard a stash or a spring, or keep others away.
11. **No threat or display** short of a blow; no bluff, no warning.

## Hand limits found (mind and learning)
12. **Teaching happens automatically inside talk** (`actions.py:761-765`), to listeners aged 4+; the teacher does not
    choose what or whom (action audit).
13. **Imitation copies all 608 habits at once** toward a respected or happier model (`actions.py:771-780`); no copying
    of one act.
14. **Written rewards** (`actions.py`): giving pays 0.1 + 0.2 kindness + 0.2 kin; care pays by kin; a kill pays
    0.3 temper - 0.2 kindness; pairing +0.5; talk 0.1 + 0.1 sociability. These are inborn likes tied to temperament;
    whether that is nature (an instinct) or a written outcome is a question for the council, not settled here.
15. **Options picked for them** (action audit): forage/hunt look at the tile, home and 6 random tiles; make offers only
    the best recipe; one action a week; reach 3.

## Hand limits found (body and things; already in the 2 Nov audits)
16. 3 made things, 20 materials, containers hold only water or embers, only one item counts per use, exact recipes,
    raw binders only (`docs/affordance_audit_2026-11-02.md`).
17. Age gates: hunt, make, steal, attack, care from 12; court 16-49 (`config.py`, `mind.py:184-186`).

## Reading (the assistant's, not a finding)
Items 1-11 are the clearest outcome-shaped laws: they decide *that* people are peaceful, faithful and fair, instead
of letting peace, faithfulness and fairness be learned or fail. Items 12-15 limit the mind. Items 16-17 are partly
body (children are weaker) and partly hand-written.

A general replacement, for the council: **any person may try any act on any person or thing within reach** (take,
keep, strike, guard, follow, leave a partner), weighed by the same need, temper, ties, fear and learned values; the
results follow from strength, who sees it, and how others respond. One change at a time, each a frozen test in a copy
with a sham, per CLAUDE.md. Real forager rates of violence, theft and pair break-up: not checked here; to research with
sources before any study.

## Council
See `docs/gpt_review_law_limits_2026-11-06.md` (GPT, Gemini, DeepSeek; opinions, not sign-off).
