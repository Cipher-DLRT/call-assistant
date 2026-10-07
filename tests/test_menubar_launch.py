"""ca-menu-launch (#6, P2.4): the ○ CA menu starts and stops demo-agent runs.

Pure helpers in app.menubar.launch, driven with tmp_path trees and a fake
Popen. Nothing here starts demo-agent.
"""
import signal
import subprocess
from datetime import datetime

import pytest

from app.menubar import launch


# -- account list --------------------------------------------------------------

def _folder(root, name, *files):
    d = root / name
    d.mkdir(parents=True)
    for f in files:
        (d / f).write_text("x")
    return d


def test_account_folders_dated_with_context_newest_first(tmp_path):
    _folder(tmp_path, "2026-07-21-acme", "context-pack.md")
    _folder(tmp_path, "2026-09-01-beta", "context.md", "context-old.md")
    _folder(tmp_path, "2026-08-01-none", "plan.md")          # no context*.md
    _folder(tmp_path, "manual", "context.md")                # undated
    _folder(tmp_path, "leg6c-r2", "context.md")              # undated
    (tmp_path / "2026-10-01-file.md").write_text("x")        # not a folder
    names = [p.name for p in launch.account_folders(tmp_path)]
    assert names == ["2026-09-01-beta", "2026-07-21-acme"]


def test_account_folders_newest_eight(tmp_path):
    for day in range(1, 12):
        _folder(tmp_path, f"2026-09-{day:02d}-acct", "context.md")
    names = [p.name for p in launch.account_folders(tmp_path)]
    assert len(names) == 8
    assert names[0] == "2026-09-11-acct"
    assert names[-1] == "2026-09-04-acct"


def test_account_folders_missing_dir(tmp_path):
    assert launch.account_folders(tmp_path / "nope") == []


def test_context_file_prefers_context_md(tmp_path):
    d = _folder(tmp_path, "2026-09-01-a", "context-z.md", "context.md")
    assert launch.context_file(d) == d / "context.md"


def test_context_file_first_by_name(tmp_path):
    d = _folder(tmp_path, "2026-09-01-a", "context-z.md", "context-pack.md")
    assert launch.context_file(d) == d / "context-pack.md"


def test_context_file_none(tmp_path):
    d = _folder(tmp_path, "2026-09-01-a", "plan.md")
    assert launch.context_file(d) is None


# -- argv, cwd, log --------------------------------------------------------------

@pytest.mark.parametrize("mode", ["prompter", "voice"])
def test_run_command_argv(mode):
    argv = launch.run_command("/d/.venv/bin/python", mode, "/d/demos/x/context.md")
    assert argv == ["/d/.venv/bin/python", "-m", "app.agent", "run",
                    "--mode", mode, "--context", "/d/demos/x/context.md"]


def test_modes_map_items_to_modes():
    assert launch.MODES == {"Start demo (prompter)": "prompter",
                            "Start demo (voice)": "voice",
                            "Start assist": "assist"}


def test_assist_passes_the_account_slug_not_the_context():
    argv = launch.run_command("/d/.venv/bin/python", "assist",
                              "/d/demos/2026-07-21-fujairah-backtest/context.md")
    assert argv == ["/d/.venv/bin/python", "-m", "app.agent", "run",
                    "--mode", "assist", "--account", "fujairah-backtest"]
    assert "--context" not in argv


def test_demo_agent_path_env_and_default():
    assert launch.demo_agent_path({}) == launch.Path("/Users/rami/dev/demo-agent")
    assert launch.demo_agent_path({"DEMO_AGENT_PATH": "/x y/da"}) == launch.Path("/x y/da")
    assert launch.python_path(launch.Path("/x y/da")) == launch.Path("/x y/da/.venv/bin/python")


def test_log_path():
    p = launch.log_path(launch.Path("/logs"), "voice", datetime(2026, 10, 5, 19, 1, 2))
    assert p == launch.Path("/logs/demo-voice-20261005-190102.log")


# -- fake Popen ----------------------------------------------------------------

class FakeStdin:
    def __init__(self, child):
        self.child = child
        self.written = b""
        self.closed = False

    def write(self, data):
        assert not self.closed, "write after close"
        self.written += data

    def flush(self):
        pass

    def close(self):
        self.closed = True
        self.child.events.append("stdin-closed")


class FakeChild:
    """obeys: which signal ends it -- 'quit', 'SIGINT', 'SIGTERM'."""

    def __init__(self, obeys="quit", pid=4242):
        self.obeys = obeys
        self.pid = pid
        self.events = []
        self.stdin = FakeStdin(self)
        self.returncode = None

    def _ended(self):
        if self.returncode is not None:
            return True
        if self.obeys == "quit" and b"quit\n" in self.stdin.written:
            self.returncode = 0
        return self.returncode is not None

    def poll(self):
        return self.returncode if self._ended() else None

    def wait(self, timeout=None):
        self.events.append(f"wait {timeout}")
        if self._ended():
            return self.returncode
        raise subprocess.TimeoutExpired("fake", timeout)

    def signal(self, sig):
        self.events.append(f"sig {sig.name}")
        if sig.name == self.obeys or sig == signal.SIGTERM:
            self.returncode = -sig


class Harness:
    def __init__(self, tmp_path, child=None, agent=None):
        self.agent = agent or tmp_path / "demo-agent"
        py = launch.python_path(self.agent)
        py.parent.mkdir(parents=True, exist_ok=True)
        py.write_text("")
        self.log_dir = tmp_path / "Logs" / "call-assistant"   # does not exist yet
        self.child = child or FakeChild()
        self.calls = []
        self.launcher = launch.Launcher(
            self.agent, self.log_dir, popen=self.popen, killpg=self.killpg,
            now=lambda: datetime(2026, 10, 5, 19, 0, 0))

    def popen(self, argv, **kw):
        self.calls.append((argv, kw))
        kw["stdout"].write("booting\n")
        return self.child

    def killpg(self, pgid, sig):
        assert pgid == self.child.pid
        self.child.signal(signal.Signals(sig))


def test_start_argv_cwd_and_stdin_kept_open(tmp_path):
    h = Harness(tmp_path)
    ctx = tmp_path / "ctx.md"
    assert h.launcher.start("prompter", ctx) is True
    argv, kw = h.calls[0]
    assert argv == [str(launch.python_path(h.agent)), "-m", "app.agent", "run",
                    "--mode", "prompter", "--context", str(ctx)]
    assert kw["cwd"] == str(h.agent)
    assert kw["stdin"] == subprocess.PIPE
    assert kw["stderr"] == subprocess.STDOUT
    assert kw["start_new_session"] is True
    # BREAK: an EOF ends the run at once -- stdin must stay open until Stop
    assert h.child.stdin.closed is False
    assert h.child.stdin.written == b""
    assert h.launcher.running()


def test_start_creates_log_dir(tmp_path):
    h = Harness(tmp_path)
    assert not h.log_dir.exists()
    h.launcher.start("voice", tmp_path / "ctx.md")
    assert h.launcher.log == h.log_dir / "demo-voice-20261005-190000.log"
    assert h.launcher.log.read_text() == "booting\n"


def test_start_refused_while_child_lives(tmp_path):
    h = Harness(tmp_path, FakeChild(obeys="never"))
    assert h.launcher.start("prompter", tmp_path / "ctx.md") is True
    assert h.launcher.start("voice", tmp_path / "ctx.md") is False
    assert len(h.calls) == 1


def test_start_refused_without_python(tmp_path):
    h = Harness(tmp_path)
    launch.python_path(h.agent).unlink()
    assert h.launcher.start("prompter", tmp_path / "ctx.md") is False
    assert h.calls == []


def test_demo_agent_path_with_spaces(tmp_path):
    h = Harness(tmp_path, agent=tmp_path / "with space" / "demo agent")
    h.launcher.start("prompter", tmp_path / "ctx.md")
    argv, kw = h.calls[0]
    assert argv[0] == str(tmp_path / "with space" / "demo agent" / ".venv/bin/python")
    assert kw["cwd"] == str(tmp_path / "with space" / "demo agent")


# -- stop ------------------------------------------------------------------------

def test_stop_plan_order():
    assert launch.stop_plan() == [("quit", 20), ("SIGINT", 5), ("SIGTERM", 5)]


def test_stop_quit_is_clean(tmp_path):
    h = Harness(tmp_path, FakeChild(obeys="quit"))
    h.launcher.start("prompter", tmp_path / "ctx.md")
    assert h.launcher.stop() == "quit"
    assert h.child.stdin.written == b"quit\n"
    assert h.child.events == ["stdin-closed", "wait 20"]
    assert not h.launcher.running()


def test_stop_reaches_sigint(tmp_path):
    h = Harness(tmp_path, FakeChild(obeys="SIGINT"))
    h.launcher.start("prompter", tmp_path / "ctx.md")
    assert h.launcher.stop() == "SIGINT"
    assert h.child.events == ["stdin-closed", "wait 20", "sig SIGINT", "wait 5"]


def test_stop_reaches_sigterm(tmp_path):
    h = Harness(tmp_path, FakeChild(obeys="never"))
    h.launcher.start("prompter", tmp_path / "ctx.md")
    assert h.launcher.stop() == "SIGTERM"
    assert h.child.events == ["stdin-closed", "wait 20", "sig SIGINT", "wait 5",
                              "sig SIGTERM", "wait 5"]


def test_stop_without_child_signals_nothing(tmp_path):
    h = Harness(tmp_path)
    assert h.launcher.stop() is None
    assert h.child.events == []


# -- status ------------------------------------------------------------------

def test_child_exit_1_shows_stop_line(tmp_path):
    h = Harness(tmp_path, FakeChild(obeys="never"))
    h.launcher.start("prompter", tmp_path / "ctx.md")
    with open(h.launcher.log, "a") as f:
        f.write("AI sales engineer\nSTOP: demo Chrome is not logged in to orbit\n\n")
    h.child.returncode = 1
    assert not h.launcher.running()
    assert h.launcher.status() == (
        "○ ended (exit 1): STOP: demo Chrome is not logged in to orbit")
    assert h.launcher.log.exists()


def test_child_exit_0_reads_ended(tmp_path):
    h = Harness(tmp_path, FakeChild(obeys="never"))
    h.launcher.start("voice", tmp_path / "ctx.md")
    h.child.returncode = 0
    assert h.launcher.status() == "○ ended"


def test_last_log_line_truncates(tmp_path):
    log = tmp_path / "x.log"
    log.write_text("first\n" + "y" * 100 + "\n  \n")
    assert launch.last_log_line(log) == "y" * 60
    assert launch.last_log_line(tmp_path / "missing.log") == ""


def test_status_lines():
    assert launch.status_line("running", mode="prompter",
                              account="2026-09-01-beta") == "◉ prompter · 2026-09-01-beta"
    assert launch.status_line("stopped", step="quit") == "○ stopped (quit)"
    assert launch.status_line("stopped", step="SIGINT") == "○ stopped (SIGINT: no run_end)"
    assert launch.status_line("stopped", step="SIGTERM") == "○ stopped (SIGTERM: no run_end)"
    assert launch.status_line("no_account") == "○ no account folder in demos/"
    assert launch.status_line("no_python", python="/x y/.venv/bin/python") == (
        "○ no python at /x y/.venv/bin/python")
    assert launch.status_line("idle") == "○ ready"


def test_status_after_stop(tmp_path):
    h = Harness(tmp_path, FakeChild(obeys="SIGINT"))
    h.launcher.start("prompter", tmp_path / "ctx.md")
    h.launcher.stop()
    assert h.launcher.status() == "○ stopped (SIGINT: no run_end)"


def test_no_rumps_or_subprocess_at_import():
    src = launch.__file__
    text = open(src).read()
    assert "import rumps" not in text
    top = [ln for ln in text.splitlines() if ln.startswith(("import ", "from "))]
    assert not any("subprocess" in ln for ln in top)
