"""Write investigations.md from the E1 investigation re-runs (inv_seed_<n>.json) and the E1 snapshots.

Read-only. Usage: python experiments/E1/analyse_inv.py
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from itertools import combinations_with_replacement
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent))

from acl import matter  # noqa: E402
from acl.config import WEEKS_PER_YEAR  # noqa: E402
from acl.historian import CLASSES, classify, describe  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402

OUT = HERE / "output"


def _pearson(xs, ys):
    n = len(xs)
    if n < 5:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if not sx or not sy:
        return None
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 3)


def _pct(a, b, digits=0):
    return f"{100 * a / b:.{digits}f}%" if b else "–"


def _load():
    runs = []
    for f in sorted(OUT.glob("inv_seed_*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        w, h = load_snapshot(OUT / f"seed_{r['seed']}_end.json.gz")
        r["_w"], r["_h"] = w, h
        runs.append(r)
    return runs


CAUSE_WORDS = {
    "tested": "a claim they were told was tested by their own experience",
    "hear_story": "a witness heard a wrong version of what they saw",
    "hear_how": "told a way of making something they had found no good",
    "hear_belief": "told a belief their own experience contradicted",
    "react": "hearing or seeing harm done (or food given) by someone",
    "_give": "receiving food",
    "_care": "being looked after",
    "_court": "becoming a couple",
    "_steal": "being stolen from",
    "_take": "finding their stored food taken",
    "_attack": "being attacked",
    "resolve_hunts": "hunting together",
}


def section_a(runs, L):
    w = L.append
    w("## A. Why doesn't accuracy affect trust?")
    w("")
    w("Every change to anyone's trust in anyone, over all 8 histories, recorded with what caused it.")
    w("")
    by = Counter()
    n = Counter()
    signed = Counter()
    for r in runs:
        for y in r["trust_years"]:
            by.update(y["by_cause"])
            n.update(y["n"])
            signed.update(y["signed"])
    total = sum(by.values())
    w("| cause | share of all trust movement | changes | net direction |")
    w("|---|---|---|---|")
    for cause, v in by.most_common():
        w(f"| {CAUSE_WORDS.get(cause, cause)} (`{cause}`) | {_pct(v, total, 1)} | {n[cause]} | "
          f"{'+' if signed[cause] > 0 else '−'}{abs(signed[cause]):.0f} |")
    w("")
    w("(Trust also starts at a set level when people grow up together, are born or are taken in, and fades for "
      "people not seen for a year. Those are not `bump` calls and are not in this table.)")
    w("")
    tests = []
    sources = 0
    per_source = Counter()
    halves_a, halves_b = [], []
    held = failed = 0
    kinds = Counter()
    touched = rel_total = 0
    for r in runs:
        for src, seq in r["tests"].items():
            sources += 1
            tests.append(len(seq))
            held += sum(seq)
            failed += len(seq) - sum(seq)
            per_source[min(len(seq), 10)] += 1
            if len(seq) >= 4:
                h = len(seq) // 2
                halves_a.append(sum(seq[:h]) / h)
                halves_b.append(sum(seq[h:]) / (len(seq) - h))
        kinds.update(r["test_kinds"])
        touched += r["touched_by_test"]
        rel_total += sum(y["relations"] for y in r["trust_years"]) / max(1, len(r["trust_years"]))
    person_years = sum(sum(1 for _ in r["trust_years"]) for r in runs)
    w(f"- **How often a claim gets tested:** {sum(tests)} tests in {person_years} world-years of all 8 histories, "
      f"about {sum(tests) / max(1, person_years):.1f} a year in a whole world.")
    w(f"- **Whose claims get tested:** {sources} different people were ever the source of a tested claim. "
      f"{per_source[1]} were tested once, {sum(v for k, v in per_source.items() if k >= 4)} four or more times.")
    w(f"- **What gets tested:** " + ", ".join(f"{k.replace('|', ' ')} {v}" for k, v in kinds.most_common())
      + " (b: = what to leave where; m: = what a made thing is worth).")
    w(f"- **How often claims hold:** {held} held, {failed} failed ({_pct(held, held + failed)} held).")
    rel = _pearson(halves_a, halves_b)
    w(f"- **Is being right a lasting trait?** For the {len(halves_a)} sources tested 4+ times, accuracy in the "
      f"first half of their tests vs the second half: r = {rel}. Near 0 means being right is luck, not a trait "
      "anyone could learn to trust.")
    w(f"- **How much of the trust web tests ever touch:** over all histories, {touched} listener→source relations "
      f"were ever moved by a test. A world holds about {rel_total / max(1, len(runs)):.0f} living relations at any "
      "moment, so in any year almost every relation has never been touched by a test.")
    w("")


def section_b(runs, L):
    w = L.append
    w("## B. Why does sowing fail?")
    w("")
    w("Every seed put in the ground, every harvest of crop, and, for everyone who believed in sowing that season, "
      "what they did instead.")
    w("")
    w("| seed | sowings | seeds sown | distinct sowers | sown on purpose (belief ≥0.2) | harvests | crop harvested | by someone who sowed that spot | crop per seed sown | summer fields: mean, max | year-end fields (E1 report) |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    bw = Counter()
    decade = Counter()
    for r in runs:
        sow, harv = r["sowings"], r["harvests"]
        seeds = sum(s[4] for s in sow)
        crop = sum(hv[4] for hv in harv)
        by_sower = sum(hv[4] for hv in harv if hv[1] in hv[5])
        purposeful = sum(1 for s in sow if s[6] >= 0.2)
        sf = r["summer_fields"]
        mean_f = sum(x[1] for x in sf) / len(sf) if sf else 0
        ye = [y["fields"] for y in r["_h"].years]
        w(f"| {r['seed']} | {len(sow)} | {seeds:.0f} | {len({s[1] for s in sow})} | {_pct(purposeful, len(sow))} | {len(harv)} | "
          f"{crop:.0f} | {_pct(by_sower, crop)} | {crop / seeds if seeds else 0:.2f} | {mean_f:.1f}, {max((x[1] for x in sf), default=0)} | "
          f"{sum(ye) / len(ye) if ye else 0:.1f} |")
        bw.update(r["believer_weeks"])
        for s in sow:
            decade[s[0] // WEEKS_PER_YEAR // 25 * 25] += 1
    w("")
    w("Sowings per 25 years, all seeds: " + ", ".join(f"yr {k}–{k + 24}: {v}" for k, v in sorted(decade.items())) + ".")
    w("")
    tot = bw["believer-weeks"]
    w(f"**People who believed in sowing that season** ({tot} person-weeks):")
    w(f"- sowing was among their top four choices in {_pct(bw['put seeds was among their top choices'], tot)} of those weeks; "
      f"they actually sowed in {_pct(bw['sowed'], tot)};")
    w(f"- they had under two weeks of food in {_pct(bw['had under 2 weeks of food'], tot)}, and went for food instead "
      f"(forage, hunt, fetch) in {_pct(bw['chose food instead'], tot)}.")
    w("")
    by_season = Counter()
    for r in runs:
        for s in r["sowings"]:
            by_season[("spring", "summer", "autumn", "winter")[s[5]]] += s[4]
    w("Seeds sown by season: " + ", ".join(f"{k} {v:.0f}" for k, v in by_season.most_common()) + ".")
    w("")


def section_c(runs, L):
    w = L.append
    w("## C. Why do rafts appear immediately?")
    w("")
    one = []
    strikable, hard = ("stone", "flint", "bone", "wood"), ("stone", "flint", "bone")

    class _Mid:
        def random(self):
            return 0.5
    for t in strikable:
        for hm in hard:
            it = matter.strike(t, hm, 0.3, _Mid())
            one.append((f"strike {t} with {hm}", classify(it) if it else []))
    for a, b in combinations_with_replacement(matter.MATERIALS, 2):
        for binder in matter.FLEXIBLE:
            one.append((f"tie {a} and {b} with {binder}", classify(matter.bind(matter.raw_props(a), matter.raw_props(b), binder))))
    named = [d for d, cl in one if cl]
    kinds = Counter(c for _, cl in one for c in cl)
    w(f"**The physics, checked without running anything.** There are {len(one)} things a person can do in one step "
      f"with raw materials (12 strikes, 42 ties). {len(named)} of them already make a named kind: "
      + ", ".join(f"{CLASSES[k][0]} ×{v}" for k, v in kinds.most_common()) + ".")
    w("")
    w("A raft is two pieces of wood tied together. Raw wood floats 0.5. Tying two buoyant things gives "
      "`max + 0.5 × min` = 0.75, and 0.65 is enough to carry a person over water. So the very first time anyone "
      "ties two sticks, they have something that can cross the sea. Wood is the commonest material near camps, "
      "fiber the next, and an untried material pulls curious people to pick it up.")
    w("")
    w("| seed | first raft (week) | first carrier | first club | crossings between islands | first crossing (year) | crossings by people born after year 0 | person-weeks at sea |")
    w("|---|---|---|---|---|---|---|---|")
    for r in runs:
        world = r["_w"]
        first = {}
        for sig, rec in world.knowledge.items():
            for c in classify(rec.get("props")):
                if c not in first or rec["first_tick"] < first[c]:
                    first[c] = rec["first_tick"]
        cr = r["crossings"]
        w(f"| {r['seed']} | {first.get('boat', '–')} | {first.get('carrier', '–')} | {first.get('club', '–')} | {len(cr)} | "
          f"{cr[0][0] // WEEKS_PER_YEAR if cr else '–'} | {sum(1 for c in cr if c[5] > 0)} | {r['at_sea_weeks']} |")
    w("")
    floats = [c[4] for r in runs for c in r["crossings"]]
    w(f"All crossings: {len(floats)}; carrying something that floats 0.65+ when they arrived: "
      f"{sum(1 for f in floats if f >= 0.65)}.")
    w("")
    # How wide is the water they crossed? A move is a jump of up to `reach` tiles, and only the landing tile is
    # checked, so a channel narrower than that can be crossed with nothing that floats.
    gaps = Counter()
    kids = no_raft = 0
    narrowest = {}
    for r in runs:
        world = r["_w"]
        comps = world.landmasses()
        c = world.cfg
        gap = {}
        for i in range(len(comps)):
            for j in range(i + 1, len(comps)):
                best = 99
                for (x1, y1) in comps[i]:
                    for (x2, y2) in comps[j]:
                        dx = min(abs(x1 - x2), c.width - abs(x1 - x2))
                        dy = min(abs(y1 - y2), c.height - abs(y1 - y2))
                        best = min(best, max(dx, dy))
                gap[(i, j)] = gap[(j, i)] = best
        narrowest[r["seed"]] = min(gap.values()) if gap else None
        for tick, pid, a, b, fl, gen in r["crossings"]:
            g = gap.get((a, b), 99)
            if fl < 0.65:
                no_raft += 1
                gaps["water ≤ 3 tiles wide" if g <= c.reach else "wider"] += 1
                age = (tick - r["names"][pid][2]) / WEEKS_PER_YEAR
                if age < 12:
                    kids += 1
    w(f"Of the {no_raft} crossings made with nothing that floats: " + ", ".join(f"{k}: {v}" for k, v in gaps.items())
      + f"; {kids} of them by children carried along by a carer.")
    w("Narrowest water between two islands, per seed (tiles): "
      + ", ".join(f"{k}: {v}" for k, v in narrowest.items()) + ". A person can move up to 3 tiles in a week.")
    w("")


TYPE_WORDS = {"tech": "way of making something", "belief": "tested belief about what to leave where",
              "hearsay": "hearsay about what to leave where", "symbol": "mark → thing", "story": "remembered event",
              "dwelling": "dwelling site (heap that keeps cold out)"}


def _story_words(r, eid: str) -> str:
    """What an event was, from the historian's record of the truth (end or year-100 snapshot)."""
    for tag in ("end", "year100"):
        if tag == "end":
            world, h = r["_w"], r["_h"]
        else:
            path = OUT / f"seed_{r['seed']}_year100.json.gz"
            if not path.exists():
                continue
            world, h = load_snapshot(path)
        t = h.truth.get(str(eid))
        if t:
            kind, actor, target = t

            def nm(x):
                if x.startswith("animal:"):
                    return {"animal:wolf": "wolves", "animal:bear": "a bear"}.get(x, x)
                return world.people[x].name if x in world.people else "someone"
            verb = {"killed": "killed", "attacked": "attacked", "stole": "stole from", "mauled": "mauled"}.get(kind)
            if verb:
                return f"{nm(actor)} {verb} {nm(target)}"
            if kind == "died":
                return f"{nm(target)} died"
    return f"event #{eid}"


def section_d(runs, L):
    global r_by_seed
    r_by_seed = {r["seed"]: r for r in runs}
    w = L.append
    w("## D. Which cultural patterns last longest?")
    w("")
    w("A pattern counts in a year if 3 or more living people hold it (a dwelling site counts if it stands). "
      "\"Passed on\" means people of at least two generations held it at once.")
    w("")
    lives = defaultdict(list)
    best = []
    for r in runs:
        years = r["patterns"]
        keys = set()
        for y in years:
            keys.update(y)
        world = r["_w"]
        for key in keys:
            run = cur = 0
            start = cur_start = 0
            span_gen = cur_gen = 0
            peak = 0
            for i, y in enumerate(years):
                v = y.get(key)
                ok = v is not None and (v[0] >= 3 or key.startswith("dwelling:"))
                if ok:
                    if cur == 0:
                        cur_start, cur_gen = i, 0
                    cur += 1
                    cur_gen = max(cur_gen, v[2] - v[1])
                    peak = max(peak, v[0])
                    if cur > run:
                        run, start, span_gen = cur, cur_start, cur_gen
                else:
                    cur = 0
            if run:
                kind = key.split(":")[0]
                lives[kind].append(run)
                best.append((run, r["seed"], key, start, span_gen, peak, world))
    w("| kind of pattern | patterns | median years | 90th percentile | longest | passed on (2+ generations at once) |")
    w("|---|---|---|---|---|---|")
    passed = Counter(b[2].split(":")[0] for b in best if b[4] >= 1)
    for kind in ("tech", "dwelling", "belief", "symbol", "story", "hearsay"):
        v = sorted(lives.get(kind, []))
        if not v:
            continue
        w(f"| {TYPE_WORDS[kind]} | {len(v)} | {v[len(v) // 2]} | {v[int(len(v) * 0.9)]} | {v[-1]} | {passed[kind]} |")
    w("")
    w("The longest-lasting of each kind:")
    w("")
    w("| kind | seed | what | from year | years in a row | most holders | generations at once |")
    w("|---|---|---|---|---|---|---|")
    for kind in ("tech", "belief", "symbol", "story", "dwelling", "hearsay"):
        top = sorted((b for b in best if b[2].split(":")[0] == kind), key=lambda b: (-b[0], -b[5], b[1]))[:4]
        for run, seed, key, start, gens, peak, world in top:
            what = key.split(":", 1)[1]
            if kind == "tech":
                rec = world.knowledge.get(what, {})
                cls = classify(rec.get("props"))
                what = describe(rec["recipe"], world) + (f" ({CLASSES[cls[0]][0]})" if cls else "") if rec else what
            elif kind == "hearsay" and "@" not in what:
                rec = world.knowledge.get(what, {})
                what = ("told that " + describe(rec["recipe"], world) + " is worth doing") if rec else what
            elif kind in ("belief", "hearsay"):
                thing, season = what.split("@")
                season = ("spring", "summer", "autumn", "winter")[int(season)]
                what = (f"strike {thing.replace('/', ' with ')} in {season}" if "/" in thing
                        else f"leave {thing} somewhere in {season}")
            elif kind == "symbol":
                shape, thing = what.rsplit("|", 1)
                what = f"<{shape}> → {thing}"
            elif kind == "story":
                what = _story_words(r_by_seed[seed], what)
            w(f"| {TYPE_WORDS[kind]} | {seed} | {what} | {start} | {run} | {peak} | {gens + 1} |")
    w("")


def main():
    runs = _load()
    L = ["# E1 — Investigations A–D", ""]
    ok = [r["identical_at_100"] for r in runs]
    L.append(f"{len(runs)} histories re-run with read-only recorders. Each re-run's world at year 100 was compared with "
             f"the snapshot E1 saved: identical in {sum(1 for x in ok if x)} of {sum(1 for x in ok if x is not None)} "
             "(seeds that died before year 100 have no snapshot to compare). No features were changed.")
    L.append("")
    section_a(runs, L)
    section_b(runs, L)
    section_c(runs, L)
    section_d(runs, L)
    (HERE / "investigations.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote", HERE / "investigations.md")


if __name__ == "__main__":
    main()
