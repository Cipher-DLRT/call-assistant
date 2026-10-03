# capture stream-online --include-pid: result (2026-10-03)

Lane ca-capture-include, issue Cipher-DLRT/call-assistant#4, brief `docs/lane-briefs/ca-capture-include.md`.
Rig: MacBook Pro (M5 Max), macOS 26.7 (25G229), default output MacBook Pro Speakers, BlackHole 2ch; test tones only, no
call audio recorded or kept. Measurement: stream 1, 0.5 s windows, one FFT per window, sine-peak dBFS at each source's
bin (2 Hz resolution at 16 kHz; every source frequency is an exact bin) — `scripts/check_capture_include_selftest.py`.

## Flag

    capture stream-online --include-pid <pid>[,<pid>…]

Stream 1 then comes from a Core Audio process tap, `CATapDescription(stereoMixdownOfProcesses:)`, of every audio
process object (`kAudioHardwarePropertyProcessObjectList`, `kAudioProcessPropertyPID`) whose PID is a listed PID or a
descendant of one (parent chain via `sysctl` `KERN_PROC_PID`). It is read through the same private aggregate device as
`--exclude-pid` (tap auto-start off, default output as the clock), so frames flow in silence, and it is resampled to the
same 16 kHz mono s16 frames. Stream 0 (mic) is untouched; the mic starts first, as on the exclude path.

- Membership is re-resolved every 1 s on the meter timer. On a change, one stderr line:
  `THEM include: <n> process(es) [<pid>,…] under [<listed pids>]`.
- A listed PID that is not running at start: one stderr line,
  `THEM include: pid [<pid>] not running; stream 1 is silent until it appears`; capture runs on in silence.
- `--include-pid` with `--exclude-pid`: usage, exit 2. No flag: the ScreenCaptureKit path, code unchanged.
  `--exclude-pid`: unchanged (no mechanism fix was needed, leg 6).

## Sources (all at once, each on its own frequency)

| | source | played |
|---|---|---|
| A | Chrome for Testing (headed, `file://` page, WebAudio); its browser pid is the listed pid | 1 kHz, -50 dBFS |
| B | a second Chrome for Testing instance (own user-data-dir) | 1.5 kHz, -50 dBFS |
| C | `afplay` to the default output | 2 kHz, -50 dBFS |
| M | a separate Python process (sounddevice) into BlackHole 2ch | 700 Hz, -20 dBFS |

## Legs (verbatim)

Leg 1, RED at the base `9d6bbc0`: `app/bin/capture stream-online --include-pid 1` printed the usage and exited 1.
Control: the base binary with `--exclude-pid <pid>` streamed (`THEM exclude: excluding pid [] no audio yet [8825]`,
`streaming`, `t+00:05 ME -38.9 dBFS | THEM -180.0 dBFS`, clean stop, exit 0).

Leg 2, the STOP-shaped proof, before any change to `main.swift`: a minimal include tap in the scratchpad (one-shot
tree resolve, same tap/aggregate/framing), sources playing before capture starts:

    LEG 2 PASS: minimal include tap (probe) --include-pid <A browser pid>, sources playing before capture starts; A Chrome for Testing -50 dBFS -> stream 1 median -50.0 dB (pass: within 6 dB); B second Chrome for Testing -50 -> max -162.4 dB; C afplay -50 -> max -159.3 dB; M BlackHole -20 -> max -154.0 dB (pass: each >= 40 dB below played); 8 windows
      capture: THEM probe include: 1 process(es) [37516] under [37350] / THEM: probe include tap — 2 ch @ 48000 Hz → stream 1

The tree is the point: the browser pid 37350 had no audio process object; its child 37516 (Chrome's audio service)
did, and only it was tapped. The same probe with an empty process list created the tap and streamed silent frames
(106 KB in 4 s), which item 5 (not-running PID) relies on.

Leg 3, build: `swiftc -O app/capture/main.swift -o app/bin/capture`, exit 0, no warnings.

Legs 2 (re-run on the built binary), 4, 5 and 6 — final run, `scripts/check_capture_include_selftest.py`, exit 0:

    LEG 2 PASS: minimal include tap (capture) --include-pid <A browser pid>, sources playing before capture starts; A Chrome for Testing -50 dBFS -> stream 1 median -50.0 dB (pass: within 6 dB); B second Chrome for Testing -50 -> max -155.1 dB; C afplay -50 -> max -162.4 dB; M BlackHole -20 -> max -150.6 dB (pass: each >= 40 dB below played); 8 windows
      capture: THEM include: 1 process(es) [57953] under [57844] / THEM: system audio (Core Audio process tap) — 2 ch @ 48000 Hz → stream 1
    LEG 4a PASS: late audio; capture started before A played (audio helper at start: none); A on stream 1 within 6 dB at +1.5 s after first playback (pass: <= 5 s, no restart)
    LEG 4b PASS: churn; A's audio helper 60748 killed, respawned as 61436; A back within 6 dB at +1.5 s after the tone restarted (pass: <= 5 s, no restart)
      capture: THEM include: 0 process(es) [] under [60373] / THEM: system audio (Core Audio process tap) — 2 ch @ 48000 Hz → stream 1 / THEM include: 1 process(es) [60748] under [60373] / THEM include: 0 process(es) [] under [60373] / THEM include: 1 process(es) [61436] under [60373]
    LEG 4c PASS: --include-pid 99999 (not running) while A, B, C, M play; 8 windows in 4 s, stream 1 max RMS -200.0 dB (pass: frames flow, <= -90); 'not running' stderr lines: 1 (pass: 1)
      capture: THEM include: 0 process(es) [] under [99999] / THEM include: pid [99999] not running; stream 1 is silent until it appears / THEM: system audio (Core Audio process tap) — 2 ch @ 48000 Hz → stream 1
    LEG 5 PASS: real topology, built binary, --include-pid <A browser pid>, capture started before the sources; A Chrome for Testing -50 dBFS -> stream 1 median -50.0 dB (pass: within 6 dB); B second Chrome for Testing -50 -> max -153.3 dB; C afplay -50 -> max -159.3 dB; M BlackHole -20 -> max -149.1 dB (pass: each >= 40 dB below played); 8 windows
      capture: THEM include: 0 process(es) [] under [63159] / THEM: system audio (Core Audio process tap) — 2 ch @ 48000 Hz → stream 1 / THEM include: 1 process(es) [63444] under [63159]
    LEG 6a PASS: no flag (today's SCK path), capture started first; A -50.0 dB, B -50.0 dB, C -50.1 dB (pass: within 6 dB of -50); M BlackHole -20 -> median -148.7 dB (recorded: SCK does not capture the windowless writer on this rig, 2026-09-26)
    LEG 6b PASS: --exclude-pid <M pid>; M BlackHole -20 -> max -150.0 dB (pass <= -60); A -50.0 dB, B -50.0 dB, C -50.0 dB (pass: A and C within 6 dB)
      capture: THEM exclude: excluding pid [64564] no audio yet [] / THEM: system audio (Core Audio process tap) — 2 ch @ 48000 Hz → stream 1
    LEG 6c PASS: exclude late-open (M opened BlackHole after capture started); max in its first 5 s -29.9 dB; max from +5 s on -200.0 dB over 10 windows (pass: <= -60 from +5 s)
      capture: THEM exclude: excluding pid [] no audio yet [65179] / THEM: system audio (Core Audio process tap) — 2 ch @ 48000 Hz → stream 1 / THEM exclude: excluding pid [65179] no audio yet []

Absent sources read -148 to -162 dB, not -200, because A's -50 dB tone is in the same s16 frames: that is the
quantization floor at the other bins, not leakage. With nothing tapped (leg 4c) stream 1 reads -200 dB.
Leg 4c's capture prints two start lines for a not-running pid: the fixed-format set line (`0 process(es)`) and the one
`not running` line the brief's item 5 asks for.

No macOS permission prompt appeared. The TCC log (`log show --predicate 'subsystem == "com.apple.TCC"' --last 40m`)
has no audio or capture event for the lane's runs.

Leg 7, suite: `13 passed` before and after (`spike/stt_bench/venv/bin/python -m pytest -q -p no:cacheprovider`).

## Update mechanism: in place (measured)

The in-place update of `kAudioTapPropertyDescription` (`desc.processes = objs`, then `AudioObjectSetPropertyData` on
the tap, as the exclude path does) takes effect for an include tap. Leg 4a: the tap was created with zero processes,
A's audio helper appeared when A first played, the set was updated in place, and A was on stream 1 within 6 dB 1.5 s
after first playback. Leg 4b: the helper was killed (`0 process(es)`), Chrome respawned it under a new pid on the next
tone, and the new pid joined in place 1.5 s after the restart. No restart of capture, no rebuild of the tap or aggregate
device. So the rebuild fallback was not built.

The exclude late-open case (leg 6c, M opens BlackHole about 4 s after capture starts) also passes with the in-place
update: -200 dB from +5 s on. But M is on stream 1 at up to -29.9 dB in its first seconds, until the next 2 s
re-resolve. That is the most likely reading of owner-ai-se-3's 2026-09-28 observation: a short leak bounded by the
poll interval, not a failed update. `--exclude-pid` keeps its 2 s poll (unchanged per the brief). The include path polls
every 1 s; its symmetric cost is that a newly started helper's first ≤ 1 s is missing from stream 1.

## Recorded, not changed

- **No-flag (SCK) path and start order.** With capture started first, A, B and C read -50.0/-50.0/-50.1 (leg 6a).
  With the sources started 2 s before capture, SCK misses `afplay` (C -120.4 dB on the base binary, -122.0 on this
  lane; A and B -50.0 on both). The base binary built from `9d6bbc0` gives the same numbers in both orders, so this is
  today's SCK behaviour, not a regression. M (the windowless BlackHole writer) is not captured by SCK on this rig
  (-148.7 dB), as recorded 2026-09-26.
- **The no-flag path's code is unchanged.** The SCK branch runs only when neither flag is given; its body is
  untouched. The usage text gains the `--include-pid` alternative.

## What this does NOT remove

Sounds the meeting itself plays — Meet's join chimes, its hold music — are rendered by the host Chrome's audio helper,
inside the listed process tree, and stay on stream 1. Filtering those is the consumer's job (demo-agent#64). Any other
tab or extension in that same host Chrome is also in the tree.

## Use

The consumer (demo-agent#64) passes the host Chrome's browser pid (CDP 9223). That is a demo-agent change, not this
lane's.
