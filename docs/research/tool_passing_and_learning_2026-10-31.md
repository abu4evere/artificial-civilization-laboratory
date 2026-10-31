# Research note: how foragers pass tools and tool-making on (31 October 2026)

**For the open question:** TR1 is running. Its smoke world (one world; not data) hinted that the best tools already in
someone's hands would add about 22% to foraged food, while tools add about 1% today, because few people hold good
ones. **How do real foragers get tools and tool skill into other hands?** These sources suggest; only a frozen study
decides.

## What was read (labels per CLAUDE.md)
1. **Lew-Levy, S., Reckin, R., Lavi, N., Cristóbal-Azkarate, J., Ellis-Davies, K. (2017).** "How do hunter-gatherer
   children learn subsistence skills? A meta-ethnographic review." *Human Nature* 28:367–394. PMC5662667.
   - **Read:** the abstract, the paragraph on transmission by age, and the conclusion; **not** the full tables.
   - 58 publications reviewed.
   - **In infancy, "parents take children on foraging expeditions and give them toy versions of tools"** (digging
     sticks, bows and arrows).
   - **In early and middle childhood,** children learn most subsistence skills in multi-age playgroups, through play,
     observation and participation. "Older children correct the tool manufacture of younger ones" (citing Imamura &
     Akiyama 2016).
   - **In adolescence,** adults (not necessarily parents) directly teach complex skills such as **multicomponent tool
     manufacture** and hunting.
   - **Innovation comes late:** "we do not find truly innovative behaviors emerging until after adolescence".
2. **Earlier today:** Lew-Levy et al. (2022), 54 societies: children readily make their own toys, mostly miniature
   versions of adult tools (`making_time_and_child_objects_2026-10-31.md`).

## Checked in the code after reading (live nature v10)
- **Among the living, a made thing changes hands only by picking it up from the ground** (nature v8, `ground_week`).
  - `_give` passes food and seeds only.
  - The only other transfers are at death: the heir takes everything (`biology.py`), and a partner or grown child at
    the body takes the tools.
  - **No living person can hand a tool to another.**
- **Children under 12 cannot make known things** (noted earlier today). They play, and play is where new kinds turn
  up, the reverse of the forager pattern in which innovation comes after adolescence.

## Bearing on ACL (suggestions, not proposals)
- **If TR1 finds "knowing matters but is unused",** one candidate reason is access: good tools cannot be handed on,
  and children cannot make copies of adult tools.
- **Handing an object to someone is a physical ability,** like giving food, and could be a law. **Whether and when
  people do it is culture,** and must not be written in (the TU1 decision: customs of giving tools are culture).
- **Any such change is a nature change.** It would need evidence, a frozen study and the creator's decision, or the
  safe path in `CLAUDE.md`. **Wait for TR1's result first.**

## Candidate next readings
- Imamura & Akiyama (2016), on children's tool making and teaching (cited in Lew-Levy 2017).
- Dira & Hewlett (2016), on adolescent learning of complex skills (cited in Lew-Levy 2017).
- Lee (1979), ch. 9: the hours on manufacture (still to find).
