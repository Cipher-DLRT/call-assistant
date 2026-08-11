# P1.5 menu-bar launcher (operator ruling: no terminal in daily use).
# rumps (MIT). Start = spawn scripts/run_call.sh exactly as the runbook
# command would; Stop = SIGINT to the process group (same clean path as
# Ctrl-C: artifact + sheets finalize). Crash law: menubar dies -> loop
# unaffected (own session); loop dies -> menu shows ○ stopped.
#
#   ./spike/stt_bench/venv/bin/python -m app.menubar.menubar

import json
import os
import signal
import subprocess
from pathlib import Path

import rumps

REPO = Path(__file__).resolve().parent.parent.parent
RUN_CALL = REPO / "scripts/run_call.sh"
CALLS = REPO / "calls"


def newest_call_dir():
    dirs = sorted(CALLS.glob("*"), key=lambda p: p.name, reverse=True)
    return dirs[0] if dirs else None


class CallAssistant(rumps.App):
    def __init__(self):
        super().__init__("○ CA", quit_button="Quit")
        self.proc = None
        self.status_item = rumps.MenuItem("○ stopped")
        self.status_item.set_callback(None)
        self.item_online = rumps.MenuItem("Start Shadow (online)",
                                          callback=self.start_online)
        self.item_inperson = rumps.MenuItem("Start Shadow (in-person)",
                                            callback=self.start_inperson)
        self.item_stop = rumps.MenuItem("Stop", callback=self.stop)
        self.menu = [
            self.status_item,
            None,
            self.item_online,
            self.item_inperson,
            self.item_stop,
            None,
            rumps.MenuItem("Open Last Call", callback=self.open_last),
        ]
        rumps.Timer(self.refresh, 2).start()

    @staticmethod
    def _any_call_running():
        """True if ANY orchestrator runs on this Mac — including calls not
        started by this menubar instance (double-capture guard)."""
        r = subprocess.run(["pgrep", "-f", "app.loop.orchestrator"],
                           capture_output=True)
        return r.returncode == 0

    # -- actions ------------------------------------------------------------
    def _start(self, mode):
        if self._any_call_running():
            return  # never start a second capture (double-overlay guard)
        # own session so a menubar crash never takes the loop down
        self.proc = subprocess.Popen([str(RUN_CALL), mode],
                                     cwd=str(REPO), start_new_session=True,
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)

    def start_online(self, _):
        self._start("online")

    def start_inperson(self, _):
        self._start("inperson")

    def stop(self, _):
        if self.proc and self.proc.poll() is None:
            # SIGINT to the group = run_call.sh trap = orchestrator finalize
            try:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGINT)
                return
            except (ProcessLookupError, PermissionError):
                pass  # already gone / reaped between poll() and killpg()
        # calls this instance didn't start: SIGINT the orchestrator directly
        # (its handler finalizes artifact + sheets)
        subprocess.run(["pkill", "-INT", "-f", "app.loop.orchestrator"],
                       capture_output=True)

    def open_last(self, _):
        d = newest_call_dir()
        if d:
            subprocess.run(["open", str(d)], check=False)

    # -- status line --------------------------------------------------------
    def refresh(self, _timer):
        running = self._any_call_running()
        # grey Start while ANY call runs; Stop only lit while one does
        self.item_online.set_callback(None if running else self.start_online)
        self.item_inperson.set_callback(None if running else self.start_inperson)
        self.item_stop.set_callback(self.stop if running else None)
        d = newest_call_dir()
        hints = 0
        cost = None
        if d:
            feed = d / "feed.jsonl"
            if feed.exists():
                try:
                    hints = sum(1 for line in feed.open()
                                if '"type": "hint"' in line or '"type":"hint"' in line)
                except OSError:
                    pass
            art = d / "artifact.json"
            if art.exists():
                try:
                    cost = json.loads(art.read_text())["cost"]["total_usd"]
                except (OSError, KeyError, json.JSONDecodeError):
                    pass
        if running:
            self.title = "◉ CA"
            self.status_item.title = f"◉ recording · {hints} hints"
        else:
            self.title = "○ CA"
            tail = f" · ${cost}" if cost is not None else ""
            self.status_item.title = f"○ stopped · {hints} hints{tail}"


if __name__ == "__main__":
    CallAssistant().run()
