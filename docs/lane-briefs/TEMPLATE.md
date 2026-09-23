# <kind>-brief <lane-name> — <one-line purpose> (<date>)

<!-- Every build, review, walk, diag and apply brief in work-automation starts from this file
     (ADVISOR.md Part II §35, formerly ADVISOR-ESTATE §35). The two header sentences below are copied VERBATIM; a brief without
     them is returned before launch. Fill every <…>; delete nothing above the Legs/Do section. -->

**Category:** <feature — milestone #<n> | path towards feature — #<issue> | fix | instrument | estate>. A build
brief with no Category line is not launched. A feature build brief that signals an advisor's main checkout is not
launched: milestone work launches from an owner's worktree (ADVISOR.md §D, operator 2026-09-16).
DESIGN: <docs/<architect design file>.md on origin/main> — on every feature build brief; a feature build with no
design is refused (ADVISOR.md L2, operator 2026-09-16).
BRIEF-REVIEW: <LAUNCH | LAUNCH WITH RISKS: <named> | DO NOT LAUNCH> | <lane>-briefreview | round <n> | <date> — on
every build brief whose HOSTS name eq14, Postgres, HubSpot, Gmail or Telegram; no line, no launch (operator, 2026-09-16).

BOUNDARY (ESTATE §31): No writes outside this worktree. Commit only in this worktree (and the sibling
worktree named in EQ14_PATH.txt / WA_PATH.txt when the brief names one); never the operator's main
checkouts, never another repo, never a tracked root file. **PUSH YOUR OWN LANE BRANCH, and never
main.** Your DONE signal names a sha the advisor verifies at origin (ESTATE §37), so an unpushed
lane cannot be landed, and its record dies with the worktree. Push early; no unpushed work stays in an Orca
worktree overnight.

HOSTS (ESTATE §34): This lane touches only the hosts named here, for the path and purpose stated:
<none | eq14 (ssh) — <path/command> — <purpose, read-only|write> | n8n API (MCP read tools) — <purpose>>.
Any read or connection beyond this list is an incident: stop, record what was read and where the copy
went in the report, and ASK-ADVISOR. A fixture that lives on the box and is not listed here is fetched
by the advisor's named worker into a briefed path first. Each entry cites the exact path and command, not the host
alone. A lane running scripts/n8n.sh symlinks the repo `.env` in and never reads, prints or commits it. A wait on a
log names a literal copied from a real line of that log, and says "read from a real line". No `$<digit>` appears in
any LANE-SIGNAL text; write "arg 1", "field 2".

REASON (ESTATE §70): exactly one of <feature | path-to-feature | fix | research | estate>, stated in
one sentence at the top, before the lane opens. `feature` names the manual act it removes and carries
a USE leg; `path-to-feature` names the feature at the end and what still stands between; `fix` names
the defect and the feature it degrades (a defect no feature depends on is a `research` question);
`research` names the decision it informs and ships no artifact; `estate` names the builder friction it
removes, who was slowed, what breaks or slows without it, and the time it returns where that can be
counted. A phase list is not a reason. Hardening, controls and refactors take no
label of their own. A brief that cannot name one does not open.

TIER (ESTATE §2): cheapest that fits — menial → opus-medium; simple bounded build → grok-medium or grok-high by
complexity, or codex-medium when the codex harness is needed; standard build → codex-high; genuinely hard → grok-xhigh, codex-xhigh or opus-xhigh; muse-xhigh on muse-spark-1.3-contributor when Muse is the chosen family; review →
cross-family from the builder. Write-enabled GitHub automation lanes are Opus 5 from the start. One-line
why: <…>. Launch with `$ESTATE/scripts/lane.sh launch <lane> <tier> <brief>`.
TIER: <grok-medium | grok-high | opus-medium | opus-high | opus-xhigh | codex-medium | codex-high | codex-xhigh | codex6-xhigh (brief review only) | muse-xhigh>. Gate: <in-lane <family> gate REQUIRED — cross-family from the builder |
NOT REQUIRED — §F all not-engaged, one git revert undoes it with no data loss>
(read-only `claude -p --model claude-opus-5`; RESULT verbatim in HANDOFF.md) — for build lanes.
External review: <NOT required (class: <presentation | additive nullable | read-only | prompt>) |
REQUIRED (class: <grant/role | containment | external write | column drop | customer data off-box>)>.
Secrets: none appear in chat, reports, git or terminals — key NAMES, byte lengths, sha256 prefixes only.
Customer content stays on the box: quote ids, counts, file names; never body text.

PREREQUISITES (ESTATE §32): each thing outside the reviewed diff that this lane
or its deploy assumes exists — a network, a directory and its mode, a secrets home, a role, a
marker path — with the seat that creates it, the command, and the check that proves it before the
step that depends on it. "<none>" is a valid entry; an unowned prerequisite sends the brief back. A
DSN-gated brief names the committed in-repo provisioning script, the admin role it runs as and the test
role it provisions.

GATE LEGS (ESTATE §47): every gate this landing meets — attest, rehearsal, coupling run,
review, test sweep — listed as a leg of its own with its command and the artifact the gate reads.
A lane that cannot run a named leg from its worktree STOPS before building and signals; an unrun
leg is never reported as absent. Standing legs when they apply: a provider-facing schema change → a
zero-spend provider-acceptance call before the first spending run; a file added, removed or renamed in
a service's runtime source set → the built image, run once, plus a COPY-set closure test; a change to
converge.sh or any deploy script → a trace per stack and per guard state plus a harness over those
states. An eq14 gate package names, per step, whether converge or a worker performs it — converge
recreates a whole stack when its directory changed — orders any prerequisite ahead of the push, and
measures the window converge forces. An operator-surface n8n release brief carries, BEFORE its update leg,
the rehearsal leg: `scripts/rehearse-flow-sql.sh flows/<flow>.json` run from the lane worktree, its `PASS:` line
pasted, and `docs/rehearsals/<flow>-<blob>.txt` committed on the lane branch by explicit path; HOSTS names the
eq14 read. `scripts/n8n.sh update` refuses (exit 6) without that exact-blob artifact.

DEPLOY PIN (deploy briefs): the code to deploy is origin/main plus an EMPTY code-diff proof against
the reviewed sha (docs/ and STATUS excluded), never a literal sha. A digest pin names what was
digested and cites the line it came from.

§F CLASSIFICATION (ADVISOR.md §F), one line per item, engaged-with-review-record or not-engaged:
grants/roles/credentials; containment/egress; external writes; column drop/alter; customer data
off-box. A destructive-SQL grep answers drop/alter only and is not the classifier.

FORBIDDEN WRITES (walk briefs): every control on the surface that writes — dismiss, accept,
reject, approve, decline, release, send — is forbidden except the ones named below, each with its
REVERSAL: the full set of named writes that returns the operator's state to exactly what it was,
with before/after proofs, stated BEFORE the walk runs. Any other write is an incident, reversed
and verified before the attest.

## Context (files to read first, with paths)
- <docs/…, build/…, schema/…>

## The change / The question / Legs
<exact scope; file:line where known; verdict forms for diag/review; numbered legs for walks>
Design-loop brief: docs/design/CONTEXT-PACK.md is required FIRST reading, the estate palette is named, and
every critic review opens by scoring the candidate against the operator's pinned verdicts, one line each.
Review brief: one or two named files, a word cap, the facts already verified supplied, the artifact frozen for
the round (or the reviewer told what moved), and the dry-run done BEFORE the review with its results attached.
Walk-brief leg: compare against the prior render for this surface.

## Pins (build lanes: build/test_code.js) / Verdict line (diag, review) / PASS rule (walks)
<…>
Walk verdicts use exactly three forms — `RESULT: PASS —`, `RESULT: FAIL —`, `RESULT: FAIL-FIXED-PENDING — …;
fixed by <ref>` — which scripts/walk-attest.sh parses. A leg that ran but cannot settle its question writes
`RESULT: PASS — not visually decidable from the rendered surface; <what you did check>`; a leg that could not
run writes `NOT EXERCISABLE — <reason>`. Do not invent a verdict either way.

## Deliverables, verbatim
0. Every timestamp in this brief's body comes from a fresh `date`; a file this brief calls "new" carries
   `git ls-files <path>` empty at the base sha.
   First act: `LANE-SIGNAL <lane> | BOOT | reading the brief` to the advisor handle. The advisor verified the
   worktree gate (fresh worktree, single occupant); this lane never calls `orca worktree`. A long-running spend
   lane states its RESUME story here (what survives an interruption without re-burning completed work).
1. Commits `<lane>:` in <tree(s)> with explicit paths; HANDOFF.md in the seat worktree root (diff summary, suite
   lines, Opus RESULT verbatim, COST line: `COST <lane>: model=<id> effort=<e> wall=<h:mm> rounds=<review rounds> spend≈$<usd or n/a (subscription)> saves≈<h/month or n/a>`).
   HANDOFF.md carries a `Removed behaviour` section (list each behaviour the diff removes, or 'none') and, for every previously-seen surface it changes, a before/after rendered pair compared against the prior walk's render (cite the prior report).
   HANDOFF.md names every standing check the lane ran (e.g. a schema/checks/ member) with its own before and
   after exit lines.
   Never commit HANDOFF.md, BRIEF.md, EQ14_PATH.txt/WA_PATH.txt or flag files.
2. `touch <worktree>/HANDOFF-READY` — the same file for every lane kind (build, review, walk, diag, apply); the outcome (verdict, PASS/FAIL, blocked reason) goes INSIDE the file, never into its name (ESTATE §8 rule 3), then signal
   `orca terminal send --terminal <advisor handle> --enter --text 'LANE-SIGNAL <lane> | <BOOT|STOP|ASK|DONE> | <one line>'`
   (or `$ESTATE/scripts/lane.sh signal`); the prefix is verbatim, pipe-delimited, and the first characters of the message.
3. A question you cannot answer from source: write ASK-ADVISOR in the worktree root and signal the same way. Never stop silently.
   Signal-at-every-stop: send the LANE-SIGNAL BEFORE any approval request, blocker, question or finish.

## Waiting on a lane (walk coordinators especially — ADVISOR.md 48, 8 rule 2b/6)
WAKE (primary): the lane's own `LANE-SIGNAL <lane> | DONE | ... pushed <sha>` into YOUR
terminal — its mandated last act, and the only true edge.

A WAKE IS NOT PROOF OF COMPLETION. The proof is the evidence at origin (37). On every wake:
`git ls-remote origin <branch>` ONCE. If the sha is not there, the leg is not done — RE-ARM
the wait. That is edge-driven with a guard, not a poll: one check per wake, no timer.

BACKSTOP: `orca terminal wait --terminal <handle> --for tui-idle --timeout-ms <ms>`, armed
only AFTER the target is confirmed busy. Measured 2026-09-09: `tui-idle` is a LEVEL, not an
edge — armed on a TUI that is idle it returns `satisfied: true` in 0 s, so arming it at launch,
or while the lane sits on an approval prompt, wakes you instantly with nothing done. On a plain
shell it never fires at all, and `--for exit` never fires for a lane that stays at its prompt.
Codex lanes use the notify-hook log tail instead (8 rule 2c).

A lane that stalls on an approval prompt cannot be un-stuck by `orca terminal send` — Orca
refuses with `agent_prompt_blocked`. Launch every lane with its approval mode ON THE COMMAND
LINE (codex `--approve-for-me`, claude `--permission-mode`), as 8 rule 1 already requires.

NEVER "poll every N s" and never a `while`/`until` read loop: 8 rule 6 caps a waiting lane's
re-read at once per 20 minutes, and walkrun-4's brief ordered a 60-90 s poll that cost 139 M
tokens in 35 minutes. Watching ORIGIN rather than screen text stays correct; it is the check
after the wake, not the wake itself.

A walk coordinator covers ONE leg or one small adjacent group (48), and runs on a machine-read
model, not Opus or Fable. $ESTATE/scripts/hooks/walk-brief-lint.py enforces all three at commit and push.
