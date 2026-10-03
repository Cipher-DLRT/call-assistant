# build-brief ca-capture-include — capture stream-online records only the meeting's process tree (2026-10-03)
FEATURE: The AI SE hears only the meeting. With `capture stream-online --include-pid <host Chrome pid>`, stream 1 carries
the audio of that Chrome and its helper processes, and nothing else the Mac plays: no Spotify, no notification sounds,
no other Chrome. The check `scripts/check_capture_include.py` shows it, one PASS line per leg.

STATUS: CLOSED 2026-10-03 PASS e3dcc20ac3e0b5ecc81278bf54d2fa3b57307986

**Category:** fix — needed by Cipher-DLRT/demo-agent#64 (voice turns; the 2026-10-03 re-sitting, demo-agent#81).
BRANCH: Cipher-DLRT/ca-capture-include
ISSUE: #4
DESIGN: Cipher-DLRT/call-assistant#4 (the issue body is the spec). Topology from the re-sitting: Meet runs in the agent's
host Chrome (CDP 9223), a third instance of the same `Google Chrome` app beside the demo Chrome (9222) and Rami's own.
Chrome plays audio from a helper process, a child of the browser pid, not from the browser pid itself (measured
2026-09-26, `docs/lane-briefs/ca-capture-apps.md` Amendment 1). So the filter is by process tree, not by bundle ID.
The `--exclude-pid` tap is `app/capture/main.swift:293-410`; its re-resolve runs every 2 s (`:441`).
BRIEF-REVIEW: not required — HOSTS name none of the fenced systems; local tooling, no data leaves the Mac.

BOUNDARY: No writes outside this worktree.
Commit only here with explicit paths. **PUSH YOUR OWN LANE BRANCH, never main**, and name the pushed sha in DONE.
Never write in `/Users/rami/dev/call-assistant` (the live checkout; its binary is deployed by the owner after landing).
Build the binary here only (`app/bin/capture` in this worktree, gitignored). Never attach to, open, or kill anything in
the demo Chrome (9222), the host Chrome (9223) or Rami's own Google Chrome. The only browsers you start are Playwright's
"Google Chrome for Testing".

HOSTS: `github.com` — write: push of the lane branch. Local only: the Core Audio process tap, the default mic,
BlackHole 2ch (test tones written into it), the default output (tones at -50 dBFS or lower only), Playwright's Chrome
for Testing on a local `file://` page.
An unlisted read or connection is an incident: stop, record the read and copy location, and ASK.
Secrets: none appear in chat, reports, git or terminals; report key names, byte lengths or sha256 prefixes.
Customer content stays on the box: report ids, counts and file names.

REASON: fix — `capture stream-online` hands the AI SE every sound the Mac plays as the far side, so music and
notifications start its acknowledgements and barge-ins (demo-agent#81 F4, #64 residual).
TIER: opus-medium (Opus 5.5). TIER-REASON: a bounded Core Audio change in one Swift file plus a measured check; the
same tier built the `--exclude-pid` tap in one pass; demo-agent `docs/rulings.md` rule 10 allows Opus 5.5 or codex
gpt-6.1-sol only.
Gate: NOT REQUIRED — §F all not-engaged, one revert restores with no data loss.
External review: NOT required — class: local tooling. The demo-agent advisor reads the result before it lands.

PREREQUISITES:
- Python for the check: `spike/stt_bench/venv` in this worktree, provisioned by owner-ai-se-2 (numpy, sounddevice,
  playwright, pytest). Check: `spike/stt_bench/venv/bin/python -c "import numpy, sounddevice, playwright"`. Chrome for
  Testing is in `~/Library/Caches/ms-playwright`. **Do NOT pip install or `playwright install`.** Missing → STOP.
- `swiftc` at `/usr/bin/swiftc`. Display on and screen unlocked; run live legs under `caffeinate -d -i`. Locked → STOP.
- Baseline suite: `spike/stt_bench/venv/bin/python -m pytest -q -p no:cacheprovider`. Paste its line before you change
  anything.

§F CLASSIFICATION: grants/roles/credentials — not-engaged; containment/egress — not-engaged; external writes —
not-engaged; column drop/alter — not-engaged; customer data off-box — not-engaged (test tones only; no call audio is
recorded or kept).

## The rules

- `CLAUDE.md` law 1 (audio never leaves the Mac) and law 10 (STATUS.md in the same commit as any state change; explicit
  staging, never `git add -A`).
- **A macOS permission prompt is a STOP.** If macOS asks for System Audio Recording or anything else, or the tap reads
  all-zero, signal STOP with the exact prompt or symptom. No seat clicks a permission dialog; the owner gets Rami.
- Keep the chosen tier on its TIER line; only a STATUS writeback may repeat it.

## The change

1. `capture stream-online --include-pid <pid>[,<pid>…]`: stream 1 comes from a Core Audio process tap of **only** the
   listed processes **and all their descendant processes** (e.g. `CATapDescription(stereoMixdownOfProcesses:)`), read
   through a private aggregate device as the exclude path does. Same framing, 16 kHz mono resampling and stderr status
   lines. Stream 0 (mic) is untouched.
2. Membership: enumerate `kAudioHardwarePropertyProcessObjectList`, read each object's PID, and include it when that PID
   is a listed PID or a descendant of one (parent chain via `sysctl` `KERN_PROC_PID`). Re-resolve on the meter timer
   (every 2 s or faster), so a helper that starts audio after capture starts, or a helper Chrome restarts, joins
   without restarting capture. One stderr line when the set changes:
   `THEM include: <n> process(es) [<pid>,…] under [<listed pids>]`.
3. **The in-place update must be measured, not assumed.** demo-agent saw a process that opened audio 4 s after
   capture start reach stream 1 despite `--exclude-pid` (owner-ai-se-3, 2026-09-28). The existing path updates
   `kAudioTapPropertyDescription` in place (`main.swift:326-339`). Leg 4 tests it for include. If the in-place update
   does not take effect, rebuild the tap and aggregate device on a change, keeping stream 1's framing continuous (a gap
   of up to 200 ms of silence is acceptable). Record which mechanism works and why in HANDOFF and the result doc.
4. `--include-pid` and `--exclude-pid` are mutually exclusive: both given → usage error, exit 2. No flag → today's SCK
   path, byte for byte. `--exclude-pid` → unchanged, except that if leg 4 shows the in-place update fails, the same
   mechanism fix applies to it. Pin it in leg 6.
5. A listed PID that is not running at start: one stderr line, keep capturing silence, pick it up when it appears.
6. Update the header comment's mode list.

## Legs

1. RED: at the base, `capture stream-online --include-pid 1` prints usage and exits non-zero. Paste it. Control: the
   base binary with `--exclude-pid <pid>` streams.
2. **STOP-shaped first: a minimal include tap proves the tree.** Chrome for Testing **A** (headed, local `file://` page,
   WebAudio 1 kHz at -50 dBFS) is the listed pid. At the same time: Chrome for Testing **B** (a second instance with
   its own `--user-data-dir`) plays 1.5 kHz at -50 dBFS, `afplay` plays 2 kHz at -50 dBFS to the default output, and a
   Python process writes 700 Hz at -20 dBFS into BlackHole 2ch. Measure stream 1 per frequency
   (Goertzel or FFT bin, 0.5 s windows). PASS: A within 6 dB of played; B, afplay and the Python tone each at least
   40 dB below played. A FAIL is a STOP: write ASK-ADVISOR with the numbers and signal ASK.
3. Implement in `app/capture/main.swift`; build `swiftc -O app/capture/main.swift -o app/bin/capture`. Commits
   `ca-capture-include:`.
4. **Late and churn, through the real binary:**
   (a) start capture with `--include-pid <A's browser pid>` before A plays anything, then start the tone. PASS: A's tone
   on stream 1 within 5 s of first playback, without a restart.
   (b) find A's audio helper pid (the descendant whose process object appeared), kill it (Chrome for Testing respawns
   its audio service), restart the tone. PASS: back within 5 s, without a restart.
   (c) `--include-pid` of a pid that is not running: capture runs, stream 1 is silence, one stderr line.
5. **The real topology, offline:** leg 2's four sources, all through `--include-pid <A>` on the built binary. Same PASS.
6. **Unchanged paths:** no flag → all four sources on stream 1 (today's SCK behaviour; record the numbers). With
   `--exclude-pid <python pid>` → the Python tone at least 40 dB below played, A and afplay present. Also the
   exclude late-open case: the Python process opens BlackHole about 4 s after capture starts. Record PASS or FAIL; a
   FAIL here is fixed by item 3's mechanism, or reported as an ASK if it cannot be.
7. Green: the baseline suite line again, same count.

Keep the check in `scripts/check_capture_include.py`, which prints one PASS/FAIL line per leg 2 and 4–6. Record the
numbers in `docs/capture-include-result-2026-10-03.md`, with a STATUS.md log line in the same commit (law 10).

USE: #4 — the consumer passes the host Chrome's browser pid. That is a demo-agent change, not this lane's.

## Pins / Verdict line / PASS rule

- Legs 1, 2 and 4–7 PASS lines verbatim in HANDOFF and the result doc.
- `git diff --stat` touches only `app/capture/main.swift`, `scripts/check_capture_include.py`,
  `docs/capture-include-result-2026-10-03.md` and `STATUS.md`.
- What this does NOT remove, recorded in the result doc: sounds the meeting itself plays (Meet's join chimes, its
  hold music) are in the host Chrome's audio and stay on stream 1. Filtering those is the consumer's job (demo-agent#64).

## Deliverables

0. `git ls-files scripts/check_capture_include.py docs/capture-include-result-2026-10-03.md` is empty at the base sha.
1. Commits `ca-capture-include:` with explicit paths; HANDOFF.md in the worktree root carries the diff summary,
   before/after suite exit lines, legs verbatim, the update mechanism chosen, and `Removed behaviour` (none expected).
   HANDOFF.md carries a `TEST:` block with indented `COMMAND: spike/stt_bench/venv/bin/python scripts/check_capture_include.py`,
   `RED: exit <non-zero>` (leg 1, before the change), and `GREEN: exit 0`.
   COST line: `COST ca-capture-include: model=<id> effort=medium wall=<h:mm> rounds=0 spend≈n/a (subscription) saves≈n/a`.
   Never commit HANDOFF.md, BRIEF.md, flag files, WAVs or the built binary.
2. `touch <worktree>/HANDOFF-READY`, then signal the launching seat. First act, BOOT; last act, DONE:

   ```
   orca terminal send --terminal term_ced6e64f-85e0-42d6-bb5f-03914233d2a2 --enter --text 'NEEDS LANE-SIGNAL ca-capture-include | BOOT | reading the brief'
   orca terminal send --terminal term_ced6e64f-85e0-42d6-bb5f-03914233d2a2 --enter --text 'NEEDS LANE-SIGNAL ca-capture-include | DONE | pushed <sha>'
   ```
3. For a question unanswered by source, write ASK-ADVISOR in the worktree root and signal ASK.
   Signal before every approval request, blocker, question or finish; never stop silently.
   Accepted signal verbs: DONE, ASK, STOP, BLOCKED. No `$<digit>` in signal text; write arg 1 or field 2.
4. Landing is the owner's: review, then an XREPO to land the branch on call-assistant main, then the owner deploys the
   binary into `/Users/rami/dev/call-assistant` (ff-only if clean, no `capture` running, built to a temp path and
   `mv`'d onto `app/bin/capture`, the menubar process untouched).
