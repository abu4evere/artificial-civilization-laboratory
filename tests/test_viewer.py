"""The live viewer serves the page, the land, a stream of weeks, and a person's life story."""
from __future__ import annotations

import http.client
import json
import threading
from http.server import ThreadingHTTPServer

from acl.viewer import Live, make_handler


def _serve(live):
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(live))
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def _get(port, path):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("GET", path)
    r = conn.getresponse()
    return r.status, r.read()


def test_viewer_serves_world():
    live = Live.fast(3, 200.0)
    sim = threading.Thread(target=live.run, daemon=True)
    sim.start()
    server = _serve(live)
    port = server.server_address[1]
    try:
        status, page = _get(port, "/")
        assert status == 200 and b"<canvas" in page
        status, body = _get(port, "/terrain")
        terrain = json.loads(body)
        assert len(terrain["tiles"]) == terrain["width"] * terrain["height"]

        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/stream")
        r = conn.getresponse()
        frames = []
        while len(frames) < 3:
            line = r.fp.readline().decode()
            if line.startswith("data: "):
                frames.append(json.loads(line[6:]))
        conn.close()
        assert frames[-1]["t"] >= frames[0]["t"]
        assert frames[-1]["people"] and len(frames[-1]["tiles"]) == len(terrain["tiles"])

        pid = frames[-1]["people"][0][0]
        status, body = _get(port, f"/person?id={pid}")
        info = json.loads(body)
        assert info["id"] == pid and "memories" in info and "makes" in info
        brain = info["brain"]   # the brain scan: situation lit, 32 x 19 learned habits, options weighed
        assert len(brain["q"]) == brain["n_contexts"] * len(brain["actions"]) and 0 <= brain["ctx"] < brain["n_contexts"]
        assert "frames" not in info and "born_year" in frames[-1]

        status, page = _get(port, "/story")   # the earlier pixel-art page is kept
        assert status == 200 and b"<canvas" in page

        status, body = _get(port, "/speed?wps=0")
        assert json.loads(body)["wps"] == 0
        assert json.loads(live.frame)["wps"] == 0   # the page learns at once that it is paused
    finally:
        live.stop = True
        with live.cond:
            live.cond.notify_all()
        server.shutdown()


def test_their_world_keeps_time_and_survives_a_restart(tmp_path):
    import time

    home = tmp_path / "world"
    # A week every 0.05 s. The first week starts at once.
    first = Live.persistent(home, seed=5, hours_per_day=0.05 / 7 / 3600)
    first.clock["last_tick_at"] = time.time() - 10 * first.clock["period"]   # it was "off" for 10 weeks
    sim = threading.Thread(target=first.run, daemon=True)
    sim.start()
    deadline = time.time() + 15          # a busy machine catches up more slowly
    while first.world.tick < 10 and time.time() < deadline:
        time.sleep(0.05)
    time.sleep(0.2)
    first.stop = True
    sim.join(timeout=5)
    with first.lock:
        first._save()
    ticks = first.world.tick
    assert ticks >= 10                    # caught up on the weeks it missed, then kept going
    assert (home / "current.json.gz").exists() and (home / "chronicle.md").exists()

    second = Live.persistent(home)        # comes back where it left off
    assert second.world.tick == ticks
    assert second.world.cfg.seed == 5
    assert second.clock["last_tick_at"] == first.clock["last_tick_at"]


def test_starting_over_keeps_the_old_world(tmp_path):
    home = tmp_path / "world"
    a = Live.persistent(home, seed=5)
    with a.lock:
        a._save()
    b = Live.persistent(home, seed=6, new=True)
    assert b.world.cfg.seed == 6
    old = list((home / "old").iterdir())
    assert len(old) == 1 and (old[0] / "current.json.gz").exists()


def test_a_week_becomes_moments_to_watch():
    from acl import stage
    from acl.runner import new_world

    w, h = new_world(4)
    kinds = set()
    for _ in range(52 * 2):
        events = w.step()
        s = stage.script(w, events, lambda p: 0, h)
        for kind, a, b, text, day, f in s["says"]:
            assert kind in ("say", "chat", "think") and text and 0 <= day < 7 and 0 <= f < 1
            assert a in w.people
            kinds.add(kind)
        for x, y, party, success, day, f in s["hunts"]:
            assert party and 0 <= day < 7
    assert {"say", "chat"} <= kinds
    # Everyone who spent the week with someone has a conversation with lines from both sides.
    # (In a hungry week everyone may be out foraging, so look across a few weeks.)
    talks = []
    for _ in range(12):
        talks += stage.script(w, w.step(), lambda p: 0, h)["talks"]
    assert talks
    for a, b, lines in talks:
        assert lines and {spk for spk, _, _ in lines} <= {a, b}
    rows = stage.people_rows(w, lambda p: 0)
    assert rows and len(rows[0]) == 23
    assert all(r[4] is not None for r in rows)          # everyone has a place they set out from
