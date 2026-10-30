# Remotion composition

The 1080 × 1920 composition is 1,547 frames at 30 fps. `npm ci` installs the
Node dependencies. `npm run validate` checks TypeScript and the existing
frame-cue/source rules. `npm run render` bundles the composition and renders
all six scenes to `out/video.mp4` with narration. Remotion requires a compatible
Chrome/Chromium installation; set `REMOTION_BROWSER_EXECUTABLE` if needed.

## Regenerating and aligning narration

`scripts/narration.json` holds the six scene texts and fixed scene ranges. The
current recordings in `public/agent-engine/scenes/` use a selected natural voice
and speak each complete phrase rather than synthesizing isolated words. The
short phrases leave intentional silent intervals within the fixed scene lengths;
changing that requires longer text or different scene timings.

The voiceover script converts each recording to PCM, checks that it fits its
scene, and uses PocketSphinx forced alignment against the actual audio and known
text. It converts estimated acoustic boundaries to 30 fps frames and assembles
`public/agent-engine/voiceover.wav` and `word-cues.json`. Alignment is estimated,
not guaranteed word-exact; listen and inspect the cues, particularly for
unfamiliar words. PocketSphinx requires all words in its pronunciation
dictionary and reports an error instead of fabricating timestamps otherwise.

To re-align the included recordings:

```sh
python3 -m venv .venv
.venv/bin/pip install pocketsphinx==5.1.1
npm ci
ALIGN_PYTHON=.venv/bin/python npm run voiceover
npm run validate
npm run render
```

If you change the text, first provide matching new recordings or synthesize them
through ElevenLabs; forced alignment assumes the supplied transcript is correct.
You can set `VOICE_SCENES_DIR` to a directory containing six WAV files named
`hook`, `twist`, `shift`, `mechanism`, `payoff` and `outro`. Set `FFMPEG_PATH`
if FFmpeg is not installed or available in Remotion's compositor package.

To synthesize new scene recordings through ElevenLabs instead, set
`ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID` in your environment before
running the voiceover script. Optionally set `ELEVENLABS_MODEL_ID` (default
`eleven_multilingual_v2`). This uses the ElevenLabs API and may incur charges;
it requires network access and an account. Generated clips replace the stored
scene recordings only after all six scenes have been processed. Do not commit
API keys. The ElevenLabs path requires a valid key and has not been exercised in
this environment.

The validator's cue-coverage warning is expected because the narration is much
shorter than the full composition.
