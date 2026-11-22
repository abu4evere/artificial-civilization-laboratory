"""Watch a throwaway ACL world drawn in text characters (a look only).

It is `python -m acl watch` with a different page: the viewer's own world, data and routes (/terrain, /stream, /speed,
/person ...) are used unchanged; only "/" serves acl_ascii.html, and the usual page moves to "/classic". Nothing in
`acl/` is changed or imported for writing; the world is a fresh one, kept nowhere.

    python design/ascii_world/ascii_watch.py [--seed 42] [--wps 1] [--port 8770] [--no-browser]
"""
from __future__ import annotations

import argparse
import sys
import threading
import webbrowser
from http.server import ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from acl import viewer as V  # noqa: E402


def handler(live, holder):
    Base = V.make_handler(live, holder)

    class Handler(Base):
        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path == "/":
                # Read fresh each time, so a changed page shows on reload without restarting the world.
                return self._send((HERE / "acl_ascii.html").read_bytes(), "text/html; charset=utf-8")
            if path == "/classic":
                self.path = "/"
            return super().do_GET()

    return Handler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--wps", type=float, default=1.0, help="weeks per second")
    ap.add_argument("--port", type=int, default=8770)
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    live = V.Live.fast(a.seed, a.wps)
    holder: list = []
    server = ThreadingHTTPServer(("127.0.0.1", a.port), handler(live, holder))
    holder.append(server)
    server.daemon_threads = True
    threading.Thread(target=live.run, daemon=True).start()
    url = f"http://127.0.0.1:{a.port}/"
    print(f"ACL in text (seed {a.seed}) at {url}   the usual page: {url}classic   Ctrl+C to stop", flush=True)
    if not a.no_browser:
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


if __name__ == "__main__":
    main()
