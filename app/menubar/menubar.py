# P2.4 menu-bar launcher (operator ruling: no terminal in daily use).
# rumps (MIT). Start = demo-agent's run CLI in its own checkout
# (DEMO_AGENT_PATH); Stop = `quit` on its stdin, so its artifact gets
# run_end, then SIGINT / SIGTERM to its group (app/menubar/launch.py).
# The child holds this process's stdin pipe: if the menu bar quits, the
# child reads EOF and ends cleanly.
#
#   ./spike/stt_bench/venv/bin/python -m app.menubar.menubar

import subprocess
import threading

import rumps

from app.menubar.launch import (Launcher, MODES, account_folders,
                                context_file, demo_agent_path, status_line)


class CallAssistant(rumps.App):
    def __init__(self):
        super().__init__("○ CA", quit_button="Quit")
        self.agent = demo_agent_path()
        self.launcher = Launcher(self.agent)
        self.stopping = False
        self.accounts = account_folders(self.agent / "demos")
        self.account = self.accounts[0] if self.accounts else None
        self.run_account = None
        self.status_item = rumps.MenuItem("○ ready")
        self.log_item = rumps.MenuItem("")
        self.account_items = [rumps.MenuItem(p.name, callback=self.pick)
                              for p in self.accounts]
        if self.account_items:
            self.account_items[0].state = 1
        self.start_items = {title: rumps.MenuItem(title, callback=self.start)
                            for title in MODES}
        self.item_stop = rumps.MenuItem("Stop", callback=self.stop)
        self.menu = [
            self.status_item,
            self.log_item,
            None,
            (rumps.MenuItem("Account"), self.account_items or ["(none)"]),
            *self.start_items.values(),
            self.item_stop,
            None,
            rumps.MenuItem("Open last run", callback=self.open_last),
        ]
        self.refresh(None)
        rumps.Timer(self.refresh, 2).start()

    # -- actions ------------------------------------------------------------
    def pick(self, item):
        for i, it in enumerate(self.account_items):
            it.state = int(it is item)
            if it is item:
                self.account = self.accounts[i]
        self.refresh(None)

    def start(self, item):
        if self.account is None:
            return
        if self.launcher.start(MODES[item.title], context_file(self.account)):
            self.run_account = self.account
        self.refresh(None)

    def stop(self, _):
        # up to 30 s of waits: off the main thread so the menu stays live
        self.stopping = True
        def run():
            self.launcher.stop()
            self.stopping = False
        threading.Thread(target=run, daemon=True).start()
        self.refresh(None)

    def open_last(self, _):
        if self.account is not None:
            subprocess.run(["open", str(self.account)], check=False)
        if self.launcher.log and self.status_item.title.startswith("○ ended ("):
            subprocess.run(["open", "-R", str(self.launcher.log)], check=False)

    # -- status line --------------------------------------------------------
    def refresh(self, _timer):
        running = self.launcher.running()
        can_start = (not running and self.account is not None
                     and self.launcher.python.exists())
        for title, it in self.start_items.items():
            it.set_callback(self.start if can_start else None)
        self.item_stop.set_callback(
            self.stop if running and not self.stopping else None)
        self.title = "◉ CA" if running else "○ CA"
        if self.account is None:
            status = status_line("no_account")
        elif not running and not self.launcher.python.exists():
            status = status_line("no_python", python=self.launcher.python)
        else:
            status = self.launcher.status(
                account=(self.run_account or self.account).name)
        self.status_item.title = status
        self.log_item.title = (f"log: {self.launcher.log}"
                               if self.launcher.log else "log: no run yet")


if __name__ == "__main__":
    CallAssistant().run()
