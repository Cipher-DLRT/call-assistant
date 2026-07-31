# Runbook P0-a — Granola coexistence check

**Question:** can a ScreenCaptureKit system-audio tap run while Granola records
simultaneously? (Two taps on one Mac is TBV, not assumed compatible.)

**Tool:** `spike/granola_coexist/granola-coexist-tap` (built from `main.swift`
with `swiftc -O main.swift -o granola-coexist-tap`). Captures system audio for
N seconds (default 30), prints a per-second level meter, writes `out.wav` to
the current directory. Requires Screen & System Audio Recording permission for
the terminal app that launches it (verified granted for Terminal, 2026-07-31).

## Design note — why headphones

Granola records BOTH the mic and system audio. If the fake-meeting video plays
through speakers, the mic hears it and Granola would transcribe the video words
even if its system-audio tap had died — a false pass. With headphones, the mic
hears (almost) nothing, so Granola's transcript containing the video words
proves its system tap stayed alive next to ours. Use headphones if at all
possible; if speakers are unavoidable, record that caveat in the result doc.

## Procedure (operator, one step at a time)

1. Plug in / connect headphones so the Mac's sound output goes to them.
   Expect: Sound output device in the menu bar shows the headphones.
2. Start a Granola recording (new note, as for a meeting). Expect: Granola
   shows it is actively recording/transcribing.
3. Start a video with clear continuous speech (any talk on YouTube), audible
   in the headphones.
4. Say "go" — Claude Code runs `./granola-coexist-tap 60` from
   `spike/granola_coexist/`. Expect: `capture started: 48000 Hz, 2 ch`, then
   ~60 lines `t+NNs  <level> dBFS  SOUND` (mostly SOUND while speech plays),
   then a `done:` summary and the out.wav path.
5. Stop the video and stop the Granola recording.
6. Verify BOTH sides got the audio:
   a. Play `spike/granola_coexist/out.wav` — it must contain the video speech.
   b. Open the Granola note — its transcript must contain the video's words
      for the same time span.

## Verdict

- **PASS:** 6a AND 6b both true → the two taps coexist; P0 capture design can
  assume SCK system-audio capture works alongside Granola.
- **FAIL:** either side silent, errored, or missing the span → full stop,
  record exactly what happened; the capture design must change (do not
  work around silently).

Result doc: `docs/p0a-granola-coexist-result.md`, committed with its STATUS.md
line in the same commit.
