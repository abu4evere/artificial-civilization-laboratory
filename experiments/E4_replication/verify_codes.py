"""Kill-criterion check: each code must still reproduce its original experiment (seed 108, year 100).
Usage: python verify_codes.py <e1|e2>"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
CODE = sys.argv[1]
sys.path.insert(0, str(ROOT / "experiments" / "E3_births" / "code_e1") if CODE == "e1" else str(ROOT))
from acl.config import WEEKS_PER_YEAR, Config  # noqa: E402
from acl.historian import Historian  # noqa: E402
from acl.measure import Lab  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402
from acl.world import World  # noqa: E402

w = World(Config(seed=108))
h = Historian()
w.observers += [h, Lab(h)]
for _ in range(100 * WEEKS_PER_YEAR):
    w.step()
exp = "E1" if CODE == "e1" else "E2"
saved, _ = load_snapshot(ROOT / "experiments" / exp / "output" / "seed_108_year100.json.gz")
print(f"{CODE} reproduces {exp} seed 108 at year 100: {saved.state_hash() == w.state_hash()}")
