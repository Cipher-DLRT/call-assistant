# Handover — call-assistant advisor — 2026-08-17

> **Read §0 first.** §0 is the boot verification by the Orca advisor session
> ('call-advisor', Claude Code, Fable 5, effort high) at 2026-08-17 19:40–19:50 +04
> against artifacts. Where §0 contradicts §1–§10, §0 wins; the wrong text below is
> struck, not deleted.

## 0. Boot verification 2026-08-17 (call-advisor) — what the artifacts say

Session identity (resurrection):
- Advisor session id: `a64314dd-04e8-4caf-b2ec-a6435f65cbfd` · worktree
  /Users/rami/orca/workspaces/call-assistant/call-advisor · branch
  `Cipher-DLRT/call-advisor` (fast-forwards main; no PRs).
- Warm route: `cd /Users/rami/orca/workspaces/call-assistant/call-advisor && claude --resume a64314dd-04e8-4caf-b2ec-a6435f65cbfd`
- Cold route (zero history): `scripts/launch-call-advisor.sh` from the same
  worktree (launches `claude --model claude-fable-5` with the boot prompt;
  `~/.claude/settings.json` carries `effortLevel: high` [verified]).
- MODEL RULING (operator, 2026-08-17): advisor sessions = Fable 5 (claude-fable-5)
  at HIGH effort; build sessions launched by the advisor = Opus 4.8 1M
  (`claude-opus-4-8[1m]`) or codex — never Fable unless the operator says so per
  instance. Operator-only tier, never delegated: spend, external sends,
  credentials, box provisioning, deletion.

Verified this boot [verified-this-session, commands in §7]:
- Git: origin/main == local main == 994af63 (this handover's commit); the
  eleven P1 commits 6497d3e→48ad45a EXIST and are on main (were [reported] in
  §2 — now verified). P2 plan IS committed: ea75aa8 (2026-08-17 19:32 +04,
  docs/p2-pack-automation-plan.md) + STATUS line b5d478e — §4's "landing
  unverified" is resolved. Handover uniqueness holds (one docs/handover-* file).
  Fetch/push to GitHub work again (outage over at boot time).
- **Pack is STALE against the live DB.** pack/manifest.json (operator checkout
  ~/dev/call-assistant, gitignored) = {active 223, total 265, sha a2a755…},
  file mtime 2026-08-11 19:15 +04, canon.json length 223 (matches manifest).
  Live EQ14 count same evening (read-only, names from work-automation .env,
  never printed): **active 292 / total 380**. The pack predates the ISO-dup
  retire request (named at 22:13 +04, commit 1e97f1d) and misses 69 facts
  added since. **STATUS's 2026-08-12 line "Pack re-export after ISO dedup:
  done" is FALSE by artifact** — struck in STATUS this commit. Nobody should
  shadow-call on this pack until `scripts/export-canon.sh` is re-run.
- ISO-27001 dedup on the DB: ids 25/27/28/30 = retired; **32 = still active**
  (kept — one ISO 27001 wording remains, which is the sane end state; the Code
  session's "keep 182" was a mis-pick: 182 is the infosec-policy fact, not an
  ISO cert). Fact 34 (SOC 2) active. So the retire is 4/5 by the request's
  letter and complete by intent — treated as DONE, no action.
- Shadow calls: ZERO real ones. calls/ holds 18 dirs, all 2026-08-11 19:42–22:09
  +04 (the shakedown evening); no sheet carries a single grade mark. Precision
  bar still unset.
- Menu bar: `app.menubar.menubar` running (LaunchAgent
  com.rami.call-assistant.menubar loaded, pid at boot 84366); no orchestrator
  running.
- Unknown untracked file in the operator's checkout: docs/evals/
  fluidaudio-role-eval.md (2026-08-15 11:48, ~18 KB, "repo-grounded" eval of a
  FluidAudio SDK role). Origin unknown to me; it asserts "no Swift in the
  project at all", which is false (app/capture/main.swift + 3 spike swifts) —
  its premise came from a task brief that does not match this repo. FLAGGED,
  NOT COMMITTED. Operator to say keep/delete/where it came from.
- Roster at boot: no call-assistant build session live (peers: advisor,
  relmem-advisor and their builds — other estates). Tree clean in both
  checkouts except the file above.
- Codebase shape (for future briefs): app/capture (Swift), app/stt (C,
  whisper.cpp), app/loop/*.py, app/overlay, app/menubar; tests/ has 4 files
  (artifact, cost, reader_law, retrieval); prompts/ versioned; export script at
  scripts/export-canon.sh (A1 manifest logic verified by reading it).

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
  [commits verified on main at boot 2026-08-17 (§0); "13 tests green" still
  reported: session summary — not re-run].
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
  AMBIGUOUS which dedup that refers to (see §10). **~~Whether
  scripts/export-canon.sh was re-run after the ISO retires is UNKNOWN~~ RESOLVED
  at boot (§0): it was NOT re-run — manifest still 223/265 (mtime 2026-08-11
  19:15), live DB 292/380; the pack still carries retired ISO dups 25/27/28/30
  and misses 69 newer facts. Re-export is the first operator action.**
- pack/manifest.json law: loader trusts manifest active_count, no pinned numbers
  [reported: approved build plan, amendment A1].
- Dashboard live on EQ14 serving canon; sweep run 1 → 35 proposals; retire surface
  fixed (98655e6) [reported: dossier-track records]. D4 (rendered per-account
  dossier md) DONE [op-observed — UNVERIFIED anywhere I can read].
- Shadow calls run so far: ZERO real ones. One staged leg-2 dry run (21 utterances,
  operator-graded all-correct, ME 0.59–0.71 / THEM 0.01–0.13, one 0.42
  near-threshold) — explicitly NOT pass evidence [verified-this-session: sheet
  uploaded + logged in 84c3642].
- ~~P2 plan draft delivered to operator's Downloads; commit commands given; landing
  UNVERIFIED.~~ VERIFIED at boot: committed as ea75aa8 at
  docs/p2-pack-automation-plan.md; STATUS line b5d478e. Copy to the dossier
  chat for the EQ14-half review: still unverified.
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
- 2026-08-17 · MODEL RULING: advisor sessions Fable 5 at high effort; build
  sessions Opus 4.8 1M or codex, never Fable unless said per instance;
  operator-only tier never delegated (spend, external sends, credentials, box
  provisioning, deletion) · operator, call-advisor launch prompt · §0.
- 2026-08-17 · Advisor moved from the claude.ai chat into an Orca Claude Code
  session ('call-advisor') with its own worktree; the chat's stand-off from
  building stays, but the advisor now verifies at source itself (git, files,
  ssh count) instead of via operator paste · operator · §0.
- PROPOSED, NEVER RULED: P1 exit = 3 graded calls (≥1 online, ≥1 in-person) with
  precision bar set BEFORE call 1 (suggested ≥70% useful, zero wrong on
  🔒/staleness) · recorded nowhere yet — chat proposal only.

## 4. Open items

- Canon re-export — owner: operator (or advisor on his word); state: NOT DONE
  (§0: pack 223 vs live 292); done = `scripts/export-canon.sh` run in
  ~/dev/call-assistant, manifest active_count == live count that minute, STATUS
  line corrected. ~~state: UNKNOWN~~
- P2 plan committed — ~~owner: operator; state: commands given, landing
  unverified~~ DONE (ea75aa8). Remaining: copy to dossier chat for the
  EQ14-half review — owner: operator; state: unverified.
- docs/evals/fluidaudio-role-eval.md (untracked, unknown origin) — owner:
  operator; done = keep (then commit with a provenance line) or delete.
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

From the call-advisor worktree (Orca session — these were run at boot 2026-08-17
and are the standard set; run them ALL before briefing):
- `git fetch --all && git status -sb && git log --oneline -5 && git branch -a -vv`
  → expect branch Cipher-DLRT/call-advisor; origin/main tip == local main tip
  (checked out at /Users/rami/dev/call-assistant).
- `git -C /Users/rami/dev/call-assistant status -sb` → expect clean; any `??`
  file is flagged in the brief, never committed.
- `cat /Users/rami/dev/call-assistant/pack/manifest.json; python3 -c "import json;print(len(json.load(open('/Users/rami/dev/call-assistant/pack/canon.json'))))"`
  → active_count == length; note exported_at/mtime.
- Live count (read-only; names from ~/dev/work-automation/.env, never printed):
  `ENV=~/dev/work-automation/.env; C=$(grep '^PG_CONTAINER=' $ENV|cut -d= -f2-); U=$(grep '^PG_USER=' $ENV|cut -d= -f2-); D=$(grep '^PG_DB=' $ENV|cut -d= -f2-); ssh -o BatchMode=yes eq14 "docker exec $C psql -U $U -d $D -Atc \"SELECT count(*) FILTER (WHERE status='active'), count(*) FROM pkms_canon\""`
  → MUST equal manifest active_count; mismatch = stale pack, say so first.
- `ls /Users/rami/dev/call-assistant/calls/ | tail; grep -l '\[x\]' /Users/rami/dev/call-assistant/calls/*/*.md`
  → new call dirs since last boot = calls happened; grep hits = graded sheets.
- `pgrep -fl app.menubar; pgrep -fl app.loop.orchestrator; launchctl list | grep call-assistant`
  → menu bar running; orchestrator only during a call.
- `ls docs/handover-*` → exactly one file.
- ListAgents → any call-assistant build session live? (none at boot.)

From chat, if the GitHub MCP is restored (else the operator runs the git/Mac
lines and pastes) [legacy — the chat-era set]:
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
  tree was reported clean at session close [reported] — and verified clean at
  the 2026-08-17 boot except the untracked docs/evals file (§0).
- call-advisor (this Orca session, Fable 5): owns advising/verifying/records
  for call-assistant; launches build sessions only on operator ask, in their
  own Orca worktrees (repo id 5dbdd45c-43eb-4fe5-953e-b76823bccef2), model per
  the ruling in §3; watch pattern = ~20-min tick, dated watch doc, cron
  deleted at stop. Sibling advisors: 'advisor' (work-automation), 'relmem-
  advisor' (relationship-memory) — nobody crosses repos; coordinate via
  operator or SendMessage.

## 9. Next actions (rewritten at boot 2026-08-17)

1. Re-export the pack — `cd ~/dev/call-assistant && ./scripts/export-canon.sh
   && cat pack/manifest.json` — expect active ~292 / total ~380 (whatever the
   DB says that minute), filter check OK, manifest written. Operator runs it,
   or tells the advisor "export" and the advisor runs it and reports the
   numbers. Blocks every shadow call.
2. Operator: state the hint precision bar (one number; ≥70% useful, zero
   wrong on 🔒/staleness was proposed, never ruled) — recorded in §3 the same
   sitting; blocks honest grading of call 1.
3. Operator: shadow call 1 (internal 1-2-1, menu bar → Start Shadow), grade
   both sheets same day in a plain editor, tell the advisor — the advisor
   scores the attribution sheet and records the numbers.
4. Operator: confirm the P2 plan copy reached the dossier chat (their EQ14-half
   review) — one word.
5. Operator: docs/evals/fluidaudio-role-eval.md — keep or delete.
6. ~~Restore the GitHub MCP connector~~ — no longer blocking: the advisor runs
   in Claude Code on the Mac and reads git/files/DB directly.

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
- ~~"I already Dedupped" is ambiguous between the 35-proposal sitting (which
  explains 261→223) and the ISO-5 retires; and whether the export ran afterward
  is unknown.~~ RESOLVED by artifact at boot (§0): the ISO retires happened on
  the DB (4/5, 32 kept), the export did NOT run afterward, and STATUS said
  "done" anyway — that STATUS line is struck this commit. Lesson re-confirmed:
  a STATUS line written from an operator "done" without the artifact is the
  XX.X% incident in another shape.
- D4 "done" is operator-reported only; the P2 plan's own header requires
  verifying the rendered md at build start rather than trusting the claim.
- The P1 exit criteria in circulation (3 calls / ≥70%) are a chat proposal that
  may read as settled in the scroll; they are NOT ruled. Distinction preserved
  per the skill ("chat proposed" ≠ "operator ruled").
- Numbers drift: 261 appears in CLAUDE.md's export section as "at record time"
  and 223/218 may both be stale by the time this is read — the manifest and the
  live DB outrank every number in this file, including this sentence's.
