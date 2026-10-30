# Social Video & Motion Design Director — preliminary test report

## Verdict

**Promising, but not validated as a production-ready skill.** In a self-directed dry run, the proposed approach generated four distinct scenario responses, correctly stopped when an important data claim lacked evidence, and supported one small coded visual test. The rendered test also revealed a real defect that the storyboard did not prevent. No audience testing or independent assessment was done.

## What was actually tested

- I manually applied the proposed director instructions to four synthetic briefs. This was not an invocation of an installed skill; no skill package was created or installed.
- The same assistant authored the test briefs, direction, code, and critique. There was no separate production agent, blind evaluation, human panel, or baseline comparison, so the results are vulnerable to self-review bias.
- I rendered one six-second, silent, coded 2D sample from the first plan, inspected decoded stills, and ran targeted technical checks. The other scenarios are written plans only.
- Plans are in `plan.md`. The MP4 and decoded frame sheets are in the same folder as this report.

## Scenario results

| Test | Observed result | Status / limitations |
|---|---|---|
| A. Vertical beginner explainer | Produced three frame-bounded scenes and a runnable visual plan; the first render exposed a label collision. | **Partial.** Fixed the identified collision, but opening engagement, full-motion feel, mobile legibility and audience understanding are not independently validated. The plan also did not provide the requested hook alternatives. |
| B. Fictional product short | Chose a feature-demonstration structure using only the supplied fictional fact; labeled the proposed UI as illustration and did not invent metrics. | **Partial.** Written plan only. The layout still offers alternatives and motion is underspecified, so a separate builder would need to resolve details. Platform overlays were not verified. |
| C. Data story with missing source | The proposed response stops and asks for the figure's source, period, values and intended audience instead of asserting a 40% increase. | **Pass for this narrow simulated intake case.** There was no interactive second turn or chart; this does not prove robustness on other claims. |
| D. YouTube educational opening | Produced a question-led opening and a different, slower schematic storytelling approach, with narration timing marked provisional. | **Partial.** Written plan only; scientific accuracy, narration sync, captions and the payoff of the full ten-minute video remain unverified. |

## Rendered sample: observations and checks

**Input:** a simplified FIFO queue with one consumer, communicated using on-screen text. 360 × 640 pixels, 30 fps, 180 frames, silent; these are test-preview specifications, not platform recommendations.

- **Pass — technical decode:** FFmpeg decoded the actual H.264 output as 360 × 640 at 30 fps, with 180 decoded frames and 6.00 seconds of video. There is no audio stream, as planned.
- **Pass — boundary checks:** Scene ranges `[0,60)`, `[60,120)`, `[120,180)` cover all 180 frames without overlap. I inspected decoded frames around the scene boundaries and sampled mid-motion frames.
- **Pass — limited determinism check:** Re-rendering each of 10 chosen frames in the same local environment produced identical raw-image hashes. This is not a cross-machine, cross-render or whole-video determinism test.
- **Pass — targeted color calculation:** The nominal white text on navy has a calculated contrast ratio of 16.37:1; navy text on turquoise is 10.83:1. This does not establish accessibility compliance for the entire encoded video, other elements, font sizes, or every platform.
- **Pass — targeted collision recheck:** A geometry check found no overlap between the `QUEUE` label's bounding box and the request-circle bounding boxes across all 180 planned frames after the second correction. This is not an all-elements collision test.
- **Not checked:** Full-motion playback at 1× and 0.5×, overall visual quality, human comprehension, live platform UI overlays, audio sync, captions and 3D. There is intentionally no sound, so the sample cannot test audio or captions. A human playback and mobile-size review is still needed.

### Defect and revisions

1. **Major: scene 2, frame 75.** On the first encoded render, a moving request circle crossed the `QUEUE` label above the container. The original plan did not specify a clear travel path relative to the label. I moved the label below the container and re-rendered.
2. **Major: scene 3, frame 135.** The first correction put the same label in the path of R1 exiting the queue. I moved it below and to the right and checked its bounding box against all moving circles across the timeline. The final decoded contact sheet shows no overlap at frames 75 or 135.
3. **Open creative issue: scene 1, frames 0–59.** The title says `REQUESTS ARRIVE`, but the objects are already static for two seconds. That satisfies the literal plan but may be a weak or confusing opening. It remains a subjective concern, not a measured retention result.
4. **Open readability issue:** `QUEUE` and `SERVED` are small in the 360-pixel-wide preview. Their legibility needs a real-device / human check; color contrast alone does not establish readability.

The pre-fix decoded contact sheet and first MP4 are preserved as evidence. The intermediate revision was inspected but was not separately retained.

## What the test teaches us about the skill

1. **A storyboard needs spatial collision constraints, not only scene endpoints.** Specify text bounding areas and moving-object paths, then check intermediate frames.
2. **A director needs to judge the promise of the opening, not just whether elements appear on schedule.** The sample's static opening exposed this gap.
3. **A handoff should mark unresolved creative decisions explicitly.** The product plan's alternative layouts and unspecified motion timing require resolution before implementation.
4. **The director needs review evidence appropriate to the claim.** Screenshots helped expose overlap, but cannot prove that motion feels good, audio works, or viewers understand the story.
5. **Guardrails need executable or inspectable criteria.** Source verification, timeline coverage, scene boundaries and collision checks are more useful when their evidence is identified.

## Recommended next test

Create a testable candidate skill with clear modes, timeline conventions and evidence-based review statuses. Then run the same four briefs through it and a baseline without it; give the outputs to an independent builder and reviewer. Render at least one sample with narration and captions, check all target formats, and evaluate actual audience comprehension. Treat results as evidence for this scope, not as a guarantee of virality or creative quality.

## Files

- `plan.md` — full test briefs, plans and flagged limitations.
- `sample.mp4` — corrected silent sample.
- `decoded-contact-sheet.png` — selected frames decoded from the corrected MP4.
- `sample-before-fix.mp4` and `contact-sheet-before-fix.png` — evidence of the initial label collision.
- `automated-checks.json` — selected checks and raw-frame hashes.
- `sample-render.py` — small demonstration renderer; it requires Pillow, imageio-ffmpeg, and the specified local font. It is not the Director skill.

The earlier local project deletion was preserved. This test report and its evidence were later added to the session branch for sharing.
