# Audio sources for the in-call loop. Live mode: spawn app/bin/capture
# (framed stdout: [u8 id][u32 LE n][s16le]), demux to per-stream stt-stream
# subprocesses and per-stream PCM ring buffers (~60 s, for voiceprint slices).
# Replay mode: stt-stream --replay handles pacing; the whole wav is loaded
# for slicing. Audio never leaves the Mac (law 1).

import json
import queue
import struct
import subprocess
import threading
import wave
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent.parent
CAPTURE_BIN = REPO / "app/bin/capture"
STT_BIN = REPO / "app/bin/stt-stream"
WHISPER_MODEL = REPO / "spike/stt_bench/models/ggml-small.bin"
RATE = 16000
RING_SECONDS = 60


def load_wav_f32(path):
    wf = wave.open(str(path))
    assert wf.getframerate() == RATE and wf.getnchannels() == 1 and \
        wf.getsampwidth() == 2, f"{path}: need 16k mono s16"
    return np.frombuffer(wf.readframes(wf.getnframes()),
                         dtype=np.int16).astype("float32") / 32768.0


class Ring:
    """Absolute-time PCM ring: slice(start_s, end_s) within the last ~60 s."""
    def __init__(self):
        self.buf = np.zeros(RING_SECONDS * RATE, dtype="float32")
        self.total = 0  # samples ever written
        self.lock = threading.Lock()

    def append(self, f32):
        with self.lock:
            n = len(f32)
            if n >= len(self.buf):
                self.buf[:] = f32[-len(self.buf):]
            else:
                self.buf = np.roll(self.buf, -n)
                self.buf[-n:] = f32
            self.total += n

    def slice(self, start_s, end_s):
        with self.lock:
            i1 = int(end_s * RATE)
            i0 = int(start_s * RATE)
            lo = self.total - len(self.buf)
            i0, i1 = max(i0, lo, 0), min(i1, self.total)
            if i1 <= i0:
                return np.zeros(0, dtype="float32")
            off = len(self.buf) - (self.total - i0)
            return self.buf[off:off + (i1 - i0)].copy()


class SttReader(threading.Thread):
    """Reads one stt-stream stdout, pushes (stream_id, event) to the queue."""
    def __init__(self, stream_id, proc, out_q):
        super().__init__(daemon=True)
        self.stream_id, self.proc, self.out_q = stream_id, proc, out_q

    def run(self):
        for line in self.proc.stdout:
            try:
                self.out_q.put((self.stream_id, json.loads(line)))
            except json.JSONDecodeError:
                continue
        self.out_q.put((self.stream_id, None))  # EOF


def _spawn_stt(extra):
    return subprocess.Popen(
        [str(STT_BIN), str(WHISPER_MODEL)] + extra,
        stdin=subprocess.PIPE if extra == ["--stdin"] else subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=extra != ["--stdin"],
    )


class ReplaySource:
    """streams: {stream_id: wav_path}. Pacing comes from stt --replay."""
    def __init__(self, streams):
        self.q = queue.Queue()
        self.pcm = {}       # full wavs for attribution slices
        self.procs = []
        self.open_streams = set(streams)
        for sid, path in streams.items():
            self.pcm[sid] = load_wav_f32(path)
            p = subprocess.Popen([str(STT_BIN), str(WHISPER_MODEL),
                                  "--replay", str(path)],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL, text=True)
            self.procs.append(p)
            SttReader(sid, p, self.q).start()

    def slice(self, sid, start_s, end_s):
        pcm = self.pcm[sid]
        return pcm[int(start_s * RATE):int(end_s * RATE)]

    def events(self):
        """Yields (stream_id, event) until every stream hits EOF."""
        while self.open_streams:
            sid, ev = self.q.get()
            if ev is None:
                self.open_streams.discard(sid)
                continue
            yield sid, ev

    def stop(self):
        for p in self.procs:
            p.terminate()


class LiveSource:
    """mode: 'stream-online' (0=mic/ME, 1=system/THEM) or 'stream-inperson'."""
    def __init__(self, mode):
        n_streams = 2 if mode == "stream-online" else 1
        self.q = queue.Queue()
        self.rings = {i: Ring() for i in range(n_streams)}
        self.open_streams = set(range(n_streams))
        self.capture = subprocess.Popen([str(CAPTURE_BIN), mode],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL)
        self.stt = {sid: _spawn_stt(["--stdin"]) for sid in range(n_streams)}
        self.readers = []
        for sid, p in self.stt.items():
            r = threading.Thread(target=self._read_stt, args=(sid, p), daemon=True)
            r.start()
            self.readers.append(r)
        self.demux = threading.Thread(target=self._demux, daemon=True)
        self.demux.start()

    def _read_stt(self, sid, proc):
        for raw in proc.stdout:
            try:
                self.q.put((sid, json.loads(raw)))
            except json.JSONDecodeError:
                continue
        self.q.put((sid, None))

    def _demux(self):
        out = self.capture.stdout
        try:
            while True:
                hdr = out.read(5)
                if len(hdr) < 5:
                    break
                sid = hdr[0]
                (n,) = struct.unpack("<I", hdr[1:5])
                payload = out.read(2 * n)
                if len(payload) < 2 * n or sid not in self.stt:
                    break
                self.rings[sid].append(
                    np.frombuffer(payload, dtype=np.int16).astype("float32") / 32768.0)
                self.stt[sid].stdin.write(payload)
                self.stt[sid].stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        for p in self.stt.values():
            try:
                p.stdin.close()
            except OSError:
                pass

    def slice(self, sid, start_s, end_s):
        return self.rings[sid].slice(start_s, end_s)

    def events(self):
        while self.open_streams:
            sid, ev = self.q.get()
            if ev is None:
                self.open_streams.discard(sid)
                continue
            yield sid, ev

    def stop(self):
        import signal
        self.capture.send_signal(signal.SIGINT)
        try:
            self.capture.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.capture.kill()
        for p in self.stt.values():
            p.terminate()
