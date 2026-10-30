# Dollar 3D — production and motion score

**Brief:** Original 15-second explanatory test for Shorts, Reels and TikTok. Topic: why the dollar is widely used. Kokoro `am_eric` narration was requested. The Drive reference was a quality/pacing bar, not a layout or shot template. This is a new procedural design; no reference frames or footage were used. Proposed rather than user-confirmed test settings: 1080×1920, 30 fps, English.

**Authority:** `src/plan.json` is the machine-readable authority for format, scenes, headings, captions and VO timing under `manifest.schema.json` (custom `motion-threejs-v1.0.0`, not the skill's vector profile). The Remotion composition reads it directly. `src/video.jsx` is authoritative for geometry, colors, lighting, and motion and its procedural textures, which the schema does not model. `audio-metadata.json`, the audio-mixing script, voice metadata, and SRT describe the separate soundtrack. Timings are test assumptions, not an approved final production schedule.

## Claim and proof

- **Hook:** “Why does so much of the world rely on dollars?” does not imply universal use.
- **Deep markets:** “Deep U.S. financial markets make dollars easy to trade and hold.” Bars are abstract and not numerical financial data. Market depth, liquidity and conversion costs are among several reasons for dollar usage ([Federal Reserve, 2023](https://www.federalreserve.gov/econres/notes/feds-notes/2nd-annual-international-roles-of-the-us-dollar-conference-20230623.html)).
- **Network:** “As more people accept dollars, they become more useful to others.” This is a simple stylized example: node D joins, connects to the unit and sends a marker toward A. It is explicitly labeled illustrative, not evidence of particular measured transactions. Network effects are one of multiple factors ([Federal Reserve, 2026](https://www.federalreserve.gov/econres/notes/feds-notes/fifth-conference-on-the-international-roles-of-the-u-s-dollar-stablecoins-digital-payments-and-the-ir-of-the-usd-20260716.html)).
- **Qualifier:** “That helps the dollar lead, but it's not the only global currency.” USD is contrasted with distinct euro and yen objects, not claimed exclusive ([Federal Reserve, 2025](https://www.federalreserve.gov/econres/notes/feds-notes/the-international-role-of-the-u-s-dollar-2025-edition-20250718.html)).

## Motion score (30 fps, frame intervals [start,end))

| Beat | Focal subject / transformation | Type / sound / readable hold |
|---|---|---|
| Question [0,85) | Gold, double-faced, extruded USD coin enters an orbital field, rotates in depth and carries into the next beat; moving camera and background add parallax. | Words spring into the upper frame with stagger and settle; lower caption follows voice. First bed pulse and impact. |
| Markets [85,195) | The coin spins through the transition and shifts as raised, non-data financial blocks emerge. Rings continue across the cut; buy/sell/hold tags support liquidity. | Staggered two-line headline, held for reading; another transition impact / rising noise. |
| Network [195,302) | The coin spins and scales down. A/B/C appear, then D joins; a luminous marker travels D → USD → A to depict an additional possible connection. Nodes and links are actual 3D geometry; paths are illustrative. | Staggered headline and delayed explanatory label; impact at boundary, an additional accent near the transfer. |
| Payoff [302,450) | Coin spins and moves up/left, while silver EUR and JPY coins enter at different depths. All three are real 3D cylinder/face meshes; rings and camera are continuous. | Two-line qualified answer shifts to the lower part of the scene, with voice/caption and a later hold. Transition impact, final music fade. |

The 3D coin marks and letter textures are procedurally generated canvas textures, not image inputs. Motion is frame-driven, including orbit rotations, object positions, springs and camera movement. Typography remains 2D overlay choreography. Effects include a soft synth pulse, kick, bed and short noise/sine transition sweeps; generated locally, no sampled music. Production code uses Three.js/React Three Fiber/Remotion; actual renderer evidence is in `review.md`. Risk: synthetic sound and visual pacing need a human playback review; four beat-level headlines may still feel too templated to the user. Neither a 3D library nor a technical render alone proves the anti-slideshow gate.

## Dependency and review notes

The video contains sentence-level burnt-in captions and a separate `.srt`, derived from clip length, not aligned word by word. Check real platform overlays before publishing. A transcript-only reading verifies that the qualifier is in the narration; actual listening is still required. Refer to `review.md` for precise performed checks and unverified items.
