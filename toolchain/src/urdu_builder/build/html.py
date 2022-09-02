"""Build html artifact from source."""

import os
from pathlib import Path
from shutil import copy, copytree, rmtree

from .inject import inject
from .source import artifact_name, read_format, read_source


def build(source_dir: str, create_artifact: bool = True) -> str:
    """Build the html artifact and return name of html file."""
    build_dir = Path("/") / "build" / "html"
    template_file = Path("/") / "templates" / "common" / "source.html.template"

    source = Path(source_dir)
    filename = f"{artifact_name(source)}.html"

    _pre_populate_build(build_dir)

    data = read_source(source)
    fmt = read_format(source)

    try:
        if fmt:
            data["format"] = {"width": fmt["poetry"]["html"]["width"]}

    except KeyError:
        pass

    text = inject(template_file, data)
    _create_html(build_dir, filename, text)

    if create_artifact:
        _copy_artifact(build_dir, filename)

    return filename


def _pre_populate_build(build_dir: Path):
    """Create a build folder and copy over assets."""
    if build_dir.exists():  # Clean up if present
        rmtree(build_dir)

    build_dir.mkdir()
    assets = Path("/") / "assets"

    copytree(assets, build_dir / "assets")


def _create_html(build_dir: Path, filename: str, text: str) -> None:
    """Create html file from injected template text."""
    tex_file = build_dir / filename
    tex_file.write_text(text)


def _copy_artifact(build_dir: Path, filename: str) -> None:
    """Copy generated artifact to the current folder."""
    copy(build_dir / filename, Path.cwd())
    os.chown(Path.cwd() / filename, 1000, 1000)  # chown artifact to avoid root-owned

    assets = Path.cwd() / "assets"
    if assets.exists():
        rmtree(assets)

    copytree(Path("/") / "assets", assets)
    os.system("chown -R 1000:1000 ./assets")
