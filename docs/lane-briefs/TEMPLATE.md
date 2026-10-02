# <kind>-brief <lane-name> — <one-line purpose> (<date>)
FEATURE: <one or two sentences: what someone can do or see when this lands that they cannot now, and the one command or screen that shows it>
<!-- It describes the result, never the change list; it names no file the lane must open. -->

<!-- Every build, review, walk, diag and apply brief in work-automation starts from this file
     (ADVISOR.md Part II §35, formerly ADVISOR-ESTATE §35). The two header sentences below are copied VERBATIM; a brief without
     them is returned before launch. Fill every <…>; delete nothing above the Legs/Do section. -->

<!-- CORE BEGIN — byte-identical in all eight endpoints. Edit ONLY in estate-tooling, the original; an edit anywhere else is drift the identity checker will refuse. -->
**Category:** <feature — milestone #<n> | path towards feature — #<issue> | fix | instrument | estate>.
ISSUE: #<issue>
DESIGN: <for a feature, docs/<design>.md on origin/main; facts with file:line, at most 120 words, no discovery history>.
BRIEF-REVIEW: <LAUNCH | LAUNCH WITH RISKS: <named> | DO NOT LAUNCH> | <lane>-briefreview | round <n> | <date>
REVIEWS: <path of the brief or artifact reviewed> — review briefs only.
REPRODUCED: <record of the command and output> — repeat review briefs only.
FILES: <path> [<path>...] — the reviewer's reading fence, besides the build brief.

BOUNDARY: No writes outside this worktree.
Commit only here with explicit paths, plus <any explicitly named sibling worktree>. **PUSH YOUR OWN LANE BRANCH, never main**, and name the pushed sha in DONE.

HOSTS: <none | host — exact path/command — purpose, read-only|write>.
An unlisted read or connection is an incident: stop, record the read and copy location, and ASK.
Declare each stub with `STUB: <tool>` and `FIXTURE: <tool> docs/fixtures/<tool>-<date>.txt`;
its answers use those bytes or a fixture derived by a named edit.
Secrets: none appear in chat, reports, git or terminals; report key names, byte lengths or sha256 prefixes.
Customer content stays on the box: report ids, counts and file names.

REASON: <one clause naming the manual act removed, defect fixed, decision informed or builder friction removed>.
TIER: <tier>. TIER-REASON: <one clause explaining why this effort fits>.
Gate: <in-lane cross-family gate REQUIRED | NOT REQUIRED — §F all not-engaged, one revert restores with no data loss>.
External review: <NOT required — class | REQUIRED — class and review record>.

PREREQUISITES: <none | dependency — seat creating it — command — check before the dependent step>.
A DSN-dependent step names its committed provisioning script, admin role and test role.

§F CLASSIFICATION: grants/roles/credentials — <not-engaged | engaged, review record>;
containment/egress — <not-engaged | engaged, review record>; external writes — <not-engaged | engaged, review record>;
column drop/alter — <not-engaged | engaged, review record>; customer data off-box — <not-engaged | engaged, review record>.

## The rules

<Rules in plain sentences with file:line. Cite rulings as docs/rulings.md <date> <heading>; do not quote the operator.>
Keep the chosen tier on its TIER line; only a STATUS writeback may repeat it.
Rewrite a brief after review; put review history and runbooks in the review record or issue.

## The change / The question / Legs

<Exact scope and numbered legs; include each applicable gate's command and artifact.>
1. RED: <failure at base and passing control>.
2. BREAK: <probes that try to evade the rule>.
3. Implement: <paths and commit prefix>.
4. Green: <checks and pasted exit lines>.
A gate leg this lane cannot run requires STOP before building; never report an unrun leg as absent.
For a provider-facing schema change, run a zero-spend acceptance call before spending.
For a runtime source-set change, run the built image and COPY-set closure test.
For a deploy-script change, trace each stack and guard state and run a harness over those states.
For an n8n release, run `scripts/rehearse-flow-sql.sh flows/<flow>.json` before the update;
paste PASS and commit `docs/rehearsals/<flow>-<blob>.txt`; HOSTS names the box read.
A deploy leg uses origin/main and proves its code diff from the reviewed sha is empty, excluding docs/ and STATUS.
A digest pin cites the source line. A log wait uses a literal read from a real log line.
For a design loop, read docs/design/CONTEXT-PACK.md first; name the estate palette and score the pinned verdicts.
For a review, freeze the artifact, name the reading fence and word cap, and supply the dry-run results.
For a walk, compare the prior render; name every permitted write and its REVERSAL with before/after proofs.
An unlisted walk write is an incident: reverse and verify it before attest.

USE: #<issue>
<!-- The architect or owner posts the USE leg as an issue comment headed USE-LEG. -->

## Pins / Verdict line / PASS rule

<Build/test pins or the review verdict form.>
Walks use `RESULT: PASS —`, `RESULT: FAIL —`, or `RESULT: FAIL-FIXED-PENDING — …; fixed by <ref>`.
An undecidable visual question says `RESULT: PASS — not visually decidable from the rendered surface; <checks>`.
A leg that cannot run says `NOT EXERCISABLE — <reason>`.

## Deliverables

0. A file called new has `git ls-files <path>` empty at the base sha.
1. Commits `<lane>:` with explicit paths; HANDOFF.md in the worktree root carries the diff summary,
   before/after suite exit lines, required gate RESULT, and `Removed behaviour` (list or none).
   HANDOFF.md carries a `TEST:` block with indented `COMMAND: <test command>`, `RED: exit <non-zero>` (fix only, before change), and `GREEN: exit 0` and, for a surface, `WALK: <walk close record or fresh screenshot under worktree>`; close refuses either missing block.
   COST line: `COST <lane>: model=<id> effort=<e> wall=<h:mm> rounds=<review rounds> spend≈$<usd or n/a (subscription)> saves≈<h/month or n/a>`.
   For a changed existing surface, cite the prior walk and compare before/after renders.
   For a spending lane, state what survives interruption without repeating completed spend.
   Commit artifacts as lane-specific paths under docs/. Never commit HANDOFF.md, BRIEF.md or flag files.
2. `touch <worktree>/HANDOFF-READY`, then signal the advisor handle read at launch with
   `orca terminal send --terminal <advisor handle> --enter --text 'LANE-SIGNAL <lane> | DONE | <one line, pushed sha>'`.
3. For a question unanswered by source, write ASK-ADVISOR in the worktree root and signal ASK.
   Signal before every approval request, blocker, question or finish; never stop silently.
   Accepted signal verbs: DONE, ASK, STOP, BLOCKED. No `$<digit>` in signal text; write arg 1 or field 2.
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
