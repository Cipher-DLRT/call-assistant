# Runbook P0-c — STT speed: faster-whisper vs whisper.cpp on the M5

**Question:** which engine hits streaming partials with p50 latency < 2 s on
this M5 (P0 pass bar)? Winner picked by numbers, not preference.

## Metric definition (fixed BEFORE measuring)

Simulated real-time streaming over the same local 60 s speech file for both
engines (bench.wav = check (a)'s out.wav, converted to 16 kHz mono — real
conversational speech, never leaves the Mac):

- Audio is "fed" in real time: sample at audio-time T is available at wall
  time T after start.
- Hop H = 1.0 s. A decode window is the most recent min(10 s, elapsed) of
  audio, ending at audio-time T_i.
- After each decode finishes, the harness immediately decodes the freshest
  available window (intermediate hops are dropped, as a live system would).
  If the engine is faster than the hop, it waits for the next hop boundary.
- **Partial latency_i = wall_time(partial text emitted) − T_i.** This
  includes decode time plus any backlog from falling behind real time.
- Report p50 and p90 over all emitted partials, plus model load time
  (excluded from latency) and realtime factor.

## Engine configuration (apples to apples)

- Model: Whisper **small**, English, greedy decoding (beam 1), no
  word-level timestamps. If both engines miss the bar on small, re-run on
  base and note the quality tradeoff for the ledger.
- whisper.cpp: Metal enabled (Apple Silicon default), harness calls
  libwhisper in-process or via whisper-cli against a persistent process —
  NO network listener (posture: no new network surface, even localhost).
- faster-whisper: CTranslate2 backend, int8 compute on CPU (its Apple
  Silicon default), model loaded once, windows transcribed in-process.

## Pass / winner

- Pass bar (CLAUDE.md P0): p50 partial latency < 2 s.
- Winner: lower p50; tie broken by p90; both recorded in the latency ledger
  either way.

Result doc: `docs/p0c-stt-latency-ledger.md`, committed with its STATUS.md
line in the same commit.
