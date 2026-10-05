"""E7.7 analysis: per-family exposure → learning → making, and the frozen predictions scored as written.
Read-only. Written before any E7.7 result was seen. Writes results.md.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
SEEDS = list(range(301, 309))
FAMILIES = ("blade", "spear", "club", "carrier", "wrap", "boat", "fired clay", "watertight")


def pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "–"


def main():
    runs = {s: json.loads((HERE / "output" / f"seed_{s}.json").read_text(encoding="utf-8"))
            for s in SEEDS if (HERE / "output" / f"seed_{s}.json").exists()}
    L = []
    w = L.append
    w("# E7.7 — Exposure and reproduction audit · Results\n")
    w("Read-only replays of the eight E7 worlds (E7 code), first 300 years. Predictions frozen in predictions.md "
      "(tag `E7.7-frozen`) before any run. Pooled over worlds unless stated.\n")

    w("## Validity\n")
    verify = (HERE / "output" / "verify.txt").read_text(encoding="utf-8").strip().splitlines() \
        if (HERE / "output" / "verify.txt").exists() else []
    ok_ro = bool(verify) and all("READ-ONLY" in v for v in verify)
    ok_rep = bool(runs) and all(r["replay_matches_saved"] for r in runs.values())
    ok_code = bool(runs) and all(r["code_hash"] == r["code_hash_after"] for r in runs.values())
    w(f"- Probe read-only (20 years): **{'yes' if ok_ro else 'NO'}** ({'; '.join(verify) or 'not run'})")
    w(f"- Every replay matches its saved run: **{'yes' if ok_rep else 'NO'}** ({sum(r['replay_matches_saved'] for r in runs.values())} of {len(runs)})")
    w(f"- Code unchanged during the runs: **{'yes' if ok_code else 'NO'}**")
    w(f"- **The audit is {'valid' if ok_ro and ok_rep and ok_code and len(runs) == 8 else 'INVALID or incomplete'}.**\n")

    pooled = {}
    for f in FAMILIES:
        acc = Counter()
        how_learn, how_carry, how_exp, how_all, watch = Counter(), Counter(), Counter(), Counter(), Counter()
        for r in runs.values():
            d = r["families"][f]
            for k in ("objects", "people_carried", "people_beside_only", "beside_only_later_knew", "exposed_before_knowing",
                      "later_learned", "later_made", "never_learned", "inherited_first", "inherited_first_later_made",
                      "ever_knew", "knew_and_made"):
                acc[k] += d[k]
            how_learn.update(d["learned_how"]); how_carry.update(d["carried_first_how"])
            how_exp.update(d["exposure_how"]); how_all.update(d["recipe_first_how_all"]); watch.update(d["watching"])
        pooled[f] = (acc, how_learn, how_carry, how_exp, how_all, watch)

    w("## The chain, family by family\n")
    w("| family | objects | people carried | lived beside only | exposed before knowing | → later learned | → later made | never learned | knew a recipe | knew but never made |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for f, (a, *_rest) in pooled.items():
        w(f"| {f} | {a['objects']} | {a['people_carried']} | {a['people_beside_only']} | {a['exposed_before_knowing']} | "
          f"{a['later_learned']} ({pct(a['later_learned'], a['exposed_before_knowing'])}) | "
          f"{a['later_made']} ({pct(a['later_made'], a['exposed_before_knowing'])}) | {a['never_learned']} | {a['ever_knew']} | "
          f"{a['ever_knew'] - a['knew_and_made']} ({pct(a['ever_knew'] - a['knew_and_made'], a['ever_knew'])}) |")
    w("")
    w("## How people first came by things, and by recipes\n")
    w("| family | first carried by (made / inherited / fire-hardened / other) | first recipe by (play / taught / read / copied / heated) |")
    w("|---|---|---|")
    for f, (a, hl, hc, he, ha, wt) in pooled.items():
        w(f"| {f} | {hc['made']} / {hc['inherited']} / {hc['fire-hardened']} / {hc['other']} | "
          f"{ha['found in play']} / {ha['taught']} / {ha['read']} / {ha['copied']} / {ha['heated']} |")
    w("")
    w("## Watching\n")
    w("| family | times watched | person watched knew the recipe | good outcome seen | copies made |")
    w("|---|---|---|---|---|")
    for f, (*_x, wt) in pooled.items():
        if wt:
            w(f"| {f} | {wt['watched']} | {wt['maker_knew']} | {wt['good_outcome']} | {wt['copied']} |")
    w("")
    kept = Counter()
    for r in runs.values():
        kept.update(r.get("kept_after_play", {}))
    sk, sf, ck, cf = kept["simple/kept"], kept["simple/forgotten"], kept["composite/kept"], kept["composite/forgotten"]
    w("## Kept after making\n")
    w(f"- Simple things made in play: kept {sk}, forgotten {sf} ({pct(sk, sk + sf)} kept).")
    w(f"- Composite things made in play: kept {ck}, forgotten {cf} ({pct(ck, ck + cf)} kept).\n")
    w("Note: a 30-year test of the probe on seed 308, run after prediction 6 was written and before freezing, showed "
      "91% vs 54%. Those weeks are part of the data above.\n")

    w("## Frozen predictions, scored\n")

    def score(ok):
        return "**confirmed**" if ok else "**wrong**"

    det1, ok1 = [], True
    for f, (a, *_r) in pooled.items():
        if f in ("carrier", "boat") or not a["exposed_before_knowing"]:
            continue
        share = a["later_made"] / a["exposed_before_knowing"]
        ok1 &= share < 0.2
        det1.append(f"{f} {pct(a['later_made'], a['exposed_before_knowing'])}")
    w(f"1. {score(ok1 and bool(det1))} — exposed without a recipe who later made one: " + ", ".join(det1) + ".")
    inh = sum(p[0]["inherited_first"] for p in pooled.values())
    inh_m = sum(p[0]["inherited_first_later_made"] for p in pooled.values())
    w(f"2. {score(inh > 0 and inh_m / inh < 0.1)} — first contact by inheriting: {inh}; later made one: {inh_m} ({pct(inh_m, inh)})."
      + (" Not scorable as no one's first contact was an inheritance." if not inh else ""))
    fc = pooled["fired clay"][0]
    w(f"3. {score(fc['people_beside_only'] > 0 and fc['beside_only_later_knew'] / fc['people_beside_only'] < 0.05)} — lived beside fired "
      f"clay only: {fc['people_beside_only']}; later knew how: {fc['beside_only_later_knew']} ({pct(fc['beside_only_later_knew'], fc['people_beside_only'])}).")
    taught = sum(p[4]["taught"] for p in pooled.values())
    copied = sum(p[4]["copied"] for p in pooled.values())
    w(f"4. {score(taught >= 5 * max(copied, 1) if copied else taught > 0)} — first recipes by teaching {taught}, by copying {copied}. "
      "Reading: with no copies at all, any teaching counts as at least five times more.")
    knew = sum(p[0]["ever_knew"] for p in pooled.values())
    knew_m = sum(p[0]["knew_and_made"] for p in pooled.values())
    w(f"5. {score(knew and (knew - knew_m) / knew >= 0.4)} — knew a recipe but never made that family: {knew - knew_m} of {knew} ({pct(knew - knew_m, knew)}).")
    gap = (sk / (sk + sf) - ck / (ck + cf)) if (sk + sf) and (ck + cf) else None
    w(f"6. {score(gap is not None and gap >= 0.2)} — kept after making: simple {pct(sk, sk + sf)} vs composite {pct(ck, ck + cf)}"
      + (f" (gap {100 * gap:.0f} points)." if gap is not None else "."))

    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
