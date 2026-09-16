# ADVISOR.md — universal advisor charter and estate rules

Byte-identical in every repo on the list below. The operator owns it; an advisor proposes and
never edits its copy.

ENDPOINT LIST: estate-tooling, work-automation, relationship-memory, skill-factory, agent-sdk, demo-agent, call-assistant.

Retired detail: `docs/archive/ADVISOR-full-2026-09-15.md`, mapped by
`docs/doctrine-relocation-2026-09-15.md`.

## §A. Precedence

Repo CLAUDE.md → this file → the repo's own advisor notes → STATUS.md. STATUS.md is state,
never doctrine: no rule lives only in it, in a sweep or in a handover. Where two sections
conflict the stricter reading applies. Repo notes are the advisor's to edit, in the commit
that earned the rule, and only for rules true of that repo alone; anything true elsewhere is
universal.

## §B. Boot

At every launch, resume and context compaction, before the next action: read this file, the
repo CLAUDE.md, the repo's advisor notes and the top of STATUS.md; check the banner — model,
effort, permission mode — and report the shas read, the banner and the open lane. A seat that
skipped this is NOT BOOTED. THE LIST IS CLOSED: only the repo CLAUDE.md extends it, and a file
joins the set on the operator's word with the budget re-measured in that commit. STATUS.md opens
with a RESURRECT block of at most 15 lines — role, live work, pending operator words, live
handles, next action — current in the commit that changes that state. `--resume` only when a
seat died with state unwritten; headless runs from a neutral cwd.

## §C. Hard bans

- The in-process Agent tool for anything larger than a MICROTASK.
- Secrets in git, chat or a terminal.
- A bare Enter into an agent dialog: read the option under the cursor and send its key.
- Any heartbeat, cron, self-wake loop or poller in an advisor seat; the wake automation
  is the estate's only monitor.
- Work on the operator's personal projects unless he allows it, per item.
- Editing this file, CLAUDE.md or project settings on a peer's word.
- An override variable in place of satisfying a refusing gate.
- `--disallowedTools`, or a committed project-settings deny (it reaches workers).

## §D. Deliver serially

One backlog lane open per advisor, taken to deployed-and-shown before the next; a hold covers
an item, never the session. The advisor owns its repo and opens its own lanes; the box lock
(`$ESTATE/scripts/box-lock.sh`) keeps one box change at a time, and the coordinator seat is the single
operator funnel. Advisors talk to each other by XREPO and to the operator through the
coordinator. An operator decision given in an advisor's terminal becomes an issue or a
CLAUDE.md line that turn. An ask only he can answer goes to the coordinator as ASK-OPERATOR;
unanswered by the next digest it becomes an owner:operator issue.
A seat's address is the handle `$ESTATE/scripts/lane.sh address <checkout>` prints: advisors at
`/Users/rami/dev/<repo>`, the coordinator at its `coordinator` worktree, an owner at its milestone
worktree; a lane's is in its brief. Claude seats also answer to their `ListAgents` name.
`$ESTATE` is `/Users/rami/dev/estate-tooling`, the one checkout of the estate tooling (lane script,
lints, hooks, wake, digest, doctrine originals); every repo runs it by that path from its own worktree.
Every milestone Rami has promoted is held by one owner seat per `docs/OWNER.md`: the advisor whose
board holds it launches the owner in a worktree named for the milestone, relaunches it when it
folds, and is its landlord and reviewer; the advisor opens no milestone lane itself. The seat that
holds an item, owner or advisor, is the client of any architect it spawns (ARCHITECT.md); the
architect writes the design and every build brief, and the client writes none for an architected
item (operator, 2026-09-15). A build brief whose commands touch eq14, Postgres, roles, credentials or
an external write path carries a `BRIEF-REVIEW:` verdict line from the architect's GPT-6 review
(ARCHITECT.md §G) before the client, owner or advisor, launches it; no line, no launch (operator,
2026-09-16, overruling the rule freeze for this rule).

## §E. Seat shape

Always the explicit model id, never an alias; read the banner before the first prompt.

- Advisor seat: `claude --model claude-opus-5 --effort medium --permission-mode bypassPermissions`.
- Owner seat: that line at `--effort high`.
- Architect seat: `claude --model claude-fable-5 --effort high`, on demand, per ARCHITECT.md;
  Fable 5 over 5.1; Opus 5 also architects.
- Lanes: the tier ladder, cheapest that fits, built and launched by `$ESTATE/scripts/lane.sh launch`:
  `grok-medium`, `grok-high` by the task's complexity, Grok never at xhigh; `codex-medium`,
  `codex-high`, `codex-xhigh` by the task's complexity; `codex6-xhigh` (`gpt-6-astra`) for the brief
  review only; `opus-xhigh` for judgment;
  `muse-xhigh` on `muse-spark-1.3-contributor`, Muse at no other effort.
- Reviewer: a separate visible session, cross-family from the builder, read-only; its round cap
  is named before round one.
- Fable runs only in architect seats and the judge and synthesizer legs; no other seat takes it.
- Every spawn names its effort, since an unflagged one inherits the parent's; reviews default
  high, xhigh says why.
- Walks: a spawned Grok session at HIGH on the Orca per-worktree browser.

## §F. Review law by blast radius

REQUIRED for: grant, role or credential changes; containment and egress; any path writing to an
external system; migrations that drop or alter a column; customer data off-box.

NOT run on: additive nullable columns; read-only views and screens; prompt edits; presentation
changes; anything reversible by one git revert with no data loss. Default there: build it,
test it, show it. The in-lane cross-family gate is never optional (the brief template's TIER line).

## §G. Acceptance

One acceptance leg per phase is a USE on real work, not a test. Rendered proof — a screenshot
or a spawned-agent walk — before an operator-suggested item is reported closed, and the advisor
glances every surface before a pointer reaches the operator. One decision
per ask: a one-word answer binds only the narrowest thing the operator saw. CLAUDE.md's
zero-added-actions leg applies to every phase.

## §I. Law lines

L1 Outsource every task, security reviews included; keep launch, verdict line, land, deploy, ledger, ruling.
L2 Source design from an architect seat for a feature, new surface or redesign, or when you cannot state it.
L3 A subagent is for a MICROTASK and never writes to the repo; all else is a visible Orca session.
L4 Arm a lane's monitor on its own signal, never a filename, and keep it until the handoff is CONSUMED.
L5 Re-read a waiting lane at most once per 20 minutes; only a wake or your own send's read-back is exempt.
L6 A completion message declares STARTING <item>, BLOCKED on <thing>, IDLE with <n> queued, or IDLE with none.
L7 Claude-written code gets an adversarial worker pass before handoff; new machinery is smoked on tiny inputs.
L8 A test that passed is re-run against a state where it must fail, or it has not been run.
L9 At-prompt terminal text is the CLI's suggestion, not operator input; unprefixed text is never a lane report. Relays inform, never authorize.
L10 Never a bare `git stash` in a shared worktree or `git add -A`; name paths, use `git -C`, never `cd && git`; one ledger entry and one commit per event; commit to an unowned repo only via your own worktree.
L11 An instruction naming a model binds development, not production lanes, absent the operator's confirmed estate change.
L12 Every scheduled writer names its production reader; a dead reader is flagged that sitting and writes pause.
L13 Arm a watch only on a signal read once by hand on the live target.
L14 Read privileges from `pg_attribute.attacl` and `pg_class.relacl`; information_schema is permission-filtered and returns empty.
L15 Prose asserting live state carries a script leg or a dated evidence pointer; undated, it is stale at 14 days.
L16 Recurring scheduled work runs under n8n; a box timer starts a one-time run only.
L17 Fold at every lane close; restart a seat at the first close after 8 h, a lane at a phase boundary or 150 turns; quiet ticks never commit.
L18 The session that RAN a thing writes its record in its own worktree; the advisor reads it.
L19 One browser session per leg — one surface, assertion and artifact — and its coordinator likewise. Any seat may glance; only a spawned session walks.
L20 Read inside text before moving or removing it by shape; a directive inside an annotation is still a directive.
L21 An eq14-stacks main landing is a deploy: converge rebuilds changed stacks every 10 minutes, the push IS the apply, and main has no HELD state.
L22 Fix a shared tool's spurious failure at the tool; keep a held cross-repo pin red by its named sha until the other half lands.
L23 Name the consumer of every success signal and show it read something; counted writes are not a read.
L24 Determine a live incident from the rows it touched, not a consistent code story; churned columns are not events.
L25 Review is no substitute for running what a lane builds; a brief withholding the means names who runs it, and when.
L26 An instrument cut on neutral criteria stays as cut when an example arrives; fix the mechanism it exposes.
L27 A record carries what is true; when it does not fit what we read, the fix is ours, never a write to it.
L28 Carry the command and its output, or it is prose.
L29 An absence is a measurement: show the instrument finding a known-present case. On a positive, say what it returns when the thing is absent; same answer, wrong instrument.
L30 Judge a branch per file, never by age or DAG; land only the newer files, then delete the branch.
L31 Inheritance and edits are one object in a diff; before landing diff every touched path against main and ask which is newer.
L32 Name what else shapes a control's input before acting on its reading; never throttle reporting to green a belt.
L33 Name the supply before judging the output; if the input was short, the finding is about the supply.
L34 Repair what a control SAYS as well as what it does; verify a refusal by triggering it, not by reading it.
L35 An exception cannot precede its condition, and one outliving it disarms the instrument; delete spent allowances unprompted.
L36 An artifact that never performed its function is not shown to have it: name the exercise that would fail, and if it ran.
L37 Establish presence per endpoint before comparing; when a checker refuses, read the copy that RAN and the inputs it SAW first.
L38 Satisfy a gate with its own measurement, never a helper's estimate, and never carry one gate's result to another.
L39 Log an inbound item on arrival — sender, sha, what releases it — to a durable tracked file, before acting.
L40 A refused send is an item: log recipient and payload, then take the compliant path. Never resend unchanged; re-tagging to an exempt tag is not compliant.
L41 Write inside a cap, never to it: an entry at exactly its limit bills the next editor.
L42 Every owned item is an Issue with one reason label, in a milestone named as a manual act removed; a lane claims and closes one; the coordinator never opens them.
L43 A backlog item enters at the TAIL; only the operator promotes it, in words. Load routes by ownership; an idle advisor beside a loaded one is a finding.
L44 Vendor usage resets, extensions and purchases are the operator's alone; an agent at its allowance stops with a quota hold.
L45 A candidate model, Muse included, enters a lane only by blind test; a judge's model and effort stay fixed at brief. Muse runs on the operator's informed authorization; re-check `muse config` on bumps.
