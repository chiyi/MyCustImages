#!/usr/bin/env python3
"""Resolve input image path and output filename for add-cute-black-cat."""

from __future__ import annotations

import json
import sys
from pathlib import Path

IMAGE_SUFFIXES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".bmp",
    ".tiff",
    ".tif",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: resolve_paths.py <image_path>", file=sys.stderr)
        return 2

    raw = Path(sys.argv[1]).expanduser()
    if not raw.is_absolute():
        raw = (Path.cwd() / raw).resolve()
    else:
        raw = raw.resolve()

    if not raw.is_file():
        print(f"error: file not found: {raw}", file=sys.stderr)
        return 1

    if raw.suffix.lower() not in IMAGE_SUFFIXES:
        print(
            f"warning: uncommon image extension {raw.suffix!r}; proceeding anyway",
            file=sys.stderr,
        )

    stem = raw.stem
    output = Path.cwd() / f"{stem}_with_cat.jpg"

    print(
        json.dumps(
            {
                "input": str(raw),
                "output": str(output.resolve()),
                "stem": stem,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())