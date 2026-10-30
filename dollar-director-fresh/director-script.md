# Why is the dollar a world currency?
## A fresh 60-second code-only Director script

**Scope:** This is a new plan, written from the brief using the improved Social Video & Motion Design Director skill. It is not a finished video. Its visual plan uses only code-drawn typography and geometric primitives—no image or video inputs.

### Brief
- **Confirmed:** 60-second subject explainer; code-only visuals; no images or videos used as inputs; frame-level direction.
- **Proposed, not confirmed:** English narration, general audience, vertical 1080 × 1920, 30 fps, 1,800 frames. The intended platform and actual overlay safe areas are unknown. Change the plan if the delivery format differs.
- **Promise:** Explain why the dollar is widely used internationally without suggesting it is the only currency or that its position is guaranteed.
- **Creative concept:** A single dollar token moves through a clean editorial diagram; history explains how it became central, a broken link marks the suspension of gold conversion, and a connected network explains why the dollar remains useful. Euro, yen and other nodes are illustrative, not exhaustive or proportional data.
- **Hook choice:** Recommended: “Why would two countries trade using a currency neither one issues?” Alternative: “The dollar lost its gold link. Why did the world keep using it?” The recommended hook establishes the viewer’s question before the historical answer.
- **Open decisions:** Platform and placement, narrator, final audio/caption delivery, and platform-specific safe areas. Draft caption timing is not synchronized to a recording.

## Strict production rules
1. **No visual media inputs:** no photos, screenshots, footage, stock clips, bitmap textures, external SVG images or generated-image assets. Draw only text, solid-color rounded rectangles, circles and lines in code. The QA contact sheet is an output, not an input. Licensed font files are allowed.
2. The `visual-plan.json` manifest is provided separately and embedded in full at the end of this document. It specifies every object, group, coordinate, visual frame interval, camera transform and provisional caption cue. The two copies are generated together and must remain identical.
3. Every visual frame is a deterministic function of the frame number and fixed inputs. No wall-clock timing, unseeded randomness or playback-history state. Scene boundaries are 0-based, start-inclusive and end-exclusive.
4. Draw at the proposed 1080 × 1920 and 30 fps. Screen center and zoom anchor are both `(540,960)`. All cameras are front-facing orthographic, yaw/pitch/roll `0°`; they are virtual 2D transforms, not video footage or a physical camera.
5. Heading and subheading are **screen-fixed** objects, entry delay 0, unaffected by the world camera. Diagram graphics are world objects; their individual delays and camera transforms are in the manifest. Captions are screen-fixed.
6. No invented statistics, real product UI, real transaction data or claims of exclusive dollar use. Use the supplied source links. The currency symbols and network do not represent measured shares, actual counterparties or all currencies.
7. The 1,800-frame visual timeline is exact only for the assumed format. Voice timing, caption sync, final playback and platform safety are **not verified**. Record the voice, realign caption cues, then verify the 60-second total and every delivery format.

## Narrative and full voiceover

**1. Hook** — Why would two countries trade using a currency neither one issues?

**2. Definition** — The dollar is the leading international currency, used in trade invoicing, finance, and central bank reserves.

**3. History** — In 1944, Bretton Woods placed the dollar at the center of the postwar monetary system.

**4. Gold Link** — Participating countries tied their currencies to the dollar, while the U.S. promised gold for dollars held by foreign central banks.

**5. 1971** — In 1971, the United States suspended that gold conversion. Yet the dollar's global role continued.

**6. Reasons** — A large U.S. economy and deep Treasury markets help support the dollar. It is also widely used for trade invoicing.

**7. Network** — When banks and businesses already use dollars, others can find it easier to use them too. That reinforces the network.

**8. Payoff** — The dollar is not the only international currency, and its lead isn't guaranteed. Its advantage rests on history, markets, and widespread use.

The text has an estimated 141 word tokens. Pronunciations of years and initials can take longer; no recording was measured. The lines are intended for one natural, clear narrator, not a rapid advertisement read.

## Timing, camera and story beats
| Scene | Time | Frames `[start,end)` | Camera zoom | What the viewer sees and learns |
|---|---|---|---|---|
| 01_hook | 00:00.000–00:06.000 | [0, 180) | 1.000 → 1.020 | A dollar token travels between two illustrative countries, making the hook visible. |
| 02_definition | 00:06.000–00:13.000 | [180, 390) | 1.000 → 1.000 | The dollar appears alongside other currency examples and three areas of international use. |
| 03_history | 00:13.000–00:20.000 | [390, 600) | 1.000 → 1.020 | A 1944 card establishes the Bretton Woods historical starting point. |
| 04_gold_link | 00:20.000–00:28.000 | [600, 840) | 1.000 → 1.000 | Other currencies, the dollar and gold connect; a label limits the gold conversion to central banks. |
| 05_1971 | 00:28.000–00:35.000 | [840, 1050) | 1.000 → 1.020 | The center gold-conversion link fades out; the dollar remains visible. |
| 06_reasons | 00:35.000–00:43.000 | [1050, 1290) | 1.000 → 1.000 | Three explicit cards identify the U.S. economy, Treasury markets and trade invoicing. |
| 07_network | 00:43.000–00:51.000 | [1290, 1530) | 1.000 → 1.020 | Banks, businesses and investors connect to a dollar hub in stages; nodes are illustrative. |
| 08_payoff | 00:51.000–01:00.000 | [1530, 1800) | 1.000 → 1.020 | Other currencies coexist around the dollar; the ending returns to the main answer. |

## Frame-state contract
For every frame `f` from 0 through 1799, select the scene with `start ≤ f < end`; set `local = f − start` and `D = end − start`. Fill the background with `#101B2B`. Use `smooth(x)=u²(3−2u)`, where `u=clamp(x,0,1)`.

- **Opacity:** Screen objects default to delay 0 and world objects to delay 6 unless their `delay` field says otherwise. `opacity=smooth((local−delay)/18)`. If `fade_out=[a,b]`, multiply by `1−smooth((local−a)/(b−a))`. There is no entry position shift.
- **Camera:** `zoom=z0+(z1−z0)×smooth(local/(D−1))`. Apply it to world points around `(540,960)`: `(540+(x−540)×zoom, 960+(y−960)×zoom)`. Scale world sizes, stroke widths and world text sizes accordingly. Screen headings, subheadings and captions do not zoom. Angles are fixed at zero.
- **Token motion:** For the two objects carrying `x_motion`, use `x=380+320×smooth((local−24)/96)` before world-camera projection. Both stay aligned. The 1971 center link fades between local frames 42 and 66. Network lines start inside the relevant nodes and share the same camera transformation; they are drawn behind the nodes.
- **Layering:** Background → world objects in manifest order → screen objects in manifest order → caption panel and text. Standard source-over alpha. Rectangles use top-left positions; circles and text use centers. Round scaled text sizes and stroke widths to the nearest pixel.
- **Captions:** Draw the current draft cue in a screen-fixed panel at `(70,1510)`, size `940 × 180`, radius 24. Font is 42 px DejaVu Sans Bold. One line is centered at `(540,1600)`; two lines at `(540,1568)` and `(540,1635)`. **Platform-safe area: NOT VERIFIED.** Copy and layout are specified; cue times are provisional and must be aligned with the final recorded audio.
- **Font:** DejaVu Sans Bold from a valid licensed font file; the test used `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`. Any substitute changes font metrics and requires renewed layout testing.

**Palette:** `night #101B2B`, `surface #1C2D40`, `ivory #F7F4EC`, `slate #C3CED7`, `gold #EAC777`.

## Complete scene instructions
The rows are base positions; apply the frame-state contract above. The full embedded manifest resolves every property and exact caption interval.

### 01_hook — frames [0, 180)
**Voiceover:** “Why would two countries trade using a currency neither one issues?”

| Object | Direction | Group / timing |
|---|---|---|
| heading | Text **WHY THE DOLLAR?**, center (540, 330), 68 px, `ivory` | screen; delay 0 |
| subheading | Text **A SHARED CURRENCY**, center (540, 440), 40 px, `slate` | screen; delay 0 |
| trade_path | Line (320, 900) → (760, 900), `slate`, 4 px | world; delay 6 |
| country_a | Circle center (250, 900), radius 70, fill `surface`, outline `slate`, 3 px | world; delay 6 |
| country_b | Circle center (830, 900), radius 70, fill `surface`, outline `slate`, 3 px | world; delay 6 |
| dollar_token | Circle center (540, 900), radius 50, fill `gold`, outline `gold`, 3 px | world; delay 6; x-motion local 24–120 |
| dollar_mark | Text **$**, center (540, 900), 67 px, `night` | world; delay 6; x-motion local 24–120 |
| country_a_label | Text **COUNTRY A**, center (250, 1090), 40 px, `slate` | world; delay 6 |
| country_b_label | Text **COUNTRY B**, center (830, 1090), 40 px, `slate` | world; delay 6 |

**Draft caption pages—timing not yet aligned to audio:**
- Frames `[0, 90)`: “Why would two countries trade” / “using a currency”
- Frames `[90, 180)`: “neither one issues?”

### 02_definition — frames [180, 390)
**Voiceover:** “The dollar is the leading international currency, used in trade invoicing, finance, and central bank reserves.”

| Object | Direction | Group / timing |
|---|---|---|
| heading | Text **A GLOBAL TOOL**, center (540, 330), 68 px, `ivory` | screen; delay 0 |
| subheading | Text **LEADING, NOT THE ONLY ONE**, center (540, 440), 40 px, `slate` | screen; delay 0 |
| euro_node | Circle center (265, 840), radius 60, fill `surface`, outline `slate`, 3 px | world; delay 6 |
| yen_node | Circle center (815, 840), radius 60, fill `surface`, outline `slate`, 3 px | world; delay 6 |
| euro | Text **€**, center (265, 840), 60 px, `slate` | world; delay 6 |
| dollar | Text **$**, center (540, 840), 150 px, `gold` | world; delay 6 |
| yen | Text **¥**, center (815, 840), 60 px, `slate` | world; delay 6 |
| card_a | Rounded rectangle at (110, 1010), size (275, 135), corner radius 24, fill `surface`, outline `slate`, 3 px | world; delay 10 |
| card_b | Rounded rectangle at (403, 1010), size (275, 135), corner radius 24, fill `surface`, outline `slate`, 3 px | world; delay 20 |
| card_c | Rounded rectangle at (695, 1010), size (275, 135), corner radius 24, fill `surface`, outline `slate`, 3 px | world; delay 30 |
| trade | Text **INVOICING**, center (247, 1077), 38 px, `ivory` | world; delay 10 |
| finance | Text **FINANCE**, center (540, 1077), 38 px, `ivory` | world; delay 20 |
| reserves | Text **RESERVES**, center (833, 1077), 38 px, `ivory` | world; delay 30 |

**Draft caption pages—timing not yet aligned to audio:**
- Frames `[180, 285)`: “The dollar is the leading” / “international currency,”
- Frames `[285, 390)`: “used in trade invoicing, finance,” / “and central bank reserves.”

### 03_history — frames [390, 600)
**Voiceover:** “In 1944, Bretton Woods placed the dollar at the center of the postwar monetary system.”

| Object | Direction | Group / timing |
|---|---|---|
| heading | Text **A POSTWAR SYSTEM**, center (540, 330), 68 px, `ivory` | screen; delay 0 |
| subheading | Text **BRETTON WOODS**, center (540, 440), 40 px, `slate` | screen; delay 0 |
| history_card | Rounded rectangle at (150, 760), size (780, 330), corner radius 24, fill `surface`, outline `gold`, 3 px | world; delay 6 |
| year | Text **1944**, center (540, 890), 155 px, `gold` | world; delay 6 |
| history_label | Text **POSTWAR FRAMEWORK**, center (540, 1030), 40 px, `slate` | world; delay 6 |

**Draft caption pages—timing not yet aligned to audio:**
- Frames `[390, 495)`: “In 1944, Bretton Woods placed” / “the dollar at the center”
- Frames `[495, 600)`: “of the postwar” / “monetary system.”

### 04_gold_link — frames [600, 840)
**Voiceover:** “Participating countries tied their currencies to the dollar, while the U.S. promised gold for dollars held by foreign central banks.”

| Object | Direction | Group / timing |
|---|---|---|
| heading | Text **DOLLARS AND GOLD**, center (540, 330), 68 px, `ivory` | screen; delay 0 |
| subheading | Text **THE BRETTON WOODS SYSTEM**, center (540, 440), 40 px, `slate` | screen; delay 0 |
| left_connector | Line (355, 925) → (420, 925), `slate`, 4 px | world; delay 6 |
| right_connector | Line (660, 925) → (725, 925), `slate`, 4 px | world; delay 6 |
| currencies_card | Rounded rectangle at (100, 830), size (255, 190), corner radius 24, fill `surface`, outline `slate`, 3 px | world; delay 6 |
| usd_card | Rounded rectangle at (420, 830), size (240, 190), corner radius 24, fill `surface`, outline `gold`, 3 px | world; delay 6 |
| gold_card | Rounded rectangle at (725, 830), size (255, 190), corner radius 24, fill `surface`, outline `gold`, 3 px | world; delay 6 |
| currency1 | Text **OTHER**, center (227, 905), 40 px, `ivory` | world; delay 6 |
| currency2 | Text **MONEY**, center (227, 960), 40 px, `ivory` | world; delay 6 |
| usd | Text **$**, center (540, 925), 90 px, `gold` | world; delay 6 |
| gold | Text **GOLD**, center (852, 925), 45 px, `gold` | world; delay 6 |
| officials | Text **FOR CENTRAL BANKS**, center (540, 1190), 40 px, `slate` | world; delay 6 |

**Draft caption pages—timing not yet aligned to audio:**
- Frames `[600, 720)`: “Participating countries tied” / “their currencies to the dollar, while”
- Frames `[720, 840)`: “the U.S. promised gold for dollars” / “held by foreign central banks.”

### 05_1971 — frames [840, 1050)
**Voiceover:** “In 1971, the United States suspended that gold conversion. Yet the dollar's global role continued.”

| Object | Direction | Group / timing |
|---|---|---|
| heading | Text **GOLD WINDOW CLOSES**, center (540, 330), 68 px, `ivory` | screen; delay 0 |
| subheading | Text **1971**, center (540, 440), 40 px, `slate` | screen; delay 0 |
| left_connector | Line (390, 920) → (490, 920), `slate`, 4 px | world; delay 6 |
| break_link | Line (490, 920) → (590, 920), `slate`, 4 px | world; delay 6; fade-out local 42–66 |
| right_connector | Line (590, 920) → (690, 920), `slate`, 4 px | world; delay 6 |
| dollar_panel | Rounded rectangle at (140, 830), size (250, 180), corner radius 24, fill `surface`, outline `gold`, 3 px | world; delay 6 |
| gold_panel | Rounded rectangle at (690, 830), size (250, 180), corner radius 24, fill `surface`, outline `gold`, 3 px | world; delay 6 |
| dollar | Text **$**, center (265, 920), 90 px, `gold` | world; delay 6 |
| gold | Text **GOLD**, center (815, 920), 44 px, `gold` | world; delay 6 |
| status | Text **CONVERSION SUSPENDED**, center (540, 1195), 42 px, `ivory` | world; delay 6 |

**Draft caption pages—timing not yet aligned to audio:**
- Frames `[840, 945)`: “In 1971, the United States” / “suspended that gold conversion.”
- Frames `[945, 1050)`: “Yet the dollar's global role” / “continued.”

### 06_reasons — frames [1050, 1290)
**Voiceover:** “A large U.S. economy and deep Treasury markets help support the dollar. It is also widely used for trade invoicing.”

| Object | Direction | Group / timing |
|---|---|---|
| heading | Text **WHY DID IT LAST?**, center (540, 330), 68 px, `ivory` | screen; delay 0 |
| subheading | Text **SCALE AND MARKET DEPTH**, center (540, 440), 40 px, `slate` | screen; delay 0 |
| economy_card | Rounded rectangle at (145, 740), size (790, 140), corner radius 24, fill `surface`, outline `slate`, 3 px | world; delay 6 |
| treasury_card | Rounded rectangle at (145, 930), size (790, 140), corner radius 24, fill `surface`, outline `gold`, 3 px | world; delay 18 |
| trade_card | Rounded rectangle at (145, 1120), size (790, 140), corner radius 24, fill `surface`, outline `slate`, 3 px | world; delay 30 |
| economy | Text **LARGE U.S. ECONOMY**, center (540, 810), 44 px, `ivory` | world; delay 6 |
| treasury | Text **DEEP TREASURY MARKETS**, center (540, 1000), 44 px, `gold` | world; delay 18 |
| invoicing | Text **TRADE INVOICING**, center (540, 1190), 44 px, `ivory` | world; delay 30 |

**Draft caption pages—timing not yet aligned to audio:**
- Frames `[1050, 1170)`: “A large U.S. economy” / “and deep Treasury markets”
- Frames `[1170, 1290)`: “help support the dollar. It is also” / “widely used for trade invoicing.”

### 07_network — frames [1290, 1530)
**Voiceover:** “When banks and businesses already use dollars, others can find it easier to use them too. That reinforces the network.”

| Object | Direction | Group / timing |
|---|---|---|
| heading | Text **THE NETWORK EFFECT**, center (540, 330), 68 px, `ivory` | screen; delay 0 |
| subheading | Text **USE CAN REINFORCE USE**, center (540, 440), 40 px, `slate` | screen; delay 0 |
| left_link | Line (470.57, 875.49) → (294.33, 990.95), `slate`, 4 px | world; delay 22 |
| right_link | Line (609.43, 875.49) → (785.67, 990.95), `slate`, 4 px | world; delay 38 |
| bottom_link | Line (540.0, 913.0) → (540.0, 1137.0), `slate`, 4 px | world; delay 54 |
| hub | Circle center (540, 830), radius 85, fill `gold`, outline `gold`, 3 px | world; delay 6 |
| hub_dollar | Text **$**, center (540, 830), 104 px, `night` | world; delay 6 |
| left_node | Circle center (250, 1020), radius 55, fill `surface`, outline `slate`, 3 px | world; delay 22 |
| right_node | Circle center (830, 1020), radius 55, fill `surface`, outline `slate`, 3 px | world; delay 38 |
| bottom_node | Circle center (540, 1190), radius 55, fill `surface`, outline `slate`, 3 px | world; delay 54 |
| banks | Text **BANKS**, center (250, 1135), 40 px, `slate` | world; delay 22 |
| businesses | Text **BUSINESSES**, center (830, 1135), 40 px, `slate` | world; delay 38 |
| investors | Text **INVESTORS**, center (540, 1300), 40 px, `slate` | world; delay 54 |

**Draft caption pages—timing not yet aligned to audio:**
- Frames `[1290, 1410)`: “When banks and businesses” / “already use dollars, others can”
- Frames `[1410, 1530)`: “find it easier to use them too.” / “That reinforces the network.”

### 08_payoff — frames [1530, 1800)
**Voiceover:** “The dollar is not the only international currency, and its lead isn't guaranteed. Its advantage rests on history, markets, and widespread use.”

| Object | Direction | Group / timing |
|---|---|---|
| heading | Text **LEADING. NOT ONLY.**, center (540, 330), 68 px, `ivory` | screen; delay 0 |
| subheading | Text **AN EVOLVING SYSTEM**, center (540, 440), 40 px, `slate` | screen; delay 0 |
| euro_link | Line (424.45, 923.91) → (308.76, 947.84), `slate`, 4 px | world; delay 6 |
| yen_link | Line (655.55, 923.91) → (771.24, 947.84), `slate`, 4 px | world; delay 6 |
| other_link | Line (540.0, 1018.0) → (540.0, 1126.0), `slate`, 4 px | world; delay 6 |
| euro_node | Circle center (250, 960), radius 62, fill `surface`, outline `slate`, 3 px | world; delay 6 |
| yen_node | Circle center (830, 960), radius 62, fill `surface`, outline `slate`, 3 px | world; delay 6 |
| other_node | Circle center (540, 1170), radius 46, fill `surface`, outline `slate`, 3 px | world; delay 6 |
| euro | Text **€**, center (250, 960), 64 px, `slate` | world; delay 6 |
| yen | Text **¥**, center (830, 960), 64 px, `slate` | world; delay 6 |
| hub | Circle center (540, 900), radius 120, fill `surface`, outline `gold`, 3 px | world; delay 6 |
| dollar | Text **$**, center (540, 900), 145 px, `gold` | world; delay 6 |
| conclusion | Text **HISTORY + MARKETS + USE**, center (540, 1335), 42 px, `ivory` | world; delay 6 |

**Draft caption pages—timing not yet aligned to audio:**
- Frames `[1530, 1605)`: “The dollar is not the only” / “international currency,”
- Frames `[1605, 1675)`: “and its lead isn't guaranteed.”
- Frames `[1675, 1800)`: “Its advantage rests on history,” / “markets, and widespread use.”

## Audio and accessibility
- Narration: one clear, unhurried voice. The script is a target, not a recorded or timed performance. Record and align it before locking captions and dependent movements.
- Music and effects: optional, understated and separately sourced or synthesized with permission; none are required to understand the story. No music or narration has been produced or mixed. Caption meaningful non-speech sounds if they are added.
- After rendering, review captions and actual backgrounds at the intended viewing size, check current platform UI overlays, provide visual description or a descriptive transcript where needed, and check applicable contrast and flashing guidance. The draft coordinates are not a platform-safety certification.

## Test and review status
- **PASS, visual timeline math only:** the eight planned intervals cover 1,800 frames, exactly 60 seconds at the proposed 30 fps.
- **PASS, selected layout checks only:** all 1,800 planned frames were checked for composition bounds, text-to-text bounding-box overlaps, selected text inside its card and draft-caption coverage/bounds. No issues remained. This is not an exhaustive all-object collision check.
- **PASS, planned graph topology:** endpoints of the network and payoff links fall inside their intended node outlines in world space; they share the same camera transform and no entry shift. This does not establish full-motion visual quality.
- **PASS, draft copy:** caption pages reproduce the planned narration. Their alignment to real speech is not checked.
- **PASS, nominal flat-color calculations:** ivory/night 15.74:1; slate/night 10.82:1. This does not prove readability or accessibility throughout fades.
- **Test defects found and fixed:** The first layout check found a history-card label too wide and three caption lines outside the planned text area. The label was shortened and the caption lines reflowed; the selected checks then passed.
- **NOT CHECKED:** a finished video, natural voice duration, caption synchronization, full-motion playback, audio mix, human comprehension, viewer retention, real-device readability and platform overlays. The contact sheet samples stills only.

## Fact sources
- [Federal Reserve: International Role of the U.S. Dollar, 2025](https://www.federalreserve.gov/econres/notes/feds-notes/the-international-role-of-the-u-s-dollar-2025-edition-20250718.html): international role, economic scale and market depth. The dollar had an international role before 1944.
- [IMF: Central Banks and the Bretton Woods Gold Puzzle](https://www.imf.org/-/media/files/publications/wp/2019/wpiea2019161.pdf): the 1944 framework and U.S. gold conversion for foreign central banks.
- [U.S. State Department: Nixon and the End of Bretton Woods](https://history.state.gov/milestones/1969-1976/nixon-shock): suspension of gold convertibility in 1971 and the broader system’s unraveling over 1971–1973.
- [BIS: Global reach of currencies](https://www.bis.org/publ/qtrpdf/r_qt2406b.htm) and [global FX markets](https://www.bis.org/publications/qr-202212/global-foreign-exchange-market-higher-volatility-environment): international dollar use and trade invoicing.
- [IMF: The Dollar’s Primacy](https://www.imf.org/en/publications/fandd/issues/2022/03/book-review-dollar-primacy-joyce): market depth and network effects; these factors do not guarantee permanent dominance.

## Embedded authoritative visual-plan.json
This is the full [separate visual-plan.json](visual-plan.json), included here so the script is usable on its own. SHA-256 of the UTF-8 JSON file: `e20aaea5c37af01e592ea1a768dbe460040f899eb61280e4b9accee19dce98f2`.
```json
{
  "project": "Why the dollar is a leading world currency",
  "brief": {
    "confirmed": [
      "60-second script",
      "no source images or video; code-drawn visuals only"
    ],
    "assumptions": [
      "English",
      "general audience",
      "9:16, 1080 x 1920",
      "30 fps",
      "vertical social viewing"
    ],
    "unverified": [
      "target platform and UI-safe areas",
      "audio delivery and voice",
      "final captions and their timing"
    ]
  },
  "format": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "frame_count": 1800,
    "interval_convention": "zero-based, start inclusive and end exclusive"
  },
  "palette": {
    "night": "#101B2B",
    "surface": "#1C2D40",
    "ivory": "#F7F4EC",
    "slate": "#C3CED7",
    "gold": "#EAC777"
  },
  "font": {
    "face": "DejaVu Sans Bold",
    "path_for_reference_test": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "fallback": "approval and retesting required"
  },
  "restrictions": [
    "No still-image, video, SVG, generated-image, photo, stock or texture input.",
    "Only code-drawn solid rectangles, circles, lines and text; font files allowed.",
    "No numerical or area-proportional claim; symbols are illustrative and not exhaustive."
  ],
  "render_rules": {
    "coordinates": "top-left origin, x right and y down; rectangles use top-left; circles and text use center",
    "scene": "Select exactly one scene with start <= frame < end. Hard cuts; background fills full frame.",
    "ease": "u=clamp(t,0,1); smooth(t)=u*u*(3-2*u)",
    "object_opacity": "local=frame-scene_start; default delay=0 for screen objects, 6 for world objects; opacity=smooth((local-delay)/18). If fade_out [a,b] is present multiply opacity by 1-smooth((local-a)/(b-a)). No entry-position shift.",
    "motion": "If x_motion exists, replace the base x of the circle center or text center with from+(to-from)*smooth((local-local_start)/(local_end-local_start)). Other coordinates remain unchanged.",
    "camera": "For local in [0,duration-1], zoom=z0+(z1-z0)*smooth(local/(duration-1)). Transform world points around the explicit zoom_anchor: (ax+(x-ax)*zoom, ay+(y-ay)*zoom); scale world sizes, line widths and world font sizes by zoom. Screen heading/subheading and captions are not camera-transformed. All camera angles remain zero.",
    "compositing": "background, world objects in listed order, screen objects in listed order, captions. Source-over compositing. Source colors and stroke widths are in the objects; round scaled font size and stroke width to nearest pixel.",
    "captions": "Draft caption timing only: at each frame choose the scene cue whose interval contains it. Draw panel x=70,y=1510,w=940,h=180,r=24, surface fill. DejaVu Sans Bold 42 px ivory centered x=540. One line center y=1600; two lines centers y=1568 and 1635. Placement safe areas NOT VERIFIED. Actual cue timing must be aligned to a recorded voice."
  },
  "scenes": [
    {
      "id": "01_hook",
      "interval": [
        0,
        180
      ],
      "camera": {
        "projection": "orthographic",
        "angle_degrees": {
          "yaw": 0,
          "pitch": 0,
          "roll": 0
        },
        "zoom_anchor": [
          540,
          960
        ],
        "viewport_center": [
          540,
          960
        ],
        "zoom": [
          1,
          1.02
        ]
      },
      "voiceover": "Why would two countries trade using a currency neither one issues?",
      "caption_timing": "PROVISIONAL; realign to recorded speech",
      "captions": [
        {
          "interval": [
            0,
            90
          ],
          "lines": [
            "Why would two countries trade",
            "using a currency"
          ]
        },
        {
          "interval": [
            90,
            180
          ],
          "lines": [
            "neither one issues?"
          ]
        }
      ],
      "objects": [
        {
          "id": "heading",
          "type": "text",
          "value": "WHY THE DOLLAR?",
          "center": [
            540,
            330
          ],
          "font_px": 68,
          "color": "ivory",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "subheading",
          "type": "text",
          "value": "A SHARED CURRENCY",
          "center": [
            540,
            440
          ],
          "font_px": 40,
          "color": "slate",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "trade_path",
          "type": "line",
          "from": [
            320,
            900
          ],
          "to": [
            760,
            900
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "country_a",
          "type": "circle",
          "center": [
            250,
            900
          ],
          "radius": 70,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "country_b",
          "type": "circle",
          "center": [
            830,
            900
          ],
          "radius": 70,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "dollar_token",
          "type": "circle",
          "center": [
            540,
            900
          ],
          "radius": 50,
          "fill": "gold",
          "stroke": "gold",
          "stroke_px": 3,
          "group": "world",
          "delay": 6,
          "x_motion": {
            "from": 380,
            "to": 700,
            "local_start": 24,
            "local_end": 120
          }
        },
        {
          "id": "dollar_mark",
          "type": "text",
          "value": "$",
          "center": [
            540,
            900
          ],
          "font_px": 67,
          "color": "night",
          "group": "world",
          "x_motion": {
            "from": 380,
            "to": 700,
            "local_start": 24,
            "local_end": 120
          }
        },
        {
          "id": "country_a_label",
          "type": "text",
          "value": "COUNTRY A",
          "center": [
            250,
            1090
          ],
          "font_px": 40,
          "color": "slate",
          "group": "world"
        },
        {
          "id": "country_b_label",
          "type": "text",
          "value": "COUNTRY B",
          "center": [
            830,
            1090
          ],
          "font_px": 40,
          "color": "slate",
          "group": "world"
        }
      ]
    },
    {
      "id": "02_definition",
      "interval": [
        180,
        390
      ],
      "camera": {
        "projection": "orthographic",
        "angle_degrees": {
          "yaw": 0,
          "pitch": 0,
          "roll": 0
        },
        "zoom_anchor": [
          540,
          960
        ],
        "viewport_center": [
          540,
          960
        ],
        "zoom": [
          1,
          1
        ]
      },
      "voiceover": "The dollar is the leading international currency, used in trade invoicing, finance, and central bank reserves.",
      "caption_timing": "PROVISIONAL; realign to recorded speech",
      "captions": [
        {
          "interval": [
            180,
            285
          ],
          "lines": [
            "The dollar is the leading",
            "international currency,"
          ]
        },
        {
          "interval": [
            285,
            390
          ],
          "lines": [
            "used in trade invoicing, finance,",
            "and central bank reserves."
          ]
        }
      ],
      "objects": [
        {
          "id": "heading",
          "type": "text",
          "value": "A GLOBAL TOOL",
          "center": [
            540,
            330
          ],
          "font_px": 68,
          "color": "ivory",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "subheading",
          "type": "text",
          "value": "LEADING, NOT THE ONLY ONE",
          "center": [
            540,
            440
          ],
          "font_px": 40,
          "color": "slate",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "euro_node",
          "type": "circle",
          "center": [
            265,
            840
          ],
          "radius": 60,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "yen_node",
          "type": "circle",
          "center": [
            815,
            840
          ],
          "radius": 60,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "euro",
          "type": "text",
          "value": "€",
          "center": [
            265,
            840
          ],
          "font_px": 60,
          "color": "slate",
          "group": "world"
        },
        {
          "id": "dollar",
          "type": "text",
          "value": "$",
          "center": [
            540,
            840
          ],
          "font_px": 150,
          "color": "gold",
          "group": "world"
        },
        {
          "id": "yen",
          "type": "text",
          "value": "¥",
          "center": [
            815,
            840
          ],
          "font_px": 60,
          "color": "slate",
          "group": "world"
        },
        {
          "id": "card_a",
          "type": "rect",
          "xy": [
            110,
            1010
          ],
          "size": [
            275,
            135
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 10
        },
        {
          "id": "card_b",
          "type": "rect",
          "xy": [
            403,
            1010
          ],
          "size": [
            275,
            135
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 20
        },
        {
          "id": "card_c",
          "type": "rect",
          "xy": [
            695,
            1010
          ],
          "size": [
            275,
            135
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 30
        },
        {
          "id": "trade",
          "type": "text",
          "value": "INVOICING",
          "center": [
            247,
            1077
          ],
          "font_px": 38,
          "color": "ivory",
          "group": "world",
          "delay": 10
        },
        {
          "id": "finance",
          "type": "text",
          "value": "FINANCE",
          "center": [
            540,
            1077
          ],
          "font_px": 38,
          "color": "ivory",
          "group": "world",
          "delay": 20
        },
        {
          "id": "reserves",
          "type": "text",
          "value": "RESERVES",
          "center": [
            833,
            1077
          ],
          "font_px": 38,
          "color": "ivory",
          "group": "world",
          "delay": 30
        }
      ]
    },
    {
      "id": "03_history",
      "interval": [
        390,
        600
      ],
      "camera": {
        "projection": "orthographic",
        "angle_degrees": {
          "yaw": 0,
          "pitch": 0,
          "roll": 0
        },
        "zoom_anchor": [
          540,
          960
        ],
        "viewport_center": [
          540,
          960
        ],
        "zoom": [
          1,
          1.02
        ]
      },
      "voiceover": "In 1944, Bretton Woods placed the dollar at the center of the postwar monetary system.",
      "caption_timing": "PROVISIONAL; realign to recorded speech",
      "captions": [
        {
          "interval": [
            390,
            495
          ],
          "lines": [
            "In 1944, Bretton Woods placed",
            "the dollar at the center"
          ]
        },
        {
          "interval": [
            495,
            600
          ],
          "lines": [
            "of the postwar",
            "monetary system."
          ]
        }
      ],
      "objects": [
        {
          "id": "heading",
          "type": "text",
          "value": "A POSTWAR SYSTEM",
          "center": [
            540,
            330
          ],
          "font_px": 68,
          "color": "ivory",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "subheading",
          "type": "text",
          "value": "BRETTON WOODS",
          "center": [
            540,
            440
          ],
          "font_px": 40,
          "color": "slate",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "history_card",
          "type": "rect",
          "xy": [
            150,
            760
          ],
          "size": [
            780,
            330
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "gold",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "year",
          "type": "text",
          "value": "1944",
          "center": [
            540,
            890
          ],
          "font_px": 155,
          "color": "gold",
          "group": "world"
        },
        {
          "id": "history_label",
          "type": "text",
          "value": "POSTWAR FRAMEWORK",
          "center": [
            540,
            1030
          ],
          "font_px": 40,
          "color": "slate",
          "group": "world"
        }
      ]
    },
    {
      "id": "04_gold_link",
      "interval": [
        600,
        840
      ],
      "camera": {
        "projection": "orthographic",
        "angle_degrees": {
          "yaw": 0,
          "pitch": 0,
          "roll": 0
        },
        "zoom_anchor": [
          540,
          960
        ],
        "viewport_center": [
          540,
          960
        ],
        "zoom": [
          1,
          1
        ]
      },
      "voiceover": "Participating countries tied their currencies to the dollar, while the U.S. promised gold for dollars held by foreign central banks.",
      "caption_timing": "PROVISIONAL; realign to recorded speech",
      "captions": [
        {
          "interval": [
            600,
            720
          ],
          "lines": [
            "Participating countries tied",
            "their currencies to the dollar, while"
          ]
        },
        {
          "interval": [
            720,
            840
          ],
          "lines": [
            "the U.S. promised gold for dollars",
            "held by foreign central banks."
          ]
        }
      ],
      "objects": [
        {
          "id": "heading",
          "type": "text",
          "value": "DOLLARS AND GOLD",
          "center": [
            540,
            330
          ],
          "font_px": 68,
          "color": "ivory",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "subheading",
          "type": "text",
          "value": "THE BRETTON WOODS SYSTEM",
          "center": [
            540,
            440
          ],
          "font_px": 40,
          "color": "slate",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "left_connector",
          "type": "line",
          "from": [
            355,
            925
          ],
          "to": [
            420,
            925
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "right_connector",
          "type": "line",
          "from": [
            660,
            925
          ],
          "to": [
            725,
            925
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "currencies_card",
          "type": "rect",
          "xy": [
            100,
            830
          ],
          "size": [
            255,
            190
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "usd_card",
          "type": "rect",
          "xy": [
            420,
            830
          ],
          "size": [
            240,
            190
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "gold",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "gold_card",
          "type": "rect",
          "xy": [
            725,
            830
          ],
          "size": [
            255,
            190
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "gold",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "currency1",
          "type": "text",
          "value": "OTHER",
          "center": [
            227,
            905
          ],
          "font_px": 40,
          "color": "ivory",
          "group": "world"
        },
        {
          "id": "currency2",
          "type": "text",
          "value": "MONEY",
          "center": [
            227,
            960
          ],
          "font_px": 40,
          "color": "ivory",
          "group": "world"
        },
        {
          "id": "usd",
          "type": "text",
          "value": "$",
          "center": [
            540,
            925
          ],
          "font_px": 90,
          "color": "gold",
          "group": "world"
        },
        {
          "id": "gold",
          "type": "text",
          "value": "GOLD",
          "center": [
            852,
            925
          ],
          "font_px": 45,
          "color": "gold",
          "group": "world"
        },
        {
          "id": "officials",
          "type": "text",
          "value": "FOR CENTRAL BANKS",
          "center": [
            540,
            1190
          ],
          "font_px": 40,
          "color": "slate",
          "group": "world"
        }
      ]
    },
    {
      "id": "05_1971",
      "interval": [
        840,
        1050
      ],
      "camera": {
        "projection": "orthographic",
        "angle_degrees": {
          "yaw": 0,
          "pitch": 0,
          "roll": 0
        },
        "zoom_anchor": [
          540,
          960
        ],
        "viewport_center": [
          540,
          960
        ],
        "zoom": [
          1,
          1.02
        ]
      },
      "voiceover": "In 1971, the United States suspended that gold conversion. Yet the dollar's global role continued.",
      "caption_timing": "PROVISIONAL; realign to recorded speech",
      "captions": [
        {
          "interval": [
            840,
            945
          ],
          "lines": [
            "In 1971, the United States",
            "suspended that gold conversion."
          ]
        },
        {
          "interval": [
            945,
            1050
          ],
          "lines": [
            "Yet the dollar's global role",
            "continued."
          ]
        }
      ],
      "objects": [
        {
          "id": "heading",
          "type": "text",
          "value": "GOLD WINDOW CLOSES",
          "center": [
            540,
            330
          ],
          "font_px": 68,
          "color": "ivory",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "subheading",
          "type": "text",
          "value": "1971",
          "center": [
            540,
            440
          ],
          "font_px": 40,
          "color": "slate",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "left_connector",
          "type": "line",
          "from": [
            390,
            920
          ],
          "to": [
            490,
            920
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "break_link",
          "type": "line",
          "from": [
            490,
            920
          ],
          "to": [
            590,
            920
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 6,
          "fade_out": [
            42,
            66
          ]
        },
        {
          "id": "right_connector",
          "type": "line",
          "from": [
            590,
            920
          ],
          "to": [
            690,
            920
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "dollar_panel",
          "type": "rect",
          "xy": [
            140,
            830
          ],
          "size": [
            250,
            180
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "gold",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "gold_panel",
          "type": "rect",
          "xy": [
            690,
            830
          ],
          "size": [
            250,
            180
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "gold",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "dollar",
          "type": "text",
          "value": "$",
          "center": [
            265,
            920
          ],
          "font_px": 90,
          "color": "gold",
          "group": "world"
        },
        {
          "id": "gold",
          "type": "text",
          "value": "GOLD",
          "center": [
            815,
            920
          ],
          "font_px": 44,
          "color": "gold",
          "group": "world"
        },
        {
          "id": "status",
          "type": "text",
          "value": "CONVERSION SUSPENDED",
          "center": [
            540,
            1195
          ],
          "font_px": 42,
          "color": "ivory",
          "group": "world"
        }
      ]
    },
    {
      "id": "06_reasons",
      "interval": [
        1050,
        1290
      ],
      "camera": {
        "projection": "orthographic",
        "angle_degrees": {
          "yaw": 0,
          "pitch": 0,
          "roll": 0
        },
        "zoom_anchor": [
          540,
          960
        ],
        "viewport_center": [
          540,
          960
        ],
        "zoom": [
          1,
          1
        ]
      },
      "voiceover": "A large U.S. economy and deep Treasury markets help support the dollar. It is also widely used for trade invoicing.",
      "caption_timing": "PROVISIONAL; realign to recorded speech",
      "captions": [
        {
          "interval": [
            1050,
            1170
          ],
          "lines": [
            "A large U.S. economy",
            "and deep Treasury markets"
          ]
        },
        {
          "interval": [
            1170,
            1290
          ],
          "lines": [
            "help support the dollar. It is also",
            "widely used for trade invoicing."
          ]
        }
      ],
      "objects": [
        {
          "id": "heading",
          "type": "text",
          "value": "WHY DID IT LAST?",
          "center": [
            540,
            330
          ],
          "font_px": 68,
          "color": "ivory",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "subheading",
          "type": "text",
          "value": "SCALE AND MARKET DEPTH",
          "center": [
            540,
            440
          ],
          "font_px": 40,
          "color": "slate",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "economy_card",
          "type": "rect",
          "xy": [
            145,
            740
          ],
          "size": [
            790,
            140
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "treasury_card",
          "type": "rect",
          "xy": [
            145,
            930
          ],
          "size": [
            790,
            140
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "gold",
          "stroke_px": 3,
          "group": "world",
          "delay": 18
        },
        {
          "id": "trade_card",
          "type": "rect",
          "xy": [
            145,
            1120
          ],
          "size": [
            790,
            140
          ],
          "radius": 24,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 30
        },
        {
          "id": "economy",
          "type": "text",
          "value": "LARGE U.S. ECONOMY",
          "center": [
            540,
            810
          ],
          "font_px": 44,
          "color": "ivory",
          "group": "world",
          "delay": 6
        },
        {
          "id": "treasury",
          "type": "text",
          "value": "DEEP TREASURY MARKETS",
          "center": [
            540,
            1000
          ],
          "font_px": 44,
          "color": "gold",
          "group": "world",
          "delay": 18
        },
        {
          "id": "invoicing",
          "type": "text",
          "value": "TRADE INVOICING",
          "center": [
            540,
            1190
          ],
          "font_px": 44,
          "color": "ivory",
          "group": "world",
          "delay": 30
        }
      ]
    },
    {
      "id": "07_network",
      "interval": [
        1290,
        1530
      ],
      "camera": {
        "projection": "orthographic",
        "angle_degrees": {
          "yaw": 0,
          "pitch": 0,
          "roll": 0
        },
        "zoom_anchor": [
          540,
          960
        ],
        "viewport_center": [
          540,
          960
        ],
        "zoom": [
          1,
          1.02
        ]
      },
      "voiceover": "When banks and businesses already use dollars, others can find it easier to use them too. That reinforces the network.",
      "caption_timing": "PROVISIONAL; realign to recorded speech",
      "captions": [
        {
          "interval": [
            1290,
            1410
          ],
          "lines": [
            "When banks and businesses",
            "already use dollars, others can"
          ]
        },
        {
          "interval": [
            1410,
            1530
          ],
          "lines": [
            "find it easier to use them too.",
            "That reinforces the network."
          ]
        }
      ],
      "objects": [
        {
          "id": "heading",
          "type": "text",
          "value": "THE NETWORK EFFECT",
          "center": [
            540,
            330
          ],
          "font_px": 68,
          "color": "ivory",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "subheading",
          "type": "text",
          "value": "USE CAN REINFORCE USE",
          "center": [
            540,
            440
          ],
          "font_px": 40,
          "color": "slate",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "left_link",
          "type": "line",
          "from": [
            470.57,
            875.49
          ],
          "to": [
            294.33,
            990.95
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 22
        },
        {
          "id": "right_link",
          "type": "line",
          "from": [
            609.43,
            875.49
          ],
          "to": [
            785.67,
            990.95
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 38
        },
        {
          "id": "bottom_link",
          "type": "line",
          "from": [
            540.0,
            913.0
          ],
          "to": [
            540.0,
            1137.0
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 54
        },
        {
          "id": "hub",
          "type": "circle",
          "center": [
            540,
            830
          ],
          "radius": 85,
          "fill": "gold",
          "stroke": "gold",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "hub_dollar",
          "type": "text",
          "value": "$",
          "center": [
            540,
            830
          ],
          "font_px": 104,
          "color": "night",
          "group": "world",
          "delay": 6
        },
        {
          "id": "left_node",
          "type": "circle",
          "center": [
            250,
            1020
          ],
          "radius": 55,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 22
        },
        {
          "id": "right_node",
          "type": "circle",
          "center": [
            830,
            1020
          ],
          "radius": 55,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 38
        },
        {
          "id": "bottom_node",
          "type": "circle",
          "center": [
            540,
            1190
          ],
          "radius": 55,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 54
        },
        {
          "id": "banks",
          "type": "text",
          "value": "BANKS",
          "center": [
            250,
            1135
          ],
          "font_px": 40,
          "color": "slate",
          "group": "world",
          "delay": 22
        },
        {
          "id": "businesses",
          "type": "text",
          "value": "BUSINESSES",
          "center": [
            830,
            1135
          ],
          "font_px": 40,
          "color": "slate",
          "group": "world",
          "delay": 38
        },
        {
          "id": "investors",
          "type": "text",
          "value": "INVESTORS",
          "center": [
            540,
            1300
          ],
          "font_px": 40,
          "color": "slate",
          "group": "world",
          "delay": 54
        }
      ]
    },
    {
      "id": "08_payoff",
      "interval": [
        1530,
        1800
      ],
      "camera": {
        "projection": "orthographic",
        "angle_degrees": {
          "yaw": 0,
          "pitch": 0,
          "roll": 0
        },
        "zoom_anchor": [
          540,
          960
        ],
        "viewport_center": [
          540,
          960
        ],
        "zoom": [
          1,
          1.02
        ]
      },
      "voiceover": "The dollar is not the only international currency, and its lead isn't guaranteed. Its advantage rests on history, markets, and widespread use.",
      "caption_timing": "PROVISIONAL; realign to recorded speech",
      "captions": [
        {
          "interval": [
            1530,
            1605
          ],
          "lines": [
            "The dollar is not the only",
            "international currency,"
          ]
        },
        {
          "interval": [
            1605,
            1675
          ],
          "lines": [
            "and its lead isn't guaranteed."
          ]
        },
        {
          "interval": [
            1675,
            1800
          ],
          "lines": [
            "Its advantage rests on history,",
            "markets, and widespread use."
          ]
        }
      ],
      "objects": [
        {
          "id": "heading",
          "type": "text",
          "value": "LEADING. NOT ONLY.",
          "center": [
            540,
            330
          ],
          "font_px": 68,
          "color": "ivory",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "subheading",
          "type": "text",
          "value": "AN EVOLVING SYSTEM",
          "center": [
            540,
            440
          ],
          "font_px": 40,
          "color": "slate",
          "group": "screen",
          "delay": 0
        },
        {
          "id": "euro_link",
          "type": "line",
          "from": [
            424.45,
            923.91
          ],
          "to": [
            308.76,
            947.84
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "yen_link",
          "type": "line",
          "from": [
            655.55,
            923.91
          ],
          "to": [
            771.24,
            947.84
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "other_link",
          "type": "line",
          "from": [
            540.0,
            1018.0
          ],
          "to": [
            540.0,
            1126.0
          ],
          "color": "slate",
          "stroke_px": 4,
          "group": "world",
          "delay": 6
        },
        {
          "id": "euro_node",
          "type": "circle",
          "center": [
            250,
            960
          ],
          "radius": 62,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "yen_node",
          "type": "circle",
          "center": [
            830,
            960
          ],
          "radius": 62,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "other_node",
          "type": "circle",
          "center": [
            540,
            1170
          ],
          "radius": 46,
          "fill": "surface",
          "stroke": "slate",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "euro",
          "type": "text",
          "value": "€",
          "center": [
            250,
            960
          ],
          "font_px": 64,
          "color": "slate",
          "group": "world"
        },
        {
          "id": "yen",
          "type": "text",
          "value": "¥",
          "center": [
            830,
            960
          ],
          "font_px": 64,
          "color": "slate",
          "group": "world"
        },
        {
          "id": "hub",
          "type": "circle",
          "center": [
            540,
            900
          ],
          "radius": 120,
          "fill": "surface",
          "stroke": "gold",
          "stroke_px": 3,
          "group": "world",
          "delay": 6
        },
        {
          "id": "dollar",
          "type": "text",
          "value": "$",
          "center": [
            540,
            900
          ],
          "font_px": 145,
          "color": "gold",
          "group": "world"
        },
        {
          "id": "conclusion",
          "type": "text",
          "value": "HISTORY + MARKETS + USE",
          "center": [
            540,
            1335
          ],
          "font_px": 42,
          "color": "ivory",
          "group": "world"
        }
      ]
    }
  ]
}
```
