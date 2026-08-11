# Utterance segmentation over stt-stream hop events (design: utterance-end =
# non-empty text + one silence hop, ~1 s at HOP=1.0). Whisper re-transcribes
# a sliding 10 s window, so consecutive windows overlap; v0 dedup strips the
# common word-prefix against the previous utterance.
#
# The silence threshold is ADAPTIVE (operator's first real call, 2026-08-11:
# room floor sat above the fixed -45 dBFS, no boundary ever fired, the whole
# call became one flushed utterance with zero gates). A hop is silence when
# it is below noise_floor + MARGIN_DB, where noise_floor tracks the 10th
# percentile of recent hop levels; -45 remains the QUIET-room lower bound and
# CEIL_DB caps runaway floors in loud rooms.

SILENCE_DB = -45.0     # absolute floor for quiet rooms
MARGIN_DB = 6.0        # silence = below noise floor + margin
CEIL_DB = -33.0        # never call a hop this loud "silence" (speech ~ -30)
FLOOR_WINDOW = 120     # hops (~2 min) for the rolling noise-floor estimate


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
        self.recent_dbs = []

    def _threshold(self, db):
        self.recent_dbs.append(db)
        if len(self.recent_dbs) > FLOOR_WINDOW:
            self.recent_dbs.pop(0)
        floor = sorted(self.recent_dbs)[max(0, len(self.recent_dbs) // 10 - 1)]
        return min(max(self.silence_db, floor + MARGIN_DB), CEIL_DB)

    def feed(self, event):
        """One stt hop event {'t','rms_db','text'}. Returns an utterance dict
        {'start','end','text'} on utterance-end, else None."""
        t, db, text = event["t"], event["rms_db"], event["text"].strip()
        voiced = db >= self._threshold(db)
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
