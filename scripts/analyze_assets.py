from pathlib import Path
import sys
from PIL import Image

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
}

def analyze(root: Path) -> None:
    if not root.exists():
        raise SystemExit(f"Directory does not exist: {root}")

    found = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        try:
            with Image.open(path) as image:
                found.append({
                    "path": str(path.relative_to(root)),
                    "width": image.width,
                    "height": image.height,
                    "format": image.format,
                    "mode": image.mode,
                })
        except Exception:
            continue

    if not found:
        print("No supported image assets found.")
        return

    print(f"Found {len(found)} image asset(s):\n")

    for asset in found:
        print(
            f"{asset['path']} | "
            f"{asset['width']}x{asset['height']} | "
            f"{asset['format']} | "
            f"{asset['mode']}"
        )


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    analyze(root)


if __name__ == "__main__":
    main()