#!/usr/bin/env python3
"""Serve dist/ over HTTP with Range support (Kodi reads ZIP central directories with Range requests;
`python -m http.server` ignores Range and Kodi 21.3 then crashes). Usage: python tools/serve.py [port] [dir]"""
import os, re, sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        rng = self.headers.get("Range")
        path = self.translate_path(self.path)
        m = re.fullmatch(r"bytes=(\d*)-(\d*)", rng or "")
        if not m or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        a, b = m.groups()
        start, end = (size - int(b), size - 1) if not a else (int(a), int(b) if b else size - 1)
        end = min(end, size - 1)
        if start > end or start >= size:
            self.send_error(416); return None
        f = open(path, "rb"); f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self._left = end - start + 1
        return f

    def copyfile(self, src, dst):
        left = getattr(self, "_left", None)
        while True:
            chunk = src.read(64 * 1024 if left is None else min(64 * 1024, left))
            if not chunk: break
            dst.write(chunk)
            if left is not None:
                left -= len(chunk)
                if left <= 0: break

    def end_headers(self):
        if not self.headers.get("Range"):
            self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    root = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dist")
    ThreadingHTTPServer(("0.0.0.0", port), partial(Handler, directory=root)).serve_forever()
