"""Build sub-package."""

from . import epub
from . import html
from . import pdf


def build(format: str, source_dir: str, include_font: bool = False) -> None:
    """Build the specified format(s) artifact."""
    match format:
        case "epub":
            epub.build(source_dir, include_font)
        case "html":
            html.build(source_dir)
        case "pdf":
            pdf.build(source_dir)
        case "all":
            epub.build(source_dir, include_font)
            html.build(source_dir)
            pdf.build(source_dir)
