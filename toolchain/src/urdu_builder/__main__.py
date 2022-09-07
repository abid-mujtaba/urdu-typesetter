"""Entrypoint for module executed as script."""


from argparse import ArgumentParser

from . import build
from . import preview


def parse_args():
    """Parse CLI args."""
    parser = ArgumentParser(
        description="Build/Preview Urdu literature artifacts from yaml source"
    )

    subparsers = parser.add_subparsers()

    source_dir_config = {
        "nargs": "?",
        "default": ".",
        "type": str,
        "help": "Folder containing the yaml source files",
    }

    sp_preview = subparsers.add_parser("preview")
    sp_preview.set_defaults(func=preview.preview)
    sp_preview.add_argument("source_dir", **source_dir_config)

    sp_build = subparsers.add_parser("build")
    sp_build.set_defaults(func=build.build)
    sp_build.add_argument(
        "--format",
        type=str,
        choices=("all", "epub", "html", "pdf"),
        default="all",
        help="Type of artifact to generate",
    )
    sp_build.add_argument("--include-font", action="store_true")
    sp_build.add_argument("source_dir", **source_dir_config)

    kwargs = vars(parser.parse_args())

    func = kwargs.pop("func")
    func(**kwargs)


def main():
    """Entrypoint of script."""
    parse_args()


if __name__ == "__main__":
    main()
