# screenshot-to-code — Repo Reference

Upstream: https://github.com/abi/screenshot-to-code (MIT). Verified against the `main` branch layout.

## What the application does

Converts a screenshot, mockup, Figma-style export, or screen recording into clean frontend code. Generation streams over a WebSocket from a FastAPI backend to a React/Vite frontend.

Four request modes:

| Mode | Input | Prompt set |
| --- | --- | --- |
| Create from image | Screenshot or mockup | `backend/prompts/create/image.py` |
| Create from text | Text description | `backend/prompts/create/text.py` |
| Create from video | Screen recording | `backend/prompts/create/video.py` |
| Update / edit | Existing page plus instruction | `backend/prompts/update/` |

Supported stacks: HTML + Tailwind, HTML + CSS, React + Tailwind, Vue + Tailwind, Bootstrap, Ionic + Tailwind.

Default models: Gemini 3 Flash / Gemini 3.1 Pro (strongest accuracy), GPT-5.5 and GPT-5.4 Mini, Claude Opus 4.6 / 4.8. Image generation uses `z-image-turbo` through Replicate. Model catalogues live in `frontend/src/lib/models.ts`; provider adapters live in `backend/agent/providers/`.

## Repository map

```
backend/
  main.py                     FastAPI app and route registration
  llm.py                      Model clients and streaming
  config.py                   Settings and environment handling
  asset_extraction.py         Pulling real assets out of the reference image
  babel_cdn.py                Pinned in-browser Babel inclusion
  custom_types.py             Shared request/response types
  start.py, utils.py          Startup helpers; utils.print_prompt_summary for prompt inspection
  run_evals.py                Model/prompt evaluation runner
  run_image_generation_evals.py
  agent/
    engine.py                 Agent loop and tool orchestration
    state.py, runner.py
    providers/                Per-provider adapters
    tools/                    definitions.py, extract_assets.py, local_assets.py,
                              parsing.py, runtime.py, screenshot_preview.py,
                              summaries.py, types.py
  codegen/                    Code generation helpers
  costs/                      Token/cost accounting
  debug/                      Debug utilities
  evals/                      config.py, core.py, runner.py, sessions.py, sets.py,
                              asset_extraction_benchmark.py
  fs_logging/                 Filesystem logging
  image_generation/           Image generation integration
  preview_screenshot/         Headless render of the generated page
  prompts/
    system_prompt.py          The main behavioural prompt
    create/                   image.py, text.py, video.py
    update/                   from_history.py, from_file_snapshot.py
    design_system.py, message_builder.py, prompt_types.py, request_parsing.py
  routes/                     HTTP routes
  tests/                      pytest suite
  video/                      Video-mode processing
  ws/                         WebSocket streaming
  pytest.ini, pyrightconfig.json, pyproject.toml, poetry.lock
  Dockerfile, .pre-commit-config.yaml

frontend/
  src/App.tsx                 Main app shell
  src/lib/                    models.ts, stacks.ts, design-systems.ts, prompt-history.ts,
                              takeScreenshot.ts, babelCdn.ts, generateCode.ts, utils.ts
  src/components/             UI components
  src/store/                  State management
  src/types.ts, config.ts, constants.ts, urls.ts
  src/tests/                  Frontend tests

docker-compose.yml, README.md, AGENTS.md (CLAUDE.md just points at it),
Evaluation.md, TESTING.md, Troubleshooting.md, design-docs/, scripts/, blog/
```

## Commands

Backend (Poetry-managed; run Python through `poetry run`):

```bash
cd backend
poetry install
poetry run playwright install chromium      # Linux: add --with-deps
poetry env activate                          # then run the printed activate command
poetry run uvicorn main:app --reload --port 7001
```

```bash
cd backend
poetry run pytest            # all tests
poetry run pytest -vv        # verbose
poetry run pytest tests/test_screenshot.py::TestNormalizeUrl
poetry run pytest --cov=routes
poetry run pyright           # type checking
poetry run pre-commit run --all-files
```

Prompt inspection:

```python
from utils import print_prompt_summary
print_prompt_summary(prompt_messages)
```

Frontend:

```bash
cd frontend
pnpm install
pnpm dev        # http://localhost:5173  (not 127.0.0.1 — Vite binds to localhost)
pnpm lint       # --max-warnings 0, so pre-existing warnings fail the run
```

Docker (from repo root, no hot reload):

```bash
echo "GEMINI_API_KEY=your-key" > .env
docker-compose up -d --build
```

## Configuration

Keys live in `backend/.env` (restart the backend after editing) or, for OpenAI/Anthropic/Gemini, the in-app Settings dialog. `REPLICATE_API_KEY` is env-only.

| Key | Required | Unlocks |
| --- | --- | --- |
| `OPENAI_API_KEY` | One of the three code-gen keys | GPT code-gen variants |
| `ANTHROPIC_API_KEY` | One of the three code-gen keys | Claude code-gen variants |
| `GEMINI_API_KEY` | One of the three — strongly recommended | Gemini variants, asset extraction, video mode |
| `REPLICATE_API_KEY` | Strongly recommended | Image editing, background removal, image generation |

Other settings:

- `OPENAI_BASE_URL` — proxy support; must include `v1` in the path.
- `VITE_WS_BACKEND_URL` — WebSocket backend (default `ws://127.0.0.1:7001`); set in `frontend/.env.local`.
- `VITE_HTTP_BACKEND_URL` — HTTP backend for non-streaming routes.
- Screenshot preview is enabled automatically once Playwright Chromium is installed; the Settings dialog reports its availability. Without it, generation still works but the agent cannot self-check its render.

## Evaluation

- 16-screenshot dataset; set `EVALS_DIR` in `backend/evals/config.py` (`backend/evals_data/inputs` and `.../outputs` by default).
- Set `STACK` and `MODEL` in `backend/run_evals.py`, then run it with a provider key in the environment.
- Rate outputs in the app at `/evals` on a 1–4 scale; run each model/prompt + stack combination several times and average.

## Test and type policy (from the repo's own agent instructions)

- Run `poetry run pytest` after every backend change.
- Run `poetry run pyright` after every backend change; introduce no new warnings in changed files.
- Run `pnpm lint` after frontend changes. Lint is expected to have pre-existing baseline errors (`@typescript-eslint/no-explicit-any` in `generateCode.ts`), so a red baseline is not proof of a regression.
- Prompt formatting: prefer triple-quoted strings, and a single triple-quoted f-string over concatenated fragments.

## Gotchas

- No model key ⇒ generation fails fast with a "No OpenAI, Anthropic, or Gemini API key" message.
- Non-interactive shells may not have `poetry` on `PATH`; use its full path if not found.
- `pyproject.toml` pins `^3.10`, but the resolved virtualenv is often Python 3.12 — that satisfies the constraint. Just use `poetry run`.
- `pnpm install` prints an "Ignored build scripts (esbuild, puppeteer)" warning; harmless.
- On Windows, save `backend/.env` as UTF-8 (Notepad++: Encoding → UTF-8) to avoid UTF-8 decode errors.
- The hosted product on the `hosted` branch targets a separate SaaS backend and is not the open-source code path.
- Logos and brand assets in the demo examples are the property of their owners; do not ship them in reproduced work.

