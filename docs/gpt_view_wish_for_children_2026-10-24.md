# GPT's view: a wish for children as human nature, and ACL's reproduction chain (24 October 2026)

**Source: GPT (ChatGPT, the creator's account, main ACL chat), asked by the assistant at the creator's request. GPT's
opinion and its reading of sources, in summary; the sources are not yet checked by the assistant; not sign-off.**

**The question.** In ACL nobody wants children or knows pairing causes them: a "wish for a partner" pull (unpartnered
adults under 45), courting that succeeds mostly on existing affection, conception as pure body (4% a week for a
partnered fertile woman within 2 tiles of her partner, 8% if they courted), and love built in only after birth. Is a
"wish for children" missing human nature (allowed under Law 126 if anchored), and how could it be tested honestly?
("We must have children or our people ends" is knowledge, never to be given.)

## GPT's answers

- **ACL's design is defensible as a minimal model, incomplete as human psychology.** Sex, attraction, attachment and
  care are partly separate motives (Fisher; Schaller et al. 2017); reproduction needs no conscious wish for children.
  But a distinct, variable desire for a baby exists in some people (Brase & Brase 2012, "baby fever"; Nelson-Coffey &
  Cavanaugh 2022: parent–child imagery raised it). Twin studies (Kohler, Rodgers & Christensen 1999; Briley, Tropf &
  Mills 2017) show genetic influence on actual fertility, varying with cohort and conditions, not a heritable "wish"
  that could be copied into a number. Infant faces raise caretaking motivation in men and women (Glocker et al. 2009;
  Parsons et al. 2011), though "baby schema" as a universal law is questioned (a 2024 reassessment). Forager care is
  widely shared beyond parents (Agta: Page et al. 2019, 2021). Wanted family size cannot be read from births: Hadza ~6.1
  and Agta 7.7 births per woman are outcomes, not wishes; Tsimane women's ideal (~3.75 near town) varied with
  conditions (McAllister et al. 2012). No sound cross-forager number for an innate wanted family size.
- **Do not add a wish for children to v6 yet.** If anything is added later, in order of support: (1) a variable
  responsiveness to existing infants (attention and care, by nonparents too); (2) a variable partner-maintenance
  motive; (3) a desire for parenthood only once a behavioural route can be specified apart from its effect on births.
- **It must never:** sense low population; contain a target family size; turn affection into conception; make everyone
  want children; make all infants equally attractive; guarantee competent care; teach that courting or closeness
  causes pregnancy; override personality, bonds or bad experience; or reward care without cost.
- **Honest test:** a behavioural-validity study, not an extinction rescue. Primary outcome = the predicted behaviour at
  real opportunities (e.g. care given when meeting a child in need, by familiarity, care trait, hunger); survival and
  births secondary and allowed to go either way; switch-off parity with v6; manipulation and negative controls; the
  strength fixed before data, never tuned on population; replication on new seeds.
- **More important first:** a read-only audit of the whole reproduction funnel (encounter, courting attempts,
  acceptance, staying together, conception, care), especially: what "unrelated" means; the attraction deadlock (courting
  needs affection, but routines rarely build it); and the 2-tile conception radius when partners are often apart. With
  4% a week, a continuously together couple conceives within a year about 88% of the time, so the body is probably not
  the limit.
- **For Bob:** an inhabitant attached to a particular child, or choosing to stay childless, or caring for others'
  children, is a richer sign of an individual than more births.

## The assistant's notes (checked in the code)

- **"Unrelated" in courting** (`acl/world.py` `kinship`): excludes parent/child, siblings and half-siblings,
  grandparents and aunts/uncles; **cousins are allowed**. Not an "any shared ancestor" rule.
- **Much of GPT's funnel audit already exists:** CP1 (where the funnel breaks in extinct 20-founder worlds: encounter),
  PF1/PF2 (courting not tried; food wins), C1, CB1, AP1 (couples apart most fertile weeks; when together, conception
  works as designed), TL1 (ageing out), MB1b (more mixing without easier pairing). A new audit would add care by
  nonparents and the affection deadlock, which have not been measured.

## Follow-up: why reproduction is low (24 October 2026)

**The assistant's quick look (not a frozen study; numbers from a throwaway script):** 4 worlds, v6, 80 founders on
40 × 40, 100 years; 43 in-world-born women who lived through ages 16–45. Births per woman: mean 3.14, median 3, max 8;
distribution 0:15, 1:2, 2:3, 3:2, 4:6, 5:3, 6:3, 7:8, 8:1; children reaching 15: 2.37 per woman (right-censored).
Across fertile woman-weeks: has a partner 55%, partner within 2 tiles 20%. Rules allow a birth about every 2.7 years
for a couple always together.

**GPT's view:** call it a reproductive-*opportunity* bottleneck, not yet a proven bimodal pattern (43 women, 4 worlds,
women not independent; selected on surviving to 45). Mothers average 4.82 births, close to some foragers' completed
family size (Ju/'hoansi 4.7, Hiwi 5.13, Aché 8.15, Agta 7.6; Hadza TFR 6.1; Tsimane ~9); interbirth intervals not yet
measured (foragers ~2.6–4.1 years). **35% childless is a serious warning sign** for a natural-fertility setting (a
Tsimane working paper, to be checked, reports ~3% nulliparity at 45+), but not yet a demonstrated defect. Do not raise
the conception chance and do not add a wish for children to fix it. **New priority order:** (1) explain the 35%
(never paired, paired late, widowed without re-pairing, apart, or eligible but unlucky); (2) the affection deadlock;
(3) care by non-parents; (4) only then any new drive. Suggested read-only measures: age at first encounter/courting/
pairing/birth; partner loss and re-pairing; fully eligible conception weeks per woman, and the chance of zero births
given them (∏(1 − p_t)); eligible men alive/reachable/met/approached by age band; all birth cohorts including women who
die before 45; complete follow-up for child survival; birth intervals for women with 2+ births, split by whether the
previous child survived (the 78-week wait applies only while the youngest lives).
