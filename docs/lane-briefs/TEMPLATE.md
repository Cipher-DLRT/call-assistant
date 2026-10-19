# <kind>-brief <lane-name> — <one-line purpose> (<date>)
FEATURE: <one or two sentences: what someone can do or see when this lands that they cannot now, and the one command or screen that shows it>
<!-- It describes the result, never the change list; it names no file the lane must open. -->

<!-- Every build, review, walk, diag and apply brief in work-automation starts from this file
     (ADVISOR.md Part II §35, formerly ADVISOR-ESTATE §35). The two header sentences below are copied unchanged; a brief without
     them is returned before launch. Fill every <…>; delete nothing above the Legs/Do section. -->

<!-- CORE BEGIN — byte-identical in all eight endpoints. Edit ONLY in estate-tooling, the original; an edit anywhere else is drift the identity checker will refuse. -->
**Category:** <feature — milestone #<n> | path towards feature — #<issue> | fix | instrument | estate>.
ISSUE: #<issue>
DESIGN: <feature only: docs/<design>.md on origin/main; facts with file:line, at most 120 words>.
BRIEF-REVIEW: <LAUNCH | LAUNCH WITH RISKS: <named> | DO NOT LAUNCH> | <lane>-briefreview | round <n> | <date> — only when a §F row is engaged.
REVIEWS: <path of the brief or artifact reviewed> — review briefs only.
REPRODUCED: <record of the command and output> — repeat review briefs only.
FILES: <path> [<path>...] — review briefs only: the reviewer reads these and the build brief, nothing else.
PRIOR LANES: <none | <lane> failed because <cause, one line>; this brief fixes it by <change>> — when a lane on this issue ran before.

## Facts
- <fact the owner already gathered> — <source: path:line, sha, #<n> or measured <date>>. One line per fact. Re-check a fact if you doubt it; never rediscover it. Name in HANDOFF anything you had to find that this list should have carried (#497).

## Scope
Build what FEATURE says, at that size. Add no cap, limit, fence, allow-list, time window, refusal or fail-closed default that this brief does not list below with its origin. If you think one is needed, ASK; do not add it.
LIMITS: <none | each limit — origin: operator ask #<n> comment | docs/rulings.md <date> | vendor documented limit <link>>.

## Boundaries
Write only inside this worktree, plus <any named sibling worktree>. Commit with explicit paths; land your own branch with lane.sh land when your close verifier is green, and name the landed sha in DONE.
HOSTS: <none | host — exact path or command — purpose — read-only|write>. An unlisted read or connection is an incident: stop, record it, and ASK.
Stubs: declare each with `STUB: <tool>` and `FIXTURE: <tool> docs/fixtures/<tool>-<date>.txt`; its answers use those bytes.
Secrets never appear in chat, reports, git or terminals; report key names, byte lengths or sha256 prefixes. Customer content stays on the box; report ids, counts and file names.

REASON: <one clause naming the manual act removed, defect fixed or decision informed>.
TIER: <tier>. TIER-REASON: <one clause: the rung (hardest, hard, the rest) and why the rung below it does not fit; then why this effort fits>.
Gate: <in-lane cross-family gate REQUIRED | NOT REQUIRED — §F all not-engaged, one revert restores with no data loss>.
External review: <NOT required — class | REQUIRED — class and review record>.
PREREQUISITES: <none | dependency — seat creating it — command — check before the dependent step>. A DSN-dependent step names its provisioning script, admin role and test role.
A change engages a §F row when, after it lands, a person, process, host or vendor can reach a credential, an account, a customer's data, money or a production host that it could not reach before, beyond what the operator's ask or a ruling already grants; a change that stays on the Mac inside a lane's own worktree, its own settings or its own box dir and opens no new path to a production host is never engaged (#554).
§F CLASSIFICATION: grants/roles/credentials — <not-engaged | engaged>; containment/egress — <not-engaged | engaged>; external writes — <not-engaged | engaged>; column drop/alter — <not-engaged | engaged>; customer data off-box — <not-engaged | engaged>; money — <not-engaged | engaged>.

## Rulings carried
<Each ruling this work must honour: docs/rulings.md <date> or the issue comment. Do not quote the operator. Do not restate doctrine here.>

## Legs
1. RED: <the failure at base, and a passing control>.
2. Implement: <paths and commit prefix>.
3. GREEN: <checks, with pasted exit lines>.
4. BREAK — gate, hook or lint briefs only: <probes that try to get past the rule>.
5. USE: <the real-work use that shows FEATURE, or who runs it and when>.
A leg you cannot run means STOP before building; never report an unrun leg as absent.

Apply the lines below that match this lane; ignore the rest:
- Provider-facing schema change: a zero-spend acceptance call before spending.
- Runtime source-set change: run the built image and the COPY-set closure test.
- Deploy-script change: trace each stack and guard state and run a harness over those states.
- n8n release: `scripts/rehearse-flow-sql.sh flows/<flow>.json` before the update; paste PASS; commit `docs/rehearsals/<flow>-<blob>.txt`; HOSTS names the box read.
- Deploy leg: uses origin/main and proves its code diff from the fix-pass tip (or the reviewed sha) is empty, excluding docs/ and STATUS.
- User surface: load the frontend-design and design-taste-frontend skills and the claude-design MCP before the first render; a render that is not elegant is refused at close (2026-10-12).
- Design loop: read docs/design/CONTEXT-PACK.md first.
- Review: freeze the artifact, name the reading fence and word cap, supply the dry-run results. The report's last line is `verdict=<token>`, outside any fence (#406).
- Walk: compare the prior render; name every permitted write and its reversal with before/after proofs. An unlisted walk write is an incident: reverse and verify it before attesting. Results read `RESULT: PASS —`, `RESULT: FAIL —` or `RESULT: FAIL-FIXED-PENDING — …; fixed by <ref>`. A leg that cannot run says `NOT EXERCISABLE — <reason>`.
- Digest pin: cite the source line. Log wait: use a literal read from a real log line.

## Deliverables
1. Commits `<lane>:` with explicit paths. A file called new has `git ls-files <path>` empty at the base sha.
2. HANDOFF.md in the worktree root (never committed): diff summary; `Removed behaviour` (list or none); the `TEST:` blocks pasted from `$ESTATE/scripts/lane-test.sh [--tag RED-PARENT|GREEN-TIP|MUTATION-RED|CONTROL] <command>` with their `ARTIFACT:` lines; for a surface, `WALK: <walk record or fresh screenshot>`; and one line:
   `COST <lane>: model=<id> effort=<e> wall=<h:mm> rounds=<n> spend≈$<usd or n/a> saves≈<h/month or n/a>`.
3. Commit artifacts under docs/ at lane-specific paths. Never commit HANDOFF.md, BRIEF.md or flag files.
4. Run the close verifier on this worktree, `touch HANDOFF-READY`, then signal the handle in this brief's signal block:
   `orca terminal send --terminal <launcher handle> --enter --text 'LANE-SIGNAL <lane> | DONE | <one line, pushed sha>'`.
5. A question the source cannot answer: write ASK-ADVISOR in the worktree root and signal ASK. Signal STOP when stopped for good. Send no other signal: no progress, INFO, UPDATE or BOOT (#540). No `$<digit>` in signal text.
<!-- CORE END -->

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
