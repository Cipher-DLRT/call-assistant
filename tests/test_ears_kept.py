import ast
import importlib.util
from pathlib import Path
import subprocess

import pytest


REPO = Path(__file__).resolve().parents[1]
REMOVED = ("orchestrator", "llm", "retrieval", "cost", "artifact")
EXEMPT = {
    "tests/test_ears_kept.py",
    "scripts/run_call.sh",
    "app/menubar/menubar.py",
}


@pytest.mark.parametrize("name", ["audio", "segmenter"])
def test_ears_load_by_path(name):
    path = REPO / "app" / "loop" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"ca_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if name == "audio":
        ring = module.Ring()
        samples = module.np.zeros(module.RATE, dtype="float32")
        ring.append(samples)
        assert module.np.array_equal(ring.slice(0, 1), samples)
    else:
        segmenter = module.Segmenter()
        assert segmenter.feed({"t": 1, "rms_db": -20, "text": "test utterance"}) is None
        assert segmenter.feed({"t": 2, "rms_db": -60, "text": ""}) == {
            "start": 0.0, "end": 1, "text": "test utterance",
        }


def tracked_files(*paths):
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--", *paths], cwd=REPO,
    )
    return [path.decode() for path in output.split(b"\0") if path]


def test_no_retired_module_references():
    names = tuple(f"app.loop.{name}" for name in REMOVED) + ("app.overlay",)
    found = []
    for path in tracked_files("app", "scripts", "tests"):
        if path in EXEMPT:
            continue
        content = (REPO / path).read_text()
        for name in names:
            if name in content:
                found.append(f"{path}: {name}")
    assert not found, "Retired module references:\n" + "\n".join(found)


def test_no_relative_retired_imports():
    found = []
    for path in tracked_files("app/loop"):
        if not path.endswith(".py"):
            continue
        for node in ast.walk(ast.parse((REPO / path).read_text())):
            if isinstance(node, ast.ImportFrom) and node.level:
                names = [node.module.split(".")[0]] if node.module else [
                    alias.name for alias in node.names
                ]
                if any(name in REMOVED for name in names):
                    found.append(f"{path}:{node.lineno}")
    assert not found, "Relative retired imports:\n" + "\n".join(found)
