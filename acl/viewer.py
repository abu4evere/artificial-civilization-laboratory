"""Watch the world in a browser. You can look, but you cannot touch.

Two ways to run it:

    python -m acl live      # their world, living on its own clock, saved as it goes
    python -m acl watch     # a throwaway world at whatever speed you like, for trying things out

**live** keeps one world in a folder (`world/` by default). Time there runs on
a clock: by default fifteen real minutes are one day for them, so a week passes
every hour and three quarters and a year about every 3.8 days. The world goes on whether or
not anyone is watching. It saves itself after every week. If the computer was
off, it catches up on the weeks it missed when it starts again, so their time
never stands still. The people know nothing of hours, weeks or years; those are
only shown to you.

The page shows the world as a relief map drawn from the land's real height and biome, with every person on it,
the bands the historian has named, fires and couples; an overview, the chronicle, charts from the historian's yearly
record, and tabs for people, bands and live readings of ACL's findings. Click anyone to see their state, thoughts,
family and history, and open their brain scan: the situation they are in, the habits they have learned, and how
instinct and habit weighed their choices this week (see mindview.py). ACL's people have no faces, so none are drawn.
The earlier pixel-art page is kept at /story.
"""
from __future__ import annotations

import html
import json
import os
import shutil
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .config import SEASONS, WEEKS_PER_YEAR
from .historian import CLASSES, Historian, classify, describe
from . import mindview, stage
from .runner import chronicle_markdown, load_snapshot, new_world, save_snapshot, write_outputs
from .mind import hunger_of
from .person import A, ACTIONS, N_ACTIONS, N_CONTEXTS
from .world import World

HERE = Path(__file__).parent
HOUR = 3600.0


class Live:
    """A running world, shared between the simulation thread and the web handlers.

    With `clock` set, a week passes every `clock["period"]` seconds of real time
    and the world is saved into `home` after each one. Without it, weeks pass at
    `wps` weeks per second and nothing is kept.
    """

    def __init__(self, world: World, historian: Historian, wps: float = 4.0,
                 clock: dict | None = None, home: Path | None = None, public: bool = False):
        self.world, self.historian = world, historian
        if historian not in world.observers:
            world.observers.append(historian)
        self.lock = threading.Lock()
        self.cond = threading.Condition()
        self.frame = ""
        self.seq = 0
        self.wps = wps
        self.clock = clock
        self.home = home
        self.public = public
        self.stop = False
        self.lineage: dict[str, int] = {}
        self.news_seen = len(historian.chronicle)
        self.year_stats: dict = {}     # births and deaths per year, for the page's overview
        self.last_script = {"says": [], "moments": [], "hunts": [], "dead": []}
        self.talk_log: list = []          # what was said in past weeks: [week, day, f, kind, a, a name, b name, text]
        self._publish([])

    # --- making one -----------------------------------------------------------------

    @classmethod
    def fast(cls, seed: int, wps: float) -> "Live":
        world, historian = new_world(seed)
        return cls(world, historian, wps=wps)

    @classmethod
    def persistent(cls, home: Path, seed: int | None = None, hours_per_day: float = 0.25,
                   new: bool = False, public: bool = False) -> "Live":
        """Open the world kept in `home`, or begin one there."""
        home.mkdir(parents=True, exist_ok=True)
        save = home / "current.json.gz"
        settings_path = home / "settings.json"
        if new and save.exists():
            _set_aside(home)
        if save.exists():
            world, historian = load_snapshot(save)
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            clock = {"period": settings["period"], "last_tick_at": settings["last_tick_at"]}
            print(f"Their world (seed {world.cfg.seed}) is back: year {world.year}, "
                  f"{len(world.living())} people.")
        else:
            if seed is None:
                seed = int.from_bytes(os.urandom(3), "big")
            world, historian = new_world(seed)
            # The first week starts right away; after that the clock takes over.
            clock = {"period": 7 * hours_per_day * HOUR, "last_tick_at": time.time() - 7 * hours_per_day * HOUR}
            settings_path.write_text(json.dumps({
                "seed": seed, "period": clock["period"], "last_tick_at": clock["last_tick_at"],
                "began": datetime.now().isoformat(timespec="seconds"),
            }, indent=1), encoding="utf-8")
            print(f"A new world begins (seed {seed}) with {len(world.living())} people.")
        live = cls(world, historian, clock=clock, home=home, public=public)
        live.news_seen = max(0, len(historian.chronicle) - 80)
        # This week's plan and moments, so a restart does not leave the week silent.
        week = home / "this_week.json"
        if week.exists():
            saved = json.loads(week.read_text(encoding="utf-8"))
            live.talk_log = saved.get("log", [])
            if saved.get("tick") == world.tick:
                live.last_script = saved["script"]
                world.plan = {pid: (tuple(v[0]), v[1]) for pid, v in saved["plan"].items()}
                live._publish([])
        return live

    # --- the simulation thread --------------------------------------------------------

    def run(self) -> None:
        if self.clock:
            self._run_clock()
        else:
            self._run_fast()

    def _run_fast(self) -> None:
        while not self.stop:
            if self.wps <= 0:
                time.sleep(0.1)
                continue
            started = time.time()
            with self.lock:
                if not self.world.living():
                    self.wps = 0
                    continue
                self._publish(self.world.step())
            if self.wps <= 0:
                continue
            wait = 1.0 / self.wps - (time.time() - started)
            if wait > 0:
                time.sleep(wait)

    def _run_clock(self) -> None:
        unsaved = 0
        while not self.stop:
            now = time.time()
            due = self.clock["last_tick_at"] + self.clock["period"]
            if now < due:
                time.sleep(min(5.0, due - now))
                continue
            with self.lock:
                if not self.world.living():
                    self.stop = True
                    self._save()
                    break
                events = self.world.step()
                self.clock["last_tick_at"] = due
                self._publish(events)
                unsaved += 1
                behind = time.time() >= due + self.clock["period"]
                if not behind or unsaved >= 52:
                    self._save()
                    unsaved = 0

    def _save(self) -> None:
        if self.home is None:
            return
        home = self.home
        tmp = home / "current.tmp.gz"
        save_snapshot(self.world, self.historian, tmp)
        os.replace(tmp, home / "current.json.gz")
        settings_path = home / "settings.json"
        settings = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.exists() else {}
        settings.update(seed=self.world.cfg.seed, period=self.clock["period"],
                        last_tick_at=self.clock["last_tick_at"], year=self.world.year,
                        people=len(self.world.living()))
        settings_path.write_text(json.dumps(settings, indent=1), encoding="utf-8")
        (home / "chronicle.md").write_text(chronicle_markdown(self.world, self.historian), encoding="utf-8")
        (home / "this_week.json").write_text(json.dumps({
            "tick": self.world.tick, "script": self.last_script, "log": self.talk_log,
            "plan": {pid: [list(v[0]), v[1]] for pid, v in self.world.plan.items()},
        }, separators=(",", ":")), encoding="utf-8")
        year = self.world.year
        if year > 0 and year % 25 == 0 and self.world.week == 0:
            archive = home / "archive"
            archive.mkdir(exist_ok=True)
            shutil.copyfile(home / "current.json.gz", archive / f"year_{year:04d}.json.gz")

    # --- frames for the page ------------------------------------------------------------

    def _publish(self, events: list) -> None:
        frame = self._frame(events)
        with self.cond:
            self.frame = json.dumps(frame, separators=(",", ":"))
            self.seq += 1
            self.cond.notify_all()

    def _line(self, p) -> int:
        """Family line: which of the founding bands someone descends from, for colouring."""
        chain = []
        while p.id not in self.lineage:
            if p.generation == 0:
                founders = [q.id for q in self.world.people.values() if q.generation == 0]
                groups = max(1, min(4, self.world.cfg.founders // 4))
                self.lineage[p.id] = founders.index(p.id) % groups
                break
            chain.append(p.id)
            p = self.world.people[p.mother or p.father]
        for pid in chain:
            self.lineage[pid] = self.lineage[p.id]
        return self.lineage[chain[0]] if chain else self.lineage[p.id]

    def _frame(self, events: list) -> dict:
        w = self.world
        news = self.historian.chronicle[self.news_seen:]
        self.news_seen = len(self.historian.chronicle)
        living = w.living()
        # Births and deaths this year, counted from the week's events (for the page's overview).
        ys = self.year_stats
        cur = ys.setdefault(w.year, {"born": 0, "died": 0})
        for e in events:
            if e.get("k") == "birth":
                cur["born"] += 1
            elif e.get("k") == "death":
                cur["died"] += 1
        for old in [y for y in ys if y < w.year - 1]:
            del ys[old]
        frame = {
            "t": w.tick, "year": w.year, "week": w.week, "season": SEASONS[w.season], "weather": w.weather,
            "pop": len(living), "gen": max((p.generation for p in living), default=0),
            "people": stage.people_rows(w, self._line), "tiles": stage.tile_rows(w),
            "animals": stage.animal_rows(w), "news": news,
            "sky": stage.sky(w), "marks": stage.mark_rows(w),
            "wps": self.wps, "now": time.time(), "born_year": cur["born"], "died_year": cur["died"],
            "bands": [[b["id"], b["name"], b["members"], 1 if b.get("announced") else 0] for b in self.historian.bands],
            "years_n": len(self.historian.years),
        }
        if events:
            # Last week's conversations are over now: keep them where anyone can read them back.
            for kind, a, b, text, day, f in self.last_script["says"]:
                self.talk_log.append([w.tick - 1, day, f, kind, a, _name(w, a), _name(w, b) if b else "", text])
            del self.talk_log[:-400]
            self.last_script = stage.script(w, events, self._line, self.historian)
        frame.update(self.last_script)
        if self.clock:
            frame["clock"] = {"period": self.clock["period"], "last": self.clock["last_tick_at"]}
        return frame

    # --- what the page asks for ------------------------------------------------------

    def terrain(self) -> dict:
        w = self.world
        return {
            "seed": w.cfg.seed, "width": w.cfg.width, "height": w.cfg.height, "live": self.clock is not None,
            "perception": w.cfg.perception,
            "tiles": [[round(t.fertility, 2), round(t.forest, 2), round(t.rock, 2), 1 if t.flinty else 0,
                       round(t.wildness, 2), 1 if t.water else 0, t.biome, round(t.height, 3)] for row in w.tiles for t in row],
            "chronicle": self.historian.chronicle[-80:],
            "log": self.talk_log[-300:],
        }

    def history(self) -> list:
        """One row per finished year, as the historian keeps it (the fields the page charts)."""
        with self.lock:
            keep = ("year", "population", "births", "deaths", "children", "pairs", "mood", "health", "generation")
            return [{k: r[k] for k in keep} for r in self.historian.years]

    def chronicle_page(self) -> str:
        with self.lock:
            text = chronicle_markdown(self.world, self.historian)
        return ("<!doctype html><meta charset='utf-8'><title>Chronicle</title>"
                "<style>body{font:15px/1.6 system-ui,sans-serif;max-width:760px;margin:32px auto;padding:0 16px}"
                "pre{white-space:pre-wrap;font:inherit}</style><pre>" + html.escape(text) + "</pre>")

    def person(self, pid: str) -> dict:
        with self.lock:
            w = self.world
            p = w.people.get(pid)
            if p is None:
                return {}
            tick = w.tick

            def name(x):
                return w.people[x].name if x and x in w.people else None

            memories = []
            for m in sorted(p.memories, key=lambda m: -(m.salience * m.strength))[:6]:
                memories.append(_memory_words(w, m))
            makes = []
            for sig in sorted(p.recipes, key=lambda s: -p.itemval.get(s, 0.0))[:6]:
                rec = w.knowledge.get(sig, {})
                cls = classify(rec.get("props"))
                makes.append({"what": CLASSES[cls[0]][1] if cls else "something of their own devising",
                              "how": describe(p.recipes[sig], w), "worth": round(p.itemval.get(sig, 0.0), 2)})
            beliefs = []
            for key, v in sorted(p.beliefs.items(), key=lambda kv: -abs(kv[1]))[:5]:
                thing, season = key.split("@")
                beliefs.append(_belief_words(thing, int(season), v))
            return {
                "id": p.id, "name": p.name, "sex": p.sex, "alive": p.alive, "loc": list(p.loc),
                "energy": round(p.energy), "band": next((b["name"] for b in self.historian.bands if p.id in b["members"]), None),
                "age": round(p.years(tick), 1), "stage": p.stage(tick), "generation": p.generation,
                "health": round(p.health), "mood": round(p.mood, 2), "doing": p.doing,
                "mother": name(p.mother), "father": name(p.father), "partner": name(p.partner),
                "children": [name(c) for c in p.children if w.people[c].alive],
                "temperament": {k: round(v, 2) for k, v in p.genes.items()},
                "carrying": {"food": round(p.food), "seeds": round(p.seeds),
                             **{k: round(v) for k, v in p.mats.items() if v >= 1}},
                "things": [", ".join(CLASSES[c][0] for c in classify(it)) or "an odd thing they made" for it in p.items],
                "memories": memories, "makes": makes, "beliefs": beliefs,
                "mind": mindview.mind(w, p) if p.alive else None,
                "brain": _brain(w, p) if p.alive else None,
                "death": p.death_cause,
            }


def _name(world, pid) -> str:
    q = world.people.get(pid) if pid else None
    return q.name if q else ""


def _brain(w, p) -> dict:
    """How p decides, for the brain scan: what they sense and feel, the situation lit this week, the habits learned for
    every situation, and how each option weighed this week splits into instinct and habit. Read-only."""
    c, tick = w.cfg, w.tick
    hunger = hunger_of(w, p, sum(d.need(c, tick) for d in w.dependents(p.id)))
    base = p.last_ctx * N_ACTIONS
    return {"ctx": p.last_ctx, "actions": list(ACTIONS), "n_contexts": N_CONTEXTS, "learned_weight": c.learned_weight,
            "q": [round(v * 100) for v in p.q], "learned": sum(1 for v in p.q if v), "chosen": p.last_action,
            "weighed": [[a, round(sc, 2), int(ch), round(c.learned_weight * p.q[base + A[a]], 2)] for a, _aim, sc, ch in p.considered],
            "body": {"hunger": round(hunger, 2), "thirst": round(p.thirst, 2), "fatigue": round(1 - p.energy / 100, 2),
                     "health": round(p.health / 100, 2), "mood": round(p.mood, 2), "fear": round(p.fear, 2),
                     "anger": round(p.anger, 2), "grief": round(p.grief, 2), "loneliness": round(p.loneliness, 2)},
            "genes": {g: round(v, 2) for g, v in p.genes.items()}}


def _set_aside(home: Path) -> None:
    """Starting over never destroys the old world: it is moved into home/old/<when>/."""
    when = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    dest = home / "old" / when
    dest.mkdir(parents=True)
    for name in ("current.json.gz", "settings.json", "chronicle.md", "archive"):
        src = home / name
        if src.exists():
            shutil.move(str(src), str(dest / name))
    print(f"The previous world was set aside in {dest}")


def _memory_words(w, m) -> str:
    def nm(x):
        return w.people[x].name if x and x in w.people else "someone"
    year = m.tick // WEEKS_PER_YEAR
    told = f" (told by {nm(m.source)})" if m.source else ""
    text = {
        "killed": f"{nm(m.actor)} killed {nm(m.target)}",
        "attacked": f"{nm(m.actor)} attacked {nm(m.target)}",
        "stole": f"{nm(m.actor)} stole from {nm(m.target)}",
        "died": f"{nm(m.target)} died",
        "born": f"{nm(m.target)} was born",
        "gave": f"{nm(m.actor)} gave food when it was needed",
        "paired": f"{nm(m.actor)} and {nm(m.target)} became a couple",
    }.get(m.kind, m.kind)
    return f"Year {year}: {text}{told}"


def _belief_words(thing: str, season: int, v: float) -> str:
    when = SEASONS[season]
    if "/" in thing:
        a, b = thing.split("/")
        what = f"striking {a} with {b}"
    elif thing == "seeds":
        what = "leaving seeds in the ground"
    elif thing == "food":
        what = "leaving food somewhere to come back for"
    else:
        what = f"leaving {thing} in a heap"
    verdict = "is worth it" if v > 0 else "does no good"
    return f"{what[:1].upper() + what[1:]} in {when} {verdict} ({v:+.2f})"


def make_handler(live: Live, server_holder: list | None = None):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _send(self, body: bytes, ctype: str) -> None:
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj) -> None:
            self._send(json.dumps(obj).encode(), "application/json")

        def _local(self) -> bool:
            return not live.public and self.client_address[0] in ("127.0.0.1", "::1")

        def do_GET(self):
            url = urlparse(self.path)
            q = parse_qs(url.query)
            if url.path == "/":
                # Read fresh each time, so a better-looking page arrives without stopping their world.
                self._send((HERE / "viewer.html").read_bytes(), "text/html; charset=utf-8")
            elif url.path == "/story":
                # The earlier pixel-art page, kept for reference; the lab view at "/" is the main one.
                self._send((HERE / "viewer_pixel.html").read_bytes(), "text/html; charset=utf-8")
            elif url.path == "/history":
                self._json(live.history())
            elif url.path == "/terrain":
                self._json(live.terrain())
            elif url.path == "/person":
                self._json(live.person(q.get("id", [""])[0]))
            elif url.path == "/chronicle":
                self._send(live.chronicle_page().encode(), "text/html; charset=utf-8")
            elif url.path == "/speed" and live.clock is None and self._local():
                try:
                    wps = max(0.0, min(200.0, float(q.get("wps", ["4"])[0])))
                except ValueError:
                    wps = live.wps
                with live.lock:
                    live.wps = wps
                    live._publish([])
                self._json({"wps": live.wps})
            elif url.path == "/shutdown" and self._local():
                self._json({"stopping": True})
                live.stop = True
                if server_holder:
                    threading.Thread(target=server_holder[0].shutdown, daemon=True).start()
            elif url.path == "/stream":
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                seen = -1
                try:
                    while not live.stop:
                        with live.cond:
                            live.cond.wait_for(lambda: live.seq != seen or live.stop, timeout=15)
                            changed = live.seq != seen
                            frame, seen = live.frame, live.seq
                        # A comment line every so often keeps idle connections open through proxies.
                        self.wfile.write(f"data: {frame}\n\n".encode() if changed else b": still here\n\n")
                        self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    pass
            else:
                self.send_response(404)
                self.end_headers()

    return Handler


def _serve(live: Live, host: str, port: int, open_browser: bool) -> None:
    holder: list = []
    try:
        server = ThreadingHTTPServer((host, port), make_handler(live, holder))
    except OSError:
        print(f"Something is already using port {port}. If their world is already running, "
              f"open http://127.0.0.1:{port}/")
        raise SystemExit(1)
    holder.append(server)
    server.daemon_threads = True
    sim = threading.Thread(target=live.run, daemon=True)
    sim.start()
    shown = "127.0.0.1" if host in ("0.0.0.0", "") else host
    url = f"http://{shown}:{port}/"
    print(f"Watch at {url}  (Ctrl+C or `python -m acl stop` to stop)", flush=True)
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        live.stop = True
        with live.cond:
            live.cond.notify_all()
        server.server_close()
        sim.join(timeout=10)


def watch(seed: int = 42, port: int = 8765, wps: float = 4.0, out: Path | None = None,
          open_browser: bool = True) -> None:
    """A throwaway world at any speed."""
    live = Live.fast(seed, wps)
    _serve(live, "127.0.0.1", port, open_browser)
    if out is not None:
        with live.lock:
            out.mkdir(parents=True, exist_ok=True)
            result = {"seed": seed, "metrics": live.historian.metrics(live.world),
                      "state_hash": live.world.state_hash(), "event_chain": live.world.event_chain,
                      "seconds": 0}
            save_snapshot(live.world, live.historian, out / "final.json.gz")
            write_outputs(live.world, live.historian, result, out)
            print(f"Saved what you watched to {out}")


def live(home: Path, seed: int | None = None, hours_per_day: float = 0.25, new: bool = False,
         host: str = "127.0.0.1", port: int = 8765, open_browser: bool = False, public: bool = False) -> None:
    """Their world, on its own clock, kept in `home`."""
    import socket
    probe = socket.socket()
    try:
        probe.bind((host, port))
    except OSError:
        # Most likely their world is already running. Never load or save a second copy.
        print(f"Port {port} is busy: their world is probably already running at http://127.0.0.1:{port}/")
        raise SystemExit(1)
    finally:
        probe.close()
    world_live = Live.persistent(home, seed, hours_per_day, new, public)
    try:
        _serve(world_live, host, port, open_browser)
    finally:
        with world_live.lock:
            world_live._save()
        print(f"Saved. Their world is in {home}")
