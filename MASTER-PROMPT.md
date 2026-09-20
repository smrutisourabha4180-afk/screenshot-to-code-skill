# MASTER PROMPT — install this skill into yourself

Ek hi prompt, kisi bhi agent ke liye (Claude Code, Codex, Cline, Gemini CLI, Copilot,
opencode, Continue, Crush, Kilo, Mimo, Vibe, ya koi bhi). Agent khud ko pehchan kar
apne skills folder me install kar lega.

Source repo (public, MIT):
`https://github.com/smrutisourabha4180-afk/screenshot-to-code-skill`

---

## The prompt — copy everything below this line

---

You are an AI coding agent. Install the `screenshot-to-code` skill **into your own
skills directory**, so that you can use it in future sessions. Do not ask me
questions unless a step below tells you to; otherwise just do it.

### Step 1 — Identify your skills directory

First run this to see which skill directories exist on this machine (Windows: use
PowerShell equivalents, `$HOME` is `C:\Users\<name>`):

```bash
for d in ~/.claude/skills ~/.codex/skills ~/.cline/skills ~/.gemini/skills \
         ~/.copilot/skills ~/.config/opencode/skills ~/.continue/skills \
         ~/.crush/skills ~/.kilocode/skills ~/.mimo/skills ~/.vibe/skills \
         ~/.agents/skills; do
  [ -d "$d" ] && echo "EXISTS: $d"
done
```

Then pick your own directory using this table:

| If you are | Your skills directory |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Codex CLI | `~/.codex/skills/` |
| Cline | `~/.cline/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| GitHub Copilot CLI | `~/.copilot/skills/` |
| opencode | `~/.config/opencode/skills/` |
| Continue | `~/.continue/skills/` |
| Crush | `~/.crush/skills/` |
| Kilo Code | `~/.kilocode/skills/` |
| Mimo | `~/.mimo/skills/` |
| Vibe | `~/.vibe/skills/` |
| anything else, or unsure | `~/.agents/skills/` (the shared hub most agents read) |

If your directory does not exist yet, create it. If several exist and you truly cannot
tell which is yours, install into `~/.agents/skills/` and tell me that you did.

### Step 2 — Download the skill

```bash
git clone --depth 1 https://github.com/smrutisourabha4180-afk/screenshot-to-code-skill.git /tmp/stc-skill
```

If `git` is unavailable, download and unzip the `main` branch archive instead. If
there is no network access at all, stop and tell me — do not invent the skill
contents from memory.

### Step 3 — Install into yourself

Copy `SKILL.md`, `README.md`, `INSTALL-PROMPT.md`, `MASTER-PROMPT.md`,
`references/`, and `scripts/` into:

```
<your skills directory>/screenshot-to-code/
```

Exclude `.git`, `.gitignore`, and any `__pycache__`. If a
`screenshot-to-code` folder is already there, replace it — an older copy may exist,
and the newest version is the correct one.

### Step 4 — Verify, and report PASS or FAIL for each check

1. `screenshot-to-code/SKILL.md` exists.
2. Its YAML frontmatter parses and contains `name: screenshot-to-code` and a
   `description`.
3. `references/` contains 3 files, including `generation-rules.md` and
   `repo-reference.md`.
4. `scripts/` contains 4 files: `inspect_project.py`, `analyze_assets.py`,
   `capture_screenshot.py`, `compare_screenshots.py`.
5. Run `python -m py_compile` on those 4 scripts — they must compile.
6. No `.git` folder and no `__pycache__` inside the installed skill.

### Step 5 — Dependencies (ask me first, never install silently)

Only two scripts need extra packages:

- Pillow → `python -c "import PIL"`
- Playwright → `python -c "import playwright"` plus `playwright install chromium`

Check them, and if something is missing simply tell me the install command. Do not run
it without my confirmation.

### Step 6 — Report

- Which agent you are, and the exact directory you installed into
- The PASS/FAIL result of each check in Step 4
- Whether the two optional dependencies are present
- Then confirm you are ready, using this example:

> Attach a UI screenshot and say: "recreate this in my project and verify the render."

### Rules

- Do not modify, delete, or overwrite any other skill.
- Do not touch any of my project repositories.
- Do not commit or push anything to GitHub.
- Do not install Python packages without asking.
- Keep the downloaded copy out of my project folders.

---

## Bonus — install into every agent on this machine

Master prompt ke saath ye ek line add kar do, to sirf apne andar nahi, **saare**
agents me install karega:

> Instead of installing only into your own directory, install into every existing
> skills directory from the Step 1 list, one copy each.

---

## Shortest version (jab sab pata ho)

Agar sirf link share karna hai:

> Read this file and follow it to install the skill into your own skills directory:
> `https://github.com/smrutisourabha4180-afk/screenshot-to-code-skill/blob/main/MASTER-PROMPT.md`
