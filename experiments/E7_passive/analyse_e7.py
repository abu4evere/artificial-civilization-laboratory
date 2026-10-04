"""E7 analysis: apply the frozen definitions, decision rule, predictions and kill criteria in E7_passive.md.
Read-only. Writes results.md.

Written before any E7 run was seen. Operational readings of the spec's wording are marked "Reading:" in the
output, so they can be argued with.
"""
from __future__ import annotations

import json
from pathlib import Path

from run_e7 import CODE, SEEDS, code_hash

HERE = Path(__file__).parent
OUT = HERE / "output"
E6_OUT = HERE.parent / "E6_novelty" / "output" / "e6"
E6_HASH = "b3f7153accc0e681"          # E6 code fingerprint recorded in E6's results.md


def load(folder: Path) -> dict:
    runs = {}
    for s in SEEDS:
        f = folder / f"seed_{s}.json"
        if f.exists():
            runs[s] = json.loads(f.read_text(encoding="utf-8"))
    return runs


def fmt(v):
    return "–" if v is None else str(v)


def main():
    e7, base, e6 = load(OUT / "e7"), load(OUT / "baseline"), load(E6_OUT)
    lines = []
    w = lines.append

    w("# E7 — Passive affordances · Results\n")
    w("Design, definitions, predictions and decision rule were frozen in E7_passive.md before any run. "
      "Implementation fixes made before the runs are listed in implementation_notes.md. "
      "LFA = first year of the latest lasting novelty (E6 definition).\n")

    # --- validity -----------------------------------------------------------------------------------------
    w("## Validity (kill criteria, §9)\n")
    verify = (OUT / "verify.txt").read_text(encoding="utf-8").strip().splitlines() if (OUT / "verify.txt").exists() else []
    ro = bool(verify) and all("READ-ONLY" in v for v in verify) and len(verify) >= 2
    he7, hb = code_hash(CODE["e7"] / "acl"), code_hash(CODE["baseline"] / "acl")
    same7 = bool(e7) and all(r["code_hash"] == r["code_hash_after"] == he7 for r in e7.values())
    sameb = bool(base) and all(r["code_hash"] == r["code_hash_after"] == hb for r in base.values())
    base_is_e6 = hb.startswith(E6_HASH)
    repl = {}
    for s, r in base.items():
        if s in e6:
            repl[s] = ([x["population"] for x in r["samples"]] == [x["population"] for x in e6[s]["samples"]]
                       and r["LFA"] == e6[s]["LFA"])
    crashed = [f"{a} {s}" for a, runs in (("e7", e7), ("baseline", base)) for s in SEEDS if s not in runs]
    checks = [
        ("Recorder read-only (state hash with and without it, 20 years, both arms)", ro, "; ".join(verify) or "not run"),
        ("E7 code unchanged during the runs", same7, he7[:16]),
        ("Baseline code unchanged during the runs, and it is E6's verified code", sameb and base_is_e6, hb[:16]),
        ("No world crashed or failed to finish", not crashed, ", ".join(crashed) or "all 16 finished"),
        ("At least 6 worlds completed in each arm", len(e7) >= 6 and len(base) >= 6, f"E7 {len(e7)}, baseline {len(base)}"),
        ("Baseline replicates E6 (population every 10 years and LFA)", bool(repl) and all(repl.values()),
         ", ".join(f"{s} {'yes' if ok else 'NO'}" for s, ok in sorted(repl.items()))),
    ]
    for name, ok, detail in checks:
        w(f"- {name}: **{'yes' if ok else 'NO'}** ({detail})")
    valid = all(ok for _, ok, _ in checks)
    w(f"- **The experiment is {'valid' if valid else 'INVALID'}.**\n")

    # --- per world ----------------------------------------------------------------------------------------
    w("## World by world\n")
    w("| seed | baseline lived | baseline LFA | E7 lived | **E7 LFA** | E7 later? | FEC water | FEC ceramic | FEC food by fire "
      "| carried-water drinks | ≥3 tiles | ≥5 tiles | max tiles | fired objects | outlived maker | new traditions after yr 100 |")
    w("|" + "---|" * 16)
    for s in SEEDS:
        b, e = base.get(s), e7.get(s)
        if not e:
            w(f"| {s} | " + " | ".join(["–"] * 15) + " |")
            continue
        later = (e["LFA"] or -1) > (b["LFA"] or -1) if b else None
        wc, fs = e["water_carried"], e["fired_summary"]
        w(f"| {s} | {fmt(b and b['years_run'])} | {fmt(b and b['LFA'])} | {e['years_run']} | **{fmt(e['LFA'])}** | "
          f"{fmt(None if later is None else ('yes' if later else 'no'))} | {e['fec']['water_passive']} | "
          f"{e['fec']['ceramic_passive']} | {e['fec']['food_by_fire']} | {wc['drinks']} | {wc['drinks_3plus']} | "
          f"{wc['drinks_5plus']} | {fmt(wc['max_tiles'])} | {fs['objects']} | {fs['outlived_maker']} | "
          f"{len(e['new_traditions'])} |")
    w("")

    if e7:
        w("Lasting novelties first appearing in each century (all worlds pooled):\n")
        w("| century | 0–100 | " + " | ".join(f"{100 * i + 1}–{100 * i + 100}" for i in range(1, 10)) + " |")
        w("|---|" + "---|" * 10)
        for name, runs in (("baseline", base), ("E7", e7)):
            counts = [0] * 10
            for r in runs.values():
                for n in r["novelties"]:
                    if n["lasting"]:
                        fy = n["first_year"]
                        counts[0 if fy <= 100 else min(9, (fy - 1) // 100)] += 1
            w(f"| {name} | " + " | ".join(map(str, counts)) + " |")
        w("")

    # --- decision rule ------------------------------------------------------------------------------------
    w("## The frozen decision rule (§7)\n")
    counted = {s: r for s, r in e7.items() if r["years_run"] >= 300}
    half = (len(counted) + 1) // 2
    late = [s for s, r in counted.items() if r["LFA"] is not None and r["LFA"] >= 150]
    early = [s for s, r in counted.items() if r["LFA"] is None or r["LFA"] <= 50]
    pairs_later = [s for s in SEEDS if s in e7 and s in base and (e7[s]["LFA"] or -1) > (base[s]["LFA"] or -1)]
    carried5 = [s for s, r in counted.items() if r["water_carried"]["drinks_5plus"] > 0]
    carried_any = [s for s, r in e7.items() if r["water_carried"]["drinks"] > 0]
    w(f"- Counted E7 worlds (lived 300+ years): {len(counted)} ({', '.join(map(str, counted)) or 'none'}); half = {half}.")
    w(f"- Counted worlds with LFA ≥ 150: {len(late)} ({', '.join(map(str, late)) or 'none'}).")
    w(f"- Counted worlds with LFA ≤ 50 (or no lasting novelty): {len(early)} ({', '.join(map(str, early)) or 'none'}).")
    w(f"- Seed pairs where E7's LFA is later than the baseline's: {len(pairs_later)} of 8.")
    w(f"- Counted worlds with water drunk 5+ tiles from fresh water: {len(carried5)}.")
    w(f"- Worlds where carried water was drunk at all: {len(carried_any)}.")
    if not counted:
        verdict = "UNDECIDABLE (no E7 world lived 300 years)"
    elif len(late) >= half and len(pairs_later) >= 6 and len(carried5) >= 3:
        verdict = "BREAKTHROUGH"
    elif len(early) >= half or not carried_any:
        verdict = "BOTTLENECK REMAINS"
    else:
        verdict = "PARTIAL"
    w(f"- Reading: \"water never carried in any world\" means no drink from a carried vessel in any E7 world.")
    w(f"- **Verdict: {verdict}.**\n")

    # --- failure modes ------------------------------------------------------------------------------------
    if verdict != "BREAKTHROUGH" and e7:
        w("## Failure mode (§7)\n")
        fw = sum(r["fec"]["water_passive"] for r in e7.values())
        fc = sum(r["fec"]["ceramic_passive"] for r in e7.values())
        trad = sum(len(r["new_traditions"]) for r in e7.values())
        w(f"- Pooled FEC: water {fw}, ceramic {fc}. New traditions after year 100: {trad}.")
        w("- Reading: the thresholds are applied to totals pooled over the 8 worlds; per-world counts are in the table.")
        if fw == 0 or fc == 0:
            w(f"- **Failure Mode A (physical starvation)**: the world made {'no passive water' if fw == 0 else 'no passive ceramic'} encounters.")
        elif (fw >= 50 or fc >= 20) and trad == 0 and len(early) >= half:
            w("- **Failure Mode B (cultural / cognitive detachment)**: encounters were plentiful, but no lasting traditions formed and LFA stayed early.")
        else:
            w("- Neither failure mode's definition is met exactly; see the per-world table.")
        w("")

    # --- predictions --------------------------------------------------------------------------------------
    w("## Frozen predictions, scored (§8)\n")

    def score(ok):
        return "**confirmed**" if ok else "**wrong**"

    r304 = e7.get(304)
    if r304:
        filled_by_50 = (r304["fec_first_year"].get("water_passive") is not None
                        and r304["fec_first_year"]["water_passive"] <= 50)
        wc = r304["water_carried"]
        span = (wc["last_year_3plus"] - wc["first_year_3plus"]) if wc["first_year_3plus"] is not None else 0
        ok1 = filled_by_50 and wc["drinks_3plus"] > 0 and span >= 50
        w(f"1. {score(ok1)} — seed 304: first passive fill year {fmt(r304['fec_first_year'].get('water_passive'))}; "
          f"drinks 3+ tiles from fresh water {wc['drinks_3plus']}, from year {fmt(wc['first_year_3plus'])} to "
          f"{fmt(wc['last_year_3plus'])}. Reading: \"lasting tradition\" = such drinks spanning 50+ years.")
    else:
        w("1. not scorable — seed 304 did not finish.")
    passive_any = any(r["fec"]["ceramic_passive"] > 0 for r in e7.values())
    long_lived = sum(r["fired_summary"]["over_50y_and_outlived"] for r in e7.values())
    w(f"2. {score(passive_any and long_lived > 0)} — passive firing happened in "
      f"{sum(1 for r in e7.values() if r['fec']['ceramic_passive'] > 0)} worlds; fired objects carried 50+ years "
      f"that outlived their maker: {long_lived}.")
    fw10 = sum(1 for r in e7.values() if r["fec"]["water_passive"] >= 10)
    fc5 = sum(1 for r in e7.values() if r["fec"]["ceramic_passive"] >= 5)
    w(f"3. {score(fw10 >= 6 and fc5 >= 4)} — FEC water ≥ 10 in {fw10} of 8 worlds (needs 6); "
      f"FEC ceramic ≥ 5 in {fc5} of 8 (needs 4).")
    lfa100 = sum(1 for r in e7.values() if r["LFA"] is not None and r["LFA"] > 100)
    w(f"4. {score(lfa100 >= 4)} — E7 LFA after year 100 in {lfa100} of 8 worlds (needs 4).")
    w(f"5. {score(len(pairs_later) >= 6)} — E7 LFA later than baseline in {len(pairs_later)} of 8 pairs (needs 6).")
    surv = [s for s, r in e7.items() if not r["extinct"] and r["years_run"] >= 1000]
    bsurv = [s for s, r in base.items() if not r["extinct"] and r["years_run"] >= 1000]
    w(f"6. {score(len(surv) >= 4 and len(surv) >= len(bsurv))} — E7 worlds alive at year 1000: {len(surv)} "
      f"({', '.join(map(str, surv)) or 'none'}); baseline: {len(bsurv)}.")
    trad_worlds = [s for s in surv if e7[s]["new_traditions"]]
    w(f"7. {score(len(trad_worlds) >= 3)} — surviving worlds with a new tradition originating after year 100: "
      f"{len(trad_worlds)} (needs 3).")
    w("")
    w("New Consequence 3 (food eaten past its natural rot threshold) is not measurable in this world: food is "
      "one pooled amount per person with no age. `food_by_fire` counts person-weeks with food beside a fire, "
      "where the existing smoke rule already slows rot.")

    (HERE / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    main()
