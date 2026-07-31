# P0-b result — Lark M2 receiver: 48 kHz confirmed; NO channel separation

**Date:** 2026-07-31 · **Runbook:** docs/runbook-p0b-lark-channels.md
**Machine:** MacBook Air (M5), macOS 26.5.1
**Hardware:** Lark M2, USB-C (mobile) receiver only — kit does NOT include the
camera-version receiver.

## Question 1 — what does it present? (verified on hardware)

- Appears as "Wireless microphone", manufacturer Shenzhen Hollyland,
  Transport: USB (system_profiler SPAudioDataType).
- **2 input channels @ 48 kHz**; recorded from it successfully with a stock
  AVAudioEngine tap — standard USB Audio Class behavior, no driver needed.
- CLAUDE.md verify item "presents as standard USB Audio Class @48 kHz on THIS
  Mac" → **confirmed**.

## Question 2 (CRITICAL) — do TX1/TX2 arrive as separate L/R channels?

**NO — on this receiver they arrive as one summed mix duplicated to both
channels.**

Evidence, scratch test (scratching a TX's grille is heard only by that
capsule):

- Run 1 (operator scratched only TX A — protocol misunderstanding, kept as
  partial evidence): A-phase elevation visible, L ≡ R to 0.1 dB throughout.
- Run 2 (clean, both TXs): A scratches s6–12 (≈ −37 dBFS), pause s13–18
  (≈ −44 floor), B scratches s19–24 (≈ −30). **Every second: L ≡ R to
  0.1 dB, through both scratch phases.** Both TXs live, both summed.

Vendor documentation agrees: mono/stereo switching exists only on the
camera-version RX ("The camera version RX supports two recording modes: mono
and stereo… by pressing the Mode Switching & Pairing button") — no stereo
mode is documented for the USB-C mobile RX.
Sources: hollyland.com/product/lark-m2 (fetched 2026-07-31); CineD Lark M2
announcement.

## Design implication

No loud flag: the hoped-for deterministic per-person channels are NOT
available on this hardware path. **Law 8 stands as written — in-person
attribution: voiceprint primary; online: channel split (Lark = operator mic,
system audio = far side).** The 2-channel presentation carries no attribution
information in-person.

Option recorded, not planned: the camera-version Lark M2 RX (3.5 mm, has the
documented stereo switch) could be acquired and tested against the Mac later
if deterministic in-person channels become worth the purchase; that would be
a new verify-before-build item.

## Incidental note

Scratch transients registered modest levels (−30 to −40 dBFS) — possibly the
TXs' noise cancellation attenuating non-speech noise. Not investigated
further; irrelevant to this question, possibly relevant to P0 audio quality
expectations.
