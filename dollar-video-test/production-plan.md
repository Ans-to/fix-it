# 15-second dollar explainer — test production plan

## Brief and status

**Confirmed by user:** 15-second test; topic is the U.S. dollar's international role; intended audiences on YouTube Shorts, Instagram Reels and TikTok; Kokoro `am_eric`; reference is for professionalism/pacing, not a template. **Proposed for this test:** 1080×1920, 30 fps, English, original procedural graphics, synthesized bed and effects. These settings are not a claim of user-approved final specs. This is a test, not a publication or platform-safe certification.

## Creative direction

Original editorial finance design: warm paper, deep ink, cobalt accent, structured typographic hierarchy and diagrams. It is not a recreation of the reference video's scenes, palette, imagery or sequence. Large high-contrast headlines are introduced with short eased motion, while progressive rows and network nodes clarify the explanation. A quieter final hold leaves room for the payoff. Graphics are illustrative, not real transactions or quantified charts.

## Claim / proof map

| Claim | Exact narration | On-screen meaning / illustration | Source / limits |
|---|---|---|---|
| Question | “Why does so much of the world rely on dollars?” | “WHY THE DOLLAR?” introduces the topic. | Question; does not assert everyone uses dollars. |
| Market liquidity supports usage | “Deep U.S. financial markets make dollars easy to trade and hold.” | Buy/sell/hold rows, expressly illustrative; do not quantify market depth. | Federal Reserve, 2023: depth/liquidity of U.S. capital markets and relatively low conversion costs are among several factors in the dollar's ubiquity: https://www.federalreserve.gov/econres/notes/feds-notes/2nd-annual-international-roles-of-the-us-dollar-conference-20230623.html |
| Network benefit | “As more people accept dollars, they become more useful to others.” | Nodes grow and a path from new participant D to A appears; expressly labeled an illustrative network model, not empirical proof. | Federal Reserve conference notes, 2026, discuss continued importance of network effects: https://www.federalreserve.gov/econres/notes/feds-notes/fifth-conference-on-the-international-roles-of-the-u-s-dollar-stablecoins-digital-payments-and-the-ir-of-the-usd-20260716.html . The line is a simplified explanation, not the sole cause. |
| Leading, not exclusive | “That helps the dollar lead, but it's not the only global currency.” | “THE LEADER. NOT THE ONLY.” with EUR, JPY and others. | Federal Reserve 2025 edition reports dominant international use alongside other currencies: https://www.federalreserve.gov/econres/notes/feds-notes/the-international-role-of-the-u-s-dollar-2025-edition-20250718.html |

The narration contains the main question, financial-market explanation, network model and non-exclusivity qualifier without needing the visuals. This is a **transcript-only** listening-path review; an actual audio-only human listening pass was not performed.

## Timeline and handoff

The authoritative `visual-plan.json` specifies timeline, text, colors, audio cues and font hashes for the `dollar-pillow-profile-1.0.0` test. `manifest.schema.json` defines its machine-readable structural contract; `test_video.py` checks it and the listed semantic constraints. `render_video.py` defines fixed original vector geometry and frame-driven animation; `audio_mix.py` defines generated tones/effects. Frame intervals below are zero-based `[start,end)` under the **proposed** 30 fps render—not an approved production schedule.

| Scene | Frames | Purpose | Voice and caption timing | Motion |
|---|---:|---|---|---|
| Question | [0,85) | Set up the dollar question. | Voice starts frame 5, lasts 2.509 s. Matching caption uses two lines. | Title eases in; orbital dots move around a dollar symbol. |
| Markets | [85,195) | Explain liquidity. | Voice starts frame 87, lasts 3.541 s. | BUY, SELL, HOLD rows enter in sequence. |
| Network | [195,302) | Model why more participants can mean more possible connections. | Voice starts frame 197, lasts 3.241 s. | Participants enter sequentially; a marker travels from new participant D to A via the central unit. |
| Payoff | [302,450) | Dollar leads but is not the only global currency. | Voice starts frame 303, lasts 3.281 s; final hold follows. | The leading USD card and alternative-currency card enter in sequence. |

Caption starts correspond to actual segment insertion; SRT end times use the measured clip length. This is not word-level alignment or a human audio review. Caption text is measured with the shipped font and panel checks; the panel's actual platform safe-area status is unknown. Scene backgrounds use a decorative grid, not data.

## Dependencies and output

- `dollar-test.mp4`: encoded output, 15.00 s vertical H.264/AAC.
- `visual-plan.json`, `render_video.py`, `build_plan.py`, `audio_mix.py`, `generate_voice.py`: machine handoff and generation source. `captions.srt` is the sentence-level voice transcript; captions are also burned into the video.
- `voice-1.wav` to `voice-4.wav`, `voiceover.wav`, `audio-mix.wav`: Kokoro voice clips, combined voice, and mixed audio. `voice-metadata.json` records the exact model/voice SHA-256; music and effects are generated original waveforms.
- `fonts/`: Anton, Manrope and IBM Plex Mono, with their SIL Open Font Licenses; hashes are in the manifest. No input image/video footage was used.
- `qa/` and `review.md`: scoped checks and retained revision evidence. The exact platform UI guides, final playback, human audio listening and audience response are NOT CHECKED.
