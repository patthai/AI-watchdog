#!/usr/bin/env python3
"""
Reverse transition GIFs:
  sleep-to-bark-[x].gif  →  bark-to-sleep-[x].gif
  sleep-to-idle-[x].gif  →  idle-to-sleep-[x].gif
  sleep-to-talk-[x].gif  →  talk-to-sleep-[x].gif

Input/Output: AI-watchdog/images/gif-transparent/
"""

import re
from pathlib import Path
from PIL import Image

GIF_DIR = Path(__file__).parent.parent / "images" / "gif-transparent"

TRANSITIONS = {
    "sleep-to-bark": "bark-to-sleep",
    "sleep-to-idle": "idle-to-sleep",
    "sleep-to-talk": "talk-to-sleep",
}

PATTERN = re.compile(r"^(sleep-to-(?:bark|idle|talk))-(\d+)\.gif$")


def reverse_gif(src: Path, dst: Path) -> None:
    gif = Image.open(src)
    frames = []
    durations = []

    for i in range(gif.n_frames):
        gif.seek(i)
        durations.append(gif.info.get("duration", 100))
        frames.append(gif.convert("RGBA").copy())

    frames.reverse()
    durations.reverse()

    frames[0].save(
        dst,
        save_all=True,
        append_images=frames[1:],
        loop=gif.info.get("loop", 0),
        duration=durations,
        disposal=2,
        format="GIF",
    )
    print(f"  {src.name}  →  {dst.name}")


def main():
    matches = [f for f in sorted(GIF_DIR.glob("*.gif")) if PATTERN.match(f.name)]
    if not matches:
        print(f"No matching transition GIFs found in {GIF_DIR}")
        return

    print(f"Reversing {len(matches)} transition GIF(s)...")
    for src in matches:
        m = PATTERN.match(src.name)
        prefix, number = m.group(1), m.group(2)
        new_prefix = TRANSITIONS[prefix]
        dst = GIF_DIR / f"{new_prefix}-{number}.gif"
        reverse_gif(src, dst)

    print("Done.")


if __name__ == "__main__":
    main()
