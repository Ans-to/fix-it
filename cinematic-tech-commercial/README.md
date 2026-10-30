# Cinematic tech commercial

Status: **storyboard approved**. Reusable atmosphere and impact-word components are in `src/components/`, and the audio sequencer is in `src/audio/`; individual scenes have not been built. The requested audio assets and measured timing data are not currently present in this checkout.

## Direction rules

- Keep each scene in its own component under `src/scenes/`; do not use monolithic scene code.
- Use atmospheric texture—such as vignettes, grids and glowing trackers—instead of flat black backgrounds, and high-velocity spring physics instead of standard web ease-in-out.
- Every impact keyword receives screen shake, chromatic aberration and a sub-bass audio trigger.
- Complete the storyboard phase before writing any video code.

## Dependencies

Install from the lockfile with `npm ci`. The requested packages are Three.js, Three.js types, React Three Fiber, Drei, Remotion Three, and Lucide React. React, React DOM and Remotion are explicit runtime dependencies; TypeScript and React types support the components. Run `npm run typecheck` and `npm run test:audio` for the component type check and audio timing unit tests.

## Component integration

- `Atmosphere` renders a textured, vignetted background with a frame-driven zoom. Supply `durationInFrames` for the containing scene when it differs from the composition length.
- `CinematicWord` wraps the **whole visual scene** in its `children` so its five-frame shake affects the viewport. Pass `text` and the Sequence-relative `triggerFrame`. When used by itself, pass `impactSoundSrc` as a path **relative to `public/`** (for example `sub_drop.mp3`); the component now applies `staticFile()` internally. This changes the previous API, which expected an already-resolved URL. When `AudioTrack` handles effects, pass `playImpactSound={false}` to prevent double-playing the sub-drop. `textStyle`, `seed`, `shakePixels`, and `impactVolume` are optional.
- Mount `AudioTrack` once at the composition root and provide `speechRanges` (all measured voice-active intervals) and `impactCues` (the actual start frames for `neither`, `only`, `leading`, and `1944`). Both use **composition-relative 30 fps frames**, and each speech range is `[startFrame, endFrame)`. Its voiceover starts at frame 0 unless `voiceoverStartFrame` is supplied. If a scene begins later, use `impactCue.frame - sceneStartFrame` as the scene-relative `CinematicWord.triggerFrame`. No cue frames or voice ranges are guessed from scene durations.
- Place `voiceover.mp3`, `bgm.mp3`, `whoosh.mp3`, and `sub_drop.mp3` in this project's `public/` directory. None are currently supplied. The BGM must cover the entire composition: the sequencer preserves position across ducking segments but does not loop a short file.
- BGM is reduced by exactly 8 dB in the supplied speech ranges using constant-volume segments. A synthetic encoded-audio test measured approximately -8.01 dB in two stable speech windows; this does not verify the unavailable real assets, actual speech boundaries, audible sync or perceived mix. Abrupt gain changes can be audible and need listening review. The storyboard is `storyboard.json`.
