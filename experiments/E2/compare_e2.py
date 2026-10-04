"""Compare E2 with E1 on the same seeds, and score E2's frozen predictions. Read-only.

Usage: python experiments/E2/compare_e2.py   (writes experiments/E2/results.md)
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
E1 = HERE.parent / "E1" / "output"
E2 = HERE / "output"
sys.path.insert(0, str(HERE.parent / "E1"))
sys.path.insert(0, str(HERE.parent.parent))

from acl.runner import load_snapshot  # noqa: E402
from analyse_inv_extra import _bands_of  # noqa: E402


def _pearson(pairs):
    n = len(pairs)
    if n < 5:
        return None
    xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 3) if sx and sy else None


def _load(out):
    runs = {}
    for f in sorted(out.glob("seed_*.json")):
        if f.name.count("_") == 1:
            r = json.loads(f.read_text(encoding="utf-8"))
            runs[r["seed"]] = r
    return runs


def _events(r, key, prefix=False):
    tot = 0
    for x in r["rows"]:
        for k, v in x["events"].items():
            if (k.startswith(key) if prefix else k == key):
                tot += v
    return tot


def _pop(r, y):
    rows = r["rows"]
    return rows[y - 1]["population"] if len(rows) >= y else 0


def _mixed(out, seed):
    path = out / f"seed_{seed}_year100.json.gz"
    if not path.exists():
        return None
    w, _ = load_snapshot(path)
    living = w.living()
    if not living:
        return None
    groups = max(1, min(4, w.cfg.founders // 4))
    memo = {}
    return sum(1 for p in living if len(_bands_of(w, p.id, memo, groups)) >= 2) / len(living)


def _end_chronicle(out, seed):
    w, h = load_snapshot(out / f"seed_{seed}_end.json.gz")
    return h.chronicle


def _split_half(runs):
    a, b = [], []
    for r in runs.values():
        for seq in (r["summary_end"].get("accuracy_sequences") or {}).values():
            hh = len(seq) // 2
            a.append(sum(seq[:hh]) / hh)
            b.append(sum(seq[hh:]) / (len(seq) - hh))
    return _pearson(list(zip(a, b))), len(a)


def main():
    e1, e2 = _load(E1), _load(E2)
    seeds = sorted(set(e1) & set(e2))
    L = []
    w = L.append
    w("# E2 — After the four changes · Results against E1")
    w("")
    w(f"Seeds {seeds[0]}–{seeds[-1]}, up to 200 years each. E1 is the frozen-feature baseline; E2 runs the same seeds "
      "after the four changes. Note: any change gives each seed a different random history, so compare across seeds, "
      "not seed by seed.")
    w("")
    w("| seed | pop @100 E1 → E2 | pop @200 E1 → E2 | tests / world-year E1 → E2 | experts @100 | open-water crossings (E2) | rafts carried @100 / known | techniques from marks | mark claims held / failed | mixed ancestry @100 E1 → E2 | harvests / yr E1 → E2 |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    stats = Counter()
    mix_lower = 0
    mix_pairs = 0
    rec_runs = 0
    for s in seeds:
        a, b = e1[s], e2[s]
        t1 = (_events(a, "verified") + _events(a, "refuted")) / max(1, a["years_run"])
        t2 = (_events(b, "verified_", True) + _events(b, "refuted_", True)) / max(1, b["years_run"])
        r100 = b["rows"][99] if len(b["rows"]) >= 100 else None
        experts = r100["trust"].get("experts", 0) if r100 else "–"
        rafts = f"{r100['trust'].get('rafts_carried', 0)} / {r100['trust'].get('rafts_known', 0)}" if r100 else "–"
        crossed = _events(b, "crossed")
        learned = _events(b, "learn_how_read")
        mh, mf = _events(b, "mark_verified"), _events(b, "mark_refuted")
        m1, m2 = _mixed(E1, s), _mixed(E2, s)
        if m1 is not None and m2 is not None:
            mix_pairs += 1
            mix_lower += m2 < m1
        h1 = _events(a, "harvest") / max(1, a["years_run"])
        h2 = _events(b, "harvest") / max(1, b["years_run"])
        chron = _end_chronicle(E2, s)
        recovered = sum(1 for c in chron if c["kind"] == "record")
        rec_runs += recovered > 0
        stats["t1"] += t1; stats["t2"] += t2; stats["h1"] += h1; stats["h2"] += h2
        stats["pop1"] += _pop(a, 100); stats["pop2"] += _pop(b, 100)
        stats["mh"] += mh; stats["mf"] += mf
        fmt = lambda v: "–" if v is None else f"{100 * v:.0f}%"  # noqa: E731
        w(f"| {s} | {_pop(a, 100)} → {_pop(b, 100)} | {_pop(a, 200)} → {_pop(b, 200)} | {t1:.1f} → {t2:.1f} | {experts} | "
          f"{crossed} | {rafts} | {learned} ({recovered} recovering a lost skill) | {mh} / {mf} | {fmt(m1)} → {fmt(m2)} | {h1:.1f} → {h2:.1f} |")
    n = len(seeds)
    w("")
    rec_pairs = []
    trust_pairs1, trust_pairs2 = [], []
    for s in seeds:
        for key in ("summary_100", "summary_end"):
            if e2[s].get(key):
                rec_pairs += e2[s][key].get("accuracy_record_pairs", [])
                trust_pairs2 += e2[s][key].get("accuracy_trust_pairs", [])
            if e1[s].get(key):
                trust_pairs1 += e1[s][key].get("accuracy_trust_pairs", [])
    r_rec, n_rec = _pearson(rec_pairs), len(rec_pairs)
    r_t1, r_t2 = _pearson(trust_pairs1), _pearson(trust_pairs2)
    sh, sh_n = _split_half(e2)
    w(f"- **Is reputation tracking truth?** How often people are right vs how others' records rate them, pooled at "
      f"years 100 and 200: r = {r_rec} over {n_rec} people. General trust vs accuracy: E1 r = {r_t1}, E2 r = {r_t2}.")
    w(f"- **Is being right a lasting trait?** Split-half correlation of each person's accuracy (people with 4+ "
      f"tested claims): r = {sh} over {sh_n} people (E1: 0.03).")
    w(f"- **Mean population at year 100** (died-out seeds count as 0): E1 {stats['pop1'] / n:.1f}, E2 {stats['pop2'] / n:.1f}.")
    w("")
    # side effects on E1's own measures
    w("**What happened to E1's measures** (all seeds):")
    w("")
    w("| measure | E1 | E2 |")
    w("|---|---|---|")
    for label, f in (("seeds that died out", lambda r: 1 if r["extinct"] else 0),
                     ("shared symbols ever", lambda r: r["summary_end"]["symbols_ever"]),
                     ("myths (shared false stories)", lambda r: r["rows"][-1]["false_beliefs"]["myths_ever"] if r["rows"] else 0),
                     ("techniques tried", lambda r: r["summary_end"]["techniques"]),
                     ("puzzles settled by testing", lambda r: r["summary_end"]["puzzles_ended"].get("settled by testing", 0)),
                     ("new techniques made while puzzling", lambda r: r["summary_end"]["techniques_from_puzzles"])):
        w(f"| {label} | {sum(f(e1[s]) for s in seeds)} | {sum(f(e2[s]) for s in seeds)} |")
    w("")
    # score
    w("## Frozen predictions, scored")
    w("")
    alive2 = [s for s in seeds if not e2[s]["extinct"]]
    alive100 = [s for s in seeds if len(e2[s]["rows"]) >= 100 and e2[s]["rows"][99]["population"] > 0]

    def say(i, ok, text):
        verdict = "**confirmed**" if ok is True else "**wrong**" if ok is False else "**unclear**"
        w(f"{i}. {verdict} — {text}")
    say(1, stats["t2"] / n >= 20, f"tested claims per world-year averaged {stats['t2'] / n:.1f} (E1 {stats['t1'] / n:.1f}).")
    say(2, None if r_rec is None else r_rec >= 0.4, f"accuracy vs others' records r = {r_rec} over {n_rec} people.")
    say(3, None if sh is None else sh < 0.2, f"split-half accuracy r = {sh} over {sh_n} people.")
    with_expert = sum(1 for s in alive100 if e2[s]["rows"][99]["trust"].get("experts", 0) >= 1)
    say(4, with_expert <= len(alive100) / 2, f"{with_expert} of {len(alive100)} seeds alive at year 100 had a person rated "
        "reliable by 5+ others.")
    crossed_ok = all(_events(e2[s], "crossed") >= 20 for s in alive2)
    carried = max((x["trust"].get("rafts_carried", 0) / x["population"] for s in seeds for x in e2[s]["rows"]
                   if x["population"]), default=0)
    say(5, crossed_ok and carried < 0.10, f"open-water crossings per surviving seed: "
        f"{', '.join(str(_events(e2[s], 'crossed')) for s in alive2)}; the most carrying a raft in any yearly count: "
        f"{100 * carried:.0f}% of the living.")
    say(6, None if mix_pairs < 5 else mix_lower >= 5, f"mixed ancestry at year 100 was lower in E2 in {mix_lower} of "
        f"{mix_pairs} seeds alive at year 100 in both.")
    learned_ok = all(_events(e2[s], "learn_how_read") >= 10 for s in alive2)
    say(7, learned_ok and rec_runs >= 2, f"techniques taken up from marks per surviving seed: "
        f"{', '.join(str(_events(e2[s], 'learn_how_read')) for s in alive2)}; seeds where a skill nobody alive knew "
        f"was recovered from a mark: {rec_runs}.")
    say(8, stats["mf"] > stats["mh"], f"claims from marks held {stats['mh']}, failed {stats['mf']}.")
    say(9, abs(stats["pop2"] - stats["pop1"]) <= 0.25 * stats["pop1"],
        f"mean population at year 100: E1 {stats['pop1'] / n:.1f}, E2 {stats['pop2'] / n:.1f}.")
    say(10, abs(stats["h2"] - stats["h1"]) <= 0.5 * stats["h1"],
        f"harvests per world-year: E1 {stats['h1'] / n:.1f}, E2 {stats['h2'] / n:.1f}.")
    w("")
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote", HERE / "results.md")


if __name__ == "__main__":
    main()
