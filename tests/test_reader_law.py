import subprocess
from pathlib import Path


# This suite pin is itself compliant: pkms_canon status='active'
def test_every_tracked_canon_read_filters_active():
    repo = Path(__file__).resolve().parent.parent
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=repo, check=True, capture_output=True,
    ).stdout.split(b"\0")
    violations = []
    for raw_path in tracked:
        if not raw_path:
            continue
        path = repo / raw_path.decode()
        try:
            contents = path.read_bytes()
            if b"\0" in contents:
                continue
            text = contents.decode()
        except (OSError, UnicodeDecodeError):
            continue
        if "pkms_canon" in text and "status='active'" not in text:
            violations.append(str(path.relative_to(repo)))
    assert violations == []
