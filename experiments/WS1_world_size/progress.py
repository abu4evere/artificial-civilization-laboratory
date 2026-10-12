"""Watch S1's progress (read-only): worlds finished per arm, pace, and time left. Prints every few minutes until done.
  python experiments/S1_world_size/progress.py [minutes between reports]"""
import sys, time
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path(__file__).parent / "output"
ARMS, TOTAL = ("c", "l", "lp", "p", "s"), 1280
every = float(sys.argv[1]) if len(sys.argv) > 1 else 5
# relative cost of one world per arm, from the runtime pilot (seconds)
COST = {"c": 220, "l": 569, "lp": 965, "p": 474, "s": 220}
start_t, start_done = time.time(), None
while True:
    n = {a: len(list(OUT.glob(f"{a}_seed_*.json"))) for a in ARMS}
    done = sum(n.values())
    work_left = sum(COST[a] * (256 - n[a]) for a in ARMS)
    work_done = sum(COST[a] * n[a] for a in ARMS)
    if start_done is None:
        start_done = work_done
    rate = (work_done - start_done) / max(1, time.time() - start_t)      # pilot-seconds of work per real second
    eta = f"~{timedelta(seconds=int(work_left / rate))} left" if rate > 0 else "measuring pace…"
    print(f"{datetime.now():%H:%M}  {done}/{TOTAL} worlds ({done / TOTAL:.0%})  "
          + "  ".join(f"{a.upper()} {n[a]}/256" for a in ARMS) + f"  |  {eta}", flush=True)
    if done >= TOTAL:
        print("S1 main run complete.", flush=True)
        break
    time.sleep(every * 60)
