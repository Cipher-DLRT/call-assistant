# P1 hint-loop runbook — silent shadow (clicks-first, P1.5)

Daily use is CLICKS ONLY via the menu bar app (operator ruling 2026-08-11:
no terminal in daily use). Terminal commands live in the appendix as fallback.

Scope: INTERNAL calls only (1-2-1s, SC enablement). External-call use does NOT
begin in P1. Every hint gets graded; the first shadow calls ARE legs 1 and 2
for the attribution bars (channel-split ≥ 98% online, voiceprint ≥ 90%
in-person). **A2 resolved: pack 223 = post-dedup active canon (operator
cleanup mini-sitting) — pack trusted, shadow calls unblocked after the smoke.**

## One-time setup

### 1. API key + ceiling (law 9 — the key never transits chat)

One command at a time:

```
mkdir -p ~/.config/call-assistant
```

```
touch ~/.config/call-assistant/env
```

```
chmod 600 ~/.config/call-assistant/env
```

```
open -e ~/.config/call-assistant/env
```

Put two lines in the file (paste your key from the Anthropic console):

```
ANTHROPIC_API_KEY=sk-ant-...
CA_COST_CEILING_USD=0.50
```

Expect: `ls -la ~/.config/call-assistant/env` shows `-rw-------`.
The ceiling is the law-5 hard cap per call. It is never silently raised —
changing it is an edit to this file, on purpose, by you.

### 2. Verify the model IDs live (A3)

```
set -a; . ~/.config/call-assistant/env; set +a; ./spike/stt_bench/venv/bin/python scripts/verify_models.py
```

Expect:
```
gate model claude-haiku-4-5 ... OK (claude-haiku-4-5)
hint model claude-sonnet-5 ... OK (claude-sonnet-5)
A3 verified: both model IDs resolve on the live models list
```
STOP if either line errors — do not run a call on unverified model IDs.

### 3. Start the menu bar app

```
cd ~/dev/call-assistant && nohup ./spike/stt_bench/venv/bin/python -m app.menubar.menubar >/dev/null 2>&1 &
```

Expect: a `○ CA` item appears in the menu bar.

**Notch gotcha (hit live 2026-08-11):** on a crowded menu bar, macOS places the
new item in the leftmost free slot — which can be UNDER THE NOTCH, where it is
invisible (verified via Accessibility: item existed at x≈706, the notch zone).
Fix (applied, persists): pin the item's slot right of the notch via its
preferred position (distance in points from the RIGHT screen edge), then
restart the launcher:

```
defaults write org.python.python "NSStatusItem Preferred Position Item-0" -float 300
```

```
launchctl kickstart -k gui/$(id -u)/com.rami.call-assistant.menubar
```

(Ice was uninstalled from this Mac on 2026-08-11 — two conflicting installs;
menu-bar overflow is now unmanaged, so if the bar gets more crowded, lower the
number to move `○ CA` further right, or raise it to move left.)

Optional login item (default OFF — the plist is a repo file, not a paste).
Run only if you want it at login, one command at a time:

```
cp ~/dev/call-assistant/scripts/menubar-launchagent.plist ~/Library/LaunchAgents/com.rami.call-assistant.menubar.plist
```

```
launchctl load ~/Library/LaunchAgents/com.rami.call-assistant.menubar.plist
```

### 4. First-run permission prompts (per-binary TCC)

The FIRST time you start a shadow call, macOS will prompt once per binary:

- "python would like to access the microphone" → **Allow** (voiceprint + mic capture)
- "capture would like to record this computer's screen and audio" → **Allow**
  (this is the ScreenCaptureKit system-audio tap; the 64×64 video is discarded)

Expect: prompts appear once, never again. If capture starts but the overlay
never shows a level line in Terminal fallback mode, check System Settings →
Privacy & Security → Microphone / Screen Recording.

## Daily use (clicks)

1. Menu bar → `○ CA` → **Start Shadow (online)** or **Start Shadow (in-person)**.
   - **Online: headset REQUIRED (A4).** Speakers bleed into the mic at
     gradable levels (smoke evidence) and would corrupt the leg-1 bar.
   - In-person: built-in MacBook mic is the primary rig (law 8); the Lark is
     an enhancement when worn, and is auto-preferred when its receiver is in.
2. The overlay appears top-right. 🔒 on a hint = drawn from internal canon —
   do NOT speak client-named material (law 6). ⏳ = fact verified >90 days ago.
3. Menu bar → **Stop** when the call ends. This is the clean SIGINT path:
   the artifact and both grading sheets are finalized (same guarantee as
   Ctrl-C — verified in the build session).
4. Menu bar → **Open Last Call** → grade:
   - `hint-sheet.md`: mark useful / on-time / wrong per hint (any combination).
   - `attribution-sheet.md`: mark correct / wrong per row, then (terminal,
     or ask the assistant): `./spike/stt_bench/venv/bin/python scripts/score_leg.py calls/<id>/attribution-sheet.md`
5. If the overlay shows "cost ceiling reached — hints stopped": the call keeps
   transcribing locally, hints stop. That is the law-5 stop working as designed.

The status line in the menu shows `◉ recording · N hints` live and
`○ stopped · N hints · $cost` after finalize.

Crash behavior (verified pattern): the menu bar app dying does NOT stop a
running call (it runs in its own session — restart the menu app and Stop
still isn't needed: use `pkill -INT -f app.loop.orchestrator` in the appendix
if you ever lose the menu). The loop dying flips the menu to `○ stopped`.

## Smoke (fake audio — run before the first real shadow call)

```
scripts/smoke_fake_call.sh
```

Expect: two replay calls run end-to-end (~40 s each). Online: ≥1 hint appears
in the overlay; a hint carries 🔒 whenever any cited fact is internal (lock
rendering itself was verified in-session against a canned feed); attribution
sheet has ME and THEM rows with sims logged on ME. In-person: voiceprint
labels, ME sims ≥ 0.55, THEM (TTS voice) low. Cost line prints per call,
well under the ceiling.

Ceiling stop check:

```
scripts/smoke_fake_call.sh ceiling
```

Expect: overlay shows the ceiling notice mid-call; artifact still written.

## Appendix: terminal fallback

```
scripts/run_call.sh online                 # headset REQUIRED
scripts/run_call.sh inperson
scripts/run_call.sh replay-online legs/smoke-p1/me.wav legs/smoke-p1/them.wav
scripts/run_call.sh replay-inperson legs/smoke-p1/mix.wav
```

Ctrl-C stops cleanly. Artifacts land in `calls/<timestamp>/` (gitignored —
they carry call speech; only telemetry summaries and graded sheets commit).
