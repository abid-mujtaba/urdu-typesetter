"""Build the pdf artifact."""

from pathlib import Path
from shutil import copy


def build(source: str) -> None:
    """Build the pdf artifact."""
    build_dir = Path("/") / "build" / "pdf"

    pre_populate_build(build_dir)
    inject_template(build_dir)


def pre_populate_build(build_dir: Path):
    """Create a build folder and copy over assets."""
    if build_dir.exists():  # Clean up if present
        build_dir.rmdir()

    build_dir.mkdir()
    assets = Path("/") / "assets"

    copy(assets / "fonts" / "jameel-noori-nastaleeq.ttf", build_dir)


def inject_template(build_dir: Path):
    """Inject source data into template."""
