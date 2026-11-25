"""A tiny local receiver for recordings made in the browser (design/video). POST /save?name=FILE writes the body to
design/video/FILE. Local only (127.0.0.1); used to save the ASCII-atlas video."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

HERE = Path(__file__).parent


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
        self.send_header("Access-Control-Allow-Headers", "*")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(b"receiver ok")

    def do_POST(self):
        name = parse_qs(urlparse(self.path).query).get("name", ["rec.webm"])[0]
        name = Path(name).name
        n = int(self.headers.get("Content-Length", 0))
        (HERE / name).write_bytes(self.rfile.read(n))
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(f"saved {name} {n}".encode())


ThreadingHTTPServer(("127.0.0.1", 8799), H).serve_forever()
