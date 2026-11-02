"""Builds the blind-recompute file for KL1: per seed, the raw counts for the primary: world-level losses by cause
(death, forgetting, mixed; all kinds) and revivals of markable kinds (through reading, and in total). Written before
data.

  python experiments/KL1_knowledge_loss/recompute/build_kl1_one_file.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["seed,loss_death,loss_forgetting,loss_mixed,markable_revivals_read,markable_revivals_all"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "k_seed_*.json"))):
    r = json.load(open(f))
    wl = [sum(v[j] for v in r["world_losses"].values()) for j in range(3)]
    mk = r["revivals"].get("1", {})
    rows.append(f"{r['seed']},{wl[0]},{wl[1]},{wl[2]},{mk.get('read', 0)},{sum(mk.values())}")
(HERE / "kl1_one_file.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "seeds")
