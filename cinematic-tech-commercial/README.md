# Cinematic tech commercial — scene 1 prototype

The approved storyboard is `storyboard.json`. **Scene 1 is a silent visual prototype**, not the completed commercial. Scene 1 uses frame-driven 3D markers, a moving USD token, camera motion, kinetic type, and the reusable atmosphere and impact components. A/B are illustrative, not representations of a particular country or transaction.

## Preview

```sh
npm ci
npm run dev
```

Open the displayed Vite URL to review the Remotion Player. Use the player controls or the cue buttons to seek. `npm run studio` also opens the `Scene1Prototype` composition in Remotion Studio. The current preview proposes 1080×1920 and uses the requested 30 fps; it runs for the approved scene's 4.7 seconds (141 frames). Output format is a prototype assumption, not an approved delivery specification.

`src/config/mockTimings.ts` contains **estimated** scene-relative word cues: they are not derived from a recording, and must be replaced before audio synchronization. At frame 86, “NEITHER” triggers the word component's spring, five-frame deterministic shake, chromatic text and one-frame flash. All timing remains provisional.

## Audio and integration

`<AudioTrack />` is intentionally a silent placeholder. It does not check for or load any MP3s; `Scene1` also disables the impact-word component's own sound. Consequently this prototype has **no music, voiceover, whoosh or sub-drop**, including at impact frames.

The earlier real-audio implementation is retained as `ProductionAudioTrack` in `src/audio/AudioTrack.tsx` but is not mounted. It requires the four named audio files in `public/`, actual voice-active ranges, and verified impact cues at composition-relative 30 fps. It uses `staticFile()` and applies an 8 dB reduction to music across supplied ranges. Its BGM must cover the full composition; it does not automatically loop. Once audio is approved, mount it at composition root and keep `playImpactSound={false}` on the words to avoid doubling the sub-drop. For a standalone `CinematicWord`, `impactSoundSrc` is a file path relative to `public/` (not an already-resolved URL).

## Checks

`npm run typecheck`, `npm run test:audio`, `npm run test:mock`, and `npm run build:preview` validate types, silent-placeholder behavior, mock timing order, audio gain math, and the preview bundle. The preview was exercised with software WebGL, including playback and seeking. Selected frames were inspected; creative quality, full real-time visual review, platform placement and all audio remain for human review. No finished video export is claimed.

The Anton font in `public/fonts/` is included with its OFL license. Remotion may have commercial-use requirements: https://www.remotion.dev/license .
