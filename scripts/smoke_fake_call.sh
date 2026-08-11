#!/bin/bash
# P1 end-to-end smoke on FAKE audio (session end state: smoke, then STOP).
# Runs both modes against legs/smoke-p1/ (TTS far side + enrollment voice).
# Expects ~/.config/call-assistant/env (see run_call.sh). Total API spend
# is well under $0.25.
#
#   scripts/smoke_fake_call.sh            # both modes, normal ceiling
#   scripts/smoke_fake_call.sh ceiling    # in-person only, $0.02 ceiling
set -euo pipefail
cd "$(dirname "$0")/.."

if [ "${1:-}" = "ceiling" ]; then
  # low enough that the smoke's 2-3 LLM calls cross it mid-call
  export CA_COST_CEILING_USD=0.001
  scripts/run_call.sh replay-online legs/smoke-p1/me.wav legs/smoke-p1/them.wav
  exit 0
fi

echo "=== smoke 1/2: online replay (channel split; expect >=1 hint, one 🔒) ==="
scripts/run_call.sh replay-online legs/smoke-p1/me.wav legs/smoke-p1/them.wav
echo
echo "=== smoke 2/2: in-person replay (voiceprint; expect ME>=0.55, THEM low) ==="
scripts/run_call.sh replay-inperson legs/smoke-p1/mix.wav
echo
echo "newest artifacts:"
ls -dt calls/* | head -2
