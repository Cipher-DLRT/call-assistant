#!/bin/sh
# Install this repo's tracked git hooks into the working git hooks directory.
#
# Git does not version .git/hooks, so a tracked copy alone does not protect anything --
# a fresh clone starts with no hooks at all. Run this once after cloning, and again after
# any change to scripts/hooks/.
#
# Why this exists: on 2026-09-07 the budget gates were found installed in all three estate
# repos but tracked in only one. A defect fixed in the installed copy would have been lost
# in two of them on the next clone, and there was no way to tell an installed hook from a
# stale one.
#
# Safe to re-run. Verifies every hook after copying and fails loudly on a mismatch.
#
# Seat mode is run by the OVERSEER, at each advisor seat's §39b restart, before the
# relaunch (docs/OVERSEER.md §4 item 5):
#     install.sh --seat <main-checkout-path>
set -e

if [ "${1-}" = "--seat" ]; then
  [ "$#" -eq 2 ] || { echo "usage: $0 --seat <main-checkout-path>" >&2; exit 2; }
  checkout=$2
  [ -d "$checkout" ] || { echo "seat checkout does not exist: $checkout" >&2; exit 2; }
  settings="$checkout/.claude/settings.local.json"
  mkdir -p "$checkout/.claude"
  python3 - "$settings" <<'PY'
import json
import os
import sys
import tempfile

path = sys.argv[1]
if os.path.exists(path):
    with open(path, encoding='utf-8') as src:
        settings = json.load(src)
else:
    settings = {}

entry = {
    "matcher": "SendMessage",
    "hooks": [{
        "type": "command",
        "command": "/Users/rami/dev/work-automation/scripts/hooks/sendmessage-gate.sh",
    }],
}
hooks = settings.setdefault("hooks", {})
pre = hooks.setdefault("PreToolUse", [])
if entry not in pre:
    pre.append(entry)

rendered = json.dumps(settings, indent=2, ensure_ascii=False) + "\n"
fd, pending = tempfile.mkstemp(prefix=".settings.local.", dir=os.path.dirname(path), text=True)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as dst:
        dst.write(rendered)
        dst.flush()
        os.fsync(dst.fileno())
    os.replace(pending, path)
except Exception:
    try:
        os.unlink(pending)
    except FileNotFoundError:
        pass
    raise
print(rendered, end="")
PY
  exit 0
fi

[ "$#" -eq 0 ] || { echo "usage: $0 [--seat <main-checkout-path>]" >&2; exit 2; }
top=$(git rev-parse --show-toplevel) || exit 1
gitdir=$(git rev-parse --git-common-dir)
case "$gitdir" in /*) ;; *) gitdir="$top/$gitdir" ;; esac
src="$top/scripts/hooks"
dst="$gitdir/hooks"

[ -d "$src" ] || { echo "no $src -- nothing to install"; exit 0; }
mkdir -p "$dst"

rc=0
for f in "$src"/*; do
  [ -f "$f" ] || continue
  name=$(basename "$f")
  case "$name" in
    install.sh|sendmessage-gate.sh|sendmessage-gate-selftest.sh|walk-brief-lint.py) continue ;;
  esac
  cp "$f" "$dst/$name"
  chmod +x "$dst/$name"
  if cmp -s "$f" "$dst/$name"; then
    echo "  installed  $name"
  else
    echo "  FAILED     $name -- installed copy differs from tracked source" >&2
    rc=1
  fi
done
[ "$rc" -eq 0 ] && echo "hooks installed into $dst"
exit $rc
