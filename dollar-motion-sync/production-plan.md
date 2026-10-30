# Dollar sync test — integrated direction and cue sheet

**Brief:** 15-second vertical test about the international role of the U.S. dollar, with Kokoro `am_eric`, actual 3D motion and kinetic typography. The user-provided Gemini analysis of the separate reference is treated as a report, not independent measurement. The original video is a quality bar, not a shot, slogan, sword motif, color, track or structural template. A short, single-idea narrative is more appropriate here than mechanically copying a 103-second two-act promotional video.

**Test assumptions, not locked production specs:** 1080×1920, 30 fps, English. Continuous-motion and sound-mix acceptance remains NEEDS HUMAN REVIEW. No reference footage, audio, stills or signature motif was used.

## Claims, voice and evidence

| Beat | Narration | Interpretation and source |
|---|---|---|
| Hook | “Why does the world use dollars? It's not just America.” | A question about widespread usage, not a claim that everyone uses USD. |
| Markets | “Deep markets make dollars easier to trade and hold.” | Stylized 3D bars and rings are abstract, not real market data. Market depth, liquidity and conversion costs are among several explanations ([Federal Reserve, 2023](https://www.federalreserve.gov/econres/notes/feds-notes/2nd-annual-international-roles-of-the-u-s-dollar-conference-20230623.html)). |
| Network | “As more people accept them, more connections become possible.” | A/B/C appear; D joins and a light travels from D through the dollar to A. It is an explicitly **illustrative model**, not recorded transactions or empirical proof. The Federal Reserve discusses network effects among multiple factors ([2026](https://www.federalreserve.gov/econres/notes/feds-notes/fifth-conference-on-the-international-roles-of-the-u-s-dollar-stablecoins-digital-payments-and-the-ir-of-the-usd-20260716.html)). |
| Qualification | “The dollar leads. But it's not the only global currency.” | USD, EUR and JPY are distinct 3D objects; the qualifier appears visually and in the narration ([Federal Reserve, 2025](https://www.federalreserve.gov/econres/notes/feds-notes/the-international-role-of-the-u-s-dollar-2025-edition-20250718.html)). |

## Motion / sync score (frames [start,end), 30 fps)

| Section | Pre-state → action → outcome; voice/type | Music / SFX |
|---|---|---|
| [0,105) hook | Rotating 3D globe and gold USD coin; oversized “WHY?”, “THE WORLD”, “DOLLARS?” then “NOT JUST / AMERICA.” Track words highlighted in a two-line caption. Globe scales down into the markets scene. | A 120 BPM original synth pulse starts immediately. Opening impact and a separate impact at the automatically estimated “dollars” word frame. |
| [105,210) markets | The globe recedes as illuminated extruded bars and coin rise, turn and travel through rings. “DEEP MARKETS” shifts to “TRADE & HOLD.” | Frame 105 is a beat-grid downbeat with impact and riser. “Trade” has a word-timed electronic tick. |
| [210,330) network | Bars recede and a labeled three-dimensional network grows around USD; new node D joins, then a marker moves from D through USD toward A. “MORE PEOPLE” changes to “MORE CONNECTIONS”. | Frame 210 is on the beat grid with impact and riser; a tick accompanies the estimated “connections” onset. Music softens in the post-voice gap and rises again for the next section. |
| [330,450) answer | Network makes way for a gold USD coin and silver EUR/JPY coins; “THE DOLLAR LEADS” becomes “NOT THE ONLY ONE.” | Frame 330 is a downbeat impact after the musical reduction. A tick lands at the estimated “not” onset. The music fades at the end. |

This structure interprets reported reference principles—punchy hook, meaningful motion, music contrast and synchronized accents—without reusing its actual layout, words, visuals or sounds. Type is a 2D overlay; the coin, wireframe globe, market bars, network nodes/links and moving perspective camera are real Three.js geometry. The timeline includes short intentional transition overlaps; these do not assert continuity of a single real-world object.

## Timing and audio handoff

`src/timeline.json` is the versioned `motion-sync-v1.0.0` authority for output settings, phrase boundaries, headings, captions and music/effect cue frames; `manifest.schema.json` validates its structure. `src/video.jsx` is authoritative for procedural 3D geometry, lighting, camera and title choreography; the schema does not model those values. `src/word-cues.json` stores separate word estimates from faster-whisper small run on the actual generated clip files, including local and absolute seconds, confidence and quantized frames. Transcript words matched normalized intended text. The estimates were not manually corrected; they are neither syllable-level nor verified timestamps. Quantization is nearest 30 fps frame, at most half a frame relative to the automatically estimated time, not relative to the true spoken onset.

`mix-audio.py` uses the same timeline for cue-driven effects. Narration is envelope-compressed, and the music bus has an automatic 10 ms VO-derived RMS duck detector, 35 ms attack, 240 ms release, and up to 7.5 dB reduction. `qa/ducking-curve.csv` records the applied control curve and `audio-metadata.json` records processing settings and peak; this is evidence of code-level behavior, not proof of clear speech, exact reference processing or artistic quality. SFX are separately generated signals and are not themselves ducked. The synthesized bed/effects are original waveforms, not sampled music. No de-essing, true-peak limiting, loudness normalization, phoneme alignment or human listening is claimed.

The 120 BPM beat grid begins at frame 0 (15 frames per beat). Three main section starts (105, 210, 330) and associated impacts coincide with beat grid positions in source timeline. Other accents follow estimated words and are not necessarily on the music beat. Caption timing is clip-duration based and highlighting follows estimated word cues; `.srt` preserves the complete phrase without word-level timing. Frame-coincident code events do not prove encoded, perceptual or syllable-exact synchronization. Review encoded playback and audio before publication.
