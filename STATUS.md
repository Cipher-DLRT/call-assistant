# STATUS — call-assistant

**Phase:** P0 — capture spike (started 2026-07-31)
**Now:** check (c) STT speed — faster-whisper vs whisper.cpp streaming on the M5, p50 partial latency
**Next:** (a) Granola coexistence → (b) Lark M2 receiver → (c) STT speed → voiceprint enrollment → STOP (live meeting legs scheduled separately)

## Log
- 2026-07-31 · repo skeleton created (spike/ prompts/ scripts/ docs/); P0 session rulings recorded in docs/p0-session-rulings.md
- 2026-07-31 · granola-coexist spike built, compiles clean, 3 s smoke run captured real system audio (48 kHz/2 ch, Terminal permission granted); runbook written; check itself NOT yet run — audio (*.wav) globally gitignored per law 1
- 2026-07-31 · **check (a) PASS** — SCK tap + Granola recorded the same 60 s fake meeting simultaneously, headphone discriminator in effect; evidence in docs/p0a-granola-coexist-result.md
- 2026-07-31 · lark-channels recorder built; smoke run: "Wireless microphone" (Hollyland) presents 2 ch @ 48 kHz over USB on this Mac; L/R identical on room noise (mix mode suspected, not concluded); scratch test pending
- 2026-07-31 · **check (b) CLOSED** — 48 kHz USB Audio Class confirmed on hardware; TX1/TX2 do NOT separate: scratch test showed one mix on both channels, vendor docs confirm USB-C RX has no stereo mode (camera RX only, not in kit). No design change: law 8 stands, voiceprint primary in-person. Evidence in docs/p0b-lark-channels-result.md
