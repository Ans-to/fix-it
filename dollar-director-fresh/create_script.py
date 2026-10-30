#!/usr/bin/env python3
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
P=json.loads((R/'visual-plan.json').read_text());Q=json.loads((R/'qa-results.json').read_text());S=[]
def w(x=''):S.append(x)
def t(f):return f'{int(f//1800):02}:{(f%1800)/30:06.3f}'
def describe(o):
 ty=o['type']
 if ty=='text':return f"Text **{o['value']}**, center {tuple(o['center'])}, {o['font_px']} px, `{o['color']}`"
 if ty=='circle':return f"Circle center {tuple(o['center'])}, radius {o['radius']}, fill `{o['fill']}`, outline `{o['stroke']}`, {o['stroke_px']} px"
 if ty=='rect':return f"Rounded rectangle at {tuple(o['xy'])}, size {tuple(o['size'])}, corner radius {o['radius']}, fill `{o['fill']}`, outline `{o['stroke']}`, {o['stroke_px']} px"
 return f"Line {tuple(o['from'])} → {tuple(o['to'])}, `{o['color']}`, {o['stroke_px']} px"

w('# Why is the dollar a world currency?')
w('## A fresh 60-second code-only Director script')
w('')
w('**Scope:** This is a new plan, written from the brief using the improved Social Video & Motion Design Director skill. It is not a finished video. Its visual plan uses only code-drawn typography and geometric primitives—no image or video inputs.')
w('')
w('### Brief')
w('- **Confirmed:** 60-second subject explainer; code-only visuals; no images or videos used as inputs; frame-level direction.')
w('- **Proposed, not confirmed:** English narration, general audience, vertical 1080 × 1920, 30 fps, 1,800 frames. The intended platform and actual overlay safe areas are unknown. Change the plan if the delivery format differs.')
w('- **Promise:** Explain why the dollar is widely used internationally without suggesting it is the only currency or that its position is guaranteed.')
w('- **Creative concept:** A single dollar token moves through a clean editorial diagram; history explains how it became central, a broken link marks the suspension of gold conversion, and a connected network explains why the dollar remains useful. Euro, yen and other nodes are illustrative, not exhaustive or proportional data.')
w('- **Hook choice:** Recommended: “Why would two countries trade using a currency neither one issues?” Alternative: “The dollar lost its gold link. Why did the world keep using it?” The recommended hook establishes the viewer’s question before the historical answer.')
w('- **Open decisions:** Platform and placement, narrator, final audio/caption delivery, and platform-specific safe areas. Draft caption timing is not synchronized to a recording.')
w('')
w('## Strict production rules')
w('1. **No visual media inputs:** no photos, screenshots, footage, stock clips, bitmap textures, external SVG images or generated-image assets. Draw only text, solid-color rounded rectangles, circles and lines in code. The QA contact sheet is an output, not an input. Licensed font files are allowed.')
w('2. The `visual-plan.json` manifest is provided separately and embedded in full at the end of this document. It specifies every object, group, coordinate, visual frame interval, camera transform and provisional caption cue. The two copies are generated together and must remain identical.')
w('3. Every visual frame is a deterministic function of the frame number and fixed inputs. No wall-clock timing, unseeded randomness or playback-history state. Scene boundaries are 0-based, start-inclusive and end-exclusive.')
w('4. Draw at the proposed 1080 × 1920 and 30 fps. Screen center and zoom anchor are both `(540,960)`. All cameras are front-facing orthographic, yaw/pitch/roll `0°`; they are virtual 2D transforms, not video footage or a physical camera.')
w('5. Heading and subheading are **screen-fixed** objects, entry delay 0, unaffected by the world camera. Diagram graphics are world objects; their individual delays and camera transforms are in the manifest. Captions are screen-fixed.')
w('6. No invented statistics, real product UI, real transaction data or claims of exclusive dollar use. Use the supplied source links. The currency symbols and network do not represent measured shares, actual counterparties or all currencies.')
w('7. The 1,800-frame visual timeline is exact only for the assumed format. Voice timing, caption sync, final playback and platform safety are **not verified**. Record the voice, realign caption cues, then verify the 60-second total and every delivery format.')
w('')
w('## Narrative and full voiceover')
for i,s in enumerate(P['scenes'],1):w(f"\n**{i}. {s['id'].split('_',1)[1].replace('_',' ').title()}** — {s['voiceover']}")
w('')
w(f"The text has an estimated {Q['voiceover_estimated_tokens']} word tokens. Pronunciations of years and initials can take longer; no recording was measured. The lines are intended for one natural, clear narrator, not a rapid advertisement read.")
w('')
w('## Timing, camera and story beats')
w('| Scene | Time | Frames `[start,end)` | Camera zoom | What the viewer sees and learns |')
w('|---|---|---|---|---|')
beats=[
 'A dollar token travels between two illustrative countries, making the hook visible.',
 'The dollar appears alongside other currency examples and three areas of international use.',
 'A 1944 card establishes the Bretton Woods historical starting point.',
 'Other currencies, the dollar and gold connect; a label limits the gold conversion to central banks.',
 'The center gold-conversion link fades out; the dollar remains visible.',
 'Three explicit cards identify the U.S. economy, Treasury markets and trade invoicing.',
 'Banks, businesses and investors connect to a dollar hub in stages; nodes are illustrative.',
 'Other currencies coexist around the dollar; the ending returns to the main answer.'
]
for s,beat in zip(P['scenes'],beats):
 a,b=s['interval'];z=s['camera']['zoom'];w(f"| {s['id']} | {t(a)}–{t(b)} | [{a}, {b}) | {z[0]:.3f} → {z[1]:.3f} | {beat} |")
w('')
w('## Frame-state contract')
w('For every frame `f` from 0 through 1799, select the scene with `start ≤ f < end`; set `local = f − start` and `D = end − start`. Fill the background with `#101B2B`. Use `smooth(x)=u²(3−2u)`, where `u=clamp(x,0,1)`.')
w('')
w('- **Opacity:** Screen objects default to delay 0 and world objects to delay 6 unless their `delay` field says otherwise. `opacity=smooth((local−delay)/18)`. If `fade_out=[a,b]`, multiply by `1−smooth((local−a)/(b−a))`. There is no entry position shift.')
w('- **Camera:** `zoom=z0+(z1−z0)×smooth(local/(D−1))`. Apply it to world points around `(540,960)`: `(540+(x−540)×zoom, 960+(y−960)×zoom)`. Scale world sizes, stroke widths and world text sizes accordingly. Screen headings, subheadings and captions do not zoom. Angles are fixed at zero.')
w('- **Token motion:** For the two objects carrying `x_motion`, use `x=380+320×smooth((local−24)/96)` before world-camera projection. Both stay aligned. The 1971 center link fades between local frames 42 and 66. Network lines start inside the relevant nodes and share the same camera transformation; they are drawn behind the nodes.')
w('- **Layering:** Background → world objects in manifest order → screen objects in manifest order → caption panel and text. Standard source-over alpha. Rectangles use top-left positions; circles and text use centers. Round scaled text sizes and stroke widths to the nearest pixel.')
w('- **Captions:** Draw the current draft cue in a screen-fixed panel at `(70,1510)`, size `940 × 180`, radius 24. Font is 42 px DejaVu Sans Bold. One line is centered at `(540,1600)`; two lines at `(540,1568)` and `(540,1635)`. **Platform-safe area: NOT VERIFIED.** Copy and layout are specified; cue times are provisional and must be aligned with the final recorded audio.')
w('- **Font:** DejaVu Sans Bold from a valid licensed font file; the test used `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`. Any substitute changes font metrics and requires renewed layout testing.')
w('')
w('**Palette:** `night #101B2B`, `surface #1C2D40`, `ivory #F7F4EC`, `slate #C3CED7`, `gold #EAC777`.')
w('')
w('## Complete scene instructions')
w('The rows are base positions; apply the frame-state contract above. The full embedded manifest resolves every property and exact caption interval.')
for s in P['scenes']:
 a,b=s['interval'];w(f"\n### {s['id']} — frames [{a}, {b})")
 w(f"**Voiceover:** “{s['voiceover']}”\n")
 w('| Object | Direction | Group / timing |')
 w('|---|---|---|')
 for o in s['objects']:
  details=[o['group'],f"delay {o.get('delay',0 if o['group']=='screen' else 6)}"]
  if 'x_motion' in o:details.append('x-motion local 24–120')
  if 'fade_out' in o:details.append(f"fade-out local {o['fade_out'][0]}–{o['fade_out'][1]}")
  w(f"| {o['id']} | {describe(o)} | {'; '.join(details)} |")
 w('\n**Draft caption pages—timing not yet aligned to audio:**')
 for cue in s['captions']:w(f"- Frames `[{cue['interval'][0]}, {cue['interval'][1]})`: "+' / '.join('“'+x+'”' for x in cue['lines']))
w('')
w('## Audio and accessibility')
w('- Narration: one clear, unhurried voice. The script is a target, not a recorded or timed performance. Record and align it before locking captions and dependent movements.')
w('- Music and effects: optional, understated and separately sourced or synthesized with permission; none are required to understand the story. No music or narration has been produced or mixed. Caption meaningful non-speech sounds if they are added.')
w('- After rendering, review captions and actual backgrounds at the intended viewing size, check current platform UI overlays, provide visual description or a descriptive transcript where needed, and check applicable contrast and flashing guidance. The draft coordinates are not a platform-safety certification.')
w('')
w('## Test and review status')
w('- **PASS, visual timeline math only:** the eight planned intervals cover 1,800 frames, exactly 60 seconds at the proposed 30 fps.')
w('- **PASS, selected layout checks only:** all 1,800 planned frames were checked for composition bounds, text-to-text bounding-box overlaps, selected text inside its card and draft-caption coverage/bounds. No issues remained. This is not an exhaustive all-object collision check.')
w('- **PASS, planned graph topology:** endpoints of the network and payoff links fall inside their intended node outlines in world space; they share the same camera transform and no entry shift. This does not establish full-motion visual quality.')
w('- **PASS, draft copy:** caption pages reproduce the planned narration. Their alignment to real speech is not checked.')
w(f"- **PASS, nominal flat-color calculations:** ivory/night {Q['nominal_contrast_ratios']['ivory/night']}:1; slate/night {Q['nominal_contrast_ratios']['slate/night']}:1. This does not prove readability or accessibility throughout fades.")
w('- **Test defects found and fixed:** The first layout check found a history-card label too wide and three caption lines outside the planned text area. The label was shortened and the caption lines reflowed; the selected checks then passed.')
w('- **NOT CHECKED:** a finished video, natural voice duration, caption synchronization, full-motion playback, audio mix, human comprehension, viewer retention, real-device readability and platform overlays. The contact sheet samples stills only.')
w('')
w('## Fact sources')
w('- [Federal Reserve: International Role of the U.S. Dollar, 2025](https://www.federalreserve.gov/econres/notes/feds-notes/the-international-role-of-the-u-s-dollar-2025-edition-20250718.html): international role, economic scale and market depth. The dollar had an international role before 1944.')
w('- [IMF: Central Banks and the Bretton Woods Gold Puzzle](https://www.imf.org/-/media/files/publications/wp/2019/wpiea2019161.pdf): the 1944 framework and U.S. gold conversion for foreign central banks.')
w('- [U.S. State Department: Nixon and the End of Bretton Woods](https://history.state.gov/milestones/1969-1976/nixon-shock): suspension of gold convertibility in 1971 and the broader system’s unraveling over 1971–1973.')
w('- [BIS: Global reach of currencies](https://www.bis.org/publ/qtrpdf/r_qt2406b.htm) and [global FX markets](https://www.bis.org/publications/qr-202212/global-foreign-exchange-market-higher-volatility-environment): international dollar use and trade invoicing.')
w('- [IMF: The Dollar’s Primacy](https://www.imf.org/en/publications/fandd/issues/2022/03/book-review-dollar-primacy-joyce): market depth and network effects; these factors do not guarantee permanent dominance.')
w('')
w('## Embedded authoritative visual-plan.json')
w('This is the full [separate visual-plan.json](visual-plan.json), included here so the script is usable on its own. SHA-256 of the UTF-8 JSON file: `'+hashlib.sha256((R/'visual-plan.json').read_bytes()).hexdigest()+'`.')
w('```json');w((R/'visual-plan.json').read_text().rstrip());w('```')
(R/'director-script.md').write_text('\n'.join(S)+'\n')
print('Generated fresh, self-contained director-script.md')
