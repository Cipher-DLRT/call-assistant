# build-brief ca-retire-loop — call-assistant becomes the ears of demo-agent's control layer; the old hint loop retires (2026-10-05)
FEATURE: call-assistant holds only what demo-agent's control layer uses: the capture and speech-to-text binaries, the audio and segmenter modules that demo-agent loads by path, the voiceprint, and the menu bar. The August hint loop, its overlay, prompts and canon pack are gone from the live path but can still be found by sha. A new CLAUDE.md and STATUS.md say what the repo is now, and Rami approves that text on the issue. Shown by `git ls-files app scripts` on the branch, and by demo-agent's voice tests passing against it.
STATUS: QUEUED 2026-10-05 by owner-prompter-2 (demo-agent plan 3ee09d2; brief written by the owner, demo-agent kickoff §3 as amended 9ca6f90); codex-medium, stop $8; wave 1 with prompter-displays (demo-agent).

**Category:** feature — milestone #1 (Prompter P2 — the control layer), design P2.5.
ISSUE: #7
BRANCH: Cipher-DLRT/ca-retire-loop
DESIGN: `Cipher-DLRT/demo-agent:docs/design-prompter-2026-10-04.md` §3, §8(b) and §10 P2.5, on demo-agent origin/main; demo-agent `docs/rulings.md` rules 15 and 18. Facts: demo-agent loads `app/loop/audio.py` and `app/loop/segmenter.py` from this repo by exact path (demo-agent `app/voice/_call_assistant.py:39`, `:44`, base `CALL_ASSISTANT_PATH`, default `/Users/rami/dev/call-assistant`). `audio.py` imports only the standard library and numpy; `segmenter.py` imports nothing. `app/menubar/menubar.py:18` starts `scripts/run_call.sh`, which starts `app.loop.orchestrator` (`run_call.sh:42`); that path is ca#6's to replace. `scripts/llm_oneshot.py:10` imports `app.loop.llm`.
BRIEF-REVIEW: not required. HOSTS name none of the fenced systems (ADVISOR.md §D).

BOUNDARY: No writes outside this worktree.
Commit only here with explicit paths. **PUSH YOUR OWN LANE BRANCH, never main**, and name the pushed sha in DONE.
Push your lane branch after every commit.
Never write in `/Users/rami/dev/call-assistant` (the live checkout) or in any demo-agent tree.

Remove (`git rm`, explicit paths):
- `app/loop/orchestrator.py`
- `app/loop/llm.py`
- `app/loop/retrieval.py`
- `app/loop/cost.py`
- `app/loop/artifact.py`
- `app/overlay/__init__.py`
- `app/overlay/overlay.py`
- `prompts/gate-v1.md`
- `prompts/hint-v1.md`
- `prompts/hint-v2.md`
- `prompts/.gitkeep`
- `scripts/export-canon.sh`
- `scripts/llm_oneshot.py`
- `scripts/smoke_fake_call.sh`
- `scripts/verify_models.py`
- `scripts/launch-call-advisor.sh`
- `tests/test_artifact.py`
- `tests/test_cost.py`
- `tests/test_retrieval.py`
- `tests/test_reader_law.py`

Rewrite: `CLAUDE.md`, `STATUS.md`, `README.md`. Add: `tests/test_ears_kept.py`.

Keep, unmoved and byte-identical: `app/loop/audio.py`, `app/loop/segmenter.py`, `app/loop/attribution.py`, `app/loop/__init__.py`, `scripts/enroll_voiceprint.py`, `app/capture/`, `app/stt/`, `scripts/check_capture_exclude.py`, `scripts/check_capture_include_selftest.py`, `scripts/grade_leg.py`, `scripts/score_leg.py`, `scripts/hooks/`, `docs/` (history stays).
Never touch `app/menubar/menubar.py`, `scripts/run_call.sh`, `scripts/menubar-launchagent.plist`: they are ca#6's (P2.4), which moves the menu to demo-agent. Because `run_call.sh` starts the orchestrator this lane removes, **the owner lands this branch only after ca#6 has landed**. Build now; do not wait.

HOSTS: none. Local files and tests only; `github.com` — push of your lane branch — write.
Read-only, outside this worktree: `/Users/rami/orca/workspaces/demo-agent/owner-prompter-2/.venv/bin/python`, to run the leg 3 import check (it has numpy). It writes nothing outside this worktree when run with `-B` and `-p no:cacheprovider`.
No model, vendor or network calls besides the push: this lane spends no API money.
An unlisted read or connection is an incident: stop, record the read and copy location, and ASK.
Secrets: none appear in chat, reports, git or terminals; report key names, byte lengths or sha256 prefixes.
Customer content stays on the box: report ids, counts and file names. Never open `calls/`, `legs/` or `pack/`.

REASON: builder friction removed: two loops, two overlays and two knowledge sources claim the same call, and the repo's CLAUDE.md still states four laws that Rami scrapped on 2026-10-04 (demo-agent rule 15). A builder who reads it today builds the wrong thing.
TIER: codex-medium. TIER-REASON: removals by an explicit list, one small test, and two documents written from pinned content. It is bounded and mechanical, so it does not need Opus (demo-agent rule 10, 2026-10-05: codex where the brief says why); the P2 envelope prices it at codex.
Gate: NOT REQUIRED — §F all not-engaged, one revert restores with no data loss.
External review: NOT required — local code removal and documents; one git revert restores every file.

**Budget:** $8 at list. Stop at $8 and write HANDOFF. No live model spend.

PREREQUISITES:
- The worktree is on `Cipher-DLRT/ca-retire-loop` cut from call-assistant origin/main immediately before launch (check: `git merge-base --is-ancestor origin/main HEAD` exits 0 at boot; if not, STOP and signal BLOCKED).
- The leg 3 Python exists (check: `/Users/rami/orca/workspaces/demo-agent/owner-prompter-2/.venv/bin/python -c "import numpy"` exits 0). Do NOT pip install.
- Base sha256 of the two kept modules, recorded at boot in HANDOFF: `shasum -a 256 app/loop/audio.py app/loop/segmenter.py`.

§F CLASSIFICATION: grants/roles/credentials — not-engaged; containment/egress — not-engaged; external writes — not-engaged; column drop/alter — not-engaged; customer data off-box — not-engaged.

## The rules

Read first: demo-agent design §3 (the shape) and §10 P2.5; demo-agent `docs/rulings.md` rules 6, 8, 15, 18; this repo's `CLAUDE.md` (all), `STATUS.md` (header and the 2026-10-04 and 2026-10-05 log lines), `README.md`.

Rulings carried, not re-decided: demo-agent rule 6 (the HDFC rule), rule 8 (secrets), rule 9 (explicit paths, never `git add -A`), rule 10 (Opus 5.5 / codex gpt-6.1-sol only), rule 15 (call audio may go to a cloud transcriber), rule 18 (shape 1: one control layer in demo-agent, call-assistant as its ears). This repo's law 10 (STATUS.md in the same commit as any state change) stays.

**CLAUDE.md, pinned content** (at most 70 lines; the lane writes the prose, Rami approves it on #7 before landing):
1. What the repo is: the ears of demo-agent's control layer (demo-agent rule 18, design §3). Its parts and who uses each: `app/capture` → `app/bin/capture` and `app/stt` → `app/bin/stt-stream` (the binaries demo-agent runs); `app/loop/audio.py` and `app/loop/segmenter.py` (loaded by path by demo-agent; **never moved or renamed**, and changed only with a demo-agent voice-test run); `app/loop/attribution.py` and `scripts/enroll_voiceprint.py` (the in-person voiceprint, demo-agent P4.3); the `○ CA` menu bar (starts demo-agent's control layer after ca#6); the leg grading tools.
2. The prime laws of 2026-08-11 are scrapped, by Rami's ruling of 2026-10-04 (demo-agent rule 15). Cite the rule; do not quote him. Say what replaces them: quality first; a cloud transcriber is allowed; the control layer's rules live in demo-agent `docs/rulings.md`.
3. What still binds: the HDFC rule (demo-agent rule 6); secrets in local env files only, never in git, chat or a terminal (rule 8); no terminal in daily use (the 2026-08-11 ruling; design §3.5 keeps it); explicit staging; STATUS.md in the same commit as any state change.
4. Where the retired loop is: the base sha of this lane, with the removed paths, so a reader can `git show <sha>:<path>`.
5. Who advises: the demo-agent advisor holds this repo (2026-10-04, STATUS log).

**STATUS.md:** replace the header (`Phase`, `Now`, `Next`) with the state after this lane. Keep every Log line; add one log line for this change (at most 350 characters) naming the base sha.
**README.md:** at most 15 lines: what the repo is now, how demo-agent uses it, and a pointer to CLAUDE.md.

## The change / Legs (in order)

1. **Base record.** At boot: base sha, the sha256 pair, `git ls-files app scripts prompts tests | wc -l`. Paste them in HANDOFF.
2. **RED.** `tests/test_ears_kept.py`: it loads `app/loop/audio.py` and `app/loop/segmenter.py` by file path with `importlib.util.spec_from_file_location`, the way demo-agent does, and asserts that no git-tracked file under `app/`, `scripts/` or `tests/` names `app.loop.orchestrator`, `app.loop.llm`, `app.loop.retrieval`, `app.loop.cost`, `app.loop.artifact` or `app.overlay`. Three files are exempt: `tests/test_ears_kept.py` itself, plus `scripts/run_call.sh` and `app/menubar/menubar.py`, which are ca#6's. It also asserts that no tracked file under `app/loop/` imports a removed module by relative import (`from .llm`, `from .cost`, `from .retrieval`, `from .artifact`). Run it at base: the import part passes, and the reference part FAILS (it names `scripts/llm_oneshot.py`, `tests/test_cost.py`, `app/loop/orchestrator.py`, ...). Paste the failure.
3. **Remove.** The list in BOUNDARY, `git rm` with explicit paths. Commit prefix `ca-retire-loop:`.
4. **GREEN.** `tests/test_ears_kept.py` passes with the leg 3 Python: `/Users/rami/orca/workspaces/demo-agent/owner-prompter-2/.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/`. The sha256 pair is unchanged (paste both runs).
5. **Write.** `CLAUDE.md`, `STATUS.md`, `README.md` per the pins. One commit, STATUS in it.
6. **Cross-repo check: NOT this lane's.** Design acceptance, "demo-agent's voice tests pass with `CALL_ASSISTANT_PATH` pointed at the new call-assistant main", is run by the owner in its demo-agent worktree against this branch. Say so in HANDOFF.

7. **USE leg**, #7: the manual act removed is a builder (or Rami) reading call-assistant's CLAUDE.md and having to work out by hand which of its laws and loops still apply. Who performs the use: the lane runs the kept modules against production inputs by loading them the way demo-agent does (leg 4). The owner will run demo-agent's voice tests against this branch, and Rami will read and approve the CLAUDE.md text on #7. Evidence pasted into HANDOFF.md: the leg 1 record, the leg 2 failure, the leg 4 output with both sha256 runs, and `git diff --stat <base>..HEAD`.

## Pins / Verdict line / PASS rule

- The sha256 pair at the end equals the pair at boot.
- `git diff --name-only <base>..HEAD` lists only the BOUNDARY paths.
- PASS = legs 2 and 4 green, the sha256 pair equal, the three documents written within their line caps, and the pushed sha named in DONE.

## Deliverables

0. A file called new has `git ls-files <path>` empty at the base sha (`tests/test_ears_kept.py`).
1. Commits `ca-retire-loop:` with explicit paths; HANDOFF.md in the worktree root carries the diff summary, the leg 1 record,
   the before and after test output, `Removed behaviour:` (the list of removed paths and what each did, one line each),
   and a `TEST:` block with indented `COMMAND: /Users/rami/orca/workspaces/demo-agent/owner-prompter-2/.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/`, `RED: exit 1` (leg 2 at base) and `GREEN: exit 0`.
   COST line: `COST ca-retire-loop: model=<id> effort=medium wall=<h:mm> rounds=0 spend≈$<list> saves≈n/a`.
   Never commit HANDOFF.md, BRIEF.md or flag files.
2. `touch <worktree>/HANDOFF-READY`, then signal the owner handle read at launch with
   `orca terminal send --terminal term_5cbbcac4-10c5-4ea8-9816-3e8a765aa1ef --enter --text 'NEEDS LANE-SIGNAL ca-retire-loop | DONE | pushed <sha>; kept modules sha256 equal, test green, CLAUDE.md for Rami'`.
   First act, the same way:
   `orca terminal send --terminal term_5cbbcac4-10c5-4ea8-9816-3e8a765aa1ef --enter --text 'UPDATE LANE-SIGNAL ca-retire-loop | UPDATE | BOOT reading the brief'`.
3. For a question unanswered by source, write ASK-ADVISOR in the worktree root with your proposal and signal
   `orca terminal send --terminal term_5cbbcac4-10c5-4ea8-9816-3e8a765aa1ef --enter --text 'NEEDS LANE-SIGNAL ca-retire-loop | ASK | <one line>'`.
   Signal before every approval request, blocker, question or finish; never stop silently.
   Accepted signal verbs: DONE, ASK, STOP, BLOCKED. No `$<digit>` in signal text; write arg 1 or field 2.
