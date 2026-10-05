# call-assistant — ears of demo-agent (2026-10-05)

This repo is the ears of demo-agent's control layer: one control layer in demo-agent, per demo-agent rule 18 and `docs/design-prompter-2026-10-04.md` §3.

## Kept parts and their consumers

- `app/capture` builds `app/bin/capture`; `app/stt` builds `app/bin/stt-stream`. Demo-agent runs these binaries by path.
- `app/loop/audio.py` and `app/loop/segmenter.py` are loaded by exact file path by demo-agent's `app/voice/_call_assistant.py`, under `CALL_ASSISTANT_PATH` (default `/Users/rami/dev/call-assistant`). Never move or rename them; change them only with a demo-agent voice-test run.
- `app/loop/attribution.py` and `scripts/enroll_voiceprint.py` provide the in-person voiceprint for demo-agent P4.3.
- The `○ CA` menu bar starts and stops demo-agent's control layer after ca#6 (P2.4). This retirement branch must land only after ca#6.
- `scripts/grade_leg.py`, `scripts/score_leg.py` and the capture checks remain for leg grading and verification. `docs/` keeps the history.

## Disposition of the ten laws of 2026-08-11

This is the P2.5 draft for Rami's approval on call-assistant #7. That approval makes the wider reading binding (demo-agent rule 15; design §8(b)). Sources below are demo-agent's `docs/rulings.md` and design unless stated otherwise.

1. Audio never leaves the Mac: **off**. Demo-agent rule 15 allows a cloud transcriber.
2. No bots: **off**, by the wider reading of rule 15 (design §8(b)); nothing in the current build adds a meeting participant (design §3.1).
3. Read-only against the spine; canon export: **retired with the loop** (design P2.5). Nothing here reads canon any more.
4. Route by reader, Haiku gate / Sonnet hint: **off here**. Model routing belongs to demo-agent's CLAUDE.md model table (rule 15; design §8(b)).
5. Cost ceiling per call: **moved**. Demo-agent rule 7 and the coach's per-call ceiling hold it (design §12); never raised silently.
6. Shareability; the HDFC law live: **stays**, as demo-agent rule 6.
7. Staleness rendering: **retired with the loop** (design P2.5). No canon hints remain.
8. Me/them attribution, voiceprint, bleed guard: **stays** (design §3.1, P4.3). The channel split runs in demo-agent's ears; the voiceprint here serves P4.3.
9. Secrets: **stays**, as demo-agent rule 8. Secrets never enter git, chat or terminals.
10. House working agreements: **stays** (this repo's 2026-08-11 law 10): evidence before theory, verify at source, one command at a time with expected outputs in runbooks, files not pastes, summaries only of verified work, explicit staging (never `git add -A`), STATUS.md in the same commit as any state change.

The August P0–P3 phase gates and their exits, and the canon-export section, retire with the loop (design P2.5).
No terminal in daily use remains binding (2026-08-11 ruling; design §3.5). The control layer's rules live in demo-agent `docs/rulings.md`.
The demo-agent advisor holds this repo (2026-10-04 STATUS log).

## Retired loop by sha

Base: `c4dc0295b0c25de60b54ccf25d6f04b0403d724b`. Recover any removed path with `git show c4dc0295b0c25de60b54ccf25d6f04b0403d724b:<path>`.
Removed paths:

- `app/loop/orchestrator.py`
- `app/loop/llm.py`
- `app/loop/retrieval.py`
- `app/loop/cost.py`
- `app/loop/artifact.py`
- `app/overlay/__init__.py`
- `app/overlay/overlay.py`
- `prompts/gate-v1.md`
- `prompts/hint-v1.md`
- `prompts/hint-v2.md`
- `prompts/.gitkeep`
- `scripts/export-canon.sh`
- `scripts/llm_oneshot.py`
- `scripts/smoke_fake_call.sh`
- `scripts/verify_models.py`
- `scripts/launch-call-advisor.sh`
- `tests/test_artifact.py`
- `tests/test_cost.py`
- `tests/test_retrieval.py`
- `tests/test_reader_law.py`
