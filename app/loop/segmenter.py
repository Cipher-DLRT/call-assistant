# Utterance segmentation over stt-stream hop events (design: utterance-end =
# non-empty text + one hop below SILENCE_DB, ~1 s of silence at HOP=1.0).
# Whisper re-transcribes a sliding 10 s window, so consecutive windows overlap;
# v0 dedup strips the common word-prefix against the previous utterance.

SILENCE_DB = -45.0


def _strip_common_prefix(prev_words, words):
    i = 0
    while i < len(prev_words) and i < len(words) and prev_words[i] == words[i]:
        i += 1
    return words[i:]


class Segmenter:
    def __init__(self, silence_db=SILENCE_DB):
        self.silence_db = silence_db
        self.window_text = ""
        self.voiced_start = None
        self.last_voiced_t = None
        self.last_emitted_words = []

    def feed(self, event):
        """One stt hop event {'t','rms_db','text'}. Returns an utterance dict
        {'start','end','text'} on utterance-end, else None."""
        t, db, text = event["t"], event["rms_db"], event["text"].strip()
        voiced = db >= self.silence_db
        if voiced:
            if self.voiced_start is None:
                self.voiced_start = t - 1.0
            self.last_voiced_t = t
            if text:
                self.window_text = text
            return None
        # silence hop: emit if we were mid-utterance with text
        if self.voiced_start is None or not self.window_text:
            self.voiced_start = None
            return None
        words = _strip_common_prefix(self.last_emitted_words,
                                     self.window_text.split())
        utt = {"start": self.voiced_start,
               "end": self.last_voiced_t if self.last_voiced_t is not None else t,
               "text": " ".join(words)}
        self.last_emitted_words = self.window_text.split()
        self.voiced_start = None
        self.window_text = ""
        if not utt["text"]:
            return None
        return utt

    def flush(self):
        """Emit the open utterance at EOF/stop, if any."""
        if self.voiced_start is None or not self.window_text:
            return None
        words = _strip_common_prefix(self.last_emitted_words,
                                     self.window_text.split())
        utt = {"start": self.voiced_start,
               "end": self.last_voiced_t or self.voiced_start,
               "text": " ".join(words)}
        self.last_emitted_words = self.window_text.split()
        self.voiced_start = None
        self.window_text = ""
        return utt if utt["text"] else None
