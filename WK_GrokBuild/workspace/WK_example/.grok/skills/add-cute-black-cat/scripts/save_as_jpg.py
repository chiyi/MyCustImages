#!/usr/bin/env python3
"""Save an image as JPEG (minimal file-handling helper)."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: save_as_jpg.py <source_image> <output.jpg>", file=sys.stderr)
        return 2

    source = Path(sys.argv[1]).resolve()
    dest = Path(sys.argv[2]).resolve()

    if not source.is_file():
        print(f"error: source not found: {source}", file=sys.stderr)
        return 1

    try:
        from PIL import Image
    except ImportError:
        print(
            "error: Pillow required. Install with: pip install --break-system-packages Pillow",
            file=sys.stderr,
        )
        return 1

    dest.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as img:
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")
        img.save(dest, format="JPEG", quality=90, optimize=True)

    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())