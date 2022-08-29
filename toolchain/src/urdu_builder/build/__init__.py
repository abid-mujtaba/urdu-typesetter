"""Build sub-package."""

from . import html
from . import pdf


def build(format: str, source_dir: str) -> None:
    """Build the specified format(s) artifact."""
    match format:
        case "html":
            html.build(source_dir)
        case "pdf":
            pdf.build(source_dir)
