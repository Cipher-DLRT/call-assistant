# call-assistant — CLAUDE.md (seed v1, 2026-07-31)

Live sales-call copilot for Rami (Solution Consultant, UnifyApps). Listens to calls
LOCALLY on the Mac, shows short answers + sales cues in an overlay while the call
runs. First reader of PKMS canon. Born in the call-assistant chat; resumed on
GATE-CA-P1 green (docs/gate-ca-p1-green.md in work-automation, 2026-07-31).

**Division of labor (house pattern): the call-assistant chat is the drawing board and
review layer; Claude Code builds from this file; the operator executes runbooks.**
Repo: private under Cipher-DLRT. Mac-resident through P1 — nothing here runs on EQ14.

## Prime laws

1. **Audio never leaves the Mac.** STT is local (operator ruling R6 default). Only
   short text excerpts (rolling transcript windows, retrieval snippets) go to the
   Anthropic API. Cloud STT on customer audio is a NEW data processor and does not
   exist here without its own explicit posture ruling.
2. **No bots.** This track never adds a meeting participant (operator ruling,
   2026-07-30). Fireflies keeps its existing spine role untouched; Vexa-class
   bot APIs are ruled out for this track.
3. **Read-only against the spine (v0).** Consumes canon snapshot exports; writes
   NOTHING to EQ14 Postgres. Per-call artifacts live in this repo on the Mac.
   `pkms_reads` wiring (the one enumerated future write) is DEFERRED — it lands
   before the refresh worker starts relying on read weights, not before.
4. **Route by reader.** Haiku = trigger gate (machine reads it). Sonnet = hint
   composition (Rami reads it). Opus and Fable never enter this loop.
5. **Cost ceiling per call.** Hard per-call spend cap (env), telemetry per call
   (gate calls, hint calls, tokens, $ recorded in the per-call artifact). Never
   silently raised — the runaway-spend law applied to a chatty loop.
6. **Shareability stays visible.** A hint drawn from a 🔒 canon fact renders the
   lock. The surface must never prompt the operator to speak client-named material
   (the HDFC law, applied live).
7. **Staleness rendering v0: verified_at ONLY.** `valid_until` is IGNORED in hint
   rendering until the seed date bug (valid_until == source_date on non-expiring
   facts — gate-doc follow-up) is verified fixed upstream. Otherwise hints would
   wrongly mark valid facts expired mid-call. Flip this law only on the upstream
   fix's committed evidence.
8. **me/them attribution: deterministic first, learned second.** Online calls:
   channel split — Lark M2 receiver = operator, system audio = far side; the
   voiceprint is backup. In-person: voiceprint is primary (one room, one stream).
   Voiceprint: one-time ~60 s enrollment, pyannote-class model, local, stored on
   the Mac only.
9. **Secrets.** Anthropic key in local env (0600) or keychain; no spine credentials
   on the Mac beyond the operator's existing ssh path. Nothing transits chat.
10. **House working agreements apply verbatim:** evidence before theory · verify at
    source (remembered behavior is not evidence) · one command at a time with
    expected outputs in operator runbooks · files not pastes · summaries state only
    what was verified this turn · explicit staging, never `git add -A` · STATUS.md
    edited in the same commit as any state change.

## Architecture — three loops

- **Pre-call (pack).** v0: the FULL canon snapshot is the pack — 265 rows travels as
  one small local file; refresh it before call days via the export below. P2 adds
  the per-account dossier md and a calendar-triggered pack build on the reflex
  plane.
- **In-call (the build).** Local capture → rolling transcript with me/them labels →
  utterance-end Haiku gate ("askable moment? cue moment?") → LOCAL retrieval over
  the pack (FTS-ish scoring; no index per the standing retrieval ruling) → Sonnet
  composes a 1–2 line hint → always-on-top overlay. NOTHING slow runs mid-call: no
  Brain, no EQ14 round-trips, no cloud STT.
- **Post-call.** Per-call artifact: transcript, hints shown, per-hint grades, cost.
  Unanswered questions ride the EXISTING spine (Fireflies extraction → answer lane)
  — this track adds no second writer to answer_jobs.

## Phases and gates

- **P0 — capture spike.** Pass conditions, all evidenced in a committed latency
  ledger: (a) streaming partials, p50 < 2 s on the M5 (measure faster-whisper vs
  whisper.cpp, pick by numbers, not preference); (b) a real ONLINE meeting with
  channel-split attribution ≥ 98% on a graded sample; (c) a real in-person 1-2-1
  with voiceprint attribution graded — proposed proceed bar ≥ 90%. Includes
  voiceprint enrollment. No hint logic in P0.
- **P1 — hint loop, silent shadow.** Internal calls only (1-2-1s, SC enablement).
  Overlay live; every hint graded Phase-0 style: useful / on-time / wrong, plus
  cost per call vs ceiling. Scope per settled R3: answers + sales cues/objection
  counters. Exit: an operator-set precision bar over a graded call sample, cost
  inside ceiling. External-call use does NOT begin in P1.
- **P2 — pack automation + dossier join.** GATED on dossier v1's rendered
  per-account md (D4) — per the gate announcement, not this repo's call. Adds:
  calendar-triggered pack builds (reflex plane), dossier slice in the pack,
  pkms_reads wiring (law 3's deferral ends here), first external-call use
  (operator call).
- **P3 — glasses (G2).** GATED on P1 grading evidence. Same hint stream, ~1 line,
  rate-limited to the HUD. G2 SDK status is a verify-before-build item, untouched
  until this gate.

## Verify before building (never assumed; each closes with evidence in docs/)

- ScreenCaptureKit system-audio tap on the INSTALLED macOS: works alongside
  Zoom/Meet/Teams, and — the real risk — alongside **Granola capturing
  simultaneously** during in-person meetings. Two taps on one Mac is TBV, not
  assumed compatible.
- Lark M2 USB-C receiver presents as standard USB Audio Class @48 kHz on THIS Mac
  (re-verify on hardware, not memory).
- faster-whisper vs whisper.cpp streaming latency/throughput on the M5 — measured,
  P0 picks the winner.
- pyannote-class voiceprint model: local runtime + license check.
- Canon export path (below) returns the expected row shape against live 019 schema.
- (P3 only) G2 SDK: text-push path, phone-companion vs BLE-direct.

## Canon snapshot export (P1 prerequisite; opens NO new surface)

Operator-run, rides the existing ssh → docker exec → psql loopback path
(outbound-only posture intact; Postgres stays unpublished):

`ssh eq14 "docker exec <pg-container> psql -U <user> -d <db> -Atc \"SELECT
json_agg(t) FROM (SELECT id, fact_text, structured_value, tier, volatility_class,
shareability, verified_at FROM pkms_canon WHERE status='active') t\"" >
pack/canon.json`

Exact container/user/db names come from the work-automation .env at run time —
names only in docs, values never in chat. Expected output: one JSON array, row
count = live active canon (265 at gate time). Script lands in scripts/ with the
expected-output line, per the operator profile.

## Repo conventions

`/spike` (P0 evidence code) · `/app` (P1+) · `/prompts` (versioned — gate + hint
prompts are the intelligence) · `/scripts` (export, enrollment) · `/docs` (records,
runbooks) · STATUS.md same-commit rule from day one. Per-call artifacts gitignored
(they carry customer speech text); telemetry summaries committed.
