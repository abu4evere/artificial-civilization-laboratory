"""CA1 analysis in the frozen order (questions.md, `CA1-frozen`). Written before any data.

  python experiments/CA1_chain_audit/analyse_ca1.py          # writes results.md
  python experiments/CA1_chain_audit/analyse_ca1.py --pilot  # reads output_pilot/ (throwaway), writes nothing

Validity (no outcome shown otherwise): zero check passes; all 36 worlds present; one code fingerprint.
Links, for each kind of thing (sig) in a world: 1 invented; 2 useful (largest factor >= 1.05); 3 transmitted (learned
by someone other than its first knower); 4 retained (someone alive held it after its first knower died; base = kinds
testable for it, i.e. first knower dead by the end); 5 built on (a later kind takes it as a part and has a greater largest
factor); 6 retransmitted (such a better kind itself passed links 3 and 4). Pass rate = reaching link k / reaching k - 1,
pooled over a set. Frozen reading: the bottleneck is the link with the lowest pass rate; found only if the same link in
discovery and holdout.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_ca1 import DISCOVERY, HOLDOUT, LONG, OUT  # noqa: E402

NAMES = ("invented", "useful", "transmitted", "retained", "built on", "retransmitted")


def chain(res):
    """Counts reaching each link in one world, and the extra measures."""
    ks = {k["sig"]: k for k in res["kinds"]}
    useful = lambda k: k["max_factor"] is not None and k["max_factor"] >= 1.05  # noqa: E731
    better_users = {s: [] for s in ks}            # part -> later kinds that use it and are better
    for k in ks.values():
        for part in k["parts"]:
            pk = ks.get(part)
            if pk and k["max_factor"] is not None and pk["max_factor"] is not None and k["max_factor"] > pk["max_factor"]:
                better_users[part].append(k["sig"])
    n = [0] * 6
    for s, k in ks.items():
        n[0] += 1
        if not useful(k):
            continue
        n[1] += 1
        if not k["transmitted"]:
            continue
        n[2] += 1
    # Link 4's base is the transmitted useful kinds whose first knower died; link 4 itself those retained.
    base4 = [k for k in ks.values() if useful(k) and k["transmitted"] and k["testable"]]
    ret = [k for k in base4 if k["retained"]]
    built = [k for k in ret if better_users[k["sig"]]]
    retx = [k for k in built if any(ks[u]["transmitted"] and ks[u]["testable"] and ks[u]["retained"]
                                    for u in better_users[k["sig"]])]
    n[3], n[4], n[5] = len(ret), len(built), len(retx)
    depth = {}

    def longest(s, seen=()):
        if s in depth:
            return depth[s]
        best = 0
        for u in better_users.get(s, ()):
            if u not in seen:
                best = max(best, 1 + longest(u, seen + (s,)))
        depth[s] = best
        return best
    return {"n": n, "base4": len(base4), "not_testable": sum(1 for k in ks.values() if useful(k) and k["transmitted"]
                                                              and not k["testable"]),
            "no_props": sum(1 for k in ks.values() if k["max_factor"] is None),
            "copy_errors": sum(1 for k in ks.values() if k["copy_error"] or k["how"] not in ("made", "heated")),
            "routes": Counter(k["route"] for k in ks.values() if k["route"]),
            "longest": max((longest(s) for s in ks), default=0),
            "gens": max((k["gens"] for k in ks.values()), default=0),
            "pops": res["pops"]}


def pass_rates(chains):
    n = [sum(c["n"][i] for c in chains) for i in range(6)]
    b4 = sum(c["base4"] for c in chains)
    bases = [None, n[0], n[1], b4, n[3], n[4]]
    rates = [None] + [n[i] / bases[i] if bases[i] else None for i in range(1, 6)]
    return n, b4, rates


def table(label, chains, L):
    n, b4, rates = pass_rates(chains)
    L += [f"### {label} ({len(chains)} worlds)", "",
          "| link | kinds reaching it | out of | pass rate |", "|---|---|---|---|",
          f"| 1 invented | {n[0]} | – | – |"]
    bases = [None, n[0], n[1], b4, n[3], n[4]]
    for i in range(1, 6):
        r = f"{rates[i]:.3f}" if rates[i] is not None else "–"
        L.append(f"| {i + 1} {NAMES[i]} | {n[i]} | {bases[i]} | {r} |")
    nt = sum(c["not_testable"] for c in chains)
    L += ["", f"Useful, transmitted kinds whose first knower was still alive at the end (left out of links 4–6): {nt}. "
          f"Kinds with no recorded properties (counted as not shown useful): {sum(c['no_props'] for c in chains)}. "
          f"Kinds that first appeared as a changed copy: {sum(c['copy_errors'] for c in chains)}.", ""]
    routes = sum((c["routes"] for c in chains), Counter())
    L.append("First transmission by route: " + ", ".join(f"{k} {v}" for k, v in routes.most_common()) + ".")
    L += ["", f"Longest chain of better kinds in a world (median / most): {statistics.median(c['longest'] for c in chains):.0f}"
          f" / {max(c['longest'] for c in chains)}; most generations a recipe passed through (median / most): "
          f"{statistics.median(c['gens'] for c in chains):.0f} / {max(c['gens'] for c in chains)}.", ""]
    pops = lambda d: statistics.median(c["pops"][d] if len(c["pops"]) > d else 0 for c in chains)  # noqa: E731
    L += ["Living people (median), decades 1–12: " + ", ".join(f"{pops(d):.0f}" for d in range(12)) + ".", ""]
    valid = [i for i in range(1, 6) if rates[i] is not None]
    return min(valid, key=lambda i: rates[i]) if valid else None


def main(pilot=False):
    out = HERE / "output_pilot" if pilot else OUT
    sets = {"discovery": DISCOVERY, "holdout": HOLDOUT, "long": LONG}
    rows, missing = {}, []
    for name, seeds in sets.items():
        for s in seeds:
            f = out / f"seed_{s}.json"
            if f.exists():
                rows.setdefault(name, []).append(json.loads(f.read_text(encoding="utf-8")))
            else:
                missing.append(str(s))
    L = ["# CA1 — the chain audit: results" + (" (PILOT, throwaway)" if pilot else ""), "",
         "Frozen as `CA1-frozen`. run_ca1.py, analyse_ca1.py. Read-only: nature v2, unchanged.", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero check (the observer leaves the world unchanged): **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing or pilot
    allr = [r for v in rows.values() for r in v]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    L.append(f"- One fingerprint (`code_v2`): **{'yes' if len(fps) == 1 else 'NO'}**")
    ok &= len(fps) == 1
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**", ""]
    if ok:
        L += ["## The chain", ""]
        low = {}
        for name in ("discovery", "holdout", "long"):
            if name in rows:
                low[name] = table(name.capitalize() + (" (300 years; beside the reading)" if name == "long" else ""),
                                  [chain(r) for r in rows[name]], L)
        d, h = low.get("discovery"), low.get("holdout")
        L += ["## The frozen reading", ""]
        if d is not None and d == h:
            L.append(f"**The bottleneck is link {d + 1}, {NAMES[d]}**: the lowest pass rate in both discovery and holdout.")
        else:
            L.append("**No single bottleneck:** the lowest pass rate was "
                     f"link {d + 1 if d is not None else '–'} in discovery and {h + 1 if h is not None else '–'} in "
                     "holdout. The drop at every link is reported above.")
    text = "\n".join(L) + "\n"
    if not pilot:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(pilot="--pilot" in sys.argv)
