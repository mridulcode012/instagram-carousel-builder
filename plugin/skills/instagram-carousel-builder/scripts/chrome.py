#!/usr/bin/env python3
"""
chrome.py - drive headless Google Chrome / Chromium over the DevTools protocol, stdlib only.

Used by render.py (screenshots and measurements), export_pdf.py and reference.py.
Set CHROME_PATH to point at a specific binary.
"""

import base64
import fcntl
import glob
import json
import os
import select
import shutil
import subprocess
import tempfile
import time
import urllib.parse


NO_CHROME = ("No Chrome/Chromium found. Install Google Chrome or set CHROME_PATH. In a sandbox without one, run "
             "`pip install playwright && python3 -m playwright install chromium` and try again.")


def find_chrome():
    cands = [
        os.environ.get("CHROME_PATH"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"), shutil.which("google-chrome-stable"),
        shutil.which("chromium"), shutil.which("chromium-browser"), shutil.which("chrome"),
    ]
    home = os.path.expanduser("~")
    cands += sorted(glob.glob(f"{home}/Library/Caches/ms-playwright/chromium-*/chrome-mac*/*.app/Contents/MacOS/*"), reverse=True)
    cands += sorted(glob.glob(f"{home}/.cache/ms-playwright/chromium-*/chrome-linux*/chrome"), reverse=True)
    # claude.ai chat sandbox and other Playwright installs (PLAYWRIGHT_BROWSERS_PATH, else /opt/pw-browsers)
    for pw in dict.fromkeys(p for p in (os.environ.get("PLAYWRIGHT_BROWSERS_PATH"), "/opt/pw-browsers") if p):
        cands += sorted(glob.glob(f"{pw}/chromium-*/chrome-linux*/chrome"), reverse=True)
        cands += sorted(glob.glob(f"{pw}/chromium_headless_shell-*/chrome-linux*/headless_shell"), reverse=True)
    for c in cands:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


class Browser:
    """Minimal Chrome DevTools Protocol client over --remote-debugging-pipe (stdlib only)."""

    def __init__(self, binary):
        self.prof = tempfile.mkdtemp(prefix="carousel-chrome-")
        r1, w1 = os.pipe()  # we write -> chrome reads on fd 3
        r2, w2 = os.pipe()  # chrome writes on fd 4 -> we read
        a = fcntl.fcntl(r1, fcntl.F_DUPFD, 10)
        b = fcntl.fcntl(w2, fcntl.F_DUPFD, 10)

        def child_fds():
            os.dup2(a, 3)
            os.dup2(b, 4)

        self.proc = subprocess.Popen(
            [binary, "--headless=new", "--remote-debugging-pipe", "--disable-gpu", "--hide-scrollbars",
             "--no-first-run", "--no-default-browser-check", "--disable-extensions",
             "--allow-file-access-from-files", "--force-device-scale-factor=1",
             "--disable-dev-shm-usage", *(["--no-sandbox"] if hasattr(os, "geteuid") and os.geteuid() == 0 else []),
             f"--user-data-dir={self.prof}", "about:blank"],
            preexec_fn=child_fds, close_fds=False,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for fd in (r1, w2, a, b):
            os.close(fd)
        self.w, self.r = w1, r2
        self.buf, self.seq, self.queue = b"", 0, []

    def _read(self, timeout):
        while b"\0" not in self.buf:
            ready, _, _ = select.select([self.r], [], [], timeout)
            if not ready:
                raise TimeoutError("Chrome did not answer in time")
            chunk = os.read(self.r, 1 << 20)
            if not chunk:
                raise RuntimeError("Chrome exited unexpectedly")
            self.buf += chunk
        raw, self.buf = self.buf.split(b"\0", 1)
        return json.loads(raw)

    def _wait(self, pred, timeout=60):
        for i, m in enumerate(self.queue):
            if pred(m):
                return self.queue.pop(i)
        deadline = time.time() + timeout
        while True:
            m = self._read(max(0.05, deadline - time.time()))
            if pred(m):
                return m
            self.queue.append(m)
            if time.time() > deadline:
                raise TimeoutError("timed out waiting for Chrome")

    def send(self, method, params=None, session=None, timeout=60):
        self.seq += 1
        n = self.seq
        msg = {"id": n, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        data = json.dumps(msg).encode() + b"\0"
        while data:
            data = data[os.write(self.w, data):]
        m = self._wait(lambda x: x.get("id") == n, timeout)
        if "error" in m:
            raise RuntimeError(f"{method}: {m['error'].get('message')}")
        return m.get("result", {})

    def page(self, w, h):
        tid = self.send("Target.createTarget", {"url": "about:blank"})["targetId"]
        sid = self.send("Target.attachToTarget", {"targetId": tid, "flatten": True})["sessionId"]
        self.send("Page.enable", session=sid)
        self.resize(sid, w, h)
        return sid

    def resize(self, sid, w, h):
        self.send("Emulation.setDeviceMetricsOverride",
                  {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": False}, sid)

    def goto(self, sid, url, ready_timeout=60, wait_ready=True):
        self.queue = [m for m in self.queue if m.get("method") != "Page.loadEventFired"]
        self.send("Page.navigate", {"url": url}, sid)
        self._wait(lambda m: m.get("method") == "Page.loadEventFired" and m.get("sessionId") == sid, ready_timeout)
        if wait_ready:
            self.js(sid, "new Promise(r => { const t = () => document.body.dataset.ready ? r(1) : setTimeout(t, 50); t(); })",
                    ready_timeout)

    def js(self, sid, expr, timeout=60):
        res = self.send("Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True},
                        sid, timeout)
        if "exceptionDetails" in res:
            raise RuntimeError("page script failed: " + json.dumps(res["exceptionDetails"])[:500])
        return res.get("result", {}).get("value")

    def shot(self, sid, path, w, h, x=0, y=0):
        """Screenshot a w x h region at page coordinates (x, y); works below the fold too."""
        res = self.send("Page.captureScreenshot",
                        {"format": "png", "captureBeyondViewport": True,
                         "clip": {"x": x, "y": y, "width": w, "height": h, "scale": 1}}, sid)
        with open(path, "wb") as f:
            f.write(base64.b64decode(res["data"]))

    def close(self):
        try:
            self.send("Browser.close", timeout=5)
        except Exception:
            pass
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        for fd in (self.w, self.r):
            try:
                os.close(fd)
            except OSError:
                pass
        shutil.rmtree(self.prof, ignore_errors=True)


def file_url(path):
    return "file://" + urllib.parse.quote(os.path.abspath(path))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
