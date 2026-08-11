# A3 (operator ruling 2026-08-11): verify model IDs against the LIVE models
# list before trusting the wiring — check, don't assume. Run after the key
# file exists:  set -a; . ~/.config/call-assistant/env; set +a; \
#               ./spike/stt_bench/venv/bin/python scripts/verify_models.py
#
# Expected output:
#   gate model claude-haiku-4-5 ... OK (<full id>)
#   hint model claude-sonnet-5 ... OK (<full id>)
#   A3 verified: both model IDs resolve on the live models list

import os
import sys

import anthropic

# Law 4: Haiku = gate, Sonnet = hint. Opus and Fable never enter this loop.
GATE_MODEL = "claude-haiku-4-5"
HINT_MODEL = "claude-sonnet-5"

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("STOP: ANTHROPIC_API_KEY not set (source ~/.config/call-assistant/env)")

client = anthropic.Anthropic()
for role, wanted in (("gate", GATE_MODEL), ("hint", HINT_MODEL)):
    m = client.models.retrieve(wanted)  # 404s if the ID is wrong
    print(f"{role} model {wanted} ... OK ({m.id})")
print("A3 verified: both model IDs resolve on the live models list")
