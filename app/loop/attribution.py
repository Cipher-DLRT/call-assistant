# me/them attribution (law 8). Voiceprint kernel ported verbatim from
# scripts/grade_leg.py::voiceprint_label — ECAPA cosine vs the enrolled
# embedding, threshold 0.55, slices under 0.5 s padded forward. Local only;
# the embedding and model cache never leave the Mac.

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
VOICEPRINT = REPO / "spike/voiceprint/operator_ecapa.pt"
MODEL_CACHE = REPO / "spike/voiceprint/model_cache"
RATE = 16000
THRESHOLD = 0.55


class Attributor:
    def __init__(self, threshold=THRESHOLD):
        import torch
        from speechbrain.inference import EncoderClassifier
        self.torch = torch
        self.threshold = threshold
        self.enrolled = torch.load(VOICEPRINT, weights_only=True)
        self.model = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb", savedir=str(MODEL_CACHE))

    def sim(self, pcm_f32):
        """Cosine similarity of a float32 mono-16k slice vs the enrolled print."""
        n = len(pcm_f32)
        if n == 0:
            return 0.0
        if n < int(0.5 * RATE):  # pad very short slices for a stable embedding
            import numpy as np
            pcm_f32 = np.pad(pcm_f32, (0, int(0.5 * RATE) - n))
        sig = self.torch.from_numpy(pcm_f32).unsqueeze(0)
        with self.torch.no_grad():
            e = self.model.encode_batch(sig).squeeze()
        e = e / e.norm()
        return float(self.enrolled @ e)

    def label(self, sim):
        return "ME" if sim >= self.threshold else "THEM"
