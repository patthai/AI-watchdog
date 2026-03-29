#!/usr/bin/env python3
"""
Remove white background from GIFs and save as transparent GIFs.
Input:  AI-watchdog/images/gif-white-bg/
Output: AI-watchdog/images/gif-transparent/
"""

import os
from pathlib import Path
from PIL import Image
import numpy as np

INPUT_DIR = Path(__file__).parent.parent / "images" / "gif-white-bg"
OUTPUT_DIR = Path(__file__).parent.parent / "images" / "gif-transparent"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def remove_white_background(frame: Image.Image, threshold: int = 240) -> Image.Image:
    """Convert near-white pixels to transparent in an RGBA frame."""
    frame = frame.convert("RGBA")
    data = np.array(frame)
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    white_mask = (r >= threshold) & (g >= threshold) & (b >= threshold)
    data[:, :, 3] = np.where(white_mask, 0, a)
    return Image.fromarray(data, "RGBA")


def process_gif(src: Path, dst: Path) -> None:
    gif = Image.open(src)
    frames = []
    durations = []

    for i in range(gif.n_frames):
        gif.seek(i)
        duration = gif.info.get("duration", 100)
        frame = remove_white_background(gif.convert("RGBA"))
        frames.append(frame)
        durations.append(duration)

    frames[0].save(
        dst,
        save_all=True,
        append_images=frames[1:],
        loop=gif.info.get("loop", 0),
        duration=durations,
        disposal=2,
        format="GIF",
    )
    print(f"  saved → {dst.name}")


def main():
    gif_files = sorted(INPUT_DIR.glob("*.gif"))
    if not gif_files:
        print(f"No GIFs found in {INPUT_DIR}")
        return

    print(f"Processing {len(gif_files)} GIF(s)...")
    for src in gif_files:
        dst = OUTPUT_DIR / src.name
        process_gif(src, dst)
    print("Done.")


if __name__ == "__main__":
    main()
