"""Inject data into jinja2 template."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

from .source import Data


def inject(template_file: Path, data: Data) -> str:
    """Inject data into template file and generate string."""
    template = _get_template(template_file)
    return template.render(**data)


def _jinja2_env(searchpath: str) -> Environment:
    """Create jinja2 env that can find templates under template/OEBPS."""
    loader = FileSystemLoader(searchpath=searchpath)
    return Environment(loader=loader)


def _get_template(template_file: Path) -> Template:
    """Read template from html template file."""
    env = _jinja2_env(template_file.parent)

    return env.get_template(template_file.name)
