# P0 enrollment result — voiceprint USABLE

**Date:** 2026-07-31 · **Runbook:** docs/runbook-p0-enrollment.md
**Model:** speechbrain/spkrec-ecapa-voxceleb (ECAPA-TDNN, 192-dim),
license Apache-2.0 verified at the HF model card 2026-07-31, ungated,
runs locally (PyTorch CPU in spike/stt_bench/venv). CLAUDE.md verify item
"pyannote-class voiceprint model: local runtime + license check" → closed.

## Procedure (as run)

One Lark TX on (worn as in meetings), second TX off, quiet room. 60 s of
natural speech recorded from the Lark via spike/lark_channels tap, converted
to 16 kHz mono, enrolled via scripts/enroll_voiceprint.py. Negative probe:
the bench.wav speaker (different voice, same format).

## Numbers (verified this turn)

- Same-speaker probe (held-out last 1/3 of recording): **cosine 0.9249**
- Other-speaker probe: **cosine 0.1828**
- Margin: **0.7421** (proposed usable bar: > 0.3) → **ENROLLMENT USABLE**

## Storage (law 8: Mac only)

`spike/voiceprint/` — whole directory gitignored: enrollment audio,
model cache, `operator_ecapa.pt` + metadata json. Nothing committed;
this doc carries numbers only.

## Incident during the run

The Lark recorder never finalized its WAV header on exit (data size 0 in
header; all audio bytes intact on disk). The 60 s enrollment take was
salvaged losslessly by re-parsing the file (float32 interleaved after the
data header) — no re-recording. Root cause fixed in
spike/lark_channels/main.swift (finalize AVAudioFile before exit, same
pattern as the Granola tap), recompiled, fix verified: a 2 s test recording
now reports the correct header duration. Note: the P0-b scratch-test
conclusions used the live meter output, not the wav, so they are unaffected.
