"""Nature v16 = v15 + FF4's fault fix (forage, hunt and gather are offered at the best target the person can afford
when the best one is too far; experiments/FF4_affordable_targets/findings.md), without FF4's study logging.

  python experiments/NV16_nature_v16/patch_v16.py <acl folder>      # patches config.py and mind.py in place (CRLF kept)
"""
import sys
from pathlib import Path


def patch(p, reps):
    s = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    for old, new in reps:
        assert s.count(old) == 1, (p, old[:70])
        s = s.replace(old, new)
    p.write_bytes((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))


root = Path(sys.argv[1])
patch(root / "config.py", [(
    "    child_make: int = 1 ",
    "    fix_affordable_target: int = 1     # NV16 (FF4): 1 = forage, hunt and gather are offered at the best target the\n"
    "                                       # person can afford when the best one is too far (0 = v15: the whole action was\n"
    "                                       # dropped)\n"
    "    child_make: int = 1 ")])
patch(root / "mind.py", [
    ('''        best, best_u, best_d = None, -1.0, 0
        for t in tiles:
            d = distance(p.loc, t, w, h)
            tile = world.tile(t)
            got = min(tile.plants + tile.crop, rate) * (1.0 - 0.1 * d)
            u = (0.25 + 1.6 * food_hunger) * min(1.0, got / (need * 1.5)) + 0.08 * g["diligence"]
            if u > best_u:
                best, best_u, best_d = t, u, d
        add("forage", best, best_u, best_d)
        best_forage = best_u
''',
     '''        best, best_u, best_d = None, -1.0, 0
        aff, aff_u, aff_d = None, -1.0, 0       # NV16 (FF4): the best target this person can afford
        for t in tiles:
            d = distance(p.loc, t, w, h)
            tile = world.tile(t)
            got = min(tile.plants + tile.crop, rate) * (1.0 - 0.1 * d)
            u = (0.25 + 1.6 * food_hunger) * min(1.0, got / (need * 1.5)) + 0.08 * g["diligence"]
            if u > best_u:
                best, best_u, best_d = t, u, d
            if u > aff_u and p.energy >= COST["forage"] + MOVE_COST * d:
                aff, aff_u, aff_d = t, u, d
        if c.fix_affordable_target and p.energy < COST["forage"] + MOVE_COST * best_d:
            if aff is not None:
                add("forage", aff, aff_u, aff_d)
        else:
            add("forage", best, best_u, best_d)
        best_forage = best_u
'''),
    ('''        best, best_u, best_d = None, -1.0, 0
        best_n = 1.0
''',
     '''        best, best_u, best_d = None, -1.0, 0
        best_n = 1.0
        aff, aff_u, aff_d, aff_n = None, -1.0, 0, 1.0       # NV16 (FF4): the best target this person can afford
'''),
    ('''            if u > best_u:
                best, best_u, best_d = t, u, d
                best_n = n
        if best is not None:
            add("hunt", best, best_u, best_d)
''',
     '''            if u > best_u:
                best, best_u, best_d = t, u, d
                best_n = n
            if u > aff_u and p.energy >= COST["hunt"] + MOVE_COST * d:
                aff, aff_u, aff_d, aff_n = t, u, d, n
        if (c.fix_affordable_target and best is not None
                and p.energy < COST["hunt"] + MOVE_COST * best_d):
            best, best_u, best_d, best_n = aff, aff_u, aff_d, aff_n
        if best is not None:
            add("hunt", best, best_u, best_d)
'''),
    ('''            best, best_u, best_d = None, 0.0, 0
            for kind in GATHERABLE + (("earth",) if c.digging else ()):''',
     '''            best, best_u, best_d = None, 0.0, 0
            aff, aff_u, aff_d = None, 0.0, 0     # NV16 (FF4): the best target this person can afford
            for kind in GATHERABLE + (("earth",) if c.digging else ()):'''),
    ('''                    if u > best_u:
                        best, best_u, best_d = (t, kind), u, d
            if best is not None:
                add("gather", best, best_u, best_d)
''',
     '''                    if u > best_u:
                        best, best_u, best_d = (t, kind), u, d
                    if u > aff_u and p.energy >= COST["gather"] + MOVE_COST * d:
                        aff, aff_u, aff_d = (t, kind), u, d
            if (c.fix_affordable_target and best is not None
                    and p.energy < COST["gather"] + MOVE_COST * best_d):
                best, best_u, best_d = aff, aff_u, aff_d
            if best is not None:
                add("gather", best, best_u, best_d)
'''),
])
print("patched", root)
