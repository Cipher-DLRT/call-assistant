import json
from pathlib import Path


def sample_even(items, n):
    if len(items) <= n:
        return items
    return [items[round(i * (len(items) - 1) / (n - 1))] for i in range(n)]


def mmss(t):
    return f"{int(t) // 60:02d}:{int(t) % 60:02d}"


def _cell(text):
    # markdown table cell: no pipes, no newlines (2-line hints are legal)
    return text.replace("|", "¦").replace("\n", " / ")


class ArtifactWriter:
    def __init__(self, call_dir: Path, config: dict):
        self.call_dir = Path(call_dir)
        self.config = dict(config)
        self.utterances = []
        self.gate_decisions = []
        self.hints = []

    def add_utterance(self, utterance):
        self.utterances.append(dict(utterance))

    def add_gate(self, gate):
        self.gate_decisions.append(dict(gate))

    def add_hint(self, hint):
        self.hints.append(dict(hint))

    def finalize(self, cost_summary):
        self.call_dir.mkdir(parents=True, exist_ok=True)
        artifact = {
            "call_id": self.config["call_id"],
            "mode": self.config["mode"],
            "config": self.config,
            "utterances": self.utterances,
            "gate_decisions": self.gate_decisions,
            "hints": self.hints,
            "cost": cost_summary,
        }
        destination = self.call_dir / "artifact.json"
        temporary = self.call_dir / "artifact.json.tmp"
        temporary.write_text(json.dumps(artifact, indent=2) + "\n")
        temporary.replace(destination)
        self._write_attribution_sheet()
        self._write_hint_sheet(cost_summary)

    def _write_attribution_sheet(self):
        call_id = self.config["call_id"]
        if self.config["mode"] == "online":
            leg, bar, threshold = 1, 98, "-"
        else:
            leg, bar, threshold = 2, 90, self.config["threshold"]
        lines = [
            f"<!-- leg:{leg} bar:{bar} threshold:{threshold} -->",
            f"# leg{leg} grading sheet — {call_id}",
            "",
            "Mark EXACTLY ONE box per row with an x: **correct** if the label matches",
            "who actually spoke that line, **wrong** if it does not. Leave a row blank",
            "only if you truly cannot tell (blank rows are excluded and reported).",
            "",
            "| # | start | label | sim | dB | utterance | correct | wrong |",
            "|---|-------|-------|-----|----|-----------|---------|-------|",
        ]
        for i, utterance in enumerate(sample_even(self.utterances, 60), 1):
            sim = f"{utterance['sim']:.2f}" if utterance["sim"] is not None else "-"
            text = _cell(utterance["text"])
            lines.append(
                f"| {i} | {mmss(utterance['start'])} | {utterance['speaker']} | {sim} "
                f"| {utterance['db']:.0f} | {text} | [ ] | [ ]  |"
            )
        (self.call_dir / "attribution-sheet.md").write_text("\n".join(lines) + "\n")

    def _write_hint_sheet(self, cost_summary):
        call_id = self.config["call_id"]
        lines = [
            f"<!-- hints call:{call_id} ceiling:{cost_summary['ceiling_usd']} -->",
            f"# hint grading sheet — {call_id}",
            "",
            "Mark each hint: useful / on-time / wrong — any combination",
            "",
            "| # | shown | hint | facts | useful | on-time | wrong |",
            "|---|-------|------|-------|--------|---------|-------|",
        ]
        for i, hint in enumerate(self.hints, 1):
            text = _cell(hint["text"])
            facts = ",".join(str(fact_id) for fact_id in hint["fact_ids"])
            lines.append(
                f"| {i} | {mmss(hint['shown_at'])} | {text} | {facts} "
                "| [ ] | [ ] | [ ] |"
            )
        (self.call_dir / "hint-sheet.md").write_text("\n".join(lines) + "\n")
