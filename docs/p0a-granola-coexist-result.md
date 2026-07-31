# P0-a result — Granola coexistence check: PASS

**Date:** 2026-07-31 · **Runbook:** docs/runbook-p0a-granola-coexist.md
**Machine:** MacBook Air (M5), macOS 26.5.1 · **Granola:** 7.452.1

## Question

Can a ScreenCaptureKit system-audio tap capture while Granola records
simultaneously? (Two taps on one Mac was TBV, not assumed compatible.)

## Setup (as run)

- Output routed to wired earphones — verified via system_profiler: "External
  Headphones" was Default Output + Default System Output Device. Headphone
  discriminator in effect: the mic could not hear the fake meeting, so any
  Granola transcript of it must come from Granola's system-audio tap.
- Granola actively recording a new note.
- Fake meeting: YouTube talk with continuous speech, audible in earphones.
- Tap: spike/granola_coexist/granola-coexist-tap, 60 s run, launched from
  Terminal (Screen & System Audio Recording permission granted to Terminal).

## Evidence (verified this turn)

- Tap output: `capture started: 48000 Hz, 2 ch`; **60/60 seconds SOUND**,
  levels −13.6 to −19.7 dBFS, exit 0; out.wav written (gitignored per law 1).
- Operator listened to the first 15 s of out.wav: video speech clearly
  present.
- Operator opened the Granola note for the same span: transcript matched the
  video's words — Granola's tap stayed live next to ours.

## Verdict and implication

**PASS.** SCK system-audio capture and Granola recording coexist on this Mac.
The P0 capture design may assume the coexistence holds, including in-person
meetings where Granola captures simultaneously.

## Caveats

- Single 60 s run, one video, one macOS/Granola version (above). If either
  updates majorly before P1, a 60 s re-run is cheap insurance.
- Granola's own capture mechanism was not inspected — only its observable
  behavior (transcript produced while our tap ran).
