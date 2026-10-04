"""Turn E1 output into summary.md: tables at year 100 and year 200, and each frozen
prediction scored against the numbers. Read-only."""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

CLASSES = ("blade", "spear", "club", "carrier", "wrap", "boat")


def _load(out: Path) -> list:
    runs = []
    for f in sorted(out.glob("seed_*.json")):
        if f.name.count("_") == 1:
            runs.append(json.loads(f.read_text(encoding="utf-8")))
    return runs


def _row(run, year):
    """The measurements for the year ending at `year` (100 -> the 100th year), or None."""
    rows = run["rows"]
    return rows[year - 1] if len(rows) >= year else None


def _pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "–"


def _pearson(pairs):
    n = len(pairs)
    if n < 5:
        return None, n
    xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if not sx or not sy:
        return None, n
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 3), n


def _years(run) -> list:
    """The years to report for a run: 100 and 200, or its last year if it ended sooner."""
    rows = run["rows"]
    ys = [y for y in (100, 200) if len(rows) >= y and rows[y - 1]["population"] > 0]
    last = max((i + 1 for i, x in enumerate(rows) if x["population"] > 0), default=0)
    if last and last < 200 and last not in ys:
        ys.append(last)
    return ys


def _first_years(run) -> dict:
    out = {}
    for c in run["chronicle"]:
        if c["kind"] != "invention" or "again" in c["text"]:
            continue
        for cls, word in (("spear", "spear"), ("blade", "blade"), ("club", "club"), ("carrier", "carrier"),
                          ("wrap", "wrap"), ("boat", "raft")):
            if f"the first {word}" in c["text"] and cls not in out:
                out[cls] = c["year"]
    return out


def write_summary(out: Path, path: Path) -> None:
    runs = _load(out)
    if not runs:
        return
    L = []
    w = L.append
    w("# E1 — Long Histories · Results")
    w("")
    w(f"{len(runs)} seeds · up to 200 years each · features frozen · "
      f"versions {runs[0]['versions']} · predictions frozen beforehand in `predictions.md`.")
    w("All numbers are measured by `acl/measure.py`, which only reads the world.")
    w("")

    # --- population ---------------------------------------------------------------------
    w("## Population (context)")
    w("")
    w("| seed | yr 0 | 25 | 50 | 100 | 150 | 200 | max gen | ended | top causes of death |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for r in runs:
        pops = [r["rows"][y - 1]["population"] if len(r["rows"]) >= y else "–" for y in (1, 25, 50, 100, 150, 200)]
        gen = max(x["generation"] for x in r["rows"]) if r["rows"] else 0
        causes = Counter()
        for x in r["rows"]:
            causes.update(x["deaths_by_cause"])
        top = ", ".join(f"{k} {v}" for k, v in causes.most_common(4))
        ended = f"extinct yr {r['years_run']}" if r["extinct"] else "alive"
        w(f"| {r['seed']} | " + " | ".join(str(p) for p in pops) + f" | {gen} | {ended} | {top} |")
    w("")

    # --- symbols ------------------------------------------------------------------------
    w("## Shared symbols (Laws 22, 23)")
    w("")
    w("A symbol is a mark shape made in 2+ places that 3+ living people take to go with the same thing "
      "(more often than that thing is around anyway).")
    w("")
    w("| seed | ever | lasted 5y+ | lasted 20y+ | reached people born after | across islands | longest (shape, thing, years) | shared now @100 / @200 |")
    w("|---|---|---|---|---|---|---|---|")
    for r in runs:
        s = r["summary_end"]
        r100, r200 = _row(r, 100), _row(r, 200)
        longest = s["longest_symbol"]
        lg = f"<{longest[0].rsplit('|', 1)[0]}> {longest[0].rsplit('|', 1)[1]}, {longest[1]}" if longest else "–"
        w(f"| {r['seed']} | {s['symbols_ever']} | {s['symbols_lasting_5y']} | {s['symbols_lasting_20y']} | "
          f"{s['symbols_reaching_younger']} | {s['symbols_across_islands']} | {lg} | "
          f"{r100['symbols']['shared_pairs'] if r100 else '–'} / {r200['symbols']['shared_pairs'] if r200 else '–'} |")
    w("")

    # --- false beliefs ------------------------------------------------------------------------
    w("## False beliefs (Laws 24-26, 49, 71)")
    w("")
    w("| seed | year | stories heard | wrong | myths so far | tested beliefs | superstitions | widest superstition | hearsay held | water believed wrongly |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for r in runs:
        for y in _years(r):
            x = _row(r, y)
            f = x["false_beliefs"]
            ws = f"{f['widest_superstition'][0]} ×{f['widest_superstition'][1]}" if f["widest_superstition"] else "–"
            w(f"| {r['seed']} | {y} | {f['stories_heard']} | {f['stories_wrong']} ({_pct(f['stories_wrong'], f['stories_heard'])}) | "
              f"{f['myths_ever']} | {f['beliefs']} | {f['superstitions']} ({_pct(f['superstitions'], f['beliefs'])}) | {ws} | "
              f"{f['hearsay']} | {f['water_believed_wrongly']} of {f['water_believed']} |")
    w("")

    # --- inventions -----------------------------------------------------------------------------
    w("## Inventions (Laws 29, 105-120)")
    w("")
    w("| seed | techniques tried by yr 100 | by yr 200 | held by 3+ at once | first blade | spear | club | carrier | wrap | raft |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for r in runs:
        fy = _first_years(r)
        t100 = _row(r, 100)["inventions"]["techniques_ever"] if _row(r, 100) else "–"
        t200 = r["rows"][-1]["inventions"]["techniques_ever"] if r["rows"] else 0
        s = r["summary_end"]
        w(f"| {r['seed']} | {t100} | {t200} | {s['techniques_ever_held_by_3plus']} ({_pct(s['techniques_ever_held_by_3plus'], s['techniques'])}) | "
          + " | ".join(f"yr {fy[c]}" if c in fy else "never" for c in CLASSES) + " |")
    w("")

    # --- technique survival and loss ---------------------------------------------------------------
    w("## Technique survival and knowledge loss (Laws 50, 57, 114)")
    w("")
    w("| seed | median life (yrs) | longest | lived 10y+ | lived 50y+ | crossed 2+ generations | known @100 | known @200 | named kinds known @200 | lost (events) | found again |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in runs:
        s = r["summary_end"]
        life = s["technique_life_years"]
        k100 = _row(r, 100)["techniques"]["known_now"] if _row(r, 100) else "–"
        last = r["rows"][-1]["techniques"] if r["rows"] else {}
        w(f"| {r['seed']} | {life['median']} | {life['max']} | {life['over_10']} | {life['over_50']} | "
          f"{s['techniques_crossing_2_generations']} | {k100} | {last.get('known_now', 0)} | "
          f"{', '.join(last.get('classes_known', [])) or '–'} | {last.get('lost_events_ever', 0)} | {last.get('found_again_ever', 0)} |")
    w("")

    # --- trust ---------------------------------------------------------------------------------
    w("## Trust networks (Laws 36, 56, 84, 92)")
    w("")
    w("| seed | year | mean trust | distrust ties | strong ties / person | largest strong cluster | clusters of 3+ | strong ties across islands | trusted by 5+ | accuracy↔trust r (n) |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    pooled = []
    for r in runs:
        for key in ("summary_100", "summary_end"):
            if r.get(key):
                pooled += r[key].get("accuracy_trust_pairs", [])
        for y in _years(r):
            x = _row(r, y)
            t = x["trust"]
            w(f"| {r['seed']} | {y} | {t['mean_trust']} | {t['distrust_ties']} | {t['strong_per_person']} | "
              f"{_pct(t['largest_cluster_share'], 1)} | {t['clusters']} | {t['cross_island_strong']} | {t['trusted_hubs']} | "
              f"{t['accuracy_vs_trust_r']} ({t['sources_measured']}) |")
    pr, pn = _pearson(pooled)
    w("")
    w(f"Pooled across seeds at years 100 and 200: accuracy as a source vs. how much others trust them, "
      f"r = {pr} over {pn} people.")
    w("")

    # --- surprise loops --------------------------------------------------------------------------------
    w("## Surprise loops (Laws 63-66, 75)")
    w("")
    w("| seed | puzzles ended | settled by testing | dropped after testing | faded untested | ended by death | mean tests | tested 3+ | new techniques made while puzzling | fires (all) | struck by hand after a sparks puzzle |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in runs:
        s = r["summary_end"]
        e = s["puzzles_ended"]
        total = sum(e.values())
        ev = Counter()
        for x in r["rows"]:
            ev.update(x["events"])
        w(f"| {r['seed']} | {total} | {_pct(e.get('settled by testing', 0), total)} | {_pct(e.get('dropped after testing', 0), total)} | "
          f"{_pct(e.get('faded untested', 0), total)} | {_pct(e.get('died', 0), total)} | {s['puzzle_tests']['mean']} | "
          f"{_pct(s['puzzle_tests']['share_3plus'], 1)} | {s['techniques_from_puzzles']} of {s['techniques']} "
          f"({_pct(s['techniques_from_puzzles'], s['techniques'])}) | {ev['fire']} | {ev['fire_after_puzzle']} |")
    w("")
    w("(\"fires (all)\" includes lightning. The last column counts only fires people struck within a year of "
      "a sparks puzzle.)")
    w("")

    # --- predictions -------------------------------------------------------------------------------------
    w("## Frozen predictions, scored")
    w("")
    for line in _score(runs, pooled):
        w(line)
    w("")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def _verdict(ok):
    return "**confirmed**" if ok is True else "**wrong**" if ok is False else "**unclear**"


def _score(runs, pooled) -> list:
    out = []
    n = len(runs)
    alive = [r for r in runs if not r["extinct"]]

    def say(i, ok, text):
        out.append(f"{i}. {_verdict(ok)} — {text}")

    ext = sum(1 for r in runs if r["extinct"])
    hold = sum(1 for r in runs if r["rows"] and r["rows"][-1]["population"] >= 20 and not r["extinct"])
    say(1, ext >= 1 and hold >= n / 2, f"{ext} of {n} died out; {hold} held or grew (20+ alive at the end).")
    cross = sum(1 for r in alive if any(x["trust"]["cross_island_strong"] > 0 for x in r["rows"][:100]))
    rare = sum(1 for r in alive if r["rows"] and r["rows"][-1]["trust"]["cross_island_strong"] <= 2)
    say(2, None, f"cross-island strong trust appeared by year 100 in {cross} of {len(alive)} surviving seeds; "
                 f"at the end it was rare (≤2 ties) in {rare}. Contact itself is not measured directly.")
    with_sym = sum(1 for r in runs if r["summary_end"]["symbols_ever"] > 0)
    say(3, with_sym >= 6, f"{with_sym} of {n} seeds had a shared symbol at some point.")
    s20 = sum(r["summary_end"]["symbols_lasting_20y"] for r in runs)
    say(4, s20 <= 3, f"{s20} symbols lasted 20+ years in total.")
    ever = sum(r["summary_end"]["symbols_ever"] for r in runs)
    young = sum(r["summary_end"]["symbols_reaching_younger"] for r in runs)
    say(5, (young < ever / 2) if ever else None, f"{young} of {ever} symbols reached someone born after they formed.")
    isl = sum(r["summary_end"]["symbols_across_islands"] for r in runs)
    say(6, isl <= 2, f"{isl} symbols were shared by people on 2+ islands.")
    worst = 0.0
    for r in runs:
        for y in (100, 200):
            x = _row(r, y)
            if x and x["false_beliefs"]["stories_heard"] >= 10:
                f = x["false_beliefs"]
                worst = max(worst, f["stories_wrong"] / f["stories_heard"])
    say(7, worst < 0.10, f"the highest share of wrong versions among stories held (where 10+ were held) was {100 * worst:.0f}%.")
    myths = sum(r["rows"][-1]["false_beliefs"]["myths_ever"] for r in runs if r["rows"])
    years = sum(r["years_run"] for r in runs)
    say(8, (myths / max(1, years / 100)) <= 2, f"{myths} myths over {years} seed-years = {myths / max(1, years / 100):.1f} per seed per century.")
    shares, wide = [], 0
    for r in runs:
        for x in r["rows"]:
            f = x["false_beliefs"]
            if f["beliefs"] >= 10:
                shares.append(f["superstitions"] / f["beliefs"])
            if f["widest_superstition"] and f["widest_superstition"][1] >= 3:
                wide = max(wide, f["widest_superstition"][1])
    mean_share = sum(shares) / len(shares) if shares else 0
    say(9, 0.05 <= mean_share <= 0.20 and wide >= 3,
        f"superstitions averaged {100 * mean_share:.0f}% of tested beliefs; the most people holding one at once was {wide}.")
    full = sum(1 for r in runs if all(c in _first_years(r) and _first_years(r)[c] < 100 for c in CLASSES))
    say(10, full >= 6, f"{full} of {n} seeds invented all six named kinds by year 100.")
    tried = [r["summary_end"]["techniques"] for r in runs]
    share3 = sum(r["summary_end"]["techniques_ever_held_by_3plus"] for r in runs) / max(1, sum(tried))
    say(11, min(tried) >= 100 and share3 < 0.10, f"techniques tried per seed: {min(tried)}–{max(tried)}; "
                                                  f"{100 * share3:.0f}% were ever held by 3+ people at once.")
    meds = [r["summary_end"]["technique_life_years"]["median"] for r in runs]
    say(12, max(meds) < 5, f"median technique life per seed: {', '.join(str(m) for m in meds)} years.")
    core = sum(1 for r in alive if r["rows"] and r["rows"][-1]["techniques"]["crossed_2_generations"] > 0)
    say(13, None if not alive else core >= len(alive) / 2,
        f"in {core} of {len(alive)} surviving seeds, a technique still known at the end was held by people "
        "two or more generations after its inventor (three generations in all).")
    lost = sum(r["rows"][-1]["techniques"]["lost_events_ever"] for r in runs if r["rows"])
    found = sum(r["rows"][-1]["techniques"]["found_again_ever"] for r in runs if r["rows"])
    say(14, lost >= 3 * found, f"{lost} losses vs {found} rediscoveries.")
    means, largest = [], []
    for r in runs:
        for x in r["rows"]:
            if x["trust"]["mean_trust"] is not None and x["population"] >= 5:
                means.append(x["trust"]["mean_trust"])
                largest.append(x["trust"]["largest_cluster_share"])
    mt = sum(means) / len(means) if means else 0
    under = sum(1 for v in largest if v < 0.8) / len(largest) if largest else 0
    say(15, 0.2 <= mt <= 0.5 and under > 0.5, f"mean trust averaged {mt:.2f}; the largest strong-trust cluster was under "
                                              f"80% of people in {100 * under:.0f}% of seed-years.")
    pr, pn = _pearson(pooled)
    say(16, None if pr is None else 0.05 <= pr <= 0.35, f"pooled accuracy↔trust r = {pr} over {pn} people.")
    ended = Counter()
    for r in runs:
        ended.update(r["summary_end"]["puzzles_ended"])
    tot = sum(ended.values())
    settled = ended.get("settled by testing", 0) / tot if tot else 0
    say(17, settled < 0.35, f"{100 * settled:.0f}% of {tot} puzzles ended settled by testing.")
    newp = sum(r["summary_end"]["techniques_from_puzzles"] for r in runs)
    newt = sum(r["summary_end"]["techniques"] for r in runs)
    say(18, 0.10 <= newp / max(1, newt) <= 0.30, f"{newp} of {newt} new techniques ({100 * newp / max(1, newt):.0f}%) were first made while puzzling.")
    fired = sum(1 for r in alive if sum(x["events"].get("fire_after_puzzle", 0) for x in r["rows"]) > 0)
    say(19, None if not alive else fired >= len(alive) / 2, f"fire struck after a sparks puzzle in {fired} of {len(alive)} surviving seeds.")
    return out


if __name__ == "__main__":
    here = Path(__file__).parent
    write_summary(here / "output", here / "summary.md")
    print("wrote", here / "summary.md")
