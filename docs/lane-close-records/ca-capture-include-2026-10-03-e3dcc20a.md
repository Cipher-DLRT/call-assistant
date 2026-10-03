# close record for ca-capture-include — CLOSED 2026-10-03 PASS e3dcc20ac3e0b5ecc81278bf54d2fa3b57307986

USE: USE-NOT-REQUIRED
TEST:
    COMMAND: spike/stt_bench/venv/bin/python scripts/check_capture_include_selftest.py
    RED: exit 1
    ARTIFACT: .lane-evidence/01-spike-stt_bench-venv-bin-python-scripts-check_capture_includ.log md5=0f348f4d53fd07cebd31b254a33cef08 bytes=1880
    GREEN: exit 0
    ARTIFACT: .lane-evidence/02-spike-stt_bench-venv-bin-python-scripts-check_capture_includ.log md5=4d1766541fbb429a7ddd7bc44935a15c bytes=3200

