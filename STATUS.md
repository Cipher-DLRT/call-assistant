# STATUS — call-assistant

**Phase:** P0 — capture spike (started 2026-07-31)
**Now:** STOPPED per session ruling 6 — P0 session work complete (checks a/b/c closed, enrollment done)
**Next:** the two live meeting legs (online channel-split ≥98%, in-person voiceprint ≥90%), scheduled separately. No hint logic, no EQ14, no new network surface until then.

## Log
- 2026-07-31 · repo skeleton created (spike/ prompts/ scripts/ docs/); P0 session rulings recorded in docs/p0-session-rulings.md
- 2026-07-31 · granola-coexist spike built, compiles clean, 3 s smoke run captured real system audio (48 kHz/2 ch, Terminal permission granted); runbook written; check itself NOT yet run — audio (*.wav) globally gitignored per law 1
- 2026-07-31 · **check (a) PASS** — SCK tap + Granola recorded the same 60 s fake meeting simultaneously, headphone discriminator in effect; evidence in docs/p0a-granola-coexist-result.md
- 2026-07-31 · lark-channels recorder built; smoke run: "Wireless microphone" (Hollyland) presents 2 ch @ 48 kHz over USB on this Mac; L/R identical on room noise (mix mode suspected, not concluded); scratch test pending
- 2026-07-31 · **check (b) CLOSED** — 48 kHz USB Audio Class confirmed on hardware; TX1/TX2 do NOT separate: scratch test showed one mix on both channels, vendor docs confirm USB-C RX has no stereo mode (camera RX only, not in kit). No design change: law 8 stands, voiceprint primary in-person. Evidence in docs/p0b-lark-channels-result.md
- 2026-07-31 · **check (c) CLOSED — whisper.cpp WINS** — measured on 60 s real speech, small model: whisper.cpp/Metal p50 0.313 s p90 0.348 s (60/60 partials); faster-whisper/CPU p50 1.402 s p90 1.867 s (2 dropped hops). Both under the 2 s bar; whisper.cpp picked by numbers. Ledger + CSVs in docs/p0c-stt-latency-ledger.md, spike/stt_bench/
- 2026-07-31 · **enrollment DONE — USABLE** — ECAPA (Apache-2.0, local) on 60 s Lark speech: same-speaker 0.9249, other-speaker 0.1828, margin 0.7421. Stored Mac-only in gitignored spike/voiceprint/. Lark tap wav-header bug found, take salvaged losslessly, fix verified. Evidence in docs/p0-enrollment-result.md. **P0 session portion COMPLETE — STOPPED per ruling 6**
