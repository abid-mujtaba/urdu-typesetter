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

    server = Server()
    server.watch(str(data_file), lambda: html.build(source_dir, create_artifact=False))

    server.serve(
        root="/build/html", default_filename=filename, host="0.0.0.0", port=8000
    )
