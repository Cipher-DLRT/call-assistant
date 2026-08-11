# In-call loop orchestrator (CLAUDE.md Architecture, P1).
#
#   python -m app.loop.orchestrator online|inperson
#   python -m app.loop.orchestrator replay-online <me.wav> <them.wav>
#   python -m app.loop.orchestrator replay-inperson <mix.wav>
#
# capture -> rolling transcript with me/them -> Haiku gate on utterance-end ->
# local retrieval over the pack -> Sonnet hint -> feed.jsonl (overlay tails it)
# -> per-call artifact + grading sheets on stop (SIGINT or replay EOF).
#
# Laws wired here: 1 (text excerpts only), 3 (pack read-only), 4 (routing),
# 5 (env ceiling, loop stops at ceiling, telemetry in artifact), 6 (lock from
# fact metadata), 7 (staleness from verified_at ONLY), 8 (channel split
# online / voiceprint in-person, sims logged always).

import datetime
import json
import os
import signal
import sys
from pathlib import Path

from . import audio
from .artifact import ArtifactWriter
from .attribution import Attributor, THRESHOLD
from .cost import CostMeter
from .llm import Llm, GATE_MODEL, HINT_MODEL, GATE_PROMPT_FILE, HINT_PROMPT_FILE, prompt_version
from .retrieval import load_pack, PackError
from .segmenter import Segmenter, SILENCE_DB

REPO = Path(__file__).resolve().parent.parent.parent
PACK = REPO / "pack/canon.json"
MANIFEST = REPO / "pack/manifest.json"
CALLS = REPO / "calls"
STALE_DAYS = 90
TOP_K = 6
WINDOW_UTTS = 6
DUP_WINDOW_S = 90   # suppress a hint whose facts were all shown this recently


def should_suppress(recent_hints, fact_ids, text, now, window=DUP_WINDOW_S):
    """recent_hints: list of (shown_at, fact_id_set, word_set). Suppress when
    every cited fact already appeared on a card within the window, OR the text
    is a near-rephrasing of a shown card (operator ruling 2026-08-11: the same
    answer must not stack twice — varying citations don't make it new)."""
    words = set(text.lower().split())
    live = [(s, w) for t, s, w in recent_hints if now - t < window]
    if not live:
        return False
    shown = set().union(*[s for s, _ in live])
    if fact_ids and fact_ids <= shown:
        return True
    for _, w in live:
        union = words | w
        if union and len(words & w) / len(union) >= 0.6:
            return True
    return False


def log(msg):
    print(msg, file=sys.stderr, flush=True)


class Call:
    def __init__(self, mode, source, replay):
        self.mode = mode          # "online" | "inperson"
        self.source = source
        self.replay = replay
        self.pack = load_pack(PACK, MANIFEST)  # refuses on manifest mismatch (A1)

        # call dir + feed FIRST — the overlay launcher finds the newest call
        # dir, and the ECAPA load below takes seconds (bug found in smoke).
        call_id = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        self.call_dir = CALLS / call_id
        self.call_dir.mkdir(parents=True, exist_ok=True)
        self.feed_path = self.call_dir / "feed.jsonl"
        self.feed_path.touch()

        ceiling = os.environ.get("CA_COST_CEILING_USD")
        if not ceiling:
            sys.exit("STOP: CA_COST_CEILING_USD not set (law 5 — no default ceiling)")
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("STOP: ANTHROPIC_API_KEY not set (law 9)")
        try:
            self.cost = CostMeter(float(ceiling))  # rejects inf/nan/<=0 (law 5)
        except ValueError as e:
            sys.exit(f"STOP: bad CA_COST_CEILING_USD: {e}")
        self.llm = Llm()
        self.attributor = Attributor()
        self.segmenters = {}
        self.utterances = []      # rolling transcript (all streams, by end time)
        self.recent_hints = []    # (shown_at, fact_id_set) for dup suppression
        self.utt_i = 0
        self.ceiling_notified = False
        self.stopping = False     # set on SIGINT: flush transcript, skip hints
        self.finalized = False

        manifest = json.loads(MANIFEST.read_text())
        self.artifact = ArtifactWriter(self.call_dir, {
            "call_id": call_id,
            "mode": mode,
            "threshold": THRESHOLD,
            "silence_db": SILENCE_DB,
            "prompts": {"gate": prompt_version(GATE_PROMPT_FILE),
                        "hint": prompt_version(HINT_PROMPT_FILE)},
            "models": {"gate": GATE_MODEL, "hint": HINT_MODEL},
            "ceiling_usd": float(ceiling),
            "pack": {"path": str(PACK.relative_to(REPO)),
                     "rows": manifest["active_count"],
                     "sha256_8": manifest["sha256"][:8]},
        })

    def feed(self, item):
        with self.feed_path.open("a") as f:
            f.write(json.dumps(item) + "\n")

    # -- per-utterance pipeline ---------------------------------------------
    def on_utterance(self, sid, utt):
        pcm = self.source.slice(sid, utt["start"], utt["end"])
        sim = None
        if self.mode == "inperson":
            sim = self.attributor.sim(pcm)          # primary (law 8)
            speaker = self.attributor.label(sim)
        else:
            speaker = "ME" if sid == 0 else "THEM"  # channel split (law 8)
            if sid == 0:
                try:
                    sim = self.attributor.sim(pcm)  # backup print, always logged
                except Exception:
                    sim = None  # backup must never break deterministic labels
        import math
        n = len(pcm)
        rms = math.sqrt(float((pcm.astype("float64") ** 2).mean())) if n else 0.0
        db = 20 * math.log10(max(rms, 1e-9))
        self.utt_i += 1
        record = {"i": self.utt_i, "start": round(utt["start"], 2),
                  "end": round(utt["end"], 2), "speaker": speaker,
                  "sim": round(sim, 4) if sim is not None else None,
                  "db": db, "text": utt["text"]}
        self.utterances.append(record)
        self.artifact.add_utterance(record)
        log(f"[{record['start']:7.1f}] {speaker} "
            f"(sim {record['sim']}) {utt['text']}")
        if speaker == "THEM":
            self.maybe_hint(record)

    def transcript_window(self):
        lines = [f"{u['speaker']}: {u['text']}"
                 for u in self.utterances[-WINDOW_UTTS:]]
        return "\n".join(lines)

    def check_ceiling(self):
        if self.cost.allow():
            return True
        if not self.ceiling_notified:
            self.ceiling_notified = True
            self.feed({"type": "notice",
                       "text": "cost ceiling reached — hints stopped"})
            log("cost ceiling reached — LLM calls stopped, transcription continues")
        return False

    def maybe_hint(self, record):
        try:
            if self.stopping or not self.check_ceiling():
                return
            window = self.transcript_window()
            gate, usage, ms = self.llm.gate(window)
            cost = self.cost.add("gate", GATE_MODEL, usage["in"], usage["out"],
                                 usage["cache_w"], usage["cache_r"])
            self.artifact.add_gate({"utterance_i": record["i"],
                                    "verdict": gate["verdict"],
                                    "topic_terms": gate["topic_terms"],
                                    "latency_ms": ms, "usage": usage,
                                    "cost_usd": round(cost, 6)})
            if gate["verdict"] == "neither":
                return
            query = " ".join(gate["topic_terms"]) + " " + record["text"]
            facts = self.pack.search(query, top_k=TOP_K)
            if not facts:
                return
            if not self.check_ceiling():
                return
            hint, usage, ms = self.llm.hint(window, gate["verdict"], facts)
            cost = self.cost.add("hint", HINT_MODEL, usage["in"], usage["out"],
                                 usage["cache_w"], usage["cache_r"])
            used = [f for f in facts if f["id"] in set(hint["fact_ids"])]
            if not hint["hint"] or not used:
                return
            ids = set(hint["fact_ids"])
            if should_suppress(self.recent_hints, ids, hint["hint"], record["end"]):
                self.artifact.add_hint({"utterance_i": record["i"],
                                        "text": hint["hint"],
                                        "fact_ids": hint["fact_ids"],
                                        "suppressed": True,
                                        "shown_at": record["end"],
                                        "latency_ms": ms, "usage": usage,
                                        "cost_usd": round(cost, 6)})
                log(f"hint suppressed (duplicate facts {sorted(ids)})")
                return
            self.recent_hints.append(
                (record["end"], ids, set(hint["hint"].lower().split())))
            locked = any(f["shareability"] != "shareable" for f in used)
            stale = any(self._age_days(f["verified_at"]) > STALE_DAYS for f in used)
            # when stale, show the OLDEST cited date (the fact causing the ⏳)
            shown_date = (min if stale else max)(
                (f["verified_at"] for f in used), default=None)
            self.feed({"type": "hint", "text": hint["hint"], "locked": locked,
                       "stale": stale, "verified_at": shown_date,
                       "ts": record["end"]})
            self.artifact.add_hint({"utterance_i": record["i"],
                                    "text": hint["hint"],
                                    "fact_ids": hint["fact_ids"],
                                    "locked": locked, "stale": stale,
                                    "shown_at": record["end"],
                                    "latency_ms": ms, "usage": usage,
                                    "cost_usd": round(cost, 6),
                                    "grade": {"useful": None, "on_time": None,
                                              "wrong": None}})
        except Exception as e:
            # silent failure mode: a broken hint path must never stop the call
            log(f"hint path error (loop continues): {e}")

    @staticmethod
    def _age_days(verified_at):
        try:
            d = datetime.datetime.fromisoformat(str(verified_at)).date()
            return (datetime.date.today() - d).days
        except ValueError:
            return 0

    # -- main loop -----------------------------------------------------------
    def run(self):
        for sid, ev in self.source.events():
            seg = self.segmenters.setdefault(sid, Segmenter())
            utt = seg.feed(ev)
            if utt:
                self.on_utterance(sid, utt)
        self.flush()

    def flush(self):
        """Emit any utterance still open at EOF/stop (review finding 14)."""
        for sid, seg in self.segmenters.items():
            utt = seg.flush()
            if utt:
                self.on_utterance(sid, utt)

    def finalize(self):
        if self.finalized:
            return
        self.finalized = True
        self.artifact.finalize(self.cost.summary())
        s = self.cost.summary()
        log(f"artifact: {self.call_dir / 'artifact.json'}")
        log(f"cost: ${s['total_usd']} of ${s['ceiling_usd']} "
            f"(gate {s['gate_calls']}, hint {s['hint_calls']}, "
            f"ceiling_hit {s['ceiling_hit']})")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__ or "usage: orchestrator online|inperson|replay-online|replay-inperson")
    cmd = args[0]
    if cmd == "online":
        source, mode, replay = audio.LiveSource("stream-online"), "online", False
    elif cmd == "inperson":
        source, mode, replay = audio.LiveSource("stream-inperson"), "inperson", False
    elif cmd == "replay-online" and len(args) == 3:
        source = audio.ReplaySource({0: args[1], 1: args[2]})
        mode, replay = "online", True
    elif cmd == "replay-inperson" and len(args) == 2:
        source = audio.ReplaySource({0: args[1]})
        mode, replay = "inperson", True
    else:
        sys.exit("usage: orchestrator online | inperson | "
                 "replay-online <me.wav> <them.wav> | replay-inperson <mix.wav>")

    try:
        call = Call(mode, source, replay)
    except PackError as e:
        sys.exit(f"STOP: pack refused (reader law / A1): {e}")

    def on_sigint(_sig, _frm):
        log("SIGINT — finalizing artifact")
        call.stopping = True
        source.stop()
        try:
            call.flush()
        except Exception:
            pass
        call.finalize()
        sys.exit(0)

    signal.signal(signal.SIGINT, on_sigint)
    log(f"call {call.artifact.config['call_id']} ({mode}) — feed {call.feed_path}")
    try:
        call.run()      # returns on replay EOF
    finally:
        source.stop()
        call.finalize()  # finding 13: artifact survives an uncaught crash


if __name__ == "__main__":
    main()
