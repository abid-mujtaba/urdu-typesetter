"""Build sub-package."""

from . import pdf


def build(format: str, source_dir: str) -> None:
    """Build the specified format(s) artifact."""
    match format:
        case "pdf":
            pdf.build(source_dir)
