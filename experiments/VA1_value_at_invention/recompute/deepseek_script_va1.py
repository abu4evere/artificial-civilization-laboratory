# DeepSeek's script for VA1's blind recompute (chat a6401531-9e18-4516-85d8-e45784b750b3, 5 November 2026).
# DeepSeek had no code tool, said so, and declined to give numbers; it wrote this script from the prompt and the CSV
# alone, without seeing analyse_va1.py. Copied from its reply; only the indentation (lost in the page copy) was
# restored. Run by the assistant in this folder: python deepseek_script_va1.py
import pandas as pd
import numpy as np

# Load only the attached file
df = pd.read_csv("va1_kinds.csv")

# Coerce numeric columns; blanks become NaN
num_cols = [
    "seed", "full", "minval", "vsim", "vmean",
    "used_before_loss", "n_uses", "first_felt", "held_first_week"
]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["full"] = df["full"].astype(int)

seeds = df["seed"].unique()
groups = {s: df[df["seed"] == s].copy() for s in seeds}


def compute_stats(d):
    out = {}

    # (1) Share used_before_loss == 1
    out["share_used_before_loss"] = (d["used_before_loss"] == 1).mean()

    # (2a) actual survival: mean held_first_week where not blank
    h = d["held_first_week"].dropna()
    out["actual_held_first_week"] = h.mean() if len(h) else np.nan

    # (2b) v_first: among n_uses > 0, full == 0 OR first_felt > minval
    q = d[d["n_uses"] > 0].copy()
    v_first_cond = (q["full"] == 0) | (q["first_felt"] > q["minval"])
    out["v_first"] = v_first_cond.mean() if len(q) else np.nan

    # (2c) v_sim: among vsim present, full == 0 OR vsim > minval
    q2 = d[d["vsim"].notna()].copy()
    v_sim_cond = (q2["full"] == 0) | (q2["vsim"] > q2["minval"])
    out["v_sim"] = v_sim_cond.mean() if len(q2) else np.nan

    # (3) Pearson corr vsim vs first_felt among n_uses > 0 and vsim present
    c = d[
        (d["n_uses"] > 0) &
        d["vsim"].notna() &
        d["first_felt"].notna()
    ].copy()

    if (
        len(c) >= 2 and
        c["vsim"].std(ddof=1) > 0 and
        c["first_felt"].std(ddof=1) > 0
    ):
        out["corr_vsim_first_felt"] = c["vsim"].corr(c["first_felt"])
    else:
        out["corr_vsim_first_felt"] = np.nan

    return out


# Point estimates on the full observed data
point = compute_stats(df)

# Point-only vmean correlation among same eligible rows
c_point = df[
    (df["n_uses"] > 0) &
    df["vsim"].notna() &
    df["vmean"].notna() &
    df["first_felt"].notna()
].copy()

corr_vmean_first_felt = c_point["vmean"].corr(c_point["first_felt"])

# World bootstrap: draw 32 seeds with replacement, pool kinds with multiplicity
rng = np.random.default_rng(20240517)
B = 10_000
boot_rows = []

for b in range(B):
    draw = rng.choice(seeds, size=len(seeds), replace=True)
    d_boot = pd.concat([groups[s] for s in draw], ignore_index=True)
    boot_rows.append(compute_stats(d_boot))

boot = pd.DataFrame(boot_rows)


def ci(col):
    return (
        boot[col].quantile(0.025),
        boot[col].quantile(0.975)
    )


used_lo, used_hi = ci("share_used_before_loss")
actual_lo, actual_hi = ci("actual_held_first_week")
vfirst_lo, vfirst_hi = ci("v_first")
vsim_lo, vsim_hi = ci("v_sim")
corr_lo, corr_hi = ci("corr_vsim_first_felt")

# Reading for (1)
if point["share_used_before_loss"] < 0.5 and used_hi < 0.5:
    used_reading = "unvalued at birth dominates"
else:
    used_reading = "not shown"

# Reading for (3)
if corr_lo > 0.2 and point["corr_vsim_first_felt"] > corr_vmean_first_felt:
    similarity_reading = "similar experience is informative"
elif corr_lo > 0.2 and corr_vmean_first_felt >= point["corr_vsim_first_felt"]:
    similarity_reading = "experience is informative, but not its similarity"
else:
    similarity_reading = "not shown"

print("N rows:", len(df))
print("N worlds:", len(seeds))
print()

print("(1) Share used_before_loss = 1")
print("point:", point["share_used_before_loss"])
print("95% world-bootstrap CI:", (used_lo, used_hi))
print("reading:", used_reading)
print()

print("(2) Share surviving at invention under three first values")
print("actual = mean held_first_week:")
print(" point:", point["actual_held_first_week"])
print(" 95% CI:", (actual_lo, actual_hi))
print("v_first = full==0 or first_felt > minval among n_uses>0:")
print(" point:", point["v_first"])
print(" 95% CI:", (vfirst_lo, vfirst_hi))
print("v_sim = full==0 or vsim > minval among vsim present:")
print(" point:", point["v_sim"])
print(" 95% CI:", (vsim_lo, vsim_hi))
print()

print("(3) Correlation with first_felt among n_uses>0 and vsim present")
print("Pearson corr vsim vs first_felt:")
print(" point:", point["corr_vsim_first_felt"])
print(" 95% CI:", (corr_lo, corr_hi))
print("Pearson corr vmean vs first_felt, point only:")
print(" point:", corr_vmean_first_felt)
print("reading:", similarity_reading)
