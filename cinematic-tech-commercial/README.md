# Cinematic tech commercial

Status: **storyboard phase pending**. Dependencies are installed; no scenes or video code have been written.

## Direction rules

- Keep each scene in its own component under `src/scenes/`; do not use monolithic scene code.
- Use atmospheric texture—such as vignettes, grids and glowing trackers—instead of flat black backgrounds, and high-velocity spring physics instead of standard web ease-in-out.
- Every impact keyword receives screen shake, chromatic aberration and a sub-bass audio trigger.
- Complete the storyboard phase before writing any video code.

## Dependencies

Install from the lockfile with `npm ci`. The requested packages are Three.js, Three.js types, React Three Fiber, Drei, Remotion Three, and Lucide React. React, React DOM and Remotion are currently installed as dependencies or peers; additional development tooling can be selected after the storyboard.
