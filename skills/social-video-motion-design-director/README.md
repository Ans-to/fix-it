# Social Video & Motion Design Director

`SKILL.md` is the entry point. Install or copy the **whole skill directory**: references and templates are required for full production/review; `code-video/` is required for a complete code-video handoff. `SKILL.md` has a missing-companion fallback. `evals/` is optional. The skill directs audience-aware storytelling, visual design, motion and handoff; it does not itself guarantee engagement, accessibility, factual accuracy or a completed video.

The operating contract covers intake/routing, confirmed vs proposed timing, claim and qualifier checks, geometry, reading holds, captions and contrast, placement sources, checksums, sampling, review status and revisions. The templates provide concrete records. Placement resources are starting points, not universal safe zones.

## Code-video profile and reference tooling

[`code-video/CONTRACT.md`](code-video/CONTRACT.md) defines mode selection, authoritative manifests, reproducible frame seeking, output files and evidence-backed QA. It includes a strict [versioned JSON Schema](code-video/manifest.schema.json) and a small deterministic single-frame SVG reference renderer. The provided profile supports 2D rectangles, circles, lines, and single-line text with explicit font assets; it intentionally does **not** encode video or support audio, image/video assets, 3D or shaders. Other formats require an appropriate explicitly documented profile and renderer—those media are not universally forbidden.

The eight-frame illustrative fixture has two checked-in expected SVG frames. Example QA tests selected seek order, validates the manifest and checks analytic shape bounds; its full review is PARTIAL. Measurement helpers test supplied boxes, endpoints and colors but do not collect/authenticate rendered evidence or replace final video QA. See the contract for exact limitations, instructions and dependency installation. Do not mistake the example renderer or fixture for a production-quality video engine.

## Tests

From the repository root, run standard-library checks:

```sh
python3 -B skills/social-video-motion-design-director/evals/test_contracts.py
python3 -B skills/social-video-motion-design-director/evals/test_review_guardrails.py
python3 -B skills/social-video-motion-design-director/evals/test_operating_contract.py
```

The vector-profile regression suite requires the optional `jsonschema` dependency from `code-video/requirements.txt` in an isolated environment, then:

```sh
python3 -B skills/social-video-motion-design-director/evals/test_code_video_profile.py
```

These test selected implementations, schema/semantic rejection and golden SVG bytes, not an independent AI agent's adherence, full video, accessibility, factual accuracy or creative quality. `evals/director-review-cases.md` and `evals/operating-contract-cases.md` are future behavioral evaluation cases, not assertions that an independent evaluation passed.
