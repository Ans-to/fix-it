# Why is the dollar a world currency?
## A new 60-second code-only Director script

### Brief and assumptions
- **Confirmed:** A one-minute script explaining the dollar’s international role. All video visuals must be created in code; no image or video inputs.
- **Proposed, not confirmed:** A general English-speaking audience; 1080 × 1920 portrait, 30 fps, exactly 1,800 visual frames; social/video feed placement. Specific platform, overlay boundaries and voice are unconfirmed.
- **Promise:** Explain how history, market depth and reinforcing use support the dollar’s international role. State that it is a leading currency, not the only one, and that its position may change.
- **Audience journey:** Ask why two parties might use someone else’s currency; establish the system’s historical foundations; explain what survived after gold conversion was suspended; show a growing illustrative network; return to the same two parties and directly answer the opening.
- **Hook options:** A: “Why might two countries trade in dollars when neither one issues them?” B: “The dollar’s gold conversion was suspended. Why did its global role continue?” **Recommended: A**, because the final scene can answer the same question with the same two parties. This is a creative judgment, not a tested retention result.

## Exact voiceover

> Why might two countries trade in dollars when neither one issues them?

> The dollar is the leading international currency, not the only one. It's widely used for trade invoicing, finance, and reserves.

> In 1944, Bretton Woods placed the dollar at the center of a new postwar monetary system.

> Participating countries tied their currencies to the dollar. The United States offered gold for dollars held by foreign central banks.

> In 1971, the United States suspended gold conversion. The dollar's international role continued after the system changed.

> A large U.S. economy and deep Treasury markets support the dollar, while widespread trade invoicing gives people reasons to use it.

> As more people use dollars, others may find them easier to use. That network effect can reinforce the dollar's role.

> So those two countries can choose dollars because they already have access to a widely used system. Other currencies can work too.

The draft contains about 149 word tokens. Numerals and initials can take longer to say. No voice has been recorded, so natural speaking rate, scene boundaries and the final 60-second mix remain unverified.

## Non-negotiable rules
1. **No visual image or video inputs.** No photographs, screenshots, footage, still-image files, generated-image assets, textures or imported SVG illustrations. Draw all visuals using text, solid colors, circles, rounded rectangles and lines in code. Licensed font files are allowed. The contact sheet is a test output, not an input asset.
2. **No invented facts or data.** Countries A and B are hypothetical. Currency symbols and network nodes are illustrative examples—not exhaustive, not real trades, and not scaled to statistics. The growing network is an explanatory model, not empirical proof that a particular person benefited.
3. **One-minute visual timeline:** 0-based, 30 fps; frames 0–1799 inclusive; intervals `[start,end)`. Exactly 1,800 planned frames under the proposed format. A recorded voice track has not been timed; caption and VO cue timings are provisional.
4. **Determinism:** Derive state from the frame, plan, font and fixed render configuration. No wall-clock timing, unseeded randomness or history-dependent playback. The font is DejaVu Sans Bold; substitute only with approval and repeat layout checks.
5. **Exact dependency:** The complete `visual-plan.json` is embedded at the end of this file and is also supplied separately. It contains every shape, motion, caption cue, group, layer, camera, color and coordinate. Keep the copies identical; no missing authoritative manifest.
6. **Review before delivery:** Do not claim sound synchronization, platform-safe placement, full visual quality, accessibility compliance or audience engagement unless the corresponding output and evidence have actually been inspected.

## Scene plan and camera
All scenes use a virtual, front-facing **orthographic camera** with pitch, yaw and roll all `0°`. Both viewport center and intentional zoom anchor are `(540,960)`; no physical camera, footage or 3D scene is used. Zoom applies to world graphics only; headings, subheadings and captions are screen-fixed.
| Scene | Time | Frames `[start,end)` | World-camera zoom | Creative purpose |
|---|---|---|---|---|
| 01_question | 00:00.000–00:06.000 | [0, 180) | 1.000 → 1.010 | Show the opening puzzle: two symbolic countries trade using a dollar. |
| 02_definition | 00:06.000–00:13.500 | [180, 405) | 1.000 → 1.000 | Give the spoken and visible qualification; the euro and yen are illustrative examples, not an exhaustive list or scaled data. |
| 03_history | 00:13.500–00:20.000 | [405, 600) | 1.000 → 1.010 | Place the 1944 conference within a postwar framework; the dollar also had an earlier international role. |
| 04_gold | 00:20.000–00:28.000 | [600, 840) | 1.000 → 1.000 | Show currency links while preserving the essential foreign-central-bank qualifier. |
| 05_suspension | 00:28.000–00:35.000 | [840, 1050) | 1.000 → 1.010 | Fade the gold-conversion link without claiming the entire Bretton Woods system ended in one day. |
| 06_economy | 00:35.000–00:43.000 | [1050, 1290) | 1.000 → 1.000 | State the supporting factors without numerical or causal overclaim. |
| 07_network | 00:43.000–00:51.000 | [1290, 1530) | 1.000 → 1.010 | First show two connected participants; then reveal a new user and two new links. The animation illustrates a mechanism, not data or causal proof. |
| 08_answer | 00:51.000–01:00.000 | [1530, 1800) | 1.000 → 1.000 | Return to the same two parties and directly answer the opening; retain non-exclusivity. |

## Per-frame construction contract
For frame `f`, select its single scene, then set `local = f − scene.start` and `D = scene.end − scene.start`. `smooth(x)=u²(3−2u)`, with `u=clamp(x,0,1)`. Coordinates use a top-left origin; rectangles use top-left positions, while text and circles use centers. All units are pixels.

- Background: fill `night #101B2B`. Colors: `panel #1C2D40`, `ivory #F7F4EC`, `muted #C3CED7`, `gold #EAC777`, `line #96AABB`.
- Each object has an explicit delay and `screen` or `world` group. Compute entry opacity `smooth((local−delay)/18)`. If `fade_out=[a,b]`, multiply opacity by `1−smooth((local−a)/(b−a))`. There is no entry-position shift. Screen headings and subheadings use delay 0 and no camera transform.
- World camera: `z=z0+(z1−z0)×smooth(local/(D−1))`; transform `(x,y)` to `(540+(x−540)×z, 960+(y−960)×z)`. Scale world radii, sizes, stroke widths and font sizes by `z`. Round raster text size and stroke width to the nearest pixel.
- If an object has `move_x`, set its pre-camera x to `from+(to−from)×smooth((local−local_start)/(local_end−local_start))`. Otherwise its base position is held. In scene 1, token and `$` travel together from x=365 to x=715 over local frames 18–120. The token radius is 50 and country radius 70; at each end it touches the respective country’s edge rather than stopping short.
- Draw background, then world objects in their listed order, then screen objects, then captions, using source-over alpha. Network lines are drawn underneath nodes; entry fades have no position shift so endpoints remain attached.
- Captions use a fixed rounded panel at `(70,1510)`, `940 × 180`, radius 22, panel fill. Use 42 px ivory DejaVu Sans Bold: one-line pages centered at `(540,1600)`; two-line pages at `(540,1568)` and `(540,1635)`. **Platform-safe area: NOT VERIFIED.** Caption copy and provisional intervals are specified below, but cue timing is not aligned to any recording.

## Scene-by-scene production directions
Base positions below are transformed by the per-frame contract. Objects inside their labeled containers are intentional. Scene 7 is a conceptual model: a new participant and new connections appear later; it illustrates a possible reinforcing mechanism, not a measured result.

### 01_question — frames [0, 180)
**Purpose:** Show the opening puzzle: two symbolic countries trade using a dollar.

**Voiceover:** “Why might two countries trade in dollars when neither one issues them?”

| Object | Base geometry and styling | Group / timing |
|---|---|---|
| heading | Text **WHY USE DOLLARS?**, center (540, 320), 66 px, color `ivory` | screen; delay 0 |
| subheading | Text **TWO COUNTRIES. ONE CURRENCY.**, center (540, 430), 40 px, color `muted` | screen; delay 0 |
| route | Line (313.0, 900.0) → (767.0, 900.0), `line`, 4 px | world; delay 6 |
| country_a | Circle center (245, 900), radius 70, fill `panel`, stroke `line` 3 px | world; delay 6 |
| country_b | Circle center (835, 900), radius 70, fill `panel`, stroke `line` 3 px | world; delay 6 |
| token | Circle center (540, 900), radius 50, fill `gold`, stroke `gold` 3 px | world; delay 6; x 365→715 at local 18–120 |
| dollar | Text **$**, center (540, 900), 66 px, color `night`, inside `token` | world; delay 6; x 365→715 at local 18–120 |
| country_a_label | Text **COUNTRY A**, center (245, 1090), 40 px, color `muted` | world; delay 6 |
| country_b_label | Text **COUNTRY B**, center (835, 1090), 40 px, color `muted` | world; delay 6 |

**Draft caption pages; real audio alignment is pending:**
- Frames `[0, 165)`: “Why might two countries trade in” / “dollars when neither one issues”
- Frames `[165, 180)`: “them?”

### 02_definition — frames [180, 405)
**Purpose:** Give the spoken and visible qualification; the euro and yen are illustrative examples, not an exhaustive list or scaled data.

**Voiceover:** “The dollar is the leading international currency, not the only one. It's widely used for trade invoicing, finance, and reserves.”

| Object | Base geometry and styling | Group / timing |
|---|---|---|
| heading | Text **LEADING. NOT ONLY.**, center (540, 320), 66 px, color `ivory` | screen; delay 0 |
| subheading | Text **CURRENCIES COEXIST**, center (540, 430), 40 px, color `muted` | screen; delay 0 |
| euro_node | Circle center (260, 810), radius 62, fill `panel`, stroke `line` 3 px | world; delay 6 |
| dollar_node | Circle center (540, 810), radius 78, fill `panel`, stroke `gold` 3 px | world; delay 6 |
| yen_node | Circle center (820, 810), radius 62, fill `panel`, stroke `line` 3 px | world; delay 6 |
| euro | Text **€**, center (260, 810), 72 px, color `ivory`, inside `euro_node` | world; delay 6 |
| dollar | Text **$**, center (540, 810), 90 px, color `gold`, inside `dollar_node` | world; delay 6 |
| yen | Text **¥**, center (820, 810), 72 px, color `ivory`, inside `yen_node` | world; delay 6 |
| trade_card | Rounded rectangle at (105, 1030), 270 × 145, radius 22, fill `panel`, stroke `line` 3 px | world; delay 12 |
| finance_card | Rounded rectangle at (405, 1030), 270 × 145, radius 22, fill `panel`, stroke `line` 3 px | world; delay 22 |
| reserve_card | Rounded rectangle at (705, 1030), 270 × 145, radius 22, fill `panel`, stroke `line` 3 px | world; delay 32 |
| trade | Text **INVOICING**, center (240, 1102), 39 px, color `ivory`, inside `trade_card` | world; delay 12 |
| finance | Text **FINANCE**, center (540, 1102), 39 px, color `ivory`, inside `finance_card` | world; delay 22 |
| reserves | Text **RESERVES**, center (840, 1102), 38 px, color `ivory`, inside `reserve_card` | world; delay 32 |

**Draft caption pages; real audio alignment is pending:**
- Frames `[180, 281)`: “The dollar is the leading” / “international currency, not the”
- Frames `[281, 394)`: “only one. It's widely used for” / “trade invoicing, finance, and”
- Frames `[394, 405)`: “reserves.”

### 03_history — frames [405, 600)
**Purpose:** Place the 1944 conference within a postwar framework; the dollar also had an earlier international role.

**Voiceover:** “In 1944, Bretton Woods placed the dollar at the center of a new postwar monetary system.”

| Object | Base geometry and styling | Group / timing |
|---|---|---|
| heading | Text **THE POSTWAR PLAN**, center (540, 320), 66 px, color `ivory` | screen; delay 0 |
| subheading | Text **BRETTON WOODS**, center (540, 430), 40 px, color `muted` | screen; delay 0 |
| history_card | Rounded rectangle at (150, 760), 780 × 310, radius 22, fill `panel`, stroke `gold` 3 px | world; delay 6 |
| year | Text **1944**, center (540, 885), 150 px, color `gold`, inside `history_card` | world; delay 6 |
| history_note | Text **POSTWAR FRAMEWORK**, center (540, 1010), 42 px, color `muted`, inside `history_card` | world; delay 6 |

**Draft caption pages; real audio alignment is pending:**
- Frames `[405, 563)`: “In 1944, Bretton Woods placed the” / “dollar at the center of a new”
- Frames `[563, 600)`: “postwar monetary system.”

### 04_gold — frames [600, 840)
**Purpose:** Show currency links while preserving the essential foreign-central-bank qualifier.

**Voiceover:** “Participating countries tied their currencies to the dollar. The United States offered gold for dollars held by foreign central banks.”

| Object | Base geometry and styling | Group / timing |
|---|---|---|
| heading | Text **THE GOLD LINK**, center (540, 320), 66 px, color `ivory` | screen; delay 0 |
| subheading | Text **FOREIGN CENTRAL BANKS**, center (540, 430), 40 px, color `muted` | screen; delay 0 |
| left_link | Line (355, 920) → (415, 920), `line`, 4 px | world; delay 6 |
| right_link | Line (665, 920) → (725, 920), `line`, 4 px | world; delay 6 |
| other_box | Rounded rectangle at (100, 830), 255 × 180, radius 22, fill `panel`, stroke `line` 3 px | world; delay 6 |
| dollar_box | Rounded rectangle at (415, 830), 250 × 180, radius 22, fill `panel`, stroke `gold` 3 px | world; delay 6 |
| gold_box | Rounded rectangle at (725, 830), 255 × 180, radius 22, fill `panel`, stroke `gold` 3 px | world; delay 6 |
| other_first | Text **OTHER**, center (227, 895), 40 px, color `ivory`, inside `other_box` | world; delay 6 |
| other_second | Text **MONEY**, center (227, 950), 40 px, color `ivory`, inside `other_box` | world; delay 6 |
| usd | Text **$**, center (540, 920), 85 px, color `gold`, inside `dollar_box` | world; delay 6 |
| gold | Text **GOLD**, center (852, 920), 43 px, color `gold`, inside `gold_box` | world; delay 6 |
| qualifier | Text **FOREIGN CENTRAL BANKS**, center (540, 1190), 42 px, color `muted` | world; delay 6 |

**Draft caption pages; real audio alignment is pending:**
- Frames `[600, 708)`: “Participating countries tied their” / “currencies to the dollar. The”
- Frames `[708, 828)`: “United States offered gold for” / “dollars held by foreign central”
- Frames `[828, 840)`: “banks.”

### 05_suspension — frames [840, 1050)
**Purpose:** Fade the gold-conversion link without claiming the entire Bretton Woods system ended in one day.

**Voiceover:** “In 1971, the United States suspended gold conversion. The dollar's international role continued after the system changed.”

| Object | Base geometry and styling | Group / timing |
|---|---|---|
| heading | Text **CONVERSION**, center (540, 320), 66 px, color `ivory` | screen; delay 0 |
| subheading | Text **SUSPENDED IN 1971**, center (540, 430), 40 px, color `muted` | screen; delay 0 |
| left_link | Line (390, 910) → (490, 910), `line`, 4 px | world; delay 6 |
| middle_link | Line (490, 910) → (590, 910), `line`, 4 px | world; delay 6; fade-out local 40–64 |
| right_link | Line (590, 910) → (690, 910), `line`, 4 px | world; delay 6 |
| dollar_box | Rounded rectangle at (140, 820), 250 × 180, radius 22, fill `panel`, stroke `gold` 3 px | world; delay 6 |
| gold_box | Rounded rectangle at (690, 820), 250 × 180, radius 22, fill `panel`, stroke `gold` 3 px | world; delay 6 |
| dollar | Text **$**, center (265, 910), 85 px, color `gold`, inside `dollar_box` | world; delay 6 |
| gold | Text **GOLD**, center (815, 910), 43 px, color `gold`, inside `gold_box` | world; delay 6 |
| status | Text **OFFICIAL CONVERSION SUSPENDED**, center (540, 1185), 40 px, color `muted` | world; delay 6 |

**Draft caption pages; real audio alignment is pending:**
- Frames `[840, 951)`: “In 1971, the United States” / “suspended gold conversion. The”
- Frames `[951, 1038)`: “dollar's international role” / “continued after the system”
- Frames `[1038, 1050)`: “changed.”

### 06_economy — frames [1050, 1290)
**Purpose:** State the supporting factors without numerical or causal overclaim.

**Voiceover:** “A large U.S. economy and deep Treasury markets support the dollar, while widespread trade invoicing gives people reasons to use it.”

| Object | Base geometry and styling | Group / timing |
|---|---|---|
| heading | Text **WHY IT CONTINUED**, center (540, 320), 66 px, color `ivory` | screen; delay 0 |
| subheading | Text **SCALE + LIQUID MARKETS**, center (540, 430), 40 px, color `muted` | screen; delay 0 |
| economy_card | Rounded rectangle at (140, 735), 800 × 140, radius 22, fill `panel`, stroke `line` 3 px | world; delay 6 |
| market_card | Rounded rectangle at (140, 920), 800 × 140, radius 22, fill `panel`, stroke `gold` 3 px | world; delay 20 |
| trade_card | Rounded rectangle at (140, 1105), 800 × 140, radius 22, fill `panel`, stroke `line` 3 px | world; delay 34 |
| economy | Text **LARGE U.S. ECONOMY**, center (540, 805), 43 px, color `ivory`, inside `economy_card` | world; delay 6 |
| market | Text **DEEP TREASURY MARKETS**, center (540, 990), 43 px, color `gold`, inside `market_card` | world; delay 20 |
| trade | Text **TRADE INVOICING**, center (540, 1175), 43 px, color `ivory`, inside `trade_card` | world; delay 34 |

**Draft caption pages; real audio alignment is pending:**
- Frames `[1050, 1164)`: “A large U.S. economy and deep” / “Treasury markets support the”
- Frames `[1164, 1267)`: “dollar, while widespread trade” / “invoicing gives people reasons to”
- Frames `[1267, 1290)`: “use it.”

### 07_network — frames [1290, 1530)
**Purpose:** First show two connected participants; then reveal a new user and two new links. The animation illustrates a mechanism, not data or causal proof.

**Voiceover:** “As more people use dollars, others may find them easier to use. That network effect can reinforce the dollar's role.”

| Object | Base geometry and styling | Group / timing |
|---|---|---|
| heading | Text **USE REINFORCES USE**, center (540, 320), 66 px, color `ivory` | screen; delay 0 |
| subheading | Text **AN ILLUSTRATIVE MODEL**, center (540, 430), 40 px, color `muted` | screen; delay 0 |
| hub_left | Line (475.27, 818.52) → (293.15, 940.98), `line`, 4 px | world; delay 16 |
| hub_right | Line (604.73, 818.52) → (786.85, 940.98), `line`, 4 px | world; delay 16 |
| existing_peers | Line (302.0, 970.0) → (778.0, 970.0), `line`, 4 px | world; delay 26 |
| new_to_left | Line (497.88, 1149.5) → (292.12, 1000.5), `line`, 4 px | world; delay 96 |
| new_to_right | Line (582.12, 1149.5) → (787.88, 1000.5), `line`, 4 px | world; delay 96 |
| new_to_hub | Line (540.0, 853.0) → (540.0, 1128.0), `line`, 4 px | world; delay 96 |
| hub | Circle center (540, 775), radius 80, fill `gold`, stroke `gold` 3 px | world; delay 6 |
| hub_dollar | Text **$**, center (540, 775), 92 px, color `night`, inside `hub` | world; delay 6 |
| left_node | Circle center (250, 970), radius 54, fill `panel`, stroke `line` 3 px | world; delay 16 |
| right_node | Circle center (830, 970), radius 54, fill `panel`, stroke `line` 3 px | world; delay 16 |
| new_node | Circle center (540, 1180), radius 54, fill `panel`, stroke `line` 3 px | world; delay 96 |
| bank_label | Text **BANKS**, center (250, 1080), 40 px, color `muted` | world; delay 16 |
| business_label | Text **BUSINESSES**, center (830, 1080), 40 px, color `muted` | world; delay 16 |
| new_label | Text **NEW USER**, center (540, 1290), 40 px, color `muted` | world; delay 96 |
| model_note | Text **USE CAN GET EASIER**, center (540, 1380), 44 px, color `ivory` | world; delay 110 |

**Draft caption pages; real audio alignment is pending:**
- Frames `[1290, 1422)`: “As more people use dollars,” / “others may find them easier to”
- Frames `[1422, 1530)`: “use. That network effect can” / “reinforce the dollar's role.”

### 08_answer — frames [1530, 1800)
**Purpose:** Return to the same two parties and directly answer the opening; retain non-exclusivity.

**Voiceover:** “So those two countries can choose dollars because they already have access to a widely used system. Other currencies can work too.”

| Object | Base geometry and styling | Group / timing |
|---|---|---|
| heading | Text **WHY THEY CHOOSE $**, center (540, 320), 66 px, color `ivory` | screen; delay 0 |
| subheading | Text **COMMON ACCESS, NOT A RULE**, center (540, 430), 40 px, color `muted` | screen; delay 0 |
| route | Line (313.0, 900.0) → (767.0, 900.0), `line`, 4 px | world; delay 6 |
| country_a | Circle center (245, 900), radius 70, fill `panel`, stroke `line` 3 px | world; delay 6 |
| country_b | Circle center (835, 900), radius 70, fill `panel`, stroke `line` 3 px | world; delay 6 |
| token | Circle center (715, 900), radius 50, fill `gold`, stroke `gold` 3 px | world; delay 6 |
| dollar | Text **$**, center (715, 900), 66 px, color `night`, inside `token` | world; delay 6 |
| country_a_label | Text **COUNTRY A**, center (245, 1090), 40 px, color `muted` | world; delay 6 |
| country_b_label | Text **COUNTRY B**, center (835, 1090), 40 px, color `muted` | world; delay 6 |
| answer | Text **BOTH CAN USE ONE SYSTEM**, center (540, 1240), 43 px, color `ivory` | world; delay 6 |
| other | Text **OTHER CURRENCIES CAN WORK TOO**, center (540, 1330), 40 px, color `muted` | world; delay 6 |

**Draft caption pages; real audio alignment is pending:**
- Frames `[1530, 1665)`: “So those two countries can choose” / “dollars because they already have”
- Frames `[1665, 1800)`: “access to a widely used system.” / “Other currencies can work too.”

## Audio and accessibility
- One clear, conversational narrator. Record the exact script and revise timing around the recording. Do not speed up speech solely to hit a frame number; rebalance scenes while preserving the final agreed duration.
- Optional original or licensed low-level music can support the voice; none is required or supplied. Add meaningful non-speech audio to captions where appropriate. Provide visual description or a descriptive transcript for important visuals not conveyed in audio.
- Perform an actual playback, listening, caption-alignment, device-size readability and platform-overlay review before delivery. These checks have not been performed here.

## Test report — narrow scope
- **PASS: visual timeline math.** Eight non-overlapping scene intervals cover frames 0–1799 at the proposed 30 fps: 60 seconds of planned visuals.
- **PASS: selected all-frame geometry.** On all 1,800 planned frames, code checked project bounds, text-to-text bounding boxes, selected text containment in both rectangular and circular containers, and caption coverage/bounds. It checked token edge contact at the two stated endpoints and network line endpoints against their nodes. This is not a complete all-object collision or playback test.
- **PASS: exact draft caption text.** The planned caption pages concatenate to the narration. Their timing is not verified against speech.
- **PASS: declared fully opaque text/background pairs only.** Ratios: gold on panel: 8.63:1; ivory on night: 15.74:1; ivory on panel: 12.75:1; muted on night: 10.82:1; muted on panel: 8.76:1; night on gold: 10.66:1. These calculations do not cover partially transparent/composited animation frames, non-text graphics, actual device readability, or overall accessibility compliance.
- **PASS: visual input restriction.** The manifest uses only programmatic text, circles, rectangles and lines. The QA contact sheet is generated from these primitives and is not a video input.
- **NOT CHECKED:** finished video, full-motion playback, narration length, audio/caption synchronization, platform UI overlays, real-device legibility, independent factual review, viewer comprehension or retention.

## Sources and scope
- [Federal Reserve: International Role of the U.S. Dollar (2025)](https://www.federalreserve.gov/econres/notes/feds-notes/the-international-role-of-the-u-s-dollar-2025-edition-20250718.html): role of economic scale and deep financial markets; the dollar had an international role before 1944.
- [IMF: Central Banks and the Bretton Woods Gold Puzzle](https://www.imf.org/-/media/files/publications/wp/2019/wpiea2019161.pdf): 1944 Bretton Woods framework and the U.S. gold-conversion commitment to other central banks.
- [U.S. State Department: Nixon and the End of Bretton Woods](https://history.state.gov/milestones/1969-1976/nixon-shock): the United States suspended gold convertibility in 1971; the broader fixed-rate system unraveled over 1971–1973.
- [BIS: Global reach of currencies](https://www.bis.org/publ/qtrpdf/r_qt2406b.htm) and [BIS: foreign-exchange markets](https://www.bis.org/publications/qr-202212/global-foreign-exchange-market-higher-volatility-environment): the dollar’s international financial role and trade invoicing.
- [IMF: The Dollar’s Primacy](https://www.imf.org/en/publications/fandd/issues/2022/03/book-review-dollar-primacy-joyce): market liquidity and network effects. The drawn network is an illustration, not causal or quantitative evidence.

## Embedded complete visual-plan.json
This is the full [separate visual-plan.json](visual-plan.json). The SHA-256 below is computed on the **actual separate UTF-8 file bytes**, including its final LF newline. To reconstruct those bytes from the fenced block, take the block content without the fence delimiter and append one LF. Do not use semantic JSON equality as proof of byte equality.

File SHA-256: `6fa1669bcf041b3cfb268f695ddd740ee46669b961f72d5b951f238b233a15f3`.
```json
{
  "title": "Why is the dollar a world currency?",
  "format": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "frames": 1800,
    "status": "PROPOSED; duration is confirmed, platform and format are not",
    "frame_range": "0-based [start,end)"
  },
  "colors": {
    "night": "#101B2B",
    "panel": "#1C2D40",
    "ivory": "#F7F4EC",
    "muted": "#C3CED7",
    "gold": "#EAC777",
    "line": "#96AABB"
  },
  "font": {
    "name": "DejaVu Sans Bold",
    "tested_path": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "substitution": "requires re-testing"
  },
  "restrictions": [
    "No photos, footage, images, screenshots, textures, external SVGs, or video inputs.",
    "Draw only solid rectangles, circles, lines and text; licensed font files allowed.",
    "All currency symbols, countries and network nodes are illustrative, not exhaustive or data-scaled."
  ],
  "contract": {
    "coordinates": "top-left origin; text and circles use centers, rectangles top-left",
    "scene_selection": "0-based start inclusive, end exclusive; hard cuts",
    "entry": "local=frame-scene.start; alpha=smooth((local-delay)/18), smooth(x)=u*u*(3-2*u), u=clamp(x,0,1). No entry translation. If fade_out=[a,b], multiply alpha by 1-smooth((local-a)/(b-a)).",
    "camera": "All cameras orthographic with yaw/pitch/roll 0. Screen center and zoom anchor (540,960). World points (x,y) map to (540+(x-540)*z,960+(y-960)*z); z=z0+(z1-z0)*smooth(local/(scene_duration-1)). Scale world shapes, text and strokes by z. Heading, subheading and captions are screen-fixed.",
    "motion": "When move_x is present, x=from+(to-from)*smooth((local-local_start)/(local_end-local_start)) before camera transform. Otherwise the object geometry holds. Token circles and glyphs use the same move_x.",
    "z_order": "Background, then world objects in listed order, then screen objects in listed order, then captions. Source-over alpha. Network lines are drawn behind nodes.",
    "captions": "Draft cue ranges are provisional, not synced to speech. Fixed panel (70,1510) size 940×180 radius 22; fill panel. Bold 42 px ivory: one line at (540,1600); two lines at (540,1568) and (540,1635). PLATFORM SAFE AREA NOT VERIFIED. Re-align to final voice, review and add meaningful non-speech captions if needed.",
    "reproducibility": "Font metrics depend on installed font version; replacement requires review. Round scaled font size and stroke width to nearest pixel."
  },
  "scenes": [
    {
      "id": "01_question",
      "start": 0,
      "end": 180,
      "camera": {
        "projection": "orthographic",
        "yaw": 0,
        "pitch": 0,
        "roll": 0,
        "screen_center": [
          540,
          960
        ],
        "zoom_anchor": [
          540,
          960
        ],
        "zoom_start": 1,
        "zoom_end": 1.01
      },
      "voiceover": "Why might two countries trade in dollars when neither one issues them?",
      "purpose": "Show the opening puzzle: two symbolic countries trade using a dollar.",
      "objects": [
        {
          "id": "heading",
          "kind": "text",
          "text": "WHY USE DOLLARS?",
          "x": 540,
          "y": 320,
          "size": 66,
          "color": "ivory",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "subheading",
          "kind": "text",
          "text": "TWO COUNTRIES. ONE CURRENCY.",
          "x": 540,
          "y": 430,
          "size": 40,
          "color": "muted",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "route",
          "kind": "line",
          "x1": 313.0,
          "y1": 900.0,
          "x2": 767.0,
          "y2": 900.0,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "country_a",
          "kind": "circle",
          "x": 245,
          "y": 900,
          "radius": 70,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "country_b",
          "kind": "circle",
          "x": 835,
          "y": 900,
          "radius": 70,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "token",
          "kind": "circle",
          "x": 540,
          "y": 900,
          "radius": 50,
          "fill": "gold",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 6,
          "move_x": {
            "from": 365,
            "to": 715,
            "local_start": 18,
            "local_end": 120
          }
        },
        {
          "id": "dollar",
          "kind": "text",
          "text": "$",
          "x": 540,
          "y": 900,
          "size": 66,
          "color": "night",
          "group": "world",
          "delay": 6,
          "background": "gold",
          "container": "token",
          "move_x": {
            "from": 365,
            "to": 715,
            "local_start": 18,
            "local_end": 120
          }
        },
        {
          "id": "country_a_label",
          "kind": "text",
          "text": "COUNTRY A",
          "x": 245,
          "y": 1090,
          "size": 40,
          "color": "muted",
          "group": "world",
          "delay": 6,
          "background": "night"
        },
        {
          "id": "country_b_label",
          "kind": "text",
          "text": "COUNTRY B",
          "x": 835,
          "y": 1090,
          "size": 40,
          "color": "muted",
          "group": "world",
          "delay": 6,
          "background": "night"
        }
      ],
      "captions": [
        {
          "start": 0,
          "end": 165,
          "lines": [
            "Why might two countries trade in",
            "dollars when neither one issues"
          ]
        },
        {
          "start": 165,
          "end": 180,
          "lines": [
            "them?"
          ]
        }
      ],
      "caption_status": "PROVISIONAL: approximate visual-time pages, not aligned to recorded audio"
    },
    {
      "id": "02_definition",
      "start": 180,
      "end": 405,
      "camera": {
        "projection": "orthographic",
        "yaw": 0,
        "pitch": 0,
        "roll": 0,
        "screen_center": [
          540,
          960
        ],
        "zoom_anchor": [
          540,
          960
        ],
        "zoom_start": 1,
        "zoom_end": 1
      },
      "voiceover": "The dollar is the leading international currency, not the only one. It's widely used for trade invoicing, finance, and reserves.",
      "purpose": "Give the spoken and visible qualification; the euro and yen are illustrative examples, not an exhaustive list or scaled data.",
      "objects": [
        {
          "id": "heading",
          "kind": "text",
          "text": "LEADING. NOT ONLY.",
          "x": 540,
          "y": 320,
          "size": 66,
          "color": "ivory",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "subheading",
          "kind": "text",
          "text": "CURRENCIES COEXIST",
          "x": 540,
          "y": 430,
          "size": 40,
          "color": "muted",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "euro_node",
          "kind": "circle",
          "x": 260,
          "y": 810,
          "radius": 62,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "dollar_node",
          "kind": "circle",
          "x": 540,
          "y": 810,
          "radius": 78,
          "fill": "panel",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "yen_node",
          "kind": "circle",
          "x": 820,
          "y": 810,
          "radius": 62,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "euro",
          "kind": "text",
          "text": "€",
          "x": 260,
          "y": 810,
          "size": 72,
          "color": "ivory",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "euro_node"
        },
        {
          "id": "dollar",
          "kind": "text",
          "text": "$",
          "x": 540,
          "y": 810,
          "size": 90,
          "color": "gold",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "dollar_node"
        },
        {
          "id": "yen",
          "kind": "text",
          "text": "¥",
          "x": 820,
          "y": 810,
          "size": 72,
          "color": "ivory",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "yen_node"
        },
        {
          "id": "trade_card",
          "kind": "rect",
          "x": 105,
          "y": 1030,
          "w": 270,
          "h": 145,
          "radius": 22,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 12
        },
        {
          "id": "finance_card",
          "kind": "rect",
          "x": 405,
          "y": 1030,
          "w": 270,
          "h": 145,
          "radius": 22,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 22
        },
        {
          "id": "reserve_card",
          "kind": "rect",
          "x": 705,
          "y": 1030,
          "w": 270,
          "h": 145,
          "radius": 22,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 32
        },
        {
          "id": "trade",
          "kind": "text",
          "text": "INVOICING",
          "x": 240,
          "y": 1102,
          "size": 39,
          "color": "ivory",
          "group": "world",
          "delay": 12,
          "background": "panel",
          "container": "trade_card"
        },
        {
          "id": "finance",
          "kind": "text",
          "text": "FINANCE",
          "x": 540,
          "y": 1102,
          "size": 39,
          "color": "ivory",
          "group": "world",
          "delay": 22,
          "background": "panel",
          "container": "finance_card"
        },
        {
          "id": "reserves",
          "kind": "text",
          "text": "RESERVES",
          "x": 840,
          "y": 1102,
          "size": 38,
          "color": "ivory",
          "group": "world",
          "delay": 32,
          "background": "panel",
          "container": "reserve_card"
        }
      ],
      "captions": [
        {
          "start": 180,
          "end": 281,
          "lines": [
            "The dollar is the leading",
            "international currency, not the"
          ]
        },
        {
          "start": 281,
          "end": 394,
          "lines": [
            "only one. It's widely used for",
            "trade invoicing, finance, and"
          ]
        },
        {
          "start": 394,
          "end": 405,
          "lines": [
            "reserves."
          ]
        }
      ],
      "caption_status": "PROVISIONAL: approximate visual-time pages, not aligned to recorded audio"
    },
    {
      "id": "03_history",
      "start": 405,
      "end": 600,
      "camera": {
        "projection": "orthographic",
        "yaw": 0,
        "pitch": 0,
        "roll": 0,
        "screen_center": [
          540,
          960
        ],
        "zoom_anchor": [
          540,
          960
        ],
        "zoom_start": 1,
        "zoom_end": 1.01
      },
      "voiceover": "In 1944, Bretton Woods placed the dollar at the center of a new postwar monetary system.",
      "purpose": "Place the 1944 conference within a postwar framework; the dollar also had an earlier international role.",
      "objects": [
        {
          "id": "heading",
          "kind": "text",
          "text": "THE POSTWAR PLAN",
          "x": 540,
          "y": 320,
          "size": 66,
          "color": "ivory",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "subheading",
          "kind": "text",
          "text": "BRETTON WOODS",
          "x": 540,
          "y": 430,
          "size": 40,
          "color": "muted",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "history_card",
          "kind": "rect",
          "x": 150,
          "y": 760,
          "w": 780,
          "h": 310,
          "radius": 22,
          "fill": "panel",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "year",
          "kind": "text",
          "text": "1944",
          "x": 540,
          "y": 885,
          "size": 150,
          "color": "gold",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "history_card"
        },
        {
          "id": "history_note",
          "kind": "text",
          "text": "POSTWAR FRAMEWORK",
          "x": 540,
          "y": 1010,
          "size": 42,
          "color": "muted",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "history_card"
        }
      ],
      "captions": [
        {
          "start": 405,
          "end": 563,
          "lines": [
            "In 1944, Bretton Woods placed the",
            "dollar at the center of a new"
          ]
        },
        {
          "start": 563,
          "end": 600,
          "lines": [
            "postwar monetary system."
          ]
        }
      ],
      "caption_status": "PROVISIONAL: approximate visual-time pages, not aligned to recorded audio"
    },
    {
      "id": "04_gold",
      "start": 600,
      "end": 840,
      "camera": {
        "projection": "orthographic",
        "yaw": 0,
        "pitch": 0,
        "roll": 0,
        "screen_center": [
          540,
          960
        ],
        "zoom_anchor": [
          540,
          960
        ],
        "zoom_start": 1,
        "zoom_end": 1
      },
      "voiceover": "Participating countries tied their currencies to the dollar. The United States offered gold for dollars held by foreign central banks.",
      "purpose": "Show currency links while preserving the essential foreign-central-bank qualifier.",
      "objects": [
        {
          "id": "heading",
          "kind": "text",
          "text": "THE GOLD LINK",
          "x": 540,
          "y": 320,
          "size": 66,
          "color": "ivory",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "subheading",
          "kind": "text",
          "text": "FOREIGN CENTRAL BANKS",
          "x": 540,
          "y": 430,
          "size": 40,
          "color": "muted",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "left_link",
          "kind": "line",
          "x1": 355,
          "y1": 920,
          "x2": 415,
          "y2": 920,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "right_link",
          "kind": "line",
          "x1": 665,
          "y1": 920,
          "x2": 725,
          "y2": 920,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "other_box",
          "kind": "rect",
          "x": 100,
          "y": 830,
          "w": 255,
          "h": 180,
          "radius": 22,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "dollar_box",
          "kind": "rect",
          "x": 415,
          "y": 830,
          "w": 250,
          "h": 180,
          "radius": 22,
          "fill": "panel",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "gold_box",
          "kind": "rect",
          "x": 725,
          "y": 830,
          "w": 255,
          "h": 180,
          "radius": 22,
          "fill": "panel",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "other_first",
          "kind": "text",
          "text": "OTHER",
          "x": 227,
          "y": 895,
          "size": 40,
          "color": "ivory",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "other_box"
        },
        {
          "id": "other_second",
          "kind": "text",
          "text": "MONEY",
          "x": 227,
          "y": 950,
          "size": 40,
          "color": "ivory",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "other_box"
        },
        {
          "id": "usd",
          "kind": "text",
          "text": "$",
          "x": 540,
          "y": 920,
          "size": 85,
          "color": "gold",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "dollar_box"
        },
        {
          "id": "gold",
          "kind": "text",
          "text": "GOLD",
          "x": 852,
          "y": 920,
          "size": 43,
          "color": "gold",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "gold_box"
        },
        {
          "id": "qualifier",
          "kind": "text",
          "text": "FOREIGN CENTRAL BANKS",
          "x": 540,
          "y": 1190,
          "size": 42,
          "color": "muted",
          "group": "world",
          "delay": 6,
          "background": "night"
        }
      ],
      "captions": [
        {
          "start": 600,
          "end": 708,
          "lines": [
            "Participating countries tied their",
            "currencies to the dollar. The"
          ]
        },
        {
          "start": 708,
          "end": 828,
          "lines": [
            "United States offered gold for",
            "dollars held by foreign central"
          ]
        },
        {
          "start": 828,
          "end": 840,
          "lines": [
            "banks."
          ]
        }
      ],
      "caption_status": "PROVISIONAL: approximate visual-time pages, not aligned to recorded audio"
    },
    {
      "id": "05_suspension",
      "start": 840,
      "end": 1050,
      "camera": {
        "projection": "orthographic",
        "yaw": 0,
        "pitch": 0,
        "roll": 0,
        "screen_center": [
          540,
          960
        ],
        "zoom_anchor": [
          540,
          960
        ],
        "zoom_start": 1,
        "zoom_end": 1.01
      },
      "voiceover": "In 1971, the United States suspended gold conversion. The dollar's international role continued after the system changed.",
      "purpose": "Fade the gold-conversion link without claiming the entire Bretton Woods system ended in one day.",
      "objects": [
        {
          "id": "heading",
          "kind": "text",
          "text": "CONVERSION",
          "x": 540,
          "y": 320,
          "size": 66,
          "color": "ivory",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "subheading",
          "kind": "text",
          "text": "SUSPENDED IN 1971",
          "x": 540,
          "y": 430,
          "size": 40,
          "color": "muted",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "left_link",
          "kind": "line",
          "x1": 390,
          "y1": 910,
          "x2": 490,
          "y2": 910,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "middle_link",
          "kind": "line",
          "x1": 490,
          "y1": 910,
          "x2": 590,
          "y2": 910,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 6,
          "fade_out": [
            40,
            64
          ]
        },
        {
          "id": "right_link",
          "kind": "line",
          "x1": 590,
          "y1": 910,
          "x2": 690,
          "y2": 910,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "dollar_box",
          "kind": "rect",
          "x": 140,
          "y": 820,
          "w": 250,
          "h": 180,
          "radius": 22,
          "fill": "panel",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "gold_box",
          "kind": "rect",
          "x": 690,
          "y": 820,
          "w": 250,
          "h": 180,
          "radius": 22,
          "fill": "panel",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "dollar",
          "kind": "text",
          "text": "$",
          "x": 265,
          "y": 910,
          "size": 85,
          "color": "gold",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "dollar_box"
        },
        {
          "id": "gold",
          "kind": "text",
          "text": "GOLD",
          "x": 815,
          "y": 910,
          "size": 43,
          "color": "gold",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "gold_box"
        },
        {
          "id": "status",
          "kind": "text",
          "text": "OFFICIAL CONVERSION SUSPENDED",
          "x": 540,
          "y": 1185,
          "size": 40,
          "color": "muted",
          "group": "world",
          "delay": 6,
          "background": "night"
        }
      ],
      "captions": [
        {
          "start": 840,
          "end": 951,
          "lines": [
            "In 1971, the United States",
            "suspended gold conversion. The"
          ]
        },
        {
          "start": 951,
          "end": 1038,
          "lines": [
            "dollar's international role",
            "continued after the system"
          ]
        },
        {
          "start": 1038,
          "end": 1050,
          "lines": [
            "changed."
          ]
        }
      ],
      "caption_status": "PROVISIONAL: approximate visual-time pages, not aligned to recorded audio"
    },
    {
      "id": "06_economy",
      "start": 1050,
      "end": 1290,
      "camera": {
        "projection": "orthographic",
        "yaw": 0,
        "pitch": 0,
        "roll": 0,
        "screen_center": [
          540,
          960
        ],
        "zoom_anchor": [
          540,
          960
        ],
        "zoom_start": 1,
        "zoom_end": 1
      },
      "voiceover": "A large U.S. economy and deep Treasury markets support the dollar, while widespread trade invoicing gives people reasons to use it.",
      "purpose": "State the supporting factors without numerical or causal overclaim.",
      "objects": [
        {
          "id": "heading",
          "kind": "text",
          "text": "WHY IT CONTINUED",
          "x": 540,
          "y": 320,
          "size": 66,
          "color": "ivory",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "subheading",
          "kind": "text",
          "text": "SCALE + LIQUID MARKETS",
          "x": 540,
          "y": 430,
          "size": 40,
          "color": "muted",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "economy_card",
          "kind": "rect",
          "x": 140,
          "y": 735,
          "w": 800,
          "h": 140,
          "radius": 22,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "market_card",
          "kind": "rect",
          "x": 140,
          "y": 920,
          "w": 800,
          "h": 140,
          "radius": 22,
          "fill": "panel",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 20
        },
        {
          "id": "trade_card",
          "kind": "rect",
          "x": 140,
          "y": 1105,
          "w": 800,
          "h": 140,
          "radius": 22,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 34
        },
        {
          "id": "economy",
          "kind": "text",
          "text": "LARGE U.S. ECONOMY",
          "x": 540,
          "y": 805,
          "size": 43,
          "color": "ivory",
          "group": "world",
          "delay": 6,
          "background": "panel",
          "container": "economy_card"
        },
        {
          "id": "market",
          "kind": "text",
          "text": "DEEP TREASURY MARKETS",
          "x": 540,
          "y": 990,
          "size": 43,
          "color": "gold",
          "group": "world",
          "delay": 20,
          "background": "panel",
          "container": "market_card"
        },
        {
          "id": "trade",
          "kind": "text",
          "text": "TRADE INVOICING",
          "x": 540,
          "y": 1175,
          "size": 43,
          "color": "ivory",
          "group": "world",
          "delay": 34,
          "background": "panel",
          "container": "trade_card"
        }
      ],
      "captions": [
        {
          "start": 1050,
          "end": 1164,
          "lines": [
            "A large U.S. economy and deep",
            "Treasury markets support the"
          ]
        },
        {
          "start": 1164,
          "end": 1267,
          "lines": [
            "dollar, while widespread trade",
            "invoicing gives people reasons to"
          ]
        },
        {
          "start": 1267,
          "end": 1290,
          "lines": [
            "use it."
          ]
        }
      ],
      "caption_status": "PROVISIONAL: approximate visual-time pages, not aligned to recorded audio"
    },
    {
      "id": "07_network",
      "start": 1290,
      "end": 1530,
      "camera": {
        "projection": "orthographic",
        "yaw": 0,
        "pitch": 0,
        "roll": 0,
        "screen_center": [
          540,
          960
        ],
        "zoom_anchor": [
          540,
          960
        ],
        "zoom_start": 1,
        "zoom_end": 1.01
      },
      "voiceover": "As more people use dollars, others may find them easier to use. That network effect can reinforce the dollar's role.",
      "purpose": "First show two connected participants; then reveal a new user and two new links. The animation illustrates a mechanism, not data or causal proof.",
      "objects": [
        {
          "id": "heading",
          "kind": "text",
          "text": "USE REINFORCES USE",
          "x": 540,
          "y": 320,
          "size": 66,
          "color": "ivory",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "subheading",
          "kind": "text",
          "text": "AN ILLUSTRATIVE MODEL",
          "x": 540,
          "y": 430,
          "size": 40,
          "color": "muted",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "hub_left",
          "kind": "line",
          "x1": 475.27,
          "y1": 818.52,
          "x2": 293.15,
          "y2": 940.98,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 16
        },
        {
          "id": "hub_right",
          "kind": "line",
          "x1": 604.73,
          "y1": 818.52,
          "x2": 786.85,
          "y2": 940.98,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 16
        },
        {
          "id": "existing_peers",
          "kind": "line",
          "x1": 302.0,
          "y1": 970.0,
          "x2": 778.0,
          "y2": 970.0,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 26
        },
        {
          "id": "new_to_left",
          "kind": "line",
          "x1": 497.88,
          "y1": 1149.5,
          "x2": 292.12,
          "y2": 1000.5,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 96
        },
        {
          "id": "new_to_right",
          "kind": "line",
          "x1": 582.12,
          "y1": 1149.5,
          "x2": 787.88,
          "y2": 1000.5,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 96
        },
        {
          "id": "new_to_hub",
          "kind": "line",
          "x1": 540.0,
          "y1": 853.0,
          "x2": 540.0,
          "y2": 1128.0,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 96
        },
        {
          "id": "hub",
          "kind": "circle",
          "x": 540,
          "y": 775,
          "radius": 80,
          "fill": "gold",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "hub_dollar",
          "kind": "text",
          "text": "$",
          "x": 540,
          "y": 775,
          "size": 92,
          "color": "night",
          "group": "world",
          "delay": 6,
          "background": "gold",
          "container": "hub"
        },
        {
          "id": "left_node",
          "kind": "circle",
          "x": 250,
          "y": 970,
          "radius": 54,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 16
        },
        {
          "id": "right_node",
          "kind": "circle",
          "x": 830,
          "y": 970,
          "radius": 54,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 16
        },
        {
          "id": "new_node",
          "kind": "circle",
          "x": 540,
          "y": 1180,
          "radius": 54,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 96
        },
        {
          "id": "bank_label",
          "kind": "text",
          "text": "BANKS",
          "x": 250,
          "y": 1080,
          "size": 40,
          "color": "muted",
          "group": "world",
          "delay": 16,
          "background": "night"
        },
        {
          "id": "business_label",
          "kind": "text",
          "text": "BUSINESSES",
          "x": 830,
          "y": 1080,
          "size": 40,
          "color": "muted",
          "group": "world",
          "delay": 16,
          "background": "night"
        },
        {
          "id": "new_label",
          "kind": "text",
          "text": "NEW USER",
          "x": 540,
          "y": 1290,
          "size": 40,
          "color": "muted",
          "group": "world",
          "delay": 96,
          "background": "night"
        },
        {
          "id": "model_note",
          "kind": "text",
          "text": "USE CAN GET EASIER",
          "x": 540,
          "y": 1380,
          "size": 44,
          "color": "ivory",
          "group": "world",
          "delay": 110,
          "background": "night"
        }
      ],
      "captions": [
        {
          "start": 1290,
          "end": 1422,
          "lines": [
            "As more people use dollars,",
            "others may find them easier to"
          ]
        },
        {
          "start": 1422,
          "end": 1530,
          "lines": [
            "use. That network effect can",
            "reinforce the dollar's role."
          ]
        }
      ],
      "caption_status": "PROVISIONAL: approximate visual-time pages, not aligned to recorded audio"
    },
    {
      "id": "08_answer",
      "start": 1530,
      "end": 1800,
      "camera": {
        "projection": "orthographic",
        "yaw": 0,
        "pitch": 0,
        "roll": 0,
        "screen_center": [
          540,
          960
        ],
        "zoom_anchor": [
          540,
          960
        ],
        "zoom_start": 1,
        "zoom_end": 1
      },
      "voiceover": "So those two countries can choose dollars because they already have access to a widely used system. Other currencies can work too.",
      "purpose": "Return to the same two parties and directly answer the opening; retain non-exclusivity.",
      "objects": [
        {
          "id": "heading",
          "kind": "text",
          "text": "WHY THEY CHOOSE $",
          "x": 540,
          "y": 320,
          "size": 66,
          "color": "ivory",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "subheading",
          "kind": "text",
          "text": "COMMON ACCESS, NOT A RULE",
          "x": 540,
          "y": 430,
          "size": 40,
          "color": "muted",
          "group": "screen",
          "delay": 0,
          "background": "night"
        },
        {
          "id": "route",
          "kind": "line",
          "x1": 313.0,
          "y1": 900.0,
          "x2": 767.0,
          "y2": 900.0,
          "color": "line",
          "stroke_width": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "country_a",
          "kind": "circle",
          "x": 245,
          "y": 900,
          "radius": 70,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "country_b",
          "kind": "circle",
          "x": 835,
          "y": 900,
          "radius": 70,
          "fill": "panel",
          "stroke": "line",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "token",
          "kind": "circle",
          "x": 715,
          "y": 900,
          "radius": 50,
          "fill": "gold",
          "stroke": "gold",
          "stroke_width": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "dollar",
          "kind": "text",
          "text": "$",
          "x": 715,
          "y": 900,
          "size": 66,
          "color": "night",
          "group": "world",
          "delay": 6,
          "background": "gold",
          "container": "token"
        },
        {
          "id": "country_a_label",
          "kind": "text",
          "text": "COUNTRY A",
          "x": 245,
          "y": 1090,
          "size": 40,
          "color": "muted",
          "group": "world",
          "delay": 6,
          "background": "night"
        },
        {
          "id": "country_b_label",
          "kind": "text",
          "text": "COUNTRY B",
          "x": 835,
          "y": 1090,
          "size": 40,
          "color": "muted",
          "group": "world",
          "delay": 6,
          "background": "night"
        },
        {
          "id": "answer",
          "kind": "text",
          "text": "BOTH CAN USE ONE SYSTEM",
          "x": 540,
          "y": 1240,
          "size": 43,
          "color": "ivory",
          "group": "world",
          "delay": 6,
          "background": "night"
        },
        {
          "id": "other",
          "kind": "text",
          "text": "OTHER CURRENCIES CAN WORK TOO",
          "x": 540,
          "y": 1330,
          "size": 40,
          "color": "muted",
          "group": "world",
          "delay": 6,
          "background": "night"
        }
      ],
      "captions": [
        {
          "start": 1530,
          "end": 1665,
          "lines": [
            "So those two countries can choose",
            "dollars because they already have"
          ]
        },
        {
          "start": 1665,
          "end": 1800,
          "lines": [
            "access to a widely used system.",
            "Other currencies can work too."
          ]
        }
      ],
      "caption_status": "PROVISIONAL: approximate visual-time pages, not aligned to recorded audio"
    }
  ]
}
```
