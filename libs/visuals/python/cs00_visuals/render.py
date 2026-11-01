# Copyright (C) 2026 SGo-Go. All rights reserved.
"""Render registered scenes to MP4 videos and PNG stills.

Run from the repository root:

    python -m cs00_visuals.render                 # all scenes, video and still
    python -m cs00_visuals.render --still-only    # stills only, fast
    python -m cs00_visuals.render --quality youtube --only BinaryCounting
"""

import argparse
import re
import shutil
import tempfile
from pathlib import Path

from manim import Scene, tempconfig

from .scenes import SCENES
from .style import BACKGROUND

# Manim quality presets: draft 480p15, web 720p30, youtube 1080p60, 4k 2160p60.
QUALITIES: dict[str, str] = {
    "draft": "low_quality",
    "web": "medium_quality",
    "youtube": "high_quality",
    "4k": "fourk_quality",
}

DEFAULT_OUTPUT = Path("docs/quarto/media/visuals")


def slug(scene_class: type[Scene]) -> str:
    """Turn a scene class name into a file name, e.g. `BinaryCounting` -> `binary-counting`."""
    return re.sub(r"(?<!^)(?=[A-Z])", "-", scene_class.__name__).lower()


def render_scene(scene_class: type[Scene], output_dir: Path, quality: str, *, movie: bool) -> Path:
    """Render one scene as an MP4 video or as a PNG of its last frame and copy it to `output_dir`."""
    with tempfile.TemporaryDirectory() as media_dir:
        options: dict[str, object] = {
            "quality": QUALITIES[quality],
            "background_color": BACKGROUND,
            "media_dir": media_dir,
            "disable_caching": True,
            "progress_bar": "none",
            "verbosity": "WARNING",
            "write_to_movie": movie,
            "save_last_frame": not movie,
        }
        if movie:
            options["format"] = "mp4"
        with tempconfig(options):
            scene = scene_class()
            scene.render()
            writer = scene.renderer.file_writer
            source = Path(writer.movie_file_path if movie else writer.image_file_path)
            target = output_dir / f"{slug(scene_class)}{source.suffix}"
            shutil.copyfile(source, target)
    return target


def main() -> None:
    """Parse arguments and render the selected scenes."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--quality", choices=QUALITIES, default="web", help="output resolution (default: web)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="output folder (default: %(default)s)")
    parser.add_argument("--only", nargs="+", metavar="SCENE", help="scene class names to render")
    kind = parser.add_mutually_exclusive_group()
    kind.add_argument("--still-only", action="store_true", help="render PNG stills only")
    kind.add_argument("--movie-only", action="store_true", help="render MP4 videos only")
    args = parser.parse_args()

    scenes = [scene for scene in SCENES if not args.only or scene.__name__ in args.only]
    unknown = set(args.only or []) - {scene.__name__ for scene in SCENES}
    if unknown:
        parser.error(f"unknown scenes: {', '.join(sorted(unknown))}")

    args.output.mkdir(parents=True, exist_ok=True)
    for scene_class in scenes:
        if not args.still_only:
            print(render_scene(scene_class, args.output, args.quality, movie=True))
        if not args.movie_only:
            print(render_scene(scene_class, args.output, args.quality, movie=False))


if __name__ == "__main__":
    main()
