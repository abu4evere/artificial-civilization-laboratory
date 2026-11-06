# DeepSeek's script for LH1's blind recompute (chat fa0480a4-5de5-4332-813d-0482fb6443fb, 5 November 2026).
# DeepSeek had no code tool, said so, gave the pooled point estimates it computed by hand, and wrote this script from
# the prompt and the CSV alone, without seeing analyse_lh1.py. Copied from its reply in pieces; only the indentation
# (lost in the page copy) was restored. Run by the assistant in this folder: python deepseek_script_lh1.py
import numpy as np
import pandas as pd

df = pd.read_csv("lh1_counts.csv")

seeds = np.sort(df["seed"].unique())
arms = ["c", "e", "m"]
cols = [
    "living_weeks", "extinct", "starvation_deaths", "killed_deaths",
    "census_adults", "census_health",
    "m3_g_chains", "m3_g_made", "m3_m_chains", "m3_m_made",
    "makes", "adult_weeks_win"
]

data = {
    a: df[df["arm"] == a].set_index("seed").loc[seeds, cols].astype(float).values
    for a in arms
}


def sums_from_counts(arr, counts):
    return dict(zip(cols, counts @ arr))


def metrics(s, sc):
    L = s["living_weeks"]
    Lc = sc["living_weeks"]

    S = s["starvation_deaths"]
    Sc = sc["starvation_deaths"]

    K = s["killed_deaths"]
    Kc = sc["killed_deaths"]

    A = s["census_adults"]
    Ac = sc["census_adults"]

    H = s["census_health"]
    Hc = sc["census_health"]

    Gch = s["m3_g_chains"]
    Gmade = s["m3_g_made"]
    Mch = s["m3_m_chains"]
    Mmade = s["m3_m_made"]

    Gchc = sc["m3_g_chains"]
    Gmadc = sc["m3_g_made"]
    Mchc = sc["m3_m_chains"]
    Mmadc = sc["m3_m_made"]

    AW = s["adult_weeks_win"]
    AWc = sc["adult_weeks_win"]
    makes = s["makes"]
    makesc = sc["makes"]

    s_rate = 52000.0 * S / L
    sc_rate = 52000.0 * Sc / Lc

    k_rate = 52000.0 * K / L
    kc_rate = 52000.0 * Kc / Lc

    health = H / A
    healthc = Hc / Ac

    m3 = Gmade / Gch - Mmade / Mch
    m3c = Gmadc / Gchc - Mmadc / Mchc

    makes_rate = makes * 52.0 / AW
    makes_ratec = makesc * 52.0 / AWc

    return {
        "living_ratio": L / Lc,
        "extra_extinct": s["extinct"] - sc["extinct"],
        "starv_rate": s_rate,
        "starv_ratio": s_rate / sc_rate,
        "kill_rate": k_rate,
        "kill_diff": k_rate - kc_rate,
        "health_mean": health,
        "health_diff": health - healthc,
        "m3": m3,
        "m3_diff": m3 - m3c,
        "makes_rate": makes_rate,
        "makes_ratio": makes_rate / makes_ratec,
    }


# Full-data point estimates
point_c = sums_from_counts(data["c"], np.ones(len(seeds)))
out_point = {}
for a in ["e", "m"]:
    point_a = sums_from_counts(data[a], np.ones(len(seeds)))
    out_point[a] = metrics(point_a, point_c)

# Bootstrap
rng = np.random.default_rng(12345)
B = 10000
boot = {a: [] for a in ["e", "m"]}

for _ in range(B):
    idx = rng.integers(0, len(seeds), len(seeds))
    counts = np.bincount(idx, minlength=len(seeds)).astype(float)

    sc = sums_from_counts(data["c"], counts)
    for a in ["e", "m"]:
        sa = sums_from_counts(data[a], counts)
        boot[a].append(metrics(sa, sc))


def ci(x):
    return np.percentile(x, [2.5, 97.5])


print("POINT ESTIMATES")
for a in ["e", "m"]:
    print("\n", a, "vs c")
    for k, v in out_point[a].items():
        print(f"{k:16s} point = {v:.8g}")

print("\nBOOTSTRAP 95% INTERVALS")
for a in ["e", "m"]:
    print("\n", a, "vs c")
    for k in out_point[a]:
        arr = np.array([b[k] for b in boot[a]])
        lo, hi = ci(arr)
        print(f"{k:16s} point = {out_point[a][k]:.8g}  95% CI = ({lo:.8g}, {hi:.8g})")


# Guard/reading logic
def reading(a):
    p = out_point[a]
    arrs = {k: np.array([b[k] for b in boot[a]]) for k in p}

    guards = {}

    lo, hi = ci(arrs["living_ratio"])
    guards["living_ratio"] = (p["living_ratio"] < 0.90) and (hi < 1.0)

    lo, hi = ci(arrs["extra_extinct"])
    guards["extra_extinct"] = (p["extra_extinct"] >= 3)

    lo, hi = ci(arrs["starv_ratio"])
    guards["starvation"] = (p["starv_ratio"] > 1.25) and (lo > 1.0)

    lo, hi = ci(arrs["kill_diff"])
    guards["killing"] = (p["kill_diff"] > 0.05) and (lo > 0.0)

    lo, hi = ci(arrs["health_diff"])
    guards["health"] = (p["health_diff"] < -5.0) and (hi < 0.0)

    lo, hi = ci(arrs["m3_diff"])
    co_m3 = lo > 0.0

    lo, hi = ci(arrs["makes_ratio"])
    co_makes = lo > 1.0

    supported = (not any(guards.values())) and co_m3 and co_makes
    return guards, co_m3, co_makes, supported


for a in ["e", "m"]:
    print("\nREADING", a)
    print(reading(a))
