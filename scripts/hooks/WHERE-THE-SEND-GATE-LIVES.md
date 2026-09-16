# The SendMessage gate does not live in this repo

There is **one** enforcer, and it is not here:

```
/Users/rami/dev/work-automation/scripts/hooks/sendmessage-gate.sh
```

Every seat registers that absolute path. This repo used to carry a synced copy of the gate and
its selftest; both were deleted on 2026-09-10 because they were dormant, and a dormant copy of an
enforcer is worse than no copy — it looks authoritative, it drifts at every gate change, and a
selftest beside it certifies the file that nothing runs.

## Proof that the copies could not execute

- `scripts/hooks/install.sh:43` registers the command as wa's absolute path above, in the
  `PreToolUse` / `SendMessage` entry it merges into each seat's `.claude/settings.local.json`.
  Nothing ever registers a path inside this repo.
- `scripts/hooks/install.sh:85` explicitly **skips** `sendmessage-gate.sh` and
  `sendmessage-gate-selftest.sh` when populating `.git/hooks`, so they were never installed
  either.
- The deleted selftest read `GATE=$SCRIPT_DIR/sendmessage-gate.sh` — it tested the local dormant
  copy, so it would have reported green while the real enforcer changed underneath it.

Note that being named in the `:85` skip list is **not** by itself proof of dormancy:
`walk-brief-lint.py` is in that same list and is very much live — `pre-commit:235` and
`pre-push:28` invoke it from the worktree by path rather than from `.git/hooks`. That file stays.

## The invariant that is actually kept

Not "three copies agree by md5". It is:

1. does wa's file enforce, and
2. does every seat's `.claude/settings.local.json` register that path.

Check the second with:

```sh
python3 -c "import json;print(json.load(open('.claude/settings.local.json'))['hooks']['PreToolUse'])"
```

## Reading the gate's behaviour

Read the enforcer itself, never a summary of it. Its refusal modes, in order: `untagged`
(the tag must be the first token of line 1), `oversize` (a hard character cap that applies to
**every** message, exempt tags included), then `rate` (which runs only for non-exempt tags).
The log is `/Users/rami/orca/sendgate.log`, tab-separated:
stamp, repo, tag, chars, verdict, recipient.
