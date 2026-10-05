# close record for ca-menu-launch — CLOSED 2026-10-05 PASS fcaf4bd0dfa318331db9014a918b61a26d023c4d

LANDED-AS: 3ee8e42

USE: USE-ABSENT
TEST:
  COMMAND: spike/stt_bench/venv/bin/python -m pytest -q -p no:cacheprovider tests/ --ignore=tests/test_retrieval.py
  GREEN: exit 0
  ARTIFACT: .lane-evidence/01-spike-stt_bench-venv-bin-python--m-pytest.log md5=61828bb8437a8c8eaca7f81e5567444f bytes=343

