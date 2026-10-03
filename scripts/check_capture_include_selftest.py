#!/usr/bin/env python3
"""Measured check for `capture stream-online --include-pid` (issue #4, lane ca-capture-include).

Four test-tone sources play at once, each on its own frequency, and stream 1 (system audio)
is measured per frequency in 0.5 s windows (FFT bin, sine-peak dBFS; at 16 kHz every
source frequency is an exact bin):
  A  Playwright's Google Chrome for Testing (headed, local file:// page), WebAudio 1 kHz
     at -50 dBFS: the listed pid is A's browser pid; Chrome plays from a helper process
  B  a second Chrome for Testing instance (its own user-data-dir), 1.5 kHz at -50 dBFS
  C  afplay, 2 kHz at -50 dBFS to the default output
  M  a separate python process, 700 Hz at -20 dBFS into BlackHole 2ch

  leg 2  minimal include tap (CAPTURE_BIN=<probe>, else the built binary), sources first:
         A within 6 dB of played; B, C and M each >= 40 dB below played
  leg 4  through the built binary: (a) capture starts before A plays; A within 5 s of first
         playback, no restart; (b) A's audio helper killed, tone restarted; back within 5 s;
         (c) a listed pid that is not running: frames flow, silence, one stderr line
  leg 5  leg 2's four sources through the built binary, same PASS
  leg 6  unchanged paths: no flag (today's SCK path, capture first; numbers recorded);
         --exclude-pid <M> (M >= 40 dB below, A and C present); exclude late-open (M opens
         BlackHole ~4 s after capture starts; >= 40 dB below from +5 s after its first audio)

Test tones only; no call audio is recorded or kept. Needs the display on and the screen
unlocked (SCK path), and the TCC grants of the calling terminal.

usage: spike/stt_bench/venv/bin/python scripts/check_capture_include_selftest.py [leg ...]
"""
import os
import signal
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
WIN = RATE // 2          # 0.5 s windows: 2 Hz bins, every source frequency is exact
A_HZ, B_HZ, C_HZ, M_HZ = 1000, 1500, 2000, 700
A_DB, B_DB, C_DB, M_DB = -50.0, -50.0, -50.0, -20.0
FREQS = {"A": A_HZ, "B": B_HZ, "C": C_HZ, "M": M_HZ}
PLAYED = {"A": A_DB, "B": B_DB, "C": C_DB, "M": M_DB}


def levels(x: np.ndarray) -> dict:
    """Sine-peak dBFS per source frequency and the window's RMS dBFS (key 'rms')."""
    spec = np.abs(np.fft.rfft(x.astype(np.float64)))
    out = {k: 20 * np.log10(max(2 * spec[f * len(x) // RATE] / len(x), 1e-10))
           for k, f in FREQS.items()}
    out["rms"] = 20 * np.log10(max(float(np.sqrt(np.mean(x.astype(np.float64) ** 2))), 1e-10))
    return out


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

    def windows(self, t0: float, t1: float) -> list[tuple[float, dict]]:
        """(end time, levels) per full 0.5 s window of samples that arrived in [t0, t1]."""
        with self.lock:
            chunks = [c for c in self.chunks if t0 <= c[0] <= t1]
        out, buf = [], np.zeros(0, np.float32)
        for t, x in chunks:
            buf = np.concatenate([buf, x])
            while len(buf) >= WIN:
                out.append((t, levels(buf[:WIN])))
                buf = buf[WIN:]
        return out

    def them(self) -> str:
        return " / ".join(l for l in self.log if l.startswith("THEM"))

    def stop(self):
        self.proc.send_signal(signal.SIGINT)
        try:
            self.proc.wait(10)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def med(ws, k) -> float:
    return float(np.median([d[k] for _, d in ws])) if ws else float("-inf")


def mx(ws, k) -> float:
    return max((d[k] for _, d in ws), default=float("-inf"))


def fmt(db: float) -> str:
    return "no samples" if db == float("-inf") else f"{db:.1f} dB"


def present(ws, k) -> bool:
    return bool(ws) and abs(med(ws, k) - PLAYED[k]) <= 6


def absent(ws, k) -> bool:
    return bool(ws) and mx(ws, k) <= PLAYED[k] - 40


# ---- tone sources ----------------------------------------------------------
MIXER_SRC = """
import sys, time
db, hz, delay, on = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4] == "on"
time.sleep(delay)   # before the import: PortAudio's init registers the process with Core Audio
import numpy as np, sounddevice as sd
dev = next(i for i, d in enumerate(sd.query_devices())
           if "BlackHole 2ch" in d["name"] and d["max_output_channels"] >= 2)
sr, amp, st = 48000, 10 ** (db / 20), {"on": on, "ph": 0}
def cb(out, frames, t, status):
    if st["on"]:
        n = np.arange(st["ph"], st["ph"] + frames); st["ph"] += frames
        x = amp * np.sin(2 * np.pi * hz * n / sr)
    else:
        x = np.zeros(frames)
    out[:, 0] = x; out[:, 1] = x
with sd.OutputStream(samplerate=sr, device=dev, channels=2, dtype="float32", callback=cb):
    print("open", flush=True)
    for line in sys.stdin:
        cmd = line.strip()
        if cmd == "quit": break
        st["on"] = cmd == "on"
"""


class Mixer:
    """Separate python process writing a 700 Hz tone into BlackHole 2ch (stdin: on/off/quit)."""

    def __init__(self, delay: float = 0.0, on: bool = True):
        self.proc = subprocess.Popen([PY, "-c", MIXER_SRC, str(M_DB), str(M_HZ), str(delay),
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

    def close(self):
        try:
            self.proc.stdin.write("quit\n")
            self.proc.stdin.flush()
            self.proc.wait(5)
        except Exception:
            self.proc.kill()


def afplay(secs: float, tmp: Path) -> subprocess.Popen:
    path = tmp / f"tone{C_HZ}.wav"
    sr = 48000
    t = np.arange(int(sr * secs)) / sr
    x = (10 ** (C_DB / 20) * np.sin(2 * np.pi * C_HZ * t) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(x.tobytes())
    return subprocess.Popen(["afplay", str(path)])


PAGE = """<!doctype html><title>test tone</title><body>
<script>
window.startTone = (db, hz) => {
  const ctx = new AudioContext();
  const osc = ctx.createOscillator(); osc.frequency.value = hz;
  const g = ctx.createGain(); g.gain.value = Math.pow(10, db / 20);
  osc.connect(g).connect(ctx.destination); osc.start();
  window._ctx = ctx;
  return ctx.resume().then(() => ctx.state);
};
window.stopTone = () => window._ctx && window._ctx.close();
</script></body>"""


class Browser:
    """One Playwright Google Chrome for Testing instance (headed, own temp user-data-dir)."""

    def __init__(self, pw, tmp: Path):
        page_path = tmp / "tone.html"
        page_path.write_text(PAGE)
        self.browser = pw.chromium.launch(
            headless=False, args=["--autoplay-policy=no-user-gesture-required"])
        info = self.browser.new_browser_cdp_session().send("SystemInfo.getProcessInfo")
        self.pid = next(p["id"] for p in info["processInfo"] if p["type"] == "browser")
        self.page = self.browser.new_page()
        self.page.goto(page_path.as_uri())

    def start_tone(self, db: float, hz: int):
        state = self.page.evaluate(f"window.startTone({db}, {hz})")
        if state != "running":
            raise RuntimeError(f"browser AudioContext state {state}")

    def stop_tone(self):
        self.page.evaluate("window.stopTone()")

    def audio_helper(self) -> int | None:
        """The child of this browser pid that runs Chrome's audio service."""
        ps = subprocess.run(["ps", "-axo", "pid=,ppid=,command="], capture_output=True,
                            text=True).stdout
        for row in ps.splitlines():
            pid, ppid, cmd = row.split(None, 2)
            if int(ppid) == self.pid and "audio.mojom.AudioService" in cmd:
                return int(pid)
        return None

    def close(self):
        self.browser.close()


class Sources:
    """A, B, C and M from the module docstring."""

    def __init__(self, tmp: Path):
        from playwright.sync_api import sync_playwright
        self.tmp = tmp
        self.pw = sync_playwright().start()
        self.a = Browser(self.pw, tmp)
        self.b = Browser(self.pw, tmp)
        self.m = Mixer()
        self.c: subprocess.Popen | None = None
        self.m.wait_open(10)

    def all_on(self, secs: float):
        self.a.start_tone(A_DB, A_HZ)
        self.b.start_tone(B_DB, B_HZ)
        self.c = afplay(secs, self.tmp)

    def close(self):
        for f in (self.m.close, self.a.close, self.b.close, self.pw.stop):
            try:
                f()
            except Exception:
                pass
        if self.c and self.c.poll() is None:
            self.c.kill()


def binary() -> str:
    return os.environ.get("CAPTURE_BIN", str(CAPTURE))


def four_sources(cmd, tmp: Path, sources_first: bool = True):
    """Plays A, B, C, M together; cmd(sources) -> capture argv; returns 4 s of windows + log."""
    src = Sources(tmp)
    try:
        if sources_first:
            src.all_on(12); time.sleep(2)
        cap = Capture(cmd(src))
        try:
            if not sources_first:
                time.sleep(1.5); src.all_on(10)
            time.sleep(1.5)
            t0 = time.monotonic(); time.sleep(4)
            ws = cap.windows(t0, time.monotonic())
        finally:
            cap.stop()
    finally:
        src.close()
    return ws, cap


def tree_line(leg: str, what: str, ws, cap) -> bool:
    ok = present(ws, "A") and absent(ws, "B") and absent(ws, "C") and absent(ws, "M")
    print(f"LEG {leg} {'PASS' if ok else 'FAIL'}: {what}; A Chrome for Testing {A_DB:.0f} dBFS "
          f"-> stream 1 median {fmt(med(ws, 'A'))} (pass: within 6 dB); B second Chrome for "
          f"Testing {B_DB:.0f} -> max {fmt(mx(ws, 'B'))}; C afplay {C_DB:.0f} -> max "
          f"{fmt(mx(ws, 'C'))}; M BlackHole {M_DB:.0f} -> max {fmt(mx(ws, 'M'))} "
          f"(pass: each >= 40 dB below played); {len(ws)} windows")
    print("  capture: " + cap.them())
    return ok


def include(src) -> list[str]:
    return [binary(), "stream-online", "--include-pid", str(src.a.pid)]


# ---- legs ------------------------------------------------------------------
def leg2(tmp: Path) -> bool:
    ws, cap = four_sources(include, tmp)
    return tree_line("2", f"minimal include tap ({Path(binary()).name}) --include-pid <A browser "
                          "pid>, sources playing before capture starts", ws, cap)


def first_back(cap, t_play: float, t_end: float) -> float | None:
    """Seconds from t_play to the first window where A is within 6 dB of played."""
    for t, d in cap.windows(t_play, t_end):
        if abs(d["A"] - A_DB) <= 6:
            return t - t_play
    return None


def leg4(tmp: Path) -> bool:
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    a = Browser(pw, tmp)
    try:
        cap = Capture([str(CAPTURE), "stream-online", "--include-pid", str(a.pid)])
        try:
            # (a) late: A has not played anything when capture starts
            time.sleep(3)
            helper_before = a.audio_helper()
            t_play = time.monotonic(); a.start_tone(A_DB, A_HZ)
            time.sleep(8)
            late = first_back(cap, t_play, time.monotonic())
            ok_a = late is not None and late <= 5
            # (b) churn: kill A's audio helper (a child of A's browser pid), restart the tone
            helper = a.audio_helper()
            if helper is None:
                raise RuntimeError("no audio helper under A's browser pid")
            os.kill(helper, signal.SIGKILL)
            time.sleep(1)
            try:
                a.stop_tone()
            except Exception:
                pass
            t_restart = time.monotonic(); a.start_tone(A_DB, A_HZ)
            time.sleep(8)
            back = first_back(cap, t_restart, time.monotonic())
            helper_after = a.audio_helper()
            ok_b = back is not None and back <= 5 and helper_after not in (None, helper)
        finally:
            cap.stop()
    finally:
        a.close(); pw.stop()
    print(f"LEG 4a {'PASS' if ok_a else 'FAIL'}: late audio; capture started before A played "
          f"(audio helper at start: {helper_before or 'none'}); A on stream 1 within 6 dB at "
          f"{'never' if late is None else f'+{late:.1f} s'} after first playback "
          f"(pass: <= 5 s, no restart)")
    print(f"LEG 4b {'PASS' if ok_b else 'FAIL'}: churn; A's audio helper {helper} killed, "
          f"respawned as {helper_after}; A back within 6 dB at "
          f"{'never' if back is None else f'+{back:.1f} s'} after the tone restarted "
          f"(pass: <= 5 s, no restart)")
    print("  capture: " + cap.them())

    dead = 99999
    while True:
        try:
            os.kill(dead, 0); dead -= 1
        except ProcessLookupError:
            break
        except PermissionError:
            dead -= 1
    src = Sources(tmp)
    try:
        src.all_on(10)
        cap = Capture([str(CAPTURE), "stream-online", "--include-pid", str(dead)])
        try:
            time.sleep(1.5)
            t0 = time.monotonic(); time.sleep(4)
            ws = cap.windows(t0, time.monotonic())
        finally:
            cap.stop()
    finally:
        src.close()
    lines = [l for l in cap.log if "not running" in l]
    ok_c = len(ws) >= 6 and mx(ws, "rms") <= -90 and len(lines) == 1
    print(f"LEG 4c {'PASS' if ok_c else 'FAIL'}: --include-pid {dead} (not running) while A, B, C, "
          f"M play; {len(ws)} windows in 4 s, stream 1 max RMS {fmt(mx(ws, 'rms'))} (pass: frames "
          f"flow, <= -90); 'not running' stderr lines: {len(lines)} (pass: 1)")
    print("  capture: " + cap.them())
    return ok_a and ok_b and ok_c


def leg5(tmp: Path) -> bool:
    ws, cap = four_sources(
        lambda src: [str(CAPTURE), "stream-online", "--include-pid", str(src.a.pid)],
        tmp, sources_first=False)
    return tree_line("5", "real topology, built binary, --include-pid <A browser pid>, "
                          "capture started before the sources", ws, cap)


def leg6(tmp: Path) -> bool:
    # capture first: SCK does not pick up an afplay that started before the stream
    # (measured 2026-10-03, base binary and this lane alike)
    ws, _ = four_sources(lambda src: [str(CAPTURE), "stream-online"], tmp, sources_first=False)
    ok_n = present(ws, "A") and present(ws, "B") and present(ws, "C")
    print(f"LEG 6a {'PASS' if ok_n else 'FAIL'}: no flag (today's SCK path), capture started "
          f"first; A {fmt(med(ws, 'A'))}, B {fmt(med(ws, 'B'))}, C {fmt(med(ws, 'C'))} "
          f"(pass: within 6 dB of -50); "
          f"M BlackHole {M_DB:.0f} -> median {fmt(med(ws, 'M'))} (recorded: SCK does not capture "
          f"the windowless writer on this rig, 2026-09-26)")

    ws, cap = four_sources(
        lambda src: [str(CAPTURE), "stream-online", "--exclude-pid", str(src.m.pid)], tmp)
    ok_x = absent(ws, "M") and present(ws, "A") and present(ws, "C")
    print(f"LEG 6b {'PASS' if ok_x else 'FAIL'}: --exclude-pid <M pid>; M BlackHole {M_DB:.0f} -> "
          f"max {fmt(mx(ws, 'M'))} (pass <= {M_DB - 40:.0f}); A {fmt(med(ws, 'A'))}, "
          f"B {fmt(med(ws, 'B'))}, C {fmt(med(ws, 'C'))} (pass: A and C within 6 dB)")
    print("  capture: " + cap.them())

    mixer = Mixer(delay=4.0, on=True)   # opens BlackHole ~4 s after capture starts, tone on
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
    early = [d["M"] for t, d in ws if t < t_open + 5]
    after = [d["M"] for t, d in ws if t >= t_open + 5]
    ok_l = bool(after) and max(after) <= M_DB - 40
    print(f"LEG 6c {'PASS' if ok_l else 'FAIL'}: exclude late-open (M opened BlackHole after "
          f"capture started); max in its first 5 s {fmt(max(early, default=float('-inf')))}; "
          f"max from +5 s on {fmt(max(after, default=float('-inf')))} over {len(after)} windows "
          f"(pass: <= {M_DB - 40:.0f} from +5 s)")
    print("  capture: " + cap.them())
    return ok_n and ok_x and ok_l


LEGS = {"2": leg2, "4": leg4, "5": leg5, "6": leg6}

if __name__ == "__main__":
    if not Path(binary()).is_file() or not CAPTURE.is_file():
        sys.exit(f"build first: swiftc -O app/capture/main.swift -o {CAPTURE}")
    chosen = sys.argv[1:] or list(LEGS)
    with tempfile.TemporaryDirectory() as d:
        results = []
        for leg in chosen:
            try:
                results.append(LEGS[leg](Path(d)))
            except RuntimeError as e:   # e.g. a binary without --include-pid prints usage
                print(f"LEG {leg} FAIL: {str(e).splitlines()[0]}")
                print("  " + " / ".join(str(e).splitlines()[1:]))
                results.append(False)
            time.sleep(1)
    print(f"check_capture_include_selftest: {sum(results)} passed, {len(results) - sum(results)} failed")
    sys.exit(0 if all(results) else 1)
