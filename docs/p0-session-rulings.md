# P0 session rulings (2026-07-31)

Recorded verbatim from the operator at P0 kickoff. CLAUDE.md is the law; these
rulings sit on top of it for this phase.

1. First create the repo skeleton (/spike /prompts /scripts /docs) and STATUS.md
   per conventions. Commit with explicit paths only.
2. Then work the verify-before-build list ONE ITEM AT A TIME, in this order:
   a. Granola coexistence — can ScreenCaptureKit tap system audio while Granola
      records simultaneously? Design the check so the operator can run it with a
      video playing as the fake meeting.
   b. Lark M2 receiver — plugged in now. Verify what it presents: sample rate,
      and CRITICALLY whether TX1 and TX2 arrive as separate left/right channels.
      If they do, flag it loudly — it changes the in-person attribution design
      (second transmitter = deterministic per-person channels, voiceprint
      demoted to backup).
   c. STT speed — faster-whisper vs whisper.cpp streaming on this M5, measured,
      p50 partial latency reported. Mic ruling: this measurement may use ANY
      audio input; it does not need the Lark.
3. Operator profile applies strictly: one command at a time, every command
   preceded by what to expect, full stop on any mismatch. Operator is not a
   developer — each step explained in one plain sentence before the command.
4. Every check closes with a written result in docs/ and a STATUS.md line in
   the same commit.
5. Voiceprint enrollment happens AFTER the three checks, on the Lark.
6. STOP after enrollment. The two live meeting legs are scheduled separately —
   no hint logic, no EQ14, no new network surface.
