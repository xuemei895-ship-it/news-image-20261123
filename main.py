#!/usr/bin/env python3
"""make.fun bounty entry: news-image-20261123.

"Sum up 23 November's world news in one image."

The entry is a program that writes one image to /output/entry.png.
The bounty brief explicitly allows the simplest form of this program:
"the simplest program copies an image the repository holds".

So this program copies assets/entry.png (a 1024x1024 PNG generated
offline by generate.py in this repository from verified 23 Nov 2026
news — see SOURCES.md) into the grader's output directory.

Pure standard library only: no network, no randomness, no wall-clock
time, no third-party packages. Two runs write byte-identical output.

Run by the grader as:  python3 -P -s /bot/main.py
Output directory: $MAKEFUN_OUTPUT_DIR (default /output).
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "assets", "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    size = os.path.getsize(dest)
    with open(dest, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    # Sanity: the image must be a whole PNG under 1 MiB.
    if size > 1024 * 1024:
        print(f"entry.png is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
