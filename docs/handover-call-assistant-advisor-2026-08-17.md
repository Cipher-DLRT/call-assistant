# Handover — call-assistant advisor — 2026-08-17

Claim classes per the handoff skill, applied throughout: [op-observed] = operator
stated it in-conversation · [verified-this-session] = tool/file/command output seen
in this conversation · [reported: source] = named source reported it, unchecked ·
[inherited] = carried from documents/memory, verify before acting.

## 1. Role and scope

Responsible for: drawing board, gatekeeper, and review layer for the call-assistant
track (local Mac sales-call copilot; repo Cipher-DLRT/call-assistant). Author of the
PKMS pull-forward brief and GATE-CA-P1. External reviewer of anything that changes
canon (PKMS DDL spec, dashboard v1 plan, DB-D canon-maintenance plan, retire-record
consumer duties). Author of the P2 pack-automation plan draft. Step-by-step operator
guidance — the operator is not a developer and wants hand-holding plus concise
output.

Explicitly stood off from: building (Claude Code builds; this chat never writes app
code) · authoring the PKMS DDL (reassigned to the dossier chat — one pen per
migration sequence; recorded in pkms-pullforward-brief §7.7) · Slack reads (dossier
track single-writer) · committing to work-automation / eq14-stacks (other track's
repos) · running probes/legs/sittings (operator-only) · committing to
call-assistant while a Code session is mid-flight.

## 2. Estate state as VERIFIED

Repos and branches:
- Cipher-DLRT/call-assistant, branch main, private. My last remote commit: 84c3642
  ("P0 closed by operator ruling…", CLAUDE.md v1.2 + STATUS.md)
  [verified-this-session — push_files result]. Later: eleven commits 6497d3e →
  48ad45a delivering the full P1 loop (Swift capture → whisper.cpp STT →
  orchestrator → overlay → menu bar), 13 tests green, shakedown fixes, clean tree
  [reported: operator-pasted Claude Code session summary — NOT verified by me; the
  GitHub MCP dropped before I could read them].
- Cipher-DLRT/work-automation, private, unreadable from here (anonymous clone
  refused + robots-blocked fetch [verified-this-session]). All its documents in
  this conversation arrived as operator uploads: gate-ca-p1-green.md,
  dashboard-dbd-plan.md, dashboard-retire-record.md, pkms-ddl-spec.md,
  dashboard-v1-plan.md [reported: uploaded files].
- eq14-stacks: fix commit 98655e6 for the retire surface [reported:
  dashboard-retire-record.md].

Verified file states (as of my reads, since possibly superseded):
- CLAUDE.md v1.2 content incl. reader law, law 8 built-in-mic primary ruling, P0
  closed, bars → P1 exit [verified-this-session, commit 84c3642].
- docs/leg-3-score.md: cross-mic transfer 100.0%, 23/23, threshold 0.55
  [verified-this-session, SHA cd0e8cf].
- legs/leg3-2026-08-11/sheet.md: ME sims 0.63–0.80 [verified-this-session].
- STATUS.md through the P0-close entry [verified-this-session, written by me in
  84c3642]. Everything after is [reported] or unknown.

Deployed vs committed vs on-box:
- The P1 app + menu bar exist on the operator's Mac and in git [reported: session
  summary]. Nothing of this track runs on EQ14 (CLAUDE.md law).
- Canon: 223 active rows post the 35-proposal sitting [op-observed: "223 is due to
  dedup work I did"]. A further 5 ISO-27001 retires (rows 25/27/28/30/32, keep 182)
  were requested by the Code session; operator later said "I already Dedupped" —
  AMBIGUOUS which dedup that refers to (see §10). **Whether
  scripts/export-canon.sh was re-run after the ISO retires is UNKNOWN — the pack
  may still carry retired duplicates; the SOC 2 answer was named as wrong until
  re-export [reported: session summary].**
- pack/manifest.json law: loader trusts manifest active_count, no pinned numbers
  [reported: approved build plan, amendment A1].
- Dashboard live on EQ14 serving canon; sweep run 1 → 35 proposals; retire surface
  fixed (98655e6) [reported: dossier-track records]. D4 (rendered per-account
  dossier md) DONE [op-observed — UNVERIFIED anywhere I can read].
- Shadow calls run so far: ZERO real ones. One staged leg-2 dry run (21 utterances,
  operator-graded all-correct, ME 0.59–0.71 / THEM 0.01–0.13, one 0.42
  near-threshold) — explicitly NOT pass evidence [verified-this-session: sheet
  uploaded + logged in 84c3642].
- P2 plan draft delivered to operator's Downloads; commit commands given; landing
  UNVERIFIED. Target: docs/p2-pack-automation-plan.md.
- GitHub MCP: functioned earlier this session (reads + one push), then its tools
  stopped loading (two tool_search attempts returned unrelated connectors)
  [verified-this-session]. Cause unknown; assume unavailable until re-proven.

## 3. Rulings ledger

- 2026-07-29 · PKMS pulled forward as one system; call assistant is its first
  reader, not owner · Brain ~5-min async is useless live · docs/pkms-pullforward-brief.md §1–2 (work-automation).
- 2026-07-29 · Slack ingestion rides the dossier; PKMS consumes spools only ·
  single-writer per source · brief §2/§4.
- 2026-07-29 · Seed curation waits for the dashboard · Telegram cards can't carry
  batch curation · brief §2/§5.
- 2026-07-29 · R1 staleness engine + R2 two laws (operator_verified never
  machine-overwritten; unchanged refresh bumps verified_at without a tap) ADOPTED ·
  brief §6. (Chat proposed, operator confirmed "1. Agreed 2. agreed".)
- 2026-07-30 · No bots, ever, on this track; local listener; voiceprint identifies
  the operator · "bot approach is iffy" · call-assistant CLAUDE.md laws 2/8.
- 2026-07-30 · R3: live scope = answers + sales cues · local latency makes cues
  viable · CLAUDE.md P1 scope. (Chat proposed as consequence, operator accepted.)
- 2026-07-31 · DB-D sweep model = Opus 4.6; cadence monthly + always-one-ping ·
  operator call · dashboard-dbd-plan §4 + dbd-review E5 (as corrected).
- 2026-08-11 · P0 CLOSED; the two attribution bars (≥98 online / ≥90 in-person)
  move to P1 exit · "I want this live the first time I use it" · CLAUDE.md v1.2 +
  STATUS (commit 84c3642).
- 2026-08-11 · Primary in-person rig = built-in MacBook mic; Lark = enhancement
  when worn · "I'm more likely to be using the built in mic" · CLAUDE.md law 8
  (84c3642).
- 2026-08-11 · No terminal in daily use — menu-bar launcher before first shadow
  call (P1.5) · operator · built per session summary; runbook [reported].
- ~2026-08-12 · "Speakerless ruling": my A4 headset requirement SUPERSEDED;
  compensators = voiceprint bleed guard + CUT-row grading · operator ·
  recorded-where UNKNOWN to me (STATUS presumed) [reported: session summary].
- 2026-08-12 · A2: pack 223 = post-dedup active canon, pack trusted ·
  op-confirmed · STATUS via Code [reported].
- 2026-08-17 · Handover format: exact headings, dated filename · operator
  instruction this session · this file (conflicts with handoff skill — §10).
- PROPOSED, NEVER RULED: P1 exit = 3 graded calls (≥1 online, ≥1 in-person) with
  precision bar set BEFORE call 1 (suggested ≥70% useful, zero wrong on
  🔒/staleness) · recorded nowhere yet — chat proposal only.

## 4. Open items

- Canon re-export after ISO dedup — owner: operator; state: UNKNOWN; done =
  export run, manifest active_count reflects retires, honest STATUS line.
- P2 plan committed — owner: operator; state: commands given, landing unverified;
  done = docs/p2-pack-automation-plan.md in repo + STATUS line + copy to dossier
  chat for EQ14-half review.
- Precision bar — owner: operator; state: unset; done = one number stated and
  recorded BEFORE grading shadow call 1.
- Shadow calls 1–3 (internal only) — owner: operator; state: zero run; done =
  each call's two sheets graded same day, scores + sheets pushed.
- P1 exit review — owner: next session; state: blocked on the above; done = exit
  declared on evidence (98/90 bars from CUT-row grading + precision bar) or
  misses named with the failing rows.
- Two canon gaps (pricing model, banking customer counts) — owner: operator via
  answer lane → curation → re-export; done = facts in canon + new pack.
- GitHub MCP restore — owner: operator (connector settings); done = repo reads
  work from chat again.
- Dossier-track items visible from here (owner: dossier chat): DB-D build state
  after my E1–E6 review [inherited]; staleness-amendment-1 committed text (was
  owed); valid_until seed-bug verification → only its committed evidence flips
  CLAUDE.md law 7.
- pgvector tripwire — owner: next session; passive; done = trigger check per
  graded call (vocabulary-mismatch misses >10–15% of askable moments → shadow
  pgvector audition).

## 5. Method rules learned

- Verify at source cuts both ways: never assert a model/product does NOT exist
  from memory (I falsely claimed "Opus 4.6 doesn't exist"; operator was right;
  correction written into dbd-review E5 visibly).
- A filename or announcement is not state — read the evidence before resuming
  work on it (gate-ca-p1-green.md read before P1 resumed).
- The vacuous-test doctrine applies to my own checks (my "no status field in
  pack" check was vacuous — a dropped WHERE never adds a field; replaced by the
  manifest law, A1).
- Corrections are written into the committed record, wrong text struck visibly,
  never papered (E5; the XX.X% STATUS placeholder).
- One pen per repo/migration sequence; reviews return as committed docs; the
  operator is never the transport layer (brief §7.6–7.7).
- Stay off a repo while another session is mid-flight; relay via operator paste.
- Operator platform observations override my inferences immediately (unplugged-
  headphones reframe; Opus 4.6).
- Don't pin moving counts anywhere; pin invariants and manifests (261→223
  lesson).
- Give exactly one command with its expected output; on mismatch, full stop.
- Grading sheets die in markdown editors ([ x] mangling) — plain editors only;
  a sed repair exists in the scroll if it recurs.

## 6. Traps

- The pack does NOT auto-update from dashboard changes. Every canon change needs
  a manual export. Check manifest vs live DB count, never remembered numbers.
- GitHub MCP can silently vanish mid-session; tool_search may not resurface it.
  Verify tool availability before promising repo operations.
- Operator claims of "done" can refer to a different task than asked ("I already
  dedupped" — which dedup?). Pin the referent before recording.
- Speakers leak far-side audio into the mic at transcribable levels (−57 dBFS
  smoke evidence). Headset requirement was superseded by operator ruling — the
  98% bar must now be proven through CUT-row grading; watch those rows.
- Staged/dry-run artifacts masquerade as pass evidence unless labeled at birth.
- STATUS lines get committed with unfilled placeholders (XX.X% incident) — read
  the numbers, not the shape.
- Private repos: web_fetch is robots-blocked and anonymous clone refuses —
  uploads are the only channel when the MCP is down.
- work-automation must stay PRIVATE (vendored proprietary skills) [inherited] —
  never suggest flipping visibility to solve access.

## 7. Live verification commands

From chat, if the GitHub MCP is restored (else the operator runs the git/Mac
lines and pastes):
- Read Cipher-DLRT/call-assistant STATUS.md → expect: P0-closed header, log
  through P1-build and P2-draft lines; no unfilled placeholders.
- Read pack/manifest.json IF committed (may be gitignored with pack/) → expect
  active_count == canon.json length; exported_at AFTER the ISO dedup date.
Operator on the Mac (~/dev/call-assistant):
- `git log --oneline -5` → expect tip ≥ 48ad45a, 84c3642 in history.
- `cat pack/manifest.json` → expect {exported_at, active_count, total_count,
  sha256}; active_count == `python3 -c "import json;print(len(json.load(open('pack/canon.json'))))"`.
- `ls calls/` → per-call dirs; each real call has artifact.json + two sheets.
- Menu bar shows ○ CA; Start/Stop present.
Operator on EQ14 (names from work-automation .env, never in chat):
- `ssh eq14 "docker exec <pg> psql -U <u> -d <db> -Atc \"SELECT count(*) FROM
  pkms_canon WHERE status='active'\""` → MUST equal manifest active_count; a
  mismatch means a stale pack — do not shadow-call on it.
- Handover uniqueness assertion (skill law): exactly one file matching
  docs/handover-* exists in call-assistant.

## 8. Sessions and concurrency

- Claude Code (operator's Mac, call-assistant checkout): built everything in
  /app; episodic sessions; last reported state clean at 48ad45a. Owns the local
  checkout. This chat commits remotely ONLY when no Code session is mid-flight
  AND the MCP is up.
- Dossier advisor chat + its Code sessions: own work-automation, eq14-stacks,
  the dashboard, PKMS, and the EQ14 half of P2 once they receive the plan. They
  hold three of my review verdicts (DDL, dashboard v1, DB-D) [reported: operator
  relayed commits].
- Codex: used inside Code's sessions for separable modules + adversarial review;
  not managed from here.
- Nothing in call-assistant is known half-done by another session; the working
  tree was reported clean at session close [reported].

## 9. Next actions

1. Operator: restore the GitHub MCP connector — blocks all chat-side
   verification (everything below is checkable without it, via paste).
2. Operator, Mac: `./scripts/export-canon.sh && cat pack/manifest.json` —
   blocks trusting any shadow call; resolves the §2 unknown.
3. Operator: confirm P2 plan committed (docs/p2-pack-automation-plan.md) and
   copy handed to the dossier chat — blocks their EQ14-half review.
4. Operator: state the hint precision bar (one number; ≥70% was proposed,
   never ruled) — blocks honest grading of call 1.
5. Operator: shadow call 1 (internal, menu bar → Start Shadow), grade both
   sheets same day, push, notify — the next session's first review input.

## 10. Contradictions you know of

- Handoff skill vs operator instruction: the skill forbids dated handover
  filenames (one-name-one-path) and mandates a separate accreting rulings-sweep
  file; the operator's instruction (this session) demands a dated single
  document with exact headings. Operator instruction followed; the skill's
  uniqueness assertion (§7 last line) will flag any second handover file.
- A4 headset requirement (mine, grounded in −57 dB smoke evidence) vs operator's
  speakerless ruling: superseded, not withdrawn — I hold that the ≥98% online
  bar is materially harder without a headset and that CUT-row grading now
  carries the burden of proof. If the bar fails on bleed rows, the ruling is the
  first suspect.
- "I already Dedupped" is ambiguous between the 35-proposal sitting (which
  explains 261→223) and the ISO-5 retires; and whether the export ran afterward
  is unknown. My last statement to the operator required the STATUS line to say
  done/pending honestly; I never saw the answer.
- D4 "done" is operator-reported only; the P2 plan's own header requires
  verifying the rendered md at build start rather than trusting the claim.
- The P1 exit criteria in circulation (3 calls / ≥70%) are a chat proposal that
  may read as settled in the scroll; they are NOT ruled. Distinction preserved
  per the skill ("chat proposed" ≠ "operator ruled").
- Numbers drift: 261 appears in CLAUDE.md's export section as "at record time"
  and 223/218 may both be stale by the time this is read — the manifest and the
  live DB outrank every number in this file, including this sentence's.
