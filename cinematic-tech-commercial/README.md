# Cinematic tech commercial

Status: **storyboard approved**. Reusable atmosphere and impact-word components are in `src/components/`; individual scenes have not been built.

## Direction rules

- Keep each scene in its own component under `src/scenes/`; do not use monolithic scene code.
- Use atmospheric texture—such as vignettes, grids and glowing trackers—instead of flat black backgrounds, and high-velocity spring physics instead of standard web ease-in-out.
- Every impact keyword receives screen shake, chromatic aberration and a sub-bass audio trigger.
- Complete the storyboard phase before writing any video code.

## Dependencies

Install from the lockfile with `npm ci`. The requested packages are Three.js, Three.js types, React Three Fiber, Drei, Remotion Three, and Lucide React. React, React DOM and Remotion are explicit runtime dependencies; TypeScript and React types support the components. Run `npm run typecheck` to check the two components.

## Component integration

- `Atmosphere` renders a textured, vignetted background with a frame-driven zoom. Supply `durationInFrames` for the containing scene when it differs from the composition length.
- `CinematicWord` wraps the **whole visual scene** in its `children` so its five-frame shake affects the viewport. Pass `text`, the Sequence-relative `triggerFrame`, and an `impactSoundSrc` pointing to an appropriately licensed sub-bass asset. The component triggers that asset at the hit but does not supply it. `textStyle`, `seed`, `shakePixels`, and `impactVolume` are optional.
- Impact words, VO timings and audio choices remain to be integrated when scenes are built. The storyboard is `storyboard.json`.
