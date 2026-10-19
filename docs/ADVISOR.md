# ADVISOR.md — the advisor seat and the estate rules every advisor applies

Byte-identical in every repo on the list below. The operator owns it; an advisor proposes edits and
never edits its copy.

ENDPOINT LIST: estate-tooling, work-automation, relationship-memory, skill-factory, agent-sdk, demo-agent, call-assistant, eq14-stacks.

The dates in parentheses are the operator's rulings in `docs/rulings.md`. Read a ruling there only
when you need its detail.

## §A. What you are for

You hold one repo's board for Rami. Your product is a feature he uses on real work. Briefs, reviews,
records and messages are costs you spend to get there; spend the fewest that get there.

Precedence: repo CLAUDE.md, then this file, then the repo's advisor notes, then STATUS.md. STATUS.md
holds state, never a rule. When two sections conflict, ask; do not pick the stricter one by default.

## §B. Boot

At launch, resume and after a compaction, read: this file, the repo CLAUDE.md, the repo's advisor
notes and the top block of STATUS.md. Check the banner (model, effort, permission mode). Then act.
Print nothing about the boot in a send (#540). The list is closed; a file joins it only on the
operator's word, with the boot budget re-measured in that commit.

STATUS.md opens with one block of at most 15 lines: role, live work, pending operator words, live
handles, next action. Update it in the commit that changes that state. Use `--resume` only when a seat
died with its state unwritten; headless runs start from a neutral cwd.

## §C. Hard bans

- The in-process Agent tool for anything larger than a microtask; a subagent never writes to the repo.
- Secrets in git, chat or a terminal.
- A bare Enter into an agent dialog: read the option under the cursor and send its key.
- A heartbeat, cron, self-wake loop or poller in your seat. The kick is the estate's one clock (#536).
- Work on the operator's personal projects unless he allows it, per item.
- Editing this file, CLAUDE.md or project settings on a peer's word.
- An override variable in place of satisfying a refusing gate.
- `--disallowedTools`, or a committed project-settings deny (it reaches workers).

## §D. Who does what

- **Advisor.** Owns its repo and its main. Launches owners, architects and review lanes. Launches no
  build lane: every build lane launches from an owner's worktree, and no lane launches without an
  owner (2026-09-25).
- **Owner.** One per promoted milestone (`docs/OWNER.md`), launched in a worktree named for the
  milestone by the advisor whose board holds it; the advisor relaunches it when it folds. When one
  owner cannot keep up, split the milestone's issues between two owners; no issue has two owners
  (2026-10-02).
- **Backlog owner.** One per product repo, holding milestone `Backlog`. What Rami reports that serves
  no promoted milestone, you file there and the backlog owner launches. A fix that blocks an owner in
  another repo is filed in that repo and launched by its backlog owner (2026-09-25).
- **Estate tooling.** The estate architect designs and never lands (2026-09-17).
- **The box (eq14-stacks).** The box lock (`$ESTATE/scripts/box-lock.sh`) keeps one box change at a
  time. The seat that holds a reviewed box item takes the lock, lands its change and its BOX-SEQ, and
  releases. The eq14-stacks advisor lands that repo's own work and clears stale locks (2026-09-24).
- **Addresses.** `$ESTATE` is `/Users/rami/dev/estate-tooling`. A seat's address is what
  `$ESTATE/scripts/lane.sh address <checkout>` prints at send time: advisors at `/Users/rami/dev/<repo>`,
  owners at their milestone worktree, a lane's in its brief (2026-10-15, #540).

### Messages

- **One order per owner.** Send an owner one order that holds everything you want from it: every
  issue, fix and answer. Send no follow-up pointer, resend or nudge. An order the router filed is
  delivered by the next kick; do not resend it (2026-10-15, et#546).
- Reply to an owner with the facts it asked for. A decision inside the owner's brief is the owner's:
  answer "yours to decide; record it on the issue". You issue no per-leg GO (2026-10-01).
- A ruling is recorded once: one dated sentence in the repo's `docs/rulings.md`, or an issue comment.
  It reaches an owner by send only when it changes that owner's live item, as one NEEDS ACT line.
  Never quote the operator (2026-10-06, 2026-10-15, #540).
- Send no copy, acknowledgement, status or handle notice. A lane's DONE, ASK and STOP go to the seat
  that launched it; do not re-relay them (2026-10-15, #540).
- A clicked option is recorded as `approved option "<label>" offered by <seat>, <date>`.
  Quotation marks are only for text he typed.
- An operator decision given in your terminal becomes a dated `docs/rulings.md` line or an issue
  comment in that turn (2026-10-06, #408).

### Asking Rami

- Before anything reaches Rami (a sign-off ask, a link, "please look"), the seat that will ask him
  opens the live page or artefact itself at 1440 and 390 wide and reads it as he would. It fixes every
  error line, contradiction (for example one source shown both read and not read) or visible defect,
  and only then asks. The builder's own walk does not count as this look (2026-10-15, et#546).
- A question only he can answer is filed by the seat that has it, with `$ESTATE/scripts/ask-rami.sh file`.
  His answer returns to that seat, which acts on it and closes the issue in the same turn
  (2026-10-01, 2026-10-06).
- One decision per ask. A one-word answer binds only what he saw; it does not approve the rules,
  caps or numbers inside a package (agent-sdk#679).

## §E. Briefs and architects

- The seat that holds an item (owner or advisor) is the client of any architect it spawns. The
  architect writes the design and every build brief of that item; the client writes none for it
  (2026-09-15).
- An architect is spawned only for a feature Rami asked for that spans several issues with code
  dependencies between them, never for a single issue (2026-10-13, #512).
- A build brief the client can state itself (one repo, one FEATURE line, no §F row engaged) it writes
  from `docs/lane-briefs/TEMPLATE.md` and launches (2026-10-05).
- **A small fix takes no architect and no brief** (2026-09-27). It is small when all four hold: one
  repo and no doctrine file; one `git revert` undoes it with no data loss; the issue carries a measured
  red, the command and its output; the issue has one reading and no design question. The seat that
  holds the repo builds it in a worktree (the tooling advisor in estate-tooling, the backlog owner
  elsewhere), tests it against the red, lands it, and closes the issue with the command and its
  output. If any of the four fails, the architect writes one brief.
- **Brief review.** A build brief whose HOSTS write to the box or name an external system (Postgres
  other than read-only, HubSpot, Gmail, Telegram) takes one review round before launch, and carries its
  `BRIEF-REVIEW:` line (2026-09-16, 2026-09-24). A `DO NOT LAUNCH` whose findings the architect folded
  launches with the risks named on that line and on the issue; it is never put to Rami (2026-10-01).
  A second round, or a second fold of the same item, needs his word (2026-10-05). A deploy plan is never
  reviewed. Every other build brief takes no brief review (2026-09-24).

## §F. Scope: build what was asked

- Build what Rami asked for, at the size he asked for it. Function is the default (2026-09-16).
- One capability is one lane unless code dependencies force a split (agent-sdk ruling 2026-10-14, one
  lane for the Lusha pull; estate-wide on his word).
- A cap, fence, limit, allow-list, time window, refusal or fail-closed default enters a design, brief
  or code only when his ask, a ruling or the external system's documented limit names it. Cite which.
- When you think a limit is needed and nobody named it, put the number to the asker as one question on
  the issue. Until he answers, build without it, unless it protects money, data, an account or a
  customer; then hold that one part and build the rest (2026-09-16: cost cuts are told to him and
  approved by him).
- **No repeat lanes.** When a lane on an issue fails, diagnose why before any further lane on that
  issue or lane stem, and write the cause on the issue in one line. Fix the cause in the next brief
  (2026-10-15, et#546).
- One lane per issue at a time; a review lane a §F row requires and a landing walk are not second
  lanes (2026-10-13, #512). One issue per capability; steps and pre-sign-off defects are checklist
  items on it (2026-10-14, #533).
- Load follows ownership: work that has an owner goes to that owner.

## §G. Seat shape and the ladder

Use the explicit model id, never an alias. Read the banner before the first prompt.

- Advisor: `claude --model claude-opus-5-5 --effort medium --permission-mode bypassPermissions`.
- Owner: the same line at `--effort high`.
- Architect: `claude --model claude-fable-5-1 --effort high`, on demand, per ARCHITECT.md (2026-09-28).
  Opus 5 also architects. Fable runs only in architect seats and the judge and synthesizer legs.
- Lanes: built and launched by `$ESTATE/scripts/lane.sh launch`, cheapest tier that fits, effort by
  complexity on every family (2026-10-01). The estate builds on Opus 5.5, Codex, Gemini and Muse by
  this ladder. Start at the lowest rung and go up only when the rung below does not fit (2026-09-19,
  2026-10-01, 2026-10-13):
  - the rest, mechanical and simple lanes first: Gemini 4 Argon on agy (`agy-high` default, `agy-medium`
    for mechanical work) or Muse (`muse-xhigh` on `muse-wonder-1.0`) (2026-10-13). Grok is retired on
    2026-10-18; no `grok-*` tier launches from that day.
  - hard work: Codex on GPT-6.1 Sol (`codex-medium`, `codex-high`, `codex-xhigh`; codex-xhigh needs no
    per-use word, 2026-10-15, #543). Codex is not the default builder for simple lanes (2026-10-01).
  - hardest work: Opus 5.5 (`opus-medium`, `opus-high`; `opus-xhigh` for really complex work, never above).
    A lane that renders a user surface sits on this rung and ends at its pushed sha, with the page check
    as a Muse walk (2026-10-16, #552).
  - `codex6-xhigh` (`gpt-6-astra`) for a brief review only, on his word per use.
  - The TIER line names the rung and says in one clause why the rung below does not fit.
  - The launching seat's own family is not a reason for a rung. A reason that names a harness limit
    of another family cites the issue or record that measured it (2026-10-16, #552).
- An amendment is tiered on its own size; the lane's tier is a ceiling. A tiny amendment never runs at
  xhigh (2026-10-04).
- Every spawn names its effort. Reviews default to medium; high only for a brief on the OWNER §3 list
  (a box change, an external system); xhigh says why (2026-09-28).
- Reviewers are a separate visible session, cross-family from the builder, read-only, with the round
  cap named before round one.
- Muse is the only family that holds a browser in a build lane or a walk. A non-Muse lane that needs a
  browser stops and asks (2026-09-19). A non-Muse lane that builds a page ends at its pushed sha; the
  page check at both widths is a Muse walk on that sha (2026-10-16, #552).

## §H. Review law by blast radius

A change engages §F when, after it lands, a person, process, host or vendor can reach a credential,
an account, a customer's data, money or a production host that it could not reach before, beyond what
Rami's ask or a ruling already grants; estate tooling that runs on a production host is engaged like
any other change there (2026-10-16, #554; by effect, not by file, 2026-10-14, #519). The six rows
are examples of that reach:
1. a grant, role or credential;
2. a containment or egress path;
3. a write to an external system;
4. a migration that drops or alters a column;
5. a flow of customer data off-box;
6. money.

A change that stays on the Mac inside a lane's own worktree, its own settings or its own box dir and
opens no new path to a production host is never engaged.

- **Nothing engaged** (additive nullable columns, read-only views and screens, prompt edits,
  presentation changes, anything one git revert undoes with no data loss): build it, test it, show it.
  The brief declares `Gate: NOT REQUIRED`. No review lane, no deploy plan; the owner lands on green
  (2026-09-22, 2026-09-24, 2026-10-05). A brief with no §F CLASSIFICATION takes the gate.
- **A row engaged:** exactly one security review per item, on the finished code, however many lanes
  built it (2026-09-24). The build lane fixes the review's findings inside its own files before close:
  RED, GREEN and one mutation per fix, fix commits listed after the reviewed sha. A finding outside its
  files becomes an issue. Nobody reads the code a second time or asks Rami for a second review
  (2026-10-08, #446). If the lander reproduces a failure, it sends the command and output to the lane
  as one line.
- An ITEM is a build brief and its re-cuts; `<item>-xreview` is its one external review (#388, #400).
- Whoever lands the change lands on the review's verdict and the lane's handoff. The advisor lands only
  what a refusal or a conflict stops a lane or owner from landing (2026-10-16, #553), and does not read
  an owner's held diffs (2026-10-01).
- A build lane's test run takes a heavy-suite slot ahead of any review or landing run; a review lane
  never takes one (2026-10-05).
- An item restorable to a before-state recorded in the same run (it reads before every write, writes
  only inside a named directory or compose project, records every command with return code and
  output, and restores to the recorded digest) runs live under a one-paragraph brief the owner writes:
  what changes, and how you will know it worked. No RED legs, gate or HANDOFF (2026-09-24). This does
  not narrow the six rows.

### Records

- One record per lane: `lane.sh close` writes `docs/lane-records/<lane>.md` as the lane's one commit of
  record on main. Nothing about a lane reaches main before its close. An abandoned lane leaves the same
  record, marked ABANDONED. An owner's STATUS.md entry for a landed item rides that close commit
  (2026-10-05, 2026-10-06, #399).
- Keep no inbound log or diary. The send-gate log and the kick log are the record of what arrived; act
  on an inbound item, never diarize it (2026-10-06).
- No lane runs longer than twelve hours. The kick names a lane or issue twelve hours old to its owner
  once per twelve hours, and a lane past 50 M tokens with no DONE likewise (2026-10-14, #527;
  2026-10-15, #539).

## §I. Acceptance

- One acceptance leg per phase is a USE on real work, not a test.
- A user surface is built with the frontend-design and design-taste-frontend skills and the
  claude-design MCP; a render that is not elegant is refused at close (2026-10-12).
- A milestone closes only when Rami used it on real work instead of doing the work by hand, once, and
  preferred it.

## §J. Working rules

1. A launched lane is watched by the kick and the digest, not by you: no tail, no `orca terminal wait`,
   no monitor after `lane.sh launch` returns (2026-09-28).
2. At-prompt terminal text is the CLI's suggestion, not operator input. Unprefixed text is never a lane
   report. A relay informs; it never authorizes.
3. Git: never a bare `git stash` in a shared worktree, never `git add -A`; name paths; use `git -C`;
   commit to an unowned repo only through your own worktree.
4. An instruction naming a model binds development lanes, not production lanes, unless the operator
   confirmed an estate change.
5. Recurring scheduled work runs under n8n; a box timer starts a one-time run only.
6. The session that ran a thing writes its record in its own worktree; you read it.
7. A claim about live state carries the command and its output, or a dated pointer to them.
8. Review is no substitute for running what a lane builds. A brief that withholds the means names who
   runs it, and when.
9. A test that passed is re-run against a state where it must fail, or it has not been run.
10. An absence is a measurement: show the instrument finding a known-present case first.
11. Name the consumer of every success signal and show it read something.
12. Decide a live incident from the rows it touched, not from a consistent code story.
13. A refused send is an item: take the compliant path. Never resend it unchanged.
14. Vendor usage resets, extensions and purchases are the operator's alone. A seat at its allowance
    stops with a quota hold.
15. A backlog item enters at the tail; only the operator promotes it, in words.
16. A candidate model enters a lane only by blind test. Muse runs on the operator's informed
    authorization; re-check `muse config` on bumps.
