"""E1 report: the seven things to review before any change to the laws.

1. Prediction scorecard
2. Shared symbol statistics
3. Technique persistence statistics
4. Knowledge-loss events
5. Population trajectories
6. Candidate cultural patterns
7. Most surprising events

Reads output/seed_<n>.json (the Lab's yearly measurements) and the end
snapshots (the full world and the historian's full record). Read-only: it
changes no world and no output it reads. Writes report.md.

Usage: python experiments/E1/report_e1.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))

from analyse_e1 import CLASSES, _first_years, _load, _pearson, _score  # noqa: E402
from acl import marks  # noqa: E402
from acl.config import WEEKS_PER_YEAR  # noqa: E402
from acl.historian import CLASSES as NAMES, PRACTICES, classify, describe  # noqa: E402
from acl.measure import superstitious  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402

OUT = HERE / "output"
BARS = "▁▂▃▄▅▆▇█"
WORD = {"blade": "blade", "spear": "spear", "club": "club", "carrier": "carrier", "wrap": "wrap", "boat": "raft"}


def _spark(values: list) -> str:
    top = max(values) if values else 0
    if not top:
        return "".join("·" for _ in values)
    return "".join(BARS[min(7, int(v / top * 7.999))] if v else "·" for v in values)


def _runs_with_worlds() -> list:
    runs = _load(OUT)
    for r in runs:
        w, h = load_snapshot(OUT / f"seed_{r['seed']}_end.json.gz")
        r["_w"], r["_h"] = w, h
    return runs


def _longest_run(flags: list) -> tuple:
    """(length, start index) of the longest run of True."""
    best, start, cur, cur_start = 0, 0, 0, 0
    for i, f in enumerate(flags):
        if f:
            if cur == 0:
                cur_start = i
            cur += 1
            if cur > best:
                best, start = cur, cur_start
        else:
            cur = 0
    return best, start


def main() -> None:
    runs = _runs_with_worlds()
    L: list = []
    w = L.append
    n = len(runs)
    w("# E1 — Long Histories · Report for review")
    w("")
    w(f"{n} seeds (101–108), up to 200 years each. Features were frozen for the whole experiment; the only "
      "code added measures and reports. Predictions were written and frozen before the first run "
      "(`predictions.md`). Detailed tables: `summary.md`.")
    w("")

    # 1 ------------------------------------------------------------------------------------------
    pooled = []
    for r in runs:
        for key in ("summary_100", "summary_end"):
            if r.get(key):
                pooled += r[key].get("accuracy_trust_pairs", [])
    lines = _score(runs, pooled)
    tally = Counter("confirmed" if "**confirmed**" in s else "wrong" if "**wrong**" in s else "unclear" for s in lines)
    w("## 1. Prediction scorecard")
    w("")
    w(f"{tally['confirmed']} confirmed · {tally['wrong']} wrong · {tally['unclear']} unclear, out of {len(lines)}.")
    w("")
    L.extend(lines)
    w("")

    # 2 ------------------------------------------------------------------------------------------
    w("## 2. Shared symbols")
    w("")
    tot = Counter()
    things = Counter()
    drift = 0
    longest = []
    for r in runs:
        s = r["summary_end"]
        for k in ("symbols_ever", "symbols_lasting_5y", "symbols_lasting_20y", "symbols_reaching_younger",
                  "symbols_across_islands"):
            tot[k] += s[k]
        for x in r["rows"]:
            things.update(x["symbols"]["things"])
        drift += sum(1 for c in r["_h"].chronicle if c["kind"] == "symbol" and "drifted" in c["text"])
        if s["longest_symbol"]:
            shape, thing = s["longest_symbol"][0].rsplit("|", 1)
            longest.append((s["longest_symbol"][1], r["seed"], shape, thing))
    w(f"- Symbols ever formed: **{tot['symbols_ever']}** across {n} seeds "
      f"({sum(1 for r in runs if r['summary_end']['symbols_ever'])} seeds had at least one).")
    w(f"- Present in 5+ yearly counts: **{tot['symbols_lasting_5y']}** · in 20+: **{tot['symbols_lasting_20y']}** "
      "(years present, not necessarily in a row) · "
      f"reached people born after they formed: **{tot['symbols_reaching_younger']}** · "
      f"shared by people standing on 2+ islands: **{tot['symbols_across_islands']}** · meanings that drifted: **{drift}**.")
    w("- What shared symbols went with, in symbol-years: "
      + ", ".join(f"{k} {v}" for k, v in things.most_common()) + ".")
    w("- Longest-lived per seed: " + "; ".join(f"seed {sd} <{sh}> → {th}, {yrs} years"
                                              for yrs, sd, sh, th in sorted(longest, reverse=True)) + ".")
    w("")
    w("| seed | marks made | shapes on the land @100 / @end | shapes known @100 / @end | shared pairs @100 / @end |")
    w("|---|---|---|---|---|")
    for r in runs:
        made = sum(x["events"].get("mark", 0) for x in r["rows"])
        a, b = (r["rows"][99] if len(r["rows"]) >= 100 else None), r["rows"][-1]
        f = lambda x, k: x["symbols"][k] if x else "–"  # noqa: E731
        w(f"| {r['seed']} | {made} | {f(a, 'shapes_on_land')} / {f(b, 'shapes_on_land')} | "
          f"{f(a, 'shapes_known')} / {f(b, 'shapes_known')} | {f(a, 'shared_pairs')} / {f(b, 'shared_pairs')} |")
    w("")

    # 3 ------------------------------------------------------------------------------------------
    w("## 3. Technique persistence")
    w("")
    spans = []
    tops = []
    for r in runs:
        world = r["_w"]
        end = world.tick
        held = Counter(sig for q in world.living() for sig in q.recipes)
        for sig, rec in world.knowledge.items():
            last = end if rec.get("alive") else (rec["lost"][-1] if rec.get("lost") else rec["first_tick"])
            span = (last - rec["first_tick"]) / WEEKS_PER_YEAR
            spans.append(span)
            tops.append((round(span, 1), r["seed"], sig, rec, held.get(sig, 0), rec.get("alive")))
    total = len(spans)
    w(f"Every distinct way of making something, across all seeds: **{total}**. Share still known (by someone) at least…")
    w("")
    w("| ≥1 yr | ≥5 yrs | ≥10 yrs | ≥25 yrs | ≥50 yrs | ≥100 yrs | ≥150 yrs |")
    w("|---|---|---|---|---|---|---|")
    w("| " + " | ".join(f"{100 * sum(1 for s in spans if s >= y) / total:.1f}%" for y in (1, 5, 10, 25, 50, 100, 150)) + " |")
    w("")
    w("(Span from first made to last known; a technique lost and later found again counts across the gap.)")
    w("")
    w("Longest-lived techniques:")
    w("")
    w("| seed | how | what it is | first made | span (yrs) | holders at the end |")
    w("|---|---|---|---|---|---|")
    for span, seed, sig, rec, holders, alive in sorted(tops, key=lambda t: (-t[0], t[1], t[2]))[:12]:
        cls = classify(rec.get("props"))
        what = ", ".join(NAMES[c][0] for c in cls) if cls else "no named use"
        w(f"| {seed} | {describe(rec['recipe'], runs[0]['_w'])} | {what} | yr {rec['first_tick'] // WEEKS_PER_YEAR} | "
          f"{span} | {holders if alive else 'lost'} |")
    w("")
    w("Named kinds of thing, by seed: years with at least one person who could make it (longest unbroken stretch):")
    w("")
    w("| seed | " + " | ".join(WORD[c] for c in CLASSES) + " |")
    w("|---|" + "---|" * len(CLASSES))
    for r in runs:
        rows = r["_h"].years
        cells = []
        for c in CLASSES:
            flags = [x["know"].get(c, 0) > 0 for x in rows]
            run, start = _longest_run(flags)
            cells.append(f"{sum(flags)} ({run} from yr {start})" if run else "never")
        w(f"| {r['seed']} | " + " | ".join(cells) + " |")
    w("")

    # 4 ------------------------------------------------------------------------------------------
    w("## 4. Knowledge-loss events")
    w("")
    w("| seed | technique losses | techniques ever lost | found again | named kinds lost (year) → regained (year) |")
    w("|---|---|---|---|---|")
    for r in runs:
        world, h = r["_w"], r["_h"]
        losses = sum(len(rec.get("lost", [])) for rec in world.knowledge.values())
        ever = sum(1 for rec in world.knowledge.values() if rec.get("lost"))
        last = r["rows"][-1]["techniques"] if r["rows"] else {}
        named = []
        for c in h.chronicle:
            if c["kind"] == "loss":
                kind = next((k for k in CLASSES if NAMES[k][0] in c["text"]), "?")
                named.append([kind, c["year"], None])
            elif c["kind"] == "invention" and "a skill lost since year" in c["text"]:
                for item in named:
                    if item[2] is None and f"{NAMES[item[0]][0]} again" in c["text"]:
                        item[2] = c["year"]
                        break
        text = "; ".join(f"{WORD.get(k, k)} {a} → {b if b is not None else 'never'}" for k, a, b in named) or "none"
        w(f"| {r['seed']} | {losses} | {ever} | {last.get('found_again_ever', 0)} | {text} |")
    w("")
    w("Only a kind of thing that at least two people knew counts as a named loss. Single techniques come and go far "
      "more often (the first columns).")
    w("")

    # 5 ------------------------------------------------------------------------------------------
    w("## 5. Population trajectories")
    w("")
    w("Every 5 years, scaled per seed (· = nobody):")
    w("")
    w("```")
    for r in runs:
        pops = [r["rows"][i]["population"] if i < len(r["rows"]) else 0 for i in range(4, 200, 5)]
        w(f"seed {r['seed']}  {_spark(pops)}  peak {max(pops) if pops else 0:>3}")
    w("```")
    w("")
    w("| seed | yr 10 | 25 | 50 | 75 | 100 | 125 | 150 | 175 | 200 | peak (yr) | generations | births | deaths |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    causes = Counter()
    for r in runs:
        rows = r["rows"]
        pops = [rows[y - 1]["population"] if len(rows) >= y else "–" for y in (10, 25, 50, 75, 100, 125, 150, 175, 200)]
        peak = max(rows, key=lambda x: x["population"]) if rows else {"population": 0, "year": 0}
        for x in rows:
            causes.update(x["deaths_by_cause"])
        w(f"| {r['seed']} | " + " | ".join(str(p) for p in pops)
          + f" | {peak['population']} ({peak['year']}) | {max(x['generation'] for x in rows) if rows else 0} | "
          f"{sum(x['births'] for x in rows)} | {sum(x['deaths'] for x in rows)} |")
    w("")
    tot_d = sum(causes.values())
    w("Deaths by cause, all seeds: " + ", ".join(f"{k} {v} ({100 * v / tot_d:.0f}%)" for k, v in causes.most_common()) + ".")
    w("")

    # 6 ------------------------------------------------------------------------------------------
    w("## 6. Candidate cultural patterns")
    w("")
    w("A candidate is something many people share, that lasts, and that passes to people who did not start it. "
      "Whether it changes behaviour (Law 42) is not yet tested. These are for review, not conclusions.")
    w("")
    w("**Practices** (share of the living who believe in the practice; longest stretch with ≥25%):")
    w("")
    w("| seed | sowing: peak, longest ≥25% | building: peak, longest ≥25% | storing: peak, longest ≥25% |")
    w("|---|---|---|---|")
    for r in runs:
        rows = r["_h"].years
        cells = []
        for k in PRACTICES:
            shares = [x["practice"].get(k, 0) / x["population"] if x["population"] else 0 for x in rows]
            run, start = _longest_run([s >= 0.25 for s in shares])
            cells.append(f"{100 * max(shares, default=0):.0f}%, {run} yrs" + (f" from yr {start}" if run else ""))
        w(f"| {r['seed']} | " + " | ".join(cells) + " |")
    w("")
    w("**Superstitions that spread** (longest stretch of years the same no-effect belief was held by 3+ people at once):")
    w("")
    for r in runs:
        best, cur_key, cur_len, best_start = (None, 0), None, 0, 0
        for i, x in enumerate(r["rows"]):
            ws = x["false_beliefs"]["widest_superstition"]
            key = ws[0] if ws and ws[1] >= 3 else None
            if key is not None and key == cur_key:
                cur_len += 1
            else:
                cur_key, cur_len = key, (1 if key else 0)
                start = i
            if cur_key and cur_len > best[1]:
                best, best_start = (cur_key, cur_len), start
        if best[0]:
            w(f"- seed {r['seed']}: `{best[0]}` for {best[1]} years from year {best_start}")
        else:
            w(f"- seed {r['seed']}: none held by 3+ at once")
    w("")
    w("**Social patterns** (the historian's detections):")
    w("")
    w("| seed | exchange partnerships | revenge acts | feuds (longest, yrs) | settlements founded | bands now | leaders named |")
    w("|---|---|---|---|---|---|---|")
    for r in runs:
        h = r["_h"]
        longest_feud = max(((f["last"] - f["start"]) / WEEKS_PER_YEAR for f in h.feuds), default=0)
        leaders = sum(1 for c in h.chronicle if c["kind"] == "leader")
        w(f"| {r['seed']} | {len(h.partnerships)} | {h.revenge_acts} | {len(h.feuds)} ({longest_feud:.0f}) | "
          f"{len(h.settlements)} | {len(h.bands)} | {leaders} |")
    w("")
    w("**Differences between islands at the end** (Law 39: groups need not converge):")
    w("")
    w("| seed | island | people | named kinds they can make | sowing / building / storing | shapes 2+ islanders read alike |")
    w("|---|---|---|---|---|---|")
    for r in runs:
        world = r["_w"]
        if not world.living():
            w(f"| {r['seed']} | – | 0 | – | – | – |")
            continue
        island = {}
        for i, comp in enumerate(world.landmasses()):
            for loc in comp:
                island[loc] = i
        groups: dict = {}
        for q in world.living():
            groups.setdefault(island.get(q.loc, -1), []).append(q)
        for isl, people in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            kinds = sorted({c for q in people for sig in q.recipes
                            for c in classify(world.knowledge.get(sig, {}).get("props"))})
            prac = []
            for k, ts in PRACTICES.items():
                share = sum(1 for q in people if any(q.beliefs.get(f"{t}@{s_}", 0) >= 0.1 for t in ts for s_ in range(4)))
                prac.append(f"{100 * share / len(people):.0f}%")
            reads = Counter()
            for q in people:
                for shape in q.marks:
                    for thing, v in marks.meaning(q, shape).items():
                        if v >= 0.3:
                            reads[(shape, thing)] += 1
            alike = ", ".join(f"<{s}>→{t} ×{k}" for (s, t), k in reads.most_common(3) if k >= 2) or "–"
            w(f"| {r['seed']} | {'at sea' if isl == -1 else isl} | {len(people)} | {', '.join(WORD[c] for c in kinds) or '–'} | "
              f"{' / '.join(prac)} | {alike} |")
    w("")

    # 7 ------------------------------------------------------------------------------------------
    w("## 7. Most surprising events")
    w("")
    w("Gathered by rule from every chronicle and measurement: the rarest kinds of event, the sharpest turns, and "
      "anything the frozen predictions said would not happen. Ordered by seed and year.")
    w("")
    picks = []
    for r in runs:
        h, rows = r["_h"], r["rows"]
        sd = r["seed"]
        for c in h.chronicle:
            if c["kind"] in ("myth", "feud", "famine", "drought", "loss"):
                picks.append((sd, c["year"], c["kind"], c["text"]))
            elif c["kind"] == "symbol" and "drifted" in c["text"]:
                picks.append((sd, c["year"], "symbol drift", c["text"]))
            elif c["kind"] == "invention" and "a skill lost since year" in c["text"]:
                picks.append((sd, c["year"], "regained", c["text"]))
            elif c["kind"] == "revenge":
                picks.append((sd, c["year"], "revenge", c["text"]))
            elif c["kind"] == "first" and any(k in c["text"] for k in ("first fire made by people", "first deliberate testing",
                                                                       "trusted them less", "first violence")):
                picks.append((sd, c["year"], "first", c["text"]))
        # sharpest population turns over 10 years
        pops = [x["population"] for x in rows]
        for i in range(10, len(pops)):
            before = pops[i - 10]
            if before >= 15 and pops[i] <= before * 0.5:
                picks.append((sd, rows[i]["year"], "collapse", f"Population fell from {before} to {pops[i]} in ten years."))
                break
        if r["extinct"]:
            picks.append((sd, r["years_run"], "extinction", f"The last person died in year {r['years_run']}."))
        # the most widely believed false story, at year 100 and at the end
        for tag in ("year100", "end"):
            path = OUT / f"seed_{sd}_{tag}.json.gz"
            if not path.exists():
                continue
            world, hist = (r["_w"], h) if tag == "end" else load_snapshot(path)
            versions = Counter()
            for q in world.living():
                for m in q.memories:
                    t = hist.truth.get(str(m.eid))
                    if t and m.source and t[1] and (m.actor or "") != t[1]:
                        versions[(m.eid, t[0], t[1], m.actor or "")] += 1
            if versions:
                (eid, kind, true, said), k = versions.most_common(1)[0]
                if k >= 3:
                    nm = lambda x: world.people[x].name if x in world.people else x.replace("animal:", "")  # noqa: E731
                    picks.append((sd, world.year, "false story",
                                  f"{k} living people believe {nm(said)} {kind} {nm(hist.truth[str(eid)][2]) if hist.truth[str(eid)][2] in world.people else 'someone'}; "
                                  f"it was {nm(true)}."))
    kinds = Counter(k for _, _, k, _ in picks)
    w("Counts by kind: " + ", ".join(f"{k} {v}" for k, v in kinds.most_common()) + ".")
    w("")
    rare = [p for p in picks if p[2] not in ("drought",)]
    for sd, yr, kind, text in sorted(rare, key=lambda p: (p[0], p[1])):
        w(f"- seed {sd}, year {yr} · {kind} · {text}")
    w("")
    (HERE / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote", HERE / "report.md")


if __name__ == "__main__":
    main()
