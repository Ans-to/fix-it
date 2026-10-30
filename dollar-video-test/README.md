# Dollar explainer — 15-second test

Main deliverable: **[`dollar-test.mp4`](dollar-test.mp4)**. This is an original vertical test for YouTube Shorts, Instagram Reels and TikTok—not a copy of the supplied reference. It uses Kokoro `am_eric`, procedurally generated background tones and effects, and original code-drawn graphics. The reference is not included as an asset. Read [`production-plan.md`](production-plan.md) for the brief, sources and timing and [`review.md`](review.md) for test scope and limitations.

The actual voice clips, captions and mixed audio are included, so rendering the video again does not require downloading the TTS model. With Python, Pillow, NumPy, `jsonschema` and FFmpeg available:

```sh
python3 dollar-video-test/build_plan.py
python3 dollar-video-test/audio_mix.py
FFMPEG=/path/to/ffmpeg python3 dollar-video-test/render_video.py --render
python3 dollar-video-test/test_video.py
```

The renderer writes `dollar-test.mp4`; back up existing outputs before rerendering. Pillow must support TrueType variable fonts; exact rasterization/encoding can differ by environment. The proposed output uses 1080×1920 and 30 fps for a 15-second test.

To regenerate the voice, the exact user-requested voice data and model are external: use `kokoro-js@1.2.1`'s `voices/am_eric.bin` and `kokoro-q8-shards@1.0.0`'s six shards from the npm registry, concatenate them in part0–part5 order, and verify model SHA-256 `fbae9257e1e05ffc727e951ef9b9c98418e6d79f1c9b6b13bd59f5c9028a1478`. Install `kokoro-onnx==0.4.9`, NumPy and ONNX Runtime in an isolated Python environment; set `KOKORO_MODEL` and `KOKORO_VOICE` to those local files and run `generate_voice.py`. The script records the actual voice hash and phonemes in `voice-metadata.json`. This project does not redistribute the large model weights. Kokoro and the voice assets are Apache-2.0 licensed; the display/body/mono font licenses are included in `fonts/`.
