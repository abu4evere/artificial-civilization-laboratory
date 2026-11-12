"""NB3-A zero check: the recorders are read-only. For each arm, a world run 8 years with NB3's own observer only must
end with the same world fingerprint and generator state as the same world run with the autopsy recorders too.

  python experiments/NB3A_feeding_autopsy/zero_nb3a.py [years]
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
YEARS = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] != "child" else 8


def child(arm, seed, years, rec):
    sys.path.insert(0, str(HERE))
    import run_nb3a as A
    P, base = A.P, A.base
    base.setup(A.CODE)
    w = P.make(seed, arm)
    P.install()
    w.observers.append(P.NB2Obs(w))
    obs = None
    if rec:
        A.install()
        obs = A.Autopsy(w, seed)
        A.CUR[0] = obs
        w.ledger = []
        w.observers.append(obs)
    for _ in range(years * A.WPY):
        w.step()
    extra = ""
    if obs is not None:
        r = obs.results()
        extra = f" starved {len(r['starved'])} survivors {len(r['survivors'])} checks {r['checks']}"
    print(base.world_hash(w) + ":" + base.rng_state(w) + "|" + extra)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "child":
        child(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1")
        sys.exit(0)
    ok = True
    lines = []
    for arm in ("c", "fH", "f"):
        outs = []
        for rec in (0, 1):
            r = subprocess.run([sys.executable, __file__, "child", arm, "25801", str(YEARS), str(rec)],
                               capture_output=True, text=True)
            if r.returncode:
                print(r.stderr[-3000:])
                sys.exit(1)
            outs.append(r.stdout.strip().splitlines()[-1])
        same = outs[0].split("|")[0] == outs[1].split("|")[0]
        ok &= same
        lines.append(f"arm {arm}, seed 25801, {YEARS} years: recorders read-only (same fingerprint and generator): "
                     f"{'yes' if same else 'NO'};{outs[1].split('|')[1]}")
    # the checkpoint continues exactly: 3 years in one job = 1 year, a checkpoint, and 2 more years in a second job
    import json
    import tempfile
    me = [sys.executable, str(HERE / "run_nb3a.py")]
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        a = subprocess.run(me + ["one", "f", "25802", "3", str(td / "a")], capture_output=True, text=True)
        b1 = subprocess.run(me + ["part", "f", "25802", "3", str(td / "b"), str(td / "ck"), "-1"],
                            capture_output=True, text=True)
        b2 = subprocess.run(me + ["part", "f", "25802", "3", str(td / "b"), str(td / "ck"), "1e9"],
                            capture_output=True, text=True)
        same_ck = False
        if not (a.returncode or b1.returncode or b2.returncode):
            ra = json.loads((td / "a" / "f_seed_25802.json").read_text())
            rb = json.loads((td / "b" / "f_seed_25802.json").read_text())
            jobs = rb.pop("jobs", None)
            ra.pop("jobs", None)
            same_ck = ra == rb and jobs == 2
        else:
            print((a.stderr + b1.stderr + b2.stderr)[-3000:])
    ok &= same_ck
    lines.append(f"arm f, seed 25802: 3 years in one job = 1 year, a checkpoint, and 2 years in a second job (every "
                 f"record equal): {'yes' if same_ck else 'NO'}")
    fp = subprocess.run(me + ["fp"], capture_output=True, text=True).stdout.split()[-1]
    lines.append(f"code_nb3 fingerprint: {fp}")
    lines.append(f"All: {'PASS' if ok else 'FAIL'}")
    text = "\n".join(lines) + "\n"
    (HERE / "zero_local.log").write_text(text, encoding="utf-8")
    print(text)
