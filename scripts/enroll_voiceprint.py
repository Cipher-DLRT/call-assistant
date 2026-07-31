# P0 voiceprint enrollment (law 8: local, one-time, ~60 s, stored on the Mac
# only). Computes an ECAPA-TDNN speaker embedding from an enrollment wav and
# verifies it against a held-out slice of the same recording (positive probe)
# and a different speaker (negative probe).
#
# Usage:
#   venv/bin/python scripts/enroll_voiceprint.py <enroll.wav> <negative.wav> <out_dir>
#
# enroll.wav: >= 60 s of the operator speaking, 16 kHz mono s16.
# negative.wav: different speaker, same format (e.g. spike/stt_bench/bench.wav).
# out_dir: gitignored directory for the embedding + model cache.

import json
import sys
import time
import wave
from pathlib import Path

import numpy as np
import torch
from speechbrain.inference import EncoderClassifier

ENROLL_SPLIT = 2 / 3  # first 2/3 -> stored embedding, last 1/3 -> positive probe


def load_wav(path):
    wf = wave.open(str(path))
    assert wf.getframerate() == 16000 and wf.getnchannels() == 1 and wf.getsampwidth() == 2, \
        f"{path}: expected 16 kHz mono s16"
    pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    return torch.from_numpy(pcm.astype(np.float32) / 32768.0).unsqueeze(0)


def embed(model, sig):
    with torch.no_grad():
        e = model.encode_batch(sig).squeeze()
    return e / e.norm()


enroll_path, negative_path, out_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
out_dir.mkdir(parents=True, exist_ok=True)

model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=str(out_dir / "model_cache"))

sig = load_wav(enroll_path)
n = sig.shape[1]
assert n >= 50 * 16000, f"enrollment audio too short: {n / 16000:.1f}s (need >= 50 s)"
split = int(n * ENROLL_SPLIT)

emb_enroll = embed(model, sig[:, :split])
emb_probe = embed(model, sig[:, split:])
emb_neg = embed(model, load_wav(negative_path))

pos = float(emb_enroll @ emb_probe)
neg = float(emb_enroll @ emb_neg)

torch.save(emb_enroll, out_dir / "operator_ecapa.pt")
(out_dir / "operator_ecapa.json").write_text(json.dumps({
    "model": "speechbrain/spkrec-ecapa-voxceleb",
    "license": "apache-2.0",
    "dim": int(emb_enroll.shape[0]),
    "created": time.strftime("%Y-%m-%d %H:%M:%S"),
    "enroll_seconds": round(split / 16000, 1),
    "probe_cosine_same": round(pos, 4),
    "probe_cosine_other": round(neg, 4),
}, indent=2))

print(f"embedding: {out_dir}/operator_ecapa.pt (dim {int(emb_enroll.shape[0])})")
print(f"cosine same-speaker probe:  {pos:.4f}   (expect high, > 0.5)")
print(f"cosine other-speaker probe: {neg:.4f}   (expect low)")
print(f"margin: {pos - neg:.4f}   (proposed usable bar: > 0.3)")
print("ENROLLMENT USABLE" if pos > 0.5 and (pos - neg) > 0.3 else "ENROLLMENT WEAK — re-record")
