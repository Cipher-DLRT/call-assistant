# Runbook P0 — voiceprint enrollment (after checks a/b/c, before STOP)

**Purpose:** law 8 — one-time ~60 s enrollment of the operator's voice,
pyannote-class model, local, stored on the Mac only. In-person attribution
uses this as primary (check (b) removed the per-TX channel hope).

**Model:** speechbrain/spkrec-ecapa-voxceleb (ECAPA-TDNN). License verified
2026-07-31 at the HF model card: Apache-2.0, ungated. Runs locally via
PyTorch/CPU; weights (~80 MB) cached on first run into the gitignored
output dir.

## Storage

Everything derived from the operator's voice lives in `spike/voiceprint/`
(whole directory gitignored): enrollment wav, model cache, embedding
(`operator_ecapa.pt` + metadata json). Nothing is committed; only the
similarity numbers go into the result doc.

## Procedure (operator)

1. ONE Lark transmitter on (the one worn in meetings), second TX OFF, quiet
   room, TX clipped as worn in a real meeting.
2. On "go": 60 s recording via spike/lark_channels/lark-channels-tap (the
   Lark presents one mixed signal; with one TX that mix is just the operator).
   Speak naturally the whole time — normal meeting voice, any content.
3. Recording is converted to 16 kHz mono (afconvert) and fed to
   scripts/enroll_voiceprint.py with bench.wav (different speaker) as the
   negative probe.

## Verification (built into the script)

- First 2/3 of the recording → stored embedding; last 1/3 → positive probe;
  bench.wav speaker → negative probe.
- Expected: same-speaker cosine > 0.5, margin over other-speaker > 0.3 →
  "ENROLLMENT USABLE". Anything else → re-record (louder/closer/quieter
  room), full stop if a second attempt still fails.

Result doc: `docs/p0-enrollment-result.md` (numbers only, no audio paths
outside the repo), committed with its STATUS.md line in the same commit.
