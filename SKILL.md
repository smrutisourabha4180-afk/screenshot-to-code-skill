---
name: screenshot-to-code
description: Converts UI screenshots, mockups, design exports, and screen recordings into working frontend code, and operates or extends the abi/screenshot-to-code application. This skill should be used when a user supplies a visual reference (image, screenshot, Figma-style mockup, or screen recording) and asks for an implementation, when a generated page must be verified against a reference image, or when work touches the screenshot-to-code repo (FastAPI backend, React/Vite frontend, prompt sets, stacks, models, or evals).
license: MIT
---

# Screenshot to Code

## Purpose

Recreate a visual reference as working frontend code, then verify the result against the reference instead of trusting the first draft.

This skill packages two things:

1. The **method** the [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code) project uses to turn pixels into pages: asset extraction over imitation, stack-pinned scaffolding, headless screenshot self-verification, and a strict visual-priority order.
2. The **application** itself: how to run, configure, and extend it when the task is about the repo rather than about one page.

The screenshot is the visual source of truth. The target project is the technical source of truth. Neither may destroy the other.

## When to Use This Skill

Use this skill when:

- A user provides a screenshot, mockup, wireframe, or design export and asks for code that matches it.
- A generated page must be visually verified or iterated against a reference image.
- A screen recording must be turned into an interactive prototype.
- The task is to run, configure, debug, or extend the screenshot-to-code repo (add a stack, add a model, change prompts, run evals).

Do not use this skill for:

- Greenfield product design with no reference image (prefer a normal frontend workflow).
- Copying a competitor's proprietary assets, logos, or copyrighted content into a deliverable.
- Reproducing a page where the user only wants a static image mockup rather than runnable code.

## Core Capabilities

| Capability | What it produces |
| --- | --- |
| Reference analysis | A structured inventory of layout, components, type scale, colors, spacing, and assets |
| Project inspection | Framework, build system, entry points, styling system, and reusable assets for the target repo |
| Implementation | Runnable code in the project's own stack, or a standalone single-file prototype |
| Asset extraction | Real images/icons pulled from the reference instead of placeholders |
| Self-verification | Headless full-page renders compared against the reference |
| Iteration | Difference-ranked fixes, largest deviation first |
| Repo operations | Local run, key configuration, prompt/stack/model extension, evals |

## Operating Loop

Run the loop in order. Do not skip verification when a browser is available.

### 1. Inspect the target project

Establish constraints before writing code.

```bash
python scripts/inspect_project.py <project-root>
```

Confirm, by reading files rather than assuming:

- Framework and build system (`package.json`, `pyproject.toml`, lockfiles)
- Entry points and routing
- Styling system (Tailwind config, CSS modules, design tokens, theme file)
- Existing components that must be reused rather than re-created
- Existing assets, and the directory convention for new ones
- Package manager in use (`pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `package-lock.json` → npm)

Record the detected dev command. Everything downstream depends on this being right.

### 2. Analyze the reference

Work outward from structure to detail:

1. Page skeleton, then regions (nav, hero, sidebar, content, footer)
2. Component tree and repetition (cards, list rows, tabs, tables)
3. Layout system (grid/flex, container widths, gutters, breakpoints)
4. Type scale, weights, and line heights
5. Color palette, borders, radii, shadows
6. Icons, images, logos, illustrations
7. Interactive and stateful regions (forms, dropdowns, carousels, modals)
8. Responsive intent, when more than one viewport is shown

Inventory assets before building:

```bash
python scripts/analyze_assets.py <project-root>
```

Name every element you cannot see clearly as an explicit open question instead of inventing it.

### 3. Plan the implementation

Decide component boundaries, layout strategy, breakpoints, required assets, and whether new dependencies are genuinely needed. Prefer the project's existing primitives, and prefer standard layout systems over absolute positioning.

### 4. Implement

Build in the target stack, changing only files the task requires. Match the reference's hierarchy first; refine detail later.

### 5. Render and capture

```bash
python scripts/capture_screenshot.py http://localhost:5173/ out.png
```

Capture the same viewport the reference uses. For long pages, capture full-page and also crop the regions under review.

### 6. Compare and rank differences

```bash
python scripts/compare_screenshots.py reference.png actual.png difference.png
```

The difference image is a locator, not a metric: it shows where to look, not how wrong things are. Judge layout, then geometry, then typography, then color, then assets.

### 7. Iterate

Fix the largest deviation first and re-render. Repeat render → capture → compare → fix until the remaining differences are cosmetic or explained. Do not stop after the first implementation when verification is available.

### 8. Report

State what was built, the files changed, the verification performed, and every known deviation from the reference.

## Visual Accuracy Priority Order

When fixes compete for effort, spend them in this order:

1. Overall layout and region boundaries
2. Component position within the layout
3. Dimensions and spacing
4. Typography (family, size, weight, line height)
5. Color
6. Images and icons
7. Borders and radii
8. Shadows and micro-detail

Never compensate for a wrong layout with extra effects, fake gradients, or decorative shadow work.

## Asset Handling

Priority order for every visual asset in the reference:

1. An asset already in the target project
2. An asset provided by the user
3. An asset extracted from the reference screenshot
4. A generated or recreated asset, as a last resort

Never substitute a random placeholder when the reference shows a specific visual. Never embed the reference screenshot itself as page content; see `references/generation-rules.md` for the full rule set and exact stack scaffolding snippets.

## Verification Tiers

Choose the strongest verification the environment allows, and say which one was used:

| Tier | Method | Requirement |
| --- | --- | --- |
| 1 | Headless render + image comparison | Playwright/Puppeteer plus Pillow available |
| 2 | Manual browser render, described region by region | A dev server and a browser |
| 3 | Static review of markup against the reference inventory | No browser available |

Tier 3 is a fallback, not a completion criterion. If only Tier 3 was possible, state that visual verification did not happen.

## Operating the screenshot-to-code Application

Use this path when the user wants the app itself, not just the technique. Full detail lives in `references/repo-reference.md`.

Backend (FastAPI, WebSocket generation stream on port `7001`):

```bash
cd backend
poetry install
poetry run playwright install chromium   # enables the screenshot-preview tool
poetry run uvicorn main:app --reload --port 7001
```

Frontend (React + Vite on port `5173`):

```bash
cd frontend
pnpm install
pnpm dev
```

Docker (production-style, no hot reload):

```bash
echo "GEMINI_API_KEY=your-key" > .env
docker-compose up -d --build
```

Keys belong in `backend/.env` (or the in-app Settings dialog):

| Key | Effect |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI code generation |
| `ANTHROPIC_API_KEY` | Claude code generation |
| `GEMINI_API_KEY` | Gemini code generation, asset extraction, video mode |
| `REPLICATE_API_KEY` | Image editing, background removal, image generation (env only) |

At least one code-generation key is required; generation fails fast without one. `REPLICATE_API_KEY` cannot be set from the UI. Verify the exact variable names against the repo's current `README.md` before relying on them, since model providers change over time.

After any change to that repo:

```bash
cd backend && poetry run pytest && poetry run pyright
cd frontend && pnpm lint
```

## Extending the Repository

| Goal | Where to work |
| --- | --- |
| Change how the model writes code | `backend/prompts/system_prompt.py` |
| Change the create prompts (image, text, video) | `backend/prompts/create/` |
| Change the update/edit prompts | `backend/prompts/update/` |
| Add a stack | `backend/prompts/` plus the stack list in `frontend/src/lib/stacks.ts` |
| Add or adjust a model | `frontend/src/lib/models.ts`, `backend/agent/providers/` |
| Change generation orchestration and tool calls | `backend/agent/engine.py`, `backend/agent/tools/` |
| Change the streaming/WebSocket contract | `backend/ws/`, `frontend/src/lib/generateCode.ts` |
| Evaluate model/prompt changes | `backend/run_evals.py`, `backend/evals/` |

House style from the repo's own agent instructions: prefer triple-quoted strings for prompt text, and prefer a single triple-quoted f-string over concatenated fragments when interpolating.

Run evals rather than intuition when changing a prompt or model: outputs land in `backend/evals_data/outputs` and are rated in the app at `/evals` on a 1–4 scale, averaged over repeated runs.

## Guardrails

- Do not invent UI that the reference does not support. If a region is unreadable, ask or declare the assumption.
- Do not restructure a working project to reproduce a screenshot. Adapt the page, not the architecture.
- Do not touch unrelated files, and do not leave debugging artifacts behind.
- Do not add dependencies when the project already contains an equivalent primitive.
- Do not claim visual verification you did not perform.
- Do not copy proprietary logos, brand marks, or copyrighted imagery into a deliverable.
- Keep secrets in `.env`. Never commit API keys or echo them into logs.

## Reference Index

| File | Contents |
| --- | --- |
| `references/workflow.md` | The phased loop in compact checklist form |
| `references/generation-rules.md` | Output discipline, asset rules, exact stack scaffolding, anti-patterns |
| `references/repo-reference.md` | Repo map, commands, configuration, stacks, models, evals, test policy, gotchas |

Scripts:

| Script | Purpose |
| --- | --- |
| `scripts/inspect_project.py` | Detect framework, package manager, entry points, assets in a target project |
| `scripts/analyze_assets.py` | Inventory image assets with dimensions, format, and color mode |
| `scripts/capture_screenshot.py` | Headless Chromium capture at a 1440×900 viewport, full page |
| `scripts/compare_screenshots.py` | Difference image between reference and render, contrast-boosted |

## Repo Quick Facts

- **Stacks:** HTML + Tailwind, HTML + CSS, React + Tailwind, Vue + Tailwind, Bootstrap, Ionic + Tailwind
- **Modes:** image → code, text → code, video/screen recording → code, and update/edit of an existing page
- **Default models:** Gemini (best accuracy), GPT-5.x, Claude Opus
- **Ports:** backend `7001`, frontend `5173`
- **Hosted alternative:** https://screenshottocode.com
- **Backend Python:** Poetry-managed; always run Python through `poetry run`
- **Screenshot preview:** optional backend tool that renders and self-checks generated pages; requires Playwright Chromium

## Limitations

- Screenshot fidelity is bounded by what the reference shows: hover, focus, empty, and error states are usually absent and must be inferred or requested.
- Screens must not be reproduced where doing so infringes copyright, trademarks, or license terms of the source design.
- The difference image is a visual aid; it is not a pixel-metric and should not be reported as an accuracy score.
- Upstream model names, keys, and ports change; confirm them against the repository's current `README.md` and `AGENTS.md` before treating the values here as authoritative.
- To read a reference screenshot directly, the agent must have image input enabled; without it, ask the user to describe the layout instead of guessing.


