# Screenshot to Code — Agent Skill

A reusable agent skill for converting UI screenshots, mockups, and screen recordings into accurate, runnable frontend implementations — plus full operating instructions for the [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code) application it is derived from.

## What it does

Given a visual reference, the agent:

1. Inspects the target project (framework, styling system, reusable components, assets)
2. Analyzes the reference (layout, components, type, color, assets, states)
3. Plans component and layout structure
4. Implements in the project's own stack
5. Renders the page headlessly and captures a screenshot
6. Diffs the render against the reference
7. Fixes the largest deviation first and repeats
8. Reports files changed, verification performed, and known deviations

It also covers running and extending the upstream app: local setup, API keys, stacks, models, prompts, and evals.

## Install

Copy or symlink this folder into your agent's skills directory:

```bash
# Claude Code
ln -s "$PWD" ~/.claude/skills/screenshot-to-code      # macOS/Linux
# Windows (PowerShell, admin)
New-Item -ItemType Junction -Path "$HOME\.claude\skills\screenshot-to-code" -Target "$PWD"
```

Any agent that reads `SKILL.md` from a skills folder can use it.

## Usage

Ask the agent with a screenshot attached:

> Recreate this screenshot in my React + Tailwind app, then verify it renders the same.

> Turn this screen recording into a working prototype page.

> This design is slightly off — the sidebar is too wide and the heading is too small. Fix it and re-verify.

## Structure

```text
screenshot-to-code-skill/
├── SKILL.md                        # Entry point: when to use, operating loop, guardrails
├── README.md                       # Install and usage
├── INSTALL-PROMPT.md               # Shareable prompt: installs by cloning this repo
├── MASTER-PROMPT.md                # Shareable prompt: any agent installs into itself
├── references/
│   ├── workflow.md                 # Phased checklist form of the loop
│   ├── generation-rules.md         # Output discipline, asset rules, stack scaffolding
│   └── repo-reference.md           # Upstream repo map, commands, config, evals, gotchas
└── scripts/
    ├── inspect_project.py          # Detect framework, package manager, entry points, assets
    ├── analyze_assets.py           # Inventory image assets (size, format, mode)
    ├── capture_screenshot.py       # Headless Chromium render (1440×900, full page)
    └── compare_screenshots.py      # Contrast-boosted difference image
```

## Requirements

- Python 3.10+ for the scripts
- `playwright` + Chromium for `capture_screenshot.py`
- `pillow` for `compare_screenshots.py` and `analyze_assets.py`
- Python 3.10+, Poetry, Node + pnpm, and at least one model API key if you intend to run the upstream app itself

## Source and license

Methodology and prompt rules derived from [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code), MIT licensed. This skill is an independent documentation layer; it ships no upstream code.
