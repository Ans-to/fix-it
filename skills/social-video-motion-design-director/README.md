# Social Video & Motion Design Director

`SKILL.md` is the entry point. It directs audience-aware storytelling, visual design, motion and production handoff for code-based video. The references and templates support specific tasks; the skill does not itself render a video or guarantee creative quality or audience retention.

## Checks

From the repository root, run the standard-library tests:

```sh
python3 -B skills/social-video-motion-design-director/evals/test_review_guardrails.py
python3 -B skills/social-video-motion-design-director/evals/test_contracts.py
```

These are mechanical examples for artifact integrity, selected geometry and contrast, frame contracts and review status. They do **not** run a separate AI agent or prove that its output is factually correct, engaging or accessible.

`evals/director-review-cases.md` contains additional behavioral scenarios for a future independent agent evaluation; those scenarios are not represented as already passed.
