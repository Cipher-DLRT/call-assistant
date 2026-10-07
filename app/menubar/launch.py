# P2.4 launcher helpers for the ○ CA menu (#6): start and stop demo-agent's
# run CLI. Pure: no rumps, no subprocess at import; menubar.py stays thin.
#
# Stop is the clean path first: demo-agent writes `run_end` only when its
# stdin says `quit` or reaches EOF (demo-agent app/agent/loop.py
# _read_console). A SIGINT skips finish(), so it is the fallback, not the
# default. This instance only ever signals the child it started.

import os
import re
import signal
from datetime import datetime
from pathlib import Path

DEFAULT_DEMO_AGENT_PATH = "/Users/rami/dev/demo-agent"
LOG_DIR = Path.home() / "Library/Logs/call-assistant"
# the one place to add a mode; assist came with demo-agent #102 (16439dd)
MODES = {"Start demo (prompter)": "prompter", "Start demo (voice)": "voice",
         "Start assist": "assist"}
MAX_ACCOUNTS = 8
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def demo_agent_path(env=os.environ):
    return Path(env.get("DEMO_AGENT_PATH") or DEFAULT_DEMO_AGENT_PATH)


def python_path(agent):
    return Path(agent) / ".venv/bin/python"


def context_file(folder):
    """context.md if present, else the first context*.md by name. Names only:
    the file is never opened here."""
    files = sorted(p for p in Path(folder).glob("context*.md") if p.is_file())
    for p in files:
        if p.name == "context.md":
            return p
    return files[0] if files else None


def account_folders(demos_dir):
    """Dated folders (YYYY-MM-DD-...) holding a context*.md, newest 8 first."""
    demos = Path(demos_dir)
    if not demos.is_dir():
        return []
    dirs = sorted((p for p in demos.iterdir()
                   if p.is_dir() and DATED.match(p.name) and context_file(p)),
                  key=lambda p: p.name, reverse=True)
    return dirs[:MAX_ACCOUNTS]


def run_command(python, mode, context):
    if mode == "assist":
        # assist takes no --context: the account is the dated folder's name
        # without its date, and demo-agent opens today's folder for it
        return [str(python), "-m", "app.agent", "run", "--mode", "assist",
                "--account", DATED.sub("", Path(context).parent.name)]
    return [str(python), "-m", "app.agent", "run",
            "--mode", mode, "--context", str(context)]


def log_path(log_dir, mode, now):
    return Path(log_dir) / f"demo-{mode}-{now:%Y%m%d-%H%M%S}.log"


def stop_plan():
    """(step, seconds to wait for exit after it), in order."""
    return [("quit", 20), ("SIGINT", 5), ("SIGTERM", 5)]


def last_log_line(path, width=60):
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return ""
    for line in reversed(lines):
        if line.strip():
            return line.strip()[:width]
    return ""


def status_line(state, mode=None, account=None, code=None, last_line="",
                step=None, python=None):
    if state == "running":
        return f"◉ {mode} · {account}"
    if state == "ended":
        if code == 0:
            return "○ ended"
        return f"○ ended (exit {code}): {last_line}"
    if state == "stopped":
        return "○ stopped (quit)" if step == "quit" else \
            f"○ stopped ({step}: no run_end)"
    if state == "no_account":
        return "○ no account folder in demos/"
    if state == "no_python":
        return f"○ no python at {python}"
    return "○ ready"


class Launcher:
    """One demo-agent child at a time, started and stopped by this instance."""

    def __init__(self, agent, log_dir=LOG_DIR, popen=None, killpg=None,
                 now=datetime.now):
        self.agent = Path(agent)
        self.python = python_path(self.agent)
        self.log_dir = Path(log_dir)
        self._popen = popen
        self._killpg = killpg or os.killpg
        self._now = now
        self.child = None
        self.mode = None
        self.log = None
        self.stopped_by = None

    def running(self):
        return self.child is not None and self.child.poll() is None

    def start(self, mode, context):
        if self.running() or not self.python.exists():
            return False
        import subprocess
        popen = self._popen or subprocess.Popen
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log = log_path(self.log_dir, mode, self._now())
        with open(self.log, "a") as out:
            # stdin stays open for the whole run: an EOF ends it at once
            self.child = popen(run_command(self.python, mode, context),
                               cwd=str(self.agent), stdin=subprocess.PIPE,
                               stdout=out, stderr=subprocess.STDOUT,
                               start_new_session=True)
        self.mode = mode
        self.stopped_by = None
        return True

    def stop(self):
        """Returns the step that ended the child, or None if none ran."""
        if not self.running():
            return None
        import subprocess
        child = self.child
        for step, timeout in stop_plan():
            if step == "quit":
                try:
                    child.stdin.write(b"quit\n")
                    child.stdin.flush()
                except (BrokenPipeError, OSError):
                    pass
                try:
                    child.stdin.close()
                except (BrokenPipeError, OSError):
                    pass
            else:
                try:
                    # start_new_session: the child's pgid is its pid
                    self._killpg(child.pid, getattr(signal, step))
                except ProcessLookupError:
                    pass
            try:
                child.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                continue
            self.stopped_by = step
            return step
        self.stopped_by = "SIGTERM"
        return "SIGTERM"

    def status(self, account=None):
        if self.child is None:
            return status_line("idle")
        code = self.child.poll()
        if code is None:
            return status_line("running", mode=self.mode, account=account)
        if self.stopped_by:
            return status_line("stopped", step=self.stopped_by)
        return status_line("ended", code=code, last_line=last_log_line(self.log))
