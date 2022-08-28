"""Entrypoint for module executed as script."""


from argparse import ArgumentParser


def parse_args():
    """Parse CLI args."""
    parser = ArgumentParser(
        description="Build/Preview Urdu literature artifacts from yaml source"
    )

    subparsers = parser.add_subparsers()

    preview = subparsers.add_parser("preview")
    preview.set_defaults(func=preview_func)
    preview.add_argument(
        "source_dir",
        nargs="?",
        default=".",
        type=str,
        help="Folder containing the yaml source files",
    )

    build = subparsers.add_parser("build")
    build.set_defaults(func=build_func)
    build.add_argument(
        "--format",
        type=str,
        choices=("all", "epub", "html", "pdf"),
        default="all",
        help="Type of artifact to generate",
    )
    build.add_argument(
        "source_dir",
        nargs="?",
        default=".",
        type=str,
        help="Folder containing the yaml source files",
    )

    kwargs = vars(parser.parse_args())

    func = kwargs.pop("func")
    func(**kwargs)


def build_func(format: str, source_dir: str):
    print(f"build {format} {source_dir}")


def preview_func(source_dir: str):
    print(f"preview {source_dir}")


def main():
    """Entrypoint of script."""
    parse_args()


if __name__ == "__main__":
    main()
