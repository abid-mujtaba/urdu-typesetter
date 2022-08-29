"""Build html artifact from source."""

import os
from pathlib import Path
from shutil import copy, copytree

from .inject import inject
from .source import read


def build(source: str, create_artifact: bool = True) -> None:
    """Build the html artifact."""
    build_dir = Path("/") / "build" / "html"
    template_file = Path("/") / "templates" / "common" / "story.html.template"

    _pre_populate_build(build_dir)

    data = read(Path(source))
    text = inject(template_file, data)
    _create_html(build_dir, text)

    if create_artifact:
        _copy_artifact(build_dir)


def _pre_populate_build(build_dir: Path):
    """Create a build folder and copy over assets."""
    if build_dir.exists():  # Clean up if present
        build_dir.rmdir()

    build_dir.mkdir()
    assets = Path("/") / "assets"

    copytree(assets, build_dir / "assets")


def _create_html(build_dir: Path, text: str) -> None:
    """Create html file from injected template text."""
    tex_file = build_dir / "story.html"
    tex_file.write_text(text)


def _copy_artifact(build_dir: Path) -> None:
    """Copy generated artifact to the current folder."""
    copy(build_dir / "story.html", Path.cwd())
    os.chown(
        Path.cwd() / "story.html", 1000, 1000
    )  # chown artifact to avoid root-owned

    assets = Path.cwd() / "assets"
    if assets.exists():
        assets.rmdir()

    copytree(Path("/") / "assets", assets)
    os.system("chown -R 1000:1000 ./assets")
