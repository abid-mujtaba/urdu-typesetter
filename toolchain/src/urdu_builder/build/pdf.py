"""Build the pdf artifact."""

import os
from pathlib import Path
from shutil import copy, rmtree
import subprocess

from .inject import inject
from .source import read


def build(source: str) -> None:
    """Build the pdf artifact."""
    build_dir = Path("/") / "build" / "pdf"
    template_file = Path("/") / "templates" / "pdf" / "story.tex.template"

    _pre_populate_build(build_dir)

    data = read(Path(source))
    text = inject(template_file, data)
    _create_tex(build_dir, text)

    _create_pdf(build_dir)
    _copy_artifact(build_dir)


def _pre_populate_build(build_dir: Path):
    """Create a build folder and copy over assets."""
    if build_dir.exists():  # Clean up if present
        rmtree(build_dir)

    build_dir.mkdir()
    assets = Path("/") / "assets"

    copy(assets / "fonts" / "jameel-noori-nastaleeq.ttf", build_dir)


def _create_tex(build_dir: Path, text: str) -> None:
    """Create tex file from injected template text."""
    tex_file = build_dir / "story.tex"
    tex_file.write_text(text)


def _create_pdf(build_dir: Path) -> None:
    """Create pdf file from tex file using xelatex."""
    cmd = ["xelatex", "story.tex"]
    subprocess.run(cmd, cwd=build_dir, check=True)


def _copy_artifact(build_dir: Path) -> None:
    """Copy generated artifact to the current folder."""
    copy(build_dir / "story.pdf", Path.cwd())
    os.chown(Path.cwd() / "story.pdf", 1000, 1000)  # chown artifact to avoid root-owned
