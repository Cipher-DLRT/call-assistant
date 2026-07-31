# P0 check (c): faster-whisper streaming-partial latency harness.
# Implements the metric in docs/runbook-p0c-stt-speed.md: real-time-paced
# sliding window (hop 1 s, window <= 10 s), latency = emit_time - T_window_end.
# Usage: python bench_fasterwhisper.py <wav 16k mono s16> <out.csv> [max_seconds]

import math
import sys
import time
import wave

import numpy as np
from faster_whisper import WhisperModel

HOP, WIN, RATE = 1.0, 10.0, 16000

wav_path, csv_path = sys.argv[1], sys.argv[2]
wf = wave.open(wav_path)
assert wf.getframerate() == RATE and wf.getnchannels() == 1 and wf.getsampwidth() == 2
audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
total = len(audio) / RATE
if len(sys.argv) > 3:
    total = min(total, float(sys.argv[3]))

t0 = time.monotonic()
model = WhisperModel("small", device="auto", compute_type="int8")
print(f"model load: {time.monotonic() - t0:.2f}s")


def decode(win: np.ndarray) -> str:
    segs, _ = model.transcribe(
        win, language="en", beam_size=1, without_timestamps=True,
        condition_on_previous_text=False, vad_filter=False)
    return "".join(s.text for s in segs)  # exhausting the generator = the decode


t0 = time.monotonic()
decode(audio[:RATE])  # warmup, excluded from measurement
print(f"warmup decode (1 s audio): {time.monotonic() - t0:.2f}s")

rows = []
start = time.monotonic()
last_end = 0.0
while last_end < total:
    elapsed = time.monotonic() - start
    T = min(math.floor(elapsed / HOP) * HOP, total)
    if T <= last_end:
        time.sleep(max(0.0, (start + last_end + HOP) - time.monotonic()))
        continue
    win = audio[int(max(0.0, T - WIN) * RATE):int(T * RATE)]
    text = decode(win)
    lat = (time.monotonic() - start) - T
    print(f"T={T:4.1f}s  lat={lat:.3f}s")
    rows.append((T, lat, text.replace('"', "'")))
    last_end = T

with open(csv_path, "w") as f:
    f.write("T,latency_s,text\n")
    for T, lat, text in rows:
        f.write(f'{T:.1f},{lat:.3f},"{text}"\n')

lats = sorted(r[1] for r in rows)
n = len(lats)
print(f"partials: {n}  p50: {lats[n // 2]:.3f}s  p90: {lats[int(0.9 * (n - 1))]:.3f}s")
