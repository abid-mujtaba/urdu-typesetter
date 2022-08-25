"""Create a livereload preview of the rendered HTML."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from livereload import Server, shell


def get_source() -> str:
    """Parse CLI args."""
    parser = ArgumentParser(description="Build HTML version of literature")
    parser.add_argument(
        "source",
        type=str,
        help="Source identifier in the form <author>/<literature-name>"
        "which are folders under data/ e.g. ghulam-abbas/aanandi",
    )

    args = parser.parse_args()
    return args.source


def main():
    """Entrypoint of script."""
    source = get_source()
    command = f"{sys.executable} build.py {source}"

    data_file = Path.cwd().parent.parent / "data" / source / "story.yaml"
    css_file = Path.cwd() / "template" / "assets" / "css" / "urdu.css"

    server = Server()
    server.watch(str(data_file), shell(command))
    server.watch(str(css_file), shell(command))

    server.serve(root="build", host="localhost", port=8000)


if __name__ == "__main__":
    main()
