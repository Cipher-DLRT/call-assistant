# Step-4 verify: one gate call + one hint call on canned input; prints the
# parsed JSON, latency, usage. Costs well under a cent. Needs the key:
#   set -a; . ~/.config/call-assistant/env; set +a; \
#   ./spike/stt_bench/venv/bin/python scripts/llm_oneshot.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.loop.llm import Llm  # noqa: E402

WINDOW = """ME: So the connector runs entirely inside your VPC.
THEM: Okay. And what's your escalation path if something breaks in production?
"""

FACTS = [
    {"id": 13, "shareability": "shareable", "verified_at": "2026-07-18",
     "fact_text": "UnifyApps escalation path for medium-priority issues (Sev 3): "
                  "3-hour response time, 4 business days resolution target."},
]

llm = Llm()
verdict, usage, ms = llm.gate(WINDOW)
print(f"gate: {verdict}  usage={usage}  latency={ms}ms")
hint, usage, ms = llm.hint(WINDOW, verdict["verdict"], FACTS)
print(f"hint: {hint}  usage={usage}  latency={ms}ms")
