def reload_check(seed):
    w = make(seed, "f")
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    from acl import brain_nb2, brain_nb3
    for d in (brain_nb2.LAST, brain_nb2.CHOSEN, brain_nb2.OBS, brain_nb3.APPR):
        d.clear()
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b) and b.cfg.nb3 == 1


def ckpt_check(seed):
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        a = subprocess.run([sys.executable, str(Path(__file__).resolve()), "one", "f", str(seed), "15", str(td / "a")],
                           capture_output=True, text=True)
        me = [sys.executable, str(Path(__file__).resolve()), "part", "f", str(seed), "15", str(td / "b"), str(td / "ck")]
        b1 = subprocess.run(me + ["-1"], capture_output=True, text=True)
        b2 = subprocess.run(me + ["1e9"], capture_output=True, text=True)
        if a.returncode or b1.returncode or b2.returncode:
            return False
        ra = json.loads((td / "a" / f"f_seed_{seed}.json").read_text())
        rb = json.loads((td / "b" / f"f_seed_{seed}.json").read_text())
        ra.pop("jobs", None)
        jobs = rb.pop("jobs", None)
        return ra == rb and jobs == 2


def unit_check(seed, years=8):
    """NB3's feelings against independent readings: the feeling genes come from the same parent as the network genome,
    within the mutation, in [0, 2]; attack and steal options carry -H in their score unless in defence; guilt rises by
    the frozen amounts for an attack one starts and not in defence; empathy, guilt and approval parts of the feeling
    equal an independent computation in sampled weeks."""
    import numpy as np
    w = make(seed, "f")
    from acl import brain_nb2 as b2, brain_nb3 as b3, actions
    st = Counter()
    child0, rescore0, feel0, attack0 = b2.child, b2.rescore, b3.feel, actions._attack
    handler0 = actions.HANDLERS["attack"]

    def child(world, mother, father):
        out = child0(world, mother, father)
        par = [x for x in (mother, father) if x is not None and x.nb is not None]
        if par and st["child_looks"] < 200:
            g = np.asarray(out["genome"])
            src = min(par, key=lambda x: float(np.abs(g - np.asarray(x.nb["genome"])).max()))
            st["child_looks"] += 1
            for k in b3.GENES:
                if not (0.0 <= out[k] <= b3.GENE_MAX) or abs(out[k] - src.nb[k]) > 6 * b3.GENE_SD:
                    st["gene_bad"] += 1
        return out

    def rescore(world, p, options, near, hunger, fatigue, lw, base_):
        new = rescore0(world, p, options, near, hunger, fatigue, lw, base_)
        if p.nb is not None and new is not options and st["hb_looks"] < 400:
            from acl.person import A
            X = b2.LAST[(id(world), p.id)][0]
            net = b2.actor_scores(p.nb["w"], X)[0]
            for k, ((s, a, t), n) in enumerate(zip(options, new)):
                hand = p.nb["g"] * (s - lw * p.q[base_ + A[a]])
                bias = n[0] - hand - float(net[k])
                expect = 0.0
                if a in ("attack", "steal"):
                    expect = -p.nb["H"]
                    if a == "attack" and isinstance(t, str) and t in world.people and b3.defence(world, p, world.people[t]):
                        expect = 0.0
                    st["hb_harm_options"] += 1
                if abs(bias - expect) > 1e-9:
                    st["hb_mismatch"] += 1
            st["hb_looks"] += 1
        return new

    def attack(world, p, target, eff):
        q = world.people.get(target)
        g0 = p.nb.get("guilt", 0.0) if p.nb is not None else None
        defending = q is not None and b3.defence(world, p, q)
        kin = q is not None and world.kinship(p, q) > 0
        out = attack0(world, p, target, eff)
        if p.alive and p.nb is not None and q is not None and g0 is not None and st["guilt_looks"] < 300:
            want = 0.0 if defending else 0.3 + ((1.0 * (2.0 if kin else 1.0)) if not q.alive else 0.0)
            if abs((p.nb.get("guilt", 0.0) - g0) - want) > 1e-9:
                st["guilt_mismatch"] += 1
            st["guilt_looks"] += 1
        return out

    def feel(world, p):
        snap = None
        if p.nb is not None and st["feel_looks"] < 300:
            nb = p.nb
            c = world.cfg
            num = den = 0.0
            for q in world.people_near(p.loc, c.reach, exclude=p.id):
                kin = world.kinship(p, q) > 0 or p.partner == q.id
                r = p.rel.get(q.id)
                wt = 1.0 if kin else (0.5 if r is not None and r.affection > 0.3 else 0.2)
                if q.nb is None:
                    last = b3.distress(world, q)
                elif q.nb.get("d_week") == world.tick:
                    last = q.nb.get("d_last", q.nb.get("d_now", 0.0))
                else:
                    last = q.nb.get("d_now", b3.distress(world, q))
                d = b3.distress(world, q)
                num += wt * (max(0.0, d - last) + 0.25 * d)
                den += wt
            emp = -nb["E"] * num / den if den else 0.0
            snap = emp - nb["G"] * nb.get("guilt", 0.0) + nb["A"] * b3.APPR.get((id(world), p.id), 0.0)
            # love and curiosity, computed independently
            tick = world.tick
            young = [world.people[k] for k in p.children if world.people[k].alive and world.people[k].age(tick) < 12 * 52]
            love = 0.0
            if young:
                small = [k for k in young if k.age(tick) < 6 * 52]
                well = 0.0
                if small:
                    good = 0
                    for k in small:
                        carer = world.people.get(k.caregiver)
                        if k.edible() >= 0.5 * k.need(c, tick) and k.health >= 50 and carer is not None and carer.loc == k.loc:
                            good += 1
                    well = good / len(small)
                love = well - 0.5 * sum(b3.distress(world, k) for k in young) / len(young)
            ch = b2.CHOSEN.get((id(world), p.id))
            care = 0.1 if (ch is not None and ch[0] == tick and ch[1] in ("care", "give") and ch[2] in p.children) else 0.0
            cur = 0.0
            if p.last_action not in ("attack", "steal"):
                cur = 0.1 / (1 + nb["cnt"].get(f"{p.last_ctx}:{p.last_action}", 0))
            snap += nb["L"] * (love + care) + nb["C"] * cur
        out = feel0(world, p)
        if snap is not None:
            st["feel_looks"] += 1
            if abs(out - snap) > 1e-9:
                st["feel_mismatch"] += 1
        return out

    b2.child, b2.rescore, b3.feel, actions._attack = child, rescore, feel, attack
    actions.HANDLERS["attack"] = attack
    try:
        for _ in range(years * WPY):
            w.step()
    finally:
        b2.child, b2.rescore, b3.feel, actions._attack = child0, rescore0, feel0, attack0
        actions.HANDLERS["attack"] = handler0
    ok = (st["child_looks"] > 0 and st["gene_bad"] == 0 and st["hb_looks"] > 0 and st["hb_mismatch"] == 0
          and st["hb_harm_options"] > 0 and st["guilt_mismatch"] == 0 and st["feel_looks"] > 0 and st["feel_mismatch"] == 0)
    return ok, dict(st)


def hashrun(code, arm, seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY
    w = make(seed, arm, code)
    obs = None
    if observe:
        install()
        obs = NB2Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results(w)
        extra = ":" + json.dumps({"ext": r.get("ext", {}), "last_year": r["years"][-1] if r["years"] else {}},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.strip().splitlines()[-1]

    def hs(x):
        return x.split(":")[:2]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    arms = list(ARMS)
    specs = [("nb2", "n2", 501, 20, 0)] + [("nb3", a, 501, 20, 0) for a in arms] + [("nb3", "f", 501, 20, 1)]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        unit = ex.submit(call, "unit", 701)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
        ck = ex.submit(lambda: subprocess.run(me + ["ckcheck", "502"], capture_output=True, text=True).stdout.split())
    same = hs(got[("nb2", "n2", 501, 20, 0)]) == hs(got[("nb3", "n2", 501, 20, 0)])
    differ = all(hs(got[("nb3", x, 501, 20, 0)]) != hs(got[("nb3", y, 501, 20, 0)])
                 for i, x in enumerate(arms) for y in arms[i + 1:])
    ro = hs(got[("nb3", "f", 501, 20, 0)]) == hs(got[("nb3", "f", 501, 20, 1)])
    ok &= same and differ and ro
    lines.append(f"seed 501, 20 years: code_nb3 with NB3 off (arm n2) = code_nb2's full arm: {'yes' if same else 'NO'}; "
                 f"the seven arms all differ: {'yes' if differ else 'NO'}; observers read-only (f): {'yes' if ro else 'NO'}")
    u = json.loads(unit.result())
    ok &= u[0]
    lines.append(f"unit checks, arm f, seed 701, 8 years (feeling genes from the genome's parent within the mutation, in "
                 f"[0, 2]; attack and steal scores carry -H unless in defence; guilt rises by the frozen amounts for an "
                 f"attack one starts, not in defence; the week's feeling = an independent computation of all its parts): "
                 f"{'yes' if u[0] else 'NO'}; {u[1]}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm f, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    t2 = ck.result()[-1:] == ["True"]
    ok &= t2
    lines.append(f"arm f, seed 502: 15 years in one job = 1 year, a checkpoint, and 14 years in a second job: "
                 f"{'yes' if t2 else 'NO'}")
    lines.append(f"code_nb3 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok
