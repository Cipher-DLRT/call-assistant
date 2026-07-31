# Runbook P0-b — Lark M2 receiver: what does it present?

**Questions:** (1) sample rate / channel count as seen by THIS Mac (not
memory); (2) CRITICAL: do TX1 and TX2 arrive as separate left/right channels?
If yes → deterministic per-person channels for in-person calls; voiceprint
demoted to backup (flag loudly per session ruling 2b).

**Tool:** `spike/lark_channels/lark-channels-tap` (built from `main.swift`
with `swiftc -O main.swift -o lark-channels-tap`). Records N seconds (default
20, first arg) from the input device whose name contains "Wireless" (second
arg overrides), prints a per-second L/R level meter, writes `lark.wav`.
Requires Microphone permission for the launching terminal app.

## Design note — why scratching

Speech in the room reaches BOTH transmitters through the air, so talking into
one TX still shows level on the other. Scratching a TX's mic grille is heard
essentially only by that capsule — a scratch that lights up one channel and
not the other is proof of separation; a scratch that moves both channels
identically is proof the receiver is mixing.

## Procedure (operator, one step at a time)

1. Power on BOTH transmitters, confirm both show paired/linked to the
   receiver. Pick one and call it **A** (mark it if unmarked); the other is
   **B**. Keep them at least an arm's length apart.
2. Say "go" — Claude Code runs a 24 s recording. During it:
   - seconds ~0–8: scratch A's mic grille repeatedly (firm finger rubs)
   - seconds ~8–12: touch nothing
   - seconds ~12–20: scratch B's mic grille repeatedly
   - seconds ~20–24: touch nothing
3. Read the meter lines together.

## Reading the meter

- **SEPARATE:** A-scratches spike ONE channel (other stays near floor), and
  B-scratches spike the OTHER → TX↔channel mapping is deterministic. Record
  which TX = which channel. FLAG LOUDLY: attribution design changes.
- **MIXED:** every scratch moves L and R together (near-identical dB) → the
  receiver is summing. Before concluding, check the receiver's stereo/mono
  mode setting (hardware/app), switch to stereo, re-run once. Only a mixed
  result IN stereo mode closes the question as "no separation".
- Smoke-run observation (2026-07-31, pre-test): L and R identical to 0.1 dB
  on room noise — consistent with mix mode; test must decide.

Result doc: `docs/p0b-lark-channels-result.md`, committed with its STATUS.md
line in the same commit.
