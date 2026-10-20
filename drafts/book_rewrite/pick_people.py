"""Pick candidates for each later chapter from people_<seed>.json (read-only summaries of replayed worlds)."""
import json
import sys
from collections import defaultdict
from pathlib import Path

WPY = 52


def load(seed):
    return json.loads((Path(__file__).parent / f"people_{seed}.json").read_text(encoding="utf-8"))


def name(d, pid):
    return d["people"][pid]["name"] if pid in d["people"] else pid


def show(seed):
    d = load(seed)
    P, E = d["people"], d["events"]
    death = {e["a"]: e for e in E if e["k"] == "death"}
    makes = defaultdict(int)
    for e in E:
        if e["k"] == "make":
            makes[e["a"]] += 1
    print(f"== seed {seed}: ended year {d['end_year']}, alive {d['alive_at_end']}, people {len(P)}")
    # Ch10: knew many recipes, made almost nothing, long adult life
    rows = []
    for pid, p in P.items():
        dt = death.get(pid)
        life = (dt["age"] if dt else d["end_year"] - p["birth_year"])
        if life >= 40 and d["recipes_max"].get(pid, 0) >= 8:
            rows.append((makes[pid], -d["recipes_max"][pid], pid, life))
    for mk, rec, pid, life in sorted(rows)[:3]:
        print(f"  ch10: {name(d, pid)} lived {life:.0f}y, knew up to {-rec} recipes, made {mk} things;"
              f" died of {death[pid]['cause'] if pid in death else '(alive)'}")
    # Ch11: small children starved in winter, with their mother's food at that winter's start
    for e in E:
        if e["k"] == "death" and e["cause"] == "starvation" and e["age"] is not None and e["age"] < 5:
            season = (e["t"] // 13) % 4
            if season in (3, 0):
                c = P.get(e["a"], {})
                m = c.get("mother")
                yr = e["t"] // WPY
                food = d["food_at_winter"].get(f"{m}|{yr if season == 3 else yr - 1}")
                sibs_dead = sum(1 for x in E if x["k"] == "death" and P.get(x["a"], {}).get("mother") == m
                                and abs(x["t"] - e["t"]) < 26 and x["a"] != e["a"])
                print(f"  ch11: {name(d, e['a'])} ({c.get('sex')}), {e['age']}y, starved year {yr} "
                      f"{'winter' if season == 3 else 'spring'}; mother {name(d, m) if m else '?'} held {food} at winter start;"
                      f" others of hers died within half a year: {sibs_dead}; mother alive after: "
                      f"{m not in death or death[m]['t'] > e['t']}")
    # Ch13: the most food given by one person to a brother or sister
    give = defaultdict(float)
    for e in E:
        if e["k"] == "give" and e["a"] in P and e["b"] in P:
            ma, mb = P[e["a"]].get("mother"), P[e["b"]].get("mother")
            if ma and ma == mb:
                give[(e["a"], e["b"])] += e["amount"] or 0
    for (a, b), amt in sorted(give.items(), key=lambda x: -x[1])[:3]:
        back = give.get((b, a), 0)
        print(f"  ch13: {name(d, a)} gave {amt:.0f} food to sibling {name(d, b)} (back {back:.0f})")
    # Ch15: women single longest in their child-bearing years
    for pid, wk in sorted(d["single_weeks"].items(), key=lambda x: -x[1])[:3]:
        kids = sum(1 for x in P.values() if x.get("mother") == pid)
        print(f"  ch15: {name(d, pid)} single {wk / WPY:.0f} of her years 16-40; children {kids};"
              f" {'died of ' + death[pid]['cause'] + ' at ' + str(death[pid]['age']) if pid in death else 'alive at end'}")
    births = [e["t"] / WPY for e in E if e["k"] == "birth"]
    print(f"  births: last in year {max(births):.0f}" if births else "  no births")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        show(int(s))
