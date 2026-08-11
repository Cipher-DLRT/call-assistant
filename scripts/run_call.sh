#!/bin/bash
# Operator entry point: load env (law 9), start overlay + orchestrator.
#
#   scripts/run_call.sh online            # headset REQUIRED (A4)
#   scripts/run_call.sh inperson
#   scripts/run_call.sh replay-online <me.wav> <them.wav>
#   scripts/run_call.sh replay-inperson <mix.wav>
#
# Ctrl-C stops the call cleanly: artifact + grading sheets are finalized.
# The overlay is a separate process (silent-failure law) and is stopped last.
set -euo pipefail
cd "$(dirname "$0")/.."

ENV_FILE="$HOME/.config/call-assistant/env"
if [ ! -f "$ENV_FILE" ]; then
  echo "STOP: $ENV_FILE not found (ANTHROPIC_API_KEY + CA_COST_CEILING_USD, chmod 600)" >&2
  exit 1
fi
PERMS=$(stat -f "%Lp" "$ENV_FILE")
if [ "$PERMS" != "600" ]; then
  echo "STOP: $ENV_FILE must be chmod 600 (is $PERMS) — law 9" >&2
  exit 1
fi
# A pre-set ceiling may only LOWER the file's value (smoke's ceiling-stop
# check). An inherited env var must never silently RAISE the cap (law 5,
# review finding 5).
PRE_CEILING="${CA_COST_CEILING_USD:-}"
set -a; . "$ENV_FILE"; set +a
if [ -n "$PRE_CEILING" ]; then
  if awk -v a="$PRE_CEILING" -v b="$CA_COST_CEILING_USD" 'BEGIN{exit !(a<b)}'; then
    export CA_COST_CEILING_USD="$PRE_CEILING"
  else
    echo "note: ignoring env ceiling $PRE_CEILING (not below file ceiling $CA_COST_CEILING_USD)" >&2
  fi
fi

PY=./spike/stt_bench/venv/bin/python
BEFORE=$(ls -dt calls/* 2>/dev/null | head -1 || true)

# Start orchestrator first; wait for ITS call dir (not just the newest — the
# newest could be a previous call; review finding 20).
$PY -m app.loop.orchestrator "$@" &
ORCH=$!
FEED=""
for _ in $(seq 1 20); do
  NEWEST=$(ls -dt calls/* 2>/dev/null | head -1 || true)
  if [ -n "$NEWEST" ] && [ "$NEWEST" != "$BEFORE" ]; then FEED="$NEWEST/feed.jsonl"; break; fi
  if ! kill -0 $ORCH 2>/dev/null; then break; fi
  sleep 0.5
done
if [ -z "$FEED" ]; then
  wait $ORCH; RC=$?
  echo "STOP: orchestrator did not start a call (exit $RC)" >&2
  exit $RC
fi
$PY -m app.overlay.overlay "$FEED" &
OVERLAY=$!

trap 'kill -INT $ORCH 2>/dev/null; wait $ORCH 2>/dev/null; kill $OVERLAY 2>/dev/null' INT TERM
RC=0
wait $ORCH || RC=$?
kill $OVERLAY 2>/dev/null || true
if [ $RC -ne 0 ] && [ $RC -ne 130 ]; then
  echo "call FAILED (orchestrator exit $RC) — check $(dirname "$FEED")" >&2
  exit $RC
fi
echo "call ended — grading sheets in $(dirname "$FEED")"
