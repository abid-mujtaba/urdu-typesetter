"""Live reloadable preview of the html artifact."""

from pathlib import Path

from livereload import Server

from .build import html


def preview(source_dir: str):
    """Create live reloadable preview of the html artifact."""
    # Start by building the html artifact
    filename = html.build(source_dir, create_artifact=False)

    source = Path(source_dir)
    data_file = source / "source.yaml"
    format_file = source / "format.yaml"

    server = Server()

    for file in map(str, (data_file, format_file)):
        server.watch(file, lambda: html.build(source_dir, create_artifact=False))

    server.serve(
        root="/build/html", default_filename=filename, host="0.0.0.0", port=8000
    )
