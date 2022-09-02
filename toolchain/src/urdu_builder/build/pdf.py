"""Build the pdf artifact."""

import os
from pathlib import Path
from shutil import copy, rmtree
import subprocess

from .inject import inject
from .source import artifact_name, read_source


def build(source_dir: str) -> None:
    """Build the pdf artifact."""
    build_dir = Path("/") / "build" / "pdf"
    template_file = Path("/") / "templates" / "pdf" / "source.tex.template"

    source = Path(source_dir)
    filename = f"{artifact_name(source)}.pdf"

    _pre_populate_build(build_dir)

    data = read_source(source)
    text = inject(template_file, data, tex=True)
    _create_tex(build_dir, text)

    _create_pdf(build_dir)
    _copy_artifact(build_dir, filename)


def _pre_populate_build(build_dir: Path):
    """Create a build folder and copy over assets."""
    if build_dir.exists():  # Clean up if present
        rmtree(build_dir)

    build_dir.mkdir()
    assets = Path("/") / "assets"

    copy(assets / "fonts" / "jameel-noori-nastaleeq.ttf", build_dir)


def _create_tex(build_dir: Path, text: str) -> None:
    """Create tex file from injected template text."""
    tex_file = build_dir / "source.tex"
    tex_file.write_text(text)


def _create_pdf(build_dir: Path) -> None:
    """Create pdf file from tex file using xelatex."""
    cmd = ["xelatex", "source.tex"]
    subprocess.run(cmd, cwd=build_dir, check=True)


def _copy_artifact(build_dir: Path, filename: str) -> None:
    """Copy generated artifact to the current folder."""
    copy(build_dir / "source.pdf", Path.cwd() / filename)
    os.chown(Path.cwd() / filename, 1000, 1000)  # chown artifact to avoid root-owned
