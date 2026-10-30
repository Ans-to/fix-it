# Remotion composition

The 1080 × 1920 composition is 1,547 frames at 30 fps. `npm ci` installs the
Node dependencies. `npm run validate` checks TypeScript and the existing
frame-cue/source rules. `npm run render` bundles the registered composition and
renders all six scenes to `out/video.mp4` (H.264), including the narration if
`public/agent-engine/voiceover.wav` exists. Remotion requires a compatible
Chrome/Chromium installation; set `REMOTION_BROWSER_EXECUTABLE` to its path if
needed. Output and bundle progress are logged.

## Regenerating the narration

The scene texts and fixed frame ranges live in `scripts/narration.json`. The
script uses the **Jenny (Dioco)** Piper voice, an open-source speech model. It
synthesizes each word individually, trims leading/trailing silence and places
it on a frame boundary, then derives cues from the resulting audio sample
positions (not character-count estimates). This provides measurable timing,
but word-by-word synthesis can sound less natural than sentence-level TTS.
There are deliberate silent pauses between the short scene texts.

Install Python 3 and Piper, and obtain a compatible Piper ONNX model and its
JSON config (the model is not committed). For example, the generated audio uses
the Jenny voice from https://github.com/piper-tts-go/piper-voice-jenny (model
card and dataset details: https://github.com/dioco-group/jenny-tts-dataset).

```sh
python3 -m venv .venv
.venv/bin/pip install piper-tts==1.8.0 zstandard==0.25.0
# Download https://github.com/piper-tts-go/piper-voice-jenny/archive/refs/heads/main.tar.gz
# Extract dist.tzst from that archive and decompress it to obtain voice.onnx
# and voice.json. (For example: zstd -d dist.tzst -c | tar -xf -)
PIPER_PYTHON=.venv/bin/python \
PIPER_MODEL=/absolute/path/to/voice.onnx \
PIPER_CONFIG=/absolute/path/to/voice.json npm run voiceover
npm run validate
npm run render
```

Generation overwrites `public/agent-engine/voiceover.wav` and
`public/agent-engine/word-cues.json`. The model's dataset requires the voice to
be identified as Jenny (Dioco) where practical in interfaces that generate
speech. If the WAV is missing, rendering emits a warning and produces a silent
video. The validator's existing coverage warning is expected because the
short narration does not fill every frame.
