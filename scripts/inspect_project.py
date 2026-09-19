from pathlib import Path
import json
import sys


IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".vite",
    "__pycache__",
    ".venv",
    "venv",
}


def detect_project(root: Path) -> dict:
    result = {
        "root": str(root.resolve()),
        "framework": "unknown",
        "package_manager": "unknown",
        "entry_points": [],
        "important_files": [],
        "assets": [],
    }

    package_json = root / "package.json"

    if package_json.exists():
        result["important_files"].append("package.json")

        try:
            data = json.loads(
                package_json.read_text(encoding="utf-8")
            )

            scripts = data.get("scripts", {})

            deps = {
                **data.get("dependencies", {}),
                **data.get("devDependencies", {}),
            }

            if "next" in deps:
                result["framework"] = "Next.js"
            elif "vite" in deps:
                result["framework"] = "Vite"
            elif "react" in deps:
                result["framework"] = "React"
            elif "vue" in deps:
                result["framework"] = "Vue"
            elif "svelte" in deps:
                result["framework"] = "Svelte"

            if (root / "pnpm-lock.yaml").exists():
                result["package_manager"] = "pnpm"
            elif (root / "yarn.lock").exists():
                result["package_manager"] = "yarn"
            elif (root / "package-lock.json").exists():
                result["package_manager"] = "npm"

            entry_candidates = [
                "src/main.tsx",
                "src/main.jsx",
                "src/main.ts",
                "src/main.js",
                "src/App.tsx",
                "src/App.jsx",
                "app/page.tsx",
                "app/page.jsx",
            ]

            for name in entry_candidates:
                if (root / name).exists():
                    result["entry_points"].append(name)

            if "dev" in scripts:
                result["important_files"].append(
                    "dev script available"
                )

        except (json.JSONDecodeError, OSError) as error:
            result["important_files"].append(
                f"package.json read error: {error}"
            )

    for name in (
        "pyproject.toml",
        "requirements.txt",
        "main.py",
        "app.py",
    ):
        if (root / name).exists():
            result["important_files"].append(name)

    if (root / "pyproject.toml").exists():
        if result["framework"] == "unknown":
            result["framework"] = "Python project"

    asset_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".svg",
        ".gif",
        ".ico",
    }

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in IGNORE_DIRS for part in path.parts):
            continue

        if path.suffix.lower() in asset_extensions:
            result["assets"].append(
                str(path.relative_to(root))
            )

    result["assets"] = result["assets"][:200]

    return result


def main() -> None:
    root = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path.cwd()
    )

    if not root.exists():
        raise SystemExit(
            f"Project does not exist: {root}"
        )

    result = detect_project(root)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()