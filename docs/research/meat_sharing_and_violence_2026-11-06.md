# Research note: who keeps a kill, and how violent foragers were (6 November 2026)

For the hand-limits road (`docs/law_limits_audit_2026-11-06.md`, item 4: shared hunt = forced equal split,
`acl/actions.py:179`; items 1-3: attack and theft gates). A source suggests; only a frozen study decides.

## Read

**Gurven, M. (2004). Reciprocal altruism and food sharing decisions among Hiwi and Ache hunter-gatherers.
Behav Ecol Sociobiol 56:366-380. DOI 10.1007/s00265-004-0793-6.** Read: abstract, introduction and model section
(full PDF text extracted; tables not read).
- Large, high-variance items (meat) are shared more widely than small, easy ones.
- Giving is conditional on receiving between pairs of families; larger and low-producing families receive more and give less.
- The model's acquirer decides "how much to keep for oneself (producer advantage) and how many people will receive
  shares of the rest": i.e. the holder decides, sharing is not automatic and not equal.
- Introduction: in some groups producers "are unable to control the distribution of their catch" (demand sharing,
  tolerated scrounging; Hadza, Hawkes et al. 2001, cited, not read).

**Our World in Data, "Ethnographic and archaeological evidence on violent deaths" (archived, 2013).** Read: page
summary via fetch (not the underlying sources). Shares of deaths from violence it lists for foragers: Hiwi 28% of all
deaths precontact (7.2% Hiwi killed by Hiwi); Anbara 4%; Tiwi 5.75%; Murngin 21% of adults; Ayoreo 20%; Casiguran
Agta 12% of adult male deaths. Caveats on the page: wide variation; often cannot tell in-group from out-group killing.

## Search summaries only (not read)
- Hill and Kaplan comment (Ache, Hadza): kill-site disputes "not uncommon"; claims like "Where's mine?"; hunters may
  play no role in the distribution. Record only.
- Fry and Söderberg (2013, Science), 21 mobile forager bands: over half of lethal events by lone individuals; most are
  homicides, few feuds, a minority war. Abstract-level summary only.
- Hawkes (2001), "Is meat the hunter's property?" Title only.

## What it suggests for ACL (not a finding)
- ACL's equal automatic split of a party's meat has no support in what was read: real sharing is a decision (by the
  holder, or pushed by demand), unequal, and tied to past giving. This backs testing "the holder keeps the kill;
  sharing is a choice" (already queued).
- ACL's violent-death share (LH1, v13: 2 killings vs 2,029 starvations, from `WORKLOG.md`/the conflict audit) is far
  below every forager figure listed above (4-28%). Not a target to tune toward; a reference to judge the gates by.
- Side note from the code (`acl/actions.py:181`): each hunter gets `min(share, carry room)`; meat above carry room
  is not given to anyone in this block. Not yet checked whether it is placed elsewhere.

## Added 6 November 18:43 (for council round 70, HK1's design): who owns a kill

**Search summaries only; the papers were not read. Hawkes et al. 2001 is offered only as a file download, so it was
not opened.**
- **Hadza.** Hawkes, O'Connell & Blurton Jones (2001), "Hadza meat sharing", *Evolution and Human Behavior*.
  - The summary says the "hunter does not control" the distribution of a large kill.
  - It says the successful hunter's household kept on average 10% or less of a carcass.
  - It says the sharing "does not fit" simple risk-reduction reciprocity.
- **Ju/'hoansi (!Kung).** From the Marshall ethnography, as summarised in search results (the book was not read).
  - The owner of the arrow that made the kill owns the meat, not necessarily the shooter.
  - That owner decides the first distribution.

**What it suggests for HK1 (not a finding).** "Who holds the kill" varies:
- Among the Hadza, others' demands take most of it.
- Among the Ju/'hoansi, the instrument's owner holds it, and distribution norms follow.

Either way, the meat goes through a person's decision, or through others' demands. It is never an automatic equal
split. ACL has no demand-sharing act (asking, or taking openly while tolerated); theft is gated (item 2 of the
law-limits audit). After HK, holders of a big kill become the natural theft targets of hungry non-kin. That is the
nearest thing ACL has to tolerated scrounging, and the measures should watch it.
