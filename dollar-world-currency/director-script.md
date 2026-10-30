# Why is the dollar a world currency? — 60-second director script

## Brief and assumptions
- **Requested:** One-minute explanatory video script and frame-level production direction; no image or video inputs. The deliverable is a production plan, not a finished video.
- **Proposed, not user-confirmed:** English; curious non-specialists; vertical 1080 × 1920; 30 fps; YouTube Shorts / vertical social context. The exact platform and placement are unspecified. The 1,800-frame plan below is exact *under these assumptions*. Recompose and retime if the approved format changes.
- **Core answer:** The dollar is the leading international currency—not the world’s only currency—because history, the size of the U.S. economy, deep markets and reinforcing use help sustain its role.
- **No CTA.** No statistics or unsupported numerical claims are used. The diagrams explain relationships, not measured sizes or real transactions.
- **Open decisions:** Confirm platform/placement and format; select or record a narrator; confirm audio choices and final caption delivery. Platform UI safe areas are not verified.

## Strict production rules
1. **No image or video assets:** no photos, stock footage, screenshots, downloaded images, image-generation outputs, bitmap textures, external SVG illustrations or video clips. Draw all visuals procedurally from text, flat fills, rounded rectangles, circles and lines. Fonts are allowed; they are not image or video assets. The contact sheet is a QA output, not an input asset.
2. **No fake data or fake interface.** Do not insert numbers, countries, flags or charts implying a statistic not supplied and sourced. Draw only the abstract diagram specified below.
3. Use DejaVu Sans / DejaVu Sans Bold with the verified font files and metrics from the test environment, or seek approval and repeat layout tests with a licensed substitute. Preserve written copy; do not silently rewrite facts.
4. Frame state is calculated from frame index and fixed inputs, not wall-clock time or unseeded randomness. Draw at 1080 × 1920 and 30 fps with 1,800 video frames; never interpret the end of a scene as an included frame.
5. There are **no photo/video cuts, no physical camera, no perspective and no 3D**. The camera is a virtual, face-on orthographic view. Any sense of depth comes from hierarchy, color and restrained 2D scale, not unrequested assets.
6. The visual timeline and draft captions are precisely specified. **Voiceover and word-level caption sync are not locked:** record and align the exact narration, then adjust caption cues and any dependent visual timing as needed while preserving the approved 60-second total. Do not claim synchronization before checking the actual recording.
7. Do not call the video visually approved or platform-safe without inspecting the final output at the intended display size, watching playback, listening to the audio and checking the actual platform placement.

## Overall creative direction
A premium editorial explainer: deep navy, warm ivory and restrained gold, with clean geometry and generous negative space. The design asks a question, demonstrates the historical system, shows the gold link breaking, and then explains why everyday use reinforces the dollar’s role. A familiar, confident narrator should sound curious and clear—not like a financial advertisement.

**Hook options:** (1) “Why does the world reach for dollars, even when the United States isn’t in the deal?” **Recommended:** it leads directly to the answer. (2) “The dollar lost its gold link. So why does the world still use it?” Both are truthful; the second foregrounds the historical turn.

## Complete voiceover

> Why does the world reach for dollars, even when the United States isn't in the deal?

> The dollar isn't the world's only currency. It's the leading currency for trade, finance, and official reserves.

> In 1944, Bretton Woods placed the dollar at the center of the postwar monetary system.

> Participating countries linked currencies to the dollar, while the U.S. linked the dollar to gold for foreign central banks.

> In 1971, the U.S. suspended that gold conversion. The dollar's international role, however, did not disappear.

> The U.S. economy was large, businesses kept using dollars, and investors could trade U.S. Treasuries in deep markets.

> That creates a network effect: the more widely a currency is used, the more useful it can become.

> Other currencies matter too, and the dollar's lead isn't guaranteed forever.

> It's not the world's only money. It's the system many already use.

The draft has an estimated 146 word tokens; numbers and abbreviations may take longer to speak. Scene rates are estimates, not a measurement of spoken audio. Record and verify the timing rather than assuming it fits.

## Timing and camera
All frame intervals are `[start, end)`: for example `[0,180)` contains frames 0–179. The following timecodes describe visual boundaries, not measured narration timing. All cameras are front-on orthographic, 0° tilt and rotation, centered on world/screen point `(540,990)`. Zoom applies to diagram graphics only; headings and captions stay screen-fixed.

| Scene | Visual time | Frames | Camera zoom start → end | Narrative purpose |
|---|---|---|---|---|
| 1. The question | 00:00.000–00:06.000 | [0, 180) | 1.000 → 1.020 | Why does the world reach for dollars, even when the United States isn't in the deal? |
| 2. What world currency means | 00:06.000–00:13.000 | [180, 390) | 1.000 → 1.000 | The dollar isn't the world's only currency. It's the leading currency for trade, finance, and official reserves. |
| 3. Postwar start | 00:13.000–00:20.000 | [390, 600) | 1.000 → 1.025 | In 1944, Bretton Woods placed the dollar at the center of the postwar monetary system. |
| 4. The gold link | 00:20.000–00:27.500 | [600, 825) | 1.000 → 1.000 | Participating countries linked currencies to the dollar, while the U.S. linked the dollar to gold for foreign central banks. |
| 5. The 1971 break | 00:27.500–00:35.000 | [825, 1050) | 1.000 → 1.025 | In 1971, the U.S. suspended that gold conversion. The dollar's international role, however, did not disappear. |
| 6. Markets and use | 00:35.000–00:42.500 | [1050, 1275) | 1.000 → 1.000 | The U.S. economy was large, businesses kept using dollars, and investors could trade U.S. Treasuries in deep markets. |
| 7. Network effect | 00:42.500–00:49.500 | [1275, 1485) | 1.000 → 1.025 | That creates a network effect: the more widely a currency is used, the more useful it can become. |
| 8. Other currencies | 00:49.500–00:55.000 | [1485, 1650) | 1.000 → 1.000 | Other currencies matter too, and the dollar's lead isn't guaranteed forever. |
| 9. Payoff | 00:55.000–01:00.000 | [1650, 1800) | 1.000 → 1.020 | It's not the world's only money. It's the system many already use. |

## Exact frame-state rules
The machine-readable **`visual-plan.json`** is the authoritative complete list of primitives, colors, text, object-level delays, paths, scene ranges and draft caption pages. The following rules define every one of frames 0–1799 without listing 1,800 separate rows:

- Coordinates use a top-left origin; x increases right, y increases down. All base positions and dimensions below are in 1080 × 1920 pixels. Text is centered on its stated point; rectangles use a top-left point and circles use a center.
- Select the unique scene whose `start_frame ≤ f < end_frame_exclusive`; set `s = f − start_frame`, `D = end_frame_exclusive − start_frame`. Hard cut at each boundary. Fill the background `#101C2D` on every frame.
- `clamp(x)=min(1,max(0,x))`; `E(x)=clamp(x)² × (3 − 2 × clamp(x))`. Heading objects use delay `d=0`, graphic objects use `d=6`, unless an object lists a delay. Compute `entry=E((s−d)/18)` and `yOffset=40×(1−entry)`. The object opacity is `entry`, except objects with a fade-out use `entry × (1−E((s−fadeStart)/(fadeEnd−fadeStart)))`. Objects with opacity zero are not drawn.
- Camera zoom is `z = zStart + (zEnd−zStart) × E(s/(D−1))`. For graphics, after adding `yOffset`, project a world point `(x,y)` to `(540+(x−540)×z, 990+(y−990)×z)`; multiply graphic sizes, line widths and font sizes by `z`. Headings retain screen x and get only `yOffset`; captions are fixed on screen. Round raster text size and line widths to the nearest pixel. Camera pitch, yaw and roll stay zero.
- Scene 1’s token circle and `$` have `x = 490 + 100 × E((s−20)/90)` before camera projection. Scene 5’s center link fades over local frames 38–56. Scene 2’s three cards reveal in sequence; scene 7’s three network branches reveal in sequence. Other primitive coordinates hold; their precise delays are listed in the scene details and JSON.
- Draw graphic primitives in their listed order, then headings, then captions. Compositing uses standard source-over alpha. The fixed draft caption background is a rounded rectangle `(70,1510)` with size `940 × 180`, radius 24, panel fill. Draw up to two lines centered at `(540,1568)` and `(540,1635)`, 42 px DejaVu Sans Bold, ivory. The exact caption cue ranges below are **provisional**, not measured audio alignment.

**Palette:** background `#101C2D`; panel `#1B2D40`; ink `#F7F4ED`; muted `#BBC9D5`; gold `#EEC86B`. These are design colors, not measured brand colors.

## Scene-by-scene visual script
The layout coordinates below are the base design; apply the frame-state rules and camera above. Shape/text overlaps inside their own containers and connecting lines are intentional.

### 1. The question — frames [0, 180)
**Narration:** “Why does the world reach for dollars, even when the United States isn't in the deal?”

| Primitive | Base direction | Special timing |
|---|---|---|
| heading | Text **WHY THE DOLLAR?**, center (540, 345), 66 px bold, color `ink` | Standard group entry |
| subheading | Text **WHEN NEITHER SIDE IS IN THE U.S.**, center (540, 455), 40 px regular, color `muted` | Standard group entry |
| buyer | Circle center (250, 925), radius 72, fill `panel`, outline `muted` / 3 px | Standard group entry |
| seller | Circle center (830, 925), radius 72, fill `panel`, outline `muted` / 3 px | Standard group entry |
| left link | Line (330, 925) → (445, 925), color `muted`, width 4 px | Standard group entry |
| right link | Line (635, 925) → (750, 925), color `muted`, width 4 px | Standard group entry |
| transfer | Circle center (540, 925), radius 70, fill `gold`, outline `gold` / 3 px | x 490→590 over local frames 20–110 |
| dollar | Text **$**, center (540, 925), 84 px bold, color `background` | x 490→590 over local frames 20–110 |
| buyer label | Text **BUYER**, center (250, 1100), 40 px bold, color `muted` | Standard group entry |
| seller label | Text **SELLER**, center (830, 1100), 40 px bold, color `muted` | Standard group entry |

**Draft caption pages — provisional until narration is recorded:**
- Frames `[0, 90)`: “Why does the world” / “reach for dollars,”
- Frames `[90, 180)`: “even when the United States” / “isn't in the deal?”

### 2. What world currency means — frames [180, 390)
**Narration:** “The dollar isn't the world's only currency. It's the leading currency for trade, finance, and official reserves.”

| Primitive | Base direction | Special timing |
|---|---|---|
| heading | Text **THE LEADING CHOICE**, center (540, 345), 66 px bold, color `ink` | Standard group entry |
| subheading | Text **NOT THE ONLY CURRENCY**, center (540, 455), 40 px regular, color `muted` | Standard group entry |
| dollar sign | Text **$**, center (540, 790), 150 px bold, color `gold` | Standard group entry |
| trade card | Rounded rectangle top-left (125, 990), 250 × 150, radius 24, fill `panel`, outline `muted` / 3 px | entry delay 12 frames |
| finance card | Rounded rectangle top-left (415, 990), 250 × 150, radius 24, fill `panel`, outline `muted` / 3 px | entry delay 22 frames |
| reserves card | Rounded rectangle top-left (705, 990), 250 × 150, radius 24, fill `panel`, outline `muted` / 3 px | entry delay 32 frames |
| trade | Text **TRADE**, center (250, 1065), 40 px bold, color `ink` | entry delay 12 frames |
| finance | Text **FINANCE**, center (540, 1065), 40 px bold, color `ink` | entry delay 22 frames |
| reserves | Text **RESERVES**, center (830, 1065), 38 px bold, color `ink` | entry delay 32 frames |

**Draft caption pages — provisional until narration is recorded:**
- Frames `[180, 285)`: “The dollar isn't the world's” / “only currency.”
- Frames `[285, 390)`: “It's the leading currency for” / “trade, finance, and official reserves.”

### 3. Postwar start — frames [390, 600)
**Narration:** “In 1944, Bretton Woods placed the dollar at the center of the postwar monetary system.”

| Primitive | Base direction | Special timing |
|---|---|---|
| heading | Text **A POSTWAR SYSTEM**, center (540, 345), 66 px bold, color `ink` | Standard group entry |
| subheading | Text **BRETTON WOODS**, center (540, 455), 40 px regular, color `muted` | Standard group entry |
| year frame | Rounded rectangle top-left (175, 805), 730 × 280, radius 32, fill `panel`, outline `gold` / 3 px | Standard group entry |
| year | Text **1944**, center (540, 920), 150 px bold, color `gold` | Standard group entry |
| history caption | Text **POSTWAR FRAMEWORK**, center (540, 1040), 40 px bold, color `muted` | Standard group entry |

**Draft caption pages — provisional until narration is recorded:**
- Frames `[390, 495)`: “In 1944, Bretton Woods placed” / “the dollar at the center”
- Frames `[495, 600)`: “of the postwar” / “monetary system.”

### 4. The gold link — frames [600, 825)
**Narration:** “Participating countries linked currencies to the dollar, while the U.S. linked the dollar to gold for foreign central banks.”

| Primitive | Base direction | Special timing |
|---|---|---|
| heading | Text **HOW IT WORKED**, center (540, 345), 66 px bold, color `ink` | Standard group entry |
| subheading | Text **THE BRETTON WOODS SYSTEM**, center (540, 455), 40 px regular, color `muted` | Standard group entry |
| currencies box | Rounded rectangle top-left (100, 840), 260 × 190, radius 24, fill `panel`, outline `muted` / 3 px | Standard group entry |
| usd box | Rounded rectangle top-left (410, 840), 260 × 190, radius 24, fill `panel`, outline `gold` / 3 px | Standard group entry |
| gold box | Rounded rectangle top-left (720, 840), 260 × 190, radius 24, fill `panel`, outline `gold` / 3 px | Standard group entry |
| currencies line 1 | Text **OTHER**, center (230, 910), 40 px bold, color `ink` | Standard group entry |
| currencies line 2 | Text **MONEY**, center (230, 965), 40 px bold, color `ink` | Standard group entry |
| usd | Text **$**, center (540, 935), 92 px bold, color `gold` | Standard group entry |
| gold | Text **GOLD**, center (850, 935), 42 px bold, color `gold` | Standard group entry |
| link a | Line (365, 935) → (405, 935), color `muted`, width 5 px | Standard group entry |
| link b | Line (675, 935) → (715, 935), color `muted`, width 5 px | Standard group entry |
| official qualifier | Text **FOR MONETARY AUTHORITIES**, center (540, 1200), 40 px bold, color `muted` | Standard group entry |

**Draft caption pages — provisional until narration is recorded:**
- Frames `[600, 712)`: “Participating countries linked” / “currencies to the dollar,”
- Frames `[712, 825)`: “while the U.S. linked the dollar” / “to gold for foreign central banks.”

### 5. The 1971 break — frames [825, 1050)
**Narration:** “In 1971, the U.S. suspended that gold conversion. The dollar's international role, however, did not disappear.”

| Primitive | Base direction | Special timing |
|---|---|---|
| heading | Text **THE GOLD LINK ENDS**, center (540, 345), 66 px bold, color `ink` | Standard group entry |
| subheading | Text **1971**, center (540, 455), 40 px regular, color `muted` | Standard group entry |
| usd panel | Rounded rectangle top-left (150, 830), 250 × 180, radius 24, fill `panel`, outline `gold` / 3 px | Standard group entry |
| gold panel | Rounded rectangle top-left (680, 830), 250 × 180, radius 24, fill `panel`, outline `gold` / 3 px | Standard group entry |
| usd symbol | Text **$**, center (275, 920), 90 px bold, color `gold` | Standard group entry |
| gold word | Text **GOLD**, center (805, 920), 43 px bold, color `gold` | Standard group entry |
| broken left | Line (410, 920) → (493, 920), color `muted`, width 5 px | Standard group entry |
| broken right | Line (587, 920) → (670, 920), color `muted`, width 5 px | Standard group entry |
| center link | Line (493, 920) → (587, 920), color `muted`, width 5 px | fade out local frames 38–56 |
| conversion status | Text **CONVERSION SUSPENDED**, center (540, 1190), 40 px bold, color `ink` | Standard group entry |

**Draft caption pages — provisional until narration is recorded:**
- Frames `[825, 937)`: “In 1971, the U.S. suspended” / “that gold conversion.”
- Frames `[937, 1050)`: “The dollar's international role,” / “however, did not disappear.”

### 6. Markets and use — frames [1050, 1275)
**Narration:** “The U.S. economy was large, businesses kept using dollars, and investors could trade U.S. Treasuries in deep markets.”

| Primitive | Base direction | Special timing |
|---|---|---|
| heading | Text **WHY IT STAYED**, center (540, 345), 66 px bold, color `ink` | Standard group entry |
| subheading | Text **USE AND LIQUID MARKETS**, center (540, 455), 40 px regular, color `muted` | Standard group entry |
| trade panel | Rounded rectangle top-left (140, 805), 800 × 150, radius 24, fill `panel`, outline `muted` / 3 px | Standard group entry |
| treasury panel | Rounded rectangle top-left (140, 1000), 800 × 150, radius 24, fill `panel`, outline `gold` / 3 px | Standard group entry |
| trade words | Text **DOLLAR TRADE**, center (540, 880), 45 px bold, color `ink` | Standard group entry |
| treasury words | Text **U.S. TREASURIES**, center (540, 1075), 45 px bold, color `gold` | Standard group entry |
| market note | Text **DEEP MARKETS**, center (540, 1250), 40 px bold, color `muted` | Standard group entry |

**Draft caption pages — provisional until narration is recorded:**
- Frames `[1050, 1162)`: “The U.S. economy was large,” / “businesses kept using dollars,”
- Frames `[1162, 1275)`: “and investors could trade U.S.” / “Treasuries in deep markets.”

### 7. Network effect — frames [1275, 1485)
**Narration:** “That creates a network effect: the more widely a currency is used, the more useful it can become.”

| Primitive | Base direction | Special timing |
|---|---|---|
| heading | Text **THE NETWORK EFFECT**, center (540, 345), 66 px bold, color `ink` | Standard group entry |
| subheading | Text **USE REINFORCES USE**, center (540, 455), 40 px regular, color `muted` | Standard group entry |
| left link | Line (305, 1030) → (470, 920), color `muted`, width 4 px | entry delay 18 frames |
| right link | Line (775, 1030) → (610, 920), color `muted`, width 4 px | entry delay 32 frames |
| bottom link | Line (540, 1140) → (540, 1000), color `muted`, width 4 px | entry delay 46 frames |
| hub | Circle center (540, 900), radius 92, fill `gold`, outline `gold` / 3 px | Standard group entry |
| hub dollar | Text **$**, center (540, 900), 105 px bold, color `background` | Standard group entry |
| node left | Circle center (250, 1065), radius 50, fill `panel`, outline `muted` / 3 px | entry delay 18 frames |
| node right | Circle center (830, 1065), radius 50, fill `panel`, outline `muted` / 3 px | entry delay 32 frames |
| node bottom | Circle center (540, 1200), radius 50, fill `panel`, outline `muted` / 3 px | entry delay 46 frames |
| left network label | Text **BUYERS**, center (250, 1170), 40 px bold, color `muted` | entry delay 18 frames |
| right network label | Text **SELLERS**, center (830, 1170), 40 px bold, color `muted` | entry delay 32 frames |
| bottom network label | Text **INVESTORS**, center (540, 1305), 40 px bold, color `muted` | entry delay 46 frames |

**Draft caption pages — provisional until narration is recorded:**
- Frames `[1275, 1380)`: “That creates a network effect:” / “the more widely a currency is used,”
- Frames `[1380, 1485)`: “the more useful” / “it can become.”

### 8. Other currencies — frames [1485, 1650)
**Narration:** “Other currencies matter too, and the dollar's lead isn't guaranteed forever.”

| Primitive | Base direction | Special timing |
|---|---|---|
| heading | Text **NOT THE ONLY ONE**, center (540, 345), 66 px bold, color `ink` | Standard group entry |
| subheading | Text **THE LEAD CAN CHANGE**, center (540, 455), 40 px regular, color `muted` | Standard group entry |
| euro circle | Circle center (250, 950), radius 95, fill `panel`, outline `muted` / 3 px | Standard group entry |
| dollar circle | Circle center (540, 950), radius 105, fill `panel`, outline `gold` / 3 px | Standard group entry |
| yen circle | Circle center (830, 950), radius 95, fill `panel`, outline `muted` / 3 px | Standard group entry |
| euro symbol | Text **€**, center (250, 950), 90 px bold, color `ink` | Standard group entry |
| dollar symbol | Text **$**, center (540, 950), 110 px bold, color `gold` | Standard group entry |
| yen symbol | Text **¥**, center (830, 950), 90 px bold, color `ink` | Standard group entry |
| other note | Text **CURRENCIES COEXIST**, center (540, 1200), 40 px bold, color `muted` | Standard group entry |

**Draft caption pages — provisional until narration is recorded:**
- Frames `[1485, 1567)`: “Other currencies matter too,” / “and the dollar's lead”
- Frames `[1567, 1650)`: “isn't guaranteed forever.”

### 9. Payoff — frames [1650, 1800)
**Narration:** “It's not the world's only money. It's the system many already use.”

| Primitive | Base direction | Special timing |
|---|---|---|
| heading | Text **HISTORY + USE**, center (540, 345), 66 px bold, color `ink` | Standard group entry |
| subheading | Text **REINFORCE THE DOLLAR’S ROLE**, center (540, 455), 40 px regular, color `muted` | Standard group entry |
| final ring | Circle center (540, 920), radius 135, fill `panel`, outline `gold` / 3 px | Standard group entry |
| final dollar | Text **$**, center (540, 920), 155 px bold, color `gold` | Standard group entry |
| final line | Text **A COMMON GLOBAL CHOICE**, center (540, 1210), 42 px bold, color `ink` | Standard group entry |

**Draft caption pages — provisional until narration is recorded:**
- Frames `[1650, 1725)`: “It's not the world's only money.”
- Frames `[1725, 1800)`: “It's the system” / “many already use.”

## Audio direction
- One natural, warm, clear narrator. Record each sentence without forcing it into a robotic tempo; preserve all words. The total recording must fit the 60-second visual edit, so adjust and recheck cue timing if necessary. The narration has not been recorded.
- Optional subtle original/synthesized music bed, low enough that speech stays clear. No music track or SFX is currently supplied, mixed or approved; do not use licensed audio without permission. If meaningful non-speech audio is added, include it in captions as appropriate. Audio is not a visual image/video asset.
- Provide accurate synchronized captions after audio alignment and a descriptive transcript or visual description where needed. Draft captions here show copy and layout only; their exact cue boundaries must be tested against speech.

## Test results
- **PASS — timeline math:** Nine consecutive scenes cover frames 0–1799, exactly 1,800 frames / 60 seconds at the proposed 30 fps.
- **PASS — planned geometry:** The test evaluated positions for all 1,800 planned frames, checked each drawn primitive against project bounds, checked separate text bounding boxes against each other, and checked selected text within its intended box. This is not a complete all-object collision test.
- **PASS — draft captions:** Every frame has exactly one planned caption page; pages reproduce the narration text and fit the specified caption rectangle using the test font. Audio synchronization has not been verified.
- **PASS — flat-color contrast calculation:** Ivory/navy 15.59:1, muted/navy 10.14:1, gold/navy 10.69:1, ivory/panel 12.78:1. These are calculations for fully opaque flat colors, not full accessibility certification or proof during animated fades.
- **PASS — restrictions in the plan:** only text, circles, rounded rectangles and lines are used as visual primitives. The QA contact sheet was generated from those primitives and is not a visual input asset.
- **NOT CHECKED:** final rendered video, spoken delivery, audio mix, actual caption timing, platform overlays, full-motion aesthetic quality, human comprehension and audience retention. A still-frame contact sheet cannot establish these.
- **Review finding and repair:** An earlier QA preview showed the year-card sublabel extending across its container edge. I shortened it to `POSTWAR FRAMEWORK` and added a per-frame test that selected labels remain inside their respective boxes. Final QA reports zero selected-geometry issues.

## Factual sources and qualifications
- [Federal Reserve, International Role of the U.S. Dollar (2025)](https://www.federalreserve.gov/econres/notes/feds-notes/the-international-role-of-the-u-s-dollar-2025-edition-20250718.html): leading reserve role, economic scale, financial-market depth, and historical context. The dollar had an international role before 1944; the script does not claim 1944 was its first use.
- [IMF working paper on Bretton Woods](https://www.imf.org/-/media/files/publications/wp/2019/wpiea2019161.pdf): the 1944 conference, dollar-centered exchange rates and the U.S. gold-conversion commitment to foreign central banks.
- [U.S. State Department, Nixon and the end of Bretton Woods](https://history.state.gov/milestones/1969-1976/nixon-shock): gold convertibility was suspended in 1971; the broader fixed-rate system unraveled over 1971–1973. The script does not say the whole system ended in one day.
- [Bank for International Settlements, Global Reach of Currencies](https://www.bis.org/publ/qtrpdf/r_qt2406b.htm): the dollar’s use in cross-border finance and as a vehicle currency.
- [IMF, The Dollar’s Primacy](https://www.imf.org/en/publications/fandd/issues/2022/03/book-review-dollar-primacy-joyce): an account of financial-market liquidity and network effects. This is an explanation of reinforcing factors, not proof that the dollar will dominate forever.
