# build-brief ca-menu-launch — the ○ CA menu bar starts and stops demo-agent's demo modes with a click (2026-10-05)
FEATURE: Rami starts a demo from the `○ CA` menu bar: he picks the account and clicks "Start demo (prompter)" or "Start demo (voice)". demo-agent's run starts in its own checkout, and in prompter mode its teleprompter window comes up. "Stop" ends the run the clean way, so its artifact gets its `run_end` row. "Open last run" opens that account's folder. If the run fails its own preflight (demo Chrome not up, not logged in), the menu says so in one line and names the log. No terminal. Shown by the menu and by `run-<ts>.jsonl` ending in `run_end` after a Stop.
STATUS: LAUNCHED 2026-10-05 by owner-prompter-2 (demo-agent plan 3ee09d2; kickoff §3 amended feb9627, brief written by the owner); opus-medium, stop $6.

**Category:** feature — milestone #1 (Prompter P2 — the control layer), design P2.4.
ISSUE: #6
BRANCH: Cipher-DLRT/ca-menu-launch
DESIGN: `Cipher-DLRT/demo-agent:docs/design-prompter-2026-10-04.md` §3.5 (last bullet) and §10 P2.4, on demo-agent origin/main. Facts: `app/menubar/menubar.py:17-18` starts `scripts/run_call.sh`, which starts `app.loop.orchestrator`, retired by #7. demo-agent's entry is `python -m app.agent run --mode {console,voice,prompter} --context <file>` (demo-agent `app/agent/__main__.py:350-357`). It needs an existing context file (`:23-29`); the run folder is that file's folder (`:288-294`). It ends cleanly, and `finish()` writes `run_end`, only when its stdin says `quit` or reaches EOF (`app/agent/loop.py:2308-2319`, `:2296-2306`, `:2262-2266`). A SIGINT skips `finish()`.
BRIEF-REVIEW: not required. HOSTS name none of the fenced systems (ADVISOR.md §D).

BOUNDARY: No writes outside this worktree.
Commit only here with explicit paths. **PUSH YOUR OWN LANE BRANCH, never main**, and name the pushed sha in DONE.
Push your lane branch after every commit.
Never write in `/Users/rami/dev/call-assistant` (the live checkout: the menu bar Rami uses runs from it) or in any demo-agent tree.

Touch only:
- `app/menubar/menubar.py` (rewrite);
- `app/menubar/launch.py` (new: pure helpers, no `rumps` import);
- `tests/test_menubar_launch.py` (new);
- `scripts/run_call.sh` (`git rm`: nothing will start it, and it starts retired code);
- `STATUS.md` (one log line, in the commit that changes behaviour; this repo's law 10).

Never `CLAUDE.md`, `README.md`, `app/loop/`, `app/capture/`, `app/stt/`, `scripts/menubar-launchagent.plist`. Lane ca-retire-loop (#7, built at `e33bcde`, landing after this one) rewrites `CLAUDE.md`, `README.md` and the STATUS header. Leave those to it.

HOSTS: none. Local files and tests only; `github.com` — push of your lane branch — write.
Read-only, outside this worktree: `/Users/rami/dev/demo-agent/app/agent/__main__.py` and `app/agent/loop.py` (the run CLI and its quit path), `/Users/rami/dev/demo-agent/demos/` (folder and file NAMES only, to test the account list; never open a file there), and `/Users/rami/dev/demo-agent/.venv/bin/python` (exists check only).
No model, vendor, orbit or demo-Chrome calls, and **never start demo-agent itself**: R5 holds the mic, speakers, orbit and the demo Chrome until 19:00Z on 2026-10-05, and a live start is the owner's USE leg.
An unlisted read or connection is an incident: stop, record the read and copy location, and ASK.
Secrets: none appear in chat, reports, git or terminals; report key names, byte lengths or sha256 prefixes.
Customer content stays on the box: report ids, counts and file names.

REASON: manual act removed: Rami opens a terminal, changes directory and types the run command, then types `quit` to end it, for every demo (the 2026-08-11 ruling that daily use needs no terminal, kept by design §3.5).
TIER: opus-medium. TIER-REASON: the advisor set Opus 5.5 for this lane (kickoff §3 amended feb9627). Rami prefers Opus, and an idle Codex lane cannot hear its owner until estate-tooling sendwait-p3 lands; medium fits one rewritten menu file and a helper module with pure tests.
Gate: NOT REQUIRED — §F all not-engaged, one revert restores with no data loss.
External review: NOT required — a local launcher; one git revert restores the old menu.

**Budget:** $6 at list (Opus 5.5). Stop at $6 and write HANDOFF. No live model spend. At $3 with legs 1–3 not green, signal ASK.

PREREQUISITES:
- The worktree is on `Cipher-DLRT/ca-menu-launch` cut from call-assistant origin/main immediately before launch (check: `git merge-base --is-ancestor origin/main HEAD` exits 0 at boot; if not, STOP and signal BLOCKED).
- Python for the tests: `spike/stt_bench/venv` in this worktree (gitignored), provisioned by the owner with `rumps`, `pytest` and `numpy`. Check: `spike/stt_bench/venv/bin/python -c "import rumps, pytest, numpy"` exits 0. Do NOT pip install.
- Baseline: `spike/stt_bench/venv/bin/python -B -m pytest -q -p no:cacheprovider tests/` passes at base. Paste its line.

§F CLASSIFICATION: grants/roles/credentials — not-engaged; containment/egress — not-engaged; external writes — not-engaged; column drop/alter — not-engaged; customer data off-box — not-engaged (the run log stays on the Mac, outside git).

## The rules

Read first: design §3.5 and §10 P2.4; `app/menubar/menubar.py` (all); `scripts/run_call.sh`; demo-agent `app/agent/__main__.py:23-29`, `:273-300`, `:350-370`; demo-agent `app/agent/loop.py:2239-2266`, `:2282-2320`.

Rulings carried, not re-decided: demo-agent `docs/rulings.md` rule 4 (share the Chrome window; the teleprompter window sits outside it), rule 8 (secrets: demo-agent reads its own env file, and the menu never reads or passes a key), rule 9 (explicit paths), rule 10 (Opus 5.5 or codex only), rule 18 (one control layer in demo-agent; this repo is its ears and its launcher); this repo's 2026-08-11 ruling of no terminal in daily use.

Pins:
- **Where demo-agent is.** `DEMO_AGENT_PATH` from the environment, default `/Users/rami/dev/demo-agent`; Python is `<DEMO_AGENT_PATH>/.venv/bin/python`; the working directory is `DEMO_AGENT_PATH`. This mirrors demo-agent's own `CALL_ASSISTANT_PATH`.
- **Menu.** Status line; then "Account ▸" (submenu); "Start demo (prompter)"; "Start demo (voice)"; "Stop"; "Open last run"; "Quit". No "assist" item yet: when demo-agent P1 #102 lands `--mode assist`, the owner adds it in a follow-up of a few lines. Write `MODES = {"Start demo (prompter)": "prompter", "Start demo (voice)": "voice"}` as the one place to add it.
- **Account list.** Under `<DEMO_AGENT_PATH>/demos/`, folders whose names start with a date (`YYYY-MM-DD-`) and that hold a file matching `context*.md`. Newest eight by folder name, newest first. When a folder has more than one such file, use `context.md` if present, else the first by name. The newest is selected at start; a click checks another. No folder means the Start items are disabled and the status reads `no account folder in demos/`. Folder names only; never open the file.
- **Start.** `subprocess.Popen([python, "-m", "app.agent", "run", "--mode", <mode>, "--context", <file>], cwd=DEMO_AGENT_PATH, stdin=subprocess.PIPE, stdout=<log>, stderr=subprocess.STDOUT, start_new_session=True)`. Keep stdin OPEN for the whole run: an EOF ends the run at once. The log is `~/Library/Logs/call-assistant/demo-<mode>-<YYYYMMDD-HHMMSS>.log`; it is never in git.
- **One run at a time.** This instance never starts a second while its child lives. Do not use `pgrep -f` to find runs that this instance did not start.
- **Stop = the clean path.** Write `quit\n` to the child's stdin and close it; wait up to 20 s for exit; then SIGINT the child's process group and wait 5 s; then SIGTERM. Record in the status which step ended it (`stopped (quit)`, `stopped (SIGINT: no run_end)`, `stopped (SIGTERM: no run_end)`). Stop never signals a process this instance did not start, so the old `pkill -INT -f` fallback goes.
- **Failure is visible.** If the child exits on its own, the status reads `○ ended (exit <code>): <last non-empty log line, 60 chars>` and keeps the log path for "Open last run". Exit 0 reads `○ ended`.
- **Open last run.** Opens the selected account folder in Finder (`open <folder>`); before any run, the selected account's folder.
- **Status title.** `◉ CA` while a child runs, `○ CA` otherwise; the status line names the mode and account while running. No cost or hint counts: those were the retired loop's files.
- **Pure helpers.** `launch.py` holds `account_folders(demos_dir)`, `context_file(folder)`, `run_command(python, mode, context)`, `stop_plan()` (the ordered steps) and `status_line(...)`, with no `rumps` and no subprocess at import. The tests drive these and a fake Popen. `menubar.py` stays thin.

## The change / Legs (in order)

1. **RED.** `tests/test_menubar_launch.py` at base fails (`app/menubar/launch.py` does not exist). It covers:
   - the account list over a `tmp_path` tree (dated and undated folders, folders with none, one or two `context*.md`, more than eight dated folders);
   - the exact argv and cwd for each mode;
   - Stop on a fake child that exits after `quit`, one that ignores `quit` (SIGINT reached), and one that ignores SIGINT (SIGTERM reached);
   - a start while a child lives is refused;
   - a child that exits 1 with a log ending in a `STOP:` line yields the ended status with that line.

   Paste the failure.
2. **BREAK.** stdin closed early (a fake child must not see EOF before Stop); a missing `.venv/bin/python` (Start disabled, status names the path); a log directory that does not exist yet (created); a `DEMO_AGENT_PATH` with spaces.
3. **Implement.** `launch.py`, the `menubar.py` rewrite, `git rm scripts/run_call.sh`, and the STATUS log line in the same commit. Commit prefix `ca-menu-launch:`; explicit paths; push after every commit.
4. **Import check, no GUI.** `spike/stt_bench/venv/bin/python -c "import app.menubar.menubar as m; print(sorted(m.MODES))"` prints the two items without opening the menu bar.
5. **Green.** `tests/` passes; paste the before and after lines.

6. **USE leg**, #6: the manual act removed is Rami opening a terminal to start and quit each demo. Who performs the use: the lane runs the launcher against production inputs only through the leg 1 and 4 checks (real account-folder names under `/Users/rami/dev/demo-agent/demos/`, the real argv). The owner will run the live leg after landing and after 19:00Z. It means a restart of the menu bar on the advisor's deploy, then Start (prompter) on a real account with the demo Chrome up, the window appearing, Stop, `run_end` at the end of `run-<ts>.jsonl`, and Open last run. Evidence pasted into HANDOFF.md: the leg 1, 4 and 5 outputs, and the account list the leg 1 helper prints for the real `demos/` (names only).

## Pins / Verdict line / PASS rule

- Leg 1's tests fail at base and pass after. Re-run the Stop test with the `quit` write removed and show it FAIL.
- `git diff --name-only <base>..HEAD` lists only the BOUNDARY touch list.
- PASS = legs 1, 2, 4 and 5 green, the diff scope held, and the pushed sha named in DONE.

## Deliverables

0. A file called new has `git ls-files <path>` empty at the base sha (`app/menubar/launch.py`, `tests/test_menubar_launch.py`).
1. Commits `ca-menu-launch:` with explicit paths; HANDOFF.md in the worktree root carries the diff summary,
   before/after test lines, the leg 4 output, `Removed behaviour:` (the orchestrator start items, the hint/cost status, the `pkill` fallback, `scripts/run_call.sh`),
   and a `TEST:` block with indented `COMMAND: spike/stt_bench/venv/bin/python -B -m pytest -q -p no:cacheprovider tests/`, `RED: exit 1` (leg 1 at base) and `GREEN: exit 0`.
   COST line: `COST ca-menu-launch: model=<id> effort=medium wall=<h:mm> rounds=0 spend≈$<list> saves≈<min per demo>`.
   Never commit HANDOFF.md, BRIEF.md or flag files.
2. `touch <worktree>/HANDOFF-READY`, then signal the owner handle read at launch with
   `orca terminal send --terminal term_5cbbcac4-10c5-4ea8-9816-3e8a765aa1ef --enter --text 'NEEDS LANE-SIGNAL ca-menu-launch | DONE | pushed <sha>; tests <n> green, menu imports, live leg is the owner's'`.
   First act, the same way:
   `orca terminal send --terminal term_5cbbcac4-10c5-4ea8-9816-3e8a765aa1ef --enter --text 'UPDATE LANE-SIGNAL ca-menu-launch | UPDATE | BOOT reading the brief'`.
3. For a question unanswered by source, write ASK-ADVISOR in the worktree root with your proposal and signal
   `orca terminal send --terminal term_5cbbcac4-10c5-4ea8-9816-3e8a765aa1ef --enter --text 'NEEDS LANE-SIGNAL ca-menu-launch | ASK | <one line>'`.
   Signal before every approval request, blocker, question or finish; never stop silently.
   Accepted signal verbs: DONE, ASK, STOP, BLOCKED. No `$<digit>` in signal text; write arg 1 or field 2.
