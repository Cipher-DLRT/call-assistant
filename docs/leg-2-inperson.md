# Leg 2 — in-person 1-2-1, voiceprint attribution (bar: ≥ 90%)

**What this measures:** one room, one audio stream (the Lark). Each utterance
is labeled ME or THEM by comparing its voice against your enrolled voiceprint
(cosine vs threshold 0.55). You grade a ~60-utterance sample; the proceed bar
is ≥ 90% correct labels.

**THE STOP RULE: if any step shows something different from its "Expect"
line, stop there. Press Ctrl-C in the capture window if it is running. Do
not improvise; bring the mismatch back to the call-assistant session.**

Wherever a command says `DATE`, type today's date instead, like
`legs/leg2-2026-08-05` — and keep the same name in every later command.

## Before the meeting (2 minutes)

1. Plug the Lark receiver into the Mac, turn on your transmitter, clip it on.
   Optional but recommended: clip the second transmitter on the other person
   — the receiver mixes both into one stream, so attribution is still done by
   voiceprint, but their audio (and their transcript) gets much cleaner.
   Expect: link light(s) steady.

2. Open Terminal and go to the project.

       cd ~/dev/call-assistant

3. Start the capture (one line):

       ./spike/leg_capture/leg-capture single Wireless legs/leg2-DATE

   Expect (first two lines):

       MIX: Wireless microphone — 2 ch @ 48000 Hz → mix.wav
       capturing → /Users/rami/dev/call-assistant/legs/leg2-DATE  (Ctrl-C to stop)

   `CAPTURE FAILED` → STOP.

4. Sanity: say "testing one two three". In the next 5-second level line MIX
   must rise clearly above −40 while you speak:

       t+00:05  MIX  -31.0 dBFS

   Stays near −60 while you talk → STOP.

## During the meeting

Nothing. Behave normally. Leave the Terminal window open.

## After the meeting

5. Ctrl-C in the Terminal window.
   Expect: `stopped cleanly — files finalized: MIX NNNN.Ns → mix.wav`

6. Build the grading sheet (local; a few minutes — voiceprint scoring adds a
   little time):

       ./spike/stt_bench/venv/bin/python scripts/grade_leg.py leg2 legs/leg2-DATE

   Expect (numbers differ):

       utterances: 240 (ME 130, THEM 110)
       sheet: legs/leg2-DATE/sheet.md  (60 rows)
       next: mark the sheet, then run scripts/score_leg.py legs/leg2-DATE/sheet.md

7. Open `legs/leg2-DATE/sheet.md` and mark every row: **correct** if the
   ME/THEM label matches who really spoke, **wrong** if not. The `sim` column
   is the voice-match score that produced the label (≥ 0.55 → ME) — useful
   context, but grade by who actually spoke, not by the number.

8. Score it:

       ./spike/stt_bench/venv/bin/python scripts/score_leg.py legs/leg2-DATE/sheet.md -o docs/leg-2-score.md

   Expect: `attribution: XX.X%  bar: 90%  → PASS` (or FAIL), then
   `summary written: docs/leg-2-score.md`.

9. Add the STATUS.md log line (fill in your numbers):

       - DATE · **leg 2 RUN** — in-person voiceprint attribution XX.X% vs 90% bar → PASS/FAIL; sheet legs/leg2-DATE/sheet.md, score docs/leg-2-score.md

10. Commit — sheet, score, STATUS only:

        git add legs/leg2-DATE/sheet.md docs/leg-2-score.md STATUS.md
        git commit -m "p0 leg2: in-person attribution XX.X% (bar 90) — PASS"

## Leg 3 (optional, ~5 minutes total) — cross-mic transfer number

Your voiceprint was enrolled through the Lark. This measures how well it
recognizes you through the MacBook's built-in mic instead — no Lark needed,
transmitters can stay off. No pass bar; the number informs the in-person
design. Do it alone in a quiet room.

1. From the project directory, start a 3-minute capture from the built-in
   mic and talk the whole time (any content, normal voice):

       ./spike/leg_capture/leg-capture single "MacBook Air Microphone" legs/leg3-DATE 180

   Expect: `MIX: MacBook Air Microphone — 1 ch @ 48000 Hz → mix.wav`, level
   lines above −40 while you speak, auto-stop at 3:00 with
   `stopped cleanly — files finalized: MIX 180.0s → mix.wav`.

2. Grade — the score is computed automatically (every utterance is you, so
   no marking is needed):

       ./spike/stt_bench/venv/bin/python scripts/grade_leg.py leg3 legs/leg3-DATE

   Expect the last lines:

       leg3 auto-score (ground truth = all ME): NN/NN = XX.X% cross-mic transfer

3. Write the summary and commit:

       ./spike/stt_bench/venv/bin/python scripts/score_leg.py legs/leg3-DATE/sheet.md -o docs/leg-3-score.md
       git add legs/leg3-DATE/sheet.md docs/leg-3-score.md STATUS.md
       git commit -m "p0 leg3: cross-mic transfer XX.X% (informational)"

   (STATUS line: `- DATE · **leg 3 RUN** — cross-mic voiceprint transfer XX.X% (no bar, informational)`)
