# build-brief ca-capture-apps — capture stream-online records only the named meeting apps (opt-in --apps) (2026-09-26)

STATUS: CLOSED 2026-09-26 PASS 9b78437955a1ba0e084fe94ae6b80f22ddefd3a5
ISSUE: Cipher-DLRT/call-assistant#2

**Category:** fix — path towards Cipher-DLRT/demo-agent#24 (the AI SE's Teams and Meet check, milestone AI SE 2).
DESIGN: Cipher-DLRT/call-assistant#2 (the issue body is the spec); the measurements are in demo-agent's
`docs/evidence/voice-routing-offline-2026-09-26.md` on its origin/main.
BRIEF-REVIEW: not required — HOSTS name none of the fenced systems.

REASON: fix — the defect: `capture stream-online` records demo-agent's own mixer output as the far side, so the AI
SE's voice mode (speaking on Rami's meeting line) barges in on itself; it degrades demo-agent#24's barge-in check.

BOUNDARY (ESTATE §31): No writes outside this worktree. Commit only in this worktree; push your own lane branch, never
main. Never write in `/Users/rami/dev/call-assistant` or `/Users/rami/dev/demo-agent`. Build the binary here only
(`app/bin/capture` in this worktree, gitignored). Never attach to or open anything in the demo Chrome (CDP port 9222)
or in Rami's own Google Chrome; the only browser you start is Playwright's "Google Chrome for Testing".

HOSTS (ESTATE §34): `github.com` — write: push of your lane branch. Nothing else. Local only: ScreenCaptureKit system
audio, the default mic, BlackHole 2ch (writes a test tone into it), the default output (quiet tones at -50 dBFS or
lower only), Playwright's Chrome for Testing on a local `file://` page.

TIER: opus-medium — Rami's ruling 2026-09-26 via the demo-agent advisor: "codex is almost burned out, it resets in 3
hours, switch to opus 5.5 on med for a bit"; grok is at its weekly limit. A bounded Swift change plus a measured check.
Gate: NOT REQUIRED — §F all not-engaged, one git revert undoes it. External review: NOT required (class: local
tooling; no data leaves the Mac). The demo-agent advisor reads the result before it lands.
Secrets: none are read by this lane.

PREREQUISITES:
- Python for the checks: `spike/stt_bench/venv` in this worktree, provisioned by owner-ai-se-2 (numpy, sounddevice,
  playwright 1.62.0, pytest). Check: `spike/stt_bench/venv/bin/python -c "import numpy, sounddevice, playwright"`.
  Chromium for Testing is already in `~/Library/Caches/ms-playwright`. **Do NOT pip install or `playwright install`.**
  If something is missing, STOP and signal.
- `swiftc` at `/usr/bin/swiftc`. The display on and the screen unlocked: ScreenCaptureKit returns "no display found"
  otherwise. Run live checks under `caffeinate -d -i`, and if the screen is locked, STOP and signal. Never unlock it.
- The baseline suite: `/Users/rami/dev/call-assistant/spike/stt_bench/venv/bin/python -m pytest -q -p no:cacheprovider`
  run from this worktree gave `13 passed` (owner-ai-se-2, 2026-09-26). Reading that venv is allowed; writing there is not.

§F CLASSIFICATION: grants/roles/credentials not-engaged; containment/egress not-engaged; external writes not-engaged;
column drop/alter not-engaged; customer data off-box not-engaged (test tones only; no call audio is recorded or kept).

## Context (read first)
- `CLAUDE.md` (law 8 and law 10: STATUS.md changes in the same commit as any state change; explicit staging).
- Cipher-DLRT/call-assistant#2 (`gh issue view 2 -R Cipher-DLRT/call-assistant`).
- `app/capture/main.swift`: the header comment (modes), `startSystemCapture` (~l.250-275, the SCK filter at 257-266),
  and the `stream-online` case (~l.288-293).
- demo-agent's consumer, read only: `/Users/rami/orca/workspaces/demo-agent/owner-ai-se-2/app/voice/ears.py` l.150-160
  (it spawns `capture stream-online` and demuxes stream 1 as `them`).

## AMENDMENT 1, 2026-09-26: the design changes to a Core Audio process tap (supersedes "The change", "Legs" and "Pins" below)

**Why:** leg 2 STOPPED as designed (the lane's ASK-ADVISOR, 2026-09-26). ScreenCaptureKit's app filter drops Chrome's
helper-process audio: a Chrome for Testing tone reads -50.0 dB unfiltered and -200 dB with `--apps`. Our Python mixer
is not an SCK application either, so exclude-by-app fails too. **Rami, verbatim via the demo-agent advisor: "go with your
recommendation."** That is the lane's proposal: exclude the agent's own process from a global Core Audio process tap.

**The change:**
1. `capture stream-online --exclude-pid <pid>[,<pid>…]`: stream 1 comes from a Core Audio process tap (macOS 14.2+:
   `CATapDescription(stereoGlobalTapButExcludeProcesses:)`, `AudioHardwareCreateProcessTap`, a private aggregate device),
   with each PID translated through `kAudioHardwarePropertyTranslatePIDToProcessObject`. Same framing, same 16 kHz mono
   resampling, same stderr status lines. Stream 0 (mic) is untouched.
2. Without `--exclude-pid`: today's SCK path, byte for byte. Every other mode is untouched.
3. A listed PID with no audio process object yet (it has not opened audio): print one stderr line, run the tap
   without it, and re-resolve on a timer until it appears. Say in HANDOFF how.
4. The `--apps` code in the worktree is not landed. Remove it, and keep only what the tap path reuses.

**Legs:**
1. **STOP-shaped, before building the flag properly: a minimal tap proves both sides.** Run a tap that excludes one
   Python process which writes a 1 kHz tone at -20 dBFS into BlackHole 2ch (the shape of demo-agent's mixer). In the
   same run, (b) Chrome for Testing plays a WebAudio 1 kHz tone at -50 dBFS on a local `file://` page, and (c) `afplay`
   plays a -50 dBFS tone to the default output. PASS: (a) the excluded process's tone is at least 40 dB below its played
   level on the tap; (b) and (c) are within 6 dB of their played levels. A leg-1 FAIL is a STOP: write ASK-ADVISOR and
   signal ASK.
   **If macOS asks for a permission** (System Audio Recording / `NSAudioCaptureUsageDescription`, a TCC prompt or a
   silent all-zero tap): STOP and signal ASK with the exact prompt or symptom. **No seat clicks a permission dialog.**
   The advisor gets Rami.
2. Build `--exclude-pid` into `capture stream-online`: `swiftc -O app/capture/main.swift -o app/bin/capture` in this worktree.
3. **Through the real binary:** leg 1's (a), (b) and (c) again via `capture stream-online --exclude-pid <python pid>`,
   stream 1 measured at 1 kHz in 0.5 s windows.
4. **Unchanged without the flag:** the same three tones with no flag. All three appear on stream 1 (today's SCK
   behaviour; (a) at about -20 dB, measured 2026-09-26).
5. **Late PID:** start capture with `--exclude-pid <pid>` for a Python process that opens BlackHole about 5 s after
   capture starts. PASS: within 5 s of its first audio, its tone is at least 40 dB below played on stream 1, without a restart.
6. Suite: `13 passed` before and after (the baseline command in PREREQUISITES).

`scripts/check_capture_apps.py` becomes the check for legs 3–5, with one PASS/FAIL line per leg. Rename it to
`scripts/check_capture_exclude.py`. Record the numbers in `docs/capture-exclude-result-2026-09-26.md`, with a STATUS.md
log line in the same commit (law 10).

**Pins:** the PASS lines of legs 1 and 3–5, verbatim, in HANDOFF and the result doc. `git diff --stat` touches only
`app/capture/main.swift`, `scripts/check_capture_exclude.py`, `docs/capture-exclude-result-2026-09-26.md` and `STATUS.md`.
Consumer follow-up, not this lane: demo-agent's `app/voice/ears.py` passes `--exclude-pid <its own PID>`.

## The change (SUPERSEDED by Amendment 1)
1. `capture stream-online --apps <bundle-id>[,<bundle-id>…]`: stream 1 records system audio only from the running
   applications whose bundle IDs are listed (`SCContentFilter(display:including:exceptingWindows:)` or an equivalent
   you can justify). Stream 0 (mic), the framing, the 16 kHz resampling and the stderr status lines are unchanged.
2. Without `--apps`: identical behaviour to today (same filter, same output). Every other mode (`online`, `single`,
   `stream-inperson`) is untouched.
3. Apps not running at start, or started later (a meeting app opened after capture starts): print one stderr line
   naming what is and isn't found, keep capturing, and pick up a listed app that starts later without a restart (e.g.
   re-resolve on a timer and `updateContentFilter`). Say in HANDOFF which mechanism you chose and why.
4. Update the header comment's mode list with the flag.

## Legs
1. Build: `swiftc -O app/capture/main.swift -o app/bin/capture` in this worktree. Paste the build line result.
2. **Chrome helper audio first (issue done-when 2, the STOP).** Before polishing anything: with `--apps
   com.google.chrome.for.testing`, play a 1 kHz tone at about -50 dBFS from a local `file://` page in Playwright's
   Chrome for Testing (headed; WebAudio or `<audio>`). Measure stream 1 at 1 kHz (Goertzel or FFT bin; use windows of
   0.5 s). PASS: it reads within 6 dB of the played level. If it is absent (Chrome renders audio in a helper process
   and SCK does not attribute it to the app), **STOP**: write ASK-ADVISOR with the measurement and signal ASK. Build
   nothing further.
3. **Negative.** With `--apps com.microsoft.teams2,com.google.Chrome`: (a) a 1 kHz tone at -20 dBFS written into
   BlackHole 2ch from a separate Python process (sounddevice, BlackHole as the output device); (b) a -50 dBFS tone to
   the default output via `afplay`. PASS: stream 1 at 1 kHz is at least 40 dB below the played level for both.
4. **Unchanged without the flag.** The same (a) and (b) without `--apps`. Expect both to appear on stream 1 (that is
   today's behaviour: -20 dB and about -50 dB, measured 2026-09-26). This is the control that shows the tones reach SCK.
5. **Late start.** Start capture with `--apps com.google.chrome.for.testing` before Chrome for Testing is running,
   then start it and play the tone. PASS: the tone appears on stream 1 within 5 s of playback, without restarting capture.
6. Suite: the baseline command above, `13 passed` before and after.

Keep the check in a committed script, `scripts/check_capture_apps.py`, which prints one PASS/FAIL line per leg 2–5.
Record the numbers in `docs/capture-apps-result-2026-09-26.md`, and add a STATUS.md log line in the same commit (law 10).

## Pins
- Legs 2–5 PASS lines pasted verbatim in HANDOFF and in the result doc.
- `git diff --stat` touches only `app/capture/main.swift`, `scripts/check_capture_apps.py`,
  `docs/capture-apps-result-2026-09-26.md`, `STATUS.md`.

## Deliverables
1. Commits `ca-capture-apps:` with explicit paths (never `git add -A`); push the lane branch early. HANDOFF.md in the
   worktree root: the diff summary, suite lines before and after, legs 2–5 verbatim, the late-start mechanism,
   `Removed behaviour` (none expected) and `COST ca-capture-apps: model=<id> effort=medium wall=<h:mm> rounds=0
   spend≈<usd or n/a>`. Never commit HANDOFF.md, WAVs or the built binary.
2. `touch <worktree>/HANDOFF-READY`, then signal the launching seat:
   `orca terminal send --terminal term_9b44935c-caba-4447-95f1-663b3d60f875 --enter --text 'LANE-SIGNAL ca-capture-apps | DONE | pushed <sha>'`.
   First act: `LANE-SIGNAL ca-capture-apps | BOOT | reading the brief` to the same terminal.
3. A question the brief doesn't answer, or the leg-2 STOP: write ASK-ADVISOR in the worktree root and signal `ASK` to
   the same terminal, with the measurement and your proposal. Never stop silently.
