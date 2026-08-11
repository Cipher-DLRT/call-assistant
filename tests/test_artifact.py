import json
import subprocess
from pathlib import Path

from app.loop.artifact import ArtifactWriter


REPO = Path(__file__).resolve().parent.parent
PYTHON = REPO / "spike/stt_bench/venv/bin/python"


def build_writer(tmp_path, mode="inperson"):
    config = {
        "call_id": "shadow-001",
        "mode": mode,
        "threshold": 0.55,
        "ceiling_usd": 0.25,
    }
    writer = ArtifactWriter(tmp_path, config)
    for i in range(80):
        writer.add_utterance({
            "i": i,
            "start": i * 3.0,
            "end": i * 3.0 + 2.0,
            "speaker": "ME" if i % 2 == 0 else "THEM",
            "sim": None if mode == "online" else 0.7,
            "db": -24.4,
            "text": f"utterance | {i}",
        })
    writer.add_gate({"i": 1, "decision": "hint"})
    writer.add_gate({"i": 2, "decision": "skip"})
    writer.add_hint({"shown_at": 12.5, "text": "First | hint", "fact_ids": ["a", "b"]})
    writer.add_hint({"shown_at": 75.0, "text": "Second hint", "fact_ids": ["c"]})
    return writer


def test_finalize_writes_artifact_and_compatible_sheets(tmp_path):
    writer = build_writer(tmp_path)
    cost = {
        "gate_calls": 2,
        "hint_calls": 2,
        "input_tokens": 100,
        "output_tokens": 50,
        "total_usd": 0.001,
        "ceiling_usd": 0.25,
        "ceiling_hit": False,
    }
    writer.finalize(cost)

    artifact = json.loads((tmp_path / "artifact.json").read_text())
    assert set(artifact) == {
        "call_id", "mode", "config", "utterances", "gate_decisions", "hints", "cost"
    }
    assert len(artifact["utterances"]) == 80
    assert len(artifact["gate_decisions"]) == 2
    assert len(artifact["hints"]) == 2

    sheet = tmp_path / "attribution-sheet.md"
    lines = sheet.read_text().splitlines()
    data_rows = [line for line in lines if line.startswith("| ") and line[2:3].isdigit()]
    assert len(data_rows) == 60
    first_index = lines.index(data_rows[0])
    lines[first_index] = data_rows[0].replace("[ ]", "[x]", 1)
    sheet.write_text("\n".join(lines) + "\n")
    result = subprocess.run(
        [str(PYTHON), "scripts/score_leg.py", str(sheet)],
        cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "attribution:" in result.stdout

    hint_sheet = (tmp_path / "hint-sheet.md").read_text()
    assert "<!-- hints call:shadow-001 ceiling:0.25 -->" in hint_sheet
    assert "First ¦ hint" in hint_sheet


def test_online_header_and_empty_lists_are_valid(tmp_path):
    writer = ArtifactWriter(tmp_path, {
        "call_id": "shadow-online",
        "mode": "online",
        "threshold": 0.55,
    })
    writer.finalize({"ceiling_usd": 0.1})

    assert (tmp_path / "attribution-sheet.md").read_text().startswith(
        "<!-- leg:1 bar:98 threshold:- -->"
    )
    artifact = json.loads((tmp_path / "artifact.json").read_text())
    assert artifact["utterances"] == []
    assert artifact["gate_decisions"] == []
    assert artifact["hints"] == []
