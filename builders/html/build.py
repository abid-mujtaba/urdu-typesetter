"""Build HTML using the template and source data (yaml)."""

from argparse import ArgumentParser
from typing import Dict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template
from ruyaml import YAML


def get_source():
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


def jinja2_env() -> Environment:
    """Create jinja2 env that can find templates under template/OEBPS."""
    loader = FileSystemLoader(searchpath="template")
    return Environment(loader=loader)


def get_template() -> Template:
    """Read template from html template file."""
    env = jinja2_env()

    return env.get_template("story.html.template")


def get_data(source: str):
    """Get data from story.yaml and validate it."""
    yaml = YAML(typ="safe")
    source_file = Path.cwd().parent.parent / "data" / source / "story.yaml"

    with source_file.open(encoding="UTF-8") as fin:
        data = yaml.load(fin)

    # Validate data
    assert "title" in data
    assert "author" in data
    assert "date" in data
    assert "description" in data
    assert "story" in data

    assert isinstance(data["story"], list)

    for line in data["story"]:
        assert isinstance(line, str)

    return data


def render_html(template: Template, data: Dict[str, str]) -> None:
    """Inject data into template and create final html file."""
    file = Path("build") / "story.html"

    file.write_text(template.render(**data))


def main():
    """Entrypoint of script."""
    template = get_template()
    source = get_source()
    data = get_data(source)

    render_html(template, data)


if __name__ == "__main__":
    main()
