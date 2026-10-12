"""Reproducibility guard: a few reference worlds must replay to exactly the recorded state.

`tests/reference_hashes.json` holds state hashes of short runs of (1) ACL's own code (the live world) and (2) the frozen
control copy used by the experiments (`experiments/E13R_replication/code_e13r`). If ACL's nature is changed on purpose,
regenerate the first set (python tests/test_reference_replays.py --update acl) and say so in the commit; the control copy
is frozen and its hashes should never change.

The hashes were made on Windows with Python 3.14; maths functions such as exp can differ in the last digit between
systems, which can change a rare choice, so the check runs on the same system in CI.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = Path(__file__).with_name("reference_hashes.json")
CODES = {"acl": ROOT, "control": ROOT / "experiments" / "E13R_replication" / "code_e13r"}
CASES = [(11, 5), (501, 5)]          # (seed, years)


def _hash(code: str, seed: int, years: int) -> str:
    """Run in a fresh process, so the two packages named `acl` never meet."""
    extra = ", anticipation_weight=1.0" if code == "control" else ""   # the experiments' setting; ACL's own code has none
    prog = ("import sys; sys.path.insert(0, sys.argv[1]); from acl import Config, World;"
            f"w = World(Config(seed=int(sys.argv[2]){extra}));"
            "[w.step() for _ in range(int(sys.argv[3]) * 52)]; print(w.state_hash())")
    out = subprocess.run([sys.executable, "-c", prog, str(CODES[code]), str(seed), str(years)],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip().splitlines()[-1]


def _check(code: str) -> None:
    ref = json.loads(REF.read_text(encoding="utf-8"))[code]
    for seed, years in CASES:
        assert _hash(code, seed, years) == ref[f"{seed}:{years}"], f"{code} world, seed {seed}, {years} years no longer replays"


def test_acl_reference_worlds_replay():
    _check("acl")


def test_frozen_control_code_replays():
    _check("control")


if __name__ == "__main__" and sys.argv[1:2] == ["--update"]:
    which = sys.argv[2:] or list(CODES)
    data = json.loads(REF.read_text(encoding="utf-8")) if REF.exists() else {}
    for code in which:
        data[code] = {f"{s}:{y}": _hash(code, s, y) for s, y in CASES}
    REF.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=1))
