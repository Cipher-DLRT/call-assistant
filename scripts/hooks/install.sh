#!/bin/sh
# Install this repo's git gates as SHIMS to the estate tooling checkout.
#
# Since 2026-09-16 (reset-8) the hooks live in ONE place, /Users/rami/dev/estate-tooling, and this
# repo's .git/hooks/<name> is a one-line `exec` of that copy: a hook fix lands once, when the
# operator fast-forwards that repo, and is live here at once. Run this once after cloning; worktrees
# share the main checkout's hooks directory, so one run covers every lane worktree. Prints the
# installed files' exec lines so the record shows what runs.
set -e
ESTATE=/Users/rami/dev/estate-tooling
[ -d "$ESTATE/scripts/hooks" ] || { echo "no estate tooling at $ESTATE/scripts/hooks -- nothing to install" >&2; exit 1; }
top=$(git rev-parse --show-toplevel) || exit 1
gitdir=$(git rev-parse --git-common-dir)
case "$gitdir" in /*) ;; *) gitdir="$top/$gitdir" ;; esac
dst="$gitdir/hooks"
mkdir -p "$dst"
for name in pre-commit pre-push commit-msg; do
  [ -f "$ESTATE/scripts/hooks/$name" ] || { echo "  MISSING    $ESTATE/scripts/hooks/$name" >&2; exit 1; }
  printf '#!/bin/sh\nexec %s/scripts/hooks/%s "$@"\n' "$ESTATE" "$name" > "$dst/$name"
  chmod +x "$dst/$name"
  printf '  installed  %s -> %s\n' "$dst/$name" "$(sed -n 2p "$dst/$name")"
done
echo "hooks installed into $dst as shims to $ESTATE/scripts/hooks"
