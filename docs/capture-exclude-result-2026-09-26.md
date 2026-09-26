# capture stream-online --exclude-pid: result (2026-09-26)

Lane ca-capture-apps, issue Cipher-DLRT/call-assistant#2, brief Amendment 1 (docs/lane-briefs/ca-capture-apps.md).
Rig: MacBook Air (M5), macOS 26.5.1, default output MacBook Air Speakers, BlackHole 2ch; test tones only, no call audio
recorded or kept. Measurement: stream 1 at 1 kHz, 0.5 s windows, Goertzel, sine-peak dBFS (`scripts/check_capture_exclude.py`).

## Flag

    capture stream-online --exclude-pid <pid>[,<pid>…]

Stream 1 then comes from a Core Audio process tap: `CATapDescription(stereoGlobalTapButExcludeProcesses:)`, a private
aggregate device, 48 kHz stereo float resampled to the same 16 kHz mono s16 frames. Stream 0 (mic) and the framing
are unchanged. Without the flag, the ScreenCaptureKit path runs as before.

## Why not the app list (`--apps`, the original design)

Leg 2 of the first design stopped as intended. With `SCContentFilter(display:including:)` set to Chrome for Testing,
its WebAudio tone read -200 dB (digital silence). Without the filter it read -50.0 dB. Chrome plays audio from a helper
process that ScreenCaptureKit does not list as an application. The windowless Python mixer is not listed either, so
excluding it by app also fails. Record: the lane's ASK-ADVISOR of 2026-09-26. The ruling was "go with your
recommendation".

## Legs

Leg 1 (a minimal tap in the scratchpad, before the flag was built; the excluded process is a Python tone into BlackHole 2ch):

    LEG 1 PASS: excluded mixer pid; (a) BlackHole -20 dBFS -> stream 1 max -200.0 dB (pass <= -60); (b) Chrome for Testing -50 dBFS -> median -50.0 dB; (c) afplay -50 dBFS -> median -50.1 dB (pass: within 6 dB)

No TCC prompt appeared, and the TCC log shows no event. The tap carried real audio, not an all-zero stream.

Leg 2, build: `swiftc -O app/capture/main.swift -o app/bin/capture` gave exit 0 with no warnings.

Legs 3–5 through the real binary (`scripts/check_capture_exclude.py`, final run):

    LEG 3 PASS: --exclude-pid <mixer pid>; (a) BlackHole -20 dBFS -> stream 1 max -200.0 dB (pass <= -60); (b) Chrome for Testing -50 dBFS -> median -50.0 dB; (c) afplay -50 dBFS -> median -50.1 dB (pass: within 6 dB); control, mixer not excluded: (a) median -20.0 dB (pass: within 6 dB)
    LEG 4 FAIL: no flag (today's SCK path); (a) BlackHole -20 dBFS -> stream 1 median -200.0 dB; (b) Chrome for Testing -50 dBFS -> median -50.0 dB; (c) afplay -50 dBFS -> median -50.0 dB (pass: all within 6 dB)
    LEG 5 PASS: late PID (mixer opened BlackHole after capture started); first window <= -60 dB at +2.0 s after its first audio; max from +5 s on -200.0 dB over 10 windows (pass: <= -60 from +5 s)

**Leg 4 is not a regression.** A baseline binary built from the unchanged `git show HEAD:app/capture/main.swift` gives
the same numbers:

    BASELINE (HEAD main.swift) LEG 4 FAIL: no flag (today's SCK path); (a) BlackHole -20 dBFS -> stream 1 median -200.0 dB; (b) Chrome for Testing -50 dBFS -> median -50.0 dB; (c) afplay -50 dBFS -> median -50.1 dB (pass: all within 6 dB)

The no-flag behaviour is therefore unchanged. The failing part is the expectation for (a). The brief expected about
-20 dB, taken from demo-agent's measurement. That does not reproduce here, with the test mixer either output-only or
duplex (default mic in, BlackHole out, the shape of `app/voice/mixer.py`). ScreenCaptureKit did not capture a
windowless process that writes only into BlackHole. afplay's tone, which goes to the default output, is captured.
Unverified hypothesis: ScreenCaptureKit takes a GUI-app or default-output mix, and demo-agent's measured process
differed in one of those ways. The advisor rules on leg 4.

Suite: `13 passed` before and after (the baseline command in the brief's PREREQUISITES).

## Findings made while building (these shape the code)

1. **Mic first, then tap.** Starting the mic `AVAudioEngine` after the tap's aggregate device is running deadlocks
   inside the HAL (`HALB_Guard::WaitFor` in `AudioOutputUnitStart`, sampled). On the `--exclude-pid` path the mic
   starts first. The SCK path keeps its original order.
2. **Tap auto-start off.** With `kAudioAggregateDeviceTapAutoStartKey: true`, the IOProc was never called while no
   non-excluded process did audio I/O, so stream 1 carried no frames at all (3 of 3 bare runs: 0 bytes). With it off,
   and with the default output device as the aggregate's main sub-device, frames flow continuously in silence, as they
   do from ScreenCaptureKit (3 of 3 runs: about 94 chunks/s from t+1 s).
3. **Late PID.** A PID gets a Core Audio process object only once it initialises audio. PortAudio's import alone is
   enough, so the test mixer imports sounddevice after its delay. The list is re-resolved every 2 s on the meter
   timer. When the set of objects changes, the tap's `kAudioTapPropertyDescription` is updated in place. There is no
   restart, and stream 1 continues. Measured: excluded 2.0 s after the process's first audio.
