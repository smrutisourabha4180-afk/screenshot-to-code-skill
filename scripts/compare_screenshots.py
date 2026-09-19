from pathlib import Path
import sys

from PIL import Image, ImageChops, ImageEnhance


def compare(reference_path: str, actual_path: str, output_path: str) -> None:
    reference = Image.open(reference_path).convert("RGB")
    actual = Image.open(actual_path).convert("RGB")

    width = max(reference.width, actual.width)
    height = max(reference.height, actual.height)

    reference_canvas = Image.new("RGB", (width, height), "white")
    actual_canvas = Image.new("RGB", (width, height), "white")

    reference_canvas.paste(reference, (0, 0))
    actual_canvas.paste(actual, (0, 0))

    difference = ImageChops.difference(
        reference_canvas,
        actual_canvas
    )

    difference = ImageEnhance.Contrast(difference).enhance(3.0)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    difference.save(output_path)

    print(f"Comparison saved: {output_path}")


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage: python compare_screenshots.py "
            "<reference.png> <actual.png> [difference.png]"
        )
        raise SystemExit(1)

    reference = sys.argv[1]
    actual = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else "difference.png"

    compare(reference, actual, output)


if __name__ == "__main__":
    main()