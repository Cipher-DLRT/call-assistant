# Gate + hint API calls (laws 1, 4). Only short text excerpts leave the Mac:
# rolling transcript windows and retrieval snippets. Never audio, never the
# whole pack. Haiku = gate (machine-read), Sonnet = hint (operator-read);
# Opus and Fable never enter this loop.

import hashlib
import json
import time
from pathlib import Path

import anthropic

REPO = Path(__file__).resolve().parent.parent.parent
GATE_MODEL = "claude-haiku-4-5"   # resolved per A3 (scripts/verify_models.py)
HINT_MODEL = "claude-sonnet-5"    # resolved per A3
GATE_PROMPT_FILE = REPO / "prompts/gate-v1.md"
HINT_PROMPT_FILE = REPO / "prompts/hint-v1.md"

GATE_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["askable", "cue", "neither"]},
        "topic_terms": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["verdict", "topic_terms"],
    "additionalProperties": False,
}

HINT_SCHEMA = {
    "type": "object",
    "properties": {
        "hint": {"type": "string"},
        "fact_ids": {"type": "array", "items": {"type": "integer"}},
    },
    "required": ["hint", "fact_ids"],
    "additionalProperties": False,
}


def prompt_version(path: Path) -> str:
    return f"{path.name}#{hashlib.sha256(path.read_bytes()).hexdigest()[:8]}"


class Llm:
    def __init__(self):
        self.client = anthropic.Anthropic()  # key from env (law 9)
        self.gate_system = GATE_PROMPT_FILE.read_text()
        self.hint_system = HINT_PROMPT_FILE.read_text()

    def _call(self, model, system, user_text, schema, max_tokens, thinking=None):
        t0 = time.monotonic()
        kwargs = dict(
            model=model,
            max_tokens=max_tokens,
            system=[{"type": "text", "text": system,
                     "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user_text}],
            output_config={"format": {"type": "json_schema", "schema": schema}},
        )
        if thinking is not None:
            kwargs["thinking"] = thinking
        resp = self.client.messages.create(**kwargs)
        latency_ms = int((time.monotonic() - t0) * 1000)
        usage = {"in": resp.usage.input_tokens, "out": resp.usage.output_tokens,
                 "cache_w": resp.usage.cache_creation_input_tokens or 0,
                 "cache_r": resp.usage.cache_read_input_tokens or 0}
        text = next(b.text for b in resp.content if b.type == "text")
        return json.loads(text), usage, latency_ms

    def gate(self, transcript_window: str):
        """transcript_window: last ~6 lines, 'ME: ...' / 'THEM: ...', newest last."""
        return self._call(GATE_MODEL, self.gate_system, transcript_window,
                          GATE_SCHEMA, max_tokens=200)

    def hint(self, transcript_window: str, verdict: str, facts: list):
        lines = [f"Gate verdict: {verdict}", "", "Transcript:", transcript_window,
                 "", "Candidate facts:"]
        for f in facts:
            lines.append(f"- id={f['id']} shareability={f['shareability']} "
                         f"verified_at={f['verified_at']}: {f['fact_text']}")
        # Sonnet 5: thinking off for latency (accepted on this model).
        return self._call(HINT_MODEL, self.hint_system, "\n".join(lines),
                          HINT_SCHEMA, max_tokens=300,
                          thinking={"type": "disabled"})
