"""Build html artifact from source."""

import os
from pathlib import Path
from shutil import copy, copytree, rmtree

from .inject import inject
from .source import artifact_name, Data, read_format, read_source


def build(source_dir: str, create_artifact: bool = True) -> str:
    """Build the html artifact and return name of html file."""
    build_dir = Path("/") / "build" / "html"

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

    _create_html(data, build_dir, filename)
    _create_css(build_dir)

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

    (build_dir / "assets" / "css").mkdir()


def _create_html(data: Data, build_dir: Path, filename: str) -> None:
    """Create html file from injected template text."""
    template_file = Path("/") / "templates" / "common" / "source.html.template"
    text = inject(template_file, data)

    html_file = build_dir / filename
    html_file.write_text(text)


def _create_css(build_dir: Path) -> None:
    """Create urdu.css file from template."""
    template_file = Path("/") / "templates" / "common" / "assets" / "css" / "urdu.css"
    text = inject(template_file, {"font": True})

    css_file = build_dir / "assets" / "css" / "urdu.css"
    css_file.write_text(text)


def _copy_artifact(build_dir: Path, filename: str) -> None:
    """Copy generated artifact to the current folder."""
    copy(build_dir / filename, Path.cwd())
    os.chown(Path.cwd() / filename, 1000, 1000)  # chown artifact to avoid root-owned

    assets = Path.cwd() / "assets"
    if assets.exists():
        rmtree(assets)

    copytree(Path("/") / "assets", assets)
    os.system("chown -R 1000:1000 ./assets")
