#!/usr/bin/env python3
"""Measured check for `capture stream-online --exclude-pid` (issue #2, lane ca-capture-apps).

Plays 1 kHz test tones from known processes and measures stream 1 (system audio)
at 1 kHz in 0.5 s windows (Goertzel, sine-peak dBFS). One PASS/FAIL line per leg.
The three tones, one after another in one capture run:
  (a) -20 dBFS into BlackHole 2ch from a separate python process with a duplex stream,
      default mic in / BlackHole out (the shape of demo-agent's mixer, app/voice/mixer.py):
      the process whose PID is excluded. Only the tone is written; the mic is read, not mixed
  (b) -50 dBFS WebAudio tone in Playwright's Google Chrome for Testing (headed,
      local file:// page; Chrome plays it from a helper process)
  (c) -50 dBFS tone to the default output via afplay

  leg 3  --exclude-pid <mixer pid>: (a) >= 40 dB below played; (b), (c) within 6 dB.
         Control in the same leg: --exclude-pid <this script's pid> (no audio of its own),
         so the mixer is not excluded: (a) within 6 dB, which shows the tap sees BlackHole
  leg 4  no flag (today's SCK path): (a), (b), (c) all within 6 dB of played
  leg 5  late PID: the mixer opens BlackHole ~5 s after capture starts; within 5 s
         of its first audio its tone is >= 40 dB below played, without a restart

Test tones only; no call audio is recorded or kept. Needs the display on and the
screen unlocked (SCK path), and the TCC grants of the calling terminal.

usage: spike/stt_bench/venv/bin/python scripts/check_capture_exclude.py [leg ...]
"""
import math
import os
import struct
import subprocess
import sys
import tempfile
import threading
import time
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CAPTURE = ROOT / "app" / "bin" / "capture"
PY = sys.executable
RATE = 16000
WIN = RATE // 2          # 0.5 s windows; 1 kHz is an exact bin (500 cycles)
FREQ = 1000.0
MIXER_DB, BROWSER_DB, AFPLAY_DB = -20.0, -50.0, -50.0


def tone_db(x: np.ndarray) -> float:
    """Sine-peak level of the 1 kHz component in dBFS (Goertzel, rectangular window)."""
    n = len(x)
    w = 2 * math.pi * FREQ / RATE
    coeff = 2 * math.cos(w)
    s1 = s2 = 0.0
    for v in x.astype(np.float64):
        s0 = v + coeff * s1 - s2
        s2, s1 = s1, s0
    mag = math.sqrt(max(s1 * s1 + s2 * s2 - coeff * s1 * s2, 0.0))
    return 20 * math.log10(max(2 * mag / n, 1e-10))


class Capture:
    """Runs a capture command, keeps its stream-1 samples with arrival times."""

    def __init__(self, args: list[str]):
        self.proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.lock = threading.Lock()
        self.chunks: list[tuple[float, np.ndarray]] = []   # (arrival, stream-1 samples)
        self.log: list[str] = []
        self.ready = threading.Event()
        threading.Thread(target=self._read_out, daemon=True).start()
        threading.Thread(target=self._read_err, daemon=True).start()
        if not self.ready.wait(15):
            self.stop()
            raise RuntimeError("capture did not start:\n" + "\n".join(self.log))

    def _read_out(self):
        f = self.proc.stdout
        while True:
            head = f.read(5)
            if len(head) < 5:
                return
            sid, n = head[0], struct.unpack("<I", head[1:])[0]
            payload = f.read(2 * n)
            if sid == 1:
                x = np.frombuffer(payload, dtype="<i2").astype(np.float32) / 32768.0
                with self.lock:
                    self.chunks.append((time.monotonic(), x))

    def _read_err(self):
        for raw in self.proc.stderr:
            line = raw.decode(errors="replace").rstrip()
            self.log.append(line)
            if line.startswith(("streaming", "CAPTURE FAILED")):
                self.ready.set()

    def windows(self, t0: float, t1: float) -> list[tuple[float, float]]:
        """(end time, 1 kHz dBFS) per full 0.5 s window of samples that arrived in [t0, t1]."""
        with self.lock:
            chunks = [c for c in self.chunks if t0 <= c[0] <= t1]
        out, buf = [], np.zeros(0, np.float32)
        for t, x in chunks:
            buf = np.concatenate([buf, x])
            while len(buf) >= WIN:
                out.append((t, tone_db(buf[:WIN])))
                buf = buf[WIN:]
        return out

    def stop(self):
        self.proc.send_signal(2)
        try:
            self.proc.wait(10)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def median_db(ws) -> float:
    return float(np.median([d for _, d in ws])) if ws else float("-inf")


def max_db(ws) -> float:
    return max((d for _, d in ws), default=float("-inf"))


def fmt(db: float) -> str:
    return "no samples" if db == float("-inf") else f"{db:.1f} dB"


# ---- tone sources ----------------------------------------------------------
MIXER_SRC = """
import sys, time
db, delay, on = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3] == "on"
time.sleep(delay)   # before the import: PortAudio's init already registers the process with Core Audio
import numpy as np, sounddevice as sd
dev = next(i for i, d in enumerate(sd.query_devices())
           if "BlackHole 2ch" in d["name"] and d["max_output_channels"] >= 2)
sr, amp, st = 48000, 10 ** (db / 20), {"on": on, "ph": 0}
def cb(indata, out, frames, t, status):
    if st["on"]:
        n = np.arange(st["ph"], st["ph"] + frames); st["ph"] += frames
        x = amp * np.sin(2 * np.pi * 1000 * n / sr)
    else:
        x = np.zeros(frames)
    out[:, 0] = x; out[:, 1] = x
with sd.Stream(samplerate=sr, device=(sd.default.device[0], dev), channels=(1, 2),
               dtype="float32", callback=cb):
    print("open", flush=True)
    for line in sys.stdin:
        cmd = line.strip()
        if cmd == "quit": break
        st["on"] = cmd == "on"
"""


class Mixer:
    """Separate python process writing a 1 kHz tone into BlackHole 2ch (stdin: on/off/quit)."""

    def __init__(self, delay: float = 0.0, on: bool = False):
        self.proc = subprocess.Popen([PY, "-c", MIXER_SRC, str(MIXER_DB), str(delay),
                                      "on" if on else "off"],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        self.pid = self.proc.pid
        self.opened_at: float | None = None
        threading.Thread(target=self._wait_open, daemon=True).start()

    def _wait_open(self):
        if self.proc.stdout.readline().strip() == "open":
            self.opened_at = time.monotonic()

    def wait_open(self, timeout: float) -> float:
        end = time.monotonic() + timeout
        while self.opened_at is None:
            if time.monotonic() > end:
                raise RuntimeError("mixer did not open BlackHole 2ch")
            time.sleep(0.05)
        return self.opened_at

    def send(self, cmd: str):
        self.proc.stdin.write(cmd + "\n")
        self.proc.stdin.flush()

    def close(self):
        try:
            self.send("quit")
            self.proc.wait(5)
        except Exception:
            self.proc.kill()


def afplay(db: float, secs: float, tmp: Path) -> subprocess.Popen:
    path = tmp / f"tone{int(db)}.wav"
    sr = 48000
    t = np.arange(int(sr * secs)) / sr
    x = (10 ** (db / 20) * np.sin(2 * np.pi * 1000 * t) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(x.tobytes())
    return subprocess.Popen(["afplay", str(path)])


PAGE = """<!doctype html><title>1 kHz test tone</title><body>
<script>
window.startTone = (db) => {
  const ctx = new AudioContext();
  const osc = ctx.createOscillator(); osc.frequency.value = 1000;
  const g = ctx.createGain(); g.gain.value = Math.pow(10, db / 20);
  osc.connect(g).connect(ctx.destination); osc.start();
  window._ctx = ctx;
  return ctx.resume().then(() => ctx.state);
};
window.stopTone = () => window._ctx && window._ctx.close();
</script></body>"""


class Browser:
    """Playwright's Google Chrome for Testing, headed, on a local file:// page."""

    def __init__(self, tmp: Path):
        from playwright.sync_api import sync_playwright
        page_path = tmp / "tone.html"
        page_path.write_text(PAGE)
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(
            headless=False, args=["--autoplay-policy=no-user-gesture-required"])
        self.page = self.browser.new_page()
        self.page.goto(page_path.as_uri())

    def start_tone(self, db: float) -> str:
        return self.page.evaluate(f"window.startTone({db})")

    def stop_tone(self):
        self.page.evaluate("window.stopTone()")

    def close(self):
        self.browser.close()
        self.pw.stop()


# ---- legs ------------------------------------------------------------------
def three_tones(cmd, tmp: Path):
    """Runs capture cmd(mixer_pid), plays (a), (b), (c) in turn; returns their windows + log."""
    br = Browser(tmp)
    mixer = Mixer()
    try:
        mixer.wait_open(10)
        cap = Capture(cmd(mixer.pid))
        try:
            time.sleep(1.5)
            mixer.send("on")
            t0 = time.monotonic(); time.sleep(4)
            a = cap.windows(t0 + 1.0, time.monotonic())
            mixer.send("off"); time.sleep(0.5)
            state = br.start_tone(BROWSER_DB)
            t0 = time.monotonic(); time.sleep(4)
            b = cap.windows(t0 + 1.0, time.monotonic())
            br.stop_tone(); time.sleep(0.5)
            p = afplay(AFPLAY_DB, 4, tmp)
            t0 = time.monotonic(); p.wait()
            c = cap.windows(t0 + 1.0, time.monotonic() - 0.3)
        finally:
            cap.stop()
    finally:
        mixer.close()
        br.close()
    if state != "running":
        raise RuntimeError(f"browser AudioContext state {state}")
    return a, b, c, cap.log


def within(ws, played: float) -> bool:
    return bool(ws) and abs(median_db(ws) - played) <= 6


def leg3(tmp: Path) -> bool:
    a, b, c, log = three_tones(
        lambda pid: [str(CAPTURE), "stream-online", "--exclude-pid", str(pid)], tmp)
    ctl, _, _, _ = three_tones(
        lambda pid: [str(CAPTURE), "stream-online", "--exclude-pid", str(os.getpid())], tmp)
    ok = (max_db(a) <= MIXER_DB - 40 and within(b, BROWSER_DB) and within(c, AFPLAY_DB)
          and within(ctl, MIXER_DB))
    print(f"LEG 3 {'PASS' if ok else 'FAIL'}: --exclude-pid <mixer pid>; (a) BlackHole "
          f"{MIXER_DB:.0f} dBFS -> stream 1 max {fmt(max_db(a))} (pass <= {MIXER_DB - 40:.0f}); "
          f"(b) Chrome for Testing {BROWSER_DB:.0f} dBFS -> median {fmt(median_db(b))}; "
          f"(c) afplay {AFPLAY_DB:.0f} dBFS -> median {fmt(median_db(c))} (pass: within 6 dB); "
          f"control, mixer not excluded: (a) median {fmt(median_db(ctl))} (pass: within 6 dB)")
    print("  capture: " + " / ".join(l for l in log if l.startswith("THEM")))
    return ok


def leg4(tmp: Path) -> bool:
    a, b, c, _ = three_tones(lambda pid: [str(CAPTURE), "stream-online"], tmp)
    ok = within(a, MIXER_DB) and within(b, BROWSER_DB) and within(c, AFPLAY_DB)
    print(f"LEG 4 {'PASS' if ok else 'FAIL'}: no flag (today's SCK path); (a) BlackHole "
          f"{MIXER_DB:.0f} dBFS -> stream 1 median {fmt(median_db(a))}; (b) Chrome for Testing "
          f"{BROWSER_DB:.0f} dBFS -> median {fmt(median_db(b))}; (c) afplay {AFPLAY_DB:.0f} dBFS "
          f"-> median {fmt(median_db(c))} (pass: all within 6 dB)")
    return ok


def leg5(tmp: Path) -> bool:
    mixer = Mixer(delay=5.0, on=True)   # opens BlackHole ~5 s after capture starts, tone on
    try:
        cap = Capture([str(CAPTURE), "stream-online", "--exclude-pid", str(mixer.pid)])
        try:
            t_open = mixer.wait_open(15)
            time.sleep(10)
            ws = cap.windows(t_open, time.monotonic())
        finally:
            cap.stop()
    finally:
        mixer.close()
    quiet = [t for t, d in ws if d <= MIXER_DB - 40]
    after = [d for t, d in ws if t >= t_open + 5]
    first = None if not quiet else quiet[0] - t_open
    ok = bool(after) and max(after) <= MIXER_DB - 40
    print(f"LEG 5 {'PASS' if ok else 'FAIL'}: late PID (mixer opened BlackHole after capture "
          f"started); first window <= {MIXER_DB - 40:.0f} dB at "
          f"{'never' if first is None else f'+{first:.1f} s'} after its first audio; "
          f"max from +5 s on {fmt(max(after, default=float('-inf')))} over {len(after)} windows "
          f"(pass: <= {MIXER_DB - 40:.0f} from +5 s)")
    print("  capture: " + " / ".join(l for l in cap.log if l.startswith("THEM")))
    return ok


LEGS = {"3": leg3, "4": leg4, "5": leg5}

if __name__ == "__main__":
    if not CAPTURE.is_file():
        sys.exit(f"build first: swiftc -O app/capture/main.swift -o {CAPTURE}")
    chosen = sys.argv[1:] or list(LEGS)
    with tempfile.TemporaryDirectory() as d:
        results = []
        for leg in chosen:
            results.append(LEGS[leg](Path(d)))
            time.sleep(1)
    sys.exit(0 if all(results) else 1)
