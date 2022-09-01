"""Inject data into jinja2 template."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

from .source import Data


def inject(template_file: Path, data: Data, tex: bool = False) -> str:
    """Inject data into template file and generate string."""
    template = _get_template(template_file, tex)
    return template.render(**data)


def _jinja2_env(searchpath: str, tex: bool = False) -> Environment:
    """Create jinja2 env that can find templates under template/OEBPS."""
    loader = FileSystemLoader(searchpath=searchpath)

    if tex:  # For tex files use (( )) to delimit variables to allow passing into tex
        # macros
        return Environment(
            loader=loader, variable_start_string="((", variable_end_string="))"
        )
    else:
        return Environment(loader=loader)


def _get_template(template_file: Path, tex: bool = False) -> Template:
    """Read template from html template file."""
    env = _jinja2_env(str(template_file.parent), tex)

    return env.get_template(template_file.name)
