import json
import sys
import time
from pathlib import Path


# Glance design: the accent bar carries the lock state (teal = shareable,
# amber = 🔒 internal — read the color before the words); newest card is
# brightest, older cards dim. Everything else stays quiet.
WIDTH = 380
POLL_MS = 200
BACKGROUND = "#101214"
CARD = "#1b1e22"
FOREGROUND = "#f2efe9"
DIMMED = "#b8b2a7"
MUTED = "#7d786f"
ACCENT_OK = "#3ea08d"      # shareable
ACCENT_LOCK = "#c98a2b"    # internal — matches the 🔒
NOTICE_BG = "#5c3a10"
FONT_HINT = ("TkDefaultFont", 13)
FONT_META = ("TkDefaultFont", 10)
CARD_TTL_S = 120   # cards auto-expire; click a card to dismiss it early


class Overlay:
    def __init__(self, root, tk, feed_path):
        self.root = root
        self.tk = tk
        self.feed_path = Path(feed_path)
        self.offset = 0
        self.pending = b""
        self.hints = []
        self.notice = None

        root.configure(bg=BACKGROUND)
        # aquaTk quirk (hit live in the P1 build): overrideredirect before the
        # window is mapped leaves the title bar in place. Map first, then strip.
        root.update_idletasks()
        try:
            root.tk.call("::tk::unsupported::MacWindowStyle", "style",
                         root._w, "help", "noActivates")
        except Exception:
            pass
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.lift()
        self.body = tk.Frame(root, bg=BACKGROUND, padx=10, pady=8)
        self.body.pack(fill="both", expand=True)
        root.update_idletasks()
        x = max(0, root.winfo_screenwidth() - WIDTH - 16)
        root.geometry(f"{WIDTH}x1+{x}+16")
        root.withdraw()   # hidden until the first card arrives
        self._schedule()

    def _safe_poll(self):
        try:
            self._poll()
        except Exception:
            pass
        try:
            self._schedule()
        except Exception:
            pass

    def _schedule(self):
        self.root.after(POLL_MS, self._safe_poll)

    def _poll(self):
        try:
            size = self.feed_path.stat().st_size
        except OSError:
            return
        if size < self.offset:
            self.offset = 0
            self.pending = b""
        try:
            with self.feed_path.open("rb") as feed:
                feed.seek(self.offset)
                chunk = feed.read()
                self.offset = feed.tell()
        except OSError:
            return
        if not chunk:
            return

        parts = (self.pending + chunk).split(b"\n")
        self.pending = parts.pop()
        changed = False
        for raw_line in parts:
            try:
                item = json.loads(raw_line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if not isinstance(item, dict):
                continue
            if item.get("type") == "notice" and isinstance(item.get("text"), str):
                self.notice = item["text"]
                changed = True
            elif item.get("type") == "hint" and isinstance(item.get("text"), str):
                item["_arrived"] = time.monotonic()
                self.hints.insert(0, item)
                self.hints = self.hints[:4]
                changed = True
        # auto-expire old cards even when nothing new arrives
        now = time.monotonic()
        fresh = [h for h in self.hints if now - h["_arrived"] < CARD_TTL_S]
        if len(fresh) != len(self.hints):
            self.hints = fresh
            changed = True
        if changed:
            self._render()

    def _dismiss(self, hint):
        self.hints = [h for h in self.hints if h is not hint]
        self._render()

    def _render(self):
        for child in self.body.winfo_children():
            child.destroy()
        if not self.hints and self.notice is None:
            self.root.withdraw()   # no black bar when the last card goes
            return
        self.root.deiconify()
        self.root.attributes("-topmost", True)
        if self.notice is not None:
            self.tk.Label(
                self.body, text=self.notice, bg=NOTICE_BG, fg=FOREGROUND,
                justify="left", anchor="w", wraplength=WIDTH - 36,
                font=FONT_META, padx=8, pady=6,
            ).pack(fill="x", pady=(0, 6))
        for i, hint in enumerate(self.hints):
            card = self.tk.Frame(self.body, bg=CARD)
            card.pack(fill="x", pady=(0, 5))
            accent = ACCENT_LOCK if hint.get("locked") else ACCENT_OK
            self.tk.Frame(card, bg=accent, width=3).pack(side="left", fill="y")
            inner = self.tk.Frame(card, bg=CARD, padx=8, pady=6)
            inner.pack(side="left", fill="x", expand=True)
            fg = FOREGROUND if i == 0 else DIMMED
            prefix = "🔒 " if hint.get("locked") else ""
            self.tk.Label(
                inner, text=prefix + hint["text"], bg=CARD, fg=fg,
                justify="left", anchor="w", wraplength=WIDTH - 56,
                font=FONT_HINT,
            ).pack(fill="x")
            if hint.get("stale") and hint.get("verified_at"):
                date = str(hint["verified_at"])[:10]
                self.tk.Label(
                    inner, text=f"⏳ verified {date}", bg=CARD, fg=MUTED,
                    font=FONT_META, anchor="w",
                ).pack(fill="x", pady=(2, 0))
            # click anywhere on the card to dismiss it
            for widget in (card, inner, *inner.winfo_children()):
                widget.bind("<Button-1>",
                            lambda _e, h=hint: self._dismiss(h))
        self.root.update_idletasks()
        height = max(1, self.body.winfo_reqheight())
        x = max(0, self.root.winfo_screenwidth() - WIDTH - 16)
        self.root.geometry(f"{WIDTH}x{height}+{x}+16")


def main():
    if len(sys.argv) != 2:
        return 0
    try:
        import tkinter as tk
        root = tk.Tk()
        Overlay(root, tk, sys.argv[1])
        root.mainloop()
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
