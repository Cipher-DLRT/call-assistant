# P0 live-leg grading sheet generator (phase0-grading pattern).
#
#   grade_leg.py leg1 <legdir>   # expects me.wav + them.wav (channel-split labels)
#   grade_leg.py leg2 <legdir>   # expects mix.wav (voiceprint labels, bar 90%)
#   grade_leg.py leg3 <legdir>   # expects mix.wav, ground truth = operator only
#   options: --samples N (default 60) --threshold T (default 0.55)
#
# Transcription: whisper.cpp small (check (c) winner), local. Voiceprint:
# enrolled ECAPA embedding (spike/voiceprint). Writes <legdir>/sheet.md.
# Raw audio and whisper JSON stay gitignored; the sheet is what commits.

import argparse
import json
import math
import re
import subprocess
import sys
import wave
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WHISPER_CLI = "/opt/homebrew/opt/whisper-cpp/bin/whisper-cli"
WHISPER_MODEL = REPO / "spike/stt_bench/models/ggml-small.bin"
VOICEPRINT = REPO / "spike/voiceprint/operator_ecapa.pt"
MODEL_CACHE = REPO / "spike/voiceprint/model_cache"
RATE = 16000
MIN_UTT_S = 0.4

BARS = {"leg1": "98", "leg2": "90", "leg3": "none"}


def to16k(src: Path) -> Path:
    dst = src.with_name(src.stem + "-16k.wav")
    subprocess.run(["afconvert", "-f", "WAVE", "-d", f"LEI16@{RATE}", "-c", "1",
                    str(src), str(dst)], check=True, capture_output=True)
    return dst


def transcribe(wav16k: Path) -> list:
    base = wav16k.with_suffix("")
    subprocess.run([WHISPER_CLI, "-m", str(WHISPER_MODEL), "-f", str(wav16k),
                    "-oj", "-of", str(base), "-np", "-l", "en"],
                   check=True, capture_output=True)
    data = json.loads(base.with_suffix(".json").read_text())
    utts = []
    for seg in data.get("transcription", []):
        text = seg.get("text", "").strip()
        start = seg["offsets"]["from"] / 1000.0
        end = seg["offsets"]["to"] / 1000.0
        if not text or re.fullmatch(r"[\[\(].*[\]\)]", text):  # [BLANK_AUDIO] etc.
            continue
        if end - start < MIN_UTT_S:
            continue
        utts.append({"start": start, "end": end, "text": text})
    return utts


def load_pcm(wav16k: Path):
    import numpy as np
    wf = wave.open(str(wav16k))
    return np.frombuffer(wf.readframes(wf.getnframes()),
                         dtype=np.int16).astype("float32") / 32768.0


def attach_levels(utts, pcm):
    for u in utts:
        s = pcm[int(u["start"] * RATE):int(u["end"] * RATE)]
        rms = math.sqrt(float((s.astype("float64") ** 2).mean())) if len(s) else 0.0
        u["db"] = 20 * math.log10(max(rms, 1e-9))


def voiceprint_label(utts, wav16k, threshold):
    import torch
    from speechbrain.inference import EncoderClassifier
    pcm = load_pcm(wav16k)
    enrolled = torch.load(VOICEPRINT, weights_only=True)
    model = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", savedir=str(MODEL_CACHE))
    for u in utts:
        i0, i1 = int(u["start"] * RATE), int(u["end"] * RATE)
        if i1 - i0 < int(0.5 * RATE):  # pad very short slices for a stable embedding
            i1 = min(len(pcm), i0 + int(0.5 * RATE))
        sig = torch.from_numpy(pcm[i0:i1]).unsqueeze(0)
        with torch.no_grad():
            e = model.encode_batch(sig).squeeze()
        e = e / e.norm()
        u["sim"] = float(enrolled @ e)
        u["label"] = "ME" if u["sim"] >= threshold else "THEM"
    return utts


def sample_even(items, n):
    if len(items) <= n:
        return items
    return [items[round(i * (len(items) - 1) / (n - 1))] for i in range(n)]


def mmss(t):
    return f"{int(t) // 60:02d}:{int(t) % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("leg", choices=["leg1", "leg2", "leg3"])
    ap.add_argument("legdir", type=Path)
    ap.add_argument("--samples", type=int, default=60)
    ap.add_argument("--threshold", type=float, default=0.55)
    args = ap.parse_args()
    d = args.legdir

    if args.leg == "leg1":
        me, them = d / "me.wav", d / "them.wav"
        for f in (me, them):
            if not f.exists():
                sys.exit(f"missing {f}")
        utts = []
        for f, label in ((me, "ME"), (them, "THEM")):
            wav16k = to16k(f)
            chan = transcribe(wav16k)
            attach_levels(chan, load_pcm(wav16k))
            for u in chan:
                u["label"] = label
                u["sim"] = None
                utts.append(u)
        utts.sort(key=lambda u: u["start"])
    else:
        mix = d / "mix.wav"
        if not mix.exists():
            sys.exit(f"missing {mix}")
        wav16k = to16k(mix)
        utts = transcribe(wav16k)
        attach_levels(utts, load_pcm(wav16k))
        utts = voiceprint_label(utts, wav16k, args.threshold)

    if not utts:
        sys.exit("no utterances found — was there speech in the capture?")
    n_me = sum(1 for u in utts if u["label"] == "ME")
    picked = sample_even(utts, args.samples)

    sheet = d / "sheet.md"
    lines = [
        f"<!-- leg:{args.leg[-1]} bar:{BARS[args.leg]} threshold:"
        f"{args.threshold if args.leg != 'leg1' else '-'} -->",
        f"# {args.leg} grading sheet — {d.name}",
        "",
        "Mark EXACTLY ONE box per row with an x: **correct** if the label matches",
        "who actually spoke that line, **wrong** if it does not. Leave a row blank",
        "only if you truly cannot tell (blank rows are excluded and reported).",
        "",
        "| # | start | label | sim | dB | utterance | correct | wrong |",
        "|---|-------|-------|-----|----|-----------|---------|-------|",
    ]
    for i, u in enumerate(picked, 1):
        sim = f"{u['sim']:.2f}" if u["sim"] is not None else "-"
        text = u["text"].replace("|", "¦")
        lines.append(f"| {i} | {mmss(u['start'])} | {u['label']} | {sim} "
                     f"| {u['db']:.0f} | {text} | [ ] | [ ]  |")
    sheet.write_text("\n".join(lines) + "\n")

    print(f"utterances: {len(utts)} (ME {n_me}, THEM {len(utts) - n_me})")
    print(f"sheet: {sheet}  ({len(picked)} rows)")
    if args.leg == "leg3":
        pct = 100.0 * n_me / len(utts)
        print(f"leg3 auto-score (ground truth = all ME): {n_me}/{len(utts)}"
              f" = {pct:.1f}% cross-mic transfer")
    print(f"next: mark the sheet, then run scripts/score_leg.py {sheet}")


if __name__ == "__main__":
    main()
