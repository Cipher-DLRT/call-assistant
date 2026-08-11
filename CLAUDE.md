# call-assistant — CLAUDE.md (seed v1.2, 2026-08-11)

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
   channel split — mic input = operator, system audio = far side; the voiceprint
   is backup — and since the speakerless ruling (2026-08-11, "no headphones is
   very important") it actively guards the mic stream: a mic utterance that
   fails the print (< threshold) is far-side speaker bleed and is CUT —
   excluded from transcript and gating; the system-audio copy remains the
   canonical THEM record. Headset recommended, no longer required. **Primary rig = the built-in MacBook mic (operator ruling
   2026-08-11); the Lark M2 is an enhancement when worn, not an assumption.**
   In-person: voiceprint is primary (one room, one stream); leg 3 proved the
   Lark-enrolled print transfers to the built-in mic (100%, sims 0.63–0.80 vs
   0.55 threshold). Voiceprint: one-time ~60 s enrollment, ECAPA-class model,
   local, stored on the Mac only.
9. **Secrets.** Anthropic key in local env (0600) or keychain; no spine credentials
   on the Mac beyond the operator's existing ssh path. Nothing transits chat.
10. **House working agreements apply verbatim:** evidence before theory · verify at
    source (remembered behavior is not evidence) · one command at a time with
    expected outputs in operator runbooks · files not pastes · summaries state only
    what was verified this turn · explicit staging, never `git add -A` · STATUS.md
    edited in the same commit as any state change.

## Architecture — three loops

- **Pre-call (pack).** v0: the FULL canon snapshot is the pack — active canon
  travels as one small local file; refresh it before call days via the export
  below. P2 adds the per-account dossier md and a calendar-triggered pack build
  on the reflex plane.
- **In-call (the build).** Local capture → rolling transcript with me/them labels →
  utterance-end Haiku gate ("askable moment? cue moment?") → LOCAL retrieval over
  the pack (FTS-ish scoring; no index per the standing retrieval ruling) → Sonnet
  composes a 1–2 line hint → always-on-top overlay. NOTHING slow runs mid-call: no
  Brain, no EQ14 round-trips, no cloud STT.
- **Post-call.** Per-call artifact: transcript, hints shown, per-hint grades, cost.
  Unanswered questions ride the EXISTING spine (Fireflies extraction → answer lane)
  — this track adds no second writer to answer_jobs.

## Phases and gates

- **P0 — capture spike. CLOSED 2026-08-11 (operator ruling: "first use is live").**
  Closed on: verify checks a/b/c (Granola coexistence PASS; Lark = mono mix, no
  TX split; whisper.cpp p50 0.313 s) · enrollment (same-speaker 0.9249, impostor
  0.1828) · leg 3 cross-mic transfer 100% (23/23, sims 0.63–0.80) · a staged
  end-to-end dry run with a real second voice (ME sims 0.59–0.71, THEM 0.01–0.13;
  one near-threshold THEM at 0.42 — recorded failure surface for P1 grading).
  **The two live attribution bars did NOT close in P0 — moved to P1 exit by the
  same ruling.** Risk accepted and stated: if live attribution disappoints, P1 is
  already built; bounded by the two measured passes above.
- **P1 — hint loop, silent shadow.** Internal calls only (1-2-1s, SC enablement).
  Overlay live; every hint graded Phase-0 style: useful / on-time / wrong, plus
  cost per call vs ceiling. Scope per settled R3: answers + sales cues/objection
  counters. **Exit: an operator-set precision bar over a graded call sample, cost
  inside ceiling, PLUS the P0-inherited attribution bars measured on the first
  real shadow calls — channel-split ≥ 98% (online; headset recommended —
  speakerless calls supported per the 2026-08-11 ruling via the voiceprint
  bleed guard, CUT rows graded on the same sheet) and voiceprint ≥ 90%
  (in-person; built-in mic = primary rig). Grading sheets auto-generate from the
  per-call artifact — the first shadow calls ARE legs 1 and 2.** External-call
  use does NOT begin in P1.
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
  assumed compatible. [CLOSED: check (a) PASS]
- Lark M2 USB-C receiver presents as standard USB Audio Class @48 kHz on THIS Mac
  (re-verify on hardware, not memory). [CLOSED: check (b) — mono mix, no TX split]
- faster-whisper vs whisper.cpp streaming latency/throughput on the M5 — measured,
  P0 picks the winner. [CLOSED: check (c) — whisper.cpp]
- pyannote-class voiceprint model: local runtime + license check. [CLOSED:
  ECAPA, Apache-2.0, local]
- Canon export path (below) returns the expected row shape against live 019 schema.
- (P3 only) G2 SDK: text-push path, phone-companion vs BLE-direct.

## Canon snapshot export (P1 prerequisite; opens NO new surface)

Operator-run, rides the existing ssh → docker exec → psql loopback path
(outbound-only posture intact; Postgres stays unpublished):

`ssh eq14 "docker exec <pg-container> psql -U <user> -d <db> -Atc \"SELECT
json_agg(t) FROM (SELECT id, fact_text, structured_value, tier, volatility_class,
shareability, verified_at FROM pkms_canon WHERE status='active') t\"" >
pack/canon.json`

**Reader law: every canon read in this repo filters status='active'; retired
facts must never reach a pack or a hint. Origin: dashboard-retire-record.md §3.**
The `WHERE status='active'` in the export above is this law, not an incident of
the query.

Exact container/user/db names come from the work-automation .env at run time —
names only in docs, values never in chat. Expected output: one JSON array, row
count = ACTIVE canon, strictly BELOW total. The absolute number moves as the
operator retires facts (261 at record time; 223 on the first real export,
2026-08-11, after the operator worked the pending retire queue — confirmed
post-dedup active canon, operator cleanup mini-sitting), so the check is the
comparison, not the number: active == total is the failure signature meaning
the status filter is missing — STOP, do not build a pack from it.
scripts/export-canon.sh runs the export and enforces this check.

**Manifest (amendment A1, 2026-08-11): filter verification lives at export
time, where DB truth is queryable.** The export script compares the JSON
length against the DB's own active count (same session), refuses on mismatch,
and writes `pack/manifest.json` `{exported_at, active_count, total_count,
sha256}`. The in-call loop loader verifies pack length == manifest.active_count
and sha256 match, and refuses to start otherwise. No pinned row count anywhere.

Suite pin (lands with the P1 retrieval code, mirror of the seed reader-law pin
in the dossier repo): any SQL touching pkms_canon without the status filter
fails the build.

## Repo conventions

`/spike` (P0 evidence code) · `/app` (P1+) · `/prompts` (versioned — gate + hint
prompts are the intelligence) · `/scripts` (export, enrollment) · `/docs` (records,
runbooks) · STATUS.md same-commit rule from day one. Per-call artifacts gitignored
(they carry customer speech text); telemetry summaries committed.
