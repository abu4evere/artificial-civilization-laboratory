"""E6 analysis: apply the frozen definitions and decision rule in predictions.md. Read-only. Writes results.md.

Written before any E6 result was seen.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
E5 = HERE.parent / "E5_millennium" / "output"
SEEDS = list(range(301, 309))


def load(arm):
    runs = {}
    for s in SEEDS:
        f = OUT / arm / f"seed_{s}.json"
        if f.exists():
            runs[s] = json.loads(f.read_text(encoding="utf-8"))
    return runs


def code_hash(folder: Path, every_file: bool = False) -> str:
    """Fingerprint a code folder the way it was recorded: the baseline over every file (CODE_HASH.txt written
    when it was copied), E6 over its .py files."""
    h = hashlib.sha256()
    files = [f for f in folder.rglob("*") if f.is_file() and "__pycache__" not in f.parts] if every_file         else list(folder.rglob("*.py"))
    for f in sorted(files, key=lambda f: f.relative_to(folder).as_posix()):
        h.update(f.relative_to(folder).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()


def baseline_reproduces_e5(run) -> bool | None:
    f = E5 / f"seed_{run['seed']}.json"
    if not f.exists():
        return None
    e5 = json.loads(f.read_text(encoding="utf-8"))["divergence"]
    mine = [s["population"] for s in run["samples"]]
    theirs = [r["population"] for r in e5]
    return mine == theirs


def fired_container(seed) -> list:
    """Things in the world's knowledge that came from a plastic material, were hardened by heat, and hold water."""
    snaps = sorted((OUT / "e6").glob(f"seed_{seed}_*.json.gz"))
    found = set()
    for f in snaps:
        d = json.loads(gzip.open(f).read())
        for sig, rec in d["world"]["knowledge"].items():
            pr = rec.get("props") or {}
            if "~" in sig and "^" in sig and pr.get("tight", 0) >= 50 and pr.get("contain", 0) >= 40:
                found.add(sig)
    return sorted(found)


def by_century(run):
    out = [0] * 10
    for n in run["novelties"]:
        if n["lasting"]:
            out[min(9, n["first_year"] // 100)] += 1
    return out


def main():
    base, e6 = load("baseline"), load("e6")
    L = ["# E6 — Can the world still surprise itself? · Results", ""]
    w = L.append
    w("Definitions, predictions and the decision rule were frozen in predictions.md before any run. "
      "LFA = the first year of the latest lasting novelty in a world (year 0 = the first year).")
    w("")

    # --- validity -----------------------------------------------------------------------------
    w("## Validity (kill criterion)")
    w("")
    hb = code_hash(HERE / "code_baseline" / "acl", every_file=True)
    he = code_hash(HERE / "code_e6" / "acl")
    hb0 = (HERE / "code_baseline" / "CODE_HASH.txt").read_text().strip()
    he0 = (HERE / "code_e6" / "CODE_HASH.txt").read_text().strip()
    w(f"- Baseline code unchanged during the runs: **{'yes' if hb == hb0 else 'NO'}** ({hb[:16]}).")
    w(f"- E6 code unchanged during the runs: **{'yes' if he == he0 else 'NO'}** ({he[:16]}).")
    w(f"- Worlds completed: baseline {len(base)} of 8, E6 {len(e6)} of 8 (at least 6 each needed).")
    rep = {s: baseline_reproduces_e5(r) for s, r in base.items()}
    w(f"- Baseline reproduces E5's population every 10 years: "
      + ", ".join(f"{s} {'yes' if v else 'NO' if v is False else '?'}" for s, v in rep.items()) + ".")
    w("- Recorder read-only (identical state hash with and without it, 20 years): baseline and E6 both verified "
      "before the runs.")
    valid = hb == hb0 and he == he0 and len(base) >= 6 and len(e6) >= 6 and all(v is not False for v in rep.values())
    w(f"- **The experiment is {'valid' if valid else 'INVALID'}.**")
    w("")

    # --- the main table --------------------------------------------------------------------------
    w("## Latest first appearance, world by world")
    w("")
    w("| seed | baseline: lived | baseline LFA | baseline share after 100 | E6: lived | **E6 LFA** | E6 share after 100 | E6 later? |")
    w("|---|---|---|---|---|---|---|---|")
    later = 0
    pairs = 0
    for s in SEEDS:
        b, e = base.get(s), e6.get(s)
        if not b or not e:
            continue
        pairs += 1
        lb, le = b["LFA"], e["LFA"]
        is_later = le is not None and (lb is None or le > lb)
        later += is_later
        fmt = lambda v: "–" if v is None else str(v)  # noqa: E731
        pct = lambda v: "–" if v is None else f"{100 * v:.0f}%"  # noqa: E731
        w(f"| {s} | {b['years_run']} yrs | {fmt(lb)} | {pct(b['share_after_100'])} | {e['years_run']} yrs | "
          f"**{fmt(le)}** | {pct(e['share_after_100'])} | {'yes' if is_later else 'no'} |")
    w("")
    w("Lasting novelties first appearing in each century (all worlds pooled):")
    w("")
    w("| century | " + " | ".join(f"{100 * i + 1}–{100 * (i + 1)}" if i else "0–100" for i in range(10)) + " |")
    w("|---|" + "---|" * 10)
    for name, runs in (("baseline", base), ("E6", e6)):
        tot = [0] * 10
        for r in runs.values():
            for i, n in enumerate(by_century(r)):
                tot[i] += n
        w(f"| {name} | " + " | ".join(str(n) for n in tot) + " |")
    w("")

    # --- decision rule ----------------------------------------------------------------------------
    counted = {s: r for s, r in e6.items() if r["years_run"] >= 300}
    late = [s for s, r in counted.items() if r["LFA"] is not None and r["LFA"] >= 300]
    early = [s for s, r in counted.items() if r["LFA"] is None or r["LFA"] <= 100]
    half = len(counted) / 2
    if counted and len(late) >= half and later >= 6:
        verdict = "BREAKTHROUGH"
    elif counted and len(early) >= half:
        verdict = "BOTTLENECK REMAINS"
    else:
        verdict = "PARTIAL"
    w("## The frozen decision rule")
    w("")
    w(f"- E6 worlds that lived 300+ years (counted): {len(counted)} ({', '.join(map(str, counted)) or 'none'}).")
    w(f"- Counted E6 worlds with LFA at year 300 or later: {len(late)} ({', '.join(map(str, late)) or 'none'}).")
    w(f"- Counted E6 worlds with LFA at year 100 or earlier: {len(early)} ({', '.join(map(str, early)) or 'none'}).")
    w(f"- Seed pairs where E6's LFA is later than the baseline's: {later} of {pairs}.")
    w(f"- **Verdict: {verdict}.**")
    w("")

    # --- predictions ------------------------------------------------------------------------------
    w("## Predictions, scored")
    w("")
    b_early = sum(1 for r in base.values() if r["LFA"] is None or r["LFA"] <= 100)
    b_last = sum(r["lasting"] for r in base.values())
    b_after = sum(sum(1 for n in r["novelties"] if n["lasting"] and n["first_year"] > 100) for r in base.values())
    b_share = b_after / b_last if b_last else 0.0
    ok1 = b_early >= 5 and b_share < 0.10
    w(f"1. Baseline: LFA ≤ 100 in ≥5 of 8 worlds ({b_early}) and under 10% of lasting novelties after year 100 "
      f"({100 * b_share:.1f}% pooled). **{'confirmed' if ok1 else 'wrong'}**")
    w(f"2. E6: LFA ≥ 300 in at least half the counted worlds ({len(late)} of {len(counted)}). "
      f"**{'confirmed' if counted and len(late) >= half else 'wrong'}**")
    s25 = [s for s, r in e6.items() if r["share_after_100"] is not None and r["share_after_100"] >= 0.25]
    w(f"3. E6: ≥25% of lasting novelties after year 100 in ≥5 of 8 worlds ({len(s25)}: "
      f"{', '.join(map(str, s25)) or 'none'}). **{'confirmed' if len(s25) >= 5 else 'wrong'}**")
    surv = [s for s, r in e6.items() if not r["extinct"]]
    trad = [s for s in surv if e6[s]["new_traditions"]]
    w(f"4. E6: a new tradition (began after year 100, 3+ people, 100+ years) in at least half the surviving worlds "
      f"({len(trad)} of {len(surv)}). **{'confirmed' if surv and len(trad) >= len(surv) / 2 else 'wrong'}**")
    dead = [s for s, r in e6.items() if r["extinct"]]
    w(f"5. E6: 3 or fewer worlds die out ({len(dead)}: {', '.join(map(str, dead)) or 'none'}). "
      f"**{'confirmed' if len(dead) <= 3 else 'wrong'}**")
    fc = {s: fired_container(s) for s in e6}
    any_fc = [s for s, v in fc.items() if v]
    w(f"6. E6: a thing shaped from soft stuff, hardened by heat, that holds water, in at least one world "
      f"({', '.join(map(str, any_fc)) or 'none'}). **{'confirmed' if any_fc else 'wrong'}** (reported only)")
    w("")

    # --- descriptive --------------------------------------------------------------------------------
    w("## New consequences in E6 (descriptive)")
    w("")
    w("| seed | " + " | ".join(("water carried", "fire carried")) + " |")
    w("|---|---|---|")
    for s, r in e6.items():
        c = r["consequences"]
        w(f"| {s} | {c.get('water_carried', 0)} | {c.get('fire_carried', 0)} |")
    w("")
    w("## The latest lasting novelties in E6 (what appeared last)")
    w("")
    for s, r in e6.items():
        last = sorted((n for n in r["novelties"] if n["lasting"]), key=lambda n: -n["first_year"])[:3]
        w(f"- seed {s}: " + "; ".join(f"year {n['first_year']}: {n['type']} `{n['key'][:110]}`" for n in last))
    w("")
    w("## New traditions in E6 (began after year 100)")
    w("")
    for s, r in e6.items():
        top = r["new_traditions"][:4]
        w(f"- seed {s}: " + ("; ".join(f"`{t['item'][:90]}` {t['years']} years from year {t['from']}" for t in top)
                             or "none"))
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote", HERE / "results.md", "| verdict:", verdict)


if __name__ == "__main__":
    main()
