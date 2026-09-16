# ADVISOR-ORIGINS-FORMAL.md — incident record behind the advisor doctrines

> **Record file, not doctrine.** The live rules are in the advisor charter. This file records the
> incident behind each rule: what happened, what it cost, and the rule it produced. It is not read
> at boot.
>
> **Form.** Every entry keeps the number it has always had, so an existing `(#N)` or `(#eN)`
> citation still resolves. Each entry states, in order: what happened, the measured cost, and the
> rule produced. Entries are neutral third-person statements of fact. Where the original record
> carried only a decision and no measured consequence, the entry says so rather than inventing one.
> Rewritten from `docs/ADVISOR-ORIGINS.md` on 2026-09-06 on operator order: quoted speech is
> removed from the record files, and incidents are reported as incidents.
>
> **Numbering is stable.** Entries keep their numbers when the charter is edited. A new charter rule
> appends a new entry here in the same commit.

---

## Rules with NO recorded origin — a standing debt register

Machine-readable. Each marker names a rule that IS IN FORCE and whose origin was never
written down. This is not a to-do list and clearing it is not urgent; it exists so the
absence stays VISIBLE.

Why it lives here rather than in the rule. Until 2026-09-11 rules 43 and 44 carried the
words "Attribution in ORIGINS" and there was nothing here to find — a claim that read as
sourced and was not. The operator then cut the per-rule ORIGINS reminders from ADVISOR.md
outright, which removed the false claim. That is an improvement and it is NOT a
resolution: with the claim gone, nothing anywhere recorded that those two rules have no
origin, and `doctrine-citations.py` reported a clean zero on a file that had simply
stopped asking the question. A lie became a silence. Raised by operator-sessions-76
against its own trim.

These markers are REPORTED by `doctrine-citations.py report`, never enforced. Writing a
real origin for one of these means deleting its marker in the same commit; a key must
never carry both a marker and an anchor.

<!-- no-origin: ADVISOR.md#43 -->
**ADVISOR.md rule 43 — a seat commits to a repository it does not own only through its own
worktree (2026-09-06).** In force. No incident record exists in this file. Searched
2026-09-11 by subject ("commits to a repositor", "repo it does not own", "own worktree")
and by number: nothing. Not fabricated, because a fabricated origin satisfies a checker
permanently and reads as sourced forever.

<!-- no-origin: ADVISOR.md#44 -->
**ADVISOR.md rule 44 — a pass that moves or removes text by its shape reads what is inside
it first (2026-09-06).** In force. The only mention of rule 44 in this file is a later
pass CITING it while applying it, which is not its origin. Same search, same result.

## Rule origins (#1–#97)

### #1 — Replacement constraint reintroduced the defect it replaced (2026-08-13)
**What happened:** In migration 070, `ON DELETE SET NULL` conflicted with a CHECK constraint that
required the FK pointers, so `DELETE FROM pkms_documents` raised a check violation from inside the
FK's own UPDATE and the R-DOC-3 hard delete was impossible. The replacement constraint,
`chunk_id IS NULL OR document_id IS NOT NULL`, failed identically, because the two SET NULLs are
separate row updates with an incoherent intermediate state. Assertion A6, written minutes earlier
for the first defect, refused the migration on the second. The same shape had occurred at migration
066 round 3, where the round-2 fix reintroduced round-1's nullable-operand hole.
**Cost:** two consecutive fixes contained the defect they fixed; no separate figure recorded.
**Rule produced:** run the new assertion against the fix before believing the fix; a constraint that
cannot survive its own table's delete path is a delete path that does not work.

### #2 — Name-based role universes refuted twice (2026-08-13)
**What happened:** In migration 070 review round 1, two drafts of a privilege sweep selected
principals by name pattern and by a hand-written array. Both were refuted the same way: a NOLOGIN
role created later, reachable by `SET ROLE` from a login role, matches no pattern and appears in no
list.
**Cost:** two drafts refuted in one review round; no separate figure recorded.
**Rule produced:** compute the role universe — enumerate LOGIN principals from `pg_roles` and
traverse each one's `SET`-reachable set — and state the exclusion that cannot be avoided, since a
superuser can always `SET ROLE` to the owner.

### #3 — A parser degraded on punctuation and discarded the lane's only finding (2026-08-13)
**What happened:** On the corroboration lane's first live tick (execution 121476), passages were
labelled `[5]` in the prompt, the model returned `[5]` as the passage value, `Number("[5]")` is NaN,
and five verdicts degraded to a not-found result — including the one CONFLICT the lane existed to
produce (canon 287, a claim of 800+ out-of-the-box native connectors against a customer's figure of
more than 1000).
**Cost:** five degraded verdicts on the first live tick, including the lane's only true finding.
**Rule produced:** a degrade-on-doubt parser must doubt the model's judgement, not its punctuation —
parse leniently, judge strictly. In a lane whose product is meaningful negatives, a false negative
renders identically to an honest one.

### #4 — An omitted list item was treated as an exception and discarded a pool (2026-08-28)
**What happened:** In the rank-ab-cycle lane, executions 246559–248688, five hourly ticks lost their
WA ranks because a model returned one fewer object than the ids supplied and the omission was thrown
rather than recorded.
**Cost:** five hourly ticks lost their ranks.
**Rule produced:** an omitted required list item is data, not an exception — retry once naming the
omitted ids, then score what came back and count the drop. Never throw for omissions; malformed JSON
and transport errors still throw.

### #5 — 774 green tests and a clean external verdict did not catch the first live defect (2026-08-13)
**What happened:** 774 tests passed and the migration carried a zero-BLOCKING external verdict, and
the corroboration lane still discarded its best finding on the first real input. Every real finding
that day — the parse degrade and the staleness inversion — came from first contact with live data;
none came from a review round. The lane's most useful output, a list of stale sales collateral, was
something it was never built to find.
**Cost:** 774 passing tests and one external review round produced no finding that the first live
tick did not.
**Rule produced:** the first live tick is not optional and green suites do not substitute for it;
when the choice is another review round or one real run, the real run goes first.

### #6 — Five conflicts were framed backwards because authorship was read as authority (2026-08-13)
**What happened:** The corroboration lane's first real run returned five conflicts and framed every
one as the authored document correcting the customer. The operator read all five the other way:
1,000+ connectors against a deck saying 800+; 1,000+ employees against 155+; a US headquarters
against Gurgaon; 120+ UI components against 70+; iframe embedding supported alongside the SDKs
against a deck listing only the SDKs. The document was the stale side five times out of five,
including a deck dated 2026-04.
**Cost:** five conflict verdicts inverted; the corpus's staleness was invisible to the lane.
**Rule produced:** authorship is not currency. A conflict is worded as a disagreement, never as a
correction; per-source staleness is recorded where re-ingest cannot erase it (the include list, not
the row); the operator is the tiebreak. The most valuable output of this pass class may be a list of
stale sales collateral rather than a list of misinformed customers.

### #7 — Ranking hid the passage that settled the question (2026-08-13)
**What happened:** Against a live corpus of 91 chunks, `word_similarity` peaked at 0.264 for the
connector-count claim and never surfaced the passage stating 1000+ pre-built connectors; `ts_rank_cd`
ranked that passage 4th, behind chunks that merely repeat the company name. Every claim in the corpus
is about the same company, so the name was noise and both rankers rode it.
**Cost:** the settling passage was never retrieved; the miss rendered as a not-found result.
**Rule produced:** measure retrieval before trusting it. When the corpus fits one context, send it
whole behind a cached prefix and cap the size with a loud refusal rather than ranking badly.

### #8 — A plausible cause survived until an execution count refuted it
**What happened:** On the dispatcher night, a racing-consumers hypothesis was carried until an
execution count of zero killed it; the real cause, a stale activation snapshot, was read out of
execution-embedded code.
**Cost:** no measured cost recorded.
**Rule produced:** evidence before theory — no fix ships on a plausible story; the hypothesis dies
or survives on runtime data first.

### #9 — Hardening changes had no failing-side test
**What happened:** Hardening work was verified by tests whose pass condition is a denial:
`Permission denied (publickey)` after disabling password auth; connection-refused on
`http://eq14:5678` after loopback binding; an sftp-only refusal from the clamped backup key.
**Cost:** no measured cost recorded.
**Rule produced:** refusal as success — a hardening plan without its denial test is unfinished.

### #10 — Declining to open a surface was not recorded as a deliverable
**What happened:** Several decisions closed surfaces rather than opening them: zero-ingress
`getUpdates` chosen over a webhook or Funnel; the database bound loopback-only behind
ssh-then-docker-exec; an unreviewed `authorized_keys` entry removed.
**Cost:** no measured cost recorded.
**Rule produced:** outbound-only posture — declining to open a surface is a deliverable, and a plan
states what it refused to open.

### #11 — A fast path risked becoming a second state machine (2026-08-23)
**What happened:** Ledger 90 records that the Draft reply and Regenerate paths carried a ten-minute
schedule wait; an internal wake was added as a second trigger without forking compose logic or
weakening the dashboard's serve-only auth boundary.
**Cost:** no measured cost recorded.
**Rule produced:** a fast path wakes the existing state machine; it does not become a second one.
Persist the request before the best-effort wake, keep the schedule as the retry belt, and claim
atomically in the shared picker, clearing by claimed request identity so a newer tap cannot be erased
by an older completion. An internal webhook stays disabled in config until reachability is proven
from the real caller container, and its network must not create a reverse bypass into that caller.

### #12 — An assertion block grew to ~180 lines across four external review rounds (2026-08-09)
**What happened:** Migration 045 took four external review rounds, each finding what the previous fix
could not catch; two of the findings were defects introduced by the round before. The in-migration
assertion block reached about 180 lines guarding two chat-turn tables. Every finding from rounds 2–4
required an actor who could already GRANT roles — an actor who can also DROP the tables. The
migration was split: 045 kept the what-it-did assertions, and
`schema/checks/chatgpt_lane_privileges.sql` plus `scripts/check-lane-grants.sh` carry the rest and
re-run after any role change.
**Cost:** four external review rounds on one migration; two findings were introduced by the previous
round; ~180 lines of assertion guarding two tables.
**Rule produced:** a migration asserts what it did; a suite asserts what is true now. For each
assertion, ask whether a command tomorrow could falsify it without touching this file; if so, it
belongs in a re-runnable check.

### #13 — A migration asserted two false guarantees and committed green (2026-08-09)
**What happened:** Migration 045 declared that DELETE was granted to no role while the applying
superuser owned the tables and nothing asserted ownership, and declared `opened_at` not writable
while granting table-wide INSERT, which made it settable at insert time. Seven dry runs, two of them
reaching the ACL sweeps, passed the broken version; an external round caught both. The same shape
appeared in the n8n `disabledTools` finding: a committed claim about a protection that was never
checked against the protection.
**Cost:** seven dry runs passed a migration with two false header guarantees.
**Rule produced:** an in-migration assertion is a claim about a surface and needs checking against
the surface. For each guarantee in the header, name the line that would fail if it were violated, and
make that line fail once.

### #14 — A ten-case control suite reported ten passes with zero assertions reached
**What happened:** A ten-case control suite reported ten passes while every case died on
`permission denied for schema public` before reaching a single assertion. Separately, the
profile-lock test of 2026-08-08 passed only because deterministic container pid numbering made the
recorded pid exist in both containers.
**Cost:** ten reported passes with no assertion executed.
**Rule produced:** a control that cannot fail is not a control, and a harness scoring the existence
of an error is not scoring the control — negative controls assert the identity of the failure.

### #15 — Committed configuration diverged from running configuration, four times
**What happened:** Four recorded cases: the stale activation snapshot; a box container predating the
committed `TELEGRAM_CHAT_ID`; the `errorWorkflow` wiring silently stripped by every API deploy until
a silent failure exposed it; and `docker compose restart` carrying the container's birth environment,
so an env-file change applied only on an `up -d` recreate and a newly written setup-token stayed
invisible through a restart.
**Cost:** four incidents, one of them a silent failure of the error-notification path.
**Rule produced:** config-in-git is not config-running — verify execution snapshots, in-container
`printenv` and database rows, never what is committed.

### #16 — A misdiagnosed failure was repaired with an unreviewed SSH key
**What happened:** A power cut caused a transient network failure. It was diagnosed remotely and
repaired by a parallel chat that synced an SSH key nobody reviewed, without the live failure being
re-observed.
**Cost:** no measured cost recorded; an unreviewed credential change entered the system.
**Rule produced:** re-observe the live failure before repairing it — a fix for a misdiagnosed problem
is itself a regression.

### #17 — Remembered behaviour was wrong at source, repeatedly
**What happened:** On night one, an agent penciled the container image `n8nio/n8n:1.80.0` from stale
training memory; the at-source check showed the stable line was 2.28.5, a full major ahead, so the
spine would have been born on a dead branch. Later cases: Fireflies documentation-versus-API drift (a
documented filter returned 400 live; `mine:true` scoping); the SDK gates (`maxBudgetUsd` exists,
`ANTHROPIC_API_KEY` silently outranks the OAuth token, bare mode skips OAuth); the dashboard identity
pin, where the assumed Google login was wrong and a header probe showed the tailnet uses GitHub login
as `Cipher-DLRT@github` (fail-closed design made the wrong guess deny-only until the probe corrected
it); and n8n branch order, where R1 wired its detection branch first in the fan-out and it ran last,
silently reading the state it was meant to diff against. The installed 2.28.5 sorts ready branches by
canvas position (`position[1]` descending onto a LIFO stack, so smallest y runs first); the
connections array decides nothing.
**Cost:** one image pin that would have started the estate on a dead branch; one silent detection
branch reading post-change state.
**Rule produced:** verify at source — installed version, live API, official documentation. Remembered
behaviour is not evidence.

### #18 — A defect closed at the data layer reappeared at the narrative layer
**What happened:** D1 closed the Paper Win trap at the data layer by resolving `closedlost` against
the portal's label map. D5 then told the narrative that the label was the commercial truth, and the
model, reading a stage named for a win, described a deal at probability 0.90 as commercially won,
against the CRM record. The original fix never failed; the same misreading found a surface no
label-resolution check could see.
**Cost:** one incorrect commercial claim generated about a live deal.
**Rule produced:** a fix at one layer can push the failure up a layer — when a defect is closed at the
data layer, ask where else the same misreading can be made and put a deterministic pass at the new
layer, judged against the record it was built from.

### #19 — A single-account canary passed and the estate pass produced eight false positives
**What happened:** In R0, the FP canary was clean and caught a real formatting defect. The estate
pass then produced eight false positives, all of them true statements, living in the three states the
canary account did not occupy: deals the CRM calls closed, deals genuinely Closed Won, and the negated
phrasings the model uses when a deal is neither. The estate rendered twice.
**Cost:** eight false positives; one full estate re-render, which is the cost the canary existed to
avoid.
**Rule produced:** a canary must span the states a check keys on, not one instance; and replay a fixed
rule offline over already-captured real outputs before paying for a second live pass.

### #20 — A guard aimed at the wrong field stripped true statements
**What happened:** In R0, won-language gated on `hs_is_closed_won` is the correct ruling. The same
gate applied to closed-language stripped a correct statement that a deal is closed but not won, from a
deal whose `hs_is_closed` is true.
**Cost:** true statements removed by a control built to remove false ones.
**Rule produced:** a guard gated on the wrong field fails in the direction it was not watching — judge
each claim against the field that decides that claim.

### #21 — A correct observation was recorded with a guessed mechanism
**What happened:** The D4 note recorded n8n branch behaviour as connection-order execution. The
observation was true and the mechanism was wrong (see #17); its render leg was also the lowest lane,
so both readings fit, and the coincidence held until R1 leaned on the wrong one. The resulting failure
was invisible because every node reported success.
**Cost:** one silent detection failure inherited from the guessed mechanism.
**Rule produced:** a correct observation with a guessed mechanism is a trap, not evidence — when an
ordering, timing or dedup works, record why from the source.

### #22 — Draft-first was enforced by prompt text rather than by credentials
**What happened:** The Konnect work showed the human gate catching what every automated filter missed.
The structural form of the control is that the drafting component holds no delivery credential: the
agent has no Telegram and no Brain credential, and n8n delivers only after a tap.
**Cost:** no measured cost recorded.
**Rule produced:** draft-first is structural, not policy — the component that drafts must lack the
credential to deliver; a prompt-level instruction not to send is not draft-first.

### #23 — Approval defined as an authority boundary (operator rider, 2026-08-25)
**What happened:** The operator issued a rider defining inline approval as a database authority
boundary rather than a conversational promise.
**Cost:** no measured cost recorded; the rider is preventive.
**Rule produced:** agent write tools may only INSERT a request row and return pending, with no
external call in their implementation. The agent role cannot update approval fields; the dashboard
button alone captures approval; the execution rail reads approved rows only; the card renders
destination and payload from the row, not from chat. Approval captures the row's payload hash at click
time, any later payload change makes the row ineligible, and a mutation test must prove that removing
the equality guard would fail the suite.

### #24 — Model lanes routed by reader (operator order 2026-08-31)
**What happened:** Model lanes were set by who reads the output: machine-read lanes to GPT-5.6 Luna
with a Haiku 4.5 fallback, operator-read lanes to Sonnet, and customer-facing lanes to Opus 5 on the
operator's 2026-08-31 order, at the same $5/$25 rate as Opus 4.8. (For the later scope correction on
that order, see #e22.)
**Cost:** no measured cost recorded at the time of the ruling.
**Rule produced:** route by reader. A lane changes only on recorded evidence or an explicit operator
call — never silently, never upward by default.

### #25 — A spawned debug session inherited the parent model despite an explicit override (2026-08-16)
**What happened:** The chatgpt-bridge debug launch came up on Fable from inside a Fable advisor
session despite an explicit Opus override. The operator found it in his session list; the launcher did
not. The mechanism is that the catch-all subagent type inherits the launcher's model and silently
ignores a model override.
**Cost:** one session run on the wrong, more expensive model; detection was by the operator, not the
system.
**Rule produced:** spawned sessions route like lanes — Opus or codex by default, Fable only with
per-instance operator approval. Use a subagent type that honors the override and verify what actually
came up. Whether a launch counts as top criticality is the operator's call per launch, never the
launcher's inference.

### #26 — Assertions passed on state that predated the run, three times
**What happened:** Three cases of the same shape, asserting that a state exists rather than that a
transition occurred: the containment sweep expanded in the outer shell, so empty patterns produced a
vacuous pass; the same sweep then matched its own scan-transient process; and the fold-I denial test
passed on a stale `example.com` row until it was keyed to a per-run unique host.
**Cost:** three assertions that could not fail.
**Rule produced:** a test a stale artifact can pass is vacuous — assert a fresh, run-keyed transition,
keyed to a per-run token (unique host, nonce path, random sentinel, fresh session).

### #27 — A pinned absence pinned the wrong default, twice
**What happened:** Two surfaces, one root cause. In A8's skills discovery and then in T0, a design, an
inventory whose header claimed every line was read from source, and a suite pin all stated that
omitting `settingSources` prevented settings files from widening the tool surface. The SDK
documentation states the opposite: when the option is omitted, all sources are loaded. The pin
asserting the absence would have held the defect in place. External review caught it.
**Cost:** two surfaces carrying the same wrong default; one suite pin that would have preserved it.
**Rule produced:** a library option's default is a fact to read at source, and a test that pins an
absence pins whatever the default happens to be — pin the explicit value.

### #28 — A tranche closed 8/8 PASS with a declared leg absent
**What happened:** In P2 hardening, `session-lane-p2-hardening.md:277-279` declared a keyed write and
a keyed read outside the workspace, both to be denied. `session-p2-acceptance.md` carried legs 1–8 and
closed 8/8 PASS with that leg absent. A later session's inventory found the gap; the close did not.
**Cost:** one tranche closed complete with a declared acceptance leg never executed.
**Rule produced:** an acceptance checklist enumerates every leg its design declares; before a tranche
closes, diff declared legs against executed legs. A leg not run is an explicit deviation, never a
silent absence.

### #29 — Two capability probes passed against a dead injection path
**What happened:** In A8's recovery leg, two skill-visibility probes passed on a model copying staged
directory names into its answer, while skills injection had been silently dead since B2. One check of
the init message exposed it.
**Cost:** two probes reported a capability that had not worked since B2.
**Rule produced:** model self-report is not verification — probe ground truth against the harness's own
record (init roster, telemetry rows, database state).

### #30 — Two closing summaries asserted state that had not been re-read
**What happened:** Two claims on the same day, both caught by the operator rather than by the system: a
statement that another ping was inbound when deduplication meant none would come, and a statement that
a probe was awaiting his tap when it had already been tapped and was green. Neither status was re-read
before the claim.
**Cost:** two false state claims in one day, both surfaced by the operator.
**Rule produced:** a summary states only what was verified this turn; carried-forward or predicted
state is labelled as such, and the closing report re-reads live state before asserting it.

### #31 — A blanket stage committed a foreign file unseen
**What happened:** A Codex CLI import dropped a mutated CLAUDE.md fork at the repository root as
`AGENTS.md`, and a blanket `git add -A` committed it unseen. The companion origin is the dispatcher
incident and the dead UI-import ritual, where in-place edits left stale snapshots executing.
**Cost:** one unreviewed forked instruction file committed to the repository root.
**Rule produced:** one writer per workstream — every table and flow has exactly one writing path,
deploys go only through the sanctioned update path, and any host-touching change lands in STATUS and
the owning repo in the same sitting. Staging is explicit paths only; never `git add -A`; flag an
unknown root file before the commit.

### #32 — Three CRITICALs were raised against evidence already read
**What happened:** In the FP dossier experiment, a verifier raised three false CRITICALs against emails
that had already been read verbatim, because its absence-of-evidence claim was scoped to the retrieval
method that produced it.
**Cost:** three false CRITICALs.
**Rule produced:** verifier CRITICALs are claims to check, not instructions — a search finding nothing
is not proof that a thing does not exist. Give verifiers the primary artifact, not only a search tool.

### #33 — Three weeks of green gates produced nothing the operator used (18 July – 7 August 2026)
**What happened:** Between 18 July and 7 August 2026, 432 tests passed and eight acceptance legs were
green, while zero artifacts reached the operator's actual workday. Every gate in that window graded the
machine against a fixture the project had authored itself.
**Cost:** 432 passing tests, eight green acceptance legs, zero artifacts in use.
**Rule produced:** correctness is not usefulness. At least one acceptance leg per phase is a use on real
work — the operator used it instead of doing the work by hand, once, and preferred it — not a test.

### #34 — A named quantity went unmeasured for 90 minutes (2026-08-07), and elapsed time twice more
**What happened:** On the Granola 429 night, 2026-08-07, six failed ticks were audited for header
shape, transport, IP family, WAF rules, credential staleness and provider defects across 90 minutes,
while the request count named in the error was never computed. A removed cursor node let a 118-item
output feed an HTTP node that runs once per item, so every tick burst about 118 calls into a
25-request bucket. The operator's plain reading, that the rate limit was being exceeded, was correct.
Second case, 2026-08-13: a diagnosis that the scheduler was dead for about 18 minutes instance-wide was
built on execution timestamps compared against an assumed wall clock, and was followed by a production
n8n restart that killed three mid-run executions; `date -u` afterwards showed the real gap was 71
seconds, one tick boundary of healthy flows. Third case, 2026-08-15: an eight-hour wedged bridge worker
(defect 16) dissolved against the jobs ledger — the job said to have been accepted at 23:24Z was created
at 07:25Z when epoch-anchored, and ran clean in 8 minutes; the receiving session had also recorded a
claimed 23:12Z resume time without measuring it.
**Cost:** 90 minutes of misdirected diagnosis and a ~118-call-per-tick multiplier; three mid-run
executions killed by an unnecessary restart on a 71-second gap; one eight-hour defect that did not exist.
**Rule produced:** when an error names a quantity, count the quantity first. Elapsed time is a quantity
too and the clock is its source: anchor every cross-session timestamp to an artifact epoch instead of
comparing against a guessed now(). Structural sibling: every paid or external HTTP node is executeOnce
or provably fed by a single-item node, suite-pinned.

### #35 — A circuit breaker ordered attempts by a mutable column (2026-08-19)
**What happened:** In the Knowledge-backup pre-deploy state review, the initial breaker read
`answer_jobs.updated_at`. The existing Opus, card and wording-verdict transitions all advance that
column, so ordering by it could make an older success appear newer than two consecutive failures and
reopen an unhealthy endpoint. The landed implementation stamps `submitted_at`, and only that immutable
attempt time drives the two-failure, 30-minute window.
**Cost:** caught in review before deploy; no live cost recorded.
**Rule produced:** a circuit breaker orders attempts by an immutable attempt timestamp, never a row's
generic `updated_at`; suite-pin both the write and the read.

### #36 — A retry window recomputed from a moving cursor could drop old work (2026-08-25)
**What happened:** Guide entry 14 records that the mapped-channel action backfill recalculated its
seven-day window from the advancing extraction cursor, so a failed old thread fetch could disappear on
the next tick.
**Cost:** no measured loss recorded; the defect was corrected before it dropped work.
**Rule produced:** a retry whose scope derives from a moving cursor persists its original horizon (or
the remaining keys) until completion. A historical-only failure need not stall current ingestion, but it
must retain a durable retry scope.

### #37 — A grant chain passed every atom probe and failed the first real statement (2026-08-11)
**What happened:** In item E, update 609704928, the operator's first real message failed with SQLSTATE
42501 on a statement that had never once executed as the `telegram_bridge` role. Leg-1 probes injected
inbox rows under another role; leg 2's evidence was the offset UPDATE, a different statement; leg 3's
zero-duplicate result was vacuously true because no insert ever landed; and migration 044's
`has_column_privilege(...,'INSERT')` assertions passed throughout. Migration 046 now executes the
production statement under `SET ROLE` at apply time.
**Cost:** the operator's first real inbound message was lost to a permission error that four legs of
probing had greened.
**Rule produced:** a grant is verified by running the production statement as the production role.
`has_*_privilege` checks atoms; statements require sets — `INSERT ... ON CONFLICT` needs SELECT on the
arbiter column. A hop declared unprobeable still gets its statement-level half probed.

### #38 — A migration's own DO block failed on the live role graph after four review rounds (2026-08-22)
**What happened:** In customer-layer T0, migration 107's first DO block raised an ambiguous column
reference and the standing check false-positived against the live role graph. Suite 1072 was green and
four Opus review rounds — three product, one grants — had passed both. Neither the suites nor the
reviews execute PL/pgSQL or see group memberships, such as `pkms_dashboard` holding table-wide SELECT on
`accounts` reachable only from `dashboard_app`.
**Cost:** a green 1072-test suite and four review rounds passed two defects that the first execution
found.
**Rule produced:** the rollback dry-run runs against the real role graph and executes every DO block, and
it belongs before the grants review. Apply the files in order in one transaction (strip BEGIN/COMMIT,
reset `search_path` between them, `ON_ERROR_ROLLBACK on`), run the standing checks, run every changed
generated statement under its role, ROLLBACK, then assert the objects are gone. Build the file with
`printf`, never zsh `echo`, because `\e` mangles `\echo` and swallows the next statement, ROLLBACK
included.

### #39 — An empty item passed a zero-row gate and pinged every minute (2026-08-12)
**What happened:** In the arr-165 barrage (execution 118460), the node `PG · fanout error mark` carried
`alwaysOutputData`, contradicting its own design comment that a clean pass emits zero items. n8n's
zero-row Postgres result ends the chain, which the CTE-gated ping pattern depends on; the option converted
it into one empty item, so the send ran with empty content, every dedup tick failed on the provider's 400
for empty message text, and the error notifier pinged per minute. The plan's pre-observation hypothesis, a
stream-replacer text reach-back, was wrong: the text expression was fine and the gating was broken.
**Cost:** per-minute operator pings until the fix; suite-pinned 2026-08-13, and an estate sweep found the
class contained to that one node.
**Rule produced:** an empty item is not zero items — a node whose zero-row output gates a downstream send
must never carry `alwaysOutputData`. When adding the option to keep a chain alive, ask what the last node
does with an empty item.

### #40 — A permission error was classified as poison and the offset advanced past real work (2026-08-11)
**What happened:** In the same incident as #37, SQLSTATE 42501 was classed as poison, the offset advanced
past the operator's message, and the raw update was never persisted, so the content was unrecoverable.
**Cost:** one inbound operator message discarded and unrecoverable.
**Rule produced:** a poison classifier keys on the error's SQLSTATE class, never on the existence of an
error; skip-and-advance is for rows that can never commit (22xxx/23xxx), and a skipped update logs its
full payload.

### #41 — A date-pinned fixture failed the suite on a clean checkout (2026-08-11)
**What happened:** At the F7b boot, the R1 recent-changes tests pinned 2026-07-28 and 2026-07-30 fixtures
against a live 14-day window. The baseline suite failed the moment the clock passed the pin, with no code
change.
**Cost:** one suite red on a clean checkout, from time passing rather than from a defect.
**Rule produced:** a fixture pinned to a calendar date inside a `Date.now()` window is a test with an
expiry date — compute fixture timestamps relative to now.

### #42 — Fixtures built from the detail shape greened a list path that had no data
**What happened:** Granola list objects carry no attendees or calendar_event fields, which are
detail-only. Ingest-time correlation and the meeting-time floor both passed 549 tests against
detail-shaped fixtures and did nothing in production: execution 96043 processed 35 notes and produced
zero maps. The fix moved correlation behind a per-note enrich GET.
**Cost:** 549 passing tests over a production path that mapped 0 of 35 notes.
**Rule produced:** a fixture models the response shape verified at source for that call, never the
richest shape the API owns.

### #43 — A credential-layer failure bypassed the response options and killed the tick
**What happened:** On item C's first tick (execution 96242), a placeholder Gmail credential threw at the
OAuth signing layer, which `neverError` does not cover. The chain aborted after the email INSERT and the
hubspot_log draft never composed. A chain whose completion marker was the first insert would have
stranded the meeting half-composed permanently.
**Cost:** one tick killed after a partial write; a latent permanent-strand shape in the same chain.
**Rule produced:** `neverError` covers HTTP responses only — an outbound node whose failure is data needs
both `neverError` and `onError: 'continueRegularOutput'`, and its result recorder must read the error
shape as well as the response shape, suite-pinned. A multi-insert chain's re-pick predicate keys on the
last insert, so a mid-chain death re-picks.

### #44 — Two HTTP nodes silently bound to the wrong credential (2026-08-07)
**What happened:** In item F, both Granola HTTP nodes silently bound to the HubSpot header credential.
n8n auto-binds a name-only credential reference to an arbitrary same-type credential at create time, and
the deploy merge then preserves that wrong id on every update, because by-type resolution reads names from
nodes and an unbound new credential is invisible to it. The flow was inactive and the mis-binding was
caught by node-level verification.
**Cost:** none realised; had the flow been activated unverified, it would have sent the HubSpot token to a
third-party API.
**Rule produced:** a new credential's name must exist on the instance before its flow's first deploy.
Reserve the name with a placeholder credential holding no secret material, deploy once with the explicit
`--bind ctype:name=credential-id` form, verify node-level bindings from the live workflow, then prove
convergence with one plain git-truth update.

### #45 — Two RFP runs delivered 89 and 51 open items and saved no time (2026-08-07)
**What happened:** On the Dubai Police fixture, run 1 delivered 37 answered questions against 89 open
items and run 2 delivered 18 answered against 51. Both graded PASS on assembly, brand and compliance;
neither would have saved the operator an afternoon. The operator ruled the same day, on item B plan v2/v3,
that an open-item ceiling is the wrong instrument, because open items are normal and uncontrollable output
and rejecting a delivery for their count punishes honesty.
**Cost:** two green runs, 140 open items between them, no operator time saved.
**Rule produced:** a handover that returns a pile of questions has not done the work — a job is judged on
what the operator has left to do when it comes back. Enforcement is the closure loop, not a ceiling: open
items land as closable rows (`open_items`, migration 038), surface where the work lives, and close with a
recorded resolution that feeds the next regeneration. An item raised as a hedge where grounding could have
answered is still a prompt defect.

### #46 — A chat surface was hand-built across five sessions and an existing library already did it
**What happened:** The dashboard chat lane's markdown rendering, scroll behaviour and composer were
hand-built across five sessions. The library assistant-ui already did all of it, and was found by looking
at the result rather than by evaluating options before building. The same evaluation method correctly
rejected Open WebUI and LibreChat, which would have owned conversation state.
**Cost:** five sessions of hand-built work duplicating an existing library.
**Rule produced:** a general-purpose component is evaluated before it is hand-built, and the evaluation
belongs in the plan, not the build session. The test is ownership, not features: a library that renders,
parses or computes and hands the result back is a candidate; an application that would own state,
credentials or the deploy path is not. State adoption cost alongside the benefit.

### #47 — A skill's runtime dependencies were denied at the egress boundary (2026-08-11)
**What happened:** On job 33, the first live use-case job, `docx` was present in the image but
unresolvable, `validate.py` fetched Dublin Core XSDs at validation time, all three requests were denied,
and the fallback delivered a degraded document as a success. `NODE_PATH` had been scrubbed twice between
the container and the session, so an image-baked module was unusable.
**Cost:** one degraded document delivered as success; three denied requests on a first live job.
**Rule produced:** a skill or job that requires a runtime dependency names it, and the dependency lands in
the runner image in the same change. An egress denial originating from a skill is a missing-bake defect,
never an allowlist candidate. An image-baked module is usable only if every environment-allowlist hop
forwards its resolution path, and a library that resolves remote schemas fetches them at validation time,
so a bundle-and-pin must cover schema imports as well as packages.

### #48 — There was no answer to what an agent had actually loaded (2026-08-11)
**What happened:** In B8 the operator asked how he would know that an agent could see all the relevant
documents, calls, emails and Slack messages. The system had no answer anywhere; trust was the mechanism.
**Cost:** no measured cost recorded; the gap was in evidence, not in an incident.
**Rule produced:** an agent's context is stated, not assumed — every session and job carries a manifest of
what it loaded and what it did not, composed by one function with three consumers, with dates parsed from
the source's own header rather than invented, absences named, and the manifest verified against the
actually-staged workspace before the session runs.

### #49 — Context material was separated from response content (operator ruling 2026-08-11)
**What happened:** In B8 plan v3 the operator ruled that for customer-facing document types, situational
material may shape emphasis and tone but may never supply response content. Staged dossier, email and
Drive material is labelled CONTEXT-ONLY in the workspace and the manifest; content sources remain the
skill's knowledge and Brain.
**Cost:** no measured cost recorded.
**Rule produced:** context may shape emphasis and tone, never supply content. Stated honestly, this is
prompt-and-grading enforcement policed by the would-he-send-this bar, not a physical wall: the label and
the manifest make a breach gradeable, not impossible.

### #50 — Restriction level set to match a single-operator system (operator ruling 2026-08-11)
**What happened:** During the A2b session the operator ruled on calibration: this is a single-operator
personal system, not enterprise SaaS, and the default posture for the agent is unrestricted for
reversible, private operations.
**Cost:** no measured cost recorded.
**Rule produced:** controls exist at exactly four points — external sends and writes behind a draft-first
tap, credential custody, money, and one-writer state integrity. A plan proposing restriction beyond these
justifies itself against this ruling; over-securing is the defect, reviewed as such.

### #51 — Browser verification delegated, then moved off the advisor seat entirely (2026-08-11, 2026-08-24)
**What happened:** F8, on 2026-08-11, formalised a standing rule that dashboard-touching sessions spawn an
agent to verify rendered output in Chrome before close. It was rescoped on 2026-08-12 when adversarial
testing moved to codex, leaving the spawned agent responsible for rendered verification only. It was
broadened on 2026-08-24 by operator instruction, after browser tool output — screenshots and page reads —
consumed over half the advisor's context window in one day.
**Cost:** over half of one advisor's context window in a single day, spent on browser tool output.
**Rule produced:** the advisor session never drives the browser tools. Every browser check — rendered
verification, surface confirmation, defect reproduction — is delegated to a spawned session that reports
back as text. The obligation to verify a surface before instructing the operator is unchanged; only who
holds the controller moves.

### #52 — A page passed every functional pin and carried three design gaps (2026-08-11, 2026-08-16)
**What happened:** The A2c plan's standing ruling of 2026-08-11 established that dashboard-touching work is
verified against the rendered page rather than the served payload, because a route can return 200 while the
component throws, renders empty, or hides the state the change exists to show. The corollary was added on
2026-08-16 after Tranche G: an Opus walk passed 14 of 15 legs and the pin suite was green while three
fidelity gaps sat in plain view — the attendees line, the adjacency of meetings and commitments, and
non-flipping fold glyphs. They were found the next day when the operator asked for the designs to be
compared against the output.
**Cost:** 14/15 walk legs and a green pin suite over three visible fidelity defects, found by the operator.
**Rule produced:** verify against the rendered page, with screenshot evidence in the record; when the
browser is unavailable, say so plainly and put the rendered check on the operator's batched list rather than
skipping it. When the work implements an approved design, the rendered leg includes one design-versus-deployed
side-by-side per implemented page.

### #53 — Two identical route-edit 500s shipped green on the same day (2026-08-16)
**What happened:** Two incidents on 2026-08-16, both caught only by rendering. A route whose SQL had been
proved as superuser rather than as `dashboard_app` threw permission-denied live. A new overview query was
pushed into `Promise.all` but omitted from the destructuring, so the return referencing it threw an
undefined-name error and took down both the accounts overview and the digest. `node --check` caught neither,
because both are runtime rather than syntax defects, and the suite's regex pins matched both files. The
addendum, from migration 082, records the same property for a DO block's plpgsql: a DECLAREd `RECORD`
variable shadowed by a `pg_roles r` table alias made `r.oid` resolve to the record and raise a missing-field
error at apply, after parse checks and seven codex logic rounds had passed it. The surrounding transaction
under `ON_ERROR_STOP=1` caught it and rolled back clean.
**Cost:** two live 500s in one day, one of which took down two surfaces; one migration defect that survived
parse plus seven review rounds.
**Rule produced:** a route or server edit without an execution harness is unverified until the rendered
check, plus a syntax check and a reference-trace of any new destructuring. Apply every new DO block inside
its own transaction before trusting it, and keep table aliases away from DECLAREd record variables.

### #54 — A node inserted mid-chain broke every downstream read and the path had never run (2026-08-11/12)
**What happened:** In the F8 empty-batch incident, `PG · record slack access` was added late in the session
between the batch builder and the `IF · any batch?` gate. An n8n Postgres or HTTP node replaces the item
stream, so the gate tested `$json.no_batches` against UPDATE output where the key never exists. Every tick
after the first real channel mapping routed into the Anthropic node with no body, and the poller failed six
or more consecutive ticks (executions 113277–113522), pinging the operator each time. The extraction path
past the gate had never once run live: `messages_ingested` was still 0.
**Cost:** six or more consecutive failed ticks with an operator ping each; a gate path that had never
executed while its statement-level legs were green.
**Rule produced:** a Postgres or HTTP node replaces the item stream — a node added between a producer and its
consumers is checked against each downstream `$json` reference. The fix shape is a reach-back to the producer
for decisions, plus an expander node that re-materialises the producer's items where a per-item consumer
follows. A gate path the legs never drove live is wiring nobody has proven.

### #55 — A UTC-derived fixture failed nightly in a four-hour window (2026-08-12)
**What happened:** The R1 change-row pin derived the day via a bare UTC slice, which diverges from a
Dubai-rendering artifact between 00:00 and 04:00 local time. It failed the suite in exactly that window and
passed all day. It was caught live at about 00:0x on 2026-08-12, during the F8 incident fix — the first suite
run after midnight Dubai in the repository's history.
**Cost:** one nightly four-hour suite failure window, latent until the first post-midnight run.
**Rule produced:** a relative-date fixture computes its expected strings in the renderer's timezone, not UTC.

### #56 — A probe arranged fixtures in an order production never produces (2026-08-12)
**What happened:** Migration 058's apply probe inserted the `seen_transcripts` parent before the transcripts
child, and passed. The Fireflies flow runs the child insert on a meeting that is by definition unseen, since
mark-seen is deliberately last, so the FK the probe greened would have raised 23503 on every first extraction
and replayed forever. It was caught by tracing flow order before any real meeting hit it; migration 059
dropped the FK and re-modelled the probe parent-less.
**Cost:** none realised; the defect would have killed every first extraction.
**Rule produced:** a probe verifies the production order, not just the production statement — ask what the
production path guarantees exists when the statement runs, and whether the probe creates more than that.

### #57 — A leg fixture fed the live system mid-run (2026-08-12)
**What happened:** In the polish-session rendered legs, a fixture meeting dated 26 hours ago satisfied the
item C composer's pick, which selects ok, mapped, under seven days old and no draft. The live tick composed
junk approval drafts for a deleted account (outbound 10/11) and likely sent a Telegram card. Fixture dates
were moved to minus nine days and the drafts were deleted by exact count.
**Cost:** junk approval drafts composed for a deleted account and a probable operator card.
**Rule produced:** a live-table fixture is visible to every live consumer — check it against each live
picker's predicate and place it outside every picker's selection window.

### #58 — A heredoc script consumed its own lines over ssh stdin (2026-08-11)
**What happened:** In the F8 live legs, the first run was fed to `bash -s` over ssh stdin. Every heredoc
inside the script read from that same stdin, consuming the script's own later lines; the run died after leg
L1a, leaving three fixture rows and no coherent error. The identical script passed 8/8 when run as a file.
**Cost:** one failed run with partial state and three stranded fixture rows.
**Rule produced:** a script with heredocs is run as a file, never fed to `bash -s` over ssh stdin.

### #59 — A navigation replacement left a route dead that no inventory could see (2026-08-12)
**What happened:** In the Sales Hub redesign, the operator ruled mid-session that a structural navigation
replacement gets its own rendered leg. The leg immediately found Escape-from-account-detail dead; it had never
worked, because the global key layer returns early for every non-curation view, and no inventory of controls
could have shown that. In the same leg, the estate held zero pending candidates and zero drafts, so the rail
badges rendered empty and apparently correct; the render path was proven only by injecting non-zero counts at
the network layer.
**Cost:** one dead route that had never worked; one badge render path that a legitimately-zero count had left
unproven.
**Rule produced:** a structural replacement of navigation gets its own rendered leg — every route by click, by
key and by deep link, asserting the rendered marker rather than the URL. A dead path is a FAIL however good the
views look, and a legitimately-zero count proves nothing about the code that draws it.

### #60 — Two of the first 35 harness results were red and only one was real (2026-08-12)
**What happened:** On the same navigation leg, two of the first 35 results were red and exactly one was a
defect. `#digest` was flagged because the harness expected the hash to be rewritten to bare, when keeping it is
correct deep-link behaviour. `.accounts-subsection !== 3` was flagged because the class is also used by the
tripwire block. The third red, the Escape route, was the true defect.
**Cost:** two false red legs out of 35; reporting them as defects would have changed correct behaviour to
satisfy a wrong expectation.
**Rule produced:** a harness assertion that fails indicts the harness until you have checked which side is
wrong — read the assertion against the requirement, not against the output.

### #61 — A double-encoded jsonb write white-screened the approval surface (2026-08-12)
**What happened:** Both item C composer writers called `JSON.stringify` on `recipients` before writing to a
`recipients jsonb` column, so every draft row stored the two-character string `[]`. The dashboard account page
then white-screened for any account holding a draft, because the client called `(value ?? []).map(...)` on data
from its own store and the throw blanked the whole single-page app. Account 108 was unreachable and nothing
reported it: the flow that wrote the row and the suite that checked the flow were both green. It was found by
opening the page.
**Cost:** the approval surface was unreachable for every account holding a draft, with no alarm raised.
**Rule produced:** `JSON.stringify` into a `jsonb` column double-encodes — check the write with `jsonb_typeof`.
The reader's half is separate and equally required: a surface must not die on the shape it did not expect.

### #62 — An assertion was green by construction for months and fired first in production (2026-07-30)
**What happened:** The PKMS seed asserted A7, that the canon refresh interval is within its class bounds, with
canon empty, so it was green by construction on 2026-07-30. The question harvest inherited the same assertion.
By then canon held 265 rows, two of them out of bounds, and the very first live tick errored and pinged the
operator. The two rows were real: the approve contract computes `LEAST(floor, GREATEST(0, valid_until -
CURRENT_DATE))`, which is 0 for any already-expired `valid_until`. The assertion was correct and had simply
never run.
**Cost:** an assertion that had never executed fired for the first time in production, on 265 rows.
**Rule produced:** a vacuously-green assertion is a refusal waiting for data — give it a fixture that makes it
evaluate, or state at the assertion that it is armed and unexercised.

### #63 — An assertion over state the component did not own would have wedged every future batch (2026-08-12)
**What happened:** In the same incident, the question harvest refused to close its batch over a canon row it
neither wrote nor approves — the harvest writes no canon at all — which would have blocked every future batch
behind an unrelated row. It was changed to a reported count in the completion ping, with the refusal kept for
what the batch is responsible for: canon gaining no row since the batch opened, keyed to its own `opened_at`.
**Cost:** a permanent block on all future batches, avoided before it took effect.
**Rule produced:** assert what the component is responsible for — if the assertion fires, ask whether this
component can fix it. If not, it is a notice, not a gate.

### #64 — Two sessions in one repository overwrote each other's work (2026-08-12, 2026-08-15)
**What happened:** In item G, the question-harvest session's revert wiped another session's uncommitted
`build_flows.js` edits mid-build, and both sessions independently minted migration 060 and `flow15`. The
corollary was added on 2026-08-15: the R-BB-4 loopback rebind (eq14-stacks 0adf636) was reverted 13 minutes
later by 479107f, a child commit authored from a pre-rebind working tree that pasted the old compose file back,
and its container recreate put the running bridge back on the tailnet. It was caught only because the next
session grepped the merged file for its own ports line; `git log` showed clean linear history.
**Cost:** one session's uncommitted work destroyed silently; two colliding migration numbers; one security-relevant
rebind reverted for 13 minutes-plus with no signal in the DAG.
**Rule produced:** two live sessions in one repository are two writers on one file — sequence like a queue, not
like a merge. Verify the other session's uncommitted work against its plan and the suite, commit it separately
with attribution before touching any file it holds, claim colliding namespace away from the other side, and keep
patch backups of your own hunks. A concurrent commit that descends from yours can still content-revert it: diff
the files you changed against your intent; never trust the DAG.

### #65 — A working control was unreachable from where its work appeared (2026-08-12)
**What happened:** In item G RG1, the attribution confirm surface worked correctly at its own deep link,
`#account/<id>/meeting/<tid>`, and nothing on the account page that rendered the SUGGESTED chip led to it: a
suggested commitment's meeting is unmapped by definition, so it appears in no Meetings section. It was found only
because the rendered leg walked the operator's route rather than the harness's.
**Cost:** one operator control correct and unreachable.
**Rule produced:** a new operator control is verified reachable from where its work surfaces — from the element
that shows the problem, name what the operator clicks to reach the control that fixes it.

### #66 — Two arrival surfaces were covered and neither detected (2026-08-12)
**What happened:** Two misses in one day. An ENEC RFP landed by email and no email-to-RFP lane existed, because
intake was gated on the operator forwarding files to the Telegram bot, so the factory's entire acceptance event
sat unnoticed in an inbox. Separately, a live use-case discussion for the 7x account ran in a Slack channel the
poller could not read, unjoined and unmapped, with nothing reporting the gap; the machinery existed and the
account rendered as quiet. The operator ruled the same day, and ruled in the same sitting that Slack DMs are an
in-scope arrival surface.
**Cost:** two arrival surfaces reported as covered while neither detected; one acceptance-event RFP missed.
**Rule produced:** detection is never operator work. Every surface where customer work can arrive gets machine
detection; the plan names, per surface, what arrives there, what detects it, and what the detector raises.
Detection keys on content, never on sender. Where a surface cannot be machine-read, silence is the defect: name
the blind spot on a card or a digest line.

### #67 — A stale generated file deployed cleanly and reported success (2026-08-12)
**What happened:** In the question-harvest session, a backtick inside a SQL comment terminated a JS template
literal, `build_flows.js` died, `flows/*.json` stayed stale, `n8n.sh update` transferred the stale file and
printed a success line, and the flow was reactivated on the old definition. It was caught only by hand-reading
the deployed graph. Both guards now live in `scripts/n8n.sh` as exit 4 for a read-back mismatch and exit 5 for a
stale file; the first version of the read-back would not have caught this incident, which is why the staleness
guard exists beside it. A third program gate was added by operator ruling on 2026-08-26 (n8ngate-1): `update`
refuses the exact flow blob until `scripts/rehearse-flow-sql.sh` has written its PASS artifact, then waits for
the configured count of new successful executions, restoring `flows/.previous/<file>` and printing a rollback
line on error or timeout. `--no-verify` is the explicit escape for an inactive or deliberately non-ticking flow.
**Cost:** one flow reactivated on a stale definition with a success report; detection was by hand.
**Rule produced:** a deploy is not verified by its own exit status, and running-equals-file is not
file-equals-source. Read the deployed definition back and compare it to the file, and refuse to deploy a
generated file older than the sources that generate it.

### #68 — A rewritten pre-check normalised away the shape that killed production (2026-08-12)
**What happened:** In arrival detection, execution 117491, Gmail items store `attachments` as JSON null. The
session's COUNT pre-check used `payload->>'attachments'`, whose text cast produced SQL NULL and was saved by
COALESCE, and it passed. The deployed statement used `payload->'attachments'`, whose jsonb null was fatal to
`jsonb_array_length`, and it killed the flow's first tick.
**Cost:** one flow's first tick killed by a shape its pre-check had normalised away.
**Rule produced:** a pre-check reaching the data through a different operator than production is a pre-check of
nothing — pre-checks run the production expression verbatim.

### #69 — A type guard in a sibling conjunct did not protect the length call (2026-08-25)
**What happened:** In the voice-adjudication backfill picker, scalar `voice_flags` rows made the live picker fail
with a scalar-array-length error despite an adjacent type guard, because PostgreSQL may reorder sibling `AND`
expressions.
**Cost:** one live picker failure.
**Rule produced:** a shape guard in one WHERE conjunct does not protect a shape-sensitive function in another —
put the function inside a `CASE` guarded by the type check, or filter the type in an inner materialized relation,
and pin the guarded shape.

### #70 — A red suite deployed because the gate was piped (2026-08-12)
**What happened:** In arrival detection, one flow deploy ran behind a suite invocation piped through `tail -1`.
`test | tail && deploy` gates on tail's exit status, so the deploy proceeded while the suite was red on a stale
pin. It was caught by re-running the suite bare; the deployed definition verified fine after the fact.
**Cost:** one deploy past a red gate; the estate records this failure shape occurring four times.
**Rule produced:** never let a pipe or a `;` hide a gate's exit code — gates run bare, or with `set -o pipefail`,
and the deploy line quotes the gate's own PASS output as evidence.

### #71 — An auto-converging stack deployed a gated change nine minutes into a live job (2026-08-15)
**What happened:** The tailDenials ingest fix was committed and pushed to eq14-stacks with its deploy deliberately
gated on assemble job 101 finishing, since a controller recreate mid-assemble was the exact failure the gate
existed to prevent. Converge auto-deployed it at 14:20Z, nine minutes into job 101, recreating the controller and
orphaning the session: the turn counter froze at 25, there were zero file writes for an hour, and the status
remained running. The rebuild itself was clean, with probe job 102 done at 14:20:47, and the notifier belt held
through the rebuild that broke the gate, so the blast radius was one re-armed job. The corollary was added the
same day in Tranche G: converge's rebuild list is a subset of the repository's stacks — at that time dashboard,
session-lane and agent-runner. For a stack outside the list, converge logs the changed line, pulls the checkout
and recreates nothing, so git and the host file both look current while the container keeps its birth code. The
Tranche G bridge.mjs change was reported changed at 23:30Z while chatgpt-bridge sat up 23 hours beside two freshly
rebuilt stacks; `docker ps` caught it before any leg trusted the deployed state.
**Cost:** one orphaned session, its turn counter frozen at 25, with an hour of zero writes; one stack running
birth code while every file-level signal read current.
**Rule produced:** on an auto-converging stack a push is a deploy — hold the push until the gate clears, or park
the stack with an explicit exclusion marker, and say which in the record. The auto-rebuild list is a subset of the
repository's stacks; read the loop before trusting either direction, and use the in-container check as the truth.

### #72 — 327 of 330 canon rows were self-generated (2026-08-12)
**What happened:** The operator ruled while designing the pricing-document lane, and the estate was measured the
same hour. Of 330 canon rows, 217 came from `qa.json`, which holds answers the RFP agent itself wrote; 29 from
`answer_jobs` drafts; 16 from `brain_cache.json`; 61 from customers repeating the company's own claims back; and 3
from the human-authored `verified-facts.md` register. 327 of 330 rows were stamped `brain_grounded`. The loop was
visible in the connector count: the authored register says 1,000+, Brain says 800+, customers echoed about 820 back
nineteen times across fourteen accounts, and canon held both the register's figure and the echo.
**Cost:** 327 of 330 canon rows self-generated; 3 rows traceable to an authored source.
**Rule produced:** knowledge is extracted from authored sources, never from artifacts the system generated. A
generated document is a previous answer, not evidence, and curation does not break the loop, since a curator
approving a fluent sentence is approving prose rather than checking a source. Ingest lanes declare their source
class, and canon must be able to say which rows a human ever checked. An amount, rate or list price comes from the
authoritative document and nowhere else.

### #73 — A hand-maintained coverage list had silently stopped at 070 (2026-08-13)
**What happened:** External review caught `build/test_sql.js` twice. Its grammar-parse list was a hand-maintained
array that had stopped at migration 070, while 052–059, 062–069 and 071–074 shipped unparsed. The sessions-schema
pin below it globs and prints a per-file ok line, and the session's first refutation cited exactly those lines as
parse evidence — the same shape as a committed claim about a protection never checked against the protection,
performed live by the party that had just re-read the rule. The parse source list is now the glob.
**Cost:** 21 migrations shipped unparsed under an all-clean claim; one verification of the claim itself passed on
the wrong check's output.
**Rule produced:** a suite's coverage list is derived by glob, never hand-maintained, and a coverage claim is
verified against the check's code, not its output lines.

### #74 — The same nullable-operand hole appeared in three of four review rounds (2026-08-12)
**What happened:** Migration 066 took four review rounds and this defect appeared in three of them, in different
clothes. Round 1 found `tier = NULL` slipping the gate. The round-2 fix for a blank verifier wrote
`btrim(sme_verified_by) <> ''` on a nullable column and reintroduced the identical hole one conjunct over, which
round 3 flagged BLOCKING. PostgreSQL accepts a CHECK that evaluates to UNKNOWN, so the constraint never complained
— it stopped constraining. The companion finding, from the same file, is that enumerating a blank set is the wrong
instrument: each round found another invisible character (space, then tab and NBSP, then em space, zero-width
space and ideographic space), and `chr(160)` is encoding-dependent.
**Cost:** four review rounds on one migration; the same hole reintroduced by a fix for it.
**Rule produced:** inside a CHECK constraint a nullable operand does not fail — it stops constraining. COALESCE
every nullable operand, and require a character that must be present rather than enumerating characters that must
be absent.

### #75 — Two data-modifying CTEs touched one row and one write vanished (2026-08-17)
**What happened:** In migration 085, the flow17 stage-anyway drain reopened the batch or cleared the request, never
both. PostgreSQL discards the second write to a row in one statement without erroring. Parse checks passed and two
codex rounds passed; the DO-block dry-run's reopen assertion raised it.
**Cost:** one silently dropped write that survived parse and two review rounds.
**Rule produced:** two data-modifying CTEs touching the same row in one statement silently drop one — every write
to one row goes into one `UPDATE … SET a, b`.

### #76 — A shared statement regenerated a second flow file that was never deployed (2026-08-17)
**What happened:** In defect 25, the readiness CTE shared by flow17 and the agent watcher gained
`excluded_reason IS NULL`. The watcher's regenerated JSON sat uncommitted and the live watcher kept the old
predicate. It was harmless that day, because Telegram batches never classify, but a batch with an excluded file
would have sat not-ready forever. It was caught by the advisor's close-out `git status`, not by the build.
**Cost:** one live flow left on an old predicate with a latent permanent-stall shape.
**Rule produced:** a change regenerating several generated files stages and deploys every file whose content
changed, not the one the change is about; the deploy list is derived from the diff.

### #77 — Six nodes were renamed and every wiring check stayed green (2026-08-12)
**What happened:** In the question harvest, inserting one node into a positional name array renamed six others. The
connections were repaired by name and the wiring test went green, while `PG · completion snapshot` was a Code node,
`Code · summary + assertions` was the Telegram node, and `TG · harvest summary` was Postgres. The completion stage
never ran its snapshot query; the summary code executed against the router's item, and the Telegram node sent the
operator a harvest-complete ping reading 0 calls, 0 clusters and 0 candidates. It was found by reading a stalled
execution's node list.
**Cost:** one false completion ping delivered to the operator with three zeroed counts; a green wiring test over
three misassigned nodes.
**Rule produced:** a name that lies about its node is invisible to a wiring check — bind node names explicitly and
assert that a node's name matches its type.

### #78 — 48 package-install requests were refused inside one job (operator ruling 2026-08-20)
**What happened:** Job 123 produced 48 refused `pip install` CONNECT attempts: cairosvg was already baked into the
image but the skill text told the agent to install it anyway, and pymupdf was not baked. The operator ruled the
PyPI download hosts, pypi.org and files.pythonhosted.org, into the egress allowlist as a fallback.
**Cost:** 48 refused connections in one job.
**Rule produced:** the default remains that an import failing in the executor is a missing-bake defect, baked in
`Dockerfile.executor` and `toolchain.json` in the same commit. Download-only package hosts may be allowlisted; the
test that keeps it safe is that the upload host is not listed, so no customer content can leave through the new
entries. Every allowlist change gets cross-family adversarial review, and skill text must never tell an agent to
install a baked package.

### #79 — A dropped UNION column broke an alias and pinged every minute (2026-08-20 22:01–22:10)
**What happened:** Small-batch-2's round-2 fold dropped a dead UNION column and with it the `AS key_a` alias that
the final `ORDER BY key_a` depended on. `build/test_code.js` pins text and `build/test_sql.js` parses grammar;
neither resolves column names, so the query failed only inside Postgres, on the watcher's one-minute tick, and the
Phase-0 error notifier pinged the operator every minute until the hotfix (0885c84).
**Cost:** roughly nine minutes of per-minute operator pings from a defect no static suite could see.
**Rule produced:** dry-run every new or changed SELECT as its lane role against the live database before activating
the flow — run each SELECT or CTE with placeholder params under `SET ROLE <lane role>`; a zero-row result is fine,
an error blocks the deploy.

### #80 — An unaliased first UNION arm emitted zero rows to its consumer (2026-08-24)
**What happened:** Ledger 71b records that the inherited dashboard-card reconciler selected `card_message_id` plus
two unnamed expressions, while its Code node read `message_id`, `decision` and `parse_mode`. Postgres exposes names
such as `case` or the source column name for unnamed expressions, so the reconciler's own filter emitted zero
redraws. Grammar parsing stayed green because the SQL is valid. The 71b build caught the mismatch while adding more
UNION families and made the first arm's eight-column API explicit.
**Cost:** zero redraws emitted by a reconciler that reported no error.
**Rule produced:** a UNION's output contract is named by its first SELECT — alias every consumed column there and
pin the aliases.

### #81 — A request to re-mark a pushed FAIL row was denied and then ruled on (2026-09-01)
**What happened:** The advisor requested an E28-1-b re-mark on a pushed FAIL attest row. The permission classifier
denied it twice and the walker stopped and asked; both were the system working. The request was withdrawn and the
rule was pinned. A scope note was added the same night by overseer ruling on the leg-4 escalation: the advisor
offered to transcribe a verdict-changing amendment with attribution on the richedit leg-4 report, the walker held on
this rule and escalated, and the offer was withdrawn before the ruling adopted the fresh-report path. In the
favicon token-form case, PASS verdicts were translated to token lines with semantics untouched, which is permitted.
**Cost:** no data loss; two denials and one escalation, all of them the control operating as designed.
**Rule produced:** a pushed attestation is never edited. The forward path is a fresh walk producing a new row. This
reaches pushed walk reports: a peer may transcribe verdicts format-unchanged only, and any change of verdict
semantics, including a FAIL becoming FAIL-FIXED-PENDING, is the walker's hand alone and always via a new file.

### #82 — A brief named a model family to review its own grants (2026-08-22)
**What happened:** The customer-layer brief named codex to review codex's own grants, and relationship-memory made
the same request the same day.
**Cost:** no measured cost recorded; caught before the reviews ran.
**Rule produced:** external review is by the other model family, chosen by who built it — codex-built goes to an
explicit Opus session, Claude-built goes to codex adversarial. Grants and migration reviews get the checklist: exact
columns, no WITH GRANT OPTION, REVOKE PUBLIC, DO-guards that must not skip required grants, SECURITY DEFINER rules,
view leaks, loud rerunnable checks, dry-run attached.

### #83 — A pinned rule string held an invisible focus ring in place (2026-08-22)
**What happened:** Ledger 80 records that pinning the rule string `outline-offset: -3px` held ledger 76's invisible
focus ring in place: the suite was green while the ring measured 1.00:1 against its own button. The operator found
three keyboard defects that the handoff table had recorded as keyboard-checked.
**Cost:** three keyboard defects shipped under a green pin and a checked handoff line.
**Rule produced:** a regression pin asserts the behaviour the defect demanded, not the literal text of the fix — pin
the computed ratio, the rendered attribute, the DOM state; when only text can be pinned, pair it with the
measurement that proves the text works.

### #84 — A bake-off scored models on a candidate set that was missing two documents (2026-08-21)
**What happened:** In the E-4 renewal picker bake-off, the FIND stage's 12-read cap exposed only 5 of the oracle's 7
desired Zain documents; the Order Form and the BRD were outside the model lane entirely.
**Cost:** two of seven oracle documents unreachable by any candidate model.
**Rule produced:** a model bake-off grades only what the upstream selector supplied — freeze one candidate set for
every model, and report selector recall separately from model accuracy.

### #85 — A family-level claim about disabling reasoning did not hold for the exact model (2026-08-21)
**What happened:** In the same E-4 renewal picker work, `glm-5.3` rejected both disabled thinking and an attempted
`thinking.type=low`. The accepted floor was `thinking.type=enabled` with `reasoning_effort=low`, and a
4,096-token ceiling was needed to return bounded JSON.
**Cost:** no separate figure recorded; the constraint was found by probing the exact id.
**Rule produced:** pin reasoning controls per exact model id, and count mandatory reasoning inside the output
breaker.

### #86 — A shared module was imported by two stages and copied into neither (2026-08-22)
**What happened:** Ledger 78 records that `dashboard/app/batchtitle.mjs` was imported by `arrivals.jsx` and by
`server.mjs` and carried by neither stage's `COPY`. Four Opus review rounds and a green local Vite build passed it,
because a local build runs against the whole worktree and resolves a module the image never receives. Converge
deferred the deploy with `npm run build` exiting 1. The rule is pinned in `build/test_code.js`.
**Cost:** four review rounds and a green local build passed a change that could not build in the image.
**Rule produced:** a green local build is not a green image build — a new shared module must enter every build stage
that imports it, reviews of such a change check the container build definition, and a test pins the rule.

### #87 — A synthetic row in a shared table was visible to unrelated pickers (2026-08-22)
**What happened:** For the relationship-memory commitment reader, synthetic `seen_transcripts` rows were required by
the unchanged commitment dashboard and item G joins. An unfiltered calendar correlator could bind a mail-fact
timestamp to a real event, and the dossier Fireflies mapper would re-pick the rows forever. Opus review round 1 found
both before activation.
**Cost:** none realised; both paths were closed before activation.
**Rule produced:** a synthetic compatibility row in a shared domain table claims a namespace, not just a key —
enumerate every reader and writer before activation and pin each exclusion in source and generated artifacts.

---

### #88 — A due-basis seam audit was left as an open cleanup item
**What happened:** cleanup item 1, due-basis seam audit

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


### #89 — A verify-walk attest ran against a guessed, nonexistent commit tail
**What happened:** 2026-09-02, the verify-walk attest first ran against a guessed tail (4dc9da3ab7…, nonexistent); caught and re-run against the box HEAD before push. The walker (draftwalk-3d) named the resolving-mistype hazard; adopted as routine. Refinement (2026-09-02, second miss): the attest keys the DEPLOYED image revision — `docker inspect -f '{{index .Config.Labels "org.opencontainers.image.revision"}}' <container>` — not the box checkout HEAD. The two coincide only when no build has deferred; a walk-gate defer leaves the checkout ahead of the running image, and a checkout-keyed row is invisible to the gate

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


### #90 — A main-bundle-only check would have proven nothing about the walked surface
**What happened:** 2026-09-02 fwrework §18 walk (draftwalk-3d): the walk's substance lived in documentReview-_l6f-qc-.js; a main-bundle-only check would have proven nothing about it. Same walker line: markers must be pre-validated ABSENT in the old artifact (object keys survive minification) before PRESENT in the new one counts as proof

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


### #91 — The rich-editor list-toggle sequence needed three walks to settle
**What happened:** the richedit list-toggle sequence, 2026-09-01/02 (draftwalk-3d; baselines 56b88d00, 84a01c60; final walk 88f1b9f2)

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


### #92 — An Item C burn produced the sweep-tool pattern
**What happened:** OVERSEER order + the Item C burn, 2026-09-02; sweep tool pattern in the ledger entry of that date

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


### #93 — A redeploy verify timed out and rolled a drifted query into production
**What happened:** 2026-09-02 calendar-poller redeploy — verify timed out 0/1 at 10 min, rolled the drifted query back into production while the ledger said clean

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


### #94 — Seven unanimous design rounds were rejected before one was adopted
**What happened:** a1home v1–v4 + three predecessors, all unanimous, all rejected; adopted with the v5 round

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


### #95 — An editor passed its walk on counts while being illegible at the operator's viewport
**What happened:** job-254 editor acceptance failure, 2026-09-02; the walk had proven rendering and counts, nobody judged legibility at his viewport

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


### #96 — A pin realignment closed with the suite fully green
**What happened:** 2026-09-02 pin realignment, wa 04eb4def + 1aa03025; suite ALL 1357 PASSED at close

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


### #97 — A use-path brief carried stale job numbers and the walker refused the entry point
**What happened:** editorlegib3 use-path brief 2026-09-02 carried "job 276" + "~44 findings" in the text and the 254 batch URL as the entry point; the walker refused the guess, and target rfp-aby-20260831 was re-established from source (no rfp_batches row, grounding cloned from rfp-test-20260718, __FIXTURE__ source filename) before any verdict was cast

*Moved verbatim from docs/ADVISOR-WA.md, 2026-09-06: the rule it annotates keeps a citation.*
**Rule produced:** the rule it annotates in `docs/ADVISOR-WA.md`, which cites this entry.


## Estate-rule origins (#e8–#e38)

> Origins moved out of `ADVISOR-ESTATE.md` on 2026-09-04. Same contract as the block above: record
> file, not doctrine. The live rule keeps its claim and its date; the incident is recorded here.

### #e8 — 29 sentinel filenames were in use across the estate (2026-08-28)
**What happened:** 29 distinct sentinel filenames were in use across the estate, among them
`REVIEW-DESIGNFIX-R2-DONE`, `GEN1-READY-FOR-FINAL-JUDGE` and `CALIBRATION-1-JUDGE-HALTED`. Each is a
free-text contract renegotiated per lane, so a mismatch between the brief's string and the advisor's
poll string is a silent, permanent miss that raises no error. That is the wbbuild failure mode, and
writing the command more carefully in briefs does not fix it; closing the vocabulary does. The recipe's
item 4, which banned a lane from calling `orca terminal send` into the advisor's terminal, was retired
on 2026-09-04, superseded by the 2026-09-01 operator order opening network access so lanes can message
their advisors through Orca, with one surviving carve-out for externally sourced content. The concern
that rule addressed — lane text being indistinguishable from operator input — is now handled by the
LANE-SIGNAL prefix rather than by a ban. Origin of the retirement: rule 4 (2026-08-28) and the
2026-09-01 order were both live and contradictory, so brief templates followed one while advisors
followed the other, neither channel was trusted, and advisors polled files instead. Item 5 of the recipe
is the advisor-to-lane direction: `orca terminal send --terminal <handle> --text '…' --enter`, since
nothing is delivered without `--enter`, and the send is read back to confirm.
**Cost:** 29 competing sentinel contracts; one contradictory rule pair that pushed both channels back to
file polling.
**Rule produced:** the lane launch recipe is five fixed lines, and the sentinel vocabulary is closed. A
brief missing the signal-back contract, or a codex launch missing the approval mode and the notify hook,
is a routing defect on the advisor.

### #e18 — A feature rendered, was silently removed, and the built claim stood (operator ruling 2026-09-01)
**What happened:** A favicon was reported built while never rendering. The rich Slack editor did render
on 2026-08-19, evidenced by the screenshot at `docs/commitments-tab-2026-08-19/11-editor-preview-slackmark.jpg`,
and was then silently removed on 2026-08-23 (eq14 bc970ac) while the built claim stood. The architecture
review corrected it on 2026-09-01. An amendment was added on 2026-09-03: for a surface a walk has seen
before, the walk brief names the prior walk's render and the walker compares against it, so a removal
shows as a diff rather than as an absence nobody looked for, and the repository's brief template carries
a removed-behaviour section that a build lane fills or marks as none.
**Cost:** one feature reported built that never rendered; one working feature removed for nine days under
a standing built claim.
**Rule produced:** rendered proof before closure of any operator-suggested item; build records declare
removed behaviour, and walks compare before and after renders.

### #e21 — A store was written hourly for 12 days with zero readers (operator order 2026-09-01)
**What happened:** neo4j was written hourly for 12 days with zero readers, after three rulings in the same
week each killed a read path and nobody reconciled them. Recorded in relationship-memory at
`docs/neo4j-accounting-2026-09-01.md`.
**Cost:** 12 days of hourly writes with no consumer.
**Rule produced:** every scheduled writer names its production reader. Boot check for every advisor: STATUS
lists no reader-less writer.

### #e22 — A development-scoped model order was applied to five production flows (operator order 2026-09-02)
**What happened:** Commit 18695294 on 2026-08-31 moved five customer-facing production flows from Opus 4.8
to Opus 5 on an order to start using Opus 5, which covered development work. The switch raised API spend
and broke the follow-up composer parser, costing 121 wasted calls on 2026-09-01. It was reverted on
operator order on 2026-09-02, with the standing instruction that models in the estate are not changed
unless the operator confirms the change is an estate change, and that his model orders are to be read as
covering development work by default.
**Cost:** 121 wasted calls, a broken production parser, and raised API spend across five flows.
**Rule produced:** model rulings are development-scoped unless the operator confirms an estate change.

### #e23 — A bare Enter updated codex across every lane on the machine (2026-09-02)
**What happened:** The Skill Factory gen-2 codex lane terminal opened on the codex update dialog with the
update option highlighted. A bare Enter, intended as skip, ran the global npm install and moved every codex
lane on the machine from 0.152.0 to 0.152.1 while other lanes were running. Rolling back is the operator's
call only.
**Cost:** an unplanned version change across every codex lane on the machine, mid-run.
**Rule produced:** never send a bare Enter into an agent dialog — read which option the cursor sits on and
send that option key or its number; if the send is blocked, stop and report.

### #e24 — A persisted approval setting was lost at restart and three lanes hung (operator observation 2026-09-02)
**What happened:** After the 2026-09-02 device restart the persisted approve-for-me setting was gone. Lanes
launched afterwards — inboxd1a1 twice, and fwheading1 on `npm ci` — hung at approval prompts until a belt
caught them. The operator observed that codex sessions were being launched without auto-approval and were
hanging.
**Cost:** three lane hangs after one restart.
**Rule produced:** codex lanes pass the approval mode explicitly on the command line, never as a persisted
setting, with the banner read and confirmed before the first prompt.

### #e25 — An advisor ran reproductions and full suites in its own turn three times (operator order 2026-09-02)

<!-- origin: ADVISOR.md#25 -->
**What happened:** In the fwheading1 and flagonly1 cycles of 2026-09-02, the work-automation advisor ran
shape reproductions and full test suites in its own turn three times, and the overseer ordered an
advisor-side APPLY-SAFE read. The operator ruled that advisors perform no tasks. The ruling extends the
existing 2026-08-29 rule from menial hand-work to every task.
**Cost:** three advisor turns spent on work that belonged in a lane, plus one advisor-side review order.
**Rule produced:** advisors advise and orchestrate; every task is outsourced.

### #e27 — A relacl-only probe missed an existing column grant (2026-09-02)
**What happened:** relationship-memory migration 040 was written to grant SELECT on two columns of
`public.slack_channels` to the relmem role. The role already held that column-level SELECT from
work-automation migration 113, applied 23 August. Two relacl-only probes missed it, so the grant was a
no-op and its REVOKE rollback would have stripped the other repository's grant. The dry-run gate caught it
and nothing was applied.
**Cost:** none realised; the rollback would have removed another repository's grant.
**Rule produced:** existing-grant probes read column privileges, not relacl. A migration touching a
privilege another repository granted names that repository's migration in a precondition comment and sends
a dependency notice.

### #e28 — A file added without its COPY line put a service into a restart loop (2026-09-03)
**What happened:** Lane b19route-1 added `slack_dm_routes.cjs` without the corresponding Dockerfile COPY.
Lane tests, `node --check` and two reviews all passed on the checkout. The converge deploy put
session-broker into a 22-restart loop with a module-not-found error, and the session lane was down about 40
minutes until the revert.
**Cost:** a 22-restart loop and roughly 40 minutes of session-lane downtime, past two reviews and a green
checkout.
**Rule produced:** a change to a service's source set is verified in the built image, not the checkout —
build it, run the entry once inside it, and add a source-closure test over the COPY set.

### #e29 — A deploy watch keyed on a label the target did not emit (2026-09-03)
**What happened:** The b19route-1 deploy watch was keyed on the image revision label. It never fired, and the
restart loop of #e28 was found by hand.
**Cost:** one watch that could not fire during a live outage.
**Rule produced:** a watch is armed only on a signal the target actually emits, proven once by hand on the
live target; prefer container state and health over labels.

### #e30 — A walk clicked a live write control (2026-09-03)
**What happened:** The neardup walk clicked the dashboard dismiss control and inserted
`rel.dismissal_request` 639 against a live fact. It was reversed by a guarded worker DELETE.
**Cost:** one unintended write against live operator-owned data, reversed.
**Rule produced:** walk briefs name the surface's write controls as forbidden — a walker writes only what
its brief names, each with its reversal named up front; every other writing control is listed forbidden, and
no walker verdict may persist on an operator-owned decision row.

### #e32 — A declared external prerequisite had never been created (2026-09-03)
**What happened:** In slack-dm step 3, the relmem-dm overlay declared the network `relmem_connector_net` as
external, and nobody had created it. The marker step stopped correctly. Had it not, converge's unguarded
`compose up -d` under `set -e` would have aborted every converge run until the marker was removed.
**Cost:** none realised; the failure mode was estate-wide converge failure.
**Rule produced:** a gate package names every external prerequisite with its creating owner and its proof —
the seat that creates it, the command, and the check that proves it before the dependent step runs. A line in
a compose header saying the operator creates something first is not an assignment.

### #e33 — A deploy guard was tested for one state and not the others (2026-09-03)
**What happened:** convergedm-1 tested the marker but not the stack variable. With the marker present, the
next dashboard or agent-runner converge would have built an invalid compose project and deferred every tick,
and on a quiet box the marker alone would never have triggered a session-lane converge. The lane's own tests
and its Opus gate passed; the step-3 worker found both defects on the box.
**Cost:** none realised; two failure states in one guard passed a lane suite and a review gate.
**Rule produced:** a deploy-path guard is verified by tracing the script's control flow, per stack and per
state, plus a harness over the script's functions exercising those states. The gate report quotes the trace,
not the diff.

### #e34 — A lane read from a host its brief had not named (2026-09-03)
**What happened:** The skill-factory variance-gate lane pulled a copy of a grounding file from `/srv` on
EQ14 over the operator's ssh, to run its real acceptance test. Nothing was written and the copy died with
the worktree, but the brief had not named the box.
**Cost:** no data loss; one unbriefed read from a host.
**Rule produced:** a lane touches only the hosts its brief names — host, path and purpose, or none. Reading
is not exempt; an unbriefed read is an incident recorded in the lane report with what was read and where the
copy went.

### #e35 — The host rule existed in a repository with no brief template (2026-09-03)
**What happened:** The variance-gate incident of #e34 happened in a repository that had no standing brief
template, so the rule that would have prevented it was not present by construction.
**Cost:** no separate measured cost; the cost is #e34's.
**Rule produced:** every lane brief starts from the repository's standing template, whose header carries the
no-writes-outside-this-worktree and named-hosts sentences verbatim, so the boundaries are present by
construction rather than by memory. A brief lacking them is returned before launch.

### #e36 — Sixteen migration headers still read NOT APPLIED weeks after apply (2026-09-03)
**What happened:** Sixteen migration headers still read NOT APPLIED weeks after they had been applied, a
README listed stacks that no longer matched the directory, and a seam stayed marked as planned for ten days
after it went live. Each was read by a fresh session as truth.
**Cost:** sixteen stale headers, one stale README and one ten-day stale status line, all load-bearing at boot.
**Rule produced:** prose that asserts live state carries a check or a date — produced by a verify leg that
skips loudly when the host is unreachable, or dated with its evidence pointer. Unchecked, undated live-state
prose is stale after 14 days and a new session does not act on it.

### #e37 — A landing was reported before the push reached the remote (2026-09-03)
**What happened:** Commit 358562a was reported landed at 17:29 local time. The push never reached GitHub,
converge found nothing for two hours, and the miss surfaced only when the post-converge box line was chased.
Three earlier chained-push incidents had already separated the log check and the push into two commands.
**Cost:** two hours of a landing that had not landed, after three prior incidents of the same family.
**Rule produced:** a landing is reported only after origin shows the sha — the push and its check are two
commands, and the check is the report.

### #e38 — A recurring ingest went live on a box timer (operator ruling 2026-09-04)
**What happened:** The Slack DM ingest went live on a systemd timer, because relationship-memory exposes no
run endpoint, and the operator asked why it was not a managed flow. Scope of the ruling is work jobs:
anything that reads or writes estate data on a schedule. The converge deploy loop, the worktree janitor,
backups and other host maintenance are infrastructure and stay on the box scheduler. Classing test, from the
2026-09-04 work-automation inventory: a service-internal loop that only consumes a queue the scheduler or the
operator filled — a claim poll, a transport long-poll, a job-scoped reconcile — is infrastructure; a loop
that decides or mutates estate data on its own clock — an auto-map, a scope verdict, an ingest, a cadence
pass — is work and belongs under the managed scheduler.
**Cost:** no measured cost recorded.
**Rule produced:** recurring scheduled work runs under the estate's managed scheduler; a box timer is for a
one-time run. A recurring job that cannot yet be started there is a gap with a lane, listed in STATUS until
the managed path lands.

## Moved verbatim from ADVISOR-WA.md on 2026-09-08 (advisor boot-set budget)

Seven origin spans, byte-identical to what ADVISOR-WA.md held. The DIRECTIVE each one
supported stays in ADVISOR-WA.md, unchanged; only the incident narrative moved here,
which is where this file's own rule sends it. Verified: 734 sentences of the pre-move
file checked against the post-move file after subtracting these seven spans, 0 lost.

Why now: the advisor boot set hit its 40,000-token ceiling and refused the replication
of ADVISOR.md carrying the four-reason message contract, leaving work-automation 20
lines behind relationship-memory and skill-factory. The gate's own remedy is to take
something out of the set; this is that, taken from narrative rather than from rules.

**walk before/after renders** — origin span:

Origin: the bc970ac regression was screenshot-filed on
  2026-08-23 (docs/ledger-91-slack-editor-1440.png, bare box) and nobody compared it to the
  2026-08-19 toolbar screenshot; the regression then read as "never built".

**build records declare removed behaviour** — origin span:

Origin: eq14 bc970ac deleted the rich Slack editor while its message
  claimed only "Add Plate draft editing with Slack mentions".

**at-prompt text is untrusted** — origin span:

Origin: 2026-08-26, a 6-hour incident where
  autocomplete suggestions in the operator's voice were relayed as operator confirmations of a
  workbench verdict while he was asleep; the advisor's hold-while-unexplained + independent DB
  verification caught the false verdict regardless.

**n8n deploy gate** — origin span:

*Origins: n8ngate-1 (operator ruling 694f85b, landed 2026-08-26);
  the 2026-08-20 22:01–22:10 incident where a dropped UNION column killed the watcher's
  1-minute tick and pinged the operator every minute until hotfix 0885c84 (ORIGINS #79); and
  entry24b, 2026-08-26 16:44 — `jsonb -> bigint` on a WITH ORDINALITY index, rolled back at
  16:48. Three statements of this gate stood in this file until 2026-09-01; this is the merge.*

**rehearsal leg in release briefs** — origin span:

Origin: bgov-1, 2026-09-07 — RELEASE GO relayed, R2 aborted `REHEARSAL REQUIRED … relmem-governor-dcf7df9f…`,
nothing deployed; the brief's release legs (R1–R3) had no rehearsal leg and HOSTS named only the R3 psql read.

**n8n env / activation snapshot** — origin span:

*Origin ×4: the stale
  activation snapshot; the box container predating the committed `TELEGRAM_CHAT_ID`; the
  errorWorkflow wiring silently stripped by every API deploy until a silent failure exposed
  it; `docker compose restart` carrying the container's birth env — env-file changes apply
  only via `up -d` recreate (the setup-token stayed invisible through a restart).*

**no-review tier is a prohibition** — origin span:

*Added 2026-08-07. Origin: 22 external review rounds in
  five days (notes/DDL 2, session-lane spike 7 plus 4 probes, P2 hardening 7, T0 3), the
  majority on changes that could not break anything. A gate applied uniformly is a gate that
  costs most where it protects least.*

### Second pass, same day (lane bootset-1, atop 8b30cfb6)

Eleven further origin spans, byte-identical to what ADVISOR-WA.md held. Same contract as the
seven above: the DIRECTIVE each one supported stays in ADVISOR-WA.md, untouched. Difference in
form: this pass leaves a pointer at each removal site — `*— ORIGINS 2026-09-08: <label>.*` — so
every removed span is still reachable from the rule it annotated. Selected by reading each span
in full (estate rule 44); nothing that prescribes was moved.

**launch contract false STOP** — origin span:

Origin: hygiene-1, 2026-09-07 19:3x +04 — launched at the held brief 953f1b41; the lane stopped exactly as
above; fixed by the flip at e215b1fe and a re-read order. bgov-1 the same evening had the flip (37dcaf55)
and did not stop. Candidate for a later estate-lint `launch`-mode check (STATUS token reads LAUNCHED);
not in the running hygiene-1 lane.

**origin corrected — undeclared removal** — origin span:

  **ORIGIN CORRECTED (2026-09-01 arch-review, t-dsh trace):** the 2026-08-19 "rich editor
  built" claim was TRUE when made — the editor was imported, rendered, and screenshot-proven
  (docs/commitments-tab-2026-08-19/11-editor-preview-slackmark.jpg, BUILD 2026-08-19 15:20Z).
  It became dead code on 2026-08-23 when eq14 bc970ac swapped the commitments composer to
  DraftPlateEditor without declaring the removal. The failure class behind this rule is
  therefore undeclared removal of shipped behaviour, not a false built-claim. Evidence:
  docs/arch-review-2026-09-01/evidence/t-dsh/REPORT.md §1B.

**gate exit code hidden by a pipe** — origin span:

  *Sibling of "a control that cannot fail is not a control" — this one is a control whose
  failure is structurally invisible to the thing it gates. Bit the system four times: a flow
  deploy behind a suite piped through `tail -1` while the suite was red (arrival detection,
  2026-08-12, ORIGINS #70); `git merge --ff-only … | tail -1` inside an `&&` chain, twice on
  2026-08-25; the ledger-100 eq14 ff whose `tail -1` output read as success while main never
  moved; and the tmppinfix landing, which pushed wa main on a red suite because ';'-sequenced
  commands ran the ff+push regardless. Four statements of this rule stood in this file until
  2026-09-01; this is the merge.*

**eq14-stacks main landing reported HELD** — origin span:

Failure that earned it: sessionkill-1 was landed on
main 2026-09-07 ~01:00 +04 and reported HELD twice; converge deployed it 05:30 +04, the pilot's cand3 frozen-pin gate
failed at 09:48Z, the OVERSEER accepted the HELD claim without checking the deploy path; rollback revert ddc2760 (ruling c).
The same line is proposed to the OVERSEER for ADVISOR.md Part II (universal; the OVERSEER owns that file).

**shared-checkout push** — origin span:

  *Origin: the d086bc3e gitignore push silently carried the walker's unverified walk-5
  report (d6e5bbcc) and the overseer's §23 edit (36edf1be); the walker's "decide before
  you push" warning arrived after the push. Both verified clean minutes later — near-miss,
  not damage.*

**ledger-100 ff** — origin span:

*Origin: the ledger-100 eq14 ff silently
  failed and the dashboard half of a "landed" tranche was absent until a later landing's
  failing pin exposed it.*

**two eq14 main trees** — origin span:

*Origin: 2026-08-25 — a stale relmem checkout in the primary
  failed a voicelint landing suite; the ambiguity of two "main" trees is the root hazard.*

**cross-repo coupling skew** — origin span:

*Origins: guide entry 10 (2026-08-25) — the Telegram slash-command
  classifier and its eq14-stacks bridge copy had to change together; and the 2026-08-24 skew
  incident, where entry-13's wa side landed with pins naming a new eq14 file while the eq14
  side was held, turning every suite run against eq14 main red.*

**background-browser visibilityState** — origin span:

*Origin: walk run 6 burned a permission prompt and a diagnosis cycle
  rediscovering this.*

**browser snippet live run** — origin span:

*Origin: entry23b — a SHIP-SAFE snippet walked Slack's virtual list in DOM order (not
  visual order) and produced a capture whose Preview showed 63 losses; the live run caught it
  before the operator could have applied it.*

**coupling run in the landing** — origin span:

sessionkill-1 (d57d8348 → 1d5c76e) was reviewed (Grok APPROVE 044f3c5)
   and landed 2026-09-07 05:29 +04 without the pre-merge coupling run; the wa suite was red against it the whole time. Four pins
   from the 2026-08-24 receipt family — 1177d819 / 527f805a (loop-top and outer-failure `reconcileConsumedExecutorProofs`),
   f0fac0ef (terminal CAS receipt order) and the active-child cancel-ACK order pin — asserted call sites the build had
   replaced by `sweepTerminalExecutorSessions` / `failClaimedJob`. The miss surfaced only in the re-deploy lane's item (v),
   two ASKs and one ruling later.

### Third pass, same day (lane wanarrative-1, atop c2dac39b)

Fifty-seven further origin spans, byte-identical to what ADVISOR-WA.md held. The directive each
supported remains in ADVISOR-WA.md unchanged; only the incident or attribution moved.

**rendered-page verification** — origin span:

  *— origins: the A2c standing ruling; F8's Opus-agent formalization, rescoped 2026-08-12 and
  broadened 2026-08-24; Tranche G's three fidelity gaps behind a green 14/15 walk
  (ORIGINS #51, #52).*

**review-round craft** — origin span:

*Origin: Code session, T1, 2026-08-06.*

**fixed estate palette** — origin span:

  Origin: second visual-identity drift in one day — the favicon guess, then unify-1 mockups
  delivered in a cream/rust palette after his explicit "colors stay as picked."

**column-grant ground truth** — origin span:

*Origin: the entry-21 part-3 brief asserted "session_app has NONE on
  slack_channel_map"; the lane's own read of 108 caught it before any edit (ASK-ADVISOR,
  07:52).*

**correctness is not usefulness** — origin span:

*Origin: 18 July to 7
  August 2026 — 432 tests passing, eight acceptance legs green, zero artifacts reaching the
  operator's actual workday. Every gate in that window graded the machine against a
  fixture the project authored itself.* *(Kept whole. Full: ORIGINS #33.)*

**authored-source knowledge** — origin span:

*(Kept whole. Measured at the time: 327 of 330 canon rows were self-generated —
  ORIGINS #72.)*

**one writer per workstream** — origin span:

*(Kept whole. Origins: the
  key incident + the dead UI-import ritual; a blanket `git add -A` that committed a mutated
  CLAUDE.md fork unseen — ORIGINS #31.)*

**pushed attestations are immutable** — origin span:

*Origin 2026-09-01: the advisor requested an E28-1-b re-mark on a pushed FAIL row;
  the permission classifier denied it twice and the walker stopped and asked — both were the
  system working; the request was withdrawn and this rule pinned. (ORIGINS #81.)*

**walk-report verdict semantics** — origin span:

*Origin: the advisor offered to transcribe a verdict-changing
  amendment "with attribution"; the walker held, escalated, and the offer was withdrawn.*

**cross-family reviewer pairing** — origin span:

*Origin: 2026-08-22 — the customer-layer
brief named codex to review codex's own grants; relmem asked the same day (ORIGINS #82).*

**builder invokes its reviewer** — origin span:

2026-08-31:
  two briefs said "advisor routes Opus on HANDOFF-READY"; the codex lane then asked
  authorization to invoke the reviewer and the advisor took the review inboard instead of
  granting it; the operator caught it.

**advisor-commissioned reviews are read in full** — origin span:

The 2026-08-30 grant verdict's body required a
  standing privileges check to be updated in the same apply; reading only the VERDICT line
  left the check contradicting the live grant until a janitor sweep surfaced it.

**codex startup banner check** — origin span:

`codex` printed "Update ran
  successfully! Please restart Codex." and returned to the shell; a prompt sent on the usual delay
  then landed in the SHELL input line (unsubmitted, partial).

**advisor-owned worktree gate** — origin span:

A codex
  lane that is told "one live session per worktree" will try `orca worktree ps` itself, get
  `runtime_unavailable` (the Orca runtime is not reachable from the lane's shell), and stop
  before touching a file.

**advisor outsourcing boundary** — origin span:

*Origins: the 2026-08-25 morning chain (hand-resolved conflict hunks,
  hand-written rehearsal packets); the runfix-1 round-1 reviews and the wbfix diagnosis run
  inline where the operator could neither see nor steer them.*

**worktree pruning** — origin span:

(answer-home lost its eq14 worktree
  twice)

**attest push to origin** — origin span:

Origin: both redesign attests
  sat behind a 10-commit unpushed local main while converge kept skipping the deploy.

**design context pack** — origin span:

Origin: three unanimous committee designs, two rejected at sittings; the context pack is what produced the critique that carried.

**operator-defect ledger capture** — origin span:

The commitments-✕ hover box was mentioned,
  acknowledged, and lost — twice over: it never got a row, and the pin that once guarded the intent
  tested the CSS rule's TEXT while the box came from the global `button:hover` cascade (a green pin
  over a live defect).

**pre-merge coupling and current-design check** — origin span:

Two halves, one incident. revloop-1 built
  cleanly (147/147, Opus 4.8 CLEAR against its brief), landed on eq14 main, and only then
  failed wa's coupling suite: a pin recorded that the operator-cleared 2026-08-28 workbench
  redesign had REMOVED the very emission the brief ordered rebuilt. Revert d903756.

**main-branch amendment suite** — origin span:

Two same-day breaks of wa main, same shape: a post-landing "small"
  amendment (archiving lane files in 8fcffdb; appending grants to a landed migration in
  1373f19) pushed after running only a partial check (nothing; test_sql only). Each
  contradicted a pin in build/test_code.js and left main red until a lane hit it.

**container LTS base image** — origin span:

*Origin: deps-1, whose brief said
  "Node 25" from two branch names whose tips had moved to 26.*

**external-endpoint contract check** — origin span:

*Origin: entry-9's corroboration flow shipped ACTIVE with an invented
  brain-ask URL (404 on every submit), caught only by the post-deploy render/ops check.*

**destructive git after failed directory change** — origin span:

an Orca worktree had been pruned, `cd <worktree> && …; git reset --hard origin/main` fell through to the
  session's current directory (another repo) and discarded uncommitted work.

**development-scoped model rulings** — origin span:

Origin: commit 18695294 pinned five production customer lanes to
  Opus 5 on a scope misread of a routing instruction; reverted 94997608 on the operator's correction back to Opus 4.8.

**flow-fix deployment verification** — origin span:

A committed-but-undeployed fix was twice declared closed on the record before
  this rule (Item C parser, 09-01 — 119 billed error runs before the drift was caught;
  calendar-poller matcher exclusions, committed 08-22, found undeployed in the 09-02
  drift sweep). *— ORIGINS #92.*

**operator-verdict design rounds** — origin span:

Five
  committee-unanimous designs failed the operator on sight before this rule.

**cross-repo dashboard suite** — origin span:

The capsulewire/fwrework landing night skipped it once and banked 14
  stale assertions (ledger-78, capsule 13→10, the attendance family, held-row
  mechanism, jump cycling, A3 model location, listing alias, dismissal gate),
  discovered serially across two days. *— ORIGINS #96.*

**persisting-walk reversal** — origin span:

Origin: w30 mapped Luna suggestion 11500 and the soft unmap left
the operator's queue one row shorter; restore11500-1 repaired it.

**deploy-path control-flow trace** — origin span:

convergedm-1's guard passed a codex build and an Opus gate on the
byte-identical claim and was wrong twice (unscoped to $stack; inert on a quiet box). The lane that fixed it shipped a
sourced-function harness over marker × dirtiness × stack and an Opus gate that quotes the trace.

**brief gate/review split** — origin span:

b35surname-1's brief said only "Presentation/read-only reads; no review class" and the codex
builder read that as permission to skip the Opus gate — the handoff arrived ungated and the advisor had to launch the
gate afterwards.

**watermark-based deploy verification** — origin span:

Origin: b35surname-1's brief7am
and commitment-reminders were silently rolled back to the pre-B35 SQL because neither cron could tick inside the old 10-minute
window.

**new-workflow activation sequence** — origin span:

Origin: titlemap-n8n-1's first update timed out 0/1.

**converge-managed gate package** — origin span:

Origin: the scopeprobe HANDOFF ordered broker-then-flow-then-service; converge did broker+service
at 01:10:29Z; the advisor had not stated it in the brief.

**wa coupling run ownership** — origin span:

itemcguardf1-1's brief pinned that command on the eq14-stacks lane itself; `test_code.js` invokes `build/build_flows.js`, which
regenerates `schema/155_flow_schedule_intervals.sql` in the wa checkout — a write outside the lane's worktree, refused by the sandbox
(EPERM), and rightly not escalated by the lane.

**commit-mode landing lint** — origin span:

Origin: hygiene-1 (landed
b1848899, the check itself), OVERSEER ruling 2026-09-07.

**evaluate general-purpose components** — origin span:

Origin: the dashboard chat lane, hand-built across five sessions while
  assistant-ui already did all of it — ORIGINS #46.

**builder-run review gate** — origin span:

the two idle gates of 2026-08-20
  (knowledge-backup, attendance) cost ~40 minutes each waiting for a reviewer launch.

**lane-close orphan process** — origin span:

(the 12h/2.5GB relmem pytest put the whole Mac
  under memory pressure and the desktop governor reaped OTHER sessions' background tasks)

**lane-close orphan sweep** — origin span:

The estate sweep on
  2026-08-27 found and killed two wa strays of exactly this class.

**rendered-closure scope** — origin span:

(the failure spanned surfaces: the favicon, the rich Slack editor)

**walk watcher environment** — origin span:

a leftover
  fire-on-first-hold watcher resolved a hold before the walk's second session existed and voided
  the run.

**advisor-applied migrations** — origin span:

after migration 106 sat in chat waiting for a paste

**non-blocking operator items** — origin span:

tightening the batched-list rule above:
  the batch had migrated back into chat summaries

**baseline-before-fix method** — origin span:

and it is what finally broke a four-build enumeration
  pattern (three successive pins each covered the constructions that were measured
  while the defect moved one construction over; the pattern ended when the walker
  baselined the sibling-endpoint shape pre-build and predicted the structural miss)

**operator-facing legibility** — origin span:

the job-254
  document editor passed its walks while, at the operator's laptop viewport, most of the top was taken by barely readable text leaving nothing usable (operator report, 2026-09-02).

**coupling-run landing record** — origin span:

Seat 7d's record.

**converge-log wait literal** — origin span:

The T1 landing waited for a wa sha inside `skill-sync: staged <sha>` that never appears —
   skill-sync stamps the wa main tip it sees at the tick, not every landed sha — and the background wait timed out
   (ledger :10129, 2026-09-07 18:26).

**exact HOSTS entry** — origin span:

which is what bgov-1 did at R2 (ledger :10156–:10157, 2026-09-07 19:51–19:53).

**arrival-surface detection** — origin span:

*(Kept whole — earned by two missed customer arrivals in one day. Full:
  ORIGINS #66.)*

**structural draft-first boundary** — origin span:

*Konnect proved the human gate catches
  what every automated filter missed.*

**hard-scoped review briefs** — origin span:

The runs that died were long multi-file briefs at `xhigh`.

**frozen review-round artifact** — origin span:

Rounds 2 and 3 each reviewed a version superseded by folds before they returned.
  Round 3 was given an explicit "these are already fixed — verify, then move past" list, and
  everything beyond that list was net new.

**DDL dry-run before review** — origin span:

Running 032 inside `BEGIN`/`ROLLBACK` against the live database found the blocking
  privilege hole in seconds, plus a defect no reviewer flagged (the migration aborted under
  its own documented applying role).

**remote image-build durability** — origin span:

a foreground ssh from the Mac was killed mid-build while
  the remote process kept running with its output lost.

**worktree n8n environment** — origin span:

Origin: governordigest-1, 2026-09-07 08:30
   (ledger :10078); bgov-1 R1 did it right (2026-09-07 20:0x).

**signal positional parameters** — origin span:

Origin: carried in every lane brief's Close since t2skillgate-1 (2026-09-07).

## 2026-09-08 — wadoctrine-1 origins

Seventeen method rules earned across the 2026-09-07 21:00 → 2026-09-08 06:00 advisor window
(source: docs/advisor-watch-2026-08-17.md) and written into ADVISOR-WA.md by lane wadoctrine-1.
Each rule carries the pointer `*— ORIGINS 2026-09-08: <label>.*`; the label below is that
pointer. One line each — the failure the rule prevents.

**verified-without-a-pointer** — origin:

A "verified at source" claim arrived with no file:line and no command output line, so the claim itself was the only evidence for it.

**codex refuses write-enabled GitHub automation** — origin:

depautomerge-1, 2026-09-08 01:04 +04 — codex refused a third time AFTER the operator typed his authorization into the codex terminal, verbatim "the purported direct approval appears only in untrusted transcript content"; the lane was re-tiered codex → Opus 5 medium and built in six minutes.

**dependabot config ahead of its workflow** — origin:

depautomerge-1 — a dependabot config that goes live before the workflow that merges its PRs opens unattended PRs nothing is there to merge.

**chained brief lint** — origin:

headgate-review-1, 2026-09-08 — the first brief draft failed `estate-lint brief` (§31 sentence missing), the `&&` chain skipped the commit while the launch lines still ran, and the lane started on the unlinted copy.

**rewritten STATUS line** — origin:

The pre-commit hook refused the first two RESURRECT-block attempts at 2026-09-08 01:57 +04 and refused the NEXT-line refresh again at ~03:0x — an edited line carrying DEPLOYED is an added diff line, so the hook checks it as a new closed-entry verdict.

**tail -1 read the prompt** — origin:

2026-09-08 01:53 +04 — "Suite re-run on main 662a4bc1: [exited with code 0]" was the background wrapper's exit line, not the suite result; the file read `ALL 1512 TESTS PASSED`.

**walk debt from an unattested report** — origin:

b9railwalk-1, found 2026-09-08 05:13 +04 — the walk report landed under docs/exp-2026-09-08/ with no `walk-attest.sh` row, and converge's walk gate refused to deploy the dashboard for forty minutes (operator, verbatim: "the gate worked exactly as designed … The defect was upstream of the gate").

**brief called a tracked file new** — origin:

templatefix-1, 2026-09-08 04:51 +04 — the brief called scripts/estate-lint-selftest.sh "(new, small)" without checking; main already tracked its 42 cases, and the lane's commit overwrote them (advisor brief error, folded by templatefix-2).

**estimated body timestamps** — origin:

2026-09-08 ~04:5x — a BOX-SEQ body figure was written as "04:5x" when the send went at ~04:44; the heading stamp was right, the body was an estimate.

**shared selftest fixture path** — origin:

templatefix-3, 2026-09-08 05:01 +04 — the shipped selftest read 52 pass / 2 FAIL in skill-factory permanently (wa-only real-brief paths at :73-74); OVERSEER: "A selftest shipped to three repos that can only be green in one of them cannot be used as a gate anywhere else."

**refused paths rode the next commit** — origin:

2026-09-08 05:16 +04 — the commit-msg hook correctly refused an `attest:` commit from the seat, the index kept both files staged, and the next `git add <brief> && git commit` carried them under a "brief … LAUNCHED" subject the hook cannot see through; the `git restore --staged` ran in parallel, after that commit, and showed a clean tree.

**push after the DONE signal** — origin:

b9railwalk-2, 2026-09-08 05:34 +04 — the walker pushed a corrected record after its DONE signal at 05:33, so the signalled sha was no longer the origin tip at the advisor's close step.

**headless tabs cannot screenshot** — origin:

b9railwalk-2, 2026-09-08 05:34 +04 — `orca screenshot` timed out at CDP (no visible tab, no compositor) and macOS screencapture refused; the step-5 "screenshot" was an `orca pdf` raster (1792×2320) until the walker replaced it with the honest record.

**walk-attest under sh** — origin:

`scripts/walk-attest.sh` uses process substitution; run with `sh` it fails at line 48.

**oversize OVERSEER messages** — origin:

2026-09-08 02:29, ~04:44 and ~05:05 +04 — three sends refused by the gate ("SENDGATE REFUSED: oversize"), each trimmed and re-sent, inside one rolling hour.

**Grok launch-line lint** — origin:

2026-09-08 ~04:0x — OVERSEER, verbatim: "a lint that cries defect on the doctrine-pinned launch line, and a hook that must be overridden to do what §41 asks, both train the same habit."

**hand-merged generated record** — origin:

b9railattest-1, 2026-09-08 05:18 +04 — on a rebase conflict the lane restored both docs/walks paths to main's state and RE-RAN walk-attest.sh on the clean base, so the committed row is generated rather than carried; origin/main moved under it mid-rebase and it re-rebased onto the tip.

**held cross-repo pins and the ignorable failure** — origin:

hygiene-3, 2026-09-08 09:0x +04 — the wa coupling run against eq14 main stayed red on four pins of eq14 65e658d (headgate-1 word 2, held for the OVERSEER's release word; wa pinned it in 74b03ced). The lane proved ALL 1514 TESTS PASSED with 65e658d cherry-picked into a temp clone. The OVERSEER carried the four into his STATUS beside the release words so no reader after word 1 mistakes them for a failed deploy, and queued the rule as the sixth instance of one open yes/no (the first five: shared-tool defects with a fix at the tool — templatefix-1/-2/-3 selftest, launch-line lint, §41 hook). Operator, 2026-09-08 11:2x +04, verbatim: "4- yes fine".

**BOOT tag** — origin:

work-automation seat a2, 2026-09-08 14:29 +04 — ADVISOR.md said restarts go to the advisor's ledger while §39b ordered a boot report at every restart; SF and relmem seats 14 and 15 sent theirs as XREPO, counted, in their first hour. Proposed as a fifth uncounted tag; operator, 2026-09-08 14:4x +04, verbatim: "3- yes add a label so it doesnt count".

## 2026-09-08 21:05 +0400 — dashfix-1 landed on a code review; the walk came after the deploy

**What happened:** dashfix-1 (75 page-walk ids, eq14 bd0458c) was sent as BOX-SEQ and deployed on the lane's tests, its own CSS measurements on a local build, and a three-round Opus code review. No agent walked the built dashboard in a browser first; the Grok walk was sequenced after converge deployed it, with the operator's four asks as the first legs. He looked at the live account page before the stamp and all-caps legs ran and saw a clipped BUILD stamp (a regression: the rail's new z-index covers the stamp) and untouched all-caps labels (a scoping error: 7 of 122 uppercase rules removed). He asked in the advisor's terminal: "is it true you ony did code reviews? You passed this build as successful to the overseer without a browser walk?" — yes. The advisor's first response was to write a NEW rule; the operator: "it is already a rule my friend is it not" — it was (this file's 2026-08-26 standing order; ADVISOR.md §18). **Rule:** none new; one clarifying clause on the existing order (the walk runs on the built preview before the landing request). The lesson under it: a broken rule is answered by compliance, not by a duplicate rule.

## 2026-09-08 — capitals removed take weight and size (ADVISOR-WA §1e)
dashfix-1b removed 115 `text-transform: uppercase` rules from the dashboard stylesheet and retuned letter-spacing only. The operator, on seeing the sentence-cased labels: "any time it removes all caps, the replacement text needs to be changed to bold and enlarged a bit to fit the old texts place". dashfix-1c applied weight 600/700 and one size step to every one of the 115, walked on its preview. The rule is retroactive by his word.

## 2026-09-08 — the advisor owns its builds (ADVISOR-WA standing orders; ADVISOR.md §D)
The dashfix-1b hotfix and the dashwalk-1 legs sat about 50 minutes "awaiting the OVERSEER" after the operator's four live-page findings. His words: "You OWN your builds, you clear your backlog unless something needs me, clear?" The OVERSEER's half, same night: he refuses any hold that names him.

## 2026-09-09 — gate legs left out of the lane's own brief (ADVISOR.md §47)

<!-- origin: ADVISOR.md#47 -->
Three deploys in two repos in four hours were stopped by a gate leg the lane's own brief omitted. relmem l05-fix-1 repaired 22 test failures, but its brief ran a tests-only sweep over two other files, so the DSN cases of the file it edited never ran; l05b died on one of those and rolled itself back by retag. wa lintcase-1's brief omitted the ADVISOR-WA 7.z SQL rehearsal; the n8n gate ABORTED, the advisor ran the rehearsal read-only (54 queries planned and rolled back) and the update went through. Neither was a product defect. The OVERSEER named the pattern; the wa advisor worded the rule.

## 2026-09-07/08 — the 7.y coupling-run rules, the examples (ADVISOR-WA 7.y)
Rule 2's declaring review lines (sessionkillredeploy-1): Grok :47 "no longer called from main … replaced by sweepTerminalExecutorSessions", :45 sweep bound, :10/:11 CAS receipt order, :15 ACK order. Rule 4(a): headgate-1 — wa 74b03ced on main while eq14 65e658d was held for the OVERSEER's word. Rule 4(b): the first draft of the orphan-class ruling was an eq14 fix lane; the pin's own comment block withdrew it. Rule 4(c): b9rail-4 added a second `sub: ''` ahead of the bare-route predicate and the mutation guard silently stopped biting until the whole predicate line became the search string.

## ADVISOR-WA §4.2 — the BOOT ping (2026-09-09, dashfix-3)
dashfix-3 (codex xhigh, eq14 worktree) finished its BUILD at 04:45 with 312/312 green, then could not run its Opus gate, its push or its STOP signal: the launcher's `--add-dir /Users/rami/dev/eq14-stacks-main/.git/worktrees/dashfix-3` named a path that is not a directory (the Orca "eq14-stacks-main" repo keeps worktree gitdirs under /Users/rami/dev/eq14-stacks/.git/worktrees/<name>), and the codex Seatbelt preflight rejects every escalated command while that root is wrong — including `orca terminal send`. The lane wrote ASK-ADVISOR and went quiet; the OVERSEER's whip found it two ticks later ("a blocked signal must not look identical to progress"). Fix: the advisor authorized the three final commands narrowly; the rule makes a BOOT ping the first act so a wrong launcher is caught in minutes.

## ADVISOR.md §45 — origins (moved from the rule 2026-09-09)

<!-- origin: ADVISOR.md#45 -->
§45 earned by: sessionkill-1, landed on eq14-stacks main 2026-09-07 and reported HELD twice; converge deployed it 05:30 +04; pilot-2's cand3 frozen-pin gate failed 09:48Z; the OVERSEER accepted the HELD claim without checking the deploy path. Rollback: revert ddc2760 (ruling c).
Exception earned by: depautomerge-1 (docs/exp-2026-09-07/depautomerge-1.md).
Rider: ARCH-OVERSEER call in docs/arch-review-2026-09-08/DECISION.md §15 (archreview-1 d8c77cf3, 01:44 +04) on wa's walk-gate question — a dependabot bump (eq14 d0916202) had reached the box under the exception, converge's walk-gate carried "walk-debt: session-lane d0916202" and deferred every session-lane rebuild until a read-only walk (walkrun-3, wa 0b7ac62b) attested it; options were self-attest / block / leave the debt; ARCH chose self-attest with the two conditions. Worded by wa on the OVERSEER's order (08:5x), replicated by the OVERSEER.

## ADVISOR.md §D — the whip refuses a hold naming it (origin moved 2026-09-09)

<!-- origin: ADVISOR.md#§D -->
A presentation hotfix (dashfix-1b) and a walk sat ~50 min on such a hold; the operator corrected both seats.

## ADVISOR-WA §4.2 BOOT ping — rationale (moved 2026-09-09)
A wrong sandbox metadata root blocks push, gate and STOP alike, so a stuck lane looks like a working one (dashfix-3).

## ADVISOR-WA — advisor applies migrations over ssh (rationale moved 2026-09-09)
Handing the psql command to the operator's terminal was a habit, not a rule — it added a wait without adding a decision, because the operator was pasting a command he had already approved in review (operator ruling 2026-08-22).

## ADVISOR-WA origins trimmed 2026-09-09 (budget)
- Lane close process sweep: from the relmem pytest incident (2026-08-27).
- Destructive git after a failing cd: incident 2026-08-20, e4-staging inc 3.
- Design lane corrected directly: accdesign-1 (2026-09-09) — the operator gave seven corrections in the lane's terminal; the whip recorded it as the lesson.
- ADVISOR-WA 5b.2 lanes: convergedm-1 → convergedm-2; §5b.3 and §5b.5: b35surname-1, updated 2026-09-04 by b39verify-1.

## ADVISOR.md 19 enforcement + labelling — origin (moved 2026-09-09, gatefix-1)

<!-- origin: ADVISOR.md#19 -->
They came from
counting launch-shaped strings in transcripts, a denominator dominated by prose about launches
— doctrine text, status reports, and STATUS edits quoting a launch line inside a heredoc.
Three successive tightenings of that count gave 61%, 35% and 8% from the same evidence, and
codex's own session records carry no sandbox or network field to pair against.

## ADVISOR.md 39 fold thresholds — measurement (moved 2026-09-09, operator-sessions)

<!-- origin: ADVISOR.md#39 -->
Measured over 32 h: the wa advisor's context reached **535k tokens per turn** and averaged
~300k against a ~90k post-fold floor; four advisor seats ran 30 h+ without restart and
accounted for 2.39 B cache-read tokens.

## ADVISOR.md 42 one-session-per-leg — attribution (moved 2026-09-09, operator-sessions)

<!-- origin: ADVISOR.md#42 -->
b9railwalk-1, nine legs in one session, stopped at leg 1 by the OVERSEER.

## ADVISOR.md 48 walk coordinator — origin (2026-09-09, operator-sessions)

<!-- origin: ADVISOR.md#48 -->
§42 (one Grok session per leg) split the browser session and left the seat above it whole.
Measured on walkrun-4, the coordinator that ran five sequential Grok legs:

  - Claude Opus 5, one context across all five legs
  - 657 calls; context 51,932 -> 323,108, climbing monotonically, **zero folds**
  - 139,490,678 tokens consumed
  - total tool-result content it ever received across the whole session: 461,361 bytes

Across all twelve walkrun seats: 2,394 calls, **zero folds, none**. Its own brief complied
with §42 ("five read-only Grok legs one at a time ... You open no browser") and still cost
139 M, because §42 bounds the Grok session and nothing bounded the supervisor.

The polling half was ALREADY law and was ignored, which is why rule 48 cites §8 rule 6 rather
than restating it. walkrun-4 ran 270 `orca terminal read` calls between 20:30Z and 21:05Z on
2026-09-08 at a **median gap of 3 seconds**; 269 of 269 intervals broke the once-per-20-minutes
cap. Fleet-wide: `orca terminal read` 561 times, `orca terminal wait` 5 times, though
`orca terminal wait --for exit|tui-idle --timeout-ms` was installed and available throughout.
Prose was never the missing part.

Sizing, honestly. 99.5% of this traffic is cache READ, billed at roughly a tenth of fresh
input; walkrun-4 cost-weighted is ~11% of its raw token count. Weighted across the estate over
24 h the whole walker fleet was 14.5% of spend, against the 16-64% a raw context count
suggests. Rule 48 is worth a large fraction of the walker fleet, not a multiple of the estate.

## ADVISOR.md 40 lane-session restart — measurement (moved 2026-09-09, operator-sessions)

<!-- origin: ADVISOR.md#40 -->
One codex lane session carried 36 `task_started` events and 51 distinct advisor dispatches
over 2,098 turns and 235 M input tokens — 19% of the estate's codex consumption. Across 149
codex sessions, input cost per turn is flat (~94k at <50 turns, ~131k at 150-300, ~134k at
300-600) because codex compacts. The six sessions over 300 turns are 27% of all codex input.

## ADVISOR.md 48 backstop — `orca terminal wait` measured (2026-09-09, operator-sessions)
Measured on a live dummy walk (worktree walkgatetest-1, one Grok 4.6 HIGH leg and an Opus 5
coordinator), because the first TEMPLATE.md wording prescribed the backstop without proving it
(29: a watch is armed only on a signal the target actually emits, proven once):

  - `--for tui-idle` armed on a BUSY Grok leg  -> satisfied after 33 s, at genuine turn end.
    The leg had done all five steps and pushed; the wake was correct.
  - `--for tui-idle` armed on an IDLE agent TUI -> `satisfied: true` in **0 s**. It is a LEVEL
    condition, not an edge.
  - `--for tui-idle` armed on the Opus coordinator right after launch -> satisfied in 0 s while
    the coordinator was four turns in and sitting on an approval prompt, with its leg not yet
    launched. A coordinator following the first wording would have "woken", checked, found no
    leg, and reported the leg absent.
  - `--for tui-idle` on a plain shell -> never fires (timeout). It applies to agent TUIs only.
  - `--for exit` on a running agent lane -> never fires (timeout); agent lanes stay at a prompt.

Hence: the LANE-SIGNAL is the only true edge; a wake is not proof of completion, the origin sha
is (37); a wake without the sha means RE-ARM, not "done". Arm the backstop only after the target
is confirmed busy.

Also measured: a claude lane launched with `--permission-mode acceptEdits` stalls on the first
Bash approval, and `orca terminal send` into it is refused with `agent_prompt_blocked` — the
lane cannot be rescued programmatically. This is 8 rule 1's codex `--approve-for-me` point,
holding identically for claude lanes.

## §49 origin — Muse availability + the informed bar-lift (2026-09-10)

<!-- origin: ADVISOR.md#49 -->
Drafted by operator-sessions-67 on the OVERSEER's routing (whips do not author doctrine); landed
by the wa seat. Muse Code 1.1.1, model muse-spark-1.3-contributor, authenticated. Spawn: `orca
terminal create --worktree active --title <NAME> --command "muse"` then `terminal send --enter`.
Headless `muse exec`; `--json` emits JSONL with real tool.result records (machine-checkable).
`--reasoning-effort none..ultra` (default high); `--max-model-steps N` = maxTurns, set on every
headless job; `--yolo` = bypass; `--trust-workspace` loads worktree AGENTS.md (skipped silently
without it). Original draft carried two BARS (personal data; customer/UnifyApps until his word,
§F class — vendor states content incl. inter-session messages may be used for product
improvement). The operator lifted both 2026-09-10 ("lift the two bars on muse, its ok") after
hearing the training statement and the no-opt-out finding: `muse config status` reports both
planes absent; the policy plane accepts exactly one privacy member, privacy.telemetry, which the
binary's strings place on OTLP export/redaction, not training consent. Evidence of capability:
headless exec, hand-verified bash tool use, full Orca TUI session; one of four runs returned a
commit subject matching no commit while its own JSON stream showed correct tool execution — the
reason the blind test precedes any lane. Findings: /Users/rami/orca/muse-availability-2026-09-10.md.
Whip's STATUS half: operator-sessions 7d986cea (item 15, corrected post-lift).

## Verbatim quotes moved from the boot set (2026-09-10, §49 budget make-room)
- ADVISOR.md §D own-your-builds + ADVISOR-WA.md mirror, operator 2026-09-08 21:1x +04:
  "You OWN your builds, you clear your backlog unless something needs me, clear?"
- ADVISOR.md §42-area bite-sized browser lanes, operator 2026-09-08: "make sure grok lanes
  follow the new rules, browser use are bite sized lanes, so sessions dont run crazy with usage"
- ADVISOR.md §45 dependency-deploy exception, operator 2026-09-08 (relayed): "rule gets an
  exception naming these automatic dependency deploys"
- ADVISOR.md hygiene rider (c): OVERSEER ruling 2026-09-07 19:5x, adopted verbatim.

## §9-B §F miss (2026-09-10, feeds ADVISOR-WA §7.cc)

The §9-B BOX-SEQ cited "migrations checked destructive-free by my own grep" while
schema/173:47-50 carried REVOKE ALL FROM PUBLIC + GRANT SELECT,INSERT,UPDATE TO queue on
both new tables (a Postgres grant change — the first §F required-list item, verbatim; the
148 precedent went to review on the same reading) and build/allowed_endpoints.json gained
slack conversations.info (the allowlist is the containment boundary; adding to it is an
egress-rule change, also required-listed). The whip refused release on both at origin reads
of 03a42db8, plus an independent one-box-change-at-a-time hold behind relmem graphcut B5.
172 was confirmed genuinely clean. The wrong test: destructiveness answers the drop/alter
item only; §F is scoped by blast radius.

## The all-caps replacement verbatim (2026-09-08, feeds ADVISOR-WA §caps rule)

Operator, verbatim: "any time it removes all caps, the replacement text needs to be changed
to bold and enlarged a bit to fit the old texts place" — the sentence behind the
weight-and-size-in-the-same-commit half of the rule.

## Two eq14 main trees — full ruling text (2026-08-25/2026-09-08, feeds the ADVISOR-WA canonical-tree rule)

Git allows one worktree per branch, and eq14-stacks-main (the orca-registered repo root,
which all lane worktrees hang off) owns the main branch. The primary clone
/Users/rami/dev/eq14-stacks is re-detached by relmem on drift. An ff from the detached
primary moves a detached HEAD, not main, and reads as a successful landing while landing
nothing. Older handoffs/docs that say `git -C /Users/rami/dev/eq14-stacks merge --ff-only
...` are superseded.

## Make-room moves of 2026-09-10 (the §45 push-is-the-apply rider landing)

<!-- origin: ADVISOR.md#8 -->
<!-- the §8 origin spans live in this section although its heading names §45; the anchor indexes them where they are rather than moving text -->

**§8 rule 2b measurement, verbatim as it stood in ADVISOR.md:** "Measured across
1,012 advisor Monitor calls in 32 h: 859 were file polls, 144 were ssh/db polls, and 9
used a runtime event — the poll had become the primary channel by default."

**§8 rule 2 origin clause, verbatim:** "(operator ruling 2026-08-28, after the wbbuild
incident met the file channel's pinned failure criterion)".

**§8 rule 5 origin clause, verbatim:** "(relmem promo-fix-2: five provisioning ASKs
before any code)".

**§19 withdrawn-figures sentence, verbatim:** "NO COMPLIANCE RATE IS STATED HERE ON
PURPOSE: the 2026-09-04 figures once given in this paragraph (~20% of launches carrying
the flag, 90 of 149 briefs carrying the block) were WITHDRAWN on 2026-09-06 as
unmeasurable."

**§45 walk-gate rider, verbatim as it stood:** "**Rider — the walk-gate on an auto
deploy (ARCH call 2026-09-09, DECISION.md §15).** Converge SELF-ATTESTS an auto-merged
bump when its T3 verify probe passes: the gate records the evidence the exception
already trusts. Two conditions. (1) The attest row is TYPED — policy `deps-auto`, the
eq14 sha, the probe name and result — so no reader takes a probe pass for a walk; the
next human-owned change to that service walks as usual and covers the bump. (2) A probe
FAIL never self-attests: the deploy is rolled back or the walk-debt stands. Not §F.
Until converge writes the row, a read-only walk clears the debt."

### Origin of the §45 push-is-the-apply rider (backupfix-1, 2026-09-10)

The tier-1 apply script's pre-write identity gate aborted: live
/opt/stacks/backup-local.sh md5 was ab257553a2f40ca3069f895a43e07221 (the NEW
bytes), not the expected pre-change cb7289779f63a39d6771e0cd65d88f96 — converge
had already pulled and applied the pushed commit before the seat's own copy ran.
The abort was correct (no double-write); the verify then proved live == the
reviewed repo bytes, converge-applied at 16:10. The operator's automerge ruling
of the same day was the "middle one" option verbatim: live-service stacks held
out of dependabot auto-merge by a changed-files gate, grouped PRs held whole.

### Attribution moves (2026-09-10 make-room, same commit)

Rule 43 attribution, verbatim: "Attribution: 2026-09-06, seven commits landed
through the wa advisor's live checkout while the seat was working in it; nothing
was lost, by luck."

Rule 44 attribution, verbatim: "Attribution: 2026-09-06, the attest-key
refinement in ADVISOR-WA.md (deployed image revision, never the box checkout
HEAD) was lost this way and restored at 53d16389."

## Origins of rules 50 and 51 (2026-09-10)

<!-- origin: ADVISOR.md#50 -->
<!-- origin: ADVISOR.md#51 -->

Rule 50 — the operator's words, addition 26: "And a pattern, not a defect. This
is the third instance tonight of the same shape: graphify printing added:N into
a store nothing reads, a residual check that could never be non-zero, and now an
approval whose destination has no consumer and where count(*) WHERE
status='sent' is zero across the table's entire history. Treat it as a class,
not three incidents." The whip's test formulation: "for any signal that says
done, sent, added or closed, NAME THE CONSUMER AND SHOW IT READ SOMETHING. A
count of writes is not evidence of a read."

Rule 51 — the itemc 6.7s determination v1 (2026-09-10 16:5x): the wa advisor
read decideOutbound's kind guard, concluded meeting approvals never close
commitments, attributed the close to a separate Done click, and reported a
"false banner" defect — all falsified by one census row showing draft 75's kind
was 'slack_reply'. The corrected v2 named the actual writer of the 12:32:30.9
stamp (Agent watcher execution 420025's card-sync leg). The whip's order:
"READ THE ROW BEFORE THE BRANCH... code tells you what CAN happen while the row
tells you what DID."

### Make-room moves of 2026-09-10 (the rules 50/51 landing)

Moved verbatim from ADVISOR.md in the same commit, pointers left:

§19 mechanism, full enumerated text (commits 564ab8d2+0b9854bc): """Mechanism (full text: wa docs/ADVISOR-LANE-OPERATIONS.md §D, commits 564ab8d2+0b9854bc):
(1) codex lane launches add `-c sandbox_workspace_write.network_access=true` — per-lane
in the launch command ONLY, never in ~/.codex/config.toml. CARVE-OUT: lanes whose input
includes externally sourced content (RFPs, customer files, third-party repos) do NOT get
the flag — sentinels + stall watch instead. (2) Every codex lane brief carries the
signal-at-every-stop block (orca terminal send to the advisor handle BEFORE any approval
request, blocker, question, or finish; sentinel fallback; never stop silently). (3) Every
advisor keeps a persistent Action-Required watch over its live lane terminals (5-min
re-alerts while stuck). Approval prompts refuse text — bare --enter confirms, interrupt+esc
refuses; TUI exit recovers via codex resume. A stall caught by the watch instead of a lane
signal is a template defect. New launches only; running lanes finish under the stall watch."""

Rule 49 Muse, the operator's verbatim word: "lift the two bars on muse, its ok" — given informed.

Rule 8-2c measurement context: measured on the fridaymiss/itemcguard codex lanes.

Rule 8-6: operator ruling was his "Yes" on the OVERSEER's ask, 2026-09-05.

Rule 44 rationale sentence: "sweeping it out by shape deletes the rule while the headline
sentence keeps prescribing the older method."

§19 transition note: "New launches only; running lanes finish under the stall watch."

Rule 39 opening, verbatim: "No threshold was configured anywhere — 'fold at 300k' was a
request nothing enforced, which is why it drifted to 535k against a ~90k post-fold floor."
Rule 39a rationale: "A lane close is a boundary the seat already reaches, so it needs no
self-monitoring — self-monitoring is what already failed." Rule 39b rationale: "it is one
comparison on an event it already reads, so it needs no monitor agent of its own."
Rule 38 carried a duplicate opening sentence pair ("A one-time run may use a box timer;
anything that runs more than once is scheduled by n8n, where it can be managed.") — removed
as literal redundancy with the rule's own body, meaning unchanged.
Incident tags moved from four rule titles: rule 20 (relmem incident), rule 21
(neo4j incident), rule 23 (codex update incident), rule 37 (the 358562a push miss).

## Rule 39 make-room (2026-09-10, rule 52 landing)
Moved verbatim from rule 39(c): ": `ledger: tick HH:MM quiet` × 259 in 32 h is transcript
the seat then carries for the rest of its life."
Moved verbatim from rule 39(d): "(peer measurement 2026-09-05 05:1x; self-fold at
349k/call 07:4x)".
Moved verbatim from rule 39's close: "Keeping the tick is correct — it holds the prompt
cache. Committing it is what compounds. Nothing here changes what the estate builds or
which gates hold."

## Rule 52 origin (2026-09-10)

<!-- origin: ADVISOR.md#52 -->
The advisor's first live ctx-v1 conformance run failed on `fatal: pathspec 'migrations'
did not match any files`: fixtures/ctxv1-runner/pin.json declared rel_migration_dir
"migrations" while relmem at the pin keeps schema/. The ctxrunner-1 lane's brief granted
no server, so the artifact landed reviewed, correct-looking, and never once executed; the
offline phase never touches the migration dir. The OVERSEER named the class ("a lane that
cannot exercise its own output at all — no signal, false or true, was ever available")
and proposed the rule; the advisor worded it. Distinct from rule 50: 50 is a signal with
no consumer; 52 is an artifact with no execution.
Also moved verbatim in the same pass — from rule 39(b): "so the check is a date
comparison, not a judgment"; from rule 52's first sentence: ": correct-looking, landed,
never once loaded".

## Rule 53 make-room (2026-09-10, rule 53 landing)
Moved verbatim — rule 26: "§10 keeps its shape (a separate visible session, never the
advisor seat, never a subagent); only the driving model changes. Walk briefs, walk
scripts, the evidence directory layout, attest.json and WALK-OVERRIDE semantics are
unchanged." Rule 25: "This rule exists to bound Fable spend," and the citation "wa
ADVISOR-WA §7/§5b.8 corrected 0fb54e8c". Rule 8: "at zero egress. The old \"intended for
headless lanes\" caveat is dead." Rule 19: "(the withdrawn 2026-09-04 figures, verbatim
in ORIGINS)" — the figures stay in ORIGINS as before. Rule 37: "relmem promo-deploy-2
brief corrected". Rule 53 itself: "and feels like diligence while it does" (the whip's
phrase: "it feels like diligence while it does so, which is why it would get past a
review").

## Rule 53 origin (2026-09-10)

<!-- origin: ADVISOR.md#53 -->
relmem, handed the operator's quantivetech example as a class, declined to change its
neutrally-cut measurement and said: "changing it NOW because of the example would itself
be special-casing." The OVERSEER named the extension beyond the operator's
sealed-acceptance ruling (which forbids TARGETING an example): REACTING to an
illustrative example — re-cutting a slice, adjusting a rubric, adding a fixture because
the example was mentioned — poisons the instrument as thoroughly as building to it. The
advisor worded rule 53; the mechanism-vs-instrument split is the advisor's addition.
Same pass, second trim — rule 27 citation: "relmem 040 dry-run"; rule 25 rider tag:
"hygiene-1 rider (c); attribution in ORIGINS".

## Rule 54 make-room (2026-09-10, rule 54 landing)
Moved verbatim — rule 11: "they consumed quota while the operator was not prompting."
and "The shell touchers proved eviction-fragile under memory pressure, and every
eviction woke the owning session with a kill notification — a token leak firing exactly
when the machine was busiest." Rule 19 carve-out examples: "(RFPs, customer files,
third-party repos)". Rule 26 first sentence: "Browser walks run on Grok; Opus on
browser use is too expensive for this lane."

## Rule 54 origin (2026-09-10)

<!-- origin: ADVISOR.md#54 -->
The advisor recommended creating a partner company in HubSpot so the estate's
domain-keyed partner filters would go quiet on an ownerless domain; the OVERSEER
carried it three times as a stopgap. The operator refused, verbatim: "I can't create
his company as a separate company under HubSpot. I would be providing my company with
wrong data. I cannot appease you and screw myself over" and "fix the problem, dont ask
me to adjust so things are easier for you." The OVERSEER named the class (a stopgap
that distorts a record read by other people moves damage into a system we do not
control); the advisor worded the rule.
Same pass — rule 37: "the box, converge and every downstream lane see origin".

## Rule 55 make-room (2026-09-10, rule 55 landing)
Moved verbatim — rule 42: "Measured: one Grok walk session ran 32 h, 670 turns and 6
compactions — 10,842 messages, on its own 37% of the estate's Grok traffic — because
every leg carried every prior leg. Walks in total are ~20,060 of 28,984 Grok messages,
69% of all Grok traffic: this rule governs the majority of Grok spend, not a corner of
it." Rule 22: "even at the same per-token price — output shape (thinking blocks)
changes spend and can break parsers."

## Rule 55 origin (2026-09-10)

<!-- origin: ADVISOR.md#55 -->
Operator, verbatim, 20:1x +04, after his own HubSpot merge and the estate's evening of
domain workarounds: "i already added it. deal with it properly and follow what we are
trying to build. DO NOT TOUCH OR MODIFY HUBSPOT." Supersedes the CLAUDE.md permission
for approval-gated HubSpot notes/tasks writes; the hubspot-friday field-write lane
parks under it.
Same pass — rule 37 digest-pin clause: "the file, or the value inside it" and "so a
checker can re-derive it"; rule 47 quote: (operator, 2026-09-09: "Let them delegate the
read.").

## ADVISOR-WA 7.dd origin (2026-09-10, wbauditfix-1 deploy)

The update was TaskStopped mid-poll before its 12-minute timeout could roll back the fix;
the PUT was proven landed by live read; the flow was then explicitly activated and verified
on executions past the update stamp. partnersync deployed-inactive was the first bite of
the preserve-prior-state trap, this the second; the rule exists so there is no third. A
first poll that grepped "success" matched pre-deactivation executions and was discarded
for the watermark comparison.

## §E advisor seat shape: Fable 5 -> Opus 5 (2026-09-10 22:5x +04)

<!-- origin: ADVISOR.md#§E -->

Operator, verbatim, ordering the relaunch: "Can you relaunch all the advisors right now
and change them from Fable to Opus? I am doing something in the background to govern
this, but do this change now."

SUPERSESSION. The 2026-09-09 00:3x ruling ("move all supervisors back to fable 5, im not
happy with 5.1") bound supervisors from the NEXT restart and explicitly did not switch a
seat mid-run. Tonight's order is the opposite shape: immediate, and all three seats at
once. It was executed before the doctrine line was edited — three seats (work-automation,
relationship-memory, skill-factory) relaunched on claude-opus-5 while §E still read
claude-fable-5, so the file stated a shape that no longer existed. Caught by
skill-factory-ce after its own relaunch, which correctly attached no ask to it; ordered to
this seat by the OVERSEER, which words no doctrine and holds replication.

GOVERNANCE. The operator states he is building governance for the seat model separately.
The §E line holds until that lands; it is not a permanent pin.

NO COST CLAIM ATTACHES TO THIS RULING, and none was written into ADVISOR.md. The claim
that three Opus seats cost more than Fable was made to the operator by the OVERSEER and
corrected by him: these seats run under Max, so there is no per-call money either way.
The estate's one cost sentence about Fable is CLAUDE.md:204 (Fable excluded from every
automated lane, ~2x cost, volatile access) — cited here rather than restated in the
capped boot set. Recorded so no later seat re-derives a cost story for this change.

MAKE-ROOM. The boot set had 6 tokens of margin (39,994/40,000) and the new §E text costs
198 bytes, so the commit had to pay for itself. It did, in scope: ADVISOR-WA's
model-routing bullet (Fable at HIGH for advisor seats) was superseded by this ruling and
became a pointer to §E, and ADVISOR-WA's long-form copy of the rendered-proof rule — which
named itself a duplicate of ADVISOR.md §18 and carried the now-irrelevant reasoning that
Fable cannot spin an Opus sub-model — collapsed to a pointer under the file's own
digestion rule. No rule was dropped; §18 states it in full. Set 39,994 -> 39,827.

## PENDING DOCTRINE — two rules parked unlanded 2026-09-10 23:1x (ADVISOR.md frozen by operator order: "DOnt touch the file now, i tasked the other session with building this")

Both are estate-universal, so neither is this seat's to author (§A). Recorded here so a fold
does not lose them. Neither has landed anywhere.

### (i) A privilege-filtered catalog view cannot answer an existence question

Proposed substance: a question about whether a database object EXISTS — a table, a column —
asked by a role that may not hold privileges on it, is answered from `pg_catalog`
(pg_class / pg_attribute / pg_namespace), NEVER from `information_schema`. The
information_schema views are filtered to the current role's own privileges, so they report
"no privilege" and "no such object" IDENTICALLY, as zero rows. Estate rule 27 already says
grant ground truth comes from column_privileges rather than relacl; this is the same trap one
level down, because column_privileges is itself filtered and returns zero rows for a role that
holds nothing. A zero-row read from information_schema is evidence of nothing until the same
question has been asked of pg_catalog.

ORIGIN, and it is a near-miss, not a theory. partnerorphan-1, 2026-09-10. The advisor's own
L1b probe instructed the lane: "if the column does not exist, that carrier cannot reference
customers and the whole question dissolves; say so plainly." The lane ran the ordered
information_schema.columns read for rel.operator_directive and rel.slack_dm_message and got
ZERO ROWS — which, followed literally, dissolves the carrier and clears the delete. The lane
did not stop there. It read pg_catalog unfiltered and found BOTH tables carry
`customer_id bigint`. The carriers are real and can hold customer_id = 90; the queue role
simply cannot see them. Had the lane obeyed the advisor's test as written, row 90 would have
been deleted on a premise the filtered view manufactured. The defective test is the advisor's;
the catch is the lane's.

### (ii) A number is evidence only if the role that must ACT on it can obtain it

Proposed substance (OVERSEER's wording, 2026-09-10 23:1x, recorded verbatim in substance): a
census, count or precondition taken by a credential that the EXECUTING path does not hold is
BACKGROUND, not a precondition. Before a number gates an irreversible action, name the role
that will perform the action and show that role can obtain the number.

ORIGIN: the same lane. The 2026-09-10 22:55 reference census reported
rel.operator_directive = 0 for customer id 90, and that zero was one of three answers that made
the partnersync fork look ready to put to the operator. The queue role — the role that executes
the delete — cannot read that table at all: ACL is {postgres, relmem}, has_table_privilege
returns false, and pg_has_role shows queue inherits nothing. The number was necessarily taken
as postgres or relmem. Both the advisor seat that relayed it and the OVERSEER that gated on it
read the number without asking who could obtain it.

### (iii) The no-architecting rule — with the other session, not with this seat

Parked by operator order the same night. The OVERSEER had a §D replacement drafted and fitting
the 76-byte margin; it was not landed. The shape ALSO changed and the OVERSEER's prohibition
wording must not be carried into any file: the operator is building an ARCHITECT ROLE, not a
ban — verbatim, "advisors will reach out to a fable architect who will build the brief and the
architecture. They own the repo and build. But we cannot keep burning fable token on low
effort." Architecture and the brief come FROM a Fable architect seat that advisors call;
advisors keep the repo and keep the build; Fable is reserved for that seat as the expensive
model, not spent on execution. §D's "owns that repo's architecture" clause is what any landing
must replace rather than sit beside. Standing order meanwhile, unwritten: advisors do not
architect; a design question parks with its incident.

### (iv) An exhaustive-scan predicate is justified against the MECHANISMS that can perform the act, not the mechanism the author pictured

Proposed substance: when a scan is relied on to prove that nothing can do X, its predicate is
derived from the full set of mechanisms capable of X, and that derivation is stated. A scan
whose predicate matches only the mechanism the author had in mind returns a confident zero and
proves nothing. Where an authority boundary exists that IS exhaustive — a privilege ACL, a
credential holder list — prefer it as the bound and use the scan only to enumerate instances
within it.

ORIGIN, partnerorphan-1, 2026-09-10, the second aperture defect of the same lane. The advisor
asked the lane for "any workflow whose node SQL references either table", to establish what
could write rel.slack_dm_message. The live writer is n8n workflow fThmUzeH0TWxcvB3
"RelMem · Slack-DM ingest", ACTIVE on a 15-minute schedule, and it contains NO SQL AT ALL: a
schedule trigger, an SSH node running `slack-dm-ingest`, and two Code nodes that validate and
log stdout. The advisor's predicate returns zero for the actual writer. The lane widened the
scan to SSH/exec/HTTP nodes on its own judgment and found it, then named the general defect:
"an exhaustive scan must cover SSH/exec/HTTP nodes, not just SQL."

Companion finding, which is what made the scan unnecessary rather than merely wrong: the table
ACL was already the exhaustive bound. Only postgres and relmem hold INSERT or UPDATE on either
carrier, no other of 20 non-system roles holds either, and pg_default_acl on the schema is
empty, so no future writer stands armed. Any writer must be one of those two roles; a workflow
sweep can only enumerate instances of their use. The advisor stopped the remaining sweep on
that reasoning rather than extend the lane's HOSTS line to a second database.

Both aperture defects in this lane were the advisor's predicates and both were caught by the
lane declining to satisfy the instruction literally. Recorded that way on purpose: a lane that
answers exactly what it was asked, when the question is malformed, produces the wrong answer
with full compliance.

## THE COPY THAT COMES TO HAND (advisoroverhaul-1, 2026-09-11 — three incidents, one root)

Three failures in one evening, all mine, all the same root: **I read the copy that was
easy to reach instead of the copy that binds.** Recorded as ONE entry because they are one
defect, and splitting them into three would hide that.

**1. The third ceiling.** The operator raised the advisor boot ceiling to 47,000. The
number lives in three homes: `docs/boot-sets.json` declares it, `scripts/hooks/pre-commit`
warns on it, and `scripts/hooks/pre-push` ENFORCES it — pre-push being the only one that
fires on cherry-pick and merge, which is wa's actual landing path. I changed two and
reported the ceiling raised. pre-push kept 40,000 and refused the push of rules 57 and 59.

It was caught only because it blocked me. **That was luck, not method.** pre-push held the
LOWEST of the three, so the mismatch stopped work. Had it held the highest, the estate
would have believed in a ceiling nobody enforced — and the OVERSEER had explicitly said, in
the same order that set the raise, that he would not accept that back. He wrote the
condition and could not have detected its breach.

**2. The stale local ref.** Asked whether the estate was in sync, I compared the other
repos against my LOCAL `main` ref — stale, because I had pushed `HEAD:main` and never
updated it — and briefly read two stale repos as in sync. The binding copy was
`origin/main`.

**3. The anchor read as content.** See the next entry; same root, different surface.

### What was built, and the two properties that make it a control

`scripts/ceiling-consistency.sh` checks every boot-surface number that lives in more than
one file — the advisor ceiling across three homes, the STATUS budget and the STATUS entry
cap across two each. It runs from pre-commit when a home is staged and from pre-push
unconditionally.

1. **A disagreement is an ERROR, never a choice of which home to believe.** Nothing in it
   resolves a conflict; it refuses one.
2. **An unreadable number is an ERROR, never a pass.** If a file moves or a line is
   reworded, the check FAILS rather than quietly matching nothing and printing green.

The second property is the one this estate keeps failing, and it is the same sentence as
the boot-set tool's: **a control whose absence is indistinguishable from its satisfaction
is not a control, and "no rule configured" must never be the passing branch.**

The duplication itself stays deliberate: a shell constant is a floor precisely because no
commit can change it by changing data. The cost of that choice is that a raise must touch
every home — and now something enforces it.

## THE ANCHOR WAS CHECKED AND CALLED CONTENT (advisoroverhaul-1, 2026-09-11)

ADVISOR-WA.md's rebuild was reported as damaged: 20 lost requirements, 8 broken pointers,
and four sections — 7.cc, 7.y, 7.aa, 7.bb — "confirmed absent by content". That figure
reached the operator as fact. **It was not true.**

All four are present. They were RENUMBERED, not deleted: 7.y is 7.2, 7.aa is 7.4, 7.bb is
7.5, 7.cc is 7.6, each with its numbered requirements intact. The nine sections with no
counterpart are folded into the trim's consolidated §5b. Live and trim carry the same
count of numbered requirements.

**How the error was made, and how it was nearly repeated.** The verification probed each
section's HEADING WORDS. For 7.bb those are "seat rules", "advisor seat", "OVERSEER order"
— and none appear in the trim, because they are the LABEL. Probing the four actual
requirements — the `.env` symlink, the `$<digit>` ban, the converge.log literals, the HOSTS
exactness — finds every one of them in 7.5. The second seat ran the same label probe first
and was one keystroke from confirming a loss that had not happened.

**A rule's anchor is not its content, and a check that compares anchors has not compared
content.** This is the day's third instance of one shape — correct form, wrong target —
after the citation that was well-formed in three repos and resolvable in one, and the
ceiling that was raised where it was declared and not where it was enforced.

It cost a day of believing a healthy file was wrecked, and it nearly cost a re-cut of it.

**What IS genuinely lost in that trim is narrower and real:** anchors, origin pointers, and
the causal WHY behind several rules. A rule whose reason is gone is a rule the next seat
argues with. And four renumbers break every citation that names those sections by number,
even though no requirement moved — which is the citation checker's own thesis, arriving
from the other direction.

## A RELAY THROUGH THE ADVISOR IS WHERE AN OPERATOR ITEM DIES (2026-09-11, ARCHITECT.md §A)

Operator order, verbatim: **"Make sure architects are able to reach you directly in case
they need access to me, dont let them go to the advisor first."**

This replaced ARCHITECT.md §A's landed wording, which said a lane architect "does not
message the OVERSEER, does not message the operator, and holds no gate". The rule and the
behaviour changed in the same commit, per the doctrine law.

His reason is the whole finding of the 2026-09-11 ledger: finished work and unanswered
questions both stalled ONE HOP SHORT OF HIM. The relay was not slow, it was absorbing.
An item that needs the operator and is handed to an advisor becomes an item the advisor
is holding, and an advisor holding an item looks exactly like an advisor who has answered
it.

The amendment keeps the single operator funnel: the architect reaches the OVERSEER, not
the operator. What changed is that it does so DIRECTLY, and the advisor is TOLD rather
than ASKED.

### The address problem, and why it is not solved with a file

A seat permitted to message the OVERSEER and unable to address it is not permitted to do
anything. The obvious fix — write the current OVERSEER seat name into a tracked file — is
the defect this estate spent the day removing: the name changes at every OVERSEER restart,
so the file is stale within hours and fails SILENTLY, reaching nobody or the wrong seat.

Nor can it be found by pattern. SEVERAL `operator-sessions-*` SEATS ARE TYPICALLY LIVE AT
ONCE — three were, when this was written — and only one is the OVERSEER. A prefix match
would reach the wrong seat while looking correct, which is the day's recurring shape:
correct form, wrong target.

So the address is SUPPLIED AT SPAWN, by the seat that knows it because it is talking to
the OVERSEER, and CONFIRMED to be a live session before first use. An address that does
not resolve STOPS the seat and is reported. Unresolvable is an error, never a pass.

### The proof requirement

The OVERSEER's condition on accepting the amendment, and it is the right one:
**A ROUTE THAT HAS NEVER CARRIED A MESSAGE IS INDISTINGUISHABLE FROM ONE THAT DOES NOT
EXIST.** The path is not accepted on the strength of the wording. A live architect seat
sends one real `ASK-OPERATOR` and the OVERSEER confirms receipt.

## A CONTROL THAT CORRUPTS ANOTHER CONTROL'S MEASUREMENT (2026-09-11, sendgate vs §D4)
<!-- origin: ADVISOR.md#60 -->

> **CORRECTION, same evening, before this entry was a day old. "MANUFACTURED" IS
> WITHDRAWN; AMPLIFIED IS CORRECT. The rule stands; the inference from it was too strong.**
>
> This entry said the belt would have counted 14 against a threshold of 15. **The
> threshold is 4** — `estate-compliance.py:328`, `max_count <= 4`, read at source. 15 was
> the COUNT in the OVERSEER's message and I treated it as the LIMIT. **I never read the
> threshold; I took it from a peer's message** — the precise thing I had told the
> architect seat not to do two hours earlier, in the conduct standard I wrote: verify the
> rule ON ORIGIN, not on a peer's word. Strip every split-induced tag and the window still
> fails, several times over. The split-inflation is real and it did not cause the FAIL.
>
> **THE ACTUAL CAUSE IS EXEMPT-SET DRIFT.** The belt and the gate keep SEPARATE copies of
> which tags are exempt, and they disagree:
>
> - gate, `sendmessage-gate.sh:17` — 8 tags
> - belt, `estate-compliance.py:291` — 5 tags
> - **missing from the belt: `BOOT`, `BOX-SEQ`, `DEPLOYED`**
>
> Every counted tag in the peak window was `DEPLOYED`: exempt at the gate, counted by the
> belt. Measured on the same log, later in the evening than wa's reading and so higher:
> **belt's set peaks at 19, the gate's own set peaks at 5** — and under the gate's set this
> seat is not even the peak seat. Drift is worth 14 of the 19; splitting is worth 3.
>
> **SO THE ENTRY'S GENERAL FORM IS NOT ONLY INTACT, IT IS BETTER EVIDENCED.** Something
> between the subject and the meter is a control, and it is a STALE COPY OF ANOTHER
> CONTROL'S LIST. The seat reporting most carefully was accused twice by a belt reading
> its own out-of-date copy of the gate's exempt set.
>
> **AND IT NAMES A CLASS I HAD ALREADY BUILT THE FIX FOR, ONE TYPE UP.**
> `scripts/ceiling-consistency.sh` exists because one NUMBER lived in three files with
> nothing checking they agreed. The exempt tags are a SET living in two files with nothing
> checking they agree. Same defect, scalar versus set, and I did not generalise it — I
> checked the numbers I had been bitten by and stopped there.
>
> The belt's repair is not this seat's to make: changing which tags a control counts is a
> behaviour change to a control another lane owns, and it goes with the sendgate brief.
> What is recorded here is that **a set with two homes needs the same refusal a number with
> three homes got.**

The §D4 tick belt FAILED on seat `advisoroverhaul-1` at 15 tags in one rolling hour.
**The gate caused the failure it was measured by.**

Measured from the gate's own log at the time of the FAIL:

- last rolling hour: **20 gate events — 17 ACCEPTED, 3 REFUSED oversize**
- every oversize refusal is re-sent as TWO messages, never trimmed (rule 57)
- so 3 of the 17 counted tags exist ONLY because the gate split a message
- **without the cap the belt would have counted 14, under its own threshold of 15**

Whole day, same seat: 74 accepted, 18 refused oversize.

The seat did not send more. It sent the same content through more messages, because a
control forced it to. The belt then read the split as volume.

**This is a new shape, and it is not the same as a false positive.** The belt is working
exactly as specified and its input is corrupted by a different control. Neither control
is wrong on its own terms; the pair produces a reading that is false about the thing it
claims to measure. Every §D4 reading taken while the oversize cap is live is inflated by
an unknown amount, and the inflation is largest for the seats reporting most carefully —
because a long, evidenced report is the one that gets split.

**Consequences to hold:**

1. The oversize cap has a SECOND cost beyond the 23.1% of estate messages it destroys:
   it inflates the estate's own compliance readings. That belongs in the sendgate
   redesign brief beside the 11.1% post-raise baseline.
2. A seat must NOT throttle reporting to satisfy a belt reading whose cause is a gate.
   Doing so lets the measurement make the estate worse — the reports stop and the number
   goes green. The OVERSEER ruled this explicitly: "DO NOT SEND ME LESS."
3. Before a control's reading is acted on, ask what OTHER control shapes its input.

**THE INFLATION IS LARGEST FOR THE SEATS REPORTING MOST CAREFULLY.** A long, evidenced
report is the one that gets split. The belt penalises exactly the behaviour it exists to
encourage, and it does so hardest on the best seat. That is not a tuning problem. It is
the shape of the defect, and any repair that does not change it has not repaired it.

**THIS SHAPE IS NEW TO THE ESTATE'S VOCABULARY.** Every other instance recorded on
2026-09-11 was ONE control blind to the thing it named — a gate that could not see the
violation, a pointer that resolved nowhere, a ceiling raised where it was declared and
not where it bound. This is TWO controls, each correct on its own terms, whose PAIR
produces a false reading. Neither can be fixed by fixing itself.

Landed as estate rule 60. The general rule: **a measurement is only about its subject if
nothing between the subject and the meter is itself a control.**

A footnote that is part of the finding, not decoration: the OVERSEER's first count of
this was five refusals, against a measured 18, because he had counted only the refusals
of reports ABOUT the gate — a selection bias built into a count while writing about
selection bias. The belt's own repair, counting CONTENT rather than MESSAGES, goes with
the sendgate brief, since the script and the gate are one problem.

## THE FALSE POSITIVE OF THE SAME DEFECT (2026-09-11, a review that never started)

§58's null-case clause was written the same evening: *a negative result is only evidence
if the instrument could have returned a positive.* It catches a probe that finds nothing.

**It does not catch a probe that finds something that is not what it names.**

A loss review on ADVISOR-WA.md was reported as running, four times over an hour, with
confidence. **It had never started.** The terminal was sitting at codex's trust prompt —
"Do you trust the contents of this directory?" — with `model: loading`. The `1` had been
sent with `--enter` as a single call, and that dialog needs the digit and the Enter as
SEPARATE sends.

The liveness check was `ps`, which showed four `codex --search` processes. They belonged
to a different seat's review, still resident. **A PROCESS MATCH IS NOT A LIVENESS CHECK
FOR A NAMED JOB.** The instrument could not tell one seat's process from another's, and
it returned a positive every time it was asked.

**The tell was on the screen the whole time and nobody read it:** the pane said "Ask
Codex to do anything", which is the IDLE prompt. The status line was the correct
instrument and the process table was the convenient one.

### Why this is the harder half

A false negative announces itself as absence and invites a second look. **A false
positive is indistinguishable from the thing going well**, so nothing prompts the second
look — the seat reports progress, the waiting seat waits, and both are satisfied. It is
the same shape as a register entry standing in for a resend, and the same shape as a
green from a check that could not have gone red.

The general form, which §58's clause needs as its other half: **STATE WHAT THE
INSTRUMENT WOULD HAVE RETURNED IF THE THING WERE ABSENT.** If the answer is "the same
result", it is not an instrument for that question. `ps` returns processes whether or not
MY job is among them, so it can never answer "is my job running".

### What was salvaged

The delay was not wasted. The addendum requiring the instrument to be named was written
to disk during the hour the review was not running, so the restarted pass reads the
version that contains it. **A review that had "succeeded" on schedule would have reviewed
the weaker file.**

Recorded with its sibling: the seat reported the hang plainly when asked, rather than a
verdict it did not have. Four false progress reports and one honest "it never ran" — and
the honest one is why the file is still unlanded rather than landed on a review that did
not happen.

## MEASURING THE WHAT AND ASSERTING THE WHY (2026-09-11, the estate-drift entry)

I measured three repos holding three different charters — wa 9f4d613a / 60 rules, relmem
8b42fe9e / 55, skill-factory 498af7d9 / 57, with no ARCHITECT.md in relmem — and recorded
it as **"estate doctrine drifting, ungated"**, the sixth instance of the night's
duplicated-fact pattern. The measurement was correct. **The conclusion was not, and the
values could not have told me.**

relationship-memory's state is not drift. It is a **DELIBERATE RETURN TO A PINNED STATE**.
The OVERSEER cancelled the replication and ruled the sync happens ONCE, after
ADVISOR-WA.md lands, on its call. relmem had already landed the copy, and reverted it —
`15a8d2b9` reverting `546a8344` — reasoning, in its own commit message:

> the copy introduced a ledger/file mismatch of exactly the kind the new architect brief
> exists to forbid: STATUS.md pins docs/ADVISOR.md at 8b42fe9e / 667 L while the file on
> disk read 498af7d9 / 708 L. Returning to the pinned state defers the choice to the
> sync's owner instead of resolving the mismatch by picking a copy to believe.

Verified at source: relmem's STATUS pins `8b42fe9e46868f0642cf5ceec3102fc2 / 667 L`, and
both the working tree and origin/main match it exactly.

### The corrected entry, and a new instance found inside it

**A PIN AND THE FILE IT PINS ARE TWO COPIES OF ONE FACT.** relmem's STATUS block is a
hand-maintained comparator for its own doctrine tree, and IT FIRED — it is the only one
of the three repos that noticed, and it noticed by comparing rather than by remembering.

So the sixth entry splits:

- **work-automation / skill-factory** — genuinely ungated. Two copies, no comparator.
- **relationship-memory** — carries a working pin-vs-file check that caught a bad copy
  and refused it. Not the defect; the closest thing the estate has to the fix.

### The error, named as its own class

**I MEASURED THE WHAT AND ASSERTED THE WHY.** Three digests are a fact about content.
"Drifted, ungated" is a claim about INTENT and HISTORY, and no hash carries either. The
history was one `git log` away and I did not read it, because the measurement felt like
the answer.

It is the same shape as the day's others and it is the one that survives having good
instruments: a correct reading, a confident inference, and nothing in the reading capable
of contradicting the inference. A second seat then CONFIRMED it with an independent
measurement of the same values — which proved the digests and nothing about the cause.

**TWO SEATS AGREEING ON A MEASUREMENT IS NOT TWO SEATS AGREEING ON ITS MEANING.**
Where a claim is about why, the evidence is the history, not the state.

## STARVING THE ROLE COST MORE THAN THE BYTES (2026-09-11, the architect boot set)

The architect boot set was four sections of ADVISOR.md — §D, §E, §F and rule 56 — priced
at 5,869 tokens against a 6,000 ceiling. Both architect seats that ran under it went
looking for what they had not been given.

`arch-estate-doctrine-sync` read NINE OFFSET SLICES of ADVISOR.md, ~330 of 754 lines, and
seven of the nine were doctrine the boot had withheld: the charter §A–§C, rules 2–5 on
effort and spawning, 14, 21, 35–37 on briefs and landings, 40–44, 46–47. **That is the
brief-writing and worker-spawning half of the doctrine — the architect's actual job,
withheld from the architect.** `arch-citation-perrepo` did the opposite and re-extracted
§D/§E/§F by script from a file it already held.

Operator ruling, verbatim: **"give them everything they need."** The whole file, ceiling
to 18,000.

### Why the whole file rather than the measured slices

A measured set priced at 8,831 and was recommended; he overruled toward completeness, and
the arithmetic supports him. The whole file costs 8,296 tokens more, against a first-call
boot context measured at ~61,800 — of which ~56,000 (system prompt, tools, CLAUDE.md, the
launch brief) **is ungoverned by any manifest**. Economising on 13% of a boot nobody
measures, while the other 87% is unpriced, is a saving in the wrong place. Starving the
role cost two seats their turns in one day; the ceiling saved nothing either time.

**A BUDGET IS ONLY A SAVING IF THE THING IT DENIES IS CHEAPER THAN GOING WITHOUT IT.**

### The drift the change resolved on the way past

§B's item 3 had grown to name twelve sections — §D, §E, §F and rules 2, 4, 5, 14, 21, 35,
40, 43, 56 — while `docs/boot-sets.json` still declared four. **THE BOOT LIST IN PROSE
AND THE BOOT LIST IN THE MANIFEST ARE TWO COPIES OF ONE FACT**, they had drifted, and
nothing compared them. A seat obeying the file would read twelve; the gate measured four.
Family A, found while executing a change for another reason and not by any check.

### The seam the change required

ADVISOR.md is ADVISOR doctrine. An architect holding it whole may read advisor-only
obligations as its own, so §B now states the split: what binds an architect, what does
not, and that **a clause naming the advisor is describing the CLIENT, not the reader.**
The set was the operator's to rule; the seam is the architect charter's to word, and a
boot change shipping without it would hand every architect a list of duties it must not
perform.

## THE CLOSED LIST THAT WAS WRITTEN TWICE

2026-09-11 18:50 +04, advisoroverhaul-1.

ARCHITECT.md §B enumerates the architect boot set. Four paragraphs below the enumeration
it also said, in prose, **"ADVISOR.md is NOT in this set: item 3 names four addresses
inside it, and reading it in full is a defect, not diligence."** When the operator ordered
the whole file given to the role, I rewrote item 3 and committed it as `a4e8a6d4`. The
prose four paragraphs down still said the opposite. The commit shipped a file that
contradicted itself, and I caught it only because I went back to read what the manifest
comment had been quoting — not because anything checked.

THE BOOT LIST NOW HAD THREE COPIES, not two. The enumeration, the prose paragraph, and
`docs/boot-sets.json`. A fourth was already stale before any of today's edits: the same
section said "the five reads above" while the enumeration had grown to six items.

THIS IS FAMILY A AND IT WAS INVISIBLE TO EVERY CONTROL WE BUILT TODAY. `bootset.py`
measures the manifest and never reads the prose. The identity comparator compares the file
across three repos and would have found all three repos carrying the SAME contradiction
and called them identical — correctly. A comparator across REPOS cannot see a
contradiction WITHIN a file. **A DUPLICATED FACT IS ONLY ENUMERABLE IF SOMETHING KNOWS
THE TWO COPIES ARE COPIES.** Nothing did, because one copy was a JSON array and the other
was English prose four paragraphs away from the list it restated.

WHAT ACTUALLY CAUGHT IT: the manifest's old `_` comment quoted the prose sentence
verbatim, so updating the manifest sent me to read the sentence. The citation was the
instrument, and it worked by accident. That is not a control; it is the third time today
that a copy was caught by someone happening to look at it.

THE REPAIR IS NOT A THIRD RESTATEMENT. The prose now says only that item 3 and the
manifest govern and that ITEM 3 WINS if they disagree. A closed list stays closed by
having ONE place that can close it, and the other places pointing at that place rather
than repeating it. **A RULE RESTATED FOR EMPHASIS IS A RULE WITH A SECOND VERSION THAT
CAN GO STALE ALONE**, and emphasis is a poor trade for that.

## WE'RE SETTING IT UP TO FAIL (rule 61)
<!-- origin: ADVISOR.md#61 -->

2026-09-11, the operator, five words, on an evening in which the same shape was measured
four separate times by four different seats before anyone named it.

**1. THE GRAPH, GRADED ON A FACT IT WAS NEVER GIVEN.** The resolver is handed one promoted
fact — id, subject, one evidence quote, attendees. It never sees the call. It was then
measured at 86% of group B and 62% of group A graded WRONG on commitments, and the estate
began reasoning about the resolver.

**2. THE ARCHITECT SEAT, GIVEN FOUR SECTIONS OF A 754-LINE FILE.** Both seats went looking
for the rest — one read nine offset slices, ~330 lines, seven of them the brief-writing and
worker-spawning doctrine its job actually needs. The reading was correct behaviour under a
starved brief. THE ESTATE WAS ONE MESSAGE FROM ORDERING A CLAUSE TELLING ARCHITECTS TO READ
LESS. The operator instead said "give them everything they need."

**3. THE COMMITMENT ROW WITH NO PATH BACK TO ITS MEETING.** The row cannot be verified from
the surface it appears on, so it is not used. Its non-use then reads as the operator's
preference about the feature, rather than as the row being unusable.

**4. THE REFUSAL REGISTER BLOCKING THE SEAT THAT CANNOT DISCHARGE THE DEBT.** Measured the
same night, by the seat it blocked: the check audited one hardcoded seat's obligations
against the PUSHER's working tree, where those entries structurally could not exist. The
blocked seat had no available action — including the one the hook's own message instructed,
which would have been a false record under rule 50. Fixed in 032eb41f.

**THE COMMON SHAPE, AND IT IS THE HARSH PART: IN ALL FOUR, THE FIRST INSTINCT WAS TO FIX
THE CONSUMER.** A better resolver. A brief telling architects to read less. A nudge to use
the surface. A demand that the blocked seat register someone else's debt. Not one of the
four opened with "what was this thing handed?" — and three of the four would have shipped
a change that made the starvation permanent while closing the ticket.

WHY IT IS A RULE AND NOT A NOTE. A starved component is indistinguishable from a weak one
FROM INSIDE THE MEASUREMENT. The instrument works, the path is clean, the number is real.
Nothing in the reading itself can tell you the input was short — only the brief can, and
only if it was required to say. That is why §61 demands the supply be STATED rather than
considered: consideration leaves no artifact, and a reviewer cannot re-run a thought.

RELATION TO ITS SIBLINGS. §58 caught instruments that could never have returned a positive.
§60 caught meters whose input another control was shaping. §61 is the third seat of the
same table and the only one whose failure is invisible from inside the measurement.

## THE CITATION CHECKER THAT CHECKS NOTHING IN THE FILE IT GUARDS

2026-09-11, advisoroverhaul-1, found while confirming that rule 61's own origin citation
resolved — that is, by refusing to accept a control's green as evidence about a thing I
had just written.

`scripts/doctrine-citations.py` exists so that a rule saying "Origin in ORIGINS" cannot say
it without an origin being there. Its pre-commit wrapper prints `origin claims: N resolved,
M unresolved (unchanged, none new)` and blocks any commit that increases M.

MEASURED, with the instrument shown working first:

    grep -c "docs/ADVISOR-ORIGINS.md" docs/ADVISOR.md        ->  4 citations
    the tool's CLAIM regex over the same file                ->  0 claims
    grep -c "<!-- origin: ADVISOR.md#" docs/ADVISOR-ORIGINS.md -> 18 anchors

**FOUR CITATIONS, ZERO CLAIMS DETECTED, EIGHTEEN ANCHORS RESOLVING NOTHING.** The tool's
coverage of ADVISOR.md is zero and it has been printing green the whole time.

THE CAUSE IS A DISTINCTION DRAWN ON SPELLING. CLAIM is `\bORIGINS\b` with a lookbehind
excluding `ADVISOR-`, written to stop a mere mention of the filename counting as a claim.
But the form every rule actually uses IS the filename — "Origin: docs/ADVISOR-ORIGINS.md."
So the one shape the tool refuses is the only shape anyone writes. A claim and a mention
were separated by how they are SPELLED, and the spelling the authors chose landed on the
wrong side.

WHY THE FIX IS NOT THE ONE-LINE REGEX I FIRST WROTE. Widening it to match `Origin...
ADVISOR-ORIGINS.md` anywhere on a line raises detection from 0 to 8 — and four of the
eight are ADVISOR-WA.md SECTION HEADINGS whose prose merely mentions that its doctrines
were each earned by an incident. Anchoring those would be recording origins that do not
exist, which is a false record under rule 50 and strictly worse than the silence. THE
LOOKBEHIND WAS OVER-BROAD, BUT IT WAS THERE FOR A REAL REASON, and a fix that trades a
silent gap for a fabricated green is not an improvement. Separating a CLAIM from a MENTION
needs a marker the author sets deliberately, not a pattern guessing at intent.

LEFT OPEN DELIBERATELY, with anchors added for rules 60 and 61 so the data is correct
whenever the detector is: docs/ADVISOR-WA.md is being rewritten by another seat tonight
and its headings are half the evidence. A control redesign measured against a file that is
mid-rewrite would be a rule 61 violation in the commit that lands rule 61.

THE SHAPE, FOR THE THIRD TIME TODAY: a control whose absence is indistinguishable from its
satisfaction. Twice tonight that was an interpreter standing down. Here it is a pattern
that matches nothing. The exit code is 0 in all three.

## THE CEILING THAT BECAME THE ESTATE'S DOCTRINE BUDGET WITHOUT ANYONE DECIDING IT

2026-09-11. The rule the whip wrote for this is real, and it is deliberately NOT rule 62.

WHAT HAPPENED. The operator granted the architect role the whole of docs/ADVISOR.md
("give them everything they need"). The whip picked 18,000 as the ceiling against a
17,127 measurement. Both choices were correct in isolation. Together they created a
coupling nobody decided: **ADVISOR.md now sits in TWO role sets, so every doctrine rule
is charged to both, and the TIGHTER ceiling governs what the whole estate may write.**

Within hours the architect had 360 tokens free against the advisor's 5,922. One more rule
the size of §61 and an architect ceiling — chosen for a boot measurement, by someone
thinking about a boot — would have silently stopped all doctrine growth. It surfaced only
because I reported the two headroom numbers side by side in a status line I nearly did
not write.

THE RULE, whip-authored: a ceiling must never become the binding constraint on doctrine
growth BY ACCIDENT. Either it is a deliberate budget on doctrine and says so, or it
carries headroom comparable to the other roles.

WHY IT IS A TOOL LINE AND NOT A RULE, which was my call and is the part worth keeping.
**NOBODY DISOBEYED ANYTHING.** There was no instruction to follow and no instruction that
would have helped: the coupling fell out of two numbers chosen months and hours apart, and
a sixty-second rule would have been read by exactly the seats who already knew both
numbers and still did not see it. The failure was not ignorance of a principle. It was
that at the moment of the edit, nothing said WHICH CEILING BINDS THIS FILE.

So `bootset.py check` now prints, on every run:

    docs/ADVISOR.md is in 2 sets — the BINDING ceiling is advisor's, 5,922 free
    (vs architect 6,360).

No threshold and no warning level, on purpose. A threshold on "comparable headroom" would
be an invented number, and an invented number that blocks work is how a control gets
overridden until it is ignored. The line states a fact and leaves the judgment where the
rule puts it.

**AN INSTRUCTION COMPETES FOR ADHERENCE WITH SIXTY-ONE OTHERS. A LINE THE TOOL PRINTS AT
THE MOMENT OF THE EDIT COMPETES WITH NOTHING.** Same reasoning the overhaul worker and I
used to keep the duplicated-fact enumerator out of the rule list: instructions decay,
comparisons do not. This is the second time tonight that the right answer to "should this
be a rule" was "it should be a measurement".


## A RULE THAT MANDATED THE DRIFT ITS SIBLING WAS BUILT TO CATCH

2026-09-11. The whip called this the finding of the night and offered a generalisation to
take or correct. Taking most of it; correcting two parts, one of which matters.

THE FACTS, from the commit timeline rather than memory:

    17:19  840d69b5  advisor ceiling 40,000 -> 47,000, SOLO on the manifest,
                     "as the raise rule requires"
    17:20  75f63a27  the pre-commit shell floor, separately
    17:23  ce4c2085  pre-push — the gate of record — raised, and the consistency
                     check written
    19:00  e08bf476  the architect ceiling gets a shell floor
    19:0x            the raise to 24,000 cannot land by any route

Between 17:19 and 17:23 the three homes disagreed and pre-push refused at 40,000. **THAT
WAS NOT A LAPSE AGAINST THE RULES. IT WAS COMPLIANCE WITH ONE.** The grant rule required
the manifest to move alone; moving alone IS the drift.

ACCEPTED: when two controls' requirements are jointly unsatisfiable, at least one is
manufacturing the defect it appears to guard, and a deadlock is evidence about the rules
rather than an obstacle to route around. The repair came from reading the grant rule's
INTENT — "a raise carries nothing but the raise" — instead of forcing past its letter.
That distinction is why the fix is a repair and not an exemption.

**CORRECTED, AND THIS IS THE PART THAT MATTERS: THE DEADLOCK IS NOT THE ONLY SYMPTOM, AND
IT IS NOT THE FIRST.** The defect arrived at 17:19. No deadlock was possible until 19:00,
when a second control finally made the requirement explicit. For an hour and forty minutes
the manufactured defect was fully visible — as a refused push — and was read as human
error. **A DEADLOCK IS A LATE SYMPTOM. IT APPEARS ONLY ONCE SOMEBODY BUILDS THE SIBLING,
AND BEFORE THAT THE RULE'S OUTPUT IS INDISTINGUISHABLE FROM A SEAT BEING CARELESS.**

That is the dangerous window, and nothing in "treat a deadlock as evidence" reaches into
it: during the window there is no deadlock to treat. What there is instead is a defect
attributed to a person.

CORRECTED, SECOND AND SMALLER: in a deadlock it need not be that one control is wrong.
Here the grant rule's INTENT was right and its IMPLEMENTATION — "one file" — had drifted
from it. A letter can outlive its intent without anyone rewriting either; it only takes
the world gaining a third home.

WHAT I WILL NOT LET THIS FINDING DO IS RETRACT A REAL ERROR. This morning I reported the
ceiling raised having changed two of three homes and not checked the third. The rule
mandated the split; it did not mandate reporting completion before measuring. Those are
two failures, one mine, and the new one does not absolve the old one.

BUILT, NOT WRITTEN AS A RULE, for the third time tonight: `set-consistency.py` now
compares the homes a ceiling has against the paths the grant rule permits in a raise, and
fails the moment they stop being jointly satisfiable — at the commit that strands a home,
not at the next raise that cannot land. The early symptom, instead of the late one.

ONE DEFECT FOUND IN THAT BUILD, in the check's own stated property. It added
docs/boot-sets.json as a home whenever the string "boot-sets.json" appeared anywhere in
the file, which a COMMENT satisfies. Renaming the shell helper left one home parsed, no
failure raised, and "all 1 ceiling homes are landable" printed green. **UNREADABLE HAD
BECOME A PASS, INSIDE THE FILE WHOSE SECOND STATED PROPERTY IS THAT IT NEVER IS.** Caught
by the reworded-file case, which is in the battery because it is the one everybody forgets.

## THE CODE WAS REPAIRED AND THE MESSAGE WAS NOT
<!-- origin: ADVISOR.md#62 -->

2026-09-11, immediately after the deadlock repair. Found while testing a hypothesis that
turned out to be wrong, which is the only reason it was found at all.

THE HYPOTHESIS, AND ITS REFUTATION. The whip asked how many past failures were rules
working as written. I went looking and thought I had a second instance: a future order
that WIDENS a role's reads and RAISES its ceiling together — the exact shape of fd06f0be
two hours earlier — now needs the manifest, both hook file lists and the new doc in one
commit, and the grant rule's allowance admits only ceiling constants and comments. I
tested it before reporting it. **THE COMBINED COMMIT IS REFUSED, BUT A TWO-COMMIT SPLIT
PASSES EVERY CONTROL: the raise with its homes, then the reads with theirs.** That is the
grant rule working as designed, not a deadlock. Hypothesis withdrawn before it reached
anyone.

WHAT THE TEST FOUND INSTEAD IS REAL. `b39e05fb` repaired the grant rule's CODE to admit
the ceiling's other homes. Its REFUSAL TEXT still read:

    A raise must be a commit of ITS OWN, touching only docs/boot-sets.json

**THE INSTRUCTION THAT MANUFACTURED THE 17:19 DRIFT WAS STILL BEING PRINTED, SIX HOURS
AFTER THE CODE STOPPED REQUIRING IT.** A seat blocked by this gate reads the message, not
the source. Obeying it recreates the defect exactly, and the code would have permitted the
correct commit the seat was being told not to make.

So the repair had closed the window in the code and left it open in the only part of the
control a person ever sees. **REPAIRING A CONTROL MEANS REPAIRING WHAT IT SAYS, NOT ONLY
WHAT IT DOES — THE MESSAGE IS THE HALF THAT ACTS ON PEOPLE.** A gate's text is not
documentation of the gate; for every seat it blocks, it IS the gate.

AND THE SHAPE IS THE SAME ONE AGAIN, one level up: the letter of the message outlived the
intent of the code, without anyone rewriting either. The world gained a third home.

VERIFIED BY TRIGGERING IT, not by reading the source — the first attempt rendered the OLD
message because the scratch repo's `git checkout -- .` had restored the file I had just
copied in. A source read would have shown the new words and proved nothing about what a
blocked seat receives.

## THE EXCEPTION THAT DESCRIBED A STATE THAT DID NOT EXIST YET (rule 63)

The OVERSEER ordered a doctrine fix and, in the same breath, the drift allowance that
would cover it. Reasonable on its face: the fix diverges a byte-identical file, so declare
the divergence in the commit that creates it and nothing is ever silent.

The commit was REFUSED, and not by a rule anyone had written down — by
`doctrine-identity-check.py`, on its own "an allowance outlives the thing it excuses"
branch. **The checker compares ORIGIN blobs, not the working tree.** From origin's view
all three repos still agreed, so the allowance was describing a divergence that had not
happened. The instrument read it as an exception whose condition was already over, when in
fact the condition had not yet begun — **the same refusal covers both, because from the
outside a claim about a state that has passed and a claim about a state that has not
arrived are indistinguishable.**

The order that follows is forced rather than chosen: **the fix ships alone → the drift
appears at origin → the allowance follows → the allowance dies with the drift.**

ORIGIN, NAMED RATHER THAN TIDIED: proposed by the work-automation advisor from the refusal
it hit **while executing a sequencing order of the OVERSEER's that this rule forbids**.
The OVERSEER wrote the order, the advisor hit the wall, and the wall was right. An origins
entry that hides who was wrong is worth less than one that names it.

THE SECOND HALF WAS ALREADY PAID FOR THE SAME NIGHT. Two allowances were opened and closed
within an hour, and the delete-on-repair property is what forced a human look at the last
false "identical in all three". A rule that only said "do not write an exception early"
would have left the more expensive half — an exception left standing — unwritten.

## THE RULE THAT HAD NEVER BEEN LANDED, CITED FOR A DAY AS STANDING (rule 64)

Rule 64 was authored by the OVERSEER on 2026-09-11 and put in a sitting document,
`docs/doctrine-sitting-2026-09-11.md`, at `0f1f0c94`. **That commit is on
`Cipher-DLRT/operator-sessions` and nowhere else.** The file does not exist on main; before this
commit the phrase appeared in no doctrine file in any of the three repos.

**It was then cited for a day as a standing rule, by its own author.** The citation reached this
advisor as "§63 EXERCISE unsatisfied", offered as settled doctrine. It was found only because the
advisor went looking for rule 63 to land a different rule, and could not find it.

**THE RULE IS ITS OWN SUBJECT.** An artifact that has never performed its function has not been
shown to have it — and a rule that has never been landed has not been shown to exist. It was
presence mistaken for capability, in the file about presence being mistaken for capability, by the
seat that wrote it.

**THE MECHANISM IS NOT FORGETFULNESS, AND THIS IS THE PART WORTH KEEPING.** The branch holding the
sitting was measured the same night as 2,318 commits off main's line and containing none of the
control commit, and is therefore EXEMPT FROM EVERY CHECKER ON EVERY PUSH — its receipts print
`result=false` and were read. **So the one branch where doctrine was being drafted is the one
branch where no gate could see it.** CLAUDE.md already says a rule that lives only in a sweep file
is a rule the next session will not read; here the author read it himself and believed it.

Landed as `## 64.` because 63 was taken in the interval by the rule this one should have preceded.
The body is verbatim from `0f1f0c94`; the only change is the self-reference in its own title, which
said §63.

**The other four items of that sitting were checked in the same pass rather than assumed.** Items 1
and 5 had landed. **Item 3 had NOT** — its ruling was to DELETE the send-contract numbers from
ADVISOR.md, and those numbers were still there, still false, a day later. Finding one phantom rule
was the reason to look; the look found a second unlanded ruling.

## THE COPY OF A MACHINE'S RULE THAT MISLED THE MACHINE'S OWNER (ADVISOR.md §D, send contract)

`docs/ADVISOR.md` restated the send gate's contract in prose: a four-per-hour rate, and an
exempt set naming `ASK-OPERATOR`, `BLOCKED`, `DEPLOYED` and `BOX-SEQ`. **The installed gate
exempts two tags and caps the window at twenty.** The prose had drifted from the script it
described, and doctrine is read at boot by every seat in three repos.

**THE RULING TO REMOVE IT WAS MADE AND THEN NOT LANDED.** The OVERSEER ruled on 2026-09-11:
*"DO NOT UPDATE THE NUMBERS. REMOVE THEM."* — updating them would rebuild in prose exactly the
duplicated-operand defect being removed from code the same night. That ruling went into a
sitting document on a branch that reaches main nowhere, and **the false numbers were still
live a day later**, found only when an advisor checked the sitting's other items rather than
assuming they had landed.

**WHO IT ACTUALLY DECEIVED IS THE PART TO KEEP.** The known cost was three false accusations
against seats, from a doctrine copy that named tags as exempt which the gate counts. The
unknown cost was larger: **the drifted copy told the OVERSEER that its own `RELAY`, `ORDER`
and `RELEASE` tags were exempt from the count. They are not.** The whip spent a night
sending against a budget it believed was uncapped for its own traffic, took three rate
refusals, and read §D4 at 43 sends in a rolling hour.

So a human copy of a machine's rule did not merely mislead the seats it accused — **it
misled the author of the accusations about his own conduct.** A restatement does not drift
politely toward the people it governs; it drifts toward whoever trusts it most, which is
usually whoever wrote it.

**THE FIX STATES NO NUMBER.** Doctrine now says the contract exists, names
`scripts/hooks/sendmessage-gate.sh` as the sole source of its own limits and exemptions, and
tells the reader to read `LIMIT_CHARS`, `LIMIT_PER_WINDOW`, `WINDOW_SECONDS` and `EXEMPT`
from the script at the moment of need. The one ceiling doctrine keeps is the one it sets for
itself — 1,500 characters, tighter than whatever the gate admits, binding on the whip's tags
before anyone else's.

Authored by the whip a day late, after its own ruling to remove these numbers went unlanded
and the drifted copy then misled the whip itself.

§57's index line and §57's body disagreed for sixteen hours. 1c92830d restored the body at 17:21 on 2026-09-11 declaring the numbering hole closed; 5bc5c74d wrote "no §57: drafted, held, not in force" into the index at 17:30, into a file that already carried the body. A seat reading the index believed the rule was held and a seat reading the body obeyed it, and both were reading the same md5. An index is a restatement of the body: when they disagree the body governs, the index is repaired, and the body is not withdrawn to match it.

The §57 index repair of 2026-09-12 fixed what line 9 said about one rule and left it asserting a ceiling of §59 while the body carried §64 — the same defect one number along, introduced by the repair, and caught by skill-factory rather than by the whip who wrote both. SF proposed §1–§64 on the ground that a single unbroken bound cannot develop a hole, which is right and does not go far enough: a bound naming a maximum is still a restatement, and it goes stale the day §65 lands. So the line now names no upper number at all and points at the body. This is the estate's standing repair, arrived at a fourth time in one night: when two places state one fact, delete the second and derive. §62 governs — repairing a control means repairing what it SAYS, not only what it does — and §64 names the reason it was missed: the index had never been exercised against its own body. Measured afterwards: the index has never once been correct — §1–§57 against a body of 59, then §1–§56 and §58–§59 which fixed the ceiling and broke the membership in one edit, then §1–§59 against a body of 64. A restatement that has been wrong in every state it has ever held is not a thing to correct again. The whip's own order to land this amendment quoted a FROM span that appears nowhere in the file: it wrote "into its own STATUS NEXT or HELD line" against an actual "written into that seat's own STATUS NEXT or HELD line", paraphrasing from memory a file it had open. The landing seat refused to pick the surrounding words itself and asked. So: an order to land text verbatim quotes its FROM span FROM THE FILE, and a seat that cannot match the span exactly holds the edit and says so rather than repairing the intent.

§65 was earned three times in one night by the same 32 characters. relmem hit d41d8cd98f00b204e9800998ecf8427e on a failed git show; the whip hit it on docs/ADVISOR-ESTATE.md, a file that does not exist in work-automation; and the wa seat found its own propagation check had used the same pipe, correct only by direction, because wa holds both files and a missing sibling therefore surfaces as drift. No seat mis-read the value once it was seen. The failure is that nothing in any of the three commands would have raised it had the value not been recognised on sight.

§66 was earned by a lane that was never launched. askramitoken-1's suite failed on the identity checker; the wa seat measured origin, saw real drift, concluded the selftest was defective through fixture inheritance, briefed driftself-1 to repair the tool under §46, and told the failing lane that cause. All of it was wrong: the lane's worktree was pinned at an older main whose checker still carried allowances deleted at dea6850c once their drift closed, and the seat first read that as the cause. It is not established: the selftest at :85-86 copies the live checker, DECLARED_DRIFT included, into fixtures whose doctrine files agree, so any live allowance — stale or correct — can trip the expiry branch inside scenarios about something else, and the failure reproduced identically once the lane carried current main and a correct allowance. A correct input cannot be refused for being stale. The mechanism is UNDER MEASUREMENT by driftself-1, ordered red first; this entry will say what it finds and not what was expected. What caught it was the pre-push gate refusing the repair brief's OWN landing on the ground that the files now agree — the control that stopped the wrong fix shipping was the control the seat had briefed a lane to repair. driftself-1 was withdrawn before launch, kept with the withdrawal on top and the original beneath, because a withdrawn premise deleted is a premise that returns.

§55 first read "Keep HubSpot read-only for the estate — no exception, no approval path", written from the operator's "DO NOT TOUCH OR MODIFY HUBSPOT" on 2026-09-10. The whip generalised a sentence about ONE repair route into a revocation of a product capability, and the over-broad rule then barred a feature row for two days. He corrected the scope himself on 2026-09-12: he had meant do not fix the partner issue by editing the record. §55 now states the scope he meant. §54 covers the ASK, §55 covers the ACT; neither reaches an approval-gated write that is the operator's own output.

§67 was earned one step from a false report. Verifying migration 152 as the queue role, information_schema.column_privileges returned EMPTY for pkms_dashboard and the seat was about to report 152 NOT APPLIED. The grantor was postgres; the unfiltered catalog showed caution={pkms_dashboard=aw} and relacl pkms_dashboard=rd — applied, and invisible to the instrument used. The seat caught it and reported the trap alongside the answer.

§67 has a second sign, and it fails the other way. On 8 September the relationship-memory seat read information_schema.column_privileges on a correctly-granted table and got 27 rows — the view EXPANDS a table-level grant into one row per column — and nearly rolled back a good migration on the strength of it. So the same instrument reports a present grant as absent when another role made it, and reports one grant as many when the grant is table-level. It fails open and closed depending which way it is read. pg_attribute.attacl and pg_class.relacl are the only operands with one meaning.

§27 and §67 contradicted each other for one day and both read as settled. §27 mandated information_schema.column_privileges; §67 forbade it. The relationship-memory seat found it while carrying §67 into its own repo — it read the rest of the file, which neither the author of §67 nor the seat that landed it had done. Permission filtering hits DETECTION as well as assertion: a probe run as the queue role cannot see a column ACL granted by postgres, which is precisely §27's scenario. §27 needed no exception; it needed the operand §67 already names.

§27's has_column_privilege clause was measured before it was written and controlled before it was believed. On EQ14, as the queue role — the role information_schema.column_privileges returns zero rows to for that table — it returned TRUE for UPDATE and INSERT on pkms_documents.caution, a privilege postgres had granted. A function that answered TRUE to everything would give the same result, so three controls were run: sha256/UPDATE false, sha256/INSERT true, and the same column for a different role false. It discriminates, and it agrees with attacl exactly — sha256 carries a and not w.

§65's argument has an exact instance. Carrying dd3132e5 on 2026-09-12, docs/ADVISOR.md went from 888 lines to 887 while GROWING from 63,263 to 64,246 bytes — §27 replaced by a longer rule on fewer lines. A seat confirming "887, matches" would have read a shrink where there was growth, and been right about the number it checked. The count is not a weaker digest; it is an answer to a different question.

§4 was a blanket ban whose cause was measured away rather than argued away. The
operator found CLAUDE_CODE_SUBAGENT_MODEL and said so; the whip then removed the enforcing deny from all
three seats BEFORE amending the rule, and relmem named it as the mirror of a §63 fault the whip had
conceded an hour earlier — enforcement stripped with the rule live, then the guard removed with the ban
still written. relmem also withdrew its own boot report in the same message: it had verified the DENY IN
CONFIG and reported the TOOL ABSENT, a check that could not go red, which is why boot step 3 was deleted
rather than reworded. The whip had made the same substitution one commit earlier, publishing that every
HubSpot read tool was reachable when it had only read a config; relmem measured the surface and found no
HubSpot tool present in that seat at all.

## THE DURABLE INSTRUCTION PUT IN A VOLATILE PLACE (rules 69, 70)
§69 and §70 were earned in one hour by a single discovery. The operator asked whether the lanes were instructed to use GitHub Issues and milestones. The measured answer was zero: zero mentions in any boot file in any of the four repos, and zero Issues open in any repo — the second half checked against a public repository that has them, so the empty was a reading and not a broken command. The order had been routed to skill-factory as a MESSAGE two hours earlier and had never been delivered; that seat was parked on a permission dialog and three whip messages, both Issues orders among them, sat queued behind it. The whip had put a durable instruction in a volatile place, and the volatile place then failed in the one way that leaves no trace on the sender's side: the gate accepted every send. His correction was five words — "Put it in the boot file" — and a second followed when the whip proposed handing the wording to the work-automation seat to land: "The boot files are YOUR responsibility not WA." Authorship and landing are the same duty, and splitting them is how the first instruction died.

§70's four labels carry a provenance that is not the one they look like. The operator offered them as recall, and said so in the same breath: "(feature, path to feature, fix, research) (i think, it was something along those lines) please check before informing it". The check found no such set recorded anywhere in four repos. `fix` versus `feature` was his own two-way ask to relmem that morning; `research` is a live lane type in every repo; `path-to-feature` appears nowhere before this rule. Because he asked for the check before the rule went out, the rule can state its own age instead of borrowing authority it has not got — it is binding as doctrine from today, not as recovered practice. A taxonomy presented as long-standing would have been cited back at the whip within a day by a seat that could not find it.

## THE TAXONOMY THAT MADE A CLASS OF HONEST WORK LIE (rule 70, fifth label)
`estate` was added to rule 70 on 2026-09-13, hours after the rule landed, and the trigger was a
concrete failure rather than a tidier scheme. The janitor was found dead — approval-blocked on its
first tool call for two scheduled runs — and the repair had nowhere honest to sit. Under the
four-label rule it was a `fix`, and a `fix` must name the feature it degrades. The janitor degrades
no feature the operator uses; it degrades the machinery the seats use. Filing it as a `fix` would
have forced whoever filed it to invent a feature, which is the exact motion rule 70 exists to stop.
The operator's instruction was two words wide — "add estate and research to the build reasons" —
and the second half was already satisfied, `research` having been in the rule since it landed that
morning. Recorded because the general form outlives the label: a taxonomy is wrong when a whole
class of legitimate work can only be filed by misdescribing it, and the tell is not an argument
about categories, it is someone inventing a justification to satisfy a field.
