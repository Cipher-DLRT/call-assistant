# call-assistant

The ears of demo-agent's control layer (demo-agent rule 18).

Demo-agent runs the capture and speech-to-text binaries built from `app/capture/` and `app/stt/`, and loads `app/loop/audio.py` and `app/loop/segmenter.py` by exact path via `CALL_ASSISTANT_PATH`.
The attribution module and voiceprint enrollment support in-person use (demo-agent P4.3); leg grading tools remain here.
After ca#6, the `○ CA` menu bar starts and stops demo-agent's control layer.
The August hint loop, overlay, prompts and canon export are retired; their base sha and removed paths are in [CLAUDE.md](CLAUDE.md).

See [CLAUDE.md](CLAUDE.md) for the repo's parts, law dispositions and working agreements. Landing awaits ca#6, owner voice tests and Rami's text approval on #7.
