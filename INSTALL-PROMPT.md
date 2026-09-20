# Install Prompt

Ye file ek **copy-paste prompt** hai. Isko jise dena ho use bhejo — uska agent khud
skill install kar lega. Kuch manually karne ki zaroorat nahi.

Source repo (public, MIT): https://github.com/smrutisourabha4180-afk/screenshot-to-code-skill

---

## Prompt A — One-paste install (recommended)

Copy everything between the lines and paste it into your agent.

---

Install the `screenshot-to-code` agent skill on this machine.

Source repo (public): `https://github.com/smrutisourabha4180-afk/screenshot-to-code-skill`

Do this:

1. Download the repo into a temporary folder with `git clone --depth 1`, or by
   downloading the zip of the `main` branch. Do not install it into my current project.
2. Detect my agent skills directories and install into **every one that exists**:
   - `~/.claude/skills/screenshot-to-code/`
   - `~/.agents/skills/screenshot-to-code/`
   - `~/.codex/skills/screenshot-to-code/`
   - `~/.gemini/skills/screenshot-to-code/`
   - `~/.copilot/skills/screenshot-to-code/`
   - `~/.config/opencode/skills/screenshot-to-code/`
   If none of them exist, ask me which agent I use before creating one.
3. Copy `SKILL.md`, `README.md`, `references/`, and `scripts/` into each destination.
   Exclude `.git`, `.gitignore`, and any `__pycache__`.
4. Verify the install, then report the result:
   - `SKILL.md` exists in each destination
   - its frontmatter contains `name: screenshot-to-code` and a `description`
   - the three files in `references/` and the four files in `scripts/` are present
5. Optionally check the runtime dependencies and install only after asking me:
   - `python -c "import PIL"` (Pillow, needed by 2 scripts)
   - `python -c "import playwright"` plus `playwright install chromium`
     (needed only by the screenshot-capture script)
   If a dependency is missing, tell me the command instead of installing silently.
6. Finish with a short report: where the skill was installed, whether dependencies are
   ready, and this one-line usage example:
   "Attach a UI screenshot and say: recreate this in my project and verify the render."

Constraints: do not modify any other skill, do not commit anything to a project repo,
do not push to GitHub, and do not edit the downloaded source.

---

## Prompt B — Offline fallback (GitHub reachable na ho to)

Ye prompt tab use karo jab internet na ho ya repo private/blocked ho. Agent skill ko
khud likh dega, isliye ye lamba hai.

---

Create an agent skill named `screenshot-to-code` on this machine, from scratch. No
network access is required for this task.

Purpose of the skill: teach an agent to convert a UI screenshot, mockup, or screen
recording into working frontend code, and to visually verify the result against the
reference instead of trusting the first draft.

Install it into every agent skills directory that exists, and skip the ones that do
not. Check these paths: `~/.claude/skills/`, `~/.agents/skills/`, `~/.codex/skills/`,
`~/.gemini/skills/`, `~/.copilot/skills/`. If none exist, ask me which agent I use
before creating one. Inside each, create the folder `screenshot-to-code/`.

### File 1 — `SKILL.md`

YAML frontmatter: `name: screenshot-to-code`, and a third-person `description` that
states what the skill does and when it should be used (user supplies a visual
reference and asks for an implementation; a rendered page must be verified against a
reference image; a screen recording must become a prototype).

Body must contain these sections:

- **Purpose** — recreate a visual reference as working frontend code, then verify.
- **When to Use This Skill** — and an explicit "do not use" list (greenfield design
  with no reference; copying someone's proprietary logos or copyrighted content;
  when the user only wants a static mockup rather than runnable code).
- **Core Capabilities** — reference analysis, project inspection, implementation,
  asset extraction, self-verification, iteration.
- **Operating Loop** — eight numbered phases: (1) inspect the target project for
  framework, build system, entry points, styling system, reusable components and
  assets, and the detected dev command; (2) analyze the reference from structure to
  detail — regions, component tree, layout system, type scale, palette, icons and
  images, interactive regions, responsive intent; (3) plan component boundaries,
  layout strategy, breakpoints, assets, dependencies; (4) implement in the project's
  own stack; (5) render and capture the page headlessly at the reference viewport;
  (6) compare the render against the reference and rank the differences; (7) fix the
  largest deviation first and repeat render → capture → compare → fix; (8) report
  files changed, verification performed, and known deviations.
- **Visual Accuracy Priority Order** — fix in this order: overall layout, component
  position, dimensions and spacing, typography, color, images and icons, borders and
  radii, shadows and micro-detail. Never compensate for a wrong layout with extra
  effects.
- **Asset Handling** — priority: asset already in the project, then user-provided,
  then extracted from the reference screenshot, then generated as a last resort.
  Never use a random placeholder when the reference shows a specific visual. Never
  embed the reference screenshot itself as page content.
- **Verification Tiers** — tier 1 headless render plus image diff, tier 2 manual
  browser render described region by region, tier 3 static review only. State that
  tier 3 is a fallback and must be declared as "no visual verification performed".
- **Guardrails** — do not invent UI the reference does not support; do not
  restructure a working project to match a screenshot; do not add dependencies the
  project already provides; do not claim verification that was not performed; do not
  copy proprietary logos or copyrighted imagery; keep API keys in `.env` and never
  commit or log them; remove debug artifacts and leave unrelated files untouched.
- **Limitations** — hover, focus, empty and error states are usually absent from a
  screenshot and must be asked for; the difference image is a visual aid, not a
  pixel-accuracy score.

### File 2 — `references/workflow.md`

The eight-phase loop rewritten as a checkbox checklist, one checklist per phase,
including: detect framework and package manager from lockfiles; locate entry points;
identify styling system and design tokens; list reusable components and existing
assets; record the dev command; capture the reference viewport sizes; fix order
layout → positioning → dimensions → spacing → typography → color → images → borders →
shadows → micro-detail; and a final "application runs clean / debug code removed /
unrelated files untouched / deviations reported" checklist.

### File 3 — `references/generation-rules.md`

These rules must appear, with the exact CDN lines:

- Output discipline: be concise in chat; never paste code into messages, write files
  instead; for a new page write the full file once, for revisions apply targeted edits
  rather than regenerating the whole file; keep one primary artifact (`index.html`
  unless the project dictates otherwise).
- Assets: extract real assets from the reference; if an asset is occluded or is part
  of the background, generate a replacement; never embed the whole screenshot as the
  page; use extracted assets for content imagery only, never for layout; if an asset
  must render larger than its source resolution, upscale it instead of stretching it
  with CSS; image generation cannot produce transparency, so use a dedicated
  background-removal step; batch independent image operations into one pass.
- Targeted element edits: a captured `outerHTML` is a locator, not source — it comes
  from the live DOM, so JSX uses `className`, Vue uses directives and interpolations,
  and Ionic/Bootstrap inject classes at runtime. Match by tag, classes, ids, and text
  content, then change only that element.
- Stack scaffolding, exactly:
  - Tailwind (HTML, React, Vue, Ionic): `<script src="https://cdn.tailwindcss.com"></script>`
  - HTML + CSS: plain HTML, CSS and JS only, no Tailwind
  - Bootstrap: `<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">`
  - React: `https://cdn.jsdelivr.net/npm/react@18.0.0/umd/react.development.js`,
    `https://cdn.jsdelivr.net/npm/react-dom@18.0.0/umd/react-dom.development.js`, and
    Babel pinned **exactly** to `https://unpkg.com/@babel/standalone@7.25.6/babel.min.js`.
    Warn that the unversioned URL now resolves to Babel 8, whose automatic JSX runtime
    injects an `import` that breaks in-browser transforms, and that
    `cdn.babeljs.io/babel.min.js` must not be used.
  - Ionic: `@ionic/core/dist/ionic/ionic.esm.js` (module), `ionic.js` (nomodule), and
    `@ionic/core/css/ionic.bundle.css`; ionicons via
    `https://cdn.jsdelivr.net/npm/ionicons/+esm` plus the nomodule and CSS links.
  - Vue global build: `https://registry.npmmirror.com/vue/3.3.11/files/dist/vue.global.js`,
    mounted with `createApp({ setup() { ... } }).mount('#app')`.
  - Fonts: Google Fonts or other publicly accessible fonts. Icons: Font Awesome
    (`https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css`)
    except for Ionic, which uses ionicons.
- Anti-patterns: embedding the reference screenshot as the page; placeholder image
  services when the reference shows a specific visual; absolute positioning where grid
  or flex works; regenerating an entire file to change one class; adding dependencies
  the project already solves internally; declaring completion without rendering.

### File 4 — `scripts/` (four Python scripts, stdlib plus Pillow/Playwright)

- `inspect_project.py [project-root]` — print JSON with detected framework (next,
  vite, react, vue, svelte from `package.json`), package manager from the lockfile
  (`pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `package-lock.json` → npm), entry
  points (`src/main.tsx`, `src/main.jsx`, `src/main.ts`, `src/main.js`, `src/App.tsx`,
  `src/App.jsx`, `app/page.tsx`, `app/page.jsx`), notable files (`pyproject.toml`,
  `requirements.txt`, `main.py`, `app.py`), and up to 200 image assets
  (`.png .jpg .jpeg .webp .svg .gif .ico`). Skip `.git`, `node_modules`, `dist`,
  `build`, `.next`, `.vite`, `__pycache__`, `.venv`, `venv`.
- `analyze_assets.py [root]` — list supported image files with path, `WxH`, format and
  colour mode; print a clear message when none are found.
- `capture_screenshot.py <url> [output.png]` — Playwright Chromium, viewport
  1440x900, `wait_until="networkidle"`, full-page screenshot, creating parent folders.
- `compare_screenshots.py <reference> <actual> [difference.png]` — pad both images
  onto a common white canvas, compute an absolute difference, boost contrast x3, save.

Each script must take its arguments from the command line, print a helpful usage line
when under-specified, and exit non-zero in that case.

### Verify before finishing

Confirm `SKILL.md` exists in each destination, that its frontmatter parses and
contains `name` and `description`, and that the three `references/` files and four
`scripts/` files are present. Run `python -m py_compile` on the four scripts to prove
they are syntactically valid. Then report what was installed, which skills
directories were used, and the one-line usage example: "Attach a UI screenshot and
say: recreate this in my project and verify the render."

Do not modify any other skill, do not touch any project repository, and do not
install Python packages without asking me first.

---

## Manual install (agent ke bina)

```bash
git clone --depth 1 https://github.com/smrutisourabha4180-afk/screenshot-to-code-skill.git
cp -r screenshot-to-code-skill ~/.claude/skills/screenshot-to-code
```

Windows PowerShell:

```powershell
git clone --depth 1 https://github.com/smrutisourabha4180-afk/screenshot-to-code-skill.git "$env:TEMP\stc-skill"
Copy-Item -Recurse "$env:TEMP\stc-skill" "$env:USERPROFILE\.claude\skills\screenshot-to-code"
```

Dependencies (sirf capture aur compare scripts ke liye zaroori):

```bash
pip install pillow playwright
playwright install chromium
```

## Ek line me

> Ye prompt paste karo, agent khud install kar lega. Phir screenshot bhej kar kaho:
> "recreate this in my project and verify the render."



