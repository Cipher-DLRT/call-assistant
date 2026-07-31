# P0-c latency ledger — STT streaming: whisper.cpp WINS

**Date:** 2026-07-31 · **Runbook/metric:** docs/runbook-p0c-stt-speed.md
**Machine:** MacBook Air (M5), macOS 26.5.1, on mains vs battery not
controlled (single session, both engines same session, minutes apart).

## Configuration

| | whisper.cpp | faster-whisper |
|---|---|---|
| Version | 1.9.1 (Homebrew), ggml 0.18.0 | 1.2.1, CTranslate2 4.8.1, Python 3.12 |
| Compute | Metal GPU (+ CPU backend apple_m4 variant) | CPU, int8 |
| Model | Whisper small (ggml-small.bin, 465 MB) | Whisper small (CT2, HF cache) |
| Decoding | greedy, no context, single segment, en | greedy (beam 1), no context, no timestamps, en |

Audio: bench.wav — 60 s of real conversational speech @ 16 kHz mono
(check (a)'s local capture, converted with afconvert; never left the Mac).
Harnesses: spike/stt_bench/bench_whispercpp.c (in-process libwhisper, no
network listener) and bench_fasterwhisper.py. Metric: real-time-paced
sliding window, hop 1 s, window ≤ 10 s; latency = emit − window-end;
warmup decode excluded. Per-partial CSVs committed alongside
(results-whispercpp.csv, results-fasterwhisper.csv).

## Results (60 s run, full 10 s windows from T=10 on)

| | partials | dropped hops | p50 | p90 | model load | warmup |
|---|---|---|---|---|---|---|
| **whisper.cpp** | **60/60** | **0** | **0.313 s** | **0.348 s** | 0.15 s | 0.18 s |
| faster-whisper | 58/60 | 2 (T=32, 46) | 1.402 s | 1.867 s | 0.68 s | 1.79 s |

## Verdict

- P0 pass bar (p50 < 2 s): **both pass** — but faster-whisper shows a
  backlog sawtooth (latency climbs to ~2 s, drops a hop, recovers). On the
  M5 it runs barely faster than real time with 10 s windows; margin is thin.
- **Winner by numbers: whisper.cpp** — 4.5× lower p50 (0.313 vs 1.402 s),
  5× lower p90, zero dropped hops, never above 0.4 s. **P0/P1 build on
  whisper.cpp (Metal).**
- Headroom note: p50 0.313 s on small leaves room to consider medium for
  quality later; that is a NEW measurement, not an assumption.

## Build gotcha recorded for P1

Homebrew's libwhisper does NOT auto-load ggml compute backends; a bare
linkee gets `devices = 0` and aborts with `GGML_ASSERT(device) failed`.
The embedding process must call `ggml_backend_load_all()` (ggml-backend.h)
before `whisper_init_*`; brew ships the backend modules in
`/opt/homebrew/opt/ggml/libexec/*.so` (Metal, BLAS, per-chip CPU).

## Posture notes

- whisper-server exists in the brew package but was NOT used — no network
  listener was opened, localhost or otherwise.
- Downloads this check: whisper-cpp + python@3.12 (brew), ggml-small.bin
  (HF), faster-whisper + deps (PyPI), CT2 small model (HF) — all public
  artifacts, inbound only; no project or audio data transmitted.
