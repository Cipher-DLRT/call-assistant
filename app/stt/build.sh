#!/bin/bash
# Build stt-stream against Homebrew whisper-cpp. The embedding process must
# call ggml_backend_load_all() (done in stt_stream.c) — Homebrew ships the
# ggml compute backends in /opt/homebrew/opt/ggml/libexec (p0c ledger).
set -euo pipefail
cd "$(dirname "$0")"
WHISPER=/opt/homebrew/opt/whisper-cpp
GGML=/opt/homebrew/opt/ggml
cc -O2 -o ../bin/stt-stream stt_stream.c \
   -I"$WHISPER/include" -I"$GGML/include" \
   -L"$WHISPER/lib" -L"$GGML/lib" -lwhisper -lggml -lggml-base -lm
echo "built: app/bin/stt-stream"
