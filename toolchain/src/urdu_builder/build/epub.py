"""Create epub artifact from yaml source."""

import os
from pathlib import Path
from shutil import copy, copytree, rmtree
from zipfile import ZipFile

from .inject import inject
from .source import Data, artifact_name, read_source


def build(source_dir: str, include_font: bool = False) -> None:
    """Build epub artifact from yaml in source_dir."""
    build_dir = Path("/") / "build" / "epub"
    source = Path(source_dir)
    filename = f"{artifact_name(source)}.epub"

    _pre_populate_build(build_dir, include_font)
    data = read_source(source)
    data["font"] = include_font

    if (source / "cover.tiff").exists():
        _copy_cover(source, build_dir)
        data["cover"] = True  # Used in template to include tag for cover in content.opf
    else:
        data["cover"] = False

    _create_oebps_file(data, "content.opf", build_dir)
    _create_oebps_file(data, "source.html", build_dir)
    _create_oebps_file(data, "toc.html", build_dir)
    _create_oebps_file(data, "toc.ncx", build_dir)

    _create_css_file(include_font, build_dir)

    _create_epub(build_dir, filename)


def _pre_populate_build(build_dir: Path, include_font: bool = False) -> None:
    """Remove and then pre-populate build folder for epub."""
    if build_dir.exists():  # Clean up if present
        rmtree(build_dir)

    build_dir.mkdir()

    # Define asset and template sources
    assets = Path("/") / "assets"
    templates = Path("/") / "templates" / "epub"

    # Create empty folders for later data injection
    (build_dir / "OEBPS").mkdir()
    (build_dir / "OEBPS" / "assets").mkdir()
    (build_dir / "OEBPS" / "assets" / "imgs").mkdir()
    (build_dir / "OEBPS" / "assets" / "css").mkdir()

    if include_font:
        fonts_dir = build_dir / "OEBPS" / "assets" / "fonts"
        fonts_dir.mkdir()
        copy(
            assets / "fonts" / "jameel-noori-nastaleeq.ttf",
            fonts_dir,
        )

    # Copy template sources that do NOT require data injection into build folder
    copy(templates / "mimetype", build_dir)
    copytree(templates / "META-INF", build_dir / "META-INF")


def _create_oebps_file(data: Data, filename: str, build_dir: Path) -> None:
    """Inject data into template to create file in OEBPS."""
    text = inject(
        Path("/") / "templates" / "epub" / "OEBPS" / f"{filename}.template", data
    )
    (build_dir / "OEBPS" / filename).write_text(text)


def _create_css_file(include_font: bool, build_dir: Path) -> None:
    """Inject data into urdu.css template and add to OEBPS."""
    text = inject(
        Path("/") / "templates" / "common" / "assets" / "css" / "urdu.css",
        {"font": include_font},
    )
    (build_dir / "OEBPS" / "assets" / "css" / "urdu.css").write_text(text)


def _copy_cover(source: Path, build_dir: Path) -> None:
    """Copy the cover image into build folder."""
    copy(source / "cover.tiff", build_dir / "OEBPS" / "assets" / "imgs")


def _create_epub(build_dir: Path, filename: str):
    """Create epub file by zipping up the contents of the build folder."""
    original = Path.cwd()

    try:
        os.chdir(build_dir)

        with ZipFile(original / filename, "w") as zip:
            for path in build_dir.glob("**/*"):
                if path.is_file():
                    zip.write(path.relative_to(build_dir))

    finally:
        os.chdir(original)

    os.chown(Path.cwd() / filename, 1000, 1000)
