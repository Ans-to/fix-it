# Review and evidence — 15-second test

The status names the specific scope checked, not a blanket claim that the video is ready for every platform.

| Check and exact scope | Status | Evidence / remaining work |
|---|---|---|
| Encoded video metadata and decode | PASS | FFmpeg decoded 450 video frames; file metadata reports 15.00 s, H.264, 1080×1920, 30 fps; AAC 48 kHz stereo. FPS and dimensions were chosen for this test and were not individually confirmed by the user. |
| Manifest structure and specified timeline/asset checks | PASS for named schema and assertions | `test_video.py` validates `visual-plan.json` against `manifest.schema.json` plus the stated frame, caption, voice-length and font-hash assertions. This does not prove full semantic or visual correctness. |
| Actual font-metric text bounds, text-to-text overlaps, caption panel fit, node-label containment | PASS for generated frames | `test_video.py` rendered all 450 plan frames in memory using the shipped fonts, checked all tracked text bounds and pairs, panel containment and network-circle text containment. This is not a full decoded-video pixel or occlusion test. |
| Static planned color pairs | PARTIAL | Table below tests selected solid palette combinations, not every fade, edge, grid line or composited state. See the actual frame samples. No WCAG conformance claim. |
| Scene/caption timing in the plan | PASS for scheduled clip intervals | WAV clip lengths and planned starts were checked against each scene; sentence captions use the same text and are scheduled against those durations. No word-level alignment is claimed. |
| Actual spoken clarity, caption alignment, audio/music balance and pronunciation | NOT CHECKED | Actual audio was generated and encoded. FFmpeg's numerical decoded audio measurement reports mean −21.9 dB and peak −6.3 dB, but no human listening pass was performed. The SRT contains speech, not a full accessibility treatment of music/effects. Please listen and check the captions. |
| Sampled decoded video frames | PARTIAL | `qa/decoded-contact-sheet.png` shows 17 selected decoded frames: 0, 5, 25, 45, 84, 85, 100, 135, 194, 195, 215, 260, 301, 302, 320, 360, 449. Not every event or cue boundary was sampled. |
| Complete motion playback / perceived pacing | NOT CHECKED | A contact sheet and full decode do not replace watching the full video at normal speed. |
| Platform-specific UI/safe areas | NOT CHECKED | No actual Shorts/Reels/TikTok in-app preview or current placement overlay was checked. Caption position is a project proposal, not a guaranteed safe zone. |
| Audience comprehension and retention | NEEDS HUMAN REVIEW | No audience test was run. The diagram is a simplified explanation, not proof of measured causation. |
| Assets and exact voice | PASS for named provenance | Procedural artwork and original generated sounds; fonts and licenses shipped. `voice-metadata.json` identifies Kokoro `am_eric`, the local model, voice SHA-256 and measured audio lengths. |

## Contrast planning pairs (unrounded calculated sRGB ratios)

| Foreground / background | Ratio | Evidence and limitation |
|---|---:|---|
| `#142738` / `#F4F1E9` | 13.510971952455721 | Ink on paper; color calculation only. |
| `#244BC7` / `#F4F1E9` | 6.40207324191143 | Blue on paper; color calculation only. |
| `#53616A` / `#F4F1E9` | 5.66235965042542 | Muted on paper; color calculation only. |
| `#53616A` / `#FDFCF8` | 6.225624887329444 | Muted on cream cards; color calculation only. |
| `#FDFCF8` / `#142738` | 14.85498068511046 | Cream on ink including captions; color calculation only. |
| `#C5D5DF` / `#142738` | 10.135606124701729 | Light label on dark card; color calculation only. |
| `#FDFCF8` / `#244BC7` | 7.038921750997432 | Cream on blue; color calculation only. |

Reference target for ordinary text: 4.5:1; these calculations do not test moving/fading states or prove accessibility compliance.

## Reading holds

The heading entrance settles 17 frames into each scene under the proposed 30 fps. Using the skill's English `max(1.5 s, characters/15 s)` planning heuristic: question 15 characters / estimate 1.5 s / hold 2.27 s; markets 28 / 1.87 s / 3.10 s; network 24 / 1.60 s / 3.00 s; payoff 25 / 1.67 s / 4.37 s. Counts join the two headline lines with a space. These are estimates only; simultaneous captions and graphics can compete for attention and actual viewer readability is NOT CHECKED.
