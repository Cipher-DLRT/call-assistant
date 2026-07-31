# Leg 1 — online meeting, channel-split attribution (bar: ≥ 98%)

**What this measures:** every utterance the system hears is labeled ME (came
from the Lark = you) or THEM (came from system audio = the far side). You
grade a ~60-utterance sample; P0 passes this leg at ≥ 98% correct labels.

**THE STOP RULE: if any step shows something different from its "Expect"
line, stop there. Press Ctrl-C in the capture window if it is running. Do
not improvise; bring the mismatch back to the call-assistant session.**

Wherever a command says `DATE`, type today's date instead, like
`legs/leg1-2026-08-05` — and keep using that exact same name in every later
command, even if you grade on a different day.

## Before the meeting (2–3 minutes)

1. Plug the Lark receiver into the Mac, turn on your transmitter, clip it on.
   Expect: the receiver/TX link lights steady.

2. Wear your normal earphones/headset for the call. (Speakers leak the far
   side's voice into your mic and will cost attribution points.)

3. Open Terminal and go to the project.

       cd ~/dev/call-assistant

   Expect: the prompt returns, no error.

4. Start the capture (one line):

       ./spike/leg_capture/leg-capture online legs/leg1-DATE

   Expect (first three lines, ~2 s):

       THEM: system audio (ScreenCaptureKit) — 2 ch @ 48000 Hz → them.wav
       ME: Wireless microphone — 2 ch @ 48000 Hz → me.wav
       capturing → /Users/rami/dev/call-assistant/legs/leg1-DATE  (Ctrl-C to stop)

   Any line starting `CAPTURE FAILED` → STOP.

5. Sanity check that both sides flow. Say "testing one two three" out loud,
   and play any sound (the meeting join chime works). A level line prints
   every 5 seconds; while you speak, ME must rise clearly above −40; while
   sound plays, THEM must rise above −40. Example of a healthy line:

       t+00:05  THEM  -16.3 dBFS | ME  -32.0 dBFS

   If either side stays near −60 while its sound is happening → STOP.

## During the meeting

Nothing. Behave normally. Leave the Terminal window open; the level lines
keep printing every 5 seconds.

## After the meeting

6. Click into the Terminal window and press Ctrl-C.
   Expect:

       Ctrl-C — stopping…
       stopped cleanly — files finalized: THEM NNNN.Ns → them.wav, ME NNNN.Ns → me.wav

   The two durations should be about the meeting length.

7. Build the grading sheet (transcription is local; a few minutes for a long
   call):

       ./spike/stt_bench/venv/bin/python scripts/grade_leg.py leg1 legs/leg1-DATE

   Expect (numbers will differ):

       utterances: 220 (ME 90, THEM 130)
       sheet: legs/leg1-DATE/sheet.md  (60 rows)
       next: mark the sheet, then run scripts/score_leg.py legs/leg1-DATE/sheet.md

   `no utterances found` → STOP.

8. Open `legs/leg1-DATE/sheet.md` in any text editor. For each row put an x
   in exactly one box: **correct** if the ME/THEM label matches who really
   spoke that line, **wrong** if not. Grading hint: an ME row with dB of −50
   or lower is almost always the far side bleeding into your mic — if the
   text is the other person's words, that row is **wrong**.

9. Score it:

       ./spike/stt_bench/venv/bin/python scripts/score_leg.py legs/leg1-DATE/sheet.md -o docs/leg-1-score.md

   Expect (your numbers):

       sheet: legs/leg1-DATE/sheet.md
       rows: 60
       graded: 60/60 (blank 0, double-marked 0)
       correct: 59  wrong: 1
       attribution: 98.3%  bar: 98%  → PASS
       summary written: docs/leg-1-score.md

10. Record it in STATUS.md — open STATUS.md and add one log line (fill in
    your numbers):

        - DATE · **leg 1 RUN** — online channel-split attribution XX.X% vs 98% bar → PASS/FAIL; sheet legs/leg1-DATE/sheet.md, score docs/leg-1-score.md

11. Commit — sheet, score, STATUS only (audio and transcripts stay
    untracked by design):

        git add legs/leg1-DATE/sheet.md docs/leg-1-score.md STATUS.md
        git commit -m "p0 leg1: online attribution XX.X% (bar 98) — PASS"

    Expect: `[main …] 3 files changed …`
